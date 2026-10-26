import zipfile, glob, json, os, re, sys
INST = os.path.expanduser(os.environ.get("ATM10_INSTANCE", "~/.sklauncher/instances/all-the-mods-10-atm10"))
def vanilla_jar():
    """the Minecraft jar that holds the vanilla data (the "-extra" client jar in the launcher's libraries)"""
    p = os.environ.get("MC_DATA_JAR")
    if p: return os.path.expanduser(p)
    hits = glob.glob(os.path.expanduser("~/.sklauncher/libraries/net/minecraft/client/*/client-*-extra.jar"))
    if not hits: sys.exit("Set MC_DATA_JAR to a Minecraft 1.21.1 jar that contains data/minecraft")
    return hits[0]

PF, CF, BM = {}, {}, {}
def handle(n, raw, src):
    m = re.match(r"data/([^/]+)/worldgen/(placed_feature|configured_feature)/(.+)\.json$", n)
    if m:
        try: d = json.loads(raw)
        except Exception: return
        (PF if m.group(2) == "placed_feature" else CF)[f"{m.group(1)}:{m.group(3)}"] = (src, d); return
    m = re.match(r"data/([^/]+)/(?:neoforge|forge)/biome_modifier/(.+)\.json$", n)
    if m:
        try: BM[f"{m.group(1)}:{m.group(2)}"] = (src, json.loads(raw))
        except Exception: pass
for j in [vanilla_jar()] + sorted(glob.glob(INST + "/mods/*.jar")):
    try:
        with zipfile.ZipFile(j) as z:
            for n in z.namelist():
                if "/worldgen/" in n and n.endswith(".json") and ("placed_feature" in n or "configured_feature" in n): handle(n, z.read(n), os.path.basename(j))
                elif "biome_modifier" in n and n.endswith(".json"): handle(n, z.read(n), os.path.basename(j))
    except Exception: pass
kd = INST + "/kubejs/data"
for root, _, files in os.walk(kd):
    for f in files:
        if f.endswith(".json"):
            full = os.path.join(root, f); rel = "data/" + os.path.relpath(full, kd).replace(os.sep, "/")
            handle(rel, open(full, "rb").read(), "kubejs")
json.dump({"PF": PF, "CF": CF, "BM": BM}, open(sys.argv[1], "w"))
print(len(PF), "placed", len(CF), "configured", len(BM), "biome modifiers")
