"""Runs tests/smoke.js inside ../index.html in headless Chrome and prints one line per check.
usage: python3 tests/run.py          (exit code 1 when a check fails, or when the page does not run at all)
Set CHROME to the browser binary if it is not found. No packages needed: the page is loaded from a temp copy with the tests added."""
import html, json, os, shutil, subprocess, sys, tempfile

root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
page = open(os.path.join(root, "index.html"), encoding="utf-8").read()
smoke = open(os.path.join(root, "tests", "smoke.js"), encoding="utf-8").read()

chrome = os.environ.get("CHROME") or next((shutil.which(n) for n in ("google-chrome-stable", "google-chrome", "chromium", "chromium-browser") if shutil.which(n)), None)
if not chrome: sys.exit("No Chrome or Chromium found. Set CHROME=/path/to/browser.")

early = '<script>window.__errs=[];window.addEventListener("error",function(e){__errs.push(String(e.message))});</script>'
page = page.replace("<head>", "<head>" + early, 1)
run = "<script>window.addEventListener('load',function(){setTimeout(function(){" + smoke + "},200)});</script>"
page = page.replace("</body>", run + "</body>", 1)

with tempfile.TemporaryDirectory() as tmp:
    path = os.path.join(tmp, "smoke.html")
    open(path, "w", encoding="utf-8").write(page)
    out = subprocess.run([chrome, "--headless=new", "--no-sandbox", "--disable-gpu", "--virtual-time-budget=20000", "--dump-dom", "file://" + path],
                         capture_output=True, text=True, timeout=120).stdout

start = out.find('<pre id="SMOKE">')
if start < 0: sys.exit("FAIL: the page produced no test results (a script error before the tests ran?)")
body = out[start + len('<pre id="SMOKE">'):out.index("</pre>", start)]
results = json.loads(html.unescape(body))
failed = 0
for r in results:
    print(("ok   " if r["ok"] else "FAIL ") + r["name"])
    if not r["ok"]:
        failed += 1
        for d in (r["detail"] if isinstance(r.get("detail"), list) else [r.get("detail")]): print("       " + str(d))
print(f"\n{len(results) - failed} of {len(results)} checks passed")
sys.exit(1 if failed else 0)
