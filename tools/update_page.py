"""Replace the generated recipe data (ITEM_DATA and UNKNOWN) inside ../index.html with a freshly generated itemdata.js"""
import re, sys, os
page = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "index.html")
new = open(sys.argv[1]).read().rstrip("\n").split("\n")
html = open(page).read()
for line in new:
    name = re.match(r"const (\w+) = ", line).group(1)
    pat = re.compile(r"^const %s = .*;$" % name, re.M)
    if not pat.search(html): sys.exit("Could not find 'const %s = ...;' in index.html" % name)
    html = pat.sub(lambda m: line, html, count=1)
open(page, "w").write(html)
print("index.html updated")
