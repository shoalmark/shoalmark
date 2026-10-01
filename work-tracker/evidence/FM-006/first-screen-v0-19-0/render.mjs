// render.mjs SITE OUT [PREVIEW] — FM-006, what a stranger meets first (v0.19.0): the Designer's renders of the BUILT landing.
// SITE is a `zensical build --clean` output (site/), served from 127.0.0.1 as a host serves it; Chrome headless over its
// DevTools protocol, offline (every host unresolvable but 127.0.0.1: the page's fonts are the site's own), a dark preference,
// device scale 1 — the way of slice L's render.mjs (../landing/start-page/), with this slice's files and the preview. Node 22+.
//   phone-390-first.png, phone-390-full.png        390 × 844, the first screen and the whole page, 3 s after load
//   desktop-1440-first.png, desktop-1440-full.png  1440 × 900, the same
//   PREVIEW, if named                              1200 × 630 of the chart at 1280 px, reduced motion: the title shows its wordmark
//                                                  alone — the headline, claim, job line and action hidden; the HUD and its
//                                                  counts are above the clip — so one image serves both languages; no wreck
//                                                  selected (every wreck aria-pressed="false", as the markup has it before
//                                                  attract mode picks one), so no single defect is singled out
// It prints a JSON summary: each first-screen part's box at both widths (document px; the fold is the window's height), the
// links in each first screen, script errors and the hosts asked, the page's sideways scroll, the fleet's tiles at 390, and the
// contrast of every text run outside the chart by slice L's flat method (checks.mjs): its colour, opacity applied, over the
// median pixel under its glyphs, the ground captured with all text transparent, under reduced motion.
import {spawn} from "node:child_process";
import {createServer} from "node:http";
import {existsSync, mkdirSync, mkdtempSync, readFileSync, statSync, writeFileSync} from "node:fs";
import {tmpdir} from "node:os";
import {join, resolve} from "node:path";
import {inflateSync} from "node:zlib";

const site = resolve(process.argv[2] ?? "site"), out = resolve(process.argv[3] ?? "."), preview = process.argv[4] ? resolve(process.argv[4]) : null;
const chrome = process.env.CHROME ?? "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome";
const port = 9400 + Math.floor(Math.random() * 500), sleep = ms => new Promise(r => setTimeout(r, ms));
const proc = spawn(chrome, ["--headless=new", "--disable-gpu", "--hide-scrollbars", `--remote-debugging-port=${port}`,
  "--host-resolver-rules=MAP * ~NOTFOUND, EXCLUDE 127.0.0.1", `--user-data-dir=${mkdtempSync(join(tmpdir(), "first-screen-"))}`, "about:blank"], {stdio: "ignore"});
for (let i = 0; i < 80; i++) { try { await fetch(`http://127.0.0.1:${port}/json/version`); break } catch { await sleep(250) } }
const TYPES = {html: "text/html", css: "text/css", js: "text/javascript", json: "application/json", svg: "image/svg+xml", png: "image/png", woff2: "font/woff2", xml: "application/xml", txt: "text/plain"};
const server = createServer((q, s) => { const f = join(site, decodeURIComponent(new URL(q.url, "http://x").pathname));
  if (!f.startsWith(site) || !existsSync(f) || statSync(f).isDirectory()) { s.writeHead(404); return s.end() }
  s.writeHead(200, {"content-type": TYPES[f.split(".").pop()] ?? "application/octet-stream"}); s.end(readFileSync(f)) });
await new Promise(r => server.listen(0, "127.0.0.1", r));
const origin = `http://127.0.0.1:${server.address().port}/`;

// ---- a PNG, decoded (slice L's decoder): Chrome's captures are 8-bit RGB or RGBA, not interlaced
function png(buf) {
  let p = 8, w, h, ct, idat = [];
  while (p < buf.length) {
    const len = buf.readUInt32BE(p), type = buf.toString("ascii", p + 4, p + 8), data = buf.subarray(p + 8, p + 8 + len);
    if (type == "IHDR") { w = data.readUInt32BE(0); h = data.readUInt32BE(4); ct = data[9]; if (data[8] != 8 || data[12]) throw Error("png: not 8-bit / interlaced") }
    if (type == "IDAT") idat.push(data);
    p += 12 + len;
  }
  const bpp = ct == 6 ? 4 : ct == 2 ? 3 : 0; if (!bpp) throw Error("png: colour type " + ct);
  const raw = inflateSync(Buffer.concat(idat)), stride = w * bpp, px = Buffer.alloc(h * stride);
  for (let y = 0; y < h; y++) {
    const f = raw[y * (stride + 1)], src = raw.subarray(y * (stride + 1) + 1, (y + 1) * (stride + 1)), o = y * stride;
    for (let x = 0; x < stride; x++) {
      const a = x >= bpp ? px[o + x - bpp] : 0, b = y ? px[o - stride + x] : 0, c = x >= bpp && y ? px[o - stride + x - bpp] : 0;
      const pa = Math.abs(b - c), pb = Math.abs(a - c), pc = Math.abs(a + b - 2 * c);
      px[o + x] = (src[x] + [0, a, b, (a + b) >> 1, pa <= pb && pa <= pc ? a : pb <= pc ? b : c][f]) & 255;
    }
  }
  return {w, h, at: (x, y) => { const i = (y * w + x) * bpp; return [px[i], px[i + 1], px[i + 2]] }};
}
const lin = c => (c /= 255) <= 0.03928 ? c / 12.92 : ((c + 0.055) / 1.055) ** 2.4;
const lum = ([r, g, b]) => 0.2126 * lin(r) + 0.7152 * lin(g) + 0.0722 * lin(b);
const ratio = (a, b) => (Math.max(lum(a), lum(b)) + 0.05) / (Math.min(lum(a), lum(b)) + 0.05);
const over = ([r, g, b, a], [R, G, B]) => [r * a + R * (1 - a), g * a + G * (1 - a), b * a + B * (1 - a)];
const hex = c => "#" + c.slice(0, 3).map(v => Math.max(0, Math.min(255, Math.round(v))).toString(16).padStart(2, "0")).join("");
const r2 = v => Math.round(v * 100) / 100;

// ---- a tab
const errors = [], asked = new Set();
async function open(w, h, reduce) {
  const t = await (await fetch(`http://127.0.0.1:${port}/json/new?about:blank`, {method: "PUT"})).json();
  const ws = new WebSocket(t.webSocketDebuggerUrl); await new Promise(r => ws.onopen = r);
  let id = 0; const pend = new Map();
  ws.onmessage = e => { const m = JSON.parse(e.data), p = m.params;
    if (m.method == "Runtime.exceptionThrown") errors.push(`${w}px: ${p.exceptionDetails.exception?.description ?? p.exceptionDetails.text}`);
    if (m.method == "Runtime.consoleAPICalled" && p.type == "error") errors.push(`${w}px console: ${p.args.map(a => a.value ?? a.description).join(" ")}`);
    if (m.method == "Log.entryAdded" && p.entry.level == "error") errors.push(`${w}px log: ${p.entry.text} ${p.entry.url ?? ""}`);
    if (m.method == "Network.requestWillBeSent" && !/^(data|about|blob):/.test(p.request.url) && !p.request.url.startsWith(origin)) asked.add(new URL(p.request.url).host);
    if (pend.has(m.id)) { pend.get(m.id)(m.result ?? {error: m.error}); pend.delete(m.id) } };
  const call = (method, params = {}) => new Promise(r => { pend.set(++id, r); ws.send(JSON.stringify({id, method, params})) });
  const js = async expr => { const r = await call("Runtime.evaluate", {expression: expr, returnByValue: true, awaitPromise: true});
    if (r.exceptionDetails) throw Error(JSON.stringify(r.exceptionDetails).slice(0, 400)); return r.result.value };
  await call("Runtime.enable"); await call("Network.enable"); await call("Log.enable");
  await call("Emulation.setDeviceMetricsOverride", {width: w, height: h, deviceScaleFactor: 1, mobile: false});
  await call("Emulation.setEmulatedMedia", {features: [{name: "prefers-color-scheme", value: "dark"}, {name: "prefers-reduced-motion", value: reduce ? "reduce" : "no-preference"}]});
  await call("Page.navigate", {url: origin + "index.html"}); await sleep(3000);
  await js("document.fonts.ready.then(() => 1)");
  const shot = async (file, clip) => { const s = await call("Page.captureScreenshot", {captureBeyondViewport: clip.y + clip.height > h, clip: {...clip, scale: 1}});
    const buf = Buffer.from(s.data, "base64"); if (file) writeFileSync(file, buf); return buf };
  const close = async () => { ws.close(); await fetch(`http://127.0.0.1:${port}/json/close/${t.id}`).catch(() => {}) };
  return {js, shot, close};
}
const style = css => `(() => { const s = document.createElement("style"); s.textContent = ${JSON.stringify(css)}; document.head.append(s); return 1 })()`;

// ---- the first screen: each part's box in document px, the links a first screen shows, the H1's face
const PARTS = `(() => {
  const box = s => { const e = document.querySelector(s); if (!e || !e.getClientRects().length) return null; const b = e.getBoundingClientRect();
    return {top: Math.round(b.top + scrollY), bottom: Math.round(b.bottom + scrollY), left: Math.round(b.left), right: Math.round(b.right)} };
  const shown = e => { const b = e.getBoundingClientRect(), s = getComputedStyle(e); return b.width > 0 && b.height > 0 && b.top < innerHeight && b.bottom > 0 && s.visibility == "visible" };
  const h1 = document.querySelector(".title h1"), f = getComputedStyle(h1);
  return {fold: innerHeight, hud: box(".hud"), wordmark: box(".title .wm"), claim: box(".title .claim"), h1: box(".title h1"), lede: box(".title .lede"),
    action: box(".title .cta a"), title: box(".title"), chart: box("#stage"), console: box(".console"), fleet: box("#seats"),
    h1Face: f.fontFamily.split(",")[0] + " " + f.fontWeight + " " + f.fontSize, h1Loaded: document.fonts.check(f.fontWeight + " " + f.fontSize + " Silkscreen"),
    linksInFirstScreen: [...document.querySelectorAll("a, button")].filter(shown).map(a => (a.textContent.trim() || a.getAttribute("aria-label")).replace(/\\s+/g, " ")),
    scroll: [document.documentElement.scrollWidth, document.documentElement.clientWidth], height: document.documentElement.scrollHeight};
})()`;
// ---- the fleet's tiles: each one's box, its texts' sizes, and whether anything in it overflows
const TILES = `[...document.querySelectorAll("#seats .seat")].map(t => { const b = t.getBoundingClientRect();
  const sizes = [...t.querySelectorAll("h3, p, code")].map(e => parseFloat(getComputedStyle(e).fontSize));
  return {name: t.querySelector("h3").textContent.trim(), width: Math.round(b.width), height: Math.round(b.height), smallestText: Math.min(...sizes),
    overflow: [...t.querySelectorAll("*")].some(e => e.scrollWidth > e.clientWidth + 1 && getComputedStyle(e).overflowX != "visible") || t.scrollWidth > t.clientWidth + 1,
    badges: [...t.querySelectorAll("svg")].map(s => Math.round(s.getBoundingClientRect().width))} })`;
// ---- every text run outside the chart (slice L's COLLECT_FLAT)
const COLLECT = `(() => {
  const col = s => { const m = s.match(/rgba?\\(([^)]+)\\)/); if (!m) return null; const v = m[1].split(/[ ,\\/]+/).filter(Boolean).map(Number); return [v[0], v[1], v[2], v[3] ?? 1] };
  const op = el => { let o = 1; for (let e = el; e && e.nodeType == 1; e = e.parentElement) o *= +getComputedStyle(e).opacity; return o };
  const name = el => el.tagName.toLowerCase() + (el.id ? "#" + el.id : "") + (el.classList.length ? "." + [...el.classList].slice(0, 2).join(".") : "");
  const path = el => { const p = []; for (let e = el; e && e.nodeType == 1 && p.length < 3; e = e.parentElement) p.unshift(name(e)); return p.join(" > ") };
  const out = [], tw = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
  for (let n; n = tw.nextNode();) {
    const el = n.parentElement, s = el && getComputedStyle(el); if (!el || !n.nodeValue.trim() || /^(SCRIPT|STYLE)$/.test(el.tagName) || s.visibility != "visible" || s.display == "none") continue;
    if (el.closest(".stage")) continue;
    const o = op(el), c = col(s.color); if (o < 0.01 || !c || c[3] == 0) continue;
    const rg = document.createRange(); rg.selectNodeContents(n);
    const rects = [...rg.getClientRects()].map(r => [r.left + scrollX, r.top + scrollY, r.right + scrollX, r.bottom + scrollY]).filter(b => b[2] - b[0] >= 2 && b[3] - b[1] >= 4);
    const isNew = !!el.closest(".title, #seats") || /Deutsch|note for trying it|the Owner's signed answer|the Owner just gave/.test(el.textContent);
    if (rects.length) out.push({where: path(el), text: n.nodeValue.trim().slice(0, 48), fg: [c[0], c[1], c[2], c[3] * o], rects, isNew, overChart: !!el.closest(".title") && innerWidth >= 1280});
  }
  return {items: out, W: document.documentElement.scrollWidth, H: document.documentElement.scrollHeight};
})()`;
async function contrast(w, h) {
  const t = await open(w, h, true), {items, W, H} = await t.js(COLLECT), clip = {x: 0, y: 0, width: W, height: H};
  const D = png(await t.shot(null, clip));
  await t.js(style("*,*::before,*::after{color:transparent!important;-webkit-text-fill-color:transparent!important;text-shadow:none!important;text-decoration-color:transparent!important}"));
  const G = png(await t.shot(null, clip)); await t.close();
  return items.flatMap(it => { const g = [], ink = [];
    for (const [x0, y0, x1, y1] of it.rects) for (let y = Math.max(0, Math.floor(y0)); y < Math.min(G.h, Math.ceil(y1)); y++) for (let x = Math.max(0, Math.floor(x0)); x < Math.min(G.w, Math.ceil(x1)); x++) {
      const a = G.at(x, y), b = D.at(x, y); g.push(a); if (a[0] != b[0] || a[1] != b[1] || a[2] != b[2]) ink.push(a) }
    const under = (ink.length ? ink : g).sort((a, b) => lum(a) - lum(b)), med = under[under.length >> 1];
    if (!med) return [];                                                  // off the page: the ticker's second, hidden copy
    return [{where: it.where, text: it.text, fg: hex(it.fg) + (it.fg[3] < 1 ? `@${r2(it.fg[3])}` : ""), ground: hex(med), ratio: r2(ratio(over(it.fg, med), med)), isNew: it.isNew, overChart: it.overChart}] });
}

mkdirSync(out, {recursive: true});
const summary = {site, at: new Date().toISOString(), chrome: (await (await fetch(`http://127.0.0.1:${port}/json/version`)).json()).Browser, widths: {}};
for (const [tag, w, h] of [["phone-390", 390, 844], ["desktop-1440", 1440, 900]]) {
  const t = await open(w, h, false), parts = await t.js(PARTS), tiles = await t.js(TILES);
  await t.shot(join(out, `${tag}-first.png`), {x: 0, y: 0, width: w, height: h});
  await t.shot(join(out, `${tag}-full.png`), {x: 0, y: 0, width: w, height: await t.js("document.documentElement.scrollHeight")});
  await t.close();
  const pairs = await contrast(w, h), low = arr => arr.reduce((m, x) => !m || x.ratio < m.ratio ? x : m, null);
  summary.widths[w] = {...parts, tiles, newPairs: pairs.filter(x => x.isNew), lowestNew: low(pairs.filter(x => x.isNew)), lowestAll: low(pairs),
    below45: pairs.filter(x => x.ratio < 4.5).map(x => `${x.ratio} ${x.where} "${x.text}"`)};
}
if (preview) {
  const t = await open(1280, 900, true);
  await t.js(style(".title .claim,.title h1,.title .lede,.title .cta{display:none!important}"));
  const selected = await t.js(`(document.querySelectorAll(".wreck").forEach(b => b.setAttribute("aria-pressed", "false")), document.querySelectorAll('.wreck[aria-pressed="true"]').length)`);
  const st = await t.js(`(() => { const r = document.getElementById("stage").getBoundingClientRect(); return [r.left + scrollX, r.top + scrollY, r.width, r.height] })()`);
  // the clip: the chart's north-west 1200 × 630 at the page's own scale (k = 4, 1280 px wide: the chart spans the window and the
  // page sets the wordmark 82 px inside its west border), from its west and north borders; the east 80 px and the south 190 px of
  // the 1280 × 820 chart are cut
  const clip = {x: st[0], y: st[1], width: 1200, height: 630};
  await t.shot(preview, clip); await t.close();
  summary.preview = {file: preview, stage: st, clip, wrecksSelected: selected};
}
proc.kill(); server.close();
summary.errors = errors; summary.hostsAsked = [...asked].sort();
console.log(JSON.stringify(summary, null, 1));
