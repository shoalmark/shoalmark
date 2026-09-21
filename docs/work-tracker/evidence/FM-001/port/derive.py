#!/usr/bin/env python3
"""The origin's release axis as a fathom-mark deriver (R&D spike). Everything here is the origin's business and the
core knows none of it: the release-target registry, the tag lookups, the submodule refusal, the three release lints."""
import json, os, pathlib, re, subprocess, sys

ask = json.load(sys.stdin)
ROOT = pathlib.Path(ask["root"])
sys.path.insert(0, str(ROOT / "scripts"))
from targets import TARGETS, release_tag, resolve  # noqa: E402

EXIT_SUBMODULES = 5
_WHERE = "(?:" + "|".join(sorted(TARGETS, key=len, reverse=True)) + r"|\?)"
_VER = r"\d+\.\d+\.\d+(?:\.\d+)?(?:-[0-9A-Za-z.]+)?"
EXACT = re.compile(r"^\d+\.\d+\.\d+(?:-[0-9A-Za-z.]+)?$")
WORDS = "A release target is one of " + " · ".join(TARGETS)
ENV = {k: v for k, v in os.environ.items() if k not in ("GIT_DIR", "GIT_WORK_TREE", "GIT_INDEX_FILE", "GIT_PREFIX")}
_tags = {}


def dash(v):
    v = (v or "").strip()
    return v if v and v not in {"-", "--", "—", "n/a", "none"} else "—"


def pairs(value):
    got = [e.split() for e in (value or "").split(",")]
    return [(p[0], p[1]) for p in got if len(p) == 2]


def tags(sub):
    if sub not in _tags:
        try:
            out = subprocess.run(["git", "-C", str(ROOT / sub), "tag", "--list"], capture_output=True, text=True, timeout=15, check=True, env=ENV).stdout
            _tags[sub] = {t.strip() for t in out.splitlines() if t.strip()}
        except Exception:
            _tags[sub] = set()
    return _tags[sub]


def live_of(name, version):
    target = resolve(name)
    tag = release_tag(target, version) if target else None
    if tag is None or not tags(target.submodule):
        return "—"
    return "live ✓" if tag in tags(target.submodule) else "on main ⏳"


def live(releases):
    states = [live_of(n, v) for n, v in releases]
    if len(states) <= 1:
        return states[0] if states else "—"
    n = sum(x == "live ✓" for x in states)
    return "live ✓" if n == len(states) else "—" if all(x == "—" for x in states) else f"on main ⏳ {n}/{len(states)} live"


trackers = ask["trackers"]
# the refusal: a submodule the Live axis reads is not checked out — every such cell would silently become `—`
at_risk = {}
for t in trackers:
    for name, _v in pairs(t["fm"].get("version")):
        if resolve(name) is not None:
            at_risk.setdefault(resolve(name).submodule, []).append(t["id"])
absent = []
for sub, ids in sorted(at_risk.items()):
    try:
        top = subprocess.run(["git", "-C", str(ROOT / sub), "rev-parse", "--show-toplevel"], capture_output=True, text=True, timeout=15, check=True, env=ENV).stdout.strip()
        ok = bool(top) and pathlib.Path(top).resolve() == (ROOT / sub).resolve()
    except Exception:
        ok = False
    if not ok:
        absent.append((sub, ids))
if absent and not os.environ.get("ALLOW_MISSING_SUBMODULES"):
    print("refusing to run — the `Live` axis derives from submodules that are not checked out:", file=sys.stderr)
    for sub, ids in absent:
        print(f"  {sub}/ — {len(ids)} tracker(s) depend on it: {', '.join(ids[:6])}", file=sys.stderr)
    print("Fix:  git submodule update --init", file=sys.stderr)
    sys.exit(EXIT_SUBMODULES)

out, problems = {}, []
for t in trackers:
    fm, tid = t["fm"], t["id"]
    releases, targets = pairs(fm.get("version")), pairs(fm.get("target"))
    version, target, suite = dash(fm.get("version")), dash(fm.get("target")), dash(fm.get("suite"))
    surface = " · ".join(dict.fromkeys(n for n, _v in (releases or targets) if n != "?")) or "—"
    out[tid] = {"Suite": suite, "Target": target, "Ver": version, "Live": live(releases), "Surface": surface,
                "Release": [version, version + (" ✓" if live(releases).startswith("live") else "")] if version != "—" else [target, "→ " + target] if target != "—" else "—"}
    if any(n == "?" for n, _v in targets):
        out[tid]["_needs"] = ["target"]           # the plan never named its release target — filled when the tracker is pulled
    if version != "—" and t["status"] not in ("Shipped", "Closed"):
        problems.append(f"{tid}: version: {version} on a {t['status']} tracker — `version:` is ship-fact-only; use `target:` for intent.")
    if suite != "—" and not (ROOT / "docs" / "features" / suite).is_dir():
        problems.append(f"{tid}: suite: {suite} has no docs/features/{suite}/ dir.")
    for name, ver in targets if t["status"] not in ("Shipped", "Closed") else []:
        if not EXACT.match(ver):
            continue
        declared = resolve(name)
        cut = sorted({f"{g.submodule}:{release_tag(g, ver)}" for g in ([declared] if declared else TARGETS.values())
                      if release_tag(g, ver) and release_tag(g, ver) in tags(g.submodule)})
        if cut:
            problems.append(f"{tid}: target: {name} {ver} is ALREADY CUT ({', '.join(cut)}) but the tracker is {t['status']} — that release shipped without it.")

out["_keys"] = {
    "suite": {"says": "the product area it belongs to — a docs/features/<suite>/ directory, or —", "who": "the filing seat"},
    "target": {"shape": rf"{_WHERE} (?:{_VER}|\d+\.\d+(?:\.x)?|\?)(?:\s*,\s*{_WHERE} (?:{_VER}|\d+\.\d+(?:\.x)?|\?))*", "who": "the filing seat",
               "says": "the PLAN — `<release target> <version>`, where it is meant to land. " + WORDS},
    "version": {"shape": rf"{_WHERE} {_VER}(?:\s*,\s*{_WHERE} {_VER})*", "who": "the ship commit",
                "says": "the FACT — `<release target> <version>` it shipped in, on a `Shipped` tracker only. " + WORDS},
}
# other generated files — the deriver has no side effects: it says what the file should hold, the core writes it
BEGIN, END = "<!-- BEGIN GENERATED: suite-roster (FEAT-086 S4) — do not hand-edit -->", "<!-- END GENERATED: suite-roster -->"
num = lambda i: (i.split("-")[0], int(i.split("-")[1]))
files = {}
for suite in sorted({out[t["id"]]["Suite"] for t in trackers} - {"—"}):
    readme = ROOT / "docs" / "features" / suite / "README.md"
    if not readme.exists():
        continue
    rows = sorted((t for t in trackers if out[t["id"]]["Suite"] == suite), key=lambda t: num(t["id"]))
    block = [BEGIN, "", f"## Trackers owned by this suite ({len(rows)})", "",
             "> **GENERATED — do not hand-edit.** Derived from `suite: " f"{suite}` in each tracker's frontmatter; run",
             "> `python3 scripts/gen-tracker-index.py`. **Ownership only** — a tracker names exactly one",
             "> suite (FEAT-086 LD1/LD4). Work that *relates* to this suite but is owned elsewhere belongs",
             "> in a hand-written **Related work** list, which this block deliberately does not replace",
             "> (LD4 as amended by P43). `Status` and `Live` are derived, so they cannot go stale — never",
             "> restate them by hand.", "", "| Tracker | Status | Live |", "|---|---|---|"]
    block += [f"| [{t['id']}](../../work-tracker/{t['file']}) | {t['status']} | {out[t['id']]['Live']} |" for t in rows] or ["| *(none yet)* | — | — |"]
    block = "\n".join(block + ["", END])
    text = readme.read_text(encoding="utf-8")
    rx = re.compile(re.escape(BEGIN) + r".*?" + re.escape(END), re.S)
    files[str(readme.relative_to(ROOT))] = rx.sub(lambda _: block, text, count=1) if rx.search(text) else text.rstrip("\n") + "\n\n" + block + "\n"
# the work-packages roll-up — what is each release FOR? It leaves INDEX.md for a file of its own.
open_rows = [t for t in trackers if t["status"] in ("Proposed", "In Progress", "Parked", "Reserved")]
by_target = {}
for t in open_rows:
    by_target.setdefault(out[t["id"]]["Target"], []).append(t)
file_of = {t["id"]: t["file"] for t in trackers}
pk = ["# Work packages — open work by target\n",
      "> **GENERATED — do not hand-edit.** Derived from each tracker's `target:` (intent) × `suite:` (the",
      "> `docs/features/<suite>/` product area). `target:` is **not** a deploy claim — see the `Ver`/`Live` columns",
      "> of [INDEX.md](INDEX.md) for that. Shipped work is omitted.\n",
      "> **Wholly-targeted work only.** `target:` is per-tracker, so a tracker whose first slices land in a cut and",
      "> whose later slices land after it stays fuzzy (`0.15.x`) and will **not** appear under the exact release.\n",
      "| Target | Suite | Open trackers |", "|--------|-------|---------------|"]
for target in sorted(by_target, key=lambda k: (k == "—", k)):
    by_suite = {}
    for t in by_target[target]:
        by_suite.setdefault(out[t["id"]]["Suite"], []).append(t["id"])
    for suite in sorted(by_suite, key=lambda k: (k == "—", k)):
        pk.append(f"| {target} | {suite} | " + " · ".join(f"[{i}]({file_of[i]})" for i in sorted(by_suite[suite])) + " |")
files["docs/work-tracker/PACKAGES.md"] = "\n".join(pk) + "\n"
out["_files"] = files
live_undet = sorted(t["id"] for t in trackers if t["status"] == "Shipped" and out[t["id"]]["Live"] == "—")
no_readme = sorted({out[t["id"]]["Suite"] for t in trackers} - {"—"} - {p.split("/")[2] for p in files if p.startswith("docs/features/")})
out["_notes"] = [
    "**Live** = deploy truth, derived from a release tag in the release target `version:` names — `live ✓` deployed ·\n`on main ⏳` merged but the release isn't cut · `—` undetermined (no `version:`, release target `?`, or tags unfetched).",
    "**Suite** = the product area, `docs/features/<suite>/`. **Target** = the release it *intends* to land in — intent,\nnot fact: `Ver` is set only at ship. Open work by target: [PACKAGES.md](PACKAGES.md).",
] + ([f"ℹ️ {len(live_undet)} shipped tracker(s) name no release in `version:`, so `Live` shows `—`."] if live_undet else []) \
  + ([f"ℹ️ {len(no_readme)} suite(s) own trackers but have no `docs/features/<suite>/README.md`, so no roster is generated for them: {', '.join(no_readme)}."] if no_readme else [])
out["_index"] = ["Suite", "Target", "Ver", "Live"]      # what an agent reads in INDEX.md — the origin's four columns
out["_board"] = ["Surface", "Release"]                  # what the Owner reads on the board — the origin's two
out["_problems"] = problems
json.dump(out, sys.stdout, ensure_ascii=False)
