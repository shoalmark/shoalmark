#!/usr/bin/env python3
"""fathom-mark — a work tracker that lives in the repository it tracks.

Markdown trackers with a small front matter, and one command that reads them all:

    fathom_mark.py                 regenerate INDEX.md and the local board (idempotent)
    fathom_mark.py --check         read-only gate: write nothing, fail on drift or a violation
    fathom_mark.py --related "…"   before filing: the existing trackers closest to an id or to words
    fathom_mark.py --new KIND "…"  file a tracker — it prints what is related first, and the gate
                                   refuses the file until `considered:` says what it was held against
    fathom_mark.py --triage        a triage pass: the seat judges a worksheet, the command applies it
    fathom_mark.py --schema        every front-matter key, its shape, who writes it
    fathom_mark.py --init          scaffold the tracker directory, TRIAGE.md and fathom-mark.toml
    fathom_mark.py --vendor DIR    copy this tool, pinned by hash, into another repository

The INDEX is a *pointer*, not a copy: each row is a terse hook and a machine-read status; the detail
lives in the tracker. `status` is the code lifecycle — `Shipped` means merged, not deployed.

Both modes FAIL on a ledger-integrity violation: a gate that always lands green is not a gate.
Configuration is `fathom-mark.toml` at the repository root; every key has a default.
"""

import argparse
import datetime
import difflib
import hashlib
import collections
import json
import math
import os
import pathlib
import re
import shutil
import subprocess
import sys
import tomllib

__version__ = "0.1.0"
HERE = pathlib.Path(__file__).resolve().parent
MARKED = HERE / "vendor" / "marked-18.0.13.umd.js"      # the one vendored, pinned third-party file (marked, MIT)
CONFIG_NAME = "fathom-mark.toml"
DEFAULTS = {
    "name": "",                                  # shown in the board's title; the directory name when empty
    "tracker_dir": "docs/work-tracker",
    "kinds": {"FEAT": "Features", "BUG": "Bugs"},  # id prefix -> the INDEX section it is listed under
    "considered_from": {},                       # kind -> first number that must carry `considered:`; default 1
    "blob": "",                                  # URL prefix for a tracker file on the forge; empty = local links
    "triage_days": 7,
    "tags": {
        "research": "explores a question; commits to nothing being built",
        "security": "credentials, exposure, access — a fix or a finding",
        "process": "how the work is done: rules, gates, tooling, the tracker itself",
    },
}


def find_root(start=None):
    """The repository this run tracks: the nearest ancestor of the working directory that holds a
    fathom-mark.toml, else the git toplevel, else the working directory."""
    here = pathlib.Path(start or os.getcwd()).resolve()
    for p in (here, *here.parents):
        if (p / CONFIG_NAME).exists():
            return p
    for p in (here, *here.parents):
        if (p / ".git").exists():
            return p
    return here


def configure(root=None):
    """Bind every path, id pattern and schema shape to one repository. Called once at import for the working
    directory, and again by `--root` and by the tests."""
    global ROOT, CONFIG, TRACKER_DIR, OUT, HTML_OUT, VIEW_DIR, REPO_BLOB, TAGS, CONSIDERED_FROM, TRIAGE_DAYS
    global KINDS, KIND_LABELS, KIND_RE, TITLE_RE, TRACKER_LINK_RE, H1_ID_RE, ROW_ID_RE, _IDS, FRONT_MATTER, CMD
    ROOT = find_root(root)
    path = ROOT / CONFIG_NAME
    CONFIG = {**DEFAULTS, **(tomllib.loads(path.read_text(encoding="utf-8")) if path.exists() else {})}
    TRACKER_DIR = ROOT / CONFIG["tracker_dir"]
    OUT, HTML_OUT, VIEW_DIR = TRACKER_DIR / "INDEX.md", TRACKER_DIR / "index.html", TRACKER_DIR / "view"
    REPO_BLOB, TAGS, TRIAGE_DAYS = CONFIG["blob"], dict(CONFIG["tags"]), int(CONFIG["triage_days"])
    KIND_LABELS = dict(CONFIG["kinds"])
    KINDS = tuple(KIND_LABELS)
    if not KINDS or not all(re.fullmatch(r"[A-Z][A-Z0-9]*", k) for k in KINDS):
        raise SystemExit(f"{CONFIG_NAME}: `kinds` needs at least one id prefix, upper case — e.g. FEAT")
    CONSIDERED_FROM = {k: int(CONFIG["considered_from"].get(k, 1)) for k in KINDS}
    alt = "|".join(sorted(KINDS, key=len, reverse=True))
    _IDS = rf"(?:{alt})-\d+"
    KIND_RE = re.compile(rf"({alt})-\d+-")
    TITLE_RE = re.compile(rf"^#\s+(?:{alt})-\d+\s*[—:-]\s*(.+?)\s*$")
    H1_ID_RE = re.compile(rf"^#\s+[*_~`]*((?:{alt})-\d+)\b")
    ROW_ID_RE = re.compile(rf"^\| \[((?:{alt})-\d+)\]")
    TRACKER_LINK_RE = re.compile(rf"\]\(((?:{alt})-\d+-[a-z0-9-]+\.md)\)")
    try:
        CMD = "python3 " + str(pathlib.Path(__file__).resolve().relative_to(ROOT))
    except ValueError:
        CMD = "python3 " + str(pathlib.Path(__file__).resolve())
    FRONT_MATTER = front_matter_schema()


# `tags:` — the KIND of work. A closed vocabulary on purpose: a synonym is how tags rot. It is `[tags]` in the
# configuration, each with its meaning. At most three per tracker.
MAX_TAGS = 3
# a tag may select the CHAIN of seats a tracker runs. No such tag
# means the build chain, which is why there is no `build` tag: a default cannot be forgotten. Tags are
# multi-valued and a chain is not, so a tracker carries at most one of these.
CHAIN_TAGS = {"research"}
# A filing looks first: a new tracker carries `considered:` — what it was held against. `--related` finds the
# candidates in under a second; the gate makes running it part of filing.
RANK_MAX = 10
# ONE window — `triage_days`, 7 by default. It is the keep test (worked on in the last 7 days) and the life of a
# judgement on work in progress. The rules, the worksheet and the board all read it.
# what a worksheet row and the ranked table DERIVE about a tracker. A judged domain word
# (obvious · complicated · complex · chaos) was tried and taken out: two cold seats agreed on 5, then 4, of 10.
# What a ranked verdict names instead is the NEXT MOVE — who or what moves the tracker next. It is EXTRACTED
# from what the tracker says is left, not judged: the words are moves, in the order the rules test them.
MOVES = ("review", "run", "wait", "owner", "script", "build")
MOVE_RE = re.compile(r"\b(%s)\b" % "|".join(MOVES), re.I)
# `kind-of-problem:` — the second try at that word, built on what took the first
# one out. A cold pass never judges it: it is left, like `next:`, by a seat that has the tracker OPEN. And it is
# judged only where it says something the move has not: `script` IS obvious, `review` and `owner`
# ARE complicated, `run` and `wait` ARE complex; only a `build` can be any of them. Harm now is chaos, any move.
PROBLEM_KINDS = ("obvious", "complicated", "complex", "chaos")
KIND_OF_MOVE = {"script": "obvious", "review": "complicated", "owner": "complicated", "run": "complex", "wait": "complex"}
# THE SCHEMA of a tracker's front matter: every key a tracker may carry, the shape of
# one value, who writes it, what it says. The gate refuses a key that is not here — until then a typo
# (`kind_of_problem:`) was silently ignored, and `rank: two` read as no rank — and a value that does not fit its
# shape. `--schema` prints this table; it is the only list of keys. What one value cannot show — that an `epic:`
# exists, that a rank names one tracker, that a `version:` is a ship fact — stays in `lint`, below each key's use.
# A shape is a regular expression matched whole, case ignored; None is free text. A `# …` line is a comment.
# REQUIRED is "all" (every tracker) or "open" (open work) — widened by slice S7 in the commit that made it green:
# 84 trackers had no front matter at all, and a triage pass could not apply a verdict to the 6 open ones.
OPEN_STATUSES = ("In Progress", "Parked", "Proposed", "Reserved", "?")
_OWNER = r"Owner(?:\s+—\s+[^,]+)?"      # `Owner`, or `Owner — the ruling awaited`, in a few words and without a comma
def front_matter_schema():
    return {
        "id":              (_IDS, "all", "the filing seat", "the tracker's id — the filename's, checked against it"),
        "status":          ("|".join(OPEN_STATUSES[:-1] + ("Shipped", "Closed")), "all", "the seat that changes it",
                            "the code lifecycle, one word — `Shipped` means merged, not deployed; a date belongs in the body"),
        "hook":            (None, "open", "the filing seat", "the problem as filed, in two or three sentences — the INDEX row"),
        "epic":            (_IDS, False, "the filing seat, or a triage pass", "the STORY this tracker is a chapter of — a tracker id; chapters inherit its `intent:`"),
        "tags":            (None, False, "the filing seat", "at most %d from the vocabulary in the configuration's [tags]" % MAX_TAGS),
        "blocked-by":      (rf"(?:{_IDS}|{_OWNER})(?:\s*,\s*(?:{_IDS}|{_OWNER}))*", False, "any seat",
                            "what this open work waits on — tracker ids, and `Owner` or `Owner — <the ruling awaited>`. *Blocked* is derived from it and clears itself; it orders nothing"),
        "considered":      (rf"none|{_IDS}(?:\s*,\s*{_IDS})*", False, "the filing seat", "the existing trackers this filing was held against — listed means LOOKED AT, not merged — or none. Triage at intake: run `--related` first; the gate refuses a new tracker without this line"),
        "intent":          (None, False, "the Owner's words only", "for · so that · never — on a story; its chapters inherit it"),
        "triaged":         (r"\d{4}-\d{2}-\d{2}", False, "a triage pass", "the day a pass last gave it a verdict"),
        "tier":            (r"P[0-3]", False, "a triage pass", "how much it matters, judged against the Owner's current path"),
        "rank":            (r"\d+", False, "a triage pass", "working order, 1–%d — the first item to work on next" % RANK_MAX),
        "next":            ("|".join(MOVES), False, "the seat that ends work; a pass only where none was left", "the next move — who or what moves it next"),
        "kind-of-problem": ("|".join(PROBLEM_KINDS), False, "a seat with the tracker open — never a pass from a row",
                            "the kind of problem that is LEFT: a script does it · found by reading · found only by running · harm now"),
    }


NOW_MAX = 600              # the worksheet's Now cell: the opening of a tracker's *What is true now* — at 320 it cut
                           # mid-sentence and a reader had to open the tracker
SIZED_LINES = 600          # past this a cold session pays for the reading before it can act
DONE_RE = re.compile(r"done when|acceptance|exit criteri|definition of done|falsifier", re.I)

# an epic's "state of the epic" is the first paragraph of the current-truth head the
# doctrine already asks for (trackers-say-what-is-true-now); no new field to keep in step.
STATE_HEAD_RE = re.compile(r"^#{2,3}\s+(what is true now|current (state|truth|status)|state of play)\b", re.I)


def current_truth(body):
    lines, out, inside = body.splitlines(), [], False
    for line in lines:
        if STATE_HEAD_RE.match(line):
            inside = True
            continue
        if inside:
            if line.startswith("#") or (out and not line.strip()):
                break
            if line.strip():
                out.append(line.strip())
    text = " ".join(out)
    text = re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", text)      # [label](url) -> label
    text = re.sub(r"[*`]|^>\s*", "", text)
    if len(text) <= NOW_MAX:
        return text
    cut = text[:NOW_MAX]
    end = max(cut.rfind(". "), cut.rfind(".** "), cut.rfind("; "))
    return cut[:end + 1] + " …" if end > 200 else cut.rstrip() + "…"


TIER_RE = re.compile(r"\*\*(?:Severity\s*/\s*)?Tier:?\*{0,2}:?\s*\*{0,2}\s*(?:S[0-4]\s*·\s*)?(?:MVP-)?(P[0-3])\b")
HOOK_MAX = 120

# Canonical statuses, matched case-insensitively in priority order (first wins).
# "Shipped" outranks everything (a shipped item that was once In Progress is
# Shipped); "Closed" covers superseded/declined/wontfix.
STATUS_RULES = [
    ("Shipped", re.compile(r"\b(shipped|merged|done|complete[d]?|fixed|resolved|landed)\b", re.I)),
    ("In Progress", re.compile(r"\bin[\s-]?progress\b", re.I)),
    # `Parked` is deliberately NOT a synonym of "blocked". Blocked-on-an-action
    # someone could take today is still `In Progress` (it waits on an owner
    # login — that is a Tuesday, not a park). `Parked` means the precondition
    # DOES NOT EXIST yet, so no one can progress it however willing they are —
    # it waits on a staging box that has not been bought. The distinction is
    # "is there a next action?", and it is what keeps `In Progress` honest.
    ("Parked", re.compile(r"\bparked\b", re.I)),
    ("Reserved", re.compile(r"\breserved\b", re.I)),
    ("Proposed", re.compile(r"\b(proposed|draft|open)\b", re.I)),
    ("Closed", re.compile(r"\b(superseded|closed|declined|won['’]?t[\s-]?fix|wontfix|obsolete)\b", re.I)),
]
# Display order for grouping the table. Parked sits next to In Progress: both are
# live work, and burying it near Closed would hide exactly what it must not.
STATUS_ORDER = {
    "In Progress": 0,
    "Parked": 1,
    "Proposed": 2,
    "Reserved": 3,
    "Shipped": 4,
    "Closed": 5,
    "?": 6,
}

STATUS_LINE_RE = re.compile(r"^\s*\*{0,2}Status\*{0,2}\s*:", re.I)
TABLE_SEP_RE = re.compile(r"^\s*\|?\s*:?-{3,}:?\s*(\|\s*:?-{3,}:?\s*)*\|?\s*$")


def orphan_rows(body):
    """Body line numbers that look like table rows but belong to no table. GFM: a table is a header, a
    delimiter of the same width, then rows — and a blank line, a note or a wrapped cell ends it, after
    which every `| … |` line renders as plain text, on GitHub and in the viewer alike (53 such
    rows in 7 trackers, found when the trackers were first rendered)."""
    def width(line):
        line = line.strip()
        line = line[1:] if line.startswith("|") else line
        line = line[:-1] if line.endswith("|") and not line.endswith("\\|") else line
        return len(re.split(r"(?<!\\)\|", line))
    out, lines, fence, in_table, i = [], body.split("\n"), False, False, 0
    bare = lambda l: re.sub(r"^\s*(>\s*)*", "", l)
    while i < len(lines):
        if re.match(r"^\s*(```|~~~)", lines[i]):
            fence, in_table = not fence, False
        elif not fence:
            line = bare(lines[i])
            if not line.startswith("|"):
                in_table = False
            elif not in_table:
                nxt = bare(lines[i + 1]) if i + 1 < len(lines) else ""
                if "-" in nxt and TABLE_SEP_RE.match(nxt) and width(nxt) == width(line):
                    in_table, i = True, i + 1
                else:
                    out.append(i + 1)
        i += 1
    return out


def tier_match(body):
    """The tracker's own Tier line: in its first 40 lines, else anywhere. ONE reader — the index shows what
    a triage pass's apply step rewrites (when the two disagreed, a fresh tier never showed)."""
    head = "\n".join(body.splitlines()[:40])
    return TIER_RE.search(head) or TIER_RE.search(body)


def parse_frontmatter(text):
    """Return (frontmatter_dict, body) — flat `key: value` lines between `---`."""
    if not text.startswith("---\n"):
        return {}, text
    end = text.find("\n---", 4)
    if end == -1:
        return {}, text
    fm = {}
    for line in text[4:end].splitlines():
        if ":" in line:
            k, _, v = line.partition(":")
            fm[k.strip().lower()] = v.strip()
    return fm, text[end + 4 :]


def classify_status(raw, prose=False):
    """Map a status string to a canonical status.

    `prose=True` marks the *fallback* path — a free-text `**Status**:` line rather
    than an authoritative frontmatter `status:`. There we classify ONLY the leading
    token, never the whole sentence.

    Why: the rules are first-match-wins with `Shipped` first, and a status line
    almost always *mentions* completed work — a shipped sub-slice, a shipped
    dependency, even "token registration is shipped; only the send side is missing".
    Scanning the whole line made every such tracker `Shipped`, and left the
    `In Progress` bucket rendering zero rows.

    This is the same lesson `version` already learned one function below — prose
    cross-references are not assertions about *this* tracker. Applied to `status`
    the fix is positional rather than lexical: the tracker states its own status
    first, then talks about everything else.
    """
    if prose:
        # The declaration is the head of the line; the rest is narrative.
        raw = " ".join(re.split(r"[\s—–-]+", raw.strip())[:3])
    for name, rx in STATUS_RULES:
        if rx.search(raw):
            return name
    return "?"


def nested_git_env():
    """Run Git against a submodule, not the parent hook's repository context.

    Git exports repository-local variables while invoking hooks. In a linked
    worktree those values point at the parent's common gitdir; inherited by
    `git -C <submodule>`, they override `-C` and make the tag query inspect the
    parent instead. The generator then silently rewrites every derived live tag
    to `—` during commit even though a direct `--check` is green.
    """
    env = os.environ.copy()
    for key in ("GIT_DIR", "GIT_WORK_TREE", "GIT_INDEX_FILE", "GIT_PREFIX"):
        env.pop(key, None)
    return env


def strip_md(s):
    return re.sub(r"[*`\[\]]", "", s).strip()


def norm_dash(v):
    """Normalise an absent/placeholder frontmatter value to the em-dash marker."""
    v = (v or "").strip()
    return v if v and v not in {"-", "--", "—", "n/a", "none"} else "—"


def extract(path):
    text = path.read_text(encoding="utf-8")
    fm, body = parse_frontmatter(text)
    tracker_id = path.name.split("-")[0] + "-" + path.name.split("-")[1]

    # the two other places a tracker states its own identity. The
    # filename is the routing key; these exist to be checked against it, never
    # to override it.
    fm_id = (fm.get("id") or "").strip()
    h1_id = None
    for line in body.splitlines():
        if line.startswith("# "):
            # Emphasis wrappers are tolerated: a falsified filing strikes its id
            # through (`# ~~BUG-209~~ — CLOSED…`) and still carries
            # it — forcing the record to unstrike for a lint would be the gate
            # bending the corpus.
            m = H1_ID_RE.match(line)
            h1_id = m.group(1) if m else ""
            break

    # Title (for the hook fallback).
    title = ""
    for line in body.splitlines():
        m = TITLE_RE.match(line)
        if m:
            title = strip_md(m.group(1))
            break

    # Status line (for status + version fallback).
    status_line = ""
    for line in body.splitlines()[:60]:
        if STATUS_LINE_RE.match(line):
            status_line = line.split(":", 1)[1] if ":" in line else line
            break

    # `status:` frontmatter is authoritative and classified as-is; the prose
    # fallback is leading-token-only.
    if fm.get("status"):
        status = classify_status(fm["status"])
    elif status_line:
        status = classify_status(status_line, prose=True)
    else:
        status = "?"

    hook = fm.get("hook") or title or "(no title)"
    hook_full = hook[1:-1] if len(hook) > 1 and hook[0] == hook[-1] == '"' else hook
    tier = tier_match(body)
    orphans = [n + text[: len(text) - len(body)].count("\n") for n in orphan_rows(body)]
    # A literal `|` in a hook silently shears the row into the wrong columns. Escape before the row is assembled.
    hook = hook.replace("|", "\\|")
    if len(hook) > HOOK_MAX:
        hook = hook[: HOOK_MAX - 1].rstrip() + "…"

    return {
        "id": tracker_id,
        "num": int(tracker_id.split("-")[1]),
        "kind": tracker_id.split("-")[0],
        "file": path.name,
        "fm_id": fm_id,
        "h1_id": h1_id,
        # the body's tracker-to-tracker links, for the dangling-link
        # lint. Collected here because `extract` is the only place the file text
        # is read; `lint` sees dicts, not paths.
        "links": sorted(set(TRACKER_LINK_RE.findall(text))),
        "hook": hook,
        "title": title or "(no title)",
        "hook_full": hook_full,
        "tier": (fm.get("tier") or "").strip() if re.fullmatch(r"P[0-3]", (fm.get("tier") or "").strip()) else (tier.group(1) if tier else "—"),
        "status": status,
        # `epic: <ID>`: the one tracker this one is a chapter of.
        "epic": norm_dash(fm.get("epic")),
        "tags": [x.strip().lstrip("#") for x in (fm.get("tags") or "").split(",") if x.strip()],
        # `blocked-by: BUG-319, Owner`: what this open work waits on. Blocked is DERIVED from
        # it, never typed as a status: the mark shows while a named tracker is open (or the Owner is
        # named) and clears by itself when the blocker ships — a hand-set status would rot.
        "blocked_by": [x.strip() for x in (fm.get("blocked-by") or "").split(",") if x.strip()],
        # `considered: BUG-012, FEAT-003` (or `none`): the existing trackers this filing was
        # held against. A new tracker is the exception; the default is a slice of one that exists.
        "considered": [x.strip() for x in (fm.get("considered") or "").split(",") if x.strip()],
        # `triaged: 2026-09-20`: the day a triage pass last gave this tracker a verdict. The
        # verdict itself is already visible — its status, its epic, a hook that says where it merged —
        # except *keep*, which changes nothing; this date is what makes a kept tracker a judged one.
        "triaged": (fm.get("triaged") or "").strip(),
        # `rank: 1`: the first item to work on next. At most RANK_MAX open trackers carry one; a triage pass
        # rewrites the whole list. Tier says how much it matters; rank says what is next.
        "rank": int(fm["rank"]) if str(fm.get("rank") or "").strip().isdigit() else 0,
        # `next: run`: the next move, written by a triage pass on what it ranks. The three ready
        # marks are derived from the file, never typed (see `ready_needs`).
        "fm": fm,
        "next": (fm.get("next") or "").strip().lower(),
        # `kind-of-problem: complicated`: the kind of problem that is LEFT, which picks the dispatch.
        "problem": (fm.get("kind-of-problem") or "").strip().lower(),
        "fm_tier": (fm.get("tier") or "").strip(),
        # `intent:` the Owner's own words — for · so that · never — on a story; its chapters
        # inherit it (`intent_of`). A seat never writes one: it is captured when the Owner says it.
        "intent": (lambda v: v[1:-1] if len(v) > 1 and v[0] == v[-1] == '"' else v)((fm.get("intent") or "").strip()),
        "lines": text.count("\n") + 1,
        "reads": len(text) // 4,
        "provable": bool(DONE_RE.search(body)),
        "orphan_rows": orphans,
        "state": current_truth(body),
    }


def is_new_filing(t):
    """Open work filed under the `considered:` rule that no pass has ever dated — it has met no second reader."""
    return (t["status"] in OPEN_STATUSES and not t.get("triaged")
            and t.get("num", 0) >= CONSIDERED_FROM.get(t.get("kind"), 10 ** 9))


def owed_a_pass(t):
    """The ONE definition of what a triage pass reads, clock aside: `In Progress` work, and a new filing. The
    worksheet and the board both ask it, so the Owner's page never says *84 to triage* while the command says
    *0 trackers to judge*. Older `Proposed`, `Reserved` and `Parked` work is backlog: the current
    path restarts it, not a clock."""
    return t["status"] == "In Progress" or is_new_filing(t)


def board(t):
    """the ONE definition of where a tracker sits on the board; INDEX.md and the dashboard both
    print it. Clock-free, so a committed file never changes because a day passed. The one clock rule — a
    judgement older than TRIAGE_DAYS counts as `triage` again — lives in the page and in the worksheet."""
    if t["status"] not in ("In Progress", "Parked", "Proposed", "Reserved", "?"):
        return "done"
    if not t.get("triaged") and owed_a_pass(t):
        return "triage"
    return "progress" if t["status"] == "In Progress" else "backlog"


def blocked_now(t, by_id):
    """BLOCKED is derived, never typed: what open
    work names in `blocked-by:` that still stands — a tracker that is itself open, or the Owner, with the ruling
    awaited where the entry says it. A blocker that ships clears itself; a typed status would have to be untyped."""
    if t.get("status") not in OPEN_STATUSES:
        return []
    return [b for b in t.get("blocked_by", []) if b.startswith("Owner") or (b in by_id and by_id[b]["status"] in OPEN_STATUSES)]


def ready_needs(t, by_id):
    """which of the four derived ready marks FAIL: stated · sized · provable · clear. Coarse on
    purpose; a failing mark names the next session's job, it gates nothing, and nothing is summed from it.
    `stated` is the fix the last seat leaves — a *What is true now* head; cold readers agree on a row that
    states one clear remainder, and on none that does not."""
    fails = (("stated", not t.get("state", "-")), ("sized", t.get("lines", 0) > SIZED_LINES),
             ("provable", not t.get("provable", True)), ("clear", bool(blocked_now(t, by_id))))
    return [name for name, failed in fails if failed]


def kind_of(t):
    """(kind, judged): the `kind-of-problem:` a seat left, else what the move already says
    (`KIND_OF_MOVE`). A `build` with none has no kind — that is a named gap (`needs_of`), never a guess."""
    return (t["problem"], True) if t.get("problem") else (KIND_OF_MOVE.get(t.get("next") or "", ""), False)


def needs_of(t, by_id):
    """What open work is missing, for both renderings: the failing ready marks, `intended` where neither the
    tracker nor its story carries the Owner's intent, `kind` where a `build` names no kind of problem."""
    return (ready_needs(t, by_id) + ([] if intent_of(t, by_id) else ["intended"])
            + (["kind"] if t.get("next") == "build" and not t.get("problem") else []))


def intent_of(t, by_id):
    """The tracker's own `intent:`, else its story's — what the work is FOR, in the Owner's words."""
    return t.get("intent") or (by_id.get(t.get("epic") or "", {}).get("intent") or "")


def render(rows, kind_label):
    rows = sorted(rows, key=lambda r: (STATUS_ORDER.get(r["status"], 9), -r["num"]))
    out = [
        f"## {kind_label}\n",
        "| ID | Tier | Hook | Status | Board | Triaged |",
        "|----|------|------|--------|-------|---------|",
    ]
    for r in rows:
        out.append(
            f"| [{r['id']}]({r['file']}) | {r['tier']} | {r['hook']} | {status_cell(r)} "
            f"| {board(r)} | {r.get('triaged') or '—'} |"
        )
    out.append("")
    return "\n".join(out)


def status_cell(t):
    """The typed status, and — on open work — what still blocks it (`mark_blocked`), so a seat reading INDEX.md
    sees what the Owner's board shows in coral."""
    return t["status"] + (f" · **blocked by** {', '.join(t['blocked_now'])}".replace("|", "\\|") if t.get("blocked_now") else "")


def mark_blocked(trackers):
    by_id = {t["id"]: t for t in trackers}
    for t in trackers:
        t["blocked_now"] = blocked_now(t, by_id)
    return trackers


def render_triage(trackers):
    """the index opens with what a seat must see first, the same picture the Owner's board shows:
    the Owner's current path, verbatim from TRIAGE.md, then the ranked trackers. No clock in it."""
    ranked = sorted((t for t in trackers if t.get("rank")), key=lambda t: t["rank"])
    out = ["## Triage — the current path, and what to work on next\n",
           "> From [`TRIAGE.md`](TRIAGE.md) and each tracker's `rank:` — what the dashboard's board shows the Owner.",
           "> Everything unranked follows below by status; a triage pass (`--triage`) re-judges open work weekly.",
           "> *Kind* is the kind of problem that is left: plain where a seat judged it (`kind-of-problem:`), *italic* where the move already says it.\n",
           triage_home()["path"] or "*No current path is written — the Owner names it in `TRIAGE.md`.*", ""]
    if ranked:
        by_id = {t["id"]: t for t in trackers}
        out += ["| # | Tier | Next | Kind | Needs | ID | Hook | Status |", "|---|------|------|------|-------|----|------|--------|"]
        kind = lambda t: (lambda k, judged: (k if judged else f"*{k}*") if k else "—")(*kind_of(t))   # *italic*: from the move
        out += [f"| {t['rank']} | {t['tier']} | {t.get('next') or '—'} | {kind(t)} | {', '.join(needs_of(t, by_id)) or '—'} "
                f"| [{t['id']}]({t['file']}) | {t['hook']} | {status_cell(t)} |" for t in ranked]
    else:
        out.append("*Nothing is ranked yet — no triage pass has run.*")
    out.append("")
    return "\n".join(out)


HTML_PAGE = r"""<!doctype html>
<html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="color-scheme" content="light dark">
<title>__NAME__ — work tracker</title>
<style>
:root{--bg:#f5f3ef;--ink:#1c1b18;--dim:#5c5852;--mute:#6b675f;--line:rgba(16,33,29,.16);--teal:#077a66;--coral:#bc4337;--blue:#3d72ff;--yellow:#a07518}
@media(prefers-color-scheme:dark){:root{--bg:#07110f;--ink:#f0f2ee;--dim:#a8b3af;--mute:#929c98;--line:rgba(226,235,230,.16);--teal:#2ed7b0;--coral:#ff735f;--blue:#3d72ff;--yellow:#f9e95e}}
*{box-sizing:border-box}
/* the page paints its WHOLE ground itself and says it is dark-aware: a clean browser showed one colour, the
   Owner's showed two — something (a dark-mode extension) painted the short `html` box under the content */
html{min-height:100%;background:var(--bg);color-scheme:light dark}
body{margin:0 auto;max-width:1100px;padding:24px 16px;background:var(--bg);color:var(--ink);font:15px/1.45 system-ui,sans-serif}
.m,input,th,button{font-family:"Berkeley Mono",ui-monospace,monospace}
header{display:flex;gap:12px;align-items:baseline;flex-wrap:wrap;margin-bottom:12px}
input{flex:1;min-width:200px;padding:8px 0;border:0;border-bottom:1px solid var(--line);background:none;color:var(--ink);font-size:15px;outline:0}
input:focus{border-color:var(--ink)}
button{border:0;background:none;color:var(--mute);font-size:12px;letter-spacing:.06em;text-transform:uppercase;cursor:pointer;padding:0}
button[aria-pressed=true]{color:var(--ink)}
#n{color:var(--dim);font-size:13px}
table{width:100%;border-collapse:collapse}
th{text-align:left;color:var(--mute);font-size:11px;font-weight:400;letter-spacing:.08em;text-transform:uppercase;padding:6px 8px 6px 0}
td{padding:7px 8px 7px 0;border-top:1px solid var(--line);vertical-align:top}
td.m{font-size:13px;white-space:nowrap;color:var(--dim)}
a{color:inherit;text-decoration:none}a:hover{text-decoration:underline}
tr.t{cursor:pointer}
.hot{color:var(--coral)}.go{color:var(--teal)}
/* status is data: one tiny 5px square leads each row and is the only coloured pixel
   status gets. Unfilled = nothing started; filled = started or ended; the colour says which:
   blue in progress · teal shipped · yellow parked · coral blocked · muted closed. The word stays
   in its column — the square is never the only carrier. */
.q{display:inline-block;width:5px;height:5px;margin-right:8px;border:1px solid var(--mute);vertical-align:middle}
.q.y{background:var(--yellow);border-color:var(--yellow)}.q.t{background:var(--teal);border-color:var(--teal)}
.q.b{background:var(--blue);border-color:var(--blue)}.q.r{background:var(--coral);border-color:var(--coral)}
.q.z{background:var(--mute)}
#p{color:var(--dim);font-size:14px;white-space:pre-line;max-width:90ch;margin:4px 0 10px;padding-left:12px;border-left:2px solid var(--line)}
#p a{color:var(--ink);text-decoration:underline}
#l{color:var(--mute);font-size:11px;margin:0 0 10px}#l .q{margin:0 5px 0 12px}#l .q:first-child{margin-left:0}
tr.c td:first-child{padding-left:20px}
/* tags are chrome, not data: muted mono text — no pill, no border, no colour. Coral also marks
   P0/P1 and teal marks live: both say what the square says — needs you now, and done. */
.k{font-size:12px;color:var(--mute);margin-left:8px;white-space:nowrap}
.h td{border:0;padding:0 8px 12px 0;color:var(--dim);font-size:14px}
.h div{font-size:12px;margin-top:4px}.h a{margin-right:4px}.off{color:var(--mute)}
.g td{border:0;padding:22px 0 4px;font-size:13px;color:var(--dim);cursor:pointer}
.s td{border:0;padding:0 0 8px 14px;color:var(--dim);font-size:14px;max-width:80ch}.g b{color:var(--ink);font-weight:600;font-size:15px}
/* the viewer — one tracker, rendered, READ-ONLY: no editing, no state, no server */
#v{max-width:900px}#v .f{margin:6px 0 2px;white-space:normal}#v .md a{text-decoration:underline}
#v h1{font-size:22px;margin:18px 0 10px}#v h2{font-size:17px;margin:28px 0 8px}#v h3,#v h4{font-size:15px;margin:20px 0 6px}
#v table{display:block;overflow-x:auto;margin:12px 0;font-size:13px}#v th,#v td{padding-right:12px}#v li{margin:2px 0}
#v code{font:13px "Berkeley Mono",ui-monospace,monospace;color:var(--dim)}#v pre{padding:12px;overflow:auto;border:1px solid var(--line)}
#v [data-s]{cursor:pointer;text-decoration:underline}#v .toc{white-space:normal;line-height:1.9;margin:10px 0}
#v blockquote{margin:12px 0;padding-left:12px;border-left:2px solid var(--line);color:var(--dim)}
@media(max-width:640px){.x{display:none}}
</style>
<div id="B"><header><input id="q" placeholder="search — id, tier, status, words · blocked · untriaged · ~ID = its neighbours" autofocus>
<button id="g" aria-pressed="true"></button><button id="o" aria-pressed="true">open</button><button id="a" aria-pressed="false">all</button><span id="n" class="m"></span></header>
<p id="l" class="m"><i class="q"></i>proposed<i class="q b"></i>in progress<i class="q y"></i>parked<i class="q r"></i>blocked<i class="q t"></i>shipped<i class="q z"></i>closed</p>
<p id="p"></p>
<table><thead><tr><th>id<th>tier<th>status<th>title</thead><tbody id="b"></tbody></table></div>
<article id="v" hidden></article>
<script>__MARKED__</script>
<script>
// row = [id, tier, status, —, —, file, title, hook, num, —, —, —, [linked ids], epic, state, [#tags], [blocked_by], triaged, rank, board, [ready marks that fail — open work only], next move, intent (own or its story's), the story it is inherited from, [date, verdict, reason] of the newest pass, tokens to read it, [kind of problem, judged — else it is from the move]]
const BLOB=__BLOB__,HOME=__HOME__,T=[
__ROWS__
];
const OPEN=new Set(["In Progress","Parked","Proposed","Reserved","?"]),$=i=>document.getElementById(i),
esc=s=>s.replace(/[&<>"]/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[c])),
dec=s=>{try{return decodeURIComponent(s)}catch(e){return s}},          // `#100%` must not blank the page
byId=new Map(T.map(t=>[t[0],t])),inb=new Map();
for(const t of T)for(const l of t[12])inb.set(l,[...(inb.get(l)||[]),t[0]]);
EPICS=new Set(T.map(t=>t[13])),
GROUPS=[["board",t=>board(t)],["epic",t=>t[13]!="—"?t[13]:EPICS.has(t[0])?t[0]:"—"]],   // two views — search covers the tags
// blocked is derived, never typed: open work whose named blocker is still open (or is the Owner)
blocked=t=>OPEN.has(t[2])&&t[16].some(b=>b.startsWith("Owner")||byId.has(b)&&OPEN.has(byId.get(b)[2])),
// the board — the generator puts every tracker in exactly one of progress · triage · backlog · done (the same
// word INDEX.md prints); `triaged` repeats the
// newest pass under `triage`. A judgement on work in progress holds __DAYS__ days, then it is back in `triage`; parked work does not go stale.
LAST=T.reduce((m,t)=>t[17]>m?t[17]:m,""),
fresh=t=>!!t[17]&&Date.now()-Date.parse(t[17])<(__DAYS__+1)*864e5,   // through day __DAYS__ inclusive — the same day the command stops calling it fresh
recent=t=>!!t[17]&&t[17]==LAST,
untriaged=t=>t[19]=="triage"||t[2]=="In Progress"&&!fresh(t),   // exactly what the next `--triage` lists: the generator's word, and work in progress judged too long ago
BOARD={progress:"kept by triage — by rank, then tier",
triage:"what the next --triage lists — in progress and unjudged or judged over __DAYS__ days ago, and new filings",
triaged:LAST?"judged "+LAST+" — each also sits in its own section":"no triage pass has run yet",
backlog:"waiting — P0 to P3, then untiered, then parked",done:"shipped or closed"},
board=t=>[...(recent(t)?["triaged"]:[]),untriaged(t)?"triage":t[19]],   // t[19] is the generator's; staleness is the one clock rule, and only work in progress goes stale
MARK={"In Progress":"b","Shipped":"t","Parked":"y","Closed":"z"},mark=t=>blocked(t)?"r":t[2].startsWith("Shipped")?"t":MARK[t[2]]||"",
ids=s=>esc(s).replace(/\b(?:__KINDS__)-\d+\b/g,i=>byId.has(i)?`<a href="#=${i}">${i}</a>`:i),   // TRIAGE.md — an id opens its tracker rendered, as in a row
chips=(ids,arrow,to="~")=>ids.length?`<div class="m">${arrow} `+ids.map(i=>`<a href="#${to}${i}" class="${byId.has(i)&&OPEN.has(byId.get(i)[2])?"":"off"}">${i}</a>`).join(" ")+"</div>":"";
let all=false,gi=0,shut=new Set(),touched=new Set();
function draw(){
  const q=$("q").value.trim(),hood=q[0]=="~"&&byId.get(q.slice(1).toUpperCase()),words=q.toLowerCase().split(/\s+/).filter(Boolean);
  const near=hood&&new Set([hood[0],...hood[12],...(inb.get(hood[0])||[])]),[gname,gkey]=GROUPS[gi],every=all||gname=="board";
  const rows=T.filter(t=>hood?near.has(t[0]):(every||OPEN.has(t[2]))&&words.every(w=>(t.join(" ")+(blocked(t)?" blocked":"")+(untriaged(t)?" untriaged":"")).toLowerCase().includes(w)))
    .sort((x,y)=>(x[2]=="Parked")-(y[2]=="Parked")||((x[18]||99)-(y[18]||99))||(x[1]<y[1]?-1:x[1]>y[1]?1:0)||y[8]-x[8]);
  const groups=new Map(),order=Object.keys(BOARD);
  for(const t of rows)for(const k of[].concat(gkey(t)))groups.set(k,[...(groups.get(k)||[]),t]);
  if(gname=="board"&&!q&&!hood)for(const k of order)groups.set(k,groups.get(k)||[]);   // the board always shows its five — an empty section is an answer
  const keys=[...groups.keys()].sort(gname=="board"?(a,b)=>order.indexOf(a)-order.indexOf(b):(a,b)=>(a=="—")-(b=="—")||(a<b?-1:a>b));
  // epics start folded — the list of stories is the answer; a search or a neighbourhood opens them
  // …so does "no tag", and so does the board below `triage` — what is kept and what is owed stay open; `triaged` keeps its pass paragraph
  for(const k of keys)if((gname=="epic"||gname=="board"&&order.indexOf(k)>1)&&!q&&!touched.has(gname+k))shut.add(gname+k);
  $("b").innerHTML=keys.map(k=>{
    const g=groups.get(k);
    const kids=gname=="epic"&&byId.has(k)?T.filter(t=>t[13]==k):[],open=kids.filter(t=>OPEN.has(t[2])),folded=shut.has(gname+k)&&!q;
    const story=kids.length?` · ${kids.length} chapter${kids.length==1?"":"s"}: ${kids.length-open.length} done · <span class="${open.some(t=>t[1]<"P2")?"hot":""}">${open.length} open</span>${open.some(t=>t[17])?` · triaged ${open.filter(t=>t[17]).length}/${open.length}`:""}`:"";
    const state=gname=="epic"&&byId.has(k)&&byId.get(k)[14]?`<tr class="s"><td colspan="4">${esc(byId.get(k)[14])}</tr>`:gname=="board"&&k=="triaged"&&HOME.last?`<tr class="s"><td colspan="4">${ids(HOME.last)}</tr>`:"";
    g.sort((x,y)=>(y[0]==k)-(x[0]==k));
    const head=`<tr class="g" data-k="${esc(gname+k)}"><td colspan="4" class="m">${folded?"▸":"▾"} <b>${esc(k=="—"?"no "+gname:k)}</b>${gname=="epic"&&byId.has(k)?" "+esc(byId.get(k)[6]):""}${story||" · "+g.length}${gname=="board"?" · "+BOARD[k]:""}</tr>${state}`;
    return head+(folded?"":g.map(t=>`<tr class="t${gname=="epic"&&byId.has(k)&&t[0]!=k?" c":""}"><td class="m"><i class="q ${mark(t)}"></i><a href="#=${t[0]}">${t[0]}</a><td class="m ${t[1]<"P2"?"hot":""}">${t[18]?"#"+t[18]+" ":""}${t[1]}${t[21]?" → "+esc(t[21]):""}<td class="m">${blocked(t)?"Blocked":t[2]}<td><a href="${BLOB+esc(t[5])}">${esc(t[6])}</a>${t[15].map(x=>`<a href="#${encodeURIComponent(x)}" class="m k">${esc(x)}</a>`).join("")}</tr><tr class="h" hidden><td colspan="4">${esc(t[7])}${blocked(t)?`<div class="m">${esc(t[2])} · blocked by ${t[16].map(b=>byId.has(b)?`<a href="#~${b}">${b}</a>`:esc(b)).join(" ")}</div>`:""}${t[17]?`<div class="m">triaged ${esc(t[17])}${t[20].length?" · needs "+t[20].join(", "):""}</div>`:""}${chips(t[12],"→")}${chips(inb.get(t[0])||[],"←")}</tr>`).join(""))}).join("");
  const hot=rows.filter(t=>OPEN.has(t[2])&&t[1]<"P2").length,go=rows.filter(t=>t[2]=="In Progress").length,stuck=rows.filter(blocked).length;
  $("n").textContent=`${rows.length} ${hood?"around "+hood[0]:every?"trackers":"open"} · ${hot} P0/P1 · ${go} in progress${stuck?` · ${stuck} blocked`:""}${rows.some(t=>t[17])?` · ${rows.filter(untriaged).length} untriaged`:""}`;
  $("o").hidden=$("a").hidden=gname=="board";   // the board shows everything — open/all has nothing to say there
  $("g").textContent="by "+gname;$("p").innerHTML=gname=="board"&&!q&&HOME.path?"<b>the current path</b> — __HOME_PATH__\n"+ids(HOME.path)+"\n\n"+(w=>`<b>waiting for you: ${w.length}</b>${w.length?" — open work whose next move is the Owner's: "+w.slice(0,14).map(t=>`<a href="#=${t[0]}">${t[0]}</a>`).join(" · ")+(w.length>14?" …":""):""}`)(T.filter(t=>OPEN.has(t[2])&&t[21]=="owner")):"";
  history.replaceState(null,"","#"+encodeURIComponent(q));
}
$("b").onclick=e=>{
  const g=e.target.closest("tr.g");
  if(g){const k=g.dataset.k;touched.add(k);shut.has(k)?shut.delete(k):shut.add(k);return draw()}
  const r=e.target.closest("tr.t");if(r&&e.target.tagName!="A")r.nextElementSibling.hidden^=1};
$("q").oninput=draw;
$("g").onclick=()=>{gi=(gi+1)%GROUPS.length;draw()};
for(const[id,v]of[["o",false],["a",true]])$(id).onclick=()=>{all=v;$("o").setAttribute("aria-pressed",!v);$("a").setAttribute("aria-pressed",v);draw()};
onkeydown=e=>{if(e.key=="/"&&document.activeElement!=$("q")){e.preventDefault();$("q").focus()}if(e.key=="Escape"&&!$("v").hidden)location.hash=""};
// the viewer: `#=FEAT-180` shows that tracker rendered. Markdown comes from view/<ID>.js (a script tag works from
// disk, a fetch does not); embedded HTML is shown, never run; bare ids and tracker links stay inside the page.
const MD=new Map(),TID=/(?:__KINDS__)-\d+\b/;
marked.use({renderer:{html:k=>esc(k.raw||k.text||"")},extensions:[{name:"tid",level:"inline",start:s=>s.match(new RegExp("\\b"+TID.source))?.index,
  tokenizer(s){if(this.lexer.state.inLink)return;const m=new RegExp("^"+TID.source).exec(s);if(m&&byId.has(m[0]))return{type:"tid",raw:m[0]}},
  renderer:k=>`<a href="#=${k.raw}">${k.raw}</a>`}]});
V=(id,md)=>{MD.set(id,md);if(dec(location.hash)=="#="+id)view(id)};
function view(id){
  const v=$("v"),t=byId.get(id);$("B").hidden=true;v.hidden=false;scrollTo(0,0);
  if(!MD.has(id)){const s=document.createElement("script");s.src="view/"+id+".js";
    s.onerror=()=>v.innerHTML=`<p class="m"><a href="#">← board</a> · no rendered copy of ${id} — run __CMD__ --html-only</p>`;
    v.innerHTML=`<p class="m">${id} …</p>`;return document.head.append(s)}
  const facts=[blocked(t)?"Blocked":t[2],t[1]!="—"&&t[1],t[18]&&"#"+t[18],board(t).at(-1),t[25]&&"reads "+(t[25]/1000).toFixed(1)+"k",t[17]&&"triaged "+t[17],...t[15]];
  v.innerHTML=`<p class="m"><a href="#">← board</a> · <a href="#~${id}">neighbours</a> · <a href="${esc(t[5])}">file</a>${BLOB?` · <a href="${BLOB+esc(t[5])}">forge</a>`:""}</p>
<p class="m f"><i class="q ${mark(t)}"></i>${facts.filter(Boolean).map(esc).join(" · ")}${t[13]!="—"?` · epic <a href="#=${esc(t[13])}">${esc(t[13])}</a>`:""}</p>
${OPEN.has(t[2])||t[22]||t[24].length?`<p class="m hd"><b>intent</b> — ${t[22]?esc(t[22])+(t[23]?` <a href="#=${esc(t[23])}">(from ${esc(t[23])})</a>`:""):"<i>missing — the Owner states it on the tracker or its story</i>"}<br>
<b>verdict</b> — ${t[24].length?`<code>${esc(t[24][1])}</code> · ${esc(t[24][0])}${t[2]=="In Progress"&&Date.now()-Date.parse(t[24][0])>=(__DAYS__+1)*864e5?" · <i>stale — older than __DAYS__ days, it counts as untriaged again</i>":""}${t[24][2]?" · "+esc(t[24][2]):""}`:"<i>none yet — no triage pass has judged it</i>"}<br>
<b>hand-over</b> — next: ${t[21]?esc(t[21]):"<i>missing</i>"}${t[21]?" · kind: "+(t[26][0]?esc(t[26][0])+(t[26][1]?"":" <i>(from the move)</i>"):"<i>missing</i>"):""} · what is true now: ${t[20].includes("stated")?"<i>missing</i>":"stated"}${(c=>c.length?`<br>
<b>chapters</b> — ${c.length}: ${Object.entries(c.filter(x=>x[2]=="In Progress"||x[2]=="Proposed").reduce((m,x)=>(m[x[21]||"no move named"]=[...(m[x[21]||"no move named"]||[]),x[0]],m),{})).map(([k,v])=>k=="no move named"?`${v.length} with no move named`:`${esc(k)} ${v.map(i=>`<a href="#=${i}">${i}</a>`).join(" ")}`).join(" · ")||"none in progress"} · ${c.filter(x=>x[2]=="Parked").length} parked · ${c.filter(x=>!OPEN.has(x[2])).length} done`:"")(T.filter(x=>x[13]==t[0]))}${t[20].filter(n=>n!="stated"&&n!="intended").length?" · needs "+t[20].filter(n=>n!="stated"&&n!="intended").join(", "):""}</p>`:""}${chips(t[16].filter(b=>byId.has(b)),"blocked by","=")}${chips(t[12],"→","=")}${chips(inb.get(id)||[],"←","=")}<div class="md">${marked.parse(MD.get(id))}</div>`;
  for(const a of v.querySelectorAll(".md a")){const h=a.getAttribute("href")||"",m=h.match(new RegExp("^("+TID.source+")-[^/]*\\.md"));
    if(m&&byId.has(m[1]))a.href="#="+m[1];else if(h[0]=="#"&&h[1]!="="){a.removeAttribute("href");a.dataset.s=dec(h.slice(1))}else if(!/^[a-z]+:/i.test(h)&&h[0]!="#")a.href=BLOB+h}
  // headings get GitHub's slug, so a tracker's own `#section` links work; a long tracker gets its sections listed.
  // The hash belongs to the router, so these scroll by click, not by address.
  const hs=[...v.querySelectorAll(".md h2,.md h3")];
  for(const h of hs)h.id="h-"+h.textContent.toLowerCase().replace(/[^\p{L}\p{N}\s-]/gu,"").trim().replace(/\s/g,"-");
  const h2=hs.filter(h=>h.tagName=="H2");
  if(h2.length>5)v.querySelector(".md").insertAdjacentHTML("beforebegin",`<p class="m toc">${h2.map(h=>`<a data-s="${esc(h.id.slice(2))}">${esc(h.textContent)}</a>`).join(" · ")}</p>`);
}
$("v").onclick=e=>{const s=e.target.closest("[data-s]");if(s)document.getElementById("h-"+s.dataset.s)?.scrollIntoView()};
(onhashchange=()=>{const h=dec(location.hash.slice(1));if(h[0]=="="&&byId.has(h.slice(1)))return view(h.slice(1));
  $("v").hidden=true;$("B").hidden=false;$("q").value=h;draw();scrollTo(0,0)})();
</script></html>
"""


def triage_home():
    """TRIAGE.md as the command and the dashboard read it: the Owner's current path, and the newest pass."""
    home = TRACKER_DIR / "TRIAGE.md"
    text = home.read_text(encoding="utf-8") if home.exists() else ""
    part = lambda name: (re.search(rf"^## {name}\n(.*?)(?=^## |\Z)", text, re.S | re.M) or ["", ""])[1].strip()
    passes = [p for p in re.split(r"\n\s*\n", part("Passes")) if p.strip() and not p.lstrip().startswith(("Newest first", "*None"))]
    return {"path": part("The current path"), "last": passes[0] if passes else "", "intent": part("The intent")}


def write_views(trackers):
    """One `view/<ID>.js` per tracker — `V(id, markdown)`. Rewritten only when changed; strays removed."""
    VIEW_DIR.mkdir(exist_ok=True)
    keep = set()
    for t in trackers:
        _fm, body = parse_frontmatter((TRACKER_DIR / t["file"]).read_text(encoding="utf-8"))
        out, text = VIEW_DIR / f'{t["id"]}.js', f'V({json.dumps(t["id"])},{json.dumps(body, ensure_ascii=False)})\n'
        keep.add(out.name)
        if not out.exists() or out.read_text(encoding="utf-8") != text:
            out.write_text(text, encoding="utf-8")
    for stray in VIEW_DIR.glob("*.js"):
        if stray.name not in keep:
            stray.unlink()


def latest_verdicts():
    """{tracker id: [date, verdict, reason]} — the newest triage worksheet row that judged it. The verdict and
    its reason live in the pass's worksheet, never in the tracker; the page shows them where the tracker is read."""
    out = {}
    for sheet in sorted((TRACKER_DIR / "evidence" / "triage").glob("triage-*.md")):
        for tid, verdict, line, error in sheet_rows(sheet.read_text(encoding="utf-8")):
            if tid and verdict and not error:
                reason = re.split(r"(?<!\\)\|", line)[-2].strip().replace("\\|", "|")
                out[tid] = [sheet.stem[len("triage-"):], verdict, reason]
    return out


def render_html(trackers):
    """one static page: data rows + ~25 lines of vanilla JS. No dates and no
    counts are baked in (both are computed in the browser), so equal trackers give
    equal bytes. The row layout is documented once, in the page's script."""

    epics = {t.get("epic", "—") for t in trackers}
    by_id, verdicts = {t["id"]: t for t in trackers}, latest_verdicts()
    rows = [
        json.dumps(
            [t["id"], t["tier"], t["status"], "—", "—",
             t["file"], t["title"], t["hook_full"], t["num"], "—", "—",
             "—", sorted({"-".join(f.split("-")[:2]) for f in t["links"]} - {t["id"]}),
             t.get("epic", "—"), t.get("state", "") if t["id"] in epics else "",
             ["#" + x for x in t.get("tags", [])], t.get("blocked_by", []), t.get("triaged", ""), t.get("rank", 0), board(t),
             needs_of(t, by_id) if t["status"] in OPEN_STATUSES else [], t.get("next", ""),
             intent_of(t, by_id), "" if t.get("intent") or not intent_of(t, by_id) else t.get("epic", ""), verdicts.get(t["id"], []), t.get("reads", 0), list(kind_of(t))],
            ensure_ascii=False,
        ).replace("</", "<\\/")  # a hook containing "</script>" must not end the block
        for t in sorted(trackers, key=lambda t: (t["kind"], t["num"]))
    ]
    unwrap = lambda md: re.sub(r" {2,}", " ", re.sub(r"(?<!\n)\n(?!\s*\n|\s*\d+\. |\s*- )", " ", md))   # source line breaks are not the reader's
    plain = lambda md: strip_md(re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", unwrap(md)))
    home = {k: plain(v) for k, v in triage_home().items()}
    page = (HTML_PAGE.replace("__KINDS__", "|".join(sorted(KINDS, key=len, reverse=True))).replace("__NAME__", CONFIG["name"] or ROOT.name)
            .replace("__HOME_PATH__", str((TRACKER_DIR / "TRIAGE.md").relative_to(ROOT))).replace("__CMD__", CMD))
    return page.replace("__MARKED__", MARKED.read_text(encoding="utf-8")).replace("__DAYS__", str(TRIAGE_DAYS)).replace("__HOME__", json.dumps(home, ensure_ascii=False).replace("</", "<\\/")).replace("__BLOB__", json.dumps(REPO_BLOB)).replace(
        "__ROWS__", ",\n".join(rows)
    )


def identity_problems(trackers):
    """the identifier is the routing key; check it BEFORE anything renders.

    Unlike lint() findings (carried into the header's ❌ banner), an identity
    failure refuses to render at all: two files claiming one id means every
    generated view would encode ambiguous authority, and deduplicating — or
    letting the last file win — would convert an identity failure into silent
    data loss. Both write mode and --check exit EXIT_LINT with nothing written.
    """
    problems = []
    by_id = {}
    for t in trackers:
        by_id.setdefault(t["id"], []).append(t["file"])
    for tid, files in sorted(by_id.items()):
        if len(files) > 1:
            problems.append(
                f"duplicate tracker id {tid} — {len(files)} files claim it: "
                + ", ".join(sorted(files))
                + ". Repair: renumber the later filing and move its references "
                "with it; the generator never "
                "deduplicates and never lets the last file win."
            )
    for t in trackers:
        fm_shown = t["fm_id"] or "(absent)"
        h1_shown = t["h1_id"] if t["h1_id"] else "(none)"
        if t["fm_id"] and t["fm_id"] != t["id"]:
            problems.append(
                f"{t['file']}: identity drift — filename says {t['id']}, "
                f"frontmatter id: says {fm_shown}, first H1 says {h1_shown}. "
                "All three must carry the filename id."
            )
        if t["h1_id"] != t["id"]:
            problems.append(
                f"{t['file']}: H1 drift — filename says {t['id']}, first H1 says "
                f"{h1_shown}, frontmatter id: says {fm_shown}. The first H1 must "
                "carry the filename id."
            )
    return problems


_STOP = set("the a an and or of to in on for with is are was be by it its this that as at from not no into "
            "than then so if but which who what when while can could would should has have had do does did "
            "will may must more most less one two three new old own up out over under after before".split())


def related_trackers(trackers, query, limit=8):
    """The existing trackers closest to `query` — a tracker id, or free words.

    Scored by the rare words two trackers share in filename, hook and opening lines, damped by
    length so a 2,000-line epic does not win every search. It is a lead for a reader, not a verdict:
    its only job is to put the tracker that already owns the problem in front of whoever is about to file it again.
    """
    def bag(t):
        text = " ".join([t["file"].replace("-", " "), t["hook_full"], t["hook_full"], t.get("state", "")])
        return collections.Counter(w for w in re.findall(r"[a-z][a-z0-9_]{2,}", text.lower()) if w not in _STOP)
    bags = {t["id"]: bag(t) for t in trackers}
    df = collections.Counter(w for b in bags.values() for w in set(b))
    n = len(trackers)
    by_id = {t["id"]: t for t in trackers}
    qid = query.strip().upper()
    q = bags[qid] if qid in bags else collections.Counter(
        w for w in re.findall(r"[a-z][a-z0-9_]{2,}", query.lower()) if w not in _STOP)
    scored = []
    for tid, b in bags.items():
        if tid == qid:
            continue
        s = sum(min(q[w], b[w]) * math.log(1 + n / df[w]) ** 2 for w in q if w in b and df[w] <= max(2, n * 0.2))   # 1 + …: a young corpus of one tracker still scores
        if s:
            scored.append((s / (1 + math.log(1 + sum(b.values()))), by_id[tid]))
    return sorted(scored, key=lambda x: -x[0])[:limit]


TRIAGE_RULES = """\
A triage pass — {left} trackers to judge. Worksheet: {path}

THE INTENT — the Owner's own words, from {home}. Where the mechanics below leave you a choice, this decides it:
{intent}

  1. Fill Verdict and Reason, row by row, FROM THE ROW — it carries the hook and the keep test. Open a
     tracker only to decide or to finish a merge, a close or a fix.
       keep Pn      it passes the keep test — worked on in the last {days} days (the row says) — or THE CURRENT
                    PATH names it or its story, or it is P0 or P1 BY TODAY'S JUDGEMENT: harm is never parked.
                    What the path lists as NEXT, NOT NOW is not named by it: park it, unless it was worked on this week.
                    EVERY KEEP CARRIES A TIER JUDGED TODAY: P0 harm in production, or the current path is
                    blocked now · P1 on the current path · P2 next · P3 someday. What the path does not name
                    is P0 or P1 only if production is being harmed today. An inherited tier is no
                    judgement. THE CURRENT PATH is the Owner's, printed below — judge against it
       epic ID Pn   a keep that is one story with ID and does not say so yet — it becomes a chapter of ID;
                    nothing closes. A row whose Story cell already names its story is a plain keep
       park Pn      a row that fails the keep test: a real remainder, and nobody working on it.
                    The Reason says what restarts it — "the Owner ranks it" counts. P2 or P3 only — the backlog
                    is read by tier, and what is P0 or P1 is not parked
       merge ID     its open scope belongs to ID. BY HAND: move the scope there, set `status: Closed`, and the
                    first line under its title: Closed — merged into [ID](file), <date>
       close        superseded or retired — name by what; NEVER on age alone. BY HAND: `status: Closed` + that line
       fix          its status is simply wrong (merged code says Shipped). BY HAND: correct it, cite the commit
     RANK: add `#1` … `#10` to at most ten keep / epic verdicts — `keep P1 #2`. The highest rank is THE FIRST
             ITEM TO WORK ON NEXT to reach what the current path names — working order, not the path's own
             numbering. Harm in production today is ranked even where the path does not name it — after the
             path's own work, unless it blocks it. What cannot be worked on now — it waits for a date, or for another tracker's run — is
             not ranked ahead of what can. Whose move it is, the next move says: an `owner` move is work too.
     NEXT: every RANKED tracker names its NEXT MOVE — who or what moves it next. Where the Facts cell already
             says `next <move>`, the seat that last worked the tracker left it: write none, unless Now
             contradicts it. Where it does not, name it in the verdict — `keep P1 #2 run`.
             Do NOT judge how hard or how nearly done it is: EXTRACT the move from what the Now cell says
             is left (where Now is empty, from the tracker's head). Test in this order; the first that fits:
               review   it is built and a branch or pull request waits to merge: an independent review is owed first
               run      it is built, and what is owed is a run nobody has made yet — a first real run, a
                        proof on a real system — even where the Owner must attend it
               wait     nothing can move before a date or an event the tracker names
               owner    the next move is the Owner's alone: a ruling, a read of production, a deploy, a
                        rotation, a signature, a pull request only the Owner opens
               script   what is left is mechanical — a script or a checklist does it, no judgement
               build    anything else: code or a document still has to be written by a seat
               (`run`: something BUILT waits for the run · `owner`: nothing built is waiting on the Owner's act)
             A label is welcome wherever it is DECIDABLE: an unranked keep or a park may name its move too —
             for a park it says what restarts it. NEVER GUESS: where the row does not say what is left,
             write none. A merge, a close or a fix names none.
     NEW FILINGS: a row marked NEW FILING was filed since the last pass and has met no second reader — this pass
             is that reader, whatever the row's status. Its Closest cell holds what the filing says it was held
             against (`considered:`) beside the three trackers the machine finds closest, done ones included.
             OPEN every one marked NOT considered. The same work: `merge ID`. Otherwise judge the row like any other.
     THE ROW carries two cells you do not fill. NOW is the opening of the tracker's *What is true now* — what
             is left; judge from it before the Hook, which only tells the problem as it was filed. FACTS are
             DERIVED: the repos whose commits name the tracker · the tokens it costs to read · the ready marks
             that FAIL (stated: no *What is true now* · sized: over {sized} lines · provable: no done-condition ·
             clear: an open blocker). `kind <word>` is the `kind-of-problem:` a seat left with the tracker
             OPEN. You do not judge it from a row — two cold seats agreed on 5, then 4, of 10 — and the move
             already says it everywhere but on a `build`, where the ranked table shows it as needed.
  2. RUN THIS COMMAND AGAIN — every ten rows or so, and at the end. It APPLIES what you filled (`triaged:`,
     `status: Parked`, `epic:`, `tier:`, `rank:`, `next:`), refreshes INDEX.md and the board, keeps your rows, and lists what is left.
     Do not make those edits by hand. The reason lives in the worksheet.
  3. The pass is RESUMABLE: whatever carries a `triaged:` date is done. Stop when you must; the next run continues.
  4. The Owner rules by merging the pull request, and can strike any row first.
  5. This worksheet is the pass's one evidence file, and one paragraph
     under *Passes* in {home} says what the pass changed — never touch its *current path*; that is the
     Owner's.

THE CURRENT PATH — from {home}:
{current_path}
"""


def last_worked_on(path):
    """The date of the last commit that was ABOUT this tracker — a commit touching more than eight
    trackers is a sweep and says nothing about any of them, and neither does one whose subject says
    `[sweep]` (a repair run over a few trackers must not make them look worked on)."""
    log = subprocess.run(["git", "log", "--format=%H %cs %s", "--", str(path)], cwd=ROOT,
                         capture_output=True, text=True).stdout.splitlines()
    for line in log:
        commit, day, subject = (line.split(" ", 2) + [""])[:3]
        if "[sweep]" in subject:
            continue
        names = subprocess.run(["git", "show", "--name-only", "--format=", commit, "--", str(TRACKER_DIR.relative_to(ROOT))],
                               cwd=ROOT, capture_output=True, text=True).stdout.split()
        if len([n for n in names if KIND_RE.match(n.rsplit("/", 1)[-1])]) <= 8:
            return day
    return log[-1].split()[1] if log else "—"


def repos_naming():
    """{tracker id: the submodules whose branch names or commit subjects name it} — where the work happened,
    from git alone. For the worksheet only: eight `git log`s are too slow for a commit hook. A submodule that
    is not checked out is skipped — `git -C` on its empty directory would answer from the parent."""
    modules, found = ROOT / ".gitmodules", {}
    for sub in re.findall(r"^\s*path\s*=\s*(\S+)", modules.read_text(encoding="utf-8"), re.M) if modules.exists() else []:
        if not (ROOT / sub / ".git").exists():
            continue
        said = "".join(subprocess.run(["git", "-C", str(ROOT / sub), *cmd], capture_output=True, text=True,
                                      env=nested_git_env()).stdout for cmd in (["log", "--all", "--format=%s %D"], ["branch", "-r"]))
        for kind, num in re.findall(r"\b(%s)[-/](\d{1,3})\b" % "|".join(KINDS), said, re.I):
            found.setdefault(f"{kind.upper()}-{int(num):03d}", set()).add(sub.rsplit("/", 1)[-1])
    return {k: sorted(v) for k, v in found.items()}


def triage_worksheet(trackers, today, worked_on, earlier="", repos=None):
    """The worksheet of a triage pass: `In Progress` trackers no pass has dated in TRIAGE_DAYS, oldest work first —
    and every NEW FILING: open work filed under the `considered:` rule that no pass has ever dated, whatever its
    status. A fresh `Proposed` tracker used to meet no second reader at all, and `considered: none` nobody. Its row
    prints what the filing says it was held against beside the three closest trackers the machine finds, done ones
    included — shipped work is prior art too. The seat judges; no score decides, and no gate turns red because
    someone else filed. `earlier` is today's worksheet if one exists: a re-run keeps every row whose Verdict is filled."""
    judged = [l for _tid, _v, l, _e in sheet_rows(earlier)]
    done = {tid for tid, _v, _l, _e in sheet_rows(earlier) if tid}
    day = lambda d: datetime.date.fromisoformat(d) if re.fullmatch(r"\d{4}-\d{2}-\d{2}", d) else datetime.date.min
    fresh = lambda d: (datetime.date.fromisoformat(today) - day(d)).days <= TRIAGE_DAYS    # one window: the keep test, and the life of a judgement
    is_new = is_new_filing
    todo = [t for t in trackers if t["id"] not in done
            and owed_a_pass(t) and not fresh(t.get("triaged") or "")]
    open_now = [t for t in trackers if t["status"] in ("Proposed", "In Progress", "Parked", "Reserved")]
    rows = []
    for t in todo:
        last = worked_on(TRACKER_DIR / t["file"])
        near = related_trackers(trackers if is_new(t) else open_now, t["id"], limit=3 if is_new(t) else 1)
        rows.append((day(last), t, last, near))
    rows.sort(key=lambda r: (r[0], r[1]["id"]))
    lines = [f"# Triage pass — worksheet of {today}", "",
             f"Generated by `{CMD} --triage`; **the Verdict and Reason columns",
             "are the pass's record.** Verdicts: keep · merge · epic · park · close · fix — the command prints what each",
             "means and what to do. Oldest work first; a **NEW FILING** has met no second reader yet. *Last worked on* ignores sweep commits. **Now** is the opening of",
             "the tracker's *What is true now*. **Facts** are derived, not judged: repos whose commits name it · tokens",
             "to read it · the ready marks that fail.", "",
             "| Tracker | Tier | Story | Last worked on · keep test | Closest open tracker | Hook | Now | Facts | Verdict | Reason |",
             "|---|---|---|---|---|---|---|---|---|---|"]
    by_id, repos = {t["id"]: t for t in trackers}, repos or {}
    carriers = sorted({(t["id"] if t.get("intent") else t.get("epic")) for t in todo if intent_of(t, by_id)} - {None, "", "—"})
    if carriers:
        lines[-2:-2] = ["**Intent — the Owner's words; a row inherits its Story's.** Judge what is left against what the work is *for*.", ""] + [
            f"- **{c}** — {by_id[c]['intent']}" for c in carriers if c in by_id] + [""]
    for _d, t, last, near in rows:
        test = ("keep" if fresh(last) else "FAILS") + (" · NEW FILING" if is_new(t) else "")
        title = t["title"].replace("|", "\\|")
        title = title if len(title) <= 70 else title[:67] + "…"
        if is_new(t):
            held = t.get("considered") or []
            closest = (f'considered {", ".join(held) or "— nothing is written"} · closest: ' + (" · ".join(
                f'{n["id"]} ({score:.0f}, {n["status"]}) {"✓" if n["id"] in held else "NOT considered"}' for score, n in near) or "—"))
        else:
            closest = f'{near[0][1]["id"]} ({near[0][0]:.0f})' if near else "—"
        hook = t["hook_full"].replace("|", "\\|")
        hook = hook if len(hook) <= 220 else hook[:217] + "…"
        fails = ready_needs(t, by_id)
        facts = (f'repos {", ".join(repos.get(t["id"], [])) or "—"} · reads {t.get("reads", 0) / 1000:.1f}k'
                 + (f' · next {t["next"]}' if t.get("next") else "") + (f' · kind {t["problem"]}' if t.get("problem") else "") + (f' · NOT {", ".join(fails)}' if fails else ""))
        now = (t.get("state") or "").replace("|", "\\|")                       # what is left — a seat fathoms this, not the hook
        now = (now if len(now) <= NOW_MAX else now[:NOW_MAX - 1].rstrip() + "…") or "—"
        lines.append(f'| [{t["id"]}](../../{t["file"]}) — {title} | {t["tier"]} | {t.get("epic", "—")} | {last} · {test} | {closest} | {hook} | {now} | {facts} | | |')
    return "\n".join(lines + judged) + "\n", len(rows)


def set_front(text, key, value):
    """Set one flat front-matter key in place — or drop it (value None). A new key goes just above `hook:`.
    A text with no front matter is returned untouched: 84 trackers have none, and rewriting one destroyed its
    title line."""
    if not text.startswith("---\n") or text.find("\n---", 4) == -1:
        return text
    end = text.find("\n---", 4)
    lines = text[4:end].split("\n")
    at = next((i for i, l in enumerate(lines) if l.lower().startswith(key + ":")), None)
    if at is not None:
        lines[at:at + 1] = [] if value is None else [f"{key}: {value}"]
    elif value is not None:
        lines.insert(next((i for i, l in enumerate(lines) if l.lower().startswith("hook:")), len(lines)), f"{key}: {value}")
    return "---\n" + "\n".join(lines) + text[end:]




def sheet_rows(sheet):
    """(tracker id, Verdict, the row, error) for every FILLED row. The Verdict is read by COLUMN, on unescaped
    pipes: read from the end of the row, a `|` typed into the Reason made a fragment of the reason the verdict
   ."""
    lines = sheet.splitlines()
    head = next((l for l in lines if l.startswith("| Tracker |")), "")
    width = len(re.split(r"(?<!\\)\|", head)) - 2
    for l in lines:
        if not l.startswith("| ["):
            continue
        cells = [c.strip() for c in re.split(r"(?<!\\)\|", l)[1:-1]]
        m = ROW_ID_RE.match(l)
        if not m:
            yield "", "", l, f"a row does not open with a tracker link — {l[:60]!r}"
        elif width > 1 and len(cells) != width:
            if any(cells[width - 2:]):
                yield m.group(1), "", l, (f"the row has {len(cells)} cells where the sheet has {width} — a `|` inside the "
                                          "Verdict or the Reason; write it as `\\|`")
        elif cells[-2]:
            yield m.group(1), cells[-2], l, ""


def apply_verdict(text, verdict, today, ids):
    """One worksheet verdict → (the tracker's new text, what is left to do by hand, error). Mechanical lines only."""
    word = verdict.split()[0].lower() if verdict.split() else ""
    tier, other, rank = (re.search(rx, verdict) for rx in (r"\bP[0-3]\b", r"\b(?:FEAT|BUG)-\d+\b", r"#(\d+)\b"))
    if word not in ("keep", "epic", "park", "merge", "close", "fix"):
        return text, "", f"`{verdict}` is no verdict"
    if not text.startswith("---\n") or text.find("\n---", 4) == -1:
        return text, "", "the tracker has no front matter — give it one by hand first; the command will not rewrite its head"
    if rank and not 1 <= int(rank.group(1)) <= RANK_MAX:
        return text, "", f"`{verdict}` — a rank is #1 … #{RANK_MAX}"
    if word in ("keep", "epic", "park") and not tier:
        return text, "", f"`{verdict}` needs a tier judged today — `{word} … P2`"
    if word == "park" and tier.group() in ("P0", "P1"):
        return text, "", f"`{verdict}` — P0 and P1 are harm now or the current path; that is a keep, not a park"
    if word in ("epic", "merge") and (not other or other.group() not in ids):
        return text, "", f"`{verdict}` must name an existing tracker"
    if rank and word not in ("keep", "epic"):
        return text, "", f"`{verdict}` — only a keep or an epic is ranked"
    tokens = re.split(r"\s+[—–-]+\s+", verdict, maxsplit=1)[0].split()[1:]     # prose after a dash is not the verdict
    move = next((m for m in (MOVE_RE.fullmatch(tok) for tok in tokens) if m), None)
    if move and word not in ("keep", "epic", "park"):
        return text, "", f"`{verdict}` — a merge, a close or a fix ends the tracker; it names no next move"
    left = re.search(r"^next:\s*(\w+)", text[:max(text.find("\n---", 4), 0)], re.M)       # what the last seat left
    if rank and not move and not (left and left.group(1).lower() in MOVES):
        return text, "", (f"`{verdict}` is ranked, so it is about to be pulled, and its tracker names no next move — "
                          f"name it: {' · '.join(MOVES)} — `{word} … #2 run`")
    text = set_front(text, "triaged", today)
    text = set_front(text, "rank", rank.group(1) if rank else None)
    if move:                                                # a move the last seat left stands until one is named
        text = set_front(text, "next", move.group(1).lower())
    if word == "park":
        text = set_front(text, "status", "Parked")
    if word == "epic":
        text = set_front(text, "epic", other.group())
    if tier and word in ("keep", "epic", "park"):           # the body's Tier sentence is the filing seat's: five seats in
        text = set_front(text, "tier", tier.group())        # a token rewritten inside a sentence contradicts that sentence
    hand = {"merge": "move the scope, `status: Closed`, the `Closed — merged into` line",
            "close": "`status: Closed` and the `Closed —` line", "fix": "correct the status, cite the commit"}.get(word, "")
    return text, hand, ""


def apply_worksheet(sheet, sheet_is_todays, trackers, today):
    """Apply every filled row of a worksheet. Idempotent; an older sheet only reaches trackers no pass has dated.
    Every verdict is validated BEFORE anything is written: a rank is taken from its holder only by a verdict
    that stands, one rank names one row, and what was freed is logged."""
    by_id, log, errors, plan, ranks = {t["id"]: t for t in trackers}, [], [], [], {}
    for tid, verdict, _line, error in sheet_rows(sheet):
        t = by_id.get(tid)
        if error:
            errors.append(f"{tid or 'worksheet'}: {error}")
            continue
        if not t or (t.get("triaged") and not sheet_is_todays):
            continue
        if t.get("status") not in OPEN_STATUSES:          # it shipped or closed since its verdict: a same-day re-run must not
            continue                                      # rank or re-date done work, nor refuse the run over it
        path = TRACKER_DIR / t["file"]
        old = path.read_text(encoding="utf-8")
        new, hand, error = apply_verdict(old, verdict, today, by_id.keys() - {tid})
        rank = re.search(r"#(\d+)\b", verdict)
        if not error and rank and rank.group(1) in ranks:
            error = f"`{verdict}` — #{rank.group(1)} is already claimed by {ranks[rank.group(1)]} on this sheet; a rank names one tracker"
        if error:
            errors.append(f"{tid}: {error}")
            continue
        if rank:
            ranks[rank.group(1)] = tid
        plan.append((tid, verdict, path, old, new, hand))
    judged = {tid for tid, *_ in plan}
    for t in trackers:                                    # a rank names one tracker: the newest judgement that STANDS wins
        if str(t.get("rank") or "") in ranks and t["id"] not in judged:
            path = TRACKER_DIR / t["file"]
            path.write_text(set_front(path.read_text(encoding="utf-8"), "rank", None), encoding="utf-8")
            log.append(f'{t["id"]}: rank #{t["rank"]} freed — {ranks[str(t["rank"])]} holds it now')
    for tid, verdict, path, old, new, hand in plan:
        if new != old:
            path.write_text(new, encoding="utf-8")
            log.append(f"{tid}: {verdict}" + (f" — BY HAND: {hand}" if hand else ""))
    return log, errors


def schema_problems(t):
    """one tracker's front matter against FRONT_MATTER: a key that is not in the schema, a value that
    does not fit its key's shape. An empty value and a `# …` comment line are neither."""
    if "fm" not in t:                       # a synthetic tracker, not one read from a file
        return []
    if not t["fm"]:
        return [f'{t["id"]}: no front matter — every tracker opens with `---`, `id:`, `status:` (open work: `hook:`), `---`. '
                f'`--schema` prints the keys; without one a triage pass cannot apply a verdict to it']
    out = []
    for key, value in t["fm"].items():
        if key.startswith("#"):
            continue
        if key not in FRONT_MATTER:
            near = difflib.get_close_matches(key.replace("_", "-"), FRONT_MATTER, 1, 0.75) or difflib.get_close_matches(key, FRONT_MATTER, 1, 0.75)
            out.append(f'{t["id"]}: `{key}:` is not a front-matter key' + (f' — did you mean `{near[0]}:`?' if near else '.')
                       + ' `--schema` prints the keys; anything else belongs in the body')
            continue
        shape, _required, _who, says = FRONT_MATTER[key]
        if shape and value and not re.fullmatch(shape, value, re.I):
            out.append(f'{t["id"]}: `{key}:` is {says} — {shape_words(shape)} — got {value!r}')
    is_open = t.get("status") in OPEN_STATUSES
    out += [f'{t["id"]}: {"open work" if required == "open" else "every tracker"} states `{key}:` — {says}'
            for key, (_s, required, _w, says) in FRONT_MATTER.items()
            if (required == "all" or (required == "open" and is_open)) and not t["fm"].get(key)]
    return out


def shape_words(shape):
    """A shape for a reader: an enumeration as its words, else the expression itself."""
    return "one of " + " · ".join(shape.split("|")) if re.fullmatch(r"[A-Za-z| ]+", shape) else f"shape `{shape}`"


def render_schema():
    rows = [f"| `{k}:`{' — required' + (' on open work' if required == 'open' else '') if required else ''} | {shape_words(shape) if shape else 'free text'} | {who} | {says} |"
            for k, (shape, required, who, says) in FRONT_MATTER.items()]
    return "\n".join(["| Key | Value | Written by | Says |", "|---|---|---|---|"] + rows)


def lint(trackers):
    """Ledger-integrity checks. Returns a list of human-readable violations.

    """
    problems = []
    ids = {t["id"] for t in trackers}
    for t in trackers:
        epic = t.get("epic", "—")
        if epic != "—" and (epic not in ids or epic == t["id"]):
            problems.append(f'{t["id"]}: `epic: {epic}` must name another existing tracker')
        tags = t.get("tags", [])
        unknown = [x for x in tags if x not in TAGS]
        if unknown:
            problems.append(f'{t["id"]}: `tags:` {unknown} not in the vocabulary {sorted(TAGS)} — '
                            f'reuse one, or add it with its meaning under [tags] in {CONFIG_NAME}')
        if len(tags) > MAX_TAGS or len(set(tags)) != len(tags):
            problems.append(f'{t["id"]}: `tags:` takes at most {MAX_TAGS} distinct tags')
        chains = sorted(x for x in set(tags) if x in CHAIN_TAGS)
        if len(chains) > 1:
            problems.append(f'{t["id"]}: `tags:` {chains} each select a chain of seats — a tracker runs one')
        considered = t.get("considered", [])
        if t.get("num", 0) >= CONSIDERED_FROM.get(t.get("kind", ""), 10**9) and not considered:
            problems.append(f'{t["id"]}: a new tracker says what it was held against — run '
                            f'`{CMD} --related {t["id"]}` and add '
                            f'`considered: <ids>` (or `considered: none`) to the front matter. The default is a '
                            f'slice of a tracker that exists, not a new one')
        wrong = [c for c in considered if c != "none" and (c not in ids or c == t["id"])]
        if wrong or ("none" in considered and len(considered) > 1):
            problems.append(f'{t["id"]}: `considered:` {wrong or considered} — each entry is another existing '
                            f'tracker id, or the single word none')
        if t.get("orphan_rows"):
            problems.append(f'{t["id"]}: line {t["orphan_rows"][0]} is a table row that belongs to no table'
                            f' ({len(t["orphan_rows"])} such) — a blank line, a note or a wrapped cell split the table;'
                            ' it renders as plain text. Rejoin it: a table is contiguous and a cell is one line')
        chapters = [o["id"] for o in trackers if o.get("epic") == t["id"] and o["status"] in OPEN_STATUSES]
        if chapters and t["status"] not in OPEN_STATUSES:
            problems.append(f'{t["id"]}: `status: {t["status"]}`, and open work names it in `epic:` — {", ".join(chapters)}. A story is open '
                            f'while a chapter is: keep it `In Progress` with `next: wait`, or give the chapters another story first')
        if t.get("rank"):
            if not 1 <= t["rank"] <= RANK_MAX or t["status"] not in ("In Progress", "Proposed"):
                problems.append(f'{t["id"]}: `rank:` is 1–{RANK_MAX}, on work that is `In Progress` or `Proposed` — '
                                f'remove it when the tracker ships, parks or closes')
            twin = [o["id"] for o in trackers if o is not t and o.get("rank") == t["rank"]]
            if twin:
                problems.append(f'{t["id"]}: `rank: {t["rank"]}` is also on {twin[0]} — a rank names one tracker')
        problems += schema_problems(t)
        bad = [b for b in t.get("blocked_by", []) if not b.startswith("Owner") and (b not in ids or b == t["id"])]
        if bad:
            problems.append(f'{t["id"]}: `blocked-by:` {bad} — each entry is another existing tracker id, '
                            f'or the word Owner')
        # a cross-reference to a tracker that does not exist — almost always rename-rot: the id is right and only
        # the slug moved. Name the replacement, don't just complain: a lint that makes you go find the answer it
        # already has is a lint people route around.
        for link in t["links"]:
            if (TRACKER_DIR / link).exists():
                continue
            link_id = link.split("-")[0] + "-" + link.split("-")[1]
            cands = sorted(p.name for p in TRACKER_DIR.glob(f"{link_id}-*.md"))
            if len(cands) == 1:
                fix = f"did you mean {cands[0]}?"
            elif cands:
                fix = f"{link_id} resolves to {len(cands)}: {', '.join(cands)}."
            else:
                # No file with that id at all — a phantom, not a rename. This is
                # a tracker stranded on an unmerged branch, or
                # never written), and it needs a human, not a slug swap.
                fix = f"NO tracker with id {link_id} exists — phantom or branch-stranded."
            problems.append(f"{t['id']}: dangling link -> {link} ({fix})")
    return problems


# Distinct codes so CI can tell "run the generator" from "fix your tracker" — the
# two want different humans. LINT outranks DRIFT: regenerating fixes drift, and
# will never fix a violation.
EXIT_OK = 0
EXIT_DRIFT = 3
EXIT_LINT = 4
# The header stamps the generation date, so a byte-compare would report drift on
# every day after the last write — a gate firing on green code, which is how you
# train people to ignore a gate.
# The date is provenance, not ledger content: the one line whose change means
# nothing.
GENERATED_RE = re.compile(r"^> Generated \d{4}-\d{2}-\d{2} ", re.M)


def drift_normalize(text):
    """Blank the generation date so only ledger content can count as drift."""
    return GENERATED_RE.sub("> Generated <date> ", text)



def parse_args(argv):
    parser = argparse.ArgumentParser(prog="fathom-mark", description="A work tracker that lives in the repository it tracks.")
    add = parser.add_argument
    add("--root", metavar="DIR", help="the repository to track; default: the nearest fathom-mark.toml or git toplevel above the working directory")
    add("--check", action="store_true",
        help=f"read-only gate: write nothing; exit {EXIT_DRIFT} if INDEX.md is stale, {EXIT_LINT} on a ledger-integrity violation")
    add("--print-written", action="store_true",
        help="write mode: print every file written, one repo-relative path per line on stdout, so a hook stages exactly that")
    add("--related", metavar="ID_OR_WORDS", help="before filing: the existing trackers closest to a tracker id or a quoted phrase. Read-only")
    add("--new", nargs=2, metavar=("KIND", "TITLE"),
        help="file a tracker: prints what is related, writes the next free id with a front matter whose `considered:` is yours to fill")
    add("--triage", action="store_true",
        help="start or continue a triage pass: applies the verdicts filled in today's worksheet, rewrites it, prints the rules")
    add("--schema", action="store_true", help="print the front-matter schema — every key, its shape, who writes it. Read-only")
    add("--html-only", action="store_true", help="write only the git-ignored board (index.html) and exit 0 — a post-merge hook cannot dirty the tree")
    add("--init", action="store_true", help="scaffold fathom-mark.toml, the tracker directory and TRIAGE.md; never overwrites")
    add("--vendor", metavar="DIR", help="copy this tool into DIR with a PIN file of sha256 hashes — a pinned, self-contained copy")
    add("--version", action="version", version=__version__)
    return parser.parse_args(argv)


def load_trackers():
    return mark_blocked([extract(p) for p in sorted(TRACKER_DIR.glob("*.md")) if KIND_RE.match(p.name)])


TOOL_FILES = ("fathom_mark.py", "vendor/marked-18.0.13.umd.js", "VERSION", "NOTICE")


def pin_problems():
    """A vendored copy carries a PIN — `sha256  path` per file. A copy that was edited in place is refused by the
    gate: fix it upstream and vendor again, so two repositories never run two tools under one name."""
    pin = HERE / "PIN"
    if not pin.exists():
        return []
    out = []
    for line in pin.read_text(encoding="utf-8").splitlines():
        want, _, rel = line.partition("  ")
        if rel and (not (HERE / rel).exists() or hashlib.sha256((HERE / rel).read_bytes()).hexdigest() != want):
            out.append(f"{(HERE / rel)}: differs from its PIN — a vendored fathom-mark is not edited in place; change it upstream and run --vendor again")
    return out


def vendor(dest):
    dest = pathlib.Path(dest).resolve()
    lines = []
    for rel in TOOL_FILES:
        src = HERE / rel
        if not src.exists():
            continue
        (dest / rel).parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(src, dest / rel)
        lines.append(f"{hashlib.sha256(src.read_bytes()).hexdigest()}  {rel}")
    (dest / "PIN").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"vendored fathom-mark {__version__} into {dest} — {len(lines)} files, pinned in PIN")
    return EXIT_OK


TRIAGE_HOME = """\
# Triage

The home of the recurring triage pass: `{cmd} --triage`. The command prints the rules and the two sections
below; its worksheets are the record, in `evidence/triage/`.

## The intent

*The Owner's own words — for · so that · never. Nobody else edits this. A pass prints it above its rules.*

- **for** —
- **so that** —
- **never** —

## The current path

*The Owner's. A pass judges every tier against it; only the Owner changes it.*

1.

## Passes

Newest first — one paragraph per pass: its date, what it changed, its worksheet.

*None yet.*
"""

CONFIG_TEMPLATE = """\
# fathom-mark — every key is optional; these are the defaults.
name = "{name}"
tracker_dir = "docs/work-tracker"
blob = ""            # URL prefix of a tracker file on the forge, e.g. https://github.com/me/repo/blob/main/docs/work-tracker/
triage_days = 7

[kinds]              # id prefix = the INDEX section it is listed under
FEAT = "Features"
BUG = "Bugs"

[tags]               # a closed vocabulary: a synonym is how tags rot
research = "explores a question; commits to nothing being built"
security = "credentials, exposure, access — a fix or a finding"
process = "how the work is done: rules, gates, tooling, the tracker itself"
"""

TRACKER_TEMPLATE = """\
---
id: {id}
status: Proposed
considered:
hook: "{title}"
---

# {id} — {title}

## What is true now

**Filed {today}; nothing is built.**

## Why

## Done when

## Ship log

| Date | Event |
|---|---|
| {today} | Filed. |
"""


def init():
    wrote = []
    for path, text in ((ROOT / CONFIG_NAME, CONFIG_TEMPLATE.format(name=ROOT.name)),
                       (TRACKER_DIR / "TRIAGE.md", TRIAGE_HOME.format(cmd=CMD))):
        if not path.exists():
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(text, encoding="utf-8")
            wrote.append(path)
    ignore, rel = ROOT / ".gitignore", str(TRACKER_DIR.relative_to(ROOT))
    have = ignore.read_text(encoding="utf-8") if ignore.exists() else ""
    lines = [l for l in (f"{rel}/index.html", f"{rel}/view/") if l not in have.splitlines()]
    if lines:
        ignore.write_text(have + ("" if have.endswith("\n") or not have else "\n") + "\n".join(lines) + "\n", encoding="utf-8")
        wrote.append(ignore)
    print("\n".join([f"wrote {p.relative_to(ROOT)}" for p in wrote] or ["nothing to write — already initialised"]))
    print(f"next: the Owner writes the intent and the current path in {(TRACKER_DIR / 'TRIAGE.md').relative_to(ROOT)}; "
          f"file the first tracker with `{CMD} --new {KINDS[0]} \"…\"`; wire `{CMD} --print-written` into pre-commit")
    return EXIT_OK


def new_tracker(kind, title, trackers):
    kind = kind.upper()
    if kind not in KINDS:
        print(f"--new: {kind} is not a kind — {', '.join(KINDS)} ({CONFIG_NAME}, [kinds])", file=sys.stderr)
        return EXIT_LINT
    near = related_trackers(trackers, title, limit=5)
    print("A filing looks first. The default is a slice of a tracker that exists, not a new one." if near
          else "Nothing related is filed yet.")
    for score, t in near:
        print(f'{score:7.1f}  {t["id"]:<9} {t["status"]:<12} {t["title"][:60]}')
    num = max([t["num"] for t in trackers if t["kind"] == kind] or [0]) + 1
    tid = f"{kind}-{num:03d}"
    slug = re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")[:80]
    path = TRACKER_DIR / f"{tid}-{slug}.md"
    TRACKER_DIR.mkdir(parents=True, exist_ok=True)
    path.write_text(TRACKER_TEMPLATE.format(id=tid, title=title.replace('"', "'"), today=datetime.date.today().isoformat()), encoding="utf-8")
    print(f"wrote {path.relative_to(ROOT)} — fill `considered:` with the ids you held it against, or `none`; the gate refuses it until then")
    return EXIT_OK


def main(argv=None):
    args = parse_args(argv)
    if args.root:
        configure(args.root)
    # under --print-written stdout carries ONE thing: the path list the caller stages
    log = sys.stderr if args.print_written else sys.stdout
    if args.schema:
        print(render_schema())
        return EXIT_OK
    if args.vendor:
        return vendor(args.vendor)
    if args.init:
        return init()
    trackers = load_trackers()
    if args.new:
        return new_tracker(args.new[0], args.new[1], trackers)
    if args.html_only:
        if TRACKER_DIR.is_dir():
            HTML_OUT.write_text(render_html(trackers), encoding="utf-8")
            write_views(trackers)
        return EXIT_OK
    if not TRACKER_DIR.is_dir():
        print(f"no tracker directory at {TRACKER_DIR} — run `{CMD} --init`", file=sys.stderr)
        return EXIT_LINT
    if args.triage:
        home, path_now = TRACKER_DIR / "TRIAGE.md", triage_home()["path"]
        if not re.search(r"\w{3,}", re.sub(r"\*[^*]*\*", "", path_now)):
            print(f"--triage: {home.relative_to(ROOT)} names no current path — tiers cannot be judged; the Owner writes it first", file=sys.stderr)
            return EXIT_LINT
        today = datetime.date.today().isoformat()
        out = TRACKER_DIR / "evidence" / "triage" / f"triage-{today}.md"
        out.parent.mkdir(parents=True, exist_ok=True)
        sheets = sorted(out.parent.glob("triage-*.md"))
        applied, errors = apply_worksheet(sheets[-1].read_text(encoding="utf-8"), sheets[-1] == out, trackers, today) if sheets else ([], [])
        trackers = load_trackers()
        earlier = out.read_text(encoding="utf-8") if out.exists() else ""
        text, left = triage_worksheet(trackers, today, last_worked_on, earlier, repos_naming())
        out.write_text(text, encoding="utf-8")
        print(TRIAGE_RULES.format(path=out.relative_to(ROOT), left=left, home=home.relative_to(ROOT), days=TRIAGE_DAYS, sized=SIZED_LINES, current_path=path_now,
                                  intent=triage_home()["intent"] or "  (none is written — the Owner writes it in the triage home)"))
        print("\n".join([f"Applied {len(applied)}:"] + [f"  {l}" for l in applied] if applied else ["Applied nothing — no new filled rows."]))
        if errors:
            print("\n".join(["NOT applied — fix the Verdict cell and run again:"] + [f"  {e}" for e in errors]), file=sys.stderr)
        refreshed = main(["--root", str(ROOT)]) if applied else EXIT_OK   # INDEX.md and the board print what was applied — refresh them
        return EXIT_LINT if errors else refreshed                        # a pass that leaves the ledger failing its gate does not exit 0
    if args.related:
        for score, t in related_trackers(trackers, args.related):
            print(f'{score:7.1f}  {t["id"]:<9} {t["status"]:<12} {t["title"][:60]}\n'
                  f'{"":9}{t["hook_full"][:170]}')
        return EXIT_OK
    # identity refusal BEFORE rendering or writing anything, in both modes: the id is the routing key
    identity = identity_problems(trackers)
    if identity:
        print(f"FAILED: {len(identity)} tracker-identity violation(s) — the id is the routing key; fix the tracker file(s). "
              "Nothing was written.", file=sys.stderr)
        for p in identity:
            print(f"  {p}", file=sys.stderr)
        return EXIT_LINT

    unknown = [t["id"] for t in trackers if t["status"] == "?"]
    problems = pin_problems() + lint(trackers)
    today = datetime.date.today().isoformat()
    counts = ", ".join(f"{sum(t['kind'] == k for t in trackers)} {KIND_LABELS[k].lower()}" for k in KINDS)
    header = (
        "# Work Tracker — Index\n\n"
        f"> **GENERATED — do not hand-edit.** Run `{CMD}` after changing any tracker's front matter\n"
        "> (or its `# title`). Rows are *pointers* — the detail lives in the tracker, never duplicated here.\n>\n"
        "> **Status** = code lifecycle; `Shipped` means merged, **not** a production claim.\n>\n"
        "> **Tier · Board · Triaged** = the triage picture — the same one the board (`index.html`) shows, from the\n"
        "> same function: `progress` kept by a pass · `triage` owed a pass · `backlog` waiting · `done`.\n"
        f"> One rule this file cannot show, because it has no clock: a judgement on work in progress older than {TRIAGE_DAYS} days\n"
        "> counts as `triage` again.\n>\n"
        f"> Generated {today} · {len(trackers)} trackers ({counts})."
    )
    if problems:
        header += f"\n>\n> ❌ {len(problems)} ledger-integrity violation(s):\n>\n" + "\n".join(f"> - {p}" for p in problems)
    if unknown:
        header += (f"\n>\n> ⚠️ {len(unknown)} tracker(s) have no machine-readable status — add a\n"
                   f"> front-matter `status:` to fix: {', '.join(sorted(unknown))}.")
    sections = [header, render_triage(trackers)] + [render([t for t in trackers if t["kind"] == k], KIND_LABELS[k]) for k in KINDS]
    body = "\n\n".join(sections).rstrip() + "\n"      # exactly one terminal newline, so `git diff --check` passes

    drifted = False
    if args.check:
        on_disk = OUT.read_text(encoding="utf-8") if OUT.exists() else ""
        drifted = drift_normalize(on_disk) != drift_normalize(body)
        if drifted:
            print(f"{OUT.relative_to(ROOT)} is STALE — a tracker changed without regenerating. Run: {CMD}", file=sys.stderr)
        else:
            print(f"{OUT.relative_to(ROOT)} is up to date — {len(trackers)} trackers.", file=log)
    else:
        OUT.write_text(body, encoding="utf-8")
        HTML_OUT.write_text(render_html(trackers), encoding="utf-8")   # git-ignored; never staged
        write_views(trackers)
        print(f"wrote {OUT.relative_to(ROOT)} — {len(trackers)} trackers, {len(unknown)} unknown-status", file=log)
        if args.print_written:
            print(OUT.relative_to(ROOT))       # the caller stages what we OWN, never a guessed glob

    for p in problems:
        print(f"  lint: {p}", file=sys.stderr)
    # the INDEX is still written when a lint fires: the ❌ banner in its header IS the violation, made visible
    # where the ledger is read. What the non-zero exit stops is the COMMIT.
    if problems:
        print(f"FAILED: {len(problems)} ledger-integrity violation(s) — fix the tracker; regenerating will not clear these.", file=sys.stderr)
        return EXIT_LINT
    return EXIT_DRIFT if drifted else EXIT_OK


configure()

if __name__ == "__main__":
    sys.exit(main())
