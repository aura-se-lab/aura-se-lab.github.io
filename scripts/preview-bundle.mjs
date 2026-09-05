#!/usr/bin/env node
/**
 * Pack the static build (dist/) into ONE self-contained HTML file that can be
 * opened anywhere — every page, stylesheet, font and image inlined — with a thin
 * navigation chrome around a srcdoc iframe. Used to share a clickable preview
 * before the site is deployed.
 *
 *   npm run build && node scripts/preview-bundle.mjs [--out preview/auralab-preview.html]
 */
import { readdir, readFile, writeFile, mkdir, stat } from "node:fs/promises";
import { join, extname, relative, dirname } from "node:path";

const args = process.argv.slice(2);
const outPath = args[args.indexOf("--out") + 1] && args.includes("--out") ? args[args.indexOf("--out") + 1] : "preview/auralab-preview.html";
const dist = "dist";
const mime = { ".css": "text/css", ".js": "text/javascript", ".svg": "image/svg+xml", ".png": "image/png", ".webp": "image/webp", ".jpg": "image/jpeg", ".woff2": "font/woff2", ".woff": "font/woff" };
const KEEP_FONT_SUBSETS = /-(latin|latin-ext)-/;

async function walk(d) {
  const out = [];
  for (const e of await readdir(d, { withFileTypes: true })) {
    const p = join(d, e.name);
    if (e.isDirectory()) out.push(...(await walk(p)));
    else out.push(p);
  }
  return out;
}

const files = await walk(dist);
const pages = {};
for (const f of files.filter((f) => f.endsWith(".html") && !f.startsWith(join(dist, "og")))) {
  let html = await readFile(f, "utf-8");
  const route = "/" + relative(dist, dirname(f)).replace(/\\/g, "/").replace(/^\.$/, "");
  const path = route === "/" ? "/" : route.replace(/\/?$/, "/");
  // the prefetch runtime has nothing to prefetch inside a srcdoc document
  html = html.replace(/<script type="module" src="\/_astro\/page\.[^"]+"><\/script>/, "");
  // 404 page keeps its path
  pages[f.endsWith("404.html") ? "/404/" : path] = html;
}

// ── assets: css (with fonts inlined), images ─────────────────────────────────
const assets = {};
const b64 = (buf, m) => `data:${m};base64,${buf.toString("base64")}`;
for (const f of files.filter((f) => f.includes("/_astro/"))) {
  const name = "/_astro/" + f.split("/_astro/")[1];
  const ext = extname(f);
  if (ext === ".css") {
    let css = await readFile(f, "utf-8");
    // drop @font-face blocks for subsets we don't ship, inline the rest
    css = css.replace(/@font-face\{[^}]*\}/g, (block) => {
      const m = block.match(/url\(([^)]+\.woff2)\)/);
      if (!m) return block;
      const url = m[1].replace(/["']/g, "");
      if (!KEEP_FONT_SUBSETS.test(url)) return "";
      return block;
    });
    for (const m of [...css.matchAll(/url\((\/_astro\/[^)]+)\)/g)]) {
      const p = join(dist, m[1]);
      try {
        const buf = await readFile(p);
        css = css.split(m[0]).join(`url(${b64(buf, mime[extname(p)] ?? "application/octet-stream")})`);
      } catch {}
    }
    assets[name] = { kind: "css", data: css };
  } else if (mime[ext] && ext !== ".woff2" && ext !== ".js") {
    assets[name] = { kind: "img", data: b64(await readFile(f), mime[ext]) };
  }
}
for (const f of ["favicon.svg", "apple-touch-icon.png"]) {
  try { assets["/" + f] = { kind: "img", data: b64(await readFile(join(dist, f)), mime[extname(f)]) }; } catch {}
}

// ── page list for the switcher ───────────────────────────────────────────────
const titleOf = (html) => (html.match(/<title>([^<]*)<\/title>/)?.[1] ?? "").replace(/&amp;/g, "&").replace(/ · AURA Lab$/, "");
const groups = [
  { label: "Site", test: (p) => ["/", "/research/", "/publications/", "/people/", "/news/", "/join/", "/404/"].includes(p) },
  { label: "Research threads", test: (p) => p.startsWith("/research/") },
  { label: "People", test: (p) => p.startsWith("/people/") },
  { label: "News", test: (p) => p.startsWith("/news/") },
  { label: "Publications", test: (p) => p.startsWith("/publications/") },
];
const order = ["/", "/research/", "/publications/", "/people/", "/news/", "/join/", "/404/"];
const index = groups.map((g) => ({
  label: g.label,
  items: Object.keys(pages)
    .filter((p) => g.test(p))
    .sort((a, b) => (order.indexOf(a) + 1 || 99) - (order.indexOf(b) + 1 || 99) || a.localeCompare(b))
    .map((p) => ({ path: p, title: titleOf(pages[p]) || p })),
})).filter((g) => g.items.length);

const json = (o) => JSON.stringify(o).replace(/<\//g, "<\\/");
const chromeCss = assets["/_astro/" + Object.keys(assets).find((k) => k.endsWith(".css"))?.split("/_astro/")[1]]?.data ?? "";
const fontFaces = (chromeCss.match(/@font-face\{[^}]*\}/g) ?? []).join("\n");

const harness = `<title>AURA Lab Preview</title>
<style>
${fontFaces}
:root{--ink:#050505;--paper:#ffffff;--ground:#efefec;--line:#dcdcd8;--mute:#5a5a56;--faint:#8e8e89;--accent:#15803d;--accent-bright:#16a34a;--chrome:#050505;--chrome-fg:#ffffff;--chrome-mute:rgba(255,255,255,.6)}
@media (prefers-color-scheme: dark){:root:not([data-theme="light"]){--ground:#161616;--line:#2a2a2a;--mute:#a9a9a4;--faint:#7c7c78}}
:root[data-theme="dark"]{--ground:#161616;--line:#2a2a2a;--mute:#a9a9a4;--faint:#7c7c78}
*{box-sizing:border-box}
html,body{height:100%}
body{margin:0;background:var(--ground);font-family:"Inter Tight Variable","Inter Tight",system-ui,sans-serif;color:var(--ink);display:flex;flex-direction:column}
.bar{flex:none;display:flex;align-items:center;gap:12px;padding:0 16px;height:52px;background:var(--chrome);color:var(--chrome-fg);border-bottom:1px solid var(--accent);font-size:13px;overflow:hidden}
.bar>*{flex:none;min-width:0}
.brand{display:flex;align-items:baseline;gap:8px;font-weight:600;letter-spacing:-.01em;white-space:nowrap}
.brand small{font-family:"JetBrains Mono Variable","JetBrains Mono",ui-monospace,monospace;font-weight:500;font-size:10px;letter-spacing:.1em;text-transform:uppercase;color:var(--accent-bright)}
.nav{display:flex;align-items:center;gap:6px}
.nav button,.vp button{height:30px;padding:0 10px;border:1px solid rgba(255,255,255,.18);border-radius:6px;background:transparent;color:var(--chrome-fg);font:inherit;font-size:12.5px;cursor:pointer}
.nav button:disabled{opacity:.35;cursor:default}
.nav button:not(:disabled):hover,.vp button:hover{background:rgba(255,255,255,.08)}
.vp button[aria-pressed="true"]{background:#fff;color:var(--ink);border-color:#fff}
select{height:30px;width:clamp(180px,26vw,360px);padding:0 8px;border:1px solid rgba(255,255,255,.18);border-radius:6px;background:#111;color:#fff;font:inherit;font-size:12.5px}
.path{font-family:"JetBrains Mono Variable","JetBrains Mono",ui-monospace,monospace;font-size:11px;color:var(--chrome-mute);overflow:hidden;text-overflow:ellipsis;white-space:nowrap;flex:1 1 0!important}
.path b{color:#fff;font-weight:500}
.vp{display:flex;gap:4px}
.stage{flex:1;min-height:0;display:flex;justify-content:center;padding:0}
.stage[data-vp="desktop"]{padding:0}
.stage:not([data-vp="desktop"]){padding:20px 0}
iframe{border:0;background:var(--paper);width:100%;height:100%;display:block}
.stage[data-vp="tablet"] iframe{width:1024px;max-width:100%;box-shadow:0 20px 60px -30px rgba(0,0,0,.6);border:1px solid var(--line)}
.stage[data-vp="phone"] iframe{width:390px;max-width:100%;border-radius:18px;box-shadow:0 20px 60px -30px rgba(0,0,0,.6);border:1px solid var(--line)}
.toast{position:fixed;left:50%;bottom:22px;transform:translate(-50%,20px);opacity:0;transition:.2s;background:var(--ink);color:#fff;font-size:13px;padding:10px 14px;border-radius:8px;border-left:3px solid var(--accent);pointer-events:none;max-width:90vw}
.toast.on{opacity:1;transform:translate(-50%,0)}
.note{font-size:11.5px;color:var(--chrome-mute);white-space:nowrap;display:none}
@media (min-width:1500px){.note{display:block}}
@media (max-width:820px){.path{display:none}.brand small{display:none}}
button:focus-visible,select:focus-visible{outline:2px solid var(--accent-bright);outline-offset:2px}
</style>
<div class="bar">
  <div class="brand">auralab.sh <small>preview · astro-rebuild</small></div>
  <div class="nav"><button id="back" title="Back" aria-label="Back" disabled>←</button><button id="fwd" title="Forward" aria-label="Forward" disabled>→</button></div>
  <select id="pick" aria-label="Go to page"></select>
  <div class="path" id="path"></div>
  <span class="note">Static preview — feeds, BibTeX download and OG cards are served by the real site.</span>
  <div class="vp" role="group" aria-label="Viewport">
    <button data-vp="desktop" aria-pressed="true">Desktop</button><button data-vp="tablet" aria-pressed="false">1024</button><button data-vp="phone" aria-pressed="false">Phone</button>
  </div>
</div>
<div class="stage" id="stage" data-vp="desktop"><iframe id="frame" title="Site preview"></iframe></div>
<div class="toast" id="toast" role="status"></div>
<script type="application/json" id="pages">${json(pages)}</script>
<script type="application/json" id="assets">${json(assets)}</script>
<script type="application/json" id="index">${json(index)}</script>
<script>
(() => {
  const PAGES = JSON.parse(document.getElementById("pages").textContent);
  const ASSETS = JSON.parse(document.getElementById("assets").textContent);
  const INDEX = JSON.parse(document.getElementById("index").textContent);
  const frame = document.getElementById("frame"), pick = document.getElementById("pick"), pathEl = document.getElementById("path");
  const back = document.getElementById("back"), fwd = document.getElementById("fwd"), toast = document.getElementById("toast"), stage = document.getElementById("stage");
  const hist = []; let cur = -1; let toastT;

  for (const g of INDEX) {
    const og = document.createElement("optgroup"); og.label = g.label;
    for (const it of g.items) { const o = document.createElement("option"); o.value = it.path; o.textContent = it.title; og.appendChild(o); }
    pick.appendChild(og);
  }

  const SHIM = \`<script>
    history.pushState = history.replaceState = function(){};
    addEventListener("click", function(e){
      const a = e.target.closest && e.target.closest("a[href]"); if (!a) return;
      const href = a.getAttribute("href");
      if (!href || href.startsWith("#")) return;
      if (/^(https?:|mailto:|tel:)/.test(href)) { a.target = "_blank"; a.rel = "noopener"; return; }
      e.preventDefault();
      parent.postMessage({ go: href }, "*");
    }, true);
  <\\/script>\`;

  function render(path) {
    const [p, hash] = path.split("#");
    let html = PAGES[p];
    if (!html) return false;
    html = html.replace(/<link rel="stylesheet" href="(\\/_astro\\/[^"]+\\.css)">/g, (m, u) => ASSETS[u] ? "<style>" + ASSETS[u].data + "</style>" : "");
    html = html.replace(/(src|href)="(\\/(?:_astro\\/)?[^"]+\\.(?:webp|png|jpg|svg))"/g, (m, k, u) => ASSETS[u] ? k + '="' + ASSETS[u].data + '"' : m);
    html = html.replace("<head>", "<head>" + SHIM);
    frame.srcdoc = html;
    if (hash) frame.addEventListener("load", () => { try { frame.contentDocument.getElementById(hash)?.scrollIntoView(); } catch {} }, { once: true });
    pick.value = p;
    pathEl.innerHTML = 'https://auralab.sh<b>' + p + (hash ? "#" + hash : "") + "</b>";
    return true;
  }
  function go(path, push = true) {
    if (!path.startsWith("/")) return;
    const clean = path.split("?")[0];
    const p = clean.split("#")[0].replace(/\\/?$/, "/") + (clean.includes("#") ? "#" + clean.split("#")[1] : "");
    if (!PAGES[p.split("#")[0]]) { say("Not part of this static preview: " + path); return; }
    if (push) { hist.splice(cur + 1); hist.push(p); cur = hist.length - 1; }
    render(p);
    back.disabled = cur <= 0; fwd.disabled = cur >= hist.length - 1;
  }
  function say(msg) { toast.textContent = msg; toast.classList.add("on"); clearTimeout(toastT); toastT = setTimeout(() => toast.classList.remove("on"), 2600); }

  addEventListener("message", (e) => { if (e.data && e.data.go) go(e.data.go); });
  pick.addEventListener("change", () => go(pick.value));
  back.addEventListener("click", () => { if (cur > 0) { cur--; render(hist[cur]); back.disabled = cur <= 0; fwd.disabled = false; } });
  fwd.addEventListener("click", () => { if (cur < hist.length - 1) { cur++; render(hist[cur]); fwd.disabled = cur >= hist.length - 1; back.disabled = false; } });
  document.querySelectorAll(".vp button").forEach((b) => b.addEventListener("click", () => {
    document.querySelectorAll(".vp button").forEach((x) => x.setAttribute("aria-pressed", String(x === b)));
    stage.dataset.vp = b.dataset.vp;
  }));
  go(location.hash && PAGES[location.hash.slice(1)] ? location.hash.slice(1) : "/");
})();
</script>
`;

await mkdir(dirname(outPath), { recursive: true });
await writeFile(outPath, harness);
const size = (await stat(outPath)).size;
console.log(`${Object.keys(pages).length} pages, ${Object.keys(assets).length} assets → ${outPath} (${(size / 1024 / 1024).toFixed(1)} MB)`);
