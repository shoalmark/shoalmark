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
DAY_SCRIPT = tuple(("\n" + line).encode("utf-8") for line in (
    "// FM-030 day: the one clipboard path — the answer's second screen (FM-013), the stand-up's and the close-out's dialog: *Copied* only when the clipboard",
    "// FM-030 day: said so, else the line that says to select the text and copy it (a board opened from a file often has no clipboard)",
    'clip=(d,text)=>{const out=d.querySelector(".said"),copy=()=>(navigator.clipboard?.writeText?navigator.clipboard.writeText(text):Promise.reject())   // FM-030 day',
    '  .then(()=>{out.className="said ok";out.innerHTML=`<span class="go">${ICO.check}${l("day.copied")}</span>`},()=>{out.className="said";out.innerHTML=`<span class="hot">${ICO.cross}${l("day.nocopy")}</span>`});d.querySelector(".copy").onclick=copy;copy()},',
    "// FM-030 day: R9's two quick wins — the stand-up's and the close-out's dialog, rendered by the generator with its values checked (`day_html`). It",
    "// FM-030 day: copies the prompt as the answer's second screen copies its command; where a value failed it holds the line that names it, and nothing to copy",
    'function DAYOPEN(k){const d=$("dlg");d.innerHTML=$("day-"+k).innerHTML;if(DAY[k])clip(d,DAY[k]);d.showModal();d.querySelector(".go").focus()}   // FM-030 day',
    "    // FM-030 day: the stand-up opens the day, before the sessions of the last day; the close-out ends the box, below (rows `day_html` renders)",
    '    +"\\n\\n"+$("day-row-standup").innerHTML   // FM-030 day',
    '  if(gname=="board"&&!q)$("p").insertAdjacentHTML("beforeend","\\n\\n"+$("day-row-closeout").innerHTML);   // FM-030 day: the close-out ends the box',
))
_T, _A = rb"[^<>]*", rb'[^"<>]*'                    # text, and an attribute's value: what may vary, never markup
_C = rb"(?:[^<>]|<code>[^<>]*</code>)*"
_ICO = re.escape('<svg class="ico" viewBox="0 0 12 12" width="12" height="12" fill="currentColor" shape-rendering="crispEdges" aria-hidden="true"><path d="M0 4h8v1h-8ZM0 5h1v6h-1ZM7 5h1v6h-1ZM0 11h8v1h-8ZM4 0h8v1h-8ZM4 1h1v2h-1ZM11 1h1v7h-1ZM9 7h2v1h-2Z"></path></svg>').encode()
_REST = (rb"<h4>" + _T + rb"</h4><p>" + _T + rb"</p><h4>" + _T + rb"</h4><p>" + _C + rb'</p><p class="ddim">' + _T
         + rb'</p><menu><button value="done" class="go">' + _T + rb"</button></menu></form></template>")
DAY_TEMPLATES = tuple(re.compile(t) for k in (b"standup", b"closeout") for t in (
    rb'\n<template id="day-row-' + k + rb'"><span>' + _T + rb'</span> <span class="c">' + _T + rb'</span> (?:<button class="act" type="button" onclick="DAYOPEN\(\''
    + k + rb'\'\)" aria-label="' + _A + rb'">' + _ICO + _T + rb'</button>|(?:<span class="why hot">' + _C + rb"</span>)+)</template>",
    rb'\n<template id="day-' + k + rb'"><form method="dialog" class="sign"><h3>' + _T + rb"</h3>(?:"
    + rb'<p class="said" aria-live="polite"></p><p class="dp">' + _T + rb'</p><pre class="cmd">' + _T + rb'</pre><p class="m ddim"><button type="button" class="copy" aria-label="' + _A + rb'">' + _ICO + _T
    + rb'</button></p>' + rb'|(?:<p class="dp hot">' + _C + rb"</p>)+)" + _REST))
_J = rb'"(?:[^"\\]|\\.)*"'                           # a JSON string
DAY_DATA = re.compile(rb',DAY=\{"standup": ' + _J + rb', "closeout": ' + _J + rb"\}(?=,BRANCH=)")
DAY_KEYS = ("day.standup.title", "day.standup.row", "day.standup.button", "day.standup.spoken", "day.closeout.title", "day.closeout.row",
            "day.closeout.button", "day.closeout.spoken", "day.standup.dialog", "day.closeout.dialog", "day.paste", "day.asks", "day.standup.asks",
            "day.closeout.asks", "day.runs", "day.standup.runs", "day.closeout.runs", "day.fixed", "day.refused",
            "day.refused.chars", "day.refused.long", "day.refused.none", "day.refused.split", "day.value.name", "day.value.path", "day.value.cmd",
            "day.value.branch", "day.copied", "day.nocopy", "day.copy", "day.standup.asks.svn", "day.standup.asks.folder", "day.standup.runs.git",
            "day.standup.runs.svn", "day.standup.runs.folder")
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


def d_batch_schema_matches(before, after):
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


# FM-053 (A2, the board's v2 look): the candidate's board page may differ from the baseline's, which predates it, where every byte of the
# candidate's page is the baseline's with A2's reviewed edits applied (FM053_PAGE_EDITS, RV-3344); and `--schema` documents `[palette]` in
# one row of its table, its brand line naming what the board no longer reads. Those, beside R21's, are the only differences a candidate may
# show here. V2_MARK, the section band's token, is only a guard: the baseline's page never carries it.
V2_MARK = b"--secbg:"
# A2's changes to the page of this fixture, as reviewed — (the baseline's text, the candidate's), applied in order, each where it occurs exactly
# once: the template's rules and code, line by line where A2 rewrote them, and the labels one by one (a changed value, a retired key, the keys
# added after the one before them). The data blocks — the trackers, HOME, BRANCH, the board's own data — are never among them: they stay the
# baseline's bytes. Each later page change on this branch carries its edit here (BF-10 to BF-14 are in it)
FM053_PAGE_EDITS = (
    # the palette's tokens, light and dark, monochrome's (G1, G2)
    (':root{--bg:#f7f7f5;--ink:#161616;--dim:#565656;--mute:#6e6e6e;--line:rgba(0,0,0,.14);--teal:#1a7f5a;--coral:#b3402f;--blue:#2f62d6;--yellow:#946c0f}\n'
     '@media(prefers-color-scheme:dark){:root{--bg:#0e0e0e;--ink:#efefef;--dim:#ababab;--mute:#8f8f8f;--line:rgba(255,255,255,.15);--teal:#4fd1a1;--coral:#ff7b66;--blue:#6f9bff;--yellow:#e8cf5a}}\n',
     "/* the board's own look, `monochrome` on its base tokens (the design guide, §2, §5): every colour a token, written here from the palette the\n"
     '   board wears — `[palette]` in shoalmark.toml, monochrome by default */\n'
     ':root{--bg:#f7f7f5;--raise:#ececea;--ink:#161616;--dim:#565656;--mute:#6a6a6a;--line:rgba(0,0,0,.14);--box:rgba(0,0,0,.28);--coral:#b3402f;--teal:#187953;--amber:#8a5600;--owed:#8a5600;--help:#7b3fbf;--head:#161616;--idink:#161616;--secbg:#efefeb;--okbg:#e1f0e7;--warnbg:#fbf0d6;--failbg:#faeae6;--blue:#2f62d6;--yellow:#946c0f}\n'
     '@media(prefers-color-scheme:dark){:root{--bg:#0e0e0e;--raise:#1d1f24;--ink:#efefef;--dim:#ababab;--mute:#8f8f8f;--line:rgba(255,255,255,.15);--box:rgba(240,241,244,.26);--coral:#ff7b66;--teal:#4fd1a1;--amber:#f0b44c;--owed:#f0b44c;--help:#c09cff;--head:#efefef;--idink:#efefef;--secbg:#18191c;--okbg:#10271d;--warnbg:#2a200d;--failbg:#2c1612;--blue:#6f9bff;--yellow:#e8cf5a}}\n'),
    # the look: one face, one grid, the header and its search, buttons, bands and rows (RV-3342, BF-2, BF-5, BF-11, BF-14 among them)
    ('body{margin:0 auto;max-width:1100px;padding:24px 16px;background:var(--bg);color:var(--ink);font:15px/1.45 system-ui,sans-serif}\n'
     '.m,input,th,button{font-family:"Berkeley Mono",ui-monospace,monospace}\n'
     'header{display:flex;gap:12px;align-items:baseline;flex-wrap:wrap;margin-bottom:12px}\n'
     'input{flex:1;min-width:200px;padding:8px 0;border:0;border-bottom:1px solid var(--line);background:none;color:var(--ink);font-size:15px;outline:0}\n'
     'input:focus{border-color:var(--ink)}\n'
     'button{border:0;background:none;color:var(--mute);font-size:12px;letter-spacing:.06em;text-transform:uppercase;cursor:pointer;padding:0}\n'
     'button[aria-pressed=true]{color:var(--ink)}\n'
     '#n{color:var(--dim);font-size:13px}\n',
     "/* one face — the system's monospace, no font file ships — one grid, 14 px on a 21 px line, and a 104-character frame */\n"
     'body{margin:0 auto;max-width:calc(104ch + 32px);padding:16px 16px 40px;background:var(--bg);color:var(--ink);font:14px/21px "Berkeley Mono",ui-monospace,"SF Mono",Menlo,Consolas,"DejaVu Sans Mono",monospace}\n'
     'p{margin:0}\n'
     'input,button,textarea{font:inherit}\n'
     'a{color:inherit;text-decoration:none}a:hover{text-decoration:underline}\n'
     'a[href^="#="]{color:var(--idink);text-decoration:underline;text-underline-offset:3px;text-decoration-color:var(--mute)}\n'
     'i{font-style:italic}\n'
     "/* three meanings, one colour each (the guide's amendment, G1): teal done or success, amber a warning, coral a failure — each beside its word */\n"
     '.hot{color:var(--coral)}.go{color:var(--teal)}.warn{color:var(--amber)}.owed{color:var(--owed)}\n'
     'svg.ico{display:inline-block;width:12px;height:12px;vertical-align:-1px;margin-right:.7ch;flex:none}a svg.ico{margin:0 0 0 .7ch}\n'
     "/* the header line: the name, then the search as a prompt line — its box is the field's; the count stands in it. Where the line is short the\n"
     '   count wraps under the field, inside the box, and the field keeps its 200 px; on a phone the search takes a row of its own (RV-3342). The\n'
     "   count stands at the field's right edge, on the field's line where it fits and on a line of its own where it does not (BF-2) */\n"
     '#H{display:flex;flex-wrap:wrap;align-items:center;gap:4px 2ch;margin:6px 0 6px}#H img{height:22px;width:auto}\n'
     '#H>b{font-weight:600;color:var(--head);white-space:nowrap}#H>span{color:var(--mute)}#H>span:empty{display:none}\n'
     '#sb{flex:1 1 calc(200px + 4ch);display:flex;flex-wrap:wrap;align-items:center;column-gap:1ch;border:1px solid var(--mute);padding:0 1ch;min-width:0}\n'
     '#sb:before{content:">";content:">" / "";color:var(--mute)}#sb:focus-within{border-color:var(--ink)}\n'
     '#q{flex:1;min-width:200px;border:0;background:none;color:var(--ink);padding:3px 0;outline:0}#q::placeholder{color:var(--mute);opacity:1}\n'
     '#n{color:var(--dim);padding:3px 0;margin-left:auto;text-align:right}\n'
     '/* never a silent loss: each brand file the board no longer reads, and what replaces it — one line, there while a file is */\n'
     '#w{color:var(--amber);margin:0 0 4px}\n'
     "/* a box means an action; information is never boxed (the Owner's rule). A button is a word in a 1px frame — the frame in --mute, which carries\n"
     '   the meaning — with 1px by 1ch of padding, so it keeps the 21 px line; ink on --raise under the pointer; a visible focus ring */\n'
     'button{cursor:pointer}\n'
     'button.act,#s,#vt button,#dlg button{line-height:17px;border:1px solid var(--mute);background:none;color:var(--dim);padding:1px 1ch;margin:0 0 0 1ch;white-space:nowrap;vertical-align:baseline}\n'
     'button.act:hover,#s:hover,#vt button:hover,#dlg button:hover{background:var(--raise);color:var(--ink);border-color:var(--ink)}\n'
     'button:focus-visible,summary:focus-visible,a:focus-visible{outline:1px solid var(--ink);outline-offset:2px}\n'
     'button[aria-pressed=true]{color:var(--ink);border-color:var(--ink)}button:disabled{opacity:.4}\n'
     "/* the Owner's box: the one titled frame, its title set into its top border; inside, sections are `## ` headings with their counts, each\n"
     "   opening on its band (G2): from frame to frame — structure, not state. The band's top edge is a 1px --box rule, so the band is the divider\n"
     "   (G8): it holds where a band's faint fill does not, on a dim screen, in print, in forced colours; the first band has none, the box's frame\n"
     "   is right above it. A folded section is its band alone, --raise under the pointer; *waiting for you*'s band is amber's tint while asks\n"
     '   wait. A tint stands only for a state the tool computed, beside its word */\n'
     '#p{position:relative;border:1px solid var(--box);padding:14px 2ch 12px;margin:22px 0}\n'
     '#p>.pt{position:absolute;top:-11px;left:1ch;padding:0 1ch;background:var(--bg);font-weight:600;color:var(--head)}\n'
     '#p>.sec+.sec{margin-top:16px}.day>.sec+.sec{margin-top:12px}\n'
     '#p>.sec>.sh,#p>.sec>summary>.sh{background:var(--secbg);margin:0 -2ch 6px;padding:4px 2ch}#p>details.sec:not([open])>summary>.sh{margin-bottom:0}\n'
     '#p>.sec+.sec>.sh,#p>.sec+.sec>summary>.sh{border-top:1px solid var(--box)}\n'
     '#p>details.sec>summary:hover>.sh{background:var(--raise)}#p>.sec.wait>.sh{background:var(--warnbg)}\n'
     '.sh{font:inherit;font-weight:600;margin:0;display:flex;align-items:baseline;gap:0 1ch;color:var(--head)}.sh>span:first-child{flex:none}\n'
     '.sh .c{flex:1 1 auto;min-width:0;font-weight:400;color:var(--dim)}\n'
     '/* the drawn markers: drawn, never read */\n'
     'h2.sh:before{content:"##";content:"##" / "";display:inline-block;min-width:2ch;color:var(--mute);font-weight:400}\n'
     'h3.sh:before{content:"###";content:"###" / "";display:inline-block;min-width:3ch;color:var(--mute);font-weight:400}\n'
     'details>summary{list-style:none;cursor:pointer}details>summary::-webkit-details-marker{display:none}\n'
     'details.fold>summary .sh:before{content:">";content:">" / ""}details.fold[open]>summary .sh:before{content:"v";content:"v" / ""}\n'
     '.day{margin:6px 0 0}\n'
     '/* the row: what it is · TYPE · state … its actions, boxed, last; rows 3px apart, a rule between them. Rows line up (G4): the id in a column\n'
     '   of its own, 10ch; the question or title, and the state line under it, start on one column after it */\n'
     '.row{padding:3px 0;border-top:1px solid var(--line)}.sh+.row,.sub+.row,summary+.row{border-top:0}\n'
     '.what{display:grid;grid-template-columns:10ch 1fr;gap:0 1ch}.what>:first-child{justify-self:start}\n'
     '.how{display:flex;flex-wrap:wrap;align-items:baseline;gap:0 1ch;padding-left:11ch}.how .acts{margin-left:auto;white-space:nowrap}.acts button:first-child{margin-left:0}\n'
     "/* a verdict's row on its meaning's tint (G3), READY teal, READY WITH FINDINGS amber, NOT READY coral: its word in that colour at 600, and nothing else\n"
     '   on the row coloured */\n'
     '.row.vok,.row.vwarn,.row.vfail{margin:0 -2ch;padding:3px 2ch}.row.vok{background:var(--okbg)}.row.vwarn{background:var(--warnbg)}.row.vfail{background:var(--failbg)}\n'
     '.vok .ty{color:var(--teal);font-weight:600}.vwarn .ty{color:var(--amber);font-weight:600}.vfail .ty{color:var(--coral);font-weight:600}\n'
     '.ty{font-size:12px;letter-spacing:.06em;text-transform:uppercase;color:var(--dim);white-space:nowrap}\n'
     '.st{color:var(--dim)}.st b:not(.go):not(.hot):not(.warn){color:var(--ink)}.st b{font-weight:600}\n'
     '.aq{display:block;padding-left:11ch;color:var(--mute)}.sub{color:var(--dim);margin:8px 0 0}\n'
     '.lim{white-space:pre-line;color:var(--dim);padding:2px 0 0 2ch}\n'
     'details.grp>summary{padding:3px 0}details.grp .subs{display:block;padding-left:2ch;color:var(--dim)}details.grp>summary:before{content:">";content:">" / "";display:inline-block;min-width:2ch;color:var(--mute)}\n'
     'details.grp[open]>summary:before{content:"v";content:"v" / ""}details.grp .aq{padding-left:4ch}\n'
     'code{font:inherit}\n'
     '/* a name in a row moves to the next line whole, and breaks only where it is longer than a line (BF-11) */\n'
     '.row code{display:inline-block}\n'
     "/* the tool's own voice: help, behind a dashed rule — never a value, a state, an action or a warning */\n"
     '.help{color:var(--help);border-left:2px dashed var(--help);padding:0 0 0 1ch;margin:2px 0 6px}\n'
     "/* the work table, by rank: no outer box, its column heads types, its groups `// `, each group a fold — a group's line wraps inside the frame\n"
     "   (BF-1: `td.m`'s nowrap is the cells' alone) */\n"
     '#vt{display:flex;flex-wrap:wrap;align-items:baseline;gap:4px 1ch;margin:22px 0 6px}#vt button{margin:0}\n'
     '#l{color:var(--mute);font-size:12px;margin-left:auto}#l span{text-transform:lowercase;margin-right:1ch}\n'),
    # the work table's heads and cells; a group's line wraps (BF-1)
    ('th{text-align:left;color:var(--mute);font-size:11px;font-weight:400;letter-spacing:.08em;text-transform:uppercase;padding:6px 8px 6px 0}\n'
     'td{padding:7px 8px 7px 0;border-top:1px solid var(--line);vertical-align:top}\n'
     'td.m{font-size:13px;white-space:nowrap;color:var(--dim)}\n'
     'a{color:inherit;text-decoration:none}a:hover{text-decoration:underline}\n'
     'tr.t{cursor:pointer}\n'
     '.hot{color:var(--coral)}.go{color:var(--teal)}\n',
     'th{text-align:left;color:var(--mute);font-size:12px;font-weight:400;letter-spacing:.06em;text-transform:uppercase;padding:3px 2ch 3px 0}\n'
     '#B thead th{background:var(--secbg);padding:4px 2ch 4px 0}#B thead th:first-child,#b td:first-child{padding-left:1ch}\n'
     'td{padding:3px 2ch 3px 0;border-top:1px solid var(--line);vertical-align:top}\n'
     'td.m{white-space:nowrap;color:var(--dim)}\n'
     'tr.t{cursor:pointer}#b tr.c td:first-child{padding-left:3ch}\n'
     '.g td{border:0;padding:14px 0 2px;color:var(--dim);cursor:pointer;white-space:normal}.g td:before{content:"v ";content:"v " / "";color:var(--mute)}.g.f td:before{content:"> ";content:"> " / ""}\n'
     '.g b{color:var(--head);font-weight:600}.g b:before{content:"// ";content:"// " / "";color:var(--mute);font-weight:400}\n'
     '.s td{border:0;padding:0 0 6px 2ch;color:var(--dim);max-width:80ch}\n'
     '.h td{border:0;padding:0 2ch 8px 2ch;color:var(--dim)}.h a{margin-right:1ch}.off{color:var(--mute)}\n'
     '/* tags are chrome, not data: muted text — no pill, no border, no colour. Coral also marks P0/P1 */\n'
     '.k{font-size:12px;color:var(--mute);margin-left:1ch;white-space:nowrap}\n'),
    # the status marker's gap, in ch
    ('.q{display:inline-block;width:5px;height:5px;margin-right:8px;border:1px solid var(--mute);vertical-align:middle}\n',
     '.q{display:inline-block;width:5px;height:5px;margin-right:1ch;border:1px solid var(--mute);vertical-align:middle}\n'),
    # the old box's rules, retired
    ('#p{color:var(--dim);font-size:14px;white-space:pre-line;max-width:90ch;margin:4px 0 10px;padding-left:12px;border-left:2px solid var(--line)}\n'
     '#p a{color:var(--ink);text-decoration:underline}\n'
     '#l{color:var(--mute);font-size:11px;margin:0 0 10px}#l .q{margin:0 5px 0 12px}#l .q:first-child{margin-left:0}\n'
     'tr.c td:first-child{padding-left:20px}\n'
     '/* tags are chrome, not data: muted mono text — no pill, no border, no colour. Coral also marks\n'
     '   P0/P1 and teal marks live: both say what the square says — needs you now, and done. */\n'
     '.k{font-size:12px;color:var(--mute);margin-left:8px;white-space:nowrap}\n'
     '.h td{border:0;padding:0 8px 12px 0;color:var(--dim);font-size:14px}\n'
     '.h div{font-size:12px;margin-top:4px}.h a{margin-right:4px}.off{color:var(--mute)}\n'
     '.g td{border:0;padding:22px 0 4px;font-size:13px;color:var(--dim);cursor:pointer}\n'
     '.s td{border:0;padding:0 0 8px 14px;color:var(--dim);font-size:14px;max-width:80ch}.g b{color:var(--ink);font-weight:600;font-size:15px}\n'
     '/* the viewer — one tracker, rendered, READ-ONLY: no editing, no state, no server */\n'
     '#v{max-width:900px}#v .f{margin:6px 0 2px;white-space:normal}#v .md a{text-decoration:underline}\n'
     '#v h1{font-size:22px;margin:18px 0 10px}#v h2{font-size:17px;margin:28px 0 8px}#v h3,#v h4{font-size:15px;margin:20px 0 6px}\n'
     '#v table{display:block;overflow-x:auto;margin:12px 0;font-size:13px}#v th,#v td{padding-right:12px}#v li{margin:2px 0}\n'
     '#v code{font:13px "Berkeley Mono",ui-monospace,monospace;color:var(--dim)}#v pre{padding:12px;overflow:auto;border:1px solid var(--line)}\n'
     '#v [data-s]{cursor:pointer;text-decoration:underline}#v .toc{white-space:normal;line-height:1.9;margin:10px 0}\n'
     '#v blockquote{margin:12px 0;padding-left:12px;border-left:2px solid var(--line);color:var(--dim)}\n',
     ""),
    # the brand's rules (R10) give way to the viewer's, the box's and the dialogs'
    ('/* the brand: a logo, the name, a tagline — and a footer, all empty unless someone says otherwise. A wordmark takes the\n'
     "   place of the logo and the name, inline, so its currentColor is the name's ink: the size its height says, else the logo's */\n"
     '#H{display:flex;gap:10px;align-items:center;margin-bottom:14px}#H img{height:22px;width:auto}#H b{font-size:16px}#H .wm{display:flex}#H .wm svg{display:block;flex:none}#H .wm svg:not([height]){height:22px;width:auto}#s{margin-left:auto}#H span,#f{color:var(--mute);font-size:13px}\n'
     'button.act{border:1px solid var(--line);padding:2px 7px;margin-left:6px;font-size:11px;text-transform:none;letter-spacing:0}button.act:hover{border-color:var(--ink);color:var(--ink)}\n'
     '/* an act that is a promise: what they promised is its line, the question it answered below it, smaller — context, not the act (FM-030) */\n'
     '#p .aq{display:inline-block;padding-left:2ch;font-size:12px;color:var(--mute)}\n'
     '#p summary{cursor:pointer}\n'
     '#dlg{border:1px solid var(--line);background:var(--bg);color:var(--ink);max-width:640px;width:calc(100% - 32px);padding:18px 20px}#dlg::backdrop{background:rgba(0,0,0,.45)}\n'
     '#dlg h3{margin:0 0 10px;font-size:14px;font-weight:600}#dlg .dq{font-size:16px;font-weight:500;margin:0 0 8px;display:block}#dlg .dp{margin:0 0 8px;color:var(--dim)}#dlg .ddim{color:var(--mute);font-size:12px}\n'
     '#dlg .dl{display:flex;gap:8px;align-items:center;justify-content:flex-start;margin:8px 0 4px;font-size:14px}#dlg .dl input{margin:0;flex:0 0 auto;min-width:0;width:auto}#dlg textarea{width:100%;font:13px/1.4 system-ui,sans-serif;background:none;color:var(--ink);border:1px solid var(--line);padding:6px;margin-top:4px}#dlg textarea:disabled{opacity:.4}\n'
     '#dlg menu{display:flex;gap:8px;margin:14px 0 0;padding:0}#dlg button{border:1px solid var(--line);padding:6px 12px;font-size:12px}#dlg button.go{border-color:var(--ink);color:var(--ink)}#dlg button:disabled{opacity:.4}\n'
     '/* the second screen: the decision is made, the terminal signs it — the command, then where, what, the end, the check, the way out */\n'
     '#dlg h4{margin:14px 0 4px;font-size:11px;font-weight:400;letter-spacing:.08em;text-transform:uppercase;color:var(--mute)}#dlg ol{margin:4px 0;padding-left:20px}#dlg li{margin:2px 0}#dlg p{margin:4px 0}\n'
     '#dlg pre{font:13px/1.45 "Berkeley Mono",ui-monospace,monospace;margin:6px 0;padding:8px 10px;border:1px solid var(--line);white-space:pre-wrap;word-break:break-all}#dlg pre.cmd{border-left:2px solid var(--teal);user-select:all}\n'
     '#dlg code{font:12px "Berkeley Mono",ui-monospace,monospace}#dlg button.copy{padding:2px 8px;font-size:11px;text-transform:none;letter-spacing:0}#dlg .said{margin-left:6px}#dlg .sign a{text-decoration:underline}\n'
     '#l span{text-transform:lowercase}#f{margin-top:28px}#f:empty,#H span:empty{display:none}\n'
     "/* three hooks a theme styles (FM-002), none of them seen without one: the Owner's box's title `.pt`, the label\n"
     "   `owner.title`; the last line's one element `#F` — the claim `#f`, shown with the board only, as when it stood in it,\n"
     "   and the running line `#r`; `zebra` on every other row of a group, which `nth-child` cannot count past a group's head */\n"
     '.pt{display:none}#B[hidden]~#F #f{display:none}\n'
     "/* the running line: the tool's, on every screen, below the footer — its mark at 16 px, the smallest size its 16-unit grid\n"
     '   stays sharp at, and the name linking to the tool; the version to its release. Muted like any link here: underlined on hover */\n'
     '#r{display:flex;gap:.6em;align-items:center;margin:20px 0 0;color:var(--mute);font-size:11px;line-height:16px}#r a:first-child{display:flex;gap:6px;align-items:center}#r svg{flex:none}\n',
     '/* the viewer — one tracker, rendered, READ-ONLY: no editing, no state, no server. Hierarchy from weight and markers, not size */\n'
     '#v{max-width:104ch}#v .f{margin:6px 0 2px}#v .md a{text-decoration:underline}#v .hd b{font-weight:600}\n'
     '#v h1,#v h2,#v h3,#v h4{font-size:inherit;font-weight:600;margin:21px 0 0;color:var(--head)}#v p,#v ul,#v ol{margin:0 0 10px}\n'
     '#v .md h1:before{content:"# ";content:"# " / "";color:var(--mute);font-weight:400}#v .md h2:before{content:"## ";content:"## " / "";color:var(--mute);font-weight:400}\n'
     '#v .md h3:before{content:"### ";content:"### " / "";color:var(--mute);font-weight:400}\n'
     '#v table{display:block;overflow-x:auto;margin:10px 0}#v th,#v td{padding-right:2ch}#v li{margin:0}\n'
     '#v code{color:var(--dim)}#v pre{padding:0 0 0 2ch;overflow:auto;border-left:2px solid var(--line)}\n'
     '#v [data-s]{cursor:pointer;text-decoration:underline}#v .toc{white-space:normal;margin:10px 0}\n'
     '#v blockquote{margin:10px 0;padding-left:2ch;border-left:2px solid var(--line);color:var(--dim)}\n'
     "/* a dialog is a window: a 1px ink frame, its title set into the top border; its sections `## `; the command behind a 1ch teal rule on the page's\n"
     '   ground; the one button that goes ahead filled in ink */\n'
     '#dlg{border:0;padding:12px 0 0;background:none;color:var(--ink);max-width:76ch;width:calc(100% - 32px);overflow:auto}#dlg::backdrop{background:rgba(0,0,0,.45)}\n'
     '#dlg>form{position:relative;border:1px solid var(--ink);background:var(--bg);padding:18px 2ch 14px}\n'
     '#dlg h3{display:table;margin:-30px 0 10px -1ch;padding:0 1ch;background:var(--bg);font:inherit;font-weight:600}\n'
     '#dlg .dq{font-weight:600;margin:0 0 8px;display:block}#dlg .dp{margin:0 0 8px;color:var(--dim)}#dlg .ddim{color:var(--mute)}\n'
     '#dlg .dl{display:flex;gap:1ch;align-items:baseline;justify-content:flex-start;margin:2px 0}#dlg .dl input{margin:0;flex:0 0 auto;accent-color:var(--ink)}\n'
     '#dlg textarea,#dlg input[type=datetime-local]{width:100%;background:none;color:var(--ink);border:1px solid var(--mute);padding:1px 1ch;margin-top:4px}#dlg textarea:disabled{opacity:.4}\n'
     '#dlg menu{display:flex;justify-content:flex-end;gap:1ch;margin:14px 0 0;padding:0}#dlg menu button{margin:0}#dlg button.go{background:var(--ink);color:var(--bg);border-color:var(--ink)}\n'
     '#dlg h4{font:inherit;color:var(--dim);margin:14px 0 2px}#dlg h4:before{content:"## ";content:"## " / "";color:var(--mute)}\n'
     '#dlg ol{margin:2px 0;padding-left:4ch}#dlg li{margin:0}#dlg p{margin:0 0 4px}\n'
     '#dlg pre{font:inherit;margin:6px 0;padding:0 0 0 2ch;border-left:2px solid var(--line);white-space:pre-wrap;word-break:break-all}\n'
     '#dlg pre.cmd{border-left:1ch solid var(--teal);padding-left:1ch;user-select:all}\n'
     '#dlg .said{margin:0 0 8px}#dlg .said:empty{display:none}#dlg .said.ok{background:var(--okbg);margin:0 -2ch 8px;padding:2px 2ch}\n'
     "/* a diff (G5): the change a command commits — its path and +n −m on a band, the old and new line numbers, an added line on teal's tint behind a\n"
     "   teal +, a removed one on coral's behind a coral − */\n"
     '.diff{margin:6px 0 8px;border-bottom:1px solid var(--line)}.diff .dfh{display:flex;gap:1ch;padding:2px 1ch;background:var(--secbg)}.diff .dfh .dfn{margin-left:auto}\n'
     '.dfl{display:grid;grid-template-columns:3ch 3ch 1ch 1fr;gap:0 1ch;padding:0 1ch;white-space:pre-wrap;word-break:break-word}\n'
     '.dfl.add{background:var(--okbg)}.dfl.add .s{color:var(--teal)}.dfl.del{background:var(--failbg)}.dfl.del .s{color:var(--coral)}#dlg .sign a{text-decoration:underline}#dlg button.copy{margin:0}\n'
     "/* the claim and the running line: the last line's one element `#F`; the claim shown with the board only, as when it stood in it */\n"
     '#f{color:var(--mute);margin:28px 0 0}#f:empty{display:none}#B[hidden]~#F #f{display:none}\n'
     "/* the running line: the tool's, on every screen — its mark at 16 px, the smallest size its 16-unit grid stays sharp at, the name linking to\n"
     '   the tool and leaving the board; the version to its release */\n'
     '#r{display:flex;gap:1ch;align-items:center;margin:20px 0 0;color:var(--mute);font-size:12px;line-height:16px}#r a:first-child{display:flex;gap:6px;align-items:center}#r svg{flex:none}#r svg.ico{margin:0}\n'
     "/* a phone: at least 24 px for every button, a heading's state flows under its title, its marker keeping its space (BF-5); the search a header\n"
     "   row of its own, the scheme's button under it at the right edge (RV-3342) */\n"
     '@media(max-width:640px){button.act,#s,#vt button,#dlg button{min-height:24px;padding:3px 1ch}.sh{display:block}.sh:before{margin-right:1ch}.how .acts{display:block;margin:4px 0 0}\n'
     '#sb{flex-basis:100%}#s{margin-left:auto}}\n'
     "/* a phone: the work table, wider than the page with its columns as they are, scrolls in its own box — the header, the box and the toolbar stay put (BF-14) */\n"
     '@media(max-width:640px){#B>table{display:block;overflow-x:auto}}\n'),
    # the print rule
    ('@media print{#s{display:none}}\n'
     '@media print{:root{--bg:#fff;--ink:#000;--dim:#333;--mute:#555;--line:rgba(0,0,0,.25)}header,#l{display:none}}\n',
     '@media print{#s,#sb,#vt{display:none}:root{--bg:#fff;--ink:#000;--dim:#333;--mute:#555;--line:rgba(0,0,0,.25)}}\n'),
    # the header's markup: the search box and its counter; the box
    ('<div id="B"><div id="H"><b>Git entry differential fixture</b><span data-l="tagline"></span><button id="s"></button></div>\n'
     '<header><input id="q" autofocus>\n'
     '<button id="g" aria-pressed="true"></button><button id="o" aria-pressed="true" data-l="view.open"></button><button id="a" aria-pressed="false" data-l="view.all"></button><span id="n" class="m"></span></header>\n'
     '<p id="l" class="m"><i class="q"></i><span data-l="status.Proposed"></span><i class="q b"></i><span data-l="status.In Progress"></span><i class="q y"></i><span data-l="status.Parked"></span><i class="q r"></i><span data-l="status.Blocked"></span><i class="q t"></i><span data-l="status.Shipped"></span><i class="q z"></i><span data-l="status.Closed"></span></p>\n'
     '<p id="p"></p>\n',
     '<div id="B"><div id="H"><b>Git entry differential fixture</b><span data-l="tagline"></span><label id="sb"><input id="q" autofocus><span id="n"></span></label><button id="s"></button></div>\n'
     '<div id="p" class="box"></div>\n'
     '<div id="vt"><button id="g" aria-pressed="true"></button><button id="o" aria-pressed="true" data-l="view.open"></button><button id="a" aria-pressed="false" data-l="view.all"></button>\n'
     '<p id="l"><i class="q"></i><span data-l="status.Proposed"></span><i class="q b"></i><span data-l="status.In Progress"></span><i class="q y"></i><span data-l="status.Parked"></span><i class="q r"></i><span data-l="status.Blocked"></span><i class="q t"></i><span data-l="status.Shipped"></span><i class="q z"></i><span data-l="status.Closed"></span></p></div>\n'),
    # the footer's icon
    ('<p id="r" class="m"><a href="https://github.com/shoalmark/shoalmark" target="_blank" rel="noopener" aria-label="shoalmark on GitHub"><svg viewBox="0 0 16 16" width="16" height="16" fill="currentColor" shape-rendering="crispEdges" aria-hidden="true"><path d="M4 0h1v1h-1ZM11 0h1v1h-1ZM0 1h1v1h-1ZM4 1h1v1h-1ZM11 1h1v1h-1ZM15 1h1v1h-1ZM1 2h1v1h-1ZM5 2h1v1h-1ZM10 2h1v1h-1ZM14 2h1v1h-1ZM2 3h1v1h-1ZM5 3h1v1h-1ZM10 3h1v1h-1ZM13 3h1v1h-1ZM3 4h1v1h-1ZM6 4h1v1h-1ZM9 4h1v1h-1ZM12 4h1v1h-1ZM4 5h1v1h-1ZM6 5h1v1h-1ZM9 5h1v1h-1ZM11 5h1v1h-1ZM5 6h1v1h-1ZM7 6h2v1h-2ZM10 6h1v1h-1ZM6 7h4v1h-4ZM7 8h2v1h-2ZM7 9h2v1h-2ZM7 10h2v1h-2ZM7 11h2v1h-2ZM7 12h2v1h-2ZM7 13h2v1h-2ZM7 14h2v1h-2ZM7 15h2v1h-2Z"></path></svg>shoalmark</a> · <a href="https://github.com/shoalmark/shoalmark/releases/tag/v0.19.4" target="_blank" rel="noopener" aria-label="release v0.19.4">v0.19.4</a></p></footer>\n',
     '<p id="r" class="m"><a href="https://github.com/shoalmark/shoalmark" target="_blank" rel="noopener" aria-label="shoalmark on GitHub"><svg viewBox="0 0 16 16" width="16" height="16" fill="currentColor" shape-rendering="crispEdges" aria-hidden="true"><path d="M4 0h1v1h-1ZM11 0h1v1h-1ZM0 1h1v1h-1ZM4 1h1v1h-1ZM11 1h1v1h-1ZM15 1h1v1h-1ZM1 2h1v1h-1ZM5 2h1v1h-1ZM10 2h1v1h-1ZM14 2h1v1h-1ZM2 3h1v1h-1ZM5 3h1v1h-1ZM10 3h1v1h-1ZM13 3h1v1h-1ZM3 4h1v1h-1ZM6 4h1v1h-1ZM9 4h1v1h-1ZM12 4h1v1h-1ZM4 5h1v1h-1ZM6 5h1v1h-1ZM9 5h1v1h-1ZM11 5h1v1h-1ZM5 6h1v1h-1ZM7 6h2v1h-2ZM10 6h1v1h-1ZM6 7h4v1h-4ZM7 8h2v1h-2ZM7 9h2v1h-2ZM7 10h2v1h-2ZM7 11h2v1h-2ZM7 12h2v1h-2ZM7 13h2v1h-2ZM7 14h2v1h-2ZM7 15h2v1h-2Z"></path></svg>shoalmark<svg class="ico" viewBox="0 0 12 12" width="12" height="12" fill="currentColor" shape-rendering="crispEdges" aria-hidden="true"><path d="M0 2h4v1h-4ZM0 3h1v8h-1ZM9 8h1v3h-1ZM0 11h10v1h-10ZM6 0h6v1h-6ZM11 1h1v5h-1ZM10 1h1v1h-1ZM9 2h1v1h-1ZM8 3h1v1h-1ZM7 4h1v1h-1ZM6 5h1v1h-1ZM5 6h1v1h-1Z"></path></svg></a> · <a href="https://github.com/shoalmark/shoalmark/releases/tag/v0.19.4" target="_blank" rel="noopener" aria-label="release v0.19.4">v0.19.4</a></p></footer>\n'),
    # label section.ended
    ('"section.ended": "ended"',
     '"section.ended": "shipped or closed"'),
    # label desc.ended
    ('"desc.ended": "shipped, or closed without shipping"',
     '"desc.ended": ""'),
    # label owner.title
    ('"owner.title": "owed to the owner"',
     '"owner.title": "yours"'),
    # label path.title
    ('"path.title": "the current path"',
     '"path.title": "your current path"'),
    # label waiting.detail
    ('"waiting.detail": "open work whose next move is the Owner\'s"',
     '"waiting.detail": "open work whose next move is yours"'),
    # label act.done.title
    ('"act.done.title": "Done — where is the result?"',
     '"act.done.title": "done — where is the result?"'),
    # label act.due.title
    ('"act.due.title": "Reschedule — to when?"',
     '"act.due.title": "reschedule — to when?"'),
    # label way.revoke.title
    ('"way.revoke.title": "Revoke — why?"',
     '"way.revoke.title": "revoke — why?"'),
    # label sessions.recent
    ('"sessions.recent": "sessions · {0} in the last day ({1} with their sub-sessions)"',
     '"sessions.recent": "sessions · {0} with a commit in the last 24 hours ({1} with their sub-sessions)"'),
    # label reviews.untraced
    ('"reviews.untraced": "untraced {0}"',
     '"reviews.untraced": "{0} untraced"'),
    # label reviews.trunk
    ('"reviews.trunk": "on trunk {0}"',
     '"reviews.trunk": "{0} on trunk"'),
    # label answer.other
    ('"answer.other": "Other:"',
     '"answer.other": "other:"'),
    # label answer.ok
    ('"answer.ok": "OK — give me the command"',
     '"answer.ok": "ok — give me the command"'),
    # label answer.sign.title
    ('"answer.sign.title": "Sign your answer"',
     '"answer.sign.title": "sign your answer"'),
    # label act.sign.title
    ('"act.sign.title": "Sign your act"',
     '"act.sign.title": "sign your act"'),
    # label answer.sign.copy
    ('"answer.sign.copy": "Copy again"',
     '"answer.sign.copy": "command"'),
    # label answer.sign.copied
    ('"answer.sign.copied": "Copied."',
     '"answer.sign.copied": "the command is on your clipboard"'),
    # label answer.sign.nocopy
    ('"answer.sign.nocopy": "Not copied — this page has no clipboard here (a board opened from a file often has none). Select the command and copy it."',
     '"answer.sign.nocopy": "copying did not work — this page has no clipboard here (a board opened from a file often has none): select the command and copy it"'),
    # label answer.sign.where
    ('"answer.sign.where": "Where"',
     '"answer.sign.where": "where"'),
    # label answer.sign.does
    ('"answer.sign.does": "What it does"',
     '"answer.sign.does": "what it does"'),
    # label answer.sign.step.commit
    ('"answer.sign.step.commit": "commits them, signed with your key — a hardware key waits for your touch"',
     '"answer.sign.step.commit": "commits them, signed with your key — it may ask you to confirm"'),
    # label answer.sign.success
    ('"answer.sign.success": "When it worked"',
     '"answer.sign.success": "when it worked"'),
    # label answer.sign.check
    ('"answer.sign.check": "To check"',
     '"answer.sign.check": "to check"'),
    # label answer.sign.fail
    ('"answer.sign.fail": "If it fails"',
     '"answer.sign.fail": "if it fails"'),
    # label answer.done
    ('"answer.done": "Done"',
     '"answer.done": "done"'),
    # label ask.ruling
    ('"ask.ruling": "a ruling"',
     '"ask.ruling": "decision"'),
    # label ask.ceremony
    ('"ask.ceremony": "a button"',
     '"ask.ceremony": "one click"'),
    # label viewer.intent.missing
    ('"viewer.intent.missing": "missing — the Owner states it on the tracker or its story"',
     '"viewer.intent.missing": "missing — you state it on the tracker or its story"'),
    # label viewer.answer
    ('"viewer.answer": "the Owner\'s answer"',
     '"viewer.answer": "your answer"'),
    # label viewer.handover
    ('"viewer.handover": "hand-over"',
     '"viewer.handover": "handover"'),
    # label reviews.week retired
    (', "reviews.week": "reviews this week · independent {0} · same session {1}"',
     ""),
    # labels scheme.button added after scheme.dark
    ('"scheme.dark": "dark", ',
     '"scheme.dark": "dark", "scheme.button": "light or dark: {0}", '),
    # labels next.owner added after col.title
    ('"col.title": "title", ',
     '"col.title": "title", "next.owner": "you", '),
    # labels path.lines, path.line added after path.title
    ('"path.title": "your current path", ',
     '"path.title": "your current path", "path.lines": "{0} lines", "path.line": "1 line", '),
    # labels waiting.more added after waiting.malformed
    ('"waiting.malformed": "{0} asks sent back — not for you", ',
     '"waiting.malformed": "{0} asks sent back — not for you", "waiting.more": "and {0} more: the oldest are above", '),
    # labels day.title, day.span added after act.sign.step.revoke.answer
    ('"act.sign.step.revoke.answer": "writes {0} as revoked — the answer it takes back goes into the ship log", ',
     '"act.sign.step.revoke.answer": "writes {0} as revoked — the answer it takes back goes into the ship log", "day.title": "the day", "day.span": "the last 24 hours", '),
    # labels reviews.title, reviews.counts added after sessions.recent
    ('"sessions.recent": "sessions · {0} with a commit in the last 24 hours ({1} with their sub-sessions)", ',
     '"sessions.recent": "sessions · {0} with a commit in the last 24 hours ({1} with their sub-sessions)", "reviews.title": "reviews · this week", "reviews.counts": "{0} by another session · {1} by the same session", '),
    # labels reviews.reports, reviews.on, reviews.sessions, reviews.sessions.more, reviews.branch, reviews.branch.merged, reviews.branch.ambiguous, reviews.ambiguous, reviews.branch.unknown, reviews.branch.none, reviews.branch.unnamed, reviews.notready, reviews.findings, verdict.READY, verdict.READY WITH FINDINGS, verdict.READY TO TAG, verdict.NOT READY, reviews.word.another, reviews.word.same, reviews.word.untraced, reviews.word.trunk, type.act, type.answer, type.verdict added after reviews.trunk
    ('"reviews.trunk": "{0} on trunk", ',
     '"reviews.trunk": "{0} on trunk", "reviews.reports": "reports, not proofs", "reviews.on": "on {0}", "reviews.sessions": "its session {0}, the branch\'s {1}", "reviews.sessions.more": "{0} and {1} more", "reviews.branch": "branch {0}", "reviews.branch.merged": "branch {0}, as its merge {1} names it", "reviews.branch.ambiguous": "branch {0}: {1} each hold the verdict on their own line", "reviews.ambiguous": "ambiguous", "reviews.branch.unknown": "branch not known — {0}", "reviews.branch.none": "no branch here holds the verdict on its own line", "reviews.branch.unnamed": "its merge {0} names no branch", "reviews.notready": "{0} not ready", "reviews.findings": "{0} with findings", "verdict.READY": "ready", "verdict.READY WITH FINDINGS": "ready with findings", "verdict.READY TO TAG": "ready to tag", "verdict.NOT READY": "not ready", "reviews.word.another": "by another session", "reviews.word.same": "by the same session", "reviews.word.untraced": "untraced", "reviews.word.trunk": "on trunk — not a branch verdict", "type.act": "act", "type.answer": "answer", "type.verdict": "verdict", '),
    # labels answer.sign.copy.name added after answer.sign.copy
    ('"answer.sign.copy": "command", ',
     '"answer.sign.copy": "command", "answer.sign.copy.name": "copy the command", '),
    # labels brand.gone, brand.gone.theme, brand.gone.fonts, brand.gone.wordmark, brand.gone.themes added at the end
    ('"viewer.none_in_progress": "none in progress"}',
     '"viewer.none_in_progress": "none in progress", "brand.gone": "no longer read: {0}", "brand.gone.theme": "[palette] in shoalmark.toml", "brand.gone.fonts": "the system\'s monospace", "brand.gone.wordmark": "the name", "brand.gone.themes": "[palette], by name"}'),
    # the icons, ICO, after the labels
    (',BRANCH=',
     ',ICO={"copy": "\\u003csvg class=\\"ico\\" viewBox=\\"0 0 12 12\\" width=\\"12\\" height=\\"12\\" fill=\\"currentColor\\" shape-rendering=\\"crispEdges\\" aria-hidden=\\"true\\"\\u003e\\u003cpath d=\\"M0 4h8v1h-8ZM0 5h1v6h-1ZM7 5h1v6h-1ZM0 11h8v1h-8ZM4 0h8v1h-8ZM4 1h1v2h-1ZM11 1h1v7h-1ZM9 7h2v1h-2Z\\"\\u003e\\u003c/path\\u003e\\u003c/svg\\u003e", "check": "\\u003csvg class=\\"ico\\" viewBox=\\"0 0 12 12\\" width=\\"12\\" height=\\"12\\" fill=\\"currentColor\\" shape-rendering=\\"crispEdges\\" aria-hidden=\\"true\\"\\u003e\\u003cpath d=\\"M10 2h2v1h-2ZM9 3h2v1h-2ZM8 4h2v1h-2ZM7 5h2v1h-2ZM6 6h2v1h-2ZM1 5h2v1h-2ZM2 6h2v1h-2ZM3 7h4v1h-4ZM4 8h2v1h-2Z\\"\\u003e\\u003c/path\\u003e\\u003c/svg\\u003e", "cross": "\\u003csvg class=\\"ico\\" viewBox=\\"0 0 12 12\\" width=\\"12\\" height=\\"12\\" fill=\\"currentColor\\" shape-rendering=\\"crispEdges\\" aria-hidden=\\"true\\"\\u003e\\u003cpath d=\\"M2 2h2v1h-2ZM8 2h2v1h-2ZM3 3h2v1h-2ZM7 3h2v1h-2ZM4 4h4v1h-4ZM5 5h2v1h-2ZM4 6h4v1h-4ZM3 7h2v1h-2ZM7 7h2v1h-2ZM2 8h2v1h-2ZM8 8h2v1h-2Z\\"\\u003e\\u003c/path\\u003e\\u003c/svg\\u003e", "out": "\\u003csvg class=\\"ico\\" viewBox=\\"0 0 12 12\\" width=\\"12\\" height=\\"12\\" fill=\\"currentColor\\" shape-rendering=\\"crispEdges\\" aria-hidden=\\"true\\"\\u003e\\u003cpath d=\\"M0 2h4v1h-4ZM0 3h1v8h-1ZM9 8h1v3h-1ZM0 11h10v1h-10ZM6 0h6v1h-6ZM11 1h1v5h-1ZM10 1h1v1h-1ZM9 2h1v1h-1ZM8 3h1v1h-1ZM7 4h1v1h-1ZM6 5h1v1h-1ZM5 6h1v1h-1Z\\"\\u003e\\u003c/path\\u003e\\u003c/svg\\u003e"},BRANCH='),
    # the Owner's box, rendered (the guide's §1, §6, §8; RV-3343, BF-6, BF-9, BF-10)
    ('chips=(ids,arrow,to="~")=>ids.length?`<div class="m">${arrow} `+ids.map(i=>`<a href="#${to}${i}" class="${byId.has(i)&&OPEN.has(byId.get(i)[2])?"":"off"}">${i}</a>`).join(" ")+"</div>":"";\n',
     'chips=(ids,arrow,to="~")=>ids.length?`<div class="m">${arrow} `+ids.map(i=>`<a href="#${to}${i}" class="${byId.has(i)&&OPEN.has(byId.get(i)[2])?"":"off"}">${i}</a>`).join(" ")+"</div>":"";\n'
     "// THE OWNER'S BOX (the design guide, §1, §6, §8): its sections in the guide's order — waiting for you, your acts, what is on its way, the day, the\n"
     '// reviews, your current path — each a `## ` heading carrying its counts; each row reads what it is · TYPE · state … its actions, each in its box,\n'
     '// last. A heading said in one label is `title · its state`: the title is what comes before the first ` · `, the rest its state, the part that wraps\n'
     'const hd=(lv,title,state)=>`<${lv} class="sh"><span>${title}</span>${state?` <span class="c">${state}</span>`:""}</${lv}>`,\n'
     'sec=(h,body,cls)=>`<div class="sec${cls?" "+cls:""}">${h}${body}</div>`,\n'
     'fold=(h,body,open)=>`<details class="fold sec"${open?" open":""}><summary>${h}</summary>${body}</details>`,\n'
     '// rows line up (G4): the id in a column of its own, then what it is\n'
     'row=(id,what,ty,st,acts,more,cls)=>`<div class="row${cls?" "+cls:""}"><div class="what">${id}<span>${what}</span></div><div class="how">${ty?`<span class="ty">${ty}</span> `:""}${st?`<span class="st">${st}</span> `:""}${acts?`<span class="acts">${acts}</span>`:""}</div>${more||""}</div>`,\n'
     "// a verdict's word, as the reviewer gave it, and its meaning (G3): READY and READY WITH FINDINGS never read as a failure\n"
     'VERDICT={"READY":"vok","READY TO TAG":"vok","READY WITH FINDINGS":"vwarn","NOT READY":"vfail"},\n'
     '// a verb button names its act; its spoken name adds what it acts on, so a list of them never reads as one button said many times\n'
     'btn=(key,id,on)=>`<button class="act" aria-label="${l(key)} ${id}" onclick="${on}">${l(key)}</button>`,\n'
     'split=s=>{const i=s.indexOf(" · ");return i<0?[s,""]:[s.slice(0,i),s.slice(i+1)]},\n'
     'idl=id=>`<a href="#=${id}">${id}</a>`,\n'
     'days=t=>(d=>d==d?d:null)(ago(t[29][2])),\n'
     'PHONE=matchMedia("(max-width:640px)").matches;           // a phone: the day\'s sessions start folded, their heading still carrying the counts\n'
     "// an answer is the Owner's own commit: the button copies the three lines and opens the file on the forge under their login —\n"
     "// no server, no token, and the seat that asked is nowhere in the path. The commit's author is the proof.\n"
     '// Two buttons — accept · reject — open a dialog that shows the whole ask with its context, so the Owner can look and\n'
     '// abort. OK yields ONE command: `--answer <id> accept|reject "text"` — the tool cuts the answer branch, writes the\n'
     '// three lines, commits SIGNED and pushes. A browser cannot sign; the dialog decides, the terminal signs.\n'
     '// what the Owner typed goes into the copied command SINGLE-quoted: in "…" a shell runs a backtick and expands a `$` (R4)\n'
     'const sq=s=>"\'"+String(s).replace(/\'/g,"\'\\\\\'\'")+"\'";\n'
     'const act=(t,kind)=>{const d=$("dlg"),id=t[0],[ask,k,since,held,,prop,opts]=t[29],cmd="shoalmark";\n'
     '  const meta=[k?l("ask."+k):"",days(t)!=null?l("waiting.days",days(t)):"",held.length?l("waiting.holds.ids",held.join(", ")):""].filter(Boolean).join(" · ");\n'
     '  // an ask offers choices: one radio per option in the order given, except the RECOMMENDED one (`ask-proposal:`)\n'
     '  // which is offered first. A proposal alone is a list of one. Last always comes Other, with the box — and when\n'
     '  // there is nothing to choose from, Other is the only row and the box is the answer.\n'
     '  const all=opts&&opts.length?opts:(prop?[prop]:[]),ordered=prop&&all.includes(prop)?[prop,...all.filter(o=>o!=prop)]:all;\n'
     '  const rows=ordered.map((o,i)=>`<label class="dl"><input type="radio" name="how" value="${i}" required> <span>${esc(o)}`\n'
     '      +(o==prop?` <span class="ddim">— ${l("answer.recommended")}</span>`:"")+`</span></label>`).join("")\n'
     '    +`<label class="dl"><input type="radio" name="how" value="other" required${ordered.length?"":" checked"}> <span>${l("answer.other")}</span></label>`;\n'
     '  d.innerHTML=`<form method="dialog"><h3>${kind=="accept"?l("answer.accept"):l("answer.reject")} · <a href="#=${id}">${id}</a>${meta?` · <span class="m">${meta}</span>`:""}</h3>\n'
     '    <p class="dq">${esc(ask)}</p>${prop?`<p class="dp"><b>${l("answer.proposal")}</b> ${esc(prop)}</p>`:""}<p class="m ddim">${esc(t[6])}</p>\n'
     '    ${kind=="accept"?`${rows}<textarea name="text" rows="3" placeholder="${l("answer.change.hint")}"${ordered.length?" disabled":" required"}></textarea>`\n'
     '    :`<textarea name="text" rows="3" placeholder="${l("answer.reject.hint")}" required></textarea>`}\n'
     '    <menu><button value="ok" class="go">${l("answer.ok")}</button><button value="abort" formnovalidate>${l("answer.abort")}</button></menu></form>`;\n'
     '  const f=d.querySelector("form"),ta=f.text;\n'
     '  f.querySelectorAll("[name=how]").forEach(r=>r.onchange=()=>{ta.disabled=r.value!="other";ta.required=r.value=="other";if(!ta.disabled)ta.focus()});\n'
     '  f.onsubmit=e=>{if(e.submitter?.value!="ok")return;e.preventDefault();const q=s=>String(s).trim().replace(/"/g,"\'");\n'
     '    // the chosen option goes into the command VERBATIM — what the Owner picked is what the tracker records\n'
     '    const pick=f.how?.value,txt=q(ta.value||""),chosen=kind=="reject"||pick=="other"||pick==null?txt:q(ordered[+pick]);\n'
     '    const line=`${cmd} --answer ${id} ${kind}${chosen?" "+sq(chosen):""}`;\n'
     '    sign(d,id,line,(kind=="accept"?"accepted":"rejected")+(chosen?" - "+chosen.replace(/\\s+/g," "):""))};\n'
     '  d.showModal()};\n'
     '// THE SECOND SCREEN (FM-013). OK used to disable itself and leave one button — abort — which read as taking the\n'
     '// decision back. The decision is made; the terminal signs it. This screen says first whether the command is on the clipboard, then what to run,\n'
     '// where, what it does step by step, what the end looks like, how to check it and where to go when signing fails — and has ONE way out, done\n'
     "// (Esc too: it is the dialog's own). It says the command is on the clipboard only when the clipboard said so: from a file there may be none.\n"
     'const sign=(d,id,line,said,kind="answer")=>{const br=`answer/${id.toLowerCase()}`,c=s=>`<code>${esc(s)}</code>`;\n'
     '  d.innerHTML=`<form method="dialog" class="sign"><h3>${l(kind=="answer"?"answer.sign.title":"act.sign.title")} · <a href="#=${id}">${id}</a></h3>\n'
     '    <p class="said" aria-live="polite"></p>\n'
     '    <p class="dp">${l("answer.sign.intro")}</p><pre class="cmd">${esc(line)}</pre>\n'
     '    <p><button type="button" class="copy" aria-label="${l("answer.sign.copy.name")}">${ICO.copy}${l("answer.sign.copy")}</button></p>\n'
     '    <h4>${l("answer.sign.where")}</h4><p>${BRANCH?lh("answer.sign.where.branch",c(BRANCH)):l("answer.sign.where.text")}</p>\n'
     '    <h4>${l("answer.sign.does")}</h4><ol><li>${kind.startsWith("revoke")?lh("way.sign.step.on",c(br)):lh("answer.sign.step.cut",c(br))}</li><li>${kind=="answer"?lh("answer.sign.step.write",c("answer:"),c("answered:"),c("answered-by:"),c("next: "+(byId.get(id)?.[29][1]=="action"?"owner":"build"))):lh("act.sign.step."+kind,c(kind.replace("revoke.","")+":"),c("## Acts"))}</li>\n'
     '    <li>${l("answer.sign.step.commit")}</li><li>${l("answer.sign.step.push")}</li></ol><p class="ddim">${l("answer.sign.slow")}</p>\n'
     '    <h4>${l("answer.sign.success")}</h4><pre>${esc(`${id} ${kind=="answer"?"answered: ":""}${said}\\n  signed, on \\`${br}\\`, pushed`)}</pre>\n'
     '    <h4>${l("answer.sign.check")}</h4><p>${lh("answer.sign.check.text",c(`git log -1 --format=%G? ${br}`),c("G"))}</p>\n'
     '    <h4>${l("answer.sign.fail")}</h4><p>${lh("answer.sign.fail.text",`<a href="${l("answer.sign.url")}" target="_blank" rel="noopener">${l("answer.sign.page")}${ICO.out}</a>`)}</p>\n'
     '    <menu><button value="done" class="go">${l("answer.done")}</button></menu></form>`;\n'
     '  const out=d.querySelector(".said"),copy=()=>(navigator.clipboard?.writeText?navigator.clipboard.writeText(line):Promise.reject())\n'
     '    .then(()=>{out.className="said ok";out.innerHTML=`<span class="go">${ICO.check}${l("answer.sign.copied")}</span>`},()=>{out.className="said";out.innerHTML=`<span class="hot">${ICO.cross}${l("answer.sign.nocopy")}</span>`});\n'
     '  d.querySelector(".copy").onclick=copy;copy();d.querySelector("button.go").focus()};\n'
     '// FM-030: an act owed to the Owner has two buttons — done · reschedule. Each asks one thing — where the result is, or the\n'
     '// new time — and OK gives ONE command, `--done <id> "<where>"` or `--due <id> <time with its zone>`, on the same second\n'
     '// screen as an answer: a browser cannot sign; the terminal does.\n'
     'const owe=(t,kind)=>{const d=$("dlg"),id=t[0],a=t[30],cmd="shoalmark";\n'
     '  d.innerHTML=`<form method="dialog"><h3>${l(kind=="done"?"act.done.title":"act.due.title")} · <a href="#=${id}">${id}</a></h3>\n'
     '    <p class="dq">${esc(a[0])}</p>${a[5]?`<p class="ddim">${l("acts.asked",a[5])}</p>`:""}<p class="m ddim">${a[3]?l("acts.due",a[3].replace("T"," ")):l("acts.nodate")}</p>\n'
     '    ${kind=="done"?`<textarea name="text" rows="2" placeholder="${l(a[5]?"act.done.hint.promise":"act.done.hint")}" required></textarea>`:`<input name="when" type="datetime-local" required>`}\n'
     '    <menu><button value="ok" class="go">${l("answer.ok")}</button><button value="abort" formnovalidate>${l("answer.abort")}</button></menu></form>`;\n'
     '  const f=d.querySelector("form");\n'
     '  f.onsubmit=e=>{if(e.submitter?.value!="ok")return;e.preventDefault();\n'
     '    if(kind=="done"){const w=String(f.text.value).trim().replace(/\\s+/g," ").replace(/"/g,"\'");return sign(d,id,`${cmd} --done ${id} ${sq(w)}`,`done: ${w}`,"done")}\n'
     "    // the time the Owner picks is their machine's; the command carries its zone, so it means the same hour everywhere\n"
     '    const v=f.when.value,dt=new Date(v),o=-dt.getTimezoneOffset(),z=(o<0?"-":"+")+String(Math.floor(Math.abs(o)/60)).padStart(2,"0")+":"+String(Math.abs(o)%60).padStart(2,"0");\n'
     '    const iso=(v.length==16?v+":00":v)+z;sign(d,id,`${cmd} --due ${id} ${iso}`,`due: ${iso}`,"due")};\n'
     '  d.showModal()};\n'
     '// FM-030, their signed answer 920970b7: on what is on its way, *revoke* in the place of the buttons — one field, why; OK gives\n'
     '// ONE command, `--revoke <id> "<why>"`, on the same second screen: it commits on top of their act, on its branch\n'
     'const rev=t=>{const d=$("dlg"),id=t[0],w=t[31],cmd="shoalmark";\n'
     '  d.innerHTML=`<form method="dialog"><h3>${l("way.revoke.title")} · <a href="#=${id}">${id}</a></h3>\n'
     '    <p class="dq">${esc(w[7])}</p>${w[8]?`<p class="ddim">${l("acts.asked",w[8])}</p>`:""}<p class="m ddim">${l("way."+w[0])} · ${esc(w[1])} @ ${esc(w[3].slice(0,7))}</p>\n'
     '    <textarea name="text" rows="2" placeholder="${l("way.revoke.hint")}" required></textarea>\n'
     '    <menu><button value="ok" class="go">${l("answer.ok")}</button><button value="abort" formnovalidate>${l("answer.abort")}</button></menu></form>`;\n'
     '  const f=d.querySelector("form");\n'
     '  f.onsubmit=e=>{if(e.submitter?.value!="ok")return;e.preventDefault();const why=String(f.text.value).trim().replace(/\\s+/g," ").replace(/"/g,"\'");\n'
     '    sign(d,id,`${cmd} --revoke ${id} ${sq(why)}`,w[0]=="done"?`done revoked: ${why}`:`answered: revoked - ${why}`,w[0]=="done"?"revoke.done":"revoke.answer")};\n'
     '  d.showModal()};\n'
     'window.ACT=act;window.OWE=owe;window.REV=rev;\n'
     'function box(){\n'
     '  const S=[];\n'
     '  // ONLY what passes the ask rules is a question here — t[29][7] is why it is not. The Owner never reads a malformed\n'
     '  // ask as one; what was sent back is listed after the queue, with its reason, for the seat that wrote it.\n'
     '  const all_=T.filter(t=>OPEN.has(t[2])&&t[21]=="owner"&&!t[29][4]&&!(t[31]&&t[31][10])),w=all_.filter(t=>!t[29][7].length),sent=all_.filter(t=>t[29][7].length);\n'
     '  // the answer first: what needs the Owner — how many, how old, what it holds up — then each ask as the question it is, its kind its type\n'
     '  const old=Math.max(-1,...w.map(t=>days(t)??-1)),held=[...new Set(w.flatMap(t=>t[29][3]))];\n'
     '  w.sort((a,b)=>(days(b)??-1)-(days(a)??-1));\n'
     '  S.push(sec(hd("h2",`${l("waiting.title")}: <span class="${w.length?"owed":""}">${w.length}</span>`,\n'
     '      w.length?[old>=0?l("waiting.oldest",old):"",held.length?l("waiting.holds",held.length):"",w.length>5?l("waiting.bottleneck",w.length,held.length):""].filter(Boolean).map(s=>"· "+s).join(" "):""),\n'
     '    w.slice(0,14).map(t=>row(idl(t[0]),t[29][0]?esc(t[29][0]):`<i>${l("waiting.unasked")}</i> — ${esc(t[6])}`,t[29][1]?l("ask."+t[29][1]):"",\n'
     '      [days(t)!=null?l("waiting.days",days(t)):"",t[29][3].length?l("waiting.holds.ids",t[29][3].join(", ")):""].filter(Boolean).join(" · "),\n'
     '      t[29][0]?btn("answer.accept",t[0],`ACT(T.find(x=>x[0]==\'${t[0]}\'),\'accept\')`)+btn("answer.reject",t[0],`ACT(T.find(x=>x[0]==\'${t[0]}\'),\'reject\')`):"")).join("")\n'
     '    +(w.length>14?`<p class="sub">${l("waiting.more",w.length-14)}</p>`:"")\n'
     '    +(sent.length?`<p class="sub">${l("waiting.malformed",sent.length)}</p>`+sent.map(t=>row(idl(t[0]),t[29][0]?esc(t[29][0]):`<i>${l("waiting.unasked")}</i>`,"",esc(t[29][7][0]),"")).join(""):""),w.length?"wait":""));\n'
     '  // FM-030: what they owe, with its time — an accepted action ask, or any `due:` — each with its state by the clock above\n'
     '  const acts=T.filter(t=>t[30].length&&!(t[31]&&!t[31][11]));\n'
     '  if(acts.length)S.push(sec(hd("h2",`${l("acts.title")}: <span class="owed">${acts.length}</span>`,""),acts.map(t=>{\n'
     '    const a=t[30],s=actstate(a),when=a[3].replace("T"," ");\n'
     '    return row(idl(t[0]),esc(a[0]),l("type.act"),(a[1]?l("acts.promised",a[2],a[1])+" · ":"")\n'
     '        +`<b class="act-${s}${s=="overdue"?" warn":s=="missed"?" hot":""}">${s=="nodate"?l("acts.nodate"):s=="missed"?l("acts.missed",when,a[4]):l("acts."+s,when)}</b>`,\n'
     '      btn("acts.done",t[0],`OWE(T.find(x=>x[0]==\'${t[0]}\'),\'done\')`)+btn("acts.reschedule",t[0],`OWE(T.find(x=>x[0]==\'${t[0]}\'),\'due\')`),\n'
     '      a[5]?`<span class="aq">${l("acts.asked",a[5])}</span>`:"")}).join("")));\n'
     '  // FM-030, their signed answer 920970b7: the board reads git. What they did and pushed on `answer/<id>` is here, not in the two\n'
     '  // lists above, until their merge — their promise or their answer first, what it is, the branch, the commit, its time, whether it\n'
     '  // verifies, and that their merge is next\n'
     '  const way=T.filter(t=>t[31]);\n'
     '  if(way.length)S.push(sec(hd("h2",`${l("way.title")}: ${way.length}`,""),way.map(t=>{const w=t[31];\n'
     '    return row(idl(t[0]),esc(w[7]),l(w[0]=="answer"||w[0]=="revoked"?"type.answer":"type.act"),\n'
     '      `<b class="go">${l("way."+w[0])}</b>`+(w[13]?" — "+esc(w[13]):w[12]?" — "+l("acts.due",w[12].replace("T"," ")):"")\n'
     '        +` · ${esc(w[1])} @ ${esc(w[3].slice(0,7))} · ${esc(w[4].slice(0,16).replace("T"," "))} · ${w[6].startsWith("merge")?`<b class="go">${l("way.signed")}</b>`:`<span class="hot">${l("way.unverified",w[6].replace(/^wait: /,""))}</span>`} · ${w[14]?l("way.held",w[14].replace(/^wait: /,"")):l("way.merge")}`,\n'
     '      w[0]=="done"||w[0]=="answer"?btn("way.revoke",t[0],`REV(T.find(x=>x[0]==\'${t[0]}\'))`):"",\n'
     '      w[8]?`<span class="aq">${l("acts.asked",w[8])}</span>`:"")}).join("")));\n'
     '  // the registry, a report of the trailers (FM-024, FM-032): the day — who committed in the last 24 hours, where — one fold, open on a desktop\n'
     '  if(REG&&REG.groups.length){const [t0,st]=split(l("sessions.recent",REG.parents,REG.all));\n'
     '    S.push(sec(hd("h2",l("day.title"),"· "+l("day.span")),`<div class="day">`+fold(hd("h3",t0,st),REG.groups.map(g=>`<details class="grp"><summary>${esc(g[0])} ${esc(g[1])} (${esc(g[2])})${g[3].length?`<span class="subs">+ ${g[3].map(esc).join(" · ")}</span>`:""}</summary>`\n'
     '      +g[4].map(m=>`<span class="aq">${esc(m[0])} (${esc(m[1])}) · ${esc(m[2])} · ${esc(m[3])}</span>`).join("\\n")+"</details>").join(""),!PHONE)+"</div>"))}\n'
     "  // …and the week's verdicts and who gave them: folded, its heading carrying the counts in words — reports, not proofs; one row per verdict\n"
     "  // a verdict's branch (RV-3343): the one that holds the verdict on its own line, or the merge that names it; else ambiguous or not known, with why —\n"
     "  // in the row's own colour: nothing on a verdict's row is coloured but its word (G3, BF-10)\n"
     '  const brn=b=>b[0]=="line"?lh("reviews.branch",`<code>${esc(b[1])}</code>`):b[0]=="merge"?lh("reviews.branch.merged",`<code>${esc(b[1])}</code>`,`<code>${esc(b[2].slice(0,10))}</code>`)\n'
     '    :b[0]=="ambiguous"?lh("reviews.branch.ambiguous",l("reviews.ambiguous"),b[1].map(n=>`<code>${esc(n)}</code>`).join(", "))\n'
     '    :`<i>${lh("reviews.branch.unknown",b[0]=="unnamed"?lh("reviews.branch.unnamed",`<code>${esc(b[1].slice(0,10))}</code>`):l("reviews.branch.none"))}</i>`;\n'
     '  if(REG&&REG.reviews){const r=REG.reviews,[t0,st]=split(l("reviews.title")),word={"independent":"reviews.word.another","untraced":"reviews.word.untraced","on trunk":"reviews.word.trunk"};\n'
     '    S.push(fold(hd("h2",t0,[st,r[4]?`· <b class="hot">${l("reviews.notready",r[4])}</b>`:"",r[5]?`· <b class="warn">${l("reviews.findings",r[5])}</b>`:"",\n'
     '        "· "+l("reviews.counts",r[0],r[1]),r[2]?"· "+l("reviews.untraced",r[2]):"",r[3]?"· "+l("reviews.trunk",r[3]):"","· "+l("reviews.reports")].filter(Boolean).join(" ")),\n'
     '      (REG.verdicts||[]).map(v=>row(`<code>${esc(v[0].slice(0,10))}</code>`,lh("reviews.on",`<code>${esc(v[1].slice(0,10))}</code>`)+" · "+brn(v[6]||["none"]),v[5]?l("verdict."+v[5]):l("type.verdict"),\n'
     '        (v[4]=="same session"?`<b>${l("reviews.word.same")}</b>`:l(word[v[4]]||"reviews.word.untraced"))+(v[4]=="on trunk"?"":" · "+lh("reviews.sessions",esc(v[2]||"—"),v[3].length>1?lh("reviews.sessions.more",esc(v[7]),v[3].length-1):esc(v[3][0]||"—"))),"","",VERDICT[v[5]])).join(""),false))}\n'
     '  // your current path: your own words, known by heart — folded, its heading carrying its line count\n'
     '  if(HOME.path){const n=HOME.path.split("\\n").filter(s=>s.trim()).length;\n'
     '    S.push(fold(hd("h2",l("path.title"),"· "+l(n==1?"path.line":"path.lines",n)+" · work-tracker/TRIAGE.md"),`<p class="lim">${ids(HOME.path)}</p>`,false))}\n'
     '  return S.join("");\n'
     '}\n'),
    # a group's head and its rows (BF-3, BF-13)
    ('    const head=`<tr class="g" data-k="${esc(gname+k)}"><td colspan="4" class="m">${folded?"▸":"▾"} <b>${k=="—"?l("group.none",vn(gname)):gname=="board"?l("section."+k):esc(k)}</b>${gname=="epic"&&byId.has(k)?" "+esc(byId.get(k)[6]):""}${story||" · "+g.length}${gname=="board"?" · "+BOARD[k]:BCOLS.filter(c=>c.toLowerCase()!=gname).map(c=>[...new Set(g.map(t=>xv(t,c)).filter(v=>v!="—"))].sort(vcmp)).filter(v=>v.length).map(v=>" · "+esc(v.slice(0,6).join(" / "))+(v.length>6?" …":"")).join("")}</tr>${state}`;   // a header sums its rows up by the board\'s columns\n'
     '    return head+(folded?"":g.map((t,i)=>`<tr class="t${gname=="epic"&&byId.has(k)&&t[0]!=k?" c":""}${i%2?" zebra":""}"><td class="m"><i class="q ${mark(t)}"></i><a href="#=${t[0]}">${t[0]}</a><td class="m ${t[1]<"P2"?"hot":""}">${t[18]?"#"+t[18]+" ":""}${t[1]}${t[21]?" → "+esc(t[21]):""}<td class="m">${esc(sl(blocked(t)?"Blocked":t[2]))}${BCOLS.map(c=>`<td class="m x">${esc((t[28]||{})[c]||xv(t,c))}`).join("")}<td><a href="${esc(BLOB)+esc(t[5])}">${esc(t[6])}</a>${t[15].map(x=>`<a href="#${encodeURIComponent(x)}" class="m k">${esc(x)}</a>`).join("")}</tr><tr class="h" hidden><td colspan="4">${esc(t[7])}${blocked(t)?`<div class="m">${esc(sl(t[2]))} · ${l("word.blocked_by")} ${t[16].map(b=>byId.has(b)?`<a href="#~${b}">${b}</a>`:esc(b)).join(" ")}</div>`:""}${t[17]?`<div class="m">${l("word.triaged")} ${esc(t[17])}${t[20].length?" · "+l("word.needs")+" "+t[20].join(", "):""}</div>`:""}${chips(t[12],"→")}${chips(inb.get(t[0])||[],"←")}</tr>`).join(""))}).join("");\n',
     '    const head=`<tr class="g${folded?" f":""}" data-k="${esc(gname+k)}"><td colspan="4" class="m"><b>${k=="—"?l("group.none",vn(gname)):gname=="board"?l("section."+k):esc(k)}</b>${gname=="epic"&&byId.has(k)?" "+esc(byId.get(k)[6]):""}${story||" · "+g.length}${gname=="board"?(BOARD[k]?" · "+BOARD[k]:""):BCOLS.filter(c=>c.toLowerCase()!=gname).map(c=>[...new Set(g.map(t=>xv(t,c)).filter(v=>v!="—"))].sort(vcmp)).filter(v=>v.length).map(v=>" · "+esc(v.slice(0,6).join(" / "))+(v.length>6?" …":"")).join("")}</tr>${state}`;   // a header sums its rows up by the board\'s columns\n'
     '    return head+(folded?"":g.map(t=>`<tr class="t${gname=="epic"&&byId.has(k)&&t[0]!=k?" c":""}"><td class="m"><i class="q ${mark(t)}"></i><a href="#=${t[0]}">${t[0]}</a><td class="m ${t[1]<"P2"?"hot":""}">${t[18]?"#"+t[18]+" ":""}${t[1]}${t[21]?" → "+(t[21]=="owner"?l("next.owner"):esc(t[21])):""}<td class="m">${esc(sl(blocked(t)?"Blocked":t[2]))}${BCOLS.map(c=>`<td class="m x">${esc((t[28]||{})[c]||xv(t,c))}`).join("")}<td><a href="${esc(BLOB)+esc(t[5])}">${esc(t[6])}</a>${t[15].map(x=>`<a href="#${encodeURIComponent(x)}" class="m k">${esc(x)}</a>`).join("")}</tr><tr class="h" hidden><td colspan="4">${esc(t[7])}${blocked(t)?`<div class="m">${esc(sl(t[2]))} · ${l("word.blocked_by")} ${t[16].map(b=>byId.has(b)?`<a href="#~${b}">${b}</a>`:esc(b)).join(" ")}</div>`:""}${t[17]?`<div class="m">${l("word.triaged")} ${esc(t[17])}${t[20].length?" · "+l("word.needs")+" "+t[20].join(", "):""}</div>`:""}${chips(t[12],"→")}${chips(inb.get(t[0])||[],"←")}</tr>`).join(""))}).join("");\n'),
    # draw() hands the box to its renderer; the old box retired
    ('  $("g").textContent=L["view.by"].replace("{0}",vn(gname));$("p").innerHTML=`<span class="pt">${l("owner.title")}</span>`+(gname=="board"&&!q?(all_=>{\n'
     '    // ONLY what passes the ask rules is a question here — t[29][7] is why it is not. The Owner never reads a malformed\n'
     '    // ask as one; what was sent back is listed after the queue, with its reason, for the seat that wrote it.\n'
     '    const w=all_.filter(t=>!t[29][7].length),sent=all_.filter(t=>t[29][7].length);\n'
     '    // the answer first: what needs the Owner — how many, how old, what it holds up — then each ask as the question it is\n'
     '    const days=t=>(d=>d==d?d:null)(ago(t[29][2])),old=Math.max(-1,...w.map(t=>days(t)??-1)),held=[...new Set(w.flatMap(t=>t[29][3]))];\n'
     '    w.sort((a,b)=>(days(b)??-1)-(days(a)??-1));\n'
     "    // an answer is the Owner's own commit: the button copies the three lines and opens the file on the forge under their login —\n"
     "    // no server, no token, and the seat that asked is nowhere in the path. The commit's author is the proof.\n"
     '    // Two buttons — accept · reject — open a dialog that shows the whole ask with its context, so the Owner can look and\n'
     '    // abort. OK yields ONE command: `--answer <id> accept|reject "text"` — the tool cuts the answer branch, writes the\n'
     '    // three lines, commits SIGNED and pushes. A browser cannot sign; the dialog decides, the terminal signs.\n'
     '    // what the Owner typed goes into the copied command SINGLE-quoted: in "…" a shell runs a backtick and expands a `$` (R4)\n'
     '    const sq=s=>"\'"+String(s).replace(/\'/g,"\'\\\\\'\'")+"\'";\n'
     '    const act=(t,kind)=>{const d=$("dlg"),id=t[0],[ask,k,since,held,,prop,opts]=t[29],cmd="shoalmark";\n'
     '      const meta=[k?l("ask."+k):"",days(t)!=null?l("waiting.days",days(t)):"",held.length?l("waiting.holds.ids",held.join(", ")):""].filter(Boolean).join(" · ");\n'
     '      // an ask offers choices: one radio per option in the order given, except the RECOMMENDED one (`ask-proposal:`)\n'
     '      // which is offered first. A proposal alone is a list of one. Last always comes Other, with the box — and when\n'
     '      // there is nothing to choose from, Other is the only row and the box is the answer.\n'
     '      const all=opts&&opts.length?opts:(prop?[prop]:[]),ordered=prop&&all.includes(prop)?[prop,...all.filter(o=>o!=prop)]:all;\n'
     '      const rows=ordered.map((o,i)=>`<label class="dl"><input type="radio" name="how" value="${i}" required> <span>${esc(o)}`\n'
     '          +(o==prop?` <span class="ddim">— ${l("answer.recommended")}</span>`:"")+`</span></label>`).join("")\n'
     '        +`<label class="dl"><input type="radio" name="how" value="other" required${ordered.length?"":" checked"}> <span>${l("answer.other")}</span></label>`;\n'
     '      d.innerHTML=`<form method="dialog"><h3>${kind=="accept"?l("answer.accept"):l("answer.reject")} · <a href="#=${id}">${id}</a>${meta?` · <span class="m">${meta}</span>`:""}</h3>\n'
     '        <p class="dq">${esc(ask)}</p>${prop?`<p class="dp"><b>${l("answer.proposal")}</b> ${esc(prop)}</p>`:""}<p class="m ddim">${esc(t[6])}</p>\n'
     '        ${kind=="accept"?`${rows}<textarea name="text" rows="3" placeholder="${l("answer.change.hint")}"${ordered.length?" disabled":" required"}></textarea>`\n'
     '        :`<textarea name="text" rows="3" placeholder="${l("answer.reject.hint")}" required></textarea>`}\n'
     '        <menu><button value="ok" class="go">${l("answer.ok")}</button><button value="abort" formnovalidate>${l("answer.abort")}</button></menu></form>`;\n'
     '      const f=d.querySelector("form"),ta=f.text;\n'
     '      f.querySelectorAll("[name=how]").forEach(r=>r.onchange=()=>{ta.disabled=r.value!="other";ta.required=r.value=="other";if(!ta.disabled)ta.focus()});\n'
     '      f.onsubmit=e=>{if(e.submitter?.value!="ok")return;e.preventDefault();const q=s=>String(s).trim().replace(/"/g,"\'");\n'
     '        // the chosen option goes into the command VERBATIM — what the Owner picked is what the tracker records\n'
     '        const pick=f.how?.value,txt=q(ta.value||""),chosen=kind=="reject"||pick=="other"||pick==null?txt:q(ordered[+pick]);\n'
     '        const line=`${cmd} --answer ${id} ${kind}${chosen?" "+sq(chosen):""}`;\n'
     '        sign(d,id,line,(kind=="accept"?"accepted":"rejected")+(chosen?" - "+chosen.replace(/\\s+/g," "):""))};\n'
     '      d.showModal()};\n'
     '    // THE SECOND SCREEN (FM-013). OK used to disable itself and leave one button — abort — which read as taking the\n'
     '    // decision back. The decision is made; the terminal signs it. This screen says what to run, where, what it does step\n'
     '    // by step, what the end looks like, how to check it and where to go when signing fails — and has ONE way out, Done\n'
     "    // (Esc too: it is the dialog's own). It says *Copied* only when the clipboard said so: from a file there may be none.\n"
     '    const sign=(d,id,line,said,kind="answer")=>{const br=`answer/${id.toLowerCase()}`,c=s=>`<code>${esc(s)}</code>`;\n'
     '      d.innerHTML=`<form method="dialog" class="sign"><h3>${l(kind=="answer"?"answer.sign.title":"act.sign.title")} · <a href="#=${id}">${id}</a></h3>\n'
     '        <p class="dp">${l("answer.sign.intro")}</p><pre class="cmd">${esc(line)}</pre>\n'
     '        <p class="m ddim"><button type="button" class="copy">${l("answer.sign.copy")}</button><span class="said" aria-live="polite"></span></p>\n'
     '        <h4>${l("answer.sign.where")}</h4><p>${BRANCH?lh("answer.sign.where.branch",c(BRANCH)):l("answer.sign.where.text")}</p>\n'
     '        <h4>${l("answer.sign.does")}</h4><ol><li>${kind.startsWith("revoke")?lh("way.sign.step.on",c(br)):lh("answer.sign.step.cut",c(br))}</li><li>${kind=="answer"?lh("answer.sign.step.write",c("answer:"),c("answered:"),c("answered-by:"),c("next: "+(byId.get(id)?.[29][1]=="action"?"owner":"build"))):lh("act.sign.step."+kind,c(kind.replace("revoke.","")+":"),c("## Acts"))}</li>\n'
     '        <li>${l("answer.sign.step.commit")}</li><li>${l("answer.sign.step.push")}</li></ol><p class="ddim">${l("answer.sign.slow")}</p>\n'
     '        <h4>${l("answer.sign.success")}</h4><pre>${esc(`${id} ${kind=="answer"?"answered: ":""}${said}\\n  signed, on \\`${br}\\`, pushed`)}</pre>\n'
     '        <h4>${l("answer.sign.check")}</h4><p>${lh("answer.sign.check.text",c(`git log -1 --format=%G? ${br}`),c("G"))}</p>\n'
     '        <h4>${l("answer.sign.fail")}</h4><p>${lh("answer.sign.fail.text",`<a href="${l("answer.sign.url")}" target="_blank" rel="noopener">${l("answer.sign.page")}</a>`)}</p>\n'
     '        <menu><button value="done" class="go">${l("answer.done")}</button></menu></form>`;\n'
     '      const out=d.querySelector(".said"),copy=()=>(navigator.clipboard?.writeText?navigator.clipboard.writeText(line):Promise.reject())\n'
     '        .then(()=>out.textContent=L["answer.sign.copied"],()=>out.textContent=L["answer.sign.nocopy"]);\n'
     '      d.querySelector(".copy").onclick=copy;copy();d.querySelector(".go").focus()};\n'
     '    window.ACT=act;\n'
     '    // FM-030: an act owed to the Owner has two buttons — done · reschedule. Each asks one thing — where the result is, or the\n'
     '    // new time — and OK gives ONE command, `--done <id> "<where>"` or `--due <id> <time with its zone>`, on the same second\n'
     '    // screen as an answer: a browser cannot sign; the terminal does.\n'
     '    const owe=(t,kind)=>{const d=$("dlg"),id=t[0],a=t[30],cmd="shoalmark";\n'
     '      d.innerHTML=`<form method="dialog"><h3>${l(kind=="done"?"act.done.title":"act.due.title")} · <a href="#=${id}">${id}</a></h3>\n'
     '        <p class="dq">${esc(a[0])}</p>${a[5]?`<p class="ddim">${l("acts.asked",a[5])}</p>`:""}<p class="m ddim">${a[3]?l("acts.due",a[3].replace("T"," ")):l("acts.nodate")}</p>\n'
     '        ${kind=="done"?`<textarea name="text" rows="2" placeholder="${l(a[5]?"act.done.hint.promise":"act.done.hint")}" required></textarea>`:`<input name="when" type="datetime-local" required>`}\n'
     '        <menu><button value="ok" class="go">${l("answer.ok")}</button><button value="abort" formnovalidate>${l("answer.abort")}</button></menu></form>`;\n'
     '      const f=d.querySelector("form");\n'
     '      f.onsubmit=e=>{if(e.submitter?.value!="ok")return;e.preventDefault();\n'
     '        if(kind=="done"){const w=String(f.text.value).trim().replace(/\\s+/g," ").replace(/"/g,"\'");return sign(d,id,`${cmd} --done ${id} ${sq(w)}`,`done: ${w}`,"done")}\n'
     "        // the time the Owner picks is their machine's; the command carries its zone, so it means the same hour everywhere\n"
     '        const v=f.when.value,dt=new Date(v),o=-dt.getTimezoneOffset(),z=(o<0?"-":"+")+String(Math.floor(Math.abs(o)/60)).padStart(2,"0")+":"+String(Math.abs(o)%60).padStart(2,"0");\n'
     '        const iso=(v.length==16?v+":00":v)+z;sign(d,id,`${cmd} --due ${id} ${iso}`,`due: ${iso}`,"due")};\n'
     '      d.showModal()};\n'
     '    window.OWE=owe;\n'
     '    // FM-030, their signed answer 920970b7: on what is on its way, *revoke* in the place of the buttons — one field, why; OK gives\n'
     '    // ONE command, `--revoke <id> "<why>"`, on the same second screen: it commits on top of their act, on its branch\n'
     '    const rev=t=>{const d=$("dlg"),id=t[0],w=t[31],cmd="shoalmark";\n'
     '      d.innerHTML=`<form method="dialog"><h3>${l("way.revoke.title")} · <a href="#=${id}">${id}</a></h3>\n'
     '        <p class="dq">${esc(w[7])}</p>${w[8]?`<p class="ddim">${l("acts.asked",w[8])}</p>`:""}<p class="m ddim">${l("way."+w[0])} · ${esc(w[1])} @ ${esc(w[3].slice(0,7))}</p>\n'
     '        <textarea name="text" rows="2" placeholder="${l("way.revoke.hint")}" required></textarea>\n'
     '        <menu><button value="ok" class="go">${l("answer.ok")}</button><button value="abort" formnovalidate>${l("answer.abort")}</button></menu></form>`;\n'
     '      const f=d.querySelector("form");\n'
     '      f.onsubmit=e=>{if(e.submitter?.value!="ok")return;e.preventDefault();const why=String(f.text.value).trim().replace(/\\s+/g," ").replace(/"/g,"\'");\n'
     '        sign(d,id,`${cmd} --revoke ${id} ${sq(why)}`,w[0]=="done"?`done revoked: ${why}`:`answered: revoked - ${why}`,w[0]=="done"?"revoke.done":"revoke.answer")};\n'
     '      d.showModal()};\n'
     '    window.REV=rev;\n'
     '    return `<b class="${w.length?"hot":""}">${l("waiting.title")}: ${w.length}</b>`+(w.length?(old>=0?" · "+l("waiting.oldest",old):"")+(held.length?" · "+l("waiting.holds",held.length):"")+(w.length>5?" · "+l("waiting.bottleneck",w.length,held.length):"")+"\\n"+w.slice(0,14).map(t=>\n'
     '      `<a href="#=${t[0]}">${t[0]}</a> `+(t[29][0]?esc(t[29][0]):`<i>${l("waiting.unasked")}</i> — ${esc(t[6])}`)+`<span class="m"> ·`+(t[29][1]?" "+l("ask."+t[29][1])+" ·":"")+(days(t)!=null?" "+l("waiting.days",days(t))+" ·":"")+(t[29][3].length?" "+l("waiting.holds.ids",t[29][3].join(", ")):"")+`</span>`+(t[29][0]?` <button class="act" onclick="ACT(T.find(x=>x[0]==\'${t[0]}\'),\'accept\')">${l("answer.accept")}</button><button class="act" onclick="ACT(T.find(x=>x[0]==\'${t[0]}\'),\'reject\')">${l("answer.reject")}</button>`:"")).join("\\n").replace(/ ·<\\/span>/g,"</span>")+(w.length>14?"\\n…":""):"")\n'
     '      +(sent.length?"\\n\\n<b>"+l("waiting.malformed",sent.length)+"</b>\\n"+sent.map(t=>\n'
     '        `<a href="#=${t[0]}">${t[0]}</a> `+(t[29][0]?esc(t[29][0]):`<i>${l("waiting.unasked")}</i>`)+`<span class="m"> — ${esc(t[29][7][0])}</span>`).join("\\n"):"")})(T.filter(t=>OPEN.has(t[2])&&t[21]=="owner"&&!t[29][4]&&!(t[31]&&t[31][10])))\n'
     '    // FM-030: what they owe, with its time — an accepted action ask, or any `due:` — each with its state by the clock above\n'
     '    +(acts=>acts.length?"\\n\\n<b class=\\""+(acts.some(t=>actstate(t[30])!="due"&&actstate(t[30])!="nodate")?"hot":"")+"\\">"+l("acts.title")+": "+acts.length+"</b>\\n"+acts.map(t=>{\n'
     '      const a=t[30],s=actstate(a),when=a[3].replace("T"," ");\n'
     '      return `<a href="#=${t[0]}">${t[0]}</a> ${esc(a[0])}<span class="m"> · `+(a[1]?l("acts.promised",a[2],a[1])+" · ":"")\n'
     '        +`<b class="act-${s}${s=="overdue"||s=="missed"?" hot":""}">${s=="nodate"?l("acts.nodate"):s=="missed"?l("acts.missed",when,a[4]):l("acts."+s,when)}</b></span>`\n'
     '        +` <button class="act" onclick="OWE(T.find(x=>x[0]==\'${t[0]}\'),\'done\')">${l("acts.done")}</button><button class="act" onclick="OWE(T.find(x=>x[0]==\'${t[0]}\'),\'due\')">${l("acts.reschedule")}</button>`\n'
     '        +(a[5]?`\\n<span class="aq">${l("acts.asked",a[5])}</span>`:"")}).join("\\n"):"")(T.filter(t=>t[30].length&&!(t[31]&&!t[31][11])))\n'
     '    // FM-030, their signed answer 920970b7: the board reads git. What they did and pushed on `answer/<id>` is here, not in the two\n'
     '    // lists above, until their merge — their promise or their answer first, what it is, the branch, the commit, its time, whether it\n'
     '    // verifies, and that their merge is next\n'
     '    +(way=>way.length?"\\n\\n<b>"+l("way.title")+": "+way.length+"</b>\\n"+way.map(t=>{const w=t[31];\n'
     '      return `<a href="#=${t[0]}">${t[0]}</a> ${esc(w[7])}<span class="m"> · <b class="go">${l("way."+w[0])}</b>`+(w[13]?" — "+esc(w[13]):w[12]?" — "+l("acts.due",w[12].replace("T"," ")):"")\n'
     '        +` · ${esc(w[1])} @ ${esc(w[3].slice(0,7))} · ${esc(w[4].slice(0,16).replace("T"," "))} · ${w[6].startsWith("merge")?l("way.signed"):l("way.unverified",w[6].replace(/^wait: /,""))} · ${w[14]?l("way.held",w[14].replace(/^wait: /,"")):l("way.merge")}</span>`\n'
     '        +(w[0]=="done"||w[0]=="answer"?` <button class="act" onclick="REV(T.find(x=>x[0]==\'${t[0]}\'))">${l("way.revoke")}</button>`:"")\n'
     '        +(w[8]?`\\n<span class="aq">${l("acts.asked",w[8])}</span>`:"")}).join("\\n"):"")(T.filter(t=>t[31]))\n'
     '    +(HOME.path?"\\n\\n<b>"+l("path.title")+"</b> — work-tracker/TRIAGE.md\\n"+ids(HOME.path):"")\n'
     "    // the registry, a report of the trailers (FM-024, FM-032): who committed in the last day, where — and how independent this week's verdicts were\n"
     '    +(REG?(REG.groups.length?"\\n\\n<b>"+l("sessions.recent",REG.parents,REG.all)+"</b>\\n"\n'
     '        +REG.groups.map(g=>`<details><summary>${esc(g[0])} ${esc(g[1])} (${esc(g[2])})${g[3].map(x=>" · "+esc(x)).join("")}</summary>`\n'
     '          +g[4].map(m=>`<span class="aq">${esc(m[0])} (${esc(m[1])}) · ${esc(m[2])} · ${esc(m[3])}</span>`).join("\\n")+"</details>").join(""):"")\n'
     '      +(REG.reviews?(REG.groups.length?"\\n":"\\n\\n")+l("reviews.week",REG.reviews[0],REG.reviews[1])+(REG.reviews[2]?" · "+l("reviews.untraced",REG.reviews[2]):"")+(REG.reviews[3]?" · "+l("reviews.trunk",REG.reviews[3]):""):""):""):"");   // the box keeps its title in every view (FM-002 R2)\n',
     '  $("g").textContent=L["view.by"].replace("{0}",vn(gname));$("p").hidden=gname!="board"||!!q;$("p").innerHTML=`<span class="pt">${l("owner.title")}</span>`+(gname=="board"&&!q?box():"");   // the box keeps its title in every view (FM-002 R2)\n'),
    # the viewer's back link, with its icon
    ('  v.innerHTML=`<p class="m"><a href="#">${l("viewer.board")}</a> · <a href="#~${id}">${l("viewer.neighbours")}</a> · <a href="${esc(t[5])}">${l("viewer.file")}</a>${BLOB?` · <a href="${esc(BLOB)+esc(t[5])}">${l("viewer.forge")}</a>`:""}</p>\n',
     '  v.innerHTML=`<p class="m"><a href="#">${l("viewer.board")}</a> · <a href="#~${id}">${l("viewer.neighbours")}</a> · <a href="${esc(t[5])}">${l("viewer.file")}</a>${BLOB?` · <a href="${esc(BLOB)+esc(t[5])}">${l("viewer.forge")}${ICO.out}</a>`:""}</p>\n'),
    # the handover line and a story's chapters (BF-3, BF-12)
    ('<b>${l("viewer.handover")}</b> — ${l("viewer.next")}: ${t[21]?esc(t[21]):"<i>"+l("word.missing")+"</i>"}${t[21]?" · "+l("viewer.kind")+": "+(t[26][0]?esc(t[26][0])+(t[26][1]?"":" <i>("+l("viewer.from_move")+")</i>"):"<i>"+l("word.missing")+"</i>"):""} · ${l("viewer.true_now")}: ${t[20].includes("stated")?"<i>"+l("word.missing")+"</i>":l("word.stated")}${(c=>c.length?`<br>\n'
     '<b>${l("story.chapters")}</b> — ${c.length}: ${Object.entries(c.filter(x=>x[2]=="In Progress"||x[2]=="Proposed").reduce((m,x)=>(m[x[21]||"no move named"]=[...(m[x[21]||"no move named"]||[]),x[0]],m),{})).map(([k,v])=>k=="no move named"?`${v.length} ${l("viewer.no_move")}`:`${esc(k)} ${v.map(i=>`<a href="#=${i}">${i}</a>`).join(" ")}`).join(" · ")||l("viewer.none_in_progress")} · ${c.filter(x=>x[2]=="Parked").length} ${l("story.parked")} · ${c.filter(x=>x[2]=="Shipped").length} ${l("story.shipped")} · ${c.filter(x=>x[2]=="Closed").length} ${l("story.closed")}`:"")(T.filter(x=>x[13]==t[0]))}${t[20].filter(n=>n!="stated"&&n!="intended").length?" · "+l("word.needs")+" "+t[20].filter(n=>n!="stated"&&n!="intended").join(", "):""}</p>`:""}${chips(t[16].filter(b=>byId.has(b)),l("word.blocked_by"),"=")}${chips(t[12],"→","=")}${chips(inb.get(id)||[],"←","=")}<div class="md">${marked.parse(MD.get(id))}</div>`;\n',
     '<b>${l("viewer.handover")}</b> — ${l("viewer.next")}: ${t[21]?(t[21]=="owner"?"<code>owner</code>":esc(t[21])):"<i>"+l("word.missing")+"</i>"}${t[21]?" · "+l("viewer.kind")+": "+(t[26][0]?esc(t[26][0])+(t[26][1]?"":" <i>("+l("viewer.from_move")+")</i>"):"<i>"+l("word.missing")+"</i>"):""} · ${l("viewer.true_now")}: ${t[20].includes("stated")?"<i>"+l("word.missing")+"</i>":l("word.stated")}${(c=>c.length?`<br>\n'
     '<b>${l("story.chapters")}</b> — ${c.length}: ${Object.entries(c.filter(x=>x[2]=="In Progress"||x[2]=="Proposed").reduce((m,x)=>(m[x[21]||"no move named"]=[...(m[x[21]||"no move named"]||[]),x[0]],m),{})).map(([k,v])=>k=="no move named"?`${v.length} ${l("viewer.no_move")}`:`${k=="owner"?"<code>owner</code>":esc(k)} ${v.map(i=>`<a href="#=${i}">${i}</a>`).join(" ")}`).join(" · ")||l("viewer.none_in_progress")} · ${c.filter(x=>x[2]=="Parked").length} ${l("story.parked")} · ${c.filter(x=>x[2]=="Shipped").length} ${l("story.shipped")} · ${c.filter(x=>x[2]=="Closed").length} ${l("story.closed")}`:"")(T.filter(x=>x[13]==t[0]))}${t[20].filter(n=>n!="stated"&&n!="intended").length?" · "+l("word.needs")+" "+t[20].filter(n=>n!="stated"&&n!="intended").join(", "):""}</p>`:""}${chips(t[16].filter(b=>byId.has(b)),l("word.blocked_by"),"=")}${chips(t[12],"→","=")}${chips(inb.get(id)||[],"←","=")}<div class="md">${marked.parse(MD.get(id))}</div>`;\n'),
    # the scheme's comment
    ("// light or dark is the viewer's choice: auto follows the system; the other two switch every theme's\n"
     '// `prefers-color-scheme` rule on or off — so a brand needs to know nothing about the button. Paper stays light.\n',
     "// light or dark is the viewer's choice: auto follows the system; the other two switch the page's own\n"
     '// `prefers-color-scheme` rules on or off. Paper stays light.\n'),
    # the scheme's button and its words
    ('setScheme=m=>{scheme=m;paint(m);$("s").textContent="◐ "+L["scheme."+m];$("s").dataset.scheme=m;try{localStorage.setItem("shoalmark.scheme",m)}catch(e){}};\n',
     'setScheme=m=>{scheme=m;paint(m);$("s").textContent=(L["scheme.button"]??"{0}").replace("{0}",L["scheme."+m]??m);$("s").dataset.scheme=m;try{localStorage.setItem("shoalmark.scheme",m)}catch(e){}};\n'),
)


def fm053_transform(page):
    """The baseline's page as A2 changes it: FM053_PAGE_EDITS applied in order, each to text that occurs exactly once — else None: a page
    those edits do not fit is no page the allowance explains."""
    text = page.decode("utf-8")
    for old, new in FM053_PAGE_EDITS:
        if text.count(old) != 1:
            return None
        text = text.replace(old, new)
    return text.encode("utf-8")
PALETTE_ROW = "| `[palette]` |"
# RV-3345: `--schema`'s two changes, exact — the `[palette]` row inserted as the first row of the top-level keys' table, right after its heads
# and before `owner`'s row; and the brand line, old for new, whole and between its blank line and the next — each anchored where it occurs once
FM053_SCHEMA_EDITS = (
    ("| Key | Value | Says |\n|---|---|---|\n| `owner` |",
     "| Key | Value | Says |\n|---|---|---|\n"
     '| `[palette]` | `name` = `"monochrome"` (the default) or `"shoalmark"`; and any of `bg` `ink` `fail` `ok` `warn` `owed` `help` `secbg` `okbg` `warnbg` `failbg` = `["#rrggbb", "#rrggbb"]`, light then dark | the board\'s colours (FM-053): a palette by name, a few of its tokens in your words over it — three meanings, `ok` (teal: done), `warn` (amber: a warning) and `fail` (coral: a failure); `dim`, `mute`, `line`, `box` and `raise` are derived from `bg` and `ink`. The surfaces, `secbg` `okbg` `warnbg` `failbg`, may be named the same way; where none is, the palette\'s own are taken. Every text colour reaches 4.5:1 on the page, `raise` and every surface, in light and in dark, or the palette is refused at configuration in one line naming the pair (exit 1). An older copy of the tool ignores the table |'
     "\n| `owner` |"),
    ("\n"
     "No key chooses the board's look: a brand is files in its places, the later one winning (`--brand` says which gave what). `--brand DIR --from THEME` writes a starter from a theme the tool ships in `brand/themes/`: none in this copy."
     "\n",
     "\n"
     'A brand place gives the board a logo and its labels, the later place winning (`--brand` says which gave what, and names each brand file the board no longer reads: `theme.css`, `fonts/`, `wordmark.svg`). No theme is read or shipped.'
     "\n"),
)


def fm053_schema(stdout):
    """The baseline's stdout as A2's `--schema` changes it: FM053_SCHEMA_EDITS applied in order, each to text that occurs exactly once —
    else None: stdout those edits do not fit is not the schema's."""
    for old, new in FM053_SCHEMA_EDITS:
        if stdout.count(old) != 1:
            return None
        stdout = stdout.replace(old, new)
    return stdout


def schema_matches(before, after):
    staged = fm053_schema(before["stdout"])
    return staged is not None and d_batch_schema_matches(dict(before, stdout=staged), after)


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


# THE BOARD'S SETTINGS ON EVERY READ. The candidate's starts and calls are held equal to the baseline's, in order, once these are set aside: from the
# candidate's, the board's settings and each emptied filter driver in a start's environment (`settings_undone`), each list of the filter drivers
# (`DRIVERS_WORDS`) and each `check-attr`, `-t` on `ls-files`, `--no-textconv` where `--text` is not beside it, and a read of the cached `origin/master`
# directly after one of the cached `origin/main` (`TRUNK_READS`); from both, every read of the working tree's edits (`edit_read`), whose number is held on
# its own (`edit_reads`).
DRIVERS_WORDS = ("config", "-z", "--name-only", "--get-regexp", "^filter\\.")
TRUNK_READS = (("rev-parse", "--verify", "--quiet", "refs/remotes/origin/main^{commit}"), ("rev-parse", "--verify", "--quiet", "refs/remotes/origin/master^{commit}"))
SETTING = re.compile(r"'(?:[^']|'\\'')*'")
BOARD_KEYS = ("'log.showSignature=", "'core.fsmonitor=", "'gpg.program=", "'gpg.openpgp.program=", "'gpg.x509.program=")
FILTER_SETTING = re.compile(r"'filter\..*\.(?:clean|smudge|process)='")


def edit_read(words):
    """Whether a start's words are a `diff` of one revision against the working tree: how either version reads the working tree's edits."""
    return (bool(words) and words[0] == "diff" and "--cached" not in words and "--name-only" in words
            and len([word for word in words[1:] if not word.startswith("-")]) == 1)


def edit_reads(rows):
    return sum(edit_read(git_words(row)) for row in rows)


def origin_undone(rows):
    """The starts or calls with these removed: each `config --get remote.origin.url`, each `ls-remote --symref origin HEAD`, and the one
    `rev-parse --verify --quiet refs/remotes/origin/<name>^{commit}` that directly follows either. Every other start and call stays, in order."""
    out, drop_next_rp = [], False
    for row in rows:
        w = git_words(row)
        if w == ("config", "--get", "remote.origin.url") or w == ("ls-remote", "--symref", "origin", "HEAD"):
            drop_next_rp = True
            continue
        if drop_next_rp and len(w) >= 2 and w[0] == "rev-parse" and "--verify" in w and any(x.startswith("refs/remotes/origin/") and x.endswith("^{commit}") for x in w):
            drop_next_rp = False
            continue
        drop_next_rp = False
        out.append(row)
    return out


def settings_undone(env):
    """A start's environment with the board's settings set aside, so it can be held equal to the baseline's: the hooks path and every emptied filter driver
    always, and the rest (`BOARD_KEYS`) where the read does not keep from fetching (`GIT_NO_LAZY_FETCH`)."""
    if not isinstance(env, dict) or "GIT_CONFIG_PARAMETERS" not in env:
        return env
    kept = [s for s in SETTING.findall(env["GIT_CONFIG_PARAMETERS"]) if not s.startswith("'core.hooksPath=") and not FILTER_SETTING.fullmatch(s)
            and (env.get("GIT_NO_LAZY_FETCH") == "1" or not s.startswith(BOARD_KEYS))]
    out = {key: value for key, value in env.items() if key != "GIT_CONFIG_PARAMETERS"}
    return dict(out, GIT_CONFIG_PARAMETERS=" ".join(kept)) if kept else out


def board_settings_undone(rows, candidate):
    """The starts or calls of a run, each read of the working tree's edits taken out; and, from the candidate's, its settings, its drivers' lists, its
    `check-attr`, its `ls-files` tag, its `--no-textconv` outside the board's own run, and each read of `origin/master` directly after one of
    `origin/main` (`TRUNK_READS`) — each as specified above."""
    out, last = [], None
    for row in rows:
        words = git_words(row)
        follows, last = last == TRUNK_READS[0], words
        if edit_read(words) or (candidate and (words == DRIVERS_WORDS or words[:1] == ("check-attr",) or (words == TRUNK_READS[1] and follows))):
            continue
        if not candidate:
            out.append(row)
            continue
        argv = list((row.get("argv") if "argv" in row else (row.get("args") or [None])[0]) or [])
        kept = [word for word in words if not (word == "--no-textconv" and "--text" not in words) and not (words[:1] == ("ls-files",) and word == "-t")]
        new_argv = argv[:len(argv) - len(words)] + kept if len(argv) >= len(words) else argv
        row = dict(row)
        if "argv" in row:
            row["argv"] = new_argv
            if "raw" in row:
                row["raw"] = subprocess.list2cmdline([str(word) for word in new_argv])
            row["environment"] = settings_undone(row.get("environment"))
        else:
            row["args"] = [new_argv, *(row.get("args") or [])[1:]]
            options = dict(row.get("options") or {})
            if "env" in options:
                options["env"] = settings_undone(options["env"])
            row["options"] = options
            result = row.get("result")
            if isinstance(result, dict) and "args" in result:
                result = dict(result, args=new_argv)
                if words[:1] == ("ls-files",) and "-t" in words and isinstance(result.get("stdout"), str):
                    result["stdout"] = "\0".join(entry[2:] if len(entry) > 2 else entry for entry in result["stdout"].split("\0"))
                row["result"] = result
        out.append(row)
    return out


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


FM057_PAGE_LINES = tuple(("\n" + line).encode("utf-8") for line in (
    '#ra{color:var(--dim);margin:0 0 2px;display:flex;flex-wrap:wrap;align-items:baseline;gap:0 2ch}#ra>span:first-child{flex:1 1 30ch}#ra .fact{display:inline-block;overflow-wrap:anywhere}'
    '#rb{margin-left:auto}#ra code{font:inherit}#ra .said{margin-left:6px}#ra .said.ok{background:var(--okbg)}'
    'details.about>summary{color:var(--dim)}details.about>summary:before{content:"> ";content:"> " / "";color:var(--mute)}details.about[open]>summary:before{content:"v ";content:"v " / ""}',
    "// FM-057: the rebuild command beside what the board read, and when — copied on the dialog's path: *Copied* only when the clipboard says so",
    '$("rb").onclick=()=>(navigator.clipboard?.writeText?navigator.clipboard.writeText($("rc").textContent):Promise.reject())',
    '  .then(()=>{$("rs").className="said ok";$("rs").innerHTML=`<span class="go">${ICO.check}${lh("read.copied",`<code>${esc($("rc").textContent)}</code>`)}</span>`},()=>{$("rc").hidden=false;$("rs").className="said";$("rs").innerHTML=`<span class="hot">${ICO.cross}${l("answer.sign.nocopy")}</span>`});',
))
FM057_READ_AT = re.compile("\n".encode() + re.escape('<p id="ra" class="m"><span><span class="fact">read from main @ ').encode() + rb"[0-9a-f]{7}"
                           + re.escape(" at ").encode() + rb"[0-9]{2}-[0-9]{2} [0-9]{2}:[0-9]{2}"
                           + re.escape('&nbsp;·</span> <span class="fact">it reads its file again when you come back to it; nothing polls</span></span><code id="rc" hidden>shoalmark --html-only</code>'
                                       '<button type="button" id="rb" class="act" aria-label="copy the rebuild command"><svg class="ico" viewBox="0 0 12 12" width="12" height="12" fill="currentColor" shape-rendering="crispEdges" aria-hidden="true"><path d="M0 4h8v1h-8ZM0 5h1v6h-1ZM7 5h1v6h-1ZM0 11h8v1h-8ZM4 0h8v1h-8ZM4 1h1v2h-1ZM11 1h1v7h-1ZM9 7h2v1h-2Z"></path></svg>rebuild command</button>'
                                       '<span id="rs" class="said" aria-live="polite"></span></p>\n<details class="about"><summary>what this page reads, and what it cannot see</summary>'
                                       "<p class=\"help\">read from main's history at ").encode() + rb"[0-9]{4}-[0-9]{2}-[0-9]{2} [0-9]{2}:[0-9]{2} [+-][0-9]{2}:[0-9]{2}"
                           + re.escape(" · no forge named in the configuration, so not linked · ").encode()
                           + rb"(?:1 path changed and not committed|[0-9]+ paths changed and not committed|nothing changed and not committed|what is changed and not committed is not read here)"
                           + re.escape("</p></details>").encode() + rb"(?=\n)")
FM057_RELOAD = ("// reload: begin — the board and its tracker pages (one page: `#=ID` is a tracker's) reload themselves when the tab is visible again, so a board rebuilt meanwhile — by an\n"
                "// explicit run, a commit or an act; no hook rebuilds it — is on the screen when the person comes back. The same page and nothing else: no poll, no timer, no second file, no server. Never while a dialog is open or a field\n").encode("utf-8"), \
               ("// reload: begin — the board and its tracker pages (one page: `#=ID` is a tracker's) reload themselves when the tab is visible again, so what a checkout, a merge or a pull\n"
                "// changed is on the screen when the person comes back. The same page and nothing else: no poll, no timer, no second file, no server. Never while a dialog is open or a field\n").encode("utf-8")
FM057_KEYS_SHOWN = ("read.git.branch", "read.git.detached", "read.git.unborn", "read.git.clean", "read.git.changed", "read.git.changed.one", "read.git.unread",
                    "read.svn", "read.svn.unread", "read.svn.new", "read.none", "read.none.why", "read.self", "read.copy", "read.copy.spoken",
                    "read.about", "read.about.git", "read.about.svn", "read.about.none", "link.unpushed", "link.noforge", "link.unknown", "link.noviewer",
                    "link.nocommit", "read.copied")
FM057_LABELS = tuple(re.compile(rb', "' + re.escape(k.encode()) + rb'": ' + _J) for k in FM057_KEYS_SHOWN)


def fm057_page_dropped(data):
    """The candidate's board page without the read-at line's parts, each taken out exactly once as specified above — the style line, the read-at
    line and its fold, the three script lines, the twenty-five words — and the reload's comment put back as the baseline's. None where any part is
    not there exactly once as written."""
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


def day_dropped(data, script=DAY_SCRIPT, sign=DAY_SIGN):
    for line in script:
        if data.count(line + b"\n") != 1:
            return None
        data = data.replace(line + b"\n", b"\n", 1)
    for pattern in DAY_TEMPLATES + (DAY_DATA,) + DAY_LABELS:
        data, n = pattern.subn(b"", data)
        if n != 1:
            return None
    if sign is None:
        return data
    if data.count(sign[0]) != 1:
        return None
    return data.replace(*sign)


DAY_SCRIPT_JOINED = DAY_SCRIPT[:7]
day_dropped_joined = lambda data: day_dropped(data, DAY_SCRIPT_JOINED, None)

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


FM054_ON_A2_EDITS = (
    ('.dfl.add{background:var(--okbg)}.dfl.add .s{color:var(--teal)}.dfl.del{background:var(--failbg)}.dfl.del .s{color:var(--coral)}#dlg .sign a{text-decoration:underline}#dlg button.copy{margin:0}\n',
     '.dfl.add{background:var(--okbg)}.dfl.add .s{color:var(--teal)}.dfl.del{background:var(--failbg)}.dfl.del .s{color:var(--coral)}#dlg .sign a{text-decoration:underline}#dlg button.copy{margin:0}\n'
     '#p .pw,#dlg .pw{color:var(--ink);font-weight:600}.cq{color:var(--amber)}#p .cq{display:block;margin:0 0 4px}#dlg .cq{margin:0 0 8px}#p .pw.au,#dlg .pw.au{color:var(--amber)}\n'),
    (FM054_PAGE_EDITS[2][0], FM054_PAGE_EDITS[2][1].replace('"answer.give.title": "Give your answer", "act.give.title": "Record your act"',
                                                       '"answer.give.title": "give your answer", "act.give.title": "record your act"')),
    ("},ICO={", "},PROOF=" + FM054_PAGE_EDITS[3][1].split("},PROOF=", 1)[1].rsplit(",BRANCH=", 1)[0] + ",ICO={"),
    ("// an answer is the Owner's own commit: the button copies the three lines and opens the file on the forge under their login —\n"
     '// no server, no token, and the seat that asked is nowhere in the path. The commit\'s author is the proof.\n'
     '// Two buttons — accept · reject — open a dialog that shows the whole ask with its context, so the Owner can look and\n'
     '// abort. OK yields ONE command: `--answer <id> accept|reject "text"` — the tool cuts the answer branch, writes the\n'
     '// three lines, commits SIGNED and pushes. A browser cannot sign; the dialog decides, the terminal signs.\n',
     ''),
    ('    <p class="dq">${esc(ask)}</p>${prop?`<p class="dp"><b>${l("answer.proposal")}</b> ${esc(prop)}</p>`:""}<p class="m ddim">${esc(t[6])}</p>\n',
     '    <p class="dq">${esc(ask)}</p>${prop?`<p class="dp"><b>${l("answer.proposal")}</b> ${esc(prop)}</p>`:""}<p class="m ddim">${esc(t[6])}</p>\n'
     '    <p class="dp proof">${lh("proof.dialog",`<b class=\"pw${PROOF.state==\"author\"?\" au\":\"\"}\">${l(PROOF.word)}</b>`)}</p>${PROOF.why?`<p class="cq">${l(PROOF.why)}</p>`:""}\n'),
    ('// THE SECOND SCREEN (FM-013). OK used to disable itself and leave one button — abort — which read as taking the\n'
     '// decision back. The decision is made; the terminal signs it. This screen says first whether the command is on the clipboard, then what to run,\n'
     '// where, what it does step by step, what the end looks like, how to check it and where to go when signing fails — and has ONE way out, done\n'
     '// (Esc too: it is the dialog\'s own). It says the command is on the clipboard only when the clipboard said so: from a file there may be none.\n',
     ''),
    ('const sign=(d,id,line,said,kind="answer")=>{const br=`answer/${id.toLowerCase()}`,c=s=>`<code>${esc(s)}</code>`;\n'
     '  d.innerHTML=`<form method="dialog" class="sign"><h3>${l(kind=="answer"?"answer.sign.title":"act.sign.title")} · <a href="#=${id}">${id}</a></h3>\n',
     'const sign=(d,id,line,said,kind="answer")=>{const br=`answer/${id.toLowerCase()}`,c=s=>`<code>${esc(s)}</code>`,P=PROOF.keys;\n'
     '  d.innerHTML=`<form method="dialog" class="sign"><h3>${l(kind=="answer"?P.title:P.act)} · <a href="#=${id}">${id}</a></h3>\n'),
    ('    <p class="dp">${l("answer.sign.intro")}</p><pre class="cmd">${esc(line)}</pre>\n',
     '    <p class="dp">${l(P.intro)}</p><pre class="cmd">${esc(line)}</pre>\n'),
    ('    <li>${l("answer.sign.step.commit")}</li><li>${l("answer.sign.step.push")}</li></ol><p class="ddim">${l("answer.sign.slow")}</p>\n'
     '    <h4>${l("answer.sign.success")}</h4><pre>${esc(`${id} ${kind=="answer"?"answered: ":""}${said}\\n  signed, on \\`${br}\\`, pushed`)}</pre>\n'
     '    <h4>${l("answer.sign.check")}</h4><p>${lh("answer.sign.check.text",c(`git log -1 --format=%G? ${br}`),c("G"))}</p>\n'
     '    <h4>${l("answer.sign.fail")}</h4><p>${lh("answer.sign.fail.text",`<a href="${l("answer.sign.url")}" target="_blank" rel="noopener">${l("answer.sign.page")}${ICO.out}</a>`)}</p>\n',
     '    <li>${l(P.commit)}</li><li>${l("answer.sign.step.push")}</li></ol><p class="ddim">${l("answer.sign.slow")}</p>\n'
     '    ${PROOF.said?`<h4>${l("answer.sign.success")}</h4><pre>${esc(`${id} ${kind=="answer"?"answered: ":""}${said}\\n  ${PROOF.said}, on \\`${br}\\`, pushed`)}</pre>`:""}\n'
     '    ${P.check?`<h4>${l("answer.sign.check")}</h4><p>${lh(P.check,c(`git log -1 --format=${PROOF.format} ${br}`),c("G"))}</p>`:""}\n'
     '    <h4>${l("answer.sign.fail")}</h4><p>${lh(P.fail,`<a href="${l("answer.sign.url")}" target="_blank" rel="noopener">${l("answer.sign.page")}${ICO.out}</a>`)}</p>\n'),
    ('      w.length?[old>=0?l("waiting.oldest",old):"",held.length?l("waiting.holds",held.length):"",w.length>5?l("waiting.bottleneck",w.length,held.length):""].filter(Boolean).map(s=>"· "+s).join(" "):""),\n'
     '    w.slice(0,14).map(t=>row(idl(t[0]),t[29][0]?esc(t[29][0]):`<i>${l("waiting.unasked")}</i> — ${esc(t[6])}`,t[29][1]?l("ask."+t[29][1]):"",\n',
     '      w.length?[old>=0?l("waiting.oldest",old):"",held.length?l("waiting.holds",held.length):"",w.length>5?l("waiting.bottleneck",w.length,held.length):"",\n'
     "      // FM-007: how an answer here is proved — the same for every ask on one repository's board, so said once, here, before *accept*:\n"
     "      // a state, its word in ink; where the author is all it proves, its consequence the line beneath, the warning colour's (PROOF, `proof_page`)\n"
     '      lh("proof.here",`<b class=\"pw${PROOF.state==\"author\"?\" au\":\"\"}\">${l(PROOF.word)}</b>`)].filter(Boolean).map(s=>"· "+s).join(" "):""),\n'
     '    (w.length&&PROOF.why?`<p class="cq">${l(PROOF.why)}</p>`:"")+w.slice(0,14).map(t=>row(idl(t[0]),t[29][0]?esc(t[29][0]):`<i>${l("waiting.unasked")}</i> — ${esc(t[6])}`,t[29][1]?l("ask."+t[29][1]):"",\n'),
)
PR_C_JOIN_EDITS = (
    ('"waiting.malformed": "{0} asks sent back — not for you", ', '"waiting.malformed": "{0} asks sent back — not for you", "waiting.malformed.one": "1 ask sent back — not for you", '),
    ('+(sent.length?`<p class="sub">${l("waiting.malformed",sent.length)}</p>`+sent.map(t=>row(idl(t[0]),t[29][0]?esc(t[29][0]):`<i>${l("waiting.unasked")}</i>`,"",esc(t[29][7][0]),"")).join(""):"")',
     '+(sent.length?`<p class="sub">${sent.length==1?l("waiting.malformed.one"):l("waiting.malformed",sent.length)}</p>`+sent.map(t=>row(idl(t[0]),t[29][0]?esc(t[29][0]):`<i>${l("waiting.unasked")}</i>`,"",esc(t[29][7][0]).replace(/`([^`]+)`/g,"<code>$1</code>"),"")).join(""):"")'),
    ('#dlg pre{font:inherit;margin:6px 0;padding:0 0 0 2ch;border-left:2px solid var(--line);white-space:pre-wrap;word-break:break-all}\n',
     '#dlg pre{font:inherit;margin:6px 0;padding:0 0 0 2ch;border-left:2px solid var(--line);white-space:pre-wrap;overflow-wrap:anywhere}\n'),
    ('.day{margin:6px 0 0}\n', '.day{margin:6px 0 0}.dr{flex-wrap:wrap;margin:8px 0 4px}.dr .c{color:var(--dim);font-weight:400;flex:1 1 20ch}.dr .act{margin-left:auto;font-weight:400}.dr .why{flex:1 1 100%;font-weight:400}\n'),
    ('  // the registry, a report of the trailers (FM-024, FM-032): the day — who committed in the last 24 hours, where — one fold, open on a desktop\n'
     '  if(REG&&REG.groups.length){const [t0,st]=split(l("sessions.recent",REG.parents,REG.all));\n'
     '    S.push(sec(hd("h2",l("day.title"),"· "+l("day.span")),`<div class="day">`+fold(hd("h3",t0,st),REG.groups.map(g=>`<details class="grp"><summary>${esc(g[0])} ${esc(g[1])} (${esc(g[2])})${g[3].length?`<span class="subs">+ ${g[3].map(esc).join(" · ")}</span>`:""}</summary>`\n'
     '      +g[4].map(m=>`<span class="aq">${esc(m[0])} (${esc(m[1])}) · ${esc(m[2])} · ${esc(m[3])}</span>`).join("\\n")+"</details>").join(""),!PHONE)+"</div>"))}\n',
     '  {const [t0,st]=REG&&REG.groups.length?split(l("sessions.recent",REG.parents,REG.all)):["",""];\n'
     '    S.push(sec(hd("h2",l("day.title"),"· "+l("day.span")),`<div class="day"><h3 class="sh dr">${$("day-row-standup").innerHTML}</h3>`+(REG&&REG.groups.length?fold(hd("h3",t0,st),REG.groups.map(g=>`<details class="grp"><summary>${esc(g[0])} ${esc(g[1])} (${esc(g[2])})${g[3].length?`<span class="subs">+ ${g[3].map(esc).join(" · ")}</span>`:""}</summary>`\n'
     '      +g[4].map(m=>`<span class="aq">${esc(m[0])} (${esc(m[1])}) · ${esc(m[2])} · ${esc(m[3])}</span>`).join("\\n")+"</details>").join(""),!PHONE):"")\n'
     '      +`<h3 class="sh dr">${$("day-row-closeout").innerHTML}</h3></div>`))}\n'),
)

# the board's next pass: each change it makes to this fixture's page — (the joined page's text, the candidate's), whole lines and the labels
# item by item, each where it occurs once — applied in order after the join's edits
BOARD_POLISH_EDITS = (
    ("/* the header line: the name, then the search as a prompt line — its box is the field's; the count stands in it. Where the line is short the\n   count wraps under the field, inside the box, and the field keeps its 200 px; on a phone the search takes a row of its own (RV-3342). The\n   count stands at the field's right edge, on the field's line where it fits and on a line of its own where it does not (BF-2) */\n",
     ''),
    ('#sb{flex:1 1 calc(200px + 4ch);display:flex;flex-wrap:wrap;align-items:center;column-gap:1ch;border:1px solid var(--mute);padding:0 1ch;min-width:0}\n',
     '#sb{flex:1 1 calc(200px + 4ch);display:flex;align-items:center;column-gap:1ch;border:1px solid var(--mute);padding:0 1ch;min-width:0}\n'),
    ('#n{color:var(--dim);padding:3px 0;margin-left:auto;text-align:right}\n',
     '.rd{display:inline-flex;align-items:center;gap:.7ch;color:var(--dim);cursor:pointer;white-space:nowrap}\n.rd input{-webkit-appearance:none;appearance:none;margin:0;width:13px;height:13px;border:1px solid var(--mute);border-radius:50%;background:none;flex:none;cursor:pointer}\n.rd input:checked{border-color:var(--ink);background:radial-gradient(circle,var(--bg) 0 2.5px,var(--ink) 3px)}.rd input:checked+span,.rd:hover{color:var(--ink)}\n.rd:hover input{border-color:var(--ink)}.rd input:focus-visible{outline:1px solid var(--ink);outline-offset:2px}#sl{margin-left:auto}\n#sl input{width:26px;height:14px;border-radius:7px;background:radial-gradient(circle at 6px 50%,var(--mute) 0 3.5px,transparent 4px)}\n#sl input:checked{background:radial-gradient(circle at calc(100% - 6px) 50%,var(--bg) 0 3.5px,transparent 4px) var(--ink)}\n#n{color:var(--dim)}#n:before{content:"·";content:"·" / "";color:var(--mute);margin-right:1ch}\n'),
    ('button.act,#s,#vt button,#dlg button{line-height:17px;border:1px solid var(--mute);background:none;color:var(--dim);padding:1px 1ch;margin:0 0 0 1ch;white-space:nowrap;vertical-align:baseline}\nbutton.act:hover,#s:hover,#vt button:hover,#dlg button:hover{background:var(--raise);color:var(--ink);border-color:var(--ink)}\n',
     'button.act,#dlg button{line-height:17px;border:1px solid var(--mute);background:none;color:var(--dim);padding:1px 1ch;margin:0 0 0 1ch;white-space:nowrap;vertical-align:baseline}\nbutton.act:hover,#dlg button:hover{background:var(--raise);color:var(--ink);border-color:var(--ink)}\n'),
    ('button[aria-pressed=true]{color:var(--ink);border-color:var(--ink)}button:disabled{opacity:.4}\n',
     'button:disabled{opacity:.4}\n'),
    ('.sh{font:inherit;font-weight:600;margin:0;display:flex;align-items:baseline;gap:0 1ch;color:var(--head)}.sh>span:first-child{flex:none}\n',
     '.sh{font:inherit;font-weight:600;margin:0;display:flex;align-items:baseline;gap:0 1ch;color:var(--head)}.sh>span:first-child{flex:none}#p .sh b{font-weight:600}\n'),
    ('.vok .ty{color:var(--teal);font-weight:600}.vwarn .ty{color:var(--amber);font-weight:600}.vfail .ty{color:var(--coral);font-weight:600}\n',
     '.vok .ty{color:var(--teal);font-weight:600}.vwarn .ty{color:var(--amber);font-weight:600}.vfail .ty{color:var(--coral);font-weight:600}\n.rv .what{grid-template-columns:8ch 1fr}.rv .how{display:block;padding-left:9ch}.rv a{text-decoration:underline;text-underline-offset:3px;text-decoration-color:var(--mute)}\ndetails.more{border-top:1px solid var(--line)}details.more>summary{color:var(--dim);padding:3px 0 3px 9ch}\ndetails.more>summary:before{content:"> ";content:"> " / "";color:var(--mute)}details.more[open]>summary:before{content:"v ";content:"v " / ""}\n'),
    ('#vt{display:flex;flex-wrap:wrap;align-items:baseline;gap:4px 1ch;margin:22px 0 6px}#vt button{margin:0}\n',
     '#vt{display:flex;flex-wrap:wrap;align-items:baseline;gap:4px 1ch;margin:22px 0 6px}\n#gv,#ov{display:inline-flex;align-items:center;flex-wrap:wrap;gap:0 2ch}#ov[hidden]{display:none}#gw{color:var(--dim)}\n#ov:before{content:"·";content:"·" / "";color:var(--mute);margin-right:-1ch}\n'),
    ("/* the claim and the running line: the last line's one element `#F`; the claim shown with the board only, as when it stood in it */\n#f{color:var(--mute);margin:28px 0 0}#f:empty{display:none}#B[hidden]~#F #f{display:none}\n/* the running line: the tool's, on every screen — its mark at 16 px, the smallest size its 16-unit grid stays sharp at, the name linking to\n   the tool and leaving the board; the version to its release */\n#r{display:flex;gap:1ch;align-items:center;margin:20px 0 0;color:var(--mute);font-size:12px;line-height:16px}#r a:first-child{display:flex;gap:6px;align-items:center}#r svg{flex:none}#r svg.ico{margin:0}\n/* a phone: at least 24 px for every button, a heading's state flows under its title, its marker keeping its space (BF-5); the search a header\n   row of its own, the scheme's button under it at the right edge (RV-3342) */\n@media(max-width:640px){button.act,#s,#vt button,#dlg button{min-height:24px;padding:3px 1ch}.sh{display:block}.sh:before{margin-right:1ch}.how .acts{display:block;margin:4px 0 0}\n#sb{flex-basis:100%}#s{margin-left:auto}}\n/* a phone: the work table, wider than the page with its columns as they are, scrolls in its own box — the header, the box and the toolbar stay put (BF-14) */\n@media(max-width:640px){#B>table{display:block;overflow-x:auto}}\n",
     '#r{display:flex;justify-content:flex-end;gap:1ch;align-items:center;margin:28px 0 0;color:var(--mute);font-size:12px;line-height:16px}#r a:first-child{display:flex;gap:6px;align-items:center}#r svg{flex:none}#r svg.ico{margin:0}\n@media(max-width:640px){button.act,#dlg button{min-height:24px;padding:3px 1ch}.rd{min-height:24px}.rv .how{padding-left:0}.sh{display:block}.sh:before{margin-right:1ch}.how .acts{display:block;margin:4px 0 0}\n#sb{flex-basis:100%;order:1}#n{flex-basis:100%}#n:before{display:none}}\n@media(max-width:640px){#B>table,#b{display:block}#B>table>thead{display:none}#b>tr:not([hidden]),#b>tr>td{display:block}#b>tr>td.x{display:none}\n#b>tr.t{display:flex;flex-wrap:wrap;align-items:baseline;column-gap:2ch;padding-left:calc(2ch + 5px);border-top:1px solid var(--line)}#b>tr.t>td{border-top:0}\n#b>tr.t>td:first-child{margin-left:calc(-2ch - 5px)}#b>tr.t>td:last-child{flex:1 1 100%;padding-top:0;overflow-wrap:anywhere}}\n'),
    ('@media print{#s,#sb,#vt{display:none}:root{--bg:#fff;--ink:#000;--dim:#333;--mute:#555;--line:rgba(0,0,0,.25)}}\n',
     '@media print{#sl,#sb,#vt{display:none}:root{--bg:#fff;--ink:#000;--dim:#333;--mute:#555;--line:rgba(0,0,0,.25)}}\n'),
    ('<div id="B"><div id="H"><b>Git entry differential fixture</b><span data-l="tagline"></span><label id="sb"><input id="q" autofocus><span id="n"></span></label><button id="s"></button></div>\n',
     '<div id="B"><div id="H"><b>Git entry differential fixture</b><span data-l="tagline"></span><label id="sb"><input id="q" autofocus></label><label id="sl" class="rd"><input type="checkbox" role="switch" id="s"><span data-l="scheme.toggle"></span></label></div>\n'),
    ('<div id="vt"><button id="g" aria-pressed="true"></button><button id="o" aria-pressed="true" data-l="view.open"></button><button id="a" aria-pressed="false" data-l="view.all"></button>\n',
     '<div id="vt"><span id="gv" role="radiogroup" aria-labelledby="gw"></span><span id="ov" role="radiogroup" aria-labelledby="ovo ova"><label class="rd"><input type="radio" name="ov" value="open" checked><span id="ovo" data-l="view.open"></span></label><label class="rd"><input type="radio" name="ov" value="all"><span id="ova" data-l="view.all"></span></label></span><span id="n"></span>\n'),
    ('<footer id="F"><p id="f" class="m" data-l="footer"></p>\n<p id="r" class="m"><a href="https://github.com/shoalmark/shoalmark" target="_blank" rel="noopener" aria-label="shoalmark on GitHub"><svg viewBox="0 0 16 16" width="16" height="16" fill="currentColor" shape-rendering="crispEdges" aria-hidden="true"><path d="M4 0h1v1h-1ZM11 0h1v1h-1ZM0 1h1v1h-1ZM4 1h1v1h-1ZM11 1h1v1h-1ZM15 1h1v1h-1ZM1 2h1v1h-1ZM5 2h1v1h-1ZM10 2h1v1h-1ZM14 2h1v1h-1ZM2 3h1v1h-1ZM5 3h1v1h-1ZM10 3h1v1h-1ZM13 3h1v1h-1ZM3 4h1v1h-1ZM6 4h1v1h-1ZM9 4h1v1h-1ZM12 4h1v1h-1ZM4 5h1v1h-1ZM6 5h1v1h-1ZM9 5h1v1h-1ZM11 5h1v1h-1ZM5 6h1v1h-1ZM7 6h2v1h-2ZM10 6h1v1h-1ZM6 7h4v1h-4ZM7 8h2v1h-2ZM7 9h2v1h-2ZM7 10h2v1h-2ZM7 11h2v1h-2ZM7 12h2v1h-2ZM7 13h2v1h-2ZM7 14h2v1h-2ZM7 15h2v1h-2Z"></path></svg>shoalmark<svg class="ico" viewBox="0 0 12 12" width="12" height="12" fill="currentColor" shape-rendering="crispEdges" aria-hidden="true"><path d="M0 2h4v1h-4ZM0 3h1v8h-1ZM9 8h1v3h-1ZM0 11h10v1h-10ZM6 0h6v1h-6ZM11 1h1v5h-1ZM10 1h1v1h-1ZM9 2h1v1h-1ZM8 3h1v1h-1ZM7 4h1v1h-1ZM6 5h1v1h-1ZM5 6h1v1h-1Z"></path></svg></a> · <a href="https://github.com/shoalmark/shoalmark/releases/tag/v0.19.4" target="_blank" rel="noopener" aria-label="release v0.19.4">v0.19.4</a></p></footer>\n',
     '<footer id="F"><p id="r" class="m"><a href="https://github.com/shoalmark/shoalmark" target="_blank" rel="noopener" aria-label="shoalmark on GitHub"><svg viewBox="0 0 16 16" width="16" height="16" fill="currentColor" shape-rendering="crispEdges" aria-hidden="true"><path d="M4 0h1v1h-1ZM11 0h1v1h-1ZM0 1h1v1h-1ZM4 1h1v1h-1ZM11 1h1v1h-1ZM15 1h1v1h-1ZM1 2h1v1h-1ZM5 2h1v1h-1ZM10 2h1v1h-1ZM14 2h1v1h-1ZM2 3h1v1h-1ZM5 3h1v1h-1ZM10 3h1v1h-1ZM13 3h1v1h-1ZM3 4h1v1h-1ZM6 4h1v1h-1ZM9 4h1v1h-1ZM12 4h1v1h-1ZM4 5h1v1h-1ZM6 5h1v1h-1ZM9 5h1v1h-1ZM11 5h1v1h-1ZM5 6h1v1h-1ZM7 6h2v1h-2ZM10 6h1v1h-1ZM6 7h4v1h-4ZM7 8h2v1h-2ZM7 9h2v1h-2ZM7 10h2v1h-2ZM7 11h2v1h-2ZM7 12h2v1h-2ZM7 13h2v1h-2ZM7 14h2v1h-2ZM7 15h2v1h-2Z"></path></svg>shoalmark<svg class="ico" viewBox="0 0 12 12" width="12" height="12" fill="currentColor" shape-rendering="crispEdges" aria-hidden="true"><path d="M0 2h4v1h-4ZM0 3h1v8h-1ZM9 8h1v3h-1ZM0 11h10v1h-10ZM6 0h6v1h-6ZM11 1h1v5h-1ZM10 1h1v1h-1ZM9 2h1v1h-1ZM8 3h1v1h-1ZM7 4h1v1h-1ZM6 5h1v1h-1ZM5 6h1v1h-1Z"></path></svg></a> · <a href="https://github.com/shoalmark/shoalmark/releases/tag/v0.19.4" target="_blank" rel="noopener" aria-label="release v0.19.4">v0.19.4</a></p></footer>\n'),
    ('"tagline": "", "footer": "", ',
     '"tagline": "", "lang": "en", '),
    ('"view.all": "all", "scheme.auto": "auto", "scheme.light": "light", "scheme.dark": "dark", "scheme.button": "light or dark: {0}", ',
     '"view.all": "all", "scheme.toggle": "dark", '),
    ('"reviews.sessions.more": "{0} and {1} more", ',
     '"reviews.sessions.more": "{0} and {1} more", "reviews.more": "and {0} more verdicts by another session this week", "reviews.more.one": "and 1 more verdict by another session this week", '),
    ('  // …and the week\'s verdicts and who gave them: folded, its heading carrying the counts in words — reports, not proofs; one row per verdict\n  // a verdict\'s branch (RV-3343): the one that holds the verdict on its own line, or the merge that names it; else ambiguous or not known, with why —\n  // in the row\'s own colour: nothing on a verdict\'s row is coloured but its word (G3, BF-10)\n  const brn=b=>b[0]=="line"?lh("reviews.branch",`<code>${esc(b[1])}</code>`):b[0]=="merge"?lh("reviews.branch.merged",`<code>${esc(b[1])}</code>`,`<code>${esc(b[2].slice(0,10))}</code>`)\n',
     '  const cid=(sha,url)=>url?`<a href="${esc(url)}" target="_blank" rel="noopener"><code>${esc(sha.slice(0,7))}</code></a>`:`<code>${esc(sha.slice(0,7))}</code>`,\n  brn=(b,u)=>b[0]=="line"?lh("reviews.branch",`<code>${esc(b[1])}</code>`):b[0]=="merge"?lh("reviews.branch.merged",`<code>${esc(b[1])}</code>`,cid(b[2],u))\n'),
    ('    :`<i>${lh("reviews.branch.unknown",b[0]=="unnamed"?lh("reviews.branch.unnamed",`<code>${esc(b[1].slice(0,10))}</code>`):l("reviews.branch.none"))}</i>`;\n  if(REG&&REG.reviews){const r=REG.reviews,[t0,st]=split(l("reviews.title")),word={"independent":"reviews.word.another","untraced":"reviews.word.untraced","on trunk":"reviews.word.trunk"};\n',
     '    :`<i>${lh("reviews.branch.unknown",b[0]=="unnamed"?lh("reviews.branch.unnamed",cid(b[1],u)):l("reviews.branch.none"))}</i>`;\n  if(REG&&REG.reviews){const r=REG.reviews,[t0,st]=split(l("reviews.title")),word={"independent":"reviews.word.another","untraced":"reviews.word.untraced","on trunk":"reviews.word.trunk"},\n    vr=v=>row(cid(v[0],(v[8]||[])[0]),lh("reviews.on",cid(v[1],(v[8]||[])[1]))+" · "+brn(v[6]||["none"],(v[8]||[])[2]),v[5]?l("verdict."+v[5]):l("type.verdict"),\n        (v[4]=="same session"?`<b>${l("reviews.word.same")}</b>`:l(word[v[4]]||"reviews.word.untraced"))+(v[4]=="on trunk"?"":" · "+lh("reviews.sessions",esc(v[2]||"—"),v[3].length>1?lh("reviews.sessions.more",esc(v[7]),v[3].length-1):esc(v[3][0]||"—"))),"","",["rv",VERDICT[v[5]]].filter(Boolean).join(" ")),\n    folds=v=>v[4]=="independent"&&(v[5]=="READY"||v[5]=="READY TO TAG"),week=REG.verdicts||[],more=week.filter(folds);\n'),
    ('      (REG.verdicts||[]).map(v=>row(`<code>${esc(v[0].slice(0,10))}</code>`,lh("reviews.on",`<code>${esc(v[1].slice(0,10))}</code>`)+" · "+brn(v[6]||["none"]),v[5]?l("verdict."+v[5]):l("type.verdict"),\n        (v[4]=="same session"?`<b>${l("reviews.word.same")}</b>`:l(word[v[4]]||"reviews.word.untraced"))+(v[4]=="on trunk"?"":" · "+lh("reviews.sessions",esc(v[2]||"—"),v[3].length>1?lh("reviews.sessions.more",esc(v[7]),v[3].length-1):esc(v[3][0]||"—"))),"","",VERDICT[v[5]])).join(""),false))}\n',
     '      week.filter(v=>!folds(v)).map(vr).join("")+(more.length?`<details class="more"><summary>${more.length==1?l("reviews.more.one"):l("reviews.more",more.length)}</summary>${more.map(vr).join("")}</details>`:""),false))}\n'),
    ('  $("o").hidden=$("a").hidden=gname=="board";   // the board shows everything — open/all has nothing to say there\n  $("g").textContent=L["view.by"].replace("{0}",vn(gname));$("p").hidden=gname!="board"||!!q;$("p").innerHTML=`<span class="pt">${l("owner.title")}</span>`+(gname=="board"&&!q?box():"");   // the box keeps its title in every view (FM-002 R2)\n',
     '  $("ov").hidden=gname=="board";\n  for(const r of document.querySelectorAll("#gv input,#ov input"))r.checked=r.name=="gv"?+r.value==gi:(r.value=="all")==all;\n  $("p").hidden=!!q;$("p").innerHTML=`<span class="pt">${l("owner.title")}</span>`+(!q?box():"");\n'),
    ('$("g").onclick=()=>{gi=(gi+1)%GROUPS.length;draw()};\nfor(const[id,v]of[["o",false],["a",true]])$(id).onclick=()=>{all=v;$("o").setAttribute("aria-pressed",!v);$("a").setAttribute("aria-pressed",v);draw()};\n',
     '{const [w,rest]=(L["view.by"]??"by {0}").split("{0}");$("gv").innerHTML=`<span id="gw">${esc(w.trim())}</span>`\n  +GROUPS.map(([g],i)=>`<label class="rd"><input type="radio" name="gv" value="${i}"${i==gi?" checked":""}><span>${esc(vn(g))}</span></label>`).join("")+(rest?.trim()?`<span>${esc(rest.trim())}</span>`:"")}\n$("gv").onchange=e=>{gi=+e.target.value;draw()};\n$("ov").onchange=e=>{all=e.target.value=="all";draw()};\n'),
    ('// light or dark is the viewer\'s choice: auto follows the system; the other two switch the page\'s own\n// `prefers-color-scheme` rules on or off. Paper stays light.\nconst ORIG=new Map(),SCHEMES=["auto","light","dark"],PCS=/\\(\\s*prefers-color-scheme\\s*:\\s*(dark|light)\\s*\\)/g;\nlet scheme="auto";try{scheme=localStorage.getItem("shoalmark.scheme")||"auto"}catch(e){}if(!SCHEMES.includes(scheme))scheme="auto";\n',
     '// WebKit draws an image\'s own `prefers-color-scheme` rules by the system\'s scheme, never the page\'s: the logo\'s SVG is written again with\n// the rule of the scheme in effect on\nconst ORIG=new Map(),PCS=/\\(\\s*prefers-color-scheme\\s*:\\s*(dark|light)\\s*\\)/g,SYS=matchMedia("(prefers-color-scheme: dark)"),sys=()=>SYS.matches?"dark":"light",\nLOGO=(i=>i&&/^data:image\\/svg\\+xml;base64,/.test(i.getAttribute("src"))?[i,new TextDecoder().decode(Uint8Array.from(atob(i.getAttribute("src").slice(26)),c=>c.charCodeAt(0)))]:null)(document.querySelector("#H>img"));\nlet scheme="auto";try{scheme=localStorage.getItem("shoalmark.scheme")||"auto"}catch(e){}if(scheme!="light"&&scheme!="dark")scheme="auto";\n'),
    ('  document.documentElement.style.colorScheme=m=="auto"?"":m},\nsetScheme=m=>{scheme=m;paint(m);$("s").textContent=(L["scheme.button"]??"{0}").replace("{0}",L["scheme."+m]??m);$("s").dataset.scheme=m;try{localStorage.setItem("shoalmark.scheme",m)}catch(e){}};\n$("s").onclick=()=>setScheme(SCHEMES[(SCHEMES.indexOf(scheme)+1)%3]);setScheme(scheme);addEventListener("load",()=>paint(scheme));\n',
     '  document.documentElement.style.colorScheme=m=="auto"?"":m;const e=m=="auto"?sys():m;\n  if(LOGO)LOGO[0].src="data:image/svg+xml;charset=utf-8,"+encodeURIComponent(LOGO[1].replace(PCS,(x,w)=>w==e?"(min-width:0px)":"(max-width:0px)"))},\nsetScheme=m=>{scheme=m;paint(m);$("s").checked=(m=="auto"?sys():m)=="dark";try{m=="auto"?localStorage.removeItem("shoalmark.scheme"):localStorage.setItem("shoalmark.scheme",m)}catch(e){}};\n$("s").onchange=()=>{const want=$("s").checked?"dark":"light";setScheme(want==sys()?"auto":want)};\nSYS.addEventListener?.("change",()=>setScheme(scheme));setScheme(scheme);addEventListener("load",()=>paint(scheme));\n'),
)


def joined_transform(page):
    """The baseline's page as the join changes it: FM053_PAGE_EDITS, FM054_ON_A2_EDITS and PR_C_JOIN_EDITS applied in order, each to text that
    occurs exactly once — else None."""
    page = fm053_transform(page)
    if page is None:
        return None
    text = page.decode("utf-8")
    for old, new in FM054_ON_A2_EDITS + PR_C_JOIN_EDITS + BOARD_POLISH_EDITS:
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
        if PROOF_MARK in old_page or V2_MARK in old_page or fm057_page_dropped(day_dropped_joined(new_page)) != joined_transform(old_page):
            return False
        candidate = with_board(candidate, PAGE_PATH, old_page)
    return fm057_board(baseline, candidate)


def snapshots_match(baseline, candidate):
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
    """A copy of an observed run whose file `path` held `data` after the run — for the allowances' controls."""
    after = dict(observed["after"], **{path: hashlib.sha256(data).hexdigest()})
    return dict(observed, after=after, **({"index_after": serial(data)} if path == INDEX_PATH else {"page_after": serial(data)} if path == PAGE_PATH else {}))


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
                observed.update(starts_raw=observed["starts"], run_calls_raw=observed["run_calls"],
                                starts=board_settings_undone(observed["starts"], version == "candidate"),
                                run_calls=board_settings_undone(observed["run_calls"], version == "candidate"))
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
            assert_control(label_prefix + "all actual process argv/effective cwd/env match, once FM-057's reads, the starts `origin_undone` removes and FM-054's "
                           "reads of the default branch's configuration, each a read, are set aside",
                           rows_match(origin_undone(before["starts"]), fm054_own(after["starts"]), counted) and not fm054_reads(before["starts"])
                           and all(fm054_read(row["argv"]) for row in fm054_reads(after["starts"])))
            assert_control(label_prefix + "run options and actual process results match, once FM-057's reads, the starts `origin_undone` removes and FM-054's "
                           "reads, each a read, are set aside",
                           rows_match(origin_undone(before["run_calls"]), fm054_own(after["run_calls"]), counted) and not fm054_reads(before["run_calls"])
                           and all(isinstance(row.get("args"), list) and row["args"] and fm054_read(row["args"][0]) for row in fm054_reads(after["run_calls"])))
            assert_control(label_prefix + "the candidate reads the working tree's edits once where the baseline reads them, and not where it does not",
                           edit_reads(after["starts_raw"]) == (1 if edit_reads(before["starts_raw"]) else 0))
            assert_control(label_prefix + "consumer byte/symlink/ref/config/hook snapshots match", snapshots_match(before, after))
            unasked = lambda entries: [{key: value for key, value in entry.items() if key != "ASK_ORIGIN"} for entry in entries]
            refuses = ask or label in ("dirty-check-fallback", "dirty-default-fallback")
            assert_control(label_prefix + "actual main state/result match with `ASK_ORIGIN` set aside; the baseline's origin policy is the case's, and the "
                           "candidate's is set for `--check` and the default run whatever the working tree holds",
                           unasked(before["main_returns"]) == unasked(after["main_returns"]) and bool(after["main_returns"])
                           and before["main_returns"][-1]["ASK_ORIGIN"] is ask and after["main_returns"][-1]["ASK_ORIGIN"] is refuses)
            assert_control(label_prefix + "Git entry emits no SVN limitation", "protected SVN acceptance" not in before["stdout"] + before["stderr"] + after["stdout"] + after["stderr"])
            assert_control(label_prefix + "production writes confined to disposable fixture", all(Path(value).is_relative_to(top)
                           for observed in pair for write in observed["writes"] for key, value in write.items() if key in ("path", "destination")))
            assert_control(label_prefix + "foreign hook repository bytes/refs/config remain unchanged", all(observed["foreign_before"] == observed["foreign_after"] for observed in pair))
            if readonly:
                assert_control(label_prefix + "read-only entry leaves consumer snapshot identical", all(observed["before"] == observed["after"] for observed in pair))
            if label in ("clean-check-origin", "dirty-check-fallback", "clean-default-origin", "dirty-default-fallback"):
                probe_argv = {"baseline": ["git", "diff", "--name-only", "--relative", "--ignore-submodules=none", "HEAD"],
                              "candidate": ["git", "diff", "-z", "--name-only", "--relative", "--ignore-submodules=dirty", "HEAD"]}
                main_probe = lambda observed: [row for row in observed["starts_raw"] if same_start(row["argv"], row.get("raw"), probe_argv[observed["version"]])
                                              and ("main" in row["product_stack"] and "worktree_edited" in row["product_stack"]
                                                   and "read_changes" not in row["product_stack"] if observed["version"] == "baseline"
                                                   else "worktree_edits" in row["product_stack"])]
                probes = [main_probe(observed) for observed in pair]
                assert_control(label_prefix + "the working tree's edit read actually runs once at consumer cwd: the baseline's from `main`'s probe, the "
                               "candidate's from `worktree_edits`", all(len(probe) == 1 and probe[0]["cwd"] == str(root) for probe in probes))
                assert_control(label_prefix + "that read drops all eight actual hook/pathspec contamination keys", all(set(POISON_KEYS).issubset(observed["invocation_environment"])
                               and len(probe) == 1 and not set(POISON_KEYS).intersection(probe[0]["environment"]) for observed, probe in zip(pair, probes)))
                assert_control(label_prefix + "candidate routes that read through common boundary", len(probes[1]) == 1
                               and all("vcs_process" in row["product_stack"] for row in probes[1]) and all("vcs_process" not in row["product_stack"] for row in probes[0]))
                if condition == "dirty":
                    assert_control(label_prefix + "dirty tree selects uncommitted fallback", all(observed["main_returns"][-1]["WALK"] == "uncommitted" for observed in pair))
                asks = lambda observed: sum(same_start(row["argv"], row.get("raw"), ["git", "ls-remote", "--symref", "origin", "HEAD"]) for row in observed["starts_raw"])
                if label == "clean-default-origin":
                    assert_control(label_prefix + "clean default starts no `ls-remote --symref origin HEAD`, and `origin_undone` removes exactly one from the baseline's starts",
                                   asks(after) == 0 and asks(before) == 1)
                if label == "dirty-default-fallback":
                    assert_control(label_prefix + "dirty default asks no origin", all(not any(row["argv"][1:2] == ["ls-remote"] for row in observed["starts_raw"]) for observed in pair))

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
        new_starts, new_calls = fm054_own(new["starts"]), fm054_own(new["run_calls"])
        page, record = (base64.b64decode(new["board_after"][path]["bytes_base64"]) for path in (PAGE_PATH, BUILT_PATH))
        old_ou = origin_undone(old["starts"])
        assert_control(allowance + "the default run's starts and calls differ by FM-057's reads and the starts `origin_undone` removes alone, its page and record by what it read, and equal runs match",
                       old["starts"] != new_starts and fm057_rows(old_ou, new_starts) and fm057_rows(origin_undone(old["run_calls"]), new_calls)
                       and fm057_board(old, new) and rows_match(new_starts, new_starts) and snapshots_match(new, new))
        extra = dict(new_starts[0], argv=new_starts[0]["argv"][:1] + ["status", "--porcelain"])
        at = next(i for i, row in enumerate(new_starts) if git_words(row) == FM057_READS[2])
        assert_control(allowance + "one start more, or FM-057's reads apart or with one missing, does not match",
                       not rows_match(old_ou, new_starts + [extra])
                       and not rows_match(old_ou, new_starts[:at] + [extra] + new_starts[at:])
                       and not rows_match(old_ou, new_starts[:at] + new_starts[at + 1:]))
        bare = [row for row in new_starts if git_words(row) not in FM057_READS[2:]]
        assert_control(allowance + "a run that reads no changed path, as the board's own run (`--html-only`) does, differs by the two moved reads alone; the "
                       "changed-path reads where none are read, or none where a run counts them, do not match",
                       len(bare) == len(new_starts) - 2 and fm057_rows(old_ou, bare, counted=False)
                       and not fm057_rows(old_ou, new_starts, counted=False) and not fm057_rows(old_ou, bare, counted=True))
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
                       "templates, prompts and words, and by FM-057's page and the join's edits, alone, and equal snapshots still match",
                       bool(old_page) and old_page != new_page and fm057_page_dropped(day_dropped_joined(new_page)) == joined_transform(old_page) and snapshots_match(old, new)
                       and snapshots_match(new, new))
        opener = b'd.querySelector(".go").focus()}   // FM-030 day'
        variants = {
            "one byte outside the day": new_page.replace(b'<dialog id="dlg"></dialog>', b'<dialog id="dlg" open></dialog>', 1),
            "a fifth template": new_page.replace(b'\n<template id="day-standup">', b'\n<template id="day-closeout"></template>\n<template id="day-standup">', 1),
            "one line's mark dropped": new_page.replace(b"   // FM-030 day\n", b"\n", 1),
            "an unrelated statement appended to a permitted line": new_page.replace(opener, b'd.querySelector(".go").focus();document.title="Unrelated title"}   // FM-030 day', 1),
            "markup inside a template's text": new_page.replace(b'<template id="day-row-standup"><span>', b'<template id="day-row-standup"><span><img src=x onerror=alert(1)>', 1),
            "an attribute added to a template's button": new_page.replace(b'onclick="DAYOPEN(\'standup\')"', b'onclick="DAYOPEN(\'standup\')" onfocus="alert(1)"', 1),
        }
        changed = {name: page != new_page for name, page in variants.items()}
        assert_control(day + "a candidate page that also changes one byte outside the day, carries a fifth template, drops one line's mark, appends an "
                       f"unrelated statement to a permitted line, or adds markup or an attribute to a template does not match (each variant made: {changed})",
                       all(changed.values()) and not any(snapshots_match(old, with_board(new, PAGE_PATH, page)) for page in variants.values()))
        # FM-057's page, held the same way beside the day: each of its parts taken out exactly once, and nothing else differs
        page057, read_at = "Git entry FM-057 page allowance: ", FM057_READ_AT.search(new_page)
        assert_control(page057 + "the default run's page, FM-030's day and then FM-057's page taken out, is the baseline's with the join's edits, every "
                       "byte; the baseline's page holds neither", bool(read_at) and fm057_page_dropped(day_dropped_joined(new_page)) == joined_transform(old_page)
                       and day_dropped(old_page) is None and fm057_page_dropped(old_page) is None)
        at = read_at.group(0) if read_at else b"\n"
        variants057 = {
            "one byte more in the read-at line": new_page.replace(at, at.replace(b"nothing polls", b"nothing polls!"), 1),
            "the read-at line twice": new_page.replace(at, at * 2, 1),
            "the read-at line's style gone": new_page.replace(FM057_PAGE_LINES[0] + b"\n", b"\n", 1),
            "a word FM-057 does not name, beside its own": new_page.replace(b'"read.copy": "rebuild command"', b'"read.copy": "rebuild command", "read.more": "more"', 1),
        }
        made057 = {name: page != new_page for name, page in variants057.items()}
        assert_control(page057 + "a page whose read-at line has one byte more or stands twice, whose read-at style is gone, or that holds a word FM-057 "
                       f"does not name does not match (each variant made: {made057})",
                       all(made057.values()) and not any(snapshots_match(old, with_board(new, PAGE_PATH, page)) for page in variants057.values()))
        settings = "Git entry board settings allowance: "
        raw = new["starts_raw"]
        reads = [i for i, row in enumerate(raw) if "GIT_CONFIG_PARAMETERS" in (row.get("environment") or {}) and git_words(row)[:1] == ("log",)
                 and fm054_own([row])]
        def changed(i, **change):
            return raw[:i] + [dict(raw[i], **change)] + raw[i + 1:]
        if reads:
            at = reads[0]
            env_ = dict(raw[at]["environment"], GIT_CONFIG_PARAMETERS=raw[at]["environment"]["GIT_CONFIG_PARAMETERS"] + " 'core.pager=more'")
            argv_ = raw[at]["argv"] + ["--text"]
        assert_control(settings + "the default run's starts differ from the baseline's by the board's settings, the drivers' lists, the tag, the flag, the "
                       "read of `origin/master`, the edits read once, the starts `origin_undone` removes and FM-054's reads alone; left in, they do not match",
                       bool(reads) and rows_match(origin_undone(old["starts"]), fm054_own(board_settings_undone(raw, True))) and not rows_match(old["starts"], raw))
        assert_control(settings + "a start with a setting the board's are not, or with `--text` beside `--no-textconv` outside the board's own run, does not "
                       "match",
                       bool(reads) and not rows_match(origin_undone(old["starts"]), fm054_own(board_settings_undone(changed(at, environment=env_), True)))
                       and not rows_match(origin_undone(old["starts"]), fm054_own(board_settings_undone(changed(at, argv=argv_), True))))
        ask_row = next((row for row in old["starts"] if git_words(row) == ("ls-remote", "--symref", "origin", "HEAD")), None)
        assert_control("Git entry origin-ask allowance: the candidate starts no `ls-remote --symref origin HEAD`, and its starts with one added do not match "
                       "once `origin_undone` has removed the baseline's",
                       ask_row is not None and not any(git_words(row) == ("ls-remote", "--symref", "origin", "HEAD") for row in raw)
                       and not rows_match(origin_undone(old["starts"]), fm054_own(board_settings_undone(raw + [ask_row], True))))
        pairs = [i for i in range(1, len(raw)) if git_words(raw[i]) == TRUNK_READS[1] and git_words(raw[i - 1]) == TRUNK_READS[0] and fm054_own([raw[i]])]
        moved = raw[:pairs[0]] + raw[pairs[0] + 1:] + [raw[pairs[0]]] if pairs else raw
        assert_control("Git entry trunk-read allowance: the clean default run reads the cached `origin/master` directly after `origin/main`, and is taken "
                       "out only there; the same read anywhere else does not match",
                       bool(pairs) and not rows_match(origin_undone(old["starts"]), fm054_own(board_settings_undone(moved, True))))
        # FM-054's allowance is held to its difference on the same pair: the page carries PROOF, and only `proof_reading`'s reads are new
        fm054 = "Git entry FM-054 allowance: "
        reads = fm054_reads(new["starts"])
        assert_control(fm054 + "the default run's board reads the default branch's configuration — starts inside `proof_reading`, each a read, which the baseline never makes",
                       bool(reads) and all(fm054_read(row["argv"]) for row in reads) and not fm054_reads(old["starts"]))
        unstacked = [dict(row, product_stack=[s for s in row["product_stack"] if s != "proof_reading"]) for row in new["starts"]]
        strip = lambda entries: [{key: value for key, value in row.items() if key != "product_stack"} for row in entries]
        assert_control(fm054 + "the same reads made outside `proof_reading` are not set aside, and do not match the baseline's starts",
                       not rows_match(origin_undone(old["starts"]), fm054_own(unstacked)) and rows_match(origin_undone(old["starts"]), fm054_own(new["starts"])))
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
        section, row = b"tr.t{cursor:pointer}", b'"entry origin selection"'
        before_page = base64.b64decode(old["board_after"][PAGE_PATH]["bytes_base64"]) if isinstance((old.get("board_after") or {}).get(PAGE_PATH), dict) else b""
        assert_control(fm054 + "the candidate's page, FM-030's day and FM-057's page taken out, is the baseline's with A2's edits and then FM054_ON_A2_EDITS — "
                       "defect 8's edits as they stand on A2's page — applied, every byte; defect 8's own edits of the baseline fit neither page",
                       fm057_page_dropped(day_dropped_joined(page)) == joined_transform(before_page) and fm054_transform(page) is None
                       and bool(FM054_ON_A2_EDITS) and fm054_transform(before_page) is not None)
        cut = page.replace(section, b"")
        assert_control(fm054 + "a page that keeps PROOF but deletes an unrelated section (A2's `tr.t` rule) does not match",
                       page.count(section) == 1 and PROOF_MARK in cut and not snapshots_match(old, as_page(cut)))
        moved = page.replace(row, b'"entry origin, changed"')
        assert_control(fm054 + "a page that keeps PROOF but changes a tracker row (WORK-001's hook) does not match",
                       page.count(row) == 1 and PROOF_MARK in moved and not snapshots_match(old, as_page(moved)))
        v2 = "Git entry FM-053 allowance: "
        old_page, new_page = (base64.b64decode(row["board_after"][PAGE_PATH]["bytes_base64"]) for row in (old, new))
        joined = fm057_page_dropped(day_dropped_joined(new_page))
        assert_control(v2 + "the default run's board page, FM-030's day and FM-057's page taken out, is the baseline's with the join's edits — "
                       "FM053_PAGE_EDITS, FM054_ON_A2_EDITS, PR_C_JOIN_EDITS — every byte; A2's edits do not fit the candidate's page; the pair still matches",
                       old_page != new_page and joined is not None and joined_transform(old_page) == joined and fm053_transform(new_page) is None
                       and snapshots_match(old, new))
        assert_control(v2 + "a candidate page without the v2 band, or a baseline page that has it, does not match",
                       not snapshots_match(old, with_board(new, PAGE_PATH, new_page.replace(V2_MARK, b"--band:")))
                       and not snapshots_match(with_board(old, PAGE_PATH, old_page + V2_MARK), new))
        marker_only = lambda page: V2_MARK in page and V2_MARK not in old_page
        section, hook = b'<dialog id="dlg"></dialog>', b'"entry origin selection"'
        variants = {"the page reduced to the band alone": b"<!-- --secbg: -->",
                    "WORK-001 renamed WORK-999 throughout": new_page.replace(b"WORK-001", b"WORK-999"),
                    "an unrelated section deleted, the dialog's element": new_page.replace(section, b""),
                    "a tracker row changed, WORK-001's hook": new_page.replace(hook, b'"entry origin, changed"')}
        for what, page in variants.items():
            assert_control(v2 + f"a page that keeps the v2 band but is not the join's edits of the baseline does not match — {what}",
                           page != new_page and marker_only(page) and not snapshots_match(old, with_board(new, PAGE_PATH, page)))
        assert_control(v2 + "the controls' anchors are real: WORK-001, the dialog's element and WORK-001's hook are each on the candidate's page",
                       new_page.count(b"WORK-001") >= 1 and new_page.count(section) == 1 and new_page.count(hook) == 1)
        before_schema, after_schema = (next(row for row in rows if row["case"] == SCHEMA_CASE and row["version"] == version) for version in ("baseline", "candidate"))
        schema_old, schema_new = before_schema["stdout"], after_schema["stdout"]
        takes = lambda stdout: schema_matches(before_schema, dict(after_schema, stdout=stdout))
        changed = schema_new.replace("`--queue`", "`--queue`, changed", 1) if "`--queue`" in schema_new else schema_new + "one more line\n"
        palette = next((line for line in schema_new.split("\n") if line.startswith(PALETTE_ROW)), "")
        assert_control(v2 + "--schema differs by its `[palette]` row and its brand line, beside the d-batch's rows; another changed line, or a second row, does not match",
                       schema_old != schema_new and bool(palette) and takes(schema_new) and not takes(changed)
                       and not takes(schema_new.replace(palette, palette + "\n" + palette, 1)))
        assert_control(v2 + "--schema is every character of the baseline's with FM053_SCHEMA_EDITS applied, then R15's rows dropped and R13's rewritten; "
                       "A2's edits do not fit the candidate's", schema_matches(before_schema, after_schema) and fm053_schema(schema_new) is None)
        opening = "A brand place gives the board a logo and its labels"          # the v2 brand line's opening, all the rule before took
        brand = next((line for line in schema_new.split("\n") if line.startswith(opening)), "")
        lines = schema_new.split("\n")
        at = lines.index(palette) if palette in lines else 0
        rest = lines[:at] + lines[at + 1:]
        moved = "\n".join(rest[:rest.index(brand)] + [palette] + rest[rest.index(brand):]) if brand in rest else schema_new
        r13_rows = {row: next((line for line in lines if line.startswith(row)), "") for row in R13_SCHEMA_ROWS}
        d_batch_old = [next((r13_rows[row] for row in R13_SCHEMA_ROWS if line.startswith(row)), line)
                       for line in schema_old.split("\n") if not line.startswith(R15_SCHEMA_ROWS)]
        def two_lines(new):
            n = new.split("\n")
            found = [i for i, line in enumerate(n) if line.startswith(PALETTE_ROW)]
            if len(found) != 1:
                return False
            n = n[:found[0]] + n[found[0] + 1:]
            diffs = [(a, b) for a, b in zip(d_batch_old, n) if a != b] if len(d_batch_old) == len(n) else []
            return len(diffs) == 1 and diffs[0][1].startswith(opening)
        schemas = {"the palette row's contents changed": schema_new.replace(palette, PALETTE_ROW + " anything at all |"),
                   "the brand line's text after its opening changed": schema_new.replace(brand, opening + " — and anything at all"),
                   "the palette row moved out of its table, before the brand line": moved}
        for what, stdout in schemas.items():
            assert_control(v2 + f"--schema with A2's two lines, one of them not as approved, does not match — {what}",
                           bool(brand) and stdout != schema_new and two_lines(stdout) and not takes(stdout))
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
