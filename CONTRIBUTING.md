# Working on the guide

The whole guide is one file, `index.html`, with no build step. Open it in a browser to use it. Everything else in this repo exists to keep that file correct.

## Where things are

| Path | What it is |
|---|---|
| `index.html` | The app: guide steps (`PHASES`), extras per step (`EXTRA`, `LOOK`, `SIDE_FOR`), Materials data (`ITEM_DATA`, `RAW`, `MAT_FOR`, `FIND_FOR`), Research data, Town planner and the styles. |
| `tools/` | Scripts that rebuild the generated data lines in `index.html` from a real ATM10 instance. See `tools/README.md`. |
| `tests/` | The smoke tests: `python3 tests/run.py`. See below. |
| `startup.lua` | The ComputerCraft request-filler script the guide tells people to copy. It is also embedded in the page. |

## The generated lines

These single-line constants are written by `tools/build.sh`. Do not edit them by hand: change `tools/want.py`, `tools/emit.py` or the other tools and rebuild.

`ITEM_REG`, `ITEM_DATA`, `UNKNOWN`, `RESEARCH`, `RESEARCH_TEXT`, `FOOT_STYLES`, `FOOT`, `FOOT_MASK`.

A rebuild needs the game, so run it on your own machine (`ATM10_INSTANCE=... ./tools/build.sh`, about 3 to 4 minutes), then read the diff: new or changed ingredients show up there.

## Everything else is edited by hand

- **A step** is an object in `PHASES` with an `id`, a `layer`, a title `t`, its mods, a `why` paragraph and `subs` (the tick-boxes). Changing a sub-step's text resets that tick for anyone who had it, because ticks are keyed by a hash of the text.
- **Materials for a step**: add an entry to `MAT_FOR` (item slugs from `ITEM_DATA` or `RAW`). If it needs a new item, add it to `tools/want.py` and rebuild.
- **Something you gather** (no recipe) needs a `raw(...)` card, and a `FIND_FOR` entry if a step should show it.
- **A side project** goes in the last phase (the one with `side: true`). Add `SIDE_FOR` entries to suggest it from the steps where it helps.

## Facts come from the pack, not memory

Every number in the guide should come from the installed pack: recipes and config from the jars and `kubejs`, quest text from `config/ftbquests`. When you add or change a claim, check it there first, and say in the step when it is something you could not check. `tools/q.py` shows what makes an item, and `tools/README.md` lists the other helpers.

## The audit record

`AUDIT.md` lists what was checked against the pack, what was wrong, and what is still judgement. Update it when you change a claim, and use it as the checklist when ATM10 releases a new version.

## Tests

```sh
python3 tests/run.py
```

This opens `index.html` in headless Chrome (set `CHROME` if it isn't found) and runs `tests/smoke.js`. It checks the data links (steps, Materials, research goals, phase checkpoints), every tab, progress export and import, the research planner, and the Town planner (layouts, snapping, outlines). It runs on every push in GitHub Actions too. Add a check to `tests/smoke.js` when you add a data structure that other data points at. The tests cannot tell you the data is out of date with a newer ATM10: that needs a rebuild.

## Commits

One topic per commit, with a message that says why. Generated data changes and the guide text that goes with them are best as two commits.
