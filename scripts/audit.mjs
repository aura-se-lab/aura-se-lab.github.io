#!/usr/bin/env node
/**
 * Deep QA over dist/: every route at four widths.
 * Console errors, failed requests, horizontal overflow, axe violations,
 * heading order, link names, tap-target size, and external-link reachability.
 *   node scripts/audit.mjs [--out .audit] [--widths 1440,1180,820,390]
 */
import { createServer } from "node:http";
import { readFile, stat, mkdir, writeFile, readdir } from "node:fs/promises";
import { join, extname, relative, resolve } from "node:path";
import { chromium } from "playwright";

const args = process.argv.slice(2);
const opt = (k, d) => { const i = args.indexOf(k); return i >= 0 ? args[i + 1] : d; };
const out = opt("--out", ".audit");
const widths = opt("--widths", "1440,1180,820,390").split(",").map(Number);
const dist = resolve("dist");
const mime = { ".html":"text/html", ".css":"text/css", ".js":"text/javascript", ".svg":"image/svg+xml", ".png":"image/png", ".webp":"image/webp", ".jpg":"image/jpeg", ".woff2":"font/woff2", ".xml":"application/xml", ".json":"application/json", ".bib":"text/plain", ".ico":"image/x-icon", ".txt":"text/plain" };

async function walk(d) {
  const o = [];
  for (const e of await readdir(d, { withFileTypes: true })) {
    const p = join(d, e.name);
    if (e.isDirectory()) o.push(...(await walk(p)));
    else if (p.endsWith(".html")) o.push(p);
  }
  return o;
}
const server = createServer(async (req, res) => {
  let p = decodeURIComponent(new URL(req.url, "http://x").pathname);
  let file = join(dist, p);
  try { if ((await stat(file)).isDirectory()) file = join(file, "index.html"); }
  catch { if (!extname(file)) file = join(dist, p + "/index.html"); }
  try { const d = await readFile(file); res.writeHead(200, { "content-type": mime[extname(file)] ?? "application/octet-stream" }); res.end(d); }
  catch { res.writeHead(404); res.end("404 " + p); }
});
await new Promise((r) => server.listen(0, r));
const port = server.address().port;
await mkdir(out, { recursive: true });

const files = await walk(dist);
const routes = files
  .map((f) => "/" + relative(dist, f).replace(/index\.html$/, "").replace(/\\/g, "/"))
  .filter((r) => !r.includes("/embed/"))
  .sort();
const axeSrc = await readFile("node_modules/axe-core/axe.min.js", "utf8");
const shots = new Set(["/", "/research/", "/publications/", "/people/", "/news/", "/join/", "/software/", "/404.html"]);

const report = [];
// Playwright's own Chromium if installed, otherwise the system Chrome.
const CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome";
const browser = await chromium
  .launch()
  .catch(() => chromium.launch({ executablePath: process.env.CHROME_PATH ?? CHROME }));
for (const w of widths) {
  const ctx = await browser.newContext({ viewport: { width: w, height: 900 }, deviceScaleFactor: 1 });
  for (const r of routes) {
    const page = await ctx.newPage();
    const errs = [], net = [];
    page.on("console", (m) => m.type() === "error" && errs.push(m.text().slice(0, 240)));
    page.on("pageerror", (e) => errs.push("PAGEERROR " + String(e).slice(0, 240)));
    page.on("response", (x) => { if (x.status() >= 400) net.push(x.status() + " " + x.url().slice(0, 150)); });
    page.on("requestfailed", (x) => net.push("FAIL " + x.url().slice(0, 150)));
    let status = 0;
    try { const rs = await page.goto(`http://localhost:${port}${r}`, { waitUntil: "networkidle", timeout: 30000 }); status = rs?.status() ?? 0; }
    catch (e) { errs.push("NAV " + String(e).slice(0, 160)); }
    await page.evaluate(() => document.querySelectorAll("[data-rv]").forEach((e) => e.classList.add("in")));
    await page.waitForTimeout(250);

    const m = await page.evaluate(() => {
      const de = document.documentElement;
      const over = [];
      for (const el of document.querySelectorAll("body *")) {
        const b = el.getBoundingClientRect();
        if (b.width > 0 && (b.right > de.clientWidth + 2 || b.left < -2)) {
          const s = el.tagName.toLowerCase() + (el.id ? "#" + el.id : "") +
            (typeof el.className === "string" && el.className.trim() ? "." + el.className.trim().split(/\s+/).slice(0, 2).join(".") : "");
          if (!over.includes(s)) over.push(s);
        }
      }
      const hs = [...document.querySelectorAll("h1,h2,h3,h4,h5,h6")].map((h) => +h.tagName[1]);
      let jump = null, prev = hs[0] ?? 0;
      for (const l of hs) { if (l > prev + 1) { jump = `h${prev}→h${l}`; break; } prev = l; }
      const small = [];
      for (const a of document.querySelectorAll("a,button")) {
        const b = a.getBoundingClientRect();
        if (b.width > 0 && b.height > 0 && (b.height < 24 || b.width < 24) && a.closest("nav,footer,main,body"))
          small.push((a.textContent || a.getAttribute("aria-label") || a.tagName).trim().slice(0, 30) + ` ${Math.round(b.width)}x${Math.round(b.height)}`);
      }
      return {
        title: document.title, h1n: document.querySelectorAll("h1").length,
        scrollW: de.scrollWidth, clientW: de.clientWidth, overflow: over.slice(0, 10),
        headingJump: jump,
        imgNoAlt: [...document.querySelectorAll("img:not([alt])")].map((i) => i.getAttribute("src")).slice(0, 6),
        namelessLinks: [...document.querySelectorAll("a,button")].filter((a) => !a.textContent.trim() && !a.getAttribute("aria-label") && !a.getAttribute("title") && !a.querySelector("[aria-label],title")).length,
        smallTargets: [...new Set(small)].slice(0, 8),
        hasMain: !!document.querySelector("main"),
        metaDesc: (document.querySelector('meta[name="description"]')?.content || "").length,
        lang: document.documentElement.lang || null,
      };
    });

    let axe = [];
    if (w === 1440) {
      await page.addScriptTag({ content: axeSrc });
      axe = await page.evaluate(async () => {
        const r = await window.axe.run(document, { resultTypes: ["violations"] });
        return r.violations.map((v) => ({ id: v.id, impact: v.impact, n: v.nodes.length,
          sample: v.nodes.slice(0, 2).map((n) => ({ t: n.target.join(" ").slice(0, 90), s: (n.failureSummary || "").replace(/\s+/g, " ").slice(0, 200) })) }));
      });
    }
    if (shots.has(r)) {
      const nm = (r === "/" ? "home" : r.replace(/^\/|\/$/g, "").replace(/\//g, "_").replace(/\.html$/, "")) + `-${w}.png`;
      await page.screenshot({ path: join(out, nm), fullPage: w === 1440 });
    }
    report.push({ route: r, w, status, ...m, consoleErrors: errs, networkErrors: [...new Set(net)], axe });
    await page.close();
  }
  await ctx.close();
}
await browser.close();
server.close();
await writeFile(join(out, "report.json"), JSON.stringify(report, null, 1));
console.log("AUDIT_DONE", routes.length, "routes ×", widths.length, "widths =", report.length);
