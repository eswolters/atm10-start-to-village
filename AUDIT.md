# Claim audit

Every sentence in the guide that holds a number was listed (350 of them) and sorted: checked against the installed pack, generated from the pack's own data (ore heights, recipes, research costs), design advice (taste, not game data), or marked as unverified. This file records what was checked, what was wrong, and what still rests on judgement, so the next update (a new ATM10 version) knows where to look.

Checked against: Minecraft 1.21.1, NeoForge 21.1.259, ATM10 (CurseForge file 9190157). Sources were the mod jars (recipes, data, language files, in-game guide pages, bytecode where a rule was not written down), the pack's configs and KubeJS scripts, the FTB quest book, and, where the files were silent, the official MineColonies wiki.

## Corrected by the audit

| What the guide said | What the pack does | Source |
|---|---|---|
| Create's ore line gives about 1.75× | 1 ingot's worth per raw ore plus by-products; 1.75× only for ore blocks mined with Silk Touch | Create crushing recipes |
| Mekanism ore chains are 2×, 3×, 4× | Those are per ore block; per raw ore they are 1.33×, 2×, 2.67× | Mekanism recipes |
| A windmill with 8 sails gives a few thousand SU | 512 SU at 8 sails; 512 SU per RPM, 1 RPM per 8 sails, up to 16 RPM | Create config |
| Pipez filters need a Basic upgrade | They need an Advanced upgrade | Pipez bytecode |
| Pipez extract is set by right-clicking | It is set with the Pipe Wrench | Pipez bytecode |
| Mobs drop Inferium essence (20%) | Turned off in this pack (`inferiumDropChance = 0.0`) | MA config |
| Silk Touch does not stop budding certus degrading | It does not degrade, except flawless budding certus | AE2 in-game guide |
| Gravel, coarse dirt and cobblestone make a road that speeds citizens up | Only gravel is on MineColonies' road-block list | MineColonies `pathblocks` tag |
| Every hut is 5–7 planks, a Build Tool and one item | The Town Hall takes 2 Build Tools; the Graveyard takes stone | Recipe data |
| The Phase 5 Powah step needs nothing from the Nether | Energizing rods need Nether quartz; AE2 needs about 55 quartz and 100 glowstone dust by Phase 8 | Recipe data |
| Guards first appear in Phase 7 | Raids are on (about every 14 nights) from the start | MineColonies config |

Also made more complete: research prerequisites that the steps left out (First Aid cost, Circus needs a Dining Hall level 2, Archery and Combat Academy need a Barracks level 3, More Scrolls needs an Enchanter's Tower level 3 and an Ancient Tome), the Infusion Crystal's 500 uses, and the Explorer's Compass's recovery compass.

## Confirmed

- All research costs and requirements quoted in the steps (22 researches), and the rabbit foot research numbers.
- Recipes: Iron Furnace, drawers, Supply Camp, Build Tool, Warp Stone, Waystone, Destruction Gadget, Mega Torch, Pipe Wrench and Pipez upgrades, AE2 cell components, Flux Cores, Explorer's Compass.
- AE2: channels (8 on standard cables, 32 on dense cables and per controller face, 8 devices without a controller), the 4 presses from a meteorite, budding certus tiers, the Charger accepting FE, wireless base range 16.
- Powah: tiers, recipes, reactor fuel and coolant, thermo generator heat sources, uraninite ore heights.
- Configs: raids (every 10–14 nights, up to 80 raiders, break blocks and doors), colony loading and FTB Chunks limits, Destruction Gadget (50 FE per block, 2,000,000 FE), FTB Ultimine (64 blocks, hunger cost), Mega Torch radius 64, Mystical Agriculture farmland and soil bonuses.
- Ore heights and the Mining dimension notes (from the world generation data).
- MineColonies wiki: a builder can only upgrade huts up to its own level; requests go to the Warehouse, then to a crafter.

## Not verified (rests on judgement or on knowledge the files don't contain)

- **Time estimates** for every phase, and the 30 to 55 hour total. They are guesses.
- **Rules of thumb:** a level 1 hut "typically needs 1–3 stacks of planks"; build the Barracks "once the colony reaches 20+ citizens"; "about 8–12 citizens" at the end of Phase 3; a second Courier's Hut "once you have more than about 8 huts"; 3 builders before level 3 upgrades.
- **Happiness:** the guide no longer gives a number, because no scale is written in the files or on the wiki.
- **The player step of the request order** (Warehouse, then a crafter, then you on the Clipboard): the first two are on the wiki and the Clipboard item exists, but the wiki doesn't describe the third.
- **Design advice** (road widths, lamp spacing, "groups of 3 or 5", skyline rules) is taste, not game data.
- **Block counts** for decoration mods (Macaw's, Handcrafted and others) came from an earlier count. A rough recount of the jars gave close but not identical numbers (605 against 607 roof blocks, 449 against 471 furniture blocks), and the two methods are not equivalent.
- **Mekanism factory slots** (3, 5, 7, 9) and the **AE2 Export Bus having 9 filter slots** are standard knowledge that the pack's files don't restate.
- **Not run in game:** `startup.lua`, the Hopper Botany Pot output behaviour, the obsidian generator layout, and the Mob Grinding Utils spikes' drops (only the mod's own tooltip was read).

## How to repeat this

1. Run `tools/build.sh` against the new instance and read the diff.
2. Re-run `tests/run.py`.
3. Re-check the "Corrected" table first: those are the claims most likely to change, because they depend on pack configs and scripts.
4. For anything new, find the source (jar data, config, in-game guide, wiki) before writing the number.
