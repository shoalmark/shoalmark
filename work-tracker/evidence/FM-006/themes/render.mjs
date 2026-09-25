// render.mjs OUT [SHOTS] — the renders of what build-mocks.py wrote to OUT: every theme's board, the answer dialog of the
// two that would ship, in both schemes, and the shoalmark theme's tracker view. The scheme is emulated through Chrome's
// DevTools protocol, never guessed from the machine's. CHROME names the browser; the default is macOS's Google Chrome.
// Node 22 or later.
import {spawn} from "node:child_process";
import {mkdirSync, mkdtempSync, writeFileSync} from "node:fs";
import {tmpdir} from "node:os";
import {join, resolve} from "node:path";

const out = resolve(process.argv[2] ?? "."), shots = resolve(process.argv[3] ?? join(out, "shots"));
const chrome = process.env.CHROME ?? "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome";
const port = 9400 + Math.floor(Math.random() * 500), sleep = ms => new Promise(r => setTimeout(r, ms));
const proc = spawn(chrome, ["--headless=new", "--disable-gpu", `--remote-debugging-port=${port}`,
  `--user-data-dir=${mkdtempSync(join(tmpdir(), "themes-"))}`, "about:blank"], {stdio: "ignore"});
for (let i = 0; i < 60; i++) { try { await fetch(`http://127.0.0.1:${port}/json/version`); break } catch { await sleep(250) } }

async function shot(url, file, scheme, w, h) {
  const t = await (await fetch(`http://127.0.0.1:${port}/json/new?about:blank`, {method: "PUT"})).json();
  const ws = new WebSocket(t.webSocketDebuggerUrl); await new Promise(r => ws.onopen = r);
  let id = 0; const pend = new Map();
  ws.onmessage = e => { const m = JSON.parse(e.data); if (pend.has(m.id)) { pend.get(m.id)(m.result); pend.delete(m.id) } };
  const call = (method, params = {}) => new Promise(r => { pend.set(++id, r); ws.send(JSON.stringify({id, method, params})) });
  await call("Emulation.setDeviceMetricsOverride", {width: w, height: h, deviceScaleFactor: 1, mobile: false});
  await call("Emulation.setEmulatedMedia", {features: [{name: "prefers-color-scheme", value: scheme}]});
  await call("Page.navigate", {url}); await sleep(1800);
  const s = await call("Page.captureScreenshot", {clip: {x: 0, y: 0, width: w, height: h, scale: 1}});
  writeFileSync(file, Buffer.from(s.data, "base64")); ws.close();
  await fetch(`http://127.0.0.1:${port}/json/close/${t.id}`).catch(() => {});
}

mkdirSync(shots, {recursive: true});
for (const theme of ["monochrome", "shoalmark", "catkin", "bagels", "seekarte"])
  for (const scheme of ["dark", "light"]) {
    await shot(`file://${out}/${theme}.html`, join(shots, `${theme}-${scheme}.png`), scheme, 1300, 1200);
    if (theme == "monochrome" || theme == "shoalmark")   // the two that would ship; build-mocks.py writes every dialog
      await shot(`file://${out}/${theme}-dialog.html`, join(shots, `${theme}-dialog-${scheme}.png`), scheme, 1300, 760);
  }
for (const scheme of ["dark", "light"])
  await shot(`file://${out}/shoalmark.html#=FM-002`, join(shots, `shoalmark-tracker-${scheme}.png`), scheme, 1300, 760);
proc.kill();
console.log(`renders in ${shots}`);
