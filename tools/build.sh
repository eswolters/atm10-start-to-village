#!/bin/sh
# Rebuild the Materials data from an installed ATM10 instance and write it into ../index.html.
# usage: ATM10_INSTANCE=/path/to/instance ./build.sh [--dry]      (default instance: ~/.sklauncher/instances/all-the-mods-10-atm10)
set -e
here=$(cd "$(dirname "$0")" && pwd)
work=$(mktemp -d)
echo "working in $work"
python3 -I "$here/index_recipes.py" "$work/idx.json"
node "$here/kubejs_shim.js" "$work/calls.json"
python3 -I "$here/apply_scripts.py" "$work/idx.json" "$work/calls.json" "$work/final.json"
python3 -I "$here/gen.py" "$work/final.json" "$here/want.py" "$work/db.json"
python3 -I "$here/emit.py" "$work/db.json" "$work/itemdata.js" "$here/want.py"
python3 -I "$here/research.py" "$work/research.js"
python3 -I "$here/footprints.py" "$work/footprints.js"
if [ "$1" = "--dry" ]; then echo "dry run: index.html not changed (result in $work/itemdata.js)"; else python3 -I "$here/update_page.py" "$work/itemdata.js"; python3 -I "$here/update_page.py" "$work/research.js"; python3 -I "$here/update_page.py" "$work/footprints.js"; fi
