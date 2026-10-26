import json, sys, re
D = json.load(open(sys.argv[1]))
R = D["recipes"]
def ing_str(i):
    if isinstance(i, list): return "|".join(ing_str(x) for x in i)
    if isinstance(i, dict):
        if "item" in i: s = i["item"]
        elif "tag" in i: s = "#" + i["tag"]
        elif "ingredient" in i: s = ing_str(i["ingredient"])
        else: s = json.dumps(i)
        c = i.get("count") or i.get("amount")
        return s + (f"×{c}" if c else "")
    return str(i)
def res_str(r):
    if r is None: return "?"
    if isinstance(r, str): return r
    if isinstance(r, list): return ", ".join(res_str(x) for x in r)
    if "id" in r: return r["id"] + (f"×{r['count']}" if r.get("count", 1) != 1 else "")
    if "item" in r: return r["item"] + (f"×{r['count']}" if r.get("count", 1) != 1 else "")
    return json.dumps(r)
def out_of(r):
    for k in ("result", "output", "results", "outputs", "itemOutput", "item_output"):
        if k in r: return r[k]
    return None
def outs_ids(r):
    o = out_of(r); ids = []
    def walk(x):
        if isinstance(x, str): ids.append(x)
        elif isinstance(x, list): [walk(y) for y in x]
        elif isinstance(x, dict):
            for k in ("id", "item"):
                if k in x and isinstance(x[k], str): ids.append(x[k])
            for k in ("item_output", "itemOutput", "output", "result"):
                if k in x: walk(x[k])
    walk(o)
    return ids
def describe(rid, e):
    r = e["r"]; t = r.get("type", "?")
    s = f"[{e['src'][:28]}] {rid} <{t}> -> {res_str(out_of(r))}\n      "
    if t in ("minecraft:crafting_shaped",):
        key = {k: ing_str(v) for k, v in r.get("key", {}).items()}
        rows = r.get("pattern", [])
        counts = {}
        for ch in "".join(rows):
            if ch != " ": counts[ch] = counts.get(ch, 0) + 1
        s += "shaped: " + ", ".join(f"{counts[k]}×{key.get(k,'?')}" for k in counts) + f"  pattern={rows}"
    elif t in ("minecraft:crafting_shapeless",):
        s += "shapeless: " + ", ".join(ing_str(i) for i in r.get("ingredients", []))
    elif t.startswith("minecraft:") and "ingredient" in r:
        s += f"{t.split(':')[1]}: {ing_str(r['ingredient'])}"
    else:
        keep = {k: v for k, v in r.items() if k not in ("type", "neoforge:conditions", "conditions", "category", "group")}
        s += json.dumps(keep)[:420]
    if r.get("neoforge:conditions") or r.get("conditions"): s += "  COND=" + json.dumps(r.get("neoforge:conditions") or r.get("conditions"))[:120]
    return s
BAD = ("salvag", "uncraft", "decompress", "compress", "sawmill", "sawing", "crushing", "cutting", "milling", "pressing", "splash", "washing", "haunting", "deploying", "mixing", "filling", "emptying", "sequenced", "item_application", "kubejs_call", "milling")
def rel(rid, e, out):
    ns = out.split(":")[0]
    ty = e["r"].get("type", "")
    if any(b in ty or b in rid for b in ("salvag", "uncraft", "decompress", "compress", "kubejs_call:recipes.modern", "kubejs_call:recipes.modular", "storage_block", "ingot_to_block", "block_to")): return False
    if e["src"].startswith(("script", "kubejs")): return True
    if rid.split(":")[0] != ns: return False
    return True
if __name__ == "__main__":
    for want in sys.argv[2:]:
        print("=====", want)
        n = 0
        for rid, e in R.items():
            if want in outs_ids(e["r"]) and rel(rid, e, want):
                print(describe(rid, e)); n += 1
        if not n: print("   (no recipe)")
