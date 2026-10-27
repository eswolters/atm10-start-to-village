# Changelog

Newest first. The guide targets ATM10 on Minecraft 1.21.1 (NeoForge), solo play.

## Roads

- New **Making roads** section on the Learn tab: which blocks make citizens walk faster (MineColonies' own road-block list), and the ways to lay a road (by hand, Construction Sticks, the Exchanging Gadget, the Shape Tool, and planning it on the Town planner first). Every road step links to it.
- **Correction:** the guide recommended a gravel, coarse dirt and cobblestone mix, but only gravel is on MineColonies' road-block list, so only gravel speeds citizens up. The steps now suggest gravel, dirt path and stone bricks or polished andesite, and say that cobblestone, coarse dirt and Macaw's paving are for looks only.
- A test now checks that every in-page jump link points at something that exists.

## Phases 7 to 11 review

- **Raids:** a new Phase 3 step, "Raids are on: your first guard". Raids are enabled in this pack's config, about every 14 nights, and the guide used to mention guards only in Phase 7. A Guard Tower needs no research (only the Barracks does). The Phase 7 guard step now builds on it.
- **One wall, three stages:** Phase 7 marks the line and builds the gatehouse and a short stretch, Phase 10 builds the wall with the Build Tool's wall and gate decorations, and Phase 11 reshapes it to follow the land. The wall used to be built in four places.
- **Shape Tool:** now described as it works (it has a builder dig, fill and flatten ground and put up simple shapes, built like any decoration inside your colony, with materials). Checked in the MineColonies and Structurize code and on the MineColonies wiki.
- **Happiness** is explained in Phase 3, where it is first used, and has a hover definition.
- **Blaze rods are now required** on the Nether trip (about 6, for the Phase 9 Powah step), and the trip warns about fortresses.

## Phases 4 to 6 review

- **New step: "Your first Nether trip"** at the start of the Create machines in Phase 5. The required path needs about 55 Nether quartz and about 100 glowstone dust by Phase 8 (Powah's energizing rods need quartz as early as Phase 5), and nothing had introduced the Nether. A test now fails if a required step needs Nether items before this step.
- The automatic smelter now uses the **Pipe Wrench**, which is what sets a pipe end to extract, and its chest layout is spelled out.
- One vault depth: the ceiling at least 12 blocks below the lowest foundation (as in Phase 1), staying above about Y -50.
- The Create basics step is now a recap of the Phase 4 machine, and the cobble project explains stress where it is first used.
- The Pipez filter project is optional (it needs an Advanced upgrade), and catching a blaze and making brass are optional until the Phase 9 trains.

## Newcomer pass

- A "Start here" panel replaces the old intro wall: what you end with (with a cross-section diagram of the town above its hidden vault), who it is for, how long it takes (about 30 to 55 hours for Phases 1 to 8), what versions it was checked against, and a three-step path. The old tips are in a collapsed "Other tools" list. "Hollowmere" is now explained as the example town's name.
- Other tabs show a compact header, so their content starts near the top. On phones all six tabs are visible and the guide filters sit behind a Filters button.
- New first step, "Your first 30 minutes", for people who have just spawned (JEI keys, the quest book's Chapter 1, the map).
- Fixed the order in Phase 1: the Nature's Compass needs iron, so it now says to come back after the first mining.
- The Warp Stone waystone (4 ender pearls) is optional in Phase 2, with the village waystone as the alternative. The ore trip no longer asks for osmium before Mekanism is relevant.

## Checked against the pack (latest audit)

- **Corrected: Create ore line.** In this pack raw ore crushes 1 to 1, so crushing and washing gives one ingot's worth plus free redstone, clay, quartz or gunpowder. It only gives about 1.75× for ore blocks mined with Silk Touch. The guide used to say 1.75× for everything.
- **Corrected: Mekanism ore processing.** The 2×, 3× and 4× counts are per ore block. Per raw ore the stages give 1.33×, 2× and 2.67×.
- **Corrected: windmill.** 8 sail blocks give 512 SU (1 RPM); each 8 more sails add 1 RPM, up to 16.
- **Corrected: Pipez filters** need an Advanced upgrade, not a Basic one.
- Powah reactor coolant (water), uraninite ore heights, and the Energy Detector source are now stated exactly.
- Missing material lists filled in for the Town Hall, food crops, guards, the gatehouse and more.

## Side projects (optional section after Phase 11)

- Mystical Agriculture crop room, a Botany Pots version of it, a Mob Grinding Utils mob farm and a Productive Bees farm. The main phases suggest them where they pay off.
- Cobblegen Galore block generators and an obsidian source are mentioned where they help.

## Town planner

- A map of real 1-block squares with chunk shading and rulers, real building outlines for the main styles, pick-then-click placing, drag with snapping and measured gaps, undo and redo.
- Resizable undercroft and market square with chunk counts, editable roads, a full-screen mode, and five ready-made layouts (starter, village, large town, castle town, main street) that pass the guide's layout rules.

## Research planner and Materials

- Research tab: pick the buildings and bonuses you want and get the ordered research list with what to bring. Finished research can be un-ticked.
- Materials tab: ingredient breakdowns, where to find each item, and automation ladders, from the real recipes of the installed pack. The two tabs link to each other.

## Guide

- 11 phases from planning to beautification, each with a goal, a time estimate, a "town win" step, optional steps and a focus mode.
- Export and import of progress, ticks and the Materials list.
- `startup.lua` (the request filler) checked against the Advanced Peripherals version in ATM10.

## Project

- Smoke tests (`python3 tests/run.py`) and a GitHub Actions run on every push.
- Data tools in `tools/` that rebuild the generated data from an ATM10 instance.
