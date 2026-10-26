"""Builds the Materials database from the real ATM10 recipes.
usage: gen.py final.json want.py out.json
want.py defines: WANT (list of (slug, registry_id, group)), MAP (ingredient key -> slug), LEAF (slug -> note), ALLOW (namespaces to recurse into), PICK (slug -> recipe id)
"""
import json, re, sys, zipfile, glob, os

IDX = json.load(open(sys.argv[1]))
R = IDX["recipes"]; TAGS = IDX["tags"]
ns = {}
exec(open(sys.argv[2]).read(), ns)
WANT, MAP, LEAF, ALLOW, PICK = ns["WANT"], ns["MAP"], ns["LEAF"], ns["ALLOW"], ns.get("PICK", {})
SKIP_OUT = ns.get("SKIP_OUT", set())

# ---- names from the language files of the installed mods
INST = os.path.expanduser(os.environ.get("ATM10_INSTANCE", "~/.sklauncher/instances/all-the-mods-10-atm10"))
def vanilla_jar():
    """the Minecraft jar that holds the vanilla data (the "-extra" client jar in the launcher's libraries)"""
    p = os.environ.get("MC_DATA_JAR")
    if p: return os.path.expanduser(p)
    hits = glob.glob(os.path.expanduser("~/.sklauncher/libraries/net/minecraft/client/*/client-*-extra.jar"))
    if not hits: sys.exit("Set MC_DATA_JAR to a Minecraft 1.21.1 jar that contains data/minecraft")
    return hits[0]

LANG = {}
def load_lang(path):
    try:
        with zipfile.ZipFile(path) as z:
            for n in z.namelist():
                if re.match(r"assets/[^/]+/lang/en_us\.json$", n):
                    try: LANG.update(json.loads(z.read(n)))
                    except Exception: pass
    except Exception: pass
load_lang(vanilla_jar())
for j in glob.glob(INST + "/mods/*.jar"): load_lang(j)
def name_of(reg):
    n, p = reg.split(":")
    for k in (f"item.{n}.{p}", f"block.{n}.{p}"):
        if k in LANG: return LANG[k]
    return p.replace("_", " ").title()

# ---- recipe helpers
def out_entries(r):
    res = []
    def walk(x):
        if isinstance(x, str): res.append((x, 1))
        elif isinstance(x, list): [walk(y) for y in x]
        elif isinstance(x, dict):
            i = x.get("id") or x.get("item")
            if isinstance(i, str): res.append((i, x.get("count", 1)))
            else:
                for k in ("item_output", "itemOutput", "output", "result", "results"):
                    if k in x: walk(x[k])
    for k in ("result", "output", "results", "outputs", "itemOutput", "item_output"):
        if k in r: walk(r[k])
    return res
def out_count(r, reg):
    for i, c in out_entries(r):
        if i == reg: return c if isinstance(c, int) else 1
    return 1

def flat(i):
    """an ingredient value -> list of {item|tag, count}"""
    if isinstance(i, list):
        return [x for y in i for x in flat(y)]
    if isinstance(i, dict):
        if "ingredient" in i and isinstance(i["ingredient"], (dict, list)):
            sub = flat(i["ingredient"]); c = i.get("amount") or i.get("count")
            if c and len(sub) == 1: sub[0] = {**sub[0], "count": c}
            return sub
        if i.get("type", "").endswith("woodless"): return [{"tag": "minecraft:planks"}]
        if "item" in i or "tag" in i: return [i]
        if "id" in i and isinstance(i["id"], str): return [{"item": i["id"], "count": i.get("count", 1)}]
        if "fluid" in i or "fluid_tag" in i: return [{"fluid": i.get("fluid") or i.get("fluid_tag"), "count": i.get("amount", 1)}]
        if "chemical" in i or "gas" in i or "infuse_type" in i: return [{"chemical": i.get("chemical") or i.get("gas") or i.get("infuse_type"), "count": i.get("amount", 1)}]
    if isinstance(i, str): return [{"tag": i[1:]} if i.startswith("#") else {"item": i}]
    return []

def slots(r):
    """list of alternatives-lists, one per required slot, each with count: [[{ing..}, ...alts], count]"""
    t = r.get("type", "")
    S = []
    if "pattern" in r and "key" in r:
        cnt = {}
        for ch in "".join(r.get("pattern", [])):
            if ch != " ": cnt[ch] = cnt.get(ch, 0) + 1
        for ch, n in cnt.items():
            if ch in r.get("key", {}): S.append((flat(r["key"][ch]), n))
    elif t == "minecraft:crafting_shapeless":
        for i in r.get("ingredients", []): S.append((flat(i), 1))
    elif t in ("minecraft:smelting", "minecraft:blasting", "minecraft:smoking", "minecraft:campfire_cooking", "minecraft:stonecutting"):
        S.append((flat(r.get("ingredient")), 1))
    elif t.startswith("ae2:inscriber"):
        for k in ("top", "middle", "bottom"):
            if k in r.get("ingredients", {}): S.append((flat(r["ingredients"][k]), 1))
    elif t.startswith("ae2:"):
        v = r.get("ingredients") or r.get("ingredient")
        if isinstance(v, dict) and not ("item" in v or "tag" in v): v = list(v.values())
        for i in (v if isinstance(v, list) else [v]): S.append((flat(i), 1))
    elif t == "powah:energizing":
        for i in r.get("ingredients", []): S.append((flat(i), 1))
    elif t.startswith("mekanism:"):
        for k in ("item_input", "itemInput", "input", "main_input", "extra_input", "left_input", "right_input", "chemical_input", "chemicalInput", "infusion_input"):
            if k in r:
                f = flat(r[k]); c = (f[0].get("count") or f[0].get("amount") or 1) if f else 1
                if k in ("chemical_input", "chemicalInput", "infusion_input") and f and f[0].get("tag", "").startswith("mekanism:"): c = max(1, -(-c // 10))
                S.append((f, c))
    else:
        for k in ("ingredients", "ingredient", "input", "inputs"):
            if k in r:
                v = r[k]
                for i in (v if isinstance(v, list) else [v]): S.append((flat(i), 1))
                break
    return S

MACH = {
    "minecraft:crafting_shaped": "crafting table", "minecraft:crafting_shapeless": "crafting table",
    "minecraft:smelting": "furnace (needs fuel)", "minecraft:blasting": "blast furnace", "minecraft:smoking": "smoker",
    "create:pressing": "Mechanical Press", "create:mixing": "Mixer + Basin", "create:item_application": "item application (hold the item and right-click the block)",
    "create:mechanical_crafting": "Mechanical Crafter array", "create:cutting": "Saw", "create:deploying": "Deployer",
    "ae2:inscriber": "Inscriber", "ae2:charger": "Charger", "ae2:transform": "thrown into water",
    "powah:energizing": "Energizing Orb", "mekanism:metallurgic_infusing": "Metallurgic Infuser", "mekanism:enriching": "Enrichment Chamber",
    "mekanism:crushing": "Crusher", "mekanism:combining": "Combiner", "mekanism:compressing": "Osmium Compressor", "mekanism:injecting": "Chemical Injection Chamber",
    "mekanism:purifying": "Purification Chamber", "mekanism:smelting": "Energized Smelter", "mekanism:pigment_mixing": "Pigment Mixer",
}
def machine(r):
    t = r.get("type", "")
    if "pattern" in r and "key" in r and t != "create:mechanical_crafting": return "crafting table"
    m = MACH.get(t, t)
    if t == "create:mixing" and r.get("heat_requirement"): m += f" ({r['heat_requirement']})"
    return m

TYPE_RANK = {"minecraft:crafting_shaped": 0, "minecraft:crafting_shapeless": 0, "minecraft:smelting": 1, "create:item_application": 2, "minecraft:blasting": 4, "minecraft:smoking": 5, "minecraft:stonecutting": 6}
def hard_penalty(r, reg):
    """compressing/decompressing recipes (one ingredient: a block or nuggets of the same stuff) and recipes with an ingredient we can't read are a last resort"""
    out_p = reg.split(":")[1]
    sl = slots(r)
    if not sl: return 1
    keys = set()
    for alts, _ in sl:
        if not alts: return 1
        a0 = alts[0]; keys.add(a0.get("item") or ("#" + a0.get("tag", "")))
        for a in alts:
            p = (a.get("item") or "").split(":")[-1]
            if p.startswith("cable_") and not out_p.startswith("cable_"): return 1
    if out_p.startswith("dust_") and all("ingot" in k or "plate" in k for k in keys): return 1  # recycling an ingot back into dust
    if all(re.search(r"block|nugget", k.split(":")[-1]) for k in keys) and not re.search(r"block|nugget", out_p): return 1
    return 0
def score(rid, e, reg):
    r = e["r"]; t = r.get("type", "")
    rank = TYPE_RANK.get(t, 3)
    soft = 1 if re.search(r"decon|_2$|dye|_alt\\b|_alt$|conversion|upgrade|repair|decompress|compress|uncraft|salvag|recycl|dupl|copy|clean|color|paint", rid) else 0
    raw_pref = 0 if any((a.get("item") or "").split(":")[-1].startswith("raw_") or "raw_materials" in (a.get("tag") or "") for alts, _ in slots(r) for a in alts) else 1
    return (hard_penalty(r, reg), soft, raw_pref, rank, 0 if rid.split(":")[1] == reg.split(":")[1] else 1, sum(n for _, n in slots(r)), len(rid), rid)

def candidates(reg):
    n = reg.split(":")[0]
    out = []
    for rid, e in R.items():
        r = e["r"]
        t = r.get("type", "")
        if "sequenced_assembly" in t: continue  # multi-step crafts with by-products: not supported, shown as "check JEI"
        if t.startswith("kubejs_call") or "salvaging" in t or "modern_industrialization" in t or "modular_machinery" in t: continue
        if not any(i == reg for i, _ in out_entries(r)): continue
        if not (e["src"].startswith(("script", "kubejs")) or rid.split(":")[0] == n or rid.split(":")[0] == "minecraft"): continue
        if reg in [x.get("item") for s, _ in slots(r) for x in s]: continue  # self-referencing
        if r.get("neoforge:conditions") or r.get("conditions"):
            c = json.dumps(r.get("neoforge:conditions") or r.get("conditions"))
            if "not" in c: pass
        out.append((rid, e))
    return sorted(out, key=lambda x: score(x[0], x[1], reg))

# ---- ingredient -> slug
def tag_members(tag, seen=None):
    seen = seen or set()
    if tag in seen: return []
    seen.add(tag)
    t = TAGS.get(tag)
    res = []
    if not t: return res
    for v in t["values"]:
        v = v if isinstance(v, str) else v.get("id", "")
        if v.startswith("#"): res += tag_members(v[1:], seen)
        else: res.append(v)
    return res
def wood_generic(key):
    if re.match(r"minecraft:(oak|spruce|birch|jungle|acacia|dark_oak|mangrove|cherry|bamboo|crimson|warped)_planks$", key): return "planks"
    if re.match(r"minecraft:(oak|spruce|birch|jungle|acacia|dark_oak|mangrove|cherry|crimson|warped)_(log|wood|stem|hyphae)$", key): return "log"
    if re.match(r"minecraft:[a-z_]+_wool$", key): return "wool"
    return None
def slug_for(ing):
    if "fluid" in ing: return "fluid:" + str(ing["fluid"])
    if "chemical" in ing: return "chem:" + str(ing["chemical"])
    key = ing.get("item") or ("#" + ing["tag"])
    if key in MAP: return MAP[key]
    g = wood_generic(key)
    if g: return g
    return None

NAMES = {}; ITEMS = {}; UNRES = {}; ORDER = []; PICKED = {}
def auto_slug(reg):
    n, p = reg.split(":")
    s = p.replace("/", "_")
    if s in LEAF: return s
    taken = [k for k, v in NAMES.items() if v != reg and k == s]
    if taken or s in LEAF or s in MAP.values(): s = n + "_" + s
    return s
REG2SLUG = {}
for slug, reg, grp in WANT: REG2SLUG[reg] = slug; NAMES[slug] = reg
for k, v in MAP.items():
    if not k.startswith("#") and ":" in k: REG2SLUG.setdefault(k, v)

def slug_of_reg(reg):
    if reg in REG2SLUG: return REG2SLUG[reg]
    s = auto_slug(reg); REG2SLUG[reg] = s; NAMES[s] = reg; return s

WANTSET = {s for s, _, _ in WANT}
queue = [(slug, reg, grp) for slug, reg, grp in WANT]
done = set()
def resolve_ing(alts, parent_grp):
    """pick the best option of an ingredient slot -> slug (queues new items)"""
    # first: any option that maps explicitly
    for a in alts:
        s = slug_for(a)
        if s: return s, a
    # second: tag -> use first member that has a recipe in an allowed namespace
    for a in alts:
        if "tag" in a:
            for m in tag_members(a["tag"]):
                if m in REG2SLUG: return REG2SLUG[m], a
    for a in alts:
        if "item" in a:
            reg = a["item"]
            return slug_of_reg(reg), a
    for a in alts:
        if "tag" in a:
            ms = tag_members(a["tag"])
            if ms: return slug_of_reg(ms[0]), a
            return "tag:" + a["tag"], a
    return "?", alts[0] if alts else {}

while queue:
    slug, reg, grp = queue.pop(0)
    if slug in done: continue
    done.add(slug)
    if slug in LEAF: continue
    cands = candidates(reg)
    if slug in PICK:
        cands = [c for c in cands if c[0] == PICK[slug]] or cands
    if not cands:
        UNRES[slug] = reg; continue
    rid, e = cands[0]; r = e["r"]
    ins = {}; also = []; tools = []
    for alts, n in slots(r):
        s, a = resolve_ing(alts, grp)
        if r.get("type", "").startswith("ae2:inscriber") and any((a.get("item") or "").endswith("_press") for a in alts):
            tools.append(name_of(alts[0]["item"])); continue
        if s.startswith(("fluid:", "chem:")): also.append(s.split(":", 1)[1] + (f" ×{n}" if n > 1 else "")); continue
        ins[s] = ins.get(s, 0) + n * (1 if "count" not in a else 1)
        if s.startswith(("tag:", "fluid:", "chem:", "?")): continue
        reg2 = NAMES.get(s)
        if s not in done and s not in LEAF and not any(q[0] == s for q in queue):
            if reg2 is None:
                item = a.get("item") or (tag_members(a["tag"])[0] if a.get("tag") and tag_members(a["tag"]) else None)
                if item: reg2 = item; NAMES[s] = item
            if reg2 and reg2.split(":")[0] in ALLOW: queue.append((s, reg2, grp))
            elif reg2: UNRES.setdefault(s, reg2)
    ITEMS[slug] = {"reg": reg, "n": name_of(reg), "out": out_count(r, reg), "in": [[k, v] for k, v in ins.items()], "at": machine(r), "grp": grp, "rid": rid,
                   "atm": e["src"].startswith(("script", "kubejs")), "alts": len(cands) - 1, "also": also, "tools": tools, "want": slug in WANTSET}
    PICKED[slug] = [c[0] for c in cands[:4]]

def cycles():
    state = {}; found = []
    def dfs(s, path):
        state[s] = 1
        for k, _ in ITEMS.get(s, {"in": []})["in"]:
            if state.get(k) == 1: found.append(path + [s, k])
            elif k not in state and k in ITEMS: dfs(k, path + [s])
        state[s] = 2
    for s in list(ITEMS): 
        if s not in state: dfs(s, [])
    return found
CYC = cycles()
print("cycles:", [" > ".join(c[-4:]) for c in CYC][:10])
json.dump({"items": ITEMS, "unresolved": UNRES, "picked": PICKED, "names": {k: name_of(v) for k, v in NAMES.items() if ":" in v}}, open(sys.argv[3], "w"), indent=1)
print(len(ITEMS), "items;", len(UNRES), "unresolved")
