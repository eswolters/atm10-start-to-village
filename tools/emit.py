"""db.json -> JS data block (ITEM_DATA, UNKNOWN_NAMES) written to argv[2]"""
import json, sys
d = json.load(open(sys.argv[1]))
I = d["items"]
OVERRIDE = {
    "planks": "Planks (any wood)", "log": "Logs (any wood)", "wool": "Wool (any colour)", "stick": "Sticks", "slab": "Wooden slabs", "stairs": "Wooden stairs",
    "fence": "Wooden fences", "fence_gate": "Wooden fence gate", "door": "Wooden doors", "trapdoor": "Wooden trapdoors", "sign": "Signs", "boat": "Boat",
    "chest_boat": "Chest boat", "bed": "Bed", "torch": "Torches", "ladder": "Ladders", "iron_nugget": "Iron nuggets", "iron_bars": "Iron bars", "glass_pane": "Glass panes",
    "stone_brick_slab": "Stone brick slabs", "stone_brick_stairs": "Stone brick stairs", "stone_brick_wall": "Stone brick walls", "cobble_slab": "Cobblestone slabs",
    "cobble_stairs": "Cobblestone stairs", "cobble_wall": "Cobblestone walls", "stone_bricks": "Stone bricks", "shaft": "Shafts", "chute": "Chutes",
    "build_tool": "Build Tool", "scan_tool": "Scan Tool", "drawer_1x1": "Drawer (1×1)", "powah_energy_cell_starter": "Starter Energy Cell (Powah)",
    "powah_energy_cell_basic": "Basic Energy Cell (Powah)", "energy_cell": "Energy Cell (AE2)", "me_interface": "ME Interface", "crafting_storage_1k": "1k Crafting Storage",
    "crafting_storage_4k": "4k Crafting Storage", "cell_component_1k": "1k Cell Component", "cell_component_4k": "4k Cell Component", "item_storage_cell_1k": "1k Storage Cell",
    "item_storage_cell_4k": "4k Storage Cell", "terminal": "ME Terminal", "controller": "ME Controller", "drive": "ME Drive", "p2p_tunnel": "ME P2P Tunnel",
    "laser_card_item": "Item Card (Laser IO)", "laser_filter_basic": "Basic Filter (Laser IO)", "pipez_item_pipe": "Item Pipe (Pipez)", "pipez_basic_upgrade": "Basic Upgrade (Pipez)",
    "stone": "Stone", "hut_field": "Scarecrow (field)", "hut_plantation_field": "Plantation field marker", "hut_citizen": "Residence",
}
out = {}
for slug, v in I.items():
    flags = (1 if v["atm"] else 0) | (2 if v["want"] else 0)
    row = [OVERRIDE.get(slug, v["n"]), v["out"], v["in"], v["at"], v["grp"], flags]
    if v["also"] or v["tools"]: row += [v["also"], v["tools"]]
    out[slug] = row
unk = {k: (OVERRIDE.get(k) or d["names"].get(k, k)) for k in ("precision_mechanism", "sturdy_sheet", "sophisticatedstorage_barrel", "track")}
unk["sophisticatedstorage_barrel"] = "Barrel (Sophisticated Storage)"
unk["track"] = "Track"
js = "const ITEM_DATA = " + json.dumps(out, ensure_ascii=False, separators=(",", ":")) + ";\nconst UNKNOWN = " + json.dumps(unk, ensure_ascii=False) + ";\n"
open(sys.argv[2], "w").write(js)
print(len(out), "items,", len(js), "bytes")
