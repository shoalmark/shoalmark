// render.mjs STAGE [SHOTS] — FM-002 slice A's renders: the board and the site's start page, before and after, dark and
// light, at 1440 and 390 px. Its method is FM-006's render.mjs (evidence/FM-006/themes/render.mjs), shot() unchanged but
// for the widths, a wait for the page's fonts and a log of every request that leaves the machine: Chrome's DevTools
// protocol, the scheme emulated, never guessed from the machine's; a site page also told by its toggle's attribute,
// since Zensical remembers the last scheme; the site served from 127.0.0.1, the board opened as a file. Offline: every host is unresolvable but the two Google Fonts hosts the site's
// own pages load (FM-006's open self-hosting item) — the board loads nothing from any host; requests.json lists, per
// render, the hosts a page reached and the hosts it asked for and was refused.
//
// STAGE holds before/ and after/, each as a commit builds them (README.md, "Rebuild"): board.html beside brand/ and
// view/ (python3 shoalmark.py --html-only), and site/ (zensical build); and, optionally, mock/: FM-006's build-mocks.py
// output, whose shoalmark.html and site-shoalmark/ are rendered beside the after pages for the comparison. CHROME names the browser; the
// default is macOS's Google Chrome. Node 22 or later.
// `render.mjs STAGE SHOTS foot` renders only the after site's foot — the page's last 240 px at 1440, both schemes, FM-006's
// foot shot (the record's R2: the site's one rule not the mock's, the foot's link, lies below every viewport render) — and
// adds its two lines to requests.json.
import {spawn} from "node:child_process";
import {createServer} from "node:http";
import {existsSync, mkdirSync, mkdtempSync, readFileSync, statSync, writeFileSync} from "node:fs";
import {tmpdir} from "node:os";
import {join, resolve} from "node:path";

const stage = resolve(process.argv[2] ?? "."), shots = resolve(process.argv[3] ?? join(stage, "shots"));
const chrome = process.env.CHROME ?? "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome";
const port = 9400 + Math.floor(Math.random() * 500), sleep = ms => new Promise(r => setTimeout(r, ms));
const offline = "MAP * ~NOTFOUND, EXCLUDE fonts.googleapis.com, EXCLUDE fonts.gstatic.com, EXCLUDE 127.0.0.1";
const proc = spawn(chrome, ["--headless=new", "--disable-gpu", `--remote-debugging-port=${port}`, `--host-resolver-rules=${offline}`,
  `--user-data-dir=${mkdtempSync(join(tmpdir(), "slice-a-"))}`, "about:blank"], {stdio: "ignore"});
for (let i = 0; i < 60; i++) { try { await fetch(`http://127.0.0.1:${port}/json/version`); break } catch { await sleep(250) } }
// the site is served from 127.0.0.1, as a host serves it: from file:// Zensical hides its search, so a page opened as a
// file is not the page a reader sees. The board is opened as a file, as its reader opens it.
const TYPES = {html: "text/html", css: "text/css", js: "text/javascript", json: "application/json", svg: "image/svg+xml",
  png: "image/png", woff2: "font/woff2", xml: "application/xml", txt: "text/plain"};
const server = createServer((q, s) => { const f = join(stage, decodeURIComponent(new URL(q.url, "http://x").pathname));
  if (!f.startsWith(stage) || !existsSync(f) || statSync(f).isDirectory()) { s.writeHead(404); return s.end() }
  s.writeHead(200, {"content-type": TYPES[f.split(".").pop()] ?? "application/octet-stream"}); s.end(readFileSync(f)) });
await new Promise(r => server.listen(0, "127.0.0.1", r));
const served = rel => `http://127.0.0.1:${server.address().port}/${rel}`;

const log = {};
async function shot(url, file, scheme, w, h, site, foot = 0) {   // foot: capture the page's last `foot` pixels
  const t = await (await fetch(`http://127.0.0.1:${port}/json/new?about:blank`, {method: "PUT"})).json();
  const ws = new WebSocket(t.webSocketDebuggerUrl); await new Promise(r => ws.onopen = r);
  let id = 0; const pend = new Map(), asked = new Map(), reached = [], refused = [];
  ws.onmessage = e => { const m = JSON.parse(e.data), p = m.params;
    if (m.method == "Network.requestWillBeSent" && !/^(file|data|about|blob):/.test(p.request.url) && !p.request.url.startsWith(served(""))) asked.set(p.requestId, new URL(p.request.url).host);
    if (m.method == "Network.responseReceived" && asked.has(p.requestId)) reached.push(asked.get(p.requestId));
    if (m.method == "Network.loadingFailed" && asked.has(p.requestId)) refused.push(asked.get(p.requestId));
    if (pend.has(m.id)) { pend.get(m.id)(m.result); pend.delete(m.id) } };
  const call = (method, params = {}) => new Promise(r => { pend.set(++id, r); ws.send(JSON.stringify({id, method, params})) });
  await call("Network.enable");
  await call("Emulation.setDeviceMetricsOverride", {width: w, height: h, deviceScaleFactor: 1, mobile: false});
  await call("Emulation.setEmulatedMedia", {features: [{name: "prefers-color-scheme", value: scheme}]});
  await call("Page.navigate", {url}); await sleep(1800);
  if (site)
    await call("Runtime.evaluate", {expression: `document.body.setAttribute("data-md-color-scheme", "${scheme == "dark" ? "slate" : "default"}")`}), await sleep(400);
  await call("Runtime.evaluate", {expression: "document.fonts.ready.then(() => 1)", awaitPromise: true});
  const y = foot ? (await call("Runtime.evaluate", {expression: "document.documentElement.scrollHeight", returnByValue: true})).result.value - foot : 0;
  const s = await call("Page.captureScreenshot", {captureBeyondViewport: !!foot, clip: {x: 0, y, width: w, height: foot || h, scale: 1}});
  writeFileSync(file, Buffer.from(s.data, "base64")); ws.close();
  await fetch(`http://127.0.0.1:${port}/json/close/${t.id}`).catch(() => {});
  log[file.split("/").pop()] = {reached: [...new Set(reached)].sort(), refused: [...new Set(refused)].sort()};
}

mkdirSync(shots, {recursive: true});
const sizes = [[1440, 1000], [390, 844]], footOnly = process.argv[4] == "foot";
if (footOnly)
  for (const scheme of ["dark", "light"])
    await shot(served("after/site/index.html"), join(shots, `site-after-foot-1440-${scheme}.png`), scheme, 1440, 1000, true, 240);
else for (const when of ["before", "after", "mock"])
  for (const [w, h] of sizes)
    for (const scheme of ["dark", "light"]) {
      const board = when == "mock" ? join(stage, "mock", "shoalmark.html") : join(stage, when, "board.html");
      if (existsSync(board)) await shot(`file://${board}`, join(shots, `board-${when}-${w}-${scheme}.png`), scheme, w, h, false);
      const site = when == "mock" ? "mock/site-shoalmark/index.html" : `${when}/site/index.html`;
      if (existsSync(join(stage, site))) await shot(served(site), join(shots, `site-${when}-${w}-${scheme}.png`), scheme, w, h, true);
    }
proc.kill(); server.close();
const prior = footOnly && existsSync(join(shots, "requests.json")) ? JSON.parse(readFileSync(join(shots, "requests.json"), "utf-8")) : {};
writeFileSync(join(shots, "requests.json"), JSON.stringify({...prior, ...log}, null, 1) + "\n");
console.log(`renders in ${shots}; hosts reached: ${JSON.stringify([...new Set(Object.values(log).flatMap(l => l.reached))])}`);
