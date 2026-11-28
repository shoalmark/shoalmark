// checks.mjs STAGE [OUT.json] — FM-002 slice A's carried checks, measured in Chrome on the BUILT files STAGE holds (as
// render.mjs reads them: after/board.html beside brand/ and view/, after/site/; before/ and mock/ for the alignment):
//   contrast  every visible text pair — each text run's colour, its opacity and alpha applied, against the pixels under
//             its glyphs: two captures, the page as it is and with all text made transparent; a pixel that differs is
//             ink, and the transparent capture gives the ground under it. The median ground is the pair's, the worst
//             (a chart line under a glyph) its floor. Each ::before/::after with text and each placeholder against its
//             own background composited over its host's and their ancestors' (the chart's figures: the page's ground);
//             ::selection; hovered controls forced by DevTools. A control element of known colours (#767676 on
//             #ffffff, 4.54:1) goes through the same pipeline first.
//   AU-16     Chrome's accessibility tree: no chart figure and no drawn marker is read; the control run removes every
//             `/ ""` alt text from the page's CSS and must then read both
//   AU-18     the Owner's box: its content width in its own font's `0` advance, and its longest rendered line of prose
//   alignment the tracker view (#=FM-002): the header's box and the view's position, after against the mock and before
// Offline as render.mjs: every host unresolvable but the site's two Google Fonts hosts; the site served from 127.0.0.1,
// the board opened as a file. Node 22 or later.
import {spawn} from "node:child_process";
import {createServer} from "node:http";
import {mkdtempSync, readFileSync, writeFileSync, cpSync, existsSync, statSync} from "node:fs";
import {tmpdir} from "node:os";
import {join, resolve} from "node:path";
import {inflateSync} from "node:zlib";

const stage = resolve(process.argv[2] ?? "."), outFile = process.argv[3] ? resolve(process.argv[3]) : null;
const chrome = process.env.CHROME ?? "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome";
const port = 9400 + Math.floor(Math.random() * 500), sleep = ms => new Promise(r => setTimeout(r, ms));
const offline = "MAP * ~NOTFOUND, EXCLUDE fonts.googleapis.com, EXCLUDE fonts.gstatic.com, EXCLUDE 127.0.0.1";
const proc = spawn(chrome, ["--headless=new", "--disable-gpu", `--remote-debugging-port=${port}`, `--host-resolver-rules=${offline}`,
  `--user-data-dir=${mkdtempSync(join(tmpdir(), "slice-a-checks-"))}`, "about:blank"], {stdio: "ignore"});
for (let i = 0; i < 60; i++) { try { await fetch(`http://127.0.0.1:${port}/json/version`); break } catch { await sleep(250) } }
// the site is served from 127.0.0.1, as a host serves it: from file:// Zensical hides its search, so a page opened as a
// file is not the page a reader sees. The board is opened as a file, as its reader opens it.
let docroot = stage;
const TYPES = {html: "text/html", css: "text/css", js: "text/javascript", json: "application/json", svg: "image/svg+xml",
  png: "image/png", woff2: "font/woff2", xml: "application/xml", txt: "text/plain"};
const server = createServer((q, s) => { const f = join(docroot, decodeURIComponent(new URL(q.url, "http://x").pathname));
  if (!f.startsWith(docroot) || !existsSync(f) || statSync(f).isDirectory()) { s.writeHead(404); return s.end() }
  s.writeHead(200, {"content-type": TYPES[f.split(".").pop()] ?? "application/octet-stream"}); s.end(readFileSync(f)) });
await new Promise(r => server.listen(0, "127.0.0.1", r));
const served = rel => `http://127.0.0.1:${server.address().port}/${rel}`;

// ---- a PNG, decoded: Chrome's captures are 8-bit RGB or RGBA, not interlaced
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
const ratio = (a, b) => { const [x, y] = [lum(a), lum(b)].sort((m, n) => n - m); return (x + 0.05) / (y + 0.05) };
const over = ([r, g, b, a], [R, G, B]) => [r * a + R * (1 - a), g * a + G * (1 - a), b * a + B * (1 - a)].map(Math.round);
const hex = c => "#" + c.slice(0, 3).map(v => Math.round(v).toString(16).padStart(2, "0")).join("");

// ---- a tab
async function open(url, scheme, w, h, site, prep) {
  const t = await (await fetch(`http://127.0.0.1:${port}/json/new?about:blank`, {method: "PUT"})).json();
  const ws = new WebSocket(t.webSocketDebuggerUrl); await new Promise(r => ws.onopen = r);
  let id = 0; const pend = new Map();
  ws.onmessage = e => { const m = JSON.parse(e.data); if (pend.has(m.id)) { pend.get(m.id)(m.result ?? {error: m.error}); pend.delete(m.id) } };
  const call = (method, params = {}) => new Promise(r => { pend.set(++id, r); ws.send(JSON.stringify({id, method, params})) });
  const js = async (expr) => { const r = await call("Runtime.evaluate", {expression: expr, returnByValue: true, awaitPromise: true});
    if (r.exceptionDetails) throw Error(JSON.stringify(r.exceptionDetails).slice(0, 400)); return r.result.value };
  await call("Emulation.setDeviceMetricsOverride", {width: w, height: h, deviceScaleFactor: 1, mobile: false});
  await call("Emulation.setEmulatedMedia", {features: [{name: "prefers-color-scheme", value: scheme}]});
  await call("Page.navigate", {url}); await sleep(1800);
  if (site) await js(`document.body.setAttribute("data-md-color-scheme", "${scheme == "dark" ? "slate" : "default"}")`), await sleep(400);
  if (prep) await js(prep), await sleep(500);
  await js("document.fonts.ready.then(() => 1)");
  const close = async () => { ws.close(); await fetch(`http://127.0.0.1:${port}/json/close/${t.id}`).catch(() => {}) };
  return {call, js, close};
}

// ---- in the page: every text run, pseudo text, placeholder and selection, with its colour and boxes (document px)
const COLLECT = (root) => `(() => {
  const col = s => { let m = s.match(/rgba?\\(([^)]+)\\)/); if (m) { const v = m[1].split(/[ ,\\/]+/).filter(Boolean).map(Number); return [v[0], v[1], v[2], v[3] ?? 1] }
    m = s.match(/color\\(srgb ([^)]+)\\)/); if (m) { const v = m[1].split(/[ \\/]+/).filter(Boolean).map(Number); return [v[0]*255, v[1]*255, v[2]*255, v[3] ?? 1] } return null };
  const ground = el => { const ls = []; for (let e = el; e; e = e.parentElement) { const c = col(getComputedStyle(e).backgroundColor);
    if (c && c[3] > 0) { ls.push(c); if (c[3] >= 1) break } } let g = [255, 255, 255];
    for (const c of ls.reverse()) g = [0, 1, 2].map(i => c[i] * c[3] + g[i] * (1 - c[3])); return g };
  const onto = (c, g) => !c || c[3] == 0 ? g : [0, 1, 2].map(i => c[i] * c[3] + g[i] * (1 - c[3]));
  const op = el => { let o = 1; for (let e = el; e && e.nodeType == 1; e = e.parentElement) o *= +getComputedStyle(e).opacity; return o };
  const vis = el => { const s = getComputedStyle(el); return s.visibility == "visible" && s.display != "none" };
  const name = el => el.tagName.toLowerCase() + (el.id ? "#" + el.id : "") + (el.classList.length ? "." + [...el.classList].slice(0, 2).join(".") : "");
  const path = el => { const p = []; for (let e = el; e && e.nodeType == 1 && p.length < 3; e = e.parentElement) p.unshift(name(e)); return p.join(" > ") };
  const sx = scrollX, sy = scrollY, W = document.documentElement.scrollWidth, H = document.documentElement.scrollHeight;
  const box = r => [Math.max(0, r.left + sx), Math.max(0, r.top + sy), Math.min(W, r.right + sx), Math.min(H, r.bottom + sy)];
  const out = [], root = ${root ? `document.querySelector(${JSON.stringify(root)})` : "document.documentElement"};
  const tw = document.createTreeWalker(root, NodeFilter.SHOW_TEXT);
  for (let n; n = tw.nextNode();) {
    const el = n.parentElement; if (!el || !n.nodeValue.trim() || /^(SCRIPT|STYLE|TITLE|NOSCRIPT|TEMPLATE)$/.test(el.tagName) || !vis(el)) continue;
    const o = op(el); if (o < 0.01) continue;
    const s = getComputedStyle(el), c = col(s.color); if (!c || c[3] == 0) continue;
    const rg = document.createRange(); rg.selectNodeContents(n);
    const rects = [...rg.getClientRects()].map(box).filter(b => b[2] - b[0] >= 2 && b[3] - b[1] >= 4);
    if (!rects.length) continue;
    out.push({kind: "text", where: path(el), text: n.nodeValue.trim().slice(0, 40), fg: [c[0], c[1], c[2], c[3] * o], rects});
  }
  for (const el of [root, ...root.querySelectorAll("*")]) {
    if (!vis(el) || !el.getClientRects().length) continue;   // in a display:none subtree an element has no box
    const o = op(el);
    for (const pe of ["::before", "::after"]) {
      const s = getComputedStyle(el, pe), txt = (s.content || "").match(/^"((?:[^"\\\\]|\\\\.)*)"/);
      if (!txt || !txt[1].trim() || s.display == "none" || s.visibility != "visible") continue;
      const c = col(s.color), bg = col(s.backgroundColor); if (!c || c[3] == 0 || o < 0.01) continue;
      out.push({kind: "pseudo", where: path(el) + pe, text: txt[1].trim().slice(0, 24), alt: s.content.includes("/"),
        fg: [c[0], c[1], c[2], c[3] * o], own: onto(bg, ground(el)), rects: []});
    }
    if (el.placeholder && el.getClientRects().length) {
      const s = getComputedStyle(el, "::placeholder"), c = col(s.color);
      if (c) out.push({kind: "placeholder", where: path(el) + "::placeholder", text: el.placeholder.slice(0, 24), fg: [c[0], c[1], c[2], c[3] * +s.opacity * o], own: ground(el), rects: []});
    }
  }
  const sel = getComputedStyle(document.body, "::selection"), sc = col(sel.color), sb = col(sel.backgroundColor);
  if (!${JSON.stringify(root)} && sc && sb && sb[3] > 0) out.push({kind: "selection", where: "body::selection", text: "", fg: sc, own: sb, rects: []});
  return {items: out, W, H};
})()`;
const TRANSPARENT = `(() => { const s = document.createElement("style"); s.id = "_t";
  s.textContent = "*,*::before,*::after,*::placeholder{color:transparent!important;-webkit-text-fill-color:transparent!important;text-shadow:none!important;text-decoration-color:transparent!important;caret-color:transparent!important}";
  document.head.append(s); return 1 })()`;
const CONTROL = `(() => { const d = document.createElement("div"); d.id = "_ctl"; d.textContent = "control 4.54";
  d.style.cssText = "position:absolute;left:4px;top:4px;z-index:2147483647;background:#ffffff;color:#767676;font:16px sans-serif;padding:6px;opacity:1";
  document.body.append(d); return 1 })()`;

async function capture(tab, W, H) {
  const s = await tab.call("Page.captureScreenshot", {captureBeyondViewport: true, clip: {x: 0, y: 0, width: W, height: H, scale: 1}});
  return png(Buffer.from(s.data, "base64"));
}
function measure(items, img, ink) {
  const res = [];
  for (const it of items) {
    if (it.kind == "selection") { res.push({...it, ground: hex(it.own), ratio: ratio(over(it.fg, it.own), it.own), floor: null}); continue }
    const grounds = [], under = [];
    for (const [x0, y0, x1, y1] of it.rects)
      for (let y = Math.floor(y0); y < Math.min(img.h, Math.ceil(y1)); y++)
        for (let x = Math.floor(x0); x < Math.min(img.w, Math.ceil(x1)); x++) {
          const g = img.at(x, y), i = ink.at(x, y); grounds.push(g);
          if (g[0] != i[0] || g[1] != i[1] || g[2] != i[2]) under.push(g);
        }
    if (it.own) { const g = it.own.slice(0, 3); res.push({...it, ground: hex(g), ratio: ratio(over(it.fg, g), g), floor: null}); continue }
    if (!grounds.length) continue;
    grounds.sort((a, b) => lum(a) - lum(b));
    const med = grounds[grounds.length >> 1];
    let floor = Infinity; for (const g of under.length ? under : grounds) floor = Math.min(floor, ratio(over(it.fg, g), g));
    res.push({...it, ground: hex(med), ratio: ratio(over(it.fg, med), med), floor: it.kind == "text" ? floor : null});
  }
  return res;
}
async function contrast(tab, root) {
  const {items, W, H} = await tab.js(COLLECT(root));
  const ink = await capture(tab, W, H);
  await tab.js(TRANSPARENT); const img = await capture(tab, W, H); await tab.js(`document.getElementById("_t").remove()`);
  return measure(items, img, ink);
}
async function hovered(tab, sel) {
  const doc = await tab.call("DOM.getDocument", {depth: 0}); const q = await tab.call("DOM.querySelector", {nodeId: doc.root.nodeId, selector: sel});
  if (!q.nodeId) return [];
  await tab.call("CSS.forcePseudoState", {nodeId: q.nodeId, forcedPseudoClasses: ["hover"]}); await sleep(150);
  const r = (await contrast(tab, sel)).map(x => ({...x, where: x.where + " :hover"}));
  await tab.call("CSS.forcePseudoState", {nodeId: q.nodeId, forcedPseudoClasses: []});
  return r;
}

// ---- AU-16: what the accessibility tree reads
const FIGURE = /\d°|\b\d\d'(N|E)?$|^\d\d'/, MARKERS = new Set(["#", "##", "###", "####", "//", ">", "[", "]", "[ ", " ]", "## ", "// ", "> "]);
async function axRead(tab) {
  await tab.call("Accessibility.enable");
  const {nodes} = await tab.call("Accessibility.getFullAXTree");
  const said = nodes.filter(n => !n.ignored).map(n => ({role: n.role?.value, name: String(n.name?.value ?? "")})).filter(n => n.name);
  return {figures: said.filter(n => FIGURE.test(n.name.trim())).map(n => n.name),
          markers: said.filter(n => MARKERS.has(n.name) || MARKERS.has(n.name.trim()) || (n.role == "button" && /[\[\]]/.test(n.name))).map(n => `${n.role}:${JSON.stringify(n.name)}`),
          buttons: [...new Set(said.filter(n => n.role == "button").map(n => n.name))]};
}
function controlCopy(src, dst, files) {       // the same page with every `/ ""` alt text removed from its CSS
  cpSync(src, dst, {recursive: true});
  let n = 0;
  for (const f of files) { const p = join(dst, f), t = readFileSync(p, "utf8"), u = t.replace(/(content:\s*"(?:[^"\\]|\\.)*")\s*\/\s*""/g, (m, a) => (n++, a)); writeFileSync(p, u) }
  return n;
}

// ---- run
const A = join(stage, "after"), results = {contrast: [], ax: {}, au18: {}, alignment: {}, control: {}};
const DIALOG = `(() => { const b = document.querySelector("button.act"); if (b) b.click(); return !!document.querySelector("dialog[open]") })()`;
const pages = [
  ["board", `file://${A}/board.html`, false, null],
  ["tracker view", `file://${A}/board.html#=FM-002`, false, null],
  ["dialog", `file://${A}/board.html`, false, DIALOG],
  ["site", served("after/site/index.html"), true, null],
];
const HOVER = {board: ["button.act", "#s", "#p a[href^='#=']", "tbody tr.t", "#r a"], dialog: ["#dlg button", "#dlg button.go"],
               site: [".md-nav__link:not(.md-nav__link--active)", ".md-typeset a", ".md-header__button.md-logo"], "tracker view": ["#v .md a"]};
for (const scheme of ["light", "dark"]) {
  // the pipeline's own control first: a known pair must come out at its known ratio
  { const t = await open(`file://${A}/board.html`, scheme, 1440, 1000, false, CONTROL);
    const r = (await contrast(t, "#_ctl")).find(x => x.kind == "text"); results.control[`contrast ${scheme}`] = r && {ratio: +r.ratio.toFixed(3), ground: r.ground, fg: hex(r.fg)}; await t.close() }
  for (const [label, url, site, prep] of pages)
    for (const [w, h] of label == "board" || label == "site" ? [[1440, 1000], [390, 844]] : [[1440, 1000]]) {
      const t = await open(url, scheme, w, h, site, prep);
      if (label == "dialog") results.control[`dialog open ${scheme}`] = await t.js(`!!document.querySelector("dialog[open]")`);
      const root = label == "dialog" ? "dialog[open]" : null;
      let rs = await contrast(t, root);
      for (const sel of w == 1440 ? HOVER[label] ?? [] : []) rs = rs.concat(await hovered(t, sel));
      for (const r of rs) results.contrast.push({page: label, scheme, width: w, kind: r.kind, where: r.where, text: r.text, fg: hex(r.fg) + (r.fg[3] < 1 ? `@${(+r.fg[3]).toFixed(2)}` : ""),
        ground: r.ground, ratio: +r.ratio.toFixed(2), floor: r.floor == null ? null : +r.floor.toFixed(2), alt: r.alt});
      if (w == 1440) results.ax[`${label} ${scheme}`] = await axRead(t);
      if (label == "board" && w == 1440) results.au18[scheme] = await t.js(`(() => { const p = document.getElementById("p"), s = getComputedStyle(p);
        const cv = document.createElement("canvas").getContext("2d"); cv.font = s.fontWeight + " " + s.fontSize + " " + s.fontFamily;
        const ch = cv.measureText("0").width, content = p.clientWidth - parseFloat(s.paddingLeft) - parseFloat(s.paddingRight);
        const lines = new Map(), tw = document.createTreeWalker(p, NodeFilter.SHOW_TEXT), rg = document.createRange();
        for (let n; n = tw.nextNode();) for (let i = 0; i < n.length; i++) { rg.setStart(n, i); rg.setEnd(n, i + 1);
          const r = rg.getClientRects()[0]; if (!r || !r.width) continue; const k = Math.round(r.top); lines.set(k, (lines.get(k) || 0) + 1) }
        return {font: s.fontFamily.split(",")[0] + " " + s.fontSize, contentPx: Math.round(content), chPx: +ch.toFixed(3), chars: +(content / ch).toFixed(1),
                longestLine: Math.max(...lines.values()), lines: lines.size} })()`);
      await t.close();
    }
}
// AU-16's control: the alt text removed, the same tree must read the figures and the markers
{ const ctl = mkdtempSync(join(tmpdir(), "slice-a-control-"));
  results.control.altRemoved = {board: controlCopy(A, join(ctl, "after"), ["board.html"]), site: controlCopy(join(A, "site"), join(ctl, "site"), ["stylesheets/shoalmark.css"])};
  for (const scheme of ["light", "dark"]) {
    docroot = ctl;
    for (const [label, url, site] of [["board", `file://${ctl}/after/board.html`, false], ["tracker view", `file://${ctl}/after/board.html#=FM-002`, false], ["site", served("site/index.html"), true]]) {
      const t = await open(url, scheme, 1440, 1000, site, null); const r = await axRead(t);
      results.control[`ax ${label} ${scheme}`] = {figures: r.figures.length, markers: r.markers.length, sample: [...r.markers.slice(0, 3), ...r.figures.slice(0, 2)]};
      await t.close();
    }
  }
}
// the tracker view's alignment: the header's box and the view's first line, after against the mock and before
for (const scheme of ["light", "dark"])
  for (const [when, file] of [["before", join(stage, "before", "board.html")], ["mock", join(stage, "mock", "shoalmark.html")], ["after", join(A, "board.html")]]) {
    if (!existsSync(file)) continue;
    const t = await open(`file://${file}#=FM-002`, scheme, 1440, 1000, false, null);
    results.alignment[`${when} ${scheme}`] = await t.js(`(() => { const r = e => e && e.getClientRects().length ? [...Object.values(e.getBoundingClientRect().toJSON())].slice(0, 4).map(Math.round) : null;
      return {header: r(document.getElementById("H")), view: r(document.getElementById("v")), firstHeading: r(document.querySelector("#v h1, #v h2"))} })()`);
    await t.close();
  }
proc.kill(); server.close();

// ---- the summary
const C = results.contrast, low = C.filter(r => r.ratio < 4.5 || (r.floor != null && r.floor < 4.5));
const pairs = new Map();
for (const r of C) { const k = `${r.scheme} ${r.fg} on ${r.ground}`, p = pairs.get(k) ?? {scheme: r.scheme, fg: r.fg, ground: r.ground, ratio: r.ratio, floor: null, pages: [], where: [], n: 0};
  p.n++; p.ratio = Math.min(p.ratio, r.ratio); if (r.floor != null) p.floor = Math.min(p.floor ?? Infinity, r.floor);
  const pg = `${r.page} ${r.width}`; if (!p.pages.includes(pg)) p.pages.push(pg); if (p.where.length < 3 && !p.where.includes(r.where)) p.where.push(r.where);
  pairs.set(k, p) }
results.pairs = [...pairs.values()].sort((a, b) => a.scheme.localeCompare(b.scheme) || a.ratio - b.ratio);
results.summary = Object.fromEntries(["light", "dark"].map(s => { const cs = C.filter(r => r.scheme == s);
  return [s, {measured: cs.length, pairs: results.pairs.filter(p => p.scheme == s).length, lowest: Math.min(...cs.map(r => r.ratio)),
    lowestFloor: Math.min(...cs.filter(r => r.floor != null).map(r => r.floor)), below: cs.filter(r => r.ratio < 4.5).length}] }));
results.summary.au16 = Object.fromEntries(Object.entries(results.ax).map(([k, v]) => [k, {figures: v.figures.length, markers: v.markers.length}]));
results.summary.pseudoWithoutAlt = [...new Set(C.filter(r => r.kind == "pseudo" && !r.alt).map(r => `${r.where} "${r.text}"`))];
if (outFile) writeFileSync(outFile, JSON.stringify(results, null, 1) + "\n");
console.log(JSON.stringify({summary: results.summary, control: results.control, au18: results.au18, alignment: results.alignment,
  below: low.slice(0, 40).map(r => `${r.page} ${r.scheme} ${r.width} ${r.where} "${r.text}" ${r.fg} on ${r.ground} ${r.ratio} floor ${r.floor}`)}, null, 1));
