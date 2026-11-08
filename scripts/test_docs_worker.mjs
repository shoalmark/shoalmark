// test_docs_worker.mjs [WORKER [CONFIG]]: .github/workflows/docs.worker.js's answers, with a stand-in for the asset layer, and
// .github/workflows/docs.wrangler.jsonc's run_worker_first. Node 18 or newer, nothing installed; docs.yml's build job runs it.
// Each check prints ok or FAIL with what it saw; the exit is 1 when one fails.
import { readFileSync } from "node:fs";
import { fileURLToPath } from "node:url";

const root = fileURLToPath(new URL("..", import.meta.url));
const workerPath = process.argv[2] || root + ".github/workflows/docs.worker.js";
const configPath = process.argv[3] || root + ".github/workflows/docs.wrangler.jsonc";
// a data: URL is read as a module whatever the file's name, and the Worker imports nothing
const worker = (await import("data:text/javascript;base64," + readFileSync(workerPath).toString("base64"))).default;

const VIDEO = "/blog/a-post/a-post.mp4", SIZE = 1000;
const bytes = Uint8Array.from({ length: SIZE }, (_, i) => (i * 7 + 3) % 256);
const FILES = {
  [VIDEO]: { body: bytes, type: "video/mp4", etag: '"v1"' },
  "/index.html": { body: "the start page", type: "text/html" },
  "/setup.html": { body: "setup", type: "text/html" },
  "/de/index.html": { body: "die Startseite", type: "text/html" },
  "/404.html": { body: "not found", type: "text/html" },
};

// The asset layer: each file at its own path, 404 for any other, 304 for a matching If-None-Match. One that honours Range
// answers bytes=a-b and bytes=a- with 206, as the live one might; the other answers every Range with the whole file.
function assets(honoursRange) {
  const asked = [];
  return {
    asked,
    async fetch(request) {
      const path = new URL(request.url).pathname, file = FILES[path];
      asked.push({ path, method: request.method, range: request.headers.get("Range") });
      if (!file) return new Response(null, { status: 404 });
      const body = typeof file.body === "string" ? new TextEncoder().encode(file.body) : file.body;
      const headers = { "Content-Type": file.type, "Content-Length": String(body.length), ...(file.etag ? { ETag: file.etag } : {}) };
      if (file.etag && request.headers.get("If-None-Match") === file.etag) return new Response(null, { status: 304, headers: { ETag: file.etag } });
      const m = honoursRange ? /^bytes=(\d+)-(\d*)$/.exec(request.headers.get("Range") || "") : null;
      if (m && +m[1] < body.length) {
        const a = +m[1], b = m[2] === "" ? body.length - 1 : Math.min(+m[2], body.length - 1);
        return new Response(request.method === "HEAD" ? null : body.slice(a, b + 1),
          { status: 206, headers: { ...headers, "Content-Range": `bytes ${a}-${b}/${body.length}`, "Content-Length": String(b - a + 1) } });
      }
      return new Response(request.method === "HEAD" ? null : body, { status: 200, headers });
    },
  };
}

async function ask(path, { method = "GET", headers = {}, honoursRange = false } = {}) {
  const env = { ASSETS: assets(honoursRange) };
  const r = await worker.fetch(new Request("https://shoalmark.tools" + path, { method, headers }), env);
  const body = new Uint8Array(await r.arrayBuffer());
  return { status: r.status, h: Object.fromEntries(r.headers), body, text: new TextDecoder().decode(body), asked: env.ASSETS.asked };
}

let failed = 0;
function check(name, ok, saw) {
  if (!ok) failed++;
  console.log(`${ok ? "ok  " : "FAIL"}  ${name}${ok ? "" : ` (saw ${JSON.stringify(saw)})`}`);
}
const same = (a, b) => a.length === b.length && a.every((x, i) => x === b[i]);
const kept = r => r.h["accept-ranges"] === "bytes" && r.h["content-type"] === "video/mp4" && r.h.etag === '"v1"';
const seen = r => ({ status: r.status, headers: r.h, length: r.body.length });

for (const honoursRange of [false, true]) {
  const how = honoursRange ? "with an asset layer that honours Range" : "with an asset layer that answers Range with the whole file";
  let r = await ask(VIDEO, { headers: { Range: "bytes=0-99" }, honoursRange });
  check(`${how}: bytes=0-99 gets 206 with the first 100 bytes, Content-Range bytes 0-99/1000 and Content-Length 100, and keeps Accept-Ranges, the type and the ETag`,
    r.status === 206 && same(r.body, bytes.slice(0, 100)) && r.h["content-range"] === "bytes 0-99/1000" && r.h["content-length"] === "100" && kept(r), seen(r));
  r = await ask(VIDEO, { headers: { Range: "bytes=990-2000" }, honoursRange });
  check(`${how}: bytes=990-2000 gets 206 with the last 10 bytes, its end cut at the file's`,
    r.status === 206 && same(r.body, bytes.slice(990)) && r.h["content-range"] === "bytes 990-999/1000" && r.h["content-length"] === "10" && kept(r), seen(r));
  r = await ask(VIDEO, { headers: { Range: "bytes=100-" }, honoursRange });
  check(`${how}: the open-ended bytes=100- gets 206 to the end`,
    r.status === 206 && same(r.body, bytes.slice(100)) && r.h["content-range"] === "bytes 100-999/1000" && r.h["content-length"] === "900" && kept(r), seen(r));
  r = await ask(VIDEO, { headers: { Range: "bytes=-100" }, honoursRange });
  check(`${how}: the suffix bytes=-100 gets 206 with the last 100 bytes`,
    r.status === 206 && same(r.body, bytes.slice(900)) && r.h["content-range"] === "bytes 900-999/1000" && kept(r), seen(r));
  for (const range of ["bytes=1000-", "bytes=2000-2100", "bytes=-0"]) {
    r = await ask(VIDEO, { headers: { Range: range }, honoursRange });
    check(`${how}: ${range}, past the end, gets 416 with Content-Range bytes */1000, no body and no Content-Length of the file's`,
      r.status === 416 && r.h["content-range"] === "bytes */1000" && r.body.length === 0 && (r.h["content-length"] || "0") === "0" && r.h["accept-ranges"] === "bytes", seen(r));
  }
  r = await ask(VIDEO, { honoursRange });
  check(`${how}: no Range gets 200 with the whole file, its Content-Length, Accept-Ranges, the type and the ETag`,
    r.status === 200 && same(r.body, bytes) && r.h["content-length"] === "1000" && kept(r) && !("content-range" in r.h), seen(r));
  for (const range of ["bytes=5-2", "bytes=0-1,4-5", "items=0-1", "bytes=-"]) {
    r = await ask(VIDEO, { headers: { Range: range }, honoursRange });
    check(`${how}: a Range of another form, ${range}, gets 200 with the whole file`, r.status === 200 && same(r.body, bytes) && kept(r), seen(r));
  }
  r = await ask(VIDEO, { headers: { Range: "bytes=0-99", "If-Range": '"v1"' }, honoursRange });
  check(`${how}: an If-Range that is the file's ETag keeps the range: 206`, r.status === 206 && same(r.body, bytes.slice(0, 100)), seen(r));
  r = await ask(VIDEO, { headers: { Range: "bytes=0-99", "If-Range": '"v0"' }, honoursRange });
  check(`${how}: an If-Range that is not the file's ETag gets 200 with the whole file`, r.status === 200 && same(r.body, bytes) && kept(r), seen(r));
  r = await ask(VIDEO, { method: "HEAD", headers: { Range: "bytes=0-99" }, honoursRange });
  check(`${how}: HEAD with bytes=0-99 answers as GET would, 206 with its Content-Range and Content-Length, without a body`,
    r.status === 206 && r.h["content-range"] === "bytes 0-99/1000" && r.h["content-length"] === "100" && kept(r) && r.body.length === 0, seen(r));
  r = await ask(VIDEO, { method: "HEAD", honoursRange });
  check(`${how}: HEAD without Range answers as GET would, 200 with Content-Length 1000, without a body`,
    r.status === 200 && r.h["content-length"] === "1000" && kept(r) && r.body.length === 0, seen(r));
  r = await ask(VIDEO, { headers: { Range: "bytes=0-99" }, honoursRange });
  check(`${how}: the asset layer is asked for the MP4 without Range, so the answer is cut by the Worker either way`,
    r.asked.length === 1 && r.asked[0].range === null && r.asked[0].method === "GET", r.asked);
}
let r = await ask(VIDEO, { headers: { "If-None-Match": '"v1"' } });
check("the asset layer's 304 for a matching If-None-Match is returned as it came", r.status === 304 && r.body.length === 0 && r.h.etag === '"v1"', seen(r));

// every other path, and the MP4's own path when it is no file, as the Worker answered them before
r = await ask("/");
check("/ gets the start page's index.html", r.status === 200 && r.text === "the start page", seen(r));
r = await ask("/setup");
check("/setup gets setup.html", r.status === 200 && r.text === "setup", seen(r));
r = await ask("/de");
check("/de gets a 301 to /de/", r.status === 301 && r.h.location === "https://shoalmark.tools/de/", seen(r));
r = await ask("/nowhere");
check("a missing path gets 404.html with status 404", r.status === 404 && r.text === "not found", seen(r));
r = await ask("/blog/a-post/gone.mp4", { headers: { Range: "bytes=0-99" } });
check("a missing MP4 gets 404.html with status 404, as any missing path", r.status === 404 && r.text === "not found", seen(r));

// the config: the MP4 alone runs the Worker first, every other file is the asset layer's
const config = JSON.parse(readFileSync(configPath, "utf8").split("\n").filter(l => !/^\s*\/\//.test(l)).join("\n"));
const first = config.assets && config.assets.run_worker_first;
const glob = (pattern, star) => new RegExp("^" + pattern.split("*").map(s => s.replace(/[.+?^${}()|[\]\\]/g, "\\$&")).join(star) + "$");
const hits = path => Array.isArray(first) && first.some(p => typeof p === "string" && [glob(p, "[^/]*"), glob(p, ".*")].every(rx => rx.test(path)));
const others = ["/index.html", "/de/index.html", "/setup.html", "/blog/index.html", "/blog/a-post.html", "/blog/a-post/card.png", "/blog/a-post/still.gif", "/a.mp4"];
check("docs.wrangler.jsonc's run_worker_first names the blog's MP4 path alone, /blog/*/*.mp4: the MP4 runs the Worker first, and no other file does",
  JSON.stringify(first) === '["/blog/*/*.mp4"]' && hits(VIDEO) && !others.some(hits), { run_worker_first: first, others: others.filter(hits) });

console.log(failed ? `${failed} check(s) failed` : "every check passed");
process.exit(failed ? 1 : 0);
