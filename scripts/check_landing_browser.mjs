// check_landing_browser.mjs SITE STATE OUT.json [PAGES [SIZES]] — the built landings, English and German, in a real headless Chrome (Node 22 or newer, Chrome in $CHROME).
// SITE is a built site, STATE is `interim` or `probe` (the launch state it was built in). The site is served from 127.0.0.1 and every other host is
// unresolvable, so a page that asks for the outside fails and is logged. For each landing and How it works page at 360, 375 and 390 px (and 1440):
//   no sideways scroll, no script error, no failed request, no request to any other host.
// On each landing the top bar's five anchors stand in one row, clear of the language switch, at the width where they first show, with the widest hi-score
// the bar can print (888/888) set in it.
// In the probe state, for each landing at those widths: the primary button opens the dialog by keyboard; the dialog is a modal that the accessibility tree
// names; focus is inside it; Tab and Shift+Tab never reach the page behind; its folds open and close by keyboard; Escape closes it and focus is back on the
// button; it fits the window and the page does not scroll sideways under it; and, with the folds closed, nothing inside it scrolls at 360×780, 375×667 and
// 390×844. Writes OUT.json (every check of every visit, with its verdict) and exits 1 where any check failed.
// PAGES (a comma-separated list) and SIZES (360x780,… and `bar` for the top bar's anchors) narrow the run to what is named; the whole run is every page at
// 360×780, 375×667, 390×844 and 1440×900, and the bar.
import {spawn} from "node:child_process";
import {createServer} from "node:http";
import {existsSync, mkdtempSync, readFileSync, statSync, writeFileSync} from "node:fs";
import {tmpdir} from "node:os";
import {join, resolve} from "node:path";

const [dir, state, out, only, sizes] = process.argv.slice(2);
if (!dir || !["interim", "probe"].includes(state) || !out) { console.error("usage: check_landing_browser.mjs SITE interim|probe OUT.json [PAGES [SIZES]]"); process.exit(2) }
const CHROME = process.env.CHROME ?? "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome";
const sleep = ms => new Promise(r => setTimeout(r, ms));
const TYPES = {html: "text/html; charset=utf-8", css: "text/css", js: "text/javascript", json: "application/json", svg: "image/svg+xml", png: "image/png",
  woff2: "font/woff2", xml: "application/xml", txt: "text/plain; charset=utf-8", md: "text/markdown; charset=utf-8"};

// the built site as a host serves it: use_directory_urls is off, the files are as they are, and the project site lives under /shoalmark/ on GitHub Pages
const root = resolve(dir);
const server = createServer((q, s) => {
  let path = decodeURIComponent(new URL(q.url, "http://x").pathname);
  if (path.startsWith("/shoalmark/")) path = path.slice(10);
  const f = join(root, path);
  if (!f.startsWith(root) || !existsSync(f) || statSync(f).isDirectory()) { s.writeHead(404); return s.end() }
  s.writeHead(200, {"content-type": TYPES[f.split(".").pop()] ?? "application/octet-stream"}); s.end(readFileSync(f));
});
await new Promise(r => server.listen(0, "127.0.0.1", r));
const origin = `http://127.0.0.1:${server.address().port}/`;

const port = 9400 + Math.floor(Math.random() * 500);
const chrome = spawn(CHROME, ["--headless=new", "--disable-gpu", "--hide-scrollbars", `--remote-debugging-port=${port}`, "--host-resolver-rules=MAP * ~NOTFOUND, EXCLUDE 127.0.0.1",
  ...(process.env.CHROME_FLAGS ? process.env.CHROME_FLAGS.split(" ") : []), `--user-data-dir=${mkdtempSync(join(tmpdir(), "shoalmark-landing-"))}`, "about:blank"], {stdio: "ignore"});
let version = null;
for (let i = 0; i < 80 && !version; i++) { try { version = (await (await fetch(`http://127.0.0.1:${port}/json/version`)).json()).Browser } catch { await sleep(250) } }
if (!version) { console.error("check_landing_browser: Chrome did not start"); chrome.kill(); server.close(); process.exit(2) }

// a tab: js(expr), call(method, params), press(key, modifiers), close(); log holds what the page did
async function open(url, {w, h, clipboard = "ok"}) {
  const t = await (await fetch(`http://127.0.0.1:${port}/json/new?about:blank`, {method: "PUT"})).json();
  const ws = new WebSocket(t.webSocketDebuggerUrl); await new Promise(r => ws.onopen = r);
  let id = 0; const pending = new Map(), asked = new Map();
  const log = {errors: [], failed: [], hosts: new Set()};
  ws.onmessage = e => { const m = JSON.parse(e.data), p = m.params;
    if (m.method == "Runtime.exceptionThrown") log.errors.push(p.exceptionDetails.exception?.description ?? p.exceptionDetails.text);
    if (m.method == "Runtime.consoleAPICalled" && p.type == "error") log.errors.push("console: " + p.args.map(a => a.value ?? a.description).join(" "));
    if (m.method == "Network.requestWillBeSent") { asked.set(p.requestId, p.request.url); if (!/^(data|about|blob):/.test(p.request.url)) log.hosts.add(new URL(p.request.url).host) }
    if (m.method == "Network.loadingFailed" && !p.canceled) log.failed.push(`${asked.get(p.requestId)} ${p.errorText}`);
    if (m.method == "Network.responseReceived" && p.response.status >= 400) log.failed.push(`${p.response.url} HTTP ${p.response.status}`);
    if (pending.has(m.id)) { pending.get(m.id)(m.result ?? {error: m.error}); pending.delete(m.id) } };
  const call = (method, params = {}) => new Promise(r => { pending.set(++id, r); ws.send(JSON.stringify({id, method, params})) });
  const js = async expr => { const r = await call("Runtime.evaluate", {expression: expr, returnByValue: true, awaitPromise: true});
    if (r.exceptionDetails) throw Error(JSON.stringify(r.exceptionDetails).slice(0, 400)); return r.result.value };
  await call("Runtime.enable"); await call("Network.enable"); await call("Page.enable");
  await call("Emulation.setDeviceMetricsOverride", {width: w, height: h, deviceScaleFactor: 1, mobile: false});
  await call("Emulation.setEmulatedMedia", {features: [{name: "prefers-reduced-motion", value: "reduce"}]});
  // the clipboard is stubbed, so that the two states of the dialog happen on demand; the page's own code runs unchanged
  await call("Page.addScriptToEvaluateOnNewDocument", {source: clipboard == "ok"
    ? `Object.defineProperty(navigator, "clipboard", {configurable: true, value: {writeText: () => Promise.resolve()}})`
    : `Object.defineProperty(navigator, "clipboard", {configurable: true, value: {writeText: () => Promise.reject(new Error("refused"))}}); document.execCommand = () => false`});
  await call("Page.navigate", {url: origin + url}); await sleep(1500);
  await js("document.fonts.ready.then(() => 1)");
  const key = async (k, mods = 0) => { for (const type of [k.text ? "keyDown" : "rawKeyDown", "keyUp"]) await call("Input.dispatchKeyEvent", {type, key: k.key, code: k.code, windowsVirtualKeyCode: k.vk, modifiers: mods, ...(type == "keyDown" ? {text: k.text} : {})}) };   // Enter carries its character, as a keyboard sends it: a summary and a link act on it
  const KEYS = {Tab: {key: "Tab", code: "Tab", vk: 9}, Escape: {key: "Escape", code: "Escape", vk: 27}, Enter: {key: "Enter", code: "Enter", vk: 13, text: "\r"}, Space: {key: " ", code: "Space", vk: 32}};
  const press = async (name, mods = 0) => { await key(KEYS[name], mods); await sleep(150) };
  const close = async () => { ws.close(); await fetch(`http://127.0.0.1:${port}/json/close/${t.id}`).catch(() => {}) };
  return {js, call, press, close, log};
}

const rows = [], info = [];
const verdict = (page, w, h, name, ok, detail = "") => rows.push({page, w, h, check: name, ok: !!ok, ...(ok ? {} : {detail})});
const PAGES = only ? only.split(",") : ["index.html", "de/index.html", "how-it-works.html", "de/how-it-works.html"];
const SIZES = sizes ? sizes.split(",").filter(s => s.includes("x")).map(s => s.split("x").map(Number)) : [[360, 780], [375, 667], [390, 844], [1440, 900]];
const BAR = !sizes || sizes.split(",").includes("bar");   // the top bar's anchors, a run of their own
const ACTIVE = `(() => { const e = document.activeElement; return e ? (e.id || e.className || e.tagName) : "none" })()`;
const OUTSIDE = `(() => { const d = document.getElementById("probe"), e = document.activeElement; return !!e && e !== document.body && e !== document.documentElement && !d.contains(e) })()`;
// an element inside the dialog that scrolls inside itself (the prompt's own box excepted)
const SCROLLS = `(() => [...document.querySelectorAll("#probe *")].filter(e => e.tagName != "TEXTAREA" && e.tagName != "PRE" && ["auto", "scroll"].includes(getComputedStyle(e).overflowY) && e.scrollHeight > e.clientHeight + 1).map(e => (e.id || e.className || e.tagName) + " " + e.scrollHeight + ">" + e.clientHeight))()`;

for (const page of PAGES) for (const [w, h] of SIZES) {
  const t = await open(page, {w, h});
  const m = await t.js(`({sw: document.documentElement.scrollWidth, iw: innerWidth})`);
  verdict(page, w, h, "no sideways scroll", m.sw <= m.iw, `${m.sw} > ${m.iw}`);
  if (state == "probe" && page.endsWith("index.html") && !page.startsWith("how")) {
    await t.js(`document.getElementById("probe-open").focus()`);
    await t.press("Enter"); await sleep(400);
    const dlg = await t.js(`(() => { const d = document.getElementById("probe"); return {open: d.open, modal: d.matches(":modal"), label: (document.getElementById(d.getAttribute("aria-labelledby")) || {}).textContent, inside: d.contains(document.activeElement)} })()`);
    verdict(page, w, h, "the dialog opens by keyboard, as a modal", dlg.open && dlg.modal, JSON.stringify(dlg));
    verdict(page, w, h, "the dialog is labelled", !!(dlg.label || "").trim(), JSON.stringify(dlg));
    await t.call("Accessibility.enable");
    const ax = (await t.call("Accessibility.getFullAXTree")).nodes.filter(n => !n.ignored && n.role?.value == "dialog");
    verdict(page, w, h, "the accessibility tree names the dialog and says it is modal", ax.length == 1 && !!ax[0].name?.value?.trim() && ax[0].properties?.find(p => p.name == "modal")?.value?.value === true, JSON.stringify(ax.map(n => [n.name?.value, n.properties])).slice(0, 300));
    verdict(page, w, h, "focus moves into the dialog", dlg.inside, await t.js(ACTIVE));
    const focusable = await t.js(`document.querySelectorAll('#probe a[href], #probe button, #probe textarea, #probe summary, #probe input, #probe [tabindex]:not([tabindex="-1"])').length`);
    let leaked = null;
    for (let i = 0; i < focusable + 3 && !leaked; i++) { await t.press("Tab"); if (await t.js(OUTSIDE)) leaked = "Tab " + (i + 1) + ": " + await t.js(ACTIVE) }
    for (let i = 0; i < focusable + 3 && !leaked; i++) { await t.press("Tab", 8); if (await t.js(OUTSIDE)) leaked = "Shift+Tab " + (i + 1) + ": " + await t.js(ACTIVE) }
    verdict(page, w, h, "Tab and Shift+Tab stay inside the dialog", !leaked && focusable > 0, leaked ?? "nothing to focus in the dialog");
    // each fold (a <details>) opens and closes by keyboard
    const folds = await t.js(`document.querySelectorAll("#probe details").length`);
    for (let i = 0; i < folds; i++) {
      const before = await t.js(`(() => { const s = document.querySelectorAll("#probe details > summary")[${i}]; s.focus(); return document.querySelectorAll("#probe details")[${i}].open })()`);
      await t.press("Enter"); const after = await t.js(`document.querySelectorAll("#probe details")[${i}].open`);
      await t.press("Space"); const again = await t.js(`document.querySelectorAll("#probe details")[${i}].open`);
      verdict(page, w, h, `fold ${i + 1} opens and closes by keyboard`, before !== after && again === before, `${before} ${after} ${again}`);
    }
    const box = await t.js(`(() => { const b = document.querySelector("#probe").getBoundingClientRect(); return {l: Math.round(b.left), r: Math.round(b.right), sw: document.documentElement.scrollWidth, iw: innerWidth} })()`);
    verdict(page, w, h, "the dialog fits the window, and the page does not scroll sideways under it", box.l >= 0 && box.r <= box.iw && box.sw <= box.iw, JSON.stringify(box));
    if (w < 500) {
      const scrolling = await t.js(SCROLLS);
      verdict(page, w, h, "with its folds closed, nothing in the dialog scrolls inside itself", scrolling.length == 0, scrolling.join("; "));
    }
    await t.js(`document.querySelectorAll("#probe details[open]").forEach(d => d.open = false)`);
    await t.press("Escape"); await sleep(300);
    const gone = await t.js(`({open: document.getElementById("probe").open, focus: document.activeElement.id})`);
    verdict(page, w, h, "Escape closes the dialog and focus is back on the button", !gone.open && gone.focus == "probe-open", JSON.stringify(gone));
  }
  verdict(page, w, h, "no script error", t.log.errors.length == 0, t.log.errors.join(" | ").slice(0, 400));
  verdict(page, w, h, "no failed request", t.log.failed.length == 0, t.log.failed.join(" | ").slice(0, 400));
  verdict(page, w, h, "no request to any other host", [...t.log.hosts].every(x => x.startsWith("127.0.0.1")), [...t.log.hosts].filter(x => !x.startsWith("127.0.0.1")).join(" "));
  await t.close();
}
// the top bar's five anchors, wherever the page first shows them (stepping the window up from 1000 px): one row each, and clear of the language switch
if (BAR) for (const page of PAGES.filter(p => p.endsWith("index.html") && !p.startsWith("how"))) {
  const t = await open(page, {w: 1000, h: 900});
  await t.js(`document.querySelector(".score .opt b").textContent = "888/888"`);   // the widest hi-score the bar can print: the breakpoint must leave room for it
  const shows = () => t.js(`getComputedStyle(document.querySelector(".hud nav a:not(.docs)")).display != "none"`);
  let first = null;
  for (let w = 1000; w <= 1400 && first === null; w++) { await t.call("Emulation.setDeviceMetricsOverride", {width: w, height: 900, deviceScaleFactor: 1, mobile: false}); if (await shows()) first = w }
  const bar = first === null ? null : await t.js(`(() => ({rows: [...document.querySelectorAll(".hud nav a")].filter(a => getComputedStyle(a).display != "none").map(a => Math.round(a.getBoundingClientRect().height)), gap: Math.round((document.querySelector(".hud nav").getBoundingClientRect().left - document.querySelector(".hud .langsw").getBoundingClientRect().right) * 10) / 10}))()`);
  verdict(page, first ?? 0, 900, "the top bar's anchors stand in one row, clear of the switch, where they first show", bar !== null && Math.max(...bar.rows) < 36 && bar.gap >= 0, `first shown at ${first} px: ${JSON.stringify(bar)}`);
  info.push({page, w: first, state: "the width where the top bar's anchors first show", scrollsInside: []});
  await t.close();
}
// a refused copy: the dialog says so and selects the prompt, so that Ctrl+C copies it. The prompt stands open there by design, so how far the dialog then
// scrolls inside itself is measured and printed, not judged.
if (state == "probe") for (const page of PAGES.filter(p => p.endsWith("index.html"))) for (const [w, h] of [[360, 780], [375, 667], [390, 844]]) {
  const t = await open(page, {w, h, clipboard: "refused"});
  await t.js(`document.getElementById("probe-open").click()`); await sleep(500);
  const s = await t.js(`(() => { const a = document.getElementById("probe-text"), st = document.getElementById("probe-status"); return {state: st.dataset.state, text: st.textContent.trim(), selected: a.selectionStart == 0 && a.selectionEnd == a.value.length && a.value.length > 0} })()`);
  verdict(page, w, h, "where the copy is refused, the dialog says so and selects the prompt", s.state == "fail" && s.text.length > 0 && s.selected, JSON.stringify(s));
  info.push({page, w, h, state: "copy refused, the prompt open", scrollsInside: await t.js(SCROLLS)});
  await t.close();
}

writeFileSync(out, JSON.stringify({chrome: version, state, rows, info}, null, 1));
const bad = rows.filter(r => !r.ok);
console.log(JSON.stringify({chrome: version, state, checks: rows.length, failing: bad.length, first: bad.slice(0, 6)}));
for (const i of info) console.log("info (not judged): " + JSON.stringify(i));
chrome.kill(); server.close();
process.exit(bad.length ? 1 : 0);
