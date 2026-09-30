"""The core's behaviour, pinned — the checks the tracker carried in the repository it was cut from, moved here with it.

Run: `python3 test_core.py`. Every check runs against a small synthetic corpus built in a throwaway git repository;
nothing reads a real one. The release axis these checks once shared a file with lives with its deriver, not here.
main() is called in-process with an argv list, so a non-zero exit is observable without a subprocess.
"""

import json
import importlib.util
import io
import os
import re
import subprocess
import sys
import tempfile
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path
from unittest.mock import patch

# The SUITE reads and writes UTF-8 whatever the machine's locale is (a Windows runner's is cp1252). The TOOL never
# relies on this: it names its encoding on every read and write — a check below holds it to that.
for _s in (sys.stdout, sys.stderr):
    _s.reconfigure(encoding="utf-8", errors="replace")
_rt, _wt = Path.read_text, Path.write_text
Path.read_text = lambda self, encoding="utf-8", errors=None: _rt(self, encoding=encoding, errors=errors)
Path.write_text = lambda self, data, encoding="utf-8", errors=None: _wt(self, data, encoding=encoding, errors=errors)


HERE = Path(__file__).resolve().parent
_spec = importlib.util.spec_from_file_location("gti", HERE / "shoalmark.py")
gti = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(gti)

# --- the synthetic corpus: a story with a chapter, open and done work of every status, a blocker, a tag -------------
_TMP = tempfile.TemporaryDirectory()
ROOT = Path(_TMP.name).resolve()
_WT = ROOT / "docs" / "work-tracker"
_WT.mkdir(parents=True)


def _file(tid, status, extra="", title="a tracker", body="## What is true now\n\n**One thing is left.**\n\n## Done when\n\nit is.\n"):
    (_WT / f"{tid}-{title.replace(' ', '-')}.md").write_text(
        f'---\nid: {tid}\nstatus: {status}\n{extra}hook: "the hook of {tid} — {title}"\n---\n\n# {tid} — {title}\n\n{body}', encoding="utf-8")


_file("FEAT-001", "Shipped", title="the first feature")
_file("FEAT-002", "In Progress", 'intent: "for — a · so that — b · never — c"\ntriaged: 2026-01-05\ntier: P1\nrank: 1\nnext: build\nkind-of-problem: complicated\n', title="a story")
_file("FEAT-003", "In Progress", "epic: FEAT-002\ntriaged: 2026-01-05\ntier: P2\n", title="a chapter",
      body="## What is true now\n\n**Left: one run.** See [the story](FEAT-002-a-story.md).\n\n## Done when\n\nit ran.\n")
_file("FEAT-004", "Proposed", "tags: research\n", title="a question")
_file("BUG-001", "Closed", title="an old bug")
_file("BUG-002", "Parked", "triaged: 2026-01-05\ntier: P3\nblocked-by: FEAT-002, Owner — the ruling\n", title="a parked bug")
_file("BUG-003", "Proposed", title="a fresh bug")
_file("ALIGN-001", "Shipped", title="parity")
(_WT / "TRIAGE.md").write_text("# Triage\n\n## The intent\n\n- **for** — consolidation\n- **never** — a Jira clone\n\n## The current path\n\n"
                               "1. [FEAT-002](FEAT-002-a-story.md) to its end.\n\n## Passes\n\nNewest first.\n\n*None yet.*\n", encoding="utf-8")
(ROOT / "shoalmark.toml").write_text('name = "synthetic"\n[kinds]\nFEAT = "Features"\nBUG = "Bugs"\nALIGN = "Alignment"\n'
                                       '[considered_from]\nFEAT = 189\nBUG = 334\nALIGN = 1000\n', encoding="utf-8")
_GIT_ENV = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
_GIT_ENV.update(GIT_AUTHOR_NAME="t", GIT_AUTHOR_EMAIL="t@t", GIT_COMMITTER_NAME="t", GIT_COMMITTER_EMAIL="t@t")
for _cmd in (["init", "-q"], ["add", "-A"], ["-c", "commit.gpgsign=false", "-c", "core.hooksPath=/dev/null", "commit", "-qm", "the synthetic corpus"]):
    subprocess.run(["git", "-C", str(ROOT), *_cmd], check=True, capture_output=True, env=_GIT_ENV)
gti.configure(ROOT)
_main = gti.main
gti.main = lambda argv=None: _main(["--root", str(ROOT), *(argv or [])])
gti.main([])

FAILS = []


def check(label, cond):
    print(f"  {'ok  ' if cond else 'FAIL'}  {label}")
    if not cond:
        FAILS.append(label)


def run(argv):
    """Call main(argv), swallowing output. Returns (exit_code, stdout, stderr)."""
    out, err = io.StringIO(), io.StringIO()
    try:
        with redirect_stdout(out), redirect_stderr(err):
            code = gti.main(argv)
    except SystemExit as e:  # argparse exits on a bad flag
        code = e.code
    return code, out.getvalue(), err.getvalue()


print("--check is REAL — an unknown flag must not be silently ignored")
# The original defect: no argv parsing at all, so `--check` fell on the floor and
# the script did a normal write and exited 0. Any argv handling at all fixes the
# silent-ignore; argparse also rejects typos instead of running the wrong mode.
code, _, _ = run(["--nonsense-flag"])
check("bogus flag -> non-zero (argparse rejects, never ignores)", code not in (0, None))
check("--check is a declared flag", gti.parse_args(["--check"]).check is True)
check("no flag -> write mode", gti.parse_args([]).check is False)

print("\nlinked-worktree hooks cannot redirect submodule tag discovery")
_git_env = os.environ.copy()
try:
    os.environ["GIT_DIR"] = "/synthetic/parent.git"
    os.environ["GIT_WORK_TREE"] = "/synthetic/parent-worktree"
    os.environ["GIT_INDEX_FILE"] = "/synthetic/index"
    os.environ["GIT_PREFIX"] = "synthetic/"
    nested = gti.nested_git_env()
    check("nested Git drops GIT_DIR", "GIT_DIR" not in nested)
    check("nested Git drops GIT_WORK_TREE", "GIT_WORK_TREE" not in nested)
    check("nested Git drops GIT_INDEX_FILE", "GIT_INDEX_FILE" not in nested)
    check("nested Git drops GIT_PREFIX", "GIT_PREFIX" not in nested)
finally:
    os.environ.clear()
    os.environ.update(_git_env)

print("\n--check is READ-ONLY — the gate must not mutate what it measures")
before = gti.OUT.read_text(encoding="utf-8")
code, _, _ = run(["--check"])
after = gti.OUT.read_text(encoding="utf-8")
check("--check writes nothing", before == after)

print("\nexit codes are distinct and ordered — LINT outranks DRIFT")
check("OK is 0", gti.EXIT_OK == 0)
check("DRIFT and LINT are both non-zero", gti.EXIT_DRIFT != 0 and gti.EXIT_LINT != 0)
check("DRIFT != LINT (CI can tell them apart)", gti.EXIT_DRIFT != gti.EXIT_LINT)

print("\nthe ledger is clean today -> the gate is GREEN (a gate must pass on green)")
# If this fails, the repo has a real ledger-integrity violation — fix the tracker,
# not this test. That is the gate doing its job.
code, _, err = run(["--check"])
check(f"--check on a clean tree -> {gti.EXIT_OK}", code == gti.EXIT_OK)
check("no lint lines on a clean tree", "lint:" not in err)

print("\nthe date stamp is NOT drift — the false-positive that would kill the gate")
# The header stamps today's date. A byte-compare would call the INDEX stale every
# day after it was written, and a gate that fires on green code gets ignored.
stamped = "> Generated 2026-07-15 · 165 trackers (x)\n| row |\n"
later = "> Generated 2099-01-01 · 165 trackers (x)\n| row |\n"
check(
    "same content, different date -> NOT drift",
    gti.drift_normalize(stamped) == gti.drift_normalize(later),
)
changed = "> Generated 2026-07-15 · 165 trackers (x)\n| DIFFERENT |\n"
check(
    "same date, different content -> IS drift",
    gti.drift_normalize(stamped) != gti.drift_normalize(changed),
)
check(
    "normalize only touches the Generated line",
    gti.drift_normalize(stamped).count("| row |") == 1,
)

print("\n--check DETECTS real drift (the whole point of the mode)")
_saved = gti.OUT.read_text(encoding="utf-8")
try:
    gti.OUT.write_text(_saved + "\n<!-- hand-edited drift -->\n", encoding="utf-8")
    code, _, err = run(["--check"])
    check(f"stale INDEX -> exit {gti.EXIT_DRIFT}", code == gti.EXIT_DRIFT)
    check("stale INDEX says how to fix it", gti.CMD in err)
finally:
    gti.OUT.write_text(_saved, encoding="utf-8")
code, _, _ = run(["--check"])
check("restored -> green again", code == gti.EXIT_OK)

print("\na lint violation FAILS — in BOTH modes (this is P42 itself)")
# lint() is pure over the tracker dicts, so a synthetic violating tracker exercises
# the gate without touching the real ledger. LD2: `version:` is ship-fact-only.
# `links` is part of the dict contract extract() builds — kept explicit here rather
# than defaulted inside lint(), so a missing key stays a loud KeyError instead of a
# silently-skipped check (which is P42's whole disease).
violating = {"id": "FEAT-999", "kind": "FEAT", "status": "Proposed", "hook": "synthetic", "links": [], "tags": ["no-such-tag"]}
problems = gti.lint([violating])
check("a tag outside the vocabulary is one violation", len(problems) == 1)
check("the violation names the tracker", "FEAT-999" in problems[0])

_real_lint = gti.lint
try:
    gti.lint = lambda trackers, **kw: ["FEAT-999: synthetic violation"]
    code, _, err = run(["--check"])
    check(f"violation in --check -> exit {gti.EXIT_LINT}", code == gti.EXIT_LINT)
    code, _, err = run([])
    check(f"violation in WRITE mode -> exit {gti.EXIT_LINT}", code == gti.EXIT_LINT)
    check("write mode surfaces the violation", "synthetic violation" in err)
    check("and says regenerating won't clear it", "regenerating will not" in err)
finally:
    gti.lint = _real_lint

# Write mode ran with a mocked lint above, so the INDEX now carries a ❌ banner for
# a tracker that does not exist. Regenerate to put the real ledger back.
run([])
check("real INDEX restored after the mocked run", "FEAT-999" not in gti.OUT.read_text(encoding="utf-8"))

print("\nthe dangling-link lint, and it must NAME the fix")
# 18 of the 19 real cases were rename-rot: the id was right, only the slug moved.
# A lint that reports the break without the replacement it can trivially compute is
# a lint people route around.
def _t(links, tid="FEAT-999"):
    return {"id": tid, "kind": "FEAT", "status": "Proposed", "hook": "synthetic", "links": links}

real = sorted(p.name for p in gti.TRACKER_DIR.glob("FEAT-002-*.md"))
check("fixture: exactly one FEAT-002 on disk", len(real) == 1)

p = gti.lint([_t(["FEAT-002-an-older-slug.md"])])
check("rename-rot -> 1 problem", len(p) == 1)
check("names the broken link", "FEAT-002-an-older-slug.md" in p[0])
check("NAMES THE FIX ('did you mean')", "did you mean" in p[0] and real[0] in p[0])

p = gti.lint([_t(["FEAT-404-does-not-exist-at-all.md"])])
check("phantom id -> 1 problem", len(p) == 1)
check(
    "phantom says NO tracker exists (BUG-078 class, needs a human not a slug swap)",
    "NO tracker with id FEAT-404" in p[0],
)

p = gti.lint([_t([real[0]])])
check("a link that RESOLVES is not a problem", len(p) == 0)

# The regression that matters most: the lint must not fire on the live corpus.
# If this fails, the repo has real link rot — fix the trackers, not this test.
trackers = [
    gti.extract(x) for x in sorted(gti.TRACKER_DIR.glob("*.md")) if gti.KIND_RE.match(x.name)
]
dangling = [x for x in gti.lint(trackers) if "dangling link" in x]
check(f"live corpus has ZERO dangling links (got {len(dangling)})", not dangling)
check("extract() populates `links` (the dict contract)", "links" in trackers[0])

print("\na duplicate identity refuses in BOTH modes, writing NOTHING")
_dupe_a = gti.TRACKER_DIR / "BUG-9998-bug204-synthetic-duplicate-a.md"
_dupe_b = gti.TRACKER_DIR / "BUG-9998-bug204-synthetic-duplicate-b.md"
_index_before = gti.OUT.read_text(encoding="utf-8")
try:
    _dupe_body = "---\nid: BUG-9998\nstatus: Proposed\nhook: synthetic BUG-204 fixture\n---\n\n# BUG-9998 — synthetic\n"
    _dupe_a.write_text(_dupe_body, encoding="utf-8")
    _dupe_b.write_text(_dupe_body, encoding="utf-8")
    code, _, err = run(["--check"])
    check(f"duplicate id -> exit {gti.EXIT_LINT} under --check", code == gti.EXIT_LINT)
    check("both colliding paths are named", _dupe_a.name in err and _dupe_b.name in err)
    check("the diagnostic forbids dedup/last-wins", "never dedup" in err or "never lets the last file win" in err)
    code, _, err = run([])
    check(f"duplicate id -> exit {gti.EXIT_LINT} in WRITE mode too", code == gti.EXIT_LINT)
    check("WRITE mode wrote NOTHING on identity failure", gti.OUT.read_text(encoding="utf-8") == _index_before)
finally:
    _dupe_a.unlink(missing_ok=True)
    _dupe_b.unlink(missing_ok=True)
check("synthetic duplicates removed", not _dupe_a.exists() and not _dupe_b.exists())

print("\nfilename/frontmatter/H1 drift prints ALL THREE identities")
_drift = gti.TRACKER_DIR / "FEAT-9997-bug204-synthetic-identity-drift.md"
try:
    _drift.write_text(
        "---\nid: FEAT-9996\nstatus: Proposed\nhook: synthetic BUG-204 fixture\n---\n\n# FEAT-9995 — synthetic\n",
        encoding="utf-8",
    )
    code, _, err = run(["--check"])
    check(f"identity drift -> exit {gti.EXIT_LINT}", code == gti.EXIT_LINT)
    check(
        "filename, frontmatter, and H1 identities all appear in the diagnostic",
        "FEAT-9997" in err and "FEAT-9996" in err and "FEAT-9995" in err,
    )
finally:
    _drift.unlink(missing_ok=True)

print("\na struck-through H1 id still counts (the BUG-209 falsified-filing form)")
_struck = gti.TRACKER_DIR / "BUG-9994-bug204-synthetic-struck-h1.md"
try:
    _struck.write_text(
        "---\nid: BUG-9994\nstatus: Closed\nhook: synthetic\n---\n\n# ~~BUG-9994~~ — CLOSED synthetic\n",
        encoding="utf-8",
    )
    check("emphasis-wrapped H1 id extracts", gti.extract(_struck)["h1_id"] == "BUG-9994")
    check("and produces no identity problem", gti.identity_problems([gti.extract(_struck)]) == [])
finally:
    _struck.unlink(missing_ok=True)

print("\nthe live corpus is identity-clean (positive control)")
_live = [gti.extract(p) for p in sorted(gti.TRACKER_DIR.glob("*.md")) if gti.KIND_RE.match(p.name)]
_live_problems = gti.identity_problems(_live)
check(f"identity_problems() empty on the live corpus (got {len(_live_problems)})", _live_problems == [])

print("\nthe dashboard is one deterministic static page")
_html = gti.render_html(_live)
check("same trackers -> same bytes (no date, no baked counts)", _html == gti.render_html(list(reversed(_live))))
check("every tracker is exactly one data row", all(_html.count(f'\n["{t["id"]}", ') == 1 for t in _live))
check("the page owns its whole ground and declares its colour scheme (V6.4: one green-black ground, no second surface)",
      '<meta name="color-scheme" content="light dark">' in _html and "html{min-height:100%;background:var(--bg);color-scheme:light dark}" in _html)
import hashlib
check("the vendored renderer is the pinned file — marked 18.0.13, sha256 b147274a…3556 — and nothing else is vendored",
      gti.digest(gti.MARKED) == "b147274a9ce27d17276587167e49483d719f6893eeca3a3667a59797661d3556"
      and sorted(f.name for f in gti.MARKED.parent.iterdir()) == ["marked-18.0.13.umd.js"])
check("the viewer is read-only and stays in the page: a row id and a bare id open `#=ID`, embedded HTML is escaped, data comes by script tag",
      '<a href="#=${t[0]}">${t[0]}</a>' in _html and 'renderer:{html:k=>esc(' in _html and 's.src="view/"+id+".js"' in _html
      and "fetch(" not in _html.split("<script>")[2] and "contenteditable" not in _html and not re.search(r'<form(?![^>]*method="dialog")', _html) and "action=" not in _html)
import tempfile
_vd, gti.VIEW_DIR = gti.VIEW_DIR, Path(tempfile.mkdtemp())
(gti.VIEW_DIR / "FEAT-99999.js").write_text("stray")
gti.write_views(_live[:2])
_vf = (gti.VIEW_DIR / f'{_live[0]["id"]}.js').read_text()
check("one data file per tracker — `V(id, markdown)` without the front matter — and a stray file is removed",
      _vf.startswith(f'V("{_live[0]["id"]}",') and '\nid: ' not in _vf[:200] and sorted(f.name for f in gti.VIEW_DIR.iterdir()) == sorted(f'{t["id"]}.js' for t in _live[:2]))
gti.VIEW_DIR = _vd
# a link is not a request — the running line's two (0.18.2) load nothing until clicked; what the page fetches by itself is
check("no external request of any kind", not re.search(r'<(?!a )[^>]*\b(?:src|href)="https?://|@import|<link', _html.split("<script>")[0])
      and re.search(r'<(?!a )[^>]*\b(?:src|href)="https?://', '<img alt="" src="https://example.org/x.png">'))
_evil = dict(_live[0], hook_full='x</script><script>alert(1)</script>', title="<b>t</b>")
check("a hook cannot close a script block (two blocks: the vendored renderer, then the page)", gti.render_html([_evil]).count("</script>") == 2)
_kid = dict(_live[0], epic=_live[1]["id"])
check("a valid `epic:` passes the lint", not any("epic:" in p for p in gti.lint([_kid, _live[1]])))
check("`epic:` naming no tracker is refused", any("epic:" in p for p in gti.lint([dict(_live[0], epic="FEAT-99999")])))
check("`epic:` naming itself is refused", any("epic:" in p for p in gti.lint([dict(_live[0], epic=_live[0]["id"])])))
_body = "# T\n\n## What is true now\n\n**Open.** See [the ledger](x.md) and `this`.\nSecond line.\n\nNext paragraph.\n\n## Other\nno\n"
check("the state of an epic is the first paragraph of its current-truth head, markdown stripped",
      gti.current_truth(_body) == "Open. See the ledger and this. Second line.")
check("no current-truth head -> no state", gti.current_truth("# T\n\n## Other\ntext\n") == "")
# tags: a closed vocabulary, at most three, rendered as #chips that are their own filter
check("a known tag passes the lint", not any("tags:" in p for p in gti.lint([dict(_live[0], tags=["research"])])))
check("an unknown tag is refused, and the refusal names the vocabulary",
      any("tags:" in p and "research" in p for p in gti.lint([dict(_live[0], tags=["exploration"])])))
check("more than three tags, or a repeated one, is refused",
      any("at most" in p for p in gti.lint([dict(_live[0], tags=["research", "research"])])))
check("one chain-selecting tag is fine; two on one tracker are refused — a tracker runs one chain",
      not any("select a chain" in p for p in gti.lint([dict(_live[0], tags=["research", "process"])]))
      and (lambda saved: (gti.CHAIN_TAGS.add("process"),
                          any("select a chain" in p for p in gti.lint([dict(_live[0], tags=["research", "process"])])),
                          gti.CHAIN_TAGS.discard("process"))[1])(None))
# a filing looks first: new trackers carry `considered:`, and `--related` finds what to consider
_new = dict(_live[0], id="FEAT-99999", num=99999, kind="FEAT")
check("a new tracker without `considered:` is refused, and the message names the command to run",
      any("--related FEAT-99999" in p for p in gti.lint([dict(_new, considered=[]), _live[1]])))
check("`considered:` naming an existing tracker, or the word none, passes",
      not any("considered" in p for p in gti.lint([dict(_new, considered=[_live[1]["id"]]), _live[1]]))
      and not any("considered" in p for p in gti.lint([dict(_new, considered=["none"]), _live[1]])))
check("`considered:` naming a tracker that does not exist, itself, or none beside an id is refused",
      any("considered" in p for p in gti.lint([dict(_new, considered=["BUG-88888"]), _live[1]]))
      and any("considered" in p for p in gti.lint([dict(_new, considered=["FEAT-99999"]), _live[1]]))
      and any("considered" in p for p in gti.lint([dict(_new, considered=["none", _live[1]["id"]]), _live[1]])))
check("trackers filed before the rule are grandfathered by number",
      not any("considered" in p for p in gti.lint([dict(_live[0], considered=[])])))
_a = dict(_live[0], id="BUG-90001", num=90001, file="BUG-90001-nightly-backup-unencrypted.md", hook_full="the nightly production backup dump is unencrypted on the storagebox", state="")
_b = dict(_live[0], id="FEAT-90002", num=90002, file="FEAT-90002-chart-colours.md", hook_full="chart marker colours follow the palette", state="")
_c = dict(_live[0], id="FEAT-90003", num=90003, file="FEAT-90003-production-data-off-the-host.md", hook_full="a copy of the production dump needs an encrypted backup source", state="")
_rel = gti.related_trackers([_a, _b, _c], "FEAT-90003")
check("`--related` ranks the tracker that shares the rare words first, and never returns the query itself",
      [t["id"] for _s, t in _rel][:1] == ["BUG-90001"] and "FEAT-90003" not in [t["id"] for _s, t in _rel])
check("`--related` takes free words as well as an id",
      [t["id"] for _s, t in gti.related_trackers([_a, _b, _c], "unencrypted nightly backup")][:1] == ["BUG-90001"])
# the dashboard shows triage: one date in the front matter, everything else derived
_tri = gti.render_html([dict(_live[0], triaged="2026-09-20"), _live[1]])
check("the triage date, the rank and the board section travel in the row — then the ready marks that fail, and last the kind of problem",
      re.search(r'"2026-09-20", 0, "\w+", \[[^\]]*\], "", "[^"]*", "[^"]*", \[\], \d+, \["", false\], \{\}, \{\}, \["", "", "", \[\], "", "", \[\], \[\], "", "", "", \[\]\], \[\]\]', _tri) is not None)
check("untriaged is derived — exactly what the next pass lists: the generator's word, and work in progress judged too long ago — counted, and searchable by its word",
      'untriaged=t=>t[19]=="triage"||t[2]=="In Progress"&&!fresh(t)' in _tri and '(untriaged(t)?" untriaged "+' in _tri and 'L["count.untriaged"]' in _tri)
check("FM-020 · a whole id alone is that tracker — `~ID` keeps the neighbourhood, and anything else still matches by substring",
      'exact=!hood&&byId.get(q.toUpperCase())' in _tri and "hood?near.has(t[0]):exact?t==exact:(every||OPEN.has(t[2]))&&words.every(" in _tri
      and '"search.help": "A whole id shows that tracker. What links to it: ~ID (Markdown links only). A story\'s chapters: the story view.' in _tri
      and '$("q").title=L["search.help"]' in _tri)
check("FM-020 · the counter names an id searched alone — it is that tracker, open or not, never counted as `open`",
      '${hood?L["count.around"].replace("{0}",hood[0]):exact?L["count.id"].replace("{0}",exact[0]):every?' in _tri and '"count.id": "tracker · {0}"' in _tri)
check("FM-024 S7, FM-032 S2 · the board carries the report — null where no commit names a session and no verdict was given — and its strip: the parents with a commit in the last day, each a line that opens on its sub-sessions, and the week's verdicts",
      "REG=null," in _tri and '+(REG?(REG.groups.length?"\\n\\n<b>"+l("sessions.recent",REG.parents,REG.all)+"</b>\\n"' in _tri and "<details><summary>" in _tri and 'l("reviews.week",REG.reviews[0],REG.reviews[1])' in _tri)
check("FM-021 · the progress line says it is empty until a first pass while none has run — no `triaged:` anywhere, no pass in TRIAGE.md",
      'PASSED=LAST||(HOME.last.match(' in _tri and 'progress:PASSED?l("desc.progress"):l("desc.progress.none")' in _tri
      and 'triaged:PASSED?l("desc.triaged",PASSED):l("desc.triaged.none")' in _tri and "LAST||HOME.last" not in _tri and '"desc.progress.none": "empty until a first triage pass has run — --triage"' in _tri)
check("a story's header says how much of it a pass has judged, and counts its chapters shipped, closed and open apart — a closed chapter is not shipped, and is not done",
      '${l("word.triaged")} ${open.filter(t=>t[17]).length}/${open.length}' in _tri and 'shipped=kids.filter(t=>t[2]=="Shipped").length' in _tri
      and 'closed=kids.filter(t=>t[2]=="Closed").length' in _tri and '${shipped} ${l("story.shipped")} · ${closed} ${l("story.closed")} · <span class=' in _tri
      and '${c.filter(x=>x[2]=="Shipped").length} ${l("story.shipped")} · ${c.filter(x=>x[2]=="Closed").length} ${l("story.closed")}' in _tri and "story.done" not in _tri)
check("FM-005 · no label calls a `Closed` tracker done: not the board's fifth section, its description, nor a story's count — in English and in the German table the tool ships",
      not any(re.search(r"\bdone\b", v, re.I) for k, v in gti.LABELS.items() if k.startswith(("story.", "section.", "desc.")))
      and {"story.shipped", "story.closed", "story.open", "section.ended", "desc.ended"} <= set(gti.LABELS) and not {"story.done", "section.done", "desc.done"} & set(gti.LABELS)
      and not any(re.search(r"erledigt", v, re.I) for k, v in gti.read_flat((HERE / "examples/de/labels.yaml").read_text(encoding="utf-8")).items() if k.startswith(("story.", "section.", "desc."))))
check("the board is the first view: progress · triage · triaged · backlog · ended, one section per tracker plus the newest pass",
      'GROUPS=[["board",' in _tri and re.search(r"BOARD=\{progress:.*triage:.*triaged:.*backlog:.*ended:", _tri, re.S) is not None
      and 'untriaged(t)?"triage":t[19]]' in _tri and "OPEN.has(t[2])&&!fresh(t)" not in _tri
      and "recent=t=>!!t[17]&&t[17]==LAST" in _tri and "(7+1)*864e5" in _tri and "__DAYS__" not in _tri and gti.TRIAGE_DAYS == 7
      and '<button id="g" aria-pressed="true"></button><button id="o"' in _tri)
check("the board shows the triage home: the Owner's current path on top, the newest pass under `triaged` — plain text, ids clickable",
      "HOME={" in _tri and "__HOME__" not in _tri and "FEAT-002 to its end" in _tri and "](FEAT-002" not in _tri.split("const BLOB")[1].split(",T=[")[0]
      and 'HOME.last?`<tr class="s">' in _tri and set(gti.triage_home()) == {"path", "last", "intent"})
_ix = gti.render_triage([dict(_live[0], rank=2, tier="P1"), dict(_live[1], rank=1, tier="P0"), _live[2]])
check("the index opens with what the board shows: the Owner's path verbatim, then the ranked trackers in order",
      "FEAT-002](FEAT-002-a-story.md) to its end" in _ix and re.search(rf"\| 1 \| P0 \| — \| — \| [^|]+ \| \[{_live[1]['id']}\]", _ix).start() < re.search(rf"\| 2 \| P1 \| — \| — \| [^|]+ \| \[{_live[0]['id']}\]", _ix).start()
      and _live[2]["id"] not in _ix and "Nothing is ranked yet" in gti.render_triage([_live[2]]))
_b = lambda **kw: gti.board(dict(_live[0], **kw))
check("one board definition — done · triage · progress · backlog — printed by INDEX.md and handed to the page",
      [_b(status="Shipped", triaged=""), _b(status="In Progress", triaged=""), _b(status="In Progress", triaged="2026-09-20"),
       _b(status="Parked", triaged="2026-09-20"), _b(status="Proposed", triaged="2026-09-20"), _b(status="Closed", triaged="2026-09-20")]
      == ["ended", "triage", "progress", "backlog", "backlog", "ended"]
      # 2026-09-21 — the board says `triage` for exactly what `--triage` lists: old undated Proposed / Reserved / Parked work is backlog, a new filing is not
      and [_b(status="Proposed", triaged="", num=1), _b(status="Reserved", triaged="", num=1), _b(status="Parked", triaged="", num=1),
           _b(status="Proposed", triaged="", num=90001, kind="FEAT")] == ["backlog", "backlog", "backlog", "triage"]
      and "| progress | 2026-09-20 |" in gti.render([dict(_live[0], status="In Progress", triaged="2026-09-20", tier="P1")], "Features")
      and '"2026-09-20", 0, "progress", [' in gti.render_html([dict(_live[0], status="In Progress", triaged="2026-09-20")])
      and '"triage":t[19]]' in _tri and "order.indexOf(k)>1" in _tri and 't[2]=="In Progress"&&Date.now()-Date.parse(t[24][0])' in _tri and "?\"progress\":\"backlog\"" not in _tri)
# FM-041 — a status is what a seat set, a rank is what a pass judged: ranked open work sits in `progress` by rank, whatever its status.
# On origin/main 2eb803b this fails at `return "progress" if t["status"] == "In Progress" else "backlog"`: the ranked Proposed one is `backlog`.
_r = lambda **kw: gti.board({**dict(_live[0], triaged="2026-09-20"), **kw})
check("FM-041: a ranked Proposed tracker is in progress; an unranked Proposed one in backlog; a ranked In Progress one stays; triage and done keep their rules",
      [_r(status="Proposed", rank=3), _r(status="Proposed", rank=0), _r(status="In Progress", rank=3), _r(status="In Progress", rank=0),
       _r(status="Proposed", rank=3, raised="2026-09-21"), _r(status="Proposed", rank=3, triaged="", num=90001, kind="FEAT"), _r(status="Shipped", rank=3), _r(status="Parked", rank=0)]
      == ["progress", "backlog", "progress", "progress", "triage", "triage", "ended", "backlog"]
      and "| progress | 2026-09-20 |" in gti.render([dict(_live[0], status="Proposed", triaged="2026-09-20", rank=3, tier="P1")], "Features")
      and "| backlog | 2026-09-20 |" in gti.render([dict(_live[0], status="Proposed", triaged="2026-09-20", rank=0, tier="P1")], "Features")
      and '"2026-09-20", 3, "progress", [' in gti.render_html([dict(_live[0], status="Proposed", triaged="2026-09-20", rank=3)]))
check("the board always shows its five sections — an empty `progress` is an answer — and a path id opens its tracker",
      "for(const k of order)groups.set(k,groups.get(k)||[])" in _tri and '`<a href="#=${i}">${i}</a>`:i)' in _tri)
check("`triaged:` is a date and nothing else",
      any("triaged" in p for p in gti.lint([dict(_live[0], fm={"triaged": "yesterday"})]))
      and not any("triaged" in p for p in gti.lint([dict(_live[0], fm={"triaged": "2026-09-20"})])))
# one command is the triage pass
_w1 = dict(_live[0], id="FEAT-91001", file="FEAT-91001-old-work.md", status="In Progress", triaged="", hook_full="old work on the scraper", state="", tier="P2", title="old work")
_w2 = dict(_live[0], id="FEAT-91002", file="FEAT-91002-judged.md", status="In Progress", triaged="2026-09-18", hook_full="already judged", state="", tier="P2", title="judged")
_w3 = dict(_live[0], id="FEAT-91003", file="FEAT-91003-proposed.md", status="Proposed", triaged="", hook_full="a proposal about the scraper", state="", tier="P2", title="proposed")
_sheet, _left = gti.triage_worksheet([_w1, _w2, _w3], "2026-09-20", lambda path: "2026-07-01")
check("the worksheet lists In Progress trackers no pass has dated — so a second run continues the first",
      _left == 1 and "FEAT-91001" in _sheet and "FEAT-91002](" not in _sheet and "FEAT-91003](" not in _sheet)
check("each row carries when it was last worked on, its closest open neighbour, and empty Verdict and Reason cells",
      "| 2026-07-01 · FAILS | FEAT-91003 (" in _sheet and _sheet.rstrip().endswith("| | |") and "old work on the scraper" in _sheet)
_filled = _sheet.replace("| | |", "| keep P1 | worked on yesterday |")
_again, _left2 = gti.triage_worksheet([dict(_w1, triaged="2026-09-20"), _w2, _w3], "2026-09-20", lambda path: "2026-07-01", _filled)
_mid, _left3 = gti.triage_worksheet([_w1, _w2, _w3], "2026-09-20", lambda path: "2026-07-01", _filled)
check("a re-run keeps every filled row — once — and lists only what is left (rehearsal 3 lost ten verdicts to a re-run)",
      _left2 == 0 and "| keep P1 | worked on yesterday |" in _again and _left3 == 0 and _mid.count("FEAT-91001](") == 1)
check("a pass needs no tracker id: the rules print the Owner's intent and current path from the triage home, and forbid touching the path",
      "{current_path}" in gti.TRIAGE_RULES and "{intent}" in gti.TRIAGE_RULES and gti.TRIAGE_RULES.index("{intent}") < gti.TRIAGE_RULES.index("  1. Fill")
      and "consolidation" in gti.triage_home()["intent"] and "{home}" in gti.TRIAGE_RULES and "{owner}" not in gti.TRIAGE_RULES
      and "never touch its *current path*" in gti.TRIAGE_RULES and (gti.TRACKER_DIR / "TRIAGE.md").exists())
check("the tier rule sits under `keep`, not under `epic`",
      gti.TRIAGE_RULES.index("EVERY KEEP CARRIES A TIER") < gti.TRIAGE_RULES.index("       epic ID"))
_old, _n_old = gti.triage_worksheet([dict(_w2, triaged="2026-09-12")], "2026-09-20", lambda path: "2026-09-19")
_wk, _ = gti.triage_worksheet([dict(_w2, triaged="")], "2026-09-20", lambda path: "2026-09-12")
check("one 7-day window: a judgement 8 days old returns to the worksheet, work 1 day old passes the keep test, work 8 days old fails",
      _n_old == 1 and "| 2026-09-19 · keep |" in _old and "| 2026-09-12 · FAILS |" in _wk)
# a re-run applies the mechanical half of every verdict; the judgement stays with the seat
_doc = '---\nid: FEAT-91001\nstatus: In Progress\nrank: 9\nhook: "h"\n---\n\n# FEAT-91001 — t\n\nbody\n'
_ids = {"FEAT-91003"}
_k, _hand, _err = gti.apply_verdict(_doc, "keep P1 #2 build", "2026-09-20", _ids)
check("keep: the date, the rank, the move and the judged tier — all in the front matter, above the hook; the body is not touched",
      not _err and "triaged: 2026-09-20\nnext: build\ntier: P1\nhook:" in _k and "rank: 2\n" in _k and "rank: 9" not in _k
      and _k.endswith("# FEAT-91001 — t\n\nbody\n") and "status: In Progress" in _k)
_k2, _, _ = gti.apply_verdict(_k, "keep P2", "2026-09-20", _ids)
check("a judged tier is replaced in place, an unranked keep loses its rank, and applying twice changes nothing",
      _k2.count("tier:") == 1 and "tier: P2\n" in _k2 and "rank:" not in _k2
      and gti.apply_verdict(_k2, "keep P2", "2026-09-20", _ids)[0] == _k2)
_pk, _, _ = gti.apply_verdict(_doc, "park P3", "2026-09-20", _ids)
_ep, _, _ = gti.apply_verdict(_doc, "epic FEAT-91003 P2", "2026-09-20", _ids)
_deep = _doc.replace("body", "\n".join(["line"] * 50) + "\n**Tier:** P0 release continuity.")
_dp, _, _ = gti.apply_verdict(_deep, "keep P2", "2026-09-20", _ids)
check("one reader for the tier: a Tier line below line 40 is read by the index — and a judged `tier:` wins over it, the sentence left as filed (rehearsals 6, 10–12)",
      gti.tier_match(gti.parse_frontmatter(_deep)[1]).group(1) == "P0" and "**Tier:** P0 release continuity." in _dp and "tier: P2\n" in _dp)
check("park sets the status, drops the rank and carries a tier — P2 or P3 only; epic sets the story and the tier",
      "tier: P3\n" in _pk and gti.apply_verdict(_doc, "park", "2026-09-20", _ids)[2] and gti.apply_verdict(_doc, "park P0", "2026-09-20", _ids)[2]
      and "status: Parked" in _pk and "rank:" not in _pk and "epic: FEAT-91003" in _ep and "tier: P2\n" in _ep)
_mg, _mh, _me = gti.apply_verdict(_doc, "merge FEAT-91003", "2026-09-20", _ids)
_sev = _doc.replace("body", "**Severity / Tier:** **S1 · P0 commissioning blocker.**")
_sv, _, _ = gti.apply_verdict(_sev, "keep P2", "2026-09-20", _ids)
check("the `Severity / Tier: S1 · P0` form (109 trackers) is read — and never rewritten: a park must not turn a severity sentence against itself",
      gti.tier_match(_sev).group(1) == "P0" and "S1 · P0 commissioning blocker" in _sv and "tier: P2\n" in _sv and "THE CURRENT PATH" in gti.TRIAGE_RULES)
check("merge only dates the tracker and says what is left by hand", not _me and "status: In Progress" in _mg and "move the scope" in _mh)
check("a verdict the command cannot read is refused, not guessed",
      all(gti.apply_verdict(_doc, v, "2026-09-20", _ids)[2] for v in ("keep", "maybe", "epic P1", "merge FEAT-99999", "park P2 #1")))
# a judged domain word was tried and taken out (rehearsals 7 and 8: two cold seats agreed on 5, then 4, of 10)
_dw, _, _dwe = gti.apply_verdict(_doc, "keep P1 #3 run complex unsettled", "2026-09-20", _ids)
check("no domain is written: a verdict that still carries the word applies as the plain keep it is, and the rules no longer ask for one",
      not _dwe and "domain:" not in _dw and "settled:" not in _dw and "rank: 3\n" in _dw and "FATHOM" not in gti.TRIAGE_RULES
      and not hasattr(gti, "DOMAINS") and "THE ROW carries two cells you do not fill" in gti.TRIAGE_RULES)
# the next move: extracted, not judged; six moves, tested in the order the rules print them
_nx, _, _nxe = gti.apply_verdict(_doc, "keep P1 #3 Run", "2026-09-20", _ids)
_nx2, _, _ = gti.apply_verdict(_nx, "keep P2", "2026-09-20", _ids)
_nx3, _, _nx3e = gti.apply_verdict(_nx, "keep P1 #4", "2026-09-20", _ids)
check("a ranked tracker names its next move — `next:` — and a move the last seat left stands until another is named (rehearsal 9)",
      not _nxe and "next: run\n" in _nx and "next: run\n" in _nx2 and "next:" not in _pk and "next: build\n" in _k
      and not _nx3e and "next: run\n" in _nx3 and "rank: 4\n" in _nx3
      and "next: owner\n" in gti.apply_verdict(_nx, "keep P1 #4 owner", "2026-09-20", _ids)[0]
      and "next: run\n" in gti.apply_verdict(_nx, "park P3", "2026-09-20", _ids)[0])
check("ranked without a move is refused, and so is a move on what is not about to be pulled — every unranked form applies as rehearsed",
      all(gti.apply_verdict(_doc, v, "2026-09-20", _ids)[2] for v in ("keep P1 #2", "epic FEAT-91003 P2 #1", "merge FEAT-91003 owner", "close review"))
      and "next: wait\n" in gti.apply_verdict(_doc, "park P3 wait", "2026-09-20", _ids)[0]
      and "next move" in gti.apply_verdict(_doc, "keep P1 #2", "2026-09-20", _ids)[2]
      and not any(gti.apply_verdict(_doc, v, "2026-09-20", _ids)[2] for v in ("keep P2", "park P3", "epic FEAT-91003 P2", "merge FEAT-91003", "close", "fix", "keep P2 owner", "epic FEAT-91003 P2 #1 review")))
_bn = lambda **kw: [p for p in gti.lint([dict(_live[0], fm=kw)]) if "`next:`" in p]
check("the index gate knows the six moves; the rules test them in one printed order, `build` last",
      _bn(next="complex") and not _bn(next="owner") and not _bn() and gti.MOVES == ("review", "run", "wait", "owner", "script", "build")
      and [gti.TRIAGE_RULES.index(f"               {m} ") for m in gti.MOVES] == sorted(gti.TRIAGE_RULES.index(f"               {m} ") for m in gti.MOVES)
      and all(k in gti.TRIAGE_RULES for k in ("EXTRACT the move", "Do NOT judge how hard or how nearly done", "even where the Owner must attend it")))
_m = lambda **kw: gti.ready_needs({**_w1, "lines": 100, "provable": True, "state": "what is true now", "blocked_by": [], **kw}, {"FEAT-91003": _w3, "FEAT-91009": dict(_w3, status="Shipped")})
check("four ready marks are derived — stated, sized, provable, clear; a failing mark is named, nothing is summed",
      _m() == [] and _m(state="") == ["stated"] and _m(lines=gti.SIZED_LINES + 1) == ["sized"] and _m(provable=False) == ["provable"] and _m(blocked_by=["FEAT-91003"]) == ["clear"]
      and _m(blocked_by=["Owner"]) == ["clear"] and _m(blocked_by=["FEAT-91009"]) == [] and _m(lines=gti.SIZED_LINES + 1, provable=False) == ["sized", "provable"]
      and gti.DONE_RE.search("## Done when\n") and gti.DONE_RE.search("its falsifier is") and not gti.DONE_RE.search("nothing of the kind"))
_fs, _ = gti.triage_worksheet([dict(_w1, reads=3470, lines=700, provable=False, next="run"), _w3], "2026-09-20", lambda path: "2026-07-01", "", {"FEAT-91001": ["fleet-launcher", "rs"]})
check("the worksheet's Facts cell is derived, sits before the Verdict, and leaves the Verdict where a re-run reads it",
      "| repos fleet-launcher, rs · reads 3.5k · next run · NOT stated, sized, provable | | |" in _fs and "| Hook | Now | Facts | Verdict | Reason |" in _fs
      and re.search(r"\| repos — · reads \d+\.\dk[^|]*\| \| \|", _sheet)
      and gti.triage_worksheet([dict(_w1, triaged="2026-09-20"), _w3], "2026-09-20", lambda path: "2026-07-01", _fs.replace("provable | | |", "provable | keep P2 | r |"))[0].count("| keep P2 | r |") == 1)
_rk = gti.render_triage([dict(_live[0], rank=1, tier="P1", lines=900, provable=False, blocked_by=[], next="run", state="x")])
_pg = gti.render_html([dict(_live[0], status="In Progress", rank=1, lines=900, provable=False, blocked_by=[], next="run", state="x", intent="", epic="—"), dict(_live[1], rank=0, lines=900, provable=False)])
check("one model, two renderings: the ranked table and the page row say a ranked tracker's next move and what it needs",
      "| 1 | P1 | run | *complex* | sized, provable, intended | [" in _rk and '["sized", "provable", "intended"], "run", "", "", [], ' in _pg
      and all(k in _pg for k in ('${l("waiting.title")}: ${w.length}</b>', '<b>${l("story.chapters")}</b> — ', 'L["word.reads"]+" "+(t[25]/1000).toFixed(1)+"k"', 'l("viewer.stale","7")',
                                 '"waiting.title": "waiting for you"', '"viewer.stale": "stale — older than {0} days'))
      and '<b>${l("viewer.handover")}</b> — ${l("viewer.next")}: ' in _pg and '<b>${l("viewer.verdict")}</b> — ' in _pg and '"<i>"+l("word.missing")' in _pg and '${t[21]?" → "+esc(t[21]):""}' in _pg and "dec=s=>{try{return decodeURIComponent(s)}catch(e){return s}}" in _pg and _pg.count("decodeURIComponent(") == 1)
# `kind-of-problem:`, the second try: left by a seat with the tracker open, never judged by a pass; derived
# from the move wherever the move already says it (rehearsal 13), so it is owed — a named gap — only on a `build`
_bk = lambda **kw: [p for p in gti.lint([dict(_live[0], fm={"kind-of-problem": kw["problem"]} if kw else {})]) if "`kind-of-problem:`" in p]
_kd = lambda **kw: gti.render_triage([dict(_live[0], rank=1, tier="P1", lines=10, provable=True, blocked_by=[], state="x", intent="i", **kw)])
check("`kind-of-problem:` is one of four words, read from the front matter, and the gate names the four tests",
      _bk(problem="easy") and "found only by running" in _bk(problem="hard")[0] and not _bk(problem="chaos") and not _bk()
      and gti.PROBLEM_KINDS == ("obvious", "complicated", "complex", "chaos")
      and gti.parse_frontmatter("---\nid: X\nkind-of-problem: Complex\n---\n")[0]["kind-of-problem"] == "Complex")
check("the kind is derived from the move where the move says it, judged only where it cannot — and a judged word wins",
      [gti.kind_of({"next": m}) for m in gti.MOVES] == [("complicated", False), ("complex", False), ("complex", False), ("complicated", False), ("obvious", False), ("", False)]
      and gti.kind_of({"next": "run", "problem": "chaos"}) == ("chaos", True) and gti.kind_of({}) == ("", False))
check("a ranked `build` with no kind NEEDS one; the table prints a judged kind plain and a derived one in italics; the Facts cell shows only what a seat left",
      "| build | — | kind |" in _kd(next="build") and "| build | complicated | — |" in _kd(next="build", problem="complicated")
      and "| owner | *complicated* | — |" in _kd(next="owner") and "| — | — | — |" in _kd()
      and "· next build · kind obvious · NOT" in gti.triage_worksheet([dict(_w1, next="build", problem="obvious"), _w3], "2026-09-20", lambda path: "2026-07-01")[0]
      and "kind" not in _fs.split("| repos fleet-launcher")[1].split("\n")[0]
      and ', ["complex", false], {}, {}, ["", "", "", [], "", "", [], [], "", "", "", []], []]' in _pg and '" · "+l("viewer.kind")+": "+(t[26][0]?' in _pg)
# the schema: FRONT_MATTER is the one list of keys; the gate refuses a key outside it, a value off its shape,
# and open work without a required key — and the live corpus is green against it (the positive control)
_sp = lambda _st="Shipped", **fm: gti.schema_problems({"id": "FEAT-91001", "status": _st, "fm": {"id": "FEAT-91001", "status": _st, **fm}})
check("a key that is not in the schema is refused, and a near miss is named — a typo was silently ignored before",
      "did you mean `kind-of-problem:`" in _sp(kind_of_problem="complex")[0] and "did you mean `blocked-by:`" in _sp(blocked_by="Owner")[0]
      and "not a front-matter key." in _sp(priority="P1")[0] and "did you mean" not in _sp(title="x")[0]
      and not _sp(**{"# a comment, with a colon": "in it"}) and not _sp(next="Run", tier="P2", rank="3", epic="FEAT-180"))
check("a value that does not fit its key's shape is refused — `rank: two` used to read as no rank at all",
      _sp(rank="two") and _sp(tier="P5") and _sp(epic="the launcher") and _sp(considered="none, FEAT-1") and _sp(**{"blocked-by": "someone"}) and _sp(**{"blocked-by": "Owner — a, b"})
      and not _sp(considered="BUG-328, BUG-327") and not _sp(**{"blocked-by": "Owner — the rotation ruling, FEAT-124"}) and not _sp(considered="none") and not _sp(hook=""))
check("every tracker has a front matter with `id:` and `status:`, open work a `hook:` too, and `status:` is one word (slice S7)",
      ["`hook:`" in p for p in _sp("In Progress")] == [True] and not _sp("Shipped") and not _sp("In Progress", hook="h")
      and "no front matter" in gti.schema_problems({"id": "FEAT-91001", "status": "Shipped", "fm": {}})[0]
      and ["every tracker states `status:`" in p for p in gti.schema_problems({"id": "FEAT-91001", "status": "Shipped", "fm": {"id": "FEAT-91001"}})] == [True]
      and _sp(status="Shipped 0.14.6") and "one of In Progress · Parked · Proposed · Reserved · Shipped · Closed" in _sp(status="Done")[0]
      and not gti.schema_problems({"id": "FEAT-91001", "status": "Shipped"})
      and {k: v[1] for k, v in gti.FRONT_MATTER.items() if v[1]} == {"id": "all", "status": "all", "hook": "open"}
      and not [t["id"] for t in _live if not t["fm"]])
check("the live corpus is green against the schema, every key the generator reads is in it, and `--schema` prints the table",
      not [p for t in _live for p in gti.schema_problems(t)]
      and {a or b for a, b in re.findall(r'fm\.get\("([a-z_-]+)"\)|fm\["([a-z_-]+)"\]', Path(gti.__file__).read_text(encoding="utf-8"))} <= set(gti.FRONT_MATTER)
      and "| `kind-of-problem:` | one of obvious · complicated · complex · chaos |" in gti.render_schema() and "| `hook:` — required on open work |" in gti.render_schema() and "| `id:` — required |" in gti.render_schema()
      and run(["--schema"])[0] == gti.EXIT_OK)
# a new filing meets a second reader: the next pass, whatever its status; `considered:` is challenged by a seat, not a score
_nf = dict(_w3, id="FEAT-91189", num=91189, kind="FEAT", file="FEAT-91189-new.md", status="Proposed", hook_full="quasar zeppelin proposal", considered=["FEAT-91001"])
_old = dict(_w3, id="FEAT-91002", file="FEAT-91002-done.md", status="Shipped", hook_full="the zeppelin work that shipped long ago")
_ns, _nn = gti.triage_worksheet([dict(_w1, hook_full="old work on the quasar"), _w3, _old, _nf, dict(_nf, id="FEAT-91190", file="FEAT-91190-n.md", hook_full="something else", considered=[], triaged="2026-09-01")], "2026-09-20", lambda path: "2026-09-19")
_nrow = next(l for l in _ns.splitlines() if l.startswith("| [FEAT-91189]"))
check("a tracker filed under the `considered:` rule and never triaged enters the worksheet in any open status; an older `Proposed` one and a triaged one do not",
      "· keep · NEW FILING |" in _nrow and "| [FEAT-91003]" not in _ns and "| [FEAT-91190]" not in _ns and "| [FEAT-91001]" in _ns and "NEW FILING" not in _ns.split("| [FEAT-91001]")[1].split("\n")[0])
check("its row prints what it was held against beside the three closest trackers, done ones included, each marked — and the rules say to open what was not considered",
      "considered FEAT-91001 · closest: " in _nrow and "FEAT-91001 (" in _nrow and ", In Progress) ✓" in _nrow and ", Shipped) NOT considered" in _nrow and _nrow.count(" | ") == _ns.splitlines()[-2].count(" | ")
      and "considered — nothing is written" in gti.triage_worksheet([_w1, dict(_nf, considered=[])], "2026-09-20", lambda path: "2026-09-19")[0]
      and "OPEN every one marked NOT considered" in gti.TRIAGE_RULES and gti.CONSIDERED_FROM == {"FEAT": 189, "BUG": 334, "ALIGN": 1000})
_nk, _, _nke = gti.apply_verdict(_doc.replace("status: In Progress", "status: Proposed"), "keep P2", "2026-09-20", _ids)
check("a verdict on a new `Proposed` filing dates it and leaves its status — so it leaves the new-filings list", not _nke and "triaged: 2026-09-20" in _nk and "status: Proposed" in _nk)
check("a triage pass still never writes a kind — a verdict carrying the word applies as the plain keep it is; the rules say why",
      "kind-of-problem" not in _dw and "You do not judge it from a row" in gti.TRIAGE_RULES)
_nw, _ = gti.triage_worksheet([dict(_w1, state="Built and merged. It stays In Progress: its Done when asks for a real fleet | " + "x" * 800), dict(_w1, id="FEAT-91004", file="FEAT-91004-x.md", state="")],
                              "2026-09-20", lambda path: "2026-07-01")
check("what is fathomed is what is LEFT: the row carries the opening of *What is true now*, capped, pipe-safe — and the rules say so (rehearsal 7: 5 of 10)",
      "| Built and merged. It stays In Progress: its Done when asks for a real fleet \\| xx" in _nw and "…" in _nw.split("FEAT-91001](")[1].split("\n")[0]
      and "| — | repos" in _nw.split("FEAT-91004](")[1] and gti.NOW_MAX == 600
      and all(k in gti.TRIAGE_RULES for k in ("what is left", "the problem as it was filed", "DERIVED", "{sized}")))
# intent: the Owner's words on a story; its chapters inherit; a seat never writes one
_st = dict(_w1, id="FEAT-91010", file="FEAT-91010-story.md", intent="for — X · so that — Y · never — Z", epic="—")
_ch = dict(_w1, id="FEAT-91011", file="FEAT-91011-chapter.md", intent="", epic="FEAT-91010")
_by = {"FEAT-91010": _st, "FEAT-91011": _ch}
_is, _ = gti.triage_worksheet([_st, _ch, dict(_w1, intent="", epic="—")], "2026-09-20", lambda path: "2026-07-01")
check("a chapter inherits its story's intent; the worksheet prints each intent once, above the rows; ranked work with none needs one",
      gti.intent_of(_ch, _by) == _st["intent"] and gti.intent_of(_st, _by) == _st["intent"] and gti.intent_of(dict(_w1, intent="", epic="—"), _by) == ""
      and _is.count("- **FEAT-91010** — for — X · so that — Y · never — Z") == 1 and _is.index("- **FEAT-91010**") < _is.index("| Tracker |")
      and "intended" not in gti.render_triage([dict(_st, rank=1, lines=10, provable=True, state="x", blocked_by=[])])
      and '"for — X · so that — Y · never — Z", "", [], ' in gti.render_html([_st, _ch]) and '"for — X · so that — Y · never — Z", "FEAT-91010", [], ' in gti.render_html([_st, _ch])
      and '(${l("viewer.from",t[23])})' in gti.render_html([_st]))
_real = {t["id"]: t for t in _live}
check("a story carries the Owner's intent in its front matter",
      all(gti.extract(next(gti.TRACKER_DIR.glob(f"{i}-*.md")))["intent"].startswith("for — ") for i in ("FEAT-002",)))
# the layer that writes to many trackers at once
import tempfile as _tf
_td, _keep_dir = Path(_tf.mkdtemp()), gti.TRACKER_DIR
_mk = lambda i, extra="": (_td / f"{i}-x.md").write_text(f'---\nid: {i}\nstatus: In Progress\n{extra}hook: "h"\n---\n\n# {i} — t\n\nbody\n', encoding="utf-8")
_mk("FEAT-91001", "rank: 1\n"); _mk("FEAT-91002"); _mk("FEAT-91003"); (_td / "FEAT-91004-x.md").write_text("# FEAT-91004 — no front matter\n\n---\n\nbody\n", encoding="utf-8")
_tk = [dict(id=f"FEAT-9100{n}", file=f"FEAT-9100{n}-x.md", rank=1 if n == 1 else 0, triaged="", status="In Progress") for n in (1, 2, 3, 4)]
_hd = "| Tracker | Tier | Verdict | Reason |\n|---|---|---|---|\n"
_rowf = lambda i, v, r="r": f"| [{i}](../../{i}-x.md) — t | P2 | {v} | {r} |\n"
_rd = lambda i: (_td / f"{i}-x.md").read_text(encoding="utf-8")
gti.TRACKER_DIR = _td
try:
    _l1, _e1 = gti.apply_worksheet(_hd + _rowf("FEAT-91002", "merge FEAT-91003", "keep P3 | see FEAT-91003"), True, _tk, "2026-09-20")
    _l2, _e2 = gti.apply_worksheet(_hd + _rowf("FEAT-91002", "keep #1 run"), True, _tk, "2026-09-20")
    _r2 = _rd("FEAT-91001")
    _l3, _e3 = gti.apply_worksheet(_hd + _rowf("FEAT-91002", "keep P1 #2 run") + _rowf("FEAT-91003", "keep P1 #2 build"), True, _tk, "2026-09-20")
    _l4, _e4 = gti.apply_worksheet(_hd + _rowf("FEAT-91004", "keep P2"), True, _tk, "2026-09-20")
    _l5, _e5 = gti.apply_worksheet(_hd + _rowf("FEAT-91003", "keep P1 #1 build"), True, _tk, "2026-09-20")
    _l7, _e7 = gti.apply_worksheet(_hd + _rowf("FEAT-91002", "keep P1 #3"), True, [dict(t, status="Shipped") if t["id"] == "FEAT-91002" else t for t in _tk], "2026-09-20")
    _r7 = _rd("FEAT-91002")
    _l6, _e6 = gti.apply_worksheet(_hd + "| FEAT-91002 no link | P2 | keep P2 | r |\n".replace("| FEAT", "| [FEAT"), True, _tk, "2026-09-20")
finally:
    gti.TRACKER_DIR = _keep_dir
check("a `|` typed into the Reason is refused by name — it never turns a fragment of the reason into the verdict",
      not _l1 and len(_e1) == 1 and "cells" in _e1[0] and "FEAT-91002" in _e1[0])
check("a verdict that does not stand takes no rank from its holder; one rank names one row; a freed rank is logged",
      _e2 and "rank: 1\n" in _r2 and len(_e3) == 1 and "already claimed by FEAT-91002" in _e3[0]
      and any("rank #1 freed" in l for l in _l5) and "rank:" not in _rd("FEAT-91001") and "rank: 1\n" in _rd("FEAT-91003"))
check("a tracker with no front matter is refused and left byte for byte — `set_front` never rewrites a head it cannot find",
      len(_e4) == 1 and "no front matter" in _e4[0] and _rd("FEAT-91004").startswith("# FEAT-91004 — no front matter")
      and gti.set_front("# T\n\n---\n\nbody\n", "rank", "1") == "# T\n\n---\n\nbody\n" and gti.set_front("no rule at all", "rank", "1") == "no rule at all")
check("a tracker that shipped since its verdict is left alone by a same-day re-run — not ranked, not re-dated, and no error over its missing move",
      not _l7 and not _e7 and "rank: 3" not in _r7)
check("a row that does not open with a tracker link is named, not a traceback", len(_e6) == 1 and "does not open with a tracker link" in _e6[0])
check("a move is a token of the verdict, never a word of its prose; a rank is 1 to ten",
      "next:" not in gti.apply_verdict(_doc, "keep P2 — the Owner's call, owner decides", "2026-09-20", _ids)[0]
      and "next: owner\n" in gti.apply_verdict(_doc, "keep P2 owner — his call", "2026-09-20", _ids)[0]
      and gti.apply_verdict(_doc, "keep P1 #47 run", "2026-09-20", _ids)[2] and gti.apply_verdict(_doc, "keep P1 #0 run", "2026-09-20", _ids)[2])
_vd, _keep2 = Path(_tf.mkdtemp()), gti.TRACKER_DIR
(_vd / "evidence" / "triage").mkdir(parents=True)
(_vd / "evidence" / "triage" / "triage-2026-09-13.md").write_text(_hd + _rowf("FEAT-91002", "keep P2", "older"), encoding="utf-8")
(_vd / "evidence" / "triage" / "triage-2026-09-20.md").write_text(_hd + _rowf("FEAT-91002", "park P3 owner", "restarts when the Owner ranks it \\| not before") + _rowf("FEAT-91003", "", ""), encoding="utf-8")
gti.TRACKER_DIR = _vd
try:
    _lv = gti.latest_verdicts()
finally:
    gti.TRACKER_DIR = _keep2
check("the page shows a tracker's newest verdict and its reason — read from the pass's worksheet, never stored in the tracker",
      _lv == {"FEAT-91002": ["2026-09-20", "park P3 owner", "restarts when the Owner ranks it | not before"]})
check("the printed rules say the five things a cold agent must not have to find elsewhere",
      all(k in gti.TRIAGE_RULES for k in ("merged into", "a merge rules nothing", "triaged:", "RESUMABLE", "one evidence file",
                                          "THE INTENT", "NEVER GUESS", "RUN THIS COMMAND AGAIN", "BY HAND", "NEXT, NOT NOW")))
# triage ranks: at most ten, unique, only on live work; the dashboard lists them first
check("two trackers cannot share a rank, and a rank is 1–10 on open, unparked work",
      any("also on" in p for p in gti.lint([dict(_live[0], rank=1, status="In Progress"), dict(_live[1], rank=1, status="In Progress")]))
      and any("`rank:` is 1" in p for p in gti.lint([dict(_live[0], rank=11, status="In Progress")]))
      and any("`rank:` is 1" in p for p in gti.lint([dict(_live[0], rank=2, status="Parked")]))
      and not any("rank" in p for p in gti.lint([dict(_live[0], rank=2, status="In Progress")])))
_rk = gti.render_html([dict(_live[0], rank=3), _live[1]])
check("ranked rows sort first and show their rank", "(x[18]||99)-(y[18]||99)" in _rk and '"#"+t[18]' in _rk)
check("the rules demand a tier judged today on every keep, and a rank list",
      "EVERY KEEP CARRIES A TIER" in gti.TRIAGE_RULES and "RANK: add `#1`" in gti.TRIAGE_RULES
      and "WRITE NOTHING ELSE INTO A TRACKER" not in gti.TRIAGE_RULES and "THE INTENT" in gti.TRIAGE_RULES)
check("a tracker without tags is not a finding", not any("tags:" in p for p in gti.lint([dict(_live[0], tags=[])])))
_tagged = gti.render_html([dict(_live[0], tags=["research"]), _live[1]])
check("a tag reaches the page as a #chip, so typing it in the filter finds the tracker", '"#research"' in _tagged)
check("tags are chrome: muted mono text, and the stylesheet gives them no colour of their own, no background, no border",
      ".k{font-size:12px;color:var(--mute)" in _tagged and "background" not in _tagged.split(".k{")[1].split("}")[0]
      and "border" not in _tagged.split(".k{")[1].split("}")[0])
check("three views — board, release, epic; a tag is found by searching it, and its chip does exactly that",
      _tagged.count('GROUPS=[["board"') == 1 and '["tag",' not in _tagged and '["suite",' not in _tagged and '["none",' not in _tagged
      and 'href="#${encodeURIComponent(x)}" class="m k"' in _tagged)
check("on the board open/all is hidden, Esc leaves the viewer, and a tracker's headings carry GitHub's slugs with a section list when long",
      '$("o").hidden=$("a").hidden=gname=="board"' in _tagged and 'e.key=="Escape"&&!$("v").hidden' in _tagged
      and 'h.id="h-"+h.textContent.toLowerCase()' in _tagged and "if(h2.length>5)" in _tagged)
_tbl = "| a | b |\n|---|---|\n| 1 | 2 |\n"
check("a table row that belongs to no table is refused: after a blank line, after a note, a wrapped cell — not inside a code fence",
      gti.orphan_rows(_tbl) == [] and gti.orphan_rows(_tbl + "\n| 3 | 4 |\n") == [5]
      and gti.orphan_rows(_tbl + "> a note\n| 3 | 4 |\n") == [5] and gti.orphan_rows("| a | b |\n|---|---|\n| 1 | wrapped\ncell |\n| 3 | 4 |\n") == [5]
      and gti.orphan_rows("```\n| not | a table |\n```\n") == [] and gti.orphan_rows("> | a | b |\n> |---|---|\n> | 1 | 2 |\n") == []
      and any("belongs to no table" in p for p in gti.lint([dict(_live[0], orphan_rows=[12, 13])]))
      and not any("belongs to no table" in p for p in gti.lint(_live)))
# status marks (Color System V6.4 §3): one square per row; Blocked is derived, never typed
_css = _tagged.split("<style>")[1].split("</style>")[0]
check("blue and yellow exist only inside the status-square rules — no text, no chrome, no background elsewhere",
      all(rule.startswith(".q.") for c in ("--blue", "--yellow")
          for rule in (r.strip() for r in _css.split("}")) if f"var({c})" in rule))
check("teal and coral keep their one text accent each, beside their square",
      _css.count(".go{color:var(--teal)}") == 1 and _css.count(".hot{color:var(--coral)}") == 1)
check("the status word is no longer coloured — the square carries the colour",
      't[2]=="In Progress"?"go"' not in _tagged)
_blk = gti.render_html([dict(_live[0], blocked_by=[_live[1]["id"], "Owner"]), _live[1]])
check("blockers travel as the row's last field", json.dumps([_live[1]["id"], "Owner"]) in _blk)
check("blocked is derived in the page from open blockers, and is searchable by its word",
      'blocked=t=>OPEN.has(t[2])&&t[16].some(' in _blk and '(blocked(t)?" blocked "+sl("Blocked"):"")' in _blk)
check("an epic's chapters are inset, and only in the epic view",
      'gname=="epic"&&byId.has(k)&&t[0]!=k?" c":""' in _blk and "tr.c td:first-child{padding-left" in _blk)
check("a blocker that is no tracker is refused — a typo would silently never block",
      any("blocked-by:" in p for p in gti.lint([dict(_live[0], blocked_by=["BUG-99999"])])))
check("a story is open while a chapter is — a done tracker that open work names in `epic:` is refused, and one whose chapters are done is not",
      any("A story is open" in p for p in gti.lint([dict(_live[0], id="FEAT-90010", status="Shipped"), dict(_live[1], id="BUG-90011", status="In Progress", epic="FEAT-90010")]))
      and not any("A story is open" in p for p in gti.lint([dict(_live[0], id="FEAT-90010", status="Shipped"), dict(_live[1], id="BUG-90011", status="Shipped", epic="FEAT-90010")])))
check("a tracker cannot block itself", any("blocked-by:" in p for p in gti.lint([dict(_live[0], blocked_by=[_live[0]["id"]])])))
_bl = gti.mark_blocked([dict(_live[0], status="In Progress", blocked_by=[_live[1]["id"], "Owner — the rotation ruling", "FEAT-91009"]), dict(_live[1], status="Proposed"), dict(_live[2], id="FEAT-91009", status="Shipped", blocked_by=["Owner"])])
check("Blocked is derived once for both renderings: INDEX.md says what still blocks open work and which ruling is awaited; a shipped blocker clears itself",
      _bl[0]["blocked_now"] == [_live[1]["id"], "Owner — the rotation ruling"] and _bl[2]["blocked_now"] == []
      and f"In Progress · **blocked by** {_live[1]['id']}, Owner — the rotation ruling" == gti.status_cell(_bl[0]) and gti.status_cell(_bl[1]) == "Proposed"
      and gti.ready_needs(dict(_bl[0], state="x", lines=1, provable=True), {t["id"]: t for t in _bl}) == ["clear"]
      and 'b.startsWith("Owner")' in gti.render_html(_live[:2]))
check("another tracker, or the Owner, is a valid blocker",
      not any("blocked-by:" in p for p in gti.lint([dict(_live[0], blocked_by=[_live[1]["id"], "Owner"]), _live[1]])))
_epic = dict(_live[1], state="STATE-OF-THE-EPIC")
_page = gti.render_html([dict(_live[0], epic=_epic["id"], state="CHILD-STATE"), _epic])
check("the state travels only with a tracker that IS an epic", "STATE-OF-THE-EPIC" in _page and "CHILD-STATE" not in _page)
_html_before = gti.HTML_OUT.read_text(encoding="utf-8") if gti.HTML_OUT.exists() else None
_index_before_html = gti.OUT.read_text(encoding="utf-8")
code, _, _ = run(["--html-only"])
check("--html-only exits 0 and writes the page", code == 0 and gti.HTML_OUT.exists())
check("--html-only never touches the INDEX", gti.OUT.read_text(encoding="utf-8") == _index_before_html)
code, out, _ = run(["--print-written"])
check("the page is never in the staging list (it is git-ignored)", "index.html" not in out)
gti.OUT.write_text(_index_before_html, encoding="utf-8")
if _html_before is None:
    gti.HTML_OUT.unlink(missing_ok=True)

# --- FM-006: a fork cannot supply the queue's verdict or carry another PR ------------------------------------
with tempfile.TemporaryDirectory() as _qd:
    _qr = Path(_qd).resolve()
    def _qgit(*args):
        return subprocess.run(["git", "-C", str(_qr), "-c", "commit.gpgsign=false", "-c", "core.hooksPath=/dev/null", *args],
                              check=True, capture_output=True, text=True, encoding="utf-8", env=_GIT_ENV).stdout.strip()
    _qgit("init", "-q", "-b", "main")
    (_qr / "base.txt").write_text("base\n")
    _qgit("add", "-A"); _qgit("commit", "-qm", "base")
    _qb = _qgit("rev-parse", "HEAD")
    _qgit("update-ref", "refs/remotes/origin/main", _qb)
    (_qr / "feature.txt").write_text("feature\n")
    _qgit("add", "-A"); _qgit("commit", "-qm", "feature")
    _qh = _qgit("rev-parse", "HEAD")
    _qreview = _qr / "docs/work-tracker/evidence/reviews/fork.md"
    _qreview.parent.mkdir(parents=True); _qreview.write_text("self-declared READY\n")
    _qgit("add", "-A"); _qgit("commit", "-qm", f"review: READY\n\nReviewed: {_qh}")
    _qv = _qgit("rev-parse", "HEAD")
    gti.configure(_qr)
    _qpr = dict(number=1, title="contribution", headRefName="feature", headRefOid=_qv, baseRefName="main",
                mergeable="MERGEABLE", mergeStateStatus="CLEAN", createdAt="2026-09-30T10:00:00Z", isCrossRepository=True)
    _qgit("remote", "add", "origin", "https://github.com/example/synthetic.git")
    _qrun = subprocess.run
    def _qforge(cmd, **kwargs):
        if cmd[0] == "synthetic-gh":
            fields = cmd[cmd.index("--json") + 1].split(",")
            return subprocess.CompletedProcess(cmd, 0, json.dumps([{k: _qpr[k] for k in fields}]), "")
        if cmd[:3] == ["git", "fetch", "--quiet"]:
            return subprocess.CompletedProcess(cmd, 0, "", "")
        return _qrun(cmd, **kwargs)
    with patch.object(gti.shutil, "which", return_value="synthetic-gh"), patch.object(gti.subprocess, "run", side_effect=_qforge):
        _qprs, _qerr = gti.forge_prs()
    check("FM-006: the forge read preserves whether the PR comes from a fork",
          _qerr is None and _qprs[0].get("isCrossRepository") is True)
    _qwait = "wait: from a fork, read it yourself"
    _qrow = gti.queue_actions([_qpr])[0]
    check("FM-006: a fork's self-declared READY stays a wait, even with clean merge status",
          _qrow[1:] == ("wait", _qwait, ""))
    check("FM-006: the same reviewed tip from this repository keeps its merge action",
          gti.queue_actions([dict(_qpr, isCrossRepository=False)])[0][1] == "merge")
    check("FM-006: an answer-named fork still requires the Owner's reading",
          gti.queue_actions([dict(_qpr, headRefName="answer/fm-006")])[0][1:3] == ("wait", _qwait))
    _qown = dict(_qpr, number=2, headRefOid=_qh, isCrossRepository=False)
    _qrows = {p["number"]: (kind, action) for p, kind, action, _ in gti.queue_actions([_qpr, _qown])}
    check("FM-006: a fork containing another PR cannot tell the Owner to close that PR",
          _qrows[2] == ("wait", f"wait: no verdict on {_qh[:7]}"))
    _qgit("checkout", "-q", "-b", "unrelated-fork", _qb)
    _qreview.parent.mkdir(parents=True, exist_ok=True); _qreview.write_text("READY for someone else's tip\n")
    _qgit("add", "-A"); _qgit("commit", "-qm", f"review: READY\n\nReviewed: {_qh}")
    _qrows = {p["number"]: (kind, action) for p, kind, action, _ in gti.queue_actions(
        [dict(_qpr, headRefOid=_qgit("rev-parse", "HEAD")), _qown])}
    check("FM-006: an unrelated fork's fabricated verdict cannot promote another PR",
          _qrows[2] == ("wait", f"wait: no verdict on {_qh[:7]}"))
    _qgit("checkout", "-q", "-b", "wraps-fork", _qh)
    (_qr / "own.txt").write_text("own\n"); _qgit("add", "-A"); _qgit("commit", "-qm", "own work on the fork's head")
    _qrows = {p["number"]: (kind, action) for p, kind, action, _ in gti.queue_actions(
        [dict(_qpr, headRefOid=_qh), dict(_qown, number=3, headRefOid=_qgit("rev-parse", "HEAD"))])}
    check("FM-006: a fork inside another PR's head waits for the Owner, never closes with it", _qrows[1] == ("wait", _qwait))
    _qgit("checkout", "-q", "-b", "conflict-fork", _qb)
    (_qr / "base.txt").write_text("fork\n"); _qgit("add", "-A"); _qgit("commit", "-qm", "fork edits base")
    _qcf = _qgit("rev-parse", "HEAD")
    _qgit("checkout", "-q", "--detach", _qb)
    (_qr / "base.txt").write_text("main\n"); _qgit("add", "-A"); _qgit("commit", "-qm", "main edits base")
    _qgit("update-ref", "refs/remotes/origin/main", _qgit("rev-parse", "HEAD"))
    check("FM-006: a conflicting fork waits for the Owner's reading, not on its conflict",
          gti.queue_actions([dict(_qpr, headRefOid=_qcf)])[0][1:3] == ("wait", _qwait))
gti.configure(ROOT)

# `last_worked_on` and `repos_naming` read git; their fixture repository lives in test_shoalmark.py.

print()
if FAILS:
    print(f"FAILED: {len(FAILS)} — {', '.join(FAILS)}")
    sys.exit(1)
print("all green")
