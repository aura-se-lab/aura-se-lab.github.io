#!/usr/bin/env node
/**
 * Full-page screenshots of the built site at three widths, for visual review.
 *   node scripts/screenshots.mjs [--out .screens] [--paths /,/publications/,...]
 * Serves ./dist on a random port with Astro's preview-compatible static server.
 */
import { createServer } from "node:http";
import { readFile, stat, mkdir } from "node:fs/promises";
import { join, extname } from "node:path";
import { chromium } from "playwright";

const args = process.argv.slice(2);
const opt = (k, d) => {
  const i = args.indexOf(k);
  return i >= 0 ? args[i + 1] : d;
};
const out = opt("--out", ".screens");
const paths = opt("--paths", "/,/research/,/publications/,/people/,/news/,/join/").split(",");
const widths = (opt("--widths", "1440,1024,390")).split(",").map(Number);
const dist = "dist";
const mime = { ".html": "text/html", ".css": "text/css", ".js": "text/javascript", ".svg": "image/svg+xml", ".png": "image/png", ".webp": "image/webp", ".jpg": "image/jpeg", ".woff2": "font/woff2", ".xml": "application/xml", ".json": "application/json", ".bib": "text/plain", ".ico": "image/x-icon" };

const server = createServer(async (req, res) => {
  let p = decodeURIComponent(new URL(req.url, "http://x").pathname);
  let file = join(dist, p);
  try {
    if ((await stat(file)).isDirectory()) file = join(file, "index.html");
  } catch {
    if (!extname(file)) file = join(dist, p + "/index.html");
  }
  try {
    const data = await readFile(file);
    res.writeHead(200, { "content-type": mime[extname(file)] ?? "application/octet-stream" });
    res.end(data);
  } catch {
    res.writeHead(404);
    res.end("not found " + p);
  }
});
await new Promise((r) => server.listen(0, r));
const port = server.address().port;
await mkdir(out, { recursive: true });

const browser = await chromium.launch();
for (const w of widths) {
  const ctx = await browser.newContext({ viewport: { width: w, height: 900 }, deviceScaleFactor: 1 });
  const page = await ctx.newPage();
  const errors = [];
  page.on("pageerror", (e) => errors.push(e.message));
  page.on("console", (m) => m.type() === "error" && errors.push(m.text()));
  for (const p of paths) {
    const url = `http://localhost:${port}${p}`;
    const res = await page.goto(url, { waitUntil: "networkidle" });
    const name = (p === "/" ? "home" : p.replace(/^\/|\/$/g, "").replace(/\//g, "_")) + `-${w}.png`;
    await page.screenshot({ path: join(out, name), fullPage: true });
    const overflow = await page.evaluate(() => document.documentElement.scrollWidth > document.documentElement.clientWidth);
    console.log(`${res?.status()} ${p} @${w} → ${name}${overflow ? "  ⚠ horizontal overflow" : ""}`);
  }
  if (errors.length) console.log(`  console errors @${w}:`, errors);
  await ctx.close();
}
await browser.close();
server.close();
