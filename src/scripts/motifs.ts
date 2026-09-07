/**
 * Four generative motifs, one per research direction. Each says something
 * about the work rather than decorating it: bits being dropped, a program
 * being parsed, a measurement refusing to settle, work moving down a pipeline.
 *
 * All of them are cheap (a few hundred primitives), pause when off-screen,
 * and stop dead under prefers-reduced-motion.
 */
export type Motif = "quantize" | "parse" | "measure" | "flow";

interface Ctl { destroy(): void; energy(v: number): void }

export function mountMotif(cv: HTMLCanvasElement, kind: Motif, color: string): Ctl {
  const ctx = cv.getContext("2d")!;
  const still = matchMedia("(prefers-reduced-motion: reduce)").matches;
  let w = 0, h = 0, raf = 0, t = 0, e = 0.35, visible = true;

  const fit = () => {
    const r = cv.getBoundingClientRect();
    const d = Math.min(devicePixelRatio || 1, 2);
    w = r.width; h = r.height;
    cv.width = Math.max(1, w * d); cv.height = Math.max(1, h * d);
    ctx.setTransform(d, 0, 0, d, 0, 0);
  };
  fit();
  const ro = new ResizeObserver(fit); ro.observe(cv);
  const io = new IntersectionObserver(([x]) => { visible = x.isIntersecting; }, { threshold: 0 });
  io.observe(cv);

  const rgba = (a: number) => color.startsWith("#")
    ? `${color}${Math.round(a * 255).toString(16).padStart(2, "0")}`
    : color.replace(/rgb\(([^)]+)\)/, (_, c) => `rgba(${c},${a})`);

  // ── quantize: a dense field losing precision, sweep by sweep ──────────────
  const quantize = () => {
    const step = 13, sweep = ((t * 0.00022) % 1.6) - 0.3;
    for (let y = step; y < h; y += step) {
      for (let x = step; x < w; x += step) {
        const p = x / w;
        const past = p < sweep;
        const k = past ? 3 : 1;                       // coarser after the sweep
        if (past && ((x / step) % k || (y / step) % k)) continue;
        const d = Math.abs(p - sweep);
        const lift = d < 0.08 ? (1 - d / 0.08) : 0;
        ctx.fillStyle = rgba((past ? 0.5 : 0.19) + lift * 0.45);
        const s = past ? 2.4 : 1.5;
        ctx.fillRect(x - s / 2, y - s / 2 + lift * 5, s, s);
      }
    }
  };

  // ── parse: a syntax tree drawing itself, then re-growing ──────────────────
  type N = { x: number; y: number; p?: N };
  let tree: N[] = [];
  const grow = () => {
    tree = [];
    const root: N = { x: w / 2, y: 22 };
    tree.push(root);
    const depthMax = w < 260 ? 3 : 4;
    const walk = (n: N, depth: number, spread: number) => {
      if (depth > depthMax || tree.length > 34) return;
      const kids = depth < 2 ? 2 : Math.random() < 0.6 ? 2 : 1;
      for (let i = 0; i < kids; i++) {
        const off = (i - (kids - 1) / 2) * spread;
        const c: N = { x: n.x + off + (Math.random() - 0.5) * 10, y: n.y + (h - 44) / (depthMax + 1), p: n };
        tree.push(c);
        walk(c, depth + 1, spread * 0.52);
      }
    };
    walk(root, 0, w * 0.26);
  };
  const parse = () => {
    if (!tree.length || w !== (tree as any)._w) { grow(); (tree as any)._w = w; }
    const cycle = (t * 0.00035) % 1.5;
    const shown = Math.min(1, cycle / 0.85) * tree.length;
    ctx.lineWidth = 1.1;
    tree.forEach((n, i) => {
      if (i > shown) return;
      const a = Math.min(1, shown - i);
      if (n.p) {
        ctx.strokeStyle = rgba(0.3 * a * (0.6 + e));
        ctx.beginPath(); ctx.moveTo(n.p.x, n.p.y); ctx.lineTo(n.x, n.y); ctx.stroke();
      }
      ctx.fillStyle = rgba((i ? 0.55 : 0.9) * a * (0.6 + e));
      ctx.beginPath(); ctx.arc(n.x, n.y, i ? 2.2 : 3.4, 0, 7); ctx.fill();
    });
    if (cycle > 1.45) tree = [];
  };

  // ── measure: estimates jittering inside their intervals, then settling ────
  const measure = () => {
    const n = Math.max(6, Math.floor(w / 42));
    const cycle = (Math.sin(t * 0.0007) + 1) / 2;          // 0 = noisy, 1 = settled
    for (let i = 0; i < n; i++) {
      const x = ((i + 0.5) / n) * w;
      const seed = Math.sin(i * 12.9898) * 43758.5453;
      const base = h * (0.34 + 0.34 * ((seed % 1) + 1) % 1);
      const spread = (1 - cycle) * h * 0.2 + 4;
      const jit = Math.sin(t * 0.002 + i) * (1 - cycle) * 9;
      ctx.strokeStyle = rgba(0.18 + 0.14 * e);
      ctx.lineWidth = 1;
      ctx.beginPath(); ctx.moveTo(x, base - spread + jit); ctx.lineTo(x, base + spread + jit); ctx.stroke();
      ctx.beginPath(); ctx.moveTo(x - 3.5, base - spread + jit); ctx.lineTo(x + 3.5, base - spread + jit);
      ctx.moveTo(x - 3.5, base + spread + jit); ctx.lineTo(x + 3.5, base + spread + jit); ctx.stroke();
      ctx.fillStyle = rgba(0.42 + 0.4 * cycle * (0.5 + e));
      ctx.beginPath(); ctx.arc(x, base + jit, 2.6, 0, 7); ctx.fill();
    }
  };

  // ── flow: work moving through stages, some of it forking ─────────────────
  const lanes = [0.3, 0.5, 0.7];
  const flow = () => {
    const stages = 4;
    ctx.lineWidth = 1;
    for (let s = 0; s <= stages; s++) {
      const x = (s / stages) * (w - 24) + 12;
      ctx.strokeStyle = rgba(0.14);
      ctx.beginPath(); ctx.moveTo(x, h * 0.2); ctx.lineTo(x, h * 0.8); ctx.stroke();
    }
    for (let i = 0; i < 22; i++) {
      const sp = 0.00006 + (i % 5) * 0.000022;
      const p = ((t * sp * (0.5 + e)) + i / 22) % 1;
      const lane = lanes[i % lanes.length] + Math.sin(p * 6.3 + i) * 0.045;
      const x = 12 + p * (w - 24);
      const y = lane * h;
      ctx.fillStyle = rgba(0.22 + 0.5 * (1 - Math.abs(p - 0.5) * 2) * (0.5 + e));
      ctx.beginPath(); ctx.roundRect(x - 5, y - 2, 10, 4, 2); ctx.fill();
    }
  };

  const draw = () => {
    ctx.clearRect(0, 0, w, h);
    if (kind === "quantize") quantize();
    else if (kind === "parse") parse();
    else if (kind === "measure") measure();
    else flow();
  };

  const loop = (ts: number) => {
    t = ts;
    if (visible) draw();
    raf = requestAnimationFrame(loop);
  };
  if (still) draw(); else raf = requestAnimationFrame(loop);

  return {
    destroy() { cancelAnimationFrame(raf); ro.disconnect(); io.disconnect(); },
    energy(v: number) { e = v; },
  };
}
