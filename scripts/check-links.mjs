#!/usr/bin/env node
/** Offline internal link check over dist/: every href/src that points inside the site must resolve. */
import { readdir, readFile, stat } from "node:fs/promises";
import { join, dirname, resolve, extname } from "node:path";

const dist = resolve("dist");
async function walk(d) {
  const out = [];
  for (const e of await readdir(d, { withFileTypes: true })) {
    const p = join(d, e.name);
    if (e.isDirectory()) out.push(...(await walk(p)));
    else if (p.endsWith(".html")) out.push(p);
  }
  return out;
}
async function exists(p) {
  try {
    const s = await stat(p);
    return s.isFile() || (s.isDirectory() && (await exists(join(p, "index.html"))));
  } catch {
    return false;
  }
}
const files = await walk(dist);
let bad = 0, checked = 0;
const ids = new Map();
for (const f of files) {
  const html = await readFile(f, "utf-8");
  ids.set(f, new Set([...html.matchAll(/\sid="([^"]+)"/g)].map((m) => m[1])));
}
for (const f of files) {
  const html = await readFile(f, "utf-8");
  for (const m of html.matchAll(/\s(?:href|src)="([^"]+)"/g)) {
    let u = m[1];
    if (/^(https?:|mailto:|tel:|data:|#|javascript:)/.test(u)) {
      if (u.startsWith("#") && u.length > 1 && !ids.get(f).has(u.slice(1))) { console.log(`✗ ${f.replace(dist, "")} → ${u} (missing anchor)`); bad++; }
      continue;
    }
    const [path, hash] = u.split("#");
    const target = path.startsWith("/") ? join(dist, path.split("?")[0]) : resolve(dirname(f), path.split("?")[0]);
    checked++;
    if (!(await exists(target))) { console.log(`✗ ${f.replace(dist, "")} → ${u}`); bad++; continue; }
    if (hash) {
      const tf = (await stat(target).then((s) => s.isDirectory())) ? join(target, "index.html") : target;
      if (extname(tf) === ".html" && !ids.get(tf)?.has(hash)) { console.log(`✗ ${f.replace(dist, "")} → ${u} (missing anchor)`); bad++; }
    }
  }
}
console.log(`${checked} internal links checked in ${files.length} pages · ${bad} broken`);
process.exit(bad ? 1 : 0);
