import json, re, sys
idx = json.load(open(sys.argv[1])); calls = json.load(open(sys.argv[2]))["calls"]; OUT = sys.argv[3]
R = {k: {"src": v["src"], "r": v["r"]} for k, v in idx["recipes"].items()}
tags = idx["tags"]
unsupported = set(); removed_n = 0; added_n = 0
def to_ing(x):
    if isinstance(x, dict):
        if "item" in x or "tag" in x or "fluid" in x: return x
        if "id" in x: return {"item": x["id"]}
        return x
    if isinstance(x, list): return [to_ing(i) for i in x]
    if isinstance(x, str):
        m = re.match(r"^(\d+)x\s+(.*)$", x)
        if m: return {**to_ing(m.group(2)), "count": int(m.group(1))}
        return {"tag": x[1:]} if x.startswith("#") else {"item": x}
    return x
def to_res(x):
    if isinstance(x, dict) and "id" in x: return x
    if isinstance(x, dict) and "item" in x: return {"id": x["item"], "count": x.get("count", 1)}
    if isinstance(x, str):
        m = re.match(r"^(\d+)x\s+(.*)$", x)
        if m: return {"id": m.group(2), "count": int(m.group(1))}
        return {"id": x}
    return x
def outs(r):
    ids = []
    def walk(x):
        if isinstance(x, str): ids.append(x)
        elif isinstance(x, list): [walk(y) for y in x]
        elif isinstance(x, dict):
            for k in ("id", "item"):
                if isinstance(x.get(k), str): ids.append(x[k])
            for k in ("item_output", "itemOutput", "output", "result", "results"):
                if k in x: walk(x[k])
    for k in ("result", "output", "results", "outputs", "itemOutput", "item_output"):
        if k in r: walk(r[k])
    return ids
def match_str(pat, s):
    if isinstance(pat, dict) and "$re" in pat: return re.search(pat["$re"], s) is not None
    return pat == s
def matches(f, rid, e):
    r = e["r"]
    if isinstance(f, str):
        if f.startswith("@"): return rid.split(":")[0] == f[1:]
        return rid == f or f in outs(r)
    if not isinstance(f, dict): return False
    ok = True
    for k, v in f.items():
        if k == "id": ok &= match_str(v, rid)
        elif k == "mod": ok &= rid.split(":")[0] == v
        elif k == "type": ok &= match_str(v, r.get("type", ""))
        elif k == "output":
            o = outs(r)
            if isinstance(v, str) and v.startswith("#"): ok &= any(tag_has(v[1:], i) for i in o)
            elif isinstance(v, str) and v.startswith("@"): ok &= any(i.split(":")[0] == v[1:] for i in o)
            else: ok &= any(match_str(v, i) for i in o)
        elif k == "input":
            s = json.dumps(r); vv = v[1:] if isinstance(v, str) and v.startswith("#") else v
            ok &= (isinstance(vv, str) and vv in s)
        elif k == "not": ok &= not matches(v, rid, e)
        elif k == "or": ok &= any(matches(x, rid, e) for x in v)
        elif k == "and": ok &= all(matches(x, rid, e) for x in v)
        else: unsupported.add(k); ok = False
    return ok
def tag_has(tag, item, seen=None):
    t = tags.get(tag)
    if not t: return False
    for v in t["values"]:
        v = v if isinstance(v, str) else v.get("id", "")
        if v == item: return True
        if v.startswith("#") and tag_has(v[1:], item): return True
    return False
n = 0
for c in calls:
    m, a = c["m"], c["args"]
    if m == "remove" and a:
        dead = [rid for rid, e in R.items() if matches(a[0], rid, e)]
        for rid in dead: del R[rid]
        removed_n += len(dead)
    elif m in ("shaped", "shapeless") and len(a) >= 2:
        rid = c.get("id") or f"script:{n}"; n += 1
        res = to_res(a[0])
        if m == "shaped":
            r = {"type": "minecraft:crafting_shaped", "pattern": a[1], "key": {k: to_ing(v) for k, v in a[2].items()}, "result": res}
        else:
            r = {"type": "minecraft:crafting_shapeless", "ingredients": [to_ing(i) for i in a[1]], "result": res}
        R[rid] = {"src": "script:" + c["file"], "r": r}; added_n += 1
    elif m in ("smelting", "blasting", "smoking", "campfireCooking") and len(a) >= 2:
        rid = c.get("id") or f"script:{n}"; n += 1
        R[rid] = {"src": "script:" + c["file"], "r": {"type": "minecraft:" + m if m != "smelting" else "minecraft:smelting", "ingredient": to_ing(a[1]), "result": to_res(a[0])}}; added_n += 1
    elif m == "custom" and a and isinstance(a[0], dict):
        rid = c.get("id") or f"script:{n}"; n += 1
        R[rid] = {"src": "script:" + c["file"], "r": a[0]}; added_n += 1
    elif m == "replaceInput" and len(a) >= 3:
        frm, to = a[1], a[2]
        for rid, e in R.items():
            if matches(a[0], rid, e):
                s = json.dumps(e["r"])
                f_item = json.dumps({"item": frm})[1:-1]; f_tag = json.dumps({"tag": frm[1:]})[1:-1] if isinstance(frm, str) and frm.startswith("#") else None
                new = {"tag": to[1:]} if isinstance(to, str) and to.startswith("#") else {"item": to}
                newj = json.dumps(new)[1:-1]
                for old in (f_item, f_tag):
                    if old: s = s.replace(old, newj)
                e["r"] = json.loads(s); e["src"] += "+replaced"
    elif m.startswith("recipes."):
        rid = c.get("id") or f"script:{n}"; n += 1
        R[rid] = {"src": "script:" + c["file"], "r": {"type": "kubejs_call:" + m, "args": a}}; added_n += 1
json.dump({"recipes": R, "tags": tags}, open(OUT, "w"))
print("removed", removed_n, "added", added_n, "final", len(R), "unsupported filter keys:", sorted(unsupported))
