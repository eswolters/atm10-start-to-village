# Reads recipe JSON from the ATM10 jars/datapacks/kubejs data and writes one JSON index (data only, nothing is executed)
import zipfile, json, os, re, sys, glob
INST = os.path.expanduser(os.environ.get("ATM10_INSTANCE", "~/.sklauncher/instances/all-the-mods-10-atm10"))
def vanilla_jar():
    """the Minecraft jar that holds the vanilla data (the "-extra" client jar in the launcher's libraries)"""
    p = os.environ.get("MC_DATA_JAR")
    if p: return os.path.expanduser(p)
    hits = glob.glob(os.path.expanduser("~/.sklauncher/libraries/net/minecraft/client/*/client-*-extra.jar"))
    if not hits: sys.exit("Set MC_DATA_JAR to a Minecraft 1.21.1 jar that contains data/minecraft")
    return hits[0]

OUT = sys.argv[1]
recipes = {}   # id -> {src, json}
tags = {}      # tag id -> {values:[...], replace:bool, src}
def add_recipe(rid, src, data):
    recipes[rid] = {"src": src, "r": data}
def handle(name, raw, src):
    m = re.match(r"data/([^/]+)/(recipes?)/(.+)\.json$", name)
    if m:
        try: add_recipe(f"{m.group(1)}:{m.group(3)}", src, json.loads(raw))
        except Exception: pass
        return
    m = re.match(r"data/([^/]+)/tags?/(items?)/(.+)\.json$", name)
    if m:
        try:
            d = json.loads(raw); tid = f"{m.group(1)}:{m.group(3)}"
            t = tags.setdefault(tid, {"values": [], "src": []})
            if d.get("replace"): t["values"] = []
            t["values"] += d.get("values", []); t["src"].append(src)
        except Exception: pass
def read_zip(path, src):
    try:
        with zipfile.ZipFile(path) as z:
            for n in z.namelist():
                if n.startswith("data/") and n.endswith(".json") and ("/recipe" in n or "/tags/item" in n or "/tags/items" in n):
                    handle(n, z.read(n), src)
                elif n.endswith(".jar") and n.startswith("META-INF/jarjar/"):
                    pass
    except Exception as e:
        print("skip", path, e, file=sys.stderr)
# vanilla first (lowest priority), then mods, then datapack zips, then kubejs data (highest)
read_zip(vanilla_jar(), "vanilla")
for j in sorted(glob.glob(INST + "/mods/*.jar")): read_zip(j, os.path.basename(j))
for z in glob.glob(INST + "/datapacks/*.zip"): read_zip(z, "datapack:" + os.path.basename(z))
kd = INST + "/kubejs/data"
for root, _, files in os.walk(kd):
    for f in files:
        if f.endswith(".json"):
            full = os.path.join(root, f); rel = "data/" + os.path.relpath(full, kd).replace(os.sep, "/")
            handle(rel, open(full, "rb").read(), "kubejs")
json.dump({"recipes": recipes, "tags": tags}, open(OUT, "w"))
print(len(recipes), "recipes", len(tags), "tags")
