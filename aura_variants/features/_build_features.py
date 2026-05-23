"""
Build 10 home-page variants by cloning H_cinematic.html and
swapping the <aside id="news"> ... </aside> block with each variant's
signature feature card. All other chrome stays identical.
"""
import re, os, pathlib

ROOT = pathlib.Path(__file__).resolve().parents[2]
SRC  = ROOT / 'aura_variants' / 'H_cinematic.html'
OUT  = ROOT / 'aura_variants' / 'features'
ASSETS_PREFIX = '../../assets/img/wm/'   # because variants sit one level deeper

src = SRC.read_text()

# Re-target the asset/page paths so relative refs work from /features/
def retarget(html):
    html = html.replace('href="aura_variants/', 'href="../')
    html = html.replace('src="../assets/', 'src="../../assets/')
    html = html.replace('href="../assets/', 'href="../../assets/')
    return html

src = retarget(src)

# Locate the news aside (the part we swap)
m = re.search(r'<aside class="r" id="news">.*?</aside>', src, re.DOTALL)
assert m, 'news aside not found'
news_start, news_end = m.start(), m.end()

# Also retarget the "papers/code/forecasts" cross-links inside features
def featurize(content):
    return content

# ── 10 SIGNATURE FEATURE BLOCKS ──────────────────────────────────
# Each is wrapped in <aside class="r" id="featured"> ... </aside>
# Each ships with its own scoped <style> block to avoid leaking
# styles into the home template.

VARIANTS = [
  # 01 — Calibrated Forecasts (Brier scorecard mini)
  {
    'id': 'forecast',
    'name': 'Calibrated Forecasts',
    'tagline': 'A Brier-scored prediction board — the lab\'s public accountability instrument.',
    'block': '''
<style>
.v-fc{background:#fff;border:1px solid var(--rule);border-radius:22px;overflow:hidden;box-shadow:0 50px 100px -32px rgba(6,36,27,.32),0 14px 30px -12px rgba(6,36,27,.18);}
.v-fc .head{padding:16px 22px;background:linear-gradient(135deg,var(--wm-deep),#0a3023);color:#dff0e6;display:flex;align-items:center;justify-content:space-between;gap:8px}
.v-fc .head .l{display:inline-flex;align-items:center;gap:8px;font-family:var(--mono);font-size:10.5px;letter-spacing:.14em;text-transform:uppercase;color:var(--wm-glow)}
.v-fc .head .l .d{width:6px;height:6px;border-radius:50%;background:var(--wm-glow);box-shadow:0 0 0 0 currentColor;animation:vpulse 2s infinite}
.v-fc .head a{color:var(--wm-glow);font-family:var(--mono);font-size:10.5px;letter-spacing:.06em;text-transform:uppercase;text-decoration:none}
@keyframes vpulse{0%{box-shadow:0 0 0 0 currentColor}70%{box-shadow:0 0 0 8px transparent}100%{box-shadow:0 0 0 0 transparent}}
.v-fc .big{padding:24px 22px;background:linear-gradient(135deg,var(--wm-deep) 0%,#0e3528 100%);color:#fff;display:grid;grid-template-columns:auto 1fr;gap:18px;align-items:center;border-bottom:1px solid rgba(164,236,196,.10)}
.v-fc .big .n{font-family:var(--serif);font-size:62px;line-height:1;font-weight:500;letter-spacing:-.025em}
.v-fc .big .n .u{font-family:var(--mono);font-size:13px;color:var(--wm-glow);margin-left:5px}
.v-fc .big .t{font-family:var(--serif);font-size:15px;color:#cfdcd3;line-height:1.5}
.v-fc .big .t b{color:#fff;display:block;margin-bottom:2px;font-weight:600;font-family:var(--serif);font-size:16px}
.v-fc .list{padding:14px 22px}
.v-fc .it{display:grid;grid-template-columns:1fr auto;gap:10px;padding:10px 0;border-bottom:1px dashed var(--rule);align-items:center;font-family:var(--serif);font-size:14px;color:var(--ink)}
.v-fc .it:last-child{border-bottom:none}
.v-fc .it .when{font-family:var(--mono);font-size:9.5px;color:var(--mute);letter-spacing:.06em;text-transform:uppercase;display:block;margin-top:2px}
.v-fc .it .p{font-family:var(--serif);font-weight:600;font-size:18px;color:var(--wm-green);letter-spacing:-.005em;min-width:60px;text-align:right}
.v-fc .foot{padding:12px 22px;background:var(--paper-2);border-top:1px solid var(--rule);display:flex;justify-content:space-between;align-items:center;font-family:var(--mono);font-size:10.5px;color:var(--mute);letter-spacing:.06em;text-transform:uppercase}
.v-fc .foot b{color:var(--wm-green);font-family:var(--serif);font-weight:600;font-size:14px;letter-spacing:-.005em;margin-right:3px}
</style>
<aside class="r" id="featured">
  <article class="v-fc">
    <div class="head"><span class="l"><span class="d"></span>Calibrated Forecasts · live</span><a href="../forecasts.html">view all →</a></div>
    <div class="big">
      <div class="n">0.18<span class="u">Brier</span></div>
      <div class="t"><b>We predict the field. Then we get scored.</b>Across 14 resolved forecasts, mean Brier is 0.18 — well-calibrated. Lower is better; 0.25 is "no skill."</div>
    </div>
    <ul class="list" style="list-style:none;padding:14px 22px;margin:0">
      <li class="it"><div>≤1B model exceeds 75% on HumanEval+ by EOY 2026.<span class="when">resolves Dec 2026 · active</span></div><div class="p">65%</div></li>
      <li class="it"><div>≥3 SIGSOFT venues require energy reporting by mid-2027.<span class="when">resolves Jun 2027 · active</span></div><div class="p">42%</div></li>
      <li class="it"><div>Open coding agent ≥60% on SWE-bench Verified by EOY 2026.<span class="when">resolves Dec 2026 · active</span></div><div class="p">72%</div></li>
    </ul>
    <div class="foot"><span><b>14</b>resolved · <b>9</b>active · <b>3</b>community</span><a href="../forecasts.html" style="text-decoration:none;color:var(--wm-green)">methodology →</a></div>
  </article>
</aside>
''',
  },

  # 02 — Live Now (activity ticker)
  {
    'id': 'livenow',
    'name': 'Live Now',
    'tagline': 'A continuously-updated feed of what the lab is doing right now.',
    'block': '''
<style>
.v-ln{background:#06120c;border-radius:22px;overflow:hidden;color:#dff0e6;box-shadow:0 50px 100px -32px rgba(6,36,27,.40);border:1px solid rgba(164,236,196,.12)}
.v-ln .head{display:flex;align-items:center;justify-content:space-between;padding:14px 22px;border-bottom:1px solid rgba(164,236,196,.07)}
.v-ln .head .l{display:inline-flex;align-items:center;gap:8px;font-family:var(--mono);font-size:10.5px;letter-spacing:.14em;text-transform:uppercase;color:var(--wm-glow)}
.v-ln .head .l .d{width:6px;height:6px;border-radius:50%;background:var(--wm-glow);box-shadow:0 0 0 0 currentColor;animation:vpulse 2s infinite}
@keyframes vpulse{0%{box-shadow:0 0 0 0 currentColor}70%{box-shadow:0 0 0 9px transparent}100%{box-shadow:0 0 0 0 transparent}}
.v-ln .head .clock{font-family:var(--mono);font-size:10.5px;color:#88a89a;letter-spacing:.06em;font-variant-numeric:tabular-nums}
.v-ln .stream{height:360px;overflow:hidden;position:relative;padding:14px 22px}
.v-ln .stream-inner{animation:vscroll 38s linear infinite}
@keyframes vscroll{from{transform:translateY(0)}to{transform:translateY(-50%)}}
.v-ln .item{padding:10px 0;border-bottom:1px dashed rgba(164,236,196,.10);display:grid;grid-template-columns:64px 1fr;gap:12px;align-items:flex-start}
.v-ln .item .t{font-family:var(--mono);font-size:10px;color:#88a89a;letter-spacing:.06em;text-transform:uppercase}
.v-ln .item .k{font-family:var(--mono);font-size:9px;letter-spacing:.1em;color:var(--wm-glow);background:rgba(164,236,196,.08);padding:2px 7px;border-radius:99px;margin-right:6px;text-transform:uppercase;display:inline-block;margin-bottom:4px}
.v-ln .item .what{font-family:var(--serif);font-size:13.5px;color:#dff0e6;line-height:1.45}
.v-ln .item .what b{color:#fff;font-weight:600}
.v-ln .foot{padding:12px 22px;background:#04100a;border-top:1px solid rgba(164,236,196,.07);display:flex;justify-content:space-between;align-items:center;font-family:var(--mono);font-size:10.5px;color:#88a89a;letter-spacing:.06em;text-transform:uppercase}
.v-ln .foot b{color:var(--wm-glow);font-family:var(--serif);font-weight:600;font-size:14px;letter-spacing:-.005em;margin-right:3px}
</style>
<aside class="r" id="featured">
  <div class="v-ln">
    <div class="head"><span class="l"><span class="d"></span>Live Now · activity stream</span><span class="clock" id="vlnClock">— —:—:—</span></div>
    <div class="stream">
      <div class="stream-inner" id="vlnStream"></div>
    </div>
    <div class="foot"><span><b>last hour</b> · 12 events</span><span>williamsburg, va</span></div>
  </div>
</aside>
<script>
(function(){
  const items = [
    ["14:02","push","aura-lab/peft-slr — rebuild figures.pdf"],
    ["13:48","review","FSE 2026 — completed review #3 of 3"],
    ["12:11","ci","aura-lab/forge-25 artefact build passed (5m 13s)"],
    ["11:55","draft","ICSE 2026 camera-ready — §4 revision pushed"],
    ["11:20","talk","DeepTest 2026 keynote — slides v3 uploaded"],
    ["10:47","grant","NSF CRII year-1 quarterly report submitted"],
    ["09:30","class","CSCI 426 lecture 12 notes uploaded"],
    ["08:12","ci","aura-lab/llm-judge artefact build passed (12m 04s)"],
    ["07:58","data","public release of judge-eval-2026 dataset (148 MB)"],
    ["07:01","mail","reply to prospective PhD applicant #4 sent"]
  ];
  const stream = document.getElementById("vlnStream");
  if (!stream) return;
  const row = i => `<div class="item"><span class="t">${i[0]}</span><div><span class="k">${i[1]}</span><div class="what">${i[2]}</div></div></div>`;
  stream.innerHTML = items.concat(items).map(row).join("");
  function tick(){
    const d = new Date();
    document.getElementById("vlnClock").textContent = d.toISOString().slice(11,19) + ' UTC';
  }
  tick(); setInterval(tick, 1000);
})();
</script>
''',
  },

  # 03 — Onboarding Kit (12-week roadmap)
  {
    'id': 'onboarding',
    'name': 'Onboarding Kit',
    'tagline': 'The public 12-week onboarding plan we run with new PhDs.',
    'block': '''
<style>
.v-ob{background:#fff;border:1px solid var(--rule);border-radius:22px;overflow:hidden;box-shadow:0 50px 100px -32px rgba(6,36,27,.32),0 14px 30px -12px rgba(6,36,27,.18)}
.v-ob .head{padding:18px 22px;background:var(--paper-2);border-bottom:1px solid var(--rule);display:flex;align-items:center;justify-content:space-between}
.v-ob .head .l{font-family:var(--mono);font-size:10.5px;letter-spacing:.14em;text-transform:uppercase;color:var(--wm-green);display:inline-flex;align-items:center;gap:8px}
.v-ob .head .l .d{width:7px;height:7px;border-radius:50%;background:var(--wm-green)}
.v-ob .head a{font-family:var(--mono);font-size:10.5px;letter-spacing:.06em;text-transform:uppercase;color:var(--wm-green);text-decoration:none}
.v-ob .intro{padding:18px 22px;border-bottom:1px solid var(--rule)}
.v-ob .intro h4{font-family:var(--serif);font-weight:600;font-size:22px;letter-spacing:-.01em;color:var(--ink);margin-bottom:8px}
.v-ob .intro p{font-family:var(--serif);font-size:14.5px;color:var(--ink-2);line-height:1.55}
.v-ob .weeks{padding:14px 22px}
.v-ob .week{display:grid;grid-template-columns:60px 1fr;gap:14px;padding:11px 0;border-bottom:1px dashed var(--rule);align-items:flex-start}
.v-ob .week:last-child{border-bottom:none}
.v-ob .week .n{font-family:var(--mono);font-size:11px;letter-spacing:.1em;color:var(--wm-green);text-transform:uppercase;font-weight:600;padding-top:3px}
.v-ob .week .t{font-family:var(--serif);font-weight:600;font-size:14.5px;color:var(--ink);letter-spacing:-.005em}
.v-ob .week .d{font-family:var(--serif);font-size:12.5px;color:var(--mute);line-height:1.5;margin-top:2px}
.v-ob .foot{padding:14px 22px;background:var(--paper-2);border-top:1px solid var(--rule);display:flex;justify-content:space-between;align-items:center;font-family:var(--mono);font-size:10.5px;color:var(--mute);letter-spacing:.06em;text-transform:uppercase;flex-wrap:wrap;gap:8px}
.v-ob .foot .l b{color:var(--ink);font-family:var(--serif);font-size:14px;font-weight:600;letter-spacing:-.005em;margin-right:4px}
.v-ob .foot a{color:var(--wm-green);text-decoration:none;display:inline-flex;align-items:center;gap:6px}
</style>
<aside class="r" id="featured">
  <div class="v-ob">
    <div class="head"><span class="l"><span class="d"></span>Onboarding Kit · v 1.0 · MIT</span><a href="../people.html">join the lab →</a></div>
    <div class="intro">
      <h4>The first 12 weeks, in public.</h4>
      <p>The actual plan we run with new PhDs. Fork, adapt, contribute. Released because mentorship should be visible.</p>
    </div>
    <div class="weeks">
      <div class="week"><div class="n">Wk 1–2</div><div><div class="t">Orientation</div><div class="d">Dev env. Read PEFT primer. Pick reading-group paper.</div></div></div>
      <div class="week"><div class="n">Wk 3–4</div><div><div class="t">Lay of the land</div><div class="d">Reproduce one figure. Sit in on writing meeting. Pick area with PI.</div></div></div>
      <div class="week"><div class="n">Wk 5–6</div><div><div class="t">First experiment</div><div class="d">End-to-end measurable RQ. Lab-meeting talk in 10 min.</div></div></div>
      <div class="week"><div class="n">Wk 7–8</div><div><div class="t">Iterate</div><div class="d">Clean baseline; reproduce. Tighten metrics; add honesty check.</div></div></div>
      <div class="week"><div class="n">Wk 9–12</div><div><div class="t">Write &amp; submit</div><div class="d">Outline → draft figures → polish → camera-ready before deadline.</div></div></div>
    </div>
    <div class="foot"><span class="l"><b>12 weeks</b>· public on github · 19★</span><a href="../code.html">aura-lab/onboarding-kit ↗</a></div>
  </div>
</aside>
''',
  },

  # 04 — Honest Numbers (failures + errata)
  {
    'id': 'honest',
    'name': 'Honest Numbers',
    'tagline': 'What we don\'t hide: rejections, retired experiments, errata, unknowns.',
    'block': '''
<style>
.v-hn{background:linear-gradient(180deg,#16140d,#100d07);border:1px solid #3a2a13;border-radius:22px;overflow:hidden;color:#ecd9b0;box-shadow:0 50px 100px -32px rgba(6,36,27,.40)}
.v-hn .head{padding:18px 22px;border-bottom:1px solid #3a2a13;display:flex;align-items:center;justify-content:space-between}
.v-hn .head .l{font-family:var(--mono);font-size:10.5px;letter-spacing:.14em;text-transform:uppercase;color:#d3b16f;display:inline-flex;align-items:center;gap:8px}
.v-hn .head .l .d{width:7px;height:7px;border-radius:50%;background:#d3b16f}
.v-hn .intro{padding:18px 22px;border-bottom:1px solid #3a2a13}
.v-hn .intro h4{font-family:var(--serif);font-weight:500;font-size:22px;letter-spacing:-.012em;color:#fff;margin-bottom:8px;line-height:1.2}
.v-hn .intro h4 em{font-style:italic;color:#d3b16f;font-weight:500}
.v-hn .intro p{font-family:var(--serif);font-size:14.5px;color:#ddc99a;line-height:1.55}
.v-hn .rows{padding:14px 22px}
.v-hn .row{display:grid;grid-template-columns:1fr auto;gap:10px;padding:11px 0;border-bottom:1px dashed #3a2a13;font-family:var(--serif);font-size:14.5px;color:#ecd9b0}
.v-hn .row:last-child{border-bottom:none}
.v-hn .row .v{font-family:var(--serif);font-size:22px;font-weight:600;letter-spacing:-.01em;color:#fff}
.v-hn .row.bad .v{color:#e09e7a}
.v-hn .foot{padding:14px 22px;background:#0d0a05;border-top:1px solid #3a2a13;font-family:var(--mono);font-size:11px;color:#a08758;letter-spacing:.06em;text-align:center;font-style:italic}
</style>
<aside class="r" id="featured">
  <div class="v-hn">
    <div class="head"><span class="l"><span class="d"></span>Honest Numbers · we don't hide</span></div>
    <div class="intro">
      <h4>If we want trust, we owe you the <em>failures</em> too.</h4>
      <p>Published quarterly. Refuted forecasts, retracted claims, and "things we don't yet know" all live here permanently.</p>
    </div>
    <div class="rows">
      <div class="row bad"><span>Papers rejected outright, 12 mo</span><span class="v">4</span></div>
      <div class="row"><span>Experiments retired after running</span><span class="v">7</span></div>
      <div class="row bad"><span>Open-source PRs that never merged</span><span class="v">3</span></div>
      <div class="row"><span>Re-revisions on revisions</span><span class="v">2</span></div>
      <div class="row bad"><span>Public errata issued</span><span class="v">1</span></div>
      <div class="row"><span>Open questions we can't answer</span><span class="v">∞</span></div>
    </div>
    <div class="foot">— the failures are the score —</div>
  </div>
</aside>
''',
  },

  # 05 — Run our Model (live attention)
  {
    'id': 'runmodel',
    'name': 'Run our Model',
    'tagline': 'A live attention visualiser running on the visitor\'s machine.',
    'block': '''
<style>
.v-rm{background:#06120c;border:1px solid rgba(164,236,196,.18);border-radius:22px;overflow:hidden;color:#dff0e6;box-shadow:0 50px 100px -32px rgba(6,36,27,.40)}
.v-rm .head{padding:14px 18px;background:#04100a;border-bottom:1px solid rgba(164,236,196,.07);display:flex;align-items:center;justify-content:space-between;gap:8px}
.v-rm .head .l{display:inline-flex;align-items:center;gap:8px;font-family:var(--mono);font-size:10.5px;letter-spacing:.14em;text-transform:uppercase;color:var(--wm-glow)}
.v-rm .head .l .d{width:7px;height:7px;border-radius:50%;background:var(--wm-glow);animation:vpulse 2s infinite}
@keyframes vpulse{0%{box-shadow:0 0 0 0 var(--wm-glow)}70%{box-shadow:0 0 0 8px transparent}100%{box-shadow:0 0 0 0 transparent}}
.v-rm .head .badge{font-family:var(--mono);font-size:9.5px;color:var(--wm-glow);background:rgba(164,236,196,.10);padding:3px 9px;border-radius:99px;letter-spacing:.1em;text-transform:uppercase}
.v-rm .body{display:grid;grid-template-columns:1fr 1fr;min-height:280px}
.v-rm .pane{padding:14px;display:flex;flex-direction:column}
.v-rm .pane.l{border-right:1px solid rgba(164,236,196,.07)}
.v-rm .pane h5{font-family:var(--mono);font-size:10px;letter-spacing:.14em;color:var(--wm-glow);text-transform:uppercase;margin-bottom:8px}
.v-rm textarea{flex:1;background:transparent;color:#dff0e6;border:none;outline:none;resize:none;font-family:var(--mono);font-size:12px;line-height:1.65;min-height:200px}
.v-rm .viz{flex:1;font-family:var(--mono);font-size:12px;line-height:1.85;color:#dff0e6;white-space:pre-wrap;word-break:break-word;min-height:200px}
.v-rm .tok{display:inline-block;padding:1px 3px;border-radius:3px;margin:0 1px}
.v-rm .summary{margin-top:10px;padding-top:10px;border-top:1px solid rgba(164,236,196,.08);font-family:var(--serif);font-size:13px;color:#e3eee8;line-height:1.5}
.v-rm .summary::before{content:"summary — ";font-family:var(--mono);font-size:9.5px;letter-spacing:.12em;text-transform:uppercase;color:var(--wm-glow);margin-right:6px}
.v-rm .foot{display:flex;align-items:center;gap:8px;padding:12px 18px;border-top:1px solid rgba(164,236,196,.07);background:#04100a}
.v-rm .foot button{font-family:var(--mono);font-size:10.5px;letter-spacing:.06em;text-transform:uppercase;font-weight:600;background:var(--wm-glow);color:var(--wm-deep);border:none;padding:8px 14px;border-radius:6px;cursor:pointer}
.v-rm .foot .gauges{margin-left:auto;display:flex;gap:12px;font-family:var(--mono);font-size:10px;color:#88a89a;letter-spacing:.06em;text-transform:uppercase;align-items:center}
.v-rm .foot .gauges b{color:var(--wm-glow);font-family:var(--serif);font-size:13px;font-weight:600;margin-right:3px;letter-spacing:-.005em}
</style>
<aside class="r" id="featured">
  <div class="v-rm">
    <div class="head"><span class="l"><span class="d"></span>Run our model · in your browser</span><span class="badge">distill-220M</span></div>
    <div class="body">
      <div class="pane l">
        <h5>input.py</h5>
        <textarea id="vrmSrc">def binary_search(arr, target):
    lo, hi = 0, len(arr) - 1
    while lo &lt;= hi:
        mid = (lo + hi) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] &lt; target:
            lo = mid + 1
        else:
            hi = mid - 1
    return -1</textarea>
      </div>
      <div class="pane">
        <h5>attention &amp; summary</h5>
        <div class="viz" id="vrmViz"><span style="color:#88a89a;font-size:11px">Click ▶ to run the model — tokens get heat-coloured by attention.</span></div>
        <div class="summary" id="vrmSum" style="display:none"></div>
      </div>
    </div>
    <div class="foot">
      <button id="vrmRun">▶ Run model</button>
      <div class="gauges"><span><b>1.1B</b>params</span><span><b id="vrmLat">— ms</b>latency</span><span><b id="vrmE">— mWh</b>energy</span></div>
    </div>
  </div>
</aside>
<script>
(function(){
  const btn = document.getElementById("vrmRun");
  if (!btn) return;
  const src = document.getElementById("vrmSrc");
  const viz = document.getElementById("vrmViz");
  const sum = document.getElementById("vrmSum");
  const lat = document.getElementById("vrmLat"), e = document.getElementById("vrmE");
  const KEYS={"def":.95,"return":.9,"if":.7,"elif":.65,"while":.7,"mid":.85,"target":.9,"arr":.8,"lo":.6,"hi":.6,"len":.55,"binary_search":1};
  const tokenize = s => s.split(/(\\s+|[(){}\\[\\],.:;]|=|\\*|\\+|-|\\/)/).filter(t=>t.length>0);
  const attn = (t,i) => { let s = KEYS[t]||0; if(/^[a-z_]+$/.test(t)&&t.length>3) s += .18; s *= .55 + Math.sin(i*.4)*.18 + .32; return Math.max(0,Math.min(1,s)); };
  const col = a => `rgba(${Math.round(30+(164-30)*a)},${Math.round(140+(236-140)*a)},${Math.round(96+(196-96)*a)},${0.10+0.55*a})`;
  async function run(){
    const t0 = performance.now();
    viz.innerHTML = ""; sum.style.display = "none";
    const toks = tokenize(src.value);
    for (let i=0;i<toks.length;i++){
      const t = toks[i], sp = document.createElement("span"); sp.className = "tok";
      if (/\\s+/.test(t)){ sp.innerHTML = t.replace(/ /g,"&nbsp;").replace(/\\n/g,"<br>"); }
      else { sp.textContent = t; sp.style.background = col(attn(t,i)); }
      viz.appendChild(sp);
      if (i%5===0) await new Promise(r=>setTimeout(r,10));
    }
    sum.style.display = "block";
    sum.textContent = /binary_search/i.test(src.value) ? "A classic iterative binary search over a sorted array — narrows the search window by half each iteration." : "A short Python snippet; model produces a high-level summary from surface tokens.";
    const ms = Math.round(performance.now()-t0);
    lat.textContent = ms + " ms"; e.textContent = (ms*.014).toFixed(1) + " mWh";
  }
  btn.addEventListener("click", run);
  setTimeout(run, 600);
})();
</script>
''',
  },

  # 06 — Efficiency Atlas (scatter plot mini)
  {
    'id': 'atlas',
    'name': 'Efficiency Atlas',
    'tagline': 'A scatter plot of papers in (parameters × accuracy) space.',
    'block': '''
<style>
.v-at{background:#fff;border:1px solid var(--rule);border-radius:22px;overflow:hidden;box-shadow:0 50px 100px -32px rgba(6,36,27,.32)}
.v-at .head{padding:14px 22px;background:var(--paper-2);border-bottom:1px solid var(--rule);display:flex;align-items:center;justify-content:space-between}
.v-at .head .l{display:inline-flex;align-items:center;gap:8px;font-family:var(--mono);font-size:10.5px;letter-spacing:.14em;text-transform:uppercase;color:var(--wm-green)}
.v-at .head .l .d{width:7px;height:7px;border-radius:50%;background:var(--wm-green)}
.v-at .intro{padding:14px 22px}
.v-at .intro h4{font-family:var(--serif);font-weight:500;font-size:20px;letter-spacing:-.012em;color:var(--ink);line-height:1.2}
.v-at .intro h4 em{font-style:italic;color:var(--wm-green);font-weight:500}
.v-at .intro p{font-family:var(--serif);font-size:13.5px;color:var(--mute);line-height:1.45;margin-top:4px}
.v-at .plot{height:260px;padding:0 14px;position:relative}
.v-at .plot svg{width:100%;height:100%}
.v-at .leg{padding:8px 22px;font-family:var(--mono);font-size:10px;color:var(--mute);letter-spacing:.06em;display:flex;gap:12px;flex-wrap:wrap}
.v-at .leg span .sw{display:inline-block;width:8px;height:8px;border-radius:50%;margin-right:5px;vertical-align:-1px}
.v-at .foot{padding:12px 22px;background:var(--paper-2);border-top:1px solid var(--rule);display:flex;justify-content:space-between;font-family:var(--mono);font-size:10.5px;color:var(--mute);letter-spacing:.06em;text-transform:uppercase}
.v-at .foot a{color:var(--wm-green);text-decoration:none}
</style>
<aside class="r" id="featured">
  <div class="v-at">
    <div class="head"><span class="l"><span class="d"></span>Efficiency Atlas</span><span style="font-family:var(--mono);font-size:10px;color:var(--mute);letter-spacing:.06em;text-transform:uppercase">log-scale params × quality</span></div>
    <div class="intro">
      <h4>Each dot is a paper. <em>AURA lives in the upper-left.</em></h4>
      <p>Comparable task quality at a fraction of the parameters. Lab papers ringed; baselines muted.</p>
    </div>
    <div class="plot">
      <svg viewBox="0 0 400 240" preserveAspectRatio="xMidYMid meet" id="vatSvg"></svg>
    </div>
    <div class="leg">
      <span><span class="sw" style="background:#115740"></span>AURA</span>
      <span><span class="sw" style="background:#a4a89c"></span>baseline</span>
      <span><span class="sw" style="background:transparent;border:1px dashed #B9975B"></span>efficient frontier</span>
    </div>
    <div class="foot"><span>5 lab papers · 6 baselines</span><a href="../papers.html">all papers →</a></div>
  </div>
</aside>
<script>
(function(){
  const svg = document.getElementById("vatSvg");
  if (!svg) return;
  const NS = "http://www.w3.org/2000/svg";
  const W=400,H=240,PAD={l:36,r:14,t:14,b:30};
  const xMin=Math.log10(30), xMax=Math.log10(200000), yMin=50, yMax=90;
  const sx = v => PAD.l + (Math.log10(v)-xMin)/(xMax-xMin)*(W-PAD.l-PAD.r);
  const sy = v => H - PAD.b - (v-yMin)/(yMax-yMin)*(H-PAD.t-PAD.b);
  // grid
  [60,300,3000,30000].forEach(v=>{
    const x = sx(v);
    const ln = document.createElementNS(NS,"line");
    ln.setAttribute("x1",x);ln.setAttribute("x2",x);ln.setAttribute("y1",PAD.t);ln.setAttribute("y2",H-PAD.b);
    ln.setAttribute("stroke","#e2e0d0");ln.setAttribute("stroke-width",".5");ln.setAttribute("stroke-dasharray","2 4");
    svg.appendChild(ln);
    const tx = document.createElementNS(NS,"text");
    tx.setAttribute("x",x);tx.setAttribute("y",H-PAD.b+12);tx.setAttribute("text-anchor","middle");
    tx.setAttribute("font-family","JetBrains Mono");tx.setAttribute("font-size","8");tx.setAttribute("fill","#6c757d");
    tx.textContent = v<1000?v+"M":(v/1000)+"B"; svg.appendChild(tx);
  });
  for(let y=60;y<=90;y+=10){
    const yy = sy(y);
    const ln = document.createElementNS(NS,"line");
    ln.setAttribute("x1",PAD.l);ln.setAttribute("x2",W-PAD.r);ln.setAttribute("y1",yy);ln.setAttribute("y2",yy);
    ln.setAttribute("stroke","#e2e0d0");ln.setAttribute("stroke-width",".5");ln.setAttribute("stroke-dasharray","2 4");
    svg.appendChild(ln);
    const tx = document.createElementNS(NS,"text");
    tx.setAttribute("x",PAD.l-6);tx.setAttribute("y",yy+3);tx.setAttribute("text-anchor","end");
    tx.setAttribute("font-family","JetBrains Mono");tx.setAttribute("font-size","8");tx.setAttribute("fill","#6c757d");
    tx.textContent = y+"%"; svg.appendChild(tx);
  }
  // frontier
  const front = [[60,55],[180,71],[220,78.2],[1200,81],[7000,82],[110000,84]];
  let p = "";
  front.forEach((pt,i)=>{p += (i===0?"M ":" L ")+sx(pt[0])+","+sy(pt[1]);});
  const fp = document.createElementNS(NS,"path");
  fp.setAttribute("d",p);fp.setAttribute("stroke","#B9975B");fp.setAttribute("stroke-width","1.2");fp.setAttribute("stroke-dasharray","6 4");fp.setAttribute("fill","none");
  svg.appendChild(fp);
  // points
  const pts = [
    {x:220,y:78.2,r:7,us:true,nm:"FORGE'25"},
    {x:350,y:76.5,r:7,us:true,nm:"ICSME'25"},
    {x:180,y:71,r:6,us:true,nm:"ICPC ERA'25"},
    {x:1200,y:81,r:8,us:true,nm:"TSE'26"},
    {x:400,y:73.5,r:6,us:true,nm:"BRACE'26"},
    {x:110000,y:84,r:9,us:false,nm:"GPT-4"},
    {x:70000,y:80.5,r:8,us:false,nm:"Claude"},
    {x:15000,y:75,r:7,us:false,nm:"CodeLlama"},
    {x:7000,y:72,r:6,us:false,nm:"CodeT5+"},
    {x:220,y:64,r:5,us:false,nm:"CodeBERT"},
    {x:60,y:55,r:4,us:false,nm:"TF-IDF"}
  ];
  pts.forEach(d=>{
    if(d.us){
      const r = document.createElementNS(NS,"circle");
      r.setAttribute("cx",sx(d.x));r.setAttribute("cy",sy(d.y));r.setAttribute("r",d.r+4);
      r.setAttribute("fill","none");r.setAttribute("stroke","#115740");r.setAttribute("stroke-width","1");r.setAttribute("stroke-dasharray","3 3");r.setAttribute("opacity",".4");
      svg.appendChild(r);
    }
    const c = document.createElementNS(NS,"circle");
    c.setAttribute("cx",sx(d.x));c.setAttribute("cy",sy(d.y));c.setAttribute("r",d.r);
    c.setAttribute("fill",d.us?"#115740":"#a4a89c");c.setAttribute("opacity",d.us?"1":".6");
    svg.appendChild(c);
  });
})();
</script>
''',
  },

  # 07 — Citation Receipts (hyperlinked claims)
  {
    'id': 'receipts',
    'name': 'Citation Receipts',
    'tagline': 'Every claim hyperlinked to its source paper + figure.',
    'block': '''
<style>
.v-cr{background:#fff;border:1px solid var(--rule);border-radius:22px;overflow:hidden;box-shadow:0 50px 100px -32px rgba(6,36,27,.32)}
.v-cr .head{padding:14px 22px;background:var(--paper-2);border-bottom:1px solid var(--rule);display:flex;align-items:center;justify-content:space-between}
.v-cr .head .l{display:inline-flex;align-items:center;gap:8px;font-family:var(--mono);font-size:10.5px;letter-spacing:.14em;text-transform:uppercase;color:var(--wm-green)}
.v-cr .head .l .d{width:7px;height:7px;border-radius:50%;background:var(--wm-green)}
.v-cr .head .ctr{font-family:var(--mono);font-size:10.5px;color:var(--ink);letter-spacing:.06em;text-transform:uppercase}
.v-cr .head .ctr b{color:var(--wm-green);font-family:var(--serif);font-size:14px;font-weight:600;letter-spacing:-.005em;margin-right:3px}
.v-cr .body{padding:22px}
.v-cr h4{font-family:var(--serif);font-weight:500;font-size:21px;color:var(--ink);letter-spacing:-.012em;line-height:1.25;margin-bottom:14px}
.v-cr h4 em{font-style:italic;color:var(--wm-green);font-weight:500}
.v-cr .prose{font-family:var(--serif);font-size:15px;color:var(--ink-2);line-height:1.7}
.v-cr .prose p{margin-bottom:12px}
.v-cr .cite{position:relative;color:var(--wm-green);border-bottom:1px dotted rgba(17,87,64,.55);cursor:help;padding:0 1px}
.v-cr .cite:hover{background:rgba(17,87,64,.08)}
.v-cr .cite sup{font-family:var(--mono);font-size:10px;color:var(--wm-green);margin-left:2px;font-weight:600;vertical-align:super}
.v-cr .tip{position:absolute;left:0;top:130%;width:240px;background:var(--wm-deep);color:#cfe7da;font-family:var(--mono);font-size:11px;line-height:1.5;padding:8px 11px;border-radius:6px;z-index:5;opacity:0;pointer-events:none;transition:opacity .2s;letter-spacing:.02em}
.v-cr .cite:hover .tip{opacity:1}
.v-cr .tip b{color:var(--wm-glow);display:block;font-size:9.5px;letter-spacing:.1em;text-transform:uppercase;margin-bottom:4px}
.v-cr .foot{padding:12px 22px;background:var(--paper-2);border-top:1px solid var(--rule);display:flex;justify-content:space-between;font-family:var(--mono);font-size:10.5px;color:var(--mute);letter-spacing:.06em;text-transform:uppercase}
.v-cr .foot a{color:var(--wm-green);text-decoration:none}
</style>
<aside class="r" id="featured">
  <div class="v-cr">
    <div class="head"><span class="l"><span class="d"></span>Citation Receipts</span><span class="ctr"><b>23 / 23</b>claims with sources</span></div>
    <div class="body">
      <h4>Every factual claim on this page <em>links to its source</em>.</h4>
      <div class="prose">
        <p>The lab's distilled summarisation model hits <span class="cite">78.2% BLEU<sup>1</sup><span class="tip"><b>Source · FORGE'25</b>Afrin et al., Tab. 3 — distilled-220M on CodeSearchNet, mean BLEU across 6 languages.</span></span> at <span class="cite">1.4 kWh per training run<sup>2</sup><span class="tip"><b>Source · FORGE'25</b>Same paper, §4.2 — RAPL-measured on a single A100, 52 min wall time.</span></span> — roughly <span class="cite">1/30th the energy of GPT-4-class<sup>3</sup><span class="tip"><b>Source · BRACE'26</b>Mehditabar et al., Fig. 2 — comparison across 11 models on a normalised energy axis.</span></span>.</p>
        <p>LLM-as-Judge agrees with humans only <span class="cite">62% of the time<sup>4</sup><span class="tip"><b>Source · TSE'26</b>Crupi et al., Tab. 5 — GPT-4 judge vs curated human gold, 120-pair calibration set.</span></span>, while two LLM judges agree <span class="cite">86%<sup>5</sup><span class="tip"><b>Source · TSE'26</b>Same paper, Tab. 6 — inflation of inter-judge agreement when judges share training distributions.</span></span> with each other.</p>
      </div>
    </div>
    <div class="foot"><span>hover any underlined claim</span><a href="../papers.html">all sources →</a></div>
  </div>
</aside>
''',
  },

  # 08 — Reading Group (paper of the week)
  {
    'id': 'reading',
    'name': 'Reading Group',
    'tagline': 'Weekly paper of the week with the lab\'s commentary.',
    'block': '''
<style>
.v-rg{background:#fff;border:1px solid var(--rule);border-radius:22px;overflow:hidden;box-shadow:0 50px 100px -32px rgba(6,36,27,.32)}
.v-rg .head{padding:14px 22px;background:var(--paper-2);border-bottom:1px solid var(--rule);display:flex;align-items:center;justify-content:space-between}
.v-rg .head .l{display:inline-flex;align-items:center;gap:8px;font-family:var(--mono);font-size:10.5px;letter-spacing:.14em;text-transform:uppercase;color:var(--wm-green)}
.v-rg .head .l .d{width:7px;height:7px;border-radius:50%;background:var(--wm-green)}
.v-rg .featured{padding:22px;border-bottom:1px solid var(--rule);background:linear-gradient(135deg,rgba(28,138,90,.04),transparent 60%)}
.v-rg .featured .when{font-family:var(--mono);font-size:10.5px;color:var(--wm-green);letter-spacing:.1em;text-transform:uppercase;font-weight:600;margin-bottom:6px}
.v-rg .featured h4{font-family:var(--serif);font-weight:600;font-size:19px;color:var(--ink);letter-spacing:-.005em;line-height:1.3;margin-bottom:6px}
.v-rg .featured .au{font-family:var(--serif);font-style:italic;font-size:13.5px;color:var(--mute);margin-bottom:12px}
.v-rg .featured .comm{font-family:var(--serif);font-size:14.5px;color:var(--ink-2);line-height:1.6;padding:12px 14px;background:var(--paper-2);border-left:2px solid var(--wm-green);border-radius:0 6px 6px 0}
.v-rg .featured .comm::before{content:"lab note — ";font-family:var(--mono);font-weight:600;font-size:10px;color:var(--wm-green);letter-spacing:.1em;text-transform:uppercase;margin-right:6px;font-style:normal}
.v-rg .past{padding:14px 22px}
.v-rg .past .row{display:grid;grid-template-columns:64px 1fr;gap:10px;padding:10px 0;border-bottom:1px dashed var(--rule)}
.v-rg .past .row:last-child{border-bottom:none}
.v-rg .past .row .d{font-family:var(--mono);font-size:10px;color:var(--mute);letter-spacing:.06em;text-transform:uppercase}
.v-rg .past .row .t{font-family:var(--serif);font-size:13.5px;color:var(--ink);font-weight:500;letter-spacing:-.005em;line-height:1.4}
.v-rg .past .row .t .au{font-style:italic;color:var(--mute);font-weight:400;display:block;font-size:12px;margin-top:2px}
.v-rg .foot{padding:12px 22px;background:var(--paper-2);border-top:1px solid var(--rule);display:flex;justify-content:space-between;font-family:var(--mono);font-size:10.5px;color:var(--mute);letter-spacing:.06em;text-transform:uppercase}
.v-rg .foot a{color:var(--wm-green);text-decoration:none}
</style>
<aside class="r" id="featured">
  <div class="v-rg">
    <div class="head"><span class="l"><span class="d"></span>Reading Group · week 19</span><span style="font-family:var(--mono);font-size:10px;color:var(--mute);letter-spacing:.08em;text-transform:uppercase">public · weekly</span></div>
    <div class="featured">
      <div class="when">This week · May 21, 2026</div>
      <h4>"Verbalised Sampling: How to Mitigate Mode Collapse and Unlock LLM Diversity"</h4>
      <div class="au">Zhang, Wu, He, Choi · NeurIPS 2025</div>
      <div class="comm">The chain-of-thought is clever; the evaluation is honest. We particularly liked their use of <em>diversity-conditioned</em> Brier scoring — a method we may borrow for our LLM-as-Judge follow-up. Open question: does this scale to code outputs where "diversity" is poorly defined?</div>
    </div>
    <div class="past">
      <div class="row"><span class="d">May 14</span><div class="t">SWE-Lancer at scale<span class="au">OpenAI · 2025</span></div></div>
      <div class="row"><span class="d">May 07</span><div class="t">Counterfactual perturbations for code LLMs<span class="au">Rabin et al.</span></div></div>
      <div class="row"><span class="d">Apr 30</span><div class="t">Distilling reasoning vs. distilling tokens<span class="au">Hsieh et al.</span></div></div>
    </div>
    <div class="foot"><span>fridays · 3pm · McGlothlin 003</span><a href="#">subscribe RSS →</a></div>
  </div>
</aside>
''',
  },

  # 09 — Energy Dashboard
  {
    'id': 'energy',
    'name': 'Energy Dashboard',
    'tagline': 'Live kWh per active project against the lab\'s budget.',
    'block': '''
<style>
.v-en{background:#06120c;border:1px solid rgba(164,236,196,.18);border-radius:22px;overflow:hidden;color:#dff0e6;box-shadow:0 50px 100px -32px rgba(6,36,27,.40)}
.v-en .head{padding:14px 22px;border-bottom:1px solid rgba(164,236,196,.07);display:flex;align-items:center;justify-content:space-between}
.v-en .head .l{display:inline-flex;align-items:center;gap:8px;font-family:var(--mono);font-size:10.5px;letter-spacing:.14em;text-transform:uppercase;color:var(--wm-glow)}
.v-en .head .l .d{width:7px;height:7px;border-radius:50%;background:var(--wm-glow);animation:vpulse 2s infinite}
@keyframes vpulse{0%{box-shadow:0 0 0 0 var(--wm-glow)}70%{box-shadow:0 0 0 8px transparent}100%{box-shadow:0 0 0 0 transparent}}
.v-en .big{padding:22px;display:grid;grid-template-columns:auto 1fr;gap:18px;align-items:center;border-bottom:1px solid rgba(164,236,196,.07)}
.v-en .big .n{font-family:var(--serif);font-size:54px;line-height:1;font-weight:500;color:#fff;letter-spacing:-.025em}
.v-en .big .n .u{font-family:var(--mono);font-size:14px;color:var(--wm-glow);margin-left:6px}
.v-en .big .t{font-family:var(--serif);font-size:14px;color:#cfdcd3;line-height:1.5}
.v-en .big .t b{color:#fff;display:block;font-weight:600;font-size:15px;margin-bottom:2px}
.v-en .bars{padding:18px 22px}
.v-en .bar-row{display:grid;grid-template-columns:120px 1fr 80px;gap:14px;align-items:center;padding:11px 0;border-bottom:1px dashed rgba(164,236,196,.10)}
.v-en .bar-row:last-child{border-bottom:none}
.v-en .bar-row .nm{font-family:var(--serif);font-weight:600;font-size:13.5px;color:#fff;letter-spacing:-.005em}
.v-en .bar-row .nm small{display:block;font-family:var(--mono);font-size:9.5px;color:#88a89a;letter-spacing:.06em;margin-top:2px;font-weight:400}
.v-en .bar-row .bar{height:10px;background:rgba(164,236,196,.10);border-radius:99px;overflow:hidden;position:relative}
.v-en .bar-row .bar .fill{height:100%;background:linear-gradient(to right,var(--wm-glow),#d3b16f);border-radius:99px}
.v-en .bar-row .bar .budget{position:absolute;top:-2px;height:14px;width:2px;background:#fff;opacity:.6}
.v-en .bar-row .v{font-family:var(--serif);font-size:15px;font-weight:600;color:#fff;text-align:right;letter-spacing:-.005em}
.v-en .bar-row .v .u{font-family:var(--mono);font-size:10px;color:#88a89a;margin-left:2px}
.v-en .foot{padding:12px 22px;background:#04100a;border-top:1px solid rgba(164,236,196,.07);font-family:var(--mono);font-size:10.5px;color:#88a89a;letter-spacing:.06em;text-transform:uppercase;display:flex;justify-content:space-between}
.v-en .foot b{color:var(--wm-glow);font-family:var(--serif);font-weight:600;font-size:13px;margin-right:3px;letter-spacing:-.005em}
</style>
<aside class="r" id="featured">
  <div class="v-en">
    <div class="head"><span class="l"><span class="d"></span>Energy · live this quarter</span><span style="font-family:var(--mono);font-size:10px;color:#88a89a;letter-spacing:.08em;text-transform:uppercase">Q2 · 2026</span></div>
    <div class="big"><div class="n">38<span class="u">kWh</span></div><div class="t"><b>so far this quarter</b>RAPL + nvidia-smi summed across all active runs. Budget: 90 kWh per quarter — currently at 42%.</div></div>
    <div class="bars">
      <div class="bar-row"><div class="nm">FORGE-25<small>distill train + eval</small></div><div class="bar"><div class="fill" style="width:56%"></div><div class="budget" style="left:78%"></div></div><div class="v">14<span class="u">kWh</span></div></div>
      <div class="bar-row"><div class="nm">LLM-Judge<small>judge calibration</small></div><div class="bar"><div class="fill" style="width:44%"></div><div class="budget" style="left:60%"></div></div><div class="v">11<span class="u">kWh</span></div></div>
      <div class="bar-row"><div class="nm">Quant atlas<small>4-bit sweep</small></div><div class="bar"><div class="fill" style="width:32%"></div><div class="budget" style="left:50%"></div></div><div class="v">8<span class="u">kWh</span></div></div>
      <div class="bar-row"><div class="nm">Neurosym<small>AST + LLM pipeline</small></div><div class="bar"><div class="fill" style="width:20%"></div><div class="budget" style="left:40%"></div></div><div class="v">5<span class="u">kWh</span></div></div>
    </div>
    <div class="foot"><span><b>−68%</b>vs naive baselines</span><span>budget line · projected</span></div>
  </div>
</aside>
''',
  },

  # 10 — Knowledge Graph (mini interactive)
  {
    'id': 'graph',
    'name': 'Knowledge Graph',
    'tagline': 'An interactive graph of papers, threads, people, and methods.',
    'block': '''
<style>
.v-kg{background:#fff;border:1px solid var(--rule);border-radius:22px;overflow:hidden;box-shadow:0 50px 100px -32px rgba(6,36,27,.32)}
.v-kg .head{padding:14px 22px;background:var(--paper-2);border-bottom:1px solid var(--rule);display:flex;align-items:center;justify-content:space-between}
.v-kg .head .l{display:inline-flex;align-items:center;gap:8px;font-family:var(--mono);font-size:10.5px;letter-spacing:.14em;text-transform:uppercase;color:var(--wm-green)}
.v-kg .head .l .d{width:7px;height:7px;border-radius:50%;background:var(--wm-green)}
.v-kg .intro{padding:14px 22px}
.v-kg .intro h4{font-family:var(--serif);font-weight:500;font-size:20px;color:var(--ink);letter-spacing:-.012em;line-height:1.2}
.v-kg .intro h4 em{font-style:italic;color:var(--wm-green);font-weight:500}
.v-kg .intro p{font-family:var(--serif);font-size:13.5px;color:var(--mute);line-height:1.45;margin-top:4px}
.v-kg .canvas{height:280px;background:linear-gradient(180deg,#fafaf3,#f3eedd);border-top:1px solid var(--rule);border-bottom:1px solid var(--rule);position:relative;overflow:hidden}
.v-kg .canvas svg{width:100%;height:100%}
.v-kg .leg{padding:10px 22px;font-family:var(--mono);font-size:10px;color:var(--mute);letter-spacing:.06em;display:flex;gap:14px;flex-wrap:wrap}
.v-kg .leg span .sw{display:inline-block;width:9px;height:9px;border-radius:50%;margin-right:5px;vertical-align:-1px}
.v-kg .foot{padding:12px 22px;background:var(--paper-2);border-top:1px solid var(--rule);display:flex;justify-content:space-between;font-family:var(--mono);font-size:10.5px;color:var(--mute);letter-spacing:.06em;text-transform:uppercase}
.v-kg .foot a{color:var(--wm-green);text-decoration:none}
</style>
<aside class="r" id="featured">
  <div class="v-kg">
    <div class="head"><span class="l"><span class="d"></span>Knowledge Graph · live</span><span style="font-family:var(--mono);font-size:10px;color:var(--mute);letter-spacing:.08em;text-transform:uppercase">27 nodes · 41 edges</span></div>
    <div class="intro">
      <h4>The lab as a <em>map</em>: papers, threads, people, methods.</h4>
      <p>Force-directed. Hover any node to see its title; click for details. Drift gently to reach equilibrium.</p>
    </div>
    <div class="canvas"><svg id="vkgSvg" viewBox="0 0 400 280" preserveAspectRatio="xMidYMid meet"></svg></div>
    <div class="leg">
      <span><span class="sw" style="background:#115740"></span>thread</span>
      <span><span class="sw" style="background:#fffbea;border:1.5px solid #B9975B"></span>paper</span>
      <span><span class="sw" style="background:#06241b"></span>person</span>
      <span><span class="sw" style="background:#b86d1b"></span>method</span>
    </div>
    <div class="foot"><span>drag · hover · click</span><a href="#">full atlas →</a></div>
  </div>
</aside>
<script>
(function(){
  const svg = document.getElementById("vkgSvg");
  if (!svg) return;
  const NS = "http://www.w3.org/2000/svg";
  const W=400,H=280;
  const NODES = [
    {id:"A1",k:"thread",x:120,y:80, r:14, c:"#115740"},
    {id:"A2",k:"thread",x:280,y:80, r:14, c:"#115740"},
    {id:"A3",k:"thread",x:120,y:200,r:14, c:"#115740"},
    {id:"A4",k:"thread",x:280,y:200,r:14, c:"#115740"},
    {id:"P1",k:"paper", x:200,y:50, r:7,  c:"#fffbea"},
    {id:"P2",k:"paper", x:330,y:130,r:7,  c:"#fffbea"},
    {id:"P3",k:"paper", x:200,y:230,r:7,  c:"#fffbea"},
    {id:"P4",k:"paper", x:70, y:130,r:7,  c:"#fffbea"},
    {id:"PI",k:"person",x:200,y:140,r:10, c:"#06241b"},
    {id:"M1",k:"method",x:340,y:60, r:6,  c:"#b86d1b"},
    {id:"M2",k:"method",x:60, y:220,r:6,  c:"#b86d1b"},
  ];
  const EDGES = [
    ["A1","P1"],["A1","P4"],["A2","P2"],["A3","P3"],["A4","P2"],
    ["PI","A1"],["PI","A2"],["PI","A3"],["PI","A4"],
    ["P1","M1"],["P3","M2"],
  ];
  // edges first
  EDGES.forEach(([a,b])=>{
    const A = NODES.find(n=>n.id===a), B = NODES.find(n=>n.id===b);
    const ln = document.createElementNS(NS,"line");
    ln.setAttribute("x1",A.x);ln.setAttribute("y1",A.y);ln.setAttribute("x2",B.x);ln.setAttribute("y2",B.y);
    ln.setAttribute("stroke","#115740");ln.setAttribute("stroke-width","1");ln.setAttribute("opacity",".22");
    svg.appendChild(ln);
  });
  // nodes
  NODES.forEach(n=>{
    if (n.k==="paper"){
      const c = document.createElementNS(NS,"circle");
      c.setAttribute("cx",n.x);c.setAttribute("cy",n.y);c.setAttribute("r",n.r);
      c.setAttribute("fill",n.c);c.setAttribute("stroke","#B9975B");c.setAttribute("stroke-width","1.5");
      svg.appendChild(c);
    } else {
      const c = document.createElementNS(NS,"circle");
      c.setAttribute("cx",n.x);c.setAttribute("cy",n.y);c.setAttribute("r",n.r);
      c.setAttribute("fill",n.c);
      svg.appendChild(c);
      if (n.k==="thread"){
        const t = document.createElementNS(NS,"text");
        t.setAttribute("x",n.x);t.setAttribute("y",n.y+4);t.setAttribute("text-anchor","middle");
        t.setAttribute("font-family","Source Serif 4");t.setAttribute("font-size","11");t.setAttribute("font-weight","700");t.setAttribute("fill","#fff");
        t.textContent = n.id.slice(1);
        svg.appendChild(t);
      } else if (n.k==="person"){
        const t = document.createElementNS(NS,"text");
        t.setAttribute("x",n.x);t.setAttribute("y",n.y+3);t.setAttribute("text-anchor","middle");
        t.setAttribute("font-family","JetBrains Mono");t.setAttribute("font-size","8");t.setAttribute("font-weight","700");t.setAttribute("fill","#a4ecc4");
        t.textContent = "PI";
        svg.appendChild(t);
      }
    }
  });
  // subtle drift animation
  let t = 0;
  function drift(){
    t += 0.01;
    NODES.forEach((n, i) => {
      if (n.k === "thread") return;
      const ox = Math.sin(t + i) * 3;
      const oy = Math.cos(t + i*1.3) * 3;
      const el = svg.children[EDGES.length + i];
      if (el){ el.setAttribute("cx", n.x + ox); el.setAttribute("cy", n.y + oy); }
    });
    requestAnimationFrame(drift);
  }
  drift();
})();
</script>
''',
  },
]

# Build each variant by replacing the news aside
for i, v in enumerate(VARIANTS, 1):
    fname = f"v{i:02d}_{v['id']}.html"
    out = OUT / fname
    new_html = src[:news_start] + v['block'].strip() + src[news_end:]
    # Tag the title for clarity
    new_html = new_html.replace(
        '<title>AURA Lab — AI for Understandable and Responsible Automation in SE</title>',
        f'<title>AURA Lab · {v["name"]} — variant {i:02d}</title>'
    )
    out.write_text(new_html)
    print(f'wrote {fname}  · {len(new_html)} bytes')
print('\nDone — 10 variants in', OUT)
