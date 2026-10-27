/* Smoke tests that run inside index.html in headless Chrome (see run.py). Each check is independent: a failing one never stops the others.
   They look at the data the guide ships with and at the behaviour of every tab, and they never touch the network. */
(function () {
  const results = [];
  const check = (name, fn) => {
    try { const detail = fn(); results.push({ name, ok: detail === undefined || detail === true || (Array.isArray(detail) && !detail.length), detail: Array.isArray(detail) && detail.length ? detail.slice(0, 12) : undefined }); }
    catch (e) { results.push({ name, ok: false, detail: String(e && e.stack || e).slice(0, 300) }); }
  };
  const dupes = list => list.filter((x, i) => list.indexOf(x) !== i);
  const stepIds = new Set(allSteps.map(s => s.id));

  /* ---- guide data ---- */
  check("steps have unique ids and the fields the page needs", () => {
    const bad = [];
    dupes(allSteps.map(s => s.id)).forEach(id => bad.push("duplicate step " + id));
    allSteps.forEach(s => { if (!s.t || !s.layer || !Array.isArray(s.mods) || !Array.isArray(s.subs)) bad.push("incomplete " + s.id); });
    return bad;
  });
  check("sub-step ids are unique and belong to their step", () => {
    const ids = []; const bad = [];
    allSteps.forEach(s => s.subs.forEach(x => { ids.push(x.id); if (!x.id.startsWith(s.id + ":")) bad.push(x.id); }));
    dupes(ids).forEach(id => bad.push("duplicate " + id));
    return bad;
  });
  check("phases: ids unique, every main phase has a goal and checkpoint, the side phase is all optional", () => {
    const bad = [];
    dupes(PHASES.map(p => p.id)).forEach(id => bad.push("duplicate phase " + id));
    PHASES.forEach(p => {
      if (!PHASE_META[p.id]) bad.push("no PHASE_META for " + p.id);
      if (p.side) { if (p.steps.some(s => !s.opt)) bad.push("side phase has a required step"); }
      else if (!MILESTONES[p.id]) bad.push("no checkpoint for " + p.id);
    });
    Object.keys(PHASE_META).concat(Object.keys(MILESTONES)).forEach(k => { if (!PHASES.some(p => p.id === k)) bad.push("unknown phase key " + k); });
    return bad;
  });
  check("every step that points at another step points at one that exists", () => {
    const bad = [];
    const need = (where, id) => { if (!stepIds.has(id)) bad.push(where + " -> " + id); };
    Object.keys(MAT_FOR).forEach(k => need("MAT_FOR", k));
    Object.keys(FIND_FOR).forEach(k => need("FIND_FOR", k));
    Object.keys(SIDE_FOR).forEach(k => { need("SIDE_FOR", k); SIDE_FOR[k].forEach(([id]) => need("SIDE_FOR target of " + k, id)); });
    Object.keys(PLAN_STEPS).forEach(k => need("PLAN_STEPS", k));
    Object.keys(RES_STEP_GOALS).forEach(k => need("RES_STEP_GOALS", k));
    Object.keys(RAW).forEach(id => (RAW[id].auto || []).forEach(a => need("RAW " + id, a[2])));
    return bad;
  });

  /* ---- materials data ---- */
  check("every Materials list resolves, and unresolved items have a hint", () => {
    const bad = [];
    Object.keys(MAT_FOR).forEach(k => {
      MAT_FOR[k].items.forEach(([id, n]) => { if (!ITEMS[id] && !RAW[id] && !UNKNOWN[id]) bad.push(k + " has unknown item " + id); if (!(n > 0)) bad.push(k + " has a bad amount for " + id); });
      const r = resolve(MAT_FOR[k].items);
      Object.keys(r.unknown).forEach(id => { if (!UNKNOWN_HINT[id]) bad.push(k + " needs " + id + " but nothing says how to make it"); });
      Object.keys(r.raw).forEach(id => { if (!RAW[id]) bad.push(k + " needs " + id + " with no gather card"); });
    });
    return bad;
  });
  check("recipes have no loops and only use known ingredients", () => {
    const bad = [];
    Object.keys(ITEMS).forEach(id => ITEMS[id].in.forEach(([c]) => { if (!ITEMS[c] && !RAW[c] && !UNKNOWN[c]) bad.push(id + " uses unknown " + c); }));
    const state = {};
    const dfs = id => { state[id] = 1; (ITEMS[id] ? ITEMS[id].in : []).forEach(([c]) => { if (state[c] === 1) bad.push("loop at " + id + " -> " + c); else if (!state[c] && ITEMS[c]) dfs(c); }); state[id] = 2; };
    Object.keys(ITEMS).forEach(id => { if (!state[id]) dfs(id); });
    return bad;
  });
  check("find-it cards and registry names point at real items", () => {
    const bad = [];
    Object.keys(FIND_FOR).forEach(k => FIND_FOR[k].forEach(id => { if (!RAW[id] && !ITEMS[id]) bad.push(k + " finds " + id); }));
    Object.keys(ITEM_REG).forEach(reg => { const s = ITEM_REG[reg]; if (!ITEMS[s] && !RAW[s]) bad.push(reg + " -> " + s); });
    return bad;
  });

  /* ---- research data ---- */
  check("research: parents exist and every goal has a plan", () => {
    const bad = [];
    Object.values(RES).forEach(r => { if (r.parent && !RES[r.parent]) bad.push(r.id + " has missing parent " + r.parent); });
    const effects = new Set(); Object.values(RES).forEach(r => r.eff.forEach(e => effects.add(e[0])));
    let goals = 0;
    effects.forEach(e => ["b:" + e, "g:" + e].forEach(key => {
      if (!goalValid(key)) return; goals++;
      const t = goalTarget(key); if (!t) { bad.push(key + " has no target"); return; }
      if (!lineage(t.id).length) bad.push(key + " has an empty lineage");
    }));
    if (goals < 20) bad.push("only " + goals + " valid goals");
    return bad;
  });

  /* ---- behaviour: every tab renders ---- */
  check("every tab renders without placeholders", () => {
    const bad = [], pages = { guide: "main", materials: "matPage", research: "resPage", planner: "planPage", learn: "learnPage", fix: "fixPage" };
    Object.keys(pages).forEach(t => {
      showTab(t); const el = document.getElementById(pages[t]);
      if (el.hidden) bad.push(t + " is hidden"); const txt = el.innerText || "";
      if (txt.length < 200) bad.push(t + " is nearly empty"); if (/\bundefined\b|\bNaN\b|\[object Object\]/.test(txt)) bad.push(t + " shows a placeholder: " + (txt.match(/.{15}(undefined|NaN|\[object Object\]).{15}/) || [""])[0]);
    });
    showTab("guide"); return bad;
  });
  check("the guide shows every step and every sub-step", () => {
    openPhases && PHASES.forEach(p => { openPhases[p.id] = true; }); render();
    const n = document.querySelectorAll("li.step").length; return n === allSteps.length ? true : ["rendered " + n + " of " + allSteps.length];
  });
  check("ticking steps updates progress and survives export, reset and import", () => {
    const s = allSteps[0], ids = s.subs.map(x => x.id); setMany(ids, true);
    if (!stepDone(s)) return ["step not done after ticking all its sub-steps"];
    const text = JSON.stringify(buildBackup()), b = parseBackup(text);
    if (b.error) return [b.error]; if (b.known.length !== ids.length) return ["backup holds " + b.known.length + " ticks, expected " + ids.length];
    setMany(ids, false); if (stepDone(s)) return ["untick did not work"];
    applyBackup(b, "replace"); if (!stepDone(s)) return ["import did not restore the ticks"];
    setMany(ids, false);
    const bad = parseBackup("{ not json"); if (!bad.error) return ["a broken file was accepted"];
    return true;
  });
  check("current phase never lands on the optional side projects", () => {
    allSteps.forEach(s => { if (!s.opt) units(s).forEach(u => { done[u] = true; }); });
    const id = PHASES[currentPhaseIndex()].id; done = {}; render();
    return PHASES.find(p => p.id === id).side ? ["the side phase became the current phase"] : true;
  });

  /* ---- behaviour: research planner ---- */
  check("research planner: pick, tick and untick a goal", () => {
    resState = { done: {}, goals: {} }; openResearch(["b:blockhutlibrary"]);
    const n = planList().length; if (!n) return ["empty plan for the Library"];
    planList().forEach(r => setResDone(r.id, true)); if (planList().length) return ["plan not empty after ticking everything"];
    const first = planList(true)[0]; setResDone(first.id, false); if (planList().length !== 1) return ["unticking one step should bring back exactly one"];
    resState = { done: {}, goals: {} }; saveRes(); showTab("guide"); return true;
  });

  /* ---- behaviour: town planner ---- */
  check("planner: every ready-made layout passes all the guide's layout rules", () => {
    const bad = [];
    ["starter", "village", "town", "castle", "street"].forEach(id => {
      planLoadLayout(id); const r = planChecks().rules.filter(x => x.st !== "ok").map(x => x.id);
      if (r.length) bad.push(id + ": " + r.join(","));
    });
    return bad;
  });
  check("planner: building outlines match their blueprint sizes", () => {
    const bad = []; let n = 0;
    Object.keys(FOOT_MASK).forEach(style => Object.keys(FOOT_MASK[style]).forEach(b => {
      const g = decodeMask(FOOT_MASK[style][b]); n++;
      if (!g.length || !g[0].length || !g.some(r => r.some(c => c))) bad.push(style + "/" + b + " is empty");
    }));
    if (n < 100) bad.push("only " + n + " outlines");
    return bad;
  });
  check("planner: snapping lines up edges, leaves 3 blocks and keeps 1 beside a road", () => {
    plan.items = []; plan.next = 1; plan.snap = true; plan.view.s = 6;
    const a = planAdd({ t: "b", k: "townhall", x: 0, z: 0, r: 0, l: 1, st: "" }), ar = rectOf(a), bad = [];
    const g = planSnap({ x: ar.x + ar.w + 5, z: ar.z + 1, w: 14, h: 14 }, null);
    if (g[0] !== ar.x + ar.w + 3 || g[1] !== ar.z) bad.push("neighbour snap gave " + g);
    planAdd({ t: "road", pts: [[-50, 60], [80, 60]], w: 4 });
    if (planSnap({ x: 0, z: 64, w: 14, h: 14 }, null)[1] !== 63) bad.push("road snap below");
    plan.snap = false; const off = planSnap({ x: ar.x + ar.w + 5, z: 1, w: 14, h: 14 }, null); if (off[0] !== ar.x + ar.w + 5 || off[1] !== 1) bad.push("snap did not switch off");
    plan.snap = true; const c = Math.round((plan.origin.x + 900) / 16) * 16 - plan.origin.x;
    if (planSnapV(c + 2, "x", -1) !== c) bad.push("chunk line snap"); if (planSnapV(c + 5, "x", -1) !== null) bad.push("snapped too far");
    plan.items = []; plan.next = 1; return bad;
  });
  check("planner: saved layouts survive export and import", () => {
    planLoadLayout("village"); const n = plan.items.length, b = parseBackup(JSON.stringify(buildBackup()));
    if (b.error || !b.plan || b.plan.items.length !== n) return ["plan lost in backup (" + (b.plan ? b.plan.items.length : "none") + " of " + n + ")"];
    plan.items = []; plan.next = 1; return true;
  });

  /* ---- first impressions: the start panel and the first steps ---- */
  check("the Start here panel is on the Guide tab only, and its links work", () => {
    const bad = [], vis = () => getComputedStyle(document.getElementById("startHere")).display !== "none";
    showTab("guide"); if (!vis()) bad.push("hidden on the Guide tab");
    showTab("learn"); if (vis()) bad.push("still showing on the Learn tab");
    document.getElementById("goPhase1").click(); if (tab !== "guide") bad.push("the Phase 1 link did not return to the Guide");
    if (!document.querySelector("details.phase").open) bad.push("Phase 1 not open after the link");
    const t = document.getElementById("filtToggle"); t.click(); const open = document.querySelector(".bar").classList.contains("filters-open"); t.click();
    if (!open || document.querySelector(".bar").classList.contains("filters-open")) bad.push("the Filters button does not toggle");
    return bad;
  });
  check("Phase 1 starts with the first-30-minutes step, and the early steps need nothing the reader can't have yet", () => {
    const bad = [], p1 = PHASES[0].steps;
    if (p1[0].id !== "p-day1") bad.push("Phase 1 does not start with p-day1");
    const site = allSteps.find(s => s.id === "p-site");
    site.subs.forEach(x => { if (/Nature's Compass/.test(x.html) && !/Phase 2|iron/.test(x.html)) bad.push("the compass step does not say it needs iron first"); });
    if (!allSteps.find(s => s.id === "s-waystone").opt) bad.push("the Warp Stone waystone step should be optional in Phase 2");
    return bad;
  });

  /* ---- no script errors ---- */
  check("no script errors while loading or running the tests", () => (window.__errs || []).slice());

  const pre = document.createElement("pre"); pre.id = "SMOKE"; pre.textContent = JSON.stringify(results); document.body.appendChild(pre);
})();
