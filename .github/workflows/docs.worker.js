// Runs only for a path that is no file of the site; the asset layer has already served every file at its own path.
// It answers those paths as GitHub Pages answers them: a folder by its index.html (/ and /de/), a page without its
// .html (/setup), a folder without its slash by a 301 to it (/de), and anything else with 404.html and status 404.
export default {
  async fetch(request, env) {
    const url = new URL(request.url);
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
