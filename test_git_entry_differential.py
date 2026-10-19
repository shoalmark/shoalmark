"""FM-044 P support: actual Git entry/process differential controls.

Outside proposal only. No handler, boundary, subprocess result or outcome is
mocked. Does not repeat generic schema/new/index/board/check/triage/session-new
pairs. Exercises clean/dirty origin selection and actual mixed-flag priorities.
All commits/configuration/remote setup are disposable fixture preparation;
production starts are reads and local generation only, with no push/hooks.
"""
import argparse
import base64
import datetime
import hashlib
import json
import os
from pathlib import Path
import re
import runpy
import shutil
import stat
import subprocess
import sys
import tempfile
import time


HERE = Path(__file__).resolve().parent
MARKER = "__GIT_ENTRY_DIFFERENTIAL__"
PAYLOAD = ("VERSION", "NOTICE", "LICENSE-APACHE", "LICENSE-MIT", "CHANGELOG.md", "README.md", "vendor/marked-18.0.13.umd.js")
POISON_KEYS = ("GIT_DIR", "GIT_WORK_TREE", "GIT_INDEX_FILE", "GIT_PREFIX", "GIT_LITERAL_PATHSPECS", "GIT_ICASE_PATHSPECS", "GIT_GLOB_PATHSPECS", "GIT_NOGLOB_PATHSPECS")
# R21 (FM-032): the candidate's INDEX.md drops the header's dated, counted line, which the 615fb1d baseline still writes after a
# bare `>` line. The one difference the consumer's snapshots may show; CI run 38744072206 failed the two default cases on it.
INDEX_PATH = "work-tracker/INDEX.md"
R21_LINE = re.compile(r"\n>\n> Generated \d{4}-\d{2}-\d{2} · \d+ trackers \([^\n]*\)\.(?=\n|\Z)".encode("utf-8"))
# FM-030, R9's two quick wins (exact text, RV-3296): what the candidate's board page may add beside the baseline's, specified here
# and matched exactly, each once — the ten lines of script the day adds, as written; four inert templates after the dialog, whose
# markup is fixed and whose text and label-valued attributes (the board's words, the four values) may vary; the prompts they copy,
# `,DAY={"standup": …, "closeout": …}` before `BRANCH=`; and the twenty-nine `day.*` words in the label table, by key. The answer's
# second screen copies through the day's clipboard helper: one line in place of its own three. Taken out, with FM-057's page
# (`fm057_page_dropped`), the page is the baseline's.
DAY_SCRIPT = tuple(("\n" + line).encode("utf-8") for line in (
    "// FM-030 day: the one clipboard path — the answer's second screen (FM-013), the stand-up's and the close-out's dialog: *Copied* only when the clipboard",
    "// FM-030 day: said so, else the line that says to select the text and copy it (a board opened from a file often has no clipboard)",
    'clip=(d,text)=>{const out=d.querySelector(".said"),copy=()=>(navigator.clipboard?.writeText?navigator.clipboard.writeText(text):Promise.reject())   // FM-030 day',
    '  .then(()=>out.textContent=L["answer.sign.copied"],()=>out.textContent=L["answer.sign.nocopy"]);d.querySelector(".copy").onclick=copy;copy()},   // FM-030 day',
    "// FM-030 day: R9's two quick wins — the stand-up's and the close-out's dialog, rendered by the generator with its values checked (`day_html`). It",
    "// FM-030 day: copies the prompt as the answer's second screen copies its command; where a value failed it holds the line that names it, and nothing to copy",
    'function DAYOPEN(k){const d=$("dlg");d.innerHTML=$("day-"+k).innerHTML;if(DAY[k])clip(d,DAY[k]);d.showModal();d.querySelector(".go").focus()}   // FM-030 day',
    "    // FM-030 day: the stand-up opens the day, before the sessions of the last day; the close-out ends the box, below (rows `day_html` renders)",
    '    +"\\n\\n"+$("day-row-standup").innerHTML   // FM-030 day',
    '  if(gname=="board"&&!q)$("p").insertAdjacentHTML("beforeend","\\n\\n"+$("day-row-closeout").innerHTML);   // FM-030 day: the close-out ends the box',
))
_T, _A = rb"[^<>]*", rb'[^"<>]*'                    # text, and an attribute's value: what may vary, never markup
_C = rb"(?:[^<>]|<code>[^<>]*</code>)*"              # text with code spans: a command, a path, a value shown
_REST = (rb"<h4>" + _T + rb"</h4><p>" + _T + rb"</p><h4>" + _T + rb"</h4><p>" + _C + rb"</p><h4>" + _T + rb"</h4><p>" + _T + rb'</p><p class="ddim">' + _T
         + rb'</p><menu><button value="done" class="go">' + _T + rb"</button></menu></form></template>")
DAY_TEMPLATES = tuple(re.compile(t) for k in (b"standup", b"closeout") for t in (
    rb'\n<template id="day-row-' + k + rb'"><b>' + _T + rb'</b><span class="m">' + _T + rb'</span> <button class="act" type="button" onclick="DAYOPEN\(\''
    + k + rb'\'\)" aria-label="' + _A + rb'">' + _T + rb"</button></template>",
    rb'\n<template id="day-' + k + rb'"><form method="dialog" class="sign"><h3>' + _T + rb"</h3>(?:"
    + rb'<p class="dp">' + _T + rb'</p><pre class="cmd">' + _T + rb'</pre><p class="m ddim"><button type="button" class="copy" aria-label="' + _A + rb'">' + _T
    + rb'</button><span class="said" aria-live="polite"></span></p>' + rb'|(?:<p class="dp hot">' + _C + rb"</p>)+)" + _REST))
_J = rb'"(?:[^"\\]|\\.)*"'                           # a JSON string
DAY_DATA = re.compile(rb',DAY=\{"standup": ' + _J + rb', "closeout": ' + _J + rb"\}(?=,BRANCH=)")
DAY_KEYS = ("day.standup.title", "day.standup.row", "day.standup.button", "day.standup.spoken", "day.closeout.title", "day.closeout.row",
            "day.closeout.button", "day.closeout.spoken", "day.standup.dialog", "day.closeout.dialog", "day.paste", "day.asks", "day.standup.asks",
            "day.closeout.asks", "day.runs", "day.standup.runs", "day.closeout.runs", "day.not", "day.not.text", "day.fixed", "day.refused",
            "day.refused.chars", "day.refused.long", "day.refused.none", "day.refused.split", "day.value.name", "day.value.path", "day.value.cmd",
            "day.value.branch")
DAY_LABELS = tuple(re.compile(rb', "' + re.escape(k.encode()) + rb'": ' + _J) for k in DAY_KEYS)
DAY_SIGN = (b'      clip(d,line);d.querySelector(".go").focus()};\n',
            b'      const out=d.querySelector(".said"),copy=()=>(navigator.clipboard?.writeText?navigator.clipboard.writeText(line):Promise.reject())\n'
            b'        .then(()=>out.textContent=L["answer.sign.copied"],()=>out.textContent=L["answer.sign.nocopy"]);\n'
            b'      d.querySelector(".copy").onclick=copy;copy();d.querySelector(".go").focus()};\n')

# R13 (FM-032): `--since` and `--until` are named as R13's, where the 615fb1d baseline said they go with `--ratio`. The one
# difference the two ratio-window cases may show: that line in stderr, as each version prints it, and nothing else.
R13_CASES = ("ratio-window-before-queue", "check-ratio-window-before-queue")
R13_OLD = "--since and --until go with --ratio\n"
R13_NEW = "--since: R13, the Owner's ruling of 12 October, removed it with --ratio — no counting view replaces it until the receipts ship\n"


# The d-batch's schema case (FM-032, R15 and R13): where the 615fb1d baseline documented `freeze_at` and `freeze_tag` and said what
# `--ratio` counts of `[ratio] records` and `exclude`, `--schema` documents no key of the filing freeze (R15) and says what a move to
# `Shipped` reads (R13). One allowance for the one case: the two freeze rows gone, the two `[ratio]` rows rewritten, each still one row of
# its key — and nothing else: not the status, not stderr, no other line.
SCHEMA_CASE = "schema-check-priority"
R15_SCHEMA_ROWS = ("| `freeze_at` |", "| `freeze_tag` |")
R13_SCHEMA_ROWS = ("| `[ratio] records` |", "| `[ratio] exclude` |")


def r15_schema_dropped(observed):
    """(status, stdout, stderr) of a baseline run of the schema case without R15's two rows; None where either is not there once."""
    lines = observed["stdout"].split("\n")
    if any(sum(line.startswith(row) for line in lines) != 1 for row in R15_SCHEMA_ROWS):
        return None
    return observed["status"], "\n".join(line for line in lines if not line.startswith(R15_SCHEMA_ROWS)), observed["stderr"]


def r13_schema_matches(before, after):
    """Whether a candidate's run of the schema case matches the baseline's but for R13's two `[ratio]` rows, each still one row of its key."""
    if (before["status"], before["stderr"]) != (after["status"], after["stderr"]):
        return False
    old, new = before["stdout"].split("\n"), after["stdout"].split("\n")
    if len(old) != len(new) or any(sum(line.startswith(row) for line in lines) != 1 for row in R13_SCHEMA_ROWS for lines in (old, new)):
        return False
    return all(any(a.startswith(row) and b.startswith(row) for row in R13_SCHEMA_ROWS) for a, b in zip(old, new) if a != b)


def schema_matches(before, after):
    """Whether a candidate's run of the schema case matches the baseline's with R15's two freeze rows dropped — each there once in the
    baseline, neither in the candidate — and R13's two `[ratio]` rows rewritten, nothing else differing (`r13_schema_matches`)."""
    dropped = r15_schema_dropped(before)
    if dropped is None or any(line.startswith(R15_SCHEMA_ROWS) for line in after["stdout"].split("\n")):
        return False
    return r13_schema_matches(dict(before, stdout=dropped[1]), after)


def r13_named(observed):
    """(status, stdout, stderr) of a baseline run of an R13 case, its one line said as R13 says it; None where that line is not there once."""
    if observed["stderr"].count(R13_OLD) != 1:
        return None
    return observed["status"], observed["stdout"], observed["stderr"].replace(R13_OLD, R13_NEW)


def r21_dropped(data):
    """The baseline's INDEX.md bytes without the header's separator and dated, counted line, removed once and in the header
    (before the first `## ` section) only. None where the header holds no such line."""
    head, sep, rest = data.partition(b"\n## ")
    head, found = R21_LINE.subn(b"", head, count=1)
    return head + sep + rest if found else None


# FM-057 (the board says what it read, and when — the quick win beside R11): the candidate's board names its own moment. A run that writes it — the default
# run, here — reads HEAD and the branch before the page, where the baseline read the branch while it rendered and HEAD while it wrote `view/built.json`, and
# two things more, the paths changed and not committed; its page and `view/built.json` differ accordingly. The one difference the starts, the calls and those
# two files may show beside the 615fb1d baseline: every other start and call, in order, and every other file, byte for byte, still match; the page's rows are
# the baseline's, and `view/built.json` is the baseline's with the four fields of what it read added.
PAGE_PATH, BUILT_PATH = "work-tracker/index.html", "work-tracker/view/built.json"
FM057_MOVED = (("rev-parse", "--verify", "-q", "HEAD"), ("branch", "--show-current"))
FM057_READS = FM057_MOVED + (("diff", "--cached", "--name-only", "--no-renames", "-z"),
                             ("ls-files", "-z", "--modified", "--others", "--exclude-standard", "--directory", "--no-empty-directory"))
FM057_KEYS = {"built_at", "vcs", "branch", "changes"}
PAGE_ROWS = re.compile(rb"\bT=\[\n(.*?)\n\];", re.S)


def git_words(row):
    """What follows the program in a start (`argv`) or a call (its first argument), as a tuple — () where it is no argument list."""
    argv = row.get("argv") if "argv" in row else (row.get("args") or [None])[0]
    return tuple(str(word) for word in argv[1:]) if isinstance(argv, list) else ()


def fm057_rows(old, new, counted=True):
    """Whether the candidate's starts or calls `new` are the baseline's `old` but for FM-057: the two moved reads taken out where the baseline made them (the
    last of each), the reads of what the board read found together where the candidate makes them — the four of a run that counts the changed paths
    (`counted`), the two moved ones alone of the board's own run, `--html-only`, which reads no changed path — and every other row equal, in order; the moved
    reads as the baseline made them but where, and the two new ones from the same folder and environment."""
    reads = FM057_READS if counted else FM057_MOVED
    strip = lambda row: {key: value for key, value in row.items() if key != "product_stack"}
    o, n = list(old), list(new)
    moved = []
    for want in FM057_MOVED:
        at = [i for i, row in enumerate(o) if git_words(row) == want]
        if not at:
            return False
        moved.append(o.pop(at[-1]))
    block = [i for i in range(len(n) - len(reads) + 1) if tuple(git_words(row) for row in n[i:i + len(reads)]) == reads]
    if len(block) != 1:
        return False
    found = n[block[0]:block[0] + len(reads)]
    del n[block[0]:block[0] + len(reads)]
    how = lambda row: {key: value for key, value in strip(row).items() if key not in ("argv", "args", "raw", "executable", "result")}     # where and how it ran
    same = lambda a, b: how(a) == how(b)
    return ([strip(row) for row in o] == [strip(row) for row in n] and all(strip(a) == strip(b) for a, b in zip(moved, found[:2]))
            and all(same(found[0], row) for row in found[2:]))


def rows_match(old, new, counted=True):
    """The starts or calls of two runs: equal, or equal but for FM-057's reads (`fm057_rows`) — counted ones but on the board's own run."""
    strip = lambda rows: [{key: value for key, value in row.items() if key != "product_stack"} for row in rows]
    return strip(old) == strip(new) or fm057_rows(old, new, counted)


def fm057_board(baseline, candidate):
    """Whether the candidate's page and `view/built.json` are the baseline's but for FM-057, each read back from the bytes its run left — the hash in the
    snapshot checked: the page's rows (`T=[…]`) are the baseline's, and the record is the baseline's with exactly the four fields of what it read added — `vcs`
    git, `changes` a count (none on the board's own run, `--html-only`, which reads no changed path), `branch` a name or none, `built_at` a time with its
    offset."""
    def read(observed, path):
        held = (observed.get("board_after") or {}).get(path)
        data = base64.b64decode(held["bytes_base64"]) if isinstance(held, dict) else None
        return data if data is not None and hashlib.sha256(data).hexdigest() == observed["after"].get(path) else None
    pages, records = [read(o, PAGE_PATH) for o in (baseline, candidate)], [read(o, BUILT_PATH) for o in (baseline, candidate)]
    if None in pages + records:
        return False
    rows = [PAGE_ROWS.search(page) for page in pages]
    try:
        old, new = (json.loads(record) for record in records)
        when = datetime.datetime.fromisoformat(new.get("built_at", ""))
    except (ValueError, TypeError, AttributeError):
        return False
    return (all(rows) and rows[0].group(1) == rows[1].group(1) and isinstance(old, dict) and isinstance(new, dict)
            and set(new) == set(old) | FM057_KEYS and not set(old) & FM057_KEYS and all(new[key] == old[key] for key in old)
            and new["vcs"] == "git" and (new["changes"] is None if "--html-only" in (candidate.get("flags") or []) else
                                         isinstance(new["changes"], int) and not isinstance(new["changes"], bool) and new["changes"] >= 0)
            and (new["branch"] is None or isinstance(new["branch"], str)) and when.tzinfo is not None)


def with_board(observed, path, data):
    """A copy of an observed run whose board file `path` held `data` after the run — for FM-057's allowance's controls."""
    return dict(observed, after=dict(observed["after"], **{path: hashlib.sha256(data).hexdigest()}),
                board_after=dict(observed.get("board_after") or {}, **{path: serial(data)}))


# FM-057's page (R11's read-at line, as reviewed): what the candidate's board page holds beside the baseline's, specified here and
# matched exactly, each once — the read-at line's style; the read-at line, whose commit, count of changed paths and time vary and
# nothing else does; the three lines of script that copy its rebuild command; the reload's comment, its first two lines rewritten;
# and the twenty-three `read.*` and `link.*` words in the label table, by key. Taken out, the page is the baseline's.
FM057_PAGE_LINES = tuple(("\n" + line).encode("utf-8") for line in (
    '#ra{color:var(--mute);font-size:12px;margin:-8px 0 12px;line-height:1.7}#ra code{font:12px "Berkeley Mono",ui-monospace,monospace;color:var(--dim)}#ra .said{margin-left:6px}',
    "// FM-057: the rebuild command beside what the board read, and when — copied on the dialog's path: *Copied* only when the clipboard says so",
    '$("rb").onclick=()=>(navigator.clipboard?.writeText?navigator.clipboard.writeText($("rc").textContent):Promise.reject())',
    '  .then(()=>$("rs").textContent=L["read.copied"],()=>$("rs").textContent=L["answer.sign.nocopy"]);',
))
FM057_READ_AT = re.compile("\n".encode() + re.escape('<p id="ra" class="m">read from main at ').encode() + rb"[0-9a-f]{7}"
                           + re.escape(" (no forge named in the configuration, so not linked) · ").encode()
                           + rb"(?:1 path changed and not committed|[0-9]+ paths changed and not committed|nothing changed and not committed|what is changed and not committed is not read here)"
                           + re.escape(" · built ").encode() + rb"[0-9]{4}-[0-9]{2}-[0-9]{2} [0-9]{2}:[0-9]{2} [+-][0-9]{2}:[0-9]{2}"
                           + re.escape(' · it reads its file again when you come back to it; nothing polls · rebuild it: <code id="rc">shoalmark --html-only</code>'
                                       '<button type="button" id="rb" class="act">copy</button><span id="rs" class="said" aria-live="polite"></span></p>').encode() + rb"(?=\n)")
FM057_RELOAD = ("// reload: begin — the board and its tracker pages (one page: `#=ID` is a tracker's) reload themselves when the tab is visible again, so a board rebuilt meanwhile — by an\n"
                "// explicit run, a commit or an act; no hook rebuilds it — is on the screen when the person comes back. The same page and nothing else: no poll, no timer, no second file, no server. Never while a dialog is open or a field\n").encode("utf-8"), \
               ("// reload: begin — the board and its tracker pages (one page: `#=ID` is a tracker's) reload themselves when the tab is visible again, so what a checkout, a merge or a pull\n"
                "// changed is on the screen when the person comes back. The same page and nothing else: no poll, no timer, no second file, no server. Never while a dialog is open or a field\n").encode("utf-8")
FM057_KEYS_SHOWN = ("read.git.branch", "read.git.detached", "read.git.unborn", "read.git.clean", "read.git.changed", "read.git.changed.one", "read.git.unread",
                    "read.svn", "read.svn.unread", "read.svn.new", "read.none", "read.none.why", "read.at", "read.self", "read.rebuild", "read.copy",
                    "read.unlinked", "link.unpushed", "link.noforge", "link.unknown", "link.noviewer", "link.nocommit", "read.copied")
FM057_LABELS = tuple(re.compile(rb', "' + re.escape(k.encode()) + rb'": ' + _J) for k in FM057_KEYS_SHOWN)


def fm057_page_dropped(data):
    """The candidate's board page without FM-057's page, each part taken out exactly once as specified above — the style line, the read-at line,
    the three script lines, the twenty-three words — and the reload's comment put back as the baseline's. None where any part is not there exactly
    once as written."""
    if data is None:
        return None
    for line in FM057_PAGE_LINES:
        if data.count(line + b"\n") != 1:
            return None
        data = data.replace(line + b"\n", b"\n", 1)
    for pattern in (FM057_READ_AT,) + FM057_LABELS:
        data, n = pattern.subn(b"", data)
        if n != 1:
            return None
    if data.count(FM057_RELOAD[0]) != 1:
        return None
    return data.replace(*FM057_RELOAD)


def day_dropped(data):
    """The candidate's board page without FM-030's day, each part taken out exactly once as specified above — the ten script lines, the
    four templates, the prompts' data, the twenty-nine words — and the answer's second screen's own three clipboard lines put back for
    the shared helper's call. None where any part is not there exactly once as written, so a line with anything more is no part."""
    for line in DAY_SCRIPT:
        if data.count(line + b"\n") != 1:
            return None
        data = data.replace(line + b"\n", b"\n", 1)
    for pattern in DAY_TEMPLATES + (DAY_DATA,) + DAY_LABELS:
        data, n = pattern.subn(b"", data)
        if n != 1:
            return None
    if data.count(DAY_SIGN[0]) != 1:
        return None
    return data.replace(*DAY_SIGN)

# FM-054 and FM-007 (v0.20.1): the board's page carries how an answer is proved, read as the gate reads it from the default branch's
# configuration (`PROOF`, `proof_reading`), and says it before *accept*. The page the 615fb1d baseline writes holds neither, and the
# board's run of the candidate reads that configuration: the second difference the consumer's snapshots may show, and the one in
# what is started — every start and `subprocess.run` call the candidate makes inside `proof_reading`, each a read (FM054_READS).
# The page is held to its difference byte for byte (RV-3308): FM054_PAGE_EDITS, applied in order to the baseline's page, each
# where it occurs exactly once, must give every byte of the candidate's, once FM-030's day and FM-057's page are taken out of it
# (`board_matches`) — and nothing else may differ. The starts and calls inside `proof_reading` are set aside before FM-057's rule
# reads them (`fm054_own`).
PROOF_MARK = b',PROOF={"state": '
FM054_READS = (("symbolic-ref",), ("rev-parse",), ("config", "--get"), ("cat-file", "--batch"), ("ls-tree",))
# FM-054's and FM-007's changes to the page of this fixture, as reviewed — (the baseline's text, the candidate's), each anchored on text
# the two share: the proof CSS; the signed commit step without the touch; the new labels (`answer.give.*`, `act.give.title`,
# `proof.*`); the page's PROOF (this fixture: no seat may answer, so *author only*); the dialog's comment and its proof line; the
# second screen read from PROOF; and the heading of *waiting for you* with the proof line
FM054_PAGE_EDITS = (
    ('#p .aq{display:inline-block;padding-left:2ch;font-size:12px;color:var(--mute)}\n',
     '#p .aq{display:inline-block;padding-left:2ch;font-size:12px;color:var(--mute)}\n/* the proof, a state (FM-007): its deciding word in ink, never framed; its consequence the line beneath, in the warning colour, never a box */\n#p .pw,#dlg .pw{color:var(--ink);font-weight:600}.cq{color:var(--coral)}#p .cq{display:inline-block;padding-left:2ch}#dlg .cq{margin:0 0 8px}\n'),
    ('"answer.sign.step.commit": "commits them, signed with your key — a hardware key waits for your touch"',
     '"answer.sign.step.commit": "commits them, signed with your key"'),
    ('"answer.sign.url": "https://shoalmark.github.io/shoalmark/signing.html", "answer.done": ',
     '"answer.sign.url": "https://shoalmark.github.io/shoalmark/signing.html", "answer.give.title": "Give your answer", "act.give.title": "Record your act", "answer.give.intro": "Your decision is made. A browser cannot write it into the repository — your terminal does, as you. Run this command:", "answer.give.step.commit": "commits them as you: this repository asks for no signature, so the commit proves the author only", "answer.give.step.commit.login": "the commit\'s author is your server login, as Subversion records it — with no signature", "answer.give.step.commit.none": "with no version control, nothing records who wrote them", "answer.give.check.text": "{0} prints your name — the author git reports, a string anyone can type.", "answer.give.fail.text": "It prints what refused it and takes back what it wrote; your words are printed again, with the command that gives them.", "proof.here": "your answers here: {0}", "proof.dialog": "your answer here: {0}", "proof.signed": "signed", "proof.author": "author only", "proof.login": "server login", "proof.none": "no author", "proof.author.why": "an answer here proves the author only: any session that can commit here can write one in your name", "answer.done": '),
    ('"viewer.none_in_progress": "none in progress"},BRANCH=',
     '"viewer.none_in_progress": "none in progress"},PROOF={"state": "author", "keys": {"title": "answer.give.title", "act": "act.give.title", "intro": "answer.give.intro", "commit": "answer.give.step.commit", "check": "answer.give.check.text", "fail": "answer.give.fail.text"}, "said": "author only", "format": "%an", "word": "proof.author", "why": "proof.author.why"},BRANCH='),
    ('    // three lines, commits SIGNED and pushes. A browser cannot sign; the dialog decides, the terminal signs.\n',
     "    // three lines, commits — signed where the default branch's configuration asks for it (FM-054) — and pushes. A browser cannot\n    // commit; the dialog decides, the terminal commits.\n"),
    ('        <p class="dq">${esc(ask)}</p>${prop?`<p class="dp"><b>${l("answer.proposal")}</b> ${esc(prop)}</p>`:""}<p class="m ddim">${esc(t[6])}</p>\n',
     '        <p class="dq">${esc(ask)}</p>${prop?`<p class="dp"><b>${l("answer.proposal")}</b> ${esc(prop)}</p>`:""}<p class="m ddim">${esc(t[6])}</p>\n        <p class="dp proof">${lh("proof.dialog",`<b class="pw">${l(PROOF.word)}</b>`)}</p>${PROOF.why?`<p class="cq">${l(PROOF.why)}</p>`:""}\n'),
    ('    // decision back. The decision is made; the terminal signs it. This screen says what to run, where, what it does step\n    // by step, what the end looks like, how to check it and where to go when signing fails — and has ONE way out, Done\n',
     '    // decision back. The decision is made; the terminal commits it. This screen says what to run, where, what it does step\n    // by step, what the end looks like, how to check it and where to go when it fails — and has ONE way out, Done\n'),
    ('    const sign=(d,id,line,said,kind="answer")=>{const br=`answer/${id.toLowerCase()}`,c=s=>`<code>${esc(s)}</code>`;\n      d.innerHTML=`<form method="dialog" class="sign"><h3>${l(kind=="answer"?"answer.sign.title":"act.sign.title")} · <a href="#=${id}">${id}</a></h3>\n        <p class="dp">${l("answer.sign.intro")}</p><pre class="cmd">${esc(line)}</pre',
     '    // FM-054: every line that says how the commit is proved is PROOF\'s — the default branch\'s configuration, as the gate and\n    // `--answer` read it (`proof_page`): *signed* only where it asks for a signature; the end previews the terminal\'s own word\n    const sign=(d,id,line,said,kind="answer")=>{const br=`answer/${id.toLowerCase()}`,c=s=>`<code>${esc(s)}</code>`,P=PROOF.keys;\n      d.innerHTML=`<form method="dialog" class="sign"><h3>${l(kind=="answer"?P.title:P.act)} · <a href="#=${id}">${id}</a></h3>\n        <p class="dp">${l(P.intro)}</p><pre class="cmd">${esc(line)}</pre'),
    ('        <li>${l("answer.sign.step.commit")}</li><li>${l("answer.sign.step.push")}</li></ol><p class="ddim">${l("answer.sign.slow")}</p>\n        <h4>${l("answer.sign.success")}</h4><pre>${esc(`${id} ${kind=="answer"?"answered: ":""}${said}\\n  signed, on \\`${br}\\`, pushed`)}</pre>\n        <h4>${l("answer.sign.check")}</h4><p>${lh("answer.sign.check.text",c(`git log -1 --format=%G? ${br}`),c("G"))}</p>\n        <h4>${l("answer.sign.fail")}</h4><p>${lh("answer.sign.fail.text",`<a href="${l("answer.sign.url")}" targ',
     '        <li>${l(P.commit)}</li><li>${l("answer.sign.step.push")}</li></ol><p class="ddim">${l("answer.sign.slow")}</p>\n        ${PROOF.said?`<h4>${l("answer.sign.success")}</h4><pre>${esc(`${id} ${kind=="answer"?"answered: ":""}${said}\\n  ${PROOF.said}, on \\`${br}\\`, pushed`)}</pre>`:""}\n        ${P.check?`<h4>${l("answer.sign.check")}</h4><p>${lh(P.check,c(`git log -1 --format=${PROOF.format} ${br}`),c("G"))}</p>`:""}\n        <h4>${l("answer.sign.fail")}</h4><p>${lh(P.fail,`<a href="${l("answer.sign.url")}" targ'),
    ('    return `<b class="${w.length?"hot":""}">${l("waiting.title")}: ${w.length}</b>`+(w.length?(old>=0?" · "+l("waiting.oldest",old):"")+(held.length?" · "+l("waiting.holds",held.length):"")+(w.length>5?" · "+l("waiting.bottleneck",w.length,held.length):"")+"\\n"+w.slice(0,14).map(t=>\n',
     '    return `<b class="${w.length?"hot":""}">${l("waiting.title")}: ${w.length}</b>`+(w.length?(old>=0?" · "+l("waiting.oldest",old):"")+(held.length?" · "+l("waiting.holds",held.length):"")+(w.length>5?" · "+l("waiting.bottleneck",w.length,held.length):"")\n      // FM-007: how an answer here is proved — the same for every ask on one repository\'s board, so said once, here, before *accept*:\n      // a state, its word in ink; where the author is all it proves, its consequence the line beneath, the warning colour\'s (PROOF, `proof_page`)\n      +" · "+lh("proof.here",`<b class="pw">${l(PROOF.word)}</b>`)+(PROOF.why?`\\n<span class="cq">${l(PROOF.why)}</span>`:"")+"\\n"+w.slice(0,14).map(t=>\n'),
)


def fm054_own(rows):
    """The starts, or `subprocess.run` calls, the candidate makes outside FM-054's reading: what the other rules compare."""
    return [row for row in rows if "proof_reading" not in (row.get("product_stack") or [])]


def fm054_reads(rows):
    """The starts, or `subprocess.run` calls, FM-054's reading makes: those with `proof_reading` on the tool's own stack."""
    return [row for row in rows if "proof_reading" in (row.get("product_stack") or [])]


def fm054_read(argv):
    """Whether one argv is a read FM-054's reading of the default branch's configuration may start: git, and one of FM054_READS."""
    argv = [str(a) for a in argv] if isinstance(argv, list) else []
    return (len(argv) > 1 and Path(argv[0]).name.lower() in ("git", "git.exe")
            and any(tuple(argv[1:1 + len(form)]) == form for form in FM054_READS))


def fm054_transform(page):
    """The baseline's page as FM-054 and FM-007 change it: FM054_PAGE_EDITS applied in order, each to text that occurs exactly once
    — else None: a page those edits do not fit is no page the allowance explains."""
    text = page.decode("utf-8")
    for old, new in FM054_PAGE_EDITS:
        if text.count(old) != 1:
            return None
        text = text.replace(old, new)
    return text.encode("utf-8")


def differs_only_by(baseline, candidate, path, key, rule):
    """Whether `path` after the run is the same file in both, or a file in both whose bytes, recorded under `key`, `rule(old, new)` allows."""
    old_hash, new_hash = baseline["after"].get(path), candidate["after"].get(path)
    if old_hash == new_hash:
        return True
    old_bytes, new_bytes = (base64.b64decode(row[key]["bytes_base64"]) if isinstance(row.get(key), dict) else None for row in (baseline, candidate))
    return (isinstance(old_hash, str) and isinstance(new_hash, str) and old_bytes is not None and new_bytes is not None
            and hashlib.sha256(old_bytes).hexdigest() == old_hash and hashlib.sha256(new_bytes).hexdigest() == new_hash and rule(old_bytes, new_bytes))


def board_matches(baseline, candidate):
    """The board's page and `view/built.json` after the run, each read back from the bytes the run left, its hash checked: the same in both; or the
    candidate's page with FM-030's day taken out (`day_dropped`), then FM-057's page (`fm057_page_dropped`), is the baseline's page with FM-054's
    edits applied (`fm054_transform`), every byte — the baseline's holding no PROOF — and the record is as `fm057_board` holds it."""
    if all(baseline["after"].get(path) == candidate["after"].get(path) for path in (PAGE_PATH, BUILT_PATH)):
        return True
    def page(observed):
        held = (observed.get("board_after") or {}).get(PAGE_PATH)
        data = base64.b64decode(held["bytes_base64"]) if isinstance(held, dict) else None
        return data if data is not None and hashlib.sha256(data).hexdigest() == observed["after"].get(PAGE_PATH) else None
    old_page, new_page = page(baseline), page(candidate)
    if old_page is None or new_page is None:
        return False
    if old_page != new_page:
        if PROOF_MARK in old_page or fm057_page_dropped(day_dropped(new_page)) != fm054_transform(old_page):
            return False
        candidate = with_board(candidate, PAGE_PATH, old_page)
    return fm057_board(baseline, candidate)


def snapshots_match(baseline, candidate):
    """The consumer's snapshots before the run are equal, and so are those after it — every path, byte, symlink, ref, config
    entry and hook — but for three named differences: INDEX.md after the run may differ where the baseline's, its header line
    dropped (`r21_dropped`, R21), is the candidate's bytes; the board page where the candidate's, FM-030's day and then FM-057's page
    taken out (`day_dropped`, `fm057_page_dropped`), is the baseline's bytes with FM-054's edits (`fm054_transform`); and
    `view/built.json` as `fm057_board` holds it (`board_matches`)."""
    if baseline["before"] != candidate["before"]:
        return False
    if baseline["after"] == candidate["after"]:
        return True
    old, new = dict(baseline["after"]), dict(candidate["after"])
    for path in (INDEX_PATH, PAGE_PATH, BUILT_PATH):
        old.pop(path, None), new.pop(path, None)
    return (old == new and differs_only_by(baseline, candidate, INDEX_PATH, "index_after", lambda o, n: r21_dropped(o) == n)
            and board_matches(baseline, candidate))


def with_index(observed, data, path=INDEX_PATH):
    """A copy of an observed run whose file `path` held `data` after the run — for the allowance's controls."""
    after = dict(observed["after"], **{path: hashlib.sha256(data).hexdigest()})
    return dict(observed, after=after, **({"index_after": serial(data)} if path == INDEX_PATH else {}))


def remove_tree(path):
    """`shutil.rmtree` that makes a refused entry writable and removes it again. Git writes its object files read-only, and Windows
    refuses to delete a read-only file (PR #173's run 38589202689, RV-3234). The handler is `onexc` from Python 3.12, `onerror` before."""
    def writable(function, target, _error):
        os.chmod(target, os.lstat(target).st_mode | stat.S_IWRITE)
        function(target)
    if sys.version_info >= (3, 12):
        shutil.rmtree(path, onexc=writable)
    else:
        shutil.rmtree(path, onerror=writable)


def serial(value):
    if isinstance(value, os.PathLike):
        return {"pathlike": os.fspath(value)}
    if isinstance(value, bytes):
        return {"bytes_base64": base64.b64encode(value).decode()}
    if isinstance(value, (tuple, list)):
        return [serial(item) for item in value]
    if isinstance(value, dict):
        return {str(key): serial(item) for key, item in sorted(value.items())}
    if value is None or isinstance(value, (str, int, float, bool)):
        return value
    return {"type": type(value).__name__}


def observe(spec):
    """Runs the actual __main__ entry, passively auditing/profile-observing it."""
    tool = str(Path(spec["tool"]).resolve())
    starts, calls, writes, entries = [], [], [], []
    active = [True]
    pending = {}

    def stack(frame=None):
        frame = frame or sys._getframe(1)
        names = []
        while frame:
            if frame.f_code.co_filename == tool:
                names.append(frame.f_code.co_name)
            frame = frame.f_back
        return list(reversed(names))

    def audit(event, arguments):
        if not active[0]:
            return
        if event == "subprocess.Popen":
            executable, argv, cwd, env = arguments
            starts.append({"executable": serial(executable), "argv": serial(argv),
                           "cwd": str(Path(os.fsdecode(cwd)).resolve()) if cwd is not None else os.getcwd(),
                           "environment": serial(dict(os.environ) if env is None else env),
                           "explicit_environment": env is not None, "product_stack": stack()})
            if executable is None and isinstance(argv, str):        # Windows' audit shape (RV-3061): `invoke` reads its argv back
                starts[-1]["raw"] = argv
        elif event == "open":
            path, mode, flags = arguments
            if flags & (os.O_WRONLY | os.O_RDWR | os.O_CREAT | os.O_TRUNC | os.O_APPEND):
                if isinstance(path, (str, bytes, os.PathLike)):
                    writes.append({"event": event, "path": os.path.abspath(os.fsdecode(path)), "flags": flags})
        elif event in ("os.mkdir", "os.remove", "os.rmdir", "os.rename", "os.symlink", "os.link", "os.chmod", "os.truncate"):
            row = {"event": event}
            for position in (0, 1) if event in ("os.rename", "os.symlink", "os.link") else (0,):
                raw = arguments[position]
                if isinstance(raw, (str, bytes, os.PathLike)):
                    row["path" if position == 0 else "destination"] = os.path.abspath(os.fsdecode(raw))
            writes.append(row)

    def profile(frame, event, result):
        if frame.f_code is subprocess.run.__code__:
            if event == "call":
                row = {"args": serial(frame.f_locals.get("popenargs")),
                       "options": serial(frame.f_locals.get("kwargs")),
                       "capture_output": frame.f_locals.get("capture_output"),
                       "timeout": frame.f_locals.get("timeout"),
                       "check": frame.f_locals.get("check"), "input": serial(frame.f_locals.get("input")),
                       "product_stack": stack(frame)}
                calls.append(row); pending[id(frame)] = row
            elif event == "return":
                row = pending.pop(id(frame), None)
                if row is not None:
                    row["result"] = ({"args": serial(result.args), "returncode": result.returncode,
                                      "stdout": serial(result.stdout), "stderr": serial(result.stderr)}
                                     if isinstance(result, subprocess.CompletedProcess) else {"type": type(result).__name__})
        if frame.f_code.co_filename == tool and frame.f_code.co_name == "main" and event == "return":
            entries.append({"result": serial(result), "ASK_ORIGIN": frame.f_globals.get("_ASK_ORIGIN"),
                            "WALK": frame.f_globals.get("_WALK"), "ROOT": str(frame.f_globals.get("ROOT")),
                            "COMMITTING": frame.f_globals.get("COMMITTING")})

    sys.addaudithook(audit)
    sys.setprofile(profile)
    sys.argv = [tool, *spec["argv"]]
    code = 0
    try:
        runpy.run_path(tool, run_name="__main__")
    except SystemExit as error:
        code = error.code if isinstance(error.code, int) else 1 if error.code else 0
    finally:
        sys.setprofile(None); active[0] = False
    report = {"starts": starts, "run_calls": calls, "writes": writes, "main_returns": entries}
    print(MARKER + json.dumps(report, ensure_ascii=True), file=sys.stderr)
    return code


def snapshot(root):
    """Consumer bytes, symlinks and stable Git administrative state; no index-stat cache."""
    files = {}
    for path in root.rglob("*"):
        rel = path.relative_to(root).as_posix()
        if rel.startswith(".git/") and not (rel in (".git/config", ".git/HEAD", ".git/packed-refs") or rel.startswith((".git/refs/", ".git/hooks/"))):
            continue
        if path.is_symlink():
            files[rel] = {"symlink": os.readlink(path)}
        elif path.is_file():
            files[rel] = hashlib.sha256(path.read_bytes()).hexdigest()
    return files


def clean_environment(top, git):
    # Controlled fixture environment; no inherited tokens or credential variables.
    home, temporary = top / "home", top / "temporary"
    home.mkdir(); temporary.mkdir()
    env = {key: os.environ[key] for key in ("SystemRoot", "WINDIR", "COMSPEC", "PATHEXT") if key in os.environ}
    paths = [str(Path(git).parent), str(Path(sys.executable).parent)]
    if os.name != "nt":
        paths += ["/usr/bin", "/bin"]
    env.update(PATH=os.pathsep.join(dict.fromkeys(paths)), HOME=str(home), USERPROFILE=str(home),
               TMPDIR=str(temporary), TMP=str(temporary), TEMP=str(temporary),
               LANG="C.UTF-8", LC_ALL="C.UTF-8", TZ="UTC", PYTHONDONTWRITEBYTECODE="1",
               GIT_CONFIG_NOSYSTEM="1", GIT_CONFIG_GLOBAL=os.devnull, GIT_TERMINAL_PROMPT="0",
               GIT_AUTHOR_NAME="fixture-only", GIT_AUTHOR_EMAIL="fixture@example.invalid",
               GIT_COMMITTER_NAME="fixture-only", GIT_COMMITTER_EMAIL="fixture@example.invalid",
               GIT_AUTHOR_DATE="2026-10-13T08:00:00+00:00", GIT_COMMITTER_DATE="2026-10-13T08:00:00+00:00",
               SHOALMARK_CMD="shoalmark")
    return env


def invoke(tool, root, flags, cwd, env):
    spec = {"tool": str(tool), "argv": ["--root", str(root), *flags]}
    before = snapshot(root)
    result = subprocess.run([sys.executable, "-B", str(Path(__file__).resolve()), "--observe", json.dumps(spec)],
                            cwd=cwd, env=env, capture_output=True, text=True, encoding="utf-8", errors="strict", timeout=45)
    lines = result.stderr.splitlines(keepends=True)
    markers = [line[len(MARKER):] for line in lines if line.startswith(MARKER)]
    if len(markers) != 1:
        raise AssertionError("actual observer did not complete: " + result.stderr[-1800:])
    report = json.loads(markers[0])
    if any("raw" in row for row in report["starts"]):
        from test_vcs_entry import read_back                        # the suite's reading of a Windows line (`fm.split_cmdline`), here in the parent
        for row in report["starts"]:
            if "raw" in row:
                row["argv"] = read_back(row["raw"])
    index = root / INDEX_PATH
    board = {path: serial((root / path).read_bytes()) for path in (PAGE_PATH, BUILT_PATH) if (root / path).is_file() and not (root / path).is_symlink()}
    report.update(status=result.returncode, stdout=result.stdout,
                  stderr="".join(line for line in lines if not line.startswith(MARKER)), before=before, after=snapshot(root),
                  index_after=serial(index.read_bytes()) if index.is_file() and not index.is_symlink() else None, board_after=board,
                  source_sha256=hashlib.sha256(tool.read_bytes()).hexdigest(), flags=flags,
                  invocation_cwd=str(cwd), consumer=str(root), invocation_environment=serial(env))
    return report


def run_git_entry_differentials(candidate, baseline, *, payload, check=None, report_path=None):
    """Portable proposed helper: returns evidence and boolean controls; P owns composition."""
    started = time.monotonic()
    git = shutil.which("git")
    if not git:
        raise RuntimeError("actual Git CLI differential controls require Git")
    candidate, baseline, payload = Path(candidate).resolve(), Path(baseline).resolve(), Path(payload).resolve()
    immutable = {"baseline": hashlib.sha256(baseline.read_bytes()).hexdigest(), "candidate": hashlib.sha256(candidate.read_bytes()).hexdigest()}
    rows, checks = [], []
    from test_vcs_entry import same_start                           # an exact start: Windows' raw line against list2cmdline, POSIX's list

    def assert_control(label, passed):
        checks.append({"name": label, "pass": bool(passed)})
        if check:
            check(label, bool(passed))

    cases = (
        ("clean-check-origin", ["--check"], "clean", True, True),
        ("dirty-check-fallback", ["--check"], "dirty", False, True),
        ("clean-default-origin", [], "clean", True, False),
        ("dirty-default-fallback", [], "dirty", False, False),
        ("schema-check-priority", ["--schema", "--check"], "clean", False, True),
        ("session-before-schema-new", ["--session-check", "--schema", "--new", "WORK", "ignored later title"], "pending-session", False, True),
        ("session-before-ratio-window", ["--session-check", "--since", "2026-10-01", "--schema"], "pending-session", False, True),
        ("check-print-written-priority", ["--check", "--print-written"], "clean", False, True),
        ("html-only-standalone-priority", ["--html-only", "--check"], "clean", False, True),
        ("ratio-window-before-queue", ["--since", "2026-10-01", "--queue"], "clean", False, True),
        ("check-ratio-window-before-queue", ["--check", "--since", "2026-10-01", "--queue"], "clean", False, True),
        ("related-check-before-origin", ["--related", "WORK-001", "--check"], "clean", False, True),
    )
    with tempfile.TemporaryDirectory(prefix="git-entry-", dir=HERE) as directory:
        top = Path(directory).resolve()
        env = clean_environment(top, git)
        root, source_home, launch = top / "consumer", top / "source", top / "launch"
        root.mkdir(); source_home.mkdir(); launch.mkdir()
        (launch / "shoalmark.toml").write_text('name = "decoy launch; never the consumer"\n')
        for name in PAYLOAD:
            target = source_home / name; target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(payload / name, target)
        tool = source_home / "shoalmark.py"
        tool.write_bytes(baseline.read_bytes())

        def setup(*args, cwd=root):
            return subprocess.run([git, *args], cwd=cwd, env=env, capture_output=True, check=True).stdout.decode()

        setup("-c", "init.templateDir=", "init", "-q", "--initial-branch=main")
        for key, value in (("user.name", "fixture-only"), ("user.email", "fixture@example.invalid"),
                           ("commit.gpgsign", "false"), ("core.autocrlf", "false"), ("seat.session", "12345678/builder-1")):
            setup("config", key, value)
        folder = root / "work-tracker"; folder.mkdir()
        config = 'name = "Git entry differential fixture"\ntracker_dir = "work-tracker"\n[seats]\nbuilder = "fixture@example.invalid"\n[kinds]\nWORK = "Work"\n'
        (root / "shoalmark.toml").write_text(config)
        (folder / "WORK-001-local.md").write_text('---\nid: WORK-001\nstatus: Proposed\nconsidered: none\nhook: "entry origin selection"\n---\n\n# WORK-001 — local\n\n## What is true now\n\nRead current local work.\n\n## Done when\n\nOrigin and local edits select the correct change.\n')
        (folder / "TRIAGE.md").write_text('# Triage\n\n## The intent\n\nRead local records.\n\n## The current path\n\nPrepare local entry behavior.\n')
        (root / "product.txt").write_text("product\n")
        (root / ".gitignore").write_text("work-tracker/index.html\nwork-tracker/view/\n")
        setup("add", "-A")
        setup("commit", "-qm", "WORK-001: fixture baseline\n\nSession: 12345678/builder-1")
        prepared = invoke(tool, root, [], launch, env)
        assert prepared["status"] == 0, prepared["stderr"]
        setup("add", "work-tracker/INDEX.md")
        setup("commit", "-qm", "WORK-001: generated fixture index\n\nSession: 12345678/builder-1")
        origin = top / "local-origin.git"
        setup("clone", "--bare", "-q", str(root), str(origin), cwd=top)
        setup("remote", "add", "origin", str(origin))
        setup("update-ref", "refs/remotes/origin/main", "HEAD")
        # Deliberately absent origin/HEAD requires a real local ls-remote on a clean walk.
        assert setup("status", "--porcelain", "--untracked-files=all") == ""
        saved = top / "saved-consumer"
        shutil.copytree(root, saved)

        # A real foreign repository supplies inherited hook context. All eight
        # contamination keys are present only during measured entry runs; setup
        # remains clean. If any survive nested_git_env, they redirect repository
        # reads or conflict over pathspec semantics instead of being inert labels.
        foreign = top / "foreign-hook-context"
        foreign.mkdir()
        setup("-c", "init.templateDir=", "init", "-q", "--initial-branch=foreign", cwd=foreign)
        setup("config", "commit.gpgsign", "false", cwd=foreign)
        (foreign / "foreign.txt").write_text("foreign repository; never the consumer\n")
        setup("add", "-A", cwd=foreign)
        setup("commit", "-qm", "disposable foreign hook context", cwd=foreign)
        poisoned_env = dict(env, GIT_DIR=str(foreign / ".git"), GIT_WORK_TREE=str(foreign),
                            GIT_INDEX_FILE=str(foreign / ".git" / "index"), GIT_PREFIX="foreign/",
                            GIT_LITERAL_PATHSPECS="1", GIT_ICASE_PATHSPECS="1",
                            GIT_GLOB_PATHSPECS="1", GIT_NOGLOB_PATHSPECS="1")
        foreign_before = snapshot(foreign)

        for label, flags, condition, ask, readonly in cases:
            pair = []
            for version, chosen in (("baseline", baseline), ("candidate", candidate)):
                remove_tree(root); shutil.copytree(saved, root)
                tool.write_bytes(chosen.read_bytes())
                if condition == "dirty":
                    (root / "product.txt").write_text("product local edit\n")
                elif condition == "pending-session":
                    (root / "product.txt").write_text("pending product edit\n")
                    setup("add", "product.txt"); setup("config", "seat.session", "malformed")
                initial_status = setup("status", "--porcelain", "--untracked-files=all")
                assert bool(initial_status) == (condition != "clean"), (label, initial_status)
                entry_env = poisoned_env if label in ("clean-check-origin", "dirty-check-fallback", "clean-default-origin", "dirty-default-fallback") else env
                observed = invoke(tool, root, flags, launch, entry_env)
                observed.update(case=label, version=version, initial_git_status=initial_status,
                                foreign_before=foreign_before, foreign_after=snapshot(foreign))
                rows.append(observed); pair.append(observed)
            before, after = pair
            label_prefix = "Git entry " + label + ": "
            said = (after["status"], after["stdout"], after["stderr"])
            if label in R13_CASES:
                assert_control(label_prefix + "actual stdout/stderr/status match immutable baseline, its one line named as R13 names `--since`",
                               r13_named(before) == said)
            elif label == SCHEMA_CASE:
                assert_control(label_prefix + "actual stdout/stderr/status match immutable baseline, but for `--schema`'s two freeze rows, gone (R15), "
                               "and its two `[ratio]` rows, rewritten (R13)", schema_matches(before, after))
            else:
                assert_control(label_prefix + "actual stdout/stderr/status match immutable baseline",
                               (before["status"], before["stdout"], before["stderr"]) == said)
            strip_stack = lambda entries: [{key: value for key, value in row.items() if key != "product_stack"} for row in entries]
            counted = "--html-only" not in flags                 # FM-057: the board's own run reads no changed paths
            assert_control(label_prefix + "all actual process argv/effective cwd/env match, but for FM-057's reads, and FM-054's reads of the default branch's "
                           "configuration set aside, each a read",
                           rows_match(before["starts"], fm054_own(after["starts"]), counted) and not fm054_reads(before["starts"])
                           and all(fm054_read(row["argv"]) for row in fm054_reads(after["starts"])))
            assert_control(label_prefix + "run options and actual process results match, but for FM-057's reads, and FM-054's reads set aside, each a read",
                           rows_match(before["run_calls"], fm054_own(after["run_calls"]), counted) and not fm054_reads(before["run_calls"])
                           and all(isinstance(row.get("args"), list) and row["args"] and fm054_read(row["args"][0]) for row in fm054_reads(after["run_calls"])))
            assert_control(label_prefix + "consumer byte/symlink/ref/config/hook snapshots match", snapshots_match(before, after))
            assert_control(label_prefix + "actual main state/result and selected origin policy match", before["main_returns"] == after["main_returns"]
                           and bool(after["main_returns"]) and after["main_returns"][-1]["ASK_ORIGIN"] is ask)
            assert_control(label_prefix + "Git entry emits no SVN limitation", "protected SVN acceptance" not in before["stdout"] + before["stderr"] + after["stdout"] + after["stderr"])
            assert_control(label_prefix + "production writes confined to disposable fixture", all(Path(value).is_relative_to(top)
                           for observed in pair for write in observed["writes"] for key, value in write.items() if key in ("path", "destination")))
            assert_control(label_prefix + "foreign hook repository bytes/refs/config remain unchanged", all(observed["foreign_before"] == observed["foreign_after"] for observed in pair))
            if readonly:
                assert_control(label_prefix + "read-only entry leaves consumer snapshot identical", all(observed["before"] == observed["after"] for observed in pair))
            if label in ("clean-check-origin", "dirty-check-fallback", "clean-default-origin", "dirty-default-fallback"):
                main_probe = lambda observed: [row for row in observed["starts"] if same_start(row["argv"], row.get("raw"), ["git", "diff", "--name-only", "--relative", "--ignore-submodules=none", "HEAD"])
                                              and "main" in row["product_stack"] and "worktree_edited" in row["product_stack"]
                                              and "read_changes" not in row["product_stack"]]
                probes = [main_probe(observed) for observed in pair]
                assert_control(label_prefix + "converted main probe actually runs once at consumer cwd", all(len(probe) == 1 and probe[0]["cwd"] == str(root) for probe in probes))
                assert_control(label_prefix + "converted probe drops all eight actual hook/pathspec contamination keys", all(set(POISON_KEYS).issubset(observed["invocation_environment"])
                               and len(probe) == 1 and not set(POISON_KEYS).intersection(probe[0]["environment"]) for observed, probe in zip(pair, probes)))
                assert_control(label_prefix + "candidate routes that probe through common boundary", all("vcs_process" in row["product_stack"] for row in probes[1])
                               and all("vcs_process" not in row["product_stack"] for row in probes[0]))
                if condition == "dirty":
                    assert_control(label_prefix + "dirty tree selects uncommitted fallback", all(observed["main_returns"][-1]["WALK"] == "uncommitted" for observed in pair))
                if label == "clean-default-origin":
                    assert_control(label_prefix + "clean default actually reads local origin once", all(sum(same_start(row["argv"], row.get("raw"), ["git", "ls-remote", "--symref", "origin", "HEAD"]) for row in observed["starts"]) == 1 for observed in pair))
                if label == "dirty-default-fallback":
                    assert_control(label_prefix + "dirty default asks no origin", all(not any(row["argv"][1:2] == ["ls-remote"] for row in observed["starts"]) for observed in pair))

        # R13's allowance is held to its one line on the real ratio-window pair: anything else the candidate says differently does not match.
        old13, new13 = (next(row for row in rows if row["case"] == R13_CASES[0] and row["version"] == version) for version in ("baseline", "candidate"))
        r13 = "Git entry R13 allowance: "
        assert_control(r13 + "the baseline says the one line once, and the candidate says R13's in its place and nothing else differs",
                       old13["stderr"].count(R13_OLD) == 1 and R13_OLD not in new13["stderr"] and r13_named(old13) == (new13["status"], new13["stdout"], new13["stderr"]))
        assert_control(r13 + "a candidate that also changes its exit, its stdout, or another line of stderr does not match",
                       r13_named(old13) != (0, new13["stdout"], new13["stderr"]) and r13_named(old13) != (new13["status"], new13["stdout"] + "more\n", new13["stderr"])
                       and r13_named(old13) != (new13["status"], new13["stdout"], new13["stderr"] + "one more line\n")
                       and r13_named(old13) != (new13["status"], new13["stdout"], new13["stderr"].replace("R13", "R14")))
        assert_control(r13 + "a baseline run that does not say the line once is not allowed at all",
                       r13_named(dict(old13, stderr="")) is None and r13_named(dict(old13, stderr=R13_OLD * 2)) is None)
        # The schema allowance is held to its four rows on the real schema pair: two gone, two rewritten, and nothing else.
        olds, news = (next(row for row in rows if row["case"] == SCHEMA_CASE and row["version"] == version) for version in ("baseline", "candidate"))
        schema, lines = "Git entry schema allowance (R15 and R13): ", news["stdout"].split("\n")
        other = next(i for i, line in enumerate(lines) if line.strip() and not line.startswith(R13_SCHEMA_ROWS))
        assert_control(schema + "the baseline holds each freeze row once and the candidate neither, the `[ratio]` rows are rewritten, and nothing else differs",
                       r15_schema_dropped(olds) is not None and not any(line.startswith(R15_SCHEMA_ROWS) for line in lines)
                       and olds["stdout"] != news["stdout"] and schema_matches(olds, news))
        assert_control(schema + "R15's half: a candidate that keeps a freeze row does not match, nor does the baseline itself",
                       not schema_matches(olds, dict(news, stdout=news["stdout"] + "| `freeze_at` | kept |\n"))
                       and not schema_matches(olds, dict(news, stdout=news["stdout"].replace(lines[other], lines[other] + "\n| `freeze_tag` | kept |", 1)))
                       and not schema_matches(olds, olds))
        assert_control(schema + "R13's half: a candidate that changes a line other than the two `[ratio]` rows, or drops or doubles a `[ratio]` row, does not match",
                       not schema_matches(olds, dict(news, stdout="\n".join(lines[:other] + [lines[other] + " changed"] + lines[other + 1:])))
                       and not schema_matches(olds, dict(news, stdout="\n".join(l for l in lines if not l.startswith(R13_SCHEMA_ROWS[1])) + "\n"))
                       and not schema_matches(olds, dict(news, stdout=news["stdout"].replace(R13_SCHEMA_ROWS[0], R13_SCHEMA_ROWS[1], 1))))
        assert_control(schema + "a schema that changes its exit or its stderr does not match, and a baseline that does not hold each freeze row once is not allowed at all",
                       not schema_matches(olds, dict(news, status=news["status"] + 1)) and not schema_matches(olds, dict(news, stderr=news["stderr"] + "x\n"))
                       and r15_schema_dropped(dict(olds, stdout="")) is None
                       and not schema_matches(dict(olds, stdout=olds["stdout"] + "| `freeze_tag` | twice |\n"), news))

        # R21's allowance is held to its one difference on the real default pair: equal snapshots match, and no variant below does.
        old, new = (next(row for row in rows if row["case"] == "clean-default-origin" and row["version"] == version) for version in ("baseline", "candidate"))
        old_index, new_index = (base64.b64decode(row["index_after"]["bytes_base64"]) for row in (old, new))
        line = R21_LINE.search(old_index)
        allowance = "Git entry R21 allowance: "
        assert_control(allowance + "the default run's INDEX.md differs by the header's dated, counted line alone, and equal snapshots still match",
                       old["after"] != new["after"] and r21_dropped(old_index) == new_index and snapshots_match(old, new) and snapshots_match(new, new))
        work = next(row for row in new_index.split(b"\n") if row.startswith(b"| [WORK-001]("))
        assert_control(allowance + "a candidate that also changes one row of INDEX.md does not match",
                       not snapshots_match(old, with_index(new, new_index.replace(work, work.replace(b"entry origin selection", b"entry origin, changed"), 1))))
        assert_control(allowance + "a candidate that writes another consumer file differently, or one more, does not match",
                       not snapshots_match(old, with_index(new, b"product, changed\n", "product.txt"))
                       and not snapshots_match(old, with_index(new, b"one more\n", "work-tracker/more.md"))
                       and not snapshots_match(dict(old, before=dict(old["before"], **{"product.txt": "0" * 64})), new))
        assert_control(allowance + "a `> Generated` line below the header, or a second one in it, is not removed and does not match",
                       bool(line) and not snapshots_match(with_index(old, new_index + line.group(0)[1:] + b"\n"), new)
                       and not snapshots_match(with_index(old, old_index.replace(line.group(0), line.group(0) * 2, 1)), new))
        # FM-057's allowance, held to its one difference on the same pair: the starts and calls by its reads alone, the page by its moment, the record by its four
        # fields — and no variant below matches.
        allowance = "Git entry FM-057 allowance: "
        new_starts, new_calls = fm054_own(new["starts"]), fm054_own(new["run_calls"])      # FM-054's reads set aside, as the rule sets them
        page, record = (base64.b64decode(new["board_after"][path]["bytes_base64"]) for path in (PAGE_PATH, BUILT_PATH))
        assert_control(allowance + "the default run's starts and calls differ by FM-057's reads alone, its page and record by what it read, and equal runs still match",
                       old["starts"] != new_starts and fm057_rows(old["starts"], new_starts) and fm057_rows(old["run_calls"], new_calls)
                       and fm057_board(old, new) and rows_match(new_starts, new_starts) and snapshots_match(new, new))
        extra = dict(new_starts[0], argv=new_starts[0]["argv"][:1] + ["status", "--porcelain"])
        at = next(i for i, row in enumerate(new_starts) if git_words(row) == FM057_READS[2])
        assert_control(allowance + "one start more, or FM-057's reads apart or with one missing, does not match",
                       not rows_match(old["starts"], new_starts + [extra])
                       and not rows_match(old["starts"], new_starts[:at] + [extra] + new_starts[at:])
                       and not rows_match(old["starts"], new_starts[:at] + new_starts[at + 1:]))
        bare = [row for row in new_starts if git_words(row) not in FM057_READS[2:]]      # the same run, as the board's own run reads: no changed path
        assert_control(allowance + "a run that reads no changed path, as the board's own run (`--html-only`) does, differs by the two moved reads alone; the "
                       "changed-path reads where none are read, or none where a run counts them, do not match",
                       len(bare) == len(new_starts) - 2 and fm057_rows(old["starts"], bare, counted=False)
                       and not fm057_rows(old["starts"], new_starts, counted=False) and not fm057_rows(old["starts"], bare, counted=True))
        row = PAGE_ROWS.search(page).group(1).split(b"\n")[0]
        built = json.loads(record)
        assert_control(allowance + "a page whose rows differ, or a record with a basis value changed, a field missing or a fifth field added, does not match",
                       not snapshots_match(old, with_board(new, PAGE_PATH, page.replace(row, row.replace(b"Proposed", b"Shipped"), 1)))
                       and not snapshots_match(old, with_board(new, BUILT_PATH, json.dumps(dict(built, trackers="0" * 64)).encode()))
                       and not snapshots_match(old, with_board(new, BUILT_PATH, json.dumps({k: v for k, v in built.items() if k != "changes"}).encode()))
                       and not snapshots_match(old, with_board(new, BUILT_PATH, json.dumps(dict(built, live=True)).encode())))
        # FM-030's allowance, held the same way: the page differs by the day's exact parts alone, beside FM-057's page, and no variant below matches (RV-3296).
        old_page, new_page = (base64.b64decode(row["board_after"][PAGE_PATH]["bytes_base64"]) if isinstance((row.get("board_after") or {}).get(PAGE_PATH), dict)
                              else b"" for row in (old, new))
        day = "Git entry FM-030 day allowance: "
        assert_control(day + "the default run's board page differs from the baseline's by the stand-up's and the close-out's exact script lines, "
                       "templates, prompts and words, and by FM-057's page and FM-054's edits, alone, and equal snapshots still match",
                       bool(old_page) and old_page != new_page and fm057_page_dropped(day_dropped(new_page)) == fm054_transform(old_page) and snapshots_match(old, new)
                       and snapshots_match(new, new))
        opener = b'd.querySelector(".go").focus()}   // FM-030 day'
        variants = {
            "one byte outside the day": new_page.replace(b'<dialog id="dlg"></dialog>', b'<dialog id="dlg" open></dialog>', 1),
            "a fifth template": new_page.replace(b'\n<template id="day-standup">', b'\n<template id="day-closeout"></template>\n<template id="day-standup">', 1),
            "one line's mark dropped": new_page.replace(b"   // FM-030 day\n", b"\n", 1),
            "an unrelated statement appended to a permitted line": new_page.replace(opener, b'd.querySelector(".go").focus();document.title="Unrelated title"}   // FM-030 day', 1),
            "markup inside a template's text": new_page.replace(b'<template id="day-row-standup"><b>', b'<template id="day-row-standup"><b><img src=x onerror=alert(1)>', 1),
            "an attribute added to a template's button": new_page.replace(b'onclick="DAYOPEN(\'standup\')"', b'onclick="DAYOPEN(\'standup\')" onfocus="alert(1)"', 1),
        }
        changed = {name: page != new_page for name, page in variants.items()}
        assert_control(day + "a candidate page that also changes one byte outside the day, carries a fifth template, drops one line's mark, appends an "
                       f"unrelated statement to a permitted line, or adds markup or an attribute to a template does not match (each variant made: {changed})",
                       all(changed.values()) and not any(snapshots_match(old, with_board(new, PAGE_PATH, page)) for page in variants.values()))
        # FM-057's page, held the same way beside the day: each of its parts taken out exactly once, and nothing else differs
        page057, read_at = "Git entry FM-057 page allowance: ", FM057_READ_AT.search(new_page)
        assert_control(page057 + "the default run's page, FM-030's day and then FM-057's page taken out, is the baseline's with FM-054's edits, every "
                       "byte; the baseline's page holds neither", bool(read_at) and fm057_page_dropped(day_dropped(new_page)) == fm054_transform(old_page)
                       and day_dropped(old_page) is None and fm057_page_dropped(old_page) is None)
        at = read_at.group(0) if read_at else b"\n"
        variants057 = {
            "one byte more in the read-at line": new_page.replace(at, at.replace(b"nothing polls", b"nothing polls!"), 1),
            "the read-at line twice": new_page.replace(at, at * 2, 1),
            "the read-at line's style gone": new_page.replace(FM057_PAGE_LINES[0] + b"\n", b"\n", 1),
            "a word FM-057 does not name, beside its own": new_page.replace(b'"read.copy": "copy"', b'"read.copy": "copy", "read.more": "more"', 1),
        }
        made057 = {name: page != new_page for name, page in variants057.items()}
        assert_control(page057 + "a page whose read-at line has one byte more or stands twice, whose read-at style is gone, or that holds a word FM-057 "
                       f"does not name does not match (each variant made: {made057})",
                       all(made057.values()) and not any(snapshots_match(old, with_board(new, PAGE_PATH, page)) for page in variants057.values()))
        # FM-054's allowance is held to its difference on the same pair: the page carries PROOF, and only `proof_reading`'s reads are new
        fm054 = "Git entry FM-054 allowance: "
        reads = fm054_reads(new["starts"])
        assert_control(fm054 + "the default run's board reads the default branch's configuration — starts inside `proof_reading`, each a read, which the baseline never makes",
                       bool(reads) and all(fm054_read(row["argv"]) for row in reads) and not fm054_reads(old["starts"]))
        unstacked = [dict(row, product_stack=[s for s in row["product_stack"] if s != "proof_reading"]) for row in new["starts"]]
        strip = lambda entries: [{key: value for key, value in row.items() if key != "product_stack"} for row in entries]
        assert_control(fm054 + "the same reads made outside `proof_reading` are not set aside, and do not match the baseline's starts",
                       not rows_match(old["starts"], fm054_own(unstacked)) and rows_match(old["starts"], fm054_own(new["starts"])))
        writes = [dict(row, argv=[row["argv"][0], "update-ref", "refs/heads/x", "HEAD"]) if row is reads[0] else row for row in new["starts"]] if reads else []
        assert_control(fm054 + "a start inside `proof_reading` that is not one of its reads is not one",
                       bool(writes) and not all(fm054_read(row["argv"]) for row in fm054_reads(writes)))
        page = base64.b64decode(new["board_after"][PAGE_PATH]["bytes_base64"]) if isinstance((new.get("board_after") or {}).get(PAGE_PATH), dict) else b""
        unproved = page.replace(PROOF_MARK, b',PRUEF={"state": ')
        as_page = lambda data: with_board(new, PAGE_PATH, data)
        unread = dict(new, board_after={k: v for k, v in (new.get("board_after") or {}).items() if k != PAGE_PATH})
        assert_control(fm054 + "the candidate's page carries PROOF, and a page that differs from the baseline's without it, or one not read back, does not match",
                       PROOF_MARK in page and snapshots_match(old, new) and not snapshots_match(old, as_page(unproved)) and not snapshots_match(old, unread))
        # RV-3308: the page is held byte for byte — the baseline's page with FM-054's edits is the candidate's; and two candidates that
        # keep PROOF_MARK, one without an unrelated section, one whose tracker row says something else, do not match
        section, row = b"#p summary{cursor:pointer}\n", b'"entry origin selection"'
        before_page = base64.b64decode(old["board_after"][PAGE_PATH]["bytes_base64"]) if isinstance((old.get("board_after") or {}).get(PAGE_PATH), dict) else b""
        assert_control(fm054 + "the candidate's page, FM-030's day and FM-057's page taken out, is the baseline's with FM054_PAGE_EDITS applied, every byte",
                       fm057_page_dropped(day_dropped(page)) == fm054_transform(before_page) and fm054_transform(page) is None)
        cut = page.replace(section, b"")
        assert_control(fm054 + "a page that keeps PROOF but deletes an unrelated section (`#p summary`'s rule) does not match",
                       page.count(section) == 1 and PROOF_MARK in cut and not snapshots_match(old, as_page(cut)))
        moved = page.replace(row, b'"entry origin, changed"')
        assert_control(fm054 + "a page that keeps PROOF but changes a tracker row (WORK-001's hook) does not match",
                       page.count(row) == 1 and PROOF_MARK in moved and not snapshots_match(old, as_page(moved)))
    assert immutable == {"baseline": hashlib.sha256(baseline.read_bytes()).hexdigest(), "candidate": hashlib.sha256(candidate.read_bytes()).hexdigest()}
    report = {"kind": "outside proposed Git entry differential evidence; no review/READY", "sources": immutable,
              "checks": checks, "cases": rows, "seconds": round(time.monotonic() - started, 3),
              "case_count": len(cases), "actual_entry_runs": len(rows), "actual_process_starts": sum(len(row["starts"]) for row in rows),
              "host": sys.platform, "python": sys.version, "git": subprocess.check_output([git, "--version"]).decode().strip(),
              "snapshot_scope": "all consumer non-administrative files/symlinks plus Git refs/config/HEAD/hooks; excludes Git object/index-stat caches"}
    if report_path:
        Path(report_path).write_text(json.dumps(report, indent=2) + "\n")
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--observe")
    parser.add_argument("--baseline", type=Path, default=HERE / "baseline.py")
    parser.add_argument("--candidate", type=Path, default=HERE / "candidate.py")
    parser.add_argument("--payload", type=Path, default=HERE / "payload")
    parser.add_argument("--report", type=Path, default=HERE / "differential-results.json")
    args = parser.parse_args()
    if args.observe:
        return observe(json.loads(args.observe))
    def check(label, passed):
        print(("ok   " if passed else "FAIL ") + label, flush=True)
    report = run_git_entry_differentials(args.candidate, args.baseline, payload=args.payload, check=check, report_path=args.report)
    print("%d/%d scoped Git entry controls passed; %d actual entry runs in %.3fs" %
          (sum(row["pass"] for row in report["checks"]), len(report["checks"]), report["actual_entry_runs"], report["seconds"]))
    return int(not all(row["pass"] for row in report["checks"]))


if __name__ == "__main__":
    raise SystemExit(main())
