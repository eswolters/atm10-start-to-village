# Recipe tools

These scripts rebuild the **Materials** data in `../index.html` (the `ITEM_DATA` and `UNKNOWN` lines) from a real ATM10 instance, so the page matches your pack version.

```sh
ATM10_INSTANCE=~/.sklauncher/instances/all-the-mods-10-atm10 ./build.sh          # rewrite index.html
ATM10_INSTANCE=... ./build.sh --dry                                              # just generate, change nothing
```

Needs `python3` and `node`. Set `MC_DATA_JAR` if the Minecraft 1.21.1 jar that holds `data/minecraft` isn't found automatically (the launcher's `client-*-extra.jar`).

What each step does:

1. `index_recipes.py` reads every recipe JSON from the vanilla jar, the mod jars, datapacks and `kubejs/data` (later sources override earlier ones). Data only: nothing from the instance is run.
2. `kubejs_shim.js` runs the pack's KubeJS recipe scripts in an empty sandbox (no file, network or process access) with stub APIs that only *record* what they would add, remove or replace.
3. `apply_scripts.py` applies those edits on top of the jar recipes to get the recipes the game really loads.
4. `gen.py` + `want.py` pick one recipe per wanted item, map ingredients and tags to short ids, and recurse into intermediates. `want.py` is where you add items (`WANT`), map tags to generic items (`MAP`) and mark things you gather instead of craft (`LEAF`).
5. `emit.py` writes the compact data and `update_page.py` splices it into the page.

6. `research.py` rebuilds the Research tab's data (`RESEARCH` and `RESEARCH_TEXT`) from the MineColonies jar and any `kubejs/data/minecolonies/researches` overrides, and `footprints.py` rebuilds the Town planner's building sizes (`FOOT` and `FOOT_STYLES`) by reading the header of every building blueprint in the style packs. `build.sh` runs both. Each can also be run alone: `python3 research.py out.js && python3 update_page.py out.js`.

Helpers: `q.py final.json minecraft:oak_planks ...` shows what makes an item (after step 3), and `worldgen.py` extracts ore placement (heights) for the "where to find it" texts, which are written by hand in `index.html` (`RAW`).

After a rebuild, check the diff: ingredients that are new or changed in the pack will show up there. Craft recipes that need several steps (Create sequenced assembly) aren't supported and appear as "look it up in JEI".

After any rebuild, run `python3 ../tests/run.py`: it checks that every step, recipe and gather card still links up.
