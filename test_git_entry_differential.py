"""FM-044 P support: actual Git entry/process differential controls.

Outside proposal only. No handler, boundary, subprocess result or outcome is
mocked. Does not repeat generic schema/new/index/board/check/triage/session-new
pairs. Exercises clean/dirty origin selection and actual mixed-flag priorities.
All commits/configuration/remote setup are disposable fixture preparation;
production starts are reads and local generation only, with no push/hooks.
"""
import argparse
import base64
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


def r21_dropped(data):
    """The baseline's INDEX.md bytes without the header's separator and dated, counted line, removed once and in the header
    (before the first `## ` section) only. None where the header holds no such line."""
    head, sep, rest = data.partition(b"\n## ")
    head, found = R21_LINE.subn(b"", head, count=1)
    return head + sep + rest if found else None


# FM-054 and FM-007 (v0.20.1): the board's page carries how an answer is proved, read as the gate reads it from the default branch's
# configuration (`PROOF`, `proof_reading`), and says it before *accept*. The page the 615fb1d baseline writes holds neither, and the
# board's run of the candidate reads that configuration: the second difference the consumer's snapshots may show, and the one in
# what is started — every start and `subprocess.run` call the candidate makes inside `proof_reading`, each a read (FM054_READS).
# The page is held to its difference byte for byte (RV-3308): FM054_PAGE_EDITS, applied in order to the baseline's page, each
# where it occurs exactly once, must give every byte of the candidate's — and nothing else may differ.
PAGE_PATH = "work-tracker/index.html"
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


def fm054_page(baseline, candidate):
    """FM-054's difference in the board's page: every byte of the candidate's page, as the run left it, is the baseline's page
    transformed by FM054_PAGE_EDITS (`fm054_transform`) — and each hash is the bytes the run left."""
    pages = [base64.b64decode(row["page_after"]["bytes_base64"]) if isinstance(row.get("page_after"), dict) else None for row in (baseline, candidate)]
    return (None not in pages and [hashlib.sha256(p).hexdigest() for p in pages] == [baseline["after"].get(PAGE_PATH), candidate["after"].get(PAGE_PATH)]
            and PROOF_MARK not in pages[0] and fm054_transform(pages[0]) == pages[1])


def snapshots_match(baseline, candidate):
    """The consumer's snapshots before the run are equal, and so are those after it — every path, byte, symlink, ref, config
    entry and hook — but for R21's difference: INDEX.md after the run may differ where the baseline's, its header line
    dropped (`r21_dropped`), is the candidate's bytes; and FM-054's: the board's page may differ where every byte of the
    candidate's is the baseline's transformed by FM-054's reviewed edits (`fm054_page`)."""
    if baseline["before"] != candidate["before"]:
        return False
    if baseline["after"] == candidate["after"]:
        return True
    old, new = dict(baseline["after"]), dict(candidate["after"])
    if old.get(PAGE_PATH) != new.get(PAGE_PATH):
        if not fm054_page(baseline, candidate):
            return False
        old.pop(PAGE_PATH, None), new.pop(PAGE_PATH, None)
        if old == new:
            return True
    if not (isinstance(old.pop(INDEX_PATH, None), str) and isinstance(new.pop(INDEX_PATH, None), str)) or old != new:
        return False
    old_bytes, new_bytes = (base64.b64decode(row["index_after"]["bytes_base64"]) if isinstance(row.get("index_after"), dict) else None
                            for row in (baseline, candidate))
    return (old_bytes is not None and new_bytes is not None
            and hashlib.sha256(old_bytes).hexdigest() == baseline["after"][INDEX_PATH]
            and hashlib.sha256(new_bytes).hexdigest() == candidate["after"][INDEX_PATH]
            and r21_dropped(old_bytes) == new_bytes)


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
    index, page = root / INDEX_PATH, root / PAGE_PATH
    report.update(status=result.returncode, stdout=result.stdout,
                  stderr="".join(line for line in lines if not line.startswith(MARKER)), before=before, after=snapshot(root),
                  index_after=serial(index.read_bytes()) if index.is_file() and not index.is_symlink() else None,
                  page_after=serial(page.read_bytes()) if page.is_file() and not page.is_symlink() else None,
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
            assert_control(label_prefix + "actual stdout/stderr/status match immutable baseline",
                           (before["status"], before["stdout"], before["stderr"]) == (after["status"], after["stdout"], after["stderr"]))
            strip_stack = lambda entries: [{key: value for key, value in row.items() if key != "product_stack"} for row in entries]
            own = lambda entries: [row for row in entries if "proof_reading" not in (row.get("product_stack") or [])]      # FM-054's reads aside
            assert_control(label_prefix + "all actual process argv/effective cwd/env match — FM-054's reads of the default branch's configuration aside, each a read",
                           strip_stack(before["starts"]) == strip_stack(own(after["starts"])) and not fm054_reads(before["starts"])
                           and all(fm054_read(row["argv"]) for row in fm054_reads(after["starts"])))
            assert_control(label_prefix + "run options and actual process results match — FM-054's reads aside, each a read",
                           strip_stack(before["run_calls"]) == strip_stack(own(after["run_calls"])) and not fm054_reads(before["run_calls"])
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
        # FM-054's allowance is held to its difference on the same pair: the page carries PROOF, and only `proof_reading`'s reads are new
        fm054 = "Git entry FM-054 allowance: "
        reads = fm054_reads(new["starts"])
        assert_control(fm054 + "the default run's board reads the default branch's configuration — starts inside `proof_reading`, each a read, which the baseline never makes",
                       bool(reads) and all(fm054_read(row["argv"]) for row in reads) and not fm054_reads(old["starts"]))
        unstacked = [dict(row, product_stack=[s for s in row["product_stack"] if s != "proof_reading"]) for row in new["starts"]]
        strip = lambda entries: [{key: value for key, value in row.items() if key != "product_stack"} for row in entries]
        assert_control(fm054 + "the same reads made outside `proof_reading` are not set aside, and do not match the baseline's starts",
                       strip(old["starts"]) != strip([row for row in unstacked if "proof_reading" not in row["product_stack"]]))
        writes = [dict(row, argv=[row["argv"][0], "update-ref", "refs/heads/x", "HEAD"]) if row is reads[0] else row for row in new["starts"]] if reads else []
        assert_control(fm054 + "a start inside `proof_reading` that is not one of its reads is not one",
                       bool(writes) and not all(fm054_read(row["argv"]) for row in fm054_reads(writes)))
        page = base64.b64decode(new["page_after"]["bytes_base64"]) if isinstance(new.get("page_after"), dict) else b""
        unproved = page.replace(PROOF_MARK, b',PRUEF={"state": ')
        as_page = lambda data: dict(new, page_after=serial(data), after=dict(new["after"], **{PAGE_PATH: hashlib.sha256(data).hexdigest()}))
        assert_control(fm054 + "the candidate's page carries PROOF, and a page that differs from the baseline's without it does not match",
                       PROOF_MARK in page and snapshots_match(old, new) and not snapshots_match(old, as_page(unproved))
                       and not snapshots_match(old, dict(as_page(page), page_after=None)))
        # RV-3308: the page is held byte for byte — the baseline's page with FM-054's edits is the candidate's; and two candidates that
        # keep PROOF_MARK, one without an unrelated section, one whose tracker row says something else, do not match
        section, row = b"#p summary{cursor:pointer}\n", b'"entry origin selection"'
        before_page = base64.b64decode(old["page_after"]["bytes_base64"]) if isinstance(old.get("page_after"), dict) else b""
        assert_control(fm054 + "the candidate's page is the baseline's with FM054_PAGE_EDITS applied, every byte",
                       fm054_transform(before_page) == page and fm054_transform(page) is None)
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
