// Runs the ATM10 KubeJS server scripts in an empty sandbox (no fs, no require, no process) with stub APIs
// that only RECORD recipe edits. Output: JSON list of calls in execution order.
const fs = require("fs"), path = require("path"), vm = require("vm");
const inst = process.env.ATM10_INSTANCE ? process.env.ATM10_INSTANCE.replace(/^~/, process.env.HOME) : path.join(process.env.HOME, ".sklauncher/instances/all-the-mods-10-atm10");
const root = path.join(inst, "kubejs/server_scripts");
const files = [];
(function walk(d) { for (const f of fs.readdirSync(d).sort()) { const p = path.join(d, f); fs.statSync(p).isDirectory() ? walk(p) : p.endsWith(".js") && files.push(p); } })(root);
const calls = []; let current = "";
function chain(rec) {
  const p = new Proxy(function () {}, {
    get: (_, k) => { if (k === "then") return undefined; if (k === Symbol.toPrimitive) return () => "[chain]";
      return (...a) => { if (k === "id") rec.id = a[0]; else (rec.mods = rec.mods || []).push([String(k), a]); return p; }; },
    apply: () => p,
  });
  return p;
}
function rec(method, args) { const r = { file: path.relative(root, current), m: method, args: JSON.parse(JSON.stringify(args, (k, v) => typeof v === "function" ? undefined : Object.prototype.toString.call(v) === "[object RegExp]" ? { $re: v.source } : v)) }; calls.push(r); return chain(r); }
function recipesProxy(prefix) {
  return new Proxy(function () {}, { get: (_, k) => typeof k === "symbol" ? undefined : recipesProxy(prefix ? prefix + "." + k : k), apply: (_, __, args) => rec("recipes." + prefix, args) });
}
const ev = new Proxy({}, { get: (_, k) => {
  if (typeof k === "symbol" || k === "then") return undefined;
  if (k === "recipes") return recipesProxy("");
  if (k === "forEachRecipe") return () => {};
  return (...args) => rec(String(k), args);
} });
const anyProxy = name => new Proxy(function () {}, { get: (_, k) => typeof k === "symbol" ? () => name : anyProxy(name + "." + String(k)), apply: () => anyProxy(name + "()") });
const handlers = [];
const ServerEvents = new Proxy({}, { get: (_, k) => (cb) => { if (k === "recipes") handlers.push([current, cb]); } });
function makeCtx() {
  const ctx = {
    ServerEvents, console: { log() {}, info() {}, warn() {}, error() {} },
    Platform: { isLoaded: () => true, getMods: () => ({}) },
    Item: { of: (id, c) => (typeof c === "number" ? { id, count: c } : id), getId: x => x, exists: () => true },
    Ingredient: { of: x => anyProxy("ing") }, Fluid: { of: (id, a) => ({ fluid: id, amount: a }) },
    JsonIO: anyProxy("JsonIO"), Utils: anyProxy("Utils"), global: {}, Math, JSON, Object, Array, String, Number, Boolean, RegExp, Date, parseInt, parseFloat, Set, Map, Symbol, isNaN,
    onEvent: () => {}, LootJS: anyProxy("LootJS"), StartupEvents: anyProxy("StartupEvents"), ClientEvents: anyProxy("ClientEvents"), BlockEvents: anyProxy("BlockEvents"),
    ItemEvents: anyProxy("ItemEvents"), PlayerEvents: anyProxy("PlayerEvents"), EntityEvents: anyProxy("EntityEvents"), LevelEvents: anyProxy("LevelEvents"), NetworkEvents: anyProxy("NetworkEvents"),
    Text: anyProxy("Text"), Color: anyProxy("Color"), Block: anyProxy("Block"), Client: anyProxy("Client"), Component: anyProxy("Component"), BlockStatePredicate: anyProxy("BSP"),
    Java: { loadClass: () => anyProxy("Java") }, Registry: anyProxy("Registry"), DataComponent: anyProxy("DC"), Direction: anyProxy("Direction"), NBT: anyProxy("NBT"),
    Rarity: anyProxy("Rarity"), Duration: anyProxy("Duration"), Biome: anyProxy("Biome"), Entity: anyProxy("Entity"), Server: anyProxy("Server"), Level: anyProxy("Level"),
  };
  return vm.createContext(ctx);
}
const ctx = makeCtx();
const errors = [];
const sroot = path.join(inst, "kubejs/startup_scripts");
const sfiles = [];
(function walk(d) { for (const f of fs.readdirSync(d).sort()) { const p = path.join(d, f); fs.statSync(p).isDirectory() ? walk(p) : p.endsWith(".js") && sfiles.push(p); } })(sroot);
for (const f of sfiles) { try { vm.runInContext(fs.readFileSync(f, "utf8"), ctx, { filename: f, timeout: 2000 }); } catch (e) { errors.push(["startup/" + path.relative(sroot, f), String(e.message).slice(0, 100)]); } }
for (const f of files) {
  current = f;
  try { vm.runInContext(fs.readFileSync(f, "utf8"), ctx, { filename: f, timeout: 2000 }); }
  catch (e) { errors.push([path.relative(root, f), String(e.message).slice(0, 100)]); }
}
for (const [f, cb] of handlers) {
  current = f;
  try { vm.runInContext("0", ctx); cb(ev); } catch (e) { errors.push([path.relative(root, f), "cb: " + String(e.message).slice(0, 120)]); }
}
fs.writeFileSync(process.argv[2], JSON.stringify({ calls, errors }));
console.log(files.length, "scripts,", handlers.length, "recipe handlers,", calls.length, "calls,", errors.length, "errors");
