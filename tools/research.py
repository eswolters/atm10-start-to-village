"""Reads the MineColonies research tree from an ATM10 instance and writes the Research planner data.
usage: research.py out.js        (then: update_page.py out.js   to put it into ../index.html)
Set ATM10_INSTANCE (and MC_DATA_JAR if the vanilla jar isn't found) like for the other tools.
"""
import glob, json, os, re, sys, zipfile

INST = os.path.expanduser(os.environ.get("ATM10_INSTANCE", "~/.sklauncher/instances/all-the-mods-10-atm10"))

def vanilla_jar():
    p = os.environ.get("MC_DATA_JAR")
    if p: return os.path.expanduser(p)
    hits = glob.glob(os.path.expanduser("~/.sklauncher/libraries/net/minecraft/client/*/client-*-extra.jar"))
    if not hits: sys.exit("Set MC_DATA_JAR to a Minecraft 1.21.1 jar that contains data/minecraft")
    return hits[0]

mc_jars = glob.glob(INST + "/mods/minecolonies-*.jar")
if not mc_jars: sys.exit("No MineColonies jar found in " + INST + "/mods")
RES, BRANCH, LANG = {}, {}, {}

def read_lang(path):
    with zipfile.ZipFile(path) as z:
        for n in z.namelist():
            if re.match(r"assets/[^/]+/lang/en_us\.json$", n):
                try: LANG.update(json.loads(z.read(n)))
                except Exception: pass
read_lang(vanilla_jar()); read_lang(mc_jars[0])

def take(name, raw):
    m = re.match(r"data/minecolonies/researches/(civilian|combat|technology|unlockable)/([^/]+)\.json$", name)
    if m: RES[m.group(1) + "/" + m.group(2)] = json.loads(raw); return
    m = re.match(r"data/minecolonies/researches/(civilian|combat|technology|unlockable)\.json$", name)
    if m: BRANCH[m.group(1)] = json.loads(raw)
with zipfile.ZipFile(mc_jars[0]) as z:
    for n in z.namelist(): take(n, z.read(n)) if n.endswith(".json") and "/researches/" in n else None
kd = INST + "/kubejs/data/minecolonies/researches"           # pack overrides win
for root, _, files in os.walk(kd):
    for f in files:
        if f.endswith(".json"):
            rel = "data/minecolonies/researches/" + os.path.relpath(os.path.join(root, f), kd).replace(os.sep, "/")
            take(rel, open(os.path.join(root, f), "rb").read())

def title(s): return s.replace("_", " ").replace("/", " ").title()
def item_name(reg):
    n, p = reg.split(":")
    for k in (f"item.{n}.{p}", f"block.{n}.{p}"):
        if k in LANG: return LANG[k]
    return title(p)
def tag_name(tag):
    p = tag.split(":")[1]
    nice = {"diamond_ores": "Diamond ore", "iron_ores": "Iron ore", "gold_ores": "Gold ore", "planks": "Planks", "concrete": "Concrete"}
    return nice.get(p, title(p)) + " (any kind)"
def building_name(b):
    k = "block.minecolonies.blockhut" + b.split(":")[1]
    return LANG.get(k) or title(b.split(":")[1])

# effect text: the game's own description, with the numeric placeholders (which live in code, not data) turned into words
def effect_text(eid):
    d = LANG.get("com.minecolonies.research.effects.%s.description" % eid)
    if not d: return title(eid)
    special = {"citizencapaddition": "Raises the citizen limit", "fleeingspeedaddition": "Fleeing guards gain Swiftness", "gravedecaybonus": "Citizen graves take longer to decay",
               "healingsaturationlimitaddition": "Healing needs less saturation", "workingdayhaddition": "Longer citizen work day", "looting": "Herders gain Looting",
               "citizeninvslotsaddition": "More citizen inventory slots", "healthaddition": "Citizen HP up", "fleeingdamagemultiplier": "Guards take less damage when fleeing",
               "enhancesgatedurabilityaddition": "Gates resist raider swarms more"}
    if eid in special: return special[eid]
    if "%" not in d: return d
    d = re.sub(r"\s*-%\d*\$?s%?%?", " (reduction)", d)
    d = re.sub(r"\s*\+?%\d*\$?s%?%?", " (bonus)", d)
    return re.sub(r"\s+", " ", d).strip()

rows, effects = [], {}
for key in sorted(RES):
    branch, rid = key.split("/")
    if branch == "unlockable" or RES[key].get("hidden"): continue
    r = RES[key]
    nm = LANG.get(f"com.minecolonies.research.{branch}.{rid}.name") or title(rid)
    sub = LANG.get(f"com.minecolonies.research.{branch}.{rid}.subtitle", "")
    parent = (r.get("parentResearch") or "").replace("minecolonies:", "")
    eff = []
    for e in r.get("effects", []):
        eid = e["id"].split("/")[-1]; effects[eid] = effect_text(eid); eff.append([eid, e.get("level", 1)])
    costs = [[item_name(c["item"]) if "item" in c else tag_name(c["tag"]), c["count"], c["item"] if "item" in c else "#" + c["tag"]] for c in r.get("costs", [])]
    reqs = []
    for q in r.get("requirements", []):
        t = q["type"].split(":")[1]
        if t == "building": reqs.append(["b", building_name(q["building"]), q["level"]])
        elif t == "single-building": reqs.append(["s", building_name(q["building"]), q["level"]])
        elif t == "alternate-building": reqs.append(["a", [building_name(b) for b in q["alternate-buildings"]], q["level"]])
    flags = ("x" if r.get("exclusiveChildResearch") else "") + ("n" if r.get("no-reset") else "")
    rows.append([key, branch, parent, r["researchLevel"], nm, sub, eff, costs, reqs, flags])

branches = {b: LANG.get(BRANCH[b]["branch-name"], title(b)) for b in ("civilian", "technology", "combat") if b in BRANCH}
js = "const RESEARCH = " + json.dumps(rows, ensure_ascii=False, separators=(",", ":")) + ";\n"
js += "const RESEARCH_TEXT = " + json.dumps({"effects": effects, "branches": branches}, ensure_ascii=False, separators=(",", ":")) + ";\n"
open(sys.argv[1], "w").write(js)
print(len(rows), "researches,", len(effects), "effects,", len(js), "bytes")
