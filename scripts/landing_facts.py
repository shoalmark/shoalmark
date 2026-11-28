"""The landing's figures and the probe prompt's pins, read from the repository at the commit the site is built from (FM-006, B1).

Run it before every site build — in docs.yml, in a local build and in the suite's own builds alike:

    python3 scripts/landing_facts.py && zensical build --clean

It writes `overrides/partials/landing/facts.html`, which is generated and never committed (`.gitignore`); the landing reads every
figure from it: `release`, `hiscore`, `scores`, `cohort_last`, `cohort_end`, `read` and `pins`. It removes the file it wrote last before
it reads anything, and writes the new one only when every reading holds: whatever it cannot read stops the build with one line
and exit 1, and a build without the file stops at the template's import, so no page is built with an empty or a stale figure.

- **release**: the release `VERSION` names, its day from that version's CHANGELOG heading, written as *9 October 2026* and
  *9. Oktober 2026*. A build that deploys — a tag's (`--event push`, its tag `--ref`) or one by hand (`--event
  workflow_dispatch`) — and a local one are built from a tagged release: the newest `v*` tag the commit holds is the one VERSION
  names. A pull request's build (`--event pull_request`), which never deploys, may run ahead of the newest tag: a release's
  own pull request carries the next VERSION; it may not fall behind it.
- **scores**, **hiscore**, **cohort_last**, **cohort_end**: FM-006's rule over the merged pull requests — the Owner's own answer branches left
  out — opened after the Owner's signed answer of 24 September 2026, 11:07 CEST (`ffa63b8`), up to `COHORT_LAST`, the last pull
  request merged under that review-file rule (FM-006, M5): one counts when a commit of its own, merge commits excluded, that adds or
  changes a file under the historical review directory is dated before the pull request was opened. The cohort is dated, not a
  series: the pull requests after it are reviewed by commit, and from `THIRD_FIRST` on they are the review-commit cohort, counted by a
  rule of its own (`score_reviewed`). `cohort_last` is the review-file cohort's last merged pull request, and `cohort_end` the Berlin
  day it was merged, in English and German. `scores` holds the review-file cohort, the review-commit cohort where it has a pull request,
  and the cohort before the rule, each {id, score, counted, of}, ranked by score, the highest first; `hiscore` is the first one's score.
  `cohort3` bounds the review-commit cohort: `THIRD_FIRST` and its last merged pull request (none where it has no pull request). The pull requests come from GitHub's API — with docs.yml's own token where `LANDING_FACTS_TOKEN` holds it, without one
  in a local build — or from a recorded response (`--pulls`); their commits come from git, so the history must be whole.
- **read**: the build's day (Europe/Berlin; `SOURCE_DATE_EPOCH` where it is set) and the commit.
- **pins**: the probe prompt's placeholders (the probe lane's pins.md). With the probe switch off — `[project.extra] probe` in
  zensical.toml — they are the commit, the release's tag and two marked stand-ins, and nothing of them is published. With it
  on they come from ADOPT's pin line, pins.md's checks 1–5 and 7 run (6, 8 and 9 too on a deploy build), and a stand-in left
  stops the build.

`--check SITE`, after `zensical build`: the landing's release label, its link and the footer's link are the release this commit
reads, and so is `facts.html`'s; the same release is checked on each landing.
"""

from __future__ import annotations

import argparse
import datetime
import fractions
import hashlib
import io
import json
import os
import re
import subprocess
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]                # the tree this build renders: its config, its template, its output
OUT = Path("overrides/partials/landing/facts.html")
RULE_COMMIT = "ffa63b8c2235e8501e6176599db11043b4cbad89"  # the Owner's signed answer of 24 September 2026, 11:07 CEST: the review rule
COHORT_LAST = 159   # FM-006, M5: the last pull request merged under the review-file rule. #159 merged on 12 October 2026, 06:39 CEST; #160 brought
                    # the Owner's signed rulings of that day (2d62fa1, 08:45 CEST), whose R2 replaced review files with review commits, to main
THIRD_FIRST = 160   # the review-commit cohort's first pull request: the one that brought review commits to main
HISTORICAL_REVIEWS = "work-tracker/evidence/reviews/"
ROWS = ("files", "commits", "before")   # the high scores' cohorts: review files to COHORT_LAST, review commits from THIRD_FIRST, before the review rule
STAND_IN = {"ARCHIVE_URL": "[ARCHIVE URL — filled at build]", "ARCHIVE_SHA256": "[SHA-256 — filled at build]"}
MONTHS_EN = ("January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December")
MONTHS_DE = ("Januar", "Februar", "März", "April", "Mai", "Juni", "Juli", "August", "September", "Oktober", "November", "Dezember")

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
    try:
        import zoneinfo
        return zoneinfo.ZoneInfo("Europe/Berlin")
    except Exception:                                     # no zoneinfo module, or no tzdata on this machine
        stop("no time zone database for Europe/Berlin here: the filing days and the build's day are Berlin days")


def day_en(d):
    return f"{d.day} {MONTHS_EN[d.month - 1]} {d.year}"


def day_de(d):
    return f"{d.day}. {MONTHS_DE[d.month - 1]} {d.year}"


def repo_url(git, commit):
    text = git("show", f"{commit}:zensical.toml", what=f"no zensical.toml at {commit[:7]}")
    m = re.search(r'^repo_url\s*=\s*"(https://github\.com/([\w.-]+/[\w.-]+))"\s*$', text, re.M)
    if not m:
        stop("zensical.toml names no repo_url on GitHub: the pull requests are read from it")
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
    for line in git("log", "--no-merges", "--no-renames", "--format=%x00%H %ct", "--name-status", "--stdin", "--", HISTORICAL_REVIEWS, stdin=heads).splitlines():
        if line.startswith("\x00"):
            sha, at = line[1:].split()
            continue
        if line.strip() and line[0] in "AMT":                # a file under the reviews folder added or changed (a deletion is neither)
            touched[sha] = int(at)
    counts = lambda p: any(touched.get(c, float("inf")) < utc(p["created_at"]) for c in own[p["number"]])
    after = [p for p in merged if utc(p["created_at"]) >= rule_at and p["number"] <= COHORT_LAST]
    before = [p for p in merged if utc(p["created_at"]) < rule_at]
    if not after:
        stop("no merged pull request was opened after the review rule: there is no high score to read")
    return (sum(map(counts, after)), len(after), after[-1]["number"]), (sum(map(counts, before)), len(before))


def score_reviewed(git, pulls):
    """The review-commit cohort, by a rule of its own: (counted, of, its first pull request, its last), or None where no merged pull request is
    numbered THIRD_FIRST or later. A merged pull request from THIRD_FIRST on, the Owner's answer branches left out and every other pull request
    kept, counts when one of its own commits (those its head holds and its base does not) carries exactly one `Reviewed:` trailer, an empty one
    counted with the rest, that trailer names one of those commits, and the commit carrying it is dated (its committer date) before the pull request
    was opened."""
    merged = sorted((p for p in map(trim, pulls) if p["merged_at"] and not p["head"]["ref"].startswith("answer/") and p["number"] >= THIRD_FIRST),
                    key=lambda p: p["number"])
    if not merged:
        return None
    ends = sorted({p[side]["sha"] for p in merged for side in ("head", "base")})
    held = {ln.split()[0] for ln in git("cat-file", "--batch-check", stdin="\n".join(ends) + "\n").splitlines() if not ln.endswith(" missing")}
    for p in merged:
        for side in ("head", "base"):
            if p[side]["sha"] not in held:
                stop(f"this history does not hold pull request #{p['number']}'s {side} {p[side]['sha'][:7]}: build from a full clone (fetch-depth: 0)")
    parents = {}
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
    own = {p["number"]: ancestors(p["head"]["sha"]) - ancestors(p["base"]["sha"]) for p in merged}
    every = sorted(set().union(*own.values()))
    dated, named = {}, {}
    if every:
        out = git("log", "--no-walk=unsorted", "--stdin", "--format=%x00%H %ct%x01%(trailers:key=Reviewed,valueonly,unfold)%x01", stdin="\n".join(every) + "\n")
        for chunk in out.split("\x00")[1:]:
            first, values, _ = chunk.split("\x01")
            sha, at = first.split()
            dated[sha], named[sha] = int(at), [v.strip() for v in values.split("\n")[:-1]]

    def counts(p):
        mine, opened = own[p["number"]], utc(p["created_at"])
        return any(len(named[c]) == 1 and re.fullmatch(r"[0-9a-f]{7,40}", named[c][0]) and sum(x.startswith(named[c][0]) for x in mine) == 1
                   and dated[c] < opened for c in mine)
    return sum(map(counts, merged)), len(merged), merged[0]["number"], merged[-1]["number"]


def ranked(rows):
    """The high scores' rows, each {"id", "score", "counted", "of"}, the highest score first; rows of the same score keep the order given, and a row
    with no pull request is left out."""
    return sorted((r for r in rows if r["of"]), key=lambda r: -fractions.Fraction(r["counted"], r["of"]))


def cohort_end(pulls, last):
    """The Berlin day the cohort's last pull request was merged, as {"en": ..., "de": ...} (FM-006, M5)."""
    merged = [p["merged_at"] for p in map(trim, pulls) if p["number"] == last and p["merged_at"]]
    if len(merged) != 1:
        stop(f"pull request #{last}, the high score's last, reads as merged {len(merged)} times")
    day = datetime.datetime.fromtimestamp(utc(merged[0]), berlin()).date()
    return {"en": day_en(day), "de": day_de(day)}


def read_pulls(recorded, slug, token):
    if recorded is None:
        return fetch_pulls(slug, token)
    try:
        data = json.loads(Path(recorded).read_text(encoding="utf-8"))
    except (OSError, ValueError) as e:
        stop(f"the recorded pull requests {recorded} cannot be read: {e}")
    return data["pulls"] if isinstance(data, dict) else data


# --- the probe prompt's pins --------------------------------------------------------------------------------------------------------------

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


def fetch_raw(url):
    """The bytes `url` serves, or None where it serves none."""
    try:
        with urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "shoalmark-landing-facts"}), timeout=60) as r:
            return r.read()
    except (OSError, urllib.error.URLError):
        return None


def pause(seconds):
    time.sleep(seconds)


def read_pins(git, commit, release, slug, switch, deploy, main, archive, building=""):
    """The prompt's four pins. Off: the commit, the release's tag and two marked stand-ins. On: ADOPT's pin line, checked.
    `building` is the tag a tag's build is for, empty on any other build."""
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
    if url != f"https://github.com/{slug}/releases/download/{tag}/shoalmark-{tag[1:]}.zip":
        stop(f"pins check 2: {url} is not {tag}'s archive, https://github.com/{slug}/releases/download/{tag}/shoalmark-{tag[1:]}.zip")
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
    if building and building != tag:
        stop(f"pins check 5: ADOPT names {tag}, and this is the build of the tag {building}")
    if deploy:
        if git.raw("merge-base", "--is-ancestor", commit, main)[0]:
            stop(f"pins check 6: {commit} is not on main")
        for f in NOTES:
            raw, want = f"https://raw.githubusercontent.com/{slug}/{commit}/{f}", git.raw("show", f"{commit}:{f}")[1]
            if fetch_raw(raw) != want:
                pause(1)
                if fetch_raw(raw) != want:
                    stop(f"pins check 8: {raw} does not serve {f} as git holds it at {commit[:7]}, asked twice, a second apart")
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


def facts_html(commit, release, hiscore, last, end, read, pins, scores=(), cohort3=None):
    obj = lambda d: "{" + ", ".join(f"{json.dumps(k)}: {lit(v)}" for k, v in d.items()) + "}"
    return (f"{{#- Generated by scripts/landing_facts.py from {commit}; never committed, never edited by hand. The landing reads\n"
            f"    every figure from here (FM-006, B1). -#}}\n"
            f"{{% set release = {obj(release)} %}}\n"
            f"{{% set hiscore = {lit(hiscore)} %}}\n"
            f"{{% set scores = [{', '.join(obj(r) for r in scores)}] %}}\n"
            f"{{% set cohort3 = {obj(cohort3) if cohort3 else 'none'} %}}\n"
            f"{{% set cohort_last = {lit(last)} %}}\n"
            f"{{% set cohort_end = {obj(end)} %}}\n"
            f"{{% set pins = {obj(pins)} %}}\n"
            f"{{% set read = {obj(read)} %}}\n")


def check_shapes(release, hiscore, last, end, read, pins, commit, scores, cohort3):
    shapes = ((release["tag"], r"v\d+\.\d+\.\d+"), (release["date_en"], r"\d{1,2} [A-Z][a-z]+ \d{4}"), (release["date_de"], r"\d{1,2}\. [A-ZÄÖÜ][a-zä]+ \d{4}"),
              (end["en"], r"\d{1,2} [A-Z][a-z]+ \d{4}"), (end["de"], r"\d{1,2}\. [A-ZÄÖÜ][a-zä]+ \d{4}"),
              (hiscore, r"\d+/\d+"), (read["date"], r"\d{4}-\d{2}-\d{2}"), (read["sha"], r"[0-9a-f]{7,40}"), (pins["ADOPT_COMMIT"], r"[0-9a-f]{40}"),
              (pins["TAG"], r"v\d+\.\d+\.\d+"), (pins["ARCHIVE_URL"], r"https://github\.com/[\w./-]+|\[ARCHIVE URL — filled at build\]"),
              (pins["ARCHIVE_SHA256"], r"[0-9a-f]{64}|\[SHA-256 — filled at build\]"))
    for value, shape in shapes:
        if not re.fullmatch(shape, value):
            stop(f"a figure reads {value!r}, not the shape facts.html carries")
    if not isinstance(last, int) or last > COHORT_LAST or pins["ADOPT_COMMIT"] != commit:
        stop("the high score's last pull request or the prompt's commit is not what was read")
    rows_ok = all(set(r) == {"id", "score", "counted", "of"} and r["id"] in ROWS and isinstance(r["counted"], int) and isinstance(r["of"], int)
                  and 0 <= r["counted"] <= r["of"] and r["score"] == f"{r['counted']}/{r['of']}" for r in scores)
    if not scores or not rows_ok or len({r["id"] for r in scores}) != len(scores) or scores != ranked(scores) or hiscore != scores[0]["score"]:
        stop(f"the high scores read {scores!r}, not the shape facts.html carries: each cohort once, ranked, the hi-score the first row's")
    if (cohort3 is None) != ("commits" not in {r["id"] for r in scores}) or cohort3 is not None and not (
            set(cohort3) == {"first", "last"} and cohort3["first"] == THIRD_FIRST and isinstance(cohort3["last"], int) and cohort3["last"] >= THIRD_FIRST):
        stop(f"the review-commit cohort's bounds read {cohort3!r}, not the shape facts.html carries")


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
    pins = read_pins(git, commit, release, slug, switch, deploy, args.main, args.archive, args.ref if args.event == "push" else "")
    pulls = read_pulls(args.pulls, slug, os.environ.get("LANDING_FACTS_TOKEN") or None)
    (counted, of, last), _before = score(git, pulls)
    end = cohort_end(pulls, last)
    epoch = os.environ.get("SOURCE_DATE_EPOCH")
    now = datetime.datetime.fromtimestamp(int(epoch), berlin()) if epoch and epoch.isdigit() else datetime.datetime.now(berlin())
    read = {"date": now.strftime("%Y-%m-%d"), "date_en": day_en(now.date()), "date_de": day_de(now.date()), "sha": commit[:7]}
    third = score_reviewed(git, pulls)
    rows = [("files", counted, of), *([("commits", third[0], third[1])] if third else []), ("before", *_before)]
    scores = ranked([{"id": i, "score": f"{c}/{o}", "counted": c, "of": o} for i, c, o in rows])
    hiscore = scores[0]["score"]
    cohort3 = {"first": THIRD_FIRST, "last": third[3]} if third else None
    check_shapes(release, hiscore, last, end, read, pins, commit, scores, cohort3)
    text = facts_html(commit, release, hiscore, last, end, read, pins, scores, cohort3)
    out.parent.mkdir(parents=True, exist_ok=True)
    tmp = out.with_name(out.name + ".tmp")
    with open(tmp, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)
    tmp.replace(out)
    print(f"landing facts: {release['tag']} · hi-score {hiscore}, pull requests to #{last}, merged by {end['en']} · "
          f"{', '.join(r['id'] + ' ' + r['score'] for r in scores)} · pins {'checked' if switch else 'stand-ins, the probe switch off'} · "
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
    site = Path(args.check)
    if not (site / "index.html").is_file():
        stop(f"no {site / 'index.html'}: the landing is checked after `zensical build`")
    for page in sorted(p for p in (site / "index.html", site / "de" / "index.html") if p.is_file()):
        html = page.read_text(encoding="utf-8")
        landing = 'class="hud"' in html or page.name == "index.html" and page.parent == site
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
