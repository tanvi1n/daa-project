/* N-Queens (N = 4) backtracking visualizer.
 * Part 1 runs the real backtracking algorithm (same logic as Project10_NQueens.java)
 * and records every step. Part 2 replays those steps on the board and the tree. */
(function () {
  "use strict";
  const N = 4;
  const SVGNS = "http://www.w3.org/2000/svg";

  /* ---------- 1. Backtracking search: records tree nodes + steps ---------- */
  const nodes = [];   // state-space tree: one node per (row, col) attempt, plus the Start node
  const steps = [];   // ordered exploration steps
  const solutions = [];
  const col = new Array(N + 1).fill(0);   // col[r] = column of the queen in row r (0 = none)

  function newNode(parent, row, c) {
    const node = { id: nodes.length, parent, row, col: c, children: [], status: null, reason: null, solution: false };
    nodes.push(node);
    if (parent) parent.children.push(node);
    return node;
  }

  // Returns null if (row, c) is safe, otherwise the reason (type + conflicting queen).
  function conflict(row, c) {
    for (let r = 1; r < row; r++) {
      if (col[r] === c) return { type: "column", row: r, col: col[r] };
      if (Math.abs(col[r] - c) === row - r) return { type: "diagonal", row: r, col: col[r] };
    }
    return null;
  }

  const queensNow = () => col.slice(1).map((c, i) => [i + 1, c]).filter(q => q[1] > 0);

  function solve(row, parent) {
    if (row > N) {                                   // all queens placed -> solution
      solutions.push(col.slice(1));
      parent.solution = true;
      steps.push({ type: "solution", node: parent, queens: queensNow(), index: solutions.length });
      return;
    }
    for (let c = 1; c <= N; c++) {                   // try every column of this row
      const node = newNode(parent, row, c);
      steps.push({ type: "try", node, queens: queensNow() });
      const bad = conflict(row, c);
      if (bad) {                                     // invalid branch (red), pruned
        node.status = "invalid"; node.reason = bad;
        steps.push({ type: "invalid", node, queens: queensNow(), reason: bad });
      } else {
        node.status = "valid"; col[row] = c;         // place queen
        steps.push({ type: "place", node, queens: queensNow() });
        solve(row + 1, node);                        // recurse into the next row
        col[row] = 0;                                // BACKTRACK: remove queen
        steps.push({ type: "backtrack", node, queens: queensNow() });
      }
    }
  }

  const root = newNode(null, 0, 0);
  steps.push({ type: "start", node: root, queens: [] });
  solve(1, root);
  steps.push({ type: "done", node: root, queens: [] });

  // Mark every node on the path to a solution (for the green path).
  nodes.forEach(n => { if (n.solution) for (let p = n; p; p = p.parent) p.onSolution = true; });
  const totalInvalid = nodes.filter(n => n.status === "invalid").length;

  /* ---------- 2. Tree layout (leaf-based, computed once) ---------- */
  const DX = 36, DY = 92, PADX = 30, PADY = 34;
  let leaf = 0;
  (function layout(n) {
    n.y = PADY + n.row * DY;
    if (!n.children.length) n.x = PADX + (leaf++) * DX;
    else {
      n.children.forEach(layout);
      n.x = (n.children[0].x + n.children[n.children.length - 1].x) / 2;
    }
  })(root);
  const treeW = PADX * 2 + (leaf - 1) * DX, treeH = PADY + N * DY + 46;

  const $ = id => document.getElementById(id);
  const el = (name, attrs, parent) => {
    const e = document.createElementNS(SVGNS, name);
    for (const k in attrs) e.setAttribute(k, attrs[k]);
    if (parent) parent.appendChild(e);
    return e;
  };

  const treeSvg = $("tree");
  treeSvg.setAttribute("width", treeW); treeSvg.setAttribute("height", treeH);
  treeSvg.setAttribute("viewBox", `0 0 ${treeW} ${treeH}`);
  const edgeEls = [], nodeEls = [];
  nodes.forEach(n => {                      // edges first so nodes draw on top
    if (!n.parent) return;
    const p = n.parent, my = (p.y + n.y) / 2;
    edgeEls[n.id] = el("path", { class: "edge hidden", d: `M${p.x},${p.y} C${p.x},${my} ${n.x},${my} ${n.x},${n.y}` }, treeSvg);
  });
  nodes.forEach(n => {
    const g = el("g", { class: "node hidden", transform: `translate(${n.x},${n.y})` }, treeSvg);
    if (!n.parent) { el("rect", { x: -25, y: -13, width: 50, height: 26, rx: 13 }, g); el("text", {}, g).textContent = "Start"; }
    else {
      el("circle", { r: 14 }, g); el("text", {}, g).textContent = "c" + n.col;
      if (n.status === "invalid") el("text", { class: "tag", y: 26 }, g).textContent = n.reason.type === "column" ? "col" : "diag";
    }
    const title = el("title", {}, g);
    title.textContent = n.parent ? `Row ${n.row}, column ${n.col}` + (n.status === "invalid" ? ` - invalid: ${n.reason.type} conflict with (R${n.reason.row}, C${n.reason.col})` : "") : "Start: empty board";
    nodeEls[n.id] = g;
  });
  for (let r = 0; r <= N; r++) {            // row labels beside the tree
    const d = document.createElement("div");
    d.style.top = (PADY + r * DY) + "px"; d.textContent = r === 0 ? "Start" : "Row " + r;
    $("levels").appendChild(d);
  }
  $("levels").style.height = treeH + "px";

  /* ---------- 3. Replay state ---------- */
  const state = new Array(nodes.length).fill("hidden");
  let pos = 0;             // number of steps applied
  let timer = null;
  const found = [];
  let stats = { nodes: 0, invalid: 0 };

  function apply(s) {
    const n = s.node;
    switch (s.type) {
      case "try": state[n.id] = "trying"; stats.nodes++; break;
      case "invalid": state[n.id] = "invalid"; stats.invalid++; break;
      case "place": state[n.id] = "placed"; break;
      case "solution": state[n.id] = "solution"; found.push(solutions[s.index - 1]); break;
      case "backtrack": state[n.id] = n.onSolution ? "solution" : "done"; break;
      case "start": state[n.id] = "placed"; break;
      case "done": state[n.id] = "solution"; break;
    }
  }

  /* ---------- 4. Rendering ---------- */
  const SQ = 80, OFF = 28;
  const cx = c => OFF + (c - 0.5) * SQ, cy = r => OFF + (r - 0.5) * SQ;

  function drawBoard(s) {
    const b = $("board"); b.innerHTML = "";
    for (let r = 1; r <= N; r++) for (let c = 1; c <= N; c++)
      el("rect", { x: OFF + (c - 1) * SQ, y: OFF + (r - 1) * SQ, width: SQ, height: SQ, fill: (r + c) % 2 ? "#b9c4da" : "#eef1f7" }, b);
    for (let i = 1; i <= N; i++) {          // coordinates
      el("text", { x: cx(i), y: 16, "text-anchor": "middle", "font-size": 13, fill: "#5d6b82" }, b).textContent = "C" + i;
      el("text", { x: 14, y: cy(i) + 4, "text-anchor": "middle", "font-size": 13, fill: "#5d6b82" }, b).textContent = "R" + i;
    }
    if (!s) return;
    if (s.row) el("rect", { x: OFF, y: OFF + (s.row - 1) * SQ, width: SQ * N, height: SQ, fill: "none", stroke: "#2b5fd9", "stroke-width": 3, "stroke-dasharray": "6 4" }, b);
    if (s.type === "invalid") {             // line from the attacking queen to the rejected square
      const q = s.reason;
      el("line", { x1: cx(q.col), y1: cy(q.row), x2: cx(s.col), y2: cy(s.row), stroke: "#d93025", "stroke-width": 4, "stroke-dasharray": "8 5", "stroke-linecap": "round" }, b);
      el("rect", { x: OFF + (s.col - 1) * SQ + 2, y: OFF + (s.row - 1) * SQ + 2, width: SQ - 4, height: SQ - 4, fill: "rgba(217,48,37,.25)", stroke: "#d93025", "stroke-width": 3 }, b);
    }
    if (s.type === "backtrack")
      el("rect", { x: OFF + (s.col - 1) * SQ + 2, y: OFF + (s.row - 1) * SQ + 2, width: SQ - 4, height: SQ - 4, fill: "none", stroke: "#2b5fd9", "stroke-width": 3, "stroke-dasharray": "5 4" }, b);
    s.queens.forEach(([r, c]) => {
      const solved = s.type === "solution";
      el("text", { x: cx(c), y: cy(r) + 14, "text-anchor": "middle", "font-size": 46, fill: solved ? "#1e8e3e" : "#16213a" }, b).textContent = "♛";
    });
    if (s.type === "try" || s.type === "invalid") {   // the queen being tried
      const bad = s.type === "invalid";
      el("text", { x: cx(s.col), y: cy(s.row) + 14, "text-anchor": "middle", "font-size": 46, fill: bad ? "#d93025" : "#e09b00", opacity: .9 }, b).textContent = "♛";
      if (bad) el("text", { x: cx(s.col) + 22, y: cy(s.row) - 16, "text-anchor": "middle", "font-size": 22, "font-weight": 700, fill: "#d93025" }, b).textContent = "✕";
    }
  }

  const where = (r, c) => `(R${r}, C${c})`;
  function reasonText(rs) { return `${rs.type === "column" ? "Column" : "Diagonal"} conflict with queen at ${where(rs.row, rs.col)}`; }

  function describe(s) {
    const n = s.node, r = n.row, c = n.col;
    switch (s.type) {
      case "start": return { banner: ["READY", "idle"], row: "–", col: "–", action: "Solve(1) called on an empty board", reason: "–", key: "head",
        msg: "Empty board. Solve(1) begins: place one queen in row 1." };
      case "try": return { banner: ["TRYING", "trying"], row: r, col: c, action: "Trying queen at " + where(r, c), reason: "checking IsSafe…", key: "check",
        msg: `Row ${r}: try column ${c}. Check it against the ${r - 1} queen(s) already placed.` };
      case "invalid": return { banner: ["INVALID", "invalid"], row: r, col: c, action: "Prune branch", reason: reasonText(s.reason), key: "prune", bad: true,
        msg: `${where(r, c)} is unsafe (${reasonText(s.reason).toLowerCase()}). The branch is marked red and nothing below it is explored.` };
      case "place": return { banner: ["VALID", "valid"], row: r, col: c, action: "Place queen, then Solve(" + (r + 1) + ")", reason: "No column or diagonal conflict", key: "place",
        msg: `${where(r, c)} is safe. Queen placed; recurse into row ${r + 1 > N ? "5 (all queens placed)" : r + 1}.` };
      case "solution": return { banner: ["SOLUTION " + s.index, "solution"], row: N, col: c, action: "Record solution " + s.index, reason: "All " + N + " queens are mutually safe", key: "solution",
        msg: `Solution ${s.index}: columns (${solutions[s.index - 1].join(", ")}) for rows 1-${N}. Backtrack to look for more.` };
      case "backtrack": {
        const dead = n.children.length > 0 && n.children.every(k => k.status === "invalid");
        const leafSol = n.solution;
        return { banner: ["BACKTRACK", "backtrack"], row: r, col: c, action: "Remove queen from " + where(r, c) + ", try next column",
          reason: leafSol ? "Solution already recorded" : dead ? `Dead end: no safe column in row ${r + 1}` : "All choices below this queen explored", key: "remove",
          msg: leafSol ? `Solution recorded; remove the queen from ${where(r, c)} and continue.`
            : dead ? `Every column of row ${r + 1} conflicts. Return from Solve(${r + 1}) and remove the queen from ${where(r, c)}.`
            : `All choices below ${where(r, c)} are explored. Return from Solve(${r + 1}) and remove the queen.` };
      }
      case "done": return { banner: ["DONE", "solution"], row: "–", col: "–", action: "Search complete", reason: "–", key: null,
        msg: `Whole tree explored: ${stats.nodes} nodes, ${stats.invalid} invalid (red), ${solutions.length} solutions.` };
    }
  }

  function render() {
    const s = pos > 0 ? steps[pos - 1] : null;
    nodes.forEach(n => {
      const st = state[n.id], hide = st === "hidden";
      nodeEls[n.id].setAttribute("class", "node " + (hide ? "hidden" : st) + (s && s.node === n && s.type !== "done" ? " current" : ""));
      if (edgeEls[n.id]) edgeEls[n.id].setAttribute("class", "edge " + (hide ? "hidden" : st === "done" ? "" : st));
    });
    if (s && s.node.parent) nodeEls[s.node.id].parentNode.appendChild(nodeEls[s.node.id]);   // draw current on top
    const d = s ? describe(s) : { banner: ["READY", "idle"], row: "–", col: "–", action: "–", reason: "–", key: null, msg: "Press Start to run the backtracking search." };
    drawBoard(s && s.type !== "done" ? { ...s, row: s.type === "start" ? 0 : s.node.row, col: s.node.col } : s);
    $("banner").textContent = d.banner[0]; $("banner").className = "banner " + d.banner[1];
    $("s-row").textContent = d.row; $("s-col").textContent = d.col; $("s-action").textContent = d.action; $("s-reason").textContent = d.reason;
    const q = s ? s.queens : [];
    $("s-queens").textContent = q.length ? q.map(x => where(x[0], x[1])).join(" ") : "none";
    $("message").textContent = d.msg;
    document.querySelectorAll("#pseudo span").forEach(sp => {
      const on = d.key && sp.dataset.k === d.key;
      sp.classList.toggle("on", !!on); sp.classList.toggle("bad", !!(on && d.bad));
    });
    $("c-step").textContent = pos; $("c-total").textContent = steps.length;
    $("c-nodes").textContent = stats.nodes; $("c-invalid").textContent = stats.invalid; $("c-sol").textContent = found.length;
    $("solutions").innerHTML = "";
    found.forEach((f, i) => { const sp = document.createElement("span"); sp.textContent = `Solution ${i + 1}: columns (${f.join(", ")})`; $("solutions").appendChild(sp); });
    $("btn-next").disabled = pos >= steps.length;
    $("btn-start").disabled = !!timer;
    $("btn-pause").disabled = !timer;
    $("btn-start").textContent = pos >= steps.length ? "▶ Replay" : pos > 0 ? "▶ Resume" : "▶ Start";
    followCurrent(s);
  }

  function followCurrent(s) {               // keep the active node visible in the scrollable tree
    if (!s || document.body.classList.contains("export")) return;
    const sc = $("treeScroll"), target = s.node.x - sc.clientWidth / 2;
    sc.scrollTo({ left: Math.max(0, target), behavior: "smooth" });
  }

  /* ---------- 5. Controls ---------- */
  const delay = () => [1400, 1000, 650, 350, 140][$("speed").value - 1];
  function stepForward() { if (pos < steps.length) apply(steps[pos++]); render(); }
  function stop() { clearTimeout(timer); timer = null; }
  function tick() {
    if (pos >= steps.length) { stop(); render(); return; }
    stepForward();
    timer = pos >= steps.length ? null : setTimeout(tick, delay());
    if (!timer) render();
  }
  function reset() {
    stop(); pos = 0; found.length = 0; stats = { nodes: 0, invalid: 0 };
    state.fill("hidden"); $("treeScroll").scrollLeft = 0; render();
  }
  $("btn-start").onclick = () => { if (pos >= steps.length) reset(); stop(); timer = setTimeout(tick, 0); render(); };
  $("btn-pause").onclick = () => { stop(); render(); };
  $("btn-next").onclick = () => { stop(); stepForward(); };
  $("btn-reset").onclick = reset;

  /* ---------- 6. Init ---------- */
  $("c-total").textContent = steps.length;
  if (location.hash === "#full") {          // static export of the complete tree (for Visualization.png)
    document.body.classList.add("export");
    steps.forEach(apply); pos = steps.length;
    nodes.forEach(n => { if (n.status === "valid" && !n.onSolution) state[n.id] = "done"; });
    render();
    document.title = "N-Queens N=4 state-space tree";
  } else {
    render();
  }
})();
