# ATM10: Start to Village

A beginner-friendly guide for **All the Mods 10** that takes a brand-new world to a fully automated medieval [MineColonies](https://minecolonies.com) town, with the tech (Create, Mekanism, Powah, AE2) hidden underneath it in an "undercroft".

## Use it

Open `index.html` in a browser. It has three tabs:

- **Guide**: the checklist. 71 steps in 10 phases, each with sub-steps you tick off (337 tasks in total). Steps explain why they matter, and many include key ingredients, layout sketches, an *Is it working?* check, a *Not working?* box and a *When it feels slow* hint. Each phase ends with a checkpoint. Filter by layer (Surface / Undercroft), by mod, or to essentials only, and search.
- **Learn the basics**: core automation concepts (input → process → output, push vs pull, sides, bottlenecks, buffers, filters, energy types), how to read a machine, where to find information in game, and a glossary. Glossary terms show their meaning when you hover them in the guide.
- **Fix it**: every troubleshooting entry from the guide by phase, plus common beginner mistakes.

Progress is kept in your browser's local storage.

## The phases

1. Plan before you place a block
2. Survive and gear up
3. Found the colony
4. Your first automation (two small starter projects)
5. Dig the undercroft: first hidden tech
6. Build the AE2 brain
7. Grow the town to levels 2–3
8. Connect the colony to AE2 (includes [`startup.lua`](startup.lua), a CC:Tweaked + Advanced Peripherals request-filler script)
9. Resource engines
10. Finish the town

## Notes

- Written for solo play on a recent ATM10 (Minecraft 1.21.1, NeoForge). ATM10 updates add and remove mods, so check JEI for exact recipes.
- `startup.lua` was written against the Advanced Peripherals 1.21.1 source (`colony_integrator`, `me_bridge`, `isCraftable`) and falls back to the older names. It has not been tested in-game, so try it on a small scale first.
