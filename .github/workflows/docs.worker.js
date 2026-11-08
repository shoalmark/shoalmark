// Runs first for the blog's MP4 (run_worker_first in docs.wrangler.jsonc), and otherwise only for a path that is no file of
// the site; the asset layer has already served every other file at its own path. It answers those paths as GitHub Pages
// answers them: a folder by its index.html (/ and /de/), a page without its .html (/setup), a folder without its slash by a
// 301 to it (/de), and anything else with 404.html and status 404.
const VIDEO = /^\/blog\/.+\.mp4$/;

// The MP4, for GET and HEAD. The asset layer is asked for the whole file without Range, so the answer does not depend on
// whether it honours Range, and the asked bytes are cut from it here: for GET, one range (bytes=a-b, bytes=a- or bytes=-n)
// gets 206 with Content-Range, a range that starts past the end gets 416, and no Range, a Range of another form, or an
// If-Range that is not the file's strong ETag gets 200 and the whole file. HEAD answers as GET without Range would, 200 with
// the whole file's headers and no body, as a server reads Range for GET alone. Each says Accept-Ranges and keeps the asset's
// headers.
// A missing file returns null, to be answered as any missing path; any other answer of the asset layer is returned as it came.
async function video(request, env, url) {
  const ask = new Headers(request.headers);
  ask.delete("Range");
  ask.delete("If-Range");
  const file = await env.ASSETS.fetch(new Request(url, { method: "GET", headers: ask }));
  if (file.status === 404) return null;
  if (file.status !== 200) return file;
  const headers = new Headers(file.headers), head = request.method === "HEAD";
  headers.set("Accept-Ranges", "bytes");
  const range = /^bytes=(\d*)-(\d*)$/.exec(request.headers.get("Range") || "");
  const etag = file.headers.get("ETag"), ifRange = request.headers.get("If-Range");
  const stale = ifRange !== null && (ifRange !== etag || ifRange.startsWith("W/"));
  const other = !range || range[1] + range[2] === "" || (range[1] !== "" && range[2] !== "" && Number(range[2]) < Number(range[1]));
  if (stale || other || head) return new Response(head ? null : file.body, { status: 200, headers });
  const whole = await file.arrayBuffer(), size = whole.byteLength;
  const first = range[1] === "" ? Math.max(size - Number(range[2]), 0) : Number(range[1]);
  const last = range[1] === "" || range[2] === "" ? size - 1 : Math.min(Number(range[2]), size - 1);
  if (first >= size) {
    headers.set("Content-Range", `bytes */${size}`);
    headers.delete("Content-Length");
    return new Response(null, { status: 416, headers });
  }
  headers.set("Content-Range", `bytes ${first}-${last}/${size}`);
  headers.set("Content-Length", String(last - first + 1));
  return new Response(whole.slice(first, last + 1), { status: 206, headers });
}

export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    if (VIDEO.test(url.pathname) && (request.method === "GET" || request.method === "HEAD")) {
      const answer = await video(request, env, url);
      if (answer) return answer;
    }
    const asset = (path, from = request) => env.ASSETS.fetch(new Request(new URL(path, url), from));
    if (url.pathname.endsWith("/")) {
      const index = await asset(url.pathname + "index.html");
      if (index.status !== 404) return index;
    } else {
      const page = await asset(url.pathname + ".html");
      if (page.status !== 404) return page;
      const folder = await asset(url.pathname + "/index.html", { method: "HEAD" });
      if (folder.status !== 404) return Response.redirect(new URL(url.pathname + "/" + url.search, url), 301);
    }
    const missing = await asset("/404.html", { method: request.method === "HEAD" ? "HEAD" : "GET" });
    return new Response(missing.body, { status: 404, headers: missing.headers });
  },
};
