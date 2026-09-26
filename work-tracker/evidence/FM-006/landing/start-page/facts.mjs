// facts.mjs SHA [MOCK] — FM-006 slice L: the landing page's facts, read from one commit of main (git only, no checkout).
// Run from the repository's root; Node 22 or later. Prints one JSON object: the commit and the time it was read
// (Europe/Berlin); the release — VERSION, its tag's commit and time, the CHANGELOG section's bold headline; and the wrecks —
// every tracker at SHA tagged `bug` or `security`, with its status and `# ` title, its incident ID and filing day (the
// commit that added the file: `git log --diff-filter=A`, the earliest, its day in Europe/Berlin), and its report: the
// tracker's `hook:`, cut to its first sentence or two, verbatim, code spans kept. How many sentences: as many as the mock's
// report carried (MOCK, the evidence page, by the same split); one for a wreck the mock did not draw. A sentence ends at
// `.`, `?` or `!` followed by a space and a capital, a backtick, an asterisk, a quote or a digit; a hook with no such end is
// one sentence.
import {execFileSync} from "node:child_process";
import {readFileSync} from "node:fs";

const [sha, mock] = process.argv.slice(2);
const git = (...a) => execFileSync("git", a, {encoding: "utf8", env: {...process.env, TZ: "Europe/Berlin"}, maxBuffer: 1 << 26});
const full = git("rev-parse", sha).trim();
const END = /(?<=[.?!]) (?=[A-Z`*"'0-9])/;
const sentences = s => s.trim().split(END);

function front(text) {
  const m = text.match(/^---\n([\s\S]*?)\n---\n/), out = {};
  for (const line of m[1].split("\n")) {
    const i = line.indexOf(":"); if (i < 0) continue;
    let v = line.slice(i + 1).trim();
    if (v.startsWith('"') && v.endsWith('"')) v = v.slice(1, -1).replace(/\\(["\\])/g, "$1");
    out[line.slice(0, i).trim()] = v;
  }
  return out;
}

const counts = {};
if (mock) for (const w of JSON.parse(readFileSync(mock, "utf8").match(/^const WRECKS = (\[.*\]);$/m)[1])) counts[w.id] = sentences(w.report).length;

const wrecks = [];
for (const path of git("ls-tree", "--name-only", full, "work-tracker/").split("\n")) {
  const m = path.match(/^work-tracker\/(FM-(\d+))-.*\.md$/); if (!m) continue;
  const text = git("show", `${full}:${path}`), fm = front(text);
  const tags = new Set((fm.tags ?? "").split(",").map(t => t.trim()));
  if (!tags.has("bug") && !tags.has("security")) continue;
  const id = m[1], title = text.match(/^# (.+)$/m)[1];
  if (!title.startsWith(`${id} — `)) throw Error(title);
  const added = git("log", full, "--diff-filter=A", "--format=%h %ad", "--date=format-local:%Y-%m-%d", "--", path).trim().split("\n").at(-1).split(" ");
  const n = counts[id] ?? 1, report = sentences(fm.hook).slice(0, n).join(" ");
  if (!fm.hook.startsWith(report)) throw Error(id);
  wrecks.push({id, inc: added[0], filed: added[1], status: fm.status, title: title.slice(id.length + 3), sentences: n, report, hook: fm.hook,
    url: `https://github.com/holgo99/shoalmark/blob/main/${path}`});
}
wrecks.sort((a, b) => +a.id.split("-")[1] - +b.id.split("-")[1]);

const version = git("show", `${full}:VERSION`).trim();
const tag = git("log", "-1", "--format=%h %ad", "--date=format-local:%Y-%m-%d %H:%M:%S", `v${version}`).trim().split(" ");
const section = git("show", `${full}:CHANGELOG.md`).match(new RegExp(`^## ${version.replace(/\./g, "\\.")} — (\\S+)\\n\\n\\*\\*([\\s\\S]+?)\\*\\*`, "m"));
const now = new Date(), berlin = new Intl.DateTimeFormat("sv-SE", {timeZone: "Europe/Berlin", dateStyle: "short", timeStyle: "medium"}).format(now);
const zone = new Intl.DateTimeFormat("en-GB", {timeZone: "Europe/Berlin", timeZoneName: "short"}).formatToParts(now).find(p => p.type == "timeZoneName").value;
console.log(JSON.stringify({
  sha: full, short: full.slice(0, 7), read: `${berlin} ${zone == "GMT+2" ? "CEST" : zone == "GMT+1" ? "CET" : zone}`,
  release: {version, tag: `v${version}`, tag_commit: tag[0], tag_time: tag.slice(1).join(" "), date: section[1], headline: section[2].replace(/\s+/g, " ")},
  wrecks,
  counts: Object.fromEntries(["In Progress", "Proposed", "Shipped", "Closed"].map(s => [s, wrecks.filter(w => w.status == s).length])),
}, null, 1));
