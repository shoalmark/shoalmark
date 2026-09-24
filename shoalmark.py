#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0 OR MIT
"""shoalmark — a work tracker that lives in the repository it tracks.

Markdown trackers with a small front matter, and one command that reads them all:

    shoalmark.py                 regenerate INDEX.md and the local board (idempotent)
    shoalmark.py --check         read-only gate: write nothing, fail on drift or a violation
    shoalmark.py --related "…"   before filing: the existing trackers closest to an id or to words
    shoalmark.py --new KIND "…"  file a tracker — it prints what is related first, and the gate
                                   refuses the file until `considered:` says what it was held against
    shoalmark.py --triage        a triage pass: the seat judges a worksheet, the command applies it
    shoalmark.py --schema        every front-matter key, its shape, who writes it
    shoalmark.py --init          scaffold the tracker directory, TRIAGE.md and shoalmark.toml
    shoalmark.py --vendor DIR    copy this tool, pinned by hash, into another repository

One seam, by convention: if `<tracker dir>/derive` exists and is executable it runs first, on every run — it may add
columns (each also a view on the board), front-matter keys, problems and other generated files, or refuse the run.

The INDEX is a *pointer*, not a copy: each row is a terse hook and a machine-read status; the detail
lives in the tracker. `status` is the code lifecycle — `Shipped` means merged, not deployed.

Both modes FAIL on a ledger-integrity violation: a gate that always lands green is not a gate.
Configuration is `shoalmark.toml` at the repository root; every key has a default.
"""

import argparse
import base64
import datetime
import difflib
import hashlib
import collections
import itertools
import json
import math
import os
import pathlib
import re
import shutil
import subprocess
import sys

HERE = pathlib.Path(__file__).resolve().parent
# The version is the `VERSION` file and nothing else. It ships in TOOL_FILES, so a vendored copy carries it, and
# `--vendor` then compares the consumer's VERSION against ours — the artifact actually being copied. Declaring it
# a second time here is what let 0.17.1 and 0.17.2 ship with a stale constant, silencing the changelog (FM-009).
__version__ = (HERE / "VERSION").read_text(encoding="utf-8").strip() if (HERE / "VERSION").exists() else "unknown"
MARKED = HERE / "vendor" / "marked-18.0.13.umd.js"      # the one vendored, pinned third-party file (marked, MIT)
# how an Owner sets up the key his answers are signed with — named where signing fails: `--answer`, and the board's
# second screen (a repository with its own page overrides the label `answer.sign.url`)
SIGNING_PAGE = "https://holgo99.github.io/shoalmark/signing/"
CONFIG_NAME = "shoalmark.toml"
DEFAULTS = {
    "name": "",                                  # shown in the board's title; the directory name when empty
    "tracker_dir": "docs/work-tracker",
    # id prefix -> the INDEX section it is listed under. ONE id space per repository, keyed by the project
    # (`MSR-012`), is what `--init` writes: an id is the routing key and encodes nothing that can change — not the
    # kind of work (a tag says `bug`), not being a story (`epic:` is a field). This two-kind default is only for a
    # repository with no configuration at all.
    "kinds": {"FEAT": "Features", "BUG": "Bugs"},
    "considered_from": {},                       # kind -> first number that must carry `considered:`; default 1
    "blob": "",                                  # URL prefix for a tracker file on the forge; empty = local links
    "triage_days": 7,
    # THE FILING FREEZE (FM-032 S4): while this many trackers or more are open, `--new` files only a product defect — a
    # filing that carries `tags: bug`; anything else goes as one line into the closest open tracker's body, or waits.
    # Filing outran closing two to one, and the open count only grew. 0 = off.
    "freeze_at": 0,
    # who may answer an ask. An answer is three lines in the tracker, committed by the answerer, and the commit is the
    # proof — but git's author is a string anyone can type. So an entry is `"name"` (Subversion, whose server
    # authenticates the committer; or git with NO enforcement, and the gate says so) or `"name signed"` (git: the
    # commit that carries the answer must VERIFY — `git verify-commit` — under a key the repository trusts; that is
    # `gpg.format`/`user.signingkey` and, for SSH keys, `gpg.ssh.allowedSignersFile`). Empty = nobody may answer.
    # A seat cannot add itself here unseen: the change is in the same diff as anything it would allow.
    "answerers": [],
    # WHO IS AT THE KEYBOARD, and what that seat may change. `[seats]` is a name of the repository's choosing → the
    # identity the version control system reports — `"principal@seat"`, or `"principal@seat signed"` where the commit
    # must also VERIFY under a key trusted for it. `[rights]` gives a name of your own its rights; the four built-in
    # names have theirs (BUILTIN_RIGHTS). ABSENT, nothing is enforced — this is for a repository that lets in agents
    # which never read its contract. It catches an agent that does not know the rule, not one that lies (README,
    # *Seats*). Under Subversion an identity is the server account and `signed` is refused: the server authenticated it.
    "seats": {},
    "rights": {},
    # humans have office hours, agents have budgets: ONE fixed sitting a day in which the Owner goes through what
    # needs him. Agents write their asks before it; a deadline is counted in standups, not in hours.
    "standup": "",                               # "09:00" — local time; empty = no standup
    "standup_minutes": 15,
    "tags": {
        "bug": "something that worked, or was meant to, and does not",
        "research": "explores a question; commits to nothing being built",
        "security": "credentials, exposure, access — a fix or a finding",
        "process": "how the work is done: rules, gates, tooling, the tracker itself",
    },
    # the section names the tool READS in a tracker and in TRIAGE.md, and writes with `--new` and `--init` — in the
    # repository's language. They are here and not in a brand's labels.yaml because the gate depends on them: what
    # the gate says is a function of the repository alone. The English ones are always understood as well.
    "headings": {"state": "What is true now", "why": "Why", "done": "Done when", "log": "Ship log",
                 "intent": "The intent", "path": "The current path", "passes": "Passes", "asks": "Asks"},
}


def read_config(text):
    """The configuration's TOML, read without a library: `tomllib` needs Python 3.11 and the Python that ships with
    macOS is 3.9 — a gate that cannot start on the client's machine is no gate. The subset is what `--init` writes:
    `[table]` headers, `key = "string"`, `key = 123`, `key = true`, `key = ["a", "b"]` (strings only), `# comments`.
    Anything else is refused by line."""
    out, table = {}, None
    for n, raw in enumerate(text.splitlines(), 1):
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        head = re.fullmatch(r"\[([A-Za-z0-9_-]+)\]\s*(?:#.*)?", line)
        if head:
            table = out.setdefault(head.group(1), {})
            continue
        m = re.fullmatch(r'([A-Za-z0-9_-]+)\s*=\s*(?:"((?:[^"\\]|\\.)*)"|(-?\d+)|(true|false)|(\[[^\]]*\]))\s*(?:#.*)?', line)
        if not m:
            raise SystemExit(f"{CONFIG_NAME}:{n}: not understood — {raw.strip()!r}. A line is `key = \"text\"`, `key = 123`, `key = true`, `key = [\"a\", \"b\"]` or `[table]`")
        key, text_value, number, flag, items = m.groups()
        if items is not None and not re.fullmatch(r'\[\s*(?:"(?:[^"\\]|\\.)*"\s*(?:,\s*"(?:[^"\\]|\\.)*"\s*)*)?,?\s*\]', items):
            raise SystemExit(f"{CONFIG_NAME}:{n}: a list holds quoted strings only — {raw.strip()!r}")
        value = (re.sub(r'\\(.)', r"\1", text_value) if text_value is not None else int(number) if number is not None
                 else re.findall(r'"((?:[^"\\]|\\.)*)"', items) if items is not None else flag == "true")
        (out if table is None else table)[key] = value
    return out


def find_root(start=None):
    """The repository this run tracks: the nearest ancestor of the working directory that holds a
    shoalmark.toml, else the git toplevel, else the working directory."""
    here = pathlib.Path(start or os.getcwd()).resolve()
    for p in (here, *here.parents):
        if (p / CONFIG_NAME).exists():
            return p
    for p in (here, *here.parents):
        if (p / ".git").exists() or (p / ".svn").exists():
            return p
    return here


def vcs():
    """"git", "svn" or "" — the nearest working copy ROOT sits in. Nothing in the gate, INDEX.md or the board asks:
    only what a version control system does differently does — hooks, ignore rules, and a pass's *last worked on*."""
    for p in (ROOT, *ROOT.parents):
        if (p / ".git").exists():
            return "git"
        if (p / ".svn").exists():
            return "svn"
    return ""


def put(path, text):
    """Every file the tool writes is UTF-8 with `\\n` line ends on every system — what is committed must not depend on
    who ran the tool."""
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)


def digest(path):
    """A PIN hash survives a checkout that converts line ends (git's autocrlf, svn:eol-style)."""
    return hashlib.sha256(pathlib.Path(path).read_bytes().replace(b"\r\n", b"\n")).hexdigest()


PY = "python" if os.name == "nt" else "python3"         # the name a message, a hook and the contract can be pasted under

# WHAT A SEAT MAY CHANGE — four rights, each one a front-matter transition the gate can see in a diff. Anything else a
# tracker carries is open to every seat and needs no right: rights are for the four changes that move authority, not
# for the work. There is no hierarchy, no deny rule and no wildcard — a name either holds a right or it does not.
RIGHTS = ("answer",      # writing `answer:` `answered:` `answered-by:` — the Owner's ruling
          "ask",         # setting `next: owner` — putting a question in front of him
          "close",       # setting a terminal status — saying work is over
          "triage")      # writing `considered:`, `kind-of-problem:`, `tier:`, `rank:`, `triaged:` — the judgement
# the four names that need no `[rights]` line, because the seats mean the same thing in every repository that runs this
BUILTIN_RIGHTS = {"owner": set(RIGHTS), "principal": {"ask", "close", "triage"}, "reviewer": {"triage"}, "implementer": set()}
TRIAGE_KEYS = ("kind-of-problem", "tier", "rank", "triaged")     # `considered:` too — except on a filing, which is the rule, not a verdict


def configure(root=None):
    """Bind every path, id pattern and schema shape to one repository. Called once at import for the working
    directory, and again by `--root` and by the tests."""
    global ROOT, CONFIG, TRACKER_DIR, OUT, HTML_OUT, VIEW_DIR, REPO_BLOB, TAGS, CONSIDERED_FROM, TRIAGE_DAYS
    global KINDS, KIND_LABELS, KIND_RE, TITLE_RE, TRACKER_LINK_RE, H1_ID_RE, ROW_ID_RE, _IDS, FRONT_MATTER, CMD
    global HEAD, STATE_HEAD_RE, DONE_RE
    ROOT = find_root(root)
    path = ROOT / CONFIG_NAME
    CONFIG = {**DEFAULTS, **(read_config(path.read_text(encoding="utf-8")) if path.exists() else {})}
    TRACKER_DIR = ROOT / CONFIG["tracker_dir"]
    OUT, HTML_OUT, VIEW_DIR = TRACKER_DIR / "INDEX.md", TRACKER_DIR / "index.html", TRACKER_DIR / "view"
    REPO_BLOB, TAGS, TRIAGE_DAYS = CONFIG["blob"], dict(CONFIG["tags"]), int(CONFIG["triage_days"])
    global FREEZE_AT
    FREEZE_AT = CONFIG["freeze_at"]
    if isinstance(FREEZE_AT, bool) or not isinstance(FREEZE_AT, int) or FREEZE_AT < 0:
        raise SystemExit(f"{CONFIG_NAME}: `freeze_at` is a whole number of open trackers — the filing freeze holds at that count and above; 0 turns it off. Got {FREEZE_AT!r}")
    global ANSWERERS, SEATS, SEAT_RIGHTS, ASKS_HEAD_RE, COMMITTING, _STAGED, _LINE_AUTHOR, _SVN_BLAME, _GIT_USER
    _GIT_USER = None                                    # `git config user.name`, read at most once for this repository
    ANSWERERS = {}                                      # name -> "signed" | "" (name only)
    for a in (CONFIG.get("answerers") or []):
        name, _, mode = str(a).strip().rpartition(" ")
        ANSWERERS[name if mode == "signed" else str(a).strip()] = "signed" if mode == "signed" else ""
    SEATS, SEAT_RIGHTS = {}, {}                         # seat name -> (identity, "signed" | ""), and seat name -> rights
    for name, value in (CONFIG.get("seats") or {}).items():
        who, _, mode = str(value).strip().rpartition(" ")
        SEATS[name] = (who if mode == "signed" else str(value).strip(), "signed" if mode == "signed" else "")
        SEAT_RIGHTS[name] = set(BUILTIN_RIGHTS.get(name, ()))
    for name, words in (CONFIG.get("rights") or {}).items():
        if isinstance(words, str) or any(w not in RIGHTS for w in words):
            bad = [words] if isinstance(words, str) else [w for w in words if w not in RIGHTS]
            raise SystemExit(f'{CONFIG_NAME}: `[rights] {name}` — {bad[0]!r} is not a right. There are four: {" · ".join(RIGHTS)}; '
                             f'anything else a tracker can carry is open to every seat and needs none')
        SEAT_RIGHTS[name] = set(words)
    COMMITTING, _STAGED, _LINE_AUTHOR, _SVN_BLAME = False, None, {}, {}    # the pre-commit run, what it stages, and who wrote which line
    KIND_LABELS = dict(CONFIG["kinds"])
    HEAD = {**DEFAULTS["headings"], **CONFIG["headings"]}
    if set(HEAD) - set(DEFAULTS["headings"]) or not all(str(v).strip() for v in HEAD.values()):
        raise SystemExit(f"{CONFIG_NAME}: `[headings]` names {', '.join(DEFAULTS['headings'])} — each a section name, none empty")
    STATE_HEAD_RE = re.compile(_STATE_HEADS[:-3] + "|" + re.escape(HEAD["state"]) + r")\b", re.I)
    DONE_RE = re.compile(_DONE_WORDS + "|" + re.escape(HEAD["done"]), re.I)
    # the body section an exchange is moved into when its ask is cleared — the repository's own word, English always
    ASKS_HEAD_RE = re.compile(r"^#{2,3}\s+(asks|" + re.escape(HEAD["asks"]) + r")\s*$", re.I | re.M)
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
        CMD = PY + " " + pathlib.Path(__file__).resolve().relative_to(ROOT).as_posix()
    except ValueError:
        CMD = PY + " " + pathlib.Path(__file__).resolve().as_posix()      # forward slashes: a hook is a `sh` script, and `\\` is its escape
    CMD = os.environ.get("SHOALMARK_CMD") or CMD        # a repository that wraps the tool is named by its own command in every message
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
# WHAT AN ASK MUST BE, in numbers. The flow held only while every agent had read the contract and chose to obey it;
# these are the same sentences, held by the gate instead (FM-008). They are deliberately generous: an ask that trips
# one of them is not borderline, it is a paragraph, a second question, or a question already asked.
ASK_MAX = 300              # characters — past this it is not a sentence he can answer in a sitting; the detail is the body's
ASK_OPTIONS_MAX = 5        # choices — a radio list he reads once, not a menu
ASK_OPTION_MAX = 120       # characters per choice — a choice is a phrase, not its rationale
BOTTLENECK = 5             # more asks than this in his queue and the queue itself is the finding, said in the first line
# the three lines an ask carries besides the question itself, each with what it is FOR — a refusal that only names a
# key sends the agent to the schema; one that says what the key is for is answerable where it is read.
ASK_NEEDS = {"ask-kind": "which of his four kinds it is", "ask-since": "the day it was first made — its age is what he sees",
             "ask-proposal": "the one the seat RECOMMENDS, and would act on"}
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
        "ask":             (None, False, "the seat that needs the Owner", "what is asked of the Owner, as ONE sentence he can answer — with `next: owner`. The board's first line is built from these; an ask buried in the body waits longest"),
        "ask-kind":        ("ruling|action|determination|ceremony", False, "the seat that needs the Owner", "ruling — a decision of intent · action — hands only the Owner has · determination — evidence could settle it · ceremony — reserved by rule, not by risk"),
        "ask-since":       (r"\d{4}-\d{2}-\d{2}", False, "the seat that needs the Owner", "the day the ask was first made — its age is what the Owner sees"),
        "ask-proposal":    (None, False, "the seat that needs the Owner", "the one the seat RECOMMENDS, and why — one sentence; it is offered first. With `ask-options:` it must be one of them. Never acted on without the answer"),
        "ask-options":     (None, False, "the seat that needs the Owner", "the choices the ask offers, ONE line separated by ` | ` — the Owner picks one, or writes his own under *Other*"),
        "answer":          (None, False, "the Owner — in his own commit", "his answer to `ask:`, in his words: `accepted`, `accepted — <his change>`, or `rejected — <why, and how to reword the ask>`. Written by him, never by the seat that asked; an answered ask leaves his queue. "
                                                                        "Never overwritten in place: `--answer <id> revoke \"<reason>\"` makes it `revoked - <reason>`, and `--answer <id> accept|reject \"<option>\" --supersede` replaces it — "
                                                                        "either moves the answer it replaces into the ship log, with the commit that wrote it, and the board says *supersedes <sha>*"),
        "answered":        (r"\d{4}-\d{2}-\d{2}", False, "the Owner", "the day he answered — the commit that carries it is the clock"),
        "answered-by":     (None, False, "the Owner", "who answered; the commit's author is the proof, this is the label"),
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
_DONE_WORDS = r"done when|acceptance|exit criteri|definition of done|falsifier"
DONE_RE = re.compile(_DONE_WORDS, re.I)                 # `configure` adds the repository's own `[headings] done`

# an epic's "state of the epic" is the first paragraph of the current-truth head the
# doctrine already asks for (trackers-say-what-is-true-now); no new field to keep in step.
_STATE_HEADS = r"^#{2,3}\s+(what is true now|current (state|truth|status)|state of play)\b"
STATE_HEAD_RE = re.compile(_STATE_HEADS, re.I)          # `configure` adds the repository's own `[headings] state`


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
    hook = hook_full.replace("|", "\\|")
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
        "ask": (lambda v: v[1:-1] if len(v) > 1 and v[0] == v[-1] == '"' else v)((fm.get("ask") or "").strip()),
        "ask_kind": (fm.get("ask-kind") or "").strip().lower(), "ask_since": (fm.get("ask-since") or "").strip(),
        "ask_proposal": (lambda v: v[1:-1] if len(v) > 1 and v[0] == v[-1] == '"' else v)((fm.get("ask-proposal") or "").strip()),
        # the choices as ONE line — `a | b | c`. Split here so the board and the gate read the same list
        "ask_options": [o.strip() for o in (lambda v: v[1:-1] if len(v) > 1 and v[0] == v[-1] == '"' else v)((fm.get("ask-options") or "").strip()).split("|") if o.strip()],
        "answer": (lambda v: v[1:-1] if len(v) > 1 and v[0] == v[-1] == '"' else v)((fm.get("answer") or "").strip()),
        "answered": (fm.get("answered") or "").strip(),
        # `<you>` or nothing is filled from `git config user.name` — ONLY where there is an answer to sign. Asked of
        # every tracker it was one git process per file: 504 of them, 15.2 s of a 16.8 s load, on a 505-tracker corpus (FM-012)
        "answered_by": (lambda v: git_user() if v in ("", "<you>") and (fm.get("answer") or "").strip() else v)((fm.get("answered-by") or "").strip()),
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
        # the body's `## Asks` section: where an exchange goes when its ask is cleared. Read here because `extract` is
        # the only place the file text is read, and both the gate and `--answered` ask whether the record is there.
        "asks_block": bool(ASKS_HEAD_RE.search(body)),
        # the answer this one replaced — the commit of the newest ship-log row `--answer … revoke|--supersede` writes
        "supersedes": superseded(body),
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


def held_up_by(t, trackers):
    """The open work that waits on this tracker, directly or through another — what an unanswered ask really costs."""
    held, frontier = [], [t["id"]]
    while frontier:
        nxt = [o["id"] for o in trackers if o["status"] in OPEN_STATUSES and o["id"] not in held and o["id"] != t["id"] and set(o.get("blocked_by", [])) & set(frontier)]
        held += nxt
        frontier = nxt
    return held


def ask_key(text):
    """An ask's normalised text, for the duplicate test only: lower case, every run of whitespace one space, trailing
    punctuation dropped. EXACT equality after that, and nothing fuzzy: two questions that differ by a word usually
    differ, and a gate that guesses is a gate people route around."""
    return re.sub(r"\s+", " ", (text or "").strip().lower()).rstrip("?!.…:;, ").strip()


def stated_ask(t):
    """Does this tracker carry an ask anyone must read — one that is open and not yet answered."""
    return t.get("status") in OPEN_STATUSES and not t.get("answer") and (t.get("ask") or t.get("next") == "owner")


def ask_problems(t, by_ask=None, provenance=True):
    """WHAT AN ASK MUST BE, in one place — the reasons this tracker's ask is not one, without its id.

    `lint` refuses on them, and `owner_queue` keeps them out of the Owner's sight: the seat that asks is the seat that
    wants an answer, so no seat polices its own asks. `by_ask` maps a normalised ask to the ids carrying it (the
    duplicate test); `provenance` runs the `seats` check, which costs a version-control call and is skipped where the
    line cannot have changed. A DRAFT — an `ask:` with `next: review` — is held to the form rules and to nothing else:
    any seat may write one, the Principal turns it into an ask the Owner sees."""
    if not stated_ask(t):
        return []
    out, ask, draft = [], (t.get("ask") or "").strip(), t.get("next") == "review"
    if t.get("next") == "owner":
        # 1. NO ASK WITHOUT A RECOMMENDATION. An ask that only asks moves the decision and none of the work.
        if not ask:
            out.append(f'not yet stated as a question — `next: owner` without `ask:`; write `ask:` in {t.get("file", "the tracker")}')
        missing = [k for k in ASK_NEEDS if not (t.get("fm", {}).get(k) or "").strip()]
        if missing:
            out.append("`next: owner` without " + ", ".join(f"`{k}:` ({ASK_NEEDS[k]})" for k in missing)
                       + " — a question with no recommendation moves the decision and none of the work")
    # 2. ONE QUESTION. One sentence, one `?`, at the end — a paragraph with three questions in it gets one answer.
    if ask and (ask.count("?") != 1 or not ask.endswith("?")):
        out.append(f'`ask:` is ONE question — exactly one `?`, at the end; the context goes in the body. Got: {ask[:80]!r}')
    if len(ask) > ASK_MAX:
        out.append(f'`ask:` is {len(ask)} characters — an ask he answers in a sitting is at most {ASK_MAX}; the detail belongs in the body')
    options = t.get("ask_options") or []
    if len(options) > ASK_OPTIONS_MAX:
        out.append(f'`ask-options:` offers {len(options)} choices — at most {ASK_OPTIONS_MAX}; more is a design review, not a question')
    long_ = [o for o in options if len(o) > ASK_OPTION_MAX]
    if long_:
        out.append(f'`ask-options:` — {long_[0][:60]!r} is {len(long_[0])} characters; a choice is at most {ASK_OPTION_MAX}, its rationale goes in `ask-proposal:` or the body')
    twice = [o for o in options if options.count(o) > 1]
    if twice:
        out.append(f'`ask-options:` names {twice[0]!r} twice — each choice appears once')
    # 3. NO DUPLICATE QUESTION. Asked twice, it is answered twice — or, more often, neither time.
    same = [o for o in (by_ask or {}).get(ask_key(ask), []) if o != t["id"]] if ask else []
    if same:
        out.append(f'`ask:` is the same question as {same[0]} — ask on it, or say why this is different in `considered:`')
    if provenance and not draft and t.get("next") == "owner":
        out += seat_problems(t)
    return out


def asks_by_key(trackers):
    """Every open, unanswered ask by its normalised text — what the duplicate test is run against."""
    out = {}
    for t in trackers:
        if stated_ask(t) and t.get("ask"):
            out.setdefault(ask_key(t["ask"]), []).append(t["id"])
    return {k: sorted(v) for k, v in out.items()}


def owner_queue(trackers):
    """What waits for the Owner, oldest ask first: (tracker, age in days or None, what it holds up) — and ONLY what
    passes the ask rules. A malformed one is `malformed_asks` below: the Owner never sees a broken question as a
    question, and a draft (`next: review`) never reaches him at all."""
    today = datetime.date.today()
    by_ask = asks_by_key(trackers)
    age = lambda t: (today - datetime.date.fromisoformat(t["ask_since"])).days if re.fullmatch(r"\d{4}-\d{2}-\d{2}", t.get("ask_since") or "") else None
    q = [(t, age(t), held_up_by(t, trackers)) for t in trackers
         if t["status"] in OPEN_STATUSES and t.get("next") == "owner" and not t.get("answer") and not ask_problems(t, by_ask)]
    return sorted(q, key=lambda r: (-(r[1] if r[1] is not None else -1), r[0]["id"]))


def malformed_asks(trackers):
    """The third layer: what was sent to the Owner and is not a question he can answer — (tracker, reasons), by id.
    The gate already refuses each of these; this is what the board, `--owner` and `--standup` show when one got in
    anyway — on a merge, under `--no-verify`, or from an agent that never ran the gate."""
    by_ask, out = asks_by_key(trackers), []
    for t in sorted(trackers, key=lambda t: t["id"]):
        why = ask_problems(t, by_ask) if t["status"] in OPEN_STATUSES and t.get("next") == "owner" and not t.get("answer") else []
        if why:
            out.append((t, why))
    return out


def bottleneck(q):
    """The one line the Owner is owed when his queue is the finding — not a tracker's problem, his."""
    held = {h for _, _, hs in q for h in hs}
    return f"you are the bottleneck — {len(q)} asks, {len(held)} trackers held up" if len(q) > BOTTLENECK else ""


def sent_back(trackers, log=None):
    """The malformed asks, printed where the Owner would have read them as questions — with the reason each was sent
    back, so the seat that wrote it knows what to fix without opening the gate's output."""
    bad = malformed_asks(trackers)
    if bad:
        print(f"\n{len(bad)} ASK(S) SENT BACK — NOT FOR YOU (the seat fixes these; they reach you when they pass the gate)", file=log or sys.stdout)
        for t, why in bad:
            print(f"  {t['id']} — {why[0]}", file=log or sys.stdout)
    return bad


def answered(trackers):
    """`--answered`: what the Owner answered and nobody has acted on yet — the seat's side of the exchange; and,
    since his last sitting, what WAS acted on, named by the commit that cleared the ask."""
    rows = sorted((t for t in trackers if t.get("answer") and t["status"] in OPEN_STATUSES), key=lambda t: t.get("answered", ""))
    print(f"{len(rows)} ANSWERED, NOT YET ACTED ON" if rows else "NOTHING ANSWERED IS WAITING FOR A SEAT.")
    for t in rows:
        print(f"\n{t['id']} · answered {t['answered']} by {t['answered_by']}\n   asked: {t['ask']}\n   answer: {t['answer']}\n   → act on it, then `{CMD} --clear-ask {t['id']} <next move>` — it moves the exchange into the body under `## {HEAD['asks']}`; the record stays, the ask goes")
    acted = acted_on(trackers)
    if acted:
        print(f"\nACTED ON SINCE THE LAST STANDUP — {len(acted)}")
        for t, commit in acted:
            print(f"  {t['id']} — acted on in `{commit}`")
    return EXIT_OK


def owner_digest(trackers):
    """`--owner`: the digest — what a session's last message leads with. It arrives; a board has to be opened."""
    q = owner_queue(trackers)
    if not q:
        print("NOTHING NEEDS THE OWNER.")
        sent_back(trackers)
        if sessions_digest():
            print("\n" + sessions_digest())
        return EXIT_OK
    ages, held, line = [a for _, a, _ in q if a is not None], sorted({h for _, _, hs in q for h in hs}), bottleneck(q)
    print(f"{len(q)} NEED THE OWNER" + (f" · oldest {max(ages)} day(s)" if ages else "") + (f" · holding up {len(held)}: {', '.join(held)}" if held else "")
          + (f" · {line}" if line else ""))
    for t, a, hs in q:
        print(f"\n{t['id']}" + (f" · {t['ask_kind']}" if t.get("ask_kind") else "") + (f" · asked {a} day(s) ago" if a is not None else "") + (f" · holds up {', '.join(hs)}" if hs else ""))
        print("   " + t["ask"])
    sent_back(trackers)
    if sessions_digest():
        print("\n" + sessions_digest())
    return EXIT_OK


STANDUP_ORDER = (("ruling", "RULINGS — answer; a provisional answer is an answer"),
                 # there was a group here for an ask that did not say which kind it was. `ask-kind:` is now one of the
                 # four lines `next: owner` requires (FM-008), so such an ask is sent back and never reaches a sitting.
                 ("action", "YOUR HANDS — one sitting, in this order: what frees the most comes first"),
                 ("determination", "EVIDENCE COULD SETTLE THESE — agree to the experiment, rule on its result later"),
                 ("ceremony", "BUTTONS — reviewed and accepted, waiting for a click"))


def standup(trackers, invite=None):
    """`--standup`: the agenda of the Owner's one sitting — by kind, and inside a kind by what frees the most.
    `--standup FILE.ics`: the recurring calendar invite for it, weekdays at `standup` for `standup_minutes`."""
    at = str(CONFIG.get("standup") or "").strip()
    if invite is not None and invite != "":
        if not re.fullmatch(r"([01]\d|2[0-3]):[0-5]\d", at):
            print(f'--standup FILE: set the time first — `standup = "09:00"` in {CONFIG_NAME}', file=sys.stderr)
            return EXIT_LINT
        day = datetime.date.today()
        while day.weekday() > 4:
            day += datetime.timedelta(days=1)
        start = datetime.datetime.combine(day, datetime.time(int(at[:2]), int(at[3:])))
        end = start + datetime.timedelta(minutes=int(CONFIG.get("standup_minutes") or 15))
        name = CONFIG["name"] or ROOT.name
        f = lambda d: d.strftime("%Y%m%dT%H%M%S")                # floating time: the Owner's own clock, wherever he is
        lines = ["BEGIN:VCALENDAR", "VERSION:2.0", "PRODID:-//shoalmark//standup//EN", "BEGIN:VEVENT",
                 f"UID:standup-{hashlib.sha256(name.encode()).hexdigest()[:16]}@shoalmark", f"DTSTAMP:{f(datetime.datetime(2000, 1, 1))}Z",
                 f"DTSTART:{f(start)}", f"DTEND:{f(end)}", "RRULE:FREQ=WEEKLY;BYDAY=MO,TU,WE,TH,FR",
                 f"SUMMARY:{name} — standup: what needs you", f"DESCRIPTION:Run `{CMD} --standup` — or open the board: its first lines are the agenda.",
                 "END:VEVENT", "END:VCALENDAR"]
        pathlib.Path(invite).write_bytes(("\r\n".join(lines) + "\r\n").encode("utf-8"))      # a calendar file ends its lines with CRLF, on every system
        print(f"wrote {invite} — weekdays {at}, {int(CONFIG.get('standup_minutes') or 15)} minutes; import it into the Owner's calendar")
        return EXIT_OK
    q = owner_queue(trackers)
    line = bottleneck(q)
    print(f"STANDUP{' — ' + at if at else ''} · {int(CONFIG.get('standup_minutes') or 15)} min · {len(q)} item(s)" + ("" if q else " — nothing needs the Owner today.")
          + (f"\n{line}" if line else ""))
    for kind, title in STANDUP_ORDER:
        rows = sorted((r for r in q if (r[0].get("ask_kind") or "") == kind), key=lambda r: (-len(r[2]), -(r[1] if r[1] is not None else -1), r[0]["id"]))
        if rows:
            print(f"\n{title}")
        for n, (t, a, hs) in enumerate(rows, 1):
            print(f"  {n}. {t['id']} — " + t["ask"] + (f"  [{a} day(s)]" if a is not None else "") + (f"  [frees {', '.join(hs)}]" if hs else ""))
    sent_back(trackers)
    return EXIT_OK


# a ship-log row `--answer … revoke` or `--supersede` writes: `| <date> | Answer of <answered> superseded: *"<answer>"* (<sha>) — …`
SUPERSEDED_RE = re.compile(r'\|\s*(\d{4}-\d{2}-\d{2})\s*\|\s*Answer of [^|]*?superseded: \*".*?"\* \(([0-9a-f]{7,40})\)')


# FM-031 S2 — THE QUEUE IN ONE VIEW. The streams run in parallel, and only the Owner saw the whole queue of pull requests:
# he was the integrator by default. He asked one seat which to merge five times in two hours, and each answer was the
# forge and `git merge-tree`, read by hand. `--queue` reads the same two and gives every open pull request ONE action, in
# the order he takes them. A view: it refuses nothing, and where the forge cannot be read it says so in one line.
QUEUE_FIELDS = "number,title,headRefName,headRefOid,baseRefName,mergeable,mergeStateStatus,createdAt"
QUEUE_BRANCH_MAX = 32      # characters of a branch in a queue line: its id and the start of its slug
QUEUE_ACTION_MAX = 36      # the action column's width at most; a longer action (many paths in conflict) runs on in its own line
EXIT_NO_FORGE = 3          # `--queue` could not read the forge — no `gh`, offline, no GitHub remote. Never 4: a view fails no hook
# a verdict's word, read from its commit's subject (`review: FM-032 at 413451a — READY WITH FINDINGS (…)`); the verdict
# commit itself is found as `--check` finds it, by its `Reviewed: <sha>` trailer
VERDICT_WORD_RE = re.compile(r"\b(NOT READY|READY(?: WITH FINDINGS| TO TAG)?)\b")


def github_remote(url):
    """Whether a remote's URL is on GitHub, the one forge `gh` reads: a host with `github` in its name — github.com, an
    Enterprise host, an ssh alias such as `github-work` — or the host `GH_HOST` names. A local path is no forge."""
    m = re.match(r"(?:[A-Za-z][A-Za-z0-9+.-]*://)?(?:[^@/]*@)?([^/:]+)", (url or "").strip())
    host, named = (m.group(1).lower() if m else ""), (os.environ.get("GH_HOST") or "").strip().lower()
    return bool(host) and ("github" in host or host == named)


def forge_prs():
    """The open pull requests as the forge lists them, with `origin` fetched ONCE — its branches and every pull request's
    head, so a head pushed from a fork is here too — or (None, the one line that says why not): not git, no `origin` on
    GitHub, no `gh`, offline, not logged in."""
    if vcs() != "git":
        return None, "--queue: not a git repository — the queue is read from GitHub with `gh`"
    url = (git_out("remote", "get-url", "origin") or "").strip()
    if not github_remote(url):
        return None, f"--queue: `origin` is {'not on GitHub (' + url + ')' if url else 'not set'} — the queue is read from GitHub with `gh`"
    gh = shutil.which("gh")
    if not gh:
        return None, "--queue: no `gh` on PATH — the queue is read with GitHub's command line (https://cli.github.com, then `gh auth login`)"
    env = dict(nested_git_env(), GH_PROMPT_DISABLED="1")
    try:
        r = subprocess.run([gh, "pr", "list", "--state", "open", "--limit", "100", "--json", QUEUE_FIELDS], cwd=ROOT, capture_output=True,
                           text=True, encoding="utf-8", errors="replace", timeout=30, env=env)
        prs = json.loads(r.stdout) if r.returncode == 0 else None
    except (OSError, ValueError, subprocess.TimeoutExpired) as e:
        return None, f"--queue: `gh pr list` did not answer — offline? ({type(e).__name__})"
    if prs is None:
        return None, "--queue: `gh pr list` failed — " + ((r.stderr or "").strip().splitlines() or ["offline, or not logged in (`gh auth status`)"])[0]
    specs = (git_out("config", "--get-all", "remote.origin.fetch") or "").split() + [f"refs/pull/{p['number']}/head" for p in prs]
    try:
        f = subprocess.run(["git", "fetch", "--quiet", "origin", *specs], cwd=ROOT, capture_output=True, text=True, encoding="utf-8",
                           errors="replace", timeout=60, env=nested_git_env())
    except (OSError, subprocess.TimeoutExpired) as e:
        return None, f"--queue: `git fetch origin` did not answer — offline? ({type(e).__name__})"
    if f.returncode != 0:
        return None, "--queue: `git fetch origin` failed — " + ((f.stderr or "").strip().splitlines() or ["offline?"])[-1]
    return prs, None


def queue_actions(prs):
    """Each open pull request's ONE action, in the order the Owner takes them: what he can act on first, then what waits;
    inside each, the oldest first. Returns [(pr, kind, action, detail)], `kind` one of merge · close · wait. The first
    rule that holds is the action:
    - `closes with PR N` — its head is inside N's head, on the same base (of twins with one head, the newer one closes);
    - `close: carried into PR N` — every commit of its own (not on its base) is on N's branch, as that commit or as the
      same patch;
    - `wait: conflict in <paths>` — `git merge-tree --write-tree origin/<base> <head>` does not merge clean;
    - `wait: NOT READY (<verdict>)` — the last verdict on its head says so;
    - `wait: no verdict on <head>` — no verdict names its head;
    - `merge` — the last verdict on its head says READY, READY WITH FINDINGS or READY TO TAG, and it merges clean.
    A verdict is a commit among the pull requests' own that carries `Reviewed: <sha>`, as `--check` reads one, with its
    word in its subject. It names a head that is <sha>, or that only review addenda follow <sha> to — commits touching
    nothing but `<tracker dir>/evidence/reviews/` and `<tracker dir>/sessions.md`, as a verdict commit itself does."""
    git = lambda *a, **k: subprocess.run(["git", "-c", "core.quotePath=false", *a], cwd=ROOT, capture_output=True, text=True,
                                         encoding="utf-8", errors="replace", env=nested_git_env(), **k)
    rel = TRACKER_DIR.relative_to(ROOT).as_posix()
    reviews, registry = f"{rel}/evidence/reviews/", f"{rel}/sessions.md"
    head, base, num = (lambda p: p["headRefOid"]), (lambda p: "origin/" + p["baseRefName"]), (lambda p: p["number"])
    age = lambda p: (p.get("createdAt") or "", p["number"])
    memo = {}

    def cached(key, f):
        if key not in memo:
            memo[key] = f()
        return memo[key]

    anc = lambda a, b: cached(("anc", a, b), lambda: git("merge-base", "--is-ancestor", a, b).returncode == 0)
    siblings = lambda p: sorted((q for q in prs if q is not p and q["baseRefName"] == p["baseRefName"]), key=age)
    within = {num(p): [q for q in siblings(p) if anc(head(p), head(q)) and (head(p) != head(q) or age(q) < age(p))] for p in prs}
    outermost = lambda qs: min(qs, key=lambda q: (bool(within[num(q)]), age(q)))

    def own(p):
        """its own commits — not on its base, merges aside — and each one's patch id"""
        def read():
            shas = git("rev-list", "--no-merges", head(p), "^" + base(p)).stdout.split()
            diff = git("log", "-p", "--no-merges", "--no-color", "--no-ext-diff", "--format=commit %H", head(p), "^" + base(p)).stdout if shas else ""
            ids = git("patch-id", "--stable", input=diff).stdout if diff else ""
            return shas, {c: pid for pid, c in (l.split()[:2] for l in ids.splitlines() if len(l.split()) >= 2)}
        return cached(("own", num(p)), read)

    def holds(q, p):
        """every commit of p's own is on q's branch — as that commit, or as the same patch"""
        (mine, my_ids), (theirs, their_ids) = own(p), own(q)
        theirs, their_ids = set(theirs), set(their_ids.values())
        return bool(mine) and all(c in theirs or my_ids.get(c) in their_ids for c in mine)

    def conflicts(p):
        r = git("merge-tree", "--write-tree", "--name-only", "--no-messages", base(p), head(p))
        if r.returncode in (0, 1):
            return list(dict.fromkeys(l for l in r.stdout.splitlines()[1:] if l.strip()))
        # merge-tree could not run — a git older than 2.38, or a head that is not here: the forge's own word stands in
        return ["(paths unread — the forge says CONFLICTING)"] if p.get("mergeable") == "CONFLICTING" else []

    heads = sorted({head(p) for p in prs})
    bases = sorted({"^" + base(p) for p in prs if git("rev-parse", "--verify", "--quiet", base(p)).returncode == 0})
    log = git("log", f"--format=%H%x01%s%x01{TRAILERS}%x02", *heads, *bases).stdout if heads else ""
    verdicts = []                                           # newest first: (verdict, the full sha it reviewed, its word)
    for rec in log.split("\x02"):
        sha, _, rest = rec.strip("\n").partition("\x01")
        subject, _, block = rest.partition("\x01")
        reviewed, word = trailer_values(block, "Reviewed"), VERDICT_WORD_RE.search(subject)
        if sha and reviewed and word:
            full = git("rev-parse", "--verify", "--quiet", reviewed[0] + "^{commit}").stdout.strip()
            if full:
                verdicts.append((sha, full, word.group(1)))

    def addenda_only(r, h):
        """every commit from r to h touches only a review or the registry — and none is a merge, which brings a line's files"""
        def read():
            out = git("log", "--format=%x00%P", "--name-only", "--no-renames", f"{r}..{h}")
            for chunk in out.stdout.split("\x00")[1:]:
                parents, *paths = chunk.strip("\n").split("\n")
                if len(parents.split()) > 1 or any(x and not (x.startswith(reviews) or x == registry) for x in paths):
                    return False
            return out.returncode == 0
        return cached(("addenda", r, h), read)

    rows = []
    for p in prs:
        carried = [q for q in siblings(p) if holds(q, p) and not (holds(p, q) and age(p) < age(q))] if not within[num(p)] else []
        paths = conflicts(p) if not (within[num(p)] or carried) else []
        last = next(((v, w) for v, r, w in verdicts if r == head(p) or (anc(r, head(p)) and addenda_only(r, head(p)))), None)
        if within[num(p)]:
            rows.append((p, "close", f"closes with PR {num(outermost(within[num(p)]))}", ""))
        elif carried:
            rows.append((p, "close", f"close: carried into PR {num(outermost(carried))}", ""))
        elif paths:
            rows.append((p, "wait", "wait: conflict in " + ", ".join(paths), ""))
        elif last is None:
            rows.append((p, "wait", f"wait: no verdict on {head(p)[:7]}", ""))
        elif last[1] == "NOT READY":
            rows.append((p, "wait", f"wait: NOT READY ({last[0][:7]})", ""))
        else:
            rows.append((p, "merge", "merge", f"verdict {last[0][:7]} {last[1]}"))
    return sorted(rows, key=lambda row: (row[1] == "wait", age(row[0])))


def queue_lines(rows):
    """The queue as the Owner reads it: one line per pull request, its columns aligned, and the count last."""
    cut = lambda b: b if len(b) <= QUEUE_BRANCH_MAX else b[:QUEUE_BRANCH_MAX - 1] + "…"
    cells = [(f"PR {p['number']}", action, f"{cut(p['headRefName'])} @ {p['headRefOid'][:7]}", detail) for p, _k, action, detail in rows]
    w = [max([len(c[i]) for c in cells] or [0]) for i in range(3)]
    w[1] = max([len(c[1]) for c in cells if len(c[1]) <= QUEUE_ACTION_MAX] or [0])      # an action past the cap runs on in its own line
    kinds = collections.Counter(k for _p, k, _a, _d in rows)
    return ([f"{a:<{w[0]}}  {b:<{w[1]}}  {c:<{w[2]}}  {d}".rstrip() for a, b, c, d in cells]
            + [f"{len(rows)} waiting on you: {kinds['merge']} merge, {kinds['close']} close, {kinds['wait']} wait"])


def queue_cmd():
    """`--queue`: the open pull requests, one action each, in the order to take them — exit 3 where the forge cannot be read."""
    prs, why = forge_prs()
    if prs is None:
        print(why, file=sys.stderr)
        return EXIT_NO_FORGE
    print("\n".join(queue_lines(queue_actions(prs))))
    return EXIT_OK


def queue_section():
    """`--owner` and `--standup` end with the queue where the forge can be read — and say nothing of it where it cannot."""
    prs, _why = forge_prs()
    if prs is not None:
        print("\nPULL REQUESTS — in the order to take them")
        print("\n".join("  " + line for line in queue_lines(queue_actions(prs))))


def answer_step(tid, n, text):
    """`--answer` says what it is doing AS EACH STEP STARTS — on stderr, flushed, before the wait and not after it. It
    reads the trackers, and a checkout hook and the pre-commit gate read them again; silent for that long, it was
    stopped by an Owner who took it for hung (FM-012). What it prints at the end is unchanged."""
    print(f"answering {tid} — {n}/4 {text} …", file=sys.stderr, flush=True)


def answer_cmd(words, trackers, supersede=False):
    """`--answer <id> accept|reject [text]` — the Owner's one command. It does what he did by hand the first time: cuts
    `answer/<id>` from the branch that carries the ask, writes the three lines, commits SIGNED under his name, pushes,
    and goes back to the branch it started on. It refuses before touching anything when it cannot end in a verified answer.
    An answer he takes back or changes (`revoke "<reason>"`, or `accept|reject "<option>" --supersede`) is never lost:
    the answer it replaces moves into the ship log, with the commit that wrote it."""
    if len(words) < 2 or words[1] not in ("accept", "reject", "revoke"):
        print("--answer <id> accept|reject [\"text\"] — reject needs a reason; accept takes an optional change. "
              "An answer given already: `--answer <id> revoke \"<reason>\"`, or `--answer <id> accept|reject \"<option>\" --supersede`", file=sys.stderr)
        return EXIT_LINT
    # the answer is ONE front-matter line: every run of whitespace — a newline above all — collapses to one space.
    # A newline would close the line and the next fragment would be read as another key (`status: Shipped` flipped one),
    # and the tracker's body is where a long answer belongs.
    tid, verdict, text = words[0].upper(), words[1], " ".join(" ".join(words[2:]).split())
    t = next((x for x in trackers if x["id"] == tid), None)
    if not t or not t.get("ask") or t.get("next") != "owner":
        print(f"--answer: {tid} asks the Owner nothing — an answer answers an `ask:` with `next: owner`", file=sys.stderr)
        return EXIT_LINT
    if t.get("answer") and not (supersede or verdict == "revoke"):
        print(f"--answer: {tid} is answered already ({t['answered']}, {t['answered_by']}) — an answer is never overwritten in place. "
              f"To take it back: `{CMD} --answer {tid} revoke \"<reason>\"`; to change it: `{CMD} --answer {tid} accept|reject \"<option>\" --supersede` — "
              f"either way the answer it replaces moves into the ship log", file=sys.stderr)
        return EXIT_LINT
    if not t.get("answer") and (supersede or verdict == "revoke"):
        print(f"--answer: {tid} carries no answer to " + ("revoke" if verdict == "revoke" else "supersede") + f" — answer it: `{CMD} --answer {tid} accept|reject`", file=sys.stderr)
        return EXIT_LINT
    if verdict == "reject" and not text:
        print("--answer: a rejection carries its reason, and how the ask should be reworded", file=sys.stderr)
        return EXIT_LINT
    if verdict == "revoke" and not text:
        print("--answer: a revocation carries its reason — the ship log keeps it beside the answer it takes back", file=sys.stderr)
        return EXIT_LINT
    if vcs() != "git":
        print(f"--answer: this is a git command; under Subversion, write the three lines and `svn commit` — the server signs for you", file=sys.stderr)
        return EXIT_LINT
    for p_ in answerers_problems():                           # a signature the configuration asks for and `[seats]` drops (FM-015)
        print(f"--answer: {p_}", file=sys.stderr)
        return EXIT_LINT
    # who may answer is asked in ONE place, `may_answer()`: with `[seats]`, the seats that hold `answer`, matched on
    # the identity git will actually write; with none, `answerers`, which always meant the author's name
    me, allowed = git_user(), may_answer()
    pend_name, pend_email = pending_author()                 # who git will actually author as — the seat is matched on that
    seat = seat_of(pend_name or me, pend_email) if SEATS else None
    if SEATS and not holds(seat, "answer"):
        print("--answer: " + no_seat(pend_name or me, pend_email, "answer", "an answer is an `answer` change"), file=sys.stderr)
        return EXIT_LINT
    if not SEATS and me not in allowed:
        print(f"--answer: `{me}` is not in `answerers` ({', '.join(allowed) or 'nobody'}) — {CONFIG_NAME} says who may answer", file=sys.stderr)
        return EXIT_LINT
    signed = (SEATS[seat][1] if SEATS else allowed.get(me)) == "signed"
    git = lambda *a: subprocess.run(["git", *a], cwd=ROOT, capture_output=True, text=True, encoding="utf-8", errors="replace", env=nested_git_env())
    dirty = changed_paths(git)
    if dirty:
        print(dirty_refusal(git, dirty), file=sys.stderr)
        return EXIT_LINT
    if signed and not git("config", "user.signingkey").stdout.strip():
        print(f'--answer: `{"[seats]" if SEATS else "answerers"}` asks for a signed answer and no `user.signingkey` is set — see the signing page, {SIGNING_PAGE}', file=sys.stderr)
        return EXIT_LINT
    # `answered-by:` is `user.name`, but the commit's author is whatever git will actually write — `GIT_AUTHOR_NAME` in
    # the environment overrides the configuration. The gate reads the author, so the two disagreeing is an answer filed
    # from an account that did not give it. Asked before anything is touched.
    author = git("var", "GIT_AUTHOR_IDENT").stdout.partition(" <")[0].strip()
    if author != me:
        print(f"--answer: git would author this commit as `{author}`, not `{me}` — the environment (GIT_AUTHOR_NAME) overrides `user.name`; "
              f"unset it, or the answer is filed from an account that did not give it", file=sys.stderr)
        return EXIT_LINT
    path = TRACKER_DIR / t["file"]
    rel = path.relative_to(ROOT).as_posix()
    # the ask is a front-matter LINE, and the answer is written under it: an ask that parsed (indented, or under a key
    # the file spells another way) but is not one raised out of `next(...)` with a traceback instead of a refusal.
    # Asked before the branch is cut — nothing is touched for an answer that cannot be written
    if not any(l.startswith("ask:") for l in path.read_text(encoding="utf-8").split("\n")):
        print(f"--answer: {tid} has no `ask:` line in {t['file']} — the front matter's question is what the answer is written under; "
              f"the ask is there but not as its own line (indented, or wrapped). Fix the file, then answer", file=sys.stderr)
        return EXIT_LINT
    answer = {"accept": "accepted", "reject": "rejected", "revoke": "revoked"}[verdict] + (f" - {text}" if text else "")
    again = f'{CMD} --answer {tid} {verdict}' + (f' "{text.replace(chr(34), chr(39))}"' if text else "") + (" --supersede" if supersede else "")
    branch, here, start = f"answer/{tid.lower()}", git("branch", "--show-current").stdout.strip(), git("rev-parse", "HEAD").stdout.strip()
    created = switched = False
    # the answer this one replaces, and the commit that wrote it — read here, on the branch the new one is cut from
    replaced = (t["answer"], t.get("answered", ""), (line_author(path, "answer:")[3] or "")[:7] or "not committed") if t.get("answer") else None

    def undo(what, said=""):
        """FM-017: a run that fails after it has written anything leaves NOTHING behind. It began on a tree with no tracked
        change (refused above otherwise), so every tracked path that differs now is its own — the tracker it wrote, the
        INDEX.md a hook regenerated — and is restored. Then it goes back to the branch it started on, and an
        `answer/<id>` it cut and never committed to is deleted. Left behind, those made the Owner's next `--answer`, on
        another ask, refuse as a dirty tree without saying why. His answer is printed with the command that gives it
        again: a refusal never costs him the words."""
        restored = changed_paths(git)
        if restored:
            git("restore", "--staged", "--worktree", "--", *[f":(top){p_}" for p_ in restored])
        back = gone = ""
        if switched:
            s_ = git("switch", here) if here else git("switch", "--detach", start)
            back = f"back on `{here or start[:10]}`" if s_.returncode == 0 else f"could NOT switch back to `{here or start[:10]}` — {s_.stderr.strip()[-160:]}"
            if created and s_.returncode == 0 and git("rev-parse", "--verify", "-q", branch).stdout.strip() == start and git("branch", "-D", branch).returncode == 0:
                gone = f"`{branch}` deleted — it carried no commit"
        print(f"--answer: {what}" + ("".join(f"\n    {l_}" for l_ in said.splitlines()) if said else ""), file=sys.stderr)
        print("  undone: " + " · ".join(x for x in (f"restored {', '.join(restored)}" if restored else "", back, gone) if x) if restored or back else "  nothing was changed", file=sys.stderr)
        print(f"  your answer, not lost: {answer}\n  to give it again: {again}", file=sys.stderr)
        return EXIT_LINT

    if here != branch:
        if git("rev-parse", "--verify", "-q", branch).returncode == 0:
            # an `answer/<id>` left from an earlier answer on this tracker: merged, it is spent — deleted and cut fresh from
            # the branch that carries the ask; not merged, it may hold work, and nothing unmerged is ever deleted for him
            trunk = default_trunk(git)
            if not trunk or git("merge-base", "--is-ancestor", branch, trunk).returncode != 0:
                print(f"--answer: `{branch}` exists and is not merged into `{trunk or 'origin'}` — it may hold work, and nothing is deleted for you. "
                      f"Clear it with `git branch -D {branch}`, then answer again", file=sys.stderr)
                return EXIT_LINT
            if git("branch", "-D", branch).returncode != 0:
                print(f"--answer: `{branch}` is merged into `{trunk}`, and could not be deleted — `git branch -D {branch}`, then answer again", file=sys.stderr)
                return EXIT_LINT
            print(f"--answer: `{branch}` was left by an earlier answer and is merged into `{trunk}` — deleted, and cut fresh", file=sys.stderr)
        answer_step(tid, 2, f"cutting `{branch}` from `{here or 'a detached HEAD'}` — the checkout hook, where one is installed, rebuilds the board")
        r = git("switch", "-c", branch)                        # from the branch that carries the ask: this one
        created = r.returncode == 0
        if r.returncode:
            return undo(f"could not switch to `{branch}` — {r.stderr.strip()[-300:]}")
        switched = True
    else:
        answer_step(tid, 2, f"on `{branch}` already")
    lines = path.read_text(encoding="utf-8").split("\n")
    at = next((i for i, l in enumerate(lines) if l.startswith("ask:")), None)
    if at is None:
        return undo(f"{tid} has no `ask:` line in {t['file']} on `{branch}` — the front matter's question is what the answer is written under")
    if replaced:                                             # the lines it replaces leave the front matter, and the ship log keeps them
        end = next((i for i, l in enumerate(lines) if i and l.strip() == "---"), len(lines))
        lines = [l for i, l in enumerate(lines) if i >= end or not l.startswith(("answer:", "answered:", "answered-by:"))]
        at = next(i for i, l in enumerate(lines) if l.startswith("ask:"))
    while at + 1 < len(lines) and lines[at + 1].startswith("ask-"):
        at += 1
    lines[at + 1:at + 1] = [f'answer: "{answer.replace(chr(34), chr(39))}"', f"answered: {datetime.date.today().isoformat()}", f"answered-by: {me}"]
    if replaced:
        cell = lambda v: v.replace(chr(34), chr(39)).replace("|", "\\|")
        lines = ship_log_row(lines, f'Answer of {replaced[1]} superseded: *"{cell(replaced[0])}"* ({replaced[2]}) — '
                                    + (f"revoked: {cell(text)}" if verdict == "revoke" else f'replaced by: *"{cell(answer)}"*'))
    try:
        put(path, "\n".join(lines))
    except OSError as e:
        return undo(f"could not write {rel} — {e}")
    if git("add", "--", rel).returncode:
        return undo(f"could not stage {rel}")
    answer_step(tid, 3, "committing, signed — your key may ask for a touch or its passphrase; the pre-commit gate runs" if signed
                else "committing — the pre-commit gate runs")
    r = git("commit", *(["-S"] if signed else []), "-m", f"{tid}: {answer[:60]}")
    if r.returncode:
        # what refused it is the HOOK's output, not git's last line — its tail, as the gate printed it
        said = re.sub(r"\x1b\[[0-9;]*[A-Za-z]", "", (r.stdout.strip() + "\n" + r.stderr.strip()).strip())
        return undo("the commit was refused — nothing is committed. What refused it:", "\n".join(said.splitlines()[-20:]) or "(git said nothing)")
    if signed:
        # the gate's own rule, asked here so the answer is never pushed under one the gate will refuse: a good signature
        # (`%G?`) AND the principal the key is trusted for (`%GS`) being the author's email — a trusted key still says
        # nothing about whose name is on the commit
        good, signer, email = (git("log", "-1", "--format=%G?%n%GS%n%ae").stdout.split("\n") + ["", "", ""])[:3]
        if good.strip() != "G" or email.strip() not in signer:
            print(f"--answer: committed, but the signature does not verify as `{me}` — `git commit --amend -S`, or check the signers file; "
                  f"NOT pushed, and the gate would refuse this answer", file=sys.stderr)
            return EXIT_LINT
    answer_step(tid, 4, "pushing to `origin`")
    r = git("push", "-u", "origin", branch)
    print(f"{tid} answered: {answer}\n  signed, on `{branch}`" + (", pushed" if r.returncode == 0 else f" — NOT pushed: {r.stderr.strip()[-160:]}") + f"\n  it has left your queue; the seat sees it under --answered")
    if r.returncode != 0:
        return EXIT_LINT
    if switched:                                             # pushed: back where he started, so his next --answer does not begin on this one's branch
        s_ = git("switch", here) if here else git("switch", "--detach", start)
        print(f"  back on `{here or start[:10]}`" if s_.returncode == 0 else f"  could NOT switch back to `{here or start[:10]}` — {s_.stderr.strip()[-160:]}")
    return EXIT_OK


def default_trunk(git):
    """`origin`'s default branch as this clone last fetched it — `origin/HEAD`, else `origin/main`, else `origin/master` —
    or None: what an earlier `answer/<id>` must be merged into before `--answer` deletes it."""
    head = git("symbolic-ref", "--quiet", "refs/remotes/origin/HEAD").stdout.strip()
    if head.startswith("refs/remotes/"):
        return head[len("refs/remotes/"):]
    return next((r for r in ("origin/main", "origin/master") if git("rev-parse", "--verify", "--quiet", r + "^{commit}").returncode == 0), None)


def ship_log_table(lines):
    """Where a tracker's ship log is: (its heading's line, the table's rule line or None, the last row's line, newest
    first?) — or None where it has no log. The order is the log's own: oldest first only when its first dated row is
    older than its last; this repository writes the newest on top."""
    head_re = re.compile(r"^#{2,3}\s+(ship log|" + re.escape(HEAD["log"]) + r")\s*$", re.I)
    at = next((i for i, l in enumerate(lines) if head_re.match(l)), None)
    if at is None:
        return None
    end = next((i for i in range(at + 1, len(lines)) if re.match(r"^#{1,3}\s", lines[i])), len(lines))
    sep = next((i for i in range(at + 1, end) if TABLE_SEP_RE.match(lines[i])), None)
    last = sep
    while sep is not None and last + 1 < end and lines[last + 1].lstrip().startswith("|"):
        last += 1
    dates = [m.group(1) for m in (re.match(r"\|\s*(\d{4}-\d{2}-\d{2})", lines[i].strip()) for i in range(sep + 1, last + 1)) if m] if sep is not None else []
    return at, sep, last, not (len(dates) >= 2 and dates[0] < dates[-1])


def ship_log_row(lines, event):
    """A tracker's lines with one ship-log row for today, where the log's own order puts it: first under its header when
    the newest row is on top, last when it runs oldest first. A tracker with no log gets one."""
    row, log = f"| {datetime.date.today().isoformat()} | {event} |", ship_log_table(lines)
    if log is None:
        while lines and not lines[-1].strip():
            lines = lines[:-1]
        return lines + ["", f"## {HEAD['log']}", "", "| Date | Event |", "|---|---|", row, ""]
    at, sep, last, newest_first = log
    if sep is None:
        return lines[:at + 1] + ["", "| Date | Event |", "|---|---|", row] + lines[at + 1:]
    at_row = sep + 1 if newest_first else last + 1
    return lines[:at_row] + [row] + lines[at_row:]


def superseded(body):
    """The commit that wrote the answer this tracker's answer replaced — from the newest ship-log row `--answer … revoke`
    or `--supersede` wrote, read in the log's own order — or ""."""
    lines = body.split("\n")
    log = ship_log_table(lines)
    if not log or log[1] is None:
        return ""
    hits = [m.group(2) for m in (SUPERSEDED_RE.match(lines[i].strip()) for i in range(log[1] + 1, log[2] + 1)) if m]
    return (hits[0] if log[3] else hits[-1]) if hits else ""


def changed_paths(git):
    """Every tracked path that differs from HEAD, staged or not — repository-relative, as git names them. `-z`, so a
    path git would quote comes back as it is; a rename's second name, which `-z` sends after it, is skipped."""
    out, paths, skip = git("status", "--porcelain", "-z", "--untracked-files=no").stdout.split("\0"), [], False
    for entry in out:
        if skip or len(entry) < 4:
            skip = False
            continue
        paths.append(entry[3:])
        skip = entry[0] in "RC"
    return paths


def dirty_refusal(git, dirty):
    """`--answer` on a tree with changes: WHICH paths, and — where one is a tracker carrying an answer that is not
    committed — that it looks like an earlier `--answer` that failed half-way (0.17.3 left its writes behind, FM-017), the
    one command that undoes it, and the answer it would have filed, so the Owner never types it from memory."""
    top = pathlib.Path(git("rev-parse", "--show-toplevel").stdout.strip() or ROOT)
    said = f"--answer: the working tree has changes — an answer is one commit with nothing else in it. Changed: {', '.join(dirty)}"
    left = []
    for p_ in dirty:
        name = p_.rsplit("/", 1)[-1]
        if not KIND_RE.match(name) or not (top / p_).is_file():
            continue
        now_ = (parse_frontmatter((top / p_).read_text(encoding="utf-8"))[0].get("answer") or "").strip()
        was_ = (parse_frontmatter(git("show", f"HEAD:{p_}").stdout)[0].get("answer") or "").strip()
        if now_ and now_ != was_:
            left.append((p_, "-".join(name.split("-")[:2]), now_.strip('"')))
    if not left:
        return said + " — commit or stash them first"
    generated = {pathlib.Path(os.path.relpath(f, top)).as_posix() for f in [OUT, *DERIVED_FILES]}
    mine = [p_ for p_ in dirty if p_ in {l_[0] for l_ in left} | generated]
    theirs = [p_ for p_ in dirty if p_ not in mine]
    for p_, tid, ans in left:
        m = re.fullmatch(r"(accepted|rejected)(?:\s+-\s+(.*))?", ans)
        said += (f"\n  {tid} carries an answer that was never committed — {ans!r}. It looks like an earlier `--answer` that failed half-way"
                 + (f"; to give it again: {CMD} --answer {tid} {m.group(1)[:-2]}" + (f' "{m.group(2)}"' if m.group(2) else "") if m else ""))
    said += (f"\n  undo what it left with ONE command:\n    git{'' if top == ROOT else ' -C ' + str(top)} restore --staged --worktree -- {' '.join(mine)}"
             + (f"\n  the rest is not the tool's — commit or stash it: {', '.join(theirs)}" if theirs else ""))
    return said


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
            + (["kind"] if t.get("next") == "build" and not t.get("problem") else []) + list(t.get("x_needs") or []))


def intent_of(t, by_id):
    """The tracker's own `intent:`, else its story's — what the work is FOR, in the Owner's words."""
    return t.get("intent") or (by_id.get(t.get("epic") or "", {}).get("intent") or "")


def render(rows, kind_label):
    rows = sorted(rows, key=lambda r: (STATUS_ORDER.get(r["status"], 9), -r["num"]))
    out = [
        f"## {kind_label}\n",
        "| ID | Tier | Hook | Status | Board | Triaged |" + "".join(f" {c} |" for c in INDEX_COLUMNS),
        "|----|------|------|--------|-------|---------|" + "".join("-" * (len(c) + 2) + "|" for c in INDEX_COLUMNS),
    ]
    for r in rows:
        out.append(
            f"| [{r['id']}]({r['file']}) | {r['tier']} | {r['hook']} | {status_cell(r)} "
            f"| {board(r)} | {r.get('triaged') or '—'} |" + "".join(f" {(r.get('x') or {}).get(c, '—').replace('|', chr(92) + '|')} |" for c in INDEX_COLUMNS)
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
<meta name="color-scheme" content="light dark">__FAVICON__
<title>__NAME__ — work tracker</title>
<style>
:root{--bg:#f7f7f5;--ink:#161616;--dim:#565656;--mute:#6e6e6e;--line:rgba(0,0,0,.14);--teal:#1a7f5a;--coral:#b3402f;--blue:#2f62d6;--yellow:#946c0f}
@media(prefers-color-scheme:dark){:root{--bg:#0e0e0e;--ink:#efefef;--dim:#ababab;--mute:#8f8f8f;--line:rgba(255,255,255,.15);--teal:#4fd1a1;--coral:#ff7b66;--blue:#6f9bff;--yellow:#e8cf5a}}
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
/* the brand: a logo, the name, a tagline — and a footer, all empty unless someone says otherwise */
#H{display:flex;gap:10px;align-items:center;margin-bottom:14px}#H img{height:22px;width:auto}#H b{font-size:16px}#s{margin-left:auto}#H span,#f{color:var(--mute);font-size:13px}
button.act{border:1px solid var(--line);padding:2px 7px;margin-left:6px;font-size:11px;text-transform:none;letter-spacing:0}button.act:hover{border-color:var(--ink);color:var(--ink)}
#dlg{border:1px solid var(--line);background:var(--bg);color:var(--ink);max-width:640px;width:calc(100% - 32px);padding:18px 20px}#dlg::backdrop{background:rgba(0,0,0,.45)}
#dlg h3{margin:0 0 10px;font-size:14px;font-weight:600}#dlg .dq{font-size:16px;font-weight:500;margin:0 0 8px;display:block}#dlg .dp{margin:0 0 8px;color:var(--dim)}#dlg .ddim{color:var(--mute);font-size:12px}
#dlg .dl{display:flex;gap:8px;align-items:center;justify-content:flex-start;margin:8px 0 4px;font-size:14px}#dlg .dl input{margin:0;flex:0 0 auto;min-width:0;width:auto}#dlg textarea{width:100%;font:13px/1.4 system-ui,sans-serif;background:none;color:var(--ink);border:1px solid var(--line);padding:6px;margin-top:4px}#dlg textarea:disabled{opacity:.4}
#dlg menu{display:flex;gap:8px;margin:14px 0 0;padding:0}#dlg button{border:1px solid var(--line);padding:6px 12px;font-size:12px}#dlg button.go{border-color:var(--ink);color:var(--ink)}#dlg button:disabled{opacity:.4}
/* the second screen: the decision is made, the terminal signs it — the command, then where, what, the end, the check, the way out */
#dlg h4{margin:14px 0 4px;font-size:11px;font-weight:400;letter-spacing:.08em;text-transform:uppercase;color:var(--mute)}#dlg ol{margin:4px 0;padding-left:20px}#dlg li{margin:2px 0}#dlg p{margin:4px 0}
#dlg pre{font:13px/1.45 "Berkeley Mono",ui-monospace,monospace;margin:6px 0;padding:8px 10px;border:1px solid var(--line);white-space:pre-wrap;word-break:break-all}#dlg pre.cmd{border-left:2px solid var(--teal);user-select:all}
#dlg code{font:12px "Berkeley Mono",ui-monospace,monospace}#dlg button.copy{padding:2px 8px;font-size:11px;text-transform:none;letter-spacing:0}#dlg .said{margin-left:6px}#dlg .sign a{text-decoration:underline}
#l span{text-transform:lowercase}#f{margin-top:28px}#f:empty,#H span:empty{display:none}
/* on paper the board is always the light one */
@media print{#s{display:none}}
@media print{:root{--bg:#fff;--ink:#000;--dim:#333;--mute:#555;--line:rgba(0,0,0,.25)}header,#l{display:none}}
</style>__THEMES__
<div id="B"><div id="H">__LOGO__<b>__NAME__</b><span data-l="tagline"></span><button id="s"></button></div>
<header><input id="q" autofocus>
<button id="g" aria-pressed="true"></button><button id="o" aria-pressed="true" data-l="view.open"></button><button id="a" aria-pressed="false" data-l="view.all"></button><span id="n" class="m"></span></header>
<p id="l" class="m"><i class="q"></i><span data-l="status.Proposed"></span><i class="q b"></i><span data-l="status.In Progress"></span><i class="q y"></i><span data-l="status.Parked"></span><i class="q r"></i><span data-l="status.Blocked"></span><i class="q t"></i><span data-l="status.Shipped"></span><i class="q z"></i><span data-l="status.Closed"></span></p>
<p id="p"></p>
<table><thead><tr><th data-l="col.id"><th data-l="col.tier"><th data-l="col.status">__COLHEADS__<th data-l="col.title"></thead><tbody id="b"></tbody></table>
<p id="f" class="m" data-l="footer"></p></div>
<article id="v" hidden></article>
<dialog id="dlg"></dialog>
<script>__MARKED__</script>
<script>
// row = [id, tier, status, —, —, file, title, hook, num, —, —, —, [linked ids], epic, state, [#tags], [blocked_by], triaged, rank, board, [ready marks that fail — open work only], next move, intent (own or its story's), the story it is inherited from, [date, verdict, reason] of the newest pass, tokens to read it, [kind of problem, judged — else it is from the move]]
const BLOB=__BLOB__,HOME=__HOME__,REG=__REG__,COLS=__COLS__,BCOLS=__BCOLS__,L=__LABELS__,BRANCH=__BRANCH__,T=[
__ROWS__
];
const OPEN=new Set(["In Progress","Parked","Proposed","Reserved","?"]),$=i=>document.getElementById(i),
esc=s=>s.replace(/[&<>"]/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[c])),
dec=s=>{try{return decodeURIComponent(s)}catch(e){return s}},          // `#100%` must not blank the page
// every word of the chrome comes from L (labels.yaml, merged over the built-in English). What the page's LOGIC compares —
// a status, a section, a move — stays the word an agent types; only what is SHOWN goes through here.
l=(k,...a)=>esc((L[k]??k).replace(/\{(\d)\}/g,(m,i)=>a[i]??"")),sl=s=>L["status."+s]||s,vn=g=>L["view."+g]||g,
// …and `lh` for a label whose {0} is MARKUP the page built itself (a `<code>`, a link): the label is escaped, the parts are not
lh=(k,...a)=>esc(L[k]??k).replace(/\{(\d)\}/g,(m,i)=>a[i]??""),
byId=new Map(T.map(t=>[t[0],t])),inb=new Map();
for(const t of T)for(const l of t[12])inb.set(l,[...(inb.get(l)||[]),t[0]]);
EPICS=new Set(T.map(t=>t[13])),
xv=(t,c)=>(t[27]||{})[c]||"—",                          // a derived value — a column, a fact, a search word and a view
ver=k=>(k.match(/\d+(?:\.(?:\d+|x))+/)||[""])[0].split(".").map(p=>p=="x"?999:+p),
vcmp=(a,b)=>{if(a=="—"||b=="—")return(a=="—")-(b=="—");const x=ver(a),y=ver(b);for(let i=0;i<4;i++){const d=(y[i]||0)-(x[i]||0);if(d)return d}return a<b?-1:a>b},
GROUPS=[["board",t=>board(t)],["epic",t=>t[13]!="—"?t[13]:EPICS.has(t[0])?t[0]:"—"],...COLS.map(c=>[c.toLowerCase(),t=>xv(t,c)])],   // board · story · then every derived column is a view
// blocked is derived, never typed: open work whose named blocker is still open (or is the Owner)
blocked=t=>OPEN.has(t[2])&&t[16].some(b=>b.startsWith("Owner")||byId.has(b)&&OPEN.has(byId.get(b)[2])),
// the board — the generator puts every tracker in exactly one of progress · triage · backlog · done (the same
// word INDEX.md prints); `triaged` repeats the
// newest pass under `triage`. A judgement on work in progress holds __DAYS__ days, then it is back in `triage`; parked work does not go stale.
LAST=T.reduce((m,t)=>t[17]>m?t[17]:m,""),
fresh=t=>!!t[17]&&Date.now()-Date.parse(t[17])<(__DAYS__+1)*864e5,   // through day __DAYS__ inclusive — the same day the command stops calling it fresh
recent=t=>!!t[17]&&t[17]==LAST,
untriaged=t=>t[19]=="triage"||t[2]=="In Progress"&&!fresh(t),   // exactly what the next `--triage` lists: the generator's word, and work in progress judged too long ago
// has a pass run? ONE answer for every line that asks: the newest date a pass left on a tracker, or else the date of the
// newest pass TRIAGE.md records. `progress` holds only what a pass kept — until a first pass it is empty by rule and says so (FM-021)
PASSED=LAST||(HOME.last.match(/\d{4}-\d\d-\d\d/)||[""])[0],
BOARD={progress:PASSED?l("desc.progress"):l("desc.progress.none"),triage:l("desc.triage","__DAYS__"),triaged:PASSED?l("desc.triaged",PASSED):l("desc.triaged.none"),backlog:l("desc.backlog"),done:l("desc.done")},
board=t=>[...(recent(t)?["triaged"]:[]),untriaged(t)?"triage":t[19]],   // t[19] is the generator's; staleness is the one clock rule, and only work in progress goes stale
MARK={"In Progress":"b","Shipped":"t","Parked":"y","Closed":"z"},mark=t=>blocked(t)?"r":t[2].startsWith("Shipped")?"t":MARK[t[2]]||"",
ids=s=>esc(s).replace(/\b(?:__KINDS__)-\d+\b/g,i=>byId.has(i)?`<a href="#=${i}">${i}</a>`:i),   // TRIAGE.md — an id opens its tracker rendered, as in a row
chips=(ids,arrow,to="~")=>ids.length?`<div class="m">${arrow} `+ids.map(i=>`<a href="#${to}${i}" class="${byId.has(i)&&OPEN.has(byId.get(i)[2])?"":"off"}">${i}</a>`).join(" ")+"</div>":"";
let all=false,gi=0,shut=new Set(),touched=new Set();
function draw(){
  // a whole id alone is that tracker — not every row whose body links to it (FM-020). What links to it is `~ID` (Markdown
  // links only: a chapter's `epic:` and `blocked-by:` are not in it); a story's chapters are the story view
  const q=$("q").value.trim(),hood=q[0]=="~"&&byId.get(q.slice(1).toUpperCase()),exact=!hood&&byId.get(q.toUpperCase()),words=q.toLowerCase().split(/\s+/).filter(Boolean);
  const near=hood&&new Set([hood[0],...hood[12],...(inb.get(hood[0])||[])]),[gname,gkey]=GROUPS[gi],every=all||gname=="board";
  const rows=T.filter(t=>hood?near.has(t[0]):exact?t==exact:(every||OPEN.has(t[2]))&&words.every(w=>(t.slice(0,27).join(" ")+" "+Object.values(t[27]||{}).join(" ")+" "+sl(t[2])+(blocked(t)?" blocked "+sl("Blocked"):"")+(untriaged(t)?" untriaged "+(L["count.untriaged"]||""):"")).toLowerCase().includes(w)))
    .sort((x,y)=>(x[2]=="Parked")-(y[2]=="Parked")||((x[18]||99)-(y[18]||99))||(x[1]<y[1]?-1:x[1]>y[1]?1:0)||y[8]-x[8]);
  const groups=new Map(),order=Object.keys(BOARD);
  for(const t of rows)for(const k of[].concat(gkey(t)))groups.set(k,[...(groups.get(k)||[]),t]);
  if(gname=="board"&&!q&&!hood)for(const k of order)groups.set(k,groups.get(k)||[]);   // the board always shows its five — an empty section is an answer
  const keys=[...groups.keys()].sort(gname=="board"?(a,b)=>order.indexOf(a)-order.indexOf(b):gname=="epic"?(a,b)=>(a=="—")-(b=="—")||(a<b?-1:a>b):vcmp);
  // epics start folded — the list of stories is the answer; a search or a neighbourhood opens them
  // …so does "no tag", and so does the board below `triage` — what is kept and what is owed stay open; `triaged` keeps its pass paragraph
  for(const k of keys)if((gname=="epic"||gname=="board"&&order.indexOf(k)>1)&&!q&&!touched.has(gname+k))shut.add(gname+k);
  $("b").innerHTML=keys.map(k=>{
    const g=groups.get(k);
    const kids=gname=="epic"&&byId.has(k)?T.filter(t=>t[13]==k):[],open=kids.filter(t=>OPEN.has(t[2])),folded=shut.has(gname+k)&&!q;
    const story=kids.length?` · ${kids.length} ${l(kids.length==1?"story.chapter":"story.chapters")}: ${kids.length-open.length} ${l("story.done")} · <span class="${open.some(t=>t[1]<"P2")?"hot":""}">${open.length} ${l("story.open")}</span>${open.some(t=>t[17])?` · ${l("word.triaged")} ${open.filter(t=>t[17]).length}/${open.length}`:""}`:"";
    const state=gname=="epic"&&byId.has(k)&&byId.get(k)[14]?`<tr class="s"><td colspan="__COLSPAN__">${esc(byId.get(k)[14])}</tr>`:gname=="board"&&k=="triaged"&&HOME.last?`<tr class="s"><td colspan="__COLSPAN__">${ids(HOME.last)}</tr>`:"";
    g.sort((x,y)=>(y[0]==k)-(x[0]==k));
    const head=`<tr class="g" data-k="${esc(gname+k)}"><td colspan="__COLSPAN__" class="m">${folded?"▸":"▾"} <b>${k=="—"?l("group.none",vn(gname)):gname=="board"?l("section."+k):esc(k)}</b>${gname=="epic"&&byId.has(k)?" "+esc(byId.get(k)[6]):""}${story||" · "+g.length}${gname=="board"?" · "+BOARD[k]:BCOLS.filter(c=>c.toLowerCase()!=gname).map(c=>[...new Set(g.map(t=>xv(t,c)).filter(v=>v!="—"))].sort(vcmp)).filter(v=>v.length).map(v=>" · "+esc(v.slice(0,6).join(" / "))+(v.length>6?" …":"")).join("")}</tr>${state}`;   // a header sums its rows up by the board's columns
    return head+(folded?"":g.map(t=>`<tr class="t${gname=="epic"&&byId.has(k)&&t[0]!=k?" c":""}"><td class="m"><i class="q ${mark(t)}"></i><a href="#=${t[0]}">${t[0]}</a><td class="m ${t[1]<"P2"?"hot":""}">${t[18]?"#"+t[18]+" ":""}${t[1]}${t[21]?" → "+esc(t[21]):""}<td class="m">${esc(sl(blocked(t)?"Blocked":t[2]))}${BCOLS.map(c=>`<td class="m x">${esc((t[28]||{})[c]||xv(t,c))}`).join("")}<td><a href="${BLOB+esc(t[5])}">${esc(t[6])}</a>${t[15].map(x=>`<a href="#${encodeURIComponent(x)}" class="m k">${esc(x)}</a>`).join("")}</tr><tr class="h" hidden><td colspan="__COLSPAN__">${esc(t[7])}${blocked(t)?`<div class="m">${esc(sl(t[2]))} · ${l("word.blocked_by")} ${t[16].map(b=>byId.has(b)?`<a href="#~${b}">${b}</a>`:esc(b)).join(" ")}</div>`:""}${t[17]?`<div class="m">${l("word.triaged")} ${esc(t[17])}${t[20].length?" · "+l("word.needs")+" "+t[20].join(", "):""}</div>`:""}${chips(t[12],"→")}${chips(inb.get(t[0])||[],"←")}</tr>`).join(""))}).join("");
  const hot=rows.filter(t=>OPEN.has(t[2])&&t[1]<"P2").length,go=rows.filter(t=>t[2]=="In Progress").length,stuck=rows.filter(blocked).length;
  $("n").textContent=`${rows.length} ${hood?L["count.around"].replace("{0}",hood[0]):exact?L["count.id"].replace("{0}",exact[0]):every?L["count.trackers"]:L["count.open"]} · ${hot} P0/P1 · ${go} ${L["count.in_progress"]}${stuck?` · ${stuck} ${L["count.blocked"]}`:""}${rows.some(t=>t[17])?` · ${rows.filter(untriaged).length} ${L["count.untriaged"]}`:""}`;
  $("o").hidden=$("a").hidden=gname=="board";   // the board shows everything — open/all has nothing to say there
  $("g").textContent=L["view.by"].replace("{0}",vn(gname));$("p").innerHTML=gname=="board"&&!q?(all_=>{
    // ONLY what passes the ask rules is a question here — t[29][7] is why it is not. The Owner never reads a malformed
    // ask as one; what was sent back is listed after the queue, with its reason, for the seat that wrote it.
    const w=all_.filter(t=>!t[29][7].length),sent=all_.filter(t=>t[29][7].length);
    // the answer first: what needs the Owner — how many, how old, what it holds up — then each ask as the question it is
    const days=t=>t[29][2]?Math.floor((Date.now()-Date.parse(t[29][2]))/864e5):null,old=Math.max(-1,...w.map(t=>days(t)??-1)),held=[...new Set(w.flatMap(t=>t[29][3]))];
    w.sort((a,b)=>(days(b)??-1)-(days(a)??-1));
    // an answer is the Owner's own commit: the button copies the three lines and opens the file on the forge under his login —
    // no server, no token, and the seat that asked is nowhere in the path. The commit's author is the proof.
    // Two buttons — accept · reject — open a dialog that shows the whole ask with its context, so the Owner can look and
    // abort. OK yields ONE command: `--answer <id> accept|reject "text"` — the tool cuts the answer branch, writes the
    // three lines, commits SIGNED and pushes. A browser cannot sign; the dialog decides, the terminal signs.
    const act=(t,kind)=>{const d=$("dlg"),id=t[0],[ask,k,since,held,,prop,opts]=t[29],cmd="__CMD__";
      const meta=[k?l("ask."+k):"",days(t)!=null?l("waiting.days",days(t)):"",held.length?l("waiting.holds.ids",held.join(", ")):""].filter(Boolean).join(" · ");
      // an ask offers choices: one radio per option in the order given, except the RECOMMENDED one (`ask-proposal:`)
      // which is offered first. A proposal alone is a list of one. Last always comes Other, with the box — and when
      // there is nothing to choose from, Other is the only row and the box is the answer.
      const all=opts&&opts.length?opts:(prop?[prop]:[]),ordered=prop&&all.includes(prop)?[prop,...all.filter(o=>o!=prop)]:all;
      const rows=ordered.map((o,i)=>`<label class="dl"><input type="radio" name="how" value="${i}" required> <span>${esc(o)}`
          +(o==prop?` <span class="ddim">— ${l("answer.recommended")}</span>`:"")+`</span></label>`).join("")
        +`<label class="dl"><input type="radio" name="how" value="other" required${ordered.length?"":" checked"}> <span>${l("answer.other")}</span></label>`;
      d.innerHTML=`<form method="dialog"><h3>${kind=="accept"?l("answer.accept"):l("answer.reject")} · <a href="#=${id}">${id}</a>${meta?` · <span class="m">${meta}</span>`:""}</h3>
        <p class="dq">${esc(ask)}</p>${prop?`<p class="dp"><b>${l("answer.proposal")}</b> ${esc(prop)}</p>`:""}<p class="m ddim">${esc(t[6])}</p>
        ${kind=="accept"?`${rows}<textarea name="text" rows="3" placeholder="${l("answer.change.hint")}"${ordered.length?" disabled":" required"}></textarea>`
        :`<textarea name="text" rows="3" placeholder="${l("answer.reject.hint")}" required></textarea>`}
        <menu><button value="ok" class="go">${l("answer.ok")}</button><button value="abort" formnovalidate>${l("answer.abort")}</button></menu></form>`;
      const f=d.querySelector("form"),ta=f.text;
      f.querySelectorAll("[name=how]").forEach(r=>r.onchange=()=>{ta.disabled=r.value!="other";ta.required=r.value=="other";if(!ta.disabled)ta.focus()});
      f.onsubmit=e=>{if(e.submitter?.value!="ok")return;e.preventDefault();const q=s=>String(s).trim().replace(/"/g,"'");
        // the chosen option goes into the command VERBATIM — what the Owner picked is what the tracker records
        const pick=f.how?.value,txt=q(ta.value||""),chosen=kind=="reject"||pick=="other"||pick==null?txt:q(ordered[+pick]);
        const line=`${cmd} --answer ${id} ${kind}${chosen?` "${chosen}"`:""}`;
        sign(d,id,line,(kind=="accept"?"accepted":"rejected")+(chosen?" - "+chosen.replace(/\s+/g," "):""))};
      d.showModal()};
    // THE SECOND SCREEN (FM-013). OK used to disable itself and leave one button — abort — which read as taking the
    // decision back. The decision is made; the terminal signs it. This screen says what to run, where, what it does step
    // by step, what the end looks like, how to check it and where to go when signing fails — and has ONE way out, Done
    // (Esc too: it is the dialog's own). It says *Copied* only when the clipboard said so: from a file there may be none.
    const sign=(d,id,line,said)=>{const br=`answer/${id.toLowerCase()}`,c=s=>`<code>${esc(s)}</code>`;
      d.innerHTML=`<form method="dialog" class="sign"><h3>${l("answer.sign.title")} · <a href="#=${id}">${id}</a></h3>
        <p class="dp">${l("answer.sign.intro")}</p><pre class="cmd">${esc(line)}</pre>
        <p class="m ddim"><button type="button" class="copy">${l("answer.sign.copy")}</button><span class="said" aria-live="polite"></span></p>
        <h4>${l("answer.sign.where")}</h4><p>${BRANCH?lh("answer.sign.where.branch",c(BRANCH)):l("answer.sign.where.text")}</p>
        <h4>${l("answer.sign.does")}</h4><ol><li>${lh("answer.sign.step.cut",c(br))}</li><li>${lh("answer.sign.step.write",c("answer:"),c("answered:"),c("answered-by:"))}</li>
        <li>${l("answer.sign.step.commit")}</li><li>${l("answer.sign.step.push")}</li></ol><p class="ddim">${l("answer.sign.slow")}</p>
        <h4>${l("answer.sign.success")}</h4><pre>${esc(`${id} answered: ${said}\n  signed, on \`${br}\`, pushed`)}</pre>
        <h4>${l("answer.sign.check")}</h4><p>${lh("answer.sign.check.text",c(`git log -1 --format=%G? ${br}`),c("G"))}</p>
        <h4>${l("answer.sign.fail")}</h4><p>${lh("answer.sign.fail.text",`<a href="${l("answer.sign.url")}" target="_blank" rel="noopener">${l("answer.sign.page")}</a>`)}</p>
        <menu><button value="done" class="go">${l("answer.done")}</button></menu></form>`;
      const out=d.querySelector(".said"),copy=()=>(navigator.clipboard?.writeText?navigator.clipboard.writeText(line):Promise.reject())
        .then(()=>out.textContent=L["answer.sign.copied"],()=>out.textContent=L["answer.sign.nocopy"]);
      d.querySelector(".copy").onclick=copy;copy();d.querySelector(".go").focus()};
    window.ACT=act;
    return `<b class="${w.length?"hot":""}">${l("waiting.title")}: ${w.length}</b>`+(w.length?(old>=0?" · "+l("waiting.oldest",old):"")+(held.length?" · "+l("waiting.holds",held.length):"")+(w.length>__BOTTLE__?" · "+l("waiting.bottleneck",w.length,held.length):"")+"\n"+w.slice(0,14).map(t=>
      `<a href="#=${t[0]}">${t[0]}</a> `+(t[29][0]?esc(t[29][0]):`<i>${l("waiting.unasked")}</i> — ${esc(t[6])}`)+`<span class="m"> ·`+(t[29][1]?" "+l("ask."+t[29][1])+" ·":"")+(days(t)!=null?" "+l("waiting.days",days(t))+" ·":"")+(t[29][3].length?" "+l("waiting.holds.ids",t[29][3].join(", ")):"")+`</span>`+(t[29][0]?` <button class="act" onclick="ACT(T.find(x=>x[0]=='${t[0]}'),'accept')">${l("answer.accept")}</button><button class="act" onclick="ACT(T.find(x=>x[0]=='${t[0]}'),'reject')">${l("answer.reject")}</button>`:"")).join("\n").replace(/ ·<\/span>/g,"</span>")+(w.length>14?"\n…":""):"")
      +(sent.length?"\n\n<b>"+l("waiting.malformed",sent.length)+"</b>\n"+sent.map(t=>
        `<a href="#=${t[0]}">${t[0]}</a> `+(t[29][0]?esc(t[29][0]):`<i>${l("waiting.unasked")}</i>`)+`<span class="m"> — ${esc(t[29][7][0])}</span>`).join("\n"):"")})(T.filter(t=>OPEN.has(t[2])&&t[21]=="owner"&&!t[29][4]))
    +(HOME.path?"\n\n<b>"+l("path.title")+"</b> — __HOME_PATH__\n"+ids(HOME.path):"")
    // the registry (FM-024): which sessions are open, for what — and how independent this week's verdicts were
    +(REG?"\n\n<b>"+l("sessions.open",REG.open.length)+"</b>"+(REG.open.length?" — "+REG.open.map(r=>`${esc(r[0])} ${esc(r[1])} (${esc(r[2])})${r[4]?" · "+l("sessions.abandoned"):""}`).join(" · "):"")
      +(REG.reviews?"\n"+l("reviews.week",REG.reviews[0],REG.reviews[1])+(REG.reviews[2]?" · "+l("reviews.untraced",REG.reviews[2]):"")+(REG.reviews[3]?" · "+l("reviews.trunk",REG.reviews[3]):""):""):""):"";
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
// the viewer: `#=MSR-012` shows that tracker rendered. Markdown comes from view/<ID>.js (a script tag works from
// disk, a fetch does not); embedded HTML is shown, never run; bare ids and tracker links stay inside the page.
const MD=new Map(),TID=/(?:__KINDS__)-\d+\b/;
marked.use({renderer:{html:k=>esc(k.raw||k.text||"")},extensions:[{name:"tid",level:"inline",start:s=>s.match(new RegExp("\\b"+TID.source))?.index,
  tokenizer(s){if(this.lexer.state.inLink)return;const m=new RegExp("^"+TID.source).exec(s);if(m&&byId.has(m[0])&&"#="+m[0]!=dec(location.hash))return{type:"tid",raw:m[0]}},
  renderer:k=>`<a href="#=${k.raw}">${k.raw}</a>`}]});
V=(id,md)=>{MD.set(id,md);if(dec(location.hash)=="#="+id)view(id)};
function view(id){
  const v=$("v"),t=byId.get(id);$("B").hidden=true;v.hidden=false;scrollTo(0,0);
  if(!MD.has(id)){const s=document.createElement("script");s.src="view/"+id+".js";
    s.onerror=()=>v.innerHTML=`<p class="m"><a href="#">${l("viewer.board")}</a> · ${l("viewer.no_copy",id,"__CMD__ --html-only")}</p>`;
    v.innerHTML=`<p class="m">${id} …</p>`;return document.head.append(s)}
  const facts=[sl(blocked(t)?"Blocked":t[2]),t[1]!="—"&&t[1],t[18]&&"#"+t[18],L["section."+board(t).at(-1)]||board(t).at(-1),t[25]&&L["word.reads"]+" "+(t[25]/1000).toFixed(1)+"k",t[17]&&L["word.triaged"]+" "+t[17],...COLS.map(c=>xv(t,c)!="—"&&c.toLowerCase()+" "+((t[28]||{})[c]||xv(t,c))),...t[15]];
  v.innerHTML=`<p class="m"><a href="#">${l("viewer.board")}</a> · <a href="#~${id}">${l("viewer.neighbours")}</a> · <a href="${esc(t[5])}">${l("viewer.file")}</a>${BLOB?` · <a href="${BLOB+esc(t[5])}">${l("viewer.forge")}</a>`:""}</p>
<p class="m f"><i class="q ${mark(t)}"></i>${facts.filter(Boolean).map(esc).join(" · ")}${t[13]!="—"?` · ${l("word.story")} <a href="#=${esc(t[13])}">${esc(t[13])}</a>`:""}</p>
${t[29][4]?`<p class="m hd"><b>${l("viewer.answer")}</b> — ${esc(t[29][4])}${[t[29][8],t[29][9]].filter(Boolean).map(x=>" · "+esc(x)).join("")}${t[29][10]?" · "+l("viewer.supersedes",esc(t[29][10])):""}</p>`:""}
${OPEN.has(t[2])||t[22]||t[24].length?`<p class="m hd"><b>${l("viewer.intent")}</b> — ${t[22]?esc(t[22])+(t[23]?` <a href="#=${esc(t[23])}">(${l("viewer.from",t[23])})</a>`:""):"<i>"+l("viewer.intent.missing")+"</i>"}<br>
<b>${l("viewer.verdict")}</b> — ${t[24].length?`<code>${esc(t[24][1])}</code> · ${esc(t[24][0])}${t[2]=="In Progress"&&Date.now()-Date.parse(t[24][0])>=(__DAYS__+1)*864e5?" · <i>"+l("viewer.stale","__DAYS__")+"</i>":""}${t[24][2]?" · "+esc(t[24][2]):""}`:"<i>"+l("viewer.verdict.none")+"</i>"}<br>
<b>${l("viewer.handover")}</b> — ${l("viewer.next")}: ${t[21]?esc(t[21]):"<i>"+l("word.missing")+"</i>"}${t[21]?" · "+l("viewer.kind")+": "+(t[26][0]?esc(t[26][0])+(t[26][1]?"":" <i>("+l("viewer.from_move")+")</i>"):"<i>"+l("word.missing")+"</i>"):""} · ${l("viewer.true_now")}: ${t[20].includes("stated")?"<i>"+l("word.missing")+"</i>":l("word.stated")}${(c=>c.length?`<br>
<b>${l("story.chapters")}</b> — ${c.length}: ${Object.entries(c.filter(x=>x[2]=="In Progress"||x[2]=="Proposed").reduce((m,x)=>(m[x[21]||"no move named"]=[...(m[x[21]||"no move named"]||[]),x[0]],m),{})).map(([k,v])=>k=="no move named"?`${v.length} ${l("viewer.no_move")}`:`${esc(k)} ${v.map(i=>`<a href="#=${i}">${i}</a>`).join(" ")}`).join(" · ")||l("viewer.none_in_progress")} · ${c.filter(x=>x[2]=="Parked").length} ${l("story.parked")} · ${c.filter(x=>!OPEN.has(x[2])).length} ${l("story.done")}`:"")(T.filter(x=>x[13]==t[0]))}${t[20].filter(n=>n!="stated"&&n!="intended").length?" · "+l("word.needs")+" "+t[20].filter(n=>n!="stated"&&n!="intended").join(", "):""}</p>`:""}${chips(t[16].filter(b=>byId.has(b)),l("word.blocked_by"),"=")}${chips(t[12],"→","=")}${chips(inb.get(id)||[],"←","=")}<div class="md">${marked.parse(MD.get(id))}</div>`;
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
for(const e of document.querySelectorAll("[data-l]"))e.textContent=L[e.dataset.l]||"";$("q").placeholder=L["search"];$("q").title=L["search.help"];
// light or dark is the viewer's choice: auto follows the system; the other two switch every theme's
// `prefers-color-scheme` rule on or off — so a brand needs to know nothing about the button. Paper stays light.
const ORIG=new Map(),SCHEMES=["auto","light","dark"],PCS=/\(\s*prefers-color-scheme\s*:\s*(dark|light)\s*\)/g;
let scheme="auto";try{scheme=localStorage.getItem("shoalmark.scheme")||"auto"}catch(e){}if(!SCHEMES.includes(scheme))scheme="auto";
const rules=(s,f)=>{try{for(const r of s.cssRules){if(r.styleSheet)rules(r.styleSheet,f);else if(r.media)f(r)}}catch(e){}},
paint=m=>{for(const s of document.styleSheets)rules(s,r=>{if(!ORIG.has(r)){if(!r.media.mediaText.includes("prefers-color-scheme"))return;ORIG.set(r,r.media.mediaText)}
    r.media.mediaText=m=="auto"?ORIG.get(r):ORIG.get(r).replace(PCS,(x,w)=>w==m?"(min-width:0px)":"(max-width:0px)")});
  document.documentElement.style.colorScheme=m=="auto"?"":m},
setScheme=m=>{scheme=m;paint(m);$("s").textContent="◐ "+L["scheme."+m];$("s").dataset.scheme=m;try{localStorage.setItem("shoalmark.scheme",m)}catch(e){}};
$("s").onclick=()=>setScheme(SCHEMES[(SCHEMES.indexOf(scheme)+1)%3]);setScheme(scheme);addEventListener("load",()=>paint(scheme));
onbeforeprint=()=>paint("light");onafterprint=()=>paint(scheme);
(onhashchange=()=>{const h=dec(location.hash.slice(1));if(h[0]=="="&&byId.has(h.slice(1)))return view(h.slice(1));
  $("v").hidden=true;$("B").hidden=false;$("q").value=h;draw();scrollTo(0,0)})();
</script></html>
"""


# Every word of the board's chrome, in English. A `labels.yaml` — flat `key: value` lines — overrides any of them;
# the words the page's LOGIC compares (a status, a section, a move) stay what an agent types: these are what is SHOWN.
LABELS = {
    "tagline": "", "footer": "",
    "search": "search · ~ID",       # fits the box at its CSS minimum, 200 px, whatever the window: the whole help is its title
    "search.help": "A whole id shows that tracker. What links to it: ~ID (Markdown links only). A story's chapters: the story view. Anything else matches by substring — tier, status, words, blocked, untriaged.",
    "view.by": "by {0}", "view.board": "board", "view.epic": "story", "view.open": "open", "view.all": "all",
    "scheme.auto": "auto", "scheme.light": "light", "scheme.dark": "dark",
    "col.id": "id", "col.tier": "tier", "col.status": "status", "col.title": "title",
    "status.Proposed": "Proposed", "status.In Progress": "In Progress", "status.Parked": "Parked", "status.Reserved": "Reserved",
    "status.Shipped": "Shipped", "status.Closed": "Closed", "status.Blocked": "Blocked",
    "section.progress": "progress", "section.triage": "triage", "section.triaged": "triaged", "section.backlog": "backlog", "section.done": "done",
    "desc.progress": "kept by triage — by rank, then tier",
    "desc.progress.none": "empty until a first triage pass has run — --triage",
    "desc.triage": "what the next --triage lists — in progress and unjudged or judged over {0} days ago, and new filings",
    "desc.triaged": "judged {0} — each also sits in its own section", "desc.triaged.none": "no triage pass has run yet",
    "desc.backlog": "waiting — P0 to P3, then untiered, then parked", "desc.done": "shipped or closed",
    "group.none": "no {0}",
    "count.trackers": "trackers", "count.open": "open", "count.around": "around {0}", "count.id": "tracker · {0}", "count.in_progress": "in progress",
    "count.blocked": "blocked", "count.untriaged": "untriaged",
    "path.title": "the current path", "waiting.title": "waiting for you", "waiting.detail": "open work whose next move is the Owner's",
    "waiting.oldest": "oldest {0} days", "waiting.holds": "holding up {0} more", "waiting.days": "{0} days", "waiting.holds.ids": "holds up {0}",
    "waiting.unasked": "not yet stated as a question",
    "waiting.bottleneck": "you are the bottleneck — {0} asks, {1} trackers held up",
    "waiting.malformed": "{0} asks sent back — not for you",
    "sessions.open": "sessions · {0} open", "sessions.abandoned": "abandoned",
    "reviews.week": "reviews this week · independent {0} · same session {1}", "reviews.untraced": "untraced {0}", "reviews.trunk": "on trunk {0}",
    "answer.accept": "accept", "answer.reject": "reject", "answer.proposal": "the seat proposes:", "answer.other": "Other:", "answer.recommended": "recommended",
    "answer.change.hint": "your change, in one line — more goes in the tracker's body", "answer.reject.hint": "why, and how the ask should be reworded (required)",
    "answer.ok": "OK — give me the command", "answer.abort": "abort",
    # the second screen (FM-013) — `{0}` in these is markup the page builds: a branch or a key as code, the signing link
    "answer.sign.title": "Sign your answer",
    "answer.sign.intro": "Your decision is made. A browser cannot sign it — your terminal does, with your key. Run this command:",
    "answer.sign.copy": "Copy again", "answer.sign.copied": "Copied.",
    "answer.sign.nocopy": "Not copied — this page has no clipboard here (a board opened from a file often has none). Select the command and copy it.",
    "answer.sign.where": "Where", "answer.sign.where.text": "In a terminal, in this repository, on the branch that carries the ask.",
    "answer.sign.where.branch": "In a terminal, in this repository, on the branch that carries the ask — {0}, the branch this board was built from.",
    "answer.sign.does": "What it does", "answer.sign.step.cut": "cuts {0} from the branch you are on",
    "answer.sign.step.write": "writes the three lines — {0} {1} {2}", "answer.sign.step.commit": "commits them, signed with your key — a hardware key waits for your touch",
    "answer.sign.step.push": "pushes the branch",
    "answer.sign.slow": "It prints each step as it starts, and it may take a while: the checkout and the commit each run the gate over every tracker.",
    "answer.sign.success": "When it worked", "answer.sign.check": "To check",
    "answer.sign.check.text": "{0} prints {1} — a good signature, under a key this repository trusts.",
    "answer.sign.fail": "If it fails", "answer.sign.fail.text": "No signing key is set, or the signature does not verify: set up your key once — {0}.",
    "answer.sign.page": "the signing page", "answer.sign.url": SIGNING_PAGE,
    "answer.done": "Done",
    "ask.ruling": "a ruling", "ask.action": "your hands", "ask.determination": "evidence could settle it", "ask.ceremony": "a button",
    "story.chapter": "chapter", "story.chapters": "chapters", "story.done": "done", "story.open": "open", "story.parked": "parked",
    "word.triaged": "triaged", "word.needs": "needs", "word.blocked_by": "blocked by", "word.reads": "reads", "word.story": "story",
    "word.missing": "missing", "word.stated": "stated",
    "viewer.board": "← board", "viewer.neighbours": "neighbours", "viewer.file": "file", "viewer.forge": "forge",
    "viewer.no_copy": "no rendered copy of {0} — run {1}",
    "viewer.intent": "intent", "viewer.from": "from {0}", "viewer.intent.missing": "missing — the Owner states it on the tracker or its story",
    "viewer.verdict": "verdict", "viewer.verdict.none": "none yet — no triage pass has judged it",
    "viewer.answer": "the Owner's answer", "viewer.supersedes": "supersedes {0}",
    "viewer.stale": "stale — older than {0} days, it counts as untriaged again",
    "viewer.handover": "hand-over", "viewer.next": "next", "viewer.kind": "kind", "viewer.from_move": "from the move",
    "viewer.true_now": "what is true now", "viewer.no_move": "with no move named", "viewer.none_in_progress": "none in progress",
}
BRAND_FILES = ("theme.css", "logo.svg", "logo.png", "labels.yaml")
LOGO_MAX = 200_000            # bytes — a logo is inlined into the page; past this it is skipped, with a warning


def brand_places():
    """Where a brand may live, farthest from the viewer first — the LATER place wins. Only the git-ignored board reads
    these: INDEX.md, the gate and the deriver are functions of the repository alone, or two people's commits would
    fight over a generated file."""
    try:
        home = pathlib.Path(os.environ.get("XDG_CONFIG_HOME") or pathlib.Path.home() / ".config") / "shoalmark"
    except (RuntimeError, KeyError):                        # no HOME — a hook, CI, an agent: the person simply has no place
        home = None
    return [(who, d) for who, d in (("organisation", HERE / "brand"), ("repository", TRACKER_DIR / "brand"), ("person", home)) if d and d.is_dir()]


def read_flat(text):
    """`key: value` lines, `#` comments, optional quotes — the form a tracker's front matter already has. No nesting."""
    out = {}
    for line in text.splitlines():
        line = line.strip()
        if line and not line.startswith("#") and ":" in line:
            k, _, v = line.partition(":")
            v = v.strip()
            out[k.strip()] = v[1:-1] if len(v) > 1 and v[0] == v[-1] and v[0] in "\"'" else v
    return out


def contrast(a, b):
    """WCAG contrast of two `#rrggbb` colours, 1–21."""
    def lum(h):
        c = [int(h[i:i + 2], 16) / 255 for i in (1, 3, 5)]
        r, g, bl = (x / 12.92 if x <= 0.03928 else ((x + 0.055) / 1.055) ** 2.4 for x in c)
        return 0.2126 * r + 0.7152 * g + 0.0722 * bl
    hi, lo = sorted((lum(a), lum(b)), reverse=True)
    return (hi + 0.05) / (lo + 0.05)


def brand():
    """The board's brand, assembled: (themes [(who, css)], logo (who, data-uri) or None, labels, sources, warnings)."""
    themes, logo, labels, src, warn = [], None, dict(LABELS), {"theme.css": [], "logo": [], "labels.yaml": []}, []
    for who, d in brand_places():
        f = d / "theme.css"
        if f.is_file():
            css = f.read_text(encoding="utf-8")
            # A path in a theme is written relative to THE FILE IT IS IN — what an editor resolves, what a person expects.
            # The page inlines the css, so each is re-based onto the page's directory; that also makes an import or a
            # font work from the organisation's and the person's place, not only from beside the trackers.
            # A theme that maps colours onto an imported file's variables is ALL-OR-NOTHING: with the import missing — a
            # submodule not checked out — every mapped colour is invalid, not the previous place's; so it is left out.
            local = lambda u: not re.match(r"[a-z][a-z0-9+.-]*:|/|#", u, re.I)
            refs = re.findall(r"""@import\s+(?:url\(\s*)?["']?([^"')\s;]+)""", css)
            gone = [u for u in refs if local(u) and not (d / u).exists()]
            css = re.sub(r"""(url\(\s*["']?|@import\s+["'])([^"')\s;]+)""",
                         lambda m: m.group(1) + (os.path.relpath(os.path.normpath(d / m.group(2)), TRACKER_DIR).replace(os.sep, "/") if local(m.group(2)) else m.group(2)), css)
            if gone:
                warn.append(f"{who}'s theme.css imports {gone[0]}, which is not there — that theme is left out, the board keeps the colours it had")
            else:
                themes.append((who, css)); src["theme.css"].append(who)
            bg, ink = re.findall(r"--bg\s*:\s*(#[0-9a-fA-F]{6})\b", css), re.findall(r"--ink\s*:\s*(#[0-9a-fA-F]{6})\b", css)
            for b, i in zip(bg, ink):                       # the light pair, then the dark one, as a theme writes them
                if contrast(b, i) < 4.5:
                    warn.append(f"{who}'s theme.css: text {i} on ground {b} has a contrast of {contrast(b, i):.1f}:1 — below 4.5:1, hard to read")
        for name, mime in (("logo.svg", "image/svg+xml"), ("logo.png", "image/png")):
            f = d / name
            if f.is_file():
                if f.stat().st_size > LOGO_MAX:
                    warn.append(f"{who}'s {name} is {f.stat().st_size // 1000} kB — over {LOGO_MAX // 1000} kB, not shown")
                else:
                    logo = (who, "data:%s;base64,%s" % (mime, base64.b64encode(f.read_bytes()).decode("ascii"))); src["logo"].append(who)
                break
        f = d / "labels.yaml"
        if f.is_file():
            given = read_flat(f.read_text(encoding="utf-8"))
            unknown = sorted(k for k in given if k not in LABELS)
            if unknown:
                warn.append(f"{who}'s labels.yaml: {', '.join(unknown[:6])} {'are' if len(unknown) > 1 else 'is'} not a label — `--brand` lists them")
            labels.update({k: v for k, v in given.items() if k in LABELS}); src["labels.yaml"].append(who)
    loose = [n for n in BRAND_FILES if (TRACKER_DIR / n).is_file() or (TRACKER_DIR / n).is_symlink()]
    if loose:
        warn.append(f"{', '.join(loose)} beside the trackers {'are' if len(loose) > 1 else 'is'} not read — a repository's brand lives in "
                    f"{(TRACKER_DIR / 'brand').relative_to(ROOT).as_posix()}/ (since 0.9.0); move {'them' if len(loose) > 1 else 'it'} there")
    return themes, logo, labels, src, warn


def brand_report(dest=None):
    """`--brand`: why does my board look like this? `--brand DIR`: a commented starter to edit."""
    if dest:
        dest = pathlib.Path(dest); dest.mkdir(parents=True, exist_ok=True)
        for name, text in (("theme.css", THEME_STARTER), ("labels.yaml", "# every word of the board's chrome — change a value, delete the lines you keep\n"
                                                           + "".join(f"{k}: {json.dumps(v, ensure_ascii=False)}\n" for k, v in LABELS.items()))):
            if not (dest / name).exists():
                put(dest / name, text); print(f"wrote {dest / name}")
        print("a logo is logo.svg or logo.png beside them; the name is `name` in " + CONFIG_NAME)
        return EXIT_OK
    themes, logo, labels, src, warn = brand()
    print("the board is built from these places, the later one winning:")
    for who, d in brand_places():
        print(f"  {who:<13} {d}")
    print(f"  name          {CONFIG['name'] or ROOT.name}  ({CONFIG_NAME})")
    for kind in ("theme.css", "logo", "labels.yaml"):
        print(f"  {kind:<13} {' → '.join(src[kind]) or 'built in'}")
    changed = sorted(k for k in LABELS if labels[k] != LABELS[k])
    print(f"  labels changed: {len(changed)} of {len(LABELS)}")
    for w in warn:
        print(f"  warning: {w}", file=sys.stderr)
    return EXIT_OK


THEME_STARTER = """/* The board's colours and fonts. Every place's theme.css is its own stylesheet, applied in order — the tool's, the
   organisation's, the repository's, the person's — so a file with ONE variable changes one colour.
   The four status colours keep their MEANING whatever their shade: blue in progress · teal shipped · yellow parked ·
   coral blocked, and P0/P1. */
:root{
  --bg:#f7f7f5;      /* the ground */
  --ink:#161616;     /* text */
  --dim:#565656;     /* secondary text */
  --mute:#6e6e6e;    /* labels, legends */
  --line:rgba(0,0,0,.14);
  --teal:#1a7f5a; --coral:#b3402f; --blue:#2f62d6; --yellow:#946c0f;
}
@media(prefers-color-scheme:dark){:root{
  --bg:#0e0e0e; --ink:#efefef; --dim:#ababab; --mute:#8f8f8f; --line:rgba(255,255,255,.15);
  --teal:#4fd1a1; --coral:#ff7b66; --blue:#6f9bff; --yellow:#e8cf5a;
}}
/* fonts: name one that is installed, or put a font file beside the trackers and load it:
   @font-face{font-family:"Mine";src:url("mine.woff2")}  body{font-family:"Mine",system-ui,sans-serif} */
"""


def triage_home():
    """TRIAGE.md as the command and the dashboard read it: the Owner's current path, and the newest pass."""
    home = TRACKER_DIR / "TRIAGE.md"
    text = home.read_text(encoding="utf-8") if home.exists() else ""
    # a section is found by the repository's own name for it, or by the English one
    part = lambda k: (re.search(rf"^## (?:{re.escape(HEAD[k])}|{re.escape(DEFAULTS['headings'][k])})[ \t]*\n(.*?)(?=^## |\Z)", text, re.S | re.M) or ["", ""])[1].strip()
    # a pass is a paragraph that carries its date — the template's own notes do not, in any language
    passes = [p for p in re.split(r"\n\s*\n", part("passes")) if re.search(r"\d{4}-\d\d-\d\d", p) and not p.lstrip().startswith(("Newest first", "*None"))]
    # an unfilled home is not a path and not an intent: what is left once the italic notes and the bare list
    # markers are gone has to say something, or INDEX.md and the board would print the template as if it were one
    said = lambda text: text if re.search(r"\w{3,}", re.sub(r"\*\*[^*]*\*\*|\*[^*]*\*", "", text)) else ""
    return {"path": said(part("path")), "last": passes[0] if passes else "", "intent": owners_intent(part("intent"))}


def owners_intent(text):
    """The intent as the Owner WROTE it: everything under the heading, less the scaffold's own words — its note, its
    lead-in, its examples and its bare lines, recognised by their exact text (whitespace aside), never by italics, bold
    or length. An example with one word changed is his; so is a line in italics, a line in bold, a line of two letters
    (FM-022, R11). A paragraph is compared whole, so the wrapped lead-in is one piece; a line is compared alone."""
    scaffold = {" ".join(s.split()) for s in INTENT_SCAFFOLD}
    kept = []
    for para in re.split(r"\n[ \t]*\n", text):
        if " ".join(para.split()) in scaffold:
            continue
        lines = [line for line in para.splitlines() if " ".join(line.split()) not in scaffold]
        if any(line.strip() for line in lines):
            kept.append("\n".join(lines))
    return "\n\n".join(kept).strip()


def write_views(trackers):
    """One `view/<ID>.js` per tracker — `V(id, markdown)`. Rewritten only when changed; strays removed."""
    VIEW_DIR.mkdir(exist_ok=True)
    keep = set()
    for t in trackers:
        _fm, body = parse_frontmatter((TRACKER_DIR / t["file"]).read_text(encoding="utf-8"))
        out, text = VIEW_DIR / f'{t["id"]}.js', f'V({json.dumps(t["id"])},{json.dumps(body, ensure_ascii=False)})\n'
        keep.add(out.name)
        if not out.exists() or out.read_text(encoding="utf-8") != text:
            put(out, text)
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


def built_on():
    """The branch this board is built from — the answer dialog's second screen names it as the place to run `--answer`:
    the board shows the asks of the trackers on this branch, so this is the branch that carries them. git only; empty on
    a detached HEAD, under Subversion, or with no version control, and the screen then says it without a name."""
    if vcs() != "git":
        return ""
    out = subprocess.run(["git", "branch", "--show-current"], cwd=ROOT, capture_output=True, text=True, encoding="utf-8", errors="replace", env=nested_git_env())
    return out.stdout.strip() if out.returncode == 0 else ""


def html_escape(text):
    return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def render_html(trackers):
    """one static page: data rows + ~25 lines of vanilla JS. No dates and no
    counts are baked in (both are computed in the browser), so equal trackers give
    equal bytes. The row layout is documented once, in the page's script."""

    epics = {t.get("epic", "—") for t in trackers}
    by_id, verdicts, by_ask = {t["id"]: t for t in trackers}, latest_verdicts(), asks_by_key(trackers)
    rows = [
        json.dumps(
            [t["id"], t["tier"], t["status"], "—", "—",
             t["file"], t["title"], t["hook_full"], t["num"], "—", "—",
             "—", sorted({"-".join(f.split("-")[:2]) for f in t["links"]} - {t["id"]}),
             t.get("epic", "—"), t.get("state", "") if t["id"] in epics else "",
             ["#" + x for x in t.get("tags", [])], t.get("blocked_by", []), t.get("triaged", ""), t.get("rank", 0), board(t),
             needs_of(t, by_id) if t["status"] in OPEN_STATUSES else [], t.get("next", ""),
             intent_of(t, by_id), "" if t.get("intent") or not intent_of(t, by_id) else t.get("epic", ""), verdicts.get(t["id"], []), t.get("reads", 0), list(kind_of(t)), t.get("x") or {}, t.get("xd") or {},
             [t.get("ask", ""), t.get("ask_kind", ""), t.get("ask_since", ""), held_up_by(t, trackers) if t.get("next") == "owner" and t["status"] in OPEN_STATUSES else [], t.get("answer", ""), t.get("ask_proposal", ""), t.get("ask_options") or [], ask_problems(t, by_ask),
              t.get("answered", ""), t.get("answered_by", ""), t.get("supersedes", "")]],
            ensure_ascii=False,
        ).replace("</", "<\\/")  # a hook containing "</script>" must not end the block
        for t in sorted(trackers, key=lambda t: (t["kind"], t["num"]))
    ]
    unwrap = lambda md: re.sub(r" {2,}", " ", re.sub(r"(?<!\n)\n(?!\s*\n|\s*\d+\. |\s*- )", " ", md))   # source line breaks are not the reader's
    plain = lambda md: strip_md(re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", unwrap(md)))
    home = {k: plain(v) for k, v in triage_home().items()}
    page = (HTML_PAGE.replace("__KINDS__", "|".join(sorted(KINDS, key=len, reverse=True))).replace("__NAME__", html_escape(CONFIG["name"] or ROOT.name))
            .replace("__COLHEADS__", "".join(f'<th class="x">{c.lower()}' for c in BOARD_COLUMNS)).replace("__COLSPAN__", str(4 + len(BOARD_COLUMNS))).replace("__BCOLS__", json.dumps(BOARD_COLUMNS, ensure_ascii=False)).replace("__COLS__", json.dumps(DERIVED_COLUMNS, ensure_ascii=False)).replace("__HOME_PATH__", str((TRACKER_DIR / "TRIAGE.md").relative_to(ROOT).as_posix())).replace("__CMD__", CMD))
    themes, logo, labels, _src, warnings = brand()
    for w in warnings:
        print(f"  brand: {w}", file=sys.stderr)
    # each place's theme is its OWN stylesheet, in order — `@import` and `@font-face` only work at the top of one
    page = page.replace("__THEMES__", "".join(f'<style data-from="{who}">' + css.replace("</", "<\\/") + "</style>" for who, css in themes))
    page = page.replace("__LOGO__", f'<img alt="" src="{logo[1]}">' if logo else "").replace("__FAVICON__", f'<link rel="icon" href="{logo[1]}">' if logo else "")
    page = page.replace("__LABELS__", json.dumps(labels, ensure_ascii=False).replace("</", "<\\/"))
    return page.replace("__MARKED__", MARKED.read_text(encoding="utf-8")).replace("__DAYS__", str(TRIAGE_DAYS)).replace("__BOTTLE__", str(BOTTLENECK)).replace("__HOME__", json.dumps(home, ensure_ascii=False).replace("</", "<\\/")).replace("__REG__", json.dumps(board_sessions(), ensure_ascii=False).replace("</", "<\\/")).replace("__BLOB__", json.dumps(REPO_BLOB)).replace("__BRANCH__", json.dumps(built_on()).replace("</", "<\\/")).replace(
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
            "will may must more most less one two three new old own up out over under after before "
            # German — trackers are written in the language of the people who read them
            "der die das den dem des ein eine einer eines einem einen und oder aber nicht kein keine ist sind war wird werden "
            "hat haben mit von für auf aus bei nach über unter vor zum zur als auch noch nur wie wenn dass sich wir sie ihr".split())


def related_trackers(trackers, query, limit=8):
    """The existing trackers closest to `query` — a tracker id, or free words.

    Scored by the rare words two trackers share in filename, hook and opening lines, damped by
    length so a 2,000-line epic does not win every search. It is a lead for a reader, not a verdict:
    its only job is to put the tracker that already owns the problem in front of whoever is about to file it again.
    """
    def bag(t):
        text = " ".join([t["file"].replace("-", " "), t["hook_full"], t["hook_full"], t.get("state", "")])
        return collections.Counter(w for w in re.findall(r"[^\W\d_]\w{2,}", text.lower()) if w not in _STOP)
    bags = {t["id"]: bag(t) for t in trackers}
    df = collections.Counter(w for b in bags.values() for w in set(b))
    n = len(trackers)
    by_id = {t["id"]: t for t in trackers}
    qid = query.strip().upper()
    q = bags[qid] if qid in bags else collections.Counter(
        w for w in re.findall(r"[^\W\d_]\w{2,}", query.lower()) if w not in _STOP)
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
                    EVERY KEEP CARRIES A TIER JUDGED TODAY: P0 harm to people who use it today, or the current path is
                    blocked now · P1 on the current path · P2 next · P3 someday. What the path does not name
                    is P0 or P1 only if people who use it are being harmed today. An inherited tier is no
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
             numbering. Harm today is ranked even where the path does not name it — after the
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
    if vcs() == "svn":
        return svn_last_worked_on(path)
    log = subprocess.run(["git", "log", "--format=%H %cs %s", "--", str(path)], cwd=ROOT,
                         capture_output=True, text=True, encoding="utf-8", errors="replace", env=nested_git_env()).stdout.splitlines()
    for line in log:
        commit, day, subject = (line.split(" ", 2) + [""])[:3]
        if "[sweep]" in subject:
            continue
        names = subprocess.run(["git", "show", "--name-only", "--format=", commit, "--", str(TRACKER_DIR.relative_to(ROOT).as_posix())],
                               cwd=ROOT, capture_output=True, text=True, encoding="utf-8", errors="replace", env=nested_git_env()).stdout.split()
        if len([n for n in names if KIND_RE.match(n.rsplit("/", 1)[-1])]) <= 8:
            return day
    return log[-1].split()[1] if log else "—"


_SVN_LOG = None


def svn_last_worked_on(path):
    """The same rule from Subversion — ONE `svn log -v --xml` over the tracker directory, read once: a log is a
    round trip to the server, and a pass asks about every tracker."""
    global _SVN_LOG
    if _SVN_LOG is None:
        import xml.etree.ElementTree as ET
        out = subprocess.run(["svn", "log", "-v", "--xml", str(TRACKER_DIR)], capture_output=True, text=True, encoding="utf-8", errors="replace")
        try:
            _SVN_LOG = [((e.findtext("date") or "")[:10], e.findtext("msg") or "", [x.text or "" for x in e.iter("path")])
                        for e in ET.fromstring(out.stdout).iter("logentry")] if out.returncode == 0 and out.stdout.strip() else []
        except ET.ParseError:
            _SVN_LOG = []
    mine = [(day, msg, names) for day, msg, names in _SVN_LOG if any(n.rsplit("/", 1)[-1] == path.name for n in names)]   # newest first
    for day, msg, names in mine:
        if "[sweep]" not in msg and len([n for n in names if KIND_RE.match(n.rsplit("/", 1)[-1])]) <= 8:
            return day
    return mine[-1][0] if mine else "—"


def repos_naming():
    """{tracker id: the submodules whose branch names or commit subjects name it} — where the work happened,
    from git alone. For the worksheet only: eight `git log`s are too slow for a commit hook. A submodule that
    is not checked out is skipped — `git -C` on its empty directory would answer from the parent."""
    modules, found = ROOT / ".gitmodules", {}
    for sub in re.findall(r"^\s*path\s*=\s*(\S+)", modules.read_text(encoding="utf-8"), re.M) if modules.exists() else []:
        if not (ROOT / sub / ".git").exists():
            continue
        said = "".join(subprocess.run(["git", "-C", str(ROOT / sub), *cmd], capture_output=True, text=True, encoding="utf-8", errors="replace",
                                      env=nested_git_env()).stdout for cmd in (["log", "--all", "--format=%s %D"], ["branch", "-r"]))
        for kind, num in re.findall(r"\b(%s)[-/](\d+)\b" % "|".join(KINDS), said, re.I):
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
    tier, other, rank = (re.search(rx, verdict) for rx in (r"\bP[0-3]\b", rf"\b{_IDS}\b", r"#(\d+)\b"))      # the repository's own id prefixes, never a fixed pair
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
            put(path, set_front(path.read_text(encoding="utf-8"), "rank", None))
            log.append(f'{t["id"]}: rank #{t["rank"]} freed — {ranks[str(t["rank"])]} holds it now')
    for tid, verdict, path, old, new, hand in plan:
        if new != old:
            put(path, new)
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
        if key in ("answer", "answered", "answered-by") and not all(t["fm"].get(k, "").strip() for k in ("answer", "answered", "answered-by")):
            out.append(f'{t["id"]}: an answer is three lines — `answer:` `answered:` `answered-by:` — and this one is missing some')
        if key == "answer" and not t["fm"].get("ask", "").strip():
            out.append(f'{t["id"]}: `answer:` with no `ask:` — an answer answers a question; write the question it answers, or drop the answer')
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


CONFIG_KEYS = {           # the configuration's keys that change what a command refuses — `--schema` prints them under the front matter
    "freeze_at": ("a whole number; `0` = off (the default)",
                  "the filing freeze (FM-032 S4): while this many trackers or more are open, `--new` files only a product defect — a filing that "
                  "carries `tags: bug`, as `--new KIND \"the title\" --tags bug` writes it; anything else goes as one line into the closest open "
                  "tracker's body, or waits. `--check` says when it holds"),
}


def render_schema():
    rows = [f"| `{k}:`{' — required' + (' on open work' if required == 'open' else '') if required else ''} | {shape_words(shape) if shape else 'free text'} | {who} | {says} |"
            for k, (shape, required, who, says) in FRONT_MATTER.items()]
    return "\n".join(["| Key | Value | Written by | Says |", "|---|---|---|---|"] + rows
                     + ["", f"`{CONFIG_NAME}`, at its top level:", "", "| Key | Value | Says |", "|---|---|---|"]
                     + [f"| `{k}` | {shape} | {says} |" for k, (shape, says) in CONFIG_KEYS.items()])


def git_user():
    """The committer's own name, as git will write it — so `answered-by:` need not be typed. Read ONCE per run and
    kept (`configure` forgets it): the answer is the only place it is needed, and a run does not change who is typing."""
    global _GIT_USER
    if _GIT_USER is None:
        out = subprocess.run(["git", "config", "user.name"], cwd=ROOT, capture_output=True, text=True, encoding="utf-8", errors="replace", env=nested_git_env())
        _GIT_USER = out.stdout.strip() if out.returncode == 0 else ""
    return _GIT_USER


def svn_blame(rel):
    """{line number: (author, revision)} for one file, from the server's own record — read once per file and kept:
    the gate asks about several lines of the same tracker, and `svn blame` is a round trip to the repository."""
    if rel in _SVN_BLAME:
        return _SVN_BLAME[rel]
    out = {}
    blame = subprocess.run(["svn", "blame", "--xml", rel], cwd=ROOT, capture_output=True, text=True, encoding="utf-8", errors="replace")
    if blame.returncode == 0:
        import xml.etree.ElementTree as ET
        try:
            for e in ET.fromstring(blame.stdout).iter("entry"):
                who, c = e.find("commit/author"), e.find("commit")
                out[int(e.get("line-number"))] = (who.text if who is not None else None, c.get("revision") if c is not None else "")
        except (ET.ParseError, ValueError, TypeError):
            out = {}
    _SVN_BLAME[rel] = out
    return out


ERE_META = frozenset(".[]()*+?{}|^$\\")                  # what a POSIX extended regular expression reserves, and nothing else


def line_regex(needle):
    """The pattern git's `-G` is handed for a front-matter key: the needle, anchored to the line start — `next: owner`
    becomes `^next: owner`, exactly that, with nothing escaped that does not have to be.

    Not `re.escape`: it escapes every character outside `[A-Za-z0-9_]` that Python reserves, which includes the SPACE
    in `next: owner` and the hyphens in `kind-of-problem:` — and `\\ ` and `\\-` are UNDEFINED in POSIX extended regular
    expressions, which is the flavour `-G` compiles. Git carries a different regex engine on each platform (glibc,
    BSD, its own bundled one on Windows), so an undefined escape is a per-platform answer to a question the gate must
    answer the same way everywhere. Only the characters ERE actually reserves are escaped here. Which of them re.escape
    reaches for has also changed between Python releases; this table does not."""
    return "^" + "".join("\\" + c if c in ERE_META else c for c in needle)


def line_author(path, needle):
    """Who committed the line this tracker carries under `needle` — from the version control system, never from the
    file: (name, email, system, commit), or (None, None, "uncommitted", ""). Git's author is a string anyone can type,
    so `signed` makes `verified_as` ask the commit; Subversion's author is the one its server authenticated, and it
    has no email. ONE reader for both the answer line and the `next: owner` line — a second would drift from this one.

    The needle names a LINE, not a substring. A tracker's body discusses its own keys — "an `answer:` counts only from
    the account it is filed from" is a sentence FM-007 carries — and a substring test cannot tell that prose from the
    front-matter line, so it answered with the commit that wrote the prose, and read a line nobody had committed as
    committed. Both tests are anchored to the line start now: git's `-G` (below) and `startswith` here."""
    rel = pathlib.Path(path).resolve().relative_to(ROOT).as_posix()
    hit = _LINE_AUTHOR.get((rel, needle))
    if hit is not None:
        return hit
    out = (None, None, "uncommitted", "")
    if vcs() == "svn":
        by_line = svn_blame(rel)                          # ONE blame per file, however many of its lines are asked about
        lines = pathlib.Path(path).read_text(encoding="utf-8").splitlines()
        n = next((i for i, l in enumerate(lines) if l.startswith(needle)), None)
        if n is not None and (n + 1) in by_line:
            who, rev = by_line[n + 1]
            out = (who, None, "svn", rev)
    else:
        # `--full-history` or the answer is the wrong seat's. Git's default history simplification follows ONE parent of
        # a merge when the merge is TREESAME to it — and a branch that moves a line away and back (owner -> review ->
        # owner) merges to a file byte-identical to the one main already had. The whole branch is then skipped and the
        # pickaxe answers with the commit BEFORE it: the seat that last touched the line is not the seat git names.
        # Not `-m`: it splits a merge against each parent, and a line that arrived only through a branch then matches on
        # the merge itself, which would name the merger as the setter. Without it a merge carries no diff and cannot win.
        # `-G`, not `-S`: `-S` counts a substring anywhere in the patch, and the body's own prose about the key counts
        # too. `-G` runs the regex over each changed line with its `+`/`-` stripped, so `^` is the line start and only a
        # commit that changed the FRONT-MATTER line matches. A commit that rewrote the line's text matches as well,
        # which is right: the setter is whoever wrote the line the file carries now.
        # during a merge the line may be committed on the side coming in: its history is read too, and "is it committed"
        # asks every parent, not HEAD alone — or an answer a merge brings reads as never committed (FM-019)
        tips = ["HEAD", *merge_heads()]
        log = subprocess.run(["git", "log", "-1", "--full-history", "--format=%H%n%an%n%ae", "-G", line_regex(needle), *tips, "--", rel], cwd=ROOT, capture_output=True, text=True, encoding="utf-8", errors="replace", env=nested_git_env())
        if log.returncode == 0 and log.stdout.strip():
            commit, name, email = (log.stdout.strip().split("\n") + ["", ""])[:3]
            dirty = subprocess.run(["git", "diff", "--quiet", "HEAD", "--", rel], cwd=ROOT, env=nested_git_env()).returncode != 0
            at = lambda rev: subprocess.run(["git", "show", f"{rev}:{rel}"], cwd=ROOT, capture_output=True, text=True, encoding="utf-8", errors="replace", env=nested_git_env()).stdout
            if not (dirty and not any(l.startswith(needle) for rev in tips for l in at(rev).splitlines())):
                out = (name, email, "git", commit)
    _LINE_AUTHOR[(rel, needle)] = out
    return out


def pending_author():
    """The author git WOULD write for the commit being made right now — `user.email`, unless the environment imposes
    another (`GIT_AUTHOR_EMAIL`). In the pre-commit run the line is not committed yet, and this is who is committing it."""
    out = subprocess.run(["git", "var", "GIT_AUTHOR_IDENT"], cwd=ROOT, capture_output=True, text=True, encoding="utf-8", errors="replace", env=nested_git_env())
    name, _, rest = out.stdout.partition(" <")
    return (name.strip(), rest.partition(">")[0].strip()) if out.returncode == 0 else ("", "")


def verified_as(commit, email=None):
    """The gate's ONE signature test, shared by every rule that asks for a signed line: `%G?` is G for a good
    signature under a trusted key, GPG or SSH alike — and the principal the key is trusted FOR (`%GS`) must be the
    identity claimed. A good signature under a trusted key still says nothing about whose name is on the commit."""
    v = subprocess.run(["git", "log", "-1", "--format=%G?%n%GS%n%ae", commit], cwd=ROOT, capture_output=True, text=True, encoding="utf-8", errors="replace", env=nested_git_env())
    good, signer, author_email = (v.stdout.split("\n") + ["", "", ""])[:3]
    claimed = (email or author_email).strip()
    return good.strip() == "G" and bool(claimed) and claimed in signer


def staged_now():
    """What the commit being made is about to carry — read once. The gate's version-control calls cost real seconds in
    a pre-commit hook, and a file this commit does not touch was checked by the run that committed it."""
    global _STAGED
    if _STAGED is None:
        out = subprocess.run(["git", "diff", "--cached", "--name-only", "--relative"], cwd=ROOT, capture_output=True, text=True, encoding="utf-8", errors="replace", env=nested_git_env())
        _STAGED = set(out.stdout.split("\n")) if out.returncode == 0 else set()
    return _STAGED


def in_this_commit(t):
    """Is this tracker's file part of what is being committed — always true outside a pre-commit run, where every
    tracker is read anyway (`--check` is the one that must miss nothing)."""
    if not COMMITTING:
        return True
    try:
        return (TRACKER_DIR / t["file"]).resolve().relative_to(ROOT).as_posix() in staged_now()
    except ValueError:
        return True


def seat_of(name, email):
    """Which seat this author is sitting in — matched on the identity `[seats]` gives it, email or name."""
    return next((s for s, (who, _m) in SEATS.items() if who and who in (email, name)), None)


def holds(seat, right):
    """Does that seat hold that right — the four built-in names carry theirs, `[rights]` defines any other name."""
    return right in SEAT_RIGHTS.get(seat, BUILTIN_RIGHTS.get(seat, set()))


def may_answer():
    """WHO MAY ANSWER, asked in ONE place — `{identity: "signed" | ""}`. With `[seats]` it is every seat that holds
    the `answer` right: the built-in `owner`, or any name `[rights]` gives it. `answerers` is the old spelling of
    exactly that list, so it is read only where there is no `[seats]` — a repository that has moved on would otherwise
    have to keep writing its Owner twice, and an answer from the seat that may give one was refused as *`answerers`
    names nobody*. The identity is the version control system's, as `[seats]` spells it: git's author email, or the
    account Subversion authenticated; `answerers` always meant the git author NAME, and still does."""
    if SEATS:
        return {who: mode for seat, (who, mode) in SEATS.items() if who and holds(seat, "answer")}
    return dict(ANSWERERS)


def answerers_problems():
    """A SIGNATURE `answerers` ASKS FOR AND `[seats]` DROPS (FM-015). With `[seats]`, `may_answer()` reads the seats
    alone, so `answerers = ["alice signed"]` beside `[seats] owner = "alice"` stopped being enforced at 0.17.1: Alice's
    unsigned answer counted, and `--answer` stopped signing. The seat that answers for an `answerers` identity is the one
    `[seats]` spells the same way — a name or an email; where none does, the tool cannot tell which of the seats holding
    `answer` is that person, so each of them stands in for it. One of those not `signed` is refused, naming both lines
    and the two ways out."""
    if not SEATS:
        return []
    out = []
    answering = [s for s, (who, _m) in SEATS.items() if who and holds(s, "answer")]
    for name, mode in ANSWERERS.items():
        if mode != "signed":
            continue
        same = [s for s in answering if SEATS[s][0] == name]
        for s in [s for s in (same or answering) if SEATS[s][1] != "signed"]:
            out.append(f'{CONFIG_NAME}: `answerers = ["{name} signed"]` asks for a signed answer, and `[seats] {s} = "{SEATS[s][0]}"` — '
                       + ("the seat that answers for it" if same else f"a seat holding `answer`; no seat is spelled `{name}`, so each stands in for it")
                       + f' — is not signed. `[seats]` alone decides who may answer (from 0.17.1), so that answer would count unsigned. '
                       f'Add `signed` to the seat (`{s} = "{SEATS[s][0]} signed"`), or remove `answerers`')
    return out


def no_seat(name, email, right, what):
    """The one refusal, worded once: who the version control system says made the change, the right it needed, and
    what the repository's seats are. It names the seat and the right — an agent told only *refused* tries again."""
    who = email or name or "nobody the version control system can name"
    seat = seat_of(name, email)
    known = ", ".join(f"{s} ({SEATS[s][0]})" for s in sorted(SEATS)) or "none"
    if seat is None:
        return (f'{what} — `{who}` is not a seat. The seats are: {known}'
                + ("" if vcs() == "svn" else ". A seat wears its badge: `git config --worktree user.email <identity>`"))
    return (f'{what} — `{who}` is the seat `{seat}`, which does not hold `{right}` '
            f'({", ".join(sorted(SEAT_RIGHTS.get(seat) or BUILTIN_RIGHTS.get(seat, set()))) or "no right"}). '
            f'A seat that needs it says so in `[rights]`, in the same diff as anything it would allow')


def seat_problems(t):
    """The `ask` right: who put this question in front of the Owner, read from the version control system.

    Absent `[seats]`, nothing is enforced. Present, the gate finds the commit that introduced this tracker's current
    `next: owner` line and refuses it when that author is not a seat holding `ask`; under `signed` the commit must
    also verify as that seat. In the pre-commit run the line is not committed yet, and the author is the one git is
    about to write. The other three rights are judged on the change itself (`rights_problems`) — this one is judged on
    the line, so the Owner's QUEUE can drop an ask that reached him another way. It catches an agent that does not
    know the rule, not one that lies: that is FM-007's class, and no gate closes it."""
    if not SEATS or not in_this_commit(t):
        return []
    name, email, how, commit = line_author(TRACKER_DIR / t["file"], "next: owner")
    if how == "uncommitted":
        if vcs() == "svn":
            return []                                    # Subversion has no client hook; the server's gate reads it next
        name, email, commit = (*pending_author(), "")    # not committed yet: the author git is about to write is who is asking
    seat = seat_of(name, email)
    if seat is None or not holds(seat, "ask"):
        return [no_seat(name, email, "ask", "`next: owner` puts a question in front of the Owner")]
    if SEATS[seat][1] == "signed" and how != "svn":
        if not commit:
            print(f'  {t["id"]}: the `next: owner` line is being committed now — the seat\'s signature is verified on the commit, by the next run', file=sys.stderr)
        elif not verified_as(commit, email or None):
            return [f'the commit `{commit[:10]}` that set `next: owner` does not verify as the seat `{seat}` — `[seats]` asks this seat to '
                    f'sign, and a git author is only a string: sign it (`git commit -S`), or the ask does not reach him']
    return []


def asks_records(body):
    """The records under the body's `## Asks` heading — one paragraph each, as `--clear-ask` writes them — normalised
    for comparison: lower case, every run of whitespace one space, quotes gone."""
    at = ASKS_HEAD_RE.search(body)
    if not at:
        return []
    rest = re.search(r"^#{2,3}\s+", body[at.end():], re.M)
    section = body[at.end(): at.end() + (rest.start() if rest else len(body) - at.end())]
    return [re.sub(r"\s+", " ", p.replace('"', "")).strip().lower() for p in re.split(r"\n\s*\n", section) if p.strip()]


def cleared(b, b_body, a, a_body):
    """THE CLEARING MOVE (FM-014): the three answer lines leave the front matter AND the body gains the record of that
    exchange under `## Asks` — the same question, the same answer, the same answered-by. That is the seat's receipt for
    acting on the answer, not an answer, and it is judged under `ask`. Anything else that touches the three lines —
    removing them with no record, editing the answer — stays the Owner's `answer`."""
    if not (b.get("answer") or "").strip() or any((a.get(k) or "").strip() for k in ("answer", "answered", "answered-by")):
        return False
    quiet = lambda s: re.sub(r"\s+", " ", (s or "").replace('"', "")).strip().lower()
    want = [quiet(b.get("ask")), quiet(b.get("answer"))] + ([quiet(b.get("answered-by"))] if quiet(b.get("answered-by")) not in ("", "<you>") else [])
    count = lambda records: sum(all(w in r for w in want) for r in records)
    return all(want[:2]) and count(asks_records(a_body)) > count(asks_records(b_body))


def transitions(before, after, new_file=False):
    """Which of the four rights a change exercises, read from the front matter on both sides. A NEW tracker is not a
    triage verdict for carrying `considered:` — that line is the filing rule; a `tier:` or a `rank:` on it is. Clearing
    an answered ask with its record is `clear` — the `ask` right's, judged on the change (`rights_problems`)."""
    b, b_body = parse_frontmatter(before)
    a, a_body = parse_frontmatter(after)
    got, changed = set(), lambda k: (a.get(k) or "").strip() != (b.get(k) or "").strip()
    if any(changed(k) for k in ("answer", "answered", "answered-by")):
        got.add("clear" if cleared(b, b_body, a, a_body) else "answer")
    if (a.get("next") or "").strip().lower() == "owner" and (b.get("next") or "").strip().lower() != "owner":
        got.add("ask")
    if a.get("status") and classify_status(a["status"]) not in OPEN_STATUSES and (not b.get("status") or classify_status(b["status"]) in OPEN_STATUSES):
        got.add("close")
    if any(changed(k) for k in TRIAGE_KEYS) or (changed("considered") and not new_file):
        got.add("triage")
    return got


def merge_heads():
    """The other parents of a merge being committed right now — `MERGE_HEAD`, one line per head — or none."""
    out = subprocess.run(["git", "rev-parse", "--git-path", "MERGE_HEAD"], cwd=ROOT, capture_output=True, text=True, encoding="utf-8", errors="replace", env=nested_git_env())
    f = pathlib.Path(out.stdout.strip()) if out.returncode == 0 and out.stdout.strip() else None
    f = f if f is None or f.is_absolute() else ROOT / f
    return f.read_text(encoding="utf-8").split() if f is not None and f.is_file() else []


def changes_under_review():
    """WHAT THIS RUN IS JUDGING, once — a list of changes, each (the revisions it is read against, the tracker files it
    touches, author name, author email, the commit or "" when it is not made yet, the revision that holds its result or
    None for the working tree, a label that names it). The commit being made — staged, or simply not committed yet —
    read against HEAD; on a clean tree, the commit at HEAD read against its parent.

    A MERGE (FM-019) is two kinds of change, and neither is the merger's alone:
    1. EACH COMMIT IT BRINGS — every non-merge commit reachable from it and not from its first parent — against its own
       parent, under its own author and its own signature. A commit made without the hook (`--no-verify`, a clone with no
       hook installed, the forge's editor) was never judged; a merge must not launder it.
    2. ITS OWN CHANGE — the tracker files where the result differs from EVERY parent (a conflict resolved, an edit made in
       the merge), judged under the merger. A clean merge adds nothing of its own.
    Read against its first parent alone, a merge was everything its branch carried and all of it the merger's: `--check`
    on a trunk went red on the first pull request carrying an answer or a close, the forge's merge identity being no
    seat. The same two parts hold for a merge being committed now — HEAD and `MERGE_HEAD` are its parents. The commits a
    merge brings are read only when there is a merge: one `git log` for all of them."""
    git = lambda *a: subprocess.run(["git", *a], cwd=ROOT, capture_output=True, text=True, encoding="utf-8", errors="replace", env=nested_git_env())
    names = lambda r: set(r.stdout.split("\n")) - {""} if r.returncode == 0 else set()

    def brought(tips, first):
        """(1): every non-merge commit reachable from `tips` and not from `first`, oldest first, each with its files."""
        if not tips:
            return []
        out = []
        log = git("log", "--no-merges", "--reverse", "--relative", "--name-only", "--format=%x00%H%x00%an%x00%ae", *tips, "--not", first)
        records = log.stdout.split("\x00")[1:]          # hash · name · email, then the files --name-only lists under it
        for i in range(0, len(records) - 2, 3):
            c, an, rest = records[i], records[i + 1], records[i + 2]
            ae, _, files = rest.partition("\n")
            out.append(([f"{c}^1"], set(files.split("\n")) - {""}, an, ae.strip(), c, c, f"in `{c[:10]}` ({ae.strip() or an}), which the merge brings"))
        return out

    heads = merge_heads()
    if COMMITTING or (git("diff", "--name-only", "--relative", "HEAD").stdout.strip()):
        files = set(staged_now()) if COMMITTING else names(git("diff", "--name-only", "--relative", "HEAD"))
        for h in heads:
            files &= names(git("diff", *(["--cached"] if COMMITTING else []), "--name-only", "--relative", h))
        return brought(heads, "HEAD") + [(["HEAD", *heads], files, *pending_author(), "", None, "")]
    parents = git("rev-list", "--parents", "-n", "1", "HEAD").stdout.split()[1:]
    if not parents:
        return []                                        # a root commit has no parent to compare with
    files = None
    for parent in parents:
        got = names(git("diff", "--name-only", "--relative", parent, "HEAD"))
        files = got if files is None else files & got
    name, email, commit = (git("log", "-1", "--format=%an%n%ae%n%H").stdout.split("\n") + ["", "", ""])[:3]
    return (brought(parents[1:], parents[0]) if len(parents) > 1 else []) + [(parents, files, name, email, commit, "HEAD", "")]


def rights_problems(trackers):
    """`answer`, `close` and `triage`: the author of the change must be a seat that holds the right for every
    transition the change makes. (`ask` is judged on the line, by `seat_problems` — except the clearing move, which has
    no line left to judge and is read here, from the change, under `ask`: FM-014.) Under Subversion there is no
    pending commit to read and no client hook to read it in — the server's own `pre-commit` hook runs the gate, and
    the author of each line is the one the server authenticated, so the transitions are read from the lines."""
    if not SEATS or vcs() not in ("git", "svn"):
        return []
    out = []
    if vcs() == "svn":
        for t in trackers:
            for right, needle in (("answer", "answer:"), ("close", "status:"), ("triage", "considered:")):
                if right == "close" and t["status"] in OPEN_STATUSES:
                    continue
                if right == "answer" and not t.get("answer"):
                    continue
                if right == "triage" and not any((t.get("fm", {}).get(k) or "").strip() for k in TRIAGE_KEYS):
                    continue
                if right == "triage":
                    needle = next(k + ":" for k in TRIAGE_KEYS if (t.get("fm", {}).get(k) or "").strip())
                name, _e, how, _rev = line_author(TRACKER_DIR / t["file"], needle)
                if how == "svn" and not holds(seat_of(name, None), right):
                    out.append(f'{t["id"]}: ' + no_seat(name, None, right, f'`{needle}` is a `{right}` change'))
        return out
    show = lambda rev, rel: subprocess.run(["git", "show", f"{rev}:{rel}"], cwd=ROOT, capture_output=True, text=True, encoding="utf-8", errors="replace", env=nested_git_env())
    rels = {(TRACKER_DIR / t["file"]).resolve().relative_to(ROOT).as_posix(): t for t in trackers}
    for bases, files, name, email, commit, result, label in changes_under_review():
        seat, where = seat_of(name, email), (label + " — " if label else "")
        for rel in sorted(files & set(rels)):
            t = rels[rel]
            now = (TRACKER_DIR / t["file"]).read_text(encoding="utf-8") if result is None else show(result, rel).stdout
            moves = None                                # a merge's own move is one it makes against EVERY parent (FM-019)
            for base in bases:
                was = show(base, rel)
                made = transitions(was.stdout if was.returncode == 0 else "", now, new_file=was.returncode != 0)
                moves = made if moves is None else moves & made
            for move in sorted(moves - {"ask"}):
                right = "ask" if move == "clear" else move
                if not holds(seat, right):
                    out.append(f'{t["id"]}: {where}' + no_seat(name, email, right, "this change clears an answered ask — the seat that acts on an answer holds `ask`"
                                                                if move == "clear" else f'this change is a `{right}`'))
                elif SEATS[seat][1] == "signed":
                    if not commit:
                        print(f'  {t["id"]}: a `{right}` change is being committed now — the seat\'s signature is verified on the commit, by the next run', file=sys.stderr)
                    elif not verified_as(commit, email or None):
                        out.append(f'{t["id"]}: the commit `{commit[:10]}` making a `{right}` change does not verify as the seat `{seat}` — '
                                   f'`[seats]` asks this seat to sign: sign it (`git commit -S`), or the change does not count')
    return out


# --- sessions (FM-024): a seat's commit names its session, and the record knows the session ------------------------
# Seat = author: WHO MAY, read by the rights above. Session = which RUN: a `Session: <id>` trailer on every seat commit,
# appended by the prepare-commit-msg hook from the worktree's `seat.session`, and one row per session in the registry
# `<tracker dir>/sessions.md` — who convened it, for what, in which worktree. The rules hold where the registry
# exists: a repository adopts them by opening its first session, and a commit made before its tree had a registry is
# not judged by them.
SESSIONS_NAME = "sessions.md"
SESSION_COLUMNS = ("Session", "Seat", "Convened by", "Scope", "Worktree", "Started", "Ended")
SESSION_ID_RE = re.compile(r"[A-Za-z0-9][A-Za-z0-9_.-]*(?:/[A-Za-z][A-Za-z0-9-]*-\d+)*")      # a9 · 8e509911 · a9/reviewer-1
SESSION_PARENT_RE = re.compile(r"(?<![\w/.-])([0-9a-f]{8}(?:/[A-Za-z][A-Za-z0-9-]*-\d+)*|[A-Za-z0-9][A-Za-z0-9_.-]*(?:/[A-Za-z][A-Za-z0-9-]*-\d+)+)(?![\w/.-])")
SESSION_IDLE = 86400          # seconds: an open session with no commit for longer than a day is abandoned — listed, closed by a pass
SESSIONS_HOME = """\
# Sessions

One row per session of a seat: who convened it, for what, in which worktree. `--session open` writes a row and
`--session close` dates its end; the gate refuses a seat's commit whose `Session:` trailer names no open row here, or
whose worktree is open under another session. An open row with no commit for a day is closed by the next triage pass,
which says so.

| {head} |
|{sep}
"""


def git_out(*a, cwd=None):
    """One git call's stdout, or None when it failed."""
    r = subprocess.run(["git", *a], cwd=cwd or ROOT, capture_output=True, text=True, encoding="utf-8", errors="replace", env=nested_git_env())
    return r.stdout if r.returncode == 0 else None


def sessions_file():
    return TRACKER_DIR / SESSIONS_NAME


def parse_sessions(text):
    """The registry's rows, in order: each a dict of the seven columns, plus `open` (no end written). A cell may carry
    `|` escaped as `\\|`. Anything that is not a seven-cell table row, or is the header or its rule, is not a row."""
    rows = []
    for line in (text or "").splitlines():
        if not line.lstrip().startswith("|"):
            continue
        cells = [c.strip().replace("\\|", "|") for c in re.split(r"(?<!\\)\|", line.strip())[1:-1]]
        if len(cells) != len(SESSION_COLUMNS) or cells[0] in ("Session", "") or set(cells[0]) <= set("-: "):
            continue
        row = dict(zip(("id", "seat", "convened", "scope", "worktree", "started", "ended"), cells))
        row["open"] = row["ended"] in ("", "—", "-")
        rows.append(row)
    return rows


def render_session_row(r):
    cell = lambda v: (v or "—").replace("|", "\\|").replace("\n", " ")
    return "| " + " | ".join(cell(r[k]) for k in ("id", "seat", "convened", "scope", "worktree", "started", "ended")) + " |"


def write_sessions(rows):
    """Rewrite the registry with these rows, keeping whatever stands above the table, and stage it."""
    path = sessions_file()
    have = path.read_text(encoding="utf-8") if path.exists() else SESSIONS_HOME.format(head=" | ".join(SESSION_COLUMNS), sep="---|" * len(SESSION_COLUMNS))
    lines = have.rstrip("\n").split("\n")
    table = [i for i, l in enumerate(lines) if l.lstrip().startswith("|")]
    head = lines[:table[0] + 2] if table else lines + ["", "| " + " | ".join(SESSION_COLUMNS) + " |", "|" + "---|" * len(SESSION_COLUMNS)]
    tail = lines[table[-1] + 1:] if table else []
    path.parent.mkdir(parents=True, exist_ok=True)
    put(path, "\n".join(head + [render_session_row(r) for r in rows] + tail) + "\n")
    if vcs() == "git":
        git_out("add", "--", path.relative_to(ROOT).as_posix())


def session_now():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M")


def session_cmd(words):
    """`--session new` · `--session open <id> <seat> "<convened by>" "<scope>" [<worktree>]` · `--session close <id>`."""
    rows = parse_sessions(sessions_file().read_text(encoding="utf-8")) if sessions_file().exists() else []
    ids = {r["id"] for r in rows}
    verb, rest = words[0], words[1:]
    if verb == "new":
        import secrets
        sid = next(s for s in iter(lambda: secrets.token_hex(4), None) if s not in ids)
        print(sid)
        return EXIT_OK
    if verb == "open" and 4 <= len(rest) <= 5:
        sid, seat, convened, scope = rest[:4]
        top = git_out("rev-parse", "--show-toplevel")
        worktree = rest[4] if len(rest) == 5 else (pathlib.Path(top.strip()).name if top else ROOT.name)
        hand = sid.rsplit("/", 1)[-1] if "/" in sid else None
        # convened by a SESSION, not a person: a sub-agent — its id derives from its parent's, or the independence report
        # cannot see that the two are one run (R3: a sibling's verdict was read as independent of the builder). A parent is
        # read only from a token in the session-id form — eight hex characters, or `<id>/<seat>-<n>` — never from a plain
        # word: "the morning session today" names no session (R6)
        parent = (SESSION_PARENT_RE.search(convened) or [None, None])[1]
        why = ("is not a session id — letters, digits, `.`, `_`, `-`; a sub-agent's is `<parent>/<seat>-<n>`" if not SESSION_ID_RE.fullmatch(sid)
               else f"is already in {SESSIONS_NAME} — an id is used once" if sid in ids
               else f"is convened by session {parent} — a sub-agent's id derives from its parent's: `{parent}/{seat}-<n>`" if parent and not sid.startswith(parent + "/")
               else f"names the hand `{hand}`, not the seat `{seat}` — a sub-agent's id is `<parent>/{seat}-<n>`" if hand and not re.fullmatch(rf"{re.escape(seat)}-\d+", hand)
               else f"is for the seat `{seat}`, which `[seats]` does not name" if SEATS and seat not in SEATS else "")
        clash = next((r for r in rows if r["open"] and r["worktree"] == worktree), None)
        if why or clash:
            print(f"--session open: {sid} {why}" if why else f"--session open: {worktree} is open under session {clash['id']} — one worktree per session", file=sys.stderr)
            return EXIT_LINT
        rows.append(dict(id=sid, seat=seat, convened=convened, scope=scope, worktree=worktree, started=session_now(), ended="—", open=True))
        write_sessions(rows)
        mine = (git_out("config", "--get", "seat.session") or "").strip()
        print(f"opened session {sid} ({seat}, {scope}) in {worktree} — {sessions_file().relative_to(ROOT).as_posix()} is staged; the session's first commit carries it"
              + ("" if mine == sid else f"\nthis worktree's commits carry it once: git config --worktree seat.session {sid}"))
        return EXIT_OK
    if verb == "close" and len(rest) == 1:
        row = next((r for r in rows if r["id"] == rest[0]), None)
        if row is None or not row["open"]:
            print(f"--session close: {rest[0]} is {'not in ' + SESSIONS_NAME if row is None else 'closed already'}", file=sys.stderr)
            return EXIT_LINT
        row["ended"] = session_now()
        write_sessions(rows)
        print(f"closed session {row['id']} — {sessions_file().relative_to(ROOT).as_posix()} is staged")
        return EXIT_OK
    print('--session: new · open <id> <seat> "<convened by>" "<scope>" [<worktree>] · close <id>', file=sys.stderr)
    return EXIT_LINT


def session_trailer(message_file):
    """What the prepare-commit-msg hook calls: append `Session: <seat.session>` to the message being written. Nothing
    when this worktree has no `seat.session` (the Owner's checkout, a person's clone), and nothing when the message
    carries a `Session:` already — an amend, a rebase, a seat that typed it."""
    sid = (git_out("config", "--get", "seat.session") or "").strip()
    if not sid or not message_file:
        return EXIT_OK
    r = subprocess.run(["git", "interpret-trailers", "--in-place", "--if-exists", "doNothing", "--trailer", f"Session: {sid}", message_file],
                       cwd=ROOT, capture_output=True, text=True, encoding="utf-8", errors="replace", env=nested_git_env())
    if r.returncode:
        print(f"--session-trailer: {r.stderr.strip()}", file=sys.stderr)
    return r.returncode


# A commit's trailers as git prints them — one `Name: value` per trailer, the trailer block only, each separated by \x03 —
# and the key picked here in Python, case aside, as git itself matches a key. Asking git to filter would put a
# `name=<value>` shape into this source, which a consumer's secret-shape gate reads as a credential (0.17.7).
TRAILERS = "%(trailers:only,separator=%x03)"


def trailer_values(block, name):
    """Every value of the trailer `name` in one TRAILERS field, in order, stripped."""
    out = []
    for item in (block or "").split("\x03"):
        k, sep, v = item.partition(":")
        if sep and k.strip().lower() == name.lower() and v.strip():
            out.append(v.strip())
    return out


def trailers_of(commit, name):
    """Every value of one trailer on one commit."""
    return trailer_values((git_out("log", "-1", f"--format={TRAILERS}", commit) or "").strip("\n"), name)


def session_problems():
    """The gate's three refusals (example e): a seat's commit — not the Owner's — must carry a `Session:` whose row is
    open and is the author's seat, and whose worktree no earlier open row holds. Judged on every change the rights are
    judged on (`changes_under_review`): the commit being made reads `seat.session`, the trailer its hook will write; a
    made commit reads its trailer; each against the registry in its own tree — a tree with none, whose parent had none,
    is not judged. A change that REMOVES the registry, drops a row or re-opens an ended one is judged against its
    parent's registry and refused (R1): the registry is the record the gate reads, so a seat never writes its way past
    it — only the Owner removes it. The commit that closes its own session's row is that session's, still (its last)."""
    if not SEATS or vcs() != "git":
        return []
    rel, out = sessions_file().relative_to(ROOT).as_posix(), []
    for bases, _files, name, email, commit, result, label in changes_under_review():
        seat = seat_of(name, email)
        if seat in (None, "owner"):
            continue
        if result is not None:
            after = git_out("show", f"{result}:{rel}")
        elif COMMITTING:
            after = git_out("show", f":{rel}")              # the index: what this commit will carry
        else:
            after = sessions_file().read_text(encoding="utf-8") if sessions_file().exists() else None
        before = git_out("show", f"{bases[0]}:{rel}") if bases else None
        if after is None and before is None:
            continue
        where = label + " — " if label else ""
        sid = (trailers_of(commit, "Session") or [""])[0] if commit else (git_out("config", "--get", "seat.session") or "").strip()
        who = f"commit {commit[:10]} by {email or name}" if commit else f"this commit by {email or name}"
        was = parse_sessions(before) if before is not None else []
        rows = parse_sessions(after) if after is not None else was
        now_by_id = {r["id"]: r for r in rows}
        if after is None:
            out.append(f"{where}refused: {who} removes {rel} — the registry is the Owner's to remove; a session ends with `{CMD} --session close <id>`")
        else:
            dropped = [r["id"] for r in was if r["id"] not in now_by_id]
            reopened = [r["id"] for r in was if not r["open"] and now_by_id.get(r["id"], {}).get("open")]
            if dropped or reopened:
                said_ = ([f"drops the row{'s' if len(dropped) > 1 else ''} {', '.join(dropped)}"] if dropped else []) + ([f"re-opens {', '.join(reopened)}, which had ended"] if reopened else [])
                out.append(f"{where}refused: {who} {'; '.join(said_)} in {rel} — a row once written stays, and an ended session stays ended: open a new one")
                rows, now_by_id = was, {r["id"]: r for r in was}
        row = now_by_id.get(sid)
        closing = row is not None and not row["open"] and any(r["id"] == sid and r["open"] for r in was)     # its last commit
        if not sid:
            out.append(f"{where}refused: {who} carries no Session: trailer — set `git config --worktree seat.session <id>` and open the row ({CMD} --session open)")
        elif row is None or not (row["open"] or closing):
            out.append(f"{where}refused: Session: {sid} has no open row in {rel}")
        elif row["seat"] != seat:
            out.append(f"{where}refused: Session: {sid} is open for the seat {row['seat']}, and {who} is the seat {seat}")
        elif row["open"]:
            first = next(r for r in rows if r["open"] and r["worktree"] == row["worktree"])
            if first is not row:
                out.append(f"{where}refused: {row['worktree']} is open under session {first['id']} — one worktree per session")
    return out


def session_check():
    """`--session-check`: the session rule on the commit being made, and nothing else — cheap enough for every commit.
    The full gate runs only when a tracker, the configuration or the tool is staged; without this, a seat's code-only
    commit would be judged by no automatic run at all (R4)."""
    global COMMITTING
    COMMITTING = True
    problems = session_problems()
    for p_ in problems:
        print(f"  {p_}", file=sys.stderr)
    return EXIT_LINT if problems else EXIT_OK


def session_stamp(text):
    """A registry time (`YYYY-MM-DD HH:MM`, or a bare date) as seconds, or None."""
    for fmt in ("%Y-%m-%d %H:%M", "%Y-%m-%d"):
        try:
            return datetime.datetime.strptime((text or "")[:len("2026-01-01 00:00") if fmt.endswith("%M") else 10], fmt).timestamp()
        except ValueError:
            pass
    return None


def abandoned_sessions(rows, now=None):
    """Open rows with no commit carrying their id for longer than SESSION_IDLE — each (row, the last sign of life as
    `YYYY-MM-DD HH:MM`). One `git log` over the commits since the oldest open row started."""
    live = [r for r in rows if r["open"]]
    if not live:
        return []
    now = now or datetime.datetime.now().timestamp()
    since = min((session_stamp(r["started"]) or now) for r in live)
    last = {}
    log = git_out("log", f"--since={int(since)}", f"--format=%ct%x01{TRAILERS}%x02", "HEAD") or ""
    for rec in log.split("\x02"):
        stamp, _, block = rec.strip("\n").partition("\x01")
        if stamp.strip().isdigit():
            for sid in trailer_values(block, "Session"):
                last[sid] = max(last.get(sid, 0), int(stamp.strip()))
    out = []
    for r in live:
        seen = max(last.get(r["id"], 0), session_stamp(r["started"]) or 0)
        if now - seen > SESSION_IDLE:
            out.append((r, datetime.datetime.fromtimestamp(seen).strftime("%Y-%m-%d %H:%M") if seen else "never"))
    return out


def trunk_ref():
    """The trunk a verdict's branch is measured against: `origin/main`, else `main`, else `master`."""
    return next((ref for ref in ("origin/main", "main", "master") if git_out("rev-parse", "--verify", "--quiet", ref + "^{commit}")), None)


def reviewed_range(tip, trunk, first_parents, on_line):
    """The reviewed branch's OWN commits (R2): `git rev-list <tip> ^<trunk> --no-merges` — what the trunk brought in by a
    merge is not the branch's. A tip the trunk has since merged is measured against the trunk as it stood before the merge
    that brought it (`^M^1`), so the report does not change when the branch lands. None: the tip is on the trunk's own
    first-parent line — not a branch verdict. Returned as the arguments of the `git log` that reads the range."""
    if not trunk:
        return ["--no-merges", tip]
    if git_out("merge-base", "--is-ancestor", tip, trunk) is None:
        stop = trunk
    elif tip in on_line:
        return None
    else:                                                   # the trunk's first-parent commits that contain the tip are a
        after = set((git_out("rev-list", "--ancestry-path", f"{tip}..{trunk}") or "").split())     # prefix of its line;
        landed = [c for c in itertools.takewhile(lambda c: c in after, first_parents)]            # the oldest brought it
        stop = f"{landed[-1]}^1" if landed else trunk
    return ["--no-merges", tip, f"^{stop}"]


def verdict_reports(days=None):
    """S6 — each verdict commit (it carries `Reviewed: <sha>`) of the last `days` days on HEAD, as (verdict, reviewed,
    its session, the reviewed range's sessions, the word): *independent* when the verdict's session root is none of the
    range's, *same session* when it is one of them, *untraced* when either side names no session, *on trunk* when the tip
    is on the trunk's first-parent line (not a branch verdict). The range is the branch's own commits, less other
    verdicts (`reviewed_range`). A report, never a refusal (slice 2 refuses, after a week of counts)."""
    days = TRIAGE_DAYS if days is None else days
    log = git_out("log", f"--since={days}.days", f"--format=%H%x01{TRAILERS}%x02", "HEAD") or ""
    found = []
    for rec in log.split("\x02"):
        sha, _, block = rec.strip("\n").partition("\x01")
        reviewed = trailer_values(block, "Reviewed")
        if sha and reviewed:
            found.append((sha, reviewed[0], (trailer_values(block, "Session") or [""])[0]))
    if not found:
        return []
    trunk = trunk_ref()
    first_parents = (git_out("rev-list", "--first-parent", trunk) or "").split() if trunk else []      # newest first
    on_line = set(first_parents)
    out = []
    for verdict, reviewed, sid in found:
        tip = (git_out("rev-parse", "--verify", "--quiet", f"{reviewed}^{{commit}}") or "").strip()
        own = reviewed_range(tip, trunk, first_parents, on_line) if tip else []
        ranged = set()
        if own:
            rng = git_out("log", f"--format={TRAILERS}%x02", *own) or ""
            for block in rng.split("\x02"):
                if not trailer_values(block, "Reviewed"):
                    ranged |= set(trailer_values(block, "Session"))
        roots = {s.split("/")[0] for s in ranged}
        word = ("on trunk" if own is None else "untraced" if not sid or not ranged
                else "same session" if sid.split("/")[0] in roots else "independent")
        out.append((verdict, reviewed, sid, sorted(ranged), word))
    return out


def sessions_report():
    """What `--check` says of the registry, never a refusal: the abandoned rows a pass will close, and this week's
    verdicts by independence."""
    if not sessions_file().exists() or vcs() != "git":
        return []
    lines = [f"session {r['id']} ({r['seat']}, {r['scope']}) has no commit since {seen} — abandoned; the next triage pass closes it"
             for r, seen in abandoned_sessions(parse_sessions(sessions_file().read_text(encoding="utf-8")))]
    reps = verdict_reports()
    if reps:
        count = collections.Counter(w for *_x, w in reps)
        lines.append(f"reviews this week · {len(reps)} verdict(s) · independent {count['independent']} · same session {count['same session']}"
                     + (f" · untraced {count['untraced']}" if count["untraced"] else "") + (f" · on trunk {count['on trunk']}" if count["on trunk"] else ""))
        lines += [f"  verdict {v[:10]} on {r[:10]}: " + ("on trunk — not a branch verdict" if w == "on trunk" else
                  f"{w} — its session {s or '(none)'}; the branch's {', '.join(rs) or '(none)'}") for v, r, s, rs, w in reps]
    return lines


def board_sessions():
    """The registry as the board shows it — the open rows (id, seat, scope, worktree, abandoned) and this week's verdicts
    as [independent, same session, untraced] — or None where there is no registry."""
    if not sessions_file().exists() or vcs() != "git":
        return None
    rows = parse_sessions(sessions_file().read_text(encoding="utf-8"))
    gone, reps = {r["id"] for r, _ in abandoned_sessions(rows)}, verdict_reports()
    count = collections.Counter(w for *_x, w in reps)
    return {"open": [[r["id"], r["seat"], r["scope"], r["worktree"], r["id"] in gone] for r in rows if r["open"]],
            "reviews": [count["independent"], count["same session"], count["untraced"], count["on trunk"]] if reps else None}


def sessions_digest():
    """The digest's one line: the open sessions, by seat — or nothing where there is no registry."""
    reg = board_sessions()
    if reg is None:
        return ""
    by = collections.defaultdict(list)
    for sid, seat, *_x in reg["open"]:
        by[seat].append(sid)
    return "SESSIONS OPEN · " + (" · ".join(f"{seat} {len(ids)} ({', '.join(ids)})" for seat, ids in by.items()) or "none")


def close_abandoned(today):
    """A triage pass closes every abandoned row — dated, with why — and returns them for its paragraph. Nothing closes
    silently: the pass prints them, and its paragraph in TRIAGE.md names them."""
    if not sessions_file().exists() or vcs() != "git":
        return []
    rows = parse_sessions(sessions_file().read_text(encoding="utf-8"))
    gone = abandoned_sessions(rows)
    for r, seen in gone:
        r["ended"] = f"closed by the pass of {today} — no commit since {seen}"
    if gone:
        write_sessions(rows)
    return gone

ASK_LINES = ("ask:", "ask-kind:", "ask-since:", "ask-proposal:", "ask-options:", "answer:", "answered:", "answered-by:")


def record_problems(t):
    """CLEARING AN ASK KEEPS THE RECORD. A tracker that had an answer and is losing it must carry the exchange in its
    body: an answer deleted from the front matter and written nowhere else is the Owner's ruling gone, and the next
    seat asks it again. Only in the pre-commit run, and only against what this commit stages — the comparison is with
    `git show HEAD:<file>`, which is the version this commit is about to replace."""
    if vcs() != "git" or not in_this_commit(t):
        return []
    rel = (TRACKER_DIR / t["file"]).resolve().relative_to(ROOT).as_posix()
    was = subprocess.run(["git", "show", f"HEAD:{rel}"], cwd=ROOT, capture_output=True, text=True, encoding="utf-8", errors="replace", env=nested_git_env())
    if was.returncode != 0:
        return []                                        # new file: there is no answer to lose
    before, _body = parse_frontmatter(was.stdout)
    had = (before.get("answer") or "").strip()
    if not had or t.get("answer"):
        return []
    for h in merge_heads():                              # a merge loses an answer only if EVERY parent had it (FM-019)
        other = subprocess.run(["git", "show", f"{h}:{rel}"], cwd=ROOT, capture_output=True, text=True, encoding="utf-8", errors="replace", env=nested_git_env())
        if not (parse_frontmatter(other.stdout)[0].get("answer") or "").strip():
            return []
    quiet = lambda s: re.sub(r"\s+", " ", s.strip().strip('"').lower())
    text = (TRACKER_DIR / t["file"]).read_text(encoding="utf-8")
    if not t.get("asks_block"):
        return [f'{t["id"]}: the answer is being removed and the exchange is nowhere in the body — an answer deleted and written nowhere '
                f'else is the ruling gone, and the next seat asks it again. `{CMD} --clear-ask {t["id"]} <next move>` moves it under `## {HEAD["asks"]}`']
    if quiet(had) not in quiet(text):
        return [f'{t["id"]}: there is a `## {HEAD["asks"]}` heading, but the answer that is being removed is not under it — the record is '
                f'the Owner\'s words, kept verbatim: date · question · answer · answered-by. `{CMD} --clear-ask {t["id"]} <next move>` writes it']
    return []


def clear_ask(words, trackers):
    """`--clear-ask <id> <next move>` — the seat has acted on the answer: the exchange moves into the body under
    `## Asks` (date · question · answer · answered-by, newest last), the ask and answer lines leave the front matter,
    and `next:` becomes the move that follows. Done by hand, the answer is usually just deleted; the gate refuses that."""
    if len(words) != 2 or words[1].lower() not in MOVES:
        print(f"--clear-ask <id> <next move> — the move that follows: {' · '.join(MOVES)}", file=sys.stderr)
        return EXIT_LINT
    tid, move = words[0].upper(), words[1].lower()
    t = next((x for x in trackers if x["id"] == tid), None)
    if not t:
        print(f"--clear-ask: no tracker {tid}", file=sys.stderr)
        return EXIT_LINT
    if not t.get("ask"):
        print(f"--clear-ask: {tid} carries no `ask:` — there is nothing to clear", file=sys.stderr)
        return EXIT_LINT
    path = TRACKER_DIR / t["file"]
    text = path.read_text(encoding="utf-8")
    fm, body = parse_frontmatter(text)
    head = text[: len(text) - len(body)]
    kept = [l for l in head.split("\n") if not any(l.startswith(k) for k in ASK_LINES)]
    kept = [f"next: {move}" if l.startswith("next:") else l for l in kept]
    if not any(l.startswith("next:") for l in kept):
        kept.insert(len(kept) - 1, f"next: {move}")       # `head` ends on the closing `---`; the move goes above it
    block = (f'**{t.get("answered") or datetime.date.today().isoformat()}** · {t["ask"]}\n'
             + (f'**answered** — {t["answer"]} · {t["answered_by"]}\n' if t.get("answer") else "**withdrawn** — no answer was given\n"))
    at = ASKS_HEAD_RE.search(body)
    if at:                                                # newest last: at the end of the section that is there
        rest = re.search(r"^#{2,3}\s+", body[at.end():], re.M)
        cut = at.end() + (rest.start() if rest else len(body) - at.end())
        body = body[:cut].rstrip("\n") + "\n\n" + block + "\n" + body[cut:]
    else:
        log = re.search(r"^#{2,3}\s+(%s)\s*$" % re.escape(HEAD["log"]), body, re.I | re.M)
        section = f'## {HEAD["asks"]}\n\n{block}\n'
        body = (body[: log.start()] + section + body[log.start():]) if log else body.rstrip("\n") + f"\n\n{section}"
    put(path, "\n".join(kept) + body)
    print(f'{tid}: the exchange is in the body under `## {HEAD["asks"]}`, the ask is cleared, `next: {move}`.\n'
          f'  commit {path.relative_to(ROOT).as_posix()} — the gate refuses an answer removed without its record')
    return EXIT_OK


def acted_on(trackers):
    """What a seat has acted on since the Owner's last sitting: a tracker whose exchange has moved into the body and
    whose `ask:` line is gone — named by the commit that removed it, so the Owner can read what his answer became.

    `-G '^ask:'`, anchored like `line_author`: trackers discuss `ask:` in their prose all the time, and a substring
    pickaxe named whichever commit last wrote a sentence about the key instead of the one that cleared the line.
    `--full-history` for the same reason it is there: an ask cleared, re-asked and cleared again on a branch merges to
    a file byte-identical to one the trunk already had, and git's default simplification walks past the whole branch."""
    if vcs() != "git":
        return []
    since = last_standup()
    out = []
    for t in trackers:
        if t.get("ask") or not t.get("asks_block"):
            continue
        rel = (TRACKER_DIR / t["file"]).resolve().relative_to(ROOT).as_posix()
        log = subprocess.run(["git", "log", "-1", "--full-history", "--format=%h %ct", "-G", line_regex("ask:"), "--", rel], cwd=ROOT, capture_output=True, text=True, encoding="utf-8", errors="replace", env=nested_git_env())
        short, _, when = log.stdout.strip().partition(" ")
        if short and when.isdigit() and int(when) >= since:
            out.append((t, short))
    return out


def last_standup():
    """The clock the seat's side of the exchange is measured on: the Owner's last sitting — `standup` in the
    configuration, the most recent one that has passed; with no standup configured, the last day."""
    now = datetime.datetime.now()
    at = str(CONFIG.get("standup") or "").strip()
    if not re.fullmatch(r"([01]\d|2[0-3]):[0-5]\d", at):
        return int((now - datetime.timedelta(days=1)).timestamp())
    today = datetime.datetime.combine(now.date(), datetime.time(int(at[:2]), int(at[3:])))
    return int((today if today <= now else today - datetime.timedelta(days=1)).timestamp())


def lint(trackers, committing=False):
    """Ledger-integrity checks. Returns a list of human-readable violations.

    `committing`: the pre-commit run — the commit does not exist yet, so an answer being committed right now is
    *pending*, not refused; who committed it, and whether it verifies, is judged on the commit, by the next run. It is
    also the ONE run that may look at less: a version-control call per tracker cost the repository this tool was cut
    from 7.5 seconds in its hook, so the rules that need one are asked only of what this commit stages. `--check`
    asks them of everything."""
    global COMMITTING
    COMMITTING = committing
    problems = []
    ids = {t["id"] for t in trackers}
    if vcs() == "svn" and any(mode == "signed" for _who, mode in SEATS.values()):
        problems.append(f'{CONFIG_NAME}: `[seats]` — {", ".join(sorted(s for s in SEATS if SEATS[s][1] == "signed"))} asks for a signature, and '
                        f'Subversion has none to give: its server authenticates the commit. Name the SVN account alone')
    # Any repository carrying `answerers` hears this — NOT only one that also has `[seats]`. Guarding it on both was
    # backwards: it spoke to the repositories part-way through the migration and stayed silent for the ones wholly on
    # the old key, which is the entire population the deprecation is for (FM-010).
    if ANSWERERS and SEATS:
        # with `[seats]` the key is NOT READ for answers (`may_answer`, from 0.17.1): telling such a repository it "still
        # works" is what let a signature it asked for go unenforced without a word (FM-015)
        print(f'  note: {CONFIG_NAME}: `answerers` is the old name for the `answer` right, and here it is not read for answers — `[seats]` decides '
              f'who may answer and whether the answer is signed. It can be removed', file=sys.stderr)
    elif ANSWERERS:
        # The schedule is ANCHORED to 0.17.3, never phrased against "this release": this note prints unchanged in every
        # later release, and a floating "the clock starts here" would restart the countdown each time it was read.
        print(f'  note: {CONFIG_NAME}: `answerers` is the old name for the `answer` right and still works — move it into `[seats]` and `[rights]`. '
              f'It is removed no sooner than the release after 0.17.3: before 0.17.3 this note never reached a repository '
              f'without `[seats]`, so the clock starts at 0.17.3', file=sys.stderr)
    problems += answerers_problems()
    problems += rights_problems(trackers)
    problems += session_problems()                   # FM-024: a seat's commit names an open session of its own seat
    by_ask = asks_by_key(trackers)
    for t in trackers:
        # WHAT AN ASK MUST BE — the same rules the Owner's queue reads, refused here first (FM-008)
        problems += [f'{t["id"]}: {why}' for why in ask_problems(t, by_ask)]
        problems += record_problems(t) if committing else []
        if t.get("answer"):
            # the pre-mortem's rule: an answer counts only from the account it is filed from. Who that may be comes
            # from `may_answer()` — the seats that hold `answer`, or `answerers` where there are no seats
            allowed = may_answer()
            if not allowed:
                problems.append(f'{t["id"]}: an answer, but ' + (f'no seat in `[seats]` holds the `answer` right — give one `answer` in `[rights]`'
                                                                 if SEATS else f'`answerers` in {CONFIG_NAME} names nobody — say who may answer')
                                + ", then the commit's author is checked against it")
            elif not SEATS and t.get("answered_by") not in allowed:
                problems.append(f'{t["id"]}: `answered-by: {t.get("answered_by")}` is not in `answerers` ({", ".join(allowed)}) — an answer counts only from an account that may give one')
            else:
                who, email, how, commit = line_author(TRACKER_DIR / t["file"], "answer:")
                seat = seat_of(who, email) if SEATS else None
                if how == "uncommitted" and committing:
                    print(f'  {t["id"]}: the answer is being committed now — its author and signature are verified on the commit, by the next run', file=sys.stderr)
                elif how == "uncommitted":
                    problems.append(f'{t["id"]}: the answer is not committed yet — commit it under your own name; the commit is the record, the file is the label')
                elif SEATS and not holds(seat, "answer"):
                    problems.append(f'{t["id"]}: ' + no_seat(who, email, "answer", "an answer counts only from a seat that may give one"))
                elif who != t.get("answered_by"):
                    problems.append(f'{t["id"]}: `answered-by: {t.get("answered_by")}` but the {how} author of the answer is `{who}` — an answer is filed from the account that gives it')
                elif how == "git" and (SEATS[seat][1] if SEATS else allowed[who]) == "signed":
                    # ONE signature test for the whole gate — `verified_as`: a good signature under a trusted key, and
                    # the identity that key is trusted FOR being the one claimed. A seat's `signed` entry asks the same
                    if not verified_as(commit, email if SEATS else None):
                        problems.append(f'{t["id"]}: the answer\'s commit `{commit[:10]}` does not verify as `{email if SEATS else who}` — '
                                        f'{"`[seats]` asks this seat" if SEATS else "`answerers` asks"} for a signed answer, and a git author is only a string: '
                                        f'sign it (`git commit -S`), or it does not count')
                elif how == "git":
                    print(f'  note: {t["id"]}: the answer\'s author `{who}` is a git author string, not a verified identity — add `signed` to '
                          f'{"that seat in `[seats]`" if SEATS else "that entry in `answerers`"} to require a signature', file=sys.stderr)
        # `ask-proposal:` is the RECOMMENDED option, and the board offers it first: with options named, it must be one
        # of them, or the Owner is shown a recommendation he cannot pick
        if t.get("ask_proposal") and t.get("ask_options") and t["ask_proposal"] not in t["ask_options"]:
            problems.append(f'{t["id"]}: `ask-proposal:` recommends {t["ask_proposal"]!r}, which is not one of `ask-options:` '
                            f'({" | ".join(t["ask_options"])}) — the recommendation is one of the choices, written the same way')
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
    parser = argparse.ArgumentParser(prog=os.environ.get("SHOALMARK_CMD") or "shoalmark", description="A work tracker that lives in the repository it tracks.")
    add = parser.add_argument
    add("--root", metavar="DIR", help="the repository to track; default: the nearest shoalmark.toml or git toplevel above the working directory")
    add("--check", action="store_true",
        help=f"read-only gate: write nothing; exit {EXIT_DRIFT} if INDEX.md is stale, {EXIT_LINT} on a ledger-integrity violation")
    add("--print-written", action="store_true",
        help="write mode: print every file written, one repo-relative path per line on stdout, so a hook stages exactly that")
    add("--related", metavar="ID_OR_WORDS", help="before filing: the existing trackers closest to a tracker id or a quoted phrase. Read-only")
    add("--new", nargs="+", metavar="WORD",
        help="file ONE tracker — `--new \"the title\"`, `--new KEY \"the title\"`, or `--new KEY-037 \"the title\"` to take a free id of your choosing: "
             "prints what is related, writes the id with a front matter whose `considered:` is yours to fill; `<tracker dir>/TEMPLATE.md`, if there is one, is the template; "
             "the id prefix is needed only where the configuration names several")
    add("--tags", metavar="TAG,TAG", help="with --new: the kind of work, as it is filed — `--new KIND \"the title\" --tags bug,process` writes `tags:` into the new tracker; "
                                           "comma-separated, deduplicated, each from [tags] in the configuration. Under the filing freeze (`freeze_at`) only a `bug` filing is written")
    add("--triage", action="store_true",
        help="start or continue a triage pass: applies the verdicts filled in today's worksheet, rewrites it, prints the rules")
    add("--next", action="store_true", help="the cold-start question: what to work on, in order, and what is true now of each. Read-only")
    add("--schema", action="store_true", help="print the front-matter schema — every key, its shape, who writes it. Read-only")
    add("--html-only", action="store_true", help="write only the git-ignored board (index.html) and exit 0 — a post-merge hook cannot dirty the tree")
    add("--install-hook", action="store_true", help="wire the gate into the version control system found: plain git hooks (pre-commit, prepare-commit-msg, post-merge, post-checkout), or on Subversion the TortoiseSVN hook properties and svn:ignore; never overwrites a hook that is not its own")
    add("--standup", nargs="?", const="", metavar="FILE.ics", help="the Owner's one sitting: the agenda by kind — rulings, his hands, what evidence could settle, buttons — and inside a kind what frees the most first. With FILE.ics: the recurring calendar invite (weekdays at `standup` in the configuration)")
    add("--answer", nargs="+", metavar="WORD", help="the Owner's one command: `--answer <id> accept|reject [\"text\"]` — cuts answer/<id> from this branch, writes the three lines, commits signed, pushes, "
             "naming each step as it starts. A failure after it wrote anything undoes it all and prints the answer and the command to give it again")
    add("--supersede", action="store_true", help="with --answer, on a tracker he has answered already: the new answer replaces the old one, which moves into the ship log "
                                                 "with the commit that wrote it — `--answer <id> accept|reject \"<option>\" --supersede`; `--answer <id> revoke \"<reason>\"` takes an answer back the same way")
    add("--answered", action="store_true", help="what the Owner answered and no seat has acted on yet — the seat's side of the exchange; and what WAS acted on since his last sitting, by commit")
    add("--clear-ask", nargs="+", metavar="WORD",
        help="`--clear-ask <id> <next move>` — the answer has been acted on: moves the exchange into the body under `## Asks` (date · question · answer · answered-by), clears the ask and answer lines and sets the next move — the `ask` right's move under [seats]. The gate refuses an answer removed without its record")
    add("--owner", action="store_true", help="the digest: what needs the Owner — how many, how old, what each holds up, each as the question it is. What a session's last message leads with; "
                                            "where `gh` reads the forge, it ends with the queue of pull requests (--queue)")
    add("--queue", action="store_true", help="the open pull requests, read from GitHub with `gh` (origin fetched once), ONE action each — merge · closes with PR N · "
                                            "close: carried into PR N · wait: conflict in … · wait: no verdict on … · wait: NOT READY (…) — in the order to take them. "
                                            f"Read-only; exit {EXIT_DRIFT} where the forge cannot be read")
    add("--session", nargs="+", metavar="WORD",
        help="a seat's session (FM-024): a sub-agent derives its id from its parent's, `<parent>/<seat>-<n>`; `--session new` prints an id no row carries — for a session with no parent and a harness with no id; "
             "the worktree carries it as `git config --worktree seat.session <id>`, beside the seat's `user.email`. "
             "`--session open <id> <seat> \"<convened by>\" \"<scope>\" [<worktree>]` writes its row in <tracker dir>/sessions.md and stages it — "
             "a sub-agent's id is `<parent>/<seat>-<n>`; `--session close <id>` dates its end")
    add("--session-check", action="store_true", help="the session rule alone, on the commit being made — what the pre-commit hook runs on EVERY commit, "
                                                     "a tracker staged or not; reads git and the registry, never the trackers")
    add("--session-trailer", nargs="+", metavar="FILE", help="what a prepare-commit-msg hook calls with its message file: appends `Session: <seat.session>` "
                                                            "to a seat's commit — nothing without `seat.session`, nothing when the message carries one already")
    add("--tsvn-hook", nargs="+", metavar="start|pre", help=argparse.SUPPRESS)      # what the TortoiseSVN properties call; TortoiseSVN appends its own arguments
    add("--derive-flag", action="append", default=[], metavar="NAME",
        help="hand NAME to the repository's deriver as one of its `flags` — the ONLY way a deriver is told anything beyond the trackers: "
             "it must never read the environment, which a git hook inherits from whatever shell ran the commit")
    add("--brand", nargs="?", const="", metavar="DIR",
        help="why does my board look like this: which places gave it its theme, logo and labels. With DIR: write a commented starter there")
    add("--init", action="store_true", help="scaffold shoalmark.toml, the tracker directory and TRIAGE.md; never overwrites")
    add("--key", metavar="KEY", help="with --init: the project key every id carries — MSR gives MSR-001; default: the directory name's first word")
    add("--vendor", metavar="DIR", help="copy this tool into DIR with a PIN file of sha256 hashes — a pinned, self-contained copy. Only from a release: "
                                            "the whole tool, a git checkout whose HEAD is at the tag of its VERSION, a clean tree — otherwise refused, nothing written. "
                                            "The PIN's first line says where the copy came from; `--check` in the consumer reads it")
    add("--partial", action="store_true", help="with --vendor: copy what the source has although files are missing, and name them in the PIN")
    add("--allow-untagged", action="store_true", help="with --vendor: vendor from a working copy that is not at its release tag, or not clean — the PIN says `untagged <sha>`")
    add("--version", action="version", version=__version__)
    return parser.parse_args(argv)


DERIVED_COLUMNS = []          # the columns a deriver contributed on this run, in the order it named them
INDEX_COLUMNS, BOARD_COLUMNS = [], []   # which derived values are columns where — all of them, unless the deriver says (`_index`, `_board`)
DERIVED_NOTES = []            # paragraphs for INDEX.md's header: what its columns mean, what it could not derive
DERIVED_FILES = {}            # other files it wants generated: {repo-relative path: text} — the core writes, checks and stages them


def deriver_env():
    """The environment a deriver runs in: what a program needs to start and to find git — nothing else. A deriver's
    answer decides what a commit stages, so it must not depend on what happens to be exported in the shell that ran
    the commit: one stray variable once rewrote eighty cells and staged them, exit 0. It is told things in `flags`."""
    keep = ("PATH", "HOME", "LANG", "TMPDIR", "SYSTEMROOT", "PYTHONPATH", "VIRTUAL_ENV")
    return {k: v for k, v in os.environ.items() if k in keep or k.startswith("LC_")}


DERIVE_TIMEOUT = 60           # seconds — a deriver runs on every commit and every checkout; one that hangs must not hang the gate


def run_deriver(trackers, mode="write", flags=()):
    """B′ — the one seam. If `<tracker dir>/derive` exists and is executable it runs first, on EVERY run: nothing
    derived is stored, so nothing derived can be stale. stdin: every tracker's id, status, file and front matter.
    stdout: `{"<ID>": {"Column": "value"}, "_keys": {key: {shape, required, who, says}}, "_problems": ["…"]}`. Each
    value key becomes a column in INDEX.md and on the board, and a view on the board. `_files: {path: text}` are other
    generated files: the deriver stays free of side effects — the core writes them, reports them under --print-written
    and counts them as drift under --check. A non-zero exit REFUSES the run before anything is written.
    Returns (exit code or None, problems)."""
    global DERIVED_COLUMNS, DERIVED_FILES, DERIVED_NOTES, FRONT_MATTER, INDEX_COLUMNS, BOARD_COLUMNS
    DERIVED_COLUMNS, DERIVED_FILES, DERIVED_NOTES, FRONT_MATTER, INDEX_COLUMNS, BOARD_COLUMNS = [], {}, [], front_matter_schema(), [], []
    for t in trackers:
        t["x"], t["xd"], t["x_needs"] = {}, {}, []
    exe = TRACKER_DIR / "derive"
    if not (exe.is_file() and (os.name == "nt" or os.access(exe, os.X_OK))):
        return None, []
    # `mode` — write · check · board (the git-ignored page only: nothing the run produces can be committed) · read.
    # `flags` — what was typed as --derive-flag on THIS invocation. Both travel on stdin, never in the environment:
    # a hook inherits the environment of whatever shell ran `git commit`, and a stray export would reach every run.
    ask = json.dumps({"root": str(ROOT), "mode": mode, "flags": sorted(set(flags)), "trackers": [{"id": t["id"], "status": t["status"], "file": t["file"], "fm": t.get("fm", {})} for t in trackers]})
    try:
        # Windows has no executable bit and reads no `#!` line: there a deriver is run by this interpreter
        run = subprocess.run(([sys.executable] if os.name == "nt" else []) + [str(exe)], input=ask, capture_output=True, text=True, encoding="utf-8",
                             cwd=ROOT, env=deriver_env(), timeout=DERIVE_TIMEOUT)
    except subprocess.TimeoutExpired:
        return EXIT_LINT, [f"{exe.relative_to(ROOT).as_posix()} did not answer within {DERIVE_TIMEOUT} s — a deriver runs on every commit and every checkout; make it fast, or make it fail"]
    if run.returncode:
        print(run.stderr.rstrip() or f"{exe.relative_to(ROOT).as_posix()} exited {run.returncode}", file=sys.stderr)
        return run.returncode, []
    try:
        said = json.loads(run.stdout or "{}")
    except ValueError as e:
        return EXIT_LINT, [f"{exe.relative_to(ROOT).as_posix()}: its output is not JSON — {e}"]
    for key, spec in (said.get("_keys") or {}).items():
        if key in FRONT_MATTER:
            return EXIT_LINT, [f"{exe.relative_to(ROOT).as_posix()}: `_keys` may add a key, never redefine one — `{key}:` is the core's"]
        FRONT_MATTER[key] = (spec.get("shape") or None, spec.get("required") or False, spec.get("who", "the deriver's owner"), spec.get("says", ""))
    by_id = {t["id"]: t for t in trackers}
    for tid, values in said.items():
        if tid.startswith("_") or tid not in by_id or not isinstance(values, dict):
            continue
        # a value may be a pair — [value, how it is shown on the board]: the value groups, sorts, searches and is what
        # INDEX.md prints; the display form is only for the board's cells (`→ 0.16.x`, `0.16.4 ✓`)
        by_id[tid]["x_needs"] = [str(n) for n in values.pop("_needs", None) or []]      # what open work is missing, in the deriver's terms
        by_id[tid]["x"] = {str(k): str(v[0] if isinstance(v, list) and v else v) for k, v in values.items()}
        by_id[tid]["xd"] = {str(k): str(v[1]) for k, v in values.items() if isinstance(v, list) and len(v) > 1 and str(v[1]) != str(v[0])}
        DERIVED_COLUMNS += [k for k in by_id[tid]["x"] if k not in DERIVED_COLUMNS]
    DERIVED_NOTES = [str(n) for n in said.get("_notes") or []]
    # one model, two renderings: INDEX.md is what an agent reads, the board what the Owner reads, and they may want
    # different columns. Every derived value stays a view, a fact and a search word on the board either way.
    INDEX_COLUMNS = [c for c in (said.get("_index") or DERIVED_COLUMNS) if c in DERIVED_COLUMNS]
    BOARD_COLUMNS = [c for c in (said.get("_board") or DERIVED_COLUMNS) if c in DERIVED_COLUMNS]
    for rel, text in (said.get("_files") or {}).items():
        path = (ROOT / rel).resolve()
        if ROOT not in path.parents:
            return EXIT_LINT, [f"{exe.relative_to(ROOT).as_posix()}: `_files` names {rel} — outside the repository"]
        DERIVED_FILES[path] = str(text)
    return None, [str(p) for p in said.get("_problems") or []]


def load_trackers():
    return mark_blocked([extract(p) for p in sorted(TRACKER_DIR.glob("*.md")) if KIND_RE.match(p.name)])


TOOL_FILES = ("shoalmark.py", "vendor/marked-18.0.13.umd.js", "VERSION", "NOTICE", "LICENSE-APACHE", "LICENSE-MIT", "CHANGELOG.md", "README.md")   # the README is written for the agent that uses the copy


def pin_problems():
    """A vendored copy carries a PIN — `sha256  path` per file. A copy that was edited in place is refused by the
    gate: fix it upstream and vendor again, so two repositories never run two tools under one name."""
    pin = HERE / "PIN"
    here = str(HERE.relative_to(ROOT).as_posix()) if ROOT in HERE.parents else str(HERE)
    if not pin.exists():
        # the tool sitting INSIDE the repository it tracks, and not at its root, is a vendored copy — and a vendored
        # copy without its PIN has had its integrity check switched off, silently
        return [f"{here}/PIN is missing — a vendored shoalmark carries its PIN; vendor again with --vendor"] if ROOT in HERE.parents else []
    out = []
    for line in pin.read_text(encoding="utf-8").splitlines():
        if line.startswith("#"):                            # the manifest: where the copy came from (FM-011)
            continue
        want, _, rel = line.partition("  ")
        if rel and (not (HERE / rel).exists() or digest(HERE / rel) != want):
            out.append(f"{here}/{rel}: differs from its PIN — a vendored shoalmark is not edited in place; change it upstream and run --vendor again")
    return out


def changes_since(version):
    """The CHANGELOG sections newer than `version` — what a consumer takes on by vendoring again."""
    log = HERE / "CHANGELOG.md"
    text = log.read_text(encoding="utf-8") if log.exists() else ""
    parts = re.split(r"^## ", text, flags=re.M)[1:]
    key = lambda v: tuple(int(x) for x in re.findall(r"\d+", v)[:3])
    return "".join("## " + p for p in parts if re.match(r"\d", p) and key(p.split()[0]) > key(version)).strip()


def source_provenance():
    """Where this copy of the tool comes from, as a vendoring vouches for it (FM-011): (the tag, the commit, the dirty
    paths, why it is no release — "" when it is one). A release is a git checkout whose HEAD is exactly at `v<VERSION>`,
    with a clean tree: a consumer runs a release, never a working copy."""
    top = git_out("rev-parse", "--show-toplevel", cwd=HERE)
    if top is None:
        return "", "", [], f"{HERE} is not a git checkout — a release is vendored from a clone at its tag"
    sha = (git_out("rev-parse", "HEAD", cwd=HERE) or "").strip()
    tags = (git_out("tag", "--points-at", "HEAD", cwd=HERE) or "").split()
    dirty = [l[3:] for l in (git_out("status", "--porcelain", "--untracked-files=all", cwd=HERE) or "").splitlines() if l.strip()]
    want = f"v{__version__}"
    why = "; ".join(([f"HEAD {sha[:10]} is not at the tag {want}" + (f" (it carries {', '.join(tags)})" if tags else "")] if want not in tags else [])
                    + ([f"the tree has changes: {', '.join(dirty[:8])}" + (" …" if len(dirty) > 8 else "")] if dirty else []))
    return (want if want in tags else ""), sha, dirty, why


# The manifest `--vendor` writes as a PIN's first line — the only form `--check` accepts (FM-011, R1)
MANIFEST_RE = re.compile(r"# shoalmark (\d+\.\d+\.\d+) · (?:tag v(\d+\.\d+\.\d+) · commit ([0-9a-f]{7,40})|untagged ([0-9a-f]{7,40}|\(no git\))( \(dirty\))?)"
                         r" · vendored (\d{4}-\d\d-\d\d) · (complete|partial)")


def pin_manifest(pin_text, pinned_version):
    """The PIN's manifest, checked: (the manifest, "") when its first line is exactly what `--vendor` writes and agrees
    with itself and with the pinned `VERSION`; ({}, what is wrong) otherwise; ({}, "") for a PIN with no manifest (one
    vendored before 0.17.8). Nothing in it is believed that was not checked."""
    lines = pin_text.splitlines()
    first = lines[0] if lines else ""
    if not first.startswith("#"):
        return {}, ""
    m = MANIFEST_RE.fullmatch(first)
    if not m:
        later = any(MANIFEST_RE.fullmatch(l) for l in lines[1:])
        return {}, "is not the PIN's first line" if later else "is not the line --vendor writes"
    version, tag, commit, untagged, dirty, date, state = m.groups()
    try:
        datetime.date.fromisoformat(date)
    except ValueError:
        return {}, "is not the line --vendor writes (its date is no date)"
    if tag and tag != version:
        return {}, f"names the tag v{tag} for the version {version}"
    if version != pinned_version:
        return {}, f"says {version}, and the pinned VERSION is {pinned_version or '(missing)'}"
    missing = lines[1][len("# missing: "):].split(", ") if state == "partial" and len(lines) > 1 and lines[1].startswith("# missing: ") else None
    if state == "partial" and not missing:
        return {}, "says partial and names nothing missing"
    return {"version": version, "tag": tag, "commit": commit, "untagged": (untagged or "") + (dirty or ""), "vendored": date,
            "partial": state == "partial", "missing": missing or []}, ""


def pin_report():
    """What `--check` says of a vendored copy's PIN manifest: where it came from, only once checked — a warning when it
    was no release or is partial, and one naming what is wrong when the manifest is not what `--vendor` wrote."""
    pin = HERE / "PIN"
    if not pin.exists() or ROOT not in HERE.parents:
        return []
    pinned = (HERE / "VERSION").read_text(encoding="utf-8").strip() if (HERE / "VERSION").exists() else ""
    m, wrong = pin_manifest(pin.read_text(encoding="utf-8"), pinned)
    if wrong:
        return [f"warning: the PIN's manifest {wrong} — this copy is unverified; vendor again from a release"]
    if not m:
        return ["no manifest — pinned before 0.17.8; where the copy came from is not recorded"]
    source = f"tag v{m['tag']} (commit {m['commit'][:10]})" if m["tag"] else f"untagged {m['untagged']}"
    lines = [f"pinned {m['version']} from {source}, vendored {m['vendored']}, {'partial' if m['partial'] else 'complete'}"]
    if not m["tag"]:
        lines.append("warning: this copy was vendored from a working copy, not a release — vendor again from a clone at a tag")
    if m["partial"]:
        lines.append(f"warning: this copy is partial — missing {', '.join(m['missing'])}")
    return lines


def vendor(dest, partial=False, allow_untagged=False):
    """Copy this tool into `dest` and pin every file (FM-011). Refused — exit 4, nothing written — when the source is
    not the whole tool (`TOOL_FILES`; `--partial` copies what there is and says so in the PIN), when it is no release
    (HEAD exactly at the tag of its `VERSION`, a clean tree; `--allow-untagged` vendors it and says so), or when the copy
    in `dest` was edited in place. The PIN's first line is the manifest: version, tag, commit, date, complete|partial."""
    dest = pathlib.Path(dest).resolve()
    had = (dest / "VERSION").read_text(encoding="utf-8").strip() if (dest / "VERSION").exists() else ""
    edited = [l.partition("  ")[2] for l in ((dest / "PIN").read_text(encoding="utf-8").splitlines() if (dest / "PIN").exists() else [])
              if not l.startswith("#") and l.partition("  ")[2] and (dest / l.partition("  ")[2]).exists()
              and digest(dest / l.partition("  ")[2]) != l.partition("  ")[0]]
    if edited:
        print(f"--vendor: {', '.join(edited)} in {dest} was edited in place — its changes would be lost. Move them upstream first, or delete the copy.", file=sys.stderr)
        return EXIT_LINT
    missing = [rel for rel in TOOL_FILES if not (HERE / rel).is_file()]
    if missing and not partial:
        print(f"--vendor: {HERE} is not the whole tool — missing {', '.join(missing)}. Vendor from a clone at a release tag; "
              f"nothing was written. (`--partial` copies what there is and names the rest in the PIN.)", file=sys.stderr)
        return EXIT_LINT
    tag, sha, dirty, why = source_provenance()
    if why and not allow_untagged:
        print(f"--vendor: {why}. A consumer runs a release, never a working copy: check out v{__version__} in a clean clone "
              f"and vendor from there; nothing was written. (`--allow-untagged` vendors it anyway and says so in the PIN.)", file=sys.stderr)
        return EXIT_LINT
    lines = []
    for rel in TOOL_FILES + tuple(f"brand/{n}" for n in BRAND_FILES):
        src = HERE / rel
        if not src.is_file():
            continue
        (dest / rel).parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(src, dest / rel)
        lines.append(f"{digest(src)}  {rel}")
    source = (f"tag {tag} · commit {sha}" if tag else f"untagged {sha[:10] or '(no git)'}" + (" (dirty)" if dirty else ""))
    head = [f"# shoalmark {__version__} · {source} · vendored {datetime.date.today().isoformat()} · {'partial' if missing else 'complete'}"]
    head += [f"# missing: {', '.join(missing)}"] if missing else []
    put((dest / "PIN"), "\n".join(head + lines) + "\n")
    print(f"vendored shoalmark {__version__} from {'tag ' + tag if tag else 'an untagged source, ' + (sha[:10] or 'no git')} into {dest} — {len(lines)} files, pinned in PIN"
          + (f" (was {had})" if had and had != __version__ else "") + (f" — PARTIAL: missing {', '.join(missing)}" if missing else ""))
    if had and had != __version__ and changes_since(had):
        print("\nWhat changes for this repository:\n\n" + changes_since(had))
    return EXIT_OK


# The scaffold's own words under the intent heading. `--init` writes the English ones; examples/de/TRIAGE.md holds the
# German ones; the bare lines are the scaffold before 0.17.5. `owners_intent()` leaves out exactly these texts and reads
# everything else there as the Owner's (R11) — so the scaffold and the reader can never disagree on what is whose.
INTENT_NOTE = "*The Owner's own words — for · so that · never. Nobody else edits this. A pass prints it above its rules.*"
INTENT_LEAD = """*Three lines in your own words about the repository as a whole, never one feature of it: what this repository, all of
it, is for · what is true when it works · what no pass or seat may do to get there. The example is a whole product;
overwrite it — a pass reads everything you write here and leaves out only this lead-in and the examples as they stand.*"""
INTENT_EXAMPLES = (
    "- **for** — *e.g. a village library's lending, all of it: members, loans, returns and the shelf in one record the librarian trusts*",
    "- **so that** — *e.g. a member finds a book and a librarian finds a member in one look, and nothing on loan is lost*",
    "- **never** — *e.g. lend what the catalogue does not hold, or drop a member's record before their last loan is back*",
)
INTENT_NOTE_DE = "*Die eigenen Worte des Owners — für · damit · niemals. Niemand sonst ändert das. Eine Sichtung druckt es über ihre Regeln.*"
INTENT_LEAD_DE = """*Drei Zeilen in Ihren eigenen Worten über das Repository als Ganzes, nie über ein einzelnes Feature: wofür dieses
Repository, all das, da ist · was gilt, wenn es funktioniert · was keine Sichtung und kein Agent tun darf, um dorthin zu
kommen. Das Beispiel ist ein ganzes Produkt; überschreiben Sie es — eine Sichtung liest alles, was Sie hier schreiben, und
lässt nur diese Einleitung und die unveränderten Beispiele aus.*"""
INTENT_EXAMPLES_DE = (
    "- **für** — *z. B. die ganze Ausleihe einer Dorfbücherei: Mitglieder, Ausleihen, Rückgaben und das Regal in einem Bestand, dem die Bibliothekarin traut*",
    "- **damit** — *z. B. ein Mitglied ein Buch und die Bibliothekarin ein Mitglied mit einem Blick findet, und nichts Verliehenes verloren geht*",
    "- **niemals** — *z. B. verleihen, was der Katalog nicht führt, oder die Akte eines Mitglieds löschen, bevor seine letzte Ausleihe zurück ist*",
)
INTENT_SCAFFOLD = (INTENT_NOTE, INTENT_LEAD, *INTENT_EXAMPLES, "- **for** —", "- **so that** —", "- **never** —",
                   INTENT_NOTE_DE, INTENT_LEAD_DE, *INTENT_EXAMPLES_DE, "- **für** —", "- **damit** —", "- **niemals** —")

TRIAGE_HOME = """\
# Triage

The home of the recurring triage pass: `{cmd} --triage`. The command prints the rules and the two sections
below; its worksheets are the record, in `evidence/triage/`.

## {intent}

""" + INTENT_NOTE + "\n\n" + INTENT_LEAD + "\n\n" + "\n".join(INTENT_EXAMPLES) + """

## {path}

*The Owner's. A pass judges every tier against it; only the Owner changes it.*

1.

## {passes}

Newest first — one paragraph per pass: its date, what it changed, its worksheet.

*None yet.*
"""

CONTRACT_BEGIN = "<!-- BEGIN shoalmark: the work-tracker contract — regenerated by --init, edit outside these markers -->"
CONTRACT_END = "<!-- END shoalmark -->"
GATE_SAYS = {"svn": "checked by a gate: **run `{cmd}` before every `svn commit`** and commit the `INDEX.md` it writes — Subversion's\ncommand line has no client-side hook (TortoiseSVN runs the gate itself, once `--install-hook` has set its properties)",
             "": "checked by a gate on every\ncommit"}
LEGACY_CONTRACT = ("<!-- BEGIN fathom-mark:", "<!-- END fathom-mark -->")      # the name until 0.6.0
CONTRACT = """\
## The work tracker — read this before you change anything

Work in this repository is tracked in `{dir}/` — one Markdown file per work item, {gate}.
**Start here:** `{cmd} --next` says what to work on and what is true now.

1. **The tracker is canonical.** The spec, the state and the record of a piece of work live in its tracker —
   never in a side plan, a chat or a TODO comment. Its *{state}* section is rewritten in place when
   the truth changes; only the ship log is append-only.
2. **Look before you file.** `{cmd} --new "what is wrong, in a sentence"` prints the closest trackers first.
   The default is a slice of one that exists. A new tracker names what it was held against in `considered:` —
   the gate refuses it otherwise.
3. **An id never changes and says nothing that can.** `{key}-012` — the kind of work is a tag (`tags: bug`),
   a story is a field (`epic: {key}-003`). Branches carry the id: `feat/{lkey}-012-slug`, `fix/{lkey}-013-slug`.
4. **The seat judges, the command applies.** `triaged:` `tier:` `rank:` and a park are written by
   `{cmd} --triage` from the worksheet you fill — never by hand. `{cmd} --schema` lists every key and who writes it.
5. **When you stop, leave the fix for the next session:** what is left, in *{state}*; the next move, in
   `next:` — review · run · wait · owner · script · build. The next session starts cold.
6. **Close out by asking what this made obsolete — and delete it in the same change.** Done means finished
   *and simpler afterwards*, not wider. A defect found on the way gets one line in the tracker, or its own
   tracker if it is real work — not a bundled side-fix.
7. **What you need from the Owner is an `ask:`** — ONE sentence he can answer, with `ask-kind:` (ruling · action ·
   determination · ceremony), `ask-since:` and `next: owner`. Write it before his standup; never bury it in the body.
   He has office hours, you have a budget: **end a session's last message with `{cmd} --owner`.**
8. **`{dir}/TRIAGE.md` is the Owner's**: the intent and the current path. Nobody else edits those two sections.
   `INDEX.md` is generated — never hand-edit it. A story stays open while a chapter is.
"""

CONFIG_TEMPLATE = """\
# shoalmark — every key is optional; these are the defaults.
name = "{name}"
tracker_dir = "docs/work-tracker"
blob = ""            # URL prefix of a tracker file on the forge, e.g. https://github.com/me/repo/blob/main/docs/work-tracker/
triage_days = 7

[kinds]              # id prefix = the INDEX section it is listed under. One id space, keyed by the project:
{key} = "Work"       # an id encodes nothing that can change — the kind of work is a tag, a story is `epic:`

[tags]               # a closed vocabulary: a synonym is how tags rot
bug = "something that worked, or was meant to, and does not"
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

## {state}

**Filed {today}; nothing is built.**

## {why}

## {done}

## {log}

| Date | Event |
|---|---|
| {today} | Filed. |
"""


HOOK_MARK = "# shoalmark"
LEGACY_HOOK_MARK = "# fathom-mark"          # the name until 0.6.0 — a hook it wrote is still ours to rewrite
HOOKS = {
    "pre-commit": """#!/bin/sh
{mark} — regenerate and stage INDEX.md when a tracker changed; a violation refuses the commit
{cmd} --session-check || exit $?
if git diff --cached --name-only | grep -q -E '^({dir}/.*\\.md|{config}|{tool}/)'; then
  written=$({cmd} --print-written) || exit $?
  printf '%s\\n' "$written" | git add --pathspec-from-file=-
fi
""",
    "prepare-commit-msg": "#!/bin/sh\n{mark} — a seat's commit names its session: `Session: <seat.session>` (FM-024)\n{cmd} --session-trailer \"$1\" \"$2\"\n",
    "post-merge": "#!/bin/sh\n{mark} — refresh the git-ignored board\n{cmd} --html-only || true\n",
    "post-checkout": "#!/bin/sh\n{mark} — refresh the git-ignored board\n{cmd} --html-only || true\n",
}


HOOK_LINES = {"pre-commit": "--print-written", "prepare-commit-msg": '--session-trailer "$1"'}     # the one line a hook that is not ours needs
TSVN_HOOKS = {"tsvn:startcommithook": "start", "tsvn:precommithook": "pre"}


def svn_ignore_board():
    """Subversion ignores by a property on the directory, and only a versioned directory can carry one: the tracker
    directory is scheduled for addition if it is not yet (nothing is committed), so the FIRST `svn add` of its
    contents already leaves the board out."""
    svn = lambda *a: subprocess.run(["svn", *a], capture_output=True, text=True, encoding="utf-8", errors="replace", cwd=ROOT)
    rel = TRACKER_DIR.relative_to(ROOT).as_posix()
    TRACKER_DIR.mkdir(parents=True, exist_ok=True)
    if svn("info", rel).returncode:                         # not versioned yet
        if svn("add", "--parents", "--depth=empty", rel).returncode:
            print(f"could not `svn add {rel}` — add it, then run --install-hook for svn:ignore", file=sys.stderr)
            return EXIT_LINT
    lines = svn("propget", "svn:ignore", rel).stdout.split()        # an unset property is an error to svn, and empty to us
    if not {"index.html", "view"} <= set(lines):
        svn("propset", "svn:ignore", "\n".join(dict.fromkeys(lines + ["index.html", "view"])) + "\n", rel)
        print(f"set svn:ignore on {rel}/ — the board is never committed")
    return EXIT_OK


def install_hook_svn():
    """What Subversion has. Its command line runs NO client-side hook; TortoiseSVN does, from versioned properties,
    after asking the user once. The board is ignored by property, not by file."""
    svn = lambda *a: subprocess.run(["svn", *a], capture_output=True, text=True, encoding="utf-8", errors="replace", cwd=ROOT)
    url = svn("info", "--show-item", "relative-url", ".")
    if url.returncode:
        print(f"--install-hook: `svn info` failed in {ROOT} — {url.stderr.strip() or 'is svn on the PATH?'}", file=sys.stderr)
        return EXIT_LINT
    here = pathlib.Path(__file__).resolve()
    tool = here.relative_to(ROOT).as_posix() if ROOT in here.parents else "tools/shoalmark/shoalmark.py"
    base = "%REPOROOT%" + url.stdout.strip().lstrip("^").rstrip("/")
    code = EXIT_OK
    for prop, kind in TSVN_HOOKS.items():
        # four lines: the command · wait for it · hide its window. TortoiseSVN is Windows: the interpreter is `python`
        value = f"python {base}/{tool} --tsvn-hook {kind}\ntrue\nhide\n"
        have = svn("propget", prop, ".").stdout
        if have.strip() and "--tsvn-hook" not in have:
            print(f"{prop} is set and is not shoalmark's — left alone. Add to it: `python {base}/{tool} --tsvn-hook {kind}`", file=sys.stderr)
            code = EXIT_LINT
            continue
        if have.strip() != value.strip():
            svn("propset", prop, value, ".")
            print(f"set {prop} on {ROOT.name}/ — TortoiseSVN asks once before it runs it")
    code = svn_ignore_board() or code
    print(f"Commit the property changes (`svn update` first if Subversion calls the directory out of date). `svn commit` on the command line runs no hook — Subversion has none on the client: "
          f"run `{CMD}` before it and commit the INDEX.md it writes (the contract in AGENTS.md says so). "
          f"For a gate nobody can skip, call `{CMD} --check` from the server's pre-commit hook.")
    return code


def install_hook():
    """Plain git hooks — a repository that vendors shoalmark needs Python and nothing else. A hook that is not
    ours is never overwritten: it is named, with the line to add to it."""
    if vcs() == "svn":
        return install_hook_svn()
    out = subprocess.run(["git", "-C", str(ROOT), "rev-parse", "--git-path", "hooks"], capture_output=True, text=True, encoding="utf-8", errors="replace", env=nested_git_env())
    if out.returncode:
        print(f"--install-hook: {ROOT} is neither a git repository nor a Subversion working copy", file=sys.stderr)
        return EXIT_LINT
    hooks = (ROOT / out.stdout.strip()).resolve()
    hooks.mkdir(parents=True, exist_ok=True)
    fill = dict(mark=HOOK_MARK, cmd=CMD, dir=TRACKER_DIR.relative_to(ROOT).as_posix(), config=CONFIG_NAME,
                tool=pathlib.Path(__file__).resolve().parent.relative_to(ROOT).as_posix() if ROOT in pathlib.Path(__file__).resolve().parents else "tools/shoalmark")
    code = EXIT_OK
    for name, text in HOOKS.items():
        path = hooks / name
        if path.exists() and not any(m in path.read_text(encoding="utf-8", errors="replace") for m in (HOOK_MARK, LEGACY_HOOK_MARK)):
            print(f"{path} exists and is not shoalmark's — left alone. Add to it: `{CMD} {HOOK_LINES.get(name, '--html-only')}`", file=sys.stderr)
            code = EXIT_LINT
            continue
        put(path, text.format(**fill))
        path.chmod(0o755)
        print(f"wrote {path}")
    return code


def init(key=None):
    wrote = []
    key = (key or re.split(r"[^A-Za-z0-9]+", ROOT.name.strip("._-"))[0][:5] or "WORK").upper()
    if not re.fullmatch(r"[A-Z][A-Z0-9]*", key):
        print(f"--key: {key!r} is not an id prefix — letters and digits, starting with a letter", file=sys.stderr)
        return EXIT_LINT
    fresh_config = not (ROOT / CONFIG_NAME).exists()
    for path, text in ((ROOT / CONFIG_NAME, CONFIG_TEMPLATE.format(name=ROOT.name, key=key)),
                       (TRACKER_DIR / "TRIAGE.md", TRIAGE_HOME.format(cmd=CMD, **HEAD))):
        if not path.exists():
            path.parent.mkdir(parents=True, exist_ok=True)
            put(path, text)
            wrote.append(path)
    if fresh_config:
        configure(ROOT)
    section = CONTRACT_BEGIN + "\n" + CONTRACT.format(dir=TRACKER_DIR.relative_to(ROOT).as_posix(), gate=GATE_SAYS.get(vcs(), GATE_SAYS[""]).format(cmd=CMD), state=HEAD["state"], cmd=CMD, key=KINDS[0], lkey=KINDS[0].lower()) + CONTRACT_END + "\n"
    agents = ROOT / "AGENTS.md"
    have = agents.read_text(encoding="utf-8") if agents.exists() else ""
    if LEGACY_CONTRACT[0] in have and LEGACY_CONTRACT[1] in have:        # the block an older copy wrote, under the old name
        a = have.index(LEGACY_CONTRACT[0]); have = have[:a] + have[have.index(LEGACY_CONTRACT[1]) + len(LEGACY_CONTRACT[1]):].lstrip("\n")
    if CONTRACT_BEGIN in have and CONTRACT_END in have:
        new = have[:have.index(CONTRACT_BEGIN)] + section + have[have.index(CONTRACT_END) + len(CONTRACT_END):].lstrip("\n")
    else:
        new = (have.rstrip("\n") + "\n\n" if have.strip() else f"# {CONFIG['name'] or ROOT.name} — for agents\n\n") + section
    if new != have:
        put(agents, new)
        wrote.append(agents)
    claude = ROOT / "CLAUDE.md"
    if not claude.exists():                                 # Claude Code reads CLAUDE.md, not AGENTS.md — a router, never a second copy
        put(claude, "# CLAUDE.md\n\nThe contract for agents in this repository is [`AGENTS.md`](AGENTS.md) — read it first. This file owns no rules.\n")
        wrote.append(claude)
    ignore, rel = ROOT / ".gitignore", TRACKER_DIR.relative_to(ROOT).as_posix()
    have = ignore.read_text(encoding="utf-8") if ignore.exists() else ""
    lines = [l for l in (f"{rel}/index.html", f"{rel}/view/") if l not in have.splitlines()]
    if vcs() == "svn":                                      # Subversion ignores by property, not by file
        svn_ignore_board()
    elif lines and (vcs() == "git" or ignore.exists()):     # no version control here (yet): nothing to ignore for
        put(ignore, have + ("" if have.endswith("\n") or not have else "\n") + "\n".join(lines) + "\n")
        wrote.append(ignore)
    print("\n".join([f"wrote {p.relative_to(ROOT).as_posix()}" for p in wrote] or ["nothing to write — already initialised"]))
    print(f"next: the Owner writes the intent and the current path in {(TRACKER_DIR / 'TRIAGE.md').relative_to(ROOT).as_posix()}; "
          f"file the first tracker with `{CMD} --new \"…\"` — it becomes {KINDS[0]}-001; branches carry the id: `feat/{KINDS[0].lower()}-001-slug`; `{CMD} --install-hook` wires the commit gate; a seat's worktree carries two settings: "
          f"`git config --worktree user.email <seat>` (who may) and `git config --worktree seat.session <id>` (which run — `{CMD} --session new` prints one)")
    return EXIT_OK


_TRANSLIT = str.maketrans({"ä": "ae", "ö": "oe", "ü": "ue", "ß": "ss", "é": "e", "è": "e", "ê": "e", "á": "a", "à": "a", "â": "a",
                            "ó": "o", "ò": "o", "ô": "o", "ú": "u", "ù": "u", "û": "u", "í": "i", "î": "i", "ç": "c", "ñ": "n", "å": "a", "ø": "o", "æ": "ae"})


def slug_of(title, limit=60):
    """The filename's slug: lower case, ASCII, cut at a word — never mid-word, never ending in a dash."""
    slug = re.sub(r"[^a-z0-9]+", "-", title.lower().translate(_TRANSLIT)).strip("-")
    return slug if len(slug) <= limit else slug[:limit + 1].rsplit("-", 1)[0].strip("-")


def next_up(trackers):
    """What a cold session asks first: what do I work on, and what is true now. The ranked work in order, each
    with its next move and the opening of its *What is true now*; what waits on the Owner is said, not hidden."""
    home, by_id = triage_home(), {t["id"]: t for t in trackers}
    ranked = sorted((t for t in trackers if t.get("rank") and t["status"] in OPEN_STATUSES), key=lambda t: t["rank"])
    print("THE CURRENT PATH — " + str((TRACKER_DIR / "TRIAGE.md").relative_to(ROOT).as_posix()))
    print(strip_md(re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", home["path"])) or "  none is written — the Owner names it; until then nothing can be ranked")
    if not ranked:
        # no pass has run yet — a cold session still gets an answer: what is open, whose move each is, and what is
        # true now. A pass ADDS the order; it is not the price of being told anything.
        owed = [t for t in trackers if board(t) == "triage"]
        print(f"\nNothing is ranked. {len(owed)} tracker(s) wait for a triage pass — `{CMD} --triage`." if owed else "\nNothing is ranked, and nothing waits for a pass.")
        live = sorted((t for t in trackers if t["status"] in OPEN_STATUSES and t["status"] != "Parked"), key=lambda t: (t["status"] != "In Progress", t["id"]))
        if live:
            print("\nOPEN, UNRANKED — work in progress first:")
        for t in live[:15]:
            needs = ", ".join(needs_of(t, by_id))
            print(f"\n{t['id']} · {t['status']} · next: {t.get('next') or '—'}" + (f" · blocked by {', '.join(t['blocked_now'])}" if t.get("blocked_now") else "")
                  + (f" · needs {needs}" if needs else "") + f"\n   {t['title']} — {t['file']}\n   {t.get('state') or '(no *' + HEAD['state'] + '* — open the tracker, and leave one when you stop)'}")
        if len(live) > 15:
            print(f"\n… and {len(live) - 15} more — {OUT.relative_to(ROOT).as_posix()} lists them all.")
        print()
        owner_digest(trackers)
        return EXIT_OK
    mine = [t for t in ranked if t.get("next") not in ("owner", "wait")]
    for t in ranked:
        needs = ", ".join(needs_of(t, by_id))
        print(f"\n#{t['rank']} {t['id']} · {t['tier']} · next: {t.get('next') or '—'}" + (f" · blocked by {', '.join(t['blocked_now'])}" if t.get("blocked_now") else "")
              + (f" · needs {needs}" if needs else "") + f"\n   {t['title']} — {t['file']}\n   {t.get('state') or '(no *What is true now* — open the tracker, and leave one when you stop)'}")
    print(f"\nSTART WITH: {mine[0]['id']}" if mine else "\nEvery ranked move is the Owner's or waits — nothing here is yours to start.")
    print()
    owner_digest(trackers)
    return EXIT_OK


WANTED_NUM = None


def filing_freeze(trackers):
    """FM-032 S4 — (open, the line) while the filing freeze holds: the trackers whose status is open number `freeze_at` or
    more. None while they do not, or where `freeze_at` is 0."""
    n = sum(t["status"] in OPEN_STATUSES for t in trackers)
    return (n, FREEZE_AT) if FREEZE_AT and n >= FREEZE_AT else None


def new_tracker(words, trackers, tags_arg=None):
    global WANTED_NUM
    m = re.fullmatch(r"([A-Za-z][A-Za-z0-9]*)-(\d+)", words[0]) if len(words) > 1 else None
    WANTED_NUM, words = (int(m.group(2)), [m.group(1), *words[1:]]) if m and m.group(1).upper() in KINDS else (None, words)
    kind, title = (words[0].upper(), " ".join(words[1:])) if len(words) > 1 and words[0].upper() in KINDS else (KINDS[0] if len(KINDS) == 1 else "", " ".join(words))
    if not kind and len(words) > 1:
        kind, title = words[0].upper(), " ".join(words[1:])
    if kind not in KINDS:
        print(f"--new: {kind or 'no id prefix given'} — this repository files under {', '.join(KINDS)} ({CONFIG_NAME}, [kinds]); say which", file=sys.stderr)
        return EXIT_LINT
    near = related_trackers(trackers, title, limit=5)
    print("A filing looks first — the closest trackers that exist. Where one of them already owns this, make it a slice of that one:" if near
          else "Nothing related is filed yet.")
    for score, t in near:
        print(f'{score:7.1f}  {t["id"]:<9} {t["status"]:<12} {t["title"][:60]}')
    house = TRACKER_DIR / "TEMPLATE.md"                     # a repository's own template, by convention — its language, its sections
    template = house.read_text(encoding="utf-8") if house.is_file() else TRACKER_TEMPLATE
    frozen = filing_freeze(trackers)
    tags = [x.strip().lstrip("#").lower() for x in (parse_frontmatter(template)[0].get("tags") or "").split(",") if x.strip()]
    if tags_arg is not None:                                # `--tags bug,process`: the kind of work, said as it is filed
        tags = list(dict.fromkeys(x.strip().lstrip("#") for x in tags_arg.split(",") if x.strip()))
        unknown = [x for x in tags if TAGS and x not in TAGS]
        if not tags or unknown or len(tags) > MAX_TAGS:
            print(f"--new: --tags {tags_arg!r} — " + (f"{', '.join(unknown)} not in the vocabulary ({', '.join(sorted(TAGS))}, [tags] in {CONFIG_NAME})" if unknown
                  else f"at most {MAX_TAGS} tags, from [tags] in {CONFIG_NAME}") + " — nothing was written", file=sys.stderr)
            return EXIT_LINT
    if frozen and "bug" not in tags:
        print(f"--new: filing freeze — {frozen[0]} open, at or above {frozen[1]} (`freeze_at` in {CONFIG_NAME}): only product defects are filed; "
              f"anything else goes as one line into the closest open tracker's body, or waits. This filing carries no `bug` tag — a product defect is filed with `--tags bug`; nothing was written", file=sys.stderr)
        return EXIT_LINT
    # a repository that already numbers its work keeps its numbers: `--new AP-037 "title"` takes that id if it is free
    num = max([t["num"] for t in trackers if t["kind"] == kind] or [0]) + 1
    if WANTED_NUM is not None:
        if any(t["kind"] == kind and t["num"] == WANTED_NUM for t in trackers):
            print(f"--new: {kind}-{WANTED_NUM:03d} exists — an id is never reused", file=sys.stderr)
            return EXIT_LINT
        num = WANTED_NUM
    tid = f"{kind}-{num:03d}"
    slug = slug_of(title)
    path = TRACKER_DIR / f"{tid}-{slug}.md"
    TRACKER_DIR.mkdir(parents=True, exist_ok=True)
    text = template.format(id=tid, title=title.replace('"', "'"), today=datetime.date.today().isoformat(), **HEAD)
    put(path, set_front(text, "tags", ", ".join(tags)) if tags_arg is not None else text)
    print(f"wrote {path.relative_to(ROOT).as_posix()} — fill `considered:` with the ids you held it against, or `none`; the gate refuses it until then")
    return EXIT_OK


def main(argv=None):
    for stream in (sys.stdout, sys.stderr):                 # a Windows console in cp1252 cannot encode `—` `→` `◐`: say it in UTF-8, never crash
        if hasattr(stream, "reconfigure"):                   # …and `\n`, never `\r\n`: a hook pipes --print-written into `git add`
            stream.reconfigure(encoding="utf-8", errors="replace", newline="\n")
    args = parse_args(argv)
    if args.tsvn_hook:
        # TortoiseSVN starts a hook wherever it likes and appends PATH DEPTH MESSAGEFILE CWD: the repository is the
        # one this copy of the tool lives in. `start` runs before the commit dialog lists its files, so the INDEX.md
        # it writes is on the list; `pre` refuses the commit on a violation, the message in TortoiseSVN's error box.
        configure(HERE)
        args = parse_args(["--root", str(ROOT)] + ([] if args.tsvn_hook[0] == "start" else ["--check"]))
    if args.root:
        configure(args.root)
    # under --print-written stdout carries ONE thing: the path list the caller stages
    log = sys.stderr if args.print_written else sys.stdout
    if args.vendor:
        return vendor(args.vendor, partial=args.partial, allow_untagged=args.allow_untagged)
    if args.brand is not None:
        return brand_report(args.brand or None)
    if args.init:
        return init(args.key)
    if args.install_hook:
        return install_hook()
    if args.session_trailer:                                # every commit runs this: it reads one git setting, never the trackers
        return session_trailer(args.session_trailer[0])
    if args.session_check:                                  # …and this: the session rule on a commit that stages no tracker (R4)
        return session_check()
    if args.session:
        return session_cmd(args.session)
    if args.queue:                                          # FM-031 S2: the forge's queue — no tracker is read
        return queue_cmd()
    if args.answer:
        answer_step(args.answer[0].upper(), 1, "reading the trackers")
    trackers = load_trackers()
    global COMMITTING
    COMMITTING = bool(args.print_written)                 # the pre-commit run: what it stages is what its git calls are spent on
    mode = "board" if args.html_only else "check" if args.check else "write" if not (args.schema or args.new or args.next or args.related) else "read"
    refused, derived_problems = run_deriver(trackers, mode, args.derive_flag)
    if args.schema:
        print(render_schema())
        return EXIT_OK
    if refused is not None and not args.html_only:            # the deriver said no: nothing is judged, nothing is written
        for p in derived_problems:
            print(f"  {p}", file=sys.stderr)
        print("REFUSED by the deriver — nothing was written.", file=sys.stderr)
        return refused
    if args.new:
        return new_tracker(args.new, trackers, args.tags)
    if args.owner:
        code = owner_digest(trackers)
        queue_section()
        return code
    if args.answered:
        return answered(trackers)
    if args.answer:
        return answer_cmd(args.answer, trackers, supersede=args.supersede)
    if args.clear_ask:
        return clear_ask(args.clear_ask, trackers)
    if args.standup is not None:
        code = standup(trackers, args.standup)
        if not args.standup:                                # the agenda, not the calendar invite
            queue_section()
        return code
    if args.next:
        return next_up(trackers)
    if args.html_only:
        if TRACKER_DIR.is_dir():
            put(HTML_OUT, render_html(trackers))
            write_views(trackers)
        return EXIT_OK
    if not TRACKER_DIR.is_dir():
        print(f"no tracker directory at {TRACKER_DIR} — run `{CMD} --init`", file=sys.stderr)
        return EXIT_LINT
    if args.triage:
        home, path_now = TRACKER_DIR / "TRIAGE.md", triage_home()["path"]
        if not path_now:
            print(f"--triage: {home.relative_to(ROOT).as_posix()} names no current path — tiers cannot be judged; the Owner writes it first", file=sys.stderr)
            return EXIT_LINT
        today = datetime.date.today().isoformat()
        for r, seen in close_abandoned(today):              # FM-024: the pass closes what nobody closed — and says so
            print(f"closed abandoned session {r['id']} ({r['seat']}, {r['scope']}) — no commit since {seen}. Say so in this pass's paragraph in {home.relative_to(ROOT).as_posix()}.")
        out = TRACKER_DIR / "evidence" / "triage" / f"triage-{today}.md"
        out.parent.mkdir(parents=True, exist_ok=True)
        sheets = sorted(out.parent.glob("triage-*.md"))
        applied, errors = apply_worksheet(sheets[-1].read_text(encoding="utf-8"), sheets[-1] == out, trackers, today) if sheets else ([], [])
        trackers = load_trackers()
        run_deriver(trackers, "write", args.derive_flag)
        earlier = out.read_text(encoding="utf-8") if out.exists() else ""
        text, left = triage_worksheet(trackers, today, last_worked_on, earlier, repos_naming())
        put(out, text)
        print(TRIAGE_RULES.format(path=out.relative_to(ROOT).as_posix(), left=left, home=home.relative_to(ROOT).as_posix(), days=TRIAGE_DAYS, sized=SIZED_LINES, current_path=path_now,
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
    problems = pin_problems() + lint(trackers, committing=args.print_written) + derived_problems
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
        + "".join("> " + n.replace("\n", "\n> ") + "\n>\n" for n in DERIVED_NOTES)
        + f"> Generated {today} · {len(trackers)} trackers ({counts})."
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
            print(f"{OUT.relative_to(ROOT).as_posix()} is STALE — a tracker changed without regenerating. Run: {CMD}", file=sys.stderr)
        for path, text in sorted(DERIVED_FILES.items()):
            if not path.exists() or path.read_text(encoding="utf-8") != text:
                drifted = True
                print(f"{path.relative_to(ROOT).as_posix()} is STALE — regenerate. Run: {CMD}", file=sys.stderr)
        if not drifted:
            print(f"{OUT.relative_to(ROOT).as_posix()} is up to date — {len(trackers)} trackers.", file=log)
        for line in sessions_report() + pin_report():       # reports, never refusals (FM-024, FM-011)
            print(line, file=log)
        frozen = filing_freeze(trackers)                    # FM-032 S4: said, never refused — the refusal is `--new`'s
        if frozen:
            print(f"filing freeze: {frozen[0]} open, at or above {frozen[1]} — only bug filings", file=log)
    else:
        put(OUT, body)
        put(HTML_OUT, render_html(trackers))   # git-ignored; never staged
        write_views(trackers)
        print(f"wrote {OUT.relative_to(ROOT).as_posix()} — {len(trackers)} trackers, {len(unknown)} unknown-status", file=log)
        print(f"  buckets — In Progress: {sum(t['status'] == 'In Progress' for t in trackers)} · generated files: {len(DERIVED_FILES)}", file=log)
        for path, text in sorted(DERIVED_FILES.items()):
            path.parent.mkdir(parents=True, exist_ok=True)
            put(path, text)
        if args.print_written:                 # the caller stages what we OWN, never a guessed glob
            for path in [OUT, *sorted(DERIVED_FILES)]:
                print(path.relative_to(ROOT).as_posix())

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
