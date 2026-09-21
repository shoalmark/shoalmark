"""Build shoalmark's test_core.py from the origin's test file: the release axis stays behind, the live corpus becomes a synthetic one."""
import re, pathlib
SRC = pathlib.Path("/Users/hf./Documents/portdive/worktrees/feat180-close/scripts/test_gen_tracker_index.py")
DST = pathlib.Path("/Users/hf./Documents/shoalmark/test_core.py")
L = SRC.read_text(encoding="utf-8").split("\n")
def section(start_pat, end_pat):
    a = next(i for i, l in enumerate(L) if l.startswith(start_pat)); b = next(i for i, l in enumerate(L) if i > a and l.startswith(end_pat))
    return a, b
cuts = [section('print("\\nFEAT-086 S4 — the suite roster', 'print("\\nBUG-204 — a duplicate identity'),          # rosters + the three staging sections that lean on them
        section("# FEAT-180 — `surface:` is gone", "# FEAT-180 — a new filing meets a second reader")]
keep = [l for i, l in enumerate(L) if not any(a <= i < b for a, b in cuts)]
s = "\n".join(keep)
head_end = s.index("def run(argv):")
HEADER = '''"""The core's behaviour, pinned — the checks the tracker carried in the repository it was cut from, moved here with it.

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

HERE = Path(__file__).resolve().parent
_spec = importlib.util.spec_from_file_location("gti", HERE / "shoalmark.py")
gti = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(gti)

# --- the synthetic corpus: a story with a chapter, open and done work of every status, a blocker, a tag -------------
_TMP = tempfile.TemporaryDirectory()
ROOT = Path(_TMP.name).resolve()
_WT = ROOT / "docs" / "work-tracker"
_WT.mkdir(parents=True)


def _file(tid, status, extra="", title="a tracker", body="## What is true now\\n\\n**One thing is left.**\\n\\n## Done when\\n\\nit is.\\n"):
    (_WT / f"{tid}-{title.replace(' ', '-')}.md").write_text(
        f'---\\nid: {tid}\\nstatus: {status}\\n{extra}hook: "the hook of {tid} — {title}"\\n---\\n\\n# {tid} — {title}\\n\\n{body}', encoding="utf-8")


_file("FEAT-001", "Shipped", title="the first feature")
_file("FEAT-002", "In Progress", 'intent: "for — a · so that — b · never — c"\\ntriaged: 2026-01-05\\ntier: P1\\nrank: 1\\nnext: build\\nkind-of-problem: complicated\\n', title="a story")
_file("FEAT-003", "In Progress", "epic: FEAT-002\\ntriaged: 2026-01-05\\ntier: P2\\n", title="a chapter",
      body="## What is true now\\n\\n**Left: one run.** See [the story](FEAT-002-a-story.md).\\n\\n## Done when\\n\\nit ran.\\n")
_file("FEAT-004", "Proposed", "tags: research\\n", title="a question")
_file("BUG-001", "Closed", title="an old bug")
_file("BUG-002", "Parked", "triaged: 2026-01-05\\ntier: P3\\nblocked-by: FEAT-002, Owner — the ruling\\n", title="a parked bug")
_file("BUG-003", "Proposed", title="a fresh bug")
_file("ALIGN-001", "Shipped", title="parity")
(_WT / "TRIAGE.md").write_text("# Triage\\n\\n## The intent\\n\\n- **for** — consolidation\\n- **never** — a Jira clone\\n\\n## The current path\\n\\n"
                               "1. [FEAT-002](FEAT-002-a-story.md) to its end.\\n\\n## Passes\\n\\nNewest first.\\n\\n*None yet.*\\n", encoding="utf-8")
(ROOT / "shoalmark.toml").write_text('name = "synthetic"\\n[kinds]\\nFEAT = "Features"\\nBUG = "Bugs"\\nALIGN = "Alignment"\\n'
                                       '[considered_from]\\nFEAT = 189\\nBUG = 334\\nALIGN = 1000\\n', encoding="utf-8")
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


'''
s = HEADER + s[head_end:]
def sub(old, new, count=1):
    global s
    assert s.count(old) == count, (s.count(old), old[:80])
    s = s.replace(old, new)
# a violation that is the core's own
sub('''violating = {
    "id": "FEAT-999", "kind": "FEAT", "status": "Proposed", "version": "0.14.15",
    "surface": "—", "suite": "—", "target": "—", "hook": "synthetic", "live": "—",
    "links": [],
}''', '''violating = {"id": "FEAT-999", "kind": "FEAT", "status": "Proposed", "hook": "synthetic", "links": [], "tags": ["no-such-tag"]}''')
sub('check("LD2 fires on `version:` on a Proposed tracker", len(problems) == 1)', 'check("a tag outside the vocabulary is one violation", len(problems) == 1)')
sub('''    return {
        "id": tid, "kind": "FEAT", "status": "Proposed", "version": "—",
        "surface": "—", "suite": "—", "target": "—", "hook": "synthetic",
        "live": "—", "links": links,
    }''', '''    return {"id": tid, "kind": "FEAT", "status": "Proposed", "hook": "synthetic", "links": links}''')
s = s.replace("FEAT-038-recordable-instruments-schema.md", "FEAT-002-an-older-slug.md").replace("FEAT-038-*.md", "FEAT-002-*.md").replace("exactly one FEAT-038 on disk", "exactly one FEAT-002 on disk")
sub('check("stale INDEX says how to fix it", "gen-tracker-index.py" in err)', 'check("stale INDEX says how to fix it", gti.CMD in err)')
sub(r"""\[\], \d+, \["", false\]\]', _tri)""", r"""\[\], \d+, \["", false\], \{\}, \{\}\]', _tri)""")
s = s.replace("FEAT-180](FEAT-180-knowledge-base-consolidation.md) to its end", "FEAT-002](FEAT-002-a-story.md) to its end")
s = s.replace("FEAT-180 to its end", "FEAT-002 to its end").replace('"](FEAT-180" not in', '"](FEAT-002" not in')
sub('"Stage 2 means reducing" in gti.triage_home()["intent"]', '"consolidation" in gti.triage_home()["intent"]')
sub("check(\"the three open stories carry the Owner's intent, and their chapters read it\",", "check(\"a story carries the Owner's intent in its front matter\",")
sub('for i in ("FEAT-180", "BUG-327", "FEAT-124")))', 'for i in ("FEAT-002",)))')
sub(''' and "| build | — | kind, target |" in _kd(next="build", targets=[("?", "0.16.x")]) and "| owner | *complicated* | — |" in _kd(next="owner", targets=[("rs-server", "0.16.x")])''', '')
sub('gti.CONSIDERED_FROM == {"FEAT": 189, "BUG": 334})', 'gti.CONSIDERED_FROM == {"FEAT": 189, "BUG": 334, "ALIGN": 1000})')
a = s.index("# FEAT-180 — the keep test stands on `last_worked_on`"); e = s.index("\nprint()\nif FAILS:")
s = s[:a] + "# `last_worked_on` and `repos_naming` read git; their fixture repository lives in test_shoalmark.py.\n" + s[e:]
# provenance from the origin's tracker stays out of this repository's labels and comments
s = re.sub(r'(?m)^(\s*#\s|print\("\\n)(?:FEAT|BUG)-\d+(?: S\d+)? — ', r'\1', s)      # comment lines and section headers only — never inside a fixture's text
sub(""", ["complex", false]]' in _pg""", """, ["complex", false], {}, {}]' in _pg""")
s = re.sub(r' \((?:Owner|independent review)[^()]*20\d\d-\d\d-\d\d[^()]*\)', '', s)
DST.write_text(s, encoding="utf-8")
print("written", len(s.split("\n")), "lines")
