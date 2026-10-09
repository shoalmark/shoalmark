"""The landing's figures and the probe prompt's pins, read from the repository at the commit the site is built from (FM-006, B1).

Run it before every site build — in docs.yml, in a local build and in the suite's own builds alike:

    python3 scripts/landing_facts.py && zensical build --clean

It writes `overrides/partials/landing/facts.html`, which is generated and never committed (`.gitignore`); the landing reads every
figure from it: `release`, `hiscore`, `hiscore_last`, `read`, `excerpt`, `pins`, `counts` and `wrecks_json`. It removes the file it wrote last before
it reads anything, and writes the new one only when every reading holds: whatever it cannot read stops the build with one line
and exit 1, and a build without the file stops at the template's import, so no page is built with an empty or a stale figure.

- **release**: the release `VERSION` names, its day from that version's CHANGELOG heading, written as *9 October 2026* and
  *9. Oktober 2026*. A build that deploys — a tag's (`--event push`, its tag `--ref`) or one by hand (`--event
  workflow_dispatch`) — and a local one are built from a tagged release: the newest `v*` tag the commit holds is the one VERSION
  names. A pull request's build (`--event pull_request`), which never deploys, may run ahead of the newest tag: a release's
  own pull request carries the next VERSION; it may not fall behind it.
- **hiscore**, **hiscore_last**: FM-006's rule over the merged pull requests — the Owner's own answer branches left out — opened
  after the Owner's signed answer of 24 September 2026, 11:07 CEST (`ffa63b8`): one counts when a commit of its own, merge
  commits excluded, that adds or changes a file under `work-tracker/evidence/reviews/` is dated before the pull request was
  opened. The pull requests come from GitHub's API — with docs.yml's own token where `LANDING_FACTS_TOKEN` holds it, without one
  in a local build — or from a recorded response (`--pulls`); their commits come from git, so the history must be whole.
- **read**: the build's day (Europe/Berlin; `SOURCE_DATE_EPOCH` where it is set) and the commit.
- **excerpt**: what `shoalmark.py --owner` prints at the commit — the commit's own tool, run in a throwaway clone checked out
  there, with no branch but the commit's history: how many questions wait for the Owner, how many acts they owe, and the first
  act's id and line as it prints them, HTML-escaped.
- **wrecks_json**: every tracker tagged `bug` or `security`, read through shoalmark.py's own reader, with the fields and the
  report's sentences as `work-tracker/evidence/FM-006/landing/start-page/facts.mjs` reads them. Open means In Progress or
  Proposed; any status but In Progress, Proposed, Shipped and Closed stops the build. A wreck keeps the position the chart's
  drawing gave it (`DRAWN`); one the drawing has not placed is placed by the drawing's rule, in the order of its id: the flat
  pixel farthest from every other wreck and every name, at least 12 chart pixels inside the border, its button clear of the
  hero's text, its 7 × 5 footprint all flat or sand. The same trackers always give the same output. **counts**, the top bar's: the
  wrecks and the open ones, counted from that same list.
- **pins**: the probe prompt's placeholders (the probe lane's pins.md). With the probe switch off — `[project.extra] probe` in
  zensical.toml — they are the commit, the release's tag and two marked stand-ins, and nothing of them is published. With it
  on they come from ADOPT's pin line, pins.md's checks 1–5 and 7 run (6 and 9 too on a deploy build), and a stand-in left
  stops the build.

`--check SITE`, after `zensical build`: the landing's release label, its link and the footer's link are the release this commit
reads, and so is `facts.html`'s; and `facts.html`'s counts are what its `wrecks_json` holds.
"""

from __future__ import annotations

import argparse
import datetime
import hashlib
import html
import importlib.util
import io
import json
import math
import os
import re
import shutil
import stat
import subprocess
import sys
import tempfile
import urllib.error
import urllib.parse
import urllib.request
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]                # the tree this build renders: its config, its template, its output
OUT = Path("overrides/partials/landing/facts.html")
RULE_COMMIT = "ffa63b8c2235e8501e6176599db11043b4cbad89"  # the Owner's signed answer of 24 September 2026, 11:07 CEST: the review rule
REVIEWS = "work-tracker/evidence/reviews/"
MOCK = "work-tracker/evidence/FM-006/landing/index.html"  # the mock the Owner saw: how many sentences each report carries
TEMPLATE = "overrides/landing.html"                      # the chart's geography and its names, as the page draws them
STATUSES, OPEN = ("In Progress", "Proposed", "Shipped", "Closed"), ("In Progress", "Proposed")
STAND_IN = {"ARCHIVE_URL": "[ARCHIVE URL — filled at build]", "ARCHIVE_SHA256": "[SHA-256 — filled at build]"}
MONTHS_EN = ("January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December")
MONTHS_DE = ("Januar", "Februar", "März", "April", "Mai", "Juni", "Juli", "August", "September", "Oktober", "November", "Dezember")

# The wrecks the chart's drawing placed, in the drawing's order: the landing's WRECKS at a86667f.
DRAWN = (
    ("FM-041", 8.223, 53.623), ("FM-040", 6.981, 53.593), ("FM-039", 8.639, 53.979), ("FM-038", 7.077, 53.54), ("FM-037", 8.38, 53.845),
    ("FM-036", 8.25, 53.735), ("FM-035", 8.52, 54.018), ("FM-034", 7.52, 53.716), ("FM-033", 8.45, 53.905), ("FM-030", 7.26, 53.706),
    ("FM-029", 7.92, 53.762), ("FM-028", 8.17, 53.69), ("FM-018", 6.84, 53.585), ("FM-007", 8.75, 54.02), ("FM-009", 6.97, 53.716),
    ("FM-010", 7.03, 53.664), ("FM-011", 7.4, 53.712), ("FM-012", 7.66, 53.736), ("FM-013", 7.8, 53.745), ("FM-014", 7.13, 53.654),
    ("FM-015", 8.02, 53.735), ("FM-016", 8.375, 53.948), ("FM-017", 8.33, 53.652), ("FM-019", 8.47, 53.8), ("FM-020", 8.57, 53.878),
    ("FM-021", 8.78, 54.075), ("FM-022", 6.72, 53.522),
)
# Measured in Chrome on the B1 template at c00a747, in chart pixels (x0, y0, x1, y1), rounded outward. TITLE: the hero's text block
# where the page lays it over the chart (1280 px wide and more) — its widest and tallest over both languages, both launch states,
# 1280 to 2560 px wide and 720 to 1200 px high: 14, 9, 164, 120.71. WRECK: a wreck's button, its label included, around the point
# it marks, at its largest (1280 to 1599 px wide): ±6.37, 6 above, 4 below. A new wreck's button stays clear of the title.
TITLE, WRECK = (14, 9, 164, 121), (-6.5, -6, 6.5, 4)
BORDER, FOOTPRINT = 12, (-3, 3, -2, 2)                   # the footprint: 7 pixels wide, 5 high, centred on the wreck's pixel
EVENTS = ("", "pull_request", "push", "workflow_dispatch")


class Stop(Exception):
    """What the build cannot read: one line, and the build stops."""


def stop(message):
    raise Stop(message)


class Git:
    def __init__(self, repo):
        self.repo = Path(repo)
        self.env = {k: v for k, v in os.environ.items() if k not in ("GIT_DIR", "GIT_WORK_TREE", "GIT_INDEX_FILE", "GIT_PREFIX")}

    def raw(self, *args, stdin=None):
        r = subprocess.run(["git", "-C", str(self.repo), *args], input=stdin, capture_output=True, env=self.env)
        return r.returncode, r.stdout

    def __call__(self, *args, stdin=None, what=None):
        code, out = self.raw(*args, stdin=None if stdin is None else stdin.encode("utf-8"))
        if code:
            stop(what or f"git {' '.join(args[:3])} failed in {self.repo}")
        return out.decode("utf-8")

    def has(self, rev):
        return self.raw("cat-file", "-e", f"{rev}^{{commit}}")[0] == 0


def berlin():
    zone, ok = _tool().ratio_zone()
    if not ok:
        stop("no time zone database for Europe/Berlin here: the filing days and the build's day are Berlin days")
    return zone


_FM = []


def _tool():
    """shoalmark.py of the tree being built, imported unchanged: the trackers are read through its own reader."""
    if not _FM:
        spec = importlib.util.spec_from_file_location("shoalmark_tool", ROOT / "shoalmark.py")
        if spec is None or not (ROOT / "shoalmark.py").is_file():
            stop(f"no shoalmark.py beside {ROOT / 'scripts'}: the trackers are read through its reader")
        fm = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(fm)
        fm.configure(ROOT)
        _FM.append(fm)
    return _FM[0]


def day_en(d):
    return f"{d.day} {MONTHS_EN[d.month - 1]} {d.year}"


def day_de(d):
    return f"{d.day}. {MONTHS_DE[d.month - 1]} {d.year}"


def repo_url(git, commit):
    text = git("show", f"{commit}:zensical.toml", what=f"no zensical.toml at {commit[:7]}")
    m = re.search(r'^repo_url\s*=\s*"(https://github\.com/([\w.-]+/[\w.-]+))"\s*$', text, re.M)
    if not m:
        stop("zensical.toml names no repo_url on GitHub: the wrecks' links and the pull requests are read from it")
    return m.group(1), m.group(2)


# --- the release -------------------------------------------------------------------------------------------------------------

def read_release(git, commit, event="", ref=""):
    version = git("show", f"{commit}:VERSION", what=f"no VERSION at {commit[:7]}").strip()
    if not re.fullmatch(r"\d+\.\d+\.\d+", version):
        stop(f"VERSION reads {version!r} at {commit[:7]}, not a release number")
    code, out = git.raw("describe", "--tags", "--abbrev=0", "--match", "v[0-9]*", commit)
    tag = out.decode("utf-8").strip() if code == 0 else ""
    if event == "pull_request":                           # never deploys: a release's own pull request runs ahead of the newest tag
        held = re.fullmatch(r"v(\d+)\.(\d+)\.(\d+)", tag)
        if tag and not held:
            stop(f"the newest release tag {commit[:7]} holds is {tag}, not vX.Y.Z")
        if held and tuple(map(int, version.split("."))) < tuple(map(int, held.groups())):
            stop(f"VERSION says {version}, behind the release tag {tag} that {commit[:7]} holds")
    elif tag != f"v{version}":
        stop(f"VERSION says {version}, and the newest release tag {commit[:7]} holds is {tag or 'none'}: a build that deploys, or a local "
             f"one, is built from a tagged release (a pull request's build reads --event pull_request)")
    if event == "push" and ref != f"v{version}":
        stop(f"a tag's build of {ref or 'no tag'}, and VERSION says {version}: the tag pushed is the release the site names")
    changelog = git("show", f"{commit}:CHANGELOG.md", what=f"no CHANGELOG.md at {commit[:7]}")
    m = re.search(rf"^## {re.escape(version)} — (\d{{4}})-(\d{{2}})-(\d{{2}})$", changelog, re.M)
    if not m:
        stop(f"CHANGELOG.md has no heading `## {version} — YYYY-MM-DD` at {commit[:7]}: the release's day is read from it")
    day = datetime.date(*map(int, m.groups()))
    return {"tag": f"v{version}", "version": version, "date_en": day_en(day), "date_de": day_de(day)}


# --- the high scores ---------------------------------------------------------------------------------------------------------

def fetch_pulls(slug, token):
    """Every closed pull request of `slug`, oldest first, from GitHub's REST API."""
    pulls, page = [], 1
    while True:
        url = f"https://api.github.com/repos/{slug}/pulls?state=closed&per_page=100&sort=created&direction=asc&page={page}"
        head = {"Accept": "application/vnd.github+json", "X-GitHub-Api-Version": "2022-11-28", "User-Agent": "shoalmark-landing-facts"}
        if token:
            head["Authorization"] = f"Bearer {token}"
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=head), timeout=60) as r:
                batch = json.loads(r.read().decode("utf-8"))
        except urllib.error.HTTPError as e:
            stop(f"GitHub's API answered {e.code} for {slug}'s pull requests, page {page}"
                 + ("" if token else " (read without a token: 60 requests an hour)"))
        except (urllib.error.URLError, OSError, ValueError) as e:
            stop(f"GitHub's API could not be read for {slug}'s pull requests, page {page}: {getattr(e, 'reason', e)}")
        if not isinstance(batch, list):
            stop(f"GitHub's API answered something other than a list for {slug}'s pull requests, page {page}")
        pulls += batch
        if len(batch) < 100:
            return pulls
        page += 1


def trim(pull):
    """A pull request as FM-006's rule reads it — the fields a recorded response keeps."""
    try:
        return {"number": int(pull["number"]), "created_at": pull["created_at"], "merged_at": pull["merged_at"],
                "head": {"ref": pull["head"]["ref"], "sha": pull["head"]["sha"]}, "base": {"sha": pull["base"]["sha"]}}
    except (KeyError, TypeError, ValueError):
        stop(f"a pull request reads without the fields FM-006's rule needs: {str(pull)[:80]}")


def utc(stamp):
    return datetime.datetime.strptime(stamp, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=datetime.timezone.utc).timestamp()


def score(git, pulls):
    """(after the rule: counted, of, the last pull request counted; before it: counted, of) — FM-006's rule."""
    if not git.has(RULE_COMMIT):
        stop(f"this history does not hold {RULE_COMMIT[:7]}, the Owner's signed answer the high scores are split at: build from a "
             f"full clone (fetch-depth: 0)")
    rule_at = int(git("show", "-s", "--format=%ct", RULE_COMMIT))
    merged = sorted((p for p in map(trim, pulls) if p["merged_at"] and not p["head"]["ref"].startswith("answer/")), key=lambda p: p["number"])
    ends = sorted({p[side]["sha"] for p in merged for side in ("head", "base")})
    held = {ln.split()[0] for ln in git("cat-file", "--batch-check", stdin="\n".join(ends) + "\n").splitlines() if not ln.endswith(" missing")}
    for p in merged:
        for side in ("head", "base"):
            if p[side]["sha"] not in held:
                stop(f"this history does not hold pull request #{p['number']}'s {side} {p[side]['sha'][:7]}: build from a full clone (fetch-depth: 0)")
    parents = {}                                           # every commit the pull requests' ends hold, with its parents
    for line in git("rev-list", "--parents", "--stdin", stdin="\n".join(ends) + "\n").splitlines():
        sha, *up = line.split()
        parents[sha] = up

    def ancestors(start):
        seen, todo = set(), [start]
        while todo:
            c = todo.pop()
            if c not in seen:
                seen.add(c)
                todo += parents.get(c, ())
        return seen
    # a pull request's own commits: those its head holds and its base does not, merge commits excluded
    own = {p["number"]: [c for c in ancestors(p["head"]["sha"]) - ancestors(p["base"]["sha"]) if len(parents.get(c, ())) < 2] for p in merged}
    touched, sha = {}, None
    heads = "\n".join(sorted({p["head"]["sha"] for p in merged})) + "\n"
    for line in git("log", "--no-merges", "--no-renames", "--format=%x00%H %ct", "--name-status", "--stdin", "--", REVIEWS, stdin=heads).splitlines():
        if line.startswith("\x00"):
            sha, at = line[1:].split()
            continue
        if line.strip() and line[0] in "AMT":                # a file under the reviews folder added or changed (a deletion is neither)
            touched[sha] = int(at)
    counts = lambda p: any(touched.get(c, float("inf")) < utc(p["created_at"]) for c in own[p["number"]])
    after = [p for p in merged if utc(p["created_at"]) >= rule_at]
    before = [p for p in merged if utc(p["created_at"]) < rule_at]
    if not after:
        stop("no merged pull request was opened after the review rule: there is no high score to read")
    return (sum(map(counts, after)), len(after), after[-1]["number"]), (sum(map(counts, before)), len(before))


def read_pulls(recorded, slug, token):
    if recorded is None:
        return fetch_pulls(slug, token)
    try:
        data = json.loads(Path(recorded).read_text(encoding="utf-8"))
    except (OSError, ValueError) as e:
        stop(f"the recorded pull requests {recorded} cannot be read: {e}")
    return data["pulls"] if isinstance(data, dict) else data


# --- the wrecks --------------------------------------------------------------------------------------------------------------

END = re.compile(r"(?<=[.?!]) (?=[A-Z`*\"'0-9])")         # a sentence ends at . ? or ! before a space and a capital, a backtick, …


def sentences(s):
    return END.split(s.strip())


def unquote(v):
    return re.sub(r'\\(["\\])', r"\1", v[1:-1]) if len(v) > 1 and v[0] == v[-1] == '"' else v


def js_array(template, name):
    m = re.search(rf"^const {name} = (\[.*?\]);", template, re.S | re.M)
    if not m:
        stop(f"{TEMPLATE} holds no `const {name} = [...]`: the chart's drawing is read from it to place a wreck")
    try:
        return json.loads(re.sub(r",\s*\]", "]", m.group(1)))
    except ValueError:
        stop(f"{TEMPLATE}'s `const {name}` is not plain data: the chart's drawing is read from it to place a wreck")


class Chart:
    """The chart as the landing's script draws it, pixel for pixel: what lies under each pixel, and where the names stand."""

    def __init__(self, template):
        m = re.search(r"^const R = \{lon0: ([\d.]+), lon1: ([\d.]+), lat0: ([\d.]+), lat1: ([\d.]+)\}, W = (\d+), H = (\d+);", template, re.M)
        if not m:
            stop(f"{TEMPLATE} holds no `const R = {{lon0: …}}, W = …, H = …;`: the chart's frame is read from it to place a wreck")
        self.lon0, self.lon1, self.lat0, self.lat1 = map(float, m.groups()[:4])
        self.w, self.h = int(m.group(5)), int(m.group(6))
        poly = lambda pts: self.box([(self.x(lo), self.y(la)) for lo, la in pts])
        self.flats = [poly(p) for p in js_array(template, "FLATS")]
        self.sand = [poly(p) for p in js_array(template, "SAND")]
        self.land = [poly(p) for p in js_array(template, "LAND")] + [poly(p) for _, p in js_array(template, "ISLES")]
        self.channels = []
        for width, pts in js_array(template, "CHANNELS"):
            p = [(self.x(lo), self.y(la)) for lo, la in pts]
            self.channels += [(width / 2, a, b, min(a[0], b[0]) - width, max(a[0], b[0]) + width, min(a[1], b[1]) - width, max(a[1], b[1]) + width)
                              for a, b in zip(p, p[1:])]
        self.names = [(self.x(lo), self.y(la)) for _, _, lo, la in js_array(template, "NAMES")]
        self._kind = {}

    def x(self, lon):
        return (lon - self.lon0) / (self.lon1 - self.lon0) * self.w

    def y(self, lat):
        return (self.lat1 - lat) / (self.lat1 - self.lat0) * self.h

    @staticmethod
    def box(pts):
        xs, ys = [p[0] for p in pts], [p[1] for p in pts]
        return pts, min(xs), max(xs), min(ys), max(ys)

    @staticmethod
    def inside(x, y, shape):                               # the script's inPoly; outside its box a point is outside it
        pts, x0, x1, y0, y1 = shape
        if not (x0 <= x <= x1 and y0 <= y <= y1):
            return False
        c, j = False, len(pts) - 1
        for i in range(len(pts)):
            (xi, yi), (xj, yj) = pts[i], pts[j]
            if (yi > y) != (yj > y) and x < (xj - xi) * (y - yi) / (yj - yi) + xi:
                c = not c
            j = i
        return c

    def kind(self, px, py):
        """flat, sand or other — the layer the script draws last at this pixel: channels, land and islands over flats and sand."""
        if (px, py) not in self._kind:
            x, y, k = px + .5, py + .5, "other"
            if any(self.inside(x, y, s) for s in self.flats):
                k = "flat"
            if any(self.inside(x, y, s) for s in self.sand):
                k = "sand"
            if k != "other":
                for half, (ax, ay), (bx, by), x0, x1, y0, y1 in self.channels:
                    if x0 <= x <= x1 and y0 <= y <= y1:
                        dx, dy = bx - ax, by - ay
                        t = max(0, min(1, ((x - ax) * dx + (y - ay) * dy) / (dx * dx + dy * dy or 1)))
                        if math.hypot(x - ax - t * dx, y - ay - t * dy) <= half:
                            k = "other"
                            break
            if k != "other" and any(self.inside(x, y, s) for s in self.land):
                k = "other"
            self._kind[px, py] = k
        return self._kind[px, py]

    def place(self, others):
        """The flat pixel farthest from every other wreck and every name, at least BORDER chart pixels inside the border, its
        button clear of the title, its footprint all flat or sand: (lon, lat) of its centre, to three places. The first such pixel,
        row by row, where two are as far."""
        (fx0, fx1, fy0, fy1), points, best, at = FOOTPRINT, list(others) + self.names, -1.0, None
        for py in range(self.h):
            for px in range(self.w):
                x, y = px + .5, py + .5
                if not (BORDER <= x <= self.w - BORDER and BORDER <= y <= self.h - BORDER):
                    continue
                if x + WRECK[0] < TITLE[2] and x + WRECK[2] > TITLE[0] and y + WRECK[1] < TITLE[3] and y + WRECK[3] > TITLE[1]:
                    continue
                if self.kind(px, py) != "flat":
                    continue
                if any(self.kind(u, v) not in ("flat", "sand") for v in range(py + fy0, py + fy1 + 1) for u in range(px + fx0, px + fx1 + 1)):
                    continue
                d = min(math.hypot(x - a, y - b) for a, b in points)
                if d > best:
                    best, at = d, (x, y)
        if at is None:
            stop("the chart has no flat pixel left to place a wreck on by the drawing's rule")
        lon = self.lon0 + at[0] / self.w * (self.lon1 - self.lon0)
        lat = self.lat1 - at[1] / self.h * (self.lat1 - self.lat0)
        return float(f"{lon:.3f}"), float(f"{lat:.3f}")


def wreck_counts(wrecks):
    """The top bar's counts, from the one list that draws the chart: every wreck, and the open ones — In Progress or Proposed."""
    return {"wrecks": len(wrecks), "open": sum(w["status"] in OPEN for w in wrecks)}


def read_wrecks(git, commit, url):
    fm, zone = _tool(), berlin()
    mock = git("show", f"{commit}:{MOCK}", what=f"no {MOCK} at {commit[:7]}: each report's sentences are counted from the mock's")
    m = re.search(r"^const WRECKS = (\[.*\]);$", mock, re.M)
    if not m:
        stop(f"{MOCK} holds no `const WRECKS = [...];` line: each report's sentences are counted from the mock's")
    counts = {w["id"]: len(sentences(w["report"])) for w in json.loads(m.group(1))}
    wrecks = {}
    for path in git("ls-tree", "-z", "--name-only", commit, "work-tracker/").split("\0"):      # -z: a name as it is, never quoted
        m = re.match(r"^work-tracker/(FM-(\d+))-.*\.md$", path)
        if not m:
            continue
        text = git("show", f"{commit}:{path}")
        t = fm.extract(Path(path), text=text)
        if "bug" not in t["tags"] and "security" not in t["tags"]:
            continue
        wid = m.group(1)
        if t["status"] not in STATUSES:
            stop(f"{wid}'s status reads as {t['status']} — a wreck is In Progress, Proposed, Shipped or Closed, and the build stops rather than guess")
        title = re.search(r"^# (.+)$", text, re.M)
        if not title or not title.group(1).startswith(f"{wid} — "):
            stop(f"{wid}'s first `# ` line does not begin `{wid} — `: the wreck's title is read from it")
        hook = unquote(t["fm"].get("hook") or "")
        if not hook:
            stop(f"{wid} has no `hook:`: the wreck's report is read from it")
        n = counts.get(wid, 1)
        report = " ".join(sentences(hook)[:n])
        if not hook.startswith(report):
            stop(f"{wid}'s report is not the beginning of its hook")
        added = git("log", commit, "--diff-filter=A", "--abbrev=7", "--format=%h %at", "--", path).strip().splitlines()
        if not added:
            stop(f"no commit before {commit[:7]} added {path}: the wreck's incident and filing day are read from it")
        inc, at = added[-1].split()
        wrecks[wid] = {"id": wid, "inc": inc, "filed": datetime.datetime.fromtimestamp(int(at), zone).strftime("%Y-%m-%d"),
                       "status": t["status"], "title": title.group(1)[len(wid) + 3:], "report": report, "url": f"{url}/blob/main/{urllib.parse.quote(path)}"}
    drawn = [(i, lon, lat) for i, lon, lat in DRAWN if i in wrecks]
    new = sorted(set(wrecks) - {i for i, _, _ in DRAWN}, key=lambda i: int(i.split("-")[1]))
    at = {i: (lon, lat) for i, lon, lat in drawn}
    if new:
        chart = Chart(git("show", f"{commit}:{TEMPLATE}", what=f"no {TEMPLATE} at {commit[:7]}: the chart's drawing is read from it"))
        for i in new:
            at[i] = chart.place((chart.x(lo), chart.y(la)) for lo, la in at.values())
    order = sorted(new, key=lambda i: -int(i.split("-")[1])) + [i for i, _, _ in drawn]   # the newest first, as the mock drew them
    return [{**{k: wrecks[i][k] for k in ("id", "inc", "filed", "status")}, "lon": at[i][0], "lat": at[i][1],
             **{k: wrecks[i][k] for k in ("title", "report", "url")}} for i in order]


# --- the board's excerpt -----------------------------------------------------------------------------------------------------

def _rmtree(path):
    """A throwaway clone removed, on Windows too, where git leaves files read-only."""
    shutil.rmtree(path, onerror=lambda f, p, e: (os.chmod(p, stat.S_IWRITE), f(p)))


def read_excerpt(git, commit):
    """{waiting, acts, act}: what `shoalmark.py --owner` prints at `commit`, run by the commit's own tool in a throwaway clone of
    this history, checked out there, its hooks off, with no remote and no branch — so only the commit and its history count."""
    d = Path(tempfile.mkdtemp(prefix="landing-facts-"))
    try:
        at = d / "at"
        q = ["-c", "core.hooksPath=" + os.devnull, "-c", "advice.detachedHead=false"]
        steps = (["clone", "--quiet", "--shared", "--no-checkout", str(git.repo), str(at)], ["-C", str(at), "checkout", "--quiet", "--detach", commit],
                 ["-C", str(at), "remote", "remove", "origin"])
        for step in steps:
            if subprocess.run(["git", *q, *step], capture_output=True, env=git.env).returncode:
                stop(f"the board's excerpt: a throwaway clone at {commit[:7]} could not be made (git {step[0] if step[0] != '-C' else step[2]})")
        heads = subprocess.run(["git", "-C", str(at), "for-each-ref", "--format=delete %(refname)", "refs/heads"], capture_output=True, env=git.env).stdout
        subprocess.run(["git", "-C", str(at), "update-ref", "--stdin"], input=heads, capture_output=True, env=git.env, check=False)
        tool = at / "shoalmark.py"
        if not tool.is_file():
            stop(f"no shoalmark.py at {commit[:7]}: the board's excerpt is what it prints")
        title = re.search(r'^ACTS_TITLE = "([^"\n]+)"$', tool.read_text(encoding="utf-8"), re.M)
        if not title:
            stop(f"shoalmark.py at {commit[:7]} names no ACTS_TITLE: the acts are read under it")
        try:
            r = subprocess.run([sys.executable, str(tool), "--root", str(at), "--owner"], cwd=str(at), capture_output=True, env=git.env, timeout=600)
        except subprocess.TimeoutExpired:
            stop(f"shoalmark.py --owner did not finish within 600 s at {commit[:7]}")
    finally:
        _rmtree(d)
    out = r.stdout.decode("utf-8", errors="replace").splitlines()
    if r.returncode or not out:
        stop(f"shoalmark.py --owner exited {r.returncode} at {commit[:7]}, printing {len(out)} line(s): the board's excerpt is what it prints")
    return excerpt_of(out, title.group(1), commit)


def excerpt_of(out, acts_title, commit=""):
    """The excerpt from `--owner`'s lines: its first line's count of questions, and the acts listed under `acts_title`."""
    head = out[0]
    m = re.match(r"^(\d+) NEED THE OWNER( · |$)", head)
    if m:
        waiting = int(m.group(1))
    elif head.startswith("NO QUESTION FOR THE OWNER") or head == "NOTHING NEEDS THE OWNER.":
        waiting = 0
    else:
        stop(f"shoalmark.py --owner's first line at {commit[:7]} reads {head[:60]!r}: neither questions counted nor none")
    acts = []
    if acts_title in out:
        for line in out[out.index(acts_title) + 1:]:
            if not line.strip():
                break
            a = re.match(r"^  ([A-Z][A-Z0-9]*-\d+) — (\S.*)$", line)
            if a:
                acts.append(a.groups())
            elif not line.startswith("       "):
                stop(f"shoalmark.py --owner lists an act at {commit[:7]} as {line[:60]!r}, not `  <id> — <its line>`")
    owed = re.search(r" · (\d+) ACT\(S\) OWED", head)
    if owed and int(owed.group(1)) != len(acts):
        stop(f"shoalmark.py --owner's first line at {commit[:7]} counts {owed.group(1)} act(s), and it lists {len(acts)}")
    return {"waiting": waiting, "acts": len(acts), "act": {"id": acts[0][0], "line": html.escape(acts[0][1])} if acts else None}


# --- the probe prompt's pins -------------------------------------------------------------------------------------------------

NOTES = {"ADOPT.md": "The pin: ", "ADOPT.de.md": "Die Festlegung: "}
SVN_NOTES = ("ADOPT.svn.md", "ADOPT.svn.de.md")


def probe_switch(config):
    """`[project.extra] probe` in zensical.toml: true or false, as Zensical reads it."""
    try:
        text = Path(config).read_text(encoding="utf-8")
    except OSError:
        stop(f"no {config}: the probe switch is read from it")
    try:
        import tomllib
    except ImportError:                                  # Python before 3.11: the one form the switch is written in, else stop
        section, value = None, False
        for line in text.splitlines():
            head = re.match(r"^\s*\[\s*([^\]]+?)\s*\]\s*(#.*)?$", line)
            if head:
                section = head.group(1)
                continue
            one = re.match(r"^\s*probe\s*=\s*(true|false)\s*(#.*)?$", line)
            if one and section == "project.extra":
                value = one.group(1) == "true"
            elif re.search(r"\bprobe\b", line):
                stop(f"{config} names `probe` where this Python ({sys.version_info[0]}.{sys.version_info[1]}) cannot read it: write the "
                     f"switch as `probe = true` or `probe = false` under [project.extra], or build with Python 3.11 or later")
        return value
    try:
        value = tomllib.loads(text).get("project", {}).get("extra", {}).get("probe", False)
    except (tomllib.TOMLDecodeError, AttributeError) as e:
        stop(f"{config} cannot be read: {e}")
    if not isinstance(value, bool):
        stop(f"{config}'s [project.extra] probe is true or false; it reads {value!r}")
    return value


def read_pins(git, commit, release, slug, switch, deploy, main, archive):
    """The prompt's four pins. Off: the commit, the release's tag and two marked stand-ins. On: ADOPT's pin line, checked."""
    if not switch:
        return {"ADOPT_COMMIT": commit, "TAG": release["tag"], **STAND_IN}
    for f in (*NOTES, *SVN_NOTES):
        if git.raw("cat-file", "-e", f"{commit}:{f}")[0]:
            stop(f"pins check 1: {f} is missing at {commit[:7]}")
    text = {f: git("show", f"{commit}:{f}") for f in (*NOTES, *SVN_NOTES)}
    lines = {f: [ln for ln in text[f].splitlines() if ln.startswith(head)] for f, head in NOTES.items()}
    if any(len(v) != 1 for v in lines.values()):
        stop("pins check 2: not exactly one pin line in each note (`The pin: ` in ADOPT.md, `Die Festlegung: ` in ADOPT.de.md)")
    fields = {f: re.findall(r"`([^`]+)`", v[0]) for f, v in lines.items()}
    if fields["ADOPT.md"] != fields["ADOPT.de.md"]:
        stop("pins check 2: the two notes pin different things")
    if len(fields["ADOPT.md"]) != 5:
        stop(f"pins check 2: the pin line has {len(fields['ADOPT.md'])} fields, not 5")
    tag, url, archive_sum, tool, tool_sum = fields["ADOPT.md"]
    if not re.fullmatch(r"v\d+\.\d+\.\d+", tag):
        stop(f"pins check 2: {tag} is no release tag")
    # one file name, in the tag's own folder of this repository's releases: no dot segment, no further slash, no percent-escape of either
    if not re.fullmatch(rf"https://github\.com/{re.escape(slug)}/releases/download/{re.escape(tag)}/[A-Za-z0-9][A-Za-z0-9._-]*", url):
        stop(f"pins check 2: {url} is not an asset of {tag}")
    if tool != "shoalmark.py" or not all(re.fullmatch(r"[0-9a-f]{64}", s) for s in (archive_sum, tool_sum)):
        stop("pins check 2: the pin line's shape — release, archive, its SHA-256, `shoalmark.py`, its SHA-256")
    for f in NOTES:
        if sum(1 for ln in text[f].splitlines() if re.search(r"[0-9a-f]{64}", ln)) != 1:
            stop(f"pins check 2: {f} names a SHA-256 outside its pin line")
    for f in SVN_NOTES:
        if re.search(r"[0-9a-f]{64}|`v[0-9]+\.[0-9]+\.[0-9]+`", text[f]):
            stop(f"pins check 2: {f} carries a pin")
    for f in (*NOTES, *SVN_NOTES):
        if "{{" in text[f]:
            stop(f"pins check 7: {f} still holds a placeholder")
    if git.raw("rev-parse", "-q", "--verify", f"refs/tags/{tag}")[0]:
        stop(f"pins check 3: {tag} does not exist")
    if not git.has(main):
        stop(f"pins check 3: {main} is not in this history: build from a full clone (fetch-depth: 0)")
    if git.raw("merge-base", "--is-ancestor", f"{tag}^{{commit}}", main)[0]:
        stop(f"pins check 3: {tag} is not on main")
    code, blob = git.raw("show", f"{tag}:shoalmark.py")
    got = hashlib.sha256(blob).hexdigest() if code == 0 else "missing"
    if got != tool_sum:
        stop(f"pins check 4: {tag}:shoalmark.py is {got}, ADOPT names {tool_sum}")
    code, out = git.raw("describe", "--tags", "--abbrev=0", "--match", "v[0-9]*", commit)
    newest = out.decode("utf-8").strip() if code == 0 else "none"
    if newest != tag:
        stop(f"pins check 5: ADOPT names {tag}, the newest release this commit holds is {newest}")
    if deploy:
        if git.raw("merge-base", "--is-ancestor", commit, main)[0]:
            stop(f"pins check 6: {commit} is not on main")
        try:
            if archive:
                data = Path(archive).read_bytes()
            else:
                with urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "shoalmark-landing-facts"}), timeout=120) as r:
                    data = r.read()
        except (OSError, urllib.error.URLError) as e:
            stop(f"pins check 9: the archive does not download: {getattr(e, 'reason', e)}")
        if hashlib.sha256(data).hexdigest() != archive_sum:
            stop(f"pins check 9: the archive's SHA-256 is not {archive_sum}")
        try:
            inside = hashlib.sha256(zipfile.ZipFile(io.BytesIO(data)).read("shoalmark.py")).hexdigest()
        except (zipfile.BadZipFile, KeyError) as e:
            stop(f"pins check 9: the archive holds no shoalmark.py: {e}")
        if inside != tool_sum:
            stop(f"pins check 9: the archive's shoalmark.py is {inside}, not {tool_sum}")
    pins = {"ADOPT_COMMIT": commit, "TAG": tag, "ARCHIVE_URL": url, "ARCHIVE_SHA256": archive_sum}
    if set(pins.values()) & set(STAND_IN.values()):
        stop("the probe switch is on and a pin is still a stand-in")
    return pins


# --- the file ----------------------------------------------------------------------------------------------------------------

SAFE = re.compile(r"[^\"\\{}%#<>\n\r]*")


def lit(value):
    """A Jinja literal for a value whose shape was checked: it holds nothing that could end the string or open a tag."""
    if isinstance(value, bool) or not isinstance(value, (int, str)) or isinstance(value, str) and not SAFE.fullmatch(value):
        stop(f"a figure reads {value!r}, which facts.html does not carry")
    return json.dumps(value, ensure_ascii=False)


def js_string(s):
    """A JSON string for inside `<script>` and a Jinja block: no `</`, no `<!--`, no brace, no JavaScript line separator."""
    out = json.dumps(s, ensure_ascii=False).replace("</", "<\\/").replace("<!--", "\\u003c!--")
    return out.replace("{", "\\u007b").replace("}", "\\u007d").replace("\u2028", "\\u2028").replace("\u2029", "\\u2029")


def js_value(v):
    return js_string(v) if isinstance(v, str) else json.dumps(v)


def jinja_value(v):
    """A Jinja literal of any text, numbers, `none` and dicts: every character that could end the string, open a tag or break a line
    written as \\uXXXX, which the template engine reads back as the character itself."""
    if v is None:
        return "none"
    if isinstance(v, bool) or isinstance(v, (int, float)):
        return json.dumps(v)
    if isinstance(v, dict):
        return "{" + ", ".join(f"{json.dumps(k)}: {jinja_value(x)}" for k, x in v.items()) + "}"
    if not isinstance(v, str):
        stop(f"a figure reads {v!r}, which facts.html does not carry")
    bad = lambda ch: ch in "\"\\{}%#<>&`'" or ord(ch) < 0x20 or 0x7f <= ord(ch) <= 0x9f or ch in "\u2028\u2029"
    return '"' + "".join(f"\\u{ord(ch):04x}" if bad(ch) else ch for ch in v) + '"'


def facts_html(commit, release, hiscore, last, read, pins, wrecks, excerpt, counts):
    obj = lambda d: "{" + ", ".join(f"{json.dumps(k)}: {lit(v)}" for k, v in d.items()) + "}"
    wrecks_json = "[" + ", ".join("{" + ", ".join(f"{json.dumps(k)}: {js_value(v)}" for k, v in w.items()) + "}" for w in wrecks) + "]"
    return (f"{{#- Generated by scripts/landing_facts.py from {commit} on {read['date']}; never committed, never edited by hand. The landing reads\n"
            f"    every figure from here (FM-006, B1). -#}}\n"
            f"{{% set release = {obj(release)} %}}\n"
            f"{{% set hiscore = {lit(hiscore)} %}}\n"
            f"{{% set hiscore_last = {lit(last)} %}}\n"
            f"{{% set pins = {obj(pins)} %}}\n"
            f"{{% set read = {obj(read)} %}}\n"
            f"{{% set excerpt = {jinja_value(excerpt)} %}}\n"
            f"{{% set counts = {obj(counts)} %}}\n"
            f"{{% set wrecks_json %}}{wrecks_json}{{% endset %}}\n")


def check_shapes(release, hiscore, last, read, pins, commit, excerpt):
    shapes = ((release["tag"], r"v\d+\.\d+\.\d+"), (release["date_en"], r"\d{1,2} [A-Z][a-z]+ \d{4}"), (release["date_de"], r"\d{1,2}\. [A-ZÄÖÜ][a-zä]+ \d{4}"),
              (hiscore, r"\d+/\d+"), (read["date"], r"\d{4}-\d{2}-\d{2}"), (read["sha"], r"[0-9a-f]{7,40}"), (pins["ADOPT_COMMIT"], r"[0-9a-f]{40}"),
              (pins["TAG"], r"v\d+\.\d+\.\d+"), (pins["ARCHIVE_URL"], r"https://github\.com/[\w./-]+|\[ARCHIVE URL — filled at build\]"),
              (pins["ARCHIVE_SHA256"], r"[0-9a-f]{64}|\[SHA-256 — filled at build\]"))
    for value, shape in shapes:
        if not re.fullmatch(shape, value):
            stop(f"a figure reads {value!r}, not the shape facts.html carries")
    if not isinstance(last, int) or pins["ADOPT_COMMIT"] != commit:
        stop("the high score's last pull request or the prompt's commit is not what was read")
    act = excerpt["act"]
    if not all(isinstance(excerpt[k], int) and excerpt[k] >= 0 for k in ("waiting", "acts")) or (act is None) != (excerpt["acts"] == 0) \
            or act is not None and not (re.fullmatch(r"[A-Z][A-Z0-9]*-\d+", act["id"]) and act["line"]):
        stop(f"the board's excerpt reads {excerpt!r}, not the shape facts.html carries")


def build(args):
    git = Git(args.repo or ROOT)
    out = Path(args.out) if args.out else ROOT / OUT
    if out.exists():
        out.unlink()                                       # a failed reading leaves no file behind, so no build reads a stale one
    commit = git("rev-parse", "--verify", f"{args.commit}^{{commit}}", what=f"{args.commit} is no commit in {git.repo}").strip()
    url, slug = repo_url(git, commit)
    if args.event not in EVENTS:
        stop(f"--event {args.event!r}: pull_request, push or workflow_dispatch, as docs.yml's GITHUB_EVENT_NAME says, or none for a local build")
    release = read_release(git, commit, args.event, args.ref)
    switch = probe_switch(args.config or ROOT / "zensical.toml")
    deploy = args.event in ("push", "workflow_dispatch")
    pins = read_pins(git, commit, release, slug, switch, deploy, args.main, args.archive)
    wrecks = read_wrecks(git, commit, url)
    excerpt = read_excerpt(git, commit)
    (counted, of, last), _before = score(git, read_pulls(args.pulls, slug, os.environ.get("LANDING_FACTS_TOKEN") or None))
    epoch = os.environ.get("SOURCE_DATE_EPOCH")
    now = datetime.datetime.fromtimestamp(int(epoch), berlin()) if epoch and epoch.isdigit() else datetime.datetime.now(berlin())
    read = {"date": now.strftime("%Y-%m-%d"), "date_en": day_en(now.date()), "date_de": day_de(now.date()), "sha": commit[:7]}
    hiscore = f"{counted}/{of}"
    check_shapes(release, hiscore, last, read, pins, commit, excerpt)
    counts = wreck_counts(wrecks)
    text = facts_html(commit, release, hiscore, last, read, pins, wrecks, excerpt, counts)
    out.parent.mkdir(parents=True, exist_ok=True)
    tmp = out.with_name(out.name + ".tmp")
    with open(tmp, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)
    tmp.replace(out)
    print(f"landing facts: {release['tag']} · hi-score {hiscore} to #{last} · {len(wrecks)} wrecks, "
          f"{counts['open']} open · the board {excerpt['waiting']} waiting, {excerpt['acts']} act(s) · pins {'checked' if switch else 'stand-ins, the probe switch off'} · "
          f"{commit[:7]} on {read['date']} → {out}")


# --- RV-2750: the built landing names the release this commit reads ------------------------------------------------------------

def check_site(args):
    git = Git(args.repo or ROOT)
    commit = git("rev-parse", "--verify", f"{args.commit}^{{commit}}", what=f"{args.commit} is no commit in {git.repo}").strip()
    tag = read_release(git, commit, args.event, args.ref)["tag"]
    facts = Path(args.out) if args.out else ROOT / OUT
    if not facts.is_file():
        stop(f"no {facts}: run scripts/landing_facts.py before the build")
    text = facts.read_text(encoding="utf-8")
    m, r = re.search(r'^\{% set release = \{"tag": "([^"]*)"', text, re.M), re.search(r'^\{% set read = \{[^}]*"sha": "([0-9a-f]+)"', text, re.M)
    if not m or m.group(1) != tag or not r or not commit.startswith(r.group(1)):
        stop(f"{facts} names {m.group(1) if m else 'no release'} read at {r.group(1) if r else 'no commit'}, and {commit[:7]} reads {tag}: "
             f"run scripts/landing_facts.py again before the build")
    c, w = re.search(r"^\{% set counts = (\{.*\}) %\}$", text, re.M), re.search(r"\{% set wrecks_json %\}(.*?)\{% endset %\}", text, re.S)
    try:
        counted, held = json.loads(c.group(1)) if c else None, wreck_counts(json.loads(w.group(1))) if w else None
    except (ValueError, TypeError, KeyError):
        counted, held = "unreadable", None
    if counted is None or held is None or counted != held:
        stop(f"{facts} counts {counted}, and its wrecks_json holds {held}: the top bar's counts come from the list that draws the chart")
    site = Path(args.check)
    if not (site / "index.html").is_file():
        stop(f"no {site / 'index.html'}: the landing is checked after `zensical build`")
    for page in sorted(p for p in (site / "index.html", site / "de" / "index.html") if p.is_file()):
        html = page.read_text(encoding="utf-8")
        landing = 'id="hud-w"' in html or page.name == "index.html" and page.parent == site
        labels = re.findall(r">[Rr]elease<b>([^<]*)</b>", html)
        links = re.findall(r'href="https://github\.com/[\w.-]+/[\w.-]+/releases/tag/([^"]*)"', html)
        texts = re.findall(r'releases/tag/[^"]*"[^>]*>(v[^<]*)</a>', html)
        named = re.findall(r'aria-label="[Rr]elease (v[^ ",]*)', html)
        if landing and (not labels or not links):
            stop(f"{page} carries no release label or no link to a release: the landing names its release")
        wrong = sorted({v for v in labels + links + texts + named if v != tag})
        if wrong:
            stop(f"{page} names {', '.join(wrong)} where the release this commit reads is {tag}")
    print(f"landing release check: the top bar's label, its link and the footer's link name {tag}, as {facts.name} does")


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--commit", default="HEAD", help="the commit the site is built from (default HEAD)")
    ap.add_argument("--repo", help="the git repository to read it from (default: the one this script is in)")
    ap.add_argument("--out", help=f"the file to write (default {OUT})")
    ap.add_argument("--config", help="the zensical.toml whose probe switch counts (default: the one beside this script's folder)")
    ap.add_argument("--event", default="", help="docs.yml's GITHUB_EVENT_NAME: push and workflow_dispatch deploy; pull_request never does")
    ap.add_argument("--ref", default="", help="docs.yml's GITHUB_REF_NAME: on a tag's build, the tag pushed")
    ap.add_argument("--pulls", help="a recorded response of the closed pull requests, read instead of GitHub's API")
    ap.add_argument("--main", default="origin/main", help="the default branch's ref (default origin/main)")
    ap.add_argument("--archive", help="the release archive as a file, read instead of its address (pins check 9)")
    ap.add_argument("--check", metavar="SITE", help="after the build: the landing in SITE names the release this commit reads")
    args = ap.parse_args(argv)
    try:
        check_site(args) if args.check else build(args)
    except Stop as e:
        print(f"landing facts: {e}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
