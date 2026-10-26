# ATM10: Start to Village

A beginner-friendly guide for **All the Mods 10** that takes a brand-new world to a fully automated medieval [MineColonies](https://minecolonies.com) town, with the tech (Create, Mekanism, Powah, AE2) hidden underneath it in an "undercroft".

## Use it

Open `index.html` in a browser. It has four tabs:

- **Guide**: the checklist. 90 steps in 11 phases, each with sub-steps you tick off (430 tasks in total). Steps explain why they matter, and many include key ingredients, layout sketches, an *Is it working?* check, a *Not working?* box and a *When it feels slow* hint. Surface steps also carry a green *Make it look good* box with design advice for that building. Several steps also show illustrations (palette builder, skyline, town layout, roads, lighting, walls, hidden tech), each as an *Avoid* / *Aim for* pair. Each phase starts with a goal, a rough time estimate and, where builders have to work, a *While you wait* list. It ends with a checkpoint and a *Town win* step, a small visible improvement to the town. By default only the phase you are in is open (*Focus on current phase*), and its next step is marked. 22 steps are optional, so *Essentials only* gives a real shortest path. Filter by layer (Surface / Undercroft), by mod, or to essentials only, and search.
- **Materials**: an ingredient calculator. Pick items and amounts (or press *Ingredients for this step* in the Guide, or *Full breakdown* in a recipe table) and it lists what to gather with where to find it, what to craft and in which order, and the AE2 patterns that would automate the chain. About 280 items are covered: building blocks, every MineColonies hut, Create, AE2, Powah, Mekanism, Pipez, Laser IO and more. It also has a *where to find it and how to automate it* ladder for each raw material (by hand, colony, machines, AE2), linking to the guide step that builds each rung. The recipes and ore heights were read from the files of an installed ATM10 instance (Create 6.0.10, AE2 19.2.18, Mekanism 10.7.19, MineColonies 1.1.1403, Powah 6.2.10 and the rest) with the pack's KubeJS recipe scripts applied on top, so they include the pack's own changes. A pack update can change them: JEI stays the authority.
- **Learn the basics**: ten illustrated town-design principles (palette, skyline, roads, lighting, hiding the tech), a guide to the town styles installed in the pack (MineColonies, StyleColonies and the Byzantine pack), the decoration mods (Macaw's, Handcrafted, Refurbished Furniture, Supplementaries, Bibliocraft and more) with real block examples, the building and digging tools (FTB Ultimine, the Destruction and Exchanging Gadgets, Construction Sticks, Nature's Compass) with their costs and which ones are gated behind Allthemodium, core automation concepts (input → process → output, push vs pull, sides, bottlenecks, buffers, filters, energy types), how to read a machine, where to find information in game, and a glossary. Glossary terms show their meaning when you hover them in the guide.
- **Fix it**: every troubleshooting entry from the guide by phase, plus common beginner mistakes.

Progress is kept in your browser's local storage.

## The phases

1. Plan before you place a block (includes a vision, palette and district plan)
2. Survive and gear up
3. Found the colony
4. Your first automation (two small starter projects)
5. Dig the undercroft: first hidden tech (Create and Powah)
6. Build the AE2 brain
7. Grow the town to levels 2–3
8. Connect the colony to AE2 (includes [`startup.lua`](startup.lua), a CC:Tweaked + Advanced Peripherals request-filler script)
9. Resource engines (starts with a *do you need this yet?* check, then optional Mekanism ore processing)
10. Finish the town
11. Make it look awesome: roads, landscaping, skyline, lighting, props, hiding the tech, and a photo tour

## Notes

- The illustrations are inline SVG drawn in `index.html`, so the guide stays a single file with no build step.
- Written for solo play on a recent ATM10 (Minecraft 1.21.1, NeoForge). ATM10 updates add and remove mods, so check JEI for exact recipes.
- `startup.lua` was written against the Advanced Peripherals 1.21.1 source (`colony_integrator`, `me_bridge`, `isCraftable`) and falls back to the older names. It has not been tested in-game, so try it on a small scale first.
