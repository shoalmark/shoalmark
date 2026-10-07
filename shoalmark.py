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
    shoalmark.py --ratio         records added : product added, per Berlin day of the merge (FM-032)
    shoalmark.py --init          scaffold the tracker directory, TRIAGE.md and shoalmark.toml
    shoalmark.py --vendor DIR    copy this tool, pinned by hash, into another repository

One seam, by convention: if `<tracker dir>/derive` exists and is executable it runs first, on every run but `--html-only`'s — it may add
columns (each also a view on the board), front-matter keys, problems and other generated files, or refuse the run.

The INDEX is a *pointer*, not a copy: each row is a terse hook and a machine-read status; the detail
lives in the tracker. `status` is the code lifecycle — `Shipped` means merged, not deployed.

Both modes FAIL on a ledger-integrity violation: a gate that always lands green is not a gate.
Configuration is `shoalmark.toml` at the repository root; every key has a default.
"""

import argparse
import atexit
import base64
import datetime
import difflib
import fnmatch
import hashlib
import collections
import itertools
import json
import math
import os
import pathlib
import re
import shlex
import shutil
import subprocess
import sys
import tempfile
import threading
import unicodedata
import urllib.parse

HERE = pathlib.Path(__file__).resolve().parent
# The version is the `VERSION` file and nothing else. It ships in TOOL_FILES, so a vendored copy carries it, and
# `--vendor` then compares the consumer's VERSION against ours — the artifact actually being copied. Declaring it
# a second time here is what let 0.17.1 and 0.17.2 ship with a stale constant, silencing the changelog (FM-009).
__version__ = (HERE / "VERSION").read_text(encoding="utf-8").strip() if (HERE / "VERSION").exists() else "unknown"
MARKED = HERE / "vendor" / "marked-18.0.13.umd.js"      # the one vendored, pinned third-party file (marked, MIT)
# THE HOOKS' COPY (a private security report): every hook `--install-hook` writes runs a copy of the tool kept in the git directory, which `--install-hook` alone writes,
# with its `COPY` file beside it. A run of that copy is a hook's run: it runs nothing the tree brought, and writes only inside the repository, through no symlink.
HOOK_RUN = __name__ == "__main__" and (HERE / "COPY").is_file()
# how an Owner sets up the key their answers are signed with — named where signing fails: `--answer`, and the board's
# second screen (a repository with its own page overrides the label `answer.sign.url`)
SIGNING_PAGE = "https://shoalmark.github.io/shoalmark/signing.html"
TOOL_PAGE = "https://github.com/shoalmark/shoalmark"          # the running line's links: the tool, and its release at VERSION
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
    # the tag that passes the freeze — a repository's own `[tags]` may have no `bug`; one that names none of its tags
    # freezes nothing, and `--check` says so
    "freeze_tag": "bug",
    # A PASS JUDGES BEFORE THE FIRST BUILD COMMIT (FM-033, the Owner's rule of 2026-09-24): a commit that changes a path
    # outside the tracker directory names a tracker that, at the commit's parent, a pass has kept `In Progress`. Off by
    # default: a repository that vendors the tool may carry no `triaged:` yet.
    "judged_before_build": False,
    # who may answer an ask. An answer is three lines in the tracker, committed by the answerer, and the commit is the
    # proof — but git's author is a string anyone can type. So an entry is `"name"` (Subversion, whose server
    # authenticates the committer; or git with NO enforcement, and the gate says so) or `"name signed"` (git: the
    # commit that carries the answer must VERIFY — `git verify-commit` — under a key the repository trusts; that is
    # `gpg.format`/`user.signingkey` and, for SSH keys, `gpg.ssh.allowedSignersFile`). Empty = nobody may answer.
    # A seat cannot add itself here unseen: the change is in the same diff as anything it would allow.
    "answerers": [],
    # WHO IS AT THE KEYBOARD, and what that seat may change. `[seats]` is a name of the repository's choosing → the
    # identity the version control system reports — `"principal@seat"`, or `"principal@seat signed"` where the commit
    # must also VERIFY under a key trusted for it — or a LIST of those, several identities for one seat (FM-024). `[rights]` gives a name of your own its rights; the four built-in
    # names have theirs (BUILTIN_RIGHTS). ABSENT, nothing is enforced — this is for a repository that lets in agents
    # which never read its contract. It catches an agent that does not know the rule, not one that lies (README,
    # *Seats*). Under Subversion an identity is the server account and `signed` is refused: the server authenticated it.
    # THE OWNER IS NOT A SEAT (FM-024, D2): a top-level `owner = "<email> signed"`, before any table, names them — the
    # same value as a `[seats]` one — and `[seats] owner` is still read, as its old spelling (`seats_of`).
    "seats": {},
    "rights": {},
    # humans have office hours, agents have budgets: ONE fixed sitting a day in which the Owner goes through what
    # needs them. Agents write their asks before it; a deadline is counted in standups, not in hours.
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
                 "intent": "The intent", "path": "The current path", "passes": "Passes", "asks": "Asks", "raised": "Raised", "acts": "Acts"},
    # where, under the tracker directory, the Reviewer's files sit — what `--queue` counts as review addenda after a verdict
    # (FM-031). A folder, or a glob of folders: a consumer that files reviews beside each tracker's evidence names `evidence/*/`
    "paths": {"reviews": "evidence/reviews/"},
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
        m = re.fullmatch(r'([A-Za-z0-9_-]+)\s*=\s*(?:"((?:[^"\\]|\\.)*)"|(-?\d+)|(true|false)|(\[(?:"(?:[^"\\]|\\.)*"|[^\]"])*\]))\s*(?:#.*)?', line)
        if not m:
            raise SystemExit(f"{CONFIG_NAME}:{n}: not understood — {raw.strip()!r}. A line is `key = \"text\"`, `key = 123`, `key = true`, `key = [\"a\", \"b\"]` or `[table]`")
        key, text_value, number, flag, items = m.groups()
        if items is not None and not re.fullmatch(r'\[\s*(?:"(?:[^"\\]|\\.)*"\s*(?:,\s*"(?:[^"\\]|\\.)*"\s*)*)?,?\s*\]', items):
            raise SystemExit(f"{CONFIG_NAME}:{n}: a list holds quoted strings only — {raw.strip()!r}")
        value = (re.sub(r'\\(.)', r"\1", text_value) if text_value is not None else int(number) if number is not None
                 else re.findall(r'"((?:[^"\\]|\\.)*)"', items) if items is not None else flag == "true")
        (out if table is None else table)[key] = value
    if isinstance(out.get("tracker_dir"), str) and "\\" in out["tracker_dir"]:     # one system reads it as a separator, another as a letter of the folder's name
        raise SystemExit(f"{CONFIG_NAME}: `tracker_dir = {json.dumps(out['tracker_dir'])}` holds a backslash, which Windows reads as a folder's separator "
                         "and every other system as a letter of the folder's name — write the folder with /")
    if isinstance(out.get("tracker_dir"), str) and (out["tracker_dir"].startswith("/") or any(p[1:2] == ":" for p in out["tracker_dir"].split("/"))):     # a root, or a drive in any part: never a folder of the repository
        raise SystemExit(f"{CONFIG_NAME}: `tracker_dir = {json.dumps(out['tracker_dir'])}` is read as absolute or drive-qualified on some system — "
                         "`tracker_dir` is a folder written relative to the repository, with /")
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


# THE WRITE RULE (the Owner's ruling filed in FM-006, *The fix round after the critical review*, added to the round): every run writes a file of the tree only as
# a regular file inside the repository, outside its git directory, never through a symlink. `write_rule` is the one place every write of the tree passes:
# the board's refresh leaves such a file unwritten with its line (`board_write`); a hook's run of the copy refuses (`guard_write`, the commit refused);
# every other run refuses in one line naming the file, exit 4, before anything is written (`refuse_tree_write`).
def tree_write(path):
    """Whether a write lands in the tree this run tracks — inside the repository as written, outside its git directory. A destination a person names
    elsewhere (`--vendor`, `--brand`, a calendar file) and `--install-hook`'s hooks and copy are not — a named one is resolved once, where it is named, and
    judged again under the folder it resolves to; a tracker folder outside the repository is refused before any run reads it (`load_trackers`)."""
    return in_tree(path) and not in_git_dir_on_disk(path)


def write_rule(path):
    """The write rule for one file of the tree: in a hook's run of the copy, `guard_write`; in every other run but the board's refresh, one line naming
    the file, exit 4, where `write_problem` finds a reason."""
    if SAFE_WRITES:
        guard_write(path)
    elif tree_write(path):
        why = write_problem(path)
        if why:
            refuse_tree_write(path, why)


def refuse_tree_write(path, why):
    """A run other than the board's refresh, and no hook's, would write a file of the tree it may not: one line naming it, exit 4, the lint code, and
    nothing written."""
    rel = os.path.relpath(path, ROOT).replace(os.sep, "/") if in_tree(path) else str(path)
    print(f"shoalmark: {rel} is {why} — the tool writes a file of the tree only as a regular file inside the repository, never through a symlink: "
          "nothing is written; put the file itself there", file=sys.stderr)
    raise SystemExit(EXIT_LINT)


def guard_write(path):
    """In a hook's run of the copy, or the board's run: refuse to write `path` where `write_problem` finds a reason — `ReadOnlyRun`, which the run says in one line."""
    why = write_problem(path) if SAFE_WRITES else ""
    if why:
        raise ReadOnlyRun(f"it would write {os.path.relpath(path, ROOT).replace(os.sep, '/') if in_tree(path) else path}, {why}")


def put(path, text):
    """Every file the tool writes is UTF-8 with `\\n` line ends on every system — what is committed must not depend on
    who ran the tool. A file of the tree is written under the write rule (`write_rule`): only a regular file inside the repository, never through a symlink."""
    if SAFE_WRITES or tree_write(path):
        write_rule(path)
        fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_TRUNC | getattr(os, "O_NOFOLLOW", 0) | getattr(os, "O_BINARY", 0), 0o666)
        with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as f:
            f.write(text)
        return
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)


# THE BOARD'S RUN — `--html-only`, what a checkout and a merge hook starts (a private security report). A branch brings the files this run
# reads, so it reads only what a regular file inside the repository holds, through no symlink; it starts nothing but read-only git; it
# writes only the board's files. Each is checked where the file is read or written, and `board_tripwire` refuses at the interpreter
# whatever else a path of the tool might reach.
SAFE_READS = False        # on for the board's run: a file in the tree is read only if it is a regular file inside the repository, reached through no symlink
SAFE_WRITES = False       # on for the board's run and every hook's run of the copy: a file is written only inside the repository, outside its git directory, through no symlink
_TRIPWIRE = False         # on for the board's run: nothing is started, written or imported but what the run is for
_TEMP = ""                # the system's temporary directory, read before the tripwire is armed: the hook must not ask `tempfile` for it (see `arm_tripwire`)
_IN_TRIPWIRE = [False]    # the hook is not judged by itself
BOARD_LEFT = []           # what the run left alone, as (file, why) — said once, at its end
TRIPPED = []              # …and what the tripwire refused


class ReadOnlyRun(BaseException):
    """What the board's run refused to do. A `BaseException` on purpose: no handler of the tool's own can take it for the failure of
    a command it may go on from."""


def _norm(path):
    return os.path.normcase(os.path.abspath(os.fspath(path)))


def in_tree(path):
    """Whether `path`, as written, lies inside the repository ROOT."""
    p, root = _norm(path), _norm(ROOT)
    return p == root or p.startswith(root.rstrip(os.sep) + os.sep)


def real_inside(path):
    """Whether `path` lies inside the repository and is reached through no symlink or junction: the path as written is the path it resolves to."""
    return in_tree(path) and os.path.normcase(os.path.realpath(_norm(path))) == _norm(path)


_GIT_DIRS = None


def git_dirs():
    """The repository's git directories — its own and the common one, which holds the hooks' copy — read once per run with one read-only call,
    and `.git` at the root whatever git says."""
    global _GIT_DIRS
    if _GIT_DIRS is None:
        out = subprocess.run(["git", "rev-parse", "--absolute-git-dir", "--git-common-dir"], cwd=ROOT, capture_output=True, text=True, encoding="utf-8",
                             errors="replace", env=nested_git_env())
        _GIT_DIRS = sorted({_norm(ROOT / ".git"), *(_norm(ROOT / l) for l in (out.stdout.splitlines() if out.returncode == 0 else []) if l.strip())})
    return _GIT_DIRS


def in_git_dir(path):
    """Whether `path`, as written or as it resolves, lies inside one of the repository's git directories."""
    ps = {_norm(path), os.path.normcase(os.path.realpath(_norm(path)))}
    return any(p == d or p.startswith(d.rstrip(os.sep) + os.sep) for p in ps for d in git_dirs())


def in_git_dir_on_disk(path):
    """Whether `path`, as written or as it resolves, lies inside one of the repository's git directories as the file system compares paths (`git_dir_holding`):
    where it ignores case and Unicode normalization, a git directory spelled in another case or normalization is that git directory."""
    p = _norm(path)
    return git_dir_holding(p) or git_dir_holding(os.path.normcase(os.path.realpath(p)))


def write_problem(path):
    """Why a hook's run of the copy, or the board's run, does not write `path`, or "": it lies outside the repository or inside its git directory —
    where the hooks and their copy are — is reached through a symlink, or is no regular file."""
    if not in_tree(path):
        return "outside the repository"
    if in_git_dir_on_disk(path):
        return "inside the git directory"
    if not real_inside(path):
        return "a symlink, or reached through one"
    if os.path.lexists(path) and not os.path.isfile(path):
        return "not a regular file"
    return ""


def left_alone(path, why):
    rel = os.path.relpath(path, ROOT).replace(os.sep, "/") if in_tree(path) else str(path)
    if all(rel != r for r, _w in BOARD_LEFT):
        BOARD_LEFT.append((rel, why))


# THE READING RULE (the Owner's ruling filed in FM-006, *The fix round after the critical review*, on a private security report): in EVERY run, a file of
# the tree — a tracker, the configuration, TRIAGE.md, a theme, the labels, a worksheet, a file the configuration names — is read only where it is a regular
# file inside the repository, reached through no symlink. `board_isfile` and `board_text` are the rule, and every reader of the tree asks them. The
# board's refresh leaves such a file unread and names it once at its end; every other run refuses in one line naming it (`refuse_tree_file`).
def board_isfile(path):
    """`path.is_file()` under the reading rule: a file of the tree only where it is a regular file inside the repository, through no symlink. One that is
    there and is not: in the board's run left unread, and named once at the end; in every other run, the run is refused (`refuse_tree_file`)."""
    path = pathlib.Path(path)
    if not in_tree(path):
        return path.is_file()
    if real_inside(path) and path.is_file():
        return True
    if os.path.lexists(path):
        why = "a symlink, or reached through one" if not real_inside(path) else "not a regular file"
        if SAFE_READS:
            left_alone(path, "a symlink, or not a regular file" if not real_inside(path) else why)
        else:
            refuse_tree_file(path, why)
    return False


def board_text(path):
    """A file's text, or None where it is not there — under the reading rule (`board_isfile`)."""
    path = pathlib.Path(path)
    if in_tree(path) and not board_isfile(path):
        return None
    return path.read_text(encoding="utf-8") if path.exists() else None


def refuse_tree_file(path, why):
    """A run other than the board's refresh meets a file of the tree it may not read: one line naming it, and the run ends — exit 4, the lint code, as
    every refusal of the gate's: a commit's hook that exits 4 refuses the commit, and `--check` in CI fails on it. Never a traceback, nothing written."""
    rel = os.path.relpath(path, ROOT).replace(os.sep, "/") if in_tree(path) else str(path)
    print(f"shoalmark: {rel} is {why} — the tool reads a file of the tree only as a regular file inside the repository, following no symlink: "
          "nothing is read from it and nothing is written; put the file itself there", file=sys.stderr)
    raise SystemExit(EXIT_LINT)


def tracker_folder_problem(what="the board is not refreshed"):
    """Why the board's run, or a hook's run of the copy, does not touch the tracker folder, in one line ending in `what` — or "": it must resolve inside the
    repository and outside its git directory, and the way to it is no symlink."""
    d = TRACKER_DIR
    if not in_tree(d):
        return f"the tracker folder {os.path.abspath(d)} is not inside the repository {ROOT} — {what}"
    real = pathlib.Path(os.path.realpath(_norm(d)))
    if not in_tree(real):
        return f"the tracker folder {os.path.relpath(d, ROOT).replace(os.sep, '/')} resolves outside the repository, to {real} — {what}"
    if in_git_dir_on_disk(d):
        return f"the tracker folder {os.path.relpath(d, ROOT).replace(os.sep, '/')} is inside the git directory, where the hooks and their copy are — {what}"
    if not real_inside(d):
        return f"the tracker folder {os.path.relpath(d, ROOT).replace(os.sep, '/')} is, or is reached through, a symlink — {what}"
    return ""


_TRACKED = None


def tracked_board_rels():
    """What git tracks of the board's files — the page and its views — as git names them, relative to the repository, with one read-only call. Where there is
    no git, none."""
    if vcs() != "git":
        return []
    rels = [HTML_OUT.relative_to(ROOT).as_posix(), VIEW_DIR.relative_to(ROOT).as_posix()]
    out = subprocess.run(["git", "ls-files", "-z", "--", *(":(literal)" + r for r in rels)], cwd=ROOT, capture_output=True, text=True, encoding="utf-8",
                         errors="replace", env=nested_git_env()).stdout
    return [r for r in out.split("\x00") if r]


def tracked_board_files():
    """What git tracks of the board's files (`tracked_board_rels`), as paths, read once per run. Where there is no git, none."""
    global _TRACKED
    if _TRACKED is None:
        _TRACKED = {_norm(ROOT / r) for r in tracked_board_rels()}
    return _TRACKED


def tracked_board_line(rels):
    """The cold review's F1 (the Owner's ruling filed in FM-006): where git tracks a view of the board, the board's run writes no page that could load it. This
    is the one line it says in place of the link, naming the file, and the page it leaves says the same. A page git tracks is left as committed, with its own
    line (`unwritable`)."""
    names = ", ".join(rels[:3]) + (f" and {len(rels) - 3} more" if len(rels) > 3 else "")
    return (f"board: not written — git tracks {names}, a file of the board: the page loads nothing; untrack it (`git rm --cached`), and the next run "
            "writes the board")


def tracked_board_page(line):
    """The page the board's run leaves where git tracks a file of the board: `line`, and nothing it loads — no script, no style, no image, and a policy that
    allows none."""
    return ('<!doctype html>\n<html lang="en"><head><meta charset="utf-8"><meta http-equiv="Content-Security-Policy" content="default-src \'none\'">'
            f"<title>board not written</title></head><body><p>{html_escape(line)}</p></body></html>\n")


def unwritable(path):
    """Why the board's run, or a hook's run of the copy, does not write one of the board's files, or "": `write_problem`'s reason — and, in the board's run, that git
    tracks it (a commit's hook rewrites a board a repository tracks, as it always has)."""
    why = write_problem(path)
    if why:
        return why
    if SAFE_READS and _norm(path) in tracked_board_files():
        return "git tracks it"
    return ""


def board_write(path, text, changed_only=False):
    """Write one of the board's files: with `put`, as ever; in the board's run and a hook's run of the copy only where `unwritable` finds no reason, and
    never through a symlink. `changed_only`: leave a file that already says this. Returns whether it wrote."""
    path = pathlib.Path(path)
    if SAFE_READS:                                          # the board's refresh: what it may not write it leaves, with its line
        why = unwritable(path)
        if why:
            left_alone(path, why)
            return False
    else:                                                   # every other run: the write rule
        write_rule(path)
    if changed_only and path.exists() and path.read_text(encoding="utf-8") == text:
        return False
    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_TRUNC | getattr(os, "O_NOFOLLOW", 0) | getattr(os, "O_BINARY", 0), 0o666)
    with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)
    return True


_PATH_SEP = re.compile(r"[\\/]")
READ_ONLY_GIT = frozenset({"rev-parse", "log", "show", "cat-file", "diff", "var", "for-each-ref", "symbolic-ref", "ls-files", "rev-list", "merge-base",
                           "show-ref", "worktree", "config", "branch"})
READ_ONLY_GIT_C = ("core.quotePath=", "gpg.ssh.allowedSignersFile=")        # the only `-c` the tool hands git: how it prints a path, and the signers it verifies against


def read_only_git(argv):
    """Whether `argv` is a call of git that changes nothing: one of the subcommands above, none of their forms that write (`config` only to read,
    `branch` only `--show-current`, `worktree` only `list`, no `--output`), and no `-c` but the two the tool uses."""
    if not isinstance(argv, (list, tuple)) or len(argv) < 2 or _PATH_SEP.split(str(argv[0]))[-1].lower() not in ("git", "git.exe"):
        return False
    rest, i = [str(a) for a in argv[1:]], 0
    while i < len(rest) and rest[i] in ("-c", "-C"):
        if rest[i] == "-c" and not (i + 1 < len(rest) and rest[i + 1].startswith(READ_ONLY_GIT_C)):
            return False
        i += 2
    if i >= len(rest) or rest[i] not in READ_ONLY_GIT:
        return False
    sub, tail = rest[i], rest[i + 1:]
    if any(a.startswith("--output") for a in tail):
        return False
    if sub == "branch":
        return tail == ["--show-current"]
    if sub == "worktree":
        return tail[:1] == ["list"]
    if sub == "config":
        return "--get" in tail or tail == ["user.name"]
    if sub == "symbolic-ref":
        return len([a for a in tail if not a.startswith("-")]) == 1
    return True


def split_cmdline(line):
    """A Windows command line as the argument list it came from (the rules `subprocess.list2cmdline` writes by): Windows hands the audit hook
    the line, POSIX the list."""
    out, cur, quoted, started, i = [], [], False, False, 0
    while i < len(line):
        c = line[i]
        if c == "\\":
            j = i
            while j < len(line) and line[j] == "\\":
                j += 1
            n = j - i
            started = True
            if j < len(line) and line[j] == '"':
                cur.append("\\" * (n // 2))
                if n % 2:
                    cur.append('"')
                    j += 1
            else:
                cur.append("\\" * n)
            i = j
        elif c == '"':
            quoted, started, i = not quoted, True, i + 1
        elif c in " \t" and not quoted:
            if started:
                out.append("".join(cur))
                cur, started = [], False
            i += 1
        else:
            cur.append(c)
            started, i = True, i + 1
    if started:
        out.append("".join(cur))
    return out


def board_tripwire(event, args):
    """The board's run, enforced where Python itself does the thing (`sys.addaudithook`): no program but read-only git, no network, nothing written
    but the board's files (and the one temporary file the signers are verified against), no file of the tree opened but a regular file inside the
    repository reached through no symlink. Whatever a path of the tool reaches that the checks above did not think of is refused here and said."""
    if not _TRIPWIRE or _IN_TRIPWIRE[0]:
        return
    _IN_TRIPWIRE[0] = True
    try:
        board_judge(event, args)
    finally:
        _IN_TRIPWIRE[0] = False


def board_judge(event, args):
    """What `board_tripwire` decides for one event: nothing, or `ReadOnlyRun`. It calls nothing that takes a lock — an event can fire while the code that raised it holds one."""
    why = ""
    if event == "subprocess.Popen":
        argv = args[1] if isinstance(args[1], (list, tuple)) else split_cmdline(args[1]) if isinstance(args[1], str) else [str(args[1])]
        if not read_only_git(argv):
            why = f"it would start {' '.join(str(a) for a in argv[:4])}"
    elif event in ("os.system", "os.exec", "os.spawn", "os.posix_spawn", "os.startfile", "os.fork", "os.forkpty", "webbrowser.open", "socket.connect"):
        why = f"{event} is not for the board's run"
    elif event in ("os.rename", "os.rmdir", "os.symlink", "os.link", "os.truncate", "os.chmod", "os.chown", "os.utime") or event.startswith("shutil."):
        why = f"{event} is not for the board's run"
    elif event == "os.mkdir":
        if _norm(args[0]) != _norm(VIEW_DIR):
            why = f"it would make {args[0]}"
    elif event == "os.remove":
        if not board_target(args[0]):
            why = f"it would remove {args[0]}"
    elif event == "open":
        target, mode, flags = args
        if isinstance(target, int) or target is None:
            return
        flags = flags if isinstance(flags, int) else 0
        writing = any(c in str(mode or "") for c in "wax+") or bool(flags & (os.O_WRONLY | os.O_RDWR | os.O_APPEND | os.O_CREAT | os.O_TRUNC))
        if writing:
            if not board_target(target):
                why = f"it would write {os.fsdecode(target)}"
        elif in_tree(os.fsdecode(target)) and not (real_inside(os.fsdecode(target)) and os.path.isfile(os.fsdecode(target))):
            why = f"it would read {os.fsdecode(target)}, which is no regular file inside the repository"
    elif event in ("os.listdir", "os.scandir"):
        if args[0] is not None and not isinstance(args[0], int) and in_tree(os.fsdecode(args[0])) and not real_inside(os.fsdecode(args[0])):
            why = f"it would list {os.fsdecode(args[0])}, a symlink or reached through one"
    if why:
        TRIPPED.append(why)
        raise ReadOnlyRun(why)


def board_target(path):
    """Whether `path` is one of the board's files: the page, a view, or the one temporary file the signers are verified against."""
    p = _norm(os.fsdecode(path))
    if p == _norm(HTML_OUT) or (os.path.dirname(p) == _norm(VIEW_DIR) and p.endswith(os.path.normcase(".js"))):
        return True
    return os.path.dirname(p) == _TEMP and os.path.basename(p).startswith("shoalmark-signers-")


def arm_tripwire():
    """Turn the tripwire on. Everything it needs is read first — the system's temporary directory above all: `tempfile` finds it under a lock of its own, on the first `os.open` it
    makes, and a hook that asked for it then would wait for ever for a lock its own thread holds."""
    global _TEMP, _TRIPWIRE
    _TEMP = _norm(tempfile.gettempdir())
    if not _AUDIT_HOOKED[0]:
        sys.addaudithook(board_tripwire)
        _AUDIT_HOOKED[0] = True
    _TRIPWIRE = True


def digest(path):
    """A PIN hash survives a checkout that converts line ends (git's autocrlf, svn:eol-style)."""
    return hashlib.sha256(pathlib.Path(path).read_bytes().replace(b"\r\n", b"\n")).hexdigest()


PY = "python" if os.name == "nt" else "python3"         # the name a message, a hook and the contract can be pasted under

# WHAT A SEAT MAY CHANGE — four rights, each one a front-matter transition the gate can see in a diff. Anything else a
# tracker carries is open to every seat and needs no right: rights are for the four changes that move authority, not
# for the work. There is no hierarchy, no deny rule and no wildcard — a name either holds a right or it does not.
RIGHTS = ("answer",      # writing `answer:` `answered:` `answered-by:` — the Owner's ruling
          "ask",         # setting `next: owner` — putting a question in front of them
          "close",       # setting a terminal status — saying work is over
          "triage")      # writing `considered:`, `kind-of-problem:`, `tier:`, `rank:`, `triaged:` — the judgement
# the four names that need no `[rights]` line, because the seats mean the same thing in every repository that runs this
BUILTIN_RIGHTS = {"owner": set(RIGHTS), "planner": {"ask", "close", "triage"}, "reviewer": {"triage"}, "builder": set(),
                  "principal": {"ask", "close", "triage"}, "implementer": set()}     # FM-024: `planner` and `builder` are the seats' names from 0.19.0;
                                                                                     # `principal` and `implementer`, their old spellings, hold the same
TRIAGE_KEYS = ("kind-of-problem", "tier", "rank", "triaged")     # `considered:` too — except on a filing, which is the rule, not a verdict
# THE KEYS A RIGHT IS JUDGED ON (the Owner's ruling of 2026-10-04, v0.19.1): `status` (`close`), `next` (`ask`), the three answer lines
# (`answer`, and `ask`'s clearing move), `considered` and the triage keys (`triage`). Each is read from ONE line, written in lower case
# (`guarded_key_problems`): a second line, or one in capitals, would be a line the reader keeps and another one judged
GUARDED_KEYS = ("status", "next", "answer", "answered", "answered-by", "considered", *TRIAGE_KEYS)


def tracker_folder(cfg, prefix=""):
    """The tracker folder a configuration names — its `tracker_dir` — as a path below `prefix`: "" for one from the
    repository's own root, as `configure` binds `TRACKER_DIR`. One reading of `tracker_dir`, for every caller."""
    return pathlib.PurePosixPath(prefix) / cfg.get("tracker_dir", DEFAULTS["tracker_dir"])


def configure(root=None):
    """Bind every path, id pattern and schema shape to one repository. Called once at import for the working
    directory, and again by `--root` and by the tests."""
    global ROOT, CONFIG, TRACKER_DIR, OUT, HTML_OUT, VIEW_DIR, REPO_BLOB, TAGS, CONSIDERED_FROM, TRIAGE_DAYS
    global KINDS, KIND_LABELS, KIND_RE, TITLE_RE, TRACKER_LINK_RE, H1_ID_RE, ROW_ID_RE, _IDS, FRONT_MATTER, CMD
    global HEAD, STATE_HEAD_RE, DONE_RE
    ROOT = find_root(root)
    path = ROOT / CONFIG_NAME
    text = board_text(path)                             # in the board's run: a regular file inside the repository, or no configuration
    CONFIG = {**DEFAULTS, **(read_config(text) if text is not None else {})}
    TRACKER_DIR = ROOT / tracker_folder(CONFIG)
    OUT, HTML_OUT, VIEW_DIR = TRACKER_DIR / "INDEX.md", TRACKER_DIR / "index.html", TRACKER_DIR / "view"
    REPO_BLOB, TAGS, TRIAGE_DAYS = CONFIG["blob"], dict(CONFIG["tags"]), int(CONFIG["triage_days"])
    global FREEZE_AT
    FREEZE_AT = CONFIG["freeze_at"]
    if isinstance(FREEZE_AT, bool) or not isinstance(FREEZE_AT, int) or FREEZE_AT < 0:
        raise SystemExit(f"{CONFIG_NAME}: `freeze_at` is a whole number of open trackers — the filing freeze holds at that count and above; 0 turns it off. Got {FREEZE_AT!r}")
    global FREEZE_TAG
    FREEZE_TAG = CONFIG["freeze_tag"]
    if not isinstance(FREEZE_TAG, str) or not FREEZE_TAG.strip():
        raise SystemExit(f"{CONFIG_NAME}: `freeze_tag` is the one tag, from [tags], that passes the filing freeze — `bug` by default. Got {FREEZE_TAG!r}")
    FREEZE_TAG = FREEZE_TAG.strip()
    if not isinstance(CONFIG["judged_before_build"], bool):
        raise SystemExit(f"{CONFIG_NAME}: `judged_before_build` is true or false — a pass judges before the first build commit (FM-033); "
                         f"false (the default) turns it off. Got {CONFIG['judged_before_build']!r}")
    global ANSWERERS, SEATS, SEAT_RIGHTS, ASKS_HEAD_RE, RAISED_HEAD_RE, ACTS_HEAD_RE, COMMITTING, _STAGED, _LINE_AUTHOR, _SVN_BLAME, _BLAME_REFUSED, _GIT_USER
    _GIT_USER = None                                    # `git config user.name`, read at most once for this repository
    ANSWERERS = {}                                      # name -> "signed" | "" (name only)
    for a in (CONFIG.get("answerers") or []):
        name, _, mode = str(a).strip().rpartition(" ")
        ANSWERERS[name if mode == "signed" else str(a).strip()] = "signed" if mode == "signed" else ""
        refuse_signed_name("`answerers`", name, mode)
    SEATS, SEAT_RIGHTS = {}, {}                         # seat name -> [(identity, "signed" | ""), …], and seat name -> rights
    seen = {}                                           # identity -> the seat that claimed it first
    for name, value in seats_of(CONFIG).items():
        SEATS[name] = seat_identities(value)            # FM-024: a string is one identity, a list is several — old and new
        for who, mode in SEATS[name]:                   # a signed identity is an email (the release bar's signed identity)
            refuse_signed_name("`owner`" if at_top(name) else f"`[seats] {name}`", who, mode)
        for who, _mode in SEATS[name]:
            if who and who in seen and at_top(seen[who]):   # the Owner named at the top is no seat and no line of `[seats]` (FM-024, D2)
                raise SystemExit(f"{CONFIG_NAME}: " + (f"`owner` lists `{who}` twice" if seen[who] == name else f"`{who}` is the Owner's (`owner`, at the top) and the seat `{name}`'s (`[seats]`)")
                                 + "; an identity is the Owner's or one seat's, listed once")
            if who and who in seen:                     # under two seats, or twice under one: `signed` would read two ways
                raise SystemExit(f"{CONFIG_NAME}: `[seats]` — `{who}` is listed " + (f"twice under `{name}`" if seen[who] == name else f"under two seats, `{seen[who]}` and `{name}`")
                                 + "; an identity is one seat's, listed once")
            if who:
                seen[who] = name
        SEAT_RIGHTS[name] = set(BUILTIN_RIGHTS.get(name, ()))
    for name, words in (CONFIG.get("rights") or {}).items():
        if isinstance(words, str) or any(w not in RIGHTS for w in words):
            bad = [words] if isinstance(words, str) else [w for w in words if w not in RIGHTS]
            raise SystemExit(f'{CONFIG_NAME}: `[rights] {name}` — {bad[0]!r} is not a right. There are four: {" · ".join(RIGHTS)}; '
                             f'anything else a tracker can carry is open to every seat and needs none')
        SEAT_RIGHTS[name] = set(words)
    COMMITTING, _STAGED, _LINE_AUTHOR, _SVN_BLAME, _BLAME_REFUSED = False, None, {}, {}, set()    # the pre-commit run, what it stages, who wrote which line, and the trackers whose blame could not be read
    global _BUILD, _CHANGES
    _BUILD, _CHANGES = None, None                       # FM-033's judgement of this run, and the changes it judges (`changes_under_review`) — each read once
    global _GUARD, _SIGNERS
    _GUARD, _SIGNERS = None, None                       # FM-037's, the same — and the signers file it verifies against
    _MODES.clear()                                      # …and the modes git records for a configuration's path (`path_mode`)
    _TREES.clear()                                      # …and the paths a revision holds, where the guard lists them (`tree_paths`)
    _VIEWS.clear()                                      # …and each revision's view of the two sections (`triage_views`)
    global _SVN_NEW, _WALK, _WALK_FAILED
    _SVN_NEW = {}                                       # which paths Subversion holds no committed revision of (`svn_new`)
    _WALK = None                                        # the default branch the branch's commits were read since — "" where there is none (`read_changes`)
    _WALK_FAILED = None                                 # the one line where git could not walk the commits a run judges (`walk_problems`)
    global _WALK_COMMITS, _HAS_SESSIONS
    _WALK_COMMITS, _HAS_SESSIONS = {}, {}               # each walked commit's parents and trailers, and whose history carries a `Session:` — read once (v0.19.1)
    global _ORIGIN_DEFAULT, _TRUNK_UNTOLD, _ASK_ORIGIN
    _ORIGIN_DEFAULT = None                              # the name origin gives its default branch, asked once per run at most (`origin_default`)
    _ASK_ORIGIN = False                                 # whether this run walks the branch's commits, and may ask origin (`main`, `default_trunk`)
    _TRUNK_UNTOLD = None                                # the one line where origin's default branch cannot be told (`default_trunk`, `walk_problems`)
    global _GIT_DIRS
    _GIT_DIRS = None                                    # the git directories a run of the copy writes nothing into, read once per repository
    KIND_LABELS = dict(CONFIG["kinds"])
    HEAD = {**DEFAULTS["headings"], **CONFIG["headings"]}
    if set(HEAD) - set(DEFAULTS["headings"]) or not all(str(v).strip() for v in HEAD.values()):
        raise SystemExit(f"{CONFIG_NAME}: `[headings]` names {', '.join(DEFAULTS['headings'])} — each a section name, none empty")
    STATE_HEAD_RE = re.compile(_STATE_HEADS[:-3] + "|" + re.escape(HEAD["state"]) + r")\b", re.I)
    DONE_RE = re.compile(_DONE_WORDS + "|" + re.escape(HEAD["done"]), re.I)
    # the body section an exchange is moved into when its ask is cleared — the repository's own word, English always
    ASKS_HEAD_RE = re.compile(r"^#{2,3}\s+(asks|" + re.escape(HEAD["asks"]) + r")\s*$", re.I | re.M)
    # …and the one a raise is written under (FM-033's second answer): one sourced line per raise
    RAISED_HEAD_RE = re.compile(r"^#{2,3}\s+(raised|" + re.escape(HEAD["raised"]) + r")\s*$", re.I | re.M)
    # …and the one an act's record is kept under (FM-030): done, scheduled, rescheduled — newest last
    ACTS_HEAD_RE = re.compile(r"^#{2,3}\s+(acts|" + re.escape(HEAD["acts"]) + r")\s*$", re.I | re.M)
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
    global CMD_OWN
    try:
        CMD_OWN = PY + " " + pathlib.Path(__file__).resolve().relative_to(ROOT).as_posix()
    except ValueError:
        CMD_OWN = PY + " " + pathlib.Path(__file__).resolve().as_posix()      # forward slashes: a hook is a `sh` script, and `\\` is its escape
    if HOOK_RUN:                                        # the hooks' copy names the command a person runs — the one `--install-hook` was run with — never its own place
        CMD_OWN = copy_record().get("cmd") or CMD_OWN
    CMD = os.environ.get("SHOALMARK_CMD") or CMD_OWN    # a repository that wraps the tool is named by its own command in every message
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
# FM-030 — the move an answer writes with itself, by the ask's kind. A ruling, a determination or a ceremony is decided by
# the answer, and the seat's move follows: `build`, the move the rules give unbuilt work (`run` is for something BUILT that
# waits for its run); `--clear-ask <id> <move>` sets the real one when the answer is acted on. An action's yes is a promise
# of the Owner's own hands, not the act: `next: owner` stays. An ask of no known kind keeps the move it had.
ANSWER_MOVE = {"ruling": "build", "determination": "build", "ceremony": "build", "action": "owner"}
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
# FM-030 — WHEN AN ACT OWED TO THE OWNER FALLS DUE: an ISO time with its zone, seconds optional, `Z` for UTC. The zone is not
# optional — a time without one is a different hour on every machine that reads it — and `parse_due` refuses one that has
# none. A zone's minutes are bounded here, not by `fromisoformat`, which reads `+05:99` as `+06:39` on 3.9 and 3.14
# alike (the pass's R8); its hours are refused there from 24 up.
DUE_SHAPE = r"\d{4}-\d{2}-\d{2}T(?:[01]\d|2[0-3]):\d{2}(?::\d{2})?Z?(?:[+-]\d{2}:[0-5]\d)?"     # hour 24 refused (R5); a zone's minutes 00–59 (R8)
WINDOW_DEFAULT = 60           # minutes after `due:` in which the act can still be done; past it with no `done:`, it is missed
NOTIFY_AHEAD = 30             # minutes before `due:` that `--notify` posts an act, and its invite's alarm rings (FM-030 D)
# WHAT AN ASK MUST BE, in numbers. The flow held only while every agent had read the contract and chose to obey it;
# these are the same sentences, held by the gate instead (FM-008). They are deliberately generous: an ask that trips
# one of them is not borderline, it is a paragraph, a second question, or a question already asked.
ASK_MAX = 300              # characters — past this it is not a sentence they can answer in a sitting; the detail is the body's
ASK_OPTIONS_MAX = 5        # choices — a radio list they read once, not a menu
ASK_OPTION_MAX = 120       # characters per choice — a choice is a phrase, not its rationale
BOTTLENECK = 5             # more asks than this in their queue and the queue itself is the finding, said in the first line
# the three lines an ask carries besides the question itself, each with what it is FOR — a refusal that only names a
# key sends the agent to the schema; one that says what the key is for is answerable where it is read.
ASK_NEEDS = {"ask-kind": "which of the four kinds it is", "ask-since": "the day it was first made — its age is what they see",
             "ask-proposal": "the one the seat RECOMMENDS, and would act on"}
def front_matter_schema():
    return {
        "id":              (_IDS, "all", "the filing seat", "the tracker's id — the filename's, checked against it"),
        "status":          ("|".join(OPEN_STATUSES[:-1] + ("Shipped", "Closed")), "all", "the seat that changes it",
                            "the code lifecycle, one word — `Shipped` means merged, not deployed, and a move to it names the commit that built it in the ship log (the gate refuses one that does not); a date belongs in the body"),
        "hook":            (None, "open", "the filing seat", "the problem as filed, in two or three sentences — the INDEX row"),
        "epic":            (_IDS, False, "the filing seat, or a triage pass", "the STORY this tracker is a chapter of — a tracker id; chapters inherit its `intent:`"),
        "tags":            (None, False, "the filing seat", "at most %d from the vocabulary in the configuration's [tags]" % MAX_TAGS),
        "blocked-by":      (rf"(?:{_IDS}|{_OWNER})(?:\s*,\s*(?:{_IDS}|{_OWNER}))*", False, "any seat",
                            "what this open work waits on — tracker ids, and `Owner` or `Owner — <the ruling awaited>`. *Blocked* is derived from it and clears itself; it orders nothing"),
        "considered":      (rf"none|{_IDS}(?:\s*,\s*{_IDS})*", False, "the filing seat", "the existing trackers this filing was held against — listed means LOOKED AT, not merged — or none. Triage at intake: run `--related` first; the gate refuses a new tracker without this line"),
        "ask":             (None, False, "the seat that needs the Owner", "what is asked of the Owner, as ONE sentence they can answer — with `next: owner`. The board's first line is built from these; an ask buried in the body waits longest"),
        "ask-kind":        ("ruling|action|determination|ceremony", False, "the seat that needs the Owner", "ruling — a decision of intent · action — hands only the Owner has · determination — evidence could settle it · ceremony — reserved by rule, not by risk. "
                                                                        "An ask whose yes needs the Owner's hands is `action`, whatever else it decides"),
        "ask-since":       (r"\d{4}-\d{2}-\d{2}", False, "the seat that needs the Owner", "the day the ask was first made — its age is what the Owner sees"),
        "ask-proposal":    (None, False, "the seat that needs the Owner", "the one the seat RECOMMENDS, and why — one sentence; it is offered first. With `ask-options:` it must be one of them. Never acted on without the answer"),
        "ask-options":     (None, False, "the seat that needs the Owner", "the choices the ask offers, ONE line separated by ` | ` — the Owner picks one, or writes their own under *Other*"),
        "answer":          (None, False, "the Owner — in their own commit", "their answer to `ask:`, in their words: `accepted`, `accepted - <the option they chose, or their change>`, or `rejected - <why, and how to reword the ask>` "
                                                                        "(a hand's ` — ` reads as ` - `). Written by them, never by the seat that asked; an answered ask leaves their queue. "
                                                                        "The word is the button's and stays as signed: every reading — the board's tracker view, `--answered`, the record `--clear-ask` writes — "
                                                                        "computes the answer's relation to `ask-proposal:` and `ask-options:` and prints it beside it: accepted the proposal · chose option N · "
                                                                        "accepted with a change · rejected · revoked · relation not computable, where there is no proposal to compare it with. "
                                                                        "Never overwritten in place: `--answer <id> revoke \"<reason>\"` makes it `revoked - <reason>`, and `--answer <id> accept|reject \"<option>\" --supersede` replaces it — "
                                                                        "either moves the answer it replaces into the ship log, with the commit that wrote it, and the board says *supersedes <sha>*. "
                                                                        "Until their merge, an answer on an `answer/<id>` not merged into the default branch reads *answered, on its way* on the board, in "
                                                                        "`--owner` and in `--standup`, and the ask leaves their queue (FM-030); `--revoke <id> \"<why>\"` takes it back there, on top of it"),
        "answered":        (r"\d{4}-\d{2}-\d{2}", False, "the Owner", "the day they answered — the commit that carries it is the clock"),
        "answered-by":     (None, False, "the Owner", "who answered; the commit's author is the proof, this is the label"),
        "due":             (DUE_SHAPE, False, "the seat that schedules an act owed to the Owner — with the action ask, or when its time is set; `--answer`, from an accepted "
                                           "action answer that names its hour; the Owner's `--due` moves it",
                            "when the Owner's act falls due (FM-030): an ISO time with its zone, `2026-09-26T07:30:00+02:00`. Until `done:` is written the act is on their "
                            "board — due, overdue, missed — and in INDEX.md with this time. `--clear-ask` leaves it: the answer is a promise, the act is still owed. "
                            "`--answer` writes it with an accepted action answer whose promise names a date with its hour — `2026-09-26 09:00`, "
                            "`2026-09-26T09:00+02:00`, or the weekday with its month and day, `Sat 09-26 09:00`, the next such day on or after the answer, "
                            "its weekday checked — in the zone it names (an offset, `Z`, `UTC`, `GMT`, or this machine's own name for its zone, `CEST`), "
                            "else this machine's zone; a weekday alone, a month and day with neither year nor weekday, a zone name this machine does not "
                            "carry, a word after the time that is no zone as written (`cest`), a 12-hour time (`9:00 PM`), a fraction of a second "
                            "(`09:00:00.000Z`), or two times are not read — nothing rather than a wrong hour — and the act shows *no date yet*. "
                            "A `due:` already set is left, and `--answer` says so. Moved by the Owner's `--due` and not merged yet, the new time is "
                            "their act on its way: the board, `--owner` and `--standup` read it from `origin/answer/<id>` as *rescheduled, on its way — "
                            "due <time>*, and the act leaves their list of acts until the merge — a `--due` after a done act too, never *done revoked*"),
        "window":          (r"\d{1,4}", False, "the seat that schedules the act", f"minutes after `due:` in which the act can still be done — {WINDOW_DEFAULT} where absent; past it with no `done:`, the act is missed"),
        "done":            (r'"?' + DUE_SHAPE + r' · .+"?', False, "the Owner's `--done`; their `--revoke` removes it",
                            "the act's result: when, and where it is — `<ISO time> · <a path or a pointer>`; the act leaves their list, its record stays under `## Acts`, "
                            "and where their answer left `next: owner`, `--done` sets `next: build` — the act done, the seat's move is next. The person gives the path; "
                            "the record gathers the facts: for a file in the repository, the commit that added it and its date, and for a review — a file "
                            "that states a verdict — its word, the `Reviewed:` sha and the `Session:` of its last pass: the last line that states a verdict, "
                            "that pass's own lines, else the trailers of the newest commit that touched the file, named as *last pass in* where it is not "
                            "the one that added it; a line anchor after the path (`file.md:12`, `#L1-L9`) is kept as given and not read as its name; "
                            "a word that names no file there is recorded as given, *not in the repository* beside it; nothing is guessed. The time is when the act "
                            "was recorded, not the act's own, which is in the evidence its path names. Until their merge, a `done:` on an `answer/<id>` not merged "
                            "reads *done, on its way* and the act leaves their list (FM-030); `--revoke <id> \"<why>\"` takes it back — `done:` leaves, the "
                            "revocation is recorded under `## Acts`, the act is owed again — on that branch, on top of it"),
        "intent":          (None, False, "the Owner's words only", "for · so that · never — on a story; its chapters inherit it"),
        "triaged":         (r"\d{4}-\d{2}-\d{2}", False, "a triage pass", "the day a pass last gave it a verdict"),
        "tier":            (r"P[0-3]", False, "a triage pass", "how much it matters, judged against the Owner's current path"),
        "rank":            (r"\d+", False, "a triage pass", "working order, 1–%d — the first item to work on next" % RANK_MAX),
        "next":            ("|".join(MOVES), False, "the seat that ends work; `--answer`, with the answer; a pass only where none was left", "the next move — who or what moves it next. `--answer` writes it with the answer: `build` for a ruling, a determination or a ceremony — the seat's move follows; "
                                                                                                         "`owner` kept for an action, whose act is still the Owner's"),
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


def answer_fields(fm):
    """The lines an answer's relation is read from — `ask-proposal:`, `ask-options:`, `answer:`, and the `ask:` a record is
    matched on — as the loader reads them: the outer quotes off, the options split. ONE reader, for a tracker as it is and
    for the revision its answer's commit left (`recover_relations`, FM-029)."""
    unquote = lambda v: v[1:-1] if len(v) > 1 and v[0] == v[-1] == '"' else v
    return {
        "ask": unquote((fm.get("ask") or "").strip()),
        "ask_proposal": unquote((fm.get("ask-proposal") or "").strip()),
        # the choices as ONE line — `a | b | c`. Split here so the board and the gate read the same list
        "ask_options": [o.strip() for o in unquote((fm.get("ask-options") or "").strip()).split("|") if o.strip()],
        "answer": unquote((fm.get("answer") or "").strip()),
    }


def extract(path, text=None):
    """One tracker as the loader reads it — from its file, or from `text`: the file as a revision had it (FM-033's gate reads
    the named tracker at a commit's parent through this one reader)."""
    text = path.read_text(encoding="utf-8") if text is None else text
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
        "key_problems": guarded_key_problems(tracker_id, text),    # a key a right is judged on, repeated or in capitals (`lint` refuses it)
        "next": (fm.get("next") or "").strip().lower(),
        "ask_kind": (fm.get("ask-kind") or "").strip().lower(), "ask_since": (fm.get("ask-since") or "").strip(),
        **answer_fields(fm),                            # ask · ask_proposal · ask_options · answer
        "answered": (fm.get("answered") or "").strip(),
        # an act owed to the Owner (FM-030): when it falls due, its window, its result
        "due": (fm.get("due") or "").strip(), "window": (fm.get("window") or "").strip(),
        "done": (lambda v: v[1:-1] if len(v) > 1 and v[0] == v[-1] == '"' else v)((fm.get("done") or "").strip()),
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
        # the relation the newest of those records carries (FM-029) — what `--answered` says an acted-on answer was
        "asks_relation": recorded_relation(body),
        # …and, where that record carries none (written before 0.18.1), its answer: what `recover_relations` looks up in
        # git when the relation is printed — never here, where every load passes (FM-012)
        "asks_answer": unrelated_answer(body),
        # …and every record's that carries none, the newest's among them — each read back from its own answer's commit
        "asks_answers": unrelated_records(body),
        "asks_key": record_key(body[slice(*newest_record(body))]),
        # the answer this one replaced — the commit of the newest ship-log row `--answer … revoke|--supersede` writes
        "supersedes": superseded(body),
        # the lines under `## Raised` — read here, the one place the body is read; which of them re-open the tracker to a
        # pass is decided by `mark_raised`, which sees the path and every answer
        "raises": raise_lines(body),
    }


def raise_lines(body):
    """The raises under the body's `## Raised` — one bullet each, `- <date> · <who> · <fact> · <source> · undermines: <what>`
    — as {date, line, undermines: [what it names]}. Keyed on the date that opens the bullet and on the `undermines:` token
    wherever it sits, never on a count of fields: FM-007's line joins its fact and its source with a dash. A bullet wrapped
    onto indented lines is read whole."""
    at = RAISED_HEAD_RE.search(body)
    if not at:
        return []
    rest = re.search(r"^#{1,3}\s+", body[at.end():], re.M)
    bullets = []
    for line in body[at.end(): at.end() + (rest.start() if rest else len(body) - at.end())].splitlines():
        if re.match(r"\s*[-*]\s", line):
            bullets.append(line.strip()[1:].strip())
        elif bullets and line.strip() and line[:1].isspace():
            bullets[-1] += " " + line.strip()
        elif not line.strip() and bullets:
            bullets.append(None)                            # a blank line ends a bullet; nothing more is joined to it
    out = []
    for b in filter(None, bullets):
        m, u = re.match(r"(\d{4}-\d{2}-\d{2})\b", b), re.search(r"\bundermines:\s*([^·]+)", b, re.I)
        if m:
            out.append({"date": m.group(1), "line": b, "undermines": [w.strip() for w in u.group(1).split(",") if w.strip()] if u else []})
    return out


def is_new_filing(t):
    """Open work filed under the `considered:` rule that no pass has ever dated — it has met no second reader."""
    return (t["status"] in OPEN_STATUSES and not t.get("triaged")
            and t.get("num", 0) >= CONSIDERED_FROM.get(t.get("kind"), 10 ** 9))


def owed_a_pass(t):
    """The ONE definition of what a triage pass reads, clock aside: `In Progress` work, a new filing, and a tracker a raise
    re-opened (`mark_raised`). The worksheet and the board both ask it, so the Owner's page never says *84 to triage*
    while the command says *0 trackers to judge*. Older `Proposed`, `Reserved` and `Parked` work is backlog: the current
    path restarts it, not a clock."""
    return t["status"] == "In Progress" or is_new_filing(t) or bool(t.get("raised"))


def board(t):
    """the ONE definition of where a tracker sits on the board; INDEX.md and the dashboard both
    print it. Clock-free, so a committed file never changes because a day passed. The one clock rule — a
    judgement older than TRIAGE_DAYS counts as `triage` again — lives in the page and in the worksheet.
    Open work with a rank sits in `progress` whatever its status (`In Progress` or `Proposed`, the two a rank may stand on — `lint`); the
    open unranked is `backlog`, `triage` keeps its precedence over both, and the sections sort by rank, then tier."""
    if t["status"] not in ("In Progress", "Parked", "Proposed", "Reserved", "?"):
        return "ended"                                               # shipped or closed — a closed tracker is not "done" (FM-005)
    if t.get("raised") or (not t.get("triaged") and owed_a_pass(t)):     # a raise on a signed rule re-judges it (FM-033)
        return "triage"
    # a status is what a seat set; a rank is what a pass judged (FM-041) — the ranked open work is the working set, whatever its status
    return "progress" if t["status"] == "In Progress" or (t.get("rank") and t["status"] == "Proposed") else "backlog"


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
        out.append(f'`ask:` is {len(ask)} characters — an ask they answer in a sitting is at most {ASK_MAX}; the detail belongs in the body')
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
    question, and a draft (`next: review`) never reaches them at all."""
    today = datetime.date.today()
    by_ask = asks_by_key(trackers)
    age = lambda t: (today - datetime.date.fromisoformat(t["ask_since"])).days if re.fullmatch(r"\d{4}-\d{2}-\d{2}", t.get("ask_since") or "") else None
    q = [(t, age(t), held_up_by(t, trackers)) for t in trackers
         if t["status"] in OPEN_STATUSES and t.get("next") == "owner" and not t.get("answer") and not ask_problems(t, by_ask)]
    return sorted(q, key=lambda r: (-(r[1] if r[1] is not None else -1), r[0]["id"]))


def malformed_asks(trackers):
    """The third layer: what was sent to the Owner and is not a question they can answer — (tracker, reasons), by id.
    The gate already refuses each of these; this is what the board, `--owner` and `--standup` show when one got in
    anyway — on a merge, under `--no-verify`, or from an agent that never ran the gate."""
    by_ask, out = asks_by_key(trackers), []
    for t in sorted(trackers, key=lambda t: t["id"]):
        why = ask_problems(t, by_ask) if t["status"] in OPEN_STATUSES and t.get("next") == "owner" and not t.get("answer") else []
        if why:
            out.append((t, why))
    return out


def bottleneck(q):
    """The one line the Owner is owed when their queue is the finding — not a tracker's problem, theirs."""
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


# FM-029 — THE ANSWER'S RELATION TO THE PROPOSAL, computed where the answer is read. The signed line keeps the button's
# word: under `accepted` the board and `--answer` write the proposal, another listed option and changed text alike, and a
# reader counting how often the Owner took the seat's proposal counted every one of them as agreement. The line is never
# rewritten; every reading names the relation beside it — the Owner's ruling of 2026-09-24: the relation only, no new verbs.
RELATION_TEXT = {"proposal": "accepted the proposal", "changed": "accepted with a change", "option": "chose option {0}",
                 "rejected": "rejected", "revoked": "revoked", "unknown": "relation not computable"}
RELATION_QUOTE = 40        # characters of an option or a reason the relation quotes — its first words, cut between two
# the answer's word and its text: ` - ` as `--answer` and the board write it, ` — ` as the schema once told a hand to
ANSWER_WORD_RE = re.compile(r"(accepted|rejected|revoked)(?:\s+[-—]\s+(.+))?", re.I | re.S)


def answer_norm(text):
    """What `--answer` does to the text it writes, and the board's dialog to the option it picks: trimmed, every run of
    whitespace one space, `"` written as `'`. Applied to BOTH sides of a comparison — a plain equality test read the
    proposal itself as changed text whenever it held a double quote or a double space."""
    return " ".join(str(text or "").replace('"', "'").split())


def first_words(text, limit=RELATION_QUOTE):
    """The opening of an option or a reason, cut between two words — what the relation quotes of it."""
    return text if len(text) <= limit else text[:limit].rsplit(" ", 1)[0].rstrip(" ,;:—-") + "…"


def answer_relation(t):
    """What the answer did with the proposal, read from `answer:` against `ask-proposal:` and `ask-options:` — the
    answer's own normalisation on both sides — as (kind, n, words), or None where there is no answer:
    - `proposal` — `accepted`, bare, or with the proposal's text;
    - `option`, n — the text is option n of `ask-options:` (its place there, from 1) and not the proposal; words: its opening;
    - `changed` — accepted, and the text is neither the proposal nor any option;
    - `rejected` · `revoked` — words: the reason's opening;
    - `unknown` — nothing to compare it with (an accepted answer on an ask with no proposal, or none and no options), or a
      word that is none of the three. Never a guess.
    The signed line is not touched: the relation is computed each time it is read."""
    answer = answer_norm(t.get("answer"))
    if not answer:
        return None
    m = ANSWER_WORD_RE.fullmatch(answer)
    if not m:
        return ("unknown", 0, "")
    word, text = m.group(1).lower(), (m.group(2) or "").strip()
    if word != "accepted":
        return (word, 0, first_words(text))
    proposal, options = answer_norm(t.get("ask_proposal")), [answer_norm(o) for o in t.get("ask_options") or []]
    if proposal and text in ("", proposal):
        return ("proposal", 0, "")
    if text and text in options:
        return ("option", options.index(text) + 1, first_words(text))
    return ("changed", 0, "") if text and (proposal or options) else ("unknown", 0, "")


def relation_text(rel):
    """The relation as a reader reads it — `chose option 3: the verbs only` — or "" where there is no answer."""
    return RELATION_TEXT[rel[0]].format(rel[1]) + (f": {rel[2]}" if rel[2] else "") if rel else ""


RELATION_LINE_RE = re.compile(r"^\*\*relation\*\* — (.+)$", re.M)     # the line `--clear-ask` writes under `**answered** —`


def record_spans(body):
    """Where each record under the body's `## Asks` stands — one paragraph each, as `--clear-ask` writes them, oldest first —
    as [(start, end)] in `body`."""
    at = ASKS_HEAD_RE.search(body)
    if not at:
        return []
    rest = re.search(r"^#{2,3}\s+", body[at.end():], re.M)
    section = body[at.end(): at.end() + (rest.start() if rest else len(body) - at.end())]
    return [(at.end() + m.start(), at.end() + m.start() + len(m.group(0).rstrip()))
            for m in re.finditer(r"(?:^[^\n]*\S[^\n]*(?:\n|$))+", section, re.M)]


def newest_record(body):
    """Where the newest record under the body's `## Asks` stands — the section's last paragraph — as (start, end) in
    `body`; (0, 0) where there is none."""
    spans = record_spans(body)
    return spans[-1] if spans else (0, 0)


def record_answer(record):
    """The answer of one record under `## Asks` when it has no `**relation** —` line — a record `--clear-ask` wrote before
    0.18.1 — else "": the text the commit that wrote it is found by. Its line is `**answered** — <answer> · <answered-by>`."""
    m = None if RELATION_LINE_RE.search(record) else re.search(r"^\*\*answered\*\* — (.+)$", record, re.M)
    if not m:
        return ""
    answer, sep, _by = m.group(1).strip().rpartition(" · ")
    return answer if sep else m.group(1).strip()


def recorded_relation(body):
    """The relation the newest record under `## Asks` carries — `--clear-ask` writes it from 0.18.1 on — or, for a record
    written before, *relation not computable*: the proposal and the options left with the ask, and the file cannot say it.
    Where it is printed, `record_relation` recovers it from the answer's own commit; read from the body alone, it is this."""
    start, end = newest_record(body)
    if "**answered**" not in body[start:end]:
        return ""
    m = RELATION_LINE_RE.search(body[start:end])
    return m.group(1).strip() if m else RELATION_TEXT["unknown"]


def unrelated_answer(body):
    """The answer of the NEWEST record under `## Asks` when it has no `**relation** —` line, else "" — what `--answered`'s
    acted-on line prints the relation of."""
    start, end = newest_record(body)
    return record_answer(body[start:end])


def record_key(record):
    """What one record under `## Asks` without its `**relation** —` line is matched on — its question, from its
    `**<date>** · <question>` line, and its answer, each with the answer's normalisation — or None."""
    answer = record_answer(record)
    if not answer:
        return None
    m = re.match(r"\s*\*\*[^*\n]+\*\* · (.+)$", record, re.M)
    return (answer_norm(m.group(1)) if m else "", answer_norm(answer))


def unrelated_records(body):
    """EVERY record under `## Asks` that has no `**relation** —` line, oldest first, each (question, answer) once — what
    the board's tracker view prints a recovered relation under (the cold second pass's R2: FM-031's older record)."""
    return list(dict.fromkeys(k for k in (record_key(body[s_:e_]) for s_, e_ in record_spans(body)) if k))


def recover_relations(trackers):
    """FM-029, the Owner's scope — every reading prints the relation — for a record `--clear-ask` wrote before 0.18.1: it
    has no `**relation** —` line, and the proposal and the options left the file with the ask. The commit that wrote the
    answer still holds them. Found, never guessed: the commits whose diff adds an `answer:` line equal to the record's
    answer (the answer's own normalisation on both sides), each read back with `git show`; the ONE whose revision holds
    that `answer:` under that record's question (`ask:` against the record's `**<date>** · <question>` line) is the
    answer's commit, and its lines go through `answer_fields` and `answer_relation`, the reader a live answer goes
    through. The same answer text can close two exchanges — FM-007 was answered twice, word for word, on 09-22 — and
    the newest commit with the text gave an older record the newer answer's relation and commit (the cold third pass's
    R1): the question decides, and where no commit, or more than one, holds both, *relation not computable* — never a
    guess. Under Subversion, not computable too. Every record without the line, not only the newest (the second pass's
    R2). Sets `t["asks_recovered_all"]` = {(question, answer): (relation, the commit's short sha)} and
    `t["asks_recovered"]` = the newest record's.

    Cost, and why it is spent only here: one `git log` for ALL the records asked about at once, and one `git show` per
    commit that wrote a record's answer text — one per record, but for text reused. `extract` never calls it — every
    load, the pre-commit hook's included, would pay; FM-012 measured one git call per tracker at 504 calls and 15.2 s of a 16.8 s load. It runs where the relation is
    printed (`--answered`'s acted-on lines, the board's tracker view), and only for a record that lacks the line. The one
    `git log` is not one per record because each walks the whole history: 0.4 s a file on a 3,755-commit repository."""
    need = {}
    for t in trackers:
        if (t.get("asks_answers") or t.get("asks_key")) and "asks_recovered_all" not in t:
            wanted = list(dict.fromkeys(k for k in (t.get("asks_answers") or []) + [t.get("asks_key")] if k))
            t["asks_recovered_all"] = {k: (RELATION_TEXT["unknown"], "") for k in wanted}
            need[(TRACKER_DIR / t["file"]).resolve().relative_to(ROOT).as_posix()] = t
    try:
        if not need or vcs() != "git":
            return
        recover_from_log(need)
    finally:
        for t in need.values():
            t["asks_recovered"] = t["asks_recovered_all"].get(t.get("asks_key"), (RELATION_TEXT["unknown"], ""))


def recover_from_log(need):
    """`recover_relations`' git work: {path relative to ROOT: tracker} — one `git log` for all of them, one `git show` per
    commit that wrote a wanted answer's text."""
    git = lambda *a: subprocess.run(["git", "-c", "core.quotePath=false", *a], cwd=ROOT, capture_output=True, text=True, encoding="utf-8",
                                    errors="replace", env=nested_git_env())
    # `-G ^answer:` anchored as `line_regex` anchors it; `--full-history` as `acted_on` has it — an answer written on a
    # branch that merged back to content the trunk already had is not walked past; the prefixes named, whatever the
    # user's `diff.noprefix`; paths relative to ROOT, as `need` holds them and `git show <sha>:./<path>` reads them;
    # `-U0`: only the lines that changed
    log = git("log", "--full-history", "--no-renames", "--relative", "--no-color", "--no-ext-diff", "--src-prefix=a/", "--dst-prefix=b/",
              "-U0", "-p", "--format=%x00%H %h", "-G", line_regex("answer:"), "--", *need)
    found = {rel: {a: [] for _q, a in t["asks_recovered_all"]} for rel, t in need.items()}      # per answer text, newest first
    for chunk in log.stdout.split("\x00")[1:]:
        head, _, diff = chunk.partition("\n")
        rel = None
        for line in diff.splitlines():
            if line.startswith("diff --git "):            # `a/<path> b/<path>`: one path twice (no renames); quoted, it is none of these
                both = line[len("diff --git a/"):] if line.startswith("diff --git a/") else ""
                rel = both[: (len(both) - len(" b/")) // 2] if both else None
            elif line.startswith("+answer:") and rel in need:
                said = answer_norm(answer_fields({"answer": line[len("+answer:"):]})["answer"])
                if said in found[rel] and head not in found[rel][said]:
                    found[rel][said].append(head)
    for rel, by_answer in found.items():
        revisions = {head: answer_fields(parse_frontmatter(git("show", f"{head.partition(' ')[0]}:./{rel}").stdout)[0])
                     for head in dict.fromkeys(h for heads in by_answer.values() for h in heads)}
        for question, said in need[rel]["asks_recovered_all"]:
            holds = [(head, fields) for head, fields in revisions.items() if head in by_answer[said]
                     and answer_norm(fields["answer"]) == said and answer_norm(fields["ask"]) == question]
            if len(holds) == 1:                               # one exchange: its own commit — none, or two, and nothing is said
                need[rel]["asks_recovered_all"][(question, said)] = (relation_text(answer_relation(holds[0][1])), holds[0][0].partition(" ")[2])


def record_relation(t):
    """What every reading prints for the newest record under `## Asks`: the relation its `**relation** —` line says, or —
    for a record without one — the one `recover_relations` reads from the answer's commit, else *relation not computable*;
    as (relation, the answer's commit where it was recovered, else ""). "" for no record, or a withdrawn one. A record
    that carries its line costs no git call."""
    if t.get("asks_answer") and "asks_recovered" not in t:
        recover_relations([t])
    return t.get("asks_recovered", (RELATION_TEXT["unknown"], "")) if t.get("asks_answer") else (t.get("asks_relation", ""), "")


def answered(trackers):
    """`--answered`: what the Owner answered and nobody has acted on yet — the seat's side of the exchange; and,
    since their last sitting, what WAS acted on, named by the commit that cleared the ask."""
    rows = sorted((t for t in trackers if t.get("answer") and t["status"] in OPEN_STATUSES), key=lambda t: t.get("answered", ""))
    print(f"{len(rows)} ANSWERED, NOT YET ACTED ON" if rows else "NOTHING ANSWERED IS WAITING FOR A SEAT.")
    for t in rows:
        print(f"\n{t['id']} · answered {t['answered']} by {t['answered_by']}\n   asked: {t['ask']}\n   answer: {t['answer']}\n   relation: {relation_text(answer_relation(t))}\n   → act on it, then `{CMD} --clear-ask {t['id']} <next move>` — it moves the exchange into the body under `## {HEAD['asks']}`; the record stays, the ask goes")
    acted = acted_on(trackers)
    if acted:
        print(f"\nACTED ON SINCE THE LAST STANDUP — {len(acted)}")
        recover_relations([t for t, _ in acted])           # a record without its relation line: one `git log` for all of them
        for t, commit in acted:
            said, source = record_relation(t)
            print(f"  {t['id']} — acted on in `{commit}`" + (f" · {said}" if said else "") + (f", read from the answer's commit `{source}`" if source else ""))
    return EXIT_OK


ACTS_TITLE = "ACTS — yours, with their time"


def acts_lines(trackers, now=None):
    """FM-030 E — the acts owed to the Owner, as `--standup` and `--owner` list them after the asks: missed and overdue
    first, then what falls due, soonest first, then what has no date yet — each with its `due:` and what it is, in the
    board's words, and the day they promised it. A promise's line is what they promised, and the question it answered follows
    on the next line, as context (the Owner's word of 2026-09-27 13:38:30). [] where they owe none."""
    now = now or datetime.datetime.now(datetime.timezone.utc)
    order = {"missed": 0, "overdue": 1, "due": 2, "nodate": 3}
    acts = sorted(((t, a) for t, a in ((t, act_of(t)) for t in trackers) if a),
                  key=lambda p: (order[act_state(p[1], now)], parse_due(p[1][3]) or now, p[0]["id"]))
    return [f"  {t['id']} — {a[0]} · {act_words(a, now)}" + (" · " + LABELS["acts.promised"].format(a[2], a[1]) if a[1] else "")
            + (f"\n       {LABELS['acts.asked'].format(a[5])}" if a[5] else "") for t, a in acts]


# FM-030 — THE BOARD READS GIT: an act or an answer they just gave, before their merge. The Owner's signed answer of 2026-09-27
# 14:56:15 (920970b7), option 1 of the ask of 14:14:18, on their words of 13:57:50 — *they pushed the button, did the answer
# and expect the page to display that state right away* (spelling normalised). Their act or answer is a signed commit on
# `answer/<id>`, pushed; the default branch knows nothing of it until their merge, and the board, `--owner` and `--standup`
# were built from the checkout alone. One truth stays, git: after the push the remote-tracking ref holds the sha the tool
# committed, and another machine has it after a fetch. Nothing is written to remember it, and nothing is fetched to read it.


def on_their_way(trackers):
    """{id: reading} — every `origin/answer/<id>` this clone holds that is NOT merged into the default branch
    (`default_trunk`; one `git for-each-ref --no-merged` for all of them), whose tracker at the tip carries a `done:`, an
    `answer:` or a `due:` the default branch's copy lacks — or drops a `done:` the default branch has, where `--revoke` made
    that change. A merged branch is not read, nor one whose tip carries no such change, nor one for a tracker this checkout
    does not hold. A reading:
    - `kind` — `done` · `answer` · `revoked` (an answer that revokes) · `undone` (a `done:` revoked) · `due` (rescheduled);
      `done` first where the tip carries both. `--due` is their act as `--done` and `--answer` are (the Principal's ruling of
      2026-09-28 on RV-730): a `due:` the default branch lacks reads *rescheduled, on its way* — and so does a `--due` that
      opened a new act after a done one and dropped its `done:`. *Done revoked* reads only where the branch's own commit
      that dropped `done:` is a revocation — `--revoke`'s subject, `REVOKE_DONE_SUBJECT` —, never on a `done:` line gone;
    - `answered` — the tip carries an answer the default branch lacks: the ask leaves their waiting list, whatever the kind;
    - `owed` — the act stays on their list of acts: the tip still owes them one (`act_of`) and no new time is on its way for
      it. Where the tip owes none — done, or a promise revoked — or carries a new time, the act leaves their acts until the
      merge, and is listed here instead;
    - `due` — the `due:` at the tip where the default branch lacks it (a reschedule, or a time their promise seeded), else "";
    - `note` — what follows the label: for `done`, where its result is; for `revoked`, the reason; else "";
    - `branch`, `tip` — its head;
    - `commit` — the newest of the branch's OWN commits that changed that line, read from its commits, never from its head
      alone: a Reviewer's verdict on top of their act is no act (RV-679); `time` its committer time, `sig` its `%G?` against the
      signers the gate trusts, `said` what `--queue` reads of it — `answer_reading`, the one reader of an answer commit;
    - `held` — `--queue`'s own line for the branch where it waits on something that commit's reading does not say —
      `answer_branch_reading` against the default branch: a seat's commit below their act (RV-710), a head past it, a base
      not here — else "": the board says the wait in place of *your merge is next* (RV-714);
    - `what` — their promise, else the answer as signed; for an act, its line; for an answer revoked, the question it answered
      (the reason follows the label, RV-734); `asked` the question, as context; `value` the `done:`, `answer:` or `due:` as
      written — for `undone`, the `done:` it revokes.
    {} without git, without a default branch, or with nothing on its way. Local: no fetch, no forge — a pull request is not
    looked up, and every reading says *your merge is next*."""
    if vcs() != "git" or not trackers:
        return {}
    git = lambda *a: subprocess.run(["git", *a], cwd=ROOT, capture_output=True, text=True, encoding="utf-8", errors="replace", env=nested_git_env())
    trunk = default_trunk(git, ask=False)               # the board asks no server
    if not trunk:
        return {}
    refs = git("for-each-ref", f"--no-merged={trunk}", "--format=%(refname:lstrip=3)%00%(objectname)", "refs/remotes/origin/answer/")
    by_id, heads = {t["id"]: t for t in trackers}, []
    for line in refs.stdout.splitlines() if refs.returncode == 0 else []:
        branch, _, tip = line.partition("\x00")
        t = by_id.get(branch[len("answer/"):].upper()) if branch.startswith("answer/") else None
        if t and tip:
            heads.append((branch, tip, t["id"], (TRACKER_DIR / t["file"]).relative_to(ROOT).as_posix()))
    blobs = cat_blobs([spec for _b, tip, _i, rel in heads for spec in (f"{tip}:{rel}", f"{trunk}:{rel}")])
    out = {}
    for branch, tip, tid, rel in heads:
        there, here = blobs.get(f"{tip}:{rel}"), blobs.get(f"{trunk}:{rel}")
        if there is None:
            continue
        at, was = extract(ROOT / rel, there), (extract(ROOT / rel, here) if here is not None else {})
        answered = bool(at.get("answer")) and at["answer"] != was.get("answer")
        word = ANSWER_WORD_RE.fullmatch(answer_norm(at.get("answer")))
        due = at.get("due", "") if at.get("due") and at.get("due") != was.get("due") else ""
        newest = lambda key: git(*signers_args(), "log", "-1", "--format=%H%x00%cI%x00%G?%x00%s", "-G", line_regex(key), tip, "^" + trunk, "--", rel).stdout.strip()
        log = ""
        if at.get("done") and at["done"] != was.get("done"):
            kind, key = "done", "done:"
        elif answered:
            kind, key = ("revoked" if word and word.group(1).lower() == "revoked" else "answer"), "answer:"
        elif was.get("done") and not at.get("done") and (log := newest("done:")).split("\x00")[-1].startswith(REVOKE_DONE_SUBJECT.format(tid)):
            kind, key = "undone", "done:"                   # `--revoke` dropped it: its own commit says so, not a line gone
        elif due or (was.get("done") and not at.get("done") and at.get("due")):
            kind, key, log, due = "due", "due:", "", at.get("due", "")   # `--due`, and `--due` after a done act: a new time, never *done revoked*
        else:
            continue
        log = log or newest(key)
        if not log:                                         # the line came in through a merge on the branch: its head speaks
            log = git(*signers_args(), "log", "-1", "--format=%H%x00%cI%x00%G?", tip).stdout.strip()
        commit, when, sig = (log.split("\x00") + ["", "", ""])[:3]
        if kind in ("done", "undone", "due"):               # the act's line, and its question, as they read while it was owed
            act = act_of({**at, "done": ""})
            what, asked = (act[0], act[5]) if act else (at.get("title") or tid, "")
        elif kind == "revoked":                             # the question they take their answer back from; the reason follows the label (RV-734)
            what, asked = at.get("ask") or at.get("title") or tid, ""
        else:
            what, asked = promise_of(at) or at["answer"], at.get("ask", "")
        value = {"undone": was.get("done", ""), "done": at.get("done", ""), "due": due}.get(kind, at.get("answer", ""))
        note = value.partition(" · ")[2] if kind == "done" else (word.group(2) or "").strip() if kind == "revoked" and word else ""
        said, queue = answer_reading(commit or tip)[1], answer_branch_reading(tip, trunk)[1]     # the act's commit, and `--queue`'s line (RV-714)
        out[tid] = {"kind": kind, "answered": answered, "owed": act_of(at) is not None and not due, "branch": branch, "tip": tip, "commit": commit or tip, "time": when, "sig": sig or "N",
                    "said": said, "held": queue if queue.startswith("wait") and queue != said else "", "what": what, "asked": asked if asked != what else "", "value": value, "due": due, "note": note}
    return out


WAY_TITLE = "ON THEIR WAY — yours, signed and pushed, before your merge"
# the subject `--revoke` gives the commit that takes back an act done — `on_their_way` reads *done revoked* on it, and on nothing else
REVOKE_DONE_SUBJECT = "{0}: done revoked — "


def way_lines(way):
    """FM-030 — what `--owner` and `--standup` print of `on_their_way`, in the board's words (`way.*`), by id: their promise
    or their answer first, what it is — *done, on its way* or *answered, on its way* —, the branch, the commit and its time,
    whether it verifies, *your merge is next* — or, where `--queue` waits on the branch for more than the act's own
    signature, *your merge waits: <its wait>* (RV-714); the question below it, as context. After the label: where the
    result is, the reason of a revocation, or the new time — *rescheduled, on its way — due <time>*. [] where nothing is
    on its way."""
    said = lambda w: (LABELS["way.signed"] if w["said"].startswith("merge") else LABELS["way.unverified"].format(re.sub(r"^wait: ", "", w["said"])))
    held = lambda w: LABELS["way.held"].format(re.sub(r"^wait: ", "", w["held"])) if w.get("held") else LABELS["way.merge"]
    after = lambda w: f" — {w['note']}" if w.get("note") else f" — {LABELS['acts.due'].format(w['due'].replace('T', ' '))}" if w.get("due") else ""
    return [f"  {tid} — {w['what']} · {LABELS['way.' + w['kind']]}" + after(w)
            + f" · {w['branch']} @ {w['commit'][:7]} · {w['time'][:16].replace('T', ' ')} · {said(w)} · {held(w)}"
            + (f"\n       {LABELS['acts.asked'].format(w['asked'])}" if w["asked"] else "") for tid, w in sorted(way.items())]


def owed_now(trackers, way):
    """The asks and the acts still theirs, with `on_their_way` read: an ask whose answer is on its way leaves their queue, an act
    the tip no longer owes — done, or a promise revoked — or whose new time is on its way leaves their acts; both are in
    `way_lines` instead. (queue, acts lines)."""
    return ([r for r in owner_queue(trackers) if not way.get(r[0]["id"], {}).get("answered")],
            acts_lines([t for t in trackers if way.get(t["id"], {}).get("owed", True)]))


def owner_digest(trackers):
    """`--owner`: the digest — what a session's last message leads with. It arrives; a board has to be opened. After the
    asks, the acts they owe, with their time, and what they did that is on its way to their merge (FM-030)."""
    way = on_their_way(trackers)
    (q, acts), ways = owed_now(trackers, way), way_lines(way)
    if not q:
        print("NOTHING NEEDS THE OWNER." if not (acts or ways) else "NO QUESTION FOR THE OWNER" + (f" · {len(acts)} ACT(S) OWED, WITH THEIR TIME" if acts else "")
              + (f" · {len(ways)} ON THEIR WAY — YOUR MERGE IS NEXT" if ways else ""))
    else:
        ages, held, line = [a for _, a, _ in q if a is not None], sorted({h for _, _, hs in q for h in hs}), bottleneck(q)
        print(f"{len(q)} NEED THE OWNER" + (f" · oldest {max(ages)} day(s)" if ages else "") + (f" · holding up {len(held)}: {', '.join(held)}" if held else "")
              + (f" · {line}" if line else "") + (f" · {len(ways)} on their way" if ways else ""))
        for t, a, hs in q:
            print(f"\n{t['id']}" + (f" · {t['ask_kind']}" if t.get("ask_kind") else "") + (f" · asked {a} day(s) ago" if a is not None else "") + (f" · holds up {', '.join(hs)}" if hs else ""))
            print("   " + t["ask"])
    if acts:
        print(f"\n{ACTS_TITLE}\n" + "\n".join(acts))
    if ways:
        print(f"\n{WAY_TITLE}\n" + "\n".join(ways))
    sent_back(trackers)
    line = sessions_digest()
    if line:
        print("\n" + line)
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
        f = lambda d: d.strftime("%Y%m%dT%H%M%S")                # floating time: the Owner's own clock, wherever they are
        lines = ["BEGIN:VCALENDAR", "VERSION:2.0", "PRODID:-//shoalmark//standup//EN", "BEGIN:VEVENT",
                 f"UID:standup-{hashlib.sha256(name.encode()).hexdigest()[:16]}@shoalmark", f"DTSTAMP:{f(datetime.datetime(2000, 1, 1))}Z",
                 f"DTSTART:{f(start)}", f"DTEND:{f(end)}", "RRULE:FREQ=WEEKLY;BYDAY=MO,TU,WE,TH,FR",
                 f"SUMMARY:{name} — standup: what needs you", f"DESCRIPTION:Run `{CMD} --standup` — or open the board: its first lines are the agenda.",
                 "END:VEVENT", "END:VCALENDAR"]
        named = pathlib.Path(invite).absolute()
        out = pathlib.Path(os.path.realpath(named.parent)) / named.name      # a destination a person names: its folder resolved once, where it is named
        write_rule(named)                                   # the write rule, as the path is named; `put` asks it again where it resolves
        put(out, "\r\n".join(lines) + "\r\n")              # a calendar file ends its lines with CRLF, on every system — `put` writes them as they are
        print(f"wrote {invite} — weekdays {at}, {int(CONFIG.get('standup_minutes') or 15)} minutes; import it into the Owner's calendar")
        return EXIT_OK
    way = on_their_way(trackers)
    (q, acts), ways = owed_now(trackers, way), way_lines(way)
    line = bottleneck(q)
    print(f"STANDUP{' — ' + at if at else ''} · {int(CONFIG.get('standup_minutes') or 15)} min · {len(q)} item(s)" + (f" · {len(acts)} act(s)" if acts else "")
          + (f" · {len(ways)} on their way" if ways else "") + ("" if q or acts or ways else " — nothing needs the Owner today.") + (f"\n{line}" if line else ""))
    for kind, title in STANDUP_ORDER:
        rows = sorted((r for r in q if (r[0].get("ask_kind") or "") == kind), key=lambda r: (-len(r[2]), -(r[1] if r[1] is not None else -1), r[0]["id"]))
        if rows:
            print(f"\n{title}")
        for n, (t, a, hs) in enumerate(rows, 1):
            print(f"  {n}. {t['id']} — " + t["ask"] + (f"  [{a} day(s)]" if a is not None else "") + (f"  [frees {', '.join(hs)}]" if hs else ""))
    if acts:                                                # FM-030: after the asks, what they owe, with its time
        print(f"\n{ACTS_TITLE}\n" + "\n".join(acts))
    if ways:                                                # …and what they did that is on its way to their merge
        print(f"\n{WAY_TITLE}\n" + "\n".join(ways))
    sent_back(trackers)
    return EXIT_OK


# a ship-log row `--answer … revoke` or `--supersede` writes: `| <date> | Answer of <answered> superseded: *"<answer>"* (<sha>) — …`
SUPERSEDED_RE = re.compile(r'\|\s*(\d{4}-\d{2}-\d{2})\s*\|\s*Answer of [^|]*?superseded: \*".*?"\* \(([0-9a-f]{7,40})\)')


# FM-031 S2 — THE QUEUE IN ONE VIEW. The streams run in parallel, and only the Owner saw the whole queue of pull requests:
# they were the integrator by default. They asked one seat which to merge five times in two hours, and each answer was the
# forge and `git merge-tree`, read by hand. `--queue` reads the same two and gives every open pull request ONE action, in
# the order they take them. A view: it refuses nothing, and where the forge cannot be read it says so in one line.
QUEUE_FIELDS = "number,title,headRefName,headRefOid,baseRefName,mergeable,mergeStateStatus,createdAt,isCrossRepository"
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


def pushed_branches(prs):
    """The branches on `origin` that no pull request carries — what the forge's banner offers the Owner, and nothing else
    showed them: every head `git ls-remote` names, less the default branch, `answer/*`, an open pull request's branch, a
    head any pull request ever had (the forge's `refs/pull/N/head`, open or closed), and a head already inside the
    default branch, an open pull request's head, or another such branch's head (of twins with one head, the first by
    name stays). A head this clone never fetched — a single-branch clone fetches one — is fetched here, by its ref;
    one still missing stays, marked, and is read as *not fetched here*. [{name, sha, base, here}], by name."""
    out = git_out("ls-remote", "--symref", "origin", "HEAD", "refs/heads/*", "refs/pull/*/head")
    if out is None:
        return []
    heads, pulled, default = {}, set(), ""
    for line in out.splitlines():
        sha, _, ref = line.partition("\t")
        if sha.startswith("ref: refs/heads/") and ref == "HEAD":
            default = sha[len("ref: refs/heads/"):]
        elif ref.startswith("refs/heads/"):
            heads[ref[len("refs/heads/"):]] = sha
        elif ref.startswith("refs/pull/"):
            pulled.add(sha)
    default = default or next((b for b in ("main", "master") if b in heads), "")
    if not default:
        return []
    inside = lambda a, b: git_out("merge-base", "--is-ancestor", a, b) is not None
    carried = {p["headRefName"] for p in prs} | {p["headRefOid"] for p in prs} | pulled
    named = [(name, sha) for name, sha in sorted(heads.items())
             if name != default and not name.startswith("answer/") and name not in carried and sha not in carried]
    lacking = set(have_not([sha for _n, sha in named]))
    if lacking:                                             # the one fetch for heads the configured refspec does not cover
        git_out("fetch", "--quiet", "origin", *[f"refs/heads/{name}" for name, sha in named if sha in lacking])
    gone = set(have_not(sorted(lacking)))
    kept = [(name, sha) for name, sha in named if sha in gone
            or not (inside(sha, f"refs/remotes/origin/{default}") or any(inside(sha, p["headRefOid"]) for p in prs))]
    kept = [(name, sha) for name, sha in kept if sha in gone or not any(
        (other != sha and inside(sha, other)) or (other == sha and o_name < name) for o_name, other in kept if other not in gone)]
    return [{"name": name, "sha": sha, "base": default, "here": sha not in gone} for name, sha in kept]


def have_not(shas):
    """The commits of these that this clone does not have — one `git cat-file --batch-check` for all of them."""
    if not shas:
        return []
    r = subprocess.run(["git", "cat-file", "--batch-check"], input="".join(f"{s_}^{{commit}}\n" for s_ in shas), cwd=ROOT,
                       capture_output=True, text=True, encoding="utf-8", errors="replace", env=nested_git_env())
    return [s_ for s_, line in zip(shas, r.stdout.splitlines()) if line.endswith(" missing")]


def answerer_of(commit):
    """(whether the author of `commit` may answer — the gate's own match, email or name —, that author as the queue names
    one — the email, else the name —, the configured identity they answer as, which a signature must name: `answerer_identity`)"""
    name, _, email = (git_out("log", "-1", "--format=%an%x01%ae", commit) or "").strip().partition("\x01")
    return (holds(seat_of(name, email), "answer") if SEATS else name in may_answer()), email or name or "no author", answerer_identity(name, email)


def answers_as_him(commit):
    """`commit` is theirs: its author may answer and it verifies as them — the gate's one test, `verified_as`, as
    `answer_reading` applies it to the commit an `answer/*` pull request is read by (FM-031, RV-710)"""
    may, _who, identity = answerer_of(commit)
    return may and verified_as(commit, identity)


def review_addendum():
    """(path, own) → whether a commit may touch `path` and still be a review addendum, as `--queue` reads one (FM-031,
    0.18.4): the review folder — `[paths] reviews`, `evidence/reviews/` by default, a glob allowed —, the registry
    `<tracker dir>/sessions.md`, and where `own`, a `review*.md` anywhere under `<tracker dir>/evidence/` — the verdict
    commit's own file"""
    rel = TRACKER_DIR.relative_to(ROOT).as_posix()
    folder = str({**DEFAULTS["paths"], **(CONFIG.get("paths") or {})}["reviews"]).strip().strip("/") + "/*"
    own_review = re.compile(r"^" + re.escape(rel) + r"/evidence/(?:.+/)?review[^/]*\.md$")     # the verdict's own file, anywhere
    return lambda x, own: ((x.startswith(rel + "/") and fnmatch.fnmatchcase(x[len(rel) + 1:], folder)) or x == f"{rel}/sessions.md"
                           or bool(own and own_review.match(x)))


def addenda_between(r, h, v=None):
    """every commit from r to h touches only review addenda (`review_addendum`) — the verdict `v` its own review file
    anywhere under evidence/ too, and with `v` None every commit its own — and none is a merge, which brings a line's
    files; False where git cannot read the range"""
    ok = review_addendum()
    out = subprocess.run(["git", "-c", "core.quotePath=false", "log", "--format=%x00%H %P", "--name-only", "--no-renames", f"{r}..{h}"],
                         cwd=ROOT, capture_output=True, text=True, encoding="utf-8", errors="replace", env=nested_git_env())
    for chunk in out.stdout.split("\x00")[1:]:
        shas, *paths = chunk.strip("\n").split("\n")
        sha, *parents = shas.split()
        if len(parents) > 1 or any(x and not ok(x, v in (None, sha)) for x in paths):
            return False
    return out.returncode == 0


REFUSAL_SUBJECT_RE = re.compile(r"^([A-Z][A-Z0-9]*-\d+): --(?:answer|done|due|revoke) refused — ")   # `record_refusal`'s subject
REFUSAL_LINE_RE = re.compile(r"^\*\*\d{4}-\d{2}-\d{2} \d{2}:\d{2}\*\* · .+ refused — ")               # … and its one line


def refusal_record(commit):
    """The tool's own refusal record (FM-030, `record_refusal`), unsigned by design: one parent, the subject `<ID>: --<act>
    refused — …`, ONE file changed — that tracker's —, and a diff that adds the one `**<date> <time>** · … refused — …`
    line and nothing else but the `## Acts` heading it may make and blank lines, and removes blank lines only: no
    front-matter key, no act. And, from the tracker's text at the parent and at the commit (RV-715, the Owner's cold
    re-check of `af5a9e2`, P1: a refusal-shaped line typed into *What is true now* passed the diff alone): the front
    matter is byte-identical, the body before `## Acts` is byte-identical (trailing blank lines aside), and the section
    under `## Acts` is the parent's plus that ONE line — nothing else changes anywhere. The gate reads no right in it;
    `--queue` admits it below their act as it admits a review file's commit (RV-712) — a forged one in their name carries in
    one line under `## Acts` that rules nothing, and nothing outside it."""
    r = subprocess.run(["git", "-c", "core.quotePath=false", "show", "--format=%P%x00%s", "--unified=0", "--no-renames", "--no-color", "--no-ext-diff", commit],
                       cwd=ROOT, capture_output=True, text=True, encoding="utf-8", errors="replace", env=nested_git_env())
    head, _, diff = r.stdout.partition("\n")
    parents, _, subject = head.partition("\x00")
    tid = REFUSAL_SUBJECT_RE.match(subject)
    if r.returncode != 0 or len(parents.split()) != 1 or not tid:
        return False
    rel = TRACKER_DIR.relative_to(ROOT).as_posix()
    files, added, removed, hunk = [], [], [], False
    for line in diff.splitlines():
        if line.startswith("diff --git "):
            hunk = False
        elif not hunk and line.startswith("+++ "):
            files.append(line[len("+++ b/"):] if line.startswith("+++ b/") else line)
        elif line.startswith("@@"):
            hunk = True
        elif hunk and line[:1] in "+-" and line:
            (added if line[0] == "+" else removed).append(line[1:])
    name = files[0][len(rel) + 1:] if len(files) == 1 and files[0].startswith(rel + "/") else ""
    if not (name.startswith(tid.group(1) + "-") and name.endswith(".md") and "/" not in name and all(not x.strip() for x in removed)
            and all(not x.strip() or ACTS_HEAD_RE.match(x) or REFUSAL_LINE_RE.match(x) for x in added)
            and sum(1 for x in added if REFUSAL_LINE_RE.match(x)) == 1):
        return False
    return refusal_record_in_place(parents.strip(), commit, files[0])


def refusal_record_in_place(parent, commit, path):
    """RV-715, RV-716 (the Owner's cold re-checks of `af5a9e2` and `729ddae`) — the diff alone said what lines were added, not
    WHERE: the tracker's text at `parent` and at `commit` is read in three parts — the body before the `## Acts` heading,
    the section from that heading to the next `##`/`###` heading (as `append_record` bounds it), and the suffix after it.
    The front matter and the body before the heading are byte-identical, the suffix is byte-identical, and the section's
    lines are the parent's followed by exactly one refusal line. Where the parent has no `## Acts`, the new section is
    the heading and that one line, placed exactly where `append_record` puts one — immediately above the ship-log heading
    where the parent has one, else at the body's end — and the rest of the body is the parent's byte for byte. Anything else — a line in *What is true now*, a line in a later `## Asks`, a moved
    heading, a second record — and it is not the tool's record, whatever the diff looked like."""
    def text_at(ref):
        r = subprocess.run(["git", "-c", "core.quotePath=false", "show", f"{ref}:{path}"], cwd=ROOT, capture_output=True, text=True,
                           encoding="utf-8", errors="replace", env=nested_git_env())
        return r.stdout if r.returncode == 0 else None
    def parts(text):
        body = parse_frontmatter(text)[1]
        front = text[: len(text) - len(body)]
        m = ACTS_HEAD_RE.search(body)
        if not m:
            return front, body, None, None
        rest = re.search(r"^#{2,3}\s+", body[m.end():], re.M)
        cut = m.end() + (rest.start() if rest else len(body) - m.end())
        return front, body[: m.start()], body[m.start():cut], body[cut:]
    lines = lambda x: [l for l in x.split("\n") if l.strip()]
    old, new = text_at(parent), text_at(commit)
    if old is None or new is None:
        return False
    of, obefore, oacts, osuffix = parts(old)
    nf, nbefore, nacts, nsuffix = parts(new)
    if of != nf or nacts is None:
        return False
    if oacts is None:
        # the heading is new: the section is the heading and one line, and it sits exactly where `append_record` puts one —
        # immediately above the ship-log heading where the parent has one, else at the body's end — with the rest of the body
        # the parent's byte for byte (a section made before any other heading is not the tool's)
        log = re.search(r"^#{2,3}\s+(%s)\s*$" % re.escape(HEAD["log"]), obefore, re.I | re.M)
        if log:
            around = nbefore == obefore[: log.start()] and nsuffix == obefore[log.start():]
        else:
            around = not nsuffix.strip() and nbefore.rstrip("\n") == obefore.rstrip("\n")
        got = lines(nacts)
        return around and len(got) == 2 and ACTS_HEAD_RE.match(got[0]) is not None and REFUSAL_LINE_RE.match(got[1]) is not None
    if nbefore != obefore or nsuffix != osuffix:
        return False
    before, after = lines(oacts), lines(nacts)
    return after[: len(before)] == before and len(after) == len(before) + 1 and REFUSAL_LINE_RE.match(after[-1]) is not None


def stray_below(commit, base, skip=True):
    """FM-031, RV-710 — what an `answer/*` branch's merge would carry in that its reading does not see: the first commit of
    its own — `git log <commit> ^<base>`, newest first, `commit` itself left out unless `skip` is False — that is not theirs
    (`answers_as_him`: may answer, verifies as them), not a review addendum (`review_addendum`, no merge), and not the
    tool's own refusal record (`refusal_record`), as the wait that names it: `wait: a seat's commit on your answer branch
    (<sha>, <author>)`, or where its author may answer, `wait: an unverified commit in your name on your answer branch
    (<sha>)` — never *a seat's* of a commit in their name (RV-712). "" where there is none; None where the walk cannot run —
    `base` is not here (RV-711): nothing below is proven, and a reader waits."""
    ok = review_addendum()
    full = (git_out("rev-parse", "--verify", "--quiet", commit + "^{commit}") or "").strip()
    out = subprocess.run(["git", "-c", "core.quotePath=false", "log", "--format=%x00%H %P", "--name-only", "--no-renames", commit, "^" + base],
                         cwd=ROOT, capture_output=True, text=True, encoding="utf-8", errors="replace", env=nested_git_env())
    if out.returncode != 0 or not full:
        return None
    for chunk in out.stdout.split("\x00")[1:]:
        shas, *paths = chunk.strip("\n").split("\n")
        sha, *parents = shas.split()
        if (skip and sha == full) or (len(parents) <= 1 and all(not x or ok(x, True) for x in paths)) or answers_as_him(sha):
            continue
        may, who, _email = answerer_of(sha)
        if may and refusal_record(sha):
            continue
        return (f"{STRAY_WAITS[1]} ({sha[:7]})" if may else f"{STRAY_WAITS[0]} ({sha[:7]}, {who})")
    return ""


STRAY_WAITS = ("wait: a seat's commit on your answer branch", "wait: an unverified commit in your name on your answer branch")   # `stray_below`'s two


def answer_branch_reading(head, base):
    """THE reading of an `answer/*` branch at `head` against `base` — `--queue`'s action for its pull request, and the
    board's for their act on its way (`on_their_way`, RV-714): (kind, action, detail). It is read by ONE commit
    (`answer_reading`): the newest of its own that changed an `answer:`, `done:` or `due:` line in a tracker —
    `owner_change` cuts the branch for `--answer`, `--done` and `--due` alike — where every commit past it is a review
    file's only (`addenda_between`, any commit's own `review*.md`) — the parent project's PRs 836, 849 and 853, a
    Reviewer's docs pass on the answer, read *not an answerer (reviewer@seat)* by the head, and its `answer/bug-327`, a
    Reviewer's verdict on their `--done`, the same (RV-679, 0.18.6); anything else past it, and the head is read, as
    before. A merge carries every commit below that one too, and `owner_change` cuts `answer/<id>` from the branch they
    stand on — a seat's, unmerged, carries its commits: *merge: your answer* only where `stray_below` finds none —
    else its wait, the first such below theirs, never the head's reading (RV-710, the Owner's cold review of 0.18.6's
    widening; RV-735, the same below their `answer:` since 0.18.4) — and where `base` is not here, a wait that says so: a
    reader that cannot see below their act never says merge (RV-711)."""
    rel = TRACKER_DIR.relative_to(ROOT).as_posix()
    at = (git_out("log", "-1", "--format=%H", "-G", "^(answer|done|due):", head, "^" + base, "--", rel) or "").strip()
    at = at if at and (at == head or addenda_between(at, head)) else head
    action = answer_reading(at)
    if action[0] != "merge":
        return action
    stray = stray_below(at, base)
    if stray is None:
        return "wait", f"wait: the base {ref_name(base)} is not fetched here — fetch it; the commits below {at[:7]} are unread", ""
    return ("wait", stray, "") if stray else action


def answer_reading(head):
    """An `answer/*` pull request is the Owner's own signed answer, `done:` or `due:`, and needs no Reviewer: `merge: your
    answer` when the author of `head` — their answer, `done:` or `due:` commit, as `queue_actions` finds it — may answer and
    the commit verifies as them — the gate's one test, `verified_as` — else it waits: on an author who may not answer,
    named, whatever the commit's signature (R8 — a signed commit by someone else read *unsigned*, and the impostor is the
    case the Owner most needs named); else on the signature. `answer_branch_reading` reads a merge here as theirs only where
    every commit of the branch's own below `head` is theirs too, a review file's only, or the tool's own refusal record
    (RV-710)."""
    may, who, identity = answerer_of(head)
    if not may:
        return "wait", f"wait: not an answerer ({who})", ""
    if verified_as(head, identity):
        return "merge", "merge: your answer", f"signed {head[:7]}"
    if signature_kind(head) not in ("", "ssh"):             # GPG, X.509: a signed line verifies by SSH only
        return "wait", f"wait: {SIGN_WITH_SSH}", ""
    gap = signature_gap(head)
    return "wait", (f"wait: answer not verified here — {gap}" if gap else "wait: unsigned answer"), ""


def triage_reading(head, base):
    """FM-037 in `--queue`: (`wait: TRIAGE.md changed unsigned`, the commit) where a commit of the head's own — not on `base`
    — changes the Owner's two sections and is not their signed commit, the walk and the judgement `--check` makes on the
    branch; (`wait: TRIAGE.md change not verified here — <why>`, the commit) where it is signed and this clone cannot check
    it; (`wait: TRIAGE.md change not judged — <the configuration> cannot be read here`, the commit) where the refusal is
    one `--check` makes because a configuration cannot be read — the default branch's, or one on the branch; (`wait:
    TRIAGE.md home in another case at the branch tip`, the head) where `--check` refuses the tip as a merge would bring it
    (`tip_variants`); None where no commit changes them unsigned, and where the default branch names no Owner. The Owner is the default branch's, as
    `--check` reads them — never a stacked pull request's base, which a seat's branch can be. No git call of its own beyond
    the walk's: `--queue` asks this for every pull request."""
    git = lambda *a: subprocess.run(["git", *a], cwd=ROOT, capture_output=True, text=True, encoding="utf-8", errors="replace", env=nested_git_env())
    trunk, why = default_trunk(git) or base, []
    owners = owners_at(trunk, why)
    if not owners and not why:
        return None
    changed = guard_walk(head, "^" + base, keys=signers_paths(trunk), unread=not owners)[1]
    if not owners:
        return (f"wait: TRIAGE.md change not judged — {ref_name(trunk)}'s configuration cannot be read here", changed[0][0][:7]) if changed else None
    verdicts = guard_verdicts(changed, owners)
    refused = [v for v in verdicts if v[4] == "refused"]
    unread = next((w[3][len("where "):].split(" — ", 1)[0] for w in (refused[0][3] if refused else []) if w[0] == "unread"), "")
    if unread:
        return f"wait: TRIAGE.md change not judged — {unread}", refused[0][0][:7]
    if refused:
        return "wait: TRIAGE.md changed unsigned", refused[0][0][:7]
    if tip_variants(trunk, head):
        return "wait: TRIAGE.md home in another case at the branch tip", head[:7]
    gaps = [v for v in verdicts if v[4] == "checkout"]
    return (f"wait: TRIAGE.md change not verified here — {gaps[0][5]}", gaps[0][0][:7]) if gaps else None


def queue_actions(prs, branches=()):
    """Each open pull request's ONE action, in the order the Owner takes them: what they can act on first, then what waits;
    inside each, the oldest first; then each branch pushed without one (`pushed_branches`), read the same way — its
    verdict or its conflict — as `wait: no pull request — …`. Returns [(pr, kind, action, detail)], `kind` one of
    merge · close · wait · branch. An `answer/*` pull request is read by `answer_reading`, not by a verdict — on their
    answer, `done:` or `due:` commit, the newest of its own that changed an `answer:`, `done:` or `due:` line, where only
    review files follow it (FM-031, 0.18.4: a Reviewer's docs pass on the answer read *not an answerer* by the head;
    0.18.6, RV-679: on their `--done` or `--due`, too); else on its head — and it reads *merge: your answer* only where
    every commit of its own below that one is theirs too, a review file's only, or the tool's own refusal record; else a wait
    naming the first that is not (RV-710, RV-712), and a wait where its base is not here (RV-711) —
    `answer_branch_reading`, the board's reader too (RV-714). For a pull request the first rule that holds is the action:
    - `wait: from a fork, read it yourself` — fork commits supply no verdict or carry-over instruction;
    - `closes with PR N` — its head is inside N's head, on the same base (of twins with one head, the newer one closes);
    - `close: carried into PR N` — every commit of its own (not on its base) is on N's branch, as that commit or as the
      same patch;
    - `wait: conflict in <paths>` — `git merge-tree --write-tree origin/<base> <head>` does not merge clean;
    - `wait: TRIAGE.md changed unsigned` — a commit of its own changes the Owner's intent or current path and is not their
      signed commit (FM-037, `triage_reading`: the walk `--check` makes on the branch);
    - `wait: NOT READY (<verdict>)` — the last verdict on its head says so;
    - `wait: no verdict on <head>` — no verdict names its head;
    - `merge` — the last verdict on its head says READY, READY WITH FINDINGS or READY TO TAG, and it merges clean.
    A verdict is a commit among the same-repository pull requests' own and the pushed branches' that carries `Reviewed: <sha>`, as `--check` reads one, with its
    word in its subject. It names a head that is <sha>, or that only review addenda follow <sha> to — commits touching
    nothing but the review folder (`[paths] reviews`, `evidence/reviews/` by default, a glob allowed) and
    `<tracker dir>/sessions.md` — and the verdict commit itself, whose own review file counts wherever it sits under
    `<tracker dir>/evidence/` (`review*.md`), as the parent project's review gate reads it: a head that IS the verdict,
    `Reviewed:` its parent, is covered (FM-031, 0.18.4)."""
    forks = [(p, "wait", "wait: from a fork, read it yourself", "") for p in prs if p.get("isCrossRepository")]
    prs = [p for p in prs if not p.get("isCrossRepository")]
    git = lambda *a, **k: subprocess.run(["git", "-c", "core.quotePath=false", *a], cwd=ROOT, capture_output=True, text=True,
                                         encoding="utf-8", errors="replace", env=nested_git_env(), **k)
    head, base, num = (lambda p: p["headRefOid"]), (lambda p: "refs/remotes/origin/" + p["baseRefName"]), (lambda p: p["number"])
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

    pushed = [{"number": None, "title": b["name"], "headRefName": b["name"], "headRefOid": b["sha"], "baseRefName": b["base"], "createdAt": ""} for b in branches]
    absent = set(have_not(sorted({head(p) for p in prs + pushed})))       # one head this clone lacks must not blank every verdict
    heads = sorted({head(p) for p in prs + pushed} - absent)
    bases = sorted({"^" + base(p) for p in prs + pushed if git("rev-parse", "--verify", "--quiet", base(p)).returncode == 0})
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

    def addenda_only(r, h, v):
        """`addenda_between`, read once per range"""
        return cached(("addenda", r, h, v), lambda: addenda_between(r, h, v))

    rows = forks
    for p in prs:
        carried = [q for q in siblings(p) if holds(q, p) and not (holds(p, q) and age(p) < age(q))] if not within[num(p)] else []
        paths = conflicts(p) if not (within[num(p)] or carried) else []
        last = next(((v, w) for v, r, w in verdicts if r == head(p) or (anc(r, head(p)) and addenda_only(r, head(p), v))), None)
        if head(p) in absent:
            rows.append((p, "wait", f"wait: {head(p)[:7]} not fetched here", ""))
        elif within[num(p)]:
            rows.append((p, "close", f"closes with PR {num(outermost(within[num(p)]))}", ""))
        elif carried:
            rows.append((p, "close", f"close: carried into PR {num(outermost(carried))}", ""))
        elif paths:
            rows.append((p, "wait", "wait: conflict in " + ", ".join(paths), ""))
        elif (guarded := triage_reading(head(p), base(p))):
            rows.append((p, "wait", *guarded))
        elif p["headRefName"].startswith("answer/"):
            rows.append((p, *answer_branch_reading(head(p), base(p))))
        elif last is None:
            rows.append((p, "wait", f"wait: no verdict on {head(p)[:7]}", ""))
        elif last[1] == "NOT READY":
            rows.append((p, "wait", f"wait: NOT READY ({last[0][:7]})", ""))
        else:
            rows.append((p, "merge", "merge", f"verdict {last[0][:7]} {last[1]}"))
    for b in pushed:
        paths = conflicts(b) if head(b) not in absent else []
        last = next(((v, w) for v, r, w in verdicts if r == head(b) or (anc(r, head(b)) and addenda_only(r, head(b), v))), None)
        said = ("not fetched here" if head(b) in absent else "conflict in " + ", ".join(paths) if paths else f"no verdict on {head(b)[:7]}" if last is None
                else f"NOT READY ({last[0][:7]})" if last[1] == "NOT READY" else f"verdict {last[0][:7]} {last[1]}: open it")
        guarded = triage_reading(head(b), base(b)) if head(b) not in absent and not paths else None
        said = guarded[0][len("wait: "):] + f" ({guarded[1]})" if guarded else said
        rows.append((b, "branch", "wait: no pull request — " + said, ""))
    return sorted(rows, key=lambda row: (row[1] == "branch", row[1] == "wait", age(row[0]) if row[1] != "branch" else row[0]["headRefName"]))


def queue_lines(rows):
    """The queue as the Owner reads it: one line per pull request, its columns aligned, and the count last."""
    cut = lambda b: b if len(b) <= QUEUE_BRANCH_MAX else b[:QUEUE_BRANCH_MAX - 1] + "…"
    cells = [(f"PR {p['number']}", action, f"{cut(p['headRefName'])} @ {p['headRefOid'][:7]}", detail) for p, k, action, detail in rows if k != "branch"]
    w = [max([len(c[i]) for c in cells] or [0]) for i in range(3)]
    w[1] = max([len(c[1]) for c in cells if len(c[1]) <= QUEUE_ACTION_MAX] or [0])      # an action past the cap runs on in its own line
    kinds = collections.Counter(k for _p, k, _a, _d in rows)
    return ([f"{a:<{w[0]}}  {b:<{w[1]}}  {c:<{w[2]}}  {d}".rstrip() for a, b, c, d in cells]
            + [f"branch {cut(p['headRefName'])} @ {p['headRefOid'][:7]}  {action}" for p, k, action, _d in rows if k == "branch"]
            + [f"{len(rows)} waiting on you: {kinds['merge']} merge, {kinds['close']} close, {kinds['wait']} wait, "
               f"{kinds['branch']} pushed without a pull request"])


def forge_closed(hours=24):
    """FM-030, widened (the Auditor seat, through the Owner, 2026-09-25): the pull requests the forge merged or closed in
    the last `hours`, so a seat's *still open* line is checked against the forge in the same turn — `gh pr list --state
    merged` and `--state closed`, one pull request once, merged where it has a merge time. [(number, merged|closed, time,
    branch)], newest first; [] where the forge does not answer."""
    since, seen = datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(hours=hours), {}
    for state in ("merged", "closed"):
        try:
            r = subprocess.run([shutil.which("gh") or "gh", "pr", "list", "--state", state, "--limit", "50", "--json", "number,headRefName,closedAt,mergedAt"],
                               cwd=ROOT, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=30,
                               env=dict(nested_git_env(), GH_PROMPT_DISABLED="1"))
            seen.update({p["number"]: p for p in (json.loads(r.stdout) if r.returncode == 0 else []) if p["number"] not in seen})
        except (OSError, ValueError, subprocess.TimeoutExpired, KeyError, TypeError):
            continue
    rows = [(n, "merged" if p.get("mergedAt") else "closed", parse_due(p.get("mergedAt") or p.get("closedAt")), p.get("headRefName", "")) for n, p in seen.items()]
    return sorted(((n, s_, at, b) for n, s_, at, b in rows if at and at >= since), key=lambda row: row[2], reverse=True)


def queue_cmd():
    """`--queue`: the open pull requests, one action each, in the order to take them — exit 3 where the forge cannot be read."""
    prs, why = forge_prs()
    if prs is None:
        print(why, file=sys.stderr)
        return EXIT_NO_FORGE
    print("\n".join(queue_lines(queue_actions(prs, pushed_branches(prs)))))
    closed = forge_closed()
    print(f"\nMERGED OR CLOSED IN THE LAST 24 HOURS — {len(closed) or 'none'}" + "".join(
        f"\n  PR {n}  {state:<6}  {at.strftime('%Y-%m-%d %H:%M')} UTC  {branch}" for n, state, at, branch in closed))
    return EXIT_OK


def queue_section():
    """`--owner` and `--standup` end with the queue where the forge can be read — and say nothing of it where it cannot."""
    prs, _why = forge_prs()
    if prs is not None:
        print("\nPULL REQUESTS — in the order to take them")
        print("\n".join("  " + line for line in queue_lines(queue_actions(prs, pushed_branches(prs)))))


def answer_step(tid, n, text, verb="answering"):
    """`--answer` says what it is doing AS EACH STEP STARTS — on stderr, flushed, before the wait and not after it. It
    reads the trackers, and a checkout hook and the pre-commit gate read them again; silent for that long, it was
    stopped by an Owner who took it for hung (FM-012). What it prints at the end is unchanged. `--done` and `--due` say
    theirs the same way, with their own word."""
    print(f"{verb} {tid} — {n}/4 {text} …", file=sys.stderr, flush=True)


def answer_cmd(words, trackers, supersede=False, onto=None, flag="--answer", verb="answering"):
    """`--answer <id> accept|reject [text]` — the Owner's one command. It does what they did by hand the first time: cuts
    `answer/<id>` from the branch that carries the ask, writes the three lines, commits SIGNED under their name, pushes,
    and goes back to the branch it started on. It refuses before touching anything when it cannot end in a verified answer.
    An answer they take back or change (`revoke "<reason>"`, or `accept|reject "<option>" --supersede`) is never lost:
    the answer it replaces moves into the ship log, with the commit that wrote it. `onto` (FM-030, `--revoke`): the ref of an
    `answer/<id>` not merged, whose tip `t` was read from — the answer is taken back there, on top of it."""
    if len(words) < 2 or words[1] not in ("accept", "reject", "revoke"):
        print("--answer <id> accept|reject [\"text\"] — reject needs a reason; accept takes an optional change. "
              "An answer given already: `--answer <id> revoke \"<reason>\"`, or `--answer <id> accept|reject \"<option>\" --supersede`", file=sys.stderr)
        return EXIT_LINT
    # the answer is ONE front-matter line: every run of whitespace — a newline above all — collapses to one space.
    # A newline would close the line and the next fragment would be read as another key (`status: Shipped` flipped one),
    # and the tracker's body is where a long answer belongs.
    tid, verdict, text = words[0].upper(), words[1], " ".join(" ".join(words[2:]).split())
    t = next((x for x in trackers if x["id"] == tid), None)
    # an answer that is there keys revoke and --supersede, not `next: owner`: the answer writes the next move (FM-030), and
    # a ruling's reads `build` from then on
    if not t or not t.get("ask"):
        print(f"--answer: {tid} asks the Owner nothing — an answer answers an `ask:` with `next: owner`", file=sys.stderr)
        return EXIT_LINT
    if not t.get("answer") and t.get("next") != "owner":
        print(f"--answer: {tid} carries an `ask:` and `next: {t.get('next') or '—'}` — an ask waits on the Owner with `next: owner`; the seat that asks sets it", file=sys.stderr)
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
    path = TRACKER_DIR / t["file"]
    answer = {"accept": "accepted", "reject": "rejected", "revoke": "revoked"}[verdict] + (f" - {text}" if text else "")
    move = ANSWER_MOVE.get(t.get("ask_kind"))
    replaced = []                                            # the answer this one replaces, and its commit — read on the branch it is cut from
    # FM-030, E0 row 20: an accepted action answer that names its hour seeds `due:` — read from what they promised, the text
    # they gave or, bare, the proposal they took (`promise_of`); a `due:` already set is left for `--due` to move
    seed = dict(zip(("when", "words", "why"), answer_due(promise_of({**t, "answer": answer}), datetime.date.today()))) if move == "owner" and verdict == "accept" else {}

    def check_ask():
        # the ask is a front-matter LINE, and the answer is written under it: an ask that parsed (indented, or under a key
        # the file spells another way) but is not one raised out of `next(...)` with a traceback instead of a refusal.
        # Asked before the branch is cut — nothing is touched for an answer that cannot be written
        if not any(l.startswith("ask:") for l in path.read_text(encoding="utf-8").split("\n")):
            return (f"{tid} has no `ask:` line in {t['file']} — the front matter's question is what the answer is written under; "
                    f"the ask is there but not as its own line (indented, or wrapped). Fix the file, then answer")
        if t.get("answer"):
            wrote = (git_out("log", "-1", "--format=%h", "-G", line_regex("answer:"), onto, "--", path.relative_to(ROOT).as_posix()) or "").strip() if onto else ""
            replaced.append((t["answer"], t.get("answered", ""), wrote or (line_author(path, "answer:")[3] or "")[:7] or "not committed"))
        return ""

    def write(lines, me, branch):
        at = next((i for i, l in enumerate(lines) if l.startswith("ask:")), None)
        if at is None:
            return None, f"{tid} has no `ask:` line in {t['file']} on `{branch}` — the front matter's question is what the answer is written under"
        if replaced:                                         # the lines it replaces leave the front matter, and the ship log keeps them
            end_ = next((i for i, l in enumerate(lines) if i and l.strip() == "---"), len(lines))
            lines = [l for i, l in enumerate(lines) if i >= end_ or not l.startswith(("answer:", "answered:", "answered-by:"))]
            at = next(i for i, l in enumerate(lines) if l.startswith("ask:"))
        while at + 1 < len(lines) and lines[at + 1].startswith("ask-"):
            at += 1
        lines[at + 1:at + 1] = [f'answer: "{answer.replace(chr(34), chr(39))}"', f"answered: {datetime.date.today().isoformat()}", f"answered-by: {me}"]
        if move:                                             # FM-030: the move after theirs — the seat's, or their own hands' for an action
            lines = set_front("\n".join(lines), "next", move).split("\n")
        if seed.get("when"):
            seed["had"] = (parse_frontmatter("\n".join(lines))[0].get("due") or "").strip()
            if not seed["had"]:
                lines = set_front("\n".join(lines), "due", seed["when"]).split("\n")
        if replaced:
            cell = lambda v: v.replace(chr(34), chr(39)).replace("|", "\\|")
            lines = ship_log_row(lines, f'Answer of {replaced[0][1]} superseded: *"{cell(replaced[0][0])}"* ({replaced[0][2]}) — '
                                        + (f"revoked: {cell(text)}" if verdict == "revoke" else f'replaced by: *"{cell(answer)}"*'))
        return lines, ""

    return owner_change(tid, t, dict(
        flag=flag, verb=verb, noun="answer", right="an answer is an `answer` change", check=check_ask, write=write, onto=bool(onto),
        subject=f"{tid}: {answer[:60]}", kept=("your answer", answer),
        again=f'{CMD} --answer {tid} {verdict}' + (f' "{text.replace(chr(34), chr(39))}"' if text else "") + (" --supersede" if supersede else ""),
        said=lambda branch, pushed: (f"{tid} answered: {answer}\n  signed, on `{branch}`" + pushed + f"\n  it has left your queue; the seat sees it under --answered"
                                     + ({"build": "\n  next: build — the seat's move follows", "owner": "\n  next: owner — an action: the act is still yours"}.get(move, ""))
                                     + seed_said(tid, seed))))


def seed_said(tid, seed):
    """What `--answer` says of the hour it read in an accepted action answer — written as `due:`, left beside a `due:` that
    was set, or not read, and why: the act then shows *no date yet*. "" where it read nothing because it looked for nothing."""
    if not seed:
        return ""
    if not seed.get("when"):
        return f"\n  no date read in your answer — {seed['why']}; the act shows *no date yet*: `{CMD} --due {tid} <time>` sets it"
    if not seed.get("had"):
        return f"\n  due: {seed['when']} — read from your answer's `{seed['words']}`, written with it; `{CMD} --due {tid} <time>` moves it"
    if parse_due(seed["had"]) == parse_due(seed["when"]):
        return f"\n  due: {seed['had']} — your answer names the same time"
    return f"\n  your answer names {seed['when']} (`{seed['words']}`); `due:` is {seed['had']} already and is left — `{CMD} --due {tid} {seed['when']}` moves it"


def unmerged_advice(git, branch, trunk, rel, tid, how, me, email):
    """What an unmerged `answer/<id>` asks of the Owner, read from what is on it. Its own commits — those not in `trunk`,
    or with no trunk, on no other branch — that are THEIRS (their name or their email) are never deleted for them: where the
    tracker's act is open there, `--done`/`--due` are run on it; otherwise it is merged first. `git branch -D` is named
    only where nothing of theirs is on it (FM-030 C, as ruled). Where `--queue` waits on it for a commit not theirs —
    `answer_branch_reading`, its own line — the advice says how that clears: the commit lands on the trunk first, by its
    own pull request; theirs are kept (RV-713)."""
    span = [f"refs/heads/{branch}", "--not", trunk] if trunk else [f"refs/heads/{branch}", "--not", f"--exclude={branch}", "--branches", f"--exclude=*/{branch}", "--remotes"]
    own = [l.split("\t") for l in git("log", "--format=%h%x09%an%x09%ae%x09%s", *span).stdout.splitlines() if l.count("\t") >= 3]
    his = [(sha, subject) for sha, name, mail, subject in own if name == me or (email and mail == email)]
    if not his:
        return (f"it may hold work, and nothing is deleted for you; nothing of yours is on it — clear it with `git branch -D {branch}`, "
                f"then `{how['again']}`")
    said = "; ".join(f"`{sha}` {subject[:60]}" for sha, subject in his[:3]) + (f"; and {len(his) - 3} more" if len(his) > 3 else "")
    tip = (git("rev-parse", "--verify", "--quiet", branch).stdout or "").strip()
    reading = answer_branch_reading(tip, trunk)[1] if trunk and tip else ""            # `--queue`'s own line for it
    stray = reading if reading.startswith(STRAY_WAITS) else ""
    held = (f"; `--queue` holds its merge on {stray[len('wait: '):]} — that commit lands on `{ref_name(trunk)}` first, by its own pull request, "
            f"never through yours" if stray else "")
    if how["flag"] in ("--done", "--due"):
        there = git("show", f"{branch}:{rel}")
        t_ = extract(ROOT / rel, there.stdout) if there.returncode == 0 else None
        if t_ and (act_of(t_) if how["flag"] == "--done" else t_.get("status") in OPEN_STATUSES):
            return (f"it carries your commit(s) — {said} — and {tid}'s act is open there: `git switch {branch}`, then "
                    f"`{how['again']}` — it commits on top, and nothing of yours is deleted" + held)
    if stray:
        return (f"it carries your commit(s) — {said} — and nothing of yours is deleted{held}; then merge it (its pull request), "
                f"then `{how['again']}`; or `git switch {branch}` and run it there")
    return (f"it carries your commit(s) — {said} — and nothing of yours is deleted: merge it first (its pull request), then `{how['again']}`; "
            f"or `git switch {branch}` and run it there")


def ics_text(value):
    """RFC 5545 3.3.11: a TEXT value, its backslash, semicolon, comma and line breaks escaped."""
    return value.replace("\\", "\\\\").replace(";", "\\;").replace(",", "\\,").replace("\r\n", "\\n").replace("\n", "\\n")


def ics_fold(line):
    """RFC 5545 3.1: a content line longer than 75 octets, folded — CRLF and one space — never inside a UTF-8 character."""
    parts, cur, size = [], "", 0
    for ch in line:
        n = len(ch.encode("utf-8"))
        if size + n > (74 if parts else 75):              # a continuation's leading space is one of its 75 octets
            parts.append(cur)
            cur, size = "", 0
        cur, size = cur + ch, size + n
    return "\r\n ".join(parts + [cur])


ACT_RECORD_RE = re.compile(r"^\*\*\d{4}-\d{2}-\d{2}\*\* · ", re.M)     # one record under `## Acts`: done, scheduled, rescheduled


def invite_cmd(tid, trackers):
    """`--invite <id>` (FM-030 D; their word: *invites + notifications*) — one calendar file for the act a tracker owes the
    Owner, beside its evidence: `<tracker dir>/evidence/<id>/<id>-act.ics`. RFC 5545, as the standup's invite is, but at
    the act's own instant, in UTC: DTSTART its `due:`, a DURATION of its `window:`, an alarm NOTIFY_AHEAD minutes before.
    The UID is the act's and SEQUENCE counts its records under `## Acts`, so the file written after a `--due` replaces
    the event when it is imported again. Deterministic: the same act writes the same bytes. The file is the Owner's to
    import, and to commit or not; nothing else is written."""
    tid = tid.upper()
    t = next((x for x in trackers if x["id"] == tid), None)
    act = act_of(t) if t else None
    if not act:
        print(f"--invite: {tid} owes the Owner no act — an accepted action ask is one, and so is a `due:`", file=sys.stderr)
        return EXIT_LINT
    when = parse_due(act[3])
    if not when:
        print(f"--invite: {tid}'s act has no `due:` yet — an invite needs a time: `{CMD} --due {tid} <time>` first", file=sys.stderr)
        return EXIT_LINT
    what, answer, answered, due, window, asked = act
    body = parse_frontmatter((TRACKER_DIR / t["file"]).read_text(encoding="utf-8"))[1]
    at = ACTS_HEAD_RE.search(body)
    records = re.split(r"^#{1,3}\s", body[at.end():], maxsplit=1, flags=re.M)[0] if at else ""
    sequence = len(ACT_RECORD_RE.findall(records))
    utc = lambda d: d.astimezone(datetime.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    name = CONFIG["name"] or ROOT.name
    said = ((f"{what}\nAsked: {asked}\n" if asked else "") + (f"Promised {answered}: {answer}. " if answer else "")
            + f"Owed to you, due {due}; it can still be done {window} minutes after. "
            f'Done: {CMD} --done {tid} "<where the result is>" — moved: {CMD} --due {tid} <time>')
    lines = ["BEGIN:VCALENDAR", "VERSION:2.0", "PRODID:-//shoalmark//act//EN", "BEGIN:VEVENT",
             f"UID:act-{tid.lower()}-{hashlib.sha256(name.encode()).hexdigest()[:16]}@shoalmark", "DTSTAMP:20000101T000000Z",
             f"SEQUENCE:{sequence}", f"DTSTART:{utc(when)}", f"DURATION:PT{window}M",
             "SUMMARY:" + ics_text(f"{name} — {tid}: {what}"), "DESCRIPTION:" + ics_text(said),
             "BEGIN:VALARM", "ACTION:DISPLAY", "DESCRIPTION:" + ics_text(f"{tid}: {what}"), f"TRIGGER:-PT{NOTIFY_AHEAD}M", "END:VALARM",
             "END:VEVENT", "END:VCALENDAR"]
    out = TRACKER_DIR / "evidence" / tid / f"{tid}-act.ics"
    write_rule(out)                                         # the write rule, before its folder is made
    out.parent.mkdir(parents=True, exist_ok=True)
    put(out, "\r\n".join(ics_fold(l) for l in lines) + "\r\n")      # CRLF, on every system — `put` writes them as they are
    print(f"wrote {out.relative_to(ROOT).as_posix()} — {tid} due {due} ({utc(when)} UTC), {window} minutes, a reminder "
          f"{NOTIFY_AHEAD} minutes before; import it into your calendar")
    return EXIT_OK


def state_dir():
    """The tool's own state — never committed, never in the repository: `$XDG_STATE_HOME/shoalmark`, else
    `%LOCALAPPDATA%/shoalmark` on Windows, else `~/.local/state/shoalmark`. None where there is no home at all."""
    try:
        base = (os.environ.get("XDG_STATE_HOME") or (os.environ.get("LOCALAPPDATA") if sys.platform == "win32" else "")
                or pathlib.Path.home() / ".local" / "state")
    except (RuntimeError, KeyError):
        return None
    return pathlib.Path(base) / "shoalmark"


def notify_argv(title, body, platform=None, which=None):
    """The command that posts one system notification on `platform`, or None where none is present: macOS `osascript`,
    Linux `notify-send`, Windows PowerShell's toast. Pure — what it WOULD run — so a test reads every platform's."""
    platform, which = platform or sys.platform, which or shutil.which
    if platform == "darwin" and which("osascript"):
        q = lambda v: '"' + v.replace("\\", "\\\\").replace('"', '\\"') + '"'
        return ["osascript", "-e", f"display notification {q(body)} with title {q(title)}"]
    if platform.startswith("linux") and which("notify-send"):
        return ["notify-send", "--app-name=shoalmark", "--", title, body]
    if platform == "win32" and which("powershell"):
        q = lambda v: "'" + v.replace("'", "''") + "'"
        app = "{1AC14E77-02E7-4E5D-B744-2EB1AE5198B7}\\WindowsPowerShell\\v1.0\\powershell.exe"     # PowerShell's own AppUserModelID
        return ["powershell", "-NoProfile", "-NonInteractive", "-Command",
                "[Windows.UI.Notifications.ToastNotificationManager, Windows.UI.Notifications, ContentType = WindowsRuntime] > $null; "
                "$x = [Windows.UI.Notifications.ToastNotificationManager]::GetTemplateContent([Windows.UI.Notifications.ToastTemplateType]::ToastText02); "
                f"$t = $x.GetElementsByTagName('text'); $t.Item(0).AppendChild($x.CreateTextNode({q(title)})) > $null; "
                f"$t.Item(1).AppendChild($x.CreateTextNode({q(body)})) > $null; "
                f"[Windows.UI.Notifications.ToastNotificationManager]::CreateToastNotifier({q(app)}).Show([Windows.UI.Notifications.ToastNotification]::new($x))"]
    return None


def post_notice(title, body):
    """Post one notification: `posted`; `printed` where this system has no notifier — the printed line is the notice; or
    `NOT posted — why`, which is not remembered, so the next run tries again."""
    argv = notify_argv(title, body)
    if not argv:
        return "printed — no notifier here"
    try:
        r = subprocess.run(argv, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=30)
    except (OSError, subprocess.TimeoutExpired) as e:
        return f"NOT posted — {type(e).__name__}"
    return "posted" if r.returncode == 0 else "NOT posted — " + ((r.stderr or r.stdout or "").strip().splitlines() or [f"exit {r.returncode}"])[-1][:120]


def notify_cmd(trackers):
    """`--notify` (FM-030 D; their word: *invites + notifications*) — one system notification for every act with a `due:`
    that falls due within NOTIFY_AHEAD minutes, is overdue, or was missed: ONE per act per state. What was posted is
    remembered in `state_dir()/notified.json`, per repository, keyed on the act, its `due:` and the state — a `--due` that
    moves it posts again, and nothing else does; a notice that could not be posted is not remembered. Meant to be
    scheduled by the person — the README has a launchd and a cron line; the tool installs nothing. It reads the
    trackers and writes nothing in the repository. Exit 1 when a notice could not be posted — a schedule's log shows it."""
    now, name = datetime.datetime.now(datetime.timezone.utc), CONFIG["name"] or ROOT.name
    store = state_dir()
    path = store / "notified.json" if store else None
    try:
        seen = json.loads(path.read_text(encoding="utf-8")) if path and path.is_file() else {}
        seen = seen if isinstance(seen, dict) else {}
    except (OSError, ValueError):
        seen = {}
    had, keep, lines, before, later, failed = set(seen.get(str(ROOT)) or []), set(), [], 0, 0, 0
    for t in sorted(trackers, key=lambda t: (t["kind"], t["num"])):
        act = act_of(t)
        when = parse_due(act[3]) if act else None
        if not when:
            continue
        state = act_state(act, now)
        if state == "due" and now < when - datetime.timedelta(minutes=NOTIFY_AHEAD):
            later += 1
            continue
        mark = f"{t['id']} {act[3]} {state}"
        if mark in had:
            keep.add(mark)
            before += 1
            continue
        said = f"due in {max(1, math.ceil((when - now).total_seconds() / 60))} min" if state == "due" else state
        how = post_notice(f"{name} · {t['id']} — {said}", f"{act[0]} · {act_words(act, now)}" + (f"\n{LABELS['acts.asked'].format(act[5])}" if act[5] else ""))
        lines.append(f"  {t['id']} — {said} · {act[0]} · {act_words(act, now)} — {how}")
        if how.startswith("NOT"):
            failed += 1
        else:
            keep.add(mark)
    where = "NOT remembered — there is no home for the tool's state; the next run posts again"
    if path:
        seen = {k: v for k, v in seen.items() if k != str(ROOT)}
        if keep:
            seen[str(ROOT)] = sorted(keep)
        try:
            write_rule(path)                                # the write rule, before its folder is made
            path.parent.mkdir(parents=True, exist_ok=True)
            put(path, json.dumps(seen, indent=1, ensure_ascii=False) + "\n")
            where = f"remembered in {path}" if keep else f"nothing remembered — {path}"
        except OSError as e:
            where = f"NOT remembered — {path}: {e.strerror or e}; the next run posts again"
    print(f"--notify: {len(lines) - failed} posted · {before} posted before · {later} not yet within {NOTIFY_AHEAD} minutes"
          + (f" · {failed} NOT posted" if failed else "") + f" — {where}")
    for l in lines:
        print(l)
    return 1 if failed else EXIT_OK                         # a notice that could not be posted is a failure a schedule must see (R6)


def owner_change(tid, t, how):
    """THE OWNER'S OWN CHANGE ON A TRACKER, the one flow `--answer`, `--done` and `--due` share: who may make it — the
    seats that hold `answer`, or `answerers` — is asked first; then `answer/<id>` is cut from the branch that carries the
    tracker (a spent one deleted and cut fresh, an unmerged one refused), `how["write"]` writes the lines, and the commit
    is made SIGNED where their seat is `signed`, verified, pushed, and they are put back on the branch they started on. A failure
    after anything was written undoes all of it and prints what they gave with the command that gives it again (FM-017).
    `how`: flag · verb (the steps' word) · noun · right (why it is an `answer` change) · check() → why not, before anything
    is touched · write(lines, me, branch) → (lines, why not) · subject · kept (its name, its text) · again · said(branch,
    ", pushed" or why not) → what it prints · onto (FM-030, `--revoke`): `answer/<id>` is not merged — their act on its way — and
    the change commits on top of it there, one branch per exchange, where every other flow refuses it."""
    flag, noun = how["flag"], how["noun"]
    step = lambda n, text: answer_step(tid, n, text, how["verb"])
    for p_ in answerers_problems():                           # a signature the configuration asks for and `[seats]` drops (FM-015)
        print(f"{flag}: {p_}", file=sys.stderr)
        return EXIT_LINT
    # who may answer is asked in ONE place, `may_answer()`: with `[seats]`, the seats that hold `answer`, matched on
    # the identity git will actually write; with none, `answerers`, which always meant the author's name
    me, allowed = git_user(), may_answer()
    pend_name, pend_email = pending_author()                 # who git will actually author as — the seat is matched on that
    seat = seat_of(pend_name or me, pend_email) if SEATS else None
    if SEATS and not holds(seat, "answer"):
        print(f"{flag}: " + no_seat(pend_name or me, pend_email, "answer", how["right"]), file=sys.stderr)
        return EXIT_LINT
    if not SEATS and me not in allowed:
        print(f"{flag}: `{me}` is not in `answerers` ({', '.join(allowed) or 'nobody'}) — {CONFIG_NAME} says who may answer", file=sys.stderr)
        return EXIT_LINT
    signed = (seat_mode(seat, pend_name or me, pend_email) if SEATS else allowed.get(me)) == "signed"
    git = lambda *a: subprocess.run(["git", *a], cwd=ROOT, capture_output=True, text=True, encoding="utf-8", errors="replace", env=nested_git_env())
    dirty = changed_paths(git)
    if dirty:
        print(dirty_refusal(git, dirty), file=sys.stderr)
        return EXIT_LINT
    if signed and not git("config", "user.signingkey").stdout.strip():
        print(f'{flag}: `{("owner" if at_top(seat) else "[seats]") if SEATS else "answerers"}` asks for a signed {noun} and no `user.signingkey` is set — see the signing page, {SIGNING_PAGE}', file=sys.stderr)
        return EXIT_LINT
    # `answered-by:` is `user.name`, but the commit's author is whatever git will actually write — `GIT_AUTHOR_NAME` in
    # the environment overrides the configuration. The gate reads the author, so the two disagreeing is an answer filed
    # from an account that did not give it. Asked before anything is touched.
    author = git("var", "GIT_AUTHOR_IDENT").stdout.partition(" <")[0].strip()
    if author != me:
        print(f"{flag}: git would author this commit as `{author}`, not `{me}` — the environment (GIT_AUTHOR_NAME) overrides `user.name`; "
              f"unset it, or the {noun} is filed from an account that did not give it", file=sys.stderr)
        return EXIT_LINT
    path = TRACKER_DIR / t["file"]
    rel = path.relative_to(ROOT).as_posix()
    why = how["check"]()
    if why:
        print(f"{flag}: {why}", file=sys.stderr)
        return EXIT_LINT
    branch, here, start = f"answer/{tid.lower()}", git("branch", "--show-current").stdout.strip(), git("rev-parse", "HEAD").stdout.strip()
    created = switched = False
    cut_at = start                                           # where a branch this run made stood when it was made — undo deletes it only there

    def undo(what, said=""):
        """FM-017: a run that fails after it has written anything leaves NOTHING behind. It began on a tree with no tracked
        change (refused above otherwise), so every tracked path that differs now is its own — the tracker it wrote, the
        INDEX.md a hook regenerated — and is restored. Then it goes back to the branch it started on, and an
        `answer/<id>` it cut and never committed to is deleted. Left behind, those made the Owner's next `--answer`, on
        another ask, refuse as a dirty tree without saying why. What they gave is printed with the command that gives it
        again: a refusal never costs them the words."""
        restored = changed_paths(git)
        if restored:
            git("restore", "--staged", "--worktree", "--", *[f":(top){p_}" for p_ in restored])
        recorded = record_refusal(what, said)
        back = gone = ""
        if switched:
            s_ = git("switch", here) if here else git("switch", "--detach", start)
            back = f"back on `{here or start[:10]}`" if s_.returncode == 0 else f"could NOT switch back to `{here or start[:10]}` — {s_.stderr.strip()[-160:]}"
            if created and s_.returncode == 0 and git("rev-parse", "--verify", "-q", branch).stdout.strip() == cut_at and git("branch", "-D", branch).returncode == 0:
                gone = f"`{branch}` deleted — it carried no commit"
        print(f"{flag}: {what}" + ("".join(f"\n    {l_}" for l_ in said.splitlines()) if said else ""), file=sys.stderr)
        print("  undone: " + " · ".join(x for x in (f"restored {', '.join(restored)}" if restored else "", back, gone) if x) if restored or back else "  nothing was changed", file=sys.stderr)
        if recorded:
            print(f"  {recorded}", file=sys.stderr)
        print(f"  {how['kept'][0]}, not lost: {how['kept'][1]}\n  to give it again: {how['again']}", file=sys.stderr)
        return EXIT_LINT

    def record_refusal(what, said):
        """FM-030, the E0 counter's row 20: one `--due` of theirs was refused after its cut and left nothing — the undo took
        it all back, and only their clone's reflog knew. A refusal on `answer/<id>`, the tree restored, leaves ONE line under
        `## Acts` there — `**<date> <time>** · <the command> refused — <why>` — committed and pushed, so the record and the
        forge show the attempt; their next run on this tracker names the branch and its commit, and commits on top of it.
        UNSIGNED, whoever runs the command, and honest so: the line changes no front-matter key and rules or records no act —
        the tool's report of one that did not happen — so the gate reads no right in it, a signature would prove nothing it
        needs, and the refusal may be the signing key's own.
        Refused itself, the line is taken back and the refusal is printed only; before the cut, it is printed only."""
        if git("branch", "--show-current").stdout.strip() != branch or not path.is_file():
            return ""
        command = how["again"][len(CMD) + 1:] if how["again"].startswith(CMD + " ") else how["again"]
        reason = refusal_reason(what, said)
        try:
            text = path.read_text(encoding="utf-8")
            body = parse_frontmatter(text)[1]
            put(path, text[: len(text) - len(body)] + append_record(body, ACTS_HEAD_RE, HEAD["acts"],
                                                                    f"**{datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}** · {command} refused — {reason}"))
        except OSError as e:
            return f"NOT recorded: {rel} could not be written — {e}"
        r = git("add", "--", rel)
        c = git("commit", "--no-gpg-sign", "-m", f"{tid}: {flag} refused — {first_words(reason, 60)}") if r.returncode == 0 else r
        if c.returncode:
            left = changed_paths(git)
            if left:
                git("restore", "--staged", "--worktree", "--", *[f":(top){p_}" for p_ in left])
            tail = re.sub(r"\x1b\[[0-9;]*[A-Za-z]", "", (c.stdout.strip() + "\n" + c.stderr.strip()).strip()).splitlines()
            return f"NOT recorded: the line's own commit was refused too — {(tail or ['git said nothing'])[-1].strip()[:160]}"
        sha = git("rev-parse", "--short", "HEAD").stdout.strip()
        p = git("push", "-u", "origin", branch)
        return (f"recorded under `## {HEAD['acts']}` on `{branch}`: `{sha}`, unsigned — " + ("pushed" if p.returncode == 0 else f"NOT pushed: {p.stderr.strip()[-160:]}")
                + f"; your next `{flag}` on {tid} names this branch — run it there, and it commits on top")

    if here != branch and how.get("onto"):
        # FM-030, `--revoke`: their act or answer is on its way on `answer/<id>`, not merged — the revocation commits on top of it,
        # on that branch; where this clone has only `origin`'s, a local one is made from it, tracking it
        step(2, f"switching to `{branch}` — your act is on its way there, and this commits on top of it")
        had = git("rev-parse", "--verify", "-q", f"refs/heads/{branch}").returncode == 0
        r = git("switch", branch) if had else git("switch", "-c", branch, "--track", f"refs/remotes/origin/{branch}")
        if r.returncode:
            return undo(f"could not switch to `{branch}` — {r.stderr.strip()[-300:]}")
        created, cut_at, switched = not had, git("rev-parse", "HEAD").stdout.strip(), True
    elif here != branch:
        if git("rev-parse", "--verify", "-q", f"refs/heads/{branch}").returncode == 0:
            # an `answer/<id>` left from an earlier answer on this tracker: merged, it is spent — deleted and cut fresh from
            # the branch that carries the ask; not merged, it may hold work, and nothing unmerged is ever deleted for them
            trunk = default_trunk(git)
            if not trunk or git("merge-base", "--is-ancestor", f"refs/heads/{branch}", trunk).returncode != 0:
                print(f"{flag}: `{branch}` exists and is not merged into `{ref_name(trunk) or 'origin'}` — " + unmerged_advice(git, branch, trunk, rel, tid, how, me, pend_email), file=sys.stderr)
                return EXIT_LINT
            if git("branch", "-D", branch).returncode != 0:
                print(f"{flag}: `{branch}` is merged into `{ref_name(trunk)}`, and could not be deleted — `git branch -D {branch}`, then answer again", file=sys.stderr)
                return EXIT_LINT
            print(f"{flag}: `{branch}` was left by an earlier answer and is merged into `{ref_name(trunk)}` — deleted, and cut fresh", file=sys.stderr)
        step(2, f"cutting `{branch}` from `{here or 'a detached HEAD'}` — the checkout hook, where one is installed, rebuilds the board")
        r = git("switch", "-c", branch)                        # from the branch that carries the ask: this one
        created = r.returncode == 0
        if r.returncode:
            return undo(f"could not switch to `{branch}` — {r.stderr.strip()[-300:]}")
        switched = True
    else:
        step(2, f"on `{branch}` already")
    lines, why = how["write"](path.read_text(encoding="utf-8").split("\n"), me, branch)
    if why:
        return undo(why)
    try:
        put(path, "\n".join(lines))
    except OSError as e:
        return undo(f"could not write {rel} — {e}")
    if git("add", "--", rel).returncode:
        return undo(f"could not stage {rel}")
    step(3, "committing, signed — your key may ask for a touch or its passphrase; the pre-commit gate runs" if signed
         else "committing — the pre-commit gate runs")
    r = git("commit", *(["-S"] if signed else []), "-m", how["subject"])
    if r.returncode:
        # what refused it is the HOOK's output, not git's last line — its tail, as the gate printed it
        said = re.sub(r"\x1b\[[0-9;]*[A-Za-z]", "", (r.stdout.strip() + "\n" + r.stderr.strip()).strip())
        return undo("the commit was refused — nothing is committed. What refused it:", "\n".join(said.splitlines()[-20:]) or "(git said nothing)")
    if signed and not verified_as("HEAD", signed_identity(seat, pend_name or me, pend_email) if SEATS else me):
        # the gate's own test, `verified_as`, asked here so the change is never pushed under one the gate will refuse: a good
        # signature under a key the DEFAULT branch's signers file trusts, for the author's email (FM-037's cold re-review, R1:
        # this read the clone's own file, so mid key rotation it said *pushed*, and the gate refused the answer after)
        print(f"{flag}: committed, but the signature does not verify as `{me}` — "
              + unverified("HEAD", "`git commit --amend -S`, or check the signers file") + f"; NOT pushed, and the gate would refuse this {noun}", file=sys.stderr)
        return EXIT_LINT
    step(4, "pushing to `origin`")
    r = git("push", "-u", "origin", branch)
    print(how["said"](branch, ", pushed" if r.returncode == 0 else f" — NOT pushed: {r.stderr.strip()[-160:]}"))
    if r.returncode != 0:
        return EXIT_LINT
    stamp = board_stamp()                                   # the board as the push left it: whatever writes it from here on, it is read below
    if switched:                                             # pushed: back where they started, so their next command does not begin on this one's branch
        s_ = git("switch", here) if here else git("switch", "--detach", start)
        print(f"  back on `{here or start[:10]}`" if s_.returncode == 0 else f"  could NOT switch back to `{here or start[:10]}` — {s_.stderr.strip()[-160:]}")
    said = board_after_act(stamp)
    if said:
        print(f"  {said}")
    return EXIT_OK


def board_stamp():
    """The board's file as the system keeps it — (modification time in nanoseconds, size) — or None where there is none."""
    try:
        st = HTML_OUT.stat()
    except OSError:
        return None
    return st.st_mtime_ns, st.st_size


def board_after_act(stamp):
    """FM-030, their signed answer 920970b7 — *right after the act* the board shows it: they pressed the button, ran the command,
    and the page they return to must say *done, on its way* (their words of 13:57:50). Put back where they started, the checkout hook
    `--install-hook` writes — it runs the copy of the tool kept in the git directory as `--html-only` — has written it already,
    and it reads the branch just pushed (`on_their_way`). How that is known: the board's file changed — its modification time or
    its size — between the push and now. Where it did not — no such hook is installed, the checkout ran none (they ran the command on
    `answer/<id>` itself), or the hook failed — the command rebuilds it itself, as the hook would: `--html-only`, in its own
    process; but never where the board is tracked by git — `--init` ignores it, and written, a committed board would leave
    the tree changed and refuse their next command. What it says of it, one line; "" where there is no tracker directory."""
    if not TRACKER_DIR.is_dir():
        return ""
    if board_stamp() != stamp:
        return "the board was rebuilt by the checkout hook — it reads the branch just pushed"
    tracked = (git_out("ls-files", "--", HTML_OUT.relative_to(ROOT).as_posix(), VIEW_DIR.relative_to(ROOT).as_posix()) or "").split()
    if tracked:
        return f"the board is NOT rebuilt — git tracks {tracked[0]} here, and writing it would leave the tree changed; `{CMD} --html-only` rebuilds it"
    try:
        r = subprocess.run([sys.executable, str(pathlib.Path(__file__).resolve()), "--root", str(ROOT), "--html-only"], cwd=ROOT, capture_output=True,
                           text=True, encoding="utf-8", errors="replace", env=nested_git_env(), timeout=300)
    except (OSError, subprocess.TimeoutExpired) as e:
        return f"the board was NOT rebuilt ({type(e).__name__}) — `{CMD} --html-only` rebuilds it"
    if r.returncode != 0 or board_stamp() == stamp:
        return f"the board was NOT rebuilt — `{CMD} --html-only` rebuilds it" + (f": {(r.stderr.strip().splitlines() or [''])[-1][:160]}" if r.stderr.strip() else "")
    return "the board is rebuilt — no checkout hook rebuilt it; it reads the branch just pushed"


def refusal_reason(what, said=""):
    """The one line a refused act command's record keeps (FM-030, E0 row 20): the undo's own words — `the commit was refused`,
    `could not write …` — and, from what refused the commit, the line that says so: the first that names a refusal, a
    failure or an error, else the last with words in it. Quoted as printed, flattened to one line, cut between two words."""
    head = re.sub(r"\s*(?:—\s*)?nothing is committed\.\s*What refused it:\s*$", "", what).strip()
    lines = [l_.strip() for l_ in (said or "").splitlines() if re.search(r"[A-Za-z]{2}", l_)]
    pick = next((l_ for l_ in lines if re.search(r"refus|fail|error|denied", l_, re.I)), lines[-1] if lines else "")
    return first_words(" ".join((head + (f": {pick}" if pick else "")).split()), 240)


def default_trunk(git, ask=None):
    """`origin`'s default branch, by its FULL ref — `origin/HEAD`'s target — or None: what an earlier `answer/<id>` must be merged
    into before `--answer` deletes it, and what the gate reads the branch, the Owner and their signers against. Never the short
    name: git reads a tag or a branch called `origin/main` before the remote-tracking ref (v0.19.1). `origin/HEAD`'s target is
    returned as it names it, held here or not: a walk from a ref this clone lacks fails, and says so (`read_changes`). Where
    this clone has no `origin/HEAD` and holds no `origin/main` or `origin/master` either — a pull request's shallow checkout —
    None, asking nothing. Where it holds one, a name a seat can push, a run that walks the branch's commits — `--check`, or the
    default run, on a clean tree (`_ASK_ORIGIN`) — asks origin which branch is its default (`origin_default`, once per run) and
    returns that branch's ref; where origin cannot be read, or names a branch this clone has not fetched, None, and
    `walk_problems` refuses in one line (v0.19.1). An origin that names none — its `HEAD` unborn — leaves the ref this clone
    holds, and so does a clone with no `origin` configured, which nobody can push to. Every other run — the hooks', the
    board's, the reports', the Owner's commands — asks no server and refuses nothing (`ask=False`): it takes origin's answer
    where this run has it, else the ref this clone holds, as before. What the tool prints is `ref_name`'s."""
    global _TRUNK_UNTOLD
    ask = _ASK_ORIGIN if ask is None else ask
    head = git("symbolic-ref", "--quiet", "refs/remotes/origin/HEAD").stdout.strip()
    if head.startswith("refs/remotes/"):
        return head                                     # set: nothing is asked of origin
    here = next((r for r in ("refs/remotes/origin/main", "refs/remotes/origin/master") if git("rev-parse", "--verify", "--quiet", r + "^{commit}").returncode == 0), None)
    if not here:
        return None                                     # no default branch here at all: the newest commit alone is judged, and `--check` says so
    if (not ask and _ORIGIN_DEFAULT is None) or git("config", "--get", "remote.origin.url").returncode != 0:
        return here                                     # no origin to push to, or a reader that asks no server: the ref this clone holds
    named = origin_default()
    if named == "":
        return here                                     # origin names no default branch: the one this clone holds
    if named and git("rev-parse", "--verify", "--quiet", f"refs/remotes/origin/{named}^{{commit}}").returncode == 0:
        return f"refs/remotes/origin/{named}"
    if not ask:
        return here
    _TRUNK_UNTOLD = ("the default branch cannot be told — this clone has no `origin/HEAD`, and origin "
                     + (f"names `{named}`, which this clone has not fetched: fetch it, or run" if named else "could not be read: run")
                     + " `git remote set-head origin <the default branch>`, then run again")
    return None


def origin_default():
    """The name origin gives its default branch — `git ls-remote --symref origin HEAD`, asked once per run at most and kept —
    "" where origin names none (its `HEAD` is unborn), None where origin could not be read or did not say the name. No
    prompt: a server that wants a password it is not given is one that could not be read."""
    global _ORIGIN_DEFAULT
    if _ORIGIN_DEFAULT is None:
        try:
            r = subprocess.run(["git", "ls-remote", "--symref", "origin", "HEAD"], cwd=ROOT, capture_output=True, text=True, encoding="utf-8",
                               errors="replace", timeout=60, env=dict(nested_git_env(), GIT_TERMINAL_PROMPT="0"))
        except (OSError, subprocess.TimeoutExpired):
            r = None
        lines = [l_.split("\t") for l_ in r.stdout.splitlines()] if r is not None and r.returncode == 0 else None
        named = next((sha[len("ref: refs/heads/"):] for sha, *ref in lines if sha.startswith("ref: refs/heads/") and ref == ["HEAD"]), None) if lines is not None else None
        _ORIGIN_DEFAULT = named if named else "" if lines is not None and not any(ref == ["HEAD"] for _sha, *ref in lines) else False
    return _ORIGIN_DEFAULT if _ORIGIN_DEFAULT is not False else None


_ORIGIN_DEFAULT, _TRUNK_UNTOLD, _ASK_ORIGIN = None, None, False      # per run: `configure` sets them again, and `main` the last


def ref_name(ref):
    """What the tool prints for a ref it hands git in full — `refs/remotes/origin/main` as `origin/main`, `refs/heads/main` as
    `main`; anything else as it is. Git is always handed the full ref (`default_trunk`)."""
    for prefix in ("refs/remotes/", "refs/heads/"):
        if ref and ref.startswith(prefix):
            return ref[len(prefix):]
    return ref


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
        if not KIND_RE.match(name) or not board_isfile(top / p_):      # the reading rule
            continue
        now_ = (parse_frontmatter((top / p_).read_text(encoding="utf-8"))[0].get("answer") or "").strip()
        was_ = (parse_frontmatter(git("show", f"HEAD:{p_}").stdout)[0].get("answer") or "").strip()
        if now_ and now_ != was_:
            left.append((p_, "-".join(name.split("-")[:2]), now_.strip('"'), was_))
    if not left:
        return said + " — commit or stash them first"
    generated = {pathlib.Path(os.path.relpath(f, top)).as_posix() for f in [OUT, *DERIVED_FILES]}
    mine = [p_ for p_ in dirty if p_ in {l_[0] for l_ in left} | generated]
    theirs = [p_ for p_ in dirty if p_ not in mine]
    for p_, tid, ans, had in left:
        # the three words `--answer` writes, and the verb that writes each; an answer that replaced one the file had
        # committed was a `--supersede` — or a `revoke`, which needs none — and is given again the same way
        m = re.fullmatch(r"(accepted|rejected|revoked)(?:\s+-\s+(.*))?", ans)
        verb = {"accepted": "accept", "rejected": "reject", "revoked": "revoke"}[m.group(1)] if m else ""
        said += (f"\n  {tid} carries an answer that was never committed — {ans!r}. It looks like an earlier `--answer` that failed half-way"
                 + (f"; to give it again: {CMD} --answer {tid} {verb}" + (f' "{m.group(2)}"' if m.group(2) else "")
                    + (" --supersede" if had and verb != "revoke" else "") if m else ""))
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


def mark_raised(trackers):
    """THE RAISE RULE — the Owner's answer to FM-033 (`9e48ee8`): *a raise naming a signed rule re-judges the tracker the
    same day; any other raise waits for the next pass.* `t["raised"]` is the raises of an OPEN tracker that are dated
    after its `triaged:` (any date, where it carries none) and whose `undermines:` names a signed rule: a line of the
    current path in TRIAGE.md (`path 5`, `TRIAGE.md path 5` — a number the path has), or a tracker's signed answer
    (`FM-033's answer` — a tracker with an answer that is not revoked, or an answered record under `## Asks`). Such a
    tracker is owed a pass and sits under *triage*. Clock-free: every input is a committed file, and a day decides — a raise
    written after the same day's pass is re-judged by that seat's own re-run, not by this rule. A shipped or closed tracker's raise
    changes nothing here."""
    lines = {int(n) for n in re.findall(r"^\s*(\d+)\.\s", triage_home()["path"], re.M)}
    answered = {t["id"] for t in trackers if (t.get("answer") and (answer_relation(t) or ("",))[0] != "revoked") or t.get("asks_relation")}
    def signed(what):
        m = re.fullmatch(r"(?:TRIAGE\.md\s+)?path\s+(\d+)", what, re.I)
        if m:
            return int(m.group(1)) in lines
        m = re.fullmatch(rf"({_IDS})['’]s answer", what)
        return bool(m) and m.group(1) in answered
    for t in trackers:
        t["raised"] = [r for r in t.get("raises") or [] if t["status"] in OPEN_STATUSES and r["date"] > (t.get("triaged") or "")
                       and any(signed(w) for w in r["undermines"])]
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
    acts = [(t, a) for t, a in ((t, act_of(t)) for t in sorted(trackers, key=lambda t: (t["kind"], t["num"]))) if a]
    if acts:                                        # FM-030: the acts owed to the Owner, with their time as written — no clock here
        cell = lambda v: str(v).replace("|", "\\|")
        out += ["", "### Acts owed to the Owner — with their time\n",
                "> Due, overdue or missed is the board's to say: it has a clock, and this file has none. `done:` takes an act off.\n",
                "| ID | Act | Promised | Due | Window |", "|----|-----|----------|-----|--------|"]
        out += [f"| [{t['id']}]({t['file']}) | {cell(what)} | {cell(f'{answered}: {answer}') if answer else '—'} | {due.replace('T', ' ') if due else 'no date yet'} | {window} min |"
                for t, (what, answer, answered, due, window, _asked) in acts]
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
/* the brand: a logo, the name, a tagline — and a footer, all empty unless someone says otherwise. A wordmark takes the
   place of the logo and the name, inline, so its currentColor is the name's ink: the size its height says, else the logo's */
#H{display:flex;gap:10px;align-items:center;margin-bottom:14px}#H img{height:22px;width:auto}#H b{font-size:16px}#H .wm{display:flex}#H .wm svg{display:block;flex:none}#H .wm svg:not([height]){height:22px;width:auto}#s{margin-left:auto}#H span,#f{color:var(--mute);font-size:13px}
button.act{border:1px solid var(--line);padding:2px 7px;margin-left:6px;font-size:11px;text-transform:none;letter-spacing:0}button.act:hover{border-color:var(--ink);color:var(--ink)}
/* an act that is a promise: what they promised is its line, the question it answered below it, smaller — context, not the act (FM-030) */
#p .aq{display:inline-block;padding-left:2ch;font-size:12px;color:var(--mute)}
#p summary{cursor:pointer}
#dlg{border:1px solid var(--line);background:var(--bg);color:var(--ink);max-width:640px;width:calc(100% - 32px);padding:18px 20px}#dlg::backdrop{background:rgba(0,0,0,.45)}
#dlg h3{margin:0 0 10px;font-size:14px;font-weight:600}#dlg .dq{font-size:16px;font-weight:500;margin:0 0 8px;display:block}#dlg .dp{margin:0 0 8px;color:var(--dim)}#dlg .ddim{color:var(--mute);font-size:12px}
#dlg .dl{display:flex;gap:8px;align-items:center;justify-content:flex-start;margin:8px 0 4px;font-size:14px}#dlg .dl input{margin:0;flex:0 0 auto;min-width:0;width:auto}#dlg textarea{width:100%;font:13px/1.4 system-ui,sans-serif;background:none;color:var(--ink);border:1px solid var(--line);padding:6px;margin-top:4px}#dlg textarea:disabled{opacity:.4}
#dlg menu{display:flex;gap:8px;margin:14px 0 0;padding:0}#dlg button{border:1px solid var(--line);padding:6px 12px;font-size:12px}#dlg button.go{border-color:var(--ink);color:var(--ink)}#dlg button:disabled{opacity:.4}
/* the second screen: the decision is made, the terminal signs it — the command, then where, what, the end, the check, the way out */
#dlg h4{margin:14px 0 4px;font-size:11px;font-weight:400;letter-spacing:.08em;text-transform:uppercase;color:var(--mute)}#dlg ol{margin:4px 0;padding-left:20px}#dlg li{margin:2px 0}#dlg p{margin:4px 0}
#dlg pre{font:13px/1.45 "Berkeley Mono",ui-monospace,monospace;margin:6px 0;padding:8px 10px;border:1px solid var(--line);white-space:pre-wrap;word-break:break-all}#dlg pre.cmd{border-left:2px solid var(--teal);user-select:all}
#dlg code{font:12px "Berkeley Mono",ui-monospace,monospace}#dlg button.copy{padding:2px 8px;font-size:11px;text-transform:none;letter-spacing:0}#dlg .said{margin-left:6px}#dlg .sign a{text-decoration:underline}
#l span{text-transform:lowercase}#f{margin-top:28px}#f:empty,#H span:empty{display:none}
/* three hooks a theme styles (FM-002), none of them seen without one: the Owner's box's title `.pt`, the label
   `owner.title`; the last line's one element `#F` — the claim `#f`, shown with the board only, as when it stood in it,
   and the running line `#r`; `zebra` on every other row of a group, which `nth-child` cannot count past a group's head */
.pt{display:none}#B[hidden]~#F #f{display:none}
/* the running line: the tool's, on every screen, below the footer — its mark at 16 px, the smallest size its 16-unit grid
   stays sharp at, and the name linking to the tool; the version to its release. Muted like any link here: underlined on hover */
#r{display:flex;gap:.6em;align-items:center;margin:20px 0 0;color:var(--mute);font-size:11px;line-height:16px}#r a:first-child{display:flex;gap:6px;align-items:center}#r svg{flex:none}
/* on paper the board is always the light one */
@media print{#s{display:none}}
@media print{:root{--bg:#fff;--ink:#000;--dim:#333;--mute:#555;--line:rgba(0,0,0,.25)}header,#l{display:none}}
</style>__THEMES__
<div id="B"><div id="H">__HEADMARK__<span data-l="tagline"></span><button id="s"></button></div>
<header><input id="q" autofocus>
<button id="g" aria-pressed="true"></button><button id="o" aria-pressed="true" data-l="view.open"></button><button id="a" aria-pressed="false" data-l="view.all"></button><span id="n" class="m"></span></header>
<p id="l" class="m"><i class="q"></i><span data-l="status.Proposed"></span><i class="q b"></i><span data-l="status.In Progress"></span><i class="q y"></i><span data-l="status.Parked"></span><i class="q r"></i><span data-l="status.Blocked"></span><i class="q t"></i><span data-l="status.Shipped"></span><i class="q z"></i><span data-l="status.Closed"></span></p>
<p id="p"></p>
<table><thead><tr><th data-l="col.id"><th data-l="col.tier"><th data-l="col.status">__COLHEADS__<th data-l="col.title"></thead><tbody id="b"></tbody></table></div>
<article id="v" hidden></article>
<footer id="F"><p id="f" class="m" data-l="footer"></p>
__RUNNING__</footer>
<dialog id="dlg"></dialog>
<script>__MARKED__</script>
<script>
// row = [id, tier, status, —, —, file, title, hook, num, —, —, —, [linked ids], epic, state, [#tags], [blocked_by], triaged, rank, board, [ready marks that fail — open work only], next move, intent (own or its story's), the story it is inherited from, [date, verdict, reason] of the newest pass, tokens to read it, [kind of problem, judged — else it is from the move], {derived values}, {their board display forms},
//        [ask, ask-kind, ask-since, [held up], answer, proposal, [options], [why it was sent back], answered, answered-by, supersedes, [relation, n, its words] — FM-029],
//        [the act owed to the Owner: what — for a promise, what they promised —, their answer, its date, due, window in minutes, the question it answered — FM-030; empty where none is owed],
//        and ONLY where their act or answer is on its way (FM-030, `on_their_way`): [kind — done · answer · revoked · undone · due, answer/<id>, its tip, the commit that wrote it, that commit's time, %G?, --queue's reading of it, their promise or their answer, the question, the done:, answer: or due: as written, 1 where the tip carries an answer main lacks, 1 where the act stays on their list, the due: on its way, what follows the label]]
const BLOB=__BLOB__,HOME=__HOME__,REG=__REG__,COLS=__COLS__,BCOLS=__BCOLS__,L=__LABELS__,BRANCH=__BRANCH__,T=[
__ROWS__
];
const OPEN=new Set(["In Progress","Parked","Proposed","Reserved","?"]),$=i=>document.getElementById(i),
esc=s=>s.replace(/[&<>"]/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[c])),
dec=s=>{try{return decodeURIComponent(s)}catch(e){return s}},          // `#100%` must not blank the page
// a link or an image a tracker's text makes is one of three kinds: http(s), mailto, or relative. The scheme is read as the DOM reads it — tabs, line breaks and
// control characters dropped — so `javascript:` and `data:` are refused however they are spelled (a private security report)
safeUrl=u=>{const s=String(u).replace(/[\u0000-\u0020\u007f-\u009f\u00ad\u200b-\u200f\u2028\u2029\ufeff]/g,"");return !/^[a-z][a-z0-9+.-]*:/i.test(s)||/^(https?|mailto):/i.test(s)},
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
// the board — the generator puts every tracker in exactly one of progress · triage · backlog · ended (the same
// word INDEX.md prints); `triaged` repeats the
// newest pass under `triage`. A judgement on work in progress holds __DAYS__ days, then it is back in `triage`; parked work does not go stale.
LAST=T.reduce((m,t)=>t[17]>m?t[17]:m,""),
// a bare date — `YYYY-MM-DD`, a day with no hour — is a LOCAL calendar day, as `--owner`, `--standup` and the triage worksheet count it: its age is the
// difference of two local dates, never elapsed time ÷ 24 h (`Date.parse` reads it as UTC's midnight, and a daylight-saving day has 23 or 25 hours).
// Both dates go onto one scale — their calendar fields as UTC midnights — so the difference is whole days; NaN where the text is no bare date.
ago=s=>{const m=/^(\d{4})-(\d\d)-(\d\d)$/.exec(s),n=new Date();return m?Math.round((Date.UTC(n.getFullYear(),n.getMonth(),n.getDate())-Date.UTC(+m[1],m[2]-1,+m[3]))/864e5):NaN},
fresh=t=>!!t[17]&&ago(t[17])<=__DAYS__,   // through day __DAYS__ inclusive — the same day the command stops calling it fresh
recent=t=>!!t[17]&&t[17]==LAST,
untriaged=t=>t[19]=="triage"||t[2]=="In Progress"&&!fresh(t),   // exactly what the next `--triage` lists: the generator's word, and work in progress judged too long ago
// the page's SECOND clock rule (FM-030), beside the first: an act owed to the Owner is due until its time, overdue after
// it, missed once `window:` minutes have passed with no result — read from `due:` and `window:` alone. The files carry the
// time as written; only the page knows what time it is now.
actstate=a=>!a[3]?"nodate":(now=>now<Date.parse(a[3])?"due":now<Date.parse(a[3])+a[4]*6e4?"overdue":"missed")(Date.now()),
// has a pass run? ONE answer for every line that asks: the newest date a pass left on a tracker, or else the date of the
// newest pass TRIAGE.md records. `progress` holds only what a pass kept — until a first pass it is empty by rule and says so (FM-021)
PASSED=LAST||(HOME.last.match(/\d{4}-\d\d-\d\d/)||[""])[0],
BOARD={progress:PASSED?l("desc.progress"):l("desc.progress.none"),triage:l("desc.triage","__DAYS__"),triaged:PASSED?l("desc.triaged",PASSED):l("desc.triaged.none"),backlog:l("desc.backlog"),ended:l("desc.ended")},
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
    const kids=gname=="epic"&&byId.has(k)?T.filter(t=>t[13]==k):[],open=kids.filter(t=>OPEN.has(t[2])),shipped=kids.filter(t=>t[2]=="Shipped").length,closed=kids.filter(t=>t[2]=="Closed").length,folded=shut.has(gname+k)&&!q;
    const story=kids.length?` · ${kids.length} ${l(kids.length==1?"story.chapter":"story.chapters")}: ${shipped} ${l("story.shipped")} · ${closed} ${l("story.closed")} · <span class="${open.some(t=>t[1]<"P2")?"hot":""}">${open.length} ${l("story.open")}</span>${open.some(t=>t[17])?` · ${l("word.triaged")} ${open.filter(t=>t[17]).length}/${open.length}`:""}`:"";
    const state=gname=="epic"&&byId.has(k)&&byId.get(k)[14]?`<tr class="s"><td colspan="__COLSPAN__">${esc(byId.get(k)[14])}</tr>`:gname=="board"&&k=="triaged"&&HOME.last?`<tr class="s"><td colspan="__COLSPAN__">${ids(HOME.last)}</tr>`:"";
    g.sort((x,y)=>(y[0]==k)-(x[0]==k));
    const head=`<tr class="g" data-k="${esc(gname+k)}"><td colspan="__COLSPAN__" class="m">${folded?"▸":"▾"} <b>${k=="—"?l("group.none",vn(gname)):gname=="board"?l("section."+k):esc(k)}</b>${gname=="epic"&&byId.has(k)?" "+esc(byId.get(k)[6]):""}${story||" · "+g.length}${gname=="board"?" · "+BOARD[k]:BCOLS.filter(c=>c.toLowerCase()!=gname).map(c=>[...new Set(g.map(t=>xv(t,c)).filter(v=>v!="—"))].sort(vcmp)).filter(v=>v.length).map(v=>" · "+esc(v.slice(0,6).join(" / "))+(v.length>6?" …":"")).join("")}</tr>${state}`;   // a header sums its rows up by the board's columns
    return head+(folded?"":g.map((t,i)=>`<tr class="t${gname=="epic"&&byId.has(k)&&t[0]!=k?" c":""}${i%2?" zebra":""}"><td class="m"><i class="q ${mark(t)}"></i><a href="#=${t[0]}">${t[0]}</a><td class="m ${t[1]<"P2"?"hot":""}">${t[18]?"#"+t[18]+" ":""}${t[1]}${t[21]?" → "+esc(t[21]):""}<td class="m">${esc(sl(blocked(t)?"Blocked":t[2]))}${BCOLS.map(c=>`<td class="m x">${esc((t[28]||{})[c]||xv(t,c))}`).join("")}<td><a href="${esc(BLOB)+esc(t[5])}">${esc(t[6])}</a>${t[15].map(x=>`<a href="#${encodeURIComponent(x)}" class="m k">${esc(x)}</a>`).join("")}</tr><tr class="h" hidden><td colspan="__COLSPAN__">${esc(t[7])}${blocked(t)?`<div class="m">${esc(sl(t[2]))} · ${l("word.blocked_by")} ${t[16].map(b=>byId.has(b)?`<a href="#~${b}">${b}</a>`:esc(b)).join(" ")}</div>`:""}${t[17]?`<div class="m">${l("word.triaged")} ${esc(t[17])}${t[20].length?" · "+l("word.needs")+" "+t[20].join(", "):""}</div>`:""}${chips(t[12],"→")}${chips(inb.get(t[0])||[],"←")}</tr>`).join(""))}).join("");
  const hot=rows.filter(t=>OPEN.has(t[2])&&t[1]<"P2").length,go=rows.filter(t=>t[2]=="In Progress").length,stuck=rows.filter(blocked).length;
  $("n").textContent=`${rows.length} ${hood?L["count.around"].replace("{0}",hood[0]):exact?L["count.id"].replace("{0}",exact[0]):every?L["count.trackers"]:L["count.open"]} · ${hot} P0/P1 · ${go} ${L["count.in_progress"]}${stuck?` · ${stuck} ${L["count.blocked"]}`:""}${rows.some(t=>t[17])?` · ${rows.filter(untriaged).length} ${L["count.untriaged"]}`:""}`;
  $("o").hidden=$("a").hidden=gname=="board";   // the board shows everything — open/all has nothing to say there
  $("g").textContent=L["view.by"].replace("{0}",vn(gname));$("p").innerHTML=`<span class="pt">${l("owner.title")}</span>`+(gname=="board"&&!q?(all_=>{
    // ONLY what passes the ask rules is a question here — t[29][7] is why it is not. The Owner never reads a malformed
    // ask as one; what was sent back is listed after the queue, with its reason, for the seat that wrote it.
    const w=all_.filter(t=>!t[29][7].length),sent=all_.filter(t=>t[29][7].length);
    // the answer first: what needs the Owner — how many, how old, what it holds up — then each ask as the question it is
    const days=t=>(d=>d==d?d:null)(ago(t[29][2])),old=Math.max(-1,...w.map(t=>days(t)??-1)),held=[...new Set(w.flatMap(t=>t[29][3]))];
    w.sort((a,b)=>(days(b)??-1)-(days(a)??-1));
    // an answer is the Owner's own commit: the button copies the three lines and opens the file on the forge under their login —
    // no server, no token, and the seat that asked is nowhere in the path. The commit's author is the proof.
    // Two buttons — accept · reject — open a dialog that shows the whole ask with its context, so the Owner can look and
    // abort. OK yields ONE command: `--answer <id> accept|reject "text"` — the tool cuts the answer branch, writes the
    // three lines, commits SIGNED and pushes. A browser cannot sign; the dialog decides, the terminal signs.
    // what the Owner typed goes into the copied command SINGLE-quoted: in "…" a shell runs a backtick and expands a `$` (R4)
    const sq=s=>"'"+String(s).replace(/'/g,"'\\''")+"'";
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
        const line=`${cmd} --answer ${id} ${kind}${chosen?" "+sq(chosen):""}`;
        sign(d,id,line,(kind=="accept"?"accepted":"rejected")+(chosen?" - "+chosen.replace(/\s+/g," "):""))};
      d.showModal()};
    // THE SECOND SCREEN (FM-013). OK used to disable itself and leave one button — abort — which read as taking the
    // decision back. The decision is made; the terminal signs it. This screen says what to run, where, what it does step
    // by step, what the end looks like, how to check it and where to go when signing fails — and has ONE way out, Done
    // (Esc too: it is the dialog's own). It says *Copied* only when the clipboard said so: from a file there may be none.
    const sign=(d,id,line,said,kind="answer")=>{const br=`answer/${id.toLowerCase()}`,c=s=>`<code>${esc(s)}</code>`;
      d.innerHTML=`<form method="dialog" class="sign"><h3>${l(kind=="answer"?"answer.sign.title":"act.sign.title")} · <a href="#=${id}">${id}</a></h3>
        <p class="dp">${l("answer.sign.intro")}</p><pre class="cmd">${esc(line)}</pre>
        <p class="m ddim"><button type="button" class="copy">${l("answer.sign.copy")}</button><span class="said" aria-live="polite"></span></p>
        <h4>${l("answer.sign.where")}</h4><p>${BRANCH?lh("answer.sign.where.branch",c(BRANCH)):l("answer.sign.where.text")}</p>
        <h4>${l("answer.sign.does")}</h4><ol><li>${kind.startsWith("revoke")?lh("way.sign.step.on",c(br)):lh("answer.sign.step.cut",c(br))}</li><li>${kind=="answer"?lh("answer.sign.step.write",c("answer:"),c("answered:"),c("answered-by:"),c("next: "+(byId.get(id)?.[29][1]=="action"?"owner":"build"))):lh("act.sign.step."+kind,c(kind.replace("revoke.","")+":"),c("## __ACTS_HEAD__"))}</li>
        <li>${l("answer.sign.step.commit")}</li><li>${l("answer.sign.step.push")}</li></ol><p class="ddim">${l("answer.sign.slow")}</p>
        <h4>${l("answer.sign.success")}</h4><pre>${esc(`${id} ${kind=="answer"?"answered: ":""}${said}\n  signed, on \`${br}\`, pushed`)}</pre>
        <h4>${l("answer.sign.check")}</h4><p>${lh("answer.sign.check.text",c(`git log -1 --format=%G? ${br}`),c("G"))}</p>
        <h4>${l("answer.sign.fail")}</h4><p>${lh("answer.sign.fail.text",`<a href="${l("answer.sign.url")}" target="_blank" rel="noopener">${l("answer.sign.page")}</a>`)}</p>
        <menu><button value="done" class="go">${l("answer.done")}</button></menu></form>`;
      const out=d.querySelector(".said"),copy=()=>(navigator.clipboard?.writeText?navigator.clipboard.writeText(line):Promise.reject())
        .then(()=>out.textContent=L["answer.sign.copied"],()=>out.textContent=L["answer.sign.nocopy"]);
      d.querySelector(".copy").onclick=copy;copy();d.querySelector(".go").focus()};
    window.ACT=act;
    // FM-030: an act owed to the Owner has two buttons — done · reschedule. Each asks one thing — where the result is, or the
    // new time — and OK gives ONE command, `--done <id> "<where>"` or `--due <id> <time with its zone>`, on the same second
    // screen as an answer: a browser cannot sign; the terminal does.
    const owe=(t,kind)=>{const d=$("dlg"),id=t[0],a=t[30],cmd="__CMD__";
      d.innerHTML=`<form method="dialog"><h3>${l(kind=="done"?"act.done.title":"act.due.title")} · <a href="#=${id}">${id}</a></h3>
        <p class="dq">${esc(a[0])}</p>${a[5]?`<p class="ddim">${l("acts.asked",a[5])}</p>`:""}<p class="m ddim">${a[3]?l("acts.due",a[3].replace("T"," ")):l("acts.nodate")}</p>
        ${kind=="done"?`<textarea name="text" rows="2" placeholder="${l(a[5]?"act.done.hint.promise":"act.done.hint")}" required></textarea>`:`<input name="when" type="datetime-local" required>`}
        <menu><button value="ok" class="go">${l("answer.ok")}</button><button value="abort" formnovalidate>${l("answer.abort")}</button></menu></form>`;
      const f=d.querySelector("form");
      f.onsubmit=e=>{if(e.submitter?.value!="ok")return;e.preventDefault();
        if(kind=="done"){const w=String(f.text.value).trim().replace(/\s+/g," ").replace(/"/g,"'");return sign(d,id,`${cmd} --done ${id} ${sq(w)}`,`done: ${w}`,"done")}
        // the time the Owner picks is their machine's; the command carries its zone, so it means the same hour everywhere
        const v=f.when.value,dt=new Date(v),o=-dt.getTimezoneOffset(),z=(o<0?"-":"+")+String(Math.floor(Math.abs(o)/60)).padStart(2,"0")+":"+String(Math.abs(o)%60).padStart(2,"0");
        const iso=(v.length==16?v+":00":v)+z;sign(d,id,`${cmd} --due ${id} ${iso}`,`due: ${iso}`,"due")};
      d.showModal()};
    window.OWE=owe;
    // FM-030, their signed answer 920970b7: on what is on its way, *revoke* in the place of the buttons — one field, why; OK gives
    // ONE command, `--revoke <id> "<why>"`, on the same second screen: it commits on top of their act, on its branch
    const rev=t=>{const d=$("dlg"),id=t[0],w=t[31],cmd="__CMD__";
      d.innerHTML=`<form method="dialog"><h3>${l("way.revoke.title")} · <a href="#=${id}">${id}</a></h3>
        <p class="dq">${esc(w[7])}</p>${w[8]?`<p class="ddim">${l("acts.asked",w[8])}</p>`:""}<p class="m ddim">${l("way."+w[0])} · ${esc(w[1])} @ ${esc(w[3].slice(0,7))}</p>
        <textarea name="text" rows="2" placeholder="${l("way.revoke.hint")}" required></textarea>
        <menu><button value="ok" class="go">${l("answer.ok")}</button><button value="abort" formnovalidate>${l("answer.abort")}</button></menu></form>`;
      const f=d.querySelector("form");
      f.onsubmit=e=>{if(e.submitter?.value!="ok")return;e.preventDefault();const why=String(f.text.value).trim().replace(/\s+/g," ").replace(/"/g,"'");
        sign(d,id,`${cmd} --revoke ${id} ${sq(why)}`,w[0]=="done"?`done revoked: ${why}`:`answered: revoked - ${why}`,w[0]=="done"?"revoke.done":"revoke.answer")};
      d.showModal()};
    window.REV=rev;
    return `<b class="${w.length?"hot":""}">${l("waiting.title")}: ${w.length}</b>`+(w.length?(old>=0?" · "+l("waiting.oldest",old):"")+(held.length?" · "+l("waiting.holds",held.length):"")+(w.length>__BOTTLE__?" · "+l("waiting.bottleneck",w.length,held.length):"")+"\n"+w.slice(0,14).map(t=>
      `<a href="#=${t[0]}">${t[0]}</a> `+(t[29][0]?esc(t[29][0]):`<i>${l("waiting.unasked")}</i> — ${esc(t[6])}`)+`<span class="m"> ·`+(t[29][1]?" "+l("ask."+t[29][1])+" ·":"")+(days(t)!=null?" "+l("waiting.days",days(t))+" ·":"")+(t[29][3].length?" "+l("waiting.holds.ids",t[29][3].join(", ")):"")+`</span>`+(t[29][0]?` <button class="act" onclick="ACT(T.find(x=>x[0]=='${t[0]}'),'accept')">${l("answer.accept")}</button><button class="act" onclick="ACT(T.find(x=>x[0]=='${t[0]}'),'reject')">${l("answer.reject")}</button>`:"")).join("\n").replace(/ ·<\/span>/g,"</span>")+(w.length>14?"\n…":""):"")
      +(sent.length?"\n\n<b>"+l("waiting.malformed",sent.length)+"</b>\n"+sent.map(t=>
        `<a href="#=${t[0]}">${t[0]}</a> `+(t[29][0]?esc(t[29][0]):`<i>${l("waiting.unasked")}</i>`)+`<span class="m"> — ${esc(t[29][7][0])}</span>`).join("\n"):"")})(T.filter(t=>OPEN.has(t[2])&&t[21]=="owner"&&!t[29][4]&&!(t[31]&&t[31][10])))
    // FM-030: what they owe, with its time — an accepted action ask, or any `due:` — each with its state by the clock above
    +(acts=>acts.length?"\n\n<b class=\""+(acts.some(t=>actstate(t[30])!="due"&&actstate(t[30])!="nodate")?"hot":"")+"\">"+l("acts.title")+": "+acts.length+"</b>\n"+acts.map(t=>{
      const a=t[30],s=actstate(a),when=a[3].replace("T"," ");
      return `<a href="#=${t[0]}">${t[0]}</a> ${esc(a[0])}<span class="m"> · `+(a[1]?l("acts.promised",a[2],a[1])+" · ":"")
        +`<b class="act-${s}${s=="overdue"||s=="missed"?" hot":""}">${s=="nodate"?l("acts.nodate"):s=="missed"?l("acts.missed",when,a[4]):l("acts."+s,when)}</b></span>`
        +` <button class="act" onclick="OWE(T.find(x=>x[0]=='${t[0]}'),'done')">${l("acts.done")}</button><button class="act" onclick="OWE(T.find(x=>x[0]=='${t[0]}'),'due')">${l("acts.reschedule")}</button>`
        +(a[5]?`\n<span class="aq">${l("acts.asked",a[5])}</span>`:"")}).join("\n"):"")(T.filter(t=>t[30].length&&!(t[31]&&!t[31][11])))
    // FM-030, their signed answer 920970b7: the board reads git. What they did and pushed on `answer/<id>` is here, not in the two
    // lists above, until their merge — their promise or their answer first, what it is, the branch, the commit, its time, whether it
    // verifies, and that their merge is next
    +(way=>way.length?"\n\n<b>"+l("way.title")+": "+way.length+"</b>\n"+way.map(t=>{const w=t[31];
      return `<a href="#=${t[0]}">${t[0]}</a> ${esc(w[7])}<span class="m"> · <b class="go">${l("way."+w[0])}</b>`+(w[13]?" — "+esc(w[13]):w[12]?" — "+l("acts.due",w[12].replace("T"," ")):"")
        +` · ${esc(w[1])} @ ${esc(w[3].slice(0,7))} · ${esc(w[4].slice(0,16).replace("T"," "))} · ${w[6].startsWith("merge")?l("way.signed"):l("way.unverified",w[6].replace(/^wait: /,""))} · ${w[14]?l("way.held",w[14].replace(/^wait: /,"")):l("way.merge")}</span>`
        +(w[0]=="done"||w[0]=="answer"?` <button class="act" onclick="REV(T.find(x=>x[0]=='${t[0]}'))">${l("way.revoke")}</button>`:"")
        +(w[8]?`\n<span class="aq">${l("acts.asked",w[8])}</span>`:"")}).join("\n"):"")(T.filter(t=>t[31]))
    +(HOME.path?"\n\n<b>"+l("path.title")+"</b> — __HOME_PATH__\n"+ids(HOME.path):"")
    // the registry, a report of the trailers (FM-024, FM-032): who committed in the last day, where — and how independent this week's verdicts were
    +(REG?(REG.groups.length?"\n\n<b>"+l("sessions.recent",REG.parents,REG.all)+"</b>\n"
        +REG.groups.map(g=>`<details><summary>${esc(g[0])} ${esc(g[1])} (${esc(g[2])})${g[3].map(x=>" · "+esc(x)).join("")}</summary>`
          +g[4].map(m=>`<span class="aq">${esc(m[0])} (${esc(m[1])}) · ${esc(m[2])} · ${esc(m[3])}</span>`).join("\n")+"</details>").join(""):"")
      +(REG.reviews?(REG.groups.length?"\n":"\n\n")+l("reviews.week",REG.reviews[0],REG.reviews[1])+(REG.reviews[2]?" · "+l("reviews.untraced",REG.reviews[2]):"")+(REG.reviews[3]?" · "+l("reviews.trunk",REG.reviews[3]):""):""):""):"");   // the box keeps its title in every view (FM-002 R2)
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
marked.use({renderer:{html:k=>esc(k.raw||k.text||""),
  link(k){return safeUrl(k.href)&&!/&(#|colon|tab|newline)/i.test(k.href)?false:this.parser.parseInline(k.tokens)},      // false: the renderer's own link; refused, the text stays
  image(k){return safeUrl(k.href)&&!/^mailto:/i.test(String(k.href).trim())&&!/&(#|colon|tab|newline)/i.test(k.href)?false:esc(k.text||"")}},extensions:[{name:"tid",level:"inline",start:s=>s.match(new RegExp("\\b"+TID.source))?.index,
  tokenizer(s){if(this.lexer.state.inLink)return;const m=new RegExp("^"+TID.source).exec(s);if(m&&byId.has(m[0])&&"#="+m[0]!=dec(location.hash))return{type:"tid",raw:m[0]}},
  renderer:k=>`<a href="#=${k.raw}">${k.raw}</a>`}]});
V=(id,md)=>{MD.set(id,md);if(dec(location.hash)=="#="+id)view(id)};
function view(id){
  const v=$("v"),t=byId.get(id);$("B").hidden=true;v.hidden=false;scrollTo(0,0);
  if(!MD.has(id)){const s=document.createElement("script");s.src="view/"+id+".js";
    s.onerror=()=>v.innerHTML=`<p class="m"><a href="#">${l("viewer.board")}</a> · ${l("viewer.no_copy",id,"__CMD__ --html-only")}</p>`;
    v.innerHTML=`<p class="m">${id} …</p>`;return document.head.append(s)}
  const facts=[sl(blocked(t)?"Blocked":t[2]),t[1]!="—"&&t[1],t[18]&&"#"+t[18],L["section."+board(t).at(-1)]||board(t).at(-1),t[25]&&L["word.reads"]+" "+(t[25]/1000).toFixed(1)+"k",t[17]&&L["word.triaged"]+" "+t[17],...COLS.map(c=>xv(t,c)!="—"&&c.toLowerCase()+" "+((t[28]||{})[c]||xv(t,c))),...t[15]];
  v.innerHTML=`<p class="m"><a href="#">${l("viewer.board")}</a> · <a href="#~${id}">${l("viewer.neighbours")}</a> · <a href="${esc(t[5])}">${l("viewer.file")}</a>${BLOB?` · <a href="${esc(BLOB)+esc(t[5])}">${l("viewer.forge")}</a>`:""}</p>
<p class="m f"><i class="q ${mark(t)}"></i>${facts.filter(Boolean).map(esc).join(" · ")}${t[13]!="—"?` · ${l("word.story")} <a href="#=${esc(t[13])}">${esc(t[13])}</a>`:""}</p>
${t[29][4]?`<p class="m hd"><b>${l("viewer.answer")}</b> — ${esc(t[29][4])}${(r=>r.length?` · <i>${l("relation."+r[0],r[1])}${r[2]?": "+esc(r[2]):""}</i>`:"")(t[29][11])}${[t[29][8],t[29][9]].filter(Boolean).map(x=>" · "+esc(x)).join("")}${t[29][10]?" · "+l("viewer.supersedes",esc(t[29][10])):""}</p>`:""}
${OPEN.has(t[2])||t[22]||t[24].length?`<p class="m hd"><b>${l("viewer.intent")}</b> — ${t[22]?esc(t[22])+(t[23]?` <a href="#=${esc(t[23])}">(${l("viewer.from",t[23])})</a>`:""):"<i>"+l("viewer.intent.missing")+"</i>"}<br>
<b>${l("viewer.verdict")}</b> — ${t[24].length?`<code>${esc(t[24][1])}</code> · ${esc(t[24][0])}${t[2]=="In Progress"&&ago(t[24][0])>__DAYS__?" · <i>"+l("viewer.stale","__DAYS__")+"</i>":""}${t[24][2]?" · "+esc(t[24][2]):""}`:"<i>"+l("viewer.verdict.none")+"</i>"}<br>
<b>${l("viewer.handover")}</b> — ${l("viewer.next")}: ${t[21]?esc(t[21]):"<i>"+l("word.missing")+"</i>"}${t[21]?" · "+l("viewer.kind")+": "+(t[26][0]?esc(t[26][0])+(t[26][1]?"":" <i>("+l("viewer.from_move")+")</i>"):"<i>"+l("word.missing")+"</i>"):""} · ${l("viewer.true_now")}: ${t[20].includes("stated")?"<i>"+l("word.missing")+"</i>":l("word.stated")}${(c=>c.length?`<br>
<b>${l("story.chapters")}</b> — ${c.length}: ${Object.entries(c.filter(x=>x[2]=="In Progress"||x[2]=="Proposed").reduce((m,x)=>(m[x[21]||"no move named"]=[...(m[x[21]||"no move named"]||[]),x[0]],m),{})).map(([k,v])=>k=="no move named"?`${v.length} ${l("viewer.no_move")}`:`${esc(k)} ${v.map(i=>`<a href="#=${i}">${i}</a>`).join(" ")}`).join(" · ")||l("viewer.none_in_progress")} · ${c.filter(x=>x[2]=="Parked").length} ${l("story.parked")} · ${c.filter(x=>x[2]=="Shipped").length} ${l("story.shipped")} · ${c.filter(x=>x[2]=="Closed").length} ${l("story.closed")}`:"")(T.filter(x=>x[13]==t[0]))}${t[20].filter(n=>n!="stated"&&n!="intended").length?" · "+l("word.needs")+" "+t[20].filter(n=>n!="stated"&&n!="intended").join(", "):""}</p>`:""}${chips(t[16].filter(b=>byId.has(b)),l("word.blocked_by"),"=")}${chips(t[12],"→","=")}${chips(inb.get(id)||[],"←","=")}<div class="md">${marked.parse(MD.get(id))}</div>`;
  for(const i of v.querySelectorAll(".md img"))if(!safeUrl(i.getAttribute("src")||"")||/^mailto:/i.test((i.getAttribute("src")||"").trim()))i.replaceWith(document.createTextNode(i.alt||""));      // the DOM's last word on what an image loads
  for(const a of v.querySelectorAll(".md a")){const h=a.getAttribute("href")||"",m=h.match(new RegExp("^("+TID.source+")-[^/]*\\.md"));
    if(!safeUrl(h)){a.removeAttribute("href");continue}
    if(m&&byId.has(m[1]))a.href="#="+m[1];else if(h[0]=="#"&&h[1]!="="){a.removeAttribute("href");a.dataset.s=dec(h.slice(1))}else if(!/^[a-z]+:/i.test(h)&&h[0]!="#")a.href=BLOB+h}
  // headings get GitHub's slug, so a tracker's own `#section` links work; a long tracker gets its sections listed.
  // The hash belongs to the router, so these scroll by click, not by address.
  const hs=[...v.querySelectorAll(".md h2,.md h3")];
  for(const h of hs)h.id="h-"+h.textContent.toLowerCase().replace(/[^\p{L}\p{N}\s-]/gu,"").trim().replace(/\s/g,"-");
  const h2=hs.filter(h=>h.tagName=="H2");
  if(h2.length>5)v.querySelector(".md").insertAdjacentHTML("beforebegin",`<p class="m toc">${h2.map(h=>`<a data-s="${esc(h.id.slice(2))}">${esc(h.textContent)}</a>`).join(" · ")}</p>`);
  if(want!=null){scrollTo(0,want);want=null}      // back from a reload: where the person was
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
// reload: begin — the board and its tracker pages (one page: `#=ID` is a tracker's) reload themselves when the tab is visible again, so what a checkout, a merge or a pull
// changed is on the screen when the person comes back. The same page and nothing else: no poll, no timer, no second file, no server. Never while a dialog is open or a field
// holds input — the search box aside: its filter, typed or linked, is kept across the reload, as the scroll position is.
let want=null,wantQ=null,hiddenAt=0;
try{const k=JSON.parse(sessionStorage.getItem("shoalmark.keep")||"null");sessionStorage.removeItem("shoalmark.keep");if(k&&k.h==location.hash&&Date.now()-k.t<1e4){want=k.y;wantQ=typeof k.q=="string"?k.q:null}}catch(e){}
const busy=()=>$("dlg").open||[...document.querySelectorAll("input:not(#q):not([type=radio]):not([type=checkbox]):not([type=hidden]),textarea,select")].some(e=>e.value!=="");
document.addEventListener("visibilitychange",()=>{
  if(document.visibilityState=="hidden"){hiddenAt=1;return}
  if(!hiddenAt||busy())return;hiddenAt=0;
  try{sessionStorage.setItem("shoalmark.keep",JSON.stringify({h:location.hash,y:scrollY,q:$("q").value,t:Date.now()}))}catch(e){}
  location.reload()});
// reload: end
(onhashchange=()=>{const h=dec(location.hash.slice(1));if(h[0]=="="&&byId.has(h.slice(1)))return view(h.slice(1));
  $("v").hidden=true;$("B").hidden=false;$("q").value=wantQ??h;wantQ=null;draw();scrollTo(0,want??0);want=null})();
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
    "section.progress": "progress", "section.triage": "triage", "section.triaged": "triaged", "section.backlog": "backlog", "section.ended": "ended",
    "desc.progress": "kept by triage — by rank, then tier",
    "desc.progress.none": "empty until a first triage pass has run — --triage",
    "desc.triage": "what the next --triage lists — in progress and unjudged or judged over {0} days ago, and new filings",
    "desc.triaged": "judged {0} — each also sits in its own section", "desc.triaged.none": "no triage pass has run yet",
    "desc.backlog": "waiting — P0 to P3, then untiered, then parked", "desc.ended": "shipped, or closed without shipping",
    "group.none": "no {0}",
    "count.trackers": "trackers", "count.open": "open", "count.around": "around {0}", "count.id": "tracker · {0}", "count.in_progress": "in progress",
    "count.blocked": "blocked", "count.untriaged": "untriaged",
    "owner.title": "owed to the owner",   # the title of the Owner's box — shown by a theme that styles `.pt` (FM-002)
    "path.title": "the current path", "waiting.title": "waiting for you", "waiting.detail": "open work whose next move is the Owner's",
    "waiting.oldest": "oldest {0} days", "waiting.holds": "holding up {0} more", "waiting.days": "{0} days", "waiting.holds.ids": "holds up {0}",
    "waiting.unasked": "not yet stated as a question",
    "waiting.bottleneck": "you are the bottleneck — {0} asks, {1} trackers held up",
    "waiting.malformed": "{0} asks sent back — not for you",
    # an act that is a promise (FM-030, the Owner's word of 2026-09-27 13:38:30): its line is what they promised, `acts.promised`
    # the day they did — {1}, their answer as signed, is there for a table that quotes it — and `acts.asked` the question below
    "acts.title": "your acts, with their time", "acts.promised": "promised {0}", "acts.asked": "asked: {0}", "acts.due": "due {0}", "acts.overdue": "overdue — due {0}",
    "acts.missed": "missed — due {0}, and {1} minutes passed with no result", "acts.nodate": "no date yet",
    "acts.done": "done", "acts.reschedule": "reschedule", "act.done.title": "Done — where is the result?", "act.done.hint": "the path to the result, or where it is",
    "act.done.hint.promise": "the path to the result of this promise, or where it is",
    "act.due.title": "Reschedule — to when?", "act.sign.step.done": "writes {0} — the time, and where the result is — and its record under {1}",
    "act.sign.step.due": "writes the new {0}, and the old one into the record under {1} — the board reads it rescheduled, on its way, until your merge",
    # FM-030, their signed answer 920970b7: what they did and pushed, before their merge — the board, `--owner` and `--standup`
    "way.title": "on their way", "way.merge": "your merge is next", "way.held": "your merge waits: {0}", "way.done": "done, on its way", "way.answer": "answered, on its way",
    "way.revoked": "revoked, on its way", "way.undone": "done revoked, on its way", "way.due": "rescheduled, on its way", "way.signed": "signed", "way.unverified": "not verified here: {0}",
    "way.revoke": "revoke", "way.revoke.title": "Revoke — why?", "way.revoke.hint": "why you take it back — the record keeps it beside what it revokes",
    "way.sign.step.on": "commits on {0}, where it is on its way — one branch per exchange",
    "act.sign.step.revoke.done": "removes {0} and records the revocation under {1} — the act is owed again",
    "act.sign.step.revoke.answer": "writes {0} as revoked — the answer it takes back goes into the ship log",
    "sessions.recent": "sessions · {0} in the last day ({1} with their sub-sessions)",
    "reviews.week": "reviews this week · independent {0} · same session {1}", "reviews.untraced": "untraced {0}", "reviews.trunk": "on trunk {0}",
    "answer.accept": "accept", "answer.reject": "reject", "answer.proposal": "the seat proposes:", "answer.other": "Other:", "answer.recommended": "recommended",
    "answer.change.hint": "your change, in one line — more goes in the tracker's body", "answer.reject.hint": "why, and how the ask should be reworded (required)",
    "answer.ok": "OK — give me the command", "answer.abort": "abort",
    # the second screen (FM-013) — `{0}` in these is markup the page builds: a branch or a key as code, the signing link
    "answer.sign.title": "Sign your answer", "act.sign.title": "Sign your act",
    "answer.sign.intro": "Your decision is made. A browser cannot sign it — your terminal does, with your key. Run this command:",
    "answer.sign.copy": "Copy again", "answer.sign.copied": "Copied.",
    "answer.sign.nocopy": "Not copied — this page has no clipboard here (a board opened from a file often has none). Select the command and copy it.",
    "answer.sign.where": "Where", "answer.sign.where.text": "In a terminal, in this repository, on the branch that carries the ask.",
    "answer.sign.where.branch": "In a terminal, in this repository, on the branch that carries the ask — {0}, the branch this board was built from.",
    "answer.sign.does": "What it does", "answer.sign.step.cut": "cuts {0} from the branch you are on",
    "answer.sign.step.write": "writes the three lines — {0} {1} {2} — and {3}", "answer.sign.step.commit": "commits them, signed with your key — a hardware key waits for your touch",
    "answer.sign.step.push": "pushes the branch",
    "answer.sign.slow": "It prints each step as it starts, and it may take a while: the checkout and the commit each run the gate over every tracker.",
    "answer.sign.success": "When it worked", "answer.sign.check": "To check",
    "answer.sign.check.text": "{0} prints {1} — a good signature, under a key this repository trusts.",
    "answer.sign.fail": "If it fails", "answer.sign.fail.text": "No signing key is set, or the signature does not verify: set up your key once — {0}.",
    "answer.sign.page": "the signing page", "answer.sign.url": SIGNING_PAGE,
    "answer.done": "Done",
    "ask.ruling": "a ruling", "ask.action": "your hands", "ask.determination": "evidence could settle it", "ask.ceremony": "a button",
    "story.chapter": "chapter", "story.chapters": "chapters", "story.shipped": "shipped", "story.closed": "closed", "story.open": "open", "story.parked": "parked",
    "word.triaged": "triaged", "word.needs": "needs", "word.blocked_by": "blocked by", "word.reads": "reads", "word.story": "story",
    "word.missing": "missing", "word.stated": "stated",
    "viewer.board": "← board", "viewer.neighbours": "neighbours", "viewer.file": "file", "viewer.forge": "forge",
    "viewer.no_copy": "no rendered copy of {0} — run {1}",
    "viewer.intent": "intent", "viewer.from": "from {0}", "viewer.intent.missing": "missing — the Owner states it on the tracker or its story",
    "viewer.verdict": "verdict", "viewer.verdict.none": "none yet — no triage pass has judged it",
    "viewer.answer": "the Owner's answer", "viewer.supersedes": "supersedes {0}",
    # the answer's relation to the proposal (FM-029), beside the answer — the word the Owner signed stays as it is
    **{"relation." + k: v for k, v in RELATION_TEXT.items()},
    "viewer.stale": "stale — older than {0} days, it counts as untriaged again",
    "viewer.handover": "hand-over", "viewer.next": "next", "viewer.kind": "kind", "viewer.from_move": "from the move",
    "viewer.true_now": "what is true now", "viewer.no_move": "with no move named", "viewer.none_in_progress": "none in progress",
}
BRAND_FILES = ("theme.css", "logo.svg", "logo.png", "wordmark.svg", "labels.yaml")
# The tool's own mark, the Pricke (FM-006) — the site's `overrides/.icons/shoalmark/pricke.svg`, one path on a 16-unit
# grid. The running line ends every page with it: the tool's name and version, not a brand, not a label, in every repository.
PRICKE = "M4 0h1v1h-1ZM11 0h1v1h-1ZM0 1h1v1h-1ZM4 1h1v1h-1ZM11 1h1v1h-1ZM15 1h1v1h-1ZM1 2h1v1h-1ZM5 2h1v1h-1ZM10 2h1v1h-1ZM14 2h1v1h-1ZM2 3h1v1h-1ZM5 3h1v1h-1ZM10 3h1v1h-1ZM13 3h1v1h-1ZM3 4h1v1h-1ZM6 4h1v1h-1ZM9 4h1v1h-1ZM12 4h1v1h-1ZM4 5h1v1h-1ZM6 5h1v1h-1ZM9 5h1v1h-1ZM11 5h1v1h-1ZM5 6h1v1h-1ZM7 6h2v1h-2ZM10 6h1v1h-1ZM6 7h4v1h-4ZM7 8h2v1h-2ZM7 9h2v1h-2ZM7 10h2v1h-2ZM7 11h2v1h-2ZM7 12h2v1h-2ZM7 13h2v1h-2ZM7 14h2v1h-2ZM7 15h2v1h-2Z"
LOGO_MAX = 200_000            # bytes — a logo or a wordmark is inlined into the page; past this it is skipped, with a warning
# What an inlined SVG may be. A logo sits in an <img>, where nothing an SVG carries can run or load; a wordmark sits IN
# the page, where a script would run, a handler fire, a reference load and a style restyle the board — so it is held to a
# grammar, not screened for bad words, and written out again from what was read (0.18.2; the Reviewer's R1–R9).
#   the file   at most LOGO_MAX bytes; UTF-8, no byte-order mark, no control character (C0 but tab and line ends, DEL,
#              C1); no DOCTYPE, ENTITY or CDATA; an <?xml?> that names an encoding names UTF-8 — all before the parse
#   the tree   at most SVG_DEPTH deep; only the elements below (another namespace's are left out, with what they hold);
#              every id defined once; every reference — a <use>'s href, a url(#id) in fill, stroke, mask or clip-path —
#              to an id the file has, followed at most SVG_REF_DEPTH deep, never in a cycle, and at most SVG_DRAWN
#              elements painted with every reference followed (a mask used n times paints n times)
#   attributes only those the element's row names — no style, no class, no handler, nothing else — each value ASCII,
#              without \ & < http data: javascript, and whole in its kind, read by one pass of a scanner, never a regex:
#                number   -?[0-9]+(.[0-9]+)?   — no +, no exponent, no .5; a length adds px or % (a font size em)
#                list     numbers, one space or one comma between two (x, y, dx, dy, points; viewBox exactly four)
#                path     path letters and numbers; one space or one comma between two numbers, at most one around a
#                         letter; nothing before the first, nothing after the last
#                transform  name(list) — matrix translate scale rotate skewX skewY — one space or comma between two
#                paint    #hex (3, 4, 6, 8) · currentColor · none · a plain colour name · url(#id); mask, clip: none · url(#id)
#              at most SVG_VALUE characters a value (a path's and points' at most SVG_TOKENS tokens), and SVG_BUDGET steps
#              for the whole file — every token read and every element visited is a step; past it, the file is refused
_SVG_SHAPE = {"id", "fill", "fill-opacity", "fill-rule", "stroke", "stroke-width", "stroke-opacity", "stroke-linecap", "stroke-linejoin",
              "stroke-miterlimit", "opacity", "transform", "clip-path", "clip-rule", "mask", "shape-rendering"}
_SVG_TEXT = {"x", "y", "dx", "dy", "font-family", "font-size", "font-weight", "font-style", "text-anchor", "letter-spacing", "xml:space"}
SVG_ATTRS = {
    "svg": _SVG_SHAPE | {"viewBox", "width", "height", "x", "y", "preserveAspectRatio", "version", "xml:space"},
    "g": _SVG_SHAPE, "defs": {"id"}, "symbol": _SVG_SHAPE | {"viewBox", "preserveAspectRatio"},
    "use": _SVG_SHAPE | {"href", "x", "y", "width", "height"}, "title": set(), "desc": set(), "metadata": set(),
    "path": _SVG_SHAPE | {"d"}, "rect": _SVG_SHAPE | {"x", "y", "width", "height", "rx", "ry"}, "circle": _SVG_SHAPE | {"cx", "cy", "r"},
    "ellipse": _SVG_SHAPE | {"cx", "cy", "rx", "ry"}, "line": _SVG_SHAPE | {"x1", "y1", "x2", "y2"},
    "polyline": _SVG_SHAPE | {"points"}, "polygon": _SVG_SHAPE | {"points"}, "text": _SVG_SHAPE | _SVG_TEXT, "tspan": _SVG_SHAPE | _SVG_TEXT,
    "clipPath": {"id", "transform", "clipPathUnits"}, "mask": {"id", "x", "y", "width", "height", "maskUnits", "maskContentUnits"},
    "linearGradient": {"id", "x1", "y1", "x2", "y2", "gradientUnits", "gradientTransform", "spreadMethod"},
    "radialGradient": {"id", "cx", "cy", "r", "fx", "fy", "gradientUnits", "gradientTransform", "spreadMethod"},
    "stop": {"offset", "stop-color", "stop-opacity"},
}
SVG_DEPTH, SVG_DRAWN, SVG_REF_DEPTH = 32, 2000, 3
SVG_VALUE, SVG_TOKENS, SVG_BUDGET = 1000, 20_000, 200_000
SVG_NS, XLINK_NS, XML_NS = "http://www.w3.org/2000/svg", "http://www.w3.org/1999/xlink", "http://www.w3.org/XML/1998/namespace"
_SVG_COLOURS = {"currentColor", "none", "black", "white", "silver", "gray", "grey", "red", "maroon", "orange", "yellow", "olive", "lime",
                "green", "teal", "aqua", "cyan", "blue", "navy", "fuchsia", "magenta", "purple", "transparent"}
_SVG_ENUMS = {
    "fill-rule": {"nonzero", "evenodd"}, "clip-rule": {"nonzero", "evenodd"}, "stroke-linecap": {"butt", "round", "square"},
    "stroke-linejoin": {"miter", "round", "bevel"}, "shape-rendering": {"auto", "crispEdges", "geometricPrecision", "optimizeSpeed"},
    "gradientUnits": {"userSpaceOnUse", "objectBoundingBox"}, "clipPathUnits": {"userSpaceOnUse", "objectBoundingBox"},
    "maskUnits": {"userSpaceOnUse", "objectBoundingBox"}, "maskContentUnits": {"userSpaceOnUse", "objectBoundingBox"},
    "spreadMethod": {"pad", "reflect", "repeat"}, "font-weight": {"normal", "bold", *(f"{n}00" for n in range(1, 10))},
    "font-style": {"normal", "italic", "oblique"}, "text-anchor": {"start", "middle", "end"}, "xml:space": {"default", "preserve"},
    "preserveAspectRatio": {"none", *(f"x{a}Y{b}{m}" for a in ("Min", "Mid", "Max") for b in ("Min", "Mid", "Max") for m in ("", " meet", " slice"))},
}
_SVG_NUMBERS = {  # attribute: (units a number may carry, at most how many numbers — 0 is any, up to SVG_TOKENS)
    **{k: (("", "px", "%"), 1) for k in ("width", "height", "rx", "ry", "cx", "cy", "r", "fx", "fy", "x1", "y1", "x2", "y2", "stroke-width", "stroke-miterlimit")},
    **{k: (("", "%"), 1) for k in ("opacity", "fill-opacity", "stroke-opacity", "stop-opacity", "offset")},
    **{k: (("", "px", "%"), 0) for k in ("x", "y", "dx", "dy")},
    "font-size": (("", "px", "em", "%"), 1), "letter-spacing": (("", "px", "em"), 1), "version": (("",), 1), "points": (("",), 0), "viewBox": (("",), 4),
}
_SVG_PATH_LETTERS, _SVG_TRANSFORMS = set("MmZzLlHhVvCcSsQqTtAa"), ("matrix(", "translate(", "scale(", "rotate(", "skewX(", "skewY(")


def _svg_number(v, i):
    """The end of the number -?[0-9]+(.[0-9]+)? that starts at i, or -1. One step a character, never back."""
    n = len(v)
    if i < n and v[i] == "-":
        i += 1
    j = i
    while i < n and "0" <= v[i] <= "9":
        i += 1
    if i == j:
        return -1
    if i < n and v[i] == ".":
        i += 1; j = i
        while i < n and "0" <= v[i] <= "9":
            i += 1
        if i == j:
            return -1
    return i


def _svg_value(key, v):
    """How many tokens `v` is, read whole as `key`'s kind in one pass — or -1 at the first character that does not fit.
    The kinds are the comment above SVG_ATTRS; nothing here backtracks, so a value costs its length and no more."""
    n = len(v)
    is_id = lambda t: 0 < len(t) <= 64 and t[0].isalpha() and all(c.isalnum() or c in "_-" for c in t)
    ref = lambda t: t.startswith("url(#") and t.endswith(")") and is_id(t[5:-1])
    if key == "id":
        return 1 if is_id(v) else -1
    if key == "href":
        return 1 if v[:1] == "#" and is_id(v[1:]) else -1
    if key in ("fill", "stroke", "stop-color"):
        hexa = v[:1] == "#" and len(v) in (4, 5, 7, 9) and all(c in "0123456789abcdefABCDEF" for c in v[1:])
        return 1 if hexa or v in _SVG_COLOURS or key != "stop-color" and ref(v) else -1
    if key in ("mask", "clip-path"):
        return 1 if v == "none" or ref(v) else -1
    if key in _SVG_ENUMS:
        return 1 if v in _SVG_ENUMS[key] else -1
    if key == "font-family":
        return 1 if v and all(c.isalnum() or c in " ,'-" for c in v) else -1
    if key in _SVG_NUMBERS:                                 # numbers, each with a unit it may carry, one separator between two
        units, most = _SVG_NUMBERS[key]
        i, count = 0, 0
        while True:
            i = _svg_number(v, i)
            if i < 0:
                return -1
            i += next((len(u) for u in units if u and v.startswith(u, i)), 0)
            count += 1
            if count > (most or SVG_TOKENS):
                return -1
            if i == n:
                return count if most in (0, 1) or count == most else -1
            if v[i] not in " ,":
                return -1
            i += 1
    if key == "d":                                          # letters and numbers; a separator only between two tokens, at most one
        i, count, last = 0, 0, ""                           # last: "" nothing yet · L a letter · N a number · S a separator
        while i < n:
            c = v[i]
            if c in _SVG_PATH_LETTERS:
                i, last = i + 1, "L"
            elif c in " ,":
                if last in ("", "S"):
                    return -1
                i, last = i + 1, "S"
            else:
                if last == "N":
                    return -1                               # two numbers need a separator: no 1-2, no .5.5
                i, last = _svg_number(v, i), "N"
                if i < 0:
                    return -1
            count += 1
            if count > SVG_TOKENS:
                return -1
        return count if last != "S" else -1
    if key in ("transform", "gradientTransform"):          # name(numbers), one separator or none between two
        i, count = 0, 0
        while True:
            name = next((f for f in _SVG_TRANSFORMS if v.startswith(f, i)), None)
            if not name:
                return -1
            i += len(name)
            while True:
                i = _svg_number(v, i)
                if i < 0:
                    return -1
                count += 1
                if count > SVG_TOKENS:
                    return -1
                if i < n and v[i] in " ," and i + 1 < n and v[i + 1] != ")":
                    i += 1
                    continue
                break
            if i >= n or v[i] != ")":
                return -1
            i += 1
            if i == n:
                return count
            if v[i] in " ,":
                i += 1
    return -1


def brand_bytes(f):
    """A brand file's bytes and its size as the cap counts them. An SVG is text: its line ends are counted and inlined as
    committed, `\r\n` as `\n` — a Windows checkout (`core.autocrlf`) writes the same file one byte longer per line, and
    the cap refused there what it showed everywhere else (FM-035). A PNG is read as it is. A file past twice the cap is
    not read at all: no line-end conversion brings it under."""
    size = f.stat().st_size
    if size > 2 * LOGO_MAX:
        return b"", size
    data = f.read_bytes()
    data = data.replace(b"\r\n", b"\n") if f.suffix == ".svg" else data
    return data, len(data)


def inline_svg(data, prefix="wm-"):
    """(markup, "") — the SVG written out again from what was read, safe to put in the page — or ("", why it is not).
    The rules are the comment above SVG_ATTRS; the first one broken refuses the file whole. Every id gets `prefix`, and
    every `#id` it is referred to by, so no id of the page's is ever shadowed; an underscore is written `&#95;`, so no
    `__PLACEHOLDER__` of the page's template can be spelled inside it. No step recurses, and none backtracks: the whole
    file costs at most SVG_BUDGET steps, and the count of what it paints stops the moment it passes SVG_DRAWN."""
    import xml.etree.ElementTree as ET
    if len(data) > LOGO_MAX:
        return "", f"it is {len(data):,} bytes — over {LOGO_MAX:,}"
    try:
        if data.startswith((b"\xef\xbb\xbf", b"\xff\xfe", b"\xfe\xff")):
            raise UnicodeError
        text = data.decode("utf-8")
    except UnicodeError:
        return "", "it is not UTF-8 without a byte-order mark"
    if re.search(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f-\x9f]", text):
        return "", "it holds a control character"
    if re.search(r"<!(?:DOCTYPE|ENTITY)|<!\[CDATA\[", text, re.I):
        return "", "it declares a DOCTYPE, an entity or CDATA"
    decl = re.match(r"\s*<\?xml\b[^>]*?\bencoding\s*=\s*[\"']([^\"']*)", text[:200])
    if decl and decl.group(1).lower().replace("-", "") != "utf8":
        return "", f"its <?xml?> names the encoding {decl.group(1)[:20]}, not UTF-8"

    class Builder(ET.TreeBuilder):                          # a DOCTYPE the checks above missed still stops the parse
        def doctype(self, *_):
            raise ValueError("it declares a DOCTYPE")
    try:
        top = ET.fromstring(text.encode("utf-8"), parser=ET.XMLParser(target=Builder(), encoding="utf-8"))
    except ValueError as e:
        return "", str(e)
    except ET.ParseError as e:
        return "", f"it is not well-formed XML ({e})"
    split = lambda n: n[1:].partition("}")[::2] if isinstance(n, str) and n.startswith("{") else ("", n)
    if split(top.tag) != (SVG_NS, "svg"):
        return "", "its root is not an <svg> in the SVG namespace"
    steps = [0]

    def spend(k):
        steps[0] += k
        if steps[0] > SVG_BUDGET:
            raise ValueError(f"it takes over {SVG_BUDGET:,} steps to check")
    esc = lambda t: html_escape(t).replace("_", "&#95;")
    try:
        stack = [(top, 1)]
        while stack:                                        # the depth first, without recursion: 1,000 nested <g> is a refusal
            e, depth = stack.pop()
            spend(1)
            if depth > SVG_DEPTH:
                raise ValueError(f"it nests deeper than {SVG_DEPTH}")
            stack.extend((c, depth + 1) for c in e)
        out, ids, edges, stack = [], {}, [], [top]
        while stack:
            e = stack.pop()
            if isinstance(e, str):                           # a closing tag and the text after it
                out.append(e)
                continue
            spend(1)
            ns, tag = split(e.tag)
            tail = "" if e is top else esc(e.tail or "")
            if ns != SVG_NS:
                out.append(tail)
                continue
            if tag not in SVG_ATTRS:
                raise ValueError(f"it holds <{tag}>")
            attrs, refs = "", []
            for k, v in e.attrib.items():
                kns, name = split(k)
                if kns not in ("", XLINK_NS, XML_NS):
                    continue                                 # an editor's own attribute (Inkscape's, Sketch's) draws nothing
                key = "xml:" + name if kns == XML_NS else name
                if key not in SVG_ATTRS[tag] or kns == XLINK_NS and name != "href":
                    raise ValueError(f"it holds {'xlink:' if kns == XLINK_NS else ''}{key}= on <{tag}>, which a wordmark may not carry")
                low = v.lower()
                bad = (not v.isascii() or any(c in v for c in "\\&<") or "http" in low or "data:" in low or "javascript" in low
                       or len(v) > SVG_VALUE and key not in ("d", "points"))
                tokens = -1 if bad else _svg_value(key, v)
                if tokens < 0:
                    raise ValueError(f'its {key}="{v[:40]}" on <{tag}> is not what {key} takes')
                spend(tokens)
                if key == "id":
                    if v in ids:
                        raise ValueError(f"the id {v} is defined twice")
                    ids[v] = e
                    v = prefix + v
                elif key == "href":
                    refs.append(v[1:]); v = "#" + prefix + v[1:]
                elif v.startswith("url(#"):
                    refs.append(v[5:-1]); v = "url(#" + prefix + v[5:]
                attrs += f' {"xlink:" if kns == XLINK_NS else ""}{key}="{esc(v)}"'
            if refs:
                edges.append((e, refs))
            out.append(f"<{tag}{attrs}>{esc(e.text or '')}")
            stack.append(f"</{tag}>{tail}")
            stack.extend(reversed(list(e)))
        refers = {}
        for e, refs in edges:
            for r in refs:
                spend(1)
                if r not in ids:
                    raise ValueError(f"it refers to #{r[:40]}, which the file does not have")
            refers[e] = refs
        painted, stack = 0, [(top, ())]                     # what the browser paints: every element, and at every reference
        while stack:                                        # the whole of what it refers to — counted as it goes, never after
            e, chain = stack.pop()
            painted += 1
            spend(1)
            if painted > SVG_DRAWN:
                raise ValueError(f"it paints over {SVG_DRAWN:,} elements once its references are followed")
            stack.extend((c, chain) for c in e if split(c.tag)[0] == SVG_NS)
            for r in refers.get(e, ()):
                if r in chain:
                    raise ValueError("its references form a cycle")
                if len(chain) >= SVG_REF_DEPTH:
                    raise ValueError(f"its references nest deeper than {SVG_REF_DEPTH}")
                stack.append((ids[r], chain + (r,)))
    except ValueError as e:
        return "", str(e)
    return "".join(out), ""


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
    """The board's brand, assembled: (themes [(who, css)], logo (who, data-uri) or None, labels, sources, warnings,
    wordmark (who, inline svg markup) or None)."""
    themes, logo, wordmark, labels, src, warn = [], None, None, dict(LABELS), {"theme.css": [], "logo": [], "wordmark": [], "labels.yaml": []}, []
    for who, d in brand_places():
        f = d / "theme.css"
        if board_isfile(f):
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
            if board_isfile(f):
                data, size = brand_bytes(f)
                if size > LOGO_MAX:
                    warn.append(f"{who}'s {name} is {size:,} bytes — over {LOGO_MAX:,}, not shown")
                else:
                    logo = (who, "data:%s;base64,%s" % (mime, base64.b64encode(data).decode("ascii"))); src["logo"].append(who)
                break
        f = d / "wordmark.svg"
        if board_isfile(f):
            data, size = brand_bytes(f)
            svg, why = ("", f"it is {size:,} bytes — over {LOGO_MAX:,}") if size > LOGO_MAX else inline_svg(data)
            if svg:
                wordmark = (who, svg); src["wordmark"].append(who)
            else:
                warn.append(f"{who}'s wordmark.svg is not shown: {why} — the header keeps {'the wordmark before it' if wordmark else 'the logo and the name'}")
        f = d / "labels.yaml"
        if board_isfile(f):
            given = read_flat(f.read_text(encoding="utf-8"))
            unknown = sorted(k for k in given if k not in LABELS)
            if unknown:
                warn.append(f"{who}'s labels.yaml: {', '.join(unknown[:6])} {'are' if len(unknown) > 1 else 'is'} not a label — `--brand` lists them")
            labels.update({k: v for k, v in given.items() if k in LABELS}); src["labels.yaml"].append(who)
    loose = [n for n in BRAND_FILES if (TRACKER_DIR / n).is_file() or (TRACKER_DIR / n).is_symlink()]
    if loose:
        warn.append(f"{', '.join(loose)} beside the trackers {'are' if len(loose) > 1 else 'is'} not read — a repository's brand lives in "
                    f"{(TRACKER_DIR / 'brand').relative_to(ROOT).as_posix()}/ (since 0.9.0); move {'them' if len(loose) > 1 else 'it'} there")
    return themes, logo, labels, src, warn, wordmark


def shipped_themes():
    """The themes this copy of the tool ships (FM-002): each folder of `brand/themes/` that holds a theme.css. Starters —
    no board reads them there; `--brand DIR --from <theme>` copies one into a place."""
    d = HERE / "brand" / "themes"
    return sorted(p.name for p in d.iterdir() if (p / "theme.css").is_file()) if d.is_dir() else []


def theme_files():
    """Every file of `brand/themes/`, relative to the tool — what `--vendor` pins and a theme's folder `--from` copies.
    A dot file (a desktop's .DS_Store) is no part of a theme and never travels."""
    d = HERE / "brand" / "themes"
    return tuple(sorted(p.relative_to(HERE).as_posix() for p in d.rglob("*")
                        if p.is_file() and not any(s.startswith(".") for s in p.relative_to(d).parts))) if d.is_dir() else ()


def brand_report(dest=None, theme=None):
    """`--brand`: why does my board look like this? `--brand DIR`: a commented starter to edit. `--brand DIR --from
    <theme>`: a starter from a theme the tool ships — its files copied, never over a file that is there."""
    if dest and theme is not None:
        names = shipped_themes()
        if theme not in names:
            print(f"--from {theme}: the tool ships no such theme — {' or '.join(names) if names else 'this copy ships none'}; nothing was written", file=sys.stderr)
            return 2
        named, src = pathlib.Path(dest), HERE / "brand" / "themes" / theme
        dest = pathlib.Path(os.path.realpath(named))        # a destination a person names: resolved once, where it is named
        rels = [r[len(f"brand/themes/{theme}/"):] for r in theme_files() if r.startswith(f"brand/themes/{theme}/")]
        for rel in rels:                                    # the write rule for every file it may write — as the path is named, and under the folder it resolves
            write_rule(named / rel)                         # to — before the first folder or copy is made
            write_rule(dest / rel)
        print(f"the {theme} theme — a starter from {src}")
        for rel in rels:
            if (dest / rel).exists():
                print(f"kept {named / rel} — it is there already; delete it to start from {theme}")
                continue
            (dest / rel).parent.mkdir(parents=True, exist_ok=True); shutil.copyfile(src / rel, dest / rel); print(f"wrote {named / rel}")
        print(f"yours to change; a board wears it from a brand place — <tracker dir>/brand/, or ~/.config/shoalmark/ for you alone (`--brand` lists them)")
        return EXIT_OK
    if dest:
        named = pathlib.Path(dest)
        dest = pathlib.Path(os.path.realpath(named))        # a destination a person names: resolved once, where it is named
        for name in ("theme.css", "labels.yaml"):          # the write rule for both — as the path is named, and under the folder it resolves to — before
            write_rule(named / name)                        # the folder is made
            write_rule(dest / name)
        dest.mkdir(parents=True, exist_ok=True)
        for name, text in (("theme.css", THEME_STARTER), ("labels.yaml", "# every word of the board's chrome — change a value, delete the lines you keep\n"
                                                           + "".join(f"{k}: {json.dumps(v, ensure_ascii=False)}\n" for k, v in LABELS.items()))):
            if not (dest / name).exists():
                put(dest / name, text); print(f"wrote {named / name}")
        print("a logo is logo.svg or logo.png beside them, a wordmark wordmark.svg; the name is `name` in " + CONFIG_NAME)
        return EXIT_OK
    themes, logo, labels, src, warn, _wordmark = brand()
    print("the board is built from these places, the later one winning:")
    for who, d in brand_places():
        print(f"  {who:<13} {d}" + ("" if any((d / n).is_file() for n in BRAND_FILES) else "  — no brand file here"
                                    + (": its themes/ are starters, worn only once --from copies one" if (d / "themes").is_dir() else "")))
    print(f"  name          {CONFIG['name'] or ROOT.name}  ({CONFIG_NAME})")
    for kind in ("theme.css", "logo", "wordmark", "labels.yaml"):
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
/* a wordmark — the mark and the name drawn as one — is wordmark.svg beside this file. It is inlined in the header in
   place of the logo and the name; the logo stays the browser tab's. To draw one:
   - one <svg> with a viewBox, and a height in pixels to fix its size — else it is the logo's 22 px;
   - fill="currentColor" (stroke="currentColor" where it strokes), so it takes --ink in light and dark alike;
   - the name as paths (outline the text in your editor), or as <text> in a font this file loads;
   - a pixel mark at a whole multiple of its grid stays sharp;
   - UTF-8, shapes, text, gradients, masks and a <use> of its own ids only; colours as #hex, currentColor, none or a
     plain name; numbers as -?digits(.digits)?, one space or comma between two (no .5, 1e3, 1-2: do not minify them);
     every id once; presentation attributes, never style="…" (export "with attributes, not CSS"). Anything else — a
     script, a handler, a <style>, a class, a reference outside the file — refuses it whole, with a warning. */
"""


def triage_home():
    """TRIAGE.md as the command and the dashboard read it: the Owner's current path, and the newest pass."""
    home = TRACKER_DIR / "TRIAGE.md"
    text = board_text(home) or ""
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
    or length. An example with one word changed is theirs; so is a line in italics, a line in bold, a line of two letters
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


def view_dir_refused():
    """The write rule for the views' folder, where it is a symlink or no folder: a hook's run refuses the commit, any other run refuses in one line."""
    why = "a symlink, or not a directory"
    if SAFE_WRITES:
        raise ReadOnlyRun(f"it would write into {os.path.relpath(VIEW_DIR, ROOT).replace(os.sep, '/') if in_tree(VIEW_DIR) else VIEW_DIR}, {why}")
    refuse_tree_write(VIEW_DIR, why)


def write_views(trackers):
    """One `view/<ID>.js` per tracker — `V(id, markdown)`. Rewritten only when changed; strays removed. The markdown is
    the file's body, and one line more under each record under `## Asks` that has no `**relation** —` line, every one of
    them, not the newest alone: the relation `recover_relations` read from that answer's commit, under `**answered** —`
    where a record from 0.18.1 on carries its own, naming that commit — or *relation not computable* (FM-029: every
    reading prints the relation)."""
    if os.path.lexists(VIEW_DIR) and not (real_inside(VIEW_DIR) and VIEW_DIR.is_dir()):
        if SAFE_READS:
            left_alone(VIEW_DIR, "a symlink, or not a directory")    # the board's run writes no view through a symlink or over a file
            return
        if SAFE_WRITES or in_tree(VIEW_DIR):                # the write rule: a folder of the tree
            view_dir_refused()
    VIEW_DIR.mkdir(exist_ok=True)
    keep = set()
    recover_relations(trackers)
    for t in trackers:
        _fm, body = parse_frontmatter((TRACKER_DIR / t["file"]).read_text(encoding="utf-8"))
        if t.get("asks_answers"):
            for start, end in reversed(record_spans(body)):   # from the end, so each cut leaves the earlier spans where they were
                key = record_key(body[start:end])
                line = re.search(r"^\*\*answered\*\* — .*$", body[start:end], re.M) if key else None
                if line:
                    said, source = (t.get("asks_recovered_all") or {}).get(key, (RELATION_TEXT["unknown"], ""))
                    cut = start + line.end()
                    body = body[:cut] + f"\n**relation** — {said}" + (f" · read from the answer's commit `{source}`" if source else "") + body[cut:]
        out, text = VIEW_DIR / f'{t["id"]}.js', f'V({script_json(t["id"])},{script_json(body)})\n'
        keep.add(out.name)
        board_write(out, text, changed_only=True)
    for stray in VIEW_DIR.glob("*.js"):
        if stray.name not in keep and not (SAFE_WRITES and unwritable(stray)):      # a stray the board's run may not write is left where it is
            stray.unlink()


def latest_verdicts():
    """{tracker id: [date, verdict, reason]} — the newest triage worksheet row that judged it. The verdict and
    its reason live in the pass's worksheet, never in the tracker; the page shows them where the tracker is read."""
    out = {}
    for sheet in sorted((TRACKER_DIR / "evidence" / "triage").glob("triage-*.md")):
        if not board_isfile(sheet):                          # the reading rule
            continue
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


def board_blob():
    """The forge URL prefix the board's links to a tracker's file are built on: `blob` from the configuration where it is an http(s) URL — a
    link of any other kind (`javascript:`, `data:`) is a link the board does not make, and says so once — else none."""
    if REPO_BLOB and not re.match(r"https?://[^\s\"'<>]+$", REPO_BLOB, re.I):
        print(f"  blob: `blob = {REPO_BLOB[:60]!r}` in {CONFIG_NAME} is not an http(s) URL — the board makes no link to the forge", file=sys.stderr)
        return ""
    return REPO_BLOB


def html_escape(text):
    return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def script_json(value):
    """JSON written for a `<script>`: `<`, `>` and `&` and the two line separators as `\\u` escapes, so no text a tracker holds can open a tag or
    a comment, or end the block — `</script>` is only one of the ways — and the browser reads back the same value."""
    return (json.dumps(value, ensure_ascii=False).replace("<", "\\u003c").replace(">", "\\u003e").replace("&", "\\u0026")
            .replace("\u2028", "\\u2028").replace("\u2029", "\\u2029"))


def render_html(trackers):
    """one static page: data rows + ~25 lines of vanilla JS. No dates and no
    counts are baked in (both are computed in the browser), so equal trackers give
    equal bytes. The row layout is documented once, in the page's script."""

    epics = {t.get("epic", "—") for t in trackers}
    by_id, verdicts, by_ask = {t["id"]: t for t in trackers}, latest_verdicts(), asks_by_key(trackers)
    # FM-030: their act or answer on its way — a 32nd cell, on the rows `on_their_way` names and on no other, so a board with
    # nothing on its way has the rows and the rendered board it had
    way = {k: [w["kind"], w["branch"], w["tip"], w["commit"], w["time"], w["sig"], w["said"], w["what"], w["asked"], w["value"], int(w["answered"]), int(w["owed"]), w["due"], w["note"], w["held"]]
           for k, w in on_their_way(trackers).items()}
    rows = [
        script_json(
            [t["id"], t["tier"], t["status"], "—", "—",
             t["file"], t["title"], t["hook_full"], t["num"], "—", "—",
             "—", sorted({"-".join(f.split("-")[:2]) for f in t["links"]} - {t["id"]}),
             t.get("epic", "—"), t.get("state", "") if t["id"] in epics else "",
             ["#" + x for x in t.get("tags", [])], t.get("blocked_by", []), t.get("triaged", ""), t.get("rank", 0), board(t),
             needs_of(t, by_id) if t["status"] in OPEN_STATUSES else [], t.get("next", ""),
             intent_of(t, by_id), "" if t.get("intent") or not intent_of(t, by_id) else t.get("epic", ""), verdicts.get(t["id"], []), t.get("reads", 0), list(kind_of(t)), t.get("x") or {}, t.get("xd") or {},
             [t.get("ask", ""), t.get("ask_kind", ""), t.get("ask_since", ""), held_up_by(t, trackers) if t.get("next") == "owner" and t["status"] in OPEN_STATUSES else [], t.get("answer", ""), t.get("ask_proposal", ""), t.get("ask_options") or [], ask_problems(t, by_ask, provenance=not (SAFE_READS and vcs() == "svn")),
              t.get("answered", ""), t.get("answered_by", ""), t.get("supersedes", ""), list(answer_relation(t) or [])],
             list(act_of(t) or [])] + ([way[t["id"]]] if t["id"] in way else []),
        )
        for t in sorted(trackers, key=lambda t: (t["kind"], t["num"]))
    ]
    unwrap = lambda md: re.sub(r" {2,}", " ", re.sub(r"(?<!\n)\n(?!\s*\n|\s*\d+\. |\s*- )", " ", md))   # source line breaks are not the reader's
    plain = lambda md: strip_md(re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", unwrap(md)))
    home = {k: plain(v) for k, v in triage_home().items()}
    page = (HTML_PAGE.replace("__KINDS__", "|".join(sorted(KINDS, key=len, reverse=True))).replace("__NAME__", html_escape(CONFIG["name"] or ROOT.name))
            .replace("__COLHEADS__", "".join(f'<th class="x">{html_escape(c.lower())}' for c in BOARD_COLUMNS)).replace("__COLSPAN__", str(4 + len(BOARD_COLUMNS))).replace("__BCOLS__", script_json(BOARD_COLUMNS)).replace("__COLS__", script_json(DERIVED_COLUMNS)).replace("__HOME_PATH__", script_json(html_escape(str((TRACKER_DIR / "TRIAGE.md").relative_to(ROOT).as_posix())))[1:-1]).replace("__CMD__", script_json(CMD)[1:-1])
            .replace("__ACTS_HEAD__", script_json(HEAD["acts"])[1:-1]))
    themes, logo, labels, _src, warnings, wordmark = brand()
    for w in warnings:
        print(f"  brand: {w}", file=sys.stderr)
    # each place's theme is its OWN stylesheet, in order — `@import` and `@font-face` only work at the top of one
    page = page.replace("__THEMES__", "".join(f'<style data-from="{who}">' + css.replace("</", "<\\/") + "</style>" for who, css in themes))
    # a wordmark is the mark and the name in one drawing: it takes their place, and the name stays the page's title and
    # the wordmark's accessible name. The logo stays the tab's.
    name = html_escape(CONFIG["name"] or ROOT.name)
    page = page.replace("__HEADMARK__", f'<b class="wm" role="img" aria-label="{name}">{wordmark[1]}</b>' if wordmark
                        else (f'<img alt="" src="{logo[1]}">' if logo else "") + f"<b>{name}</b>")
    page = page.replace("__FAVICON__", f'<link rel="icon" href="{logo[1]}">' if logo else "")
    # the running line: outside the board and the tracker view, so every screen shows it — the copy's own VERSION
    v = html_escape(__version__)
    page = page.replace("__RUNNING__", f'<p id="r" class="m"><a href="{TOOL_PAGE}" target="_blank" rel="noopener" aria-label="shoalmark on GitHub">'
                        '<svg viewBox="0 0 16 16" width="16" height="16" fill="currentColor" shape-rendering="crispEdges" aria-hidden="true">'
                        f'<path d="{PRICKE}"></path></svg>shoalmark</a> · <a href="{TOOL_PAGE}/releases/tag/v{v}" target="_blank" rel="noopener" '
                        f'aria-label="release v{v}">v{v}</a></p>')
    page = page.replace("__LABELS__", script_json(labels))
    return page.replace("__MARKED__", MARKED.read_text(encoding="utf-8")).replace("__DAYS__", str(TRIAGE_DAYS)).replace("__BOTTLE__", str(BOTTLENECK)).replace("__HOME__", script_json(home)).replace("__REG__", script_json(board_sessions())).replace("__BLOB__", script_json(board_blob())).replace("__BRANCH__", script_json(built_on())).replace(
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
             against (`considered:`) beside the three trackers the machine finds closest, shipped and closed ones included.
             OPEN every one marked NOT considered. The same work: `merge ID`. Otherwise judge the row like any other.
     RAISED: a row marked RAISED carries a raise — a line under the tracker's `## Raised` — dated after its last
             judgement and naming a signed rule it undermines: a line of the current path, or a tracker's signed
             answer. The Owner's rule (FM-033): a raise naming a signed rule re-judges the tracker the same day; any
             other raise waits for the next pass. Its Now cell is the raise: judge the row again, whatever its keep
             test says.
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
     ONE TRACKER, TWO ROWS: a same-day re-judgement — a raise — is a second filled row for the tracker, below the first.
     The LAST filled row in the file is applied; the earlier is left as it is, the record of the first judgement, and
     each run names it: superseded on this sheet by the later row. Never strike the earlier row to make one apply.
  3. The pass is RESUMABLE: whatever carries a `triaged:` date is done. Stop when you must; the next run continues.
  4. The pass is the seat's judgement, dated by its commit; the Owner lands it by merging; a row they disagree
     with is re-made by the seat on their word, or ruled by their signed answer — a merge rules nothing: an answer is
     written and signed, and a merge is not one.
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
    is not checked out is skipped — `git -C` on its empty directory would answer from the parent — and so is one whose path resolves outside the
    repository, symlinks resolved: no git runs there."""
    modules, found = ROOT / ".gitmodules", {}
    top = os.path.normcase(os.path.realpath(ROOT))
    for sub in re.findall(r"^\s*path\s*=\s*(\S+)", board_text(modules) or "", re.M):      # the reading rule
        if not os.path.normcase(os.path.realpath(_norm(ROOT / sub))).startswith(top.rstrip(os.sep) + os.sep):
            continue
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
    prints what the filing says it was held against beside the three closest trackers the machine finds, shipped and
    closed ones included — shipped work is prior art too. The seat judges; no score decides, and no gate turns red because
    someone else filed. `earlier` is today's worksheet if one exists: a re-run keeps every row whose Verdict is filled."""
    judged = [l for _tid, _v, l, _e in sheet_rows(earlier)]
    done = {tid for tid, _v, _l, _e in sheet_rows(earlier) if tid}
    day = lambda d: datetime.date.fromisoformat(d) if re.fullmatch(r"\d{4}-\d{2}-\d{2}", d) else datetime.date.min
    fresh = lambda d: (datetime.date.fromisoformat(today) - day(d)).days <= TRIAGE_DAYS    # one window: the keep test, and the life of a judgement
    is_new = is_new_filing
    todo = [t for t in trackers if t["id"] not in done         # a raise re-judges it however fresh its judgement (FM-033)
            and (t.get("raised") or (owed_a_pass(t) and not fresh(t.get("triaged") or "")))]
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
        test = ("keep" if fresh(last) else "FAILS") + (" · NEW FILING" if is_new(t) else "") + (" · RAISED" if t.get("raised") else "")
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
        if t.get("raised"):                                                   # …and for a raised row, the raise it is re-judged on
            now = max(t["raised"], key=lambda r: r["date"])["line"].replace("|", "\\|")
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


def apply_worksheet(sheet, sheet_is_todays, trackers, today, superseded=None):
    """Apply every filled row of a worksheet. Idempotent; an older sheet only reaches trackers no pass has dated.
    Every verdict is validated BEFORE anything is written: a rank is taken from its holder only by a verdict
    that stands, one rank names one row, and what was freed is logged. FM-036: two filled rows for one tracker — a
    same-day re-judgement, the raise rule's normal case — apply the LAST in the file; the earlier is left as it is,
    the record of the first judgement, and named in `superseded` where a list is given. Both applied in order, the
    tracker flipped between them on every run, and *Applied nothing* never came."""
    by_id, log, errors, plan, ranks = {t["id"]: t for t in trackers}, [], [], [], {}
    rows = list(sheet_rows(sheet))
    last = {row[0]: i for i, row in enumerate(rows) if row[0]}
    for i, (tid, verdict, _line, error) in enumerate(rows):
        if tid and last[tid] != i:                          # the newest filled row for this tracker is further down
            if superseded is not None:
                superseded.append(f"{tid}: `{verdict or '(unreadable)'}` — superseded on this sheet by the later row, `{rows[last[tid]][1] or '(unreadable)'}`")
            continue
        t = by_id.get(tid)
        if error:
            errors.append(f"{tid or 'worksheet'}: {error}")
            continue
        if not t or (t.get("triaged") and not sheet_is_todays):
            continue
        if t.get("status") not in OPEN_STATUSES:          # it shipped or closed since its verdict: a same-day re-run must not
            continue                                      # rank or re-date ended work, nor refuse the run over it
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
        if key not in FRONT_MATTER and DERIVER_LEFT:          # a hook ran no deriver, so the keys it declares are unknown here: `--check`, which runs it, judges them
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
        elif key in ("due", "done") and value and not parse_due(value.strip('"').split(" · ")[0]):
            out.append(f'{t["id"]}: `{key}:` names no real time — {value!r}: a date and an hour that exist, with the zone')
    is_open = t.get("status") in OPEN_STATUSES
    out += [f'{t["id"]}: {"open work" if required == "open" else "every tracker"} states `{key}:` — {says}'
            for key, (_s, required, _w, says) in FRONT_MATTER.items()
            if (required == "all" or (required == "open" and is_open)) and not t["fm"].get(key)]
    return out


def parse_due(text):
    """An act's time as an aware datetime — `due:`, and the time `done:` opens with — or None where it names no real time
    (`2026-13-01T07:30+02:00`), or no zone. `Z` is UTC; Python 3.9 reads `+00:00` only."""
    text = (text or "").strip()
    if not re.fullmatch(DUE_SHAPE, text) or "Z" in text[:-1]:     # one zone: `Z`, at the end, or an offset — never both
        return None
    try:
        when = datetime.datetime.fromisoformat(text[:-1] + "+00:00" if text.endswith("Z") else text)
    except ValueError:
        return None
    return when if when.tzinfo is not None else None


# FM-030, the E0 counter's row 20 — AN ANSWER'S HOUR SEEDS `due:`. Their promise *accepted - Sat 09-26 09:00 CEST* showed
# *no date yet* for five hours past the hour it named: the hour lived only in `answer:`. What is read, and nothing else —
# the smallest rule that is honest about a date: a date with its hour, `2026-09-26 09:00` or `2026-09-26T09:00+02:00`,
# or the weekday with its month and day, `Sat 09-26 09:00`, whose year is the answer's, or the next where that day has
# passed, and whose weekday must be that day's. A weekday alone (`Sat 09:00`) names no date, and a month and day with
# neither year nor weekday (`09-26 09:00`) is not read either: nothing checks it. The zone: an offset, `Z`, `UTC` or `GMT`,
# or the name this machine gives its own zone at that hour (`CEST` in Berlin in summer); none, this machine's zone — the
# one `--done` writes its time in, and the board's reschedule takes from the browser. Any other name is not guessed, and
# nor is any other shape (the pass's R2 on 9c96f5b): a fraction of a second, `09:00:00.000Z`, whose `.000` hid the zone;
# a 12-hour time, `9:00 PM`, read as nine in the morning; a word after the time the zone does not take, `cest` — each
# seeds nothing, and says why, rather than a wrong `due:`.
_WEEKDAY = (r"(?i:(?P<wd>mon(?:day)?|tue(?:s(?:day)?)?|wed(?:nesday)?|thu(?:r(?:s(?:day)?)?)?|fri(?:day)?|sat(?:urday)?|sun(?:day)?))\.?,?\s+")
ANSWER_TIME_RE = re.compile(r"(?<![\w:.+-])(?:" + _WEEKDAY + r")?(?:(?P<y>\d{4})-)?(?P<mo>\d{2})-(?P<d>\d{2})(?:T|\s+(?:at\s+)?)"
                            r"(?P<h>[01]?\d|2[0-3]):(?P<mi>[0-5]\d)(?::(?P<s>[0-5]\d))?"
                            r"(?:\s*(?P<z>Z|UTC|GMT|[+-](?:[01]\d|2[0-3]):?[0-5]\d|[A-Z]{3,5})(?![\w:])"
                            r"|(?P<odd>[.,]\d+|\s*[A-Za-z][A-Za-z.]*)|(?![\w:]))")


def local_time(naive):
    """A wall-clock time as this machine keeps it — aware, in its zone at that date, summer or winter. One place, so the
    suite can stand in a machine of another zone."""
    return naive.astimezone()


def answer_due(text, day):
    """The time an answer's text names, read as `ANSWER_TIME_RE` says — (the ISO time with its zone, the words it was read
    from, "") — or (None, "", why not): no date with an hour in it; a year-less day with no weekday; a weekday that is not
    the date's; a zone name this machine does not carry; or two times that differ — nothing is chosen between them.
    `day` is the day of the answer: a year-less date is the next on or after it. A time in any other shape — a fraction of
    a second, a 12-hour time, a word after it that is no zone as written — is not read, and nothing is chosen instead."""
    found = []
    for m in ANSWER_TIME_RE.finditer(text or ""):
        words = " ".join(m.group(0).split())
        odd = (m.group("odd") or "").strip()
        if odd:
            return None, "", f"`{words}`: " + ("a fraction of a second is not read" if odd[0] in ".," else
                                               "a 12-hour time is not read — the hour is 00–23" if re.fullmatch(r"[AaPp]\.?[Mm]\.?", odd) else
                                               f"`{odd}` after the time is no zone as written — an offset, `Z`, `UTC`, `GMT` or this machine's own "
                                               "name for its zone, in capitals; nothing is guessed")
        mo, d, h, mi, s = (int(m.group(k) or 0) for k in ("mo", "d", "h", "mi", "s"))
        try:
            if m.group("y"):
                date = datetime.date(int(m.group("y")), mo, d)
            elif not m.group("wd"):
                return None, "", f"`{words}` names neither the year nor the weekday — nothing checks which {mo:02d}-{d:02d} it is"
            else:
                date = datetime.date(day.year, mo, d)
                if date < day:
                    date = datetime.date(day.year + 1, mo, d)
        except ValueError:
            return None, "", f"`{words}` names no real date"
        wd = (m.group("wd") or "")[:3].lower()
        if wd and date.weekday() != ("mon", "tue", "wed", "thu", "fri", "sat", "sun").index(wd):
            return None, "", f"`{words}`: {date.isoformat()} is a {date.strftime('%A')}"
        naive, zone = datetime.datetime(date.year, date.month, date.day, h, mi, s), m.group("z")
        if not zone:
            when = local_time(naive)
        elif zone in ("Z", "UTC", "GMT"):
            when = naive.replace(tzinfo=datetime.timezone.utc)
        elif zone[0] in "+-":
            sign, digits = (1 if zone[0] == "+" else -1), zone[1:].replace(":", "")
            when = naive.replace(tzinfo=datetime.timezone(sign * datetime.timedelta(hours=int(digits[:2]), minutes=int(digits[2:]))))
        else:
            here = local_time(naive)
            if here.tzname() != zone:
                return None, "", f"`{zone}` is not this machine's zone at that hour ({here.tzname()}) — an offset is not guessed from a name"
            when = here
        found.append((when.isoformat(), words))
    if not found:
        return None, "", "it names no date with an hour — `2026-09-26 09:00`, or `Sat 09-26 09:00`; a weekday alone is not a date"
    if len({datetime.datetime.fromisoformat(w) for w, _ in found}) > 1:
        return None, "", "it names " + " and ".join(f"`{w_}`" for _, w_ in found) + " — two times, and neither is chosen"
    return found[0][0], found[0][1], ""


def promise_of(t):
    """What an accepted answer promised, in their words — the Owner's word of 2026-09-27 13:38:30 (FM-030): the text their
    `answer:` carries after its word — the option they chose, or their change — else, for a bare `accepted`, the proposal it
    took; "" where neither says it, and for an answer that did not accept. The signed line is not touched."""
    word = ANSWER_WORD_RE.fullmatch(answer_norm(t.get("answer")))
    if not word or word.group(1).lower() != "accepted":
        return ""
    return (word.group(2) or "").strip() or answer_norm(t.get("ask_proposal"))


def act_of(t):
    """FM-030 — the act a tracker owes the Owner, while it is owed: (what, their answer, its date, due, window, asked) or None.
    An accepted action ask is one — its answer is a promise of their hands, the act still theirs — and so is any `due:`, which
    the seat that schedules an act writes. `done:` closes it; closed work owes nothing. `window:` is minutes, 60 where absent.
    `what` is the act's line: for a promise, what they promised (`promise_of`), and `asked` the question it answered, the
    context below it — the Owner's word of 2026-09-27 13:38:30: the question alone read as the act, where the act is the
    option they took. A `due:` beside a question they have not answered keeps its own line, and the question stays on their
    queue (the pass's R1 on 52cfcc7): `asked` is "" there. Where no promise can be read, the question is the line."""
    if t.get("status") not in OPEN_STATUSES or t.get("done"):
        return None
    word = ANSWER_WORD_RE.fullmatch(answer_norm(t.get("answer")))
    promised = t.get("ask_kind") == "action" and bool(word) and word.group(1).lower() == "accepted"
    if not (promised or t.get("due")):
        return None
    window = int(t["window"]) if str(t.get("window") or "").isdigit() else WINDOW_DEFAULT
    promise = promise_of(t) if promised else ""
    return (promise or (t.get("ask") if promised else "") or t.get("title") or t["id"], t.get("answer", "") if promised else "",
            t.get("answered", "") if promised else "", t.get("due", ""), window, t.get("ask", "") if promise else "")


def act_state(act, now=None):
    """An act's state by the clock — the page's second rule (`actstate`), read in Python for `--standup`, `--owner` and
    `--notify`: `nodate` · `due` before its time · `overdue` after it · `missed` once `window:` minutes have passed."""
    when = parse_due(act[3])
    if not when:
        return "nodate"
    now = now or datetime.datetime.now(datetime.timezone.utc)
    return "due" if now < when else "overdue" if now < when + datetime.timedelta(minutes=act[4]) else "missed"


def act_words(act, now=None):
    """The act's state in the board's own words — its `acts.*` labels, as the built-in English has them."""
    state, when = act_state(act, now), act[3].replace("T", " ")
    return (LABELS["acts.nodate"] if state == "nodate" else LABELS["acts.missed"].format(when, act[4]) if state == "missed"
            else LABELS["acts." + state].format(when))


def shape_words(shape):
    """A shape for a reader: an enumeration as its words, else the expression itself."""
    return "one of " + " · ".join(shape.split("|")) if re.fullmatch(r"[A-Za-z| ]+", shape) else f"shape `{shape}`"


CONFIG_KEYS = {           # the configuration's keys that change what a command refuses — `--schema` prints them under the front matter
    "owner": ("one identity, or a list of them, as a `[seats]` value: `\"<email or name>\"` or `\"<email> signed\"` — a signed identity is an email; at the top of the file, before any table",
              "who the Owner is (FM-024): the one who answers, and holds all four rights — the Owner is not a seat. `signed` is read per identity, as for a seat. "
              "`[seats] owner` is still read, as its old spelling: both present and the same are read once; both present and different are refused at configuration (exit 1), "
              "and so is an `owner` key inside any other table, naming this place (in `[rights]`, a list of rights is the Owner's own) — a key after a `[table]` header belongs to that table"),
    "[paths] reviews": ("a folder under the tracker directory, or a glob of folders; `evidence/reviews/` (the default)",
                        "where the Reviewer's files sit (FM-031): `--queue` reads a verdict as covering a head that only commits touching this "
                        "folder and `sessions.md` follow — a consumer that files reviews beside each tracker's evidence names `evidence/*/`. The "
                        "verdict commit's own `review*.md` counts wherever it sits under `evidence/`"),
    "[seats] <seat>": ("one identity, or a list of them; each `\"<email or name>\"` or `\"<email> signed\"` — a signed identity is an email, verified by SSH",
                       "who sits in that seat (FM-024): every identity listed maps to the seat — `planner = [\"principal@seat\", "
                       "\"12345+shoalmark-planner[bot]@users.noreply.github.com\"]` keeps the old address resolving beside the new — and `signed` "
                       "is read per identity. A string is one identity, as ever. An identity under two seats is refused at configuration, naming both (exit 1, as every configuration refusal). "
                       "`principal` and `implementer`, the former names of `planner` and `builder`, still read and hold the same. "
                       "The tool knows the Owner, and three seats with their rights built in — `planner` ask · close · triage, `reviewer` triage, `builder` none"),
    "[ratio] records": ("a list of repository-relative prefixes; the tracker directory, `tracker_dir` — `docs/work-tracker/` by default (the default where `[ratio]` is present)",
                        "the records-to-product ratio (FM-032): what `--ratio` counts as a record — a prefix with a trailing slash is a directory, a plain "
                        "path is that one file; every other path is product. A repository without a `[ratio]` section has no ratio: `--ratio` says so, exit 2"),
    "[ratio] exclude": ("a list of repository-relative prefixes; `[]` (the default)",
                        "prefixes `--ratio` leaves out of both sides — neither a record nor product (a vendored copy, a generated tree)"),
    "freeze_at": ("a whole number; `0` = off (the default)",
                  "the filing freeze (FM-032 S4): while this many trackers or more are open, `--new` files only a product defect — a filing that "
                  "carries `freeze_tag` (`bug`), as `--new KIND \"the title\" --tags bug` writes it; anything else goes as one line into the closest "
                  "open tracker's body, or waits. `--check` says when it holds"),
    "freeze_tag": ("one tag from `[tags]`; `bug` (the default)",
                   "the tag that passes the filing freeze. Where `[tags]` does not carry it, the freeze refuses nothing, and `--check` says so in one line"),
    "judged_before_build": ("`true` or `false` (the default)",
                            "a pass judges before the first build commit (FM-033): a commit that changes a path outside the tracker directory names a tracker — "
                            "the ids in its subject, else its branch `<kind>/<NNN>-…` — that at the commit's parent carries `triaged:`, is not Parked and is "
                            "`In Progress`; else it is refused, and so is one that names none. The commit-msg hook (`--commit-msg`) judges the commit being made, with its subject, before it is made; "
                            "`--check` judges each commit of the branch since `origin`'s default branch, a merge by the commits it carries; on the default "
                            "branch nothing is judged. `--check` says whether it is on"),
}


WORKTREE_KEYS = {         # a seat's worktree carries its identity in git's own per-worktree settings, `git config --worktree` — `--schema` prints them last
    "user.email": ("the seat's address in `[seats]`", "who may: the gate reads a commit's rights from its author; the badge of the worktree"),
    "seat.session": ("eight hex characters, or `<parent>/<seat>-<n>` for a sub-agent",
                     "which run: the prepare-commit-msg hook appends it as the `Session:` trailer of every commit made here; `--session new` prints an id"),
    "seat.harness": ("the id the harness gave this seat: Claude Code's session id, or a sub-agent's agent id; Codex's thread id",
                     "which log: whoever spawns the seat writes it, from the spawn's result. `--whoami` opens the one log file whose name carries the id — "
                     "`~/.claude/projects/<slug>/<id>.jsonl`, `…/<session>/subagents/agent-<id>.jsonl`, or `~/.codex/sessions/…/rollout-*-<id>.jsonl` — "
                     "and reads its newest model and effort, top-level fields only; the hook appends them as `Model:` and `Effort:`. Two files for one id refuse; none is `—`"),
}


def render_schema():
    rows = [f"| `{k}:`{' — required' + (' on open work' if required == 'open' else '') if required else ''} | {shape_words(shape) if shape else 'free text'} | {who} | {says} |"
            for k, (shape, required, who, says) in FRONT_MATTER.items()]
    return "\n".join(["| Key | Value | Written by | Says |", "|---|---|---|---|"] + rows
                     + ["", f"`{CONFIG_NAME}`, at its top level:", "", "| Key | Value | Says |", "|---|---|---|"]
                     + [f"| `{k}` | {shape} | {says} |" for k, (shape, says) in CONFIG_KEYS.items()]
                     + ["", "A seat's worktree, `git config --worktree <key> <value>`:", "", "| Key | Value | Says |", "|---|---|---|"]
                     + [f"| `{k}` | {shape} | {says} |" for k, (shape, says) in WORKTREE_KEYS.items()]
                     + ["", "No key chooses the board's look: a brand is files in its places, the later one winning (`--brand` says which gave "
                            "what). `--brand DIR --from THEME` writes a starter from a theme the tool ships in `brand/themes/`: "
                            + (" · ".join(f"`{n}`" for n in shipped_themes()) or "none in this copy") + "."])


def git_user():
    """The committer's own name, as git will write it — so `answered-by:` need not be typed. Read ONCE per run and
    kept (`configure` forgets it): the answer is the only place it is needed, and a run does not change who is typing."""
    global _GIT_USER
    if _GIT_USER is None:
        out = subprocess.run(["git", "config", "user.name"], cwd=ROOT, capture_output=True, text=True, encoding="utf-8", errors="replace", env=nested_git_env())
        _GIT_USER = out.stdout.strip() if out.returncode == 0 else ""
    return _GIT_USER


BLAME_ANSWERS = ("E195002", "E200009")      # the history's own answer *not committed*, which is what a blame of a tracker nobody has committed says: E195002 the path has no committed
                                            # revision (scheduled for addition), E200009 the target is not in version control (a file not yet `svn add`ed). A failure to READ is none of them


def svn_new(rel):
    """Whether Subversion holds no committed revision of this path, read from its own record of it — `svn info`'s schedule:
    `add` or `replace`, a copy included, or a path not in version control at all (the Owner's ruling of 2026-10-04, v0.19.1).
    Read once per path and kept; where the record cannot be read, SvnUnreadable — kept too, as `svn_blame` keeps it."""
    if rel in _SVN_NEW:
        if isinstance(_SVN_NEW[rel], Exception):
            raise _SVN_NEW[rel]
        return _SVN_NEW[rel]
    try:
        info = svn_run("info", rel, xml=True, answers=("E200009",))      # E200009: not in version control
    except SvnUnreadable as e:
        _SVN_NEW[rel] = e
        raise
    _SVN_NEW[rel] = info is None or (info.findtext("entry/wc-info/schedule") or "").strip() in ("add", "replace")
    return _SVN_NEW[rel]


MERGED_IN = object()         # the author of a line older than a merge that put its path here: no one's, refused (`svn_blame`, `line_author`)


def svn_merged(rev):
    """Whether revision `rev` merged anything — `svn log -g` lists the revisions it merged under it — read at the repository's root,
    which this run reads once, and kept by revision: each revision's log is asked once per run. Where Subversion cannot
    answer, SvnUnreadable (v0.19.1)."""
    if ("root",) not in _SVN_BLAME:
        _SVN_BLAME[("root",)] = (svn_run("info", "--show-item", "repos-root-url", ".") or "").strip()
    if not _SVN_BLAME[("root",)]:
        raise SvnUnreadable("svn info did not name the repository's root")
    if ("merged", rev) not in _SVN_BLAME:
        log = svn_run("log", "-q", "-g", "-r", str(rev), f'{_SVN_BLAME[("root",)]}@{rev}', xml=True)
        top = log.find("logentry") if log is not None else None
        if top is None:
            raise SvnUnreadable(f"svn log did not answer for revision {rev}")
        _SVN_BLAME[("merged", rev)] = top.find("logentry") is not None
    return _SVN_BLAME[("merged", rev)]


def svn_tracker_new(t):
    """`svn_new` of a tracker's file — where Subversion's record cannot be read, True: the rights refuse it, in their one line (`blame_refusal`)."""
    try:
        return svn_new((TRACKER_DIR / t["file"]).resolve().relative_to(ROOT).as_posix())
    except SvnUnreadable:
        return True


def svn_blame(rel):
    """{line number: (author, revision)} for one file, from the server's own record — read once per file and kept:
    the gate asks about several lines of the same tracker, and `svn blame` is a round trip to the repository. {} for a
    file that is not committed. Where the blame CANNOT be read (no server, no network, svn not there) SvnUnreadable, with
    svn's own error — kept as well, so the one failure is raised again, not asked again: a rights check that cannot read
    who wrote a line refuses, and never passes unread (the second fail-open of the cold audit's round, the Owner's ruling).
    A blame follows a copy to its source: a line older than the path's own first revision — the oldest of `svn log
    --stop-on-copy` — was put at this path by that revision. Where that revision merged nothing, the line is its author's: a
    copy is its copier's — and its own author's, as the blame reads it through the copy, is kept beside it, so a guarded line
    passes only where both hold its right (`line_author`). Where it merged anything (`svn_merged`), the line is no one's here —
    `MERGED_IN`, refused, neither credited to that revision's author nor followed to an earlier one (v0.19.1). A line a merge
    brought into a path that was already here is its own author's (`-g`)."""
    if rel in _SVN_BLAME:
        if isinstance(_SVN_BLAME[rel], Exception):
            raise _SVN_BLAME[rel]
        return _SVN_BLAME[rel]
    out = {}
    try:
        blame = svn_run("blame", "-g", rel, xml=True, answers=BLAME_ANSWERS)     # `-g`: a line a merge brought is its author's, never the merger's (v0.19.1)
    except SvnUnreadable as e:
        _SVN_BLAME[rel] = e
        raise
    try:
        for e in (blame.iter("entry") if blame is not None else []):
            c = e.find("merged/commit") if e.find("merged/commit") is not None else e.find("commit")
            who = c.find("author") if c is not None else None
            out[int(e.get("line-number"))] = (who.text if who is not None else None, c.get("revision") if c is not None else "")
    except (ValueError, TypeError):                     # a blame that cannot be read is no answer of the history's: refused, never read as nothing committed
        _SVN_BLAME[rel] = SvnUnreadable("svn blame printed lines that could not be read")
        raise _SVN_BLAME[rel]
    if out:
        try:
            log = svn_run("log", "-q", "--stop-on-copy", rel, xml=True)
        except SvnUnreadable as e:
            _SVN_BLAME[rel] = e
            raise
        first = log.findall("logentry")[-1] if log is not None and log.findall("logentry") else None
        if first is not None and (first.get("revision") or "").isdigit():
            at, by = int(first.get("revision")), first.findtext("author")
            if any(rev.isdigit() and int(rev) < at for _w, rev in out.values()):
                try:
                    by = MERGED_IN if svn_merged(at) else by      # a merge that put the path here: its older lines are no one's here
                except SvnUnreadable as e:
                    _SVN_BLAME[rel] = e
                    raise
                if by is not MERGED_IN:                         # a copy: each older line's own author, read through it by the same blame (v0.19.1)
                    _SVN_BLAME[("through", rel)] = {n: (who, rev) for n, (who, rev) in out.items() if rev.isdigit() and int(rev) < at}
                out = {n: ((by, str(at)) if rev.isdigit() and int(rev) < at else (who, rev)) for n, (who, rev) in out.items()}
            _SVN_BLAME[("first", rel)] = str(at)        # the revision that filed the path: a line it wrote was written at the filing
    _SVN_BLAME[rel] = out
    return out


def blame_refusal(t, why):
    """The one refusal for a tracker whose blame could not be read — once per tracker per run, whichever gate asked first: Subversion's history
    could not be read, so who changed it is not known and its rights are not judged, and are not passed unread."""
    if t["id"] in _BLAME_REFUSED:
        return []
    _BLAME_REFUSED.add(t["id"])
    return [f'{t["id"]}: Subversion\'s history could not be read, so who changed this tracker is not known and its rights are not judged — and not passed unread. '
            f'svn said: {why}. Reach the repository, then run again']


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


FM_BREAKS = re.compile("[\n\x0b\x0c\x1c\x1d\x1e\x85\u2028\u2029]")       # where `str.splitlines` breaks a line, once newlines are translated


def frontmatter_keys(raw, cr_breaks=False):
    """[(key, line, the key as written)] — every front-matter line `parse_frontmatter` reads a key from, in order: the text as `extract`
    reads it (its newlines translated), split as `str.splitlines` splits it, each key stripped and lower-cased — the LAST entry for a key
    is the one the parser keeps. `line` is the 1-based line it stands on as version control counts lines in `raw`, the file as written:
    git breaks a line at `\\n` alone, Subversion at a lone `\\r` as well (`cr_breaks`)."""
    text, line_of, n, i = [], [], 1, 0
    while i < len(raw):
        c = raw[i]
        if c == "\r":
            text.append("\n"); line_of.append(n)
            if raw[i + 1:i + 2] == "\n":
                i += 1; n += 1
            elif cr_breaks:
                n += 1
        else:
            text.append(c); line_of.append(n)
            n += c == "\n"
        i += 1
    text = "".join(text)
    if not text.startswith("---\n"):
        return []
    end = text.find("\n---", 4)
    if end == -1:
        return []
    out, at = [], 4
    for m in [*FM_BREAKS.finditer(text, 4, end), None]:
        part = text[at:m.start() if m else end]
        if ":" in part:
            k = part.partition(":")[0]
            out.append((k.strip().lower(), line_of[at], k.strip()))
        at = m.end() if m else end
    return out


def guarded_key_problems(tid, text):
    """LAYER 2 (the Owner's ruling of 2026-10-04, v0.19.1): a front matter that repeats a key a right is judged on (`GUARDED_KEYS`), or
    spells one other than in lower case, is refused — one line for each such key, naming its lines and the way through. Every other key
    may repeat and carry capitals, as prose in a front matter does."""
    seen = {}
    for key, line, written in frontmatter_keys(text):
        if key in GUARDED_KEYS:
            seen.setdefault(key, []).append((line, written))
    out = []
    for key, at in seen.items():
        odd = list(dict.fromkeys(w for _l, w in at if w != key))
        if len(at) > 1 or odd:
            out.append(f'{tid}: the front matter carries `{key}:` on line{"s" if len(at) > 1 else ""} {" and ".join(str(l) for l, _w in at)}'
                       + (f', spelled {", ".join(f"`{w}:`" for w in odd)}' if odd else "")
                       + f' — a key a right is judged on is read from one line: write one `{key}:` line, in lower case')
    return out


def guarded_line(raw, key, cr_breaks=False):
    """The line `parse_frontmatter` keeps for `key` — the last one, its key's case folded — as version control numbers it (`frontmatter_keys`), or None."""
    return next((line for k, line, _w in reversed(frontmatter_keys(raw, cr_breaks)) if k == key), None)


def exact_line_regex(line):
    """The pattern git's `-G` is handed for one exact line: anchored at both ends, the characters an extended regular expression reserves
    escaped as `line_regex` escapes them, and an optional carriage return before the end — the line as committed with CRLF."""
    return "^" + "".join("\\" + c if c in ERE_META else c for c in line) + "\r?$"


def line_author(path, needle):
    """Who committed the line this tracker carries under `needle` — from the version control system, never from the
    file: (name, email, system, commit) — or (None, None, "uncommitted", "") where version control's own record says the line
    is not committed yet (the working copy or the index carries it, no commit does), (None, None, "unattributed", "")
    where it names no commit for a line a commit carries, and on Subversion (None, None, "merged", <revision>) for a line older
    than a merge that put the tracker's path here (`svn_blame`). Git's author is a string anyone can type,
    so `signed` makes `verified_as` ask the commit; Subversion's author is the one its server authenticated, and it
    has no email. ONE reader for both the answer line and the `next: owner` line — a second would drift from this one.

    The needle names a LINE, not a substring. A tracker's body discusses its own keys — "an `answer:` counts only from
    the account it is filed from" is a sentence FM-007 carries — and a substring test cannot tell that prose from the
    front-matter line, so it answered with the commit that wrote the prose, and read a line nobody had committed as
    committed. The line read is the one the parser keeps (`guarded_line`): the needle's key, its case folded, the LAST such
    line of the front matter — git's `-G` searches for that line exactly as written, and Subversion's blame is read at its
    number (the Owner's ruling of 2026-10-04, v0.19.1)."""
    rel = pathlib.Path(path).resolve().relative_to(ROOT).as_posix()
    key = needle.partition(":")[0].strip().lower()      # the line is found as the parser keeps it: its key's case folded, the last one (v0.19.1)
    hit = _LINE_AUTHOR.get((rel, key))
    if hit is not None:
        return hit
    out = (None, None, "uncommitted", "")
    raw = pathlib.Path(path).read_bytes().decode("utf-8", errors="replace")
    if vcs() == "svn":
        by_line = svn_blame(rel)                          # ONE blame per file, however many of its lines are asked about
        n = guarded_line(raw, key, cr_breaks=True)
        if n is not None and n in by_line:
            who, rev = by_line[n]
            through = _SVN_BLAME.get(("through", rel), {})
            own = through.get(n)
            right = {"answer": "answer", "next": "ask", "status": "close"}.get(key, "triage")
            may = (lambda w: holds(seat_of(w, None), right)) if SEATS else (lambda w: right == "answer" and w in may_answer())
            if key == "considered":
                if own and own[1] != through.get(1, (None, None))[1]:
                    who, rev = own                      # a `considered:` changed after its source's filing is its own author's triage, not the copy's filing
            elif own and own[0] != who and may(who) and not may(own[0]):
                who, rev = own                          # a copied line passes only where its copier and its own author both hold its right (v0.19.1)
            out = (None, None, "merged", rev) if who is MERGED_IN else (who, None, "svn", rev) if rev else out   # no revision yet: changed in the working copy
        elif by_line:
            out = (None, None, "unattributed", "")
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
        # the line searched for is the one the parser keeps (`guarded_line`), exactly as written; it is committed where a tip carries it,
        # and `-G` names the last commit that wrote or removed that exact line — `--full-history`, as above
        tips = ["HEAD", *merge_heads()]
        n = guarded_line(raw, key)
        line = raw.split("\n")[n - 1].rstrip("\r") if n is not None else None
        if ("tips", rel) not in _LINE_AUTHOR:           # each tip's copy of the file, read once for all its keys
            _LINE_AUTHOR[("tips", rel)] = [l.rstrip("\r") for rev in tips for l in subprocess.run(["git", "show", f"{rev}:{rel}"], cwd=ROOT, capture_output=True,
                                                                                                     env=nested_git_env()).stdout.decode("utf-8", errors="replace").split("\n")]
        if line is None:
            out = (None, None, "unattributed", "")
        elif line in _LINE_AUTHOR[("tips", rel)]:
            try:
                log = subprocess.run(["git", "log", "-1", "--full-history", "--format=%H%n%an%n%ae", "-G", exact_line_regex(line), *tips, "--", rel], cwd=ROOT, capture_output=True,
                                     text=True, encoding="utf-8", errors="replace", env=nested_git_env())
            except ValueError:                          # a NUL in the line: no argument can carry it
                log = None
            if log is not None and log.returncode == 0 and log.stdout.strip():
                commit, name, email = (log.stdout.strip().split("\n") + ["", ""])[:3]
                out = (name, email, "git", commit)
            else:
                out = (None, None, "unattributed", "")
    _LINE_AUTHOR[(rel, key)] = out
    return out


def unattributed(t, needle, how, named=True):
    """LAYER 3 (the Owner's ruling of 2026-10-04, v0.19.1): a guarded line no commit can be named for is refused, in one line — never judged
    as whoever runs the gate. Not committed yet, it is judged only in the run that makes its commit (git's pre-commit hook), as that
    commit's author; Subversion knows who makes a commit only once it is made. `named`: the line opens with the tracker's id — not
    where the caller's own lines are prefixed with it (`seat_problems`, read through `ask_problems`)."""
    who = f'{t["id"]}: ' if named else ""
    if how == "merged":
        return (f'{who}`{needle}` is older than the merge that put this tracker here, so who set it is not known; it is refused, never credited '
                f'to the merge\'s author. Write the line again, in a commit of its own after the merge')
    if how == "uncommitted":
        return (f'{who}`{needle}` is not committed yet — who set a line is read from the commit that made it, and only the hook that makes '
                f'that commit judges it before: commit it' + (" (on Subversion who makes a commit is known only once it is made)" if vcs() == "svn" else "")
                + ", then run again")
    return (f'{who}`{needle}` — version control names no commit for this line, so who set it is not known; it is refused, never judged '
            f'as whoever runs the gate. Write it again, in a commit of its own')


def pending_author():
    """The author git WOULD write for the commit being made right now — `user.email`, unless the environment imposes
    another (`GIT_AUTHOR_EMAIL`). In the pre-commit run the line is not committed yet, and this is who is committing it."""
    out = subprocess.run(["git", "var", "GIT_AUTHOR_IDENT"], cwd=ROOT, capture_output=True, text=True, encoding="utf-8", errors="replace", env=nested_git_env())
    name, _, rest = out.stdout.partition(" <")
    return (name.strip(), rest.partition(">")[0].strip()) if out.returncode == 0 else ("", "")


# A SIGNED IDENTITY (FM-024; the Owner's ruling filed in FM-006, *The release bar*, on a private security report): a `signed` identity is an email address —
# one `@`, something on both sides, no whitespace — and it verifies by SSH only. Configuration refuses any other `signed` identity; a commit signed any other
# way than SSH is refused on a signed line with `SIGN_WITH_SSH`.
EMAIL_RE = re.compile(r"[^@\s]+@[^@\s]+")
SIGN_WITH_SSH = "sign with SSH; GPG returns with a fingerprint binding"


def signature_kind(commit):
    """The kind of `commit`'s signature, read from the commit object's own header — never from configuration: "ssh", "pgp", "x509" or "other",
    and "" where it carries none."""
    head = (git_out("cat-file", "commit", commit) or "").split("\n\n", 1)[0]
    m = re.search(r"^gpgsig(?:-sha256)? (.*)$", head, re.M)
    if not m:
        return ""
    first = m.group(1)
    return ("ssh" if "BEGIN SSH SIGNATURE" in first else "pgp" if "BEGIN PGP SIGNATURE" in first
            else "x509" if "BEGIN SIGNED MESSAGE" in first or "BEGIN CMS" in first else "other")


def verified_as(commit, identity):
    """The gate's ONE signature test, shared by every rule that asks for a signed line — the identity a signature must name is the configured one
    (`signed_identity`), never the commit's author standing in for it. All three must hold: the signature, read from the commit object's own header,
    is SSH; `%G?` is G under the DEFAULT branch's signers file (`trusted_signers`, FM-037's AU-19: an answer branch that appends its own key under the
    Owner's email vouches for nothing); and the principal that file trusts the key for (`%GS`) IS the identity's email — equal, never containing it."""
    if not identity or not EMAIL_RE.fullmatch(identity) or signature_kind(commit) != "ssh" or signature_gap(commit):
        return False
    v = subprocess.run(["git", *signers_args(), "log", "-1", "--format=%G?%n%GS", commit], cwd=ROOT, capture_output=True, text=True, encoding="utf-8", errors="replace", env=nested_git_env())
    good, signer = (v.stdout.split("\n") + ["", ""])[:2]
    return good.strip() == "G" and signer.strip() == identity


_SIGNERS = None


def trusted_signers():
    """{"file": the signers file SSH signatures are verified against, or None; "why": why there is none; "rel": its path in
    the repository, or None; "trunk": the default branch} — FM-037's AU-19, the Auditor seat's: never a file the branch
    being judged can have written. `gpg.ssh.allowedSignersFile` names the file. Where it sits in a checkout of this
    repository — the signing page keeps it in the tracker directory — what verifies is the DEFAULT branch's copy, written
    to a temporary file for this run: a branch that appends its own key under the Owner's email and signs with it vouches
    for nothing. Where the default branch does not carry it, NOTHING verifies against it until its first version lands
    there (FM-037's cold re-review, R2): the checkout's copy is whatever branch is checked out, and a checkout on a branch
    that writes one vouched for another pull request's commits. A file outside every checkout is used as it is: no branch
    writes it; so is the clone's file where there is no default branch to read. A path that is a symlink, or is reached
    through one, inside a checkout — a link a branch can write — is refused before anything decides which checkout holds
    it, as a deriver is (`run_deriver`): nothing verifies against it (`symlink_in_checkout`). Which working tree holds it
    is decided by the file system's identity, never by spelling (`signers_home`), its path spelled as git spells it
    (`signers_rel`); one in another clone's working tree is refused: a branch writes it. Read once per run."""
    global _SIGNERS
    if _SIGNERS is not None:
        return _SIGNERS
    conf = (git_out("config", "--path", "--get", "gpg.ssh.allowedSignersFile") or "").strip()
    if not conf:
        _SIGNERS = {"file": None, "why": "`gpg.ssh.allowedSignersFile` is not set", "rel": None, "trunk": None}
        return _SIGNERS
    written = pathlib.Path(conf) if os.path.isabs(conf) else ROOT / conf
    trees = {top: fs_chain(top)[:1] for top in (os.path.normcase(t) for t in worktree_tops())}
    link = symlink_in_checkout(written, trees)
    if link:
        _SIGNERS = {"file": None, "why": f"`gpg.ssh.allowedSignersFile` names {conf}, and `{link}` on the way to it is a symlink in a checkout: the signers file "
                                         "is, or is reached through, a symlink, and nothing verifies against it — name the file itself", "rel": None, "trunk": None}
        return _SIGNERS
    path = written.resolve()
    top, below, other = signers_home(str(path), trees)       # the working tree that holds it, by the file system's identity — or another clone's
    if other:
        _SIGNERS = {"file": None, "why": f"`gpg.ssh.allowedSignersFile` names {conf}, inside another checkout ({other}): the signers file is inside another checkout, "
                                         "where a branch writes it — name this repository's own file, or one outside every checkout", "rel": None, "trunk": None}
        return _SIGNERS
    git = lambda *a: subprocess.run(["git", *a], cwd=ROOT, capture_output=True, text=True, encoding="utf-8", errors="replace", env=nested_git_env())
    trunk = default_trunk(git) if top is not None else None
    rel = signers_rel(top, below, str(path), trunk) if top is not None else None
    blob = cat_blobs([f"{trunk}:{rel}"]).get(f"{trunk}:{rel}") if trunk else None
    if blob is not None:
        fd, tmp = tempfile.mkstemp(prefix="shoalmark-signers-")
        with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as f:
            f.write(blob)
        atexit.register(lambda: os.path.exists(tmp) and os.remove(tmp))
        _SIGNERS = {"file": tmp, "why": "", "rel": rel, "trunk": trunk}
    elif trunk:
        _SIGNERS = {"file": None, "why": f"`{rel}` is not on {ref_name(trunk)}: commit its first version there, signed — a branch cannot prove a key the default branch does not hold",
                    "rel": rel, "trunk": trunk}
    elif not path.is_file():
        _SIGNERS = {"file": None, "why": f"`gpg.ssh.allowedSignersFile` names {conf}, which does not exist", "rel": rel, "trunk": trunk}
    else:
        _SIGNERS = {"file": str(path), "why": "", "rel": rel, "trunk": trunk}
    return _SIGNERS


def symlink_in_checkout(path, trees):
    """The first symlink on the way to `path` — itself, or a folder above it — whose folder lies in one of the working trees
    `trees` (`tree_holding`), or in another git working tree (`signers_home`): a link a branch can write. The path is
    walked as written, a name at a time, each link read before a `..` after it applies — as the system reads the path. ""
    where there is none: a link outside every working tree — the system's own, say — is no branch's to write."""
    parts = pathlib.PurePath(os.fspath(path)).parts
    at = parts[0] if parts else ""
    for name in parts[1:]:
        if name in ("", "."):
            continue
        if name == "..":
            at = os.path.dirname(at)
            continue
        step = os.path.join(at, name)
        if os.path.islink(step):
            if tree_holding(os.path.realpath(at), trees) is not None or signers_home(os.path.realpath(at), trees)[2]:
                return step
            at = os.path.realpath(step)
        else:
            at = step
    return ""


def signers_home(real, trees):
    """(the working tree of `trees` that holds the resolved path `real`, the names below it as they are written there, "") —
    or (None, None, the folder of another git working tree that holds it, where a `.git` file or folder is found first) —
    or (None, None, ""): outside every working tree. One walk up its ancestors, nearest first, each matched by the file
    system's own identity (`fs_chain`), never by spelling — a working tree whose folder is gone holds nothing."""
    held = {folder[0][0]: top for top, folder in trees.items() if folder and not folder[0][1]}
    parts = pathlib.PurePath(real).parts
    for ident, below in fs_chain(real):
        at = os.path.join(*parts[:len(parts) - len(below)])
        if ident in held:
            return held[ident], list(parts[len(parts) - len(below):]), ""
        if os.path.lexists(os.path.join(at, ".git")):
            return None, None, at
    return None, None, ""


def signers_rel(top, below, real, trunk):
    """The signers file's path in the repository, as git spells it on the default branch — never as it was typed: the path of
    the default branch's tree (`tree_paths`) that names the names `below` the working tree `top`, as a file system that
    ignores case and Unicode normalization reads them (`fs_fold`), and is that very file there (`fs_identity`) where it is
    there. Where the default branch holds no such path, the names as written: no copy there, and nothing verifies."""
    typed = "/".join(below)
    here = fs_identity(real)
    same = [p for p in (tree_paths(trunk) or [] if trunk else []) if p == typed or (fs_fold(p) == fs_fold(typed)
            and (here is None or fs_identity(os.path.join(top, *p.split("/"))) == here))]
    return typed if typed in same or len(same) != 1 else same[0]


def signers_args():
    """`-c gpg.ssh.allowedSignersFile=<the trusted file>` for a git call that reads `%G?` — nothing where there is none."""
    s = trusted_signers()
    return ["-c", f"gpg.ssh.allowedSignersFile={s['file']}"] if s["file"] else []


def signers_gap(commit):
    """Why an SSH signature cannot be verified here, or "": no signers file to verify against — none set, none there, or
    one in a checkout that the default branch does not carry yet: a signers file a branch writes vouches for nothing (AU-19,
    and the cold re-review's R2). The same for every commit; the argument keeps the callers' shape."""
    return trusted_signers()["why"]


def signature_gap(commit):
    """Why an SSH-signed commit cannot be verified in this clone — the clone's configuration, not the commit — or "": the commit
    carries no SSH signature, or the check could run. A refusal that said *sign it* to a signed commit blamed the Owner's
    key for a missing file in the reader's setup: SSH needs `gpg.ssh.allowedSignersFile`. Any other kind is no gap: a signed line refuses it
    (`SIGN_WITH_SSH`)."""
    return signers_gap(commit) if signature_kind(commit) == "ssh" else ""      # FM-037's AU-19: the default branch's signers file, never the branch's


def unverified(commit, tail):
    """The end of a refusal for a commit that does not verify: *cannot verify* and why, where the clone cannot check a
    signed commit; where it is SSH-signed and the check ran, that its key is not the one the signers file the gate reads
    holds for it, with the way through — a key lands in that file first (FM-037's cold re-review, R1: mid key rotation the
    answer gate told the Owner to sign a commit they had signed) — `%G?` U, a key the file does not hold, or G, one it holds for
    someone else; else the seat's own words (`tail`), which ask for a signature — a bad signature (`%G?` B) among them."""
    if signature_kind(commit) not in ("", "ssh"):          # GPG, X.509 or another kind: a signed line verifies by SSH only
        return SIGN_WITH_SSH
    gap = signature_gap(commit)
    if gap:
        return f"it is signed, but {CHECKOUT_MARKS[0]}: {gap} — see {SIGNING_PAGE}"
    s = trusted_signers()
    ssh = signature_kind(commit) == "ssh"
    if ssh and s["file"] and (git_out(*signers_args(), "log", "-1", "--format=%G?", commit) or "").strip() in ("G", "U"):
        held = f"`{s['rel']}` on {ref_name(s['trunk'])}" if s["rel"] and s["trunk"] else f"`{s['file']}`"
        return (f"it is signed, but not with a key {held} holds for that identity — a new key verifies once it is there"
                + (f": the Owner's signed commit to that file, merged into {ref_name(s['trunk'])} first" if s["rel"] and s["trunk"] else "")
                + f" — see {SIGNING_PAGE}")
    return tail


# FM-034 — WHAT IS THE CHECKOUT'S, NOT THE LEDGER'S: a signed commit this clone cannot verify (its signers file, its
# keyring), a pinned file this checkout has not got. Each is said on stderr, grouped, and never written into the generated
# INDEX: written there, the INDEX a fresh clone generated differed from the committed one by that line, and `--check` said
# STALE where no tracker had changed. The drift test is not widened; the finding still fails the run. Recognised by these
# words, which the places that write such a finding use and nothing else does — a default branch this clone cannot tell
# is one too (`default_trunk`, v0.19.1).
CHECKOUT_MARKS = ("this clone cannot verify", "this checkout cannot read it", "the default branch cannot be told — this clone has no `origin/HEAD`")


PENDING_MARKS = ("` is not committed yet — who set a line is read from the commit that made it", ": is not committed yet, and it carries ",
                 ": the answer is not committed yet — commit it under your own name")     # the lines that judge the commit being made, not the ledger


def pending_finding(problem):
    """A line that says a line is not committed yet: it judges the commit being made, not the ledger — so INDEX.md leaves it out, and the
    INDEX.md written before such a commit is the one the next run writes (v0.19.1). It is printed, and refuses, as every line does."""
    return any(m in problem for m in PENDING_MARKS)


def checkout_finding(problem):
    return any(m in problem for m in CHECKOUT_MARKS)


def checkout_lines(problems):
    """The checkout's findings as a reader takes them: ONE line per cause — the signers file this clone has not got, not
    one per answer it could not check — naming what it could not check, each commit once: two rules can ask of one
    answer's commit, and the count said 8 where 5 commits were meant (the cold second pass's R4)."""
    groups = {}
    for p_ in (p_ for p_ in problems if checkout_finding(p_)):
        what, sep, why = p_.partition(" — it is signed, but ")
        if sep:
            m = re.search(r"`([0-9a-f]{7,40})`", what)
            groups.setdefault("it is signed, but " + why, {}).setdefault(m.group(1) if m else what, what.split(":")[0] + (f" `{m.group(1)}`" if m else ""))
        else:
            groups.setdefault(p_, {})
    return [f"  checkout: {why}" + (f" — {len(items)} signed commit(s) it could not check: {', '.join(items.values())}" if items else "") for why, items in groups.items()]


def index_env():
    """The environment for a git call that reads the index of the commit being made: `commit -a` and `commit <path>` hand the hook an
    index of their own (`GIT_INDEX_FILE`), which `nested_git_env` strips — so the hook would judge `.git/index` and the working tree."""
    return dict(nested_git_env(), **({"GIT_INDEX_FILE": os.environ["GIT_INDEX_FILE"]} if os.environ.get("GIT_INDEX_FILE") else {}))


def staged_now():
    """What the commit being made is about to carry — read once. The gate's version-control calls cost real seconds in
    a pre-commit hook, and a file this commit does not touch was checked by the run that committed it."""
    global _STAGED
    if _STAGED is None:
        out = subprocess.run(["git", "diff", "--cached", "-z", "--name-only", "--relative"], cwd=ROOT, capture_output=True, text=True, encoding="utf-8", errors="replace", env=index_env())
        _STAGED = set(out.stdout.split("\x00")) if out.returncode == 0 else set()         # NUL-separated: git quotes a name with a non-ASCII byte, a `"` or a control character (RV-2151)
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


def refuse_signed_name(where, who, mode):
    """A `signed` identity that is not an email is refused when the configuration is read — exit 1, one line on how to migrate: a signature
    verifies against the email the signers file names for the key, and nothing else. An identity without `signed` stays as it is."""
    if mode == "signed" and not EMAIL_RE.fullmatch(who or ""):
        raise SystemExit(f'{CONFIG_NAME}: {where} names `{who}` as signed, and a signed identity is an email address — write the email the signers file names for the key: '
                         + ('`owner = "<email> signed"`, before any table (`answerers` is its old spelling, read by the git author\'s name)' if where == "`answerers`" else '`"<email> signed"`'))


def seat_identities(value):
    """A `[seats]` value as its identities, `[(identity, "signed" | ""), …]` (FM-024): a string is one, as ever —
    `"principal@seat"`, `"you@example.org signed"` — a list is several, each item optionally `… signed`, so the address a
    seat commits under can change while history and the branches in flight keep resolving to it."""
    out = []
    for item in (value if isinstance(value, list) else [value]):
        who, _, mode = str(item).strip().rpartition(" ")
        out.append((who if mode == "signed" else str(item).strip(), "signed" if mode == "signed" else ""))
    return out


def seats_of(cfg):
    """`[seats]` as the tool reads it, `{seat: value}`, with the Owner folded in (FM-024, D2: the Owner is not a seat). A
    top-level `owner`, before any table, names them; `[seats] owner` is still read, as its old spelling. Both present and
    the same: read once. Both present and different: refused at configuration, exit 1, one line naming both and the way
    through. An `owner` key inside any other table is refused, naming where it belongs — a key after a `[table]` header
    belongs to that table, so a line meant for the top and written at the end of the file lands in the last table, and
    is read by nobody. `[rights]` keeps its own `owner`, a seat's rights as a list; there only a string is misplaced.
    The Owner is still the seat `owner` inside the tool, with its four rights; only the configuration moved."""
    seats = cfg.get("seats") or {}
    if not isinstance(seats, dict):
        raise SystemExit(f"{CONFIG_NAME}: `seats` is a table — `[seats]`, one line per seat")
    where = [t for t, body in cfg.items() if isinstance(body, dict) and "owner" in body and t not in ("owner", "seats")
             and not (t == "rights" and not isinstance(body["owner"], str))]
    if where:
        raise SystemExit(f'{CONFIG_NAME}: `owner` is inside {" and ".join(f"`[{t}]`" for t in where)}, where it does not name the Owner — '
                         f'put it at the top of the file, before any table: `owner = "<email> signed"`'
                         + ("; if it is a tag, give it another name: `owner` names the Owner" if "tags" in where else ""))
    top = cfg.get("owner")
    if top is None:
        return seats
    if not isinstance(top, (str, list)):
        raise SystemExit(f'{CONFIG_NAME}: `owner` is a key at the top of the file, before any table — `owner = "<email> signed"`, or a list of them. '
                         f'Got {"a table, `[owner]`" if isinstance(top, dict) else repr(top)}')
    old = seats.get("owner")
    if old is not None and seat_identities(old) != seat_identities(top):
        shown = lambda v: json.dumps(v, ensure_ascii=False)
        raise SystemExit(f"{CONFIG_NAME}: the Owner is named twice, and differently — `owner = {shown(top)}` at the top of the file, `owner = {shown(old)}` under `[seats]`. "
                         "Name them once, at the top: delete the `[seats]` line, or make the two the same")
    return {"owner": top, **{k: v for k, v in seats.items() if k != "owner"}}


def seat_of(name, email):
    """Which seat this author is sitting in — matched on any identity `[seats]` gives it, email or name."""
    return next((s for s, ids in SEATS.items() if any(who and who in (email, name) for who, _m in ids)), None)


def seat_mode(seat, name, email):
    """`"signed"` or `""` for the identity this author wears in that seat — `signed` is read per identity (FM-024). An author
    that matches none of its identities (a name where the seat lists an email) reads the seat's first."""
    ids = SEATS[seat]
    return next((m for who, m in ids if who and who in (email, name)), ids[0][1] if ids else "")


def signed_identity(seat, name, email):
    """The identity a signature must name for this author in that seat: the configured `signed` identity it wears — matched as `seat_mode` matches,
    on its email or its name — which configuration holds to an email; None where the identity it wears asks for no signature. Never the commit's
    author standing in for it."""
    ids = SEATS.get(seat) or []
    hit = next(((who, m) for who, m in ids if who and who in (email, name)), ids[0] if ids else None)
    return hit[0] if hit and hit[1] == "signed" else None


def answerer_identity(name, email):
    """The configured identity this author answers as — with `[seats]`, the one their seat lists that they match (or the seat's first, as `seat_mode`
    reads it); without, the `answerers` entry their name, else their email, is — or None. What `--queue` verifies an answer against."""
    if SEATS:
        ids = SEATS.get(seat_of(name, email)) or []
        hit = next((who for who, _m in ids if who and who in (email, name)), ids[0][0] if ids else None)
        return hit
    return name if name in may_answer() else None          # `answerers` always meant the git author's name


def at_top(seat):
    """Is this seat the Owner, named by the top-level `owner` (FM-024, D2) rather than by a line of `[seats]`? A message that points at the line
    asking a signature says `owner` then — a line of its own, in no table — and `[seats]` otherwise."""
    return seat == "owner" and CONFIG.get("owner") is not None


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
        return {who: mode for seat, ids in SEATS.items() if holds(seat, "answer") for who, mode in ids if who}
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
    answering = [s for s in SEATS if holds(s, "answer") and any(who for who, _m in SEATS[s])]
    for name, mode in ANSWERERS.items():
        if mode != "signed":
            continue
        same = [s for s in answering if any(who == name for who, _m in SEATS[s])]
        for s in (same or answering):
            for who, imode in SEATS[s]:                  # FM-024: each identity of the seat — `signed` is read per identity
                if not who or imode == "signed" or (same and who != name):
                    continue
                line = "owner" if at_top(s) else f"[seats] {s}"      # the Owner named at the top is a line of its own (FM-024, D2)
                shown = f'`{line} = "{who}"`' if len(SEATS[s]) == 1 else f'`{line}` lists `"{who}"`'       # a list seat: the item, not the whole seat
                advice = f'Add `signed` to {"`owner`" if at_top(s) else "the seat"} (`{s} = "{who} signed"`)' if len(SEATS[s]) == 1 else f'Add `signed` to that item (`"{who} signed"`)'
                out.append(f'{CONFIG_NAME}: `answerers = ["{name} signed"]` asks for a signed answer, and {shown} — '
                           + (("the Owner, who answers for it" if at_top(s) else "the seat that answers for it") if same
                              else ("the Owner, who holds `answer`" if at_top(s) else "a seat holding `answer`") + f"; no seat is spelled `{name}`, so each stands in for it")
                           + f' — is not signed. {"`owner` and `[seats]` alone decide" if CONFIG.get("owner") is not None else "`[seats]` alone decides"} who may answer (from 0.17.1), so that answer would count unsigned. '
                           f'{advice}, or remove `answerers`')
    return out


def no_seat(name, email, right, what):
    """The one refusal, worded once: who the version control system says made the change, the right it needed, and
    what the repository's seats are. It names the seat and the right — an agent told only *refused* tries again."""
    who = email or name or "nobody the version control system can name"
    seat = seat_of(name, email)
    known = ", ".join(f"{s} ({' · '.join(who for who, _m in SEATS[s])})" for s in sorted(SEATS) if s != "owner") or "none"
    owner = " · ".join(w for w, _m in SEATS.get("owner", ()) if w)             # the Owner is not a seat (FM-024, D2): named apart from the list
    if seat is None:
        return (f'{what} — `{who}` is not a seat. The seats are: {known}' + (f". The Owner, who is not a seat, is {owner}" if owner else "")
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
    the line, so the Owner's QUEUE can drop an ask that reached them another way. A made merge's own `next: owner` is
    judged on its change as well, under that merge's author (`rights_problems`). Anywhere else, a line no commit can be
    named for is refused (`unattributed`). It catches an agent that does not know the rule, not one that lies: that is
    FM-007's class, and no gate closes it."""
    if not SEATS or not in_this_commit(t):
        return []
    try:
        name, email, how, commit = line_author(TRACKER_DIR / t["file"], "next: owner")
    except SvnUnreadable as e:
        return blame_refusal(t, e)
    if how not in ("git", "svn"):
        if how == "uncommitted" and vcs() == "git" and COMMITTING:
            name, email, commit = (*pending_author(), "")    # the pre-commit run: the author git is about to write is who is asking
        elif how == "uncommitted" and vcs() == "svn" and svn_tracker_new(t):
            return []                                    # a tracker Subversion holds no revision of: the rights refuse it, in one line
        else:
            return [unattributed(t, "next: owner", how, named=False)]        # `lint` names the tracker on `ask_problems`' lines
    seat = seat_of(name, email)
    if seat is None or not holds(seat, "ask"):
        return [no_seat(name, email, "ask", "`next: owner` puts a question in front of the Owner")]
    if seat_mode(seat, name, email) == "signed" and how != "svn":
        if not commit:
            print(f'  {t["id"]}: the `next: owner` line is being committed now — the seat\'s signature is verified on the commit, by the next run', file=sys.stderr)
        elif not verified_as(commit, signed_identity(seat, name, email)):
            return [f'the commit `{commit[:10]}` that set `next: owner` does not verify as the seat `{seat}` — '
                    + unverified(commit, f'{"`owner`" if at_top(seat) else "`[seats]`"} asks this seat to sign, and a git author is only a string: sign it (`git commit -S`), or the ask does not reach them')]
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


_CHANGES = None


def changes_under_review():
    """`read_changes`, read ONCE per run: the rights, the sessions and the Shipped rule judge the same changes, and each reading is
    several version-control calls — 0.07 s in the pre-commit run and 0.13 s on a clean tree, in the repository this tool was cut from.
    The answer depends on `COMMITTING`, so a run that asks both ways reads twice. No reader changes what it is given."""
    global _CHANGES
    if _CHANGES is None or _CHANGES[0] != COMMITTING:
        _CHANGES = (COMMITTING, read_changes())
    return _CHANGES[1]


def read_changes():
    """WHAT THIS RUN IS JUDGING, once — a list of changes, each (the revisions it is read against, the tracker files it
    touches, author name, author email, the commit or "" when it is not made yet, the revision that holds its result or
    None for the working tree, a label that names it). The commit being made — staged, or simply not committed yet —
    read against HEAD; on a clean tree, the commit at HEAD read against its parent.

    A MERGE (FM-019) is two kinds of change, and neither is the merger's alone:
    1. EACH COMMIT IT BRINGS — every commit reachable from it and not from its first parent — under its own author and its
       own signature: an ordinary commit against its own parent; a merge among them, nested at any depth, by ITS OWN
       CHANGE (2), against each of its parents (the Owner's ruling of 2026-10-03, v0.19.1). A commit made without the hook
       (`--no-verify`, a clone with no hook installed, the forge's editor) was never judged; a merge must not launder it.
    2. ITS OWN CHANGE — the tracker files where the result differs from EVERY parent (a conflict resolved, an edit made in
       the merge), judged under the merger. A clean merge adds nothing of its own.
    Read against its first parent alone, a merge was everything its branch carried and all of it the merger's: `--check`
    on a trunk went red on the first pull request carrying an answer or a close, the forge's merge identity being no
    seat. The same two parts hold for a merge being committed now — HEAD and `MERGE_HEAD` are its parents. The commits a
    merge brings are read only when there is a merge: one `git log` for all of them, the merges among them included.

    On a clean tree, every commit of the branch since `origin`'s default branch is read the same way (1) — one more `git log`
    — so a change made under a later commit is judged where `--check` runs, as the merge's walk judges it on the trunk
    (the Owner's ruling of 2026-10-04, v0.19.1). Where no default branch is found (`default_trunk`), the newest commit
    alone is judged, as before, and `--check` says so in one line — never the whole history."""
    global _WALK
    git = lambda *a: subprocess.run(["git", *a], cwd=ROOT, capture_output=True, text=True, encoding="utf-8", errors="replace", env=nested_git_env())
    names = lambda r: set(r.stdout.split("\x00")) - {""} if r.returncode == 0 else set()          # every name list is read with `-z`: git quotes a name it finds odd (RV-2151)

    def brought(tips, first, why="which the merge brings"):
        """(1): every commit reachable from `tips` and not from `first`, oldest first, each with its files — an ordinary commit's
        against its parent; a merge's, its own change (2): `-c` lists only the files where its result differs from every parent,
        from its diff against each of them, and the merge is read against all its parents, as the merge at HEAD is."""
        if not tips:
            return []
        out = []
        log = git("log", "-z", "-c", "--reverse", "--topo-order", "--relative", "--name-only", f"--format=%x01%H%x02%an%x02%ae%x02%P%x02{TRAILERS}",
                  *tips, "--not", first)                # parents and trailers too: the rules read them from here, one call however long the walk (v0.19.1)
        if log.returncode != 0:                         # a walk git cannot make judges nothing — refused, never passed unread (v0.19.1)
            global _WALK_FAILED
            said = next((l.strip() for l in log.stderr.splitlines() if l.strip()), f"git log exited {log.returncode}")
            _WALK_FAILED = _WALK_FAILED or (f"the branch's commits could not be read — git could not walk them since `{ref_name(first)}` ({said}) — so they are "
                                            f"not judged, and not passed unread. Fetch `origin`, or set its default branch again (`git remote set-head origin --auto`), then run again")
        for record in log.stdout.split("\x01")[1:]:         # one per commit: hash · name · email · parents · trailers, then the NUL-separated files --name-only lists under it
            head, _, files = record.partition("\x00")
            c, an, ae, ps, tr = (head.split("\x02") + ["", "", "", ""])[:5]
            _WALK_COMMITS[c] = (ps.split(), tr.strip("\n"))
            bases = ps.split() if len(ps.split()) > 1 else [f"{c}^1"]
            out.append((bases, set(files.lstrip("\n").split("\x00")) - {""}, an, ae.strip(), c, c, f"in `{c[:10]}` ({ae.strip() or an}), {why}"))
        return out

    heads = merge_heads()
    if COMMITTING or worktree_edited(git):
        files = set(staged_now()) if COMMITTING else names(git("diff", "-z", "--name-only", "--relative", "HEAD"))
        if not COMMITTING:
            _WALK = "uncommitted"                       # `--check` says it judged the edits against HEAD, not the branch's commits
        for h in heads:
            files &= names(git("diff", "-z", *(["--cached"] if COMMITTING else []), "--name-only", "--relative", h))
        return brought(heads, "HEAD") + [(["HEAD", *heads], files, *pending_author(), "", None, "")]
    parents = git("rev-list", "--parents", "-n", "1", "HEAD").stdout.split()[1:]
    if not parents:
        return []                                        # a root commit has no parent to compare with
    files = None
    for parent in parents:
        got = names(git("diff", "-z", "--name-only", "--relative", parent, "HEAD"))
        files = got if files is None else files & got
    name, email, commit = (git("log", "-1", "--format=%an%n%ae%n%H").stdout.split("\n") + ["", "", ""])[:3]
    merged = brought(parents[1:], parents[0]) if len(parents) > 1 else []
    trunk = default_trunk(git)                          # every commit of the branch since the default branch, read as a merge's are (v0.19.1)
    _WALK = trunk or ("untold" if _TRUNK_UNTOLD else "")      # none: the newest commit alone is judged, and `--check` says so — never the whole history
    seen = {c[4] for c in merged} | {commit}
    own = [c for c in brought(["HEAD"], trunk, f"on this branch since {ref_name(trunk)}") if c[4] not in seen] if trunk else []
    return own + merged + [(parents, files, name, email, commit, "HEAD", "")]


def staged_absent(rels):
    """{path: tracker} — in the pre-commit run, each tracker the index carries and the working tree lacks (deleted or moved there,
    unstaged), read from the index as the commit being made holds it; nothing in any other run (v0.19.1)."""
    if not COMMITTING:
        return {}
    home = TRACKER_DIR.resolve().relative_to(ROOT).as_posix()
    names = [rel for rel in sorted(staged_now()) if rel not in rels and pathlib.PurePath(rel).parent.as_posix() == home
             and rel.endswith(".md") and KIND_RE.match(pathlib.PurePath(rel).name)]
    texts = cat_blobs([f":./{rel}" for rel in names], index_env())
    return {rel: extract(ROOT / rel, texts[f":./{rel}"]) for rel in names if texts.get(f":./{rel}") is not None}


def worktree_edited(git):
    """Whether the working tree holds an edit against HEAD (`git diff --name-only HEAD`) — the one reading `read_changes` and `main`
    share: a diff git cannot make reads as no edit in both, so a run that walks the branch's commits asks origin as it walks
    (v0.19.1)."""
    return bool(git("diff", "--name-only", "--relative", "HEAD").stdout.strip())


def walk_problems():
    """The one line where git could not walk the commits this run judges — a default branch `origin/HEAD` names and this clone does
    not hold, or any `git log` of the walk that failed (`read_changes`) — or where the default branch cannot be told (`default_trunk`):
    they are refused, never judged as nothing (v0.19.1)."""
    if _WALK_FAILED:
        return [_WALK_FAILED]
    if vcs() == "git":
        default_trunk(lambda *a: subprocess.run(["git", *a], cwd=ROOT, capture_output=True, text=True, encoding="utf-8", errors="replace", env=nested_git_env()))
    return [_TRUNK_UNTOLD] if _TRUNK_UNTOLD else []


def line_break_problems(trackers):
    """A tracker whose file name holds a line break, refused in one line: asked for that file's text, git reads its name as two, so
    no change to it can be judged. The trackers this run loads, and — under git — each tracker file a change it judges touches."""
    rels = {(TRACKER_DIR / t["file"]).relative_to(ROOT).as_posix() for t in trackers if "\n" in t.get("file", "") or "\r" in t.get("file", "")}
    if vcs() == "git":
        home = TRACKER_DIR.resolve().relative_to(ROOT).as_posix()
        rels |= {rel for c in changes_under_review() for rel in c[1] if ("\n" in rel or "\r" in rel) and rel.endswith(".md")
                 and pathlib.PurePosixPath(rel).parent.as_posix() == home and KIND_RE.match(pathlib.PurePosixPath(rel).name)}
    return [f"{json.dumps(rel)}: a tracker's file name holds a line break — git reads it as two names, so no change to the tracker can be "
            "judged; give the file a name without one" for rel in sorted(rels)]


def rights_problems(trackers):
    """`answer`, `close` and `triage`: the author of the change must be a seat that holds the right for every transition
    the change makes. (`ask` is judged on the line, by `seat_problems` — except the clearing move, which has no line
    left to judge and is read here, from the change, under `ask`: FM-014; and a made merge's own `next: owner`, which no
    parent carries, read from that merge's own change under its author — the Owner's ruling of 2026-10-03, v0.19.1.)
    Under Subversion there is no pending commit to read and no client hook to read it in, and the author of each line is
    the one the server authenticated, so the transitions are read from the lines. A tracker Subversion holds no
    committed revision of — added, replaced or copied, or not yet `svn add`ed (`svn_new`) — has no author to read until
    the commit is made, so it may carry no line a right guards: where it does, it is refused before the commit, in one
    line naming the rights (the Owner's ruling of 2026-10-03, v0.19.1)."""
    if not SEATS or vcs() not in ("git", "svn"):
        return []
    out = []
    if vcs() == "svn":
        for t in trackers:
            fm_ = t.get("fm", {})
            guarded = [r for r, on in (("answer", any((fm_.get(k) or "").strip() for k in ("answer", "answered", "answered-by"))), ("ask", t.get("next") == "owner"),
                                       ("close", t["status"] not in OPEN_STATUSES), ("triage", any((fm_.get(k) or "").strip() for k in TRIAGE_KEYS))) if on]
            if guarded:
                try:
                    fresh = svn_new((TRACKER_DIR / t["file"]).resolve().relative_to(ROOT).as_posix())      # no committed revision: no line has an author
                except SvnUnreadable as e:
                    out += blame_refusal(t, e)
                    continue
                if fresh:
                    named = " and ".join([", ".join(f"`{r}`" for r in guarded[:-1]), f"`{guarded[-1]}`"] if len(guarded) > 1 else [f"`{guarded[0]}`"])
                    out.append(f'{t["id"]}: is not committed yet, and it carries {"a line" if len(guarded) == 1 else "lines"} that {named} guard{"s" if len(guarded) == 1 else ""} — '
                               'on Subversion who makes a commit is known only once it is made, so a tracker not yet committed may carry no protected state. '
                               'File it open, with no such line, and make that change in a commit of its own')
                    continue
            fm_ = t.get("fm", {})
            judged = ([("answer", "answer:"), ("close", "status:")] + [("triage", k + ":") for k in TRIAGE_KEYS if (fm_.get(k) or "").strip()]   # each triage key
                      + ([("triage", "considered:")] if (fm_.get("considered") or "").strip() else []))                                    # that carries a value (v0.19.1)
            for right, needle in judged:
                if right == "close" and t["status"] in OPEN_STATUSES:
                    continue
                if right == "answer" and not t.get("answer"):
                    continue
                try:
                    name, _e, how, rev = line_author(TRACKER_DIR / t["file"], needle)
                except SvnUnreadable as e:
                    out += blame_refusal(t, e)
                    break                                # the tracker's blame is unreadable: one line, not one for each right
                if needle == "considered:" and ((how in ("svn", "merged") and rev == _SVN_BLAME.get(("first", (TRACKER_DIR / t["file"]).resolve().relative_to(ROOT).as_posix())))
                                                or (how == "uncommitted" and svn_tracker_new(t))):
                    continue                             # written when the tracker is filed — here, a merge's filing too: the filing rule, not a verdict
                if how in ("uncommitted", "unattributed", "merged"):
                    if right != "answer":                # the answer gate says it of the answer line
                        out.append(unattributed(t, needle, how))
                elif how == "svn" and not holds(seat_of(name, None), right):
                    out.append(f'{t["id"]}: ' + no_seat(name, None, right, f'`{needle}` is a `{right}` change'))
        return out
    rels = {(TRACKER_DIR / t["file"]).resolve().relative_to(ROOT).as_posix(): t for t in trackers}
    rels.update(staged_absent(rels))                    # the commit being made: a tracker it carries that the working tree lacks is judged too
    changes = changes_under_review()
    blobs = cat_blobs(list(dict.fromkeys(f"{rev}:{rel}" for bases, files, *_who, result, _l in changes for rel in sorted(files & set(rels))
                                         for rev in ([result] if result else []) + list(bases))))     # one call for every change (v0.19.1)
    show = lambda rev, rel: (lambda t_: None if t_ is None else t_.replace("\r\n", "\n").replace("\r", "\n"))(blobs.get(f"{rev}:{rel}"))
    for bases, files, name, email, commit, result, label in changes:
        seat, where = seat_of(name, email), (label + " — " if label else "")
        on_line = set() if commit and len(bases) > 1 else {"ask"}        # a made merge's own `next: owner` is judged on its change, under its author
        touched = sorted(files & set(rels))
        staged = cat_blobs([f":./{rel}" for rel in touched], index_env()) if result is None and COMMITTING else {}     # the commit being made is what its index holds
        for rel in touched:
            t = rels[rel]
            now = ((show(result, rel) or "") if result is not None else (staged.get(f":./{rel}") or "") if COMMITTING
                   else (TRACKER_DIR / t["file"]).read_text(encoding="utf-8"))
            moves = None                                # a merge's own move is one it makes against EVERY parent (FM-019)
            for base in bases:
                was = show(base, rel)
                made = transitions(was if was is not None else "", now, new_file=was is None)
                moves = made if moves is None else moves & made
            for move in sorted(moves - on_line):
                right = "ask" if move == "clear" else move
                if not holds(seat, right):
                    out.append(f'{t["id"]}: {where}' + no_seat(name, email, right, "this change clears an answered ask — the seat that acts on an answer holds `ask`"
                                                                if move == "clear" else f'this change is a `{right}`'))
                elif seat_mode(seat, name, email) == "signed":
                    if not commit:
                        print(f'  {t["id"]}: a `{right}` change is being committed now — the seat\'s signature is verified on the commit, by the next run', file=sys.stderr)
                    elif not verified_as(commit, signed_identity(seat, name, email)):
                        out.append(f'{t["id"]}: the commit `{commit[:10]}` making a `{right}` change does not verify as the seat `{seat}` — '
                                   + unverified(commit, f'{"`owner`" if at_top(seat) else "`[seats]`"} asks this seat to sign: sign it (`git commit -S`), or the change does not count'))
    return out


# --- the Shipped rule (FM-005, the Owner's ruling of 2026-09-30) ---------------------------------------------------------
# The claim is *a gate that refuses a done without a commit behind it*. A change that moves a tracker to `Shipped` — its status
# classifies as Shipped after and did not before, a new tracker included — is refused unless the tracker's ship log, as that
# change leaves it, names a commit that is (a) in the change's history (an ancestor of the commit being judged: a commit being made
# cannot name itself) and (b) changes at least one path outside the records. It judges exactly the changes the gate already
# judges (`changes_under_review`), so a `Shipped` tracker no change moves is never read. It holds for every author, the Owner
# included, and without `[seats]`: it reads no seat and no right. A move to `Closed` is not judged.
GIT_NAME_RE = re.compile(r"(?<![0-9A-Za-z])[0-9a-f]{7,64}(?![0-9A-Za-z])")     # a commit as a ship-log row names it: seven hex characters or more, up to a SHA-256 hash's 64
SVN_NAME_RE = re.compile(r"(?<![0-9A-Za-z])r[0-9]+(?![0-9A-Za-z])")             # …and on Subversion a revision, `r123`


def is_shipped(text):
    """Does this tracker's `status:` classify as Shipped, as the gate reads it elsewhere — False for no text, a file that was not there."""
    status = (parse_frontmatter(text)[0].get("status") or "") if text is not None else ""
    return bool(status) and classify_status(status) == "Shipped"


def ship_log_rows(text):
    """The rows of a tracker's ship log as one string — "" where it has no log, or a heading with no table under it."""
    lines = parse_frontmatter(text)[1].split("\n")
    log = ship_log_table(lines)
    return "\n".join(lines[log[1] + 1:log[2] + 1]) if log and log[1] is not None else ""


def commits_named(rows):
    """The commits a ship log's rows name, once each in the order written: git hashes, or on Subversion `r<N>` revisions."""
    return list(dict.fromkeys((SVN_NAME_RE if vcs() == "svn" else GIT_NAME_RE).findall(rows)))


def ship_records():
    """The prefixes that are the records for this rule — `[ratio] records` where that section is set, as `--ratio` reads it, else the
    tracker directory, written from the top of the repository (git). A ValueError with the line to print where `[ratio]` is malformed."""
    section = CONFIG.get("ratio")
    if isinstance(section, dict):
        return ratio_paths(section)[0]
    prefix = (git_out("rev-parse", "--show-prefix") or "").strip() if vcs() == "git" else ""
    return [prefix + p for p in ratio_defaults()["records"]]


def git_ship_verdicts(names, bases, records):
    """{name: "" when that commit is a commit behind the change, else why it is not} — in the change's history (reachable from its
    parents, `bases`) and changing a path outside `records`: a merge read against its first parent, a root commit by all its paths.
    At most three git calls for all the names — which of them are commits, which of those the parents reach, what those change."""
    git = lambda *a, **k: subprocess.run(["git", *a], cwd=ROOT, capture_output=True, text=True, encoding="utf-8", errors="replace", env=nested_git_env(), **k)
    found = git("cat-file", "--batch-check=%(objectname) %(objecttype)", input="".join(f"{n}\n{n}^{{commit}}\n" for n in names))     # each name twice: as written, where git says *ambiguous*, and peeled to its commit
    lines = found.stdout.split("\n") + [""] * (2 * len(names))
    shas = {n: lines[2 * i + 1].partition(" ")[0] for i, n in enumerate(names) if lines[2 * i + 1].partition(" ")[2] == "commit"}
    ambiguous = {n for i, n in enumerate(names) if n not in shas and lines[2 * i].endswith(" ambiguous")}
    behind, changed = {}, {}
    if shas:
        beyond = git("rev-list", *dict.fromkeys(shas.values()), "--not", *bases)          # what the candidates reach that the parents do not
        unreached = set(beyond.stdout.split()) if beyond.returncode == 0 else set(shas.values())      # no parent (a first commit): nothing is behind it
        behind = {n: s for n, s in shas.items() if s not in unreached}
    if behind:
        log = git("log", "-z", "--no-walk=unsorted", "-m", "--first-parent", "--no-renames", "--name-only", "--format=%x01%H", *dict.fromkeys(behind.values()))
        for record in log.stdout.split("\x01")[1:]:         # NUL-separated names: a `"` or a tab in a name is no quoted name here (RV-2151)
            sha, _, files = record.partition("\x00")
            changed[sha.strip()] = [f for f in files.lstrip("\n").split("\x00") if f]
    out = {}
    for n in names:
        if n in ambiguous:
            out[n] = "names more than one commit — write more of its hash"
        elif n not in behind:
            out[n] = "is not in the history" + ("" if n in shas else " (no such commit)")
        elif any(ratio_class(f, records, []) == "product" for f in changed.get(behind[n], [])):
            out[n] = ""
        else:
            out[n] = f"changes nothing outside the records ({', '.join(records)})"
    return out


class SvnUnreadable(Exception):
    """Subversion's history could not be read — svn is not there, or the call failed (no server, no network, a repository moved away) —
    as against an answer, which may be empty. `tracker` names the one it was reading for, where it knows (F1 of the cold audit)."""
    tracker = None
    newest = False                              # the read that failed was the newest revision's — which only the server holds (RV-2267)


SVN_ANSWERS = ("E160006", "E195012")        # *no such revision*, and *the path is not in that revision*: an answer of the history, not a failure to read it


def svn_run(*args, xml=False, answers=()):
    """One `svn` call in the working copy — its output parsed where `xml`, else as text — or None where the answer is empty, or is an
    error code in `answers`. Where svn is not there or fails, SvnUnreadable with svn's own error: a done check that cannot read the
    history it needs REFUSES, and never reads the failure as nothing changed (the cold audit's F1, the Owner's ruling)."""
    import xml.etree.ElementTree as ET
    try:
        done = subprocess.run(["svn", *args, *(["--xml"] if xml else [])], cwd=ROOT, capture_output=True, text=True, encoding="utf-8", errors="replace")
    except OSError as e:
        raise SvnUnreadable(f"svn could not be run: {e}")
    if done.returncode != 0:
        codes = re.findall(r"\bE\d{6}\b", done.stderr)
        if codes and all(c in answers for c in codes):
            return None
        raise SvnUnreadable(" · ".join(l.strip() for l in done.stderr.strip().splitlines()[:2] if l.strip())[:300] or f"svn exited {done.returncode}")
    if not done.stdout.strip():
        return None
    if not xml:
        return done.stdout
    try:
        return ET.fromstring(done.stdout)
    except ET.ParseError:
        raise SvnUnreadable("svn printed XML that could not be read")


def svn_entry(*args, answers=()):
    """The one `<logentry>` that `svn log <args> .` prints for the working copy, or None."""
    log = svn_run("log", *args, ".", xml=True, answers=answers)
    return log.find("logentry") if log is not None else None


def svn_shipped_moves(rels):
    """Subversion's reading of "what this run is judging", the one git's is: the change NOT YET COMMITTED — the trackers the working
    copy has modified, added or not yet `svn add`ed — else the NEWEST revision, at HEAD, that changed anything under the working
    copy, read against the one before it. The rights read the `status:` line's last author by `svn blame`, which judges a STATE: read so, every
    Shipped tracker there ever was would be a move, and each one shipped before this rule would be refused for ever. Only the change in
    front of the run is a move here. The calls: `svn status`; where nothing is pending, `svn log -l 1` and one `svn cat` for each tracker the
    newest revision changed; and one more `svn cat` for each that is Shipped after."""
    def read(rel, *args, answers=()):
        try:
            return svn_run(*args, answers=answers)
        except SvnUnreadable as e:
            e.tracker = rels[rel]["id"]; raise                             # a failed read for this tracker names it

    status, pending = svn_run("status", TRACKER_DIR.relative_to(ROOT).as_posix(), xml=True), {}
    for e in (status.iter("entry") if status is not None else []):
        wc, rel = e.find("wc-status"), pathlib.PurePath(e.get("path") or "").as_posix()
        if rel in rels and wc is not None and wc.get("item") in ("modified", "added", "replaced", "unversioned"):
            pending[rel] = wc.get("item") != "modified"                     # is it new to the repository
    at, touched = None, {}
    if pending:
        touched = {rel: (ROOT / rel).read_text(encoding="utf-8") for rel in pending}
        was = lambda rel: None if pending[rel] else read(rel, "cat", "-r", "BASE", rel)
    else:
        try:
            newest = svn_entry("-l", "1", "-v", "-r", "HEAD:1")              # HEAD, not the working copy's BASE: a commit made and not yet updated to is the newest too
        except SvnUnreadable as e:
            e.newest = True; raise
        at = int(newest.get("revision")) if newest is not None else None
        paths = [p.text or "" for p in newest.iter("path") if p.get("action") in ("M", "A", "R")] if newest is not None else []
        touched = {rel: read(rel, "cat", "-r", str(at), rel) for rel in rels if any(p.endswith("/" + rel) for p in paths)}
        was = lambda rel: read(rel, "cat", "-r", str(at - 1), rel, answers=SVN_ANSWERS)
    for rel, now in touched.items():
        if is_shipped(now) and not is_shipped(was(rel)):
            yield rels[rel], "", ship_log_rows(now), lambda names, records, at=at: svn_ship_verdicts(names, at, records)


def svn_ship_verdicts(names, at, records):
    """{name: "" when that revision is a revision behind the change, else why it is not} — one before `at`, the revision being judged
    (any, for a change not yet committed), that changed something under this working copy, with a path outside `records`, which are
    read from the working copy's root. One `svn info`, and one `svn log` for each revision named."""
    base = ("/" + urllib.parse.unquote((svn_run("info", "--show-item", "relative-url", ".") or "^/").strip()[2:]).strip("/")).rstrip("/")   # the working copy's own path in the repository — "" at its root
    out = {}
    for n in names:
        entry = None if at is not None and int(n[1:]) >= at else svn_entry("-r", n[1:], "-v", answers=SVN_ANSWERS)
        inside = [p.text[len(base) + 1:] if p.text.startswith(base + "/") else p.text for p in entry.iter("path") if p.text] if entry is not None else []
        out[n] = ("is not in the history" if entry is None
                  else "" if any(ratio_class(p, records, []) == "product" for p in inside) else f"changes nothing outside the records ({', '.join(records)})")
    return out


def shipped_moves(rels):
    """Every move to Shipped the run is judging: (the tracker, where the change is said to be, the rows of its ship log as the change
    leaves them, and what tells the commits those rows name apart). Git: each change `changes_under_review` lists — the ship log read
    from the working tree for the commit being made, from the commit otherwise — and a move is one the tracker makes against EVERY
    parent. Only a tracker that is Shipped after is read on the other side."""
    if vcs() == "svn":
        yield from svn_shipped_moves(rels)
        return
    spec = lambda rev, rel: f"{rev}:./{rel}"                                # `./`: from the working directory, which is ROOT — as `--relative` made the paths
    changes = [(c, sorted(c[1] & set(rels))) for c in changes_under_review()]
    changes = [(c, touched) for c, touched in changes if touched]
    made = cat_blobs([spec(c[5], rel) for c, touched in changes if c[5] is not None for rel in touched])     # every change's trackers, one call (v0.19.1)
    moved = []
    for (bases, files, _name, _email, _commit, result, label), touched in changes:
        if result is None and COMMITTING:
            texts = cat_blobs([f":./{rel}" for rel in touched], index_env())         # the commit being made is what its index holds, not the working tree
            now = {rel: texts.get(f":./{rel}") for rel in touched}
        elif result is None:
            now = {rel: (TRACKER_DIR / rels[rel]["file"]).read_text(encoding="utf-8") for rel in touched}
        else:
            now = {rel: made.get(spec(result, rel)) for rel in touched}
        moved.append((bases, label, now, [rel for rel in touched if is_shipped(now.get(rel))]))
    earlier = cat_blobs([spec(base, rel) for bases, _l, _n, shipped in moved for rel in shipped for base in bases])      # …and what each move was against, one call
    for bases, label, now, shipped in moved:
        before = {spec(base, rel): earlier.get(spec(base, rel)) for rel in shipped for base in bases}
        for base, rel in [(b, r) for r in shipped for b in bases if before.get(spec(b, r)) is None]:     # absent at a base: new, or the same tracker renamed — its id says which
            d = pathlib.PurePath(rel).parent.as_posix()
            was = next((n for n in (git_out("ls-tree", "-z", "--name-only", f"{base}:./{d}") or "").split("\x00") if n.startswith(rels[rel]["id"] + "-") and n.endswith(".md")), None)
            before[spec(base, rel)] = cat_blobs([f"{base}:./{d}/{was}"]).get(f"{base}:./{d}/{was}") if was else None
        for rel in shipped:
            if not any(is_shipped(before.get(spec(base, rel))) for base in bases):
                yield rels[rel], (label + " — " if label else ""), ship_log_rows(now[rel]), lambda names, records, bases=bases: git_ship_verdicts(names, bases, records)


def ship_problems(trackers):
    """THE SHIPPED RULE's refusals, one line for each tracker a change moves to Shipped without a commit behind it: which tracker,
    what is missing — no commit named · not in the history · nothing changed outside the records — and the way through."""
    if vcs() not in ("git", "svn"):
        return []
    rels = {}
    for t in trackers:
        try:
            rels[(TRACKER_DIR / t["file"]).resolve().relative_to(ROOT).as_posix()] = t
        except (KeyError, ValueError):
            continue                                     # no file, or a link to one outside the repository — as `in_this_commit` reads it
    if vcs() == "git":
        rels.update(staged_absent(rels))                 # the commit being made: a tracker it carries that the working tree lacks is judged too
    if not rels:
        return []                                        # no tracker read from a file: nothing a change could have moved
    records, out, noun = [], [], "revision" if vcs() == "svn" else "commit"

    def unread(why, named=None, newest=False):
        """F1: Subversion's history could not be read, so a move to Shipped cannot be judged — and is refused, not passed. The tracker it was
        reading for, where that is known; else every tracker that is Shipped in the working copy, the ones such a move could be. Where the
        read that failed is the NEWEST revision's — the change judged where nothing is pending, which only the server holds — and no tracker
        in the working copy is Shipped to name, the refusal says that instead: the newest revision is not judged, and is not passed unread (RV-2267)."""
        ids = [named] if named else [t["id"] for t in trackers if t.get("status") == "Shipped"]
        if not ids and newest:
            out.append(f"Subversion's newest revision could not be read, so a move to `Shipped` in it is not judged — and not passed unread. svn said: {why}. Reach the repository, then run again")
        if ids:
            out.append(f'{", ".join(ids[:5])}{f" and {len(ids) - 5} more" if len(ids) > 5 else ""}: Subversion\'s history could not be read, so a move to `Shipped` '
                       f'is not judged — and not passed unread. svn said: {why}. Reach the repository, then run again')

    try:
        for t, where, rows, judge in shipped_moves(rels):
            names = commits_named(rows)
            try:
                records = records or ship_records()
            except ValueError as bad:
                out.append(f'{t["id"]}: {where}moved to `Shipped`, which needs the records told from the product — {bad}')
                continue
            try:
                verdicts = judge(names, records) if names else {}
            except SvnUnreadable as e:
                unread(e, t["id"])
                continue
            if "" in verdicts.values():
                continue
            found = "svn log -v -l 20" if vcs() == "svn" else "git log --oneline -- . " + " ".join(f"':(exclude,top){p}'" for p in records)
            out.append(f'{t["id"]}: {where}moved to `Shipped` with no {noun} behind it — '
                       + (f"its ship log names no {noun}" if not names else "; ".join(f"`{n}` {why}" for n, why in verdicts.items()))
                       + f'. Name the {noun} that built it in a ship-log row (`{found}` finds it), or, where nothing was built, mark it `Closed`, not `Shipped`')
    except SvnUnreadable as e:
        unread(e, e.tracker, e.newest)
    return out


# --- sessions (FM-024, FM-032): a seat's commit names its session, and the registry is a report of the trailers --------
# Seat = author: WHO MAY, read by the rights above. Session = which RUN: a `Session: <id>` trailer on every seat commit,
# appended by the prepare-commit-msg hook from the worktree's `seat.session`, with `Worktree: <the checkout's directory>`
# beside it. The registry is generated from those trailers by `--sessions`, the way INDEX is from the trackers, and is
# kept in no file: until 0.18.0 it was `<tracker dir>/sessions.md`, written by hand and read by the gate, and it
# conflicted whenever two branches landed (FM-032 S2, which is FM-031's S1). The gate keeps one rule: a seat's commit
# carries a `Session:` of the accepted shape whose seat part is its own.
SESSIONS_NAME = "sessions.md"          # the registry's file until 0.18.0 — `--check` warns where one is left
SESSION_ID_RE = re.compile(r"[0-9a-f]{8}(?:/([A-Za-z][A-Za-z0-9_-]*)-\d+)?")      # 8e509911 · 8e509911/reviewer-1
SESSION_RECENT = 86400        # seconds: the board and the digest name the sessions with a commit this recent


def git_out(*a, cwd=None):
    """One git call's stdout, or None when it failed."""
    r = subprocess.run(["git", *a], cwd=cwd or ROOT, capture_output=True, text=True, encoding="utf-8", errors="replace", env=nested_git_env())
    return r.stdout if r.returncode == 0 else None


def sessions_file():
    return TRACKER_DIR / SESSIONS_NAME


def session_log():
    """Every commit of HEAD's history that carries a `Session:`, oldest first — (short sha, commit time, author email,
    author name, the trailer block). One `git log`."""
    log = git_out("log", "--reverse", "-i", "--grep", "^session:", f"--format=%h%x01%ct%x01%ae%x01%an%x01{TRAILERS}%x02",
                  "HEAD") or ""
    out = []
    for rec in log.split("\x02"):
        sha, stamp, email, name, block = (rec.strip("\n").split("\x01") + [""] * 5)[:5]
        if sha and stamp.strip().isdigit():
            out.append((sha, int(stamp), email, name, block))
    return out


def session_rows():
    """THE REGISTRY, generated (FM-032 S2): one row per `Session:` id in HEAD's history — its seat (the author through
    `[seats]`, else the raw author), its first and last commit (time, short sha), how many commits carry it, and its
    worktree (the `Worktree:` trailer, written from 0.18.0 on; an id with two is shown with both), and its model and
    effort (the newest `Model:` and `Effort:` trailers, from 0.19.0 on; empty where none) — in the order of the first commits. Nothing is opened or closed: a session is what its commits say, and it ends at its last one."""
    rows = {}
    for sha, stamp, email, name, block in session_log():
        sid = (trailer_values(block, "Session") or [""])[0]
        if not sid:
            continue
        r = rows.setdefault(sid, dict(id=sid, seats=[], first=(stamp, sha), last=(stamp, sha), commits=0, worktrees=[], model="", effort="", _at={}))
        for key in ("model", "effort"):                                            # the newest commit that carries one, else nothing (shown as —)
            v = (trailer_values(block, key) or [""])[0]
            if v and stamp >= r["_at"].get(key, -1):
                r[key], r["_at"][key] = v, stamp
        seat, where = seat_of(name, email) or email or name, (trailer_values(block, "Worktree") or [""])[0]
        r["seats"] += [seat] if seat not in r["seats"] else []
        r["worktrees"] += [where] if where and where not in r["worktrees"] else []
        r["first"] = (stamp, sha) if stamp < r["first"][0] else r["first"]          # oldest first: a tie keeps the earlier
        r["last"] = (stamp, sha) if stamp >= r["last"][0] else r["last"]            # …and the later one here
        r["commits"] += 1
    return sorted(rows.values(), key=lambda r: r["first"][0])


def sessions_cmd():
    """`--sessions`: the registry as Markdown on stdout — generated from the trailers, written nowhere."""
    if vcs() != "git":
        print("--sessions: the registry is read from git's commit trailers — this is no git repository", file=sys.stderr)
        return EXIT_LINT
    rows = session_rows()
    when = lambda st: f"{datetime.datetime.fromtimestamp(st[0]).strftime('%Y-%m-%d %H:%M')} · {st[1]}"
    cell = lambda v: (v or "—").replace("|", "\\|").replace("\n", " ")
    print("# Sessions\n\nGenerated by `--sessions` from the `Session:` and `Worktree:` trailers of this checkout's history — "
          f"{len(rows)} session(s), {sum(r['commits'] for r in rows)} commit(s). Nothing is kept in a file.\n")
    print("| Session | Seat | First commit | Last commit | Commits | Worktree |\n|---|---|---|---|---|---|")
    for r in rows:
        print("| " + " | ".join(cell(v) for v in (r["id"], ", ".join(r["seats"]), when(r["first"]), when(r["last"]), str(r["commits"]), ", ".join(r["worktrees"]))) + " |")
    twice = [r for r in rows if len(r["worktrees"]) > 1]
    if twice:
        print("\n" + "\n".join(f"- one id, {len(r['worktrees'])} worktrees: {r['id']} ({', '.join(r['worktrees'])})" for r in twice))
    return EXIT_OK


# --- the records-to-product ratio (FM-032) -----------------------------------------------------------------------------
# The rule is filed on its own page (work-tracker/evidence/FM-032/records-to-product-ratio.md); this is the command that page
# names as the reference, and a difference between the two is a bug against the page. Merged pull requests are the merge
# commits on the default branch's first-parent line, each compared with its first parent; a day is the merge's committer date
# in Europe/Berlin; added and deleted lines are counted apart and never netted; a submodule pointer is no line, a binary file
# is 0 lines and one file.
RATIO_DAYS = 7          # the window when `--since` is not given, and the rolling sum's length


def ratio_defaults():
    """`[ratio]`'s defaults as `DEFAULTS` keeps every other: `records` is the tracker directory this tool is configured with
    (`tracker_dir`, wherever a repository keeps it), `exclude` is empty."""
    folder = tracker_folder(CONFIG).as_posix()           # the folder `configure` binds, as `tracker_folder` reads it
    return {"records": [("" if folder == "." else folder) + "/"], "exclude": []}


def ratio_paths(section):
    """(records, exclude): `[ratio]`'s two lists, checked; a ValueError with the one line to print where one is no list of prefixes."""
    out = []
    for key, default in ratio_defaults().items():
        value = section.get(key, default)
        if not isinstance(value, list) or not all(isinstance(v, str) and v.strip() for v in value):
            raise ValueError(f"{CONFIG_NAME}: `[ratio] {key}` is a list of repository-relative prefixes, each a non-empty string — "
                             f"`{key} = {json.dumps(default)}`. Got {value!r}")
        out.append([v.strip() for v in value])
    return out


def ratio_class(path, records, exclude):
    """"skip" for a path left out, "records", or "product" — a prefix with a trailing slash is a directory, a plain one is that file."""
    hit = lambda prefixes: any(path.startswith(p) if p.endswith("/") else path == p for p in prefixes)
    return "skip" if hit(exclude) else "records" if hit(records) else "product"


def ratio_merge(merge, records, exclude):
    """One merge against its first parent: {"records": [added, deleted], "product": [added, deleted], "binary": files}."""
    tot = {"records": [0, 0], "product": [0, 0], "binary": 0}
    raw = (git_out("diff", "--raw", "--no-renames", "-z", f"{merge}^1", merge) or "").split("\0")
    pointers = {raw[i + 1] for i in range(0, len(raw) - 1, 2) if "160000" in raw[i].lstrip(":").split()[:2]}       # ":100644 160000 <sha> <sha> M"
    for entry in (git_out("diff", "--numstat", "--no-renames", "-z", f"{merge}^1", merge) or "").split("\0"):
        if not entry:
            continue
        added, deleted, path = entry.split("\t", 2)
        kind = ratio_class(path, records, exclude)
        if path in pointers or kind == "skip":
            continue
        if added == "-":                                  # binary: no lines, one file
            tot["binary"] += 1
        else:
            tot[kind][0] += int(added)
            tot[kind][1] += int(deleted)
    return tot


def ratio_zone():
    """(the zone as datetime's tzinfo or None, whether it is Europe/Berlin): where no tz database is installed, None."""
    try:
        import zoneinfo
        return zoneinfo.ZoneInfo("Europe/Berlin"), True
    except Exception:                                     # no zoneinfo module, or no tzdata on this machine
        return None, False


def ratio_line(label, tot, merges=None):
    """One day's line — the four counts, the ratio (records added : product added, or why there is none), and the merges."""
    (ra, rd), (pa, pd) = tot["records"], tot["product"]
    ratio = f"{ra / pa:.1f}:1" if pa else "no finite ratio"
    tail = "" if merges is None else f"  ({merges} merge{'' if merges == 1 else 's'}" + (f", {tot['binary']} binary" if tot["binary"] else "") + ")"
    return f"{label}  records +{ra:,} \u2212{rd:,}  product +{pa:,} \u2212{pd:,}  {ratio}{tail}"


def ratio_cmd(since=None, until=None):
    """`--ratio`: records added : product added per Berlin day of the merge, and the rolling seven-day sums. Exit 0; 2 where
    there is nothing to read (no `[ratio]`, no git, no default branch, a date that is none)."""
    section = CONFIG.get("ratio")
    if not isinstance(section, dict):
        print(f"--ratio: {CONFIG_NAME} has no [ratio] section, so there is no ratio to count — add `[ratio]` with `records = {json.dumps(ratio_defaults()['records'])}` "
              "(the prefixes that are records; everything else is product)", file=sys.stderr)
        return 2
    try:
        records, exclude = ratio_paths(section)
    except ValueError as e:
        print(f"--ratio: {e}", file=sys.stderr)
        return 2
    if vcs() != "git":
        print("--ratio: the merges are read from git's first-parent history — this is no git repository", file=sys.stderr)
        return 2
    git = lambda *a: subprocess.run(["git", *a], cwd=ROOT, capture_output=True, text=True, encoding="utf-8", errors="replace", env=nested_git_env())
    trunk = default_trunk(git) or trunk_ref()             # origin's default as this clone fetched it (as `--answer` and the gate read it), else the local one
    if trunk is None:
        print("--ratio: no default branch (origin/HEAD, origin/main, origin/master, main or master) to read the merges from", file=sys.stderr)
        return 2
    zone, berlin = ratio_zone()
    parse = lambda s: datetime.date.fromisoformat(s)
    try:
        today = datetime.datetime.now(zone).date() if zone else datetime.date.today()
        last = parse(until) if until else today
        first = parse(since) if since else last - datetime.timedelta(days=RATIO_DAYS - 1)
    except ValueError:
        print("--ratio: --since and --until are days, YYYY-MM-DD", file=sys.stderr)
        return 2
    if first > last:
        print(f"--ratio: --since {first} is after --until {last}", file=sys.stderr)
        return 2
    log = git_out("log", "--first-parent", "--merges", "--format=%H%x00%cI", trunk)
    if log is None:
        print(f"--ratio: git could not read {ref_name(trunk)}", file=sys.stderr)
        return 2
    lo = first - datetime.timedelta(days=RATIO_DAYS - 1)           # the sums of the window's first days reach back before it
    days = {}
    for row in log.splitlines():
        sha, _, stamp = row.partition("\0")
        when = datetime.datetime.fromisoformat(stamp[:-1] + "+00:00" if stamp.endswith("Z") else stamp)     # 3.9 reads no `Z`
        day = (when.astimezone(zone) if zone else when).date()     # no zone database: the commit's own offset
        if lo <= day <= last:
            tot = days.setdefault(day, {"records": [0, 0], "product": [0, 0], "binary": 0, "merges": 0})
            one = ratio_merge(sha, records, exclude)
            for k in ("records", "product"):
                tot[k][0] += one[k][0]
                tot[k][1] += one[k][1]
            tot["binary"] += one["binary"]
            tot["merges"] += 1
    empty = lambda: {"records": [0, 0], "product": [0, 0], "binary": 0, "merges": 0}
    def add(a, b):
        return {"records": [a["records"][0] + b["records"][0], a["records"][1] + b["records"][1]],
                "product": [a["product"][0] + b["product"][0], a["product"][1] + b["product"][1]],
                "binary": a["binary"] + b["binary"], "merges": a["merges"] + b["merges"]}
    span = lambda a, b: [a + datetime.timedelta(days=i) for i in range((b - a).days + 1)]
    print(f"records-to-product ratio \u2014 records: {', '.join(records)}"
          + (f" (left out: {', '.join(exclude)})" if exclude else "") + "; product: every other path; a submodule pointer is no line, a binary file 0 lines")
    print(f"trunk {ref_name(trunk)} \u00b7 {first} to {last} \u00b7 days are Europe/Berlin"
          + ("" if berlin else " \u2014 NOT: no time zone database here, so each day is the merge's own UTC offset"))
    print("added and deleted lines are apart, never netted; the ratio is records added : product added\n")
    whole = empty()
    for day in span(first, last):
        one = days.get(day, empty())
        whole = add(whole, one)
        print(ratio_line(str(day), one, one["merges"]))
    print("\n" + ratio_line("window    ", whole, whole["merges"]))
    print(f"\n{RATIO_DAYS}-day sums \u2014 each day and the {RATIO_DAYS - 1} before it, read from the repository, not only the window")
    for day in span(first, last):
        run = empty()
        for back in span(day - datetime.timedelta(days=RATIO_DAYS - 1), day):
            run = add(run, days.get(back, empty()))
        print(ratio_line(str(day), run, run["merges"]))
    return EXIT_OK


def session_cmd(words):
    """`--session new` prints an id no `Session:` in this history carries. `open` and `close` are gone since 0.18.0."""
    verb = words[0]
    if verb in ("open", "close"):
        print("--session open/close are gone since 0.18.0: the registry is a report — run --sessions", file=sys.stderr)
        return 2                                        # a command that no longer exists, as argparse says of one it never knew
    if verb == "new" and len(words) == 1:
        import secrets
        ids = {r["id"] for r in session_rows()} if vcs() == "git" else set()
        print(next(s for s in iter(lambda: secrets.token_hex(4), None) if s not in ids))
        return EXIT_OK
    print("--session: new — prints an id no commit carries; the registry is `--sessions`", file=sys.stderr)
    return EXIT_LINT


# --- the harness's own log (FM-024, 0.19.0): what model, at what effort, ran this seat -----------------------------------
# A seat cannot be asked what it runs on — it would answer from its prompt. The harness writes a log of every turn, and the
# log names the model and the effort. Which log is this seat's is never a path: a transcript's `cwd` is the directory the
# session was LAUNCHED in, on every turn, sub-agents included (measured 2026-09-30) — so a seat committing in its own
# worktree matches no log, and one committing in the launch directory matches every sub-agent's. The match is by the id
# the harness gave this seat, written into its worktree by whoever spawned it — `git config --worktree seat.harness <id>`:
# Claude Code's session id for a top-level session (`<slug>/<id>.jsonl`) or the agent id of a sub-agent
# (`<slug>/<session>/subagents/agent-<id>.jsonl`); Codex's thread id (`CODEX_THREAD_ID`, its rollout
# `sessions/Y/M/D/rollout-<time>-<id>.jsonl`). The one file whose NAME carries the id is read, and from it only TOP-LEVEL
# fields of the newest turn that has them — never `message.content`, never a tool's result.
HARNESS_ID_RE = re.compile(r"[0-9A-Za-z][0-9A-Za-z-]{7,}")                  # an id is a name: no separator, no glob character
LOG_WORD_RE = re.compile(r"[A-Za-z0-9][A-Za-z0-9._:/\[\]-]{0,63}")            # a model or an effort as a trailer: one word — no space, no line break
LOG_SCAN = 8 << 20                                                          # bytes, newest first: a log whose fields are older than this names none


def harness_id():
    """This seat's harness id: `seat.harness` of its worktree, else the thread id Codex puts in the environment. A
    Claude Code session's environment names its PARENT's id inside a sub-agent, so it is never read."""
    return (git_out("config", "--get", "seat.harness") or "").strip() or os.environ.get("CODEX_THREAD_ID", "").strip()


def harness_logs(hid):
    """Every log file whose name carries `hid`, under the harness's own folders in the home directory — sorted."""
    home = pathlib.Path(os.path.expanduser("~"))
    claude, codex = home / ".claude" / "projects", home / ".codex" / "sessions"
    return sorted({*claude.glob(f"*/{hid}.jsonl"), *claude.glob(f"*/*/subagents/agent-{hid}.jsonl"), *codex.glob(f"*/*/*/rollout-*-{hid}.jsonl")})


def log_lines_newest_first(path, budget=LOG_SCAN):
    """The lines of a file, last first, reading from its end in blocks — at most `budget` bytes."""
    with open(path, "rb") as f:
        pos, seen, rest = f.seek(0, 2), 0, b""
        while pos > 0 and seen < budget:
            step = min(1 << 20, pos)
            pos -= step
            f.seek(pos)
            parts = (f.read(step) + rest).split(b"\n")
            seen += step
            rest, done = (parts[0], parts[1:]) if pos > 0 else (b"", parts)
            yield from reversed(done)


def read_harness_log(path):
    """{model, effort, cwd} from the newest turns that carry them — top-level fields only. Claude Code: `message.model`, the
    top-level `perTurnEffort` and `cwd`; Codex: `turn_context`'s `model` and `effort`, and `cwd`. `message.content`, a
    tool's result and every other field are never looked at, and the values that come back are single words — a value
    with a space or a line break is no value, so nothing a transcript says reaches a commit message as a second trailer."""
    got = {}
    for raw in log_lines_newest_first(path):
        try:
            turn = json.loads(raw)
        except ValueError:
            continue
        if not isinstance(turn, dict):
            continue
        message, payload = turn.get("message"), turn.get("payload")
        found = {}
        if isinstance(message, dict):
            found = {"model": message.get("model"), "effort": turn.get("perTurnEffort"), "cwd": turn.get("cwd")}
        elif turn.get("type") == "turn_context" and isinstance(payload, dict):
            found = {"model": payload.get("model"), "effort": payload.get("effort"), "cwd": payload.get("cwd")}
        elif turn.get("type") == "session_meta" and isinstance(payload, dict):
            found = {"cwd": payload.get("cwd")}
        for key, value in found.items():
            ok = isinstance(value, str) and (LOG_WORD_RE.fullmatch(value) if key != "cwd" else 0 < len(value) < 400 and value.isprintable())
            if ok and key not in got:
                got[key] = value
        if len(got) == 3:
            break
    return {"model": got.get("model", ""), "effort": got.get("effort", ""), "cwd": got.get("cwd", "")}


def harness_reading(hid):
    """(reading, problem) for a harness id: reading is {path, model, effort, cwd} or None where there is no id or no log by
    that id; problem says why there is none, or that two files carry the id — never a guess between them."""
    if not hid:
        return None, "`seat.harness` is not set in this worktree — no model or effort"
    if not HARNESS_ID_RE.fullmatch(hid):
        return None, f"`seat.harness` is {hid!r} — an id is letters, digits and hyphens, at least eight"
    logs = harness_logs(hid)
    if len(logs) > 1:
        return None, f"two logs carry the harness id {hid}: {logs[0]} and {logs[1]}" + (f" (and {len(logs) - 2} more)" if len(logs) > 2 else "") + " — refusing to pick one"
    if not logs:
        return None, f"no log carries the harness id {hid} under ~/.claude/projects or ~/.codex/sessions — no model or effort"
    found = dict(read_harness_log(logs[0]), path=str(logs[0]))
    gone = [k for k in ("model", "effort") if not found[k]]
    return found, (f"{logs[0]} names no {' and no '.join(gone)} in its newest {LOG_SCAN >> 20} MiB" if gone else "")


def whoami():
    """`--whoami`: who this session is, as the line a seat's report opens with (AGENTS.md) —
    `From: <session> <seat> (<worktree>) · <model> · <effort>`; a message a person carries between sessions names its target
    by the same identity after `To:`. The session is from `seat.session`, the seat from `[seats]` by the
    worktree's `user.email`, the worktree's folder, and the model and effort from the harness's log by `seat.harness`
    (`—` where there is none). A second line names the log and the directory its session was launched in, for a person to
    read. Exit 4 (the lint code) without a `seat.session`; exit 2 where two logs carry the id."""
    sid = (git_out("config", "--get", "seat.session") or "").strip()
    if not sid:
        print("--whoami: this worktree has no `seat.session` — a seat's worktree carries one (`git config --worktree seat.session <id>`; the Owner's checkout none)", file=sys.stderr)
        return EXIT_LINT
    email, name = (git_out("config", "--get", "user.email") or "").strip(), (git_out("config", "--get", "user.name") or "").strip()
    top = (git_out("rev-parse", "--show-toplevel") or "").strip()
    reading, problem = harness_reading(harness_id())
    if reading is None and problem.startswith("two logs"):
        print(f"--whoami: {problem}", file=sys.stderr)
        return 2
    print(f"From: {sid} {seat_of(name, email) or email or name or '—'} ({pathlib.Path(top).name if top else ROOT.name}) · "
          f"{(reading or {}).get('model') or '—'} · {(reading or {}).get('effort') or '—'}")
    if reading:
        print(f"    read from {reading['path']}" + (f" — its session was launched in {reading['cwd']}" if reading["cwd"] else ""))
    if problem:
        print(f"--whoami: {problem}", file=sys.stderr)
    return EXIT_OK


def session_trailer(message_file):
    """What the prepare-commit-msg hook calls: append `Session: <seat.session>` and `Worktree: <the checkout's directory>`
    to the message being written — and `Model:` and `Effort:` where the harness's log, found by `seat.harness`, names them
    (`whoami`'s reading). Nothing when this worktree has no `seat.session` (the Owner's checkout, a person's clone); a
    trailer the message carries already is left alone — an amend, a rebase, a seat that typed it. A log that cannot be
    read, or two that carry the id, costs the commit its two trailers and a line on stderr — never the commit."""
    sid = (git_out("config", "--get", "seat.session") or "").strip()
    if not sid or not message_file:
        return EXIT_OK
    top = (git_out("rev-parse", "--show-toplevel") or "").strip()
    worktree = pathlib.Path(top).name if top else ROOT.name
    hid = harness_id()
    reading, problem = harness_reading(hid) if hid else (None, "")
    if problem:
        print(f"--session-trailer: {problem}" + (" — no Model: or Effort: on this commit" if reading is None else ""), file=sys.stderr)
    trailers = [f"Session: {sid}", f"Worktree: {worktree}"] + [f"{key}: {reading[k]}" for key, k in (("Model", "model"), ("Effort", "effort")) if reading and reading[k]]
    r = subprocess.run(["git", "interpret-trailers", "--in-place", "--if-exists", "doNothing", *itertools.chain.from_iterable(("--trailer", t) for t in trailers), message_file],
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


def history_has_sessions(revs):
    """Has this history adopted the session rule — does any commit reachable from `revs` carry a `Session:`? A repository
    adopts the rule with its first trailer, as it adopted it with its first registry row until 0.18.0: a seat's commit
    made before any is not judged, and a consumer that never set `seat.session` is not refused on vendoring."""
    return bool(revs) and bool((git_out("log", "-1", "--format=%H", "-i", "--grep", "^session:", *revs) or "").strip())


FORMER_NAMES = {"planner": ("principal",), "builder": ("implementer",)}     # the built-in seats' former names (FM-024): a session id may still carry them


def session_names(seat):
    """The names a session id's `<seat>-<n>` part may carry for this seat (FM-024, the switch): its own; and the labels it has left
    from before — its built-in former name (`principal` for `planner`, `implementer` for `builder`) and the name of each `<name>@seat`
    address it lists. A seat renamed keeps its old address beside the new, and the sessions begun under the old name
    (`<id>/gtm-<n>`, `<id>/implementer-<n>`), in the history and in worktrees in flight, keep reading as the seat's.
    EVERY LABEL NAMES EXACTLY ONE SEAT (RV-2207, RV-2240): a label that is another seat's own name stays that seat's — both
    spellings configured as two seats, or a list that holds `builder@seat` beside a seat `builder` — and a label two seats
    claim as a former name or an old address passes for neither. An unshared old label keeps passing."""
    claims = {}                                   # label -> the seats that claim it as a former name or an old address
    for s, ids in SEATS.items():
        for label in {*FORMER_NAMES.get(s, ()), *(who[:-len("@seat")] for who, _mode in ids if who.endswith("@seat"))}:
            claims.setdefault(label, set()).add(s)
    return {seat} | {label for label, by in claims.items() if by == {seat} and label not in SEATS}


def session_problems():
    """THE GATE'S ONE RULE (FM-032 S2): a commit by a seat `[seats]` names — never the Owner's, never an author outside
    `[seats]` — carries a `Session:` of the accepted shape, `<8 hex>` or `<8 hex>/<seat>-<n>`, whose seat part, where it
    has one, is the author's seat (or a name the seat had: `session_names`). Judged on every change the rights are judged on (`changes_under_review`): the commit
    being made reads `seat.session`, the trailer its hook will write; a made commit — HEAD, or one a merge brings — reads
    its own trailer. A commit with no `Session:` anywhere in its history is not judged (`history_has_sessions`). No row
    is read: the open and closed rows, the one-worktree rule and the registry's removal went with the file in 0.18.0."""
    if not SEATS or vcs() != "git":
        return []
    out = []
    for bases, _files, name, email, commit, _result, label in changes_under_review():
        seat = seat_of(name, email)
        if seat in (None, "owner"):
            continue
        sid = ((trailer_values(_WALK_COMMITS[commit][1], "Session") if commit in _WALK_COMMITS else trailers_of(commit, "Session")) or [""])[0] if commit \
            else (git_out("config", "--get", "seat.session") or "").strip()
        who = f"commit {commit[:10]} by {email or name}" if commit else f"this commit by {email or name}"
        shape = SESSION_ID_RE.fullmatch(sid)
        if not sid:
            why = f"{who} carries no Session: trailer — set `git config --worktree seat.session <id>` in its worktree: the harness's session id, its first eight hex characters, or `<parent>/{seat}-<n>` for a sub-agent"
        elif not shape:
            why = f"{who} carries `Session: {sid}` — a session id is eight hex characters, or `<id>/<seat>-<n>` for a sub-agent"
        elif shape[1] and shape[1] not in session_names(seat):
            why = f"{who} is the seat {seat}, and its Session: {sid} names the seat {shape[1]}"
        else:
            continue
        if sessions_before(_WALK_COMMITS[commit][0][:1] if commit in _WALK_COMMITS else bases):
            out.append(f"{label + ' — ' if label else ''}refused: {why}")
    return out


def sessions_before(revs):
    """`history_has_sessions`, answered from the walk's own log where `revs` are commits it listed — a commit carries a `Session:`, or one
    of its parents' histories does — and with one git call for each other revision, kept: a fixed number of calls however long the
    branch (v0.19.1)."""
    for rev in [r for r in revs if r in _WALK_COMMITS]:
        todo = [rev]
        while todo:                                     # oldest first, without recursion: a long branch is a deep chain
            c = todo[-1]
            if c in _HAS_SESSIONS:
                todo.pop()
                continue
            parents, block = _WALK_COMMITS[c]
            pending = [q for q in parents if q in _WALK_COMMITS and q not in _HAS_SESSIONS]
            if pending:
                todo += pending
                continue
            _HAS_SESSIONS[c] = bool(trailer_values(block, "Session")) or any(
                _HAS_SESSIONS[q] if q in _WALK_COMMITS else outside_sessions(q) for q in parents)
            todo.pop()
    return any(_HAS_SESSIONS[r] if r in _WALK_COMMITS else outside_sessions(r) for r in revs)


def outside_sessions(rev):
    """`history_has_sessions` of one revision outside the walk, asked once per run."""
    key = ("outside", rev)
    if key not in _HAS_SESSIONS:
        _HAS_SESSIONS[key] = history_has_sessions([rev])
    return _HAS_SESSIONS[key]


def session_check():
    """`--session-check`: the session rule on the commit being made, and nothing else — cheap enough for every commit.
    The full gate runs only when a tracker, the configuration or the tool is staged; without this, a seat's code-only
    commit would be judged by no automatic run at all (R4). FM-033's judgement needs the commit's subject, which the
    pre-commit stage has not got: it is the commit-msg hook's (`--commit-msg`)."""
    global COMMITTING
    COMMITTING = True
    problems = session_problems()
    for p_ in problems:
        print(f"  {p_}", file=sys.stderr)
    return EXIT_LINT if problems else EXIT_OK


BUILD_WHY = "a pass judges before the first build commit (FM-033): keep it with --triage first, or build under a judged In Progress tracker"


def branch_tracker(name):
    """The tracker a branch names: `fm/029-…` → FM-029 — the kind in lower case, a slash, the number, then a dash or the end
    (the house shape `<kind>/<NNN>-<slug>`). None for any other name, and for a detached HEAD."""
    m = re.match(r"(%s)/(\d+)(?:-|$)" % "|".join(KINDS), name or "", re.I)
    return f"{m.group(1).upper()}-{m.group(2)}" if m else None


def named_trackers(subject, branch):
    """The trackers a commit is built under: the ids its subject names when it names any, else its branch's (C1 of the
    0.18.3 design, ruled 2026-09-24) — a commit `FM-030: …` on a branch named for FM-029 is FM-030's work."""
    if subject is None:                                    # a message that keeps no subject line: nothing names a tracker
        return []
    ids = list(dict.fromkeys(re.findall(rf"(?<![A-Za-z0-9])({_IDS})(?!\d)", subject or "")))
    return ids or [b for b in [branch_tracker(branch)] if b]


def commit_list(*revs):
    """[(commit, its first parent, the paths it changes relative to ROOT, its subject)] of `git log --no-merges <revs>`,
    newest first — one call for all of them."""
    out = git_out("log", "--no-merges", "--relative", "--name-only", "--format=%x00%H%x00%P%x00%s", *revs) or ""
    records, got = out.split("\x00")[1:], []
    for i in range(0, len(records) - 2, 3):
        subject, _, files = records[i + 2].partition("\n")
        got.append((records[i], (records[i + 1].split() or [""])[0], set(files.split("\n")) - {""}, subject.strip()))
    return got


def cat_blobs(specs, env=None, types=None):
    """The text of each `<rev>:<path>` — one `git cat-file --batch` for all of them; None for one that is not there. `env`:
    the hook's own, where `:<path>` must read the index git hands it (FM-037). `types`, where given, gets each object's type —
    `blob` for a file, `tree` for a folder, `commit` for a submodule: one whose commit this clone holds, and one git answers
    `<oid> submodule` for — a header with no size and nothing after it — whose text is None. A header read no other way is
    no text, and nothing after it is read: where its object ends cannot be told, so neither can the next one's header. A
    spec holding a line break is never asked — git would read it as two names, and answer each — and its text is None."""
    got = {s_: None for s_ in specs if "\n" in s_ or "\r" in s_}
    asked = [s_ for s_ in specs if s_ not in got]
    if not asked:
        return got
    r = subprocess.run(["git", "cat-file", "--batch"], input="".join(s_ + "\n" for s_ in asked).encode("utf-8"), cwd=ROOT,
                       capture_output=True, env=env or nested_git_env())
    data, i = r.stdout, 0
    for spec in asked:
        nl = data.find(b"\n", i)
        if nl < 0:
            break
        head, i = data[i:nl].decode("utf-8", "replace"), nl + 1
        if head.endswith((" missing", " ambiguous")):
            got[spec] = None
            continue
        if re.fullmatch(r"(?:[0-9a-f]{40}|[0-9a-f]{64}) submodule", head):
            got[spec] = None                            # a submodule: no text, and the next header follows at once
            if types is not None:
                types[spec] = "commit"
            continue
        m = re.fullmatch(r"(?:[0-9a-f]{40}|[0-9a-f]{64}) ([a-z]+) ([0-9]+)", head)
        if not m or data[i + int(m[2]):i + int(m[2]) + 1] != b"\n":
            got[spec] = None                            # a header it cannot read, or an object cut short: no text, and nothing after it is read
            break
        size = int(m[2])
        if types is not None:
            types[spec] = m[1]
        got[spec], i = data[i:i + size].decode("utf-8", "replace"), i + size + 1
    return got


def judge_commits(commits, branch):
    """FM-033's gate over made or pending commits — [(commit or "", the parent it is judged at, paths, subject)] — as refusal
    lines. A commit that changes no path outside the tracker directory is not judged. One that does names its trackers
    (`named_trackers`), and at its parent at least one of them carries `triaged:`, is not Parked and is `In Progress`, read
    through `extract` from the parent's own file: one `git ls-tree` per parent and one `git cat-file --batch` for all."""
    rel = TRACKER_DIR.resolve().relative_to(ROOT).as_posix().rstrip("/") + "/"
    work = []
    for commit, parent, files, subject in commits:
        outside = sorted(f for f in files if f and not f.startswith(rel))       # `staged_now` keeps git's last empty line
        if outside:
            work.append((commit, parent, outside, subject, named_trackers(subject, branch)))
    key = lambda tid: (tid.split("-")[0].upper(), int(tid.split("-")[1]))
    names = {}
    for parent in sorted({w[1] for w in work if w[4]}):
        listed = (git_out("ls-tree", "--full-name", "--name-only", parent, "--", rel) or "").split("\n")
        names[parent] = {}
        for full in listed:
            m = re.match(r"(%s)-(\d+)-" % "|".join(KINDS), full.rsplit("/", 1)[-1])
            if m:
                names[parent][(m.group(1), int(m.group(2)))] = full
    wanted = {f"{parent}:{names[parent][key(tid)]}" for _c, parent, _o, _s, ids in work for tid in ids if key(tid) in names.get(parent, {})}
    texts = cat_blobs(sorted(wanted))
    out = []
    for commit, parent, outside, subject, ids in work:
        reasons = []
        for tid in ids:
            full = names.get(parent, {}).get(key(tid))
            text = texts.get(f"{parent}:{full}") if full else None
            t = extract(pathlib.Path(full), text=text) if text is not None else None
            if t is None:
                reasons.append(f"{tid}: not at its parent")
            elif t["status"] == "Parked":
                reasons.append(f"{tid}: Parked")
            elif not t.get("triaged"):
                reasons.append(f"{tid}: not judged" + ("" if t["status"] == "In Progress" else f", not In Progress ({t['status']})"))
            elif t["status"] != "In Progress":
                reasons.append(f"{tid}: not In Progress ({t['status']})")
            else:
                reasons = []
                break
        else:
            if not ids and subject is None:
                reasons = ["names no tracker: every line of its message is a comment, which git strips — no subject is left to name one"]
            elif not ids:
                reasons = [f"names no tracker: no {'/'.join(KINDS)}-N in its subject, and "
                           + (f"its branch `{branch}` names none (`<kind>/<NNN>-…`)" if branch else "a detached HEAD names none")]
        if reasons:
            who = (f'commit {commit[:7]} "{first_words(subject, 60)}"' if commit
                   else "this commit, with no subject," if subject is None else f'this commit "{first_words(subject, 60)}"')
            more = f" (+{len(outside) - 1} more)" if len(outside) > 1 else ""
            out.append(f"refused: {who} changes {outside[0]}{more} outside {rel} — {'; '.join(reasons)} — {BUILD_WHY}")
    return out


_BUILD = None


def build_judgement(subject=None):
    """(refusals, the one line `--check` says) — FM-033's gate, where `judged_before_build` is on. At commit time it runs
    where the subject is known — the commit-msg hook, `--commit-msg`, `subject` its message's first line — and judges the
    commit being made at HEAD exactly as the history is judged: the subject's ids, else the branch (a merge: each commit it
    brings, the trunk's aside, at its own parent by its own subject; its own change never). The pre-commit run, which has
    no message yet, judges nothing here: judged by its branch alone, `FM-007: …` on a branch named for FM-029 passed the
    hook and failed `--check` (the cold review's R1). Any other run judges each commit of `merge-base(origin's default,
    HEAD)..HEAD`, merges walked, not judged. On the default branch nothing is judged. Read once per run."""
    global _BUILD
    if COMMITTING and not subject:
        return [], ""                                      # the commit-msg stage judges it, with its subject (`pending_judgement`)
    if _BUILD is not None:
        return _BUILD
    if not CONFIG.get("judged_before_build"):
        _BUILD = ([], f"judged before build: off — `judged_before_build = true` in {CONFIG_NAME} turns it on")
        return _BUILD
    if vcs() != "git":
        _BUILD = ([], "judged before build: on — this is no git repository: nothing is judged")
        return _BUILD
    git = lambda *a: subprocess.run(["git", *a], cwd=ROOT, capture_output=True, text=True, encoding="utf-8", errors="replace", env=nested_git_env())
    trunk, branch = default_trunk(git), built_on()
    if trunk and branch == ref_name(trunk).split("/", 1)[1]:
        _BUILD = ([], f"judged before build: on — `{branch}` is the default branch: nothing on it is judged")
        return _BUILD
    if COMMITTING:
        _BUILD = (pending_judgement(subject, git, trunk, branch), "")
        return _BUILD
    if not trunk:
        _BUILD = ([], "judged before build: on — no `origin` default branch to measure from: nothing is judged")
        return _BUILD
    base = git("merge-base", trunk, "HEAD").stdout.strip()
    commits = commit_list(f"{base}..HEAD") if base else []
    refused = judge_commits(commits, branch)
    _BUILD = (refused, f"judged before build: on — {len(commits)} commit(s) on {f'`{branch}`' if branch else 'a detached HEAD'} since {ref_name(trunk)}, "
                       + (f"{len(refused)} refused" if refused else "every build commit under a judged In Progress tracker"))
    return _BUILD


def build_problems():
    return build_judgement()[0]


def pending_judgement(subject, git, trunk, branch):
    """The commit being made, at HEAD, with `subject` — None where its message keeps no subject line — as refusal lines; a
    merge being made: each commit it brings, the trunk's aside, by its own subject."""
    heads = merge_heads()
    if heads:
        return judge_commits(commit_list(*heads, "--not", "HEAD", *([trunk] if trunk else [])), branch)
    if git("rev-parse", "--verify", "-q", "HEAD").returncode != 0:
        return []                                          # a first commit has no parent to be judged at
    # what THIS commit carries: `commit -a` and `commit <path>` hand the hook an index of their own
    env = dict(nested_git_env(), **({"GIT_INDEX_FILE": os.environ["GIT_INDEX_FILE"]} if os.environ.get("GIT_INDEX_FILE") else {}))
    staged = subprocess.run(["git", "diff", "--cached", "--name-only", "--relative"], cwd=ROOT, capture_output=True, text=True,
                            encoding="utf-8", errors="replace", env=env).stdout
    return judge_commits([("", "HEAD", set(staged.split("\n")) - {""}, subject)], branch)


def message_subject(text, comment="#"):
    """A commit message's subject as git keeps it when it strips comments — an edited message, `--cleanup=strip`: its
    first line that is not blank and does not start with the comment character (`core.commentChar`), above the scissors
    line an editor commit carries. "" where none is left."""
    for line in text.split(f"{comment} ------------------------ >8 ------------------------")[0].splitlines():
        if line.strip() and not line.startswith(comment):
            return line.strip()
    return ""


def literal_subject(text):
    """A commit message's subject as git keeps it when it does NOT strip comments — `-m`/`-F` (whitespace cleanup), or
    `--cleanup=verbatim`: its first line that is not blank, a `#` at its start kept."""
    return next((line.strip() for line in text.splitlines() if line.strip()), "")


def commit_msg_check(message_file):
    """`--commit-msg <file>`: what the commit-msg hook runs — FM-033's judgement on the commit being made, with its subject,
    before the commit is made: the same refusal `--check` prints of it once made. BEST-EFFORT, the Principal's ruling: git's
    `--no-verify` skips any hook by design, so the gate is `--check` on the branch.

    The hook sees the message BEFORE git's cleanup, and cannot always know which cleanup git will apply: an edited message
    is stripped of its comment lines, `-m` keeps them (the cold second pass's R1: `-m '# FM-007: …'` passed a hook that
    skipped every `#` line, and `--check` refused the commit git made with that subject). So it judges every subject git
    could keep: the first line left once comment lines are stripped (`core.commentChar`, `#` by default) — and none left
    is *names no tracker* — and, where git keeps comment lines (no editor, the hook's `GIT_EDITOR=:`; or `commit.cleanup`
    `whitespace` or `verbatim`), the literal first line too. The commit is refused if any of them is."""
    global COMMITTING
    COMMITTING = True
    try:
        text = pathlib.Path(message_file).read_text(encoding="utf-8", errors="replace")
    except OSError as e:
        print(f"--commit-msg: cannot read {message_file} — {e}", file=sys.stderr)
        return EXIT_LINT
    if not CONFIG.get("judged_before_build") or vcs() != "git":
        return EXIT_OK
    git = lambda *a: subprocess.run(["git", *a], cwd=ROOT, capture_output=True, text=True, encoding="utf-8", errors="replace", env=nested_git_env())
    trunk, branch = default_trunk(git), built_on()
    if trunk and branch == ref_name(trunk).split("/", 1)[1]:
        return EXIT_OK                                     # on the default branch nothing is judged
    comment = ((git_out("config", "--get", "core.commentChar") or "#").strip() or "#")[:1]
    comment = "#" if comment == "a" else comment          # `auto`: git picks one the message does not use; `#` is its first choice
    keeps = os.environ.get("GIT_EDITOR") == ":" or (git_out("config", "--get", "commit.cleanup") or "").strip() in ("whitespace", "verbatim")
    stripped, literal = message_subject(text, comment), literal_subject(text)
    subjects = list(dict.fromkeys([stripped or None] + ([literal] if keeps and literal and literal != stripped else [])))
    problems = []
    for subject in subjects:
        problems += [p_ for p_ in pending_judgement(subject, git, trunk, branch) if p_ not in problems]
    if stripped == "" and len(problems) > 1:              # the precise refusal of the literal subject says it; the empty one adds nothing
        problems = [p_ for p_ in problems if "no subject is left" not in p_]
    for p_ in problems:
        print(f"  {p_}", file=sys.stderr)
    return EXIT_LINT if problems else EXIT_OK


# FM-037 — ONLY THE OWNER CHANGES THEIR INTENT AND THEIR CURRENT PATH (their word of 2026-09-25, through the Auditor seat's AU-12:
# a seat's unsigned commit rewrote a line of their path, and every gate passed it). The two sections of TRIAGE.md a pass reads
# as theirs — `## The intent` and `## The current path`, by the repository's names or the English ones — are judged by what
# the tool READS: each commit is read under its OWN `shoalmark.toml` (its `tracker_dir` names the file, its `[headings]` the
# two names), a section is its heading line and everything under it up to the next `## `, byte for byte, and that text is
# compared with what the commit's parent reads — a merge's with what each of its parents reads. Renaming or removing a
# heading, deleting TRIAGE.md, moving it away from its name or out from under the tracker directory, pointing `tracker_dir`
# elsewhere: after each the tool reads other words or none, and each is a change. A move of the whole tracker together with
# its key, the two sections byte-identical before and after — `ae1f05e`, FM-002's move out of `docs/work-tracker/` — is not:
# every word of theirs reads as it did (the pass's R7; the reading is stated in the README). Whitespace counts: the text is
# printed as written, and a comparison with no normaliser has nothing a seat could learn to slip past. `## Passes` and all
# outside the two stay open to seats; a scaffold, where no section was, is accepted (`unwritten`). A change is refused
# unless it is the Owner's signed commit: `%G?` G, the signer principal (`%GS`) the author's email, the author the Owner.
# The Owner is read from the default branch's `shoalmark.toml`, never the branch's own: a branch that named a seat the Owner,
# or took `signed` off their seat, and then changed their words, would otherwise judge itself. Nor may it vouch for its own key
# (the Auditor seat's AU-19): a signature is verified against the default branch's signers file (`trusted_signers`), and
# a change to that file is kept like the two sections (`signers_paths`, `kept_changes`).
GUARDED = ("intent", "path")
GUARD_WHY = "only the Owner changes their intent and their current path (FM-037)"
# …and the file their signature is verified against (the Auditor seat's AU-19): a branch that appends its own key under their
# email to the repository's signers file would otherwise have vouched for itself
GUARD_WHY_KEYS = "only the Owner changes the keys their signature is verified against (FM-037, AU-19)"
# the way through, as the tool already asks a seat to put a question in front of them (`--new`, the contract's `ask:` rule)
GUARD_WAY = ("the Owner commits it signed; a seat proposes the change as an ask — `ask:` in its tracker, one sentence they can "
             "answer, with `ask-kind: ruling`, `ask-since:` and `next: owner`")
GUARD_LIMIT = "a commit signed with the Owner's key passes; at tier 0 any process on their account holds that key (FM-007)"
# what it can prove where their seat asks for no signature (clause 5) — and where it proves nothing, Subversion's working copy
GUARD_AUTHOR_ONLY = "the author only — mark `owner` signed to prove the key"
# where this tool refuses the default branch's configuration, who the Owner is is not known: a change to what only they change is
# refused, not left unguarded (the Owner's ruling of 2026-10-03, v0.19.1) — and the way through, the words such a refusal ends on
GUARD_UNREAD = "configuration cannot be read here, so who the Owner is is not known, and a change to their two sections or their signers file is not passed unread"
GUARD_UNREAD_WAY = "land the configuration change on the default branch first, or upgrade there"
GUARD_SVN = ("the Owner's two sections: Subversion is out of scope for FM-037 — its working copy carries no signature, so "
             "nothing here can tell their commit from a seat's")
_GUARD = None


def guarded_sections(text, heads):
    """{"intent": the section as a pass reads it — its heading line and all under it up to the next `## `, byte for byte — or
    None, "path": …} of one TRIAGE.md (`text` None: no file). `heads` names them as that revision's `[headings]` does; the
    English names are read as well and the first heading found is the one read, as `triage_home` reads them."""
    out = {}
    for k in GUARDED:
        m = re.search(rf"^## (?:{re.escape(heads[k])}|{re.escape(DEFAULTS['headings'][k])})[ \t]*\n.*?(?=^## |\Z)", text, re.S | re.M) if text is not None else None
        out[k] = m.group(0) if m else None
    return out


_MODES = {}
_TREES = {}
_VIEWS = {}


def tree_paths(rev, env=None):
    """Every path `rev` holds, from the repository's root — "" the index (`env` the hook's) — or None where git cannot list
    them: one `git ls-tree -r` (for the index `git ls-files`) a revision, read once per run."""
    key = (str(ROOT), rev)
    if key not in _TREES:
        args = ["ls-files", "-z", "--full-name", "--", ":/"] if rev == "" else ["ls-tree", "-r", "-z", "--name-only", "--full-tree", rev]
        r = subprocess.run(["git", *args], cwd=ROOT, capture_output=True, text=True, encoding="utf-8", errors="replace", env=env or nested_git_env())
        _TREES[key] = [x for x in r.stdout.split("\x00") if x] if r.returncode == 0 else None
    return _TREES[key]


def path_mode(rev, path, env=None):
    """The mode git records for `path`, from the repository's root, at `rev` — "" where nothing is there, "?" where git
    cannot say; "" as `rev` is the index (`env` carries the hook's). Asked only where `git cat-file` found nothing, which
    is also what it says of a submodule whose commit this clone does not hold: one `git ls-tree` a revision and path, read
    once per run."""
    key = (str(ROOT), rev, path)
    if key not in _MODES:
        args = ["ls-files", "-s", "-z", "--full-name", "--", f":/{path}"] if rev == "" else ["ls-tree", "-z", "--full-tree", rev, "--", path]
        r = subprocess.run(["git", *args], cwd=ROOT, capture_output=True, text=True, encoding="utf-8", errors="replace", env=env or nested_git_env())
        rows = [row.partition("\t") for row in r.stdout.split("\x00") if row]
        _MODES[key] = ("?" if r.returncode != 0 else next((m.split(" ", 1)[0] for m, _t, name in rows if name == path), "040000" if rows else ""))
    return _MODES[key]


def config_not_file(kind):
    """Why a revision's configuration cannot be read where git records no file at its path: `kind` the mode or the type."""
    what = {"160000": "a submodule", "commit": "a submodule", "040000": "a folder", "tree": "a folder", "120000": "a symlink"}.get(kind, f"no file it can list (`{kind}`)")
    return f"{CONFIG_NAME}: not a file — git records {what} at that path, and only a file is read as the configuration"


def guard_config(text, prefix=""):
    """(`tracker_dir`, `[headings]`, the tracker folder below `prefix`) as `configure` reads them from one revision's
    configuration — `text` None: there is none, the defaults. The folder is `tracker_folder`'s, the one `configure` binds:
    the guard computes no path of its own. Where this tool cannot read it as `configure` would — `read_config` refuses it,
    `tracker_dir` is no folder of the repository, `[headings]` is not the table `configure` takes — SystemExit with the
    reason: never the defaults."""
    cfg = read_config(text) if text is not None else {}
    tdir, heads = cfg.get("tracker_dir", DEFAULTS["tracker_dir"]), cfg.get("headings", {})
    if not isinstance(tdir, str) or tracker_folder(cfg).is_absolute() or ".." in tracker_folder(cfg).parts:
        raise SystemExit(f"{CONFIG_NAME}: `tracker_dir` is a folder inside the repository, its path in quotes — got {tdir!r}")
    if not isinstance(heads, dict) or set(heads) - set(DEFAULTS["headings"]) or not all(isinstance(v, str) and v.strip() for v in heads.values()):
        raise SystemExit(f"{CONFIG_NAME}: `[headings]` names {', '.join(DEFAULTS['headings'])} — each a section name, none empty")
    return tdir, {**DEFAULTS["headings"], **heads}, tracker_folder(cfg, prefix).as_posix()


def view_label(rev):
    """A revision as a guard's line names it: a commit by its 7 characters, the index as what the commit being made stages."""
    return "what this commit stages" if rev == "" else rev[:7] if re.fullmatch(r"[0-9a-f]{40}", rev) else ref_name(rev)


def triage_views(revs, env=None, prefix=None, modes=()):
    """{rev: (its `tracker_dir`, its TRIAGE.md from the repository's root, whether that file is there, its two sections, its
    `[headings]`, "" — or why its configuration cannot be read, its tracker folder from the root)} — the folder and the
    home `tracker_folder`'s, as the tool reads them — each revision read under its OWN `shoalmark.toml`; "" is
    the index, what a commit being made stages (`env` carries the hook's `GIT_INDEX_FILE`). A configuration this tool cannot
    read (`guard_config`), or no file at its path — a submodule, a folder (`path_mode`) — is never read as the defaults: its
    view says so, and reads no sections — every reader of a view refuses where one it needs cannot be read. Only a path
    with nothing at it is no configuration: the defaults, as `configure` reads them. A symlink there is no file either: its
    mode is read (`path_mode`) for each revision of `modes` — the default branch, and a revision that changes the
    configuration's path; at any other, the path holds what its parent's did. `prefix`: the repository's, where the caller
    has it. Two `git cat-file --batch` calls for all of them that this run has not read yet — a revision is read once per
    run (`_VIEWS`), the index never kept."""
    if prefix is None:
        prefix = _VIEWS.get((str(ROOT), "prefix"))
        if prefix is None:
            prefix = _VIEWS[(str(ROOT), "prefix")] = (git_out("rev-parse", "--show-prefix") or "").strip()
    key = lambda r: (str(ROOT), prefix, r, r in modes)
    kept = {r: _VIEWS[key(r)] for r in revs if r != "" and key(r) in _VIEWS}
    revs = [r for r in revs if r not in kept]
    at = lambda rev, path: f"{rev}:{path}"
    types = {}
    configs = cat_blobs([at(r, prefix + CONFIG_NAME) for r in revs], env, types)
    where = {}
    for r in revs:
        spec = at(r, prefix + CONFIG_NAME)
        try:
            kind = types.get(spec, "blob") if configs.get(spec) is not None else path_mode(r, prefix + CONFIG_NAME, env) or "blob"
            if kind == "blob" and r in modes and path_mode(r, prefix + CONFIG_NAME, env) == "120000":
                kind = "120000"
            if kind != "blob":
                raise SystemExit(config_not_file(kind))
            tdir, heads, folder = guard_config(configs.get(spec), prefix)
        except SystemExit as e:
            where[r] = (None, "", None, f"{prefix + CONFIG_NAME} at {view_label(r)} cannot be read here — {e}", "")
            continue
        where[r] = (tdir, (pathlib.PurePosixPath(folder) / "TRIAGE.md").as_posix(), heads, "", folder)
    texts = cat_blobs(sorted({at(r, home) for r, (_d, home, _h, why, _f) in where.items() if not why}), env)
    read = {r: (tdir, home, False, {k: None for k in GUARDED}, heads, why, folder) if why else
               (tdir, home, texts.get(at(r, home)) is not None, guarded_sections(texts.get(at(r, home)), heads), heads, "", folder)
            for r, (tdir, home, heads, why, folder) in where.items()}
    _VIEWS.update({key(r): v for r, v in read.items() if r != ""})
    return {**kept, **read}


def section_changes(now, before, touched=()):
    """[(key, what it did, the heading, the rest of the phrase)] — what one commit does to each of the two sections, `now` and
    `before` read by `triage_views`:
    nothing where its text is its parent's — for a merge, ANY parent's: the text a merge carries was judged on the commit
    that made it, and only a text no parent had is the merge's own (FM-019). A root commit has no parent: it had none. A
    scaffold, where no parent had the section, is not a change (clause 3): `unwritten`. Where a view on either side cannot
    be read, nothing is read as the sections: the commit changes the files `touched` names — every TRIAGE.md and the
    configuration file it changes (`guard_touched`) — where that configuration cannot be read (`unread`)."""
    why = next((v[5] for v in (now, *before) if v[5]), "")
    if why:
        return [("unread", "changes", f"`{p}`", f"where {why}") for p in (touched or ["TRIAGE.md"])]
    tdir, home, there, secs, heads, _why, _f = now
    out = []
    for k in GUARDED:
        had = [b[3][k] for b in before] or [None]
        if secs[k] in had:
            continue
        if all(h is None for h in had) and unwritten(k, secs[k]):
            continue
        b_dir, b_home, b_there, b_secs, _h, _w, _f = before[0] if before else (tdir, home, False, {g: None for g in GUARDED}, heads, "", "")
        name = f"`{(b_secs[k] or secs[k] or '## ' + heads[k]).split(chr(10), 1)[0].rstrip()}`"
        if len(before) > 1:
            out.append((k, "brings a text under", name, f"in {home} that no parent had"))
        elif b_secs[k] is None:
            out.append((k, "writes", name, f"in {home}, where there was none"))
        elif b_dir != tdir:
            out.append((k, f"points the tracker directory elsewhere (`{b_dir}` → `{tdir}`), and the tool reads", name, "otherwise" if secs[k] is not None else "nowhere"))
        elif not there:
            out.append((k, f"deletes or moves {b_home}, and", name, "with it"))
        elif secs[k] is None:
            out.append((k, "renames or removes the heading", name, f"in {home}"))
        else:
            out.append((k, "changes the text under", name, f"in {home}"))
    return out


def unwritten(k, section):
    """A section that holds nothing but a scaffold's own words — the one `--init` writes today, the German one, the bare
    lines before 0.17.5 (`INTENT_SCAFFOLD`, `PATH_SCAFFOLD`) — recognised by their exact text, whitespace aside, as
    `owners_intent` recognises them: never by italics, bold or length. Where there was none, writing one says nothing of the
    Owner's (clause 3; the Auditor seat's AU-20: main's root commit wrote 0.1.0's bare scaffold)."""
    body = section.split("\n", 1)[1] if "\n" in section else ""
    if k == "intent":
        return owners_intent(body) == ""
    words = {" ".join(s.split()) for s in PATH_SCAFFOLD}
    return all(" ".join(line.split()) in words for line in body.splitlines() if line.strip())


def kept_changes(path, now, before):
    """[("signers", what it did, the file, "")] — what one commit does to a file the guard keeps beside the two sections, the
    signers file (AU-19): its text against its parent's, a merge's against every parent's, as `section_changes` reads them."""
    had = [b for b in before] or [None]
    if now in had:
        return []
    name = f"`{path}`"
    if len(before) > 1:
        return [("signers", "brings a text into the signers file", name, "that no parent had")]
    return [("signers", "writes the signers file" if had[0] is None else "deletes or moves the signers file" if now is None
             else "changes the signers file", name, "")]


def signers_paths(trunk):
    """The signers files the guard keeps (AU-19), from the repository's root: the one `gpg.ssh.allowedSignersFile` names,
    where it sits in a checkout of this repository, and the default branch's `<tracker dir>/allowed_signers` — where the
    signing page puts it — whether this clone names it or not. Where the default branch's configuration cannot be read, its
    tracker directory is not known and the second is not named: there, `owners_at` refuses that configuration, and the
    guard refuses every change to a file named `allowed_signers` (`guard_touched`)."""
    out = [trusted_signers()["rel"]]
    view = triage_views([trunk], modes={trunk})[trunk] if trunk else None
    if view and not view[5]:
        out.append((pathlib.PurePosixPath(view[6]) / "allowed_signers").as_posix())
    return list(dict.fromkeys(x for x in out if x))


def did_words(what):
    """What a commit did to the sections, in one phrase: `changes the text under `## The intent` and `## The current path`
    in work-tracker/TRIAGE.md` — the headings that one thing happened to, named together."""
    said = {}
    for _k, verb, name, tail in what:
        said.setdefault((verb, tail), []).append(name)
    return "; ".join(f"{verb} {' and '.join(names)} {tail}".rstrip() for (verb, tail), names in said.items())


def guard_touched(files, prefix, keys=(), unread=False, homes=()):
    """The files of `files` (paths from the repository's root) a reading of the two sections depends on: every `TRIAGE.md`,
    in any folder, the root's included, each TRIAGE.md `homes` names (`tracker_folder`'s), and the configuration file — and,
    where the default branch's configuration cannot be read (`unread`), every file named `allowed_signers` and each `keys`
    names: its tracker directory, and so its signers file, is not known there. Each compared as a file system that ignores
    case and Unicode normalization compares it (`fs_fold`), on every system."""
    base = lambda f: fs_fold(f.rsplit("/", 1)[-1])
    names = {fs_fold("TRIAGE.md"), *([fs_fold("allowed_signers")] if unread else [])}
    watched = {fs_fold(w) for w in (*homes, prefix + CONFIG_NAME, *(keys if unread else ()))}
    return sorted({f for f in files if base(f) in names or fs_fold(f) in watched})


def variant_changes(files, watched):
    """[("variant", "changes", the file, the path it is read as)] — each of `files` that a path the guard watches, other than
    itself, is as a file system that ignores case and Unicode normalization reads it (`fs_fold`): on such a file system —
    macOS's default one, Windows's — the two are one file, and it can be the very file the tool reads. Folded on every
    system."""
    out = []
    for f in sorted(files):
        other = next((w for w in watched if w != f and fs_fold(w) == fs_fold(f)), None)
        if other is not None:
            out.append(("variant", "changes", f"`{f}`", f"which a file system that ignores case or Unicode normalization reads as `{other}`"))
    return out


def tree_variants(home, paths, files):
    """[("variant", "holds", the path, its home)] — where a commit's TRIAGE.md home is not its parent's (the tracker moved, or
    `tracker_dir` respelled), each path its tree holds (`paths`, `tree_paths`), other than the home, that is the home as a
    file system that ignores case and Unicode normalization reads it — one the commit changes itself (`files`) is
    `variant_changes`'. None as `paths`: git could not list them, and the move is refused."""
    if paths is None:
        return [("variant", "moves the tracker to", f"`{home}`", "where git cannot list the files beside it")]
    return [("variant", "holds", f"`{p}`", f"which a file system that ignores case or Unicode normalization reads as `{home}`")
            for p in sorted(paths) if p != home and p not in files and fs_fold(p) == fs_fold(home)]


def guard_changes(now, before, kept, files, prefix, keys=(), unread=False, tree=None):
    """What one commit does that FM-037 judges: `section_changes` and `kept_changes` (`kept`), read under the views `now` and
    `before`, each of the files it changes (`files`) that is a watched path in another case or Unicode normalization
    (`variant_changes`), and — where its TRIAGE.md home is not a parent's — each path its tree holds that is that home so
    (`tree_variants`; `tree` lists them, once) — where a view on either side cannot be read, the files `guard_touched`
    names, refused as changes, never read under the defaults. `unread`: the default branch's configuration cannot be read —
    every file `guard_touched` names is a change, whatever the views read."""
    views = (now, *before)
    homes = [v[1] for v in views if v[1]]
    touched = guard_touched(files, prefix, keys, unread, homes)
    if any(v[5] for v in views):
        own = ([("unread", "changes", f"`{p}`", "") for p in touched] if unread else section_changes(now, before, touched)) if touched else []
    else:
        own = section_changes(now, before) + variant_changes(files, [*dict.fromkeys([*homes, prefix + CONFIG_NAME, *keys])])
        if tree is not None and (not before or any(b[1] != now[1] for b in before)):
            own += tree_variants(now[1], tree(), files)
    own += kept
    return own or ([("unread", "changes", f"`{p}`", "") for p in touched] if unread else [])


def guard_walk(*revs, keys=(), unread=False):
    """FM-037's walk of `git log <revs>` — merges INCLUDED, each read against every parent: (how many commits it read,
    [(commit, subject, TRIAGE.md's path at it, what `guard_changes` says of it)] for each that changes one of the two
    sections, or one of the files `keys` names (`signers_paths`) — or, where a view cannot be read, or the default branch's
    configuration cannot be (`unread`), a file the reading depends on (`guard_touched`). The same one `git log` names the
    files each commit changes — a merge's, those that differ from every parent — split on a mark no commit can carry."""
    mark = f"\x1f{os.urandom(8).hex()}\x1f"
    out = git_out("-c", "diff.relative=false", "-c", "log.showSignature=false", "-c", "log.showRoot=true", "log", "-z", "-c",
                  "--name-only", "--no-renames", f"--format={mark}%H %P{mark}%s{mark}", *revs) or ""
    parts, commits = out.split(mark)[1:], []
    for i in range(0, len(parts) - 2, 3):
        c, *ps = parts[i].split()
        commits.append((c, ps, parts[i + 1].strip(), [f.lstrip("\n") for f in parts[i + 2].split("\x00") if f.lstrip("\n")]))
    prefix = (git_out("rev-parse", "--show-prefix") or "").strip() if commits else ""
    revs_ = sorted({c for c, _p, _s, _f in commits} | {p for _c, ps, _s, _f in commits for p in ps})
    views = triage_views(revs_, prefix=prefix, modes={c for c, _p, _s, files in commits if prefix + CONFIG_NAME in files}) if commits else {}
    kept = cat_blobs([f"{r}:{k}" for r in revs_ for k in keys]) if commits else {}
    changed = [(c, subject, next((views[r][1] for r in (c, *ps) if views[r][1]), "TRIAGE.md"),
                guard_changes(views[c], [views[p] for p in ps], [w for k in keys for w in kept_changes(k, kept.get(f"{c}:{k}"), [kept.get(f"{p}:{k}") for p in ps])],
                              files, prefix, keys, unread, lambda c=c: tree_paths(c)))
               for c, ps, subject, files in commits]
    return len(commits), [row for row in changed if row[3]]


def owners_of(cfg):
    """`may_answer()` for a configuration read from a revision — {identity: "signed" | ""}: each seat of its `[seats]`, and
    the Owner its top-level `owner` names (`seats_of`), that holds `answer` (the built-in `owner`, or a name its `[rights]`
    gives it), or with neither its `answerers`."""
    seats, rights, out = seats_of(cfg), cfg.get("rights") if isinstance(cfg.get("rights"), dict) else {}, {}
    if seats:
        for name, value in seats.items():
            for who, mode in seat_identities(value):    # the same refusal as this checkout's configuration: `owners_at` says it
                refuse_signed_name("`owner`" if name == "owner" and cfg.get("owner") is not None else f"`[seats] {name}`", who, mode)
            words = rights.get(name, BUILTIN_RIGHTS.get(name, ()))
            if "answer" in ([words] if isinstance(words, str) else words):
                out.update(seat_identities(value))
        return {w: m for w, m in out.items() if w}
    for a in (cfg.get("answerers") or []):
        name, _, mode = str(a).strip().rpartition(" ")
        refuse_signed_name("`answerers`", name, mode)
        out[name if mode == "signed" else str(a).strip()] = "signed" if mode == "signed" else ""
    return {w: m for w, m in out.items() if w}


def owners_at(rev, refused=None):
    """The Owner as `rev`'s `shoalmark.toml` names them — the default branch's, so a branch never names its own Owner — or
    this checkout's where `rev` is None or carries no configuration — nothing at its path (`path_mode`); a submodule or a
    folder there is a configuration this tool cannot read. Where this tool refuses that configuration, nobody —
    and the refusal is appended to `refused`, so the caller says so rather than that it names no Owner (FM-024, D2), and
    refuses every change to the two sections (v0.19.1) — a configuration whose tracker directory or `[headings]` the guard
    cannot read (`guard_config`) is refused the same way."""
    if not rev:
        return may_answer()
    prefix = (git_out("rev-parse", "--show-prefix") or "").strip()
    spec, types = f"{rev}:{prefix}{CONFIG_NAME}", {}
    text = cat_blobs([spec], types=types).get(spec)
    kind = types.get(spec, "blob") if text is not None else path_mode(rev, prefix + CONFIG_NAME)
    if kind == "blob" and path_mode(rev, prefix + CONFIG_NAME) == "120000":       # a symlink: its text is no configuration
        kind = "120000"
    if not kind:                                        # nothing at that path: no configuration — the adoption, as documented
        return may_answer()
    try:
        if kind != "blob":
            raise SystemExit(config_not_file(kind))
        guard_config(text)                              # where it puts the two sections, as the guard reads them
        return owners_of(read_config(text))
    except SystemExit as e:
        if refused is not None:
            refused.append(str(e))
        return {}


def guard_verdicts(changed, owners):
    """[(commit, subject, home, what, verdict, why)] for each commit of `guard_walk` that changes a section — `verdict`:
    `signed` (the Owner's signed commit), `author` (the Owner's, where their seat asks for no signature: the author is all
    it proves), `checkout` (signed, and this clone cannot check it — `why` the cause) or `refused` (`why` the reason).
    One `git log --no-walk` reads every author and signature."""
    shas = [c for c, _s, _h, _w in changed]
    out = git_out(*signers_args(), "log", "--no-walk=unsorted", "--format=%x00%H%x01%an%x01%ae%x01%G?%x01%GS", *shas) if shas else ""
    sigs = {}
    for rec in (out or "").split("\x00")[1:]:
        c, name, email, good, signer = (rec.strip("\n").split("\x01") + [""] * 5)[:5]
        sigs[c] = (name, email, good.strip(), signer)
    verdicts = []
    for c, subject, home, what in changed:
        name, email, good, signer = sigs.get(c, ("", "", "", ""))
        identity, mode = next(((who, m) for who, m in owners.items() if who in (email, name)), (None, None))
        kind = signature_kind(c)
        if mode is None:
            verdict, why = "refused", f"its author `{email or name or 'nobody git can name'}` is not the Owner ({' · '.join(f'`{w}`' for w in owners)})"
        elif mode != "signed":
            verdict, why = "author", ""
        elif kind not in ("", "ssh"):                       # GPG, X.509: the Owner's signed line verifies by SSH only
            verdict, why = "refused", SIGN_WITH_SSH
        elif signature_gap(c):                              # before `%G?`: read against a signers file the branch wrote, it says G
            verdict, why = "checkout", signature_gap(c)
        elif good == "G" and signer.strip() == identity:    # the principal IS the Owner's configured email — never a principal that contains it, never the author
            verdict, why = "signed", ""
        elif good == "G":
            verdict, why = "refused", f"signed as `{signer}`, not as the Owner's `{identity}`"
        else:
            verdict, why = "refused", ("the Owner's email, unsigned — a git author is a string anyone can type" if good == "N"
                                       else f"the Owner's email, and its signature does not verify (`%G?` {good})")
        verdicts.append((c, subject, home, what, verdict, why))
    return verdicts


def guard_proof(owners):
    """What a refusal can say it proved: the Owner's signed commit — or, where a seat that is theirs asks for no signature, the
    author only, and how to prove the key (clause 5)."""
    return "not the Owner's signed commit" if all(m == "signed" for m in owners.values()) else GUARD_AUTHOR_ONLY


def guard_why(what):
    """Whose the thing changed is: their two sections, the keys their signature is verified against, or both."""
    keys = {k for k, *_r in what}
    return "; ".join(w for w, on in ((GUARD_WHY, bool(keys & {*GUARDED, "unread", "variant"})), (GUARD_WHY_KEYS, "signers" in keys)) if on)


def unread_why(trunk):
    """Why a change to the Owner's two sections or their signers file is refused where this tool refuses `trunk`'s configuration,
    and the way through — last, so a refusal of this kind is told by its end (`unread_refusal`)."""
    return f"{ref_name(trunk)}'s {GUARD_UNREAD}. The way through: {GUARD_UNREAD_WAY}"


def unread_lines(changed, trunk):
    """FM-037 where this tool refuses `trunk`'s configuration: each commit of `guard_walk` that changes the two sections or their
    signers file, refused in one line — whoever made it, signed or not."""
    return [f'refused: commit {c[:7]} "{first_words(subject, 60)}" {did_words(what)} — {unread_why(trunk)}' for c, subject, _home, what in changed]


def unread_refusal(line):
    """Whether a line of the guard is the refusal `unread_why` ends: no author and no signature judged, so the lines on what a
    signature proves are not said under it. Told by its end — every other line of the guard ends on fixed words of its own."""
    return line.endswith(GUARD_UNREAD_WAY)


def guard_lines(verdicts, owners):
    """The refusals of `guard_verdicts` as `--check` prints them — a checkout's own finding (signed, this clone cannot check
    it) worded as FM-034 groups it, never written into INDEX.md."""
    out = []
    for c, subject, home, what, verdict, why in verdicts:
        did = did_words(what)
        if verdict == "checkout":
            out.append(f'{home}: commit `{c[:10]}` "{first_words(subject, 60)}" {did} — it is signed, but {CHECKOUT_MARKS[0]}: {why} — see {SIGNING_PAGE}')
        elif verdict == "refused":
            out.append(f'refused: commit {c[:7]} "{first_words(subject, 60)}" {did} — {why}: {guard_proof(owners)} — {guard_why(what)}. '
                       f'The way through: {GUARD_WAY}')
    return out


def triage_pending(subject):
    """(refusals, notes) — FM-037 at commit time, in the commit-msg hook: what the commit being made does to the two
    sections, read from what it stages (the index git hands the hook, `GIT_INDEX_FILE`) against HEAD — a merge being made
    against each of its parents — and every commit a merge being made brings, walked as `--check` walks them. What the
    hook CAN prove is the author: git signs the commit after the hook has run, so the Owner's own commit passes here on their
    name and a seat's is refused before it is made. `--check` on the branch judges the signature: it is the gate, the hook
    best-effort (the 0.18.3 ruling on FM-033's hook). Where this tool refuses the default branch's configuration, who the Owner
    is is not known, and every such change is refused, whoever makes it (v0.19.1) — as is every change to a file the reading
    depends on (`guard_touched`), and so where a view of the index or a parent cannot be read. `subject` names the commit in
    what it says."""
    if vcs() != "git":
        return [], []
    git = lambda *a: subprocess.run(["git", *a], cwd=ROOT, capture_output=True, text=True, encoding="utf-8", errors="replace", env=nested_git_env())
    trunk, why = default_trunk(git), []
    owners = owners_at(trunk, why)
    if not owners and not why:
        return [], []
    heads = merge_heads()
    parents = (["HEAD"] if git("rev-parse", "--verify", "-q", "HEAD").returncode == 0 else []) + heads
    env = dict(nested_git_env(), **({"GIT_INDEX_FILE": os.environ["GIT_INDEX_FILE"]} if os.environ.get("GIT_INDEX_FILE") else {}))
    prefix = (git_out("rev-parse", "--show-prefix") or "").strip()
    staged = staged_files(parents, env)
    views = triage_views(["", *parents], env, prefix, {""} if prefix + CONFIG_NAME in staged else ())     # "" — the index: what this commit carries
    keys = signers_paths(trunk)
    kept = cat_blobs([f"{r}:{k}" for r in ["", *parents] for k in keys], env)
    what = guard_changes(views[""], [views[p] for p in parents],
                         [w for k in keys for w in kept_changes(k, kept.get(f":{k}"), [kept.get(f"{p}:{k}") for p in parents])],
                         staged, prefix, keys, not owners, lambda: tree_paths("", env))
    brought = guard_walk(*heads, "--not", *parents[:1], *([trunk] if trunk else []), keys=keys, unread=not owners)[1] if heads else []
    refused = guard_lines(guard_verdicts(brought, owners), owners) if owners else unread_lines(brought, trunk)
    notes = []
    if what:
        name, email = pending_author()
        mode = next((m for who, m in owners.items() if who in (email, name)), None)
        this = f'this commit "{first_words(subject, 60)}"' if subject else "this commit"
        if not owners:
            refused.append(f'refused: {this} {did_words(what)} — {unread_why(trunk)}')
        elif mode is None:
            refused.append(f'refused: {this} {did_words(what)} — its author `{email or name or "nobody git can name"}` is not the Owner '
                           f'({" · ".join(f"`{w}`" for w in owners)}): {guard_proof(owners)} — {guard_why(what)}. The way through: {GUARD_WAY}')
        else:
            notes.append(f"note: {this} {did_words(what)}, under the Owner's name — "
                         + ("its signature is judged on the commit, by `--check` on the branch" if mode == "signed" else GUARD_AUTHOR_ONLY))
    return refused, notes


def staged_files(parents, env):
    """The files the commit being made changes, from the repository's root: what its index (`env`) holds that differs from
    every parent — a merge being made, from each of its parents; a first commit, all it holds. One `git diff` a parent."""
    run = lambda *a: subprocess.run(["git", "-c", "diff.relative=false", *a], cwd=ROOT, capture_output=True, text=True, encoding="utf-8", errors="replace", env=env)
    every_file = lambda: run("ls-files", "-z", "--full-name", "--", ":/")
    sets = [run("diff", "--cached", "--name-only", "-z", "--no-renames", p) for p in parents] or [every_file()]
    names = [set(r.stdout.split("\x00")) - {""} if r.returncode == 0 else None for r in sets]
    if any(n is None for n in names):                          # git could not say: every file it holds counts — and where it cannot list them, a TRIAGE.md
        r = every_file()
        return set(r.stdout.split("\x00")) - {""} if r.returncode == 0 else {"TRIAGE.md"}
    return set.intersection(*names)


def commit_msg_hook(message_file):
    """`--commit-msg <file>`, the commit-msg hook: FM-033's judgement of the commit being made (`commit_msg_check`), then
    FM-037's (`triage_pending`) — each best-effort, `--check` on the branch the gate."""
    code = commit_msg_check(message_file)
    try:
        text = pathlib.Path(message_file).read_text(encoding="utf-8", errors="replace")
    except OSError:
        return code
    refused, notes = triage_pending(message_subject(text) or literal_subject(text))
    for line in refused + notes:
        print(f"  {line}", file=sys.stderr)
    if notes or not all(unread_refusal(line) for line in refused):          # what the hook proves, where it judged an author
        print("  the hook proves the author only: git signs a commit after its hooks have run — `--check` on the branch is the gate, "
              "and it judges the signature", file=sys.stderr)
        print(f"  the limit: {GUARD_LIMIT}", file=sys.stderr)
    return EXIT_LINT if refused else code


def guard_footer(problems):
    """The refusal's last line, under every line the run printed (clause 6): what a signature proves — the key, not the hand.
    Said once, where the guard said anything."""
    return [f"  the limit: {GUARD_LIMIT}"] if any(p_ in problems and not unread_refusal(p_) for p_ in (_GUARD or ([], ""))[0]) else []


def tip_variants(trunk, tip=None):
    """FM-037 on the branch tip as a merge would bring it: where its TRIAGE.md home is not the default branch's — the tracker
    moved on either side — each path the tip's tree holds (`tree_paths`, one listing), other than a home, that is either
    home as a file system that ignores case and Unicode normalization reads it (`fs_fold`). Refused whoever made it, in
    one line each; nothing listed where the two homes are one, or one cannot be read (the walk judges that). `tip`: the
    commit to judge — `--queue`'s pull request head — else HEAD."""
    tip = tip or (git_out("rev-parse", "--verify", "-q", "HEAD") or "").strip()
    if not tip or not trunk:
        return []
    views = triage_views([trunk, tip], modes={trunk})
    homes = list(dict.fromkeys(v[1] for v in (views[trunk], views[tip])))
    if len(homes) < 2 or not all(homes):
        return []
    held = tree_paths(tip)
    if held is None:
        return [f"refused: the branch tip `{tip[:7]}` moves the tracker from {ref_name(trunk)}'s `{homes[0]}` to `{homes[1]}`, and git cannot list the files beside it"]
    return [f"refused: the branch tip `{tip[:7]}` holds `{p}` which a file system that ignores case or Unicode normalization reads as `{h}` — "
            f"{ref_name(trunk)}'s TRIAGE.md is `{homes[0]}`, the tip's `{homes[1]}`, and a merge brings it: carry the work onto a branch without it"
            for p in sorted(held) for h in homes if p not in homes and fs_fold(p) == fs_fold(h)]


def triage_guard():
    """(refusals, the one line `--check` says) — FM-037 over the branch's own commits, `HEAD` less `origin`'s default branch,
    merges walked and judged by the text they bring — where this tool refuses the default branch's configuration, each commit
    that changes them, their signers file, a TRIAGE.md or the configuration file refused, signed or not (the Owner's ruling of
    2026-10-03, v0.19.1). Read once per run; the pre-commit run judges nothing here (the commit-msg hook judges the commit
    being made)."""
    global _GUARD
    if COMMITTING:
        return [], ""
    if _GUARD is not None:
        return _GUARD
    if vcs() != "git":
        _GUARD = ([], GUARD_SVN if vcs() == "svn" else "the Owner's two sections: this is no git repository — nothing is judged")
        return _GUARD
    git = lambda *a: subprocess.run(["git", *a], cwd=ROOT, capture_output=True, text=True, encoding="utf-8", errors="replace", env=nested_git_env())
    trunk, branch = default_trunk(git), built_on()
    if not trunk:
        _GUARD = ([], "the Owner's two sections: " + ("the default branch cannot be told — nothing is judged until it can" if _TRUNK_UNTOLD
                                                      else "no `origin` default branch to measure from — nothing is judged"))
        return _GUARD
    why = []
    owners = owners_at(trunk, why)
    if not owners and why:                                   # refused here: every change to the two sections, their signers file, a TRIAGE.md or the configuration
        n, changed = guard_walk("HEAD", "^" + trunk, keys=signers_paths(trunk), unread=True)
        refused = unread_lines(changed, trunk) + tip_variants(trunk)
        _GUARD = (refused, f"the Owner's two sections: guarded — {ref_name(trunk)}'s configuration cannot be read here, so every change to them or their signers file is refused: {why[0]} — "
                           f"{n} commit(s) on {f'`{branch}`' if branch else 'a detached HEAD'} since {ref_name(trunk)}, "
                           + (f"{len(changed)} change them or their signers file, {len(refused)} refused" if changed or refused else "none changes them or their signers file"))
        return _GUARD
    if not owners:
        _GUARD = ([], f"the Owner's two sections: not guarded — {ref_name(trunk)}'s configuration names no Owner: name them (`owner = \"<email> signed\"`, before any table)")
        return _GUARD
    n, changed = guard_walk("HEAD", "^" + trunk, keys=signers_paths(trunk))
    verdicts = guard_verdicts(changed, owners)
    refused = guard_lines(verdicts, owners) + tip_variants(trunk)
    proof = "" if all(m == "signed" for m in owners.values()) else f" ({GUARD_AUTHOR_ONLY})"
    _GUARD = (refused, f"the Owner's two sections: guarded{proof} — {n} commit(s) on {f'`{branch}`' if branch else 'a detached HEAD'} since {ref_name(trunk)}, "
                       + (f"{len(changed)} change them or their signers file, {len(refused)} refused" if refused
                          else f"{len(changed)} change them or their signers file, each their own commit" if changed else "none changes them or their signers file"))
    return _GUARD


class History:
    """FM-040 — the history reader: a repository's commits with their parents and trailers, read by ONE `git log` and answered
    in memory. It answers what `verdict_reports` used to ask git one subprocess at a time (about four per verdict, 33 ms
    each): is X an ancestor of Y (`git merge-base --is-ancestor`), the ancestry path from a tip to the trunk
    (`git rev-list --ancestry-path <tip>..<trunk>`), the trunk's first-parent line (`git rev-list --first-parent`), the
    commits `<tip> ^<stop> --no-merges` names, and a commit's trailers. A commit is immutable, so the answers cannot go
    stale within a run. Built by `read_history`; every sha here is a full one."""

    def __init__(self, log=""):
        self.parents, self.blocks = {}, {}       # sha -> its parents, in order · sha -> its TRAILERS block
        self._ancestors, self._children, self._line = {}, None, {}
        for rec in log.split("\x02"):
            sha, _, rest = rec.strip("\n").partition("\x01")
            parents, _, block = rest.partition("\x01")
            if sha:
                self.parents[sha], self.blocks[sha] = tuple(parents.split()), block

    def trailers(self, sha, name):
        """Every value of the trailer `name` on one commit, in order — `trailers_of`, without the subprocess."""
        return trailer_values(self.blocks.get(sha, ""), name)

    def ancestors(self, sha):
        """Every commit reachable from `sha`, itself included."""
        got = self._ancestors.get(sha)
        if got is None:
            got, todo = {sha}, [sha]
            while todo:
                for parent in self.parents.get(todo.pop(), ()):
                    if parent not in got:
                        got.add(parent)
                        todo.append(parent)
            self._ancestors[sha] = got
        return got

    def is_ancestor(self, sha, of):
        """`git merge-base --is-ancestor <sha> <of>` — true also where the two are one commit."""
        return sha in self.ancestors(of)

    def first_parents(self, tip):
        """`git rev-list --first-parent <tip>`: the tip, its first parent, and so on down — newest first."""
        line = self._line.get(tip)
        if line is None:
            line, at = [], tip
            while at:
                line.append(at)
                at = (self.parents.get(at) or (None,))[0]
            self._line[tip] = line
        return line

    def ancestry_path(self, tip, trunk):
        """`git rev-list --ancestry-path <tip>..<trunk>`: the commits the trunk reaches and the tip does not, that stand
        above the tip — its descendants below the trunk."""
        if self._children is None:
            self._children = {}
            for sha, parents in self.parents.items():
                for parent in parents:
                    self._children.setdefault(parent, []).append(sha)
        reach, found, todo = self.ancestors(trunk), set(), [tip]
        while todo:
            for child in self._children.get(todo.pop(), ()):
                if child in reach and child not in found:
                    found.add(child)
                    todo.append(child)
        return found - self.ancestors(tip)

    def commits(self, tip, stop=None):
        """`git rev-list <tip> ^<stop> --no-merges`: what the tip reaches and `stop` does not, less the merges (a commit
        with more than one parent). With no `stop`, everything the tip reaches."""
        gone = self.ancestors(stop) if stop else ()
        out, seen, todo = set(), {tip}, [tip]
        while todo:
            sha = todo.pop()
            if sha in gone:
                continue
            parents = self.parents.get(sha, ())
            if len(parents) < 2:
                out.add(sha)
            for parent in parents:
                if parent not in seen:
                    seen.add(parent)
                    todo.append(parent)
        return out

    def reviewed_commits(self, tip, trunk):
        """The reviewed branch's OWN commits (R2) — the range as R2 defined it — `git rev-list <tip> ^<trunk> --no-merges`, a set of
        shas (until FM-040 `reviewed_range` built the arguments of a `git log` for it). A tip the trunk has since merged is measured against the
        trunk as it stood before the merge that brought it (`^M^1`), so the report does not change when the branch lands. None:
        the tip is on the trunk's own first-parent line — not a branch verdict. `trunk` None: no trunk to measure from."""
        if not trunk:
            return self.commits(tip)
        if not self.is_ancestor(tip, trunk):
            return self.commits(tip, trunk)
        line = self.first_parents(trunk)
        if tip in set(line):
            return None
        after = self.ancestry_path(tip, trunk)          # the trunk's first-parent commits that contain the tip are a prefix
        landed = list(itertools.takewhile(lambda c: c in after, line))       # of its line; the oldest brought it
        if not landed:
            return self.commits(tip, trunk)
        first = self.parents.get(landed[-1])
        return self.commits(tip, first[0]) if first else set()      # `^<root>^1` is no revision: git reads nothing


def resolve_commits(names):
    """{name: the full sha of the commit it names, or ""} — `git rev-parse --verify --quiet <name>^{commit}` for each name, in one
    `git cat-file --batch-check`. A name git could not take on a line of its own (a newline in it) is asked one call at a time."""
    names = list(dict.fromkeys(names))
    got = {n: "" for n in names}
    lines = [n for n in names if n and "\n" not in n and "\r" not in n]
    if lines:
        r = subprocess.run(["git", "cat-file", "--batch-check"], cwd=ROOT, input="".join(f"{n}^{{commit}}\n" for n in lines), capture_output=True,
                           text=True, encoding="utf-8", errors="replace", env=nested_git_env())
        answers = r.stdout.split("\n") if r.returncode == 0 else []
        if len(answers) >= len(lines):
            for name, answer in zip(lines, answers):
                hit = re.fullmatch(r"([0-9a-f]{40}|[0-9a-f]{64}) commit \d+", answer)
                got[name] = hit[1] if hit else ""
        else:
            lines = []
    for name in names:
        if name and name not in lines:
            got[name] = (git_out("rev-parse", "--verify", "--quiet", f"{name}^{{commit}}") or "").strip()
    return got


def read_history(*revs):
    """The History of everything `revs` reach — one `git log`, full shas. Nothing reads no history: `git log` with no revision
    would read HEAD."""
    revs = [r for r in revs if r]
    return History(git_out("log", f"--format=%H%x01%P%x01{TRAILERS}%x02", *revs) or "" if revs else "")


def trunk_ref():
    """The trunk a verdict's branch is measured against — a report's, never a refusal's: the default branch as `--check` reads it
    (`default_trunk`, asking no server: origin's answer where this run has it), else the local `main`, else `master` — each by its
    full ref (v0.19.1)."""
    held = default_trunk(lambda *a: subprocess.run(["git", *a], cwd=ROOT, capture_output=True, text=True, encoding="utf-8", errors="replace", env=nested_git_env()), ask=False)
    return held or next((ref for ref in ("refs/heads/main", "refs/heads/master") if git_out("rev-parse", "--verify", "--quiet", ref + "^{commit}")), None)


def verdict_reports(days=None):
    """S6 — each verdict commit (it carries `Reviewed: <sha>`) of the last `days` days on HEAD, as (verdict, reviewed,
    its session, the reviewed range's sessions, the word): *independent* when the verdict's session root is none of the
    range's, *same session* when it is one of them, *untraced* when either side names no session, *on trunk* when the tip
    is on the trunk's first-parent line (not a branch verdict). The range is the branch's own commits, less other
    verdicts (`History.reviewed_commits`, read from one `git log`, FM-040). A report, never a refusal (slice 2 refuses, after a week of counts)."""
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
    shas = resolve_commits([reviewed for _v, reviewed, _s in found] + ([trunk] if trunk else []))       # FM-040: the window's history,
    history = read_history(*sorted({s for s in shas.values() if s}))       # read once — every question below is answered from it
    trunk_sha = shas[trunk] if trunk else ""
    out = []
    for verdict, reviewed, sid in found:
        tip = shas[reviewed]
        own = history.reviewed_commits(tip, trunk_sha or None) if tip else set()          # None: the tip is on the trunk's line
        ranged = set()
        for sha in own or ():
            if not history.trailers(sha, "Reviewed"):
                ranged |= set(history.trailers(sha, "Session"))
        roots = {s.split("/")[0] for s in ranged}
        word = ("on trunk" if own is None else "untraced" if not sid or not ranged
                else "same session" if sid.split("/")[0] in roots else "independent")
        out.append((verdict, reviewed, sid, sorted(ranged), word))
    return out


def sessions_report():
    """What `--check` says of sessions, never a refusal: a registry file left from before 0.18.0, and this week's
    verdicts by independence."""
    lines = [f"warning: {sessions_file().relative_to(ROOT).as_posix()} is a report since 0.18.0 — delete it; --sessions prints it"] if sessions_file().exists() else []
    if vcs() != "git":
        return lines
    reps = verdict_reports()
    if reps:
        count = collections.Counter(w for *_x, w in reps)
        lines.append(f"reviews this week · {len(reps)} verdict(s) · independent {count['independent']} · same session {count['same session']}"
                     + (f" · untraced {count['untraced']}" if count["untraced"] else "") + (f" · on trunk {count['on trunk']}" if count["on trunk"] else ""))
        lines += [f"  verdict {v[:10]} on {r[:10]}: " + ("on trunk — not a branch verdict" if w == "on trunk" else
                  f"{w} — its session {s or '(none)'}; the branch's {', '.join(rs) or '(none)'}") for v, r, s, rs, w in reps]
    return lines


def collapse_runs(numbers):
    """`[1, 2, 3, 4, 5, 7]` → `1–5, 7`: a run of three or more is `a–b`, a run of two is both, a lone number is itself."""
    nums, out, i = sorted(set(numbers)), [], 0
    while i < len(nums):
        j = i
        while j + 1 < len(nums) and nums[j + 1] == nums[j] + 1:
            j += 1
        out += [f"{nums[i]}–{nums[j]}"] if j - i >= 2 else [str(n) for n in nums[i:j + 1]]
        i = j + 1
    return ", ".join(out)


def session_groups(since=SESSION_RECENT):
    """THE STRIP, grouped by parent (FM-024): one entry per parent session with a commit in the last `since` seconds — its
    own or a sub-session's. `id` is the parent; `seat` and `worktree` its own commits' (`—` for a parent that made none:
    it is derived from its sub-sessions' ids, `<parent>/<seat>-<n>`); `runs` the sub-sessions' seats with their numbers,
    runs collapsed (`implementer 1–6`, `reviewer 1–5, 7`); `subs` how many sub-sessions are in the window; `members` the
    parent first where it has commits, then each sub-session in the window, as (id, worktree, model, effort) — `—` where
    no commit carried one. Read from the trailers alone, never from a transcript."""
    cutoff = datetime.datetime.now().timestamp() - since
    groups = {}
    for r in session_rows():
        parent, _, hand = r["id"].partition("/")
        g = groups.setdefault(parent, dict(own=None, subs=[], first=r["first"][0]))
        g["first"] = min(g["first"], r["first"][0])
        if hand:
            g["subs"].append(r)
        else:
            g["own"] = r
    show = lambda v: v or "—"
    out = []
    for parent, g in sorted(groups.items(), key=lambda kv: kv[1]["first"]):
        subs, own = [r for r in g["subs"] if r["last"][0] >= cutoff], g["own"]
        if not subs and not (own and own["last"][0] >= cutoff):
            continue
        numbers = {}                                    # seat -> its sub-sessions' numbers, in the order the seats first appear
        for r in subs:
            m = re.fullmatch(r"(.+)-(\d+)", r["id"].partition("/")[2])
            numbers.setdefault(m[1] if m else r["id"].partition("/")[2], []).extend([int(m[2])] if m else [])
        out.append(dict(id=parent, seat=", ".join(own["seats"]) if own and own["seats"] else "—", subs=len(subs),
                        worktree=", ".join(own["worktrees"]) if own and own["worktrees"] else "—",
                        runs=[f"{name} {collapse_runs(nums)}".rstrip() for name, nums in numbers.items()],
                        members=[(r["id"], show(", ".join(r["worktrees"])), show(r["model"]), show(r["effort"])) for r in ([own] if own else []) + subs]))
    return out


def group_line(g):
    """One parent's line, the board's and the digest's alike: `<parent> <seat> (<worktree>) · implementer 1–6 · reviewer 1–5, 7`."""
    return f"{g['id']} {g['seat']} ({g['worktree']})" + "".join(f" · {run}" for run in g["runs"])


def group_counts(groups):
    """(parents, all) — the header's two numbers: the parents with a commit in the last day, and them with their sub-sessions."""
    return len(groups), len(groups) + sum(g["subs"] for g in groups)


def board_sessions():
    """The report as the board shows it — the parents with a commit in the last day (each: id, seat, worktree, its
    sub-sessions' runs, and every member's worktree, model and effort for the expand), the header's two counts, and this
    week's verdicts as [independent, same session, untraced, on trunk] — or None where there is neither, or no git."""
    if vcs() != "git":
        return None
    groups = session_groups()
    reps = verdict_reports()
    if not groups and not reps:
        return None
    count = collections.Counter(w for *_x, w in reps)
    parents, everyone = group_counts(groups)
    return {"groups": [[g["id"], g["seat"], g["worktree"], g["runs"], [list(m) for m in g["members"]]] for g in groups],
            "parents": parents, "all": everyone,
            "reviews": [count["independent"], count["same session"], count["untraced"], count["on trunk"]] if reps else None}


def sessions_digest():
    """The digest's lines, grouped as the board's strip is: a header with the two counts, then one line per parent with a
    commit in the last day — or nothing where there is none. It reads git for the sessions alone, never the verdicts."""
    groups = session_groups() if vcs() == "git" else []
    if not groups:
        return ""
    parents, everyone = group_counts(groups)
    return "\n".join([f"SESSIONS IN THE LAST DAY · {parents} ({everyone} with their sub-sessions)"] + [f"  {group_line(g)}" for g in groups])


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
    `## Asks` (date · question · answer · answered-by, and the answer's relation to the proposal, newest last), the ask and answer lines leave the front matter,
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
    # the relation goes with the record (FM-029): the proposal and the options leave with the ask, and a record without
    # it could never say again whether the answer was the proposal
    block = (f'**{t.get("answered") or datetime.date.today().isoformat()}** · {t["ask"]}\n'
             + (f'**answered** — {t["answer"]} · {t["answered_by"]}\n**relation** — {relation_text(answer_relation(t))}\n' + signed_line(path) if t.get("answer")
                else "**withdrawn** — no answer was given\n"))
    body = append_record(body, ASKS_HEAD_RE, HEAD["asks"], block)
    put(path, "\n".join(kept) + body)
    print(f'{tid}: the exchange is in the body under `## {HEAD["asks"]}`, the ask is cleared, `next: {move}`.\n'
          f'  commit {path.relative_to(ROOT).as_posix()} — the gate refuses an answer removed without its record')
    return EXIT_OK


def signed_line(path):
    """FM-029, the Auditor seat's AU-29 — the record names the commit that signed the answer: `**signed** — <sha> · <G|N|U>`,
    the commit that wrote the `answer:` line and what git says of its signature here (`%G?`: G good, U good from a key
    not trusted here, N none; B, E, X, Y, R as git has them). The tier is not printed yet (FM-007). Under Subversion the
    server authenticated the committer and there is no signature to name: no line. An answer not yet committed:
    `not committed · N`."""
    if vcs() != "git":
        return ""
    commit = line_author(path, "answer:")[3]
    if not commit:
        return "**signed** — not committed · N\n"
    said = (git_out("log", "-1", "--format=%G?", commit) or "").strip() or "N"
    return f"**signed** — {commit[:7]} · {said}\n"


def append_record(body, head_re, word, block):
    """The body with `block` at the end of the section `head_re` finds — newest last — or, where there is none, a new
    `## <word>` above the ship log, at the end without one. `## Asks` (`--clear-ask`) and `## Acts` (`--done`, `--due`)."""
    at = head_re.search(body)
    if at:
        rest = re.search(r"^#{2,3}\s+", body[at.end():], re.M)
        cut = at.end() + (rest.start() if rest else len(body) - at.end())
        return body[:cut].rstrip("\n") + "\n\n" + block + "\n" + body[cut:]
    log = re.search(r"^#{2,3}\s+(%s)\s*$" % re.escape(HEAD["log"]), body, re.I | re.M)
    section = f'## {word}\n\n{block}\n'
    return (body[: log.start()] + section + body[log.start():]) if log else body.rstrip("\n") + f"\n\n{section}"


def act_record(lines, fields, block):
    """A tracker's lines with front-matter `fields` set (None drops one) and `block` recorded under `## Acts`."""
    text = "\n".join(lines)
    for key, value in fields.items():
        text = set_front(text, key, value)
    _fm, body = parse_frontmatter(text)
    return (text[: len(text) - len(body)] + append_record(body, ACTS_HEAD_RE, HEAD["acts"], block)).split("\n")


# a review file's verdict, stated: `Verdict` before the word (`**Verdict: READY.**`, `## Verdict — READY WITH FINDINGS`,
# `**Verdict on 67532e3:** …`), or the word in bold opening its line (`**NOT READY — one P2.**`); prose that mentions a
# verdict in passing (`came back NOT READY at 14:23`) does not state one, nor does the shape quoted in code — the README's
# act row writes `Verdict: READY` to say what a review looks like, and the README is no review
VERDICT_LINE_RE = re.compile(r"(?<![`\w])Verdict\b[^A-Za-z]*(?:on\s+`?[0-9a-f]{7,40}`?\s*[:—-]?\s*)?" + VERDICT_WORD_RE.pattern
                             + r"|^(?:#{1,6}\s+)?(?:\*\*|__)" + VERDICT_WORD_RE.pattern, re.M)
_FILE_SHA_RE = re.compile(r"^\s*(?:[-*]\s+)?(?:\*\*)?Reviewed:(?:\*\*)?\s*`?([0-9a-f]{7,40})\b", re.M)
_FILE_SESSION_RE = re.compile(r"^\s*(?:[-*]\s+)?(?:\*\*)?Session:(?:\*\*)?\s*`?(" + SESSION_ID_RE.pattern + r")(?![\w/-])", re.M)
# a line anchor after a path, as a review or a forge writes one — `file.md:12`, `file.md:12-20`, `file.md#L1`, `#L1-L9`
_LINE_ANCHOR_RE = re.compile(r"(?:#[\w.-]*|:\d+(?:[-:]\d+)?)$")


def result_facts(where):
    """FM-030, the Owner's word of 2026-09-27 13:42:40: *the person gives the path; the record gathers the facts.*
    What the repository says of `where` — read, never guessed — as one clause for the record beside it, or "":
    - a file in the repository (from its root, or from the tracker directory, as evidence paths are written — never one
      outside it; a trailing line anchor, `file.md:12` or `file.md#L1-L9`, is not part of its name — `where` is recorded
      as given, anchor and all): the commit that added it under that name and the commit's date (`git log --no-renames
      --diff-filter=A`), or *not committed*;
    - where the file states a verdict (`VERDICT_LINE_RE`) it is a review, and its LAST such line is the verdict — a file
      that carries several passes is superseded pass by pass, and the last stated verdict is the newest verdict commit's
      in every review file of this repository (the pass's R1 on 9c96f5b; 77 of 77 at d18c9ba). Its `Reviewed:` sha and
      `Session:` are that pass's own lines — the nearest after it, or the file's only ones — else the trailers of the
      newest commit that touched the file; where that commit is not the one that added it, *last pass in* names it;
    - one word that names no file in the repository: *not in the repository* — recorded as given, never refused;
    - words, a link, a folder: nothing beside it."""
    w = (where or "").strip()
    if not w:
        return ""
    top, found, bare = ROOT.resolve(), None, _LINE_ANCHOR_RE.sub("", w)
    for name in dict.fromkeys(n for n in (w, bare) if n):     # as given first: a name may carry a `#` or a `:` of its own
        for base in (ROOT, TRACKER_DIR):
            try:
                p = (base / name).resolve()
                p.relative_to(top)
            except (ValueError, OSError, RuntimeError):
                continue
            if p.exists():
                found = p
                break
        if found is not None:
            break
    if found is None:
        return "" if re.search(r"\s", w) or "://" in w else "not in the repository"
    if not found.is_file():
        return ""
    rel, facts = found.relative_to(top).as_posix(), []
    if rel not in (w, w.lstrip("./"), bare, bare.lstrip("./")):
        facts.append(rel)
    try:
        with found.open(encoding="utf-8", errors="replace") as f:
            text = f.read(1 << 20)
    except OSError:
        text = ""
    added = newest = ("", "", "")
    if vcs() == "git":
        log = lambda *a: tuple(((git_out("log", "-1", "--no-renames", *a, f"--format=%h%x00%cI%x00{TRAILERS}", "--", rel) or "")
                                .strip("\n").split("\x00") + ["", ""])[:3])
        added, newest = log("--diff-filter=A"), log()
    stated = list(VERDICT_LINE_RE.finditer(text))
    if stated:
        last = stated[-1]
        facts.append("verdict " + next(g for g in last.groups() if g))
        after = text.find("\n", last.end()) + 1 or len(text)     # the lines after the last verdict's own line

        def own(rx):
            """The pass's own line: the nearest after its verdict, else the file's only value; None where neither says."""
            near = rx.search(text, after)
            if near:
                return near.group(1)
            every = {m.group(1) for m in rx.finditer(text)}
            return every.pop() if len(every) == 1 else None
        reviewed = own(_FILE_SHA_RE) or (trailer_values(newest[2], "Reviewed") or [""])[0]
        session = own(_FILE_SESSION_RE) or (trailer_values(newest[2], "Session") or [""])[0]
        facts += ([f"reviewed {reviewed[:7]}"] if re.fullmatch(r"[0-9a-f]{7,40}", reviewed or "") else []) + ([f"session {session}"] if session else [])
    facts.append(f"added in {added[0]} {added[1]}" if added[0] else "not committed")
    if stated and newest[0] and newest[0] != added[0]:
        facts.append(f"last pass in {newest[0]} {newest[1]}")        # the verdict's own time, where a later pass wrote it
    return ", ".join(facts)


def done_cmd(words, trackers):
    """`--done <id> "<where the result is>"` — the Owner's act is done: `done:` gets the time and where its result is, the
    act leaves their list, and its record goes under `## Acts`. Their own change, made as `--answer` makes their answer: on
    `answer/<id>`, signed where their seat is `signed`, pushed (`owner_change`). The seats that hold `answer` may run it."""
    tid, where = words[0].upper(), " ".join(" ".join(words[1:]).split()).replace('"', "'")
    t = next((x for x in trackers if x["id"] == tid), None)
    act = act_of(t) if t else None
    if not act and t and vcs() == "git":                    # R3: their answer — the act — may be on `answer/<id>`, not merged yet
        git = lambda *a: subprocess.run(["git", *a], cwd=ROOT, capture_output=True, text=True, encoding="utf-8", errors="replace", env=nested_git_env())
        branch, trunk, rel = f"answer/{tid.lower()}", default_trunk(git), (TRACKER_DIR / t["file"]).relative_to(ROOT).as_posix()
        if git("rev-parse", "--verify", "-q", f"refs/heads/{branch}").returncode == 0 and (not trunk or git("merge-base", "--is-ancestor", f"refs/heads/{branch}", trunk).returncode != 0):
            there = git("show", f"refs/heads/{branch}:{rel}")
            if there.returncode == 0 and act_of(extract(ROOT / rel, there.stdout)):
                print(f"--done: {tid}'s act is on `{branch}`, not merged into `{ref_name(trunk) or 'origin'}` — " + unmerged_advice(
                    git, branch, trunk, rel, tid, dict(flag="--done", again=f"{CMD} --done {tid} {shlex.quote(where)}"), git_user(), pending_author()[1]), file=sys.stderr)
                return EXIT_LINT
    if not act:
        print(f"--done: {tid} owes the Owner no act — an accepted action ask is one, and so is a `due:`; "
              + (f"`done:` is written already ({t.get('done')})" if t and t.get("done") else "there is nothing to record"), file=sys.stderr)
        return EXIT_LINT
    if not where:
        print("--done: say where the result is — a path in the repository, or a pointer to it; the record keeps it", file=sys.stderr)
        return EXIT_LINT
    if vcs() != "git":
        print("--done: this is a git command; under Subversion, write `done:` and its record under `## Acts`, and `svn commit` — the server signs for you", file=sys.stderr)
        return EXIT_LINT
    now, today = datetime.datetime.now().astimezone().replace(microsecond=0).isoformat(), datetime.date.today().isoformat()
    what, _answer, _answered, due, _window, _asked = act
    # an action's yes left `next: owner` — the promise was their hands (ANSWER_MOVE); the act done, the seat's move follows.
    # ONLY there: a `due:` beside a question they have not answered keeps `next: owner` — the question is still theirs, and
    # moving it would take it off their list unanswered (the pass's R1 on 52cfcc7)
    fields = {"done": f'"{now} · {where}"', **({"next": "build"} if t.get("next") == "owner" and act[1] else {})}
    facts = result_facts(where)                             # the person gives the path; the record gathers the facts
    return owner_change(tid, t, dict(
        flag="--done", verb="recording", noun="record", right="the result of the Owner's act is an `answer` change", check=lambda: "",
        write=lambda lines, me, branch: (act_record(lines, fields,
                                                    f"**{today}** · done — {where}" + (f" ({facts})" if facts else "") + f" · {what}"
                                                    + (f" · due {due}" if due else "") + f" · {me}"), ""),
        subject=f"{tid}: done — {where[:50]}", kept=("your record", f"done — {where}"), again=f'{CMD} --done {tid} "{where}"',
        said=lambda branch, pushed: f"{tid} done: {where}\n  signed, on `{branch}`{pushed}\n  the act has left your list; its record is under `## {HEAD['acts']}`"
                                     + (f" — with what the repository says of it: {facts}" if facts else "")
                                     + ("\n  next: build — the seat's move follows" if "next" in fields else "")))


def due_cmd(words, trackers):
    """`--due <id> <time>` — the Owner's act moves: `due:` gets the new time, the old one goes into the record under
    `## Acts`. On a tracker whose act was done, it is a new act: `done:` leaves the front matter, its record stays. Their
    own change, made as `--answer` makes their answer (`owner_change`); the seats that hold `answer` may run it."""
    tid, when = words[0].upper(), words[1].strip() if len(words) > 1 else ""
    t = next((x for x in trackers if x["id"] == tid), None)
    if not t:
        print(f"--due: no tracker {tid}", file=sys.stderr)
        return EXIT_LINT
    if t["status"] not in OPEN_STATUSES:
        print(f"--due: {tid} is {t['status']} — closed work owes no act", file=sys.stderr)
        return EXIT_LINT
    if not parse_due(when):
        print(f"--due: {when!r} is not a time with its zone — `2026-09-26T07:30:00+02:00`, or `2026-09-26T05:30Z` for UTC", file=sys.stderr)
        return EXIT_LINT
    if vcs() != "git":
        print("--due: this is a git command; under Subversion, write `due:` and its record under `## Acts`, and `svn commit` — the server signs for you", file=sys.stderr)
        return EXIT_LINT
    today, act = datetime.date.today().isoformat(), act_of(t)
    what, old = (act[0] if act else t.get("title") or tid), ("" if t.get("done") else t.get("due", ""))
    # a new act on one that was done: `done:` leaves the front matter, so the record keeps it — its time, where its result
    # is, and what the repository says of that (`result_facts`)
    was_done, _, was_where = (t.get("done") or "").partition(" · ")
    before = (f", a new act — the one before was done {was_done} · {was_where}" + (lambda f: f" ({f})" if f else "")(result_facts(was_where))) if t.get("done") else ""
    return owner_change(tid, t, dict(
        flag="--due", verb="rescheduling", noun="record", right="the time of the Owner's act is an `answer` change", check=lambda: "",
        write=lambda lines, me, branch: (act_record(lines, {"due": when, "done": None},
                                                    f"**{today}** · " + (f"rescheduled — was due {old}, now due {when}" if old else f"scheduled — due {when}{before}")
                                                    + f" · {what} · {me}"), ""),
        subject=f"{tid}: due {when}", kept=("the new time", when), again=f"{CMD} --due {tid} {when}",
        said=lambda branch, pushed: f"{tid} due: {when}\n  signed, on `{branch}`{pushed}\n  " + (f"was due {old} — the old time is in the record under `## {HEAD['acts']}`" if old else f"its record is under `## {HEAD['acts']}`")))


def revoke_cmd(words, trackers):
    """`--revoke <id> "<why>"` (FM-030, their signed answer 920970b7: *revoke* in the place of the buttons) — the Owner takes
    back what they last did on a tracker, as a new signed commit, never an overwrite. An act done: `done:` leaves the front
    matter, the revocation is recorded under `## Acts` beside what it revokes, and where their accepted action answer had
    `--done` hand the move to the seat, `next: owner` is theirs again — the act is owed. Else their answer, taken back as
    `--answer <id> revoke` takes it: `revoked - <why>`, the answer it replaces into the ship log with its commit. Where
    `answer/<id>` is not merged — here or on `origin` — the act is on its way there: the tracker is read at its tip and
    the revocation commits on top of it, on that branch (one branch per exchange); else `answer/<id>` is cut as for any
    act of theirs. Made as `--answer` makes their answer (`owner_change`); the seats that hold `answer` may run it."""
    tid, why = words[0].upper(), " ".join(" ".join(words[1:]).split()).replace('"', "'")
    t = next((x for x in trackers if x["id"] == tid), None)
    if not t:
        print(f"--revoke: no tracker {tid}", file=sys.stderr)
        return EXIT_LINT
    if not why:
        print("--revoke: a revocation carries its reason — the record keeps it beside what it revokes", file=sys.stderr)
        return EXIT_LINT
    if vcs() != "git":
        print("--revoke: this is a git command; under Subversion, write the revocation and `svn commit` — the server signs for you", file=sys.stderr)
        return EXIT_LINT
    git = lambda *a: subprocess.run(["git", *a], cwd=ROOT, capture_output=True, text=True, encoding="utf-8", errors="replace", env=nested_git_env())
    branch, trunk, rel = f"answer/{tid.lower()}", default_trunk(git), (TRACKER_DIR / t["file"]).relative_to(ROOT).as_posix()
    tip = next((ref for ref in (f"refs/heads/{branch}", f"refs/remotes/origin/{branch}") if git("rev-parse", "--verify", "-q", ref).returncode == 0), None)
    onto = tip if tip and git("branch", "--show-current").stdout.strip() != branch and (not trunk or git("merge-base", "--is-ancestor", tip, trunk).returncode != 0) else None
    if onto:
        there = git("show", f"{onto}:{rel}")
        t = extract(ROOT / rel, there.stdout) if there.returncode == 0 else t
    if not t.get("done"):
        if not t.get("answer"):
            print(f"--revoke: {tid} carries neither `done:` nor `answer:`" + (f" on `{branch}`" if onto else "") + " — there is nothing of yours to revoke", file=sys.stderr)
            return EXIT_LINT
        return answer_cmd([tid, "revoke", why], [t if x["id"] == tid else x for x in trackers], onto=onto, flag="--revoke", verb="revoking")
    today, (was, _, where) = datetime.date.today().isoformat(), t["done"].partition(" · ")
    act = act_of({**t, "done": ""})
    what = act[0] if act else t.get("title") or tid
    # `--done` handed the move to the seat where their accepted action answer had left it theirs (`next: owner`): taken back, it is theirs again
    fields = {"done": None, **({"next": "owner"} if act and act[1] and t.get("next") == "build" else {})}
    return owner_change(tid, t, dict(
        flag="--revoke", verb="revoking", noun="revocation", right="taking back the Owner's act is an `answer` change", check=lambda: "", onto=bool(onto),
        write=lambda lines, me, branch_: (act_record(lines, fields, f"**{today}** · done revoked — {why} · it was done {was} · {where} · {what} · {me}"), ""),
        subject=REVOKE_DONE_SUBJECT.format(tid) + why[:50], kept=("your revocation", why), again=f'{CMD} --revoke {tid} "{why}"',
        said=lambda branch_, pushed: f"{tid} done revoked: {why}\n  signed, on `{branch_}`{pushed}\n  the act is owed again — it is back on your list; "
                                     f"the revocation is under `## {HEAD['acts']}`" + ("\n  next: owner — the act is yours again" if "next" in fields else "")))


def acted_on(trackers):
    """What a seat has acted on since the Owner's last sitting: a tracker whose exchange has moved into the body and
    whose `ask:` line is gone — named by the commit that removed it, so the Owner can read what their answer became.

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
    if vcs() == "svn" and any(mode == "signed" for ids in SEATS.values() for _who, mode in ids):
        problems.append(f'{CONFIG_NAME}: {", ".join("`owner`" if at_top(s) else f"`[seats] {s}`" for s in sorted(s for s in SEATS if any(mode == "signed" for _who, mode in SEATS[s])))} asks for a signature, and '
                        f'Subversion has none to give: its server authenticates the commit. Name the SVN account alone')
    # Any repository carrying `answerers` hears this — NOT only one that also has `[seats]`. Guarding it on both was
    # backwards: it spoke to the repositories part-way through the migration and stayed silent for the ones wholly on
    # the old key, which is the entire population the deprecation is for (FM-010).
    if ANSWERERS and SEATS:
        # with `[seats]` the key is NOT READ for answers (`may_answer`, from 0.17.1): telling such a repository it "still
        # works" is what let a signature it asked for go unenforced without a word (FM-015)
        print(f'  note: {CONFIG_NAME}: `answerers` is the old name for the `answer` right, and here it is not read for answers — '
              f'{"`owner` and `[seats]` decide" if CONFIG.get("owner") is not None else "`[seats]` decides"} who may answer and whether the answer is signed. It can be removed', file=sys.stderr)
    elif ANSWERERS:
        # The schedule is ANCHORED to 0.17.3, never phrased against "this release": this note prints unchanged in every
        # later release, and a floating "the clock starts here" would restart the countdown each time it was read.
        print(f'  note: {CONFIG_NAME}: `answerers` is the old name for the `answer` right and still works — name the Owner at the top instead '
              f'(`owner = "<email> signed"`, before any table), and give any other name that answers `answer` in `[rights]`. '
              f'It is removed no sooner than the release after 0.17.3: before 0.17.3 this note never reached a repository '
              f'without `[seats]`, so the clock starts at 0.17.3', file=sys.stderr)
    problems += answerers_problems()
    problems += line_break_problems(trackers)        # a tracker whose file name git would read as two names (v0.19.1)
    problems += rights_problems(trackers)
    problems += ship_problems(trackers)              # FM-005: no move to Shipped without a commit behind it, every author
    problems += session_problems()                   # FM-024, FM-032: a seat's commit names a session of its own seat
    problems += walk_problems()                      # v0.19.1: a walk of those commits git could not make is refused, never read as nothing
    problems += build_problems()                     # FM-033: no build commit before a judgement, where it is on
    problems += triage_guard()[0]                    # FM-037: only the Owner changes their intent and their current path
    by_ask = asks_by_key(trackers)
    for t in trackers:
        problems += t.get("key_problems") or []         # each key a right is judged on is read from one line, in lower case (v0.19.1)
        # WHAT AN ASK MUST BE — the same rules the Owner's queue reads, refused here first (FM-008)
        problems += [f'{t["id"]}: {why}' for why in ask_problems(t, by_ask)]
        problems += record_problems(t) if committing else []
        if t.get("answer"):
            # the pre-mortem's rule: an answer counts only from the account it is filed from. Who that may be comes
            # from `may_answer()` — the seats that hold `answer`, or `answerers` where there are no seats
            allowed = may_answer()
            if not allowed:
                problems.append(f'{t["id"]}: an answer, but ' + (f'no seat in `[seats]` holds the `answer` right — name the Owner (`owner = "<email> signed"`, before any table), or give one seat `answer` in `[rights]`'
                                                                 if SEATS else f'`answerers` in {CONFIG_NAME} names nobody — say who may answer')
                                + ", then the commit's author is checked against it")
            elif not SEATS and t.get("answered_by") not in allowed:
                problems.append(f'{t["id"]}: `answered-by: {t.get("answered_by")}` is not in `answerers` ({", ".join(allowed)}) — an answer counts only from an account that may give one')
            else:
                try:
                    who, email, how, commit = line_author(TRACKER_DIR / t["file"], "answer:")
                except SvnUnreadable as e:
                    problems += blame_refusal(t, e)
                    who, email, how, commit = None, None, "unreadable", ""
                seat = seat_of(who, email) if SEATS else None
                if how == "unreadable":
                    pass                                 # refused above: who wrote the answer cannot be read
                elif how == "uncommitted" and committing:
                    print(f'  {t["id"]}: the answer is being committed now — its author and signature are verified on the commit, by the next run', file=sys.stderr)
                elif how == "uncommitted" and SEATS and vcs() == "svn" and svn_tracker_new(t):
                    pass                                 # a tracker Subversion holds no revision of: the rights refuse it, in one line (`rights_problems`)
                elif how == "uncommitted":
                    problems.append(f'{t["id"]}: the answer is not committed yet — commit it under your own name; the commit is the record, the file is the label')
                elif how in ("unattributed", "merged"):
                    problems.append(unattributed(t, "answer:", how))
                elif SEATS and not holds(seat, "answer"):
                    problems.append(f'{t["id"]}: ' + no_seat(who, email, "answer", "an answer counts only from a seat that may give one"))
                elif who != t.get("answered_by"):
                    problems.append(f'{t["id"]}: `answered-by: {t.get("answered_by")}` but the {how} author of the answer is `{who}` — an answer is filed from the account that gives it')
                elif how == "git" and (seat_mode(seat, who, email) if SEATS else allowed[who]) == "signed":
                    # ONE signature test for the whole gate — `verified_as`: a good signature under a trusted key, and
                    # the identity that key is trusted FOR being the one claimed. A seat's `signed` entry asks the same
                    claimed = signed_identity(seat, who, email) if SEATS else who
                    if not verified_as(commit, claimed):
                        problems.append(f'{t["id"]}: the answer\'s commit `{commit[:10]}` does not verify as `{claimed}` — '
                                        + unverified(commit, f'{(("`owner`" if at_top(seat) else "`[seats]`") + " asks this seat") if SEATS else "`answerers` asks"} for a signed answer, and a git author is only a string: '
                                                             f'sign it (`git commit -S`), or it does not count'))
                elif how == "git":
                    print(f'  note: {t["id"]}: the answer\'s author `{who}` is a git author string, not a verified identity — add `signed` to '
                          f'{("`owner`" if at_top(seat) else "that seat in `[seats]`") if SEATS else "that entry in `answerers`"} to require a signature', file=sys.stderr)
        # `ask-proposal:` is the RECOMMENDED option, and the board offers it first: with options named, it must be one
        # of them, or the Owner is shown a recommendation they cannot pick
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


def board_link():
    """The one line that says where the board was written: `board: file:///…/index.html` — the written file as a URI, right on Windows, macOS and Linux."""
    return f"board: {HTML_OUT.resolve().as_uri()}"


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
    add("--html-only", action="store_true",
        help="the board's read-only run: write only the git-ignored board — index.html and view/ in the tracker folder — and print its link. It starts no deriver and no program but read-only git, "
             "reads only regular files inside the repository (no symlink is followed), refuses a tracker folder that resolves outside it, and writes neither through a symlink nor over a file git "
             "tracks; its board carries no derived columns. It stands alone, with --root. The checkout and merge hooks run it from the copy of the tool kept in the git directory")
    add("--install-hook", action="store_true", help="wire the gate into the version control system found: plain git hooks — pre-commit, prepare-commit-msg, commit-msg, and post-checkout, post-merge and post-rewrite, which refresh the board — every one running a COPY of the tool this keeps in the git directory (shoalmark-trusted/, shared by every worktree), which runs nothing a branch brings; a commit's hook fails closed, and no hook runs the deriver — explicit runs do. A hooks folder inside the working tree is refused. Only this writes or replaces the copy: from a pinned copy that passes its PIN, else from the working tree's tool, and it names the commit and branch — run it on your default branch, and again after upgrading — or on Subversion the TortoiseSVN hook properties and svn:ignore; never overwrites a hook that is not its own")
    add("--standup", nargs="?", const="", metavar="FILE.ics", help="the Owner's one sitting: the agenda by kind — rulings, their hands, what evidence could settle, buttons — and inside a kind what frees the most first. With FILE.ics: the recurring calendar invite (weekdays at `standup` in the configuration)")
    add("--answer", nargs="+", metavar="WORD", help="the Owner's one command: `--answer <id> accept|reject [\"text\"]` — cuts answer/<id> from this branch, writes the three lines, commits signed, pushes, "
             "naming each step as it starts, and goes back to the branch it started on. An answer/<id> left from an earlier answer is cut fresh when it is merged into "
             "origin's default branch, and refused, naming `git branch -D`, when it is not. An answer given already: `--answer <id> revoke \"<reason>\"`, or "
             "`--answer <id> accept|reject \"<option>\" --supersede` — the old one moves into the ship log. A failure after it wrote anything undoes it all and "
             "prints the answer and the command to give it again. The word it writes stays the button's; every reading names the answer's relation to the proposal")
    add("--supersede", action="store_true", help="with --answer, on a tracker they have answered already: the new answer replaces the old one, which moves into the ship log "
                                                 "with the commit that wrote it — `--answer <id> accept|reject \"<option>\" --supersede`; `--answer <id> revoke \"<reason>\"` takes an answer back the same way")
    add("--invite", metavar="ID", help="an act owed to the Owner as a calendar file (FM-030): `<tracker dir>/evidence/<id>/<id>-act.ics` — its `due:` in "
                                       "UTC, a DURATION of its `window:`, a reminder 30 minutes before; RFC 5545. Import it; after a `--due`, write it again")
    add("--notify", action="store_true", help="one system notification per act owed to the Owner that falls due within 30 minutes, is overdue or was "
                                              "missed (FM-030) — once per act per state, remembered outside the repository: $XDG_STATE_HOME/shoalmark/"
                                              "notified.json, else ~/.local/state/shoalmark on macOS and Linux, %%LOCALAPPDATA%%/shoalmark on Windows. "
                                              "Schedule it yourself: the README has a launchd and a cron line")
    add("--done", nargs=2, metavar=("ID", "WHERE"), help="the Owner's act is done (FM-030): `--done <id> \"<where the result is>\"` writes `done:` — the time and "
                                                        "where its result is — and its record under `## Acts`; the act leaves their list. Made as --answer makes their answer: on "
                                                        "`answer/<id>`, signed where their `owner` is `signed`, pushed. The board's *done* button copies it")
    add("--due", nargs=2, metavar=("ID", "TIME"), help="the Owner's act moves (FM-030): `--due <id> 2026-09-26T07:30:00+02:00` writes the new `due:` and records the "
                                                       "old one under `## Acts`; on an act that was done, a new act. Made as --answer makes their answer. The board's "
                                                       "*reschedule* button copies it")
    add("--revoke", nargs=2, metavar=("ID", "WHY"), help="the Owner takes back what they last did on a tracker (FM-030): `--revoke <id> \"<why>\"` — an act done: "
                                                          "`done:` leaves the front matter, the revocation is recorded under `## Acts`, the act is owed again; else their "
                                                          "answer, as `--answer <id> revoke`. Where `answer/<id>` is not merged — on its way — it commits on top of it there. "
                                                          "Made as --answer makes their answer. The board's *revoke* button copies it")
    add("--answered", action="store_true", help="what the Owner answered and no seat has acted on yet — the seat's side of the exchange — each answer with its relation to the proposal: "
                                               "accepted the proposal · chose option N · accepted with a change · rejected · revoked · relation not computable; and what WAS acted on since their last sitting, by commit, with the relation its record carries — "
                                               "for a record written before 0.18.1, the one the commit that wrote its answer gives")
    add("--clear-ask", nargs="+", metavar="WORD",
        help="`--clear-ask <id> <next move>` — the answer has been acted on: moves the exchange into the body under `## Asks` (date · question · answer · answered-by · the answer's relation to the proposal), clears the ask and answer lines and sets the next move — the `ask` right's move under [seats]. The gate refuses an answer removed without its record")
    add("--owner", action="store_true", help="the digest: what needs the Owner — how many, how old, what each holds up, each as the question it is. What a session's last message leads with; "
                                            "where `gh` reads the forge, it ends with the queue of pull requests (--queue)")
    add("--queue", action="store_true", help="the open pull requests, read from GitHub with `gh` (origin fetched once), ONE action each — wait: from a fork, read it yourself (first) · merge · closes with PR N · "
                                            "close: carried into PR N · wait: conflict in … · wait: TRIAGE.md changed unsigned (FM-037) · wait: no verdict on … · wait: NOT READY (…); an answer/* pull request reads "
                                            "merge: your answer · wait: not an answerer (<author>) · wait: a seat's commit on your answer branch (<sha>, <author>) · wait: an unverified commit in your name on your answer branch (<sha>) · wait: the base <base> is not fetched here — … · wait: unsigned answer · wait: answer not verified here — … — in the order to take them; then each branch on "
                                            "origin no pull request carries, as `branch <name> @ <sha>  wait: no pull request — …`, and a count; then the pull requests "
                                            "merged or closed in the last 24 hours, with their times. "
                                            f"Read-only; exit {EXIT_DRIFT} where the forge cannot be read")
    add("--session", nargs="+", metavar="WORD",
        help="a seat's session (FM-024): the worktree carries its id as `git config --worktree seat.session <id>`, beside the seat's `user.email` — the harness's session id, "
             "its first eight hex characters; a sub-agent's is its parent's and its hand, `<parent>/<seat>-<n>`. `--session new` prints an id no commit carries, for a session "
             "with no parent and a harness with no id. `open` and `close` are gone since 0.18.0: the registry is a report, `--sessions`")
    add("--ratio", action="store_true", help="the records-to-product ratio (FM-032): per Europe/Berlin day of the merge, the lines added and deleted in records "
                                            "(`[ratio] records` in the configuration) and in product (every other path), counted apart, for the merge commits on "
                                            "the default branch's first-parent line — then the rolling seven-day sums. The rule is "
                                            "work-tracker/evidence/FM-032/records-to-product-ratio.md. Read-only; exit 2 without a `[ratio]` section")
    add("--since", metavar="YYYY-MM-DD", help="with --ratio: the first day of the window (default: six days before --until)")
    add("--until", metavar="YYYY-MM-DD", help="with --ratio: the last day of the window (default: today, Europe/Berlin)")
    add("--sessions", action="store_true", help="the registry of seat sessions, generated from the `Session:` and `Worktree:` trailers of this checkout's history "
                                               "(FM-032): one row per id — its seat, first and last commit, how many, its worktree. Markdown on stdout; nothing is written")
    add("--session-check", action="store_true", help="the session rule alone, on the commit being made — what the pre-commit hook runs on EVERY commit, "
                                                     "a tracker staged or not: a seat's commit carries a `Session:` of its own seat. Reads git, never the trackers")
    add("--commit-msg", nargs=1, metavar="FILE", help="what a commit-msg hook calls with its message file: where `judged_before_build` is on, the commit being made is "
                                                      "judged with its subject (FM-033) — the ids it names, else its branch `<kind>/<NNN>-…`, judged and In Progress at HEAD — "
                                                      "and refused before it is made, with the line `--check` prints of it; and, where the default branch's configuration names the "
                                                      "Owner, a commit that changes their intent or current path in TRIAGE.md is refused before it is made unless they are its author "
                                                      "(FM-037 — the hook sees the author; `--check` judges the signature)")
    add("--session-trailer", nargs="+", metavar="FILE", help="what a prepare-commit-msg hook calls with its message file: appends `Session: <seat.session>` "
                                                            "and `Worktree: <the checkout's directory>` to a seat's commit — and `Model:` and `Effort:` where `seat.harness` "
                                                            "names a log that carries them (`--whoami`) — nothing without `seat.session`; "
                                                            "a trailer the message carries already is left alone")
    add("--whoami", action="store_true", help="who this session is — the line a seat's report opens with (AGENTS.md): "
                                              "`From: <session> <seat> (<worktree>) · <model> · <effort>` — the session from `seat.session`, the seat from `[seats]`, the "
                                              "worktree's folder, and the model and effort from the harness's own log, found by the id in `seat.harness` "
                                              "(`—` where there is none); a message's target is the same identity after `To:`. "
                                              "Reads top-level fields of the log, never its messages; exit 2 where two logs carry the id")
    add("--tsvn-hook", nargs="+", metavar="start|pre", help=argparse.SUPPRESS)      # what the TortoiseSVN properties call; TortoiseSVN appends its own arguments
    add("--derive-flag", action="append", default=[], metavar="NAME",
        help="hand NAME to the repository's deriver as one of its `flags` — the ONLY way a deriver is told anything beyond the trackers: "
             "it must never read the environment, which a git hook inherits from whatever shell ran the commit")
    add("--brand", nargs="?", const="", metavar="DIR",
        help="why does my board look like this: which places gave it its theme, logo, wordmark and labels. With DIR: write a commented starter there")
    add("--from", dest="theme", metavar="THEME",
        help=f"with --brand DIR: the starter is a theme the tool ships in brand/themes/ — {' or '.join(shipped_themes()) or 'none in this copy'}: its theme.css and "
             "its fonts copied into DIR, never over a file there, and yours to change. No setting chooses a theme: a board wears the one in its places")
    add("--init", action="store_true", help="scaffold shoalmark.toml, the tracker directory and TRIAGE.md; never overwrites")
    add("--key", metavar="KEY", help="with --init: the project key every id carries — MSR gives MSR-001; default: the directory name's first word, cut to five characters")
    add("--vendor", metavar="DIR", help="copy this tool into DIR — the themes it ships in brand/themes/ with it — with a PIN file of sha256 hashes: a pinned, self-contained copy. Only from a release: "
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


DERIVE_TIMEOUT = 60           # seconds — a deriver runs on every commit; one that hangs must not hang the gate
# NO DERIVER IN HOOKS (the Owner's ruling filed in FM-006, *No deriver in hooks*): a hook's run of the copy starts no deriver — a deriver is the tree's own
# program. Where the repository has one, the commit's hook leaves INDEX.md and the derived files as they are staged, never rewritten without the derived
# columns, and says so in this line; explicit runs run the deriver, and CI's `--check` holds what it derives.
DERIVER_HOOK_LINE = "shoalmark: the deriver runs only in explicit runs — INDEX.md and the files it derives are left as staged: run `{cmd}` before committing; CI's `--check` holds them"
DERIVER_LEFT = False          # a hook's run of the copy found a deriver it does not start (`run_deriver`)


def no_derived(trackers):
    """What a run knows before any deriver has spoken — and what `--html-only` knows, which never runs one: no derived column, file, note or key."""
    global DERIVED_COLUMNS, DERIVED_FILES, DERIVED_NOTES, FRONT_MATTER, INDEX_COLUMNS, BOARD_COLUMNS
    DERIVED_COLUMNS, DERIVED_FILES, DERIVED_NOTES, FRONT_MATTER, INDEX_COLUMNS, BOARD_COLUMNS = [], {}, [], front_matter_schema(), [], []
    for t in trackers:
        t["x"], t["xd"], t["x_needs"] = {}, {}, []


def run_deriver(trackers, mode="write", flags=()):
    """B′ — the one seam. If `<tracker dir>/derive` exists and is executable it runs first, on every explicit run but `--html-only`'s: nothing
    derived is stored, so nothing derived can be stale. A hook's run of the copy starts none (`DERIVER_LEFT`). stdin: every tracker's id, status, file and front matter.
    stdout: `{"<ID>": {"Column": "value"}, "_keys": {key: {shape, required, who, says}}, "_problems": ["…"]}`. Each
    value key becomes a column in INDEX.md and on the board, and a view on the board. `_files: {path: text}` are other
    generated files: the deriver stays free of side effects — the core writes them, reports them under --print-written
    and counts them as drift under --check. A non-zero exit REFUSES the run before anything is written.
    Returns (exit code or None, problems)."""
    global DERIVED_COLUMNS, DERIVED_FILES, DERIVED_NOTES, FRONT_MATTER, INDEX_COLUMNS, BOARD_COLUMNS, DERIVER_LEFT
    no_derived(trackers)
    exe = TRACKER_DIR / "derive"
    if not HOOK_RUN and os.path.lexists(exe) and not real_inside(exe):     # a deriver that is a symlink starts nothing; a folder of that name is no deriver
        rel = os.path.relpath(exe, ROOT).replace(os.sep, "/") if in_tree(exe) else str(exe)
        print(f"shoalmark: {rel} is a symlink, or reached through one — the tool runs a deriver only as a regular file inside the repository, following no "
              "symlink: nothing is run and nothing is written; put the deriver itself there", file=sys.stderr)
        raise SystemExit(EXIT_LINT)
    if not (exe.is_file() and (os.name == "nt" or os.access(exe, os.X_OK))):
        return None, []
    if HOOK_RUN:                                            # a hook starts no deriver: the run leaves what it derives as staged (`main`)
        DERIVER_LEFT = True
        return None, []
    # `mode` — write · check · read.
    # `flags` — what was typed as --derive-flag on THIS invocation. Both travel on stdin, never in the environment:
    # a hook inherits the environment of whatever shell ran `git commit`, and a stray export would reach every run.
    ask = json.dumps({"root": str(ROOT), "mode": mode, "flags": sorted(set(flags)), "trackers": [{"id": t["id"], "status": t["status"], "file": t["file"], "fm": t.get("fm", {})} for t in trackers]})
    try:
        # Windows has no executable bit and reads no `#!` line: there a deriver is run by this interpreter
        run = subprocess.run(([sys.executable] if os.name == "nt" else []) + [str(exe)], input=ask, capture_output=True, text=True, encoding="utf-8",
                             cwd=ROOT, env=deriver_env(), timeout=DERIVE_TIMEOUT)
    except subprocess.TimeoutExpired:
        return EXIT_LINT, [f"{exe.relative_to(ROOT).as_posix()} did not answer within {DERIVE_TIMEOUT} s — a deriver runs on every commit; make it fast, or make it fail"]
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
        path = pathlib.Path(os.path.abspath(ROOT / rel)) if SAFE_WRITES else (ROOT / rel).resolve()      # a hook's run of the copy judges the path as written: `write_problem`
        if ROOT not in path.parents:
            return EXIT_LINT, [f"{exe.relative_to(ROOT).as_posix()}: `_files` names {rel} — outside the repository"]
        DERIVED_FILES[path] = str(text)
    return None, [str(p) for p in said.get("_problems") or []]


def load_trackers():
    if not SAFE_READS:                                      # the tracker folder, read and written, judged in every run as the board's refresh judges it
        refused = tracker_folder_problem("nothing is written, and the commit is refused" if HOOK_RUN else "nothing is read or written")
        if refused:
            print(refused, file=sys.stderr)
            raise SystemExit(EXIT_LINT)
    return mark_raised(mark_blocked([extract(p) for p in sorted(TRACKER_DIR.glob("*.md")) if KIND_RE.match(p.name) and board_isfile(p)]))      # the reading rule


TOOL_FILES = ("shoalmark.py", "vendor/marked-18.0.13.umd.js", "VERSION", "NOTICE", "LICENSE-APACHE", "LICENSE-MIT", "CHANGELOG.md", "README.md")   # the README is written for the agent that uses the copy


def pin_problems():
    """A vendored copy carries a PIN — `sha256  path` per file. A copy that was edited in place is refused by the
    gate: fix it upstream and vendor again, so two repositories never run two tools under one name. The hooks' copy judges the
    repository's own tool (`tool_here`), not itself."""
    tool = tool_here()
    if tool is None:
        return []
    pin = tool / "PIN"
    here = str(tool.relative_to(ROOT).as_posix()) if ROOT in tool.parents else str(tool)
    pin_text = board_text(pin)                              # the reading rule: the tool in the tree is a file of the tree too
    if pin_text is None:
        # the tool sitting INSIDE the repository it tracks, and not at its root, is a vendored copy — and a vendored
        # copy without its PIN has had its integrity check switched off, silently
        return [f"{here}/PIN is missing — a vendored shoalmark carries its PIN; vendor again with --vendor"] if ROOT in tool.parents else []
    out = []
    for line in pin_text.splitlines():
        if line.startswith("#"):                            # the manifest: where the copy came from (FM-011)
            continue
        want, _, rel = line.partition("  ")
        if rel and not _norm(tool / rel).startswith(_norm(tool).rstrip(os.sep) + os.sep):     # RV-2316: a name outside the copy is refused, and never read
            out.append(f"{here}/PIN names {rel}, outside the copy — a PIN names only the copy's own files; vendor again with --vendor")
            continue
        if rel and not board_isfile(tool / rel):            # the working tree lacks it — the checkout's finding (FM-034)
            out.append(f"{here}/{rel}: the PIN names it, and {CHECKOUT_MARKS[1]} — restore it from git, or run --vendor again")
        elif rel and digest(tool / rel) != want:
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
    if ROOT not in HERE.parents or not board_isfile(pin):  # the reading rule: the running copy's PIN and VERSION are files of the tree, as in `pin_problems`
        return []
    pinned = (board_text(HERE / "VERSION") or "").strip()
    m, wrong = pin_manifest(board_text(pin) or "", pinned)
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
    copied = [rel for rel in TOOL_FILES + tuple(f"brand/{n}" for n in BRAND_FILES) + theme_files() if (HERE / rel).is_file()]   # the themes it ships travel, pinned (FM-002)
    named = pathlib.Path(dest).absolute()
    dest = pathlib.Path(os.path.realpath(named))            # a destination a person names: resolved once, where it is named
    for rel in copied + ["PIN"]:                            # the write rule for every file it writes — as the path is named, and under the folder it resolves to —
        write_rule(named / rel)                             # before anything is read or written
        write_rule(dest / rel)
    had = (board_text(dest / "VERSION") or "").strip()     # the reading rule
    # the file a PIN line names is read only where the copy would overwrite it — one of `copied` — and under the reading rule
    edited = [l.partition("  ")[2] for l in (board_text(dest / "PIN") or "").splitlines()
              if not l.startswith("#") and l.partition("  ")[2] in copied and board_isfile(dest / l.partition("  ")[2])
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
    for rel in copied:
        src = HERE / rel
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
# …and under the path heading: its note, English and German, and the first bare line (AU-20; `unwritten`)
PATH_SCAFFOLD = ("*The Owner's. A pass judges every tier against it; only the Owner changes it.*",
                 "*Gehört dem Owner. Eine Sichtung misst jede Stufe daran; nur der Owner ändert ihn.*", "1.")
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
7. **What you need from the Owner is an `ask:`** — ONE sentence they can answer, with `ask-kind:` (ruling · action ·
   determination · ceremony), `ask-since:` and `next: owner`. Write it before their standup; never bury it in the body.
   They have office hours, you have a budget: **end a session's last message with `{cmd} --owner`.**
8. **`{dir}/TRIAGE.md` is the Owner's**: the intent and the current path. Nobody else edits those two sections.
   `INDEX.md` is generated — never hand-edit it. A story stays open while a chapter is.
9. **A seat's report opens with its identity as the tool prints it:** `From: <session> <seat> (<worktree>)` —
   `{cmd} --whoami` prints it, with the model and effort the harness's log names, never the seat's own
   word for them. A message a person carries between sessions names its target with `To:` and the same identity.
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
# THE HOOKS RUN THE COPY (a private security report): every hook `--install-hook` writes runs the copy of the tool kept in the common git directory — shared by
# every worktree, outside every working tree, written only by `--install-hook` — against the worktree it runs in, and never the tool a branch brings. The commit's
# hooks fail closed: no copy, a refusal or the copy's bound, and the commit is refused with one line. The checkout and merge hooks never block: they run the copy's
# read-only `--html-only` and always exit 0, with one line where the refresh failed. A person, an agent and CI run the repository's own tool, as ever.
COPY_DIR = "shoalmark-trusted"
COPY_AT = '"$(git rev-parse --git-common-dir)/' + COPY_DIR + '/shoalmark.py" --root "$(git rev-parse --show-toplevel)"'      # the copy, against this worktree — after the interpreter and `-I`
COPY_RUN = COPY_AT + " --html-only"
_COPY_FIND = 'root=$(git rev-parse --show-toplevel 2>/dev/null)\ncopy="$(git rev-parse --git-common-dir 2>/dev/null)/' + COPY_DIR + '/shoalmark.py"\n'
_COPY_SAYS = ("# It runs the copy of the tool kept in the git directory, which only `--install-hook` writes — never the tool a branch brings; the commit is refused\n"
              "# with one line where the copy is not there, refuses it, or does not finish within its bound.\n")
_COPY_GONE = ('if [ -z "$root" ] || [ ! -f "$copy" ]; then\n  echo "shoalmark: the commit is refused — the hooks\' copy of the tool is not in the git directory: run --install-hook" >&2\n'
              '  exit 1\nfi\n')
HOOKS = {
    "pre-commit": "#!/bin/sh\n{mark} — regenerate and stage INDEX.md when a tracker changed; a violation refuses the commit.\n" + _COPY_SAYS + _COPY_FIND + _COPY_GONE
                  + '{py} -I "$copy" --root "$root" --session-check || exit $?\n'
                  "if git -c core.quotePath=false diff --cached --name-only | grep -q -E '^\"?({dir}/.*\\.md|{config}|{tool}/)'; then\n"
                  '  written=$({py} -I "$copy" --root "$root" --print-written) || exit $?\n'
                  "  [ -z \"$written\" ] || printf '%s\\n' \"$written\" | git add --pathspec-from-file=-\nfi\n",
    "prepare-commit-msg": "#!/bin/sh\n{mark} — a seat's commit names its session: `Session: <seat.session>` (FM-024).\n" + _COPY_SAYS + _COPY_FIND + _COPY_GONE
                          + 'exec {py} -I "$copy" --root "$root" --session-trailer "$1" "$2"\n',
    "commit-msg": "#!/bin/sh\n{mark} — no build commit before a judgement: judged with its subject, before it is made (FM-033).\n" + _COPY_SAYS + _COPY_FIND + _COPY_GONE
                  + 'exec {py} -I "$copy" --root "$root" --commit-msg "$1"\n',
}


HOOK_LINES = {"pre-commit": "--print-written", "prepare-commit-msg": '--session-trailer "$1" "$2"', "commit-msg": '--commit-msg "$1"',
              "post-checkout": "--html-only", "post-merge": "--html-only", "post-rewrite": "--html-only"}     # what a hook that is not ours runs, after the interpreter, `-I` and the copy (`COPY_AT`)
COPY_HOOKS = {
    name: "#!/bin/sh\n{mark} — after a " + when + ": refresh the git-ignored board, from the copy of the tool kept in the git directory (`--install-hook` writes it). It reads the tree\n"
          "# and writes the board, and runs nothing a branch brings; it never blocks a " + when + " — it exits 0, with one line where the refresh failed.\n"
          + _COPY_FIND +
          'if [ -z "$root" ] || [ ! -f "$copy" ]; then\n  echo "shoalmark: the board is not refreshed — the hooks\' copy of the tool is not in the git directory: run --install-hook"\n  exit 0\nfi\n'
          'out=$({py} -I "$copy" --root "$root" --html-only 2>&1)\ncode=$?\n'
          'if [ "$code" -eq 0 ]; then\n  printf \'%s\\n\' "$out"\nelse\n  echo "shoalmark: the board is not refreshed (exit $code): $(printf \'%s\' "$out" | tail -n 1)"\nfi\nexit 0\n'
    for name, when in (("post-checkout", "checkout"), ("post-merge", "merge"), ("post-rewrite", "rebase or an amend"))
}       # `post-rewrite`: a rebase — `git pull --rebase` with local commits among them — runs `post-checkout` before it replays them, and no other refresh after
TSVN_HOOKS = {"tsvn:startcommithook": "start", "tsvn:precommithook": "pre"}


def svn_ignore_board():
    """Subversion ignores by a property on the directory, and only a versioned directory can carry one: the tracker
    directory is scheduled for addition if it is not yet (nothing is committed), so the FIRST `svn add` of its
    contents already leaves the board out."""
    svn = lambda *a: subprocess.run(["svn", *a], capture_output=True, text=True, encoding="utf-8", errors="replace", cwd=ROOT)
    rel = TRACKER_DIR.relative_to(ROOT).as_posix()
    refused = tracker_folder_problem("no folder is made there, and the board is not ignored")      # the tracker folder, judged before it is made
    if refused:
        print(refused, file=sys.stderr)
        raise SystemExit(EXIT_LINT)
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
          f"`{CMD} --check` after the commit is what judges it.")
    return code


def copy_files():
    """What the hooks' copy of the tool holds, relative to the tool: the tool, the vendored `marked`, the VERSION, and the themes it ships — all it needs to render the board."""
    return ("shoalmark.py", MARKED.relative_to(HERE).as_posix(), "VERSION") + theme_files()


def default_branch():
    """The repository's default branch as this clone last fetched it (`origin/HEAD`, else `origin/main`, else `origin/master`), read-only and
    asking no server — or None where it cannot be told."""
    git = lambda *a: subprocess.run(["git", *a], cwd=ROOT, capture_output=True, text=True, encoding="utf-8", errors="replace", env=nested_git_env())
    trunk = default_trunk(git, ask=False)
    return ref_name(trunk).split("/", 1)[1] if trunk else None


def install_copy():
    """Write — or replace — the hooks' copy of the tool in the common git directory, `shoalmark-trusted/`: (an exit code, the lines to say). Only `--install-hook` writes it,
    and only from this copy of the tool where it is a pinned one whose files pass their checksum (`pin_problems`, and each file's own hash, read once and written as read);
    where there is no pin — the tool runs from the repository's root, or from outside it — from the working tree's tool, and the first line says so. It also says which
    commit and branch it was taken from, and warns, without refusing, where that is not the default branch: the PIN it was checked against comes from the same tree, so a
    copy installed from another branch carries that branch's tool. Beside it, `COPY` records the command it was run with, for the copy's messages."""
    out = subprocess.run(["git", "-C", str(ROOT), "rev-parse", "--git-common-dir"], capture_output=True, text=True, encoding="utf-8", errors="replace", env=nested_git_env())
    if out.returncode:
        return EXIT_LINT, [f"--install-hook: {ROOT} has no git directory to keep the hooks' copy in"]
    target = (ROOT / out.stdout.strip()).resolve() / COPY_DIR
    pin, lines = HERE / "PIN", []
    problems = pin_problems()
    if problems:
        return EXIT_LINT, [f"--install-hook: the hooks' copy of the tool is not written — {problems[0]}", "  vendor the tool again (--vendor), then run --install-hook; no hook is written"]
    pins = {rel: want for want, _, rel in (l.partition("  ") for l in pin.read_text(encoding="utf-8").splitlines() if l and not l.startswith("#"))} if pin.exists() else {}
    files = {}
    for rel in copy_files():
        try:
            data = (HERE / rel).read_bytes()
        except OSError as e:
            return EXIT_LINT, [f"--install-hook: the hooks' copy of the tool is not written — {rel} cannot be read ({e.strerror or type(e).__name__})"]
        if pin.exists() and hashlib.sha256(data.replace(b"\r\n", b"\n")).hexdigest() != pins.get(rel):
            return EXIT_LINT, [f"--install-hook: the hooks' copy of the tool is not written — {rel} is " + ("not named by the PIN" if rel not in pins else "not what the PIN names")
                               + "; vendor the tool again (--vendor), then run --install-hook"]
        files[rel] = data
    if not pin.exists():
        lines.append(f"this repository pins no copy of the tool: the hooks' copy is taken from the working tree's tool, {HERE}")
    here_rel = os.path.relpath(HERE, ROOT).replace(os.sep, "/") if in_tree(HERE) else "-"
    sha = (git_out("rev-parse", "--short", "HEAD") or "").strip() or "no commit yet"
    branch = (git_out("branch", "--show-current") or "").strip()
    default = default_branch()
    stage = target.with_name(COPY_DIR + ".new")
    shutil.rmtree(stage, ignore_errors=True)
    for rel, data in files.items():
        (stage / rel).parent.mkdir(parents=True, exist_ok=True)
        (stage / rel).write_bytes(data)
    put(stage / "COPY", "# the hooks' copy of the tool — written by --install-hook, run by every hook it writes, and by nothing else\n"
        f"version: {__version__}\ntool: {'' if here_rel == '.' else here_rel}\nsource: {'pinned copy' if pin.exists() else 'working tree'}\ncommit: {sha}\nbranch: {branch or '(detached HEAD)'}\n"
        f"cmd: {CMD_OWN}\n")
    if target.is_symlink():
        target.unlink()
    shutil.rmtree(target, ignore_errors=True)
    os.replace(stage, target)
    lines.append(f"wrote {target} — the hooks' copy of the tool, {__version__}, from {HERE / 'shoalmark.py'} at {sha} on {branch or '(detached HEAD)'}")
    same_tree = "the PIN this copy was checked against comes from the same tree, so " if pin.exists() else ""     # a PIN is named only where one is pinned
    if default is None:
        lines.append(f"warning: the default branch cannot be told here (no origin/HEAD, origin/main or origin/master) — {same_tree}"
                     f"a copy installed from a branch that is not the default one carries that branch's tool: run --install-hook on your default branch")
    elif branch != default:
        lines.append(f"warning: {branch or '(detached HEAD)'} is not {default}, the default branch — {same_tree}"
                     f"a copy installed from another branch carries that branch's tool: run --install-hook on {default}")
    return EXIT_OK, lines


_COPY_RECORD = None


def copy_record():
    """What `--install-hook` wrote beside the hooks' copy — its `COPY` file, read once, as data: {} where this run is not the copy. A value that is not one
    printable line is no value."""
    global _COPY_RECORD
    if _COPY_RECORD is None:
        marker = HERE / "COPY"
        try:
            made = read_flat(marker.read_text(encoding="utf-8")) if marker.is_file() else {}
        except (OSError, UnicodeDecodeError):
            made = {}
        _COPY_RECORD = {k: v for k, v in made.items() if isinstance(v, str) and len(v) < 400 and v.isprintable()}
    return _COPY_RECORD


def tree_tool_dir():
    """In the hooks' copy: the folder of the repository's own tool — the one `--install-hook` was run from, as its `COPY` says — or None where that was outside
    the repository, or is not said."""
    tool = copy_record().get("tool", "-")
    if tool == "-" or not re.fullmatch(r"[A-Za-z0-9_./-]*", tool) or ".." in tool.split("/"):
        return None
    return ROOT / tool if tool else ROOT


def tool_here():
    """Where the repository's own tool is, for its PIN: this file's folder — in the hooks' copy, the tree's tool's (`tree_tool_dir`)."""
    return tree_tool_dir() if HOOK_RUN else HERE


def tree_bytes(path):
    """A file of the tree as bytes, `\\r\\n` read as `\\n` — or None where it is not there, or, in the board's run, not a regular file inside the repository."""
    path = pathlib.Path(path)
    if not board_isfile(path):
        return None
    try:
        return path.read_bytes().replace(b"\r\n", b"\n")
    except OSError:
        return None


def hooks_copy_drift():
    """Where this run IS the hooks' copy (its `COPY` file is beside it): the one line that says the repository's own tool is not the copy — another version, read as
    data from the PIN's manifest or the VERSION of the tool the copy was taken from; or the same version with other files — else "". Where the tree holds no
    `shoalmark.py` there, there is nothing to compare."""
    if not (HERE / "COPY").is_file():
        return ""
    tool = tree_tool_dir()
    if tool is None:
        return ""
    pin, version = board_text(tool / "PIN"), board_text(tool / "VERSION")
    first = (pin or "").splitlines()[0] if pin else ""
    manifest = MANIFEST_RE.fullmatch(first)
    pinned = manifest.group(1) if manifest else (version or "").strip()
    if re.fullmatch(r"\d+\.\d+\.\d+", pinned) and pinned != __version__:
        return f"the hooks' copy is {__version__}, the repository pins {pinned}: run --install-hook"
    if tree_bytes(tool / "shoalmark.py") is None:
        return ""
    if any(tree_bytes(tool / rel) != (HERE / rel).read_bytes().replace(b"\r\n", b"\n") for rel in copy_files()):
        return f"the hooks' copy is {__version__}, and the repository's tool differs from it: run --install-hook"
    return ""


def worktree_tops():
    """Every working tree of this repository — this one, the main one and every linked one — as `git worktree list` names them, resolved: one it marks
    `prunable`, whose folder is gone, included, for that folder can come back."""
    tops = {os.path.realpath(ROOT)}
    for record in (git_out("worktree", "list", "--porcelain") or "").split("\n\n"):
        top = next((l[len("worktree "):] for l in record.splitlines() if l.startswith("worktree ")), None)
        if top:
            tops.add(os.path.realpath(top))
    return sorted(tops)


def worktree_git_dirs():
    """Every worktree of this repository as (its folder, its git directory, the files of its own configuration), whether or not the folder is there: the main
    one — the common git directory, its `config` and `config.worktree` — and each linked one under the common git directory's `worktrees/`, its
    `config.worktree`, its folder as its `gitdir` file names it (None where that cannot be read)."""
    common = os.path.abspath(ROOT / ((git_out("rev-parse", "--git-common-dir") or "").strip() or ".git"))
    main = next((l[len("worktree "):] for l in (git_out("worktree", "list", "--porcelain") or "").splitlines() if l.startswith("worktree ")), None)
    found = [(os.path.realpath(main or ROOT), common, [os.path.join(common, "config"), os.path.join(common, "config.worktree")])]
    try:
        names = sorted(os.listdir(os.path.join(common, "worktrees")))
    except OSError:
        names = []
    for name in names:
        gitdir = os.path.join(common, "worktrees", name)
        if not os.path.isdir(gitdir):
            continue
        said = ""
        if os.path.isfile(os.path.join(gitdir, "gitdir")):
            try:
                said = pathlib.Path(gitdir, "gitdir").read_text(encoding="utf-8", errors="replace").strip()
            except OSError:
                pass
        found.append((os.path.realpath(os.path.join(gitdir, re.sub(r"[\\/]\.git$", "", said))) if said else None, gitdir, [os.path.join(gitdir, "config.worktree")]))
    return found


def config_file_unreadable(path):
    """Why git cannot read the configuration file `path`, in a few words — or "": it is there, and is not a regular file, or cannot be opened to read. A
    file that is not there is no problem: git reads none."""
    if not os.path.lexists(path):
        return ""
    if not os.path.isfile(path):
        return f"{path} is not a regular file"
    try:
        with open(path, "rb"):
            pass
    except OSError as e:
        return f"{path} cannot be read ({e.strerror or type(e).__name__})"
    return ""


def hooks_folder_problem(hooks):
    """Why `--install-hook` writes nothing into the hooks folder git reads, in one line — or "": it resolves, symlinks resolved, inside a working tree of this
    repository and outside its git directory, so a branch can change the hooks themselves. It is judged against EVERY working tree `git worktree list` names,
    the main one and each linked one: a relative `core.hooksPath` is read where each of them resolves it — a hook runs in the working tree of whichever
    worktree it runs in — and an absolute one as it is; with none set, the folder is the common git directory's `hooks`, which passes. `hooks` is that
    folder as this worktree resolves it."""
    tops = worktree_tops()
    said = (git_out("config", "--path", "--get", "core.hooksPath") or "").strip()
    seen = [hooks] if not said or os.path.isabs(said) else [os.path.join(top, said) for top in tops]
    trees = {top: fs_chain(top)[:1] for top in tops}
    for where in seen:
        top = tree_holding(os.path.normcase(os.path.realpath(where)), trees)
        if top:
            return (f"--install-hook: the hooks folder {where} is inside the working tree {top}, where a branch can change the hooks themselves — no hook and no copy is "
                    f"written; point `core.hooksPath` outside every working tree, or read the README's paragraph on a repository with its own hook runner (§Sessions)")
    return ""


def tree_holding(real, trees):
    """The working tree of `trees` that the path `real`, resolved, is or lies in, outside the repository's git directories (`git_dir_holding`) — or None:
    the judgement the hooks folder and the configuration check share, made as the file system compares paths. A tree is found by the file system's own
    identity (`fs_chain`) — the path, or one of its ancestors that exists, is the tree's folder, so a spelling in another case, where the file system
    ignores case, is the same tree — and by its spelling, `os.path.normcase`d. The tree is returned `os.path.normcase`d. `trees` maps each tree's folder to
    its `fs_chain(…)[:1]`, read once by the caller for every path it judges."""
    if git_dir_holding(real):
        return None
    mine, real = fs_chain(real), os.path.normcase(real)
    for top, folder in trees.items():
        top = os.path.normcase(top)
        if real == top or real.startswith(top.rstrip(os.sep) + os.sep):
            return top
        if folder and any(ident == folder[0][0] and below[:len(folder[0][1])] == folder[0][1] for ident, below in mine):
            return top
    return None


def git_dir_holding(real):
    """Whether the path `real`, resolved, lies in one of the repository's git directories as the file system compares paths: as `in_git_dir` finds it, or —
    where `os.path.normcase` keeps case — spelled so in another case or Unicode normalization (`fs_fold`), its ancestor there being that git directory by
    the file system's own identity."""
    if in_git_dir(real):
        return True
    if os.path.normcase("A") != "A":
        return False
    parts = real.rstrip(os.sep).split(os.sep)
    for gd in git_dirs():
        named = gd.rstrip(os.sep).split(os.sep)
        if len(parts) >= len(named) and [fs_fold(p) for p in parts[:len(named)]] == [fs_fold(p) for p in named]:
            same = fs_identity(os.sep.join(parts[:len(named)]))
            if same is not None and same == fs_identity(gd):
                return True
    return False


def fs_identity(path):
    """The file system's own identity of `path` — its device and inode, symlinks followed — or None where it is not there or has no inode."""
    try:
        st = os.stat(path)
    except (OSError, ValueError):
        return None
    return (st.st_dev, st.st_ino) if st.st_ino else None


def fs_chain(path):
    """The path `path`, resolved, as the file system knows it: for it and each of its ancestors that has an identity (`fs_identity`), nearest first,
    (that identity, and the names of the path below it, folded as `fs_fold` folds them)."""
    chain, below = [], []
    while True:
        ident = fs_identity(path)
        if ident is not None:
            chain.append((ident, tuple(below)))
        parent = os.path.dirname(path)
        if parent == path:
            return chain
        below.insert(0, fs_fold(os.path.basename(path)))
        path = parent


def fs_fold(name):
    """A file's name as a file system that ignores case and Unicode normalization compares it — macOS's default one does both: case-folded, and in one
    normalization (NFD) before and after."""
    return unicodedata.normalize("NFD", unicodedata.normalize("NFD", name).casefold())


def config_file_problem():
    """Why `--install-hook` writes nothing because of where git reads its configuration from, in one line — or "": a value comes from a file that resolves,
    symlinks resolved, inside a working tree of this repository and outside its git directory (an `include.path` into the tree, say), so a branch can
    change what git runs — a hooks folder, a filter, a program. Read from `git config --list --show-origin` and judged as the hooks folder is: against
    every working tree `git worktree list` names, removed ones included (`worktree_tops`); the git directories themselves (`.git/config`, a worktree's
    `config.worktree`) pass. The target of every include setting is judged the same way (`include_targets`): conditional ones whether or not the condition
    holds, and whether or not the target exists yet. The settings of EVERY worktree are read, removed ones included, from its git directory
    (`worktree_git_dirs`) as git reads them there — its own configuration included (`config.worktree`, under `extensions.worktreeConfig`), with its include
    settings — as the hooks folder is judged in every one. Where the settings of a worktree cannot be read — a file of its own configuration is not a
    regular file git can read (`config_file_unreadable`), or `git config` fails — that is the one line, naming the worktree and why."""
    trees = {top: fs_chain(top)[:1] for top in (os.path.normcase(t) for t in worktree_tops())}
    for folder, gitdir, own in worktree_git_dirs():
        why = next((w for w in map(config_file_unreadable, own) if w), "")
        out = None if why else subprocess.run(["git", f"--git-dir={gitdir}", "config", "--list", "--show-origin", "-z"], cwd=ROOT, capture_output=True,
                                                text=True, encoding="utf-8", errors="replace", env=nested_git_env())
        if out is not None and out.returncode:
            why = "; ".join(dict.fromkeys(l.strip() for l in out.stderr.splitlines() if l.strip())) or f"`git config` exits {out.returncode}"
        if why:
            return (f"--install-hook: the configuration of the worktree {folder or gitdir} cannot be read — {why} — no hook and no copy is written; fix it, "
                    f"or remove the worktree (`git worktree remove`, or `git worktree prune` where its folder is gone)")
        listing = out.stdout.split("\0")
        for origin in dict.fromkeys(listing[0::2]):
            if not origin.startswith("file:"):
                continue
            where = origin[len("file:"):]
            real = os.path.normcase(os.path.realpath(where if os.path.isabs(where) else os.path.join(ROOT, where)))
            top = tree_holding(real, trees)
            if top:
                return (f"--install-hook: git reads configuration from {real}, inside the working tree {top}, where a branch can change what git runs — no hook and no "
                        f"copy is written; keep that setting in .git/config or outside every working tree")
        for holder, target in include_targets(listing):
            real = os.path.normcase(os.path.realpath(target))
            top = tree_holding(real, trees)
            if top:
                return (f"--install-hook: an include setting in {os.path.realpath(holder) if holder else 'the command line'} names {real}, inside the working tree {top}, "
                        f"where a branch can change what git runs — no hook and no copy is written; point every include outside every working tree, whatever its condition")
    return ""


INCLUDE_KEY = re.compile(r"include(?:if\..*)?\.path", re.I | re.S)     # `include.path`, and `includeIf.<condition>.path` whatever the condition


def include_targets(listing):
    """Every include setting of git's configuration, as (the file that holds it, or None for the command line; its target). The target is taken as
    written, whether or not it exists: `~` from the home folder, `%(prefix)/` from git's own, any other relative target from the folder of the file that
    holds it. A target that is a file is read for its own include settings in turn, whatever its condition. `listing` is `git config --list --show-origin
    -z` split at its NULs, run at the repository's root: a relative origin is read from there."""
    at = lambda origin: os.path.join(ROOT, origin[len("file:"):]) if origin.startswith("file:") else None
    todo = [(at(o), *e.partition("\n")[::2]) for o, e in zip(listing[0::2], listing[1::2])]
    found, read = [], set()
    while todo:
        holder, key, value = todo.pop(0)
        if not INCLUDE_KEY.fullmatch(key) or not value:
            continue
        if value.startswith("%(prefix)/"):
            target = os.path.join(re.sub(r"[\\/]libexec[\\/]git-core[\\/]*$", "", (git_out("--exec-path") or "").strip()), value[len("%(prefix)/"):])
        else:
            target = os.path.expanduser(value)
            if not os.path.isabs(target):
                if holder is None:
                    continue                                # git refuses a relative include that comes from no file
                target = os.path.join(os.path.dirname(holder), target)
        found.append((holder, target))
        if os.path.realpath(target) not in read and os.path.isfile(target):
            read.add(os.path.realpath(target))
            todo += [(target, *e.partition("\n")[::2]) for e in (git_out("config", "--file", target, "--no-includes", "--list", "-z") or "").split("\0") if e]
    return found


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
    refused = hooks_folder_problem(hooks) or config_file_problem()
    if refused:                                             # a hooks folder, or a configuration file, a branch can change runs what the branch names: no hook, and no copy
        print(refused, file=sys.stderr)
        return EXIT_LINT
    hooks.mkdir(parents=True, exist_ok=True)
    fill = dict(mark=HOOK_MARK, cmd=CMD, dir=TRACKER_DIR.relative_to(ROOT).as_posix(), config=CONFIG_NAME,
                tool=pathlib.Path(__file__).resolve().parent.relative_to(ROOT).as_posix() if ROOT in pathlib.Path(__file__).resolve().parents else "tools/shoalmark")
    code = EXIT_OK
    copy_code, copy_lines = install_copy()
    hook_set = {**HOOKS, **COPY_HOOKS} if copy_code == EXIT_OK else {}      # every hook runs the copy: none is written where it is not there
    for name, text in hook_set.items():
        path = hooks / name
        if path.exists() and not any(m in path.read_text(encoding="utf-8", errors="replace") for m in (HOOK_MARK, LEGACY_HOOK_MARK)):
            print(f"{path} exists and is not shoalmark's — left alone. Add to it: `{PY} -I {COPY_AT} {HOOK_LINES[name]}`", file=sys.stderr)
            code = EXIT_LINT
            continue
        put(path, text.format(py=PY, **fill))
        path.chmod(0o755)
        print(f"wrote {path}")
    for line in copy_lines:
        print(line, file=sys.stderr if copy_code != EXIT_OK or line.startswith("warning:") else sys.stdout)
    return code or copy_code


def init(key=None):
    refused = tracker_folder_problem("nothing is written")  # the tracker folder, judged first, as every run judges it (`load_trackers`)
    if refused:
        print(refused, file=sys.stderr)
        return EXIT_LINT
    wrote = []
    key = (key or re.split(r"[^A-Za-z0-9]+", ROOT.name.strip("._-"))[0][:5] or "WORK").upper()
    if not re.fullmatch(r"[A-Z][A-Z0-9]*", key):
        print(f"--key: {key!r} is not an id prefix — letters and digits, starting with a letter", file=sys.stderr)
        return EXIT_LINT
    fresh_config = not (ROOT / CONFIG_NAME).exists()
    config_text = CONFIG_TEMPLATE.format(name=ROOT.name.replace("\\", "\\\\").replace('"', '\\"'), key=key)       # the folder's name as a TOML string
    if fresh_config:                                        # read back before anything is written: a name it cannot carry is refused in one line
        try:
            read_config(config_text)
        except SystemExit:
            print(f"--init: the folder's name {ROOT.name!r} cannot be written into {CONFIG_NAME} as one line — nothing is written; give the folder a name "
                  "without a line break", file=sys.stderr)
            return EXIT_LINT
    made = [(path, text) for path, text in ((ROOT / CONFIG_NAME, config_text),
                                            (TRACKER_DIR / "TRIAGE.md", TRIAGE_HOME.format(cmd=CMD, **HEAD))) if not path.exists()]
    agents, claude, ignore, svn = ROOT / "AGENTS.md", ROOT / "CLAUDE.md", ROOT / ".gitignore", vcs() == "svn"
    had_agents, had_ignore = board_text(agents) or "", board_text(ignore) or ""        # the reading rule, before anything is written
    for path in [path for path, _text in made] + [agents] + ([] if claude.exists() else [claude]) + ([ignore] if not svn and (vcs() == "git" or ignore.exists()) else []):
        write_rule(path)                                    # the write rule for every file --init may write, before the first is written or a folder made
    for path, text in made:
        path.parent.mkdir(parents=True, exist_ok=True)
        put(path, text)
        wrote.append(path)
    if fresh_config:
        configure(ROOT)
    section = CONTRACT_BEGIN + "\n" + CONTRACT.format(dir=TRACKER_DIR.relative_to(ROOT).as_posix(), gate=GATE_SAYS.get(vcs(), GATE_SAYS[""]).format(cmd=CMD), state=HEAD["state"], cmd=CMD, key=KINDS[0], lkey=KINDS[0].lower()) + CONTRACT_END + "\n"
    have = had_agents
    if LEGACY_CONTRACT[0] in have and LEGACY_CONTRACT[1] in have:        # the block an older copy wrote, under the old name
        a = have.index(LEGACY_CONTRACT[0]); have = have[:a] + have[have.index(LEGACY_CONTRACT[1]) + len(LEGACY_CONTRACT[1]):].lstrip("\n")
    if CONTRACT_BEGIN in have and CONTRACT_END in have:
        new = have[:have.index(CONTRACT_BEGIN)] + section + have[have.index(CONTRACT_END) + len(CONTRACT_END):].lstrip("\n")
    else:
        new = (have.rstrip("\n") + "\n\n" if have.strip() else f"# {CONFIG['name'] or ROOT.name} — for agents\n\n") + section
    if new != have:
        put(agents, new)
        wrote.append(agents)
    if not claude.exists():                                 # Claude Code reads CLAUDE.md, not AGENTS.md — a router, never a second copy
        put(claude, "# CLAUDE.md\n\nThe contract for agents in this repository is [`AGENTS.md`](AGENTS.md) — read it first. This file owns no rules.\n")
        wrote.append(claude)
    rel, have = TRACKER_DIR.relative_to(ROOT).as_posix(), had_ignore
    lines = [l for l in (f"{rel}/index.html", f"{rel}/view/") if l not in have.splitlines()]
    if svn:                                                 # Subversion ignores by property, not by file
        svn_ignore_board()
    elif lines and (vcs() == "git" or ignore.exists()):     # no version control here (yet): nothing to ignore for
        put(ignore, have + ("" if have.endswith("\n") or not have else "\n") + "\n".join(lines) + "\n")
        wrote.append(ignore)
    print("\n".join([f"wrote {p.relative_to(ROOT).as_posix()}" for p in wrote] or ["nothing to write — already initialised"]))
    print(f"next: the Owner writes the intent and the current path in {(TRACKER_DIR / 'TRIAGE.md').relative_to(ROOT).as_posix()}; "
          f"file the first tracker with `{CMD} --new \"…\"` — it becomes {KINDS[0]}-001; branches carry the id: `feat/{KINDS[0].lower()}-001-slug`; `{CMD} --install-hook` wires the commit gate; a seat's worktree carries two settings: "
          f"`git config --worktree user.email <seat>` (who may) and `git config --worktree seat.session <id>` (which run — `{CMD} --session new` prints one); `seat.harness` (the id the harness gave the seat, for its `Model:` and `Effort:`) is `{CMD} --whoami`'s")
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
    more. None while they do not, where `freeze_at` is 0, and where `[tags]` has no `freeze_tag` — a freeze nothing could
    pass would refuse even the defect it exists to let through (`freeze_unpassable` says so)."""
    n = sum(t["status"] in OPEN_STATUSES for t in trackers)
    return (n, FREEZE_AT) if FREEZE_AT and n >= FREEZE_AT and not freeze_unpassable() else None


def freeze_unpassable():
    """The one line `--check` owes a repository whose freeze is set and whose `[tags]` cannot pass it — or ""."""
    if FREEZE_AT and FREEZE_TAG.lower() not in {k.lower() for k in TAGS}:
        return (f"filing freeze: off — `freeze_tag` {FREEZE_TAG!r} is not in [tags] ({', '.join(sorted(TAGS)) or 'none'}); "
                f"add it there, or set `freeze_tag` in {CONFIG_NAME} to the tag a product defect carries")
    return ""


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
    template = board_text(house) or TRACKER_TEMPLATE        # the reading rule
    frozen = filing_freeze(trackers)
    tags = [x.strip().lstrip("#").lower() for x in (parse_frontmatter(template)[0].get("tags") or "").split(",") if x.strip()]
    if tags_arg is not None:                                # `--tags bug,process`: the kind of work, said as it is filed
        vocab = {k.lower(): k for k in TAGS}                # matched as the template's are, case aside; written as [tags] spells it
        said = [x.strip().lstrip("#") for x in tags_arg.split(",") if x.strip().lstrip("#")]
        tags = list(dict.fromkeys(vocab.get(x.lower(), x) for x in said))
        unknown = [x for x in tags if vocab and x.lower() not in vocab]
        if not tags or unknown or len(tags) > MAX_TAGS:
            why = ("no tag was given" if not tags else f"{', '.join(unknown)} not in the vocabulary ({', '.join(sorted(TAGS))}, [tags] in {CONFIG_NAME})" if unknown
                   else f"at most {MAX_TAGS} tags, from [tags] in {CONFIG_NAME}")
            print(f"--new: --tags {tags_arg!r} — {why} — nothing was written", file=sys.stderr)
            return EXIT_LINT
    if frozen and FREEZE_TAG.lower() not in {x.lower() for x in tags}:
        print(f"--new: filing freeze — {frozen[0]} open, at or above {frozen[1]} (`freeze_at` in {CONFIG_NAME}): only product defects are filed; "
              f"anything else goes as one line into the closest open tracker's body, or waits. This filing carries no `{FREEZE_TAG}` tag — "
              f"a product defect is filed with `--tags {FREEZE_TAG}`; nothing was written", file=sys.stderr)
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
    write_rule(path)                                        # the write rule, before its folder is made
    TRACKER_DIR.mkdir(parents=True, exist_ok=True)
    text = template.format(id=tid, title=title.replace('"', "'"), today=datetime.date.today().isoformat(), **HEAD)
    put(path, set_front(text, "tags", ", ".join(tags)) if tags_arg is not None else text)
    print(f"wrote {path.relative_to(ROOT).as_posix()} — fill `considered:` with the ids you held it against, or `none`; the gate refuses it until then")
    return EXIT_OK


def board_run(root):
    """`--html-only`: the board's own run, the one a checkout and a merge hook starts (a private security report). It reads what the repository holds
    and writes the board — `index.html` and `view/<ID>.js` in the tracker folder — and does nothing else:
    - it starts no deriver and no program but read-only git — `board_tripwire` refuses anything else where Python does it;
    - it reads the tree only as regular files inside the repository, through no symlink: the trackers, the configuration, the brand's files;
    - the tracker folder must resolve inside the repository, and the board is written only there, never through a symlink and never over a file git tracks;
    - it imports nothing from the repository, and writes no bytecode.
    What it leaves alone it names, in one line — and where that is the page itself, it prints that line and no link; a tracker folder it refuses, in one line, exit 4."""
    global SAFE_READS, SAFE_WRITES, _TRIPWIRE, _TRACKED
    saved = (sys.dont_write_bytecode, list(sys.path), os.environ.get("NoDefaultCurrentDirectoryInExePath"), SAFE_WRITES)
    SAFE_READS, SAFE_WRITES, _TRACKED = True, True, None
    BOARD_LEFT.clear(), TRIPPED.clear()
    sys.dont_write_bytecode = True
    os.environ["NoDefaultCurrentDirectoryInExePath"] = "1"          # Windows starts `git` from the current directory first, and the checkout's is the branch's
    try:
        configure(root)
        sys.path[:] = [e for e in sys.path if not in_tree(e or ".") or _norm(e or ".") == _norm(HERE)]      # nothing is imported from the tree, but the tool's own place
        refused = tracker_folder_problem()
        if refused:
            print(refused, file=sys.stderr)
            return EXIT_LINT
        arm_tripwire()
        trackers = load_trackers()
        no_derived(trackers)                                        # no deriver: no derived column, file, note or key
        if TRACKER_DIR.is_dir():
            tracked = tracked_board_rels()
            if any(r != HTML_OUT.relative_to(ROOT).as_posix() for r in tracked):     # the cold review's F1: no page this run writes loads a view git tracks
                line = tracked_board_line(tracked)
                if board_write(HTML_OUT, tracked_board_page(line)):     # a page git tracks itself is left as committed, with its line
                    print(line, file=sys.stderr)                    # in place of the link
            else:                                                   # a page git tracks is left as committed, its line said in place of the link
                written = board_write(HTML_OUT, render_html(trackers))
                write_views(trackers)
                if written:
                    print(board_link())                             # where the board is written, to open (FM-006) — only a board this run wrote; never with --print-written
            drift = hooks_copy_drift()
            if drift:
                print(drift)                                        # the hook still refreshed: it only says that the copy is not what the repository pins
        return EXIT_OK
    except ReadOnlyRun as e:
        print(f"the board's run was stopped: {e} — it starts nothing but read-only git and writes only the board", file=sys.stderr)
        return EXIT_LINT
    finally:
        _TRIPWIRE = SAFE_READS = False
        SAFE_WRITES = saved[3]
        sys.dont_write_bytecode, sys.path[:] = saved[0], saved[1]
        if saved[2] is None:
            os.environ.pop("NoDefaultCurrentDirectoryInExePath", None)
        else:
            os.environ["NoDefaultCurrentDirectoryInExePath"] = saved[2]
        if BOARD_LEFT:
            shown = ", ".join(f"{rel} ({why})" for rel, why in BOARD_LEFT[:4]) + (f" and {len(BOARD_LEFT) - 4} more" if len(BOARD_LEFT) > 4 else "")
            print(f"board: left alone — {shown}", file=sys.stderr)


_AUDIT_HOOKED = [False]
BOARD_RUN_SECONDS = int(os.environ.get("SHOALMARK_BOARD_SECONDS") or 35)      # how long the board's run, or any hook's run of the copy, may take: nothing waits longer for it


def board_watchdog(board=True):
    """Bound the board's run when it is a program (a hook's, a hand run's), and every hook's run of the copy: after `BOARD_RUN_SECONDS` a thread of its own says so on stderr
    and ends the process, exit 4, whatever the main thread waits on — a lock, a child, a pipe. A checkout or a merge hook prints one line and returns, so they never wait on
    it; a commit's hook (`board` false) fails closed: its one line says the commit is refused, and the hook's exit refuses it."""
    said = (f"the board's run took longer than {BOARD_RUN_SECONDS} s and was stopped" if board
            else f"shoalmark: the hook's run took longer than {BOARD_RUN_SECONDS} s and was stopped — the commit is refused; SHOALMARK_BOARD_SECONDS gives it longer")
    def stop():
        os.write(2, (said + "\n").encode("utf-8"))
        os._exit(EXIT_LINT)
    timer = threading.Timer(BOARD_RUN_SECONDS, stop)
    timer.daemon = True
    timer.start()


def main(argv=None):
    for stream in (sys.stdout, sys.stderr):                 # a Windows console in cp1252 cannot encode `—` `→` `◐`: say it in UTF-8, never crash
        if hasattr(stream, "reconfigure"):                   # …and `\n`, never `\r\n`: a hook pipes --print-written into `git add`
            stream.reconfigure(encoding="utf-8", errors="replace", newline="\n")
    args = parse_args(argv)
    for flag, needs, alone, like in (("--tags", "--new", args.tags is not None and not args.new, '`--new KIND "the title" --tags bug`'),
                                     ("--supersede", "--answer", args.supersede and not args.answer, '`--answer <id> accept|reject "<option>" --supersede`'),
                                     ("--from", "--brand DIR", args.theme is not None and not args.brand, f"`--brand DIR --from {'|'.join(shipped_themes()) or 'THEME'}`")):
        if alone:                                           # a flag that means nothing alone is refused, never silently ignored
            print(f"{flag} goes with {needs} — {like}", file=sys.stderr)
            return 2
    if args.html_only:                                      # …and nothing else, whatever else was said: the board's run is read-only and stands alone
        others = [f"--{k.replace('_', '-')}" for k, v in vars(args).items() if v and k not in ("html_only", "root")]
        if others:
            print(f"--html-only is the board's read-only run and stands alone, with --root: {', '.join(others)} goes with another run", file=sys.stderr)
            return 2
        return board_run(args.root)
    if args.tsvn_hook:
        # TortoiseSVN starts a hook wherever it likes and appends PATH DEPTH MESSAGEFILE CWD: the repository is the
        # one this copy of the tool lives in. `start` runs before the commit dialog lists its files, so the INDEX.md
        # it writes is on the list; `pre` refuses the commit on a violation, the message in TortoiseSVN's error box.
        configure(HERE)
        args = parse_args(["--root", str(ROOT)] + ([] if args.tsvn_hook[0] == "start" else ["--check"]))
    if args.root:
        configure(args.root)
    if HOOK_RUN:                                            # a hook's run of the copy writes only inside the repository, outside its git directory, through no symlink
        global SAFE_WRITES
        SAFE_WRITES = True
        os.environ["NoDefaultCurrentDirectoryInExePath"] = "1"          # Windows starts a program from the current directory first, and the checkout's is the branch's
        drift = "" if args.print_written else hooks_copy_drift()        # once per hook: the pre-commit hook says it with --session-check, before --print-written
        if drift:
            print(drift, file=sys.stderr)
    # under --print-written stdout carries ONE thing: the path list the caller stages
    log = sys.stderr if args.print_written else sys.stdout
    if args.vendor:
        return vendor(args.vendor, partial=args.partial, allow_untagged=args.allow_untagged)
    if args.brand is not None:
        return brand_report(args.brand or None, args.theme)
    if args.init:
        return init(args.key)
    if args.install_hook:
        return install_hook()
    if args.session_trailer:                                # every commit runs this: it reads one git setting, never the trackers
        return session_trailer(args.session_trailer[0])
    if args.whoami:                                         # who this session is: git's settings and the harness's own log, no tracker
        return whoami()
    if args.session_check:                                  # …and this: the session rule on a commit that stages no tracker (R4)
        return session_check()
    if args.commit_msg:                                     # …and this, once the message exists: no build commit before a judgement (FM-033), the Owner's two sections (FM-037)
        return commit_msg_hook(args.commit_msg[0])
    if args.session:
        return session_cmd(args.session)
    if args.sessions:                                       # the registry: a report of the trailers, read from git alone
        return sessions_cmd()
    if args.ratio:                                          # FM-032: a report of git's first-parent history — no tracker is read
        return ratio_cmd(args.since, args.until)
    if args.since or args.until:
        print("--since and --until go with --ratio", file=sys.stderr)
        return 2
    if args.queue:                                          # FM-031 S2: the forge's queue — no tracker is read
        return queue_cmd()
    if args.answer:
        answer_step(args.answer[0].upper(), 1, "reading the trackers")
    for words, verb in ((args.done, "recording"), (args.due, "rescheduling"), (args.revoke, "revoking")):
        if words:
            answer_step(words[0].upper(), 1, "reading the trackers", verb)
    trackers = load_trackers()
    global COMMITTING
    COMMITTING = bool(args.print_written)                 # the pre-commit run: what it stages is what its git calls are spent on
    mode = "check" if args.check else "write" if not (args.schema or args.new or args.next or args.related or args.notify or args.invite) else "read"
    refused, derived_problems = run_deriver(trackers, mode, args.derive_flag)
    if args.schema:
        print(render_schema())
        return EXIT_OK
    if refused is not None:                                 # the deriver said no: nothing is judged, nothing is written
        for p in derived_problems:
            print(f"  {p}", file=sys.stderr)
        print("REFUSED by the deriver — nothing was written.", file=sys.stderr)
        return refused
    if args.new:
        return new_tracker(args.new, trackers, args.tags)
    if args.invite:
        return invite_cmd(args.invite, trackers)
    if args.notify:
        return notify_cmd(trackers)
    if args.owner:
        code = owner_digest(trackers)
        queue_section()
        return code
    if args.answered:
        return answered(trackers)
    if args.answer:
        return answer_cmd(args.answer, trackers, supersede=args.supersede)
    if args.done:
        return done_cmd(args.done, trackers)
    if args.due:
        return due_cmd(args.due, trackers)
    if args.revoke:
        return revoke_cmd(args.revoke, trackers)
    if args.clear_ask:
        return clear_ask(args.clear_ask, trackers)
    if args.standup is not None:
        code = standup(trackers, args.standup)
        if not args.standup:                                # the agenda, not the calendar invite
            queue_section()
        return code
    if args.next:
        return next_up(trackers)
    if not TRACKER_DIR.is_dir():
        print(f"no tracker directory at {TRACKER_DIR} — run `{CMD} --init`", file=sys.stderr)
        return EXIT_LINT
    if args.triage:
        home, path_now = TRACKER_DIR / "TRIAGE.md", triage_home()["path"]
        if not path_now:
            print(f"--triage: {home.relative_to(ROOT).as_posix()} names no current path — tiers cannot be judged; the Owner writes it first", file=sys.stderr)
            return EXIT_LINT
        today = datetime.date.today().isoformat()
        out = TRACKER_DIR / "evidence" / "triage" / f"triage-{today}.md"
        write_rule(out)                                     # the write rule, before its folder is made — as for the derived files
        out.parent.mkdir(parents=True, exist_ok=True)
        sheets = sorted(out.parent.glob("triage-*.md"))
        superseded = []
        applied, errors = apply_worksheet(board_text(sheets[-1]) or "", sheets[-1] == out, trackers, today, superseded) if sheets else ([], [])      # the reading rule
        trackers = load_trackers()
        run_deriver(trackers, "write", args.derive_flag)
        earlier = board_text(out) or ""
        text, left = triage_worksheet(trackers, today, last_worked_on, earlier, repos_naming())
        put(out, text)
        print(TRIAGE_RULES.format(path=out.relative_to(ROOT).as_posix(), left=left, home=home.relative_to(ROOT).as_posix(), days=TRIAGE_DAYS, sized=SIZED_LINES, current_path=path_now,
                                  intent=triage_home()["intent"] or "  (none is written — the Owner writes it in the triage home)"))
        print("\n".join([f"Applied {len(applied)}:"] + [f"  {l}" for l in applied] if applied else ["Applied nothing — no new filled rows."]))
        if superseded:                                      # FM-036: said on every run, applied on none — the earlier row is the record
            print("\n".join(["Superseded on this sheet by the later row — left as it is, the record of the earlier judgement:"] + [f"  {l}" for l in superseded]))
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
    global _ASK_ORIGIN
    _ASK_ORIGIN = (mode in ("check", "write") and not args.print_written and vcs() == "git"       # `--check`, or the default run, on a clean tree: the
                   and not worktree_edited(lambda *a: subprocess.run(["git", *a], cwd=ROOT, capture_output=True, text=True, encoding="utf-8",
                                                                     errors="replace", env=nested_git_env())))      # runs that walk the branch's commits — no hook's (v0.19.1)
    problems = pin_problems() + lint(trackers, committing=args.print_written) + derived_problems
    ledger = [p for p in problems if not checkout_finding(p)]          # FM-034: the checkout's own findings stay out of INDEX.md
    today = datetime.date.today().isoformat()
    counts = ", ".join(f"{sum(t['kind'] == k for t in trackers)} {KIND_LABELS[k].lower()}" for k in KINDS)
    header = (
        "# Work Tracker — Index\n\n"
        f"> **GENERATED — do not hand-edit.** Run `{CMD}` after changing any tracker's front matter\n"
        "> (or its `# title`). Rows are *pointers* — the detail lives in the tracker, never duplicated here.\n>\n"
        "> **Status** = code lifecycle; `Shipped` means merged, **not** a production claim.\n>\n"
        "> **Tier · Board · Triaged** = the triage picture — the same one the board (`index.html`) shows, from the\n"
        "> same function: `progress` kept by a pass · `triage` owed a pass · `backlog` waiting · `ended` shipped or closed.\n"
        f"> One rule this file cannot show, because it has no clock: a judgement on work in progress older than {TRIAGE_DAYS} days\n"
        "> counts as `triage` again.\n>\n"
        + "".join("> " + n.replace("\n", "\n> ") + "\n>\n" for n in DERIVED_NOTES)
        + f"> Generated {today} · {len(trackers)} trackers ({counts})."
    )
    banner = [p for p in ledger if not pending_finding(p)]          # the commit being made is judged on stderr, not in INDEX.md
    if banner:
        header += f"\n>\n> ❌ {len(banner)} ledger-integrity violation(s):\n>\n" + "\n".join(f"> - {p}" for p in banner)
    if unknown:
        header += (f"\n>\n> ⚠️ {len(unknown)} tracker(s) have no machine-readable status — add a\n"
                   f"> front-matter `status:` to fix: {', '.join(sorted(unknown))}.")
    sections = [header, render_triage(trackers)] + [render([t for t in trackers if t["kind"] == k], KIND_LABELS[k]) for k in KINDS]
    body = "\n\n".join(sections).rstrip() + "\n"      # exactly one terminal newline, so `git diff --check` passes

    drifted = False
    if args.check:
        on_disk = board_text(OUT) or ""                     # the reading rule
        drifted = drift_normalize(on_disk) != drift_normalize(body)
        if drifted:
            print(f"{OUT.relative_to(ROOT).as_posix()} is STALE — a tracker changed without regenerating. Run: {CMD}", file=sys.stderr)
        for path, text in sorted(DERIVED_FILES.items()):
            if board_text(path) != text:
                drifted = True
                print(f"{path.relative_to(ROOT).as_posix()} is STALE — regenerate. Run: {CMD}", file=sys.stderr)
        if not drifted:
            print(f"{OUT.relative_to(ROOT).as_posix()} is up to date — {len(trackers)} trackers.", file=log)
        for line in sessions_report() + pin_report():       # reports, never refusals (FM-024, FM-011)
            print(line, file=log)
        print(build_judgement()[1], file=log)               # FM-033: whether the judgement gate is on, and what it judged
        print(triage_guard()[1], file=log)                  # FM-037: whether the Owner's two sections are guarded, and what it read
        if _WALK == "":                                     # v0.19.1: no default branch to read the branch's commits since
            print("the branch's commits: no default branch was found — no `origin/HEAD`, `origin/main` or `origin/master` — so only the newest commit is judged", file=log)
        elif _WALK == "uncommitted":                        # v0.19.1: the tree has edits — they were judged, not the branch's commits
            print("the branch's commits: the tree has uncommitted edits, so `--check` judged them against what HEAD holds, not the branch's commits", file=log)
        frozen = filing_freeze(trackers)                    # FM-032 S4: said, never refused — the refusal is `--new`'s
        if frozen:
            print(f"filing freeze: {frozen[0]} open, at or above {frozen[1]} — only {FREEZE_TAG} filings", file=log)
        elif freeze_unpassable():
            print(freeze_unpassable(), file=log)
    else:
        refused = tracker_folder_problem("nothing is written, and the commit is refused") if SAFE_WRITES else ""
        if refused:                                             # a hook's run of the copy writes nothing where the tracker folder may lead it out
            print(refused, file=sys.stderr)
            return EXIT_LINT
        try:
            for target in ([] if DERIVER_LEFT else [OUT]) + [HTML_OUT, *sorted(DERIVED_FILES)]:     # the write rule for every file this run writes, before it writes one
                write_rule(target)
            if os.path.lexists(VIEW_DIR) and (SAFE_WRITES or in_tree(VIEW_DIR)) and not (real_inside(VIEW_DIR) and VIEW_DIR.is_dir()):
                view_dir_refused()
            if DERIVER_LEFT:                                        # a hook ran no deriver: INDEX.md and what it derives stay as staged, never rewritten without its columns
                print(DERIVER_HOOK_LINE.format(cmd=CMD), file=sys.stderr)
            else:
                put(OUT, body)
            board_write(HTML_OUT, render_html(trackers))   # git-ignored; never staged
            write_views(trackers)
            if not DERIVER_LEFT:
                print(f"wrote {OUT.relative_to(ROOT).as_posix()} — {len(trackers)} trackers, {len(unknown)} unknown-status", file=log)
                print(f"  buckets — In Progress: {sum(t['status'] == 'In Progress' for t in trackers)} · generated files: {len(DERIVED_FILES)}", file=log)
            if not args.print_written:                              # the pre-commit run pipes its stdout into `git add` and its output stays as it was
                print(board_link())
            for path, text in sorted(DERIVED_FILES.items()):        # none where a hook ran no deriver
                guard_write(path)                                   # before its folder is made
                path.parent.mkdir(parents=True, exist_ok=True)
                put(path, text)
        except ReadOnlyRun as e:                                    # what a hook's run of the copy will not write refuses the commit, in one line
            print(f"shoalmark: the hooks' copy stopped: {e} — the commit is refused", file=sys.stderr)
            return EXIT_LINT
        if SAFE_WRITES and BOARD_LEFT:
            shown = ", ".join(f"{rel} ({why})" for rel, why in BOARD_LEFT[:4]) + (f" and {len(BOARD_LEFT) - 4} more" if len(BOARD_LEFT) > 4 else "")
            print(f"board: left alone — {shown}", file=sys.stderr)
        if args.print_written and not DERIVER_LEFT:     # the caller stages what we OWN, never a guessed glob — nothing where a hook ran no deriver
            for path in [OUT, *sorted(DERIVED_FILES)]:
                print(path.relative_to(ROOT).as_posix())

    for p in ledger:
        print(f"  lint: {p}", file=sys.stderr)
    for line in checkout_lines(problems):
        print(line, file=sys.stderr)
    for line in guard_footer(problems):                     # FM-037: the refusal's last line is its limit
        print(line, file=sys.stderr)
    # the INDEX is still written when a lint fires: the ❌ banner in its header IS the violation, made visible
    # where the ledger is read. What the non-zero exit stops is the COMMIT.
    if ledger:
        print(f"FAILED: {len(ledger)} ledger-integrity violation(s) — fix the tracker; regenerating will not clear these.", file=sys.stderr)
        return EXIT_LINT
    if problems:
        print("FAILED: this checkout's own finding — the ledger is sound; set the checkout up as the line says.", file=sys.stderr)
        return EXIT_LINT
    return EXIT_DRIFT if drifted else EXIT_OK


if __name__ == "__main__":                                  # what is said while the configuration is read, here, is in UTF-8 too — as `main` says
    for _stream in (sys.stdout, sys.stderr):                # everything after: a Windows console in cp1252 would say `—` in its own code page
        if hasattr(_stream, "reconfigure"):
            _stream.reconfigure(encoding="utf-8", errors="replace", newline="\n")
SAFE_READS = __name__ == "__main__" and "--html-only" in sys.argv[1:]     # the configuration `configure()` reads here is the board's run's first read: the same rule
if SAFE_READS or HOOK_RUN:
    board_watchdog(board=SAFE_READS)                                        # the board's run, and every hook's run of the copy, is bounded
configure()
SAFE_READS = False

if __name__ == "__main__":
    sys.exit(main())
