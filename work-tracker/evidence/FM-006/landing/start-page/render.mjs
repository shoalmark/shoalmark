// render.mjs STAGE [SHOTS] — FM-006 slice L's renders of the BUILT start page. STAGE holds `zensical build` outputs, each
// as a commit builds it (README.md, "Rebuild"): page/ — the slice's tip — and, for R3's before and after, r3-before/ (the
// mock as the site builds it, item 1) and r3-after/ (item 2: the chart's names and figures above the CRT overlay). Each is
// served from 127.0.0.1, as a host serves it. Chrome's DevTools protocol, offline: every host unresolvable but the two
// Google Fonts hosts the page loads; requests.json lists, per render, the hosts reached and refused. The page is dark by
// choice (`color-scheme: dark`, no scheme query): it is rendered under a dark preference; checks.mjs shows a light one
// gives the same pixels. CHROME names the browser (default: macOS's Google Chrome). Node 22 or later.
//   start-<w>.png, start-<w>-full.png   the first screen and the whole page, 1440, 1024 and 390 px, motion allowed,
//                                        captured 3 s after load (the chart has drawn in; the console shows the first open wreck)
//   reduced-<w>.png                      the first screen under prefers-reduced-motion: reduce
//   r3-before-<w>.png, r3-after-<w>.png  the chart alone (the stage), 1440 and 1024 px, reduced motion, before and after R3
import {spawn} from "node:child_process";
import {createServer} from "node:http";
import {existsSync, mkdirSync, mkdtempSync, readFileSync, statSync, writeFileSync} from "node:fs";
import {tmpdir} from "node:os";
import {join, resolve} from "node:path";

const stage = resolve(process.argv[2] ?? "."), shots = resolve(process.argv[3] ?? join(stage, "shots"));
const chrome = process.env.CHROME ?? "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome";
const port = 9400 + Math.floor(Math.random() * 500), sleep = ms => new Promise(r => setTimeout(r, ms));
const offline = "MAP * ~NOTFOUND, EXCLUDE fonts.googleapis.com, EXCLUDE fonts.gstatic.com, EXCLUDE 127.0.0.1";
const proc = spawn(chrome, ["--headless=new", "--disable-gpu", "--hide-scrollbars", `--remote-debugging-port=${port}`, `--host-resolver-rules=${offline}`,
  `--user-data-dir=${mkdtempSync(join(tmpdir(), "slice-l-render-"))}`, "about:blank"], {stdio: "ignore"});
for (let i = 0; i < 80; i++) { try { await fetch(`http://127.0.0.1:${port}/json/version`); break } catch { await sleep(250) } }
const TYPES = {html: "text/html", css: "text/css", js: "text/javascript", json: "application/json", svg: "image/svg+xml", png: "image/png", woff2: "font/woff2", xml: "application/xml", txt: "text/plain"};
const server = createServer((q, s) => { const f = join(stage, decodeURIComponent(new URL(q.url, "http://x").pathname));
  if (!f.startsWith(stage) || !existsSync(f) || statSync(f).isDirectory()) { s.writeHead(404); return s.end() }
  s.writeHead(200, {"content-type": TYPES[f.split(".").pop()] ?? "application/octet-stream"}); s.end(readFileSync(f)) });
await new Promise(r => server.listen(0, "127.0.0.1", r));
const served = rel => `http://127.0.0.1:${server.address().port}/${rel}`;

const log = {};
async function shot(dir, file, w, h, {reduce = false, full = false, chart = false} = {}) {
  const t = await (await fetch(`http://127.0.0.1:${port}/json/new?about:blank`, {method: "PUT"})).json();
  const ws = new WebSocket(t.webSocketDebuggerUrl); await new Promise(r => ws.onopen = r);
  let id = 0; const pend = new Map(), asked = new Map(), reached = [], refused = [], errors = [];
  ws.onmessage = e => { const m = JSON.parse(e.data), p = m.params;
    if (m.method == "Network.requestWillBeSent" && !/^(file|data|about|blob):/.test(p.request.url) && !p.request.url.startsWith(served(""))) asked.set(p.requestId, new URL(p.request.url).host);
    if (m.method == "Network.responseReceived" && asked.has(p.requestId)) reached.push(asked.get(p.requestId));
    if (m.method == "Network.loadingFailed" && asked.has(p.requestId)) refused.push(asked.get(p.requestId));
    if (m.method == "Runtime.exceptionThrown") errors.push(p.exceptionDetails.exception?.description ?? p.exceptionDetails.text);
    if (pend.has(m.id)) { pend.get(m.id)(m.result); pend.delete(m.id) } };
  const call = (method, params = {}) => new Promise(r => { pend.set(++id, r); ws.send(JSON.stringify({id, method, params})) });
  const js = async expression => (await call("Runtime.evaluate", {expression, returnByValue: true, awaitPromise: true})).result.value;
  await call("Network.enable"); await call("Runtime.enable");
  await call("Emulation.setDeviceMetricsOverride", {width: w, height: h, deviceScaleFactor: 1, mobile: false});
  await call("Emulation.setEmulatedMedia", {features: [{name: "prefers-color-scheme", value: "dark"}, {name: "prefers-reduced-motion", value: reduce ? "reduce" : "no-preference"}]});
  await call("Page.navigate", {url: served(`${dir}/index.html`)}); await sleep(3000);
  await js("document.fonts.ready.then(() => 1)");
  let clip = {x: 0, y: 0, width: w, height: h, scale: 1};
  if (full) clip.height = await js("document.documentElement.scrollHeight");
  if (chart) { const r = await js(`(() => { const r = document.getElementById("stage").getBoundingClientRect(); return [r.left + scrollX, r.top + scrollY, r.width, r.height] })()`);
    clip = {x: r[0], y: r[1], width: r[2], height: r[3], scale: 1} }
  const s = await call("Page.captureScreenshot", {captureBeyondViewport: full || chart, clip});
  writeFileSync(join(shots, file), Buffer.from(s.data, "base64")); ws.close();
  await fetch(`http://127.0.0.1:${port}/json/close/${t.id}`).catch(() => {});
  log[file] = {page: dir, width: w, height: clip.height, reduce, reached: [...new Set(reached)].sort(), refused: [...new Set(refused)].sort(), errors};
}

mkdirSync(shots, {recursive: true});
for (const [w, h] of [[1440, 900], [1024, 900], [390, 844]]) {
  await shot("page", `start-${w}.png`, w, h);
  await shot("page", `start-${w}-full.png`, w, h, {full: true});
  await shot("page", `reduced-${w}.png`, w, h, {reduce: true});
}
for (const w of [1440, 1024])
  for (const when of ["before", "after"])
    if (existsSync(join(stage, `r3-${when}`, "index.html"))) await shot(`r3-${when}`, `r3-${when}-${w}.png`, w, 900, {reduce: true, chart: true});
proc.kill(); server.close();
writeFileSync(join(shots, "requests.json"), JSON.stringify(log, null, 1) + "\n");
console.log(`renders in ${shots}; hosts reached: ${JSON.stringify([...new Set(Object.values(log).flatMap(l => l.reached))])}; refused: ${JSON.stringify([...new Set(Object.values(log).flatMap(l => l.refused))])}; errors: ${Object.values(log).flatMap(l => l.errors).length}`);
