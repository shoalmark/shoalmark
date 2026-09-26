// checks.mjs SITE OUT.json [MOCK.html] — FM-006 slice L's checks on the BUILT start page: SITE is a `zensical build`
// output (site/), served from 127.0.0.1 as a host serves it; MOCK, optional, is the evidence mock opened as a file, for the
// fonts' comparison. Chrome's DevTools protocol, offline: every host unresolvable but the two Google Fonts hosts the page
// loads. prefers-reduced-motion is emulated for every measure, so nothing moves between two captures. Node 22 or later.
//
//   chart     every chart text as drawn — the names (.name), the figures (.fig) and the wrecks' labels (.wreck span) —
//             at 1440 and 1024 px (at 700 px and less the page hides them all), by two methods:
//             R  the Reviewer's (review-the-boards-themes-record-2.md, R3): the specified colour against the ground, the
//                ground captured with the chart's text transparent and its halo off; as drawn, the layers above the text —
//                the CRT overlay (.crt) where the text lies under it, and the title's backdrop (.title) — darken the text
//                by the factor they darken the ground under its box: the ground with them over the ground without them,
//                per channel, summed over the box. The ground is the box's median pixel (by luminance).
//             S  the seat's: pixels only. The page as drawn against the same page with the chart's text transparent (its
//                halo and label backgrounds kept): a pixel that differs by 16 levels or more is ink; the glyph core is the
//                quarter of the ink that differs most; the text is the core's median pixel as drawn, the ground the
//                median pixel under the core with the text transparent.
//   flat      every other text run on the page, at 1440, 1024 and 390 px: its colour (opacity and alpha applied) over the
//             median pixel under its glyphs, the ground captured with all text transparent (FM-002 slice A's method).
//   page      script errors and failed requests; sideways scroll; the accessibility tree — the focusable wrecks, the
//             canvas's description, no chart figure read; reduced motion — two captures 7 s apart; the scheme — the page
//             under a light and a dark preference; the fonts — the faces the page loaded, and the mock's.
import {spawn} from "node:child_process";
import {createServer} from "node:http";
import {existsSync, mkdtempSync, readFileSync, statSync, writeFileSync} from "node:fs";
import {tmpdir} from "node:os";
import {join, resolve} from "node:path";
import {inflateSync} from "node:zlib";

const site = resolve(process.argv[2] ?? "site"), outFile = resolve(process.argv[3] ?? "checks.json"), mock = process.argv[4] ? resolve(process.argv[4]) : null;
const chrome = process.env.CHROME ?? "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome";
const port = 9400 + Math.floor(Math.random() * 500), sleep = ms => new Promise(r => setTimeout(r, ms));
const offline = "MAP * ~NOTFOUND, EXCLUDE fonts.googleapis.com, EXCLUDE fonts.gstatic.com, EXCLUDE 127.0.0.1";
const proc = spawn(chrome, ["--headless=new", "--disable-gpu", "--hide-scrollbars", `--remote-debugging-port=${port}`, `--host-resolver-rules=${offline}`,
  `--user-data-dir=${mkdtempSync(join(tmpdir(), "slice-l-checks-"))}`, "about:blank"], {stdio: "ignore"});
for (let i = 0; i < 80; i++) { try { await fetch(`http://127.0.0.1:${port}/json/version`); break } catch { await sleep(250) } }
const TYPES = {html: "text/html", css: "text/css", js: "text/javascript", json: "application/json", svg: "image/svg+xml", png: "image/png", woff2: "font/woff2", xml: "application/xml", txt: "text/plain"};
const server = createServer((q, s) => { const f = join(site, decodeURIComponent(new URL(q.url, "http://x").pathname));
  if (!f.startsWith(site) || !existsSync(f) || statSync(f).isDirectory()) { s.writeHead(404); return s.end() }
  s.writeHead(200, {"content-type": TYPES[f.split(".").pop()] ?? "application/octet-stream"}); s.end(readFileSync(f)) });
await new Promise(r => server.listen(0, "127.0.0.1", r));
const PAGE = `http://127.0.0.1:${server.address().port}/index.html`, origin = `http://127.0.0.1:${server.address().port}/`;

// ---- a PNG, decoded: Chrome's captures are 8-bit RGB or RGBA, not interlaced (slice A's decoder)
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
  return {w, h, px, bpp, at: (x, y) => { const i = (y * w + x) * bpp; return [px[i], px[i + 1], px[i + 2]] }};
}
const lin = c => (c /= 255) <= 0.03928 ? c / 12.92 : ((c + 0.055) / 1.055) ** 2.4;
const lum = ([r, g, b]) => 0.2126 * lin(r) + 0.7152 * lin(g) + 0.0722 * lin(b);
const ratioL = (a, b) => (Math.max(a, b) + 0.05) / (Math.min(a, b) + 0.05);
const ratio = (a, b) => ratioL(lum(a), lum(b));
const over = ([r, g, b, a], [R, G, B]) => [r * a + R * (1 - a), g * a + G * (1 - a), b * a + B * (1 - a)];
const hex = c => "#" + c.slice(0, 3).map(v => Math.max(0, Math.min(255, Math.round(v))).toString(16).padStart(2, "0")).join("");
const r2 = v => Math.round(v * 100) / 100;

// ---- a tab
const log = {errors: [], refused: new Set(), reached: new Set()};
async function open(w, h, {scheme = "dark", reduce = true} = {}, url = PAGE) {
  const t = await (await fetch(`http://127.0.0.1:${port}/json/new?about:blank`, {method: "PUT"})).json();
  const ws = new WebSocket(t.webSocketDebuggerUrl); await new Promise(r => ws.onopen = r);
  let id = 0; const pend = new Map(), asked = new Map();
  ws.onmessage = e => { const m = JSON.parse(e.data), p = m.params;
    if (m.method == "Runtime.exceptionThrown") log.errors.push(`${w}px: ${p.exceptionDetails.exception?.description ?? p.exceptionDetails.text}`);
    if (m.method == "Runtime.consoleAPICalled" && p.type == "error") log.errors.push(`${w}px console: ${p.args.map(a => a.value ?? a.description).join(" ")}`);
    if (m.method == "Network.requestWillBeSent" && !/^(file|data|about|blob):/.test(p.request.url) && !p.request.url.startsWith(origin)) asked.set(p.requestId, new URL(p.request.url).host);
    if (m.method == "Network.responseReceived" && asked.has(p.requestId)) log.reached.add(asked.get(p.requestId));
    if (m.method == "Network.loadingFailed" && asked.has(p.requestId)) log.refused.add(asked.get(p.requestId));
    if (pend.has(m.id)) { pend.get(m.id)(m.result ?? {error: m.error}); pend.delete(m.id) } };
  const call = (method, params = {}) => new Promise(r => { pend.set(++id, r); ws.send(JSON.stringify({id, method, params})) });
  const js = async (expr) => { const r = await call("Runtime.evaluate", {expression: expr, returnByValue: true, awaitPromise: true});
    if (r.exceptionDetails) throw Error(JSON.stringify(r.exceptionDetails).slice(0, 400)); return r.result.value };
  await call("Runtime.enable"); await call("Network.enable");
  await call("Emulation.setDeviceMetricsOverride", {width: w, height: h, deviceScaleFactor: 1, mobile: false});
  await call("Emulation.setEmulatedMedia", {features: [{name: "prefers-color-scheme", value: scheme}, {name: "prefers-reduced-motion", value: reduce ? "reduce" : "no-preference"}]});
  await call("Page.navigate", {url}); await sleep(2600);
  await js("document.fonts.ready.then(() => 1)");
  const close = async () => { ws.close(); await fetch(`http://127.0.0.1:${port}/json/close/${t.id}`).catch(() => {}) };
  return {call, js, close};
}
async function capture(tab, [x, y, w, h]) {
  const s = await tab.call("Page.captureScreenshot", {captureBeyondViewport: true, clip: {x, y, width: w, height: h, scale: 1}});
  return png(Buffer.from(s.data, "base64"));
}
const style = (id, css) => `(() => { const s = document.createElement("style"); s.id = ${JSON.stringify(id)}; s.textContent = ${JSON.stringify(css)}; document.head.append(s); return 1 })()`;
const unstyle = id => `(document.getElementById(${JSON.stringify(id)})?.remove(), 1)`;
const CHART = ".stage .name,.stage .fig,.stage .wreck span";
const CHART_T = `${CHART}{color:transparent!important;-webkit-text-fill-color:transparent!important}`;
const CHART_T_BARE = `${CHART}{color:transparent!important;-webkit-text-fill-color:transparent!important;text-shadow:none!important}`;

// ---- in the page: the chart's texts, their colour, box (document px) and whether they lie under the CRT overlay
const COLLECT_CHART = `(() => {
  const col = s => { const m = s.match(/rgba?\\(([^)]+)\\)/); const v = m[1].split(/[ ,\\/]+/).filter(Boolean).map(Number); return [v[0], v[1], v[2], v[3] ?? 1] };
  const z = el => { for (let e = el; e; e = e.parentElement) { const s = getComputedStyle(e); if (s.zIndex != "auto") return +s.zIndex } return 0 };
  const crt = +getComputedStyle(document.querySelector(".crt")).zIndex, title = document.querySelector(".title"), tr = title.getBoundingClientRect();
  const titleOver = getComputedStyle(title).position == "absolute";
  const st = document.getElementById("stage").getBoundingClientRect(), sx = scrollX, sy = scrollY;
  const out = [];
  for (const el of document.querySelectorAll(${JSON.stringify(CHART)})) {
    const s = getComputedStyle(el); if (s.display == "none" || s.visibility != "visible" || !el.getClientRects().length) continue;
    const r = el.getBoundingClientRect(); if (r.width < 1 || r.height < 1) continue;
    const kind = el.classList.contains("fig") ? "figure" : el.classList.contains("name") ? "name" : "wreck label";
    const x0 = Math.max(Math.floor(r.left), Math.floor(st.left)), x1 = Math.min(Math.ceil(r.right), Math.ceil(st.right));
    const y0 = Math.max(Math.floor(r.top), Math.floor(st.top)), y1 = Math.min(Math.ceil(r.bottom), Math.ceil(st.bottom));
    const underTitle = titleOver && r.right > tr.left && r.left < tr.right && r.bottom > tr.top && r.top < tr.bottom;
    out.push({kind, text: el.textContent.trim(), cls: el.className, fg: col(s.color), z: z(el), underCrt: z(el) < crt, underTitle,
      box: [x0 + sx, y0 + sy, x1 + sx, y1 + sy]});
  }
  return {items: out, stage: [st.left + sx, st.top + sy, st.width, st.height], crt};
})()`;

function chartMeasure(items, clip, D, T, Gall, GnoC, Gnone) {
  const [cx, cy] = clip, res = [];
  for (const it of items) {
    const [x0, y0, x1, y1] = it.box.map(Math.round), px = [];
    for (let y = y0; y < y1; y++) for (let x = x0; x < x1; x++) { const u = x - cx, v = y - cy; if (u >= 0 && v >= 0 && u < D.w && v < D.h) px.push([u, v]) }
    if (!px.length) continue;
    // R — the Reviewer's method
    const grounds = px.map(([u, v]) => Gall.at(u, v)).sort((a, b) => lum(a) - lum(b)), gmed = grounds[grounds.length >> 1];
    const above = it.underCrt ? Gall : it.underTitle ? GnoC : null;          // the layers over the text, applied to the ground
    let f = [1, 1, 1];
    if (above) { const s = [0, 0, 0], t = [0, 0, 0]; for (const [u, v] of px) { const a = above.at(u, v), b = Gnone.at(u, v); for (let i = 0; i < 3; i++) { s[i] += a[i]; t[i] += b[i] } } f = s.map((v, i) => t[i] ? Math.min(1, v / t[i]) : 1) }
    const fg = over(it.fg, gmed), drawnR = fg.map((v, i) => v * f[i]);
    const R = ratio(drawnR, gmed);
    // S — the seat's method: ink against the ground under it, both as drawn
    const ink = [];
    for (const [u, v] of px) { const a = D.at(u, v), b = T.at(u, v); const d = Math.max(Math.abs(a[0] - b[0]), Math.abs(a[1] - b[1]), Math.abs(a[2] - b[2])); if (d >= 16) ink.push({a: lum(a), b: lum(b), d: Math.abs(lum(a) - lum(b))}) }
    let S = null, core = 0;
    if (ink.length) { ink.sort((m, n) => n.d - m.d); const c = ink.slice(0, Math.max(1, Math.ceil(ink.length / 4))); core = c.length;
      const med = arr => arr.sort((m, n) => m - n)[arr.length >> 1];
      S = ratioL(med(c.map(q => q.a)), med(c.map(q => q.b))) }
    res.push({kind: it.kind, text: it.text, fg: hex(it.fg), z: it.z, underCrt: it.underCrt, underTitle: it.underTitle, ground: hex(gmed),
      darkening: f.map(r2), reviewer: r2(R), seat: S == null ? null : r2(S), ink: ink.length, core});
  }
  return res;
}

async function chart(w, h) {
  const t = await open(w, h);
  const {items, stage} = await t.js(COLLECT_CHART);
  // the clip: the stage, and the title where it lies over the chart
  const clip = [Math.floor(stage[0]), Math.floor(stage[1]), Math.ceil(stage[2]), Math.ceil(stage[3])];
  const D = await capture(t, clip);
  await t.js(style("_t", CHART_T)); const T = await capture(t, clip); await t.js(unstyle("_t"));
  await t.js(style("_t", CHART_T_BARE)); const Gall = await capture(t, clip);
  await t.js(style("_c", ".crt{visibility:hidden!important}")); const GnoC = await capture(t, clip);
  await t.js(style("_d", ".title{visibility:hidden!important}")); const Gnone = await capture(t, clip);
  await t.close();
  return {width: w, count: items.length, texts: chartMeasure(items, clip, D, T, Gall, GnoC, Gnone)};
}

// ---- every other text run: its colour over the median pixel under its glyphs (the chart's texts and the title's excluded)
const COLLECT_FLAT = `(() => {
  const col = s => { const m = s.match(/rgba?\\(([^)]+)\\)/); if (!m) return null; const v = m[1].split(/[ ,\\/]+/).filter(Boolean).map(Number); return [v[0], v[1], v[2], v[3] ?? 1] };
  const op = el => { let o = 1; for (let e = el; e && e.nodeType == 1; e = e.parentElement) o *= +getComputedStyle(e).opacity; return o };
  const vis = el => { const s = getComputedStyle(el); return s.visibility == "visible" && s.display != "none" };
  const name = el => el.tagName.toLowerCase() + (el.id ? "#" + el.id : "") + (el.classList.length ? "." + [...el.classList].slice(0, 2).join(".") : "");
  const path = el => { const p = []; for (let e = el; e && e.nodeType == 1 && p.length < 3; e = e.parentElement) p.unshift(name(e)); return p.join(" > ") };
  const sx = scrollX, sy = scrollY, W = document.documentElement.scrollWidth, H = document.documentElement.scrollHeight;
  const out = [], tw = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
  for (let n; n = tw.nextNode();) {
    const el = n.parentElement; if (!el || !n.nodeValue.trim() || /^(SCRIPT|STYLE)$/.test(el.tagName) || !vis(el)) continue;
    if (el.closest(".stage")) continue;                                    // the chart's texts: measured as drawn above
    const o = op(el); if (o < 0.01) continue;
    const c = col(getComputedStyle(el).color); if (!c || c[3] == 0) continue;
    const rg = document.createRange(); rg.selectNodeContents(n);
    const rects = [...rg.getClientRects()].map(r => [r.left + sx, r.top + sy, r.right + sx, r.bottom + sy]).filter(b => b[2] - b[0] >= 2 && b[3] - b[1] >= 4);
    if (rects.length) out.push({where: path(el), text: n.nodeValue.trim().slice(0, 40), fg: [c[0], c[1], c[2], c[3] * o], rects, title: !!el.closest(".title")});
  }
  return {items: out, W, H};
})()`;
async function flat(w, h) {
  const t = await open(w, h);
  const {items, W, H} = await t.js(COLLECT_FLAT);
  const clip = [0, 0, W, H], D = await capture(t, clip);
  await t.js(style("_t", "*,*::before,*::after{color:transparent!important;-webkit-text-fill-color:transparent!important;text-shadow:none!important;text-decoration-color:transparent!important}"));
  const G = await capture(t, clip);
  const scroll = await t.js("[document.documentElement.scrollWidth, document.documentElement.clientWidth]");
  await t.close();
  const res = [];
  for (const it of items) {
    const g = [], ink = [];
    for (const [x0, y0, x1, y1] of it.rects) for (let y = Math.floor(y0); y < Math.min(G.h, Math.ceil(y1)); y++) for (let x = Math.floor(x0); x < Math.min(G.w, Math.ceil(x1)); x++) {
      const a = G.at(x, y), b = D.at(x, y); g.push(a); if (a[0] != b[0] || a[1] != b[1] || a[2] != b[2]) ink.push(a) }
    const under = (ink.length ? ink : g).sort((a, b) => lum(a) - lum(b)); if (!under.length) continue;
    const med = under[under.length >> 1];
    res.push({where: it.where, text: it.text, fg: hex(it.fg) + (it.fg[3] < 1 ? `@${r2(it.fg[3])}` : ""), ground: hex(med), ratio: r2(ratio(over(it.fg, med), med)), overChart: it.title && w >= 1280});
  }
  return {width: w, scroll, count: res.length, texts: res};
}

// ---- the page: the accessibility tree, motion, the scheme, the fonts
const FIGURE = /\d°\d\d'[NE]/;
async function tree(w, h) {
  const t = await open(w, h);
  await t.call("Accessibility.enable");
  const {nodes} = await t.call("Accessibility.getFullAXTree");
  const said = nodes.filter(n => !n.ignored).map(n => ({role: n.role?.value, name: String(n.name?.value ?? ""), focusable: !!n.properties?.find(p => p.name == "focusable" && p.value.value)}));
  const wrecks = said.filter(n => n.role == "button" && /^FM-\d+, /.test(n.name));
  const canvas = said.filter(n => /^(img|image)$/.test(n.role) && /night chart/.test(n.name)).map(n => `${n.role}: ${n.name}`);
  const figures = said.filter(n => FIGURE.test(n.name)).map(n => `${n.role}: ${n.name.slice(0, 80)}`);
  // the chart's names and figures: no node of the tree is theirs (their text nodes' backend ids, read from the DOM)
  const doc = await t.call("DOM.getDocument", {depth: 0}), ids = new Set();
  for (const sel of [".stage .name", ".stage .fig"]) for (const nodeId of (await t.call("DOM.querySelectorAll", {nodeId: doc.root.nodeId, selector: sel})).nodeIds) {
    const {node} = await t.call("DOM.describeNode", {nodeId, depth: 1}); ids.add(node.backendNodeId); for (const c of node.children ?? []) ids.add(c.backendNodeId) }
  const namesRead = nodes.filter(n => !n.ignored && ids.has(n.backendDOMNodeId)).map(n => `${n.role?.value}: ${n.name?.value ?? ""}`);
  await t.close();
  return {width: w, wrecks: wrecks.length, focusable: wrecks.filter(n => n.focusable).length, wreckNames: wrecks.map(n => n.name), canvas, figures, chartNamesRead: namesRead};
}
function same(a, b) { if (a.w != b.w || a.h != b.h) return false; return Buffer.compare(a.px, b.px) == 0 }
function diffShare(a, b) { let n = 0; for (let i = 0; i < a.px.length; i += a.bpp) if (a.px[i] != b.px[i] || a.px[i + 1] != b.px[i + 1] || a.px[i + 2] != b.px[i + 2]) n++; return n / (a.w * a.h) }
async function motion() {
  const t = await open(1440, 900), [W, H] = await t.js("[document.documentElement.scrollWidth, document.documentElement.scrollHeight]");
  const a = await capture(t, [0, 0, W, H]); await sleep(7000); const b = await capture(t, [0, 0, W, H]); await t.close();
  return {reduced: {identical: same(a, b), height: H}};
}
async function scheme() {
  const out = {};
  for (const w of [1440, 390]) {
    const d = await open(w, 900, {scheme: "dark"}), l = await open(w, 900, {scheme: "light"});
    const a = await capture(d, [0, 0, w, 900]), b = await capture(l, [0, 0, w, 900]);
    out[w] = {identical: same(a, b), differing: diffShare(a, b), colorScheme: await l.js("getComputedStyle(document.documentElement).colorScheme")};
    await d.close(); await l.close();
  }
  return out;
}
const FONTS = `document.fonts.ready.then(() => [...document.fonts].filter(f => f.status == "loaded").map(f => [f.family.replace(/"/g, ""), f.weight, f.style].join(" ")).filter((v, i, a) => a.indexOf(v) == i).sort())`;
const LINKS = `[...document.querySelectorAll("link[rel=stylesheet],link[rel=preconnect]")].map(l => l.rel + " " + l.href)`;
async function fonts() {
  const t = await open(1440, 900, {reduce: false}); await t.js("window.scrollTo(0, document.body.scrollHeight)"); await sleep(1500);
  const built = {loaded: await t.js(FONTS), links: await t.js(LINKS)}; await t.close();
  let theMock = null;
  if (mock) { const m = await open(1440, 900, {reduce: false}, "file://" + mock); await m.js("window.scrollTo(0, document.body.scrollHeight)"); await sleep(1500);
    theMock = {loaded: await m.js(FONTS), links: await m.js(LINKS)}; await m.close() }
  return {built, mock: theMock, sameFaces: theMock ? JSON.stringify(built.loaded) == JSON.stringify(theMock.loaded) : null};
}

// ---- run
const results = {site, at: new Date().toISOString(), chart: [], flat: [], tree: [], motion: null, scheme: null, fonts: null};
for (const [w, h] of [[1440, 900], [1024, 900]]) results.chart.push(await chart(w, h));
for (const [w, h] of [[1440, 900], [1024, 900], [390, 844]]) { results.flat.push(await flat(w, h)); results.tree.push(await tree(w, h)) }
results.motion = await motion();
results.scheme = await scheme();
results.fonts = await fonts();
results.errors = log.errors; results.hosts = {reached: [...log.reached].sort(), refused: [...log.refused].sort()};
proc.kill(); server.close();
// the summary
const low = (xs, k) => xs.reduce((m, x) => x[k] != null && (m == null || x[k] < m[k]) ? x : m, null);
results.summary = {
  chart: results.chart.map(c => { const R = low(c.texts, "reviewer"), S = low(c.texts, "seat");
    return {width: c.width, texts: c.count, lowestReviewer: R && `${R.reviewer} ${R.kind} ${R.text}`, lowestSeat: S && `${S.seat} ${S.kind} ${S.text}`,
      belowReviewer: c.texts.filter(x => x.reviewer < 4.5).map(x => `${x.reviewer} ${x.text}${x.underTitle ? " (under the title)" : ""}`),
      belowSeat: c.texts.filter(x => x.seat != null && x.seat < 4.5).map(x => `${x.seat} ${x.text}${x.underTitle ? " (under the title)" : ""}`),
      noInk: c.texts.filter(x => x.seat == null).map(x => x.text)} }),
  flat: results.flat.map(f => { const L = low(f.texts.filter(x => !x.overChart), "ratio"); return {width: f.width, runs: f.count, lowest: L && `${L.ratio} ${L.where} "${L.text}" ${L.fg} on ${L.ground}`,
    below: f.texts.filter(x => x.ratio < 4.5 && !x.overChart).map(x => `${x.ratio} ${x.where} "${x.text}"`), scroll: f.scroll} }),
  tree: results.tree.map(t => ({width: t.width, wrecks: t.wrecks, focusable: t.focusable, canvasDescribed: t.canvas.length == 1, figuresRead: t.figures.length, chartNamesRead: t.chartNamesRead.length})),
  errors: results.errors.length, hosts: results.hosts, motion: results.motion, scheme: results.scheme, sameFacesAsMock: results.fonts.sameFaces};
writeFileSync(outFile, JSON.stringify(results, null, 1) + "\n");
console.log(JSON.stringify(results.summary, null, 1));
