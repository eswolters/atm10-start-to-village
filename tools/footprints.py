"""Reads the size of every MineColonies building blueprint (all styles) from an ATM10 instance and writes the town planner's footprint data.
usage: footprints.py out.js        (then: update_page.py out.js   to put it into ../index.html)
Blueprints are gzip-compressed NBT files; only the three size fields in the header are read, nothing is executed.
Set ATM10_INSTANCE like for the other tools.
"""
import glob, gzip, json, os, re, struct, sys, zipfile

INST = os.path.expanduser(os.environ.get("ATM10_INSTANCE", "~/.sklauncher/instances/all-the-mods-10-atm10"))

def sizes(data):
    """walk the top-level tags of a blueprint until size_x, size_y and size_z are known"""
    pos = 0
    def u(fmt):
        nonlocal pos
        v = struct.unpack_from(">" + fmt, data, pos); pos += struct.calcsize(">" + fmt); return v[0]
    def string():
        nonlocal pos
        n = u("H"); s = data[pos:pos + n].decode("utf-8", "replace"); pos += n; return s
    def skip(t):
        nonlocal pos
        fixed = {1: 1, 2: 2, 3: 4, 4: 8, 5: 4, 6: 8}
        if t in fixed: pos += fixed[t]
        elif t == 7: n = u("i"); pos += n
        elif t == 8: string()
        elif t == 9:
            it = u("b"); n = u("i")
            for _ in range(n): skip(it)
        elif t == 10:
            while True:
                tt = u("b")
                if tt == 0: return
                string(); skip(tt)
        elif t == 11: n = u("i"); pos += 4 * n
        elif t == 12: n = u("i"); pos += 8 * n
        else: raise ValueError(t)
    if u("b") != 10: raise ValueError("not a compound")
    string()
    out = {}
    while len(out) < 3:
        t = u("b")
        if t == 0: break
        k = string()
        if k in ("size_x", "size_y", "size_z"): out[k] = u({1: "b", 2: "h", 3: "i"}[t]); continue
        skip(t)
    return out

AIR = {"minecraft:air", "minecraft:cave_air", "minecraft:void_air"}
MASK_STYLES = ["medievalspruce", "medievaloak", "medievalbirch", "medievaldarkoak", "fortress", "shire", "nordic", "caledonia", "colonial", "original"]

def blueprint(data):
    """size, the block grid and the palette names (needed for the real outline of a building)"""
    pos = 0
    def u(fmt):
        nonlocal pos
        v = struct.unpack_from(">" + fmt, data, pos); pos += struct.calcsize(">" + fmt); return v[0]
    def string():
        nonlocal pos
        n = u("H"); s = data[pos:pos + n].decode("utf-8", "replace"); pos += n; return s
    def skip(t):
        nonlocal pos
        fixed = {1: 1, 2: 2, 3: 4, 4: 8, 5: 4, 6: 8}
        if t in fixed: pos += fixed[t]
        elif t == 7: n = u("i"); pos += n
        elif t == 8: string()
        elif t == 9:
            it = u("b"); n = u("i")
            for _ in range(n): skip(it)
        elif t == 10:
            while True:
                tt = u("b")
                if tt == 0: return
                string(); skip(tt)
        elif t == 11: n = u("i"); pos += 4 * n
        elif t == 12: n = u("i"); pos += 8 * n
        else: raise ValueError(t)
    u("b"); string()
    out = {}
    while True:
        t = u("b")
        if t == 0: break
        k = string()
        if k in ("size_x", "size_y", "size_z"): out[k] = u({1: "b", 2: "h", 3: "i"}[t])
        elif k == "blocks":
            n = u("i"); out["blocks"] = struct.unpack_from(">%di" % n, data, pos); pos += 4 * n
        elif k == "palette":
            u("b"); n = u("i"); names = []
            for _ in range(n):
                name = None
                while True:
                    tt = u("b")
                    if tt == 0: break
                    kk = string()
                    if kk == "Name" and tt == 8: name = string()
                    else: skip(tt)
                names.append(name)
            out["palette"] = names
        else: skip(t)
    return out

def outline(bp):
    """which columns (x, z) have any real block at any height: two shorts are packed in each int, x runs fastest, then z, then y"""
    X, Y, Z = bp["size_x"], bp["size_y"], bp["size_z"]
    shorts = [0] * (X * Y * Z)
    for i, v in enumerate(bp["blocks"]):
        shorts[2 * i] = v & 0xFFFF
        if 2 * i + 1 < len(shorts): shorts[2 * i + 1] = (v >> 16) & 0xFFFF
    ignore = {i for i, n in enumerate(bp["palette"]) if n in AIR or (n and "substitution" in n)}
    grid = [[0] * X for _ in range(Z)]
    for y in range(Y):
        for z in range(Z):
            base = (y * Z + z) * X
            for x in range(X):
                if shorts[base + x] not in ignore: grid[z][x] = 1
    return grid

def pack_mask(grid):
    h, w = len(grid), len(grid[0]); bits = [c for row in grid for c in row]
    bits += [0] * (-len(bits) % 8)
    b = bytes(int("".join(map(str, bits[i:i + 8])), 2) for i in range(0, len(bits), 8))
    return f"{w}:{h}:" + base64.b64encode(b).decode()

import base64
BEST, MASK = {}, {}
FOOT, STYLES = {}, {}
for jar in sorted(glob.glob(INST + "/mods/*.jar")):
    try: z = zipfile.ZipFile(jar)
    except Exception: continue
    names = z.namelist()
    if not any(n.startswith("blueprints/") and n.endswith(".blueprint") for n in names): continue
    for n in names:
        m = re.match(r"blueprints/([^/]+)/([^/]+)/(.+)\.blueprint$", n)
        if m:
            pack, style, rest = m.groups()
            base = rest.split("/")[-1]
            mm = re.match(r"^(.*?)(\d+)$", base)
            if not mm: continue
            b, lvl = mm.group(1), int(mm.group(2))
            if rest.split("/")[0] in ("walls", "infrastructure"): continue   # wall pieces and mine shafts aren't buildings you place
            if not 1 <= lvl <= 5: continue
            try:
                s = sizes(gzip.decompress(z.read(n)))
                if len(s) < 3: raise ValueError("no size")
            except Exception as e: print("skip", n, e, file=sys.stderr); continue
            lv = FOOT.setdefault(style, {}).setdefault(b, [None] * 5)
            lv[lvl - 1] = [s["size_x"], s["size_z"]]
            if style in MASK_STYLES and lvl >= BEST.get((style, b), (0,))[0]: BEST[(style, b)] = (lvl, jar, n)
        m = re.match(r"blueprints/([^/]+)/([^/]+)/pack\.json$", n)
        if m:
            try:
                d = json.loads(z.read(n)); STYLES[m.group(2)] = d.get("name", m.group(2)).replace("_", " ")
            except Exception: pass
for (style, b), (lvl, jar, n) in BEST.items():
    try:
        with zipfile.ZipFile(jar) as zz: g = outline(blueprint(gzip.decompress(zz.read(n))))
    except Exception as e: print("outline skipped", n, e, file=sys.stderr); continue
    if sum(map(sum, g)) >= 0.97 * len(g) * len(g[0]): continue      # practically a full rectangle: draw the box
    MASK.setdefault(style, {})[b] = pack_mask(g)
styles = [[k, STYLES.get(k, k)] for k in sorted(FOOT, key=lambda s: STYLES.get(s, s).lower()) if len(FOOT[k]) >= 15]
FOOT = {k: FOOT[k] for k, _ in styles}
# compact form: [x, z, n] when levels 1..n all have the same size, otherwise a list of [x, z] per level (null where a level is missing)
for st in FOOT.values():
    for b, lv in list(st.items()):
        n = max((i + 1 for i, v in enumerate(lv) if v), default=0)
        if n and all(lv[i] == lv[0] for i in range(n)): st[b] = lv[0] + [n]
        else: st[b] = lv[:n]
js = "const FOOT_STYLES = " + json.dumps(styles, ensure_ascii=False, separators=(",", ":")) + ";\n"
js += "const FOOT = " + json.dumps(FOOT, ensure_ascii=False, separators=(",", ":")) + ";\n"
js += "const FOOT_MASK = " + json.dumps(MASK, ensure_ascii=False, separators=(",", ":")) + ";\n"
open(sys.argv[1], "w").write(js)
print(len(styles), "styles,", sum(len(v) for v in FOOT.values()), "building types,", len(js), "bytes")
