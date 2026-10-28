"""The class test of the board's resume command per session, and of the first turn's folder in `--whoami`.

- A home folder of its own holds the harnesses' logs: Claude Code's `.claude/projects/<project>/<uuid>.jsonl` and Codex's
  `.codex/sessions/<y>/<m>/<d>/rollout-<time>-<uuid>.jsonl`, each with a canary in its first turn's message content; beside them, files
  that start with an id and are no log — a sub-agent's, one a level deeper, one outside a project folder, a name that holds no UUID.
- A repository's day has a parent session for each case: one Claude Code log whose first turn ran under the home folder and whose later
  turns ran elsewhere, with another model and effort; one Codex log; a log outside the home folder; two logs, one of each harness; two
  Codex logs whose ids collide on their time; no log; a first folder with a space; a log that names no folder in its first MiB; a log
  that cannot be opened — and sub-sessions, each with a log of its own.
- Its board, built by `--html-only` with HOME that folder, read as HTML (no browser): the command or the reason in the page's data, by
  parent; nothing for a sub-session or a session with no log; the canary nowhere; the fold of what the page reads naming both folders.
  The strip's rows are drawn by the page's own script in Node, where Node is installed: a session with no entry draws none of the resume
  parts, and each entry its own. The digest (`--owner`), `--standup`, INDEX.md, the views, `built.json`, the commit hook's trailers and
  the history hold no command.
- `--whoami` and the commit hook (`--session-trailer`) on the log whose first and newest turns differ in folder, model and effort: the
  first turn's folder, and the newest turn's model and effort.
- The read, function by function: one listing of each folder, the one log of each id opened and no other file, the paste check, the
  folder written with `~`, and the command's two forms — PowerShell's where the tool runs on Windows, a POSIX shell's elsewhere — with
  Windows read from `sys.platform` alone, as `printed_arg` reads it.

Run: `python3 test_resume_command.py` — exit 1 on a failure. `SHOALMARK_RESUME_TOOL=<path>` runs it against another copy of the tool, and
`python3 test_resume_command.py --mutants` runs it against each of `MUTANTS`, each of which must fail it. test_shoalmark.py runs both.
"""

import contextlib
import html
import importlib.util
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
from unittest import mock

from test_vcs_shared import fixture_saw


HERE = Path(__file__).resolve().parent
CANARY = "CANARY-b41e93f0"
A, B, C, D, E, F, G, H, I = "aaaa1111", "bbbb2222", "cccc3333", "dddd4444", "eeee5555", "ffff6666", "abcd0007", "0199a1b2", "abcd0009"
UUID = {A: "aaaa1111-2c3d-4e5f-8a6b-7c8d9e0f1a2b", B: "bbbb2222-1111-4222-8333-444455556666", D: "dddd4444-0199-7a00-8b11-c22d33e44f55",
        E: "eeee5555-1111-4222-8333-444455556666", F: "ffff6666-1111-4222-8333-444455556666", G: "abcd0007-1111-4222-8333-444455556666",
        I: "abcd0009-1111-4222-8333-444455556666"}
CODEX_B = "bbbb2222-0199-7a00-8b11-c22d33e44f66"
COLLIDE = ("0199a1b2-7c00-7d11-8e22-f33a44b55c66", "0199a1b2-9f00-7d11-8e22-f33a44b55c77")
SUBS = (f"{A}/builder-1", f"{D}/reviewer-1")
MARKS = ("claude --resume", "codex resume", *UUID.values(), CODEX_B, *COLLIDE)

MUTANTS = (
    ("reads the newest cwd", "for raw in log_lines_oldest_first(path, RESUME_SCAN):", "for raw in log_lines_newest_first(path, RESUME_SCAN):"),
    ("takes the first turn's model and effort", "for raw in log_lines_newest_first(path):", "for raw in log_lines_oldest_first(path, LOG_SCAN):"),
    ("picks one of two logs", "        if len(found) > 1:\n            out[sid] = [\"two\", len(found)]", "        if len(found) > 2:\n            out[sid] = [\"two\", len(found)]"),
    ("skips the plain-set check", 'if not DAY_PLAIN.fullmatch(folder) or " " in folder or ("\\\\" in folder and sys.platform != "win32"):', "if False:"),
    ("gives a sub-session a command", "wanted = {sid for sid in ids if RESUME_ID_RE.fullmatch(sid)}", "wanted = {sid for sid in ids if RESUME_ID_RE.match(sid)}"),
    ("reads message content (the canary)", 'if codex else turn.get("cwd")', 'if codex else next(iter(re.findall(r\'"cwd": "([^"]*)"\', raw.decode("utf-8", "replace"))), None)'),
    ("puts the command in the digest", '[f"  {group_line(g)}" for g in groups])', '[f"  {group_line(g)} {resume_commands([g[\'id\']]).get(g[\'id\'], \'\')}" for g in groups])'),
    ("gives a log that cannot be read the no-folder reason", '            out[sid] = ["unread"]\n', '            out[sid] = ["nofolder", RESUME_SCAN >> 20]\n'),
)
UNREAD_MUTANT = MUTANTS[-1][0]


def tool_path():
    return Path(os.environ.get("SHOALMARK_RESUME_TOOL") or HERE / "shoalmark.py").resolve()


def load(tool):
    spec = importlib.util.spec_from_file_location("resume_fm_" + str(abs(hash(str(tool)))), tool)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def write(path, lines):
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write("".join(json.dumps(line) + "\n" for line in lines))
    return path


def claude_turn(cwd=None, model=None, effort=None, content=CANARY, kind="assistant"):
    """One Claude Code log line: the model inside `message`, the effort and `cwd` at the top — none where it is not given."""
    turn = {"type": kind, "sessionId": "x", "message": {"role": kind, "content": content}}
    if cwd is not None:
        turn["cwd"] = cwd
    if model:
        turn["message"]["model"] = model
    if effort:
        turn["perTurnEffort"] = effort
    return turn


def codex_log(cwd, later=None):
    """A Codex rollout: `session_meta` with the folder its session began in, the canary in its first message, and a later turn elsewhere."""
    return [{"type": "session_meta", "payload": {"id": "x", "cwd": cwd}},
            {"type": "response_item", "payload": {"type": "message", "content": [{"type": "input_text", "text": CANARY}]}},
            {"type": "turn_context", "payload": {"model": "gpt-6.1-sol", "effort": "medium", "cwd": later or cwd + "-later"}}]


def logs(home, outside):
    """The fixture home's logs and its decoys. Returns the folders each listing should read."""
    projects, sessions = home / ".claude" / "projects", home / ".codex" / "sessions"
    first, later = str(home / "work" / "first"), str(home / "work" / "later")
    canary = [{"type": "text", "text": CANARY}, {"type": "tool_use", "input": {"cwd": f"/{CANARY}/x"}}]
    write(projects / "-fixture-a" / f"{UUID[A]}.jsonl", [claude_turn(kind="user", content=canary), claude_turn(first, "claude-first-1", "low"),
                                                          claude_turn(later, "claude-newest-2", "max", content="later")])
    write(projects / "-fixture-a" / UUID[A] / "subagents" / f"agent-{A}0000feed.jsonl", [claude_turn(str(home / "sub"), "claude-sub-1", "low")])
    write(projects / "-fixture-a" / UUID[A] / f"{A}-0000-4000-8000-000000000001.jsonl", [claude_turn(str(home / "deeper"))])
    write(projects / f"{A}-0000-4000-8000-000000000002.jsonl", [claude_turn(str(home / "loose"))])
    write(projects / "-fixture-a" / f"{A}-no-uuid.jsonl", [claude_turn(str(home / "no-uuid"))])
    write(projects / "-fixture-b" / f"{UUID[B]}.jsonl", [claude_turn(str(home / "b"))])
    write(sessions / "2026" / "10" / "23" / f"rollout-2026-10-23T08-00-00-{CODEX_B}.jsonl", codex_log(str(home / "b-codex")))
    write(sessions / "2026" / "10" / "23" / f"rollout-2026-10-23T09-30-00-{UUID[D]}.jsonl", codex_log(str(home / "codex" / "proj"), str(home / "codex" / "moved")))
    write(sessions / "2026" / "10" / "22" / f"rollout-2026-10-22T07-00-00-{COLLIDE[0]}.jsonl", codex_log(str(home / "h1")))
    write(sessions / "2026" / "10" / "22" / f"rollout-2026-10-22T07-00-41-{COLLIDE[1]}.jsonl", codex_log(str(home / "h2")))
    write(projects / "-fixture-e" / f"{UUID[E]}.jsonl", [claude_turn(str(home / "work" / "a b")), claude_turn(first)])
    write(projects / "-fixture-f" / f"{UUID[F]}.jsonl", [claude_turn(content=CANARY + " " + "x" * (1 << 20)), claude_turn(first)])
    write(projects / "-fixture-g" / f"{UUID[G]}.jsonl", [claude_turn(outside)])
    write(projects / "-fixture-i" / f"{UUID[I]}.jsonl", [claude_turn(first)])
    return [projects, *(projects / p for p in ("-fixture-a", "-fixture-b", "-fixture-e", "-fixture-f", "-fixture-g", "-fixture-i")),
            sessions, sessions / "2026", sessions / "2026" / "10", sessions / "2026" / "10" / "22", sessions / "2026" / "10" / "23"]


def git(cwd, *a, env):
    return subprocess.run(["git", *a], cwd=str(cwd), capture_output=True, text=True, encoding="utf-8", errors="replace", env=env, check=True).stdout


def repository(root, env):
    """A repository whose day holds a parent session for each case, and two sub-sessions; each commit past every hook."""
    root.mkdir(parents=True)
    git(root, "init", "-q", env=env)
    git(root, "symbolic-ref", "HEAD", "refs/heads/main", env=env)
    for k, v in (("user.name", "planner"), ("user.email", "planner@seat"), ("commit.gpgsign", "false"), ("core.hooksPath", os.devnull)):
        git(root, "config", k, v, env=env)
    (root / "docs/work-tracker").mkdir(parents=True)
    (root / "shoalmark.toml").write_text('name = "resume"\n[kinds]\nAP = "Work"\n', encoding="utf-8")
    (root / ".gitignore").write_text("docs/work-tracker/index.html\ndocs/work-tracker/view/\n", encoding="utf-8")
    (root / "docs/work-tracker/AP-001-x.md").write_text('---\nid: AP-001\nstatus: In Progress\nconsidered: none\nhook: "h"\n---\n\n# AP-001 — the work\n\n'
                                                        "## What is true now\n\n**One thing is left.**\n\n## Done when\n\nit is.\n", encoding="utf-8")
    git(root, "add", "-A", env=env)
    git(root, "commit", "-qm", "the work", env=env)
    for sid in (A, B, C, E, F, G, H, I, *SUBS):
        git(root, "commit", "-q", "--allow-empty", "-m", f"a step of {sid}\n\nSession: {sid}\nWorktree: wt-{sid.replace('/', '-')}", env=env)


def run(tool, root, env, *a):
    r = subprocess.run([sys.executable, str(tool), "--root", str(root), *a], cwd=str(root), capture_output=True, text=True, encoding="utf-8",
                       errors="replace", env=env, timeout=300)
    return r.returncode, r.stdout, r.stderr


def page_data(page, name="REG"):
    """One of the page's script values — REG, the strip's data, by default — as JSON, or None."""
    at = page.find(f",{name}=")
    try:
        return json.JSONDecoder().raw_decode(page, at + len(name) + 2)[0] if at >= 0 else None
    except ValueError:
        return None


def rows_drawn(page, script, env, area):
    """[[id, what `rsm` gives, the row as the strip draws it, the same row drawn with no resume parts]] for each group of the page's data, by
    the page's own script run in Node outside any browser: its `esc`, `l`, `lh`, `rse` and `rsm`, and the strip's row, with the page's labels
    and icons. A string where it cannot run: no Node here, a part not in the page once, or the run's error."""
    node = shutil.which("node")
    if not node:
        return "no Node here"
    lines = script.split("\n")
    def line(start, n=1):
        at = [i for i, text in enumerate(lines) if text.startswith(start)]
        return "\n".join(lines[at[0]:at[0] + n]).rstrip(",") if len(at) == 1 else None
    a = script.find("REG.groups.map(g=>")
    b = script.find('+"</details>")', a) if a >= 0 and script.count("REG.groups.map(g=>") == 1 else -1
    parts = {"esc": line("esc=s=>"), "l": line("l=(k,...a)=>"), "lh": line("lh=(k,...a)=>"), "rse": line("rse=id=>"), "rsm": line("rsm=id=>", 2),
             "the row": script[a + len("REG.groups.map("):b + len('+"</details>"')] if b >= 0 else None}
    data = {k: page_data(page, k) for k in ("REG", "L", "ICO")}
    missing = [k for k, v in {**parts, **data}.items() if v is None]
    if missing:
        return f"not in the page once: {missing}"
    js = area / "rows.js"
    js.write_text("".join(f"const {k}={json.dumps(v)};\n" for k, v in data.items())
                  + "".join(f"const {parts[k]};\n" for k in ("esc", "l", "lh", "rse", "rsm"))
                  + f"const drawn=(rsm,rse)=>{parts['the row']};\nconst row=drawn(rsm,rse),plain=drawn(()=>\"\",()=>null);\n"
                  + "console.log(JSON.stringify(REG.groups.map(g=>[g[0],rsm(g[0]),row(g),plain(g)])));\n", encoding="utf-8")
    r = subprocess.run([node, str(js)], capture_output=True, text=True, encoding="utf-8", errors="replace", env=env, timeout=60)
    try:
        return json.loads(r.stdout)
    except ValueError:
        return f"exit {r.returncode}: {r.stderr.strip()[-300:]}"


@contextlib.contextmanager
def step(add, label):
    """A failed fixture gives one diagnostic and leaves the next part runnable."""
    try:
        yield
    except Exception as error:
        add(f"resume · {label}: a fixture step failed", False, fixture_saw(error))


@contextlib.contextmanager
def home_of(path):
    saved = {k: os.environ.get(k) for k in ("HOME", "USERPROFILE")}
    os.environ["HOME"] = os.environ["USERPROFILE"] = str(path)
    try:
        yield
    finally:
        for k, v in saved.items():
            os.environ.pop(k, None) if v is None else os.environ.__setitem__(k, v)


def expected(home, outside):
    """What the strip's data says of each parent, with this machine's separators, plain set and form of the command."""
    sep, nt = os.sep, sys.platform == "win32"
    cmd = lambda folder, run, uuid: f"cd '{folder}'; if ($?) {{ {run} '{uuid}' }}" if nt else f"cd {folder} && {run} {uuid}"
    return {A: ["resume", cmd(f"~{sep}work{sep}first", "claude --resume", UUID[A])], B: ["two", 2],
            D: ["resume", cmd(f"~{sep}codex{sep}proj", "codex resume", UUID[D])],
            E: ["refused", "chars.nt" if nt else "chars", f"~{sep}work{sep}a b", 200], F: ["nofolder", 1],
            G: ["resume", cmd(outside, "claude --resume", UUID[G])], H: ["two", 2], I: ["unread"]}


@contextlib.contextmanager
def unreadable(path):
    """`path` held so that nothing can open it, and given back after: by its permissions, or on Windows by a handle of this process that
    shares the file with no one. Yields whether that took — a user whom permissions do not bind opens it all the same, and that is said."""
    handle = None
    try:
        if os.name == "nt":
            try:
                import _winapi
                handle = _winapi.CreateFile(str(path), _winapi.GENERIC_READ, 0, _winapi.NULL, _winapi.OPEN_EXISTING, 0, _winapi.NULL)
            except (ImportError, AttributeError, OSError):
                handle = None
        else:
            os.chmod(path, 0)
        try:
            with open(path, "rb"):
                took = False
        except OSError:
            took = True
        yield took
    finally:
        if handle is not None:
            _winapi.CloseHandle(handle)
        elif os.name != "nt":
            os.chmod(path, 0o600)


def can_unread():
    """Whether this machine keeps a file from being opened as `unreadable` holds it."""
    with tempfile.TemporaryDirectory(prefix="shoalmark-resume-probe-") as tmp:
        log = Path(tmp) / "log.jsonl"
        log.write_text("{}\n", encoding="utf-8")
        with unreadable(log) as took:
            return took


def run_checks(mutants=False, *, results=None):
    """[(label, ok, detail)] — ok None where a part cannot run here, with why. With `mutants`, each of MUTANTS is run instead, and must fail."""
    results = [] if results is None else results
    add = lambda label, ok, detail="": results.append((label, bool(ok) if ok is not None else None, detail))
    if mutants:
        return run_mutants(add, results)
    tool = tool_path()
    fm = load(tool)
    env = {k: v for k, v in os.environ.items() if not k.startswith(("GIT_", "SHOALMARK_")) and k != "CODEX_THREAD_ID"}
    env.update(GIT_CONFIG_GLOBAL=os.devnull, GIT_CONFIG_NOSYSTEM="1", GIT_TERMINAL_PROMPT="0", PYTHONIOENCODING="utf-8")
    with tempfile.TemporaryDirectory(prefix="shoalmark-resume-") as tmp, contextlib.ExitStack() as held:
        area = Path(tmp).resolve()
        home, root, outside = area / "home", area / "repo", str(area / "elsewhere" / "proj")
        env.update(HOME=str(home), USERPROFILE=str(home))
        want = expected(home, outside)
        plain_outside = not fm.resume_folder_problem(outside, outside)
        took = False
        with step(add, "the fixture"):
            listed = logs(home, outside)
            repository(root, env)
            took = held.enter_context(unreadable(home / ".claude" / "projects" / "-fixture-i" / f"{UUID[I]}.jsonl"))
        if not took:
            want.pop(I)
            add("resume · a log that cannot be opened", None, "this machine opens the fixture's log although nothing may: its user is one permissions do not bind")
        same = lambda d: {k: v for k, v in d.items() if k != G and (took or k != I)}

        with step(add, "the read"), home_of(home):
            seen = []
            watch = [True]
            sys.addaudithook(lambda event, args: seen.append((event, str(args[0]))) if watch[0] and event in ("os.scandir", "open") else None)
            try:
                got = fm.resume_commands([A, B, C, D, E, F, G, H, I, *SUBS, "AAAA1111", "aaaa111", "aaaa11111"])
                seen_none = len(seen)
                fm.resume_commands([])
                fm.resume_commands([*SUBS, "AAAA1111", "-x"])
            finally:
                watch[0] = False
            scans = [p for e, p in seen[:seen_none] if e == "os.scandir"]
            opened = sorted(p for e, p in seen[:seen_none] if e == "open")
            one = sorted(str(home / ".claude" / "projects" / f"-fixture-{k}" / f"{UUID[x]}.jsonl") for k, x in (("a", A), ("e", E), ("f", F), ("g", G), ("i", I)))
            one.append(str(next((home / ".codex" / "sessions" / "2026" / "10" / "23").glob(f"*{UUID[D]}.jsonl"))))
            add(f"resume · the read lists each folder once — the projects, each project folder's top level, the sessions and each year, month and day — "
                f"and opens the one log of each id that has one, no other file; no id, or only a sub-session's, lists nothing (saw {len(scans)} listings, "
                f"{len(opened)} files opened, {len(seen) - seen_none} events with no id)",
                sorted(scans) == sorted(str(p) for p in listed) and opened == sorted(one) and len(seen) == seen_none)
            add(f"resume · each parent's command or reason, by its id alone: an id that is not exactly 8 lower-case hex digits, a sub-session's and one "
                f"with no log get nothing (saw {got})", same(got) == same(want))
            if took:
                add(f"resume · a log that cannot be opened gets its own reason, that its log could not be read — never the one for a log that was read "
                    f"and names no folder (saw {got.get(I)})", got.get(I) == ["unread"])
            if plain_outside:
                add("resume · a folder outside the home folder is written as it is", got.get(G) == want[G], f"{got.get(G)}")
            else:
                add("resume · a folder outside the home folder", None, f"this machine's temporary folder fails the paste check: {outside!r}")
            sep = os.sep
            homes = {"the home folder": (str(home), "~"), "under it": (str(home / "x" / "y"), f"~{sep}x{sep}y"),
                     "a sibling that starts with its name": (str(home) + "x" + sep + "y", str(home) + "x" + sep + "y"), "elsewhere": (outside, outside)}
            wrote = {k: fm.resume_folder(v) for k, (v, _w) in homes.items()}
            add(f"resume · the folder is written with ~ where it lies under the home folder, cut at a path boundary only (saw {wrote})",
                all(wrote[k] == w for k, (_v, w) in homes.items()))
            absolute = str(home / "x")
            cases = {"plain": ("~/a.b_c/d-e:f/~g", ""), "a space": ("~/a b", "chars"), "a quote": ("~/it's", "chars"), "a double quote": ('~/a"b', "chars"),
                     "a backtick": ("~/a`b", "chars"), "`$(`": ("~/a$(id)", "chars"), "a line break": ("~/a\nb", "chars"), "a tab": ("~/a\tb", "chars"),
                     "a semicolon": ("~/a;b", "chars"), "an ampersand": ("~/a&b", "chars"), "a letter outside ASCII": ("~/grüße", "chars"),
                     "a bidi override": ("~/a‮b", "chars"), "the backslash": ("~\\a", "" if sys.platform == "win32" else "chars"),
                     "200 characters": ("~/" + "x" * 198, ""), "201 characters": ("~/" + "x" * 199, "long")}
            said = {k: fm.resume_folder_problem(absolute, v) for k, (v, _w) in cases.items()}
            add(f"resume · the paste check: the day prompts' plain set without the space, the backslash only on Windows, at most 200 characters "
                f"(saw {said})", all(said[k] == w for k, (_v, w) in cases.items()) and fm.resume_folder_problem("work/x", "work/x") == "relative")
            forms, on_windows = {}, {}
            for platform in ("linux", "win32"):
                with mock.patch.object(fm.sys, "platform", platform):
                    forms[platform] = [fm.resume_command("~/work/first", "claude", UUID[A]), fm.resume_command("~/codex/proj", "codex", UUID[D])]
                    if platform == "win32":
                        on_windows = fm.resume_commands([A, D, E])
            add(f"resume · the command's two forms: where the tool runs on Windows, PowerShell's — each argument a PowerShell literal, and the harness "
                f"started only where the folder change succeeded —, else a POSIX shell's; Windows is read from sys.platform alone, by every step of the "
                f"read (saw {forms}, {on_windows})",
                forms == {"linux": [f"cd ~/work/first && claude --resume {UUID[A]}", f"cd ~/codex/proj && codex resume {UUID[D]}"],
                          "win32": [f"cd '~/work/first'; if ($?) {{ claude --resume '{UUID[A]}' }}", f"cd '~/codex/proj'; if ($?) {{ codex resume '{UUID[D]}' }}"]}
                and on_windows == {A: ["resume", f"cd '~{sep}work{sep}first'; if ($?) {{ claude --resume '{UUID[A]}' }}"],
                                   D: ["resume", f"cd '~{sep}codex{sep}proj'; if ($?) {{ codex resume '{UUID[D]}' }}"],
                                   E: ["refused", "chars.nt", f"~{sep}work{sep}a b", 200]})

        with step(add, "the board"):
            code, out_, err = run(tool, root, env, "--html-only")
            page = (root / "docs/work-tracker/index.html").read_text(encoding="utf-8")
            reg = page_data(page) or {}
            resume = reg.get("resume") or {}
            add(f"resume · board: the page's data holds each parent's command or reason, by its id alone — none for a sub-session or a session with no "
                f"log (saw exit {code}, {resume}, {err.strip()[-200:]!r})",
                code == 0 and same(resume) == same(want)
                and (resume.get(G) == want[G] if plain_outside else True) and not any("/" in k for k in resume))
            if took:
                add("resume · board: a log that cannot be opened says so in its parent's row, in its own words",
                    resume.get(I) == ["unread"] and 'r[0]=="unread"?l("resume.unread")' in page)
            members = [m for g in reg.get("groups", []) for m in g[4]]
            add("resume · board: the strip's groups and their members are as they were — five fields a group, four a member — and no command is in them",
                bool(members) and all(len(g) == 5 for g in reg["groups"]) and all(len(m) == 4 for m in members)
                and not any(mark in json.dumps(reg["groups"]) for mark in MARKS))
            add("resume · board: each command is in the page once, in its parent's data", all(page.count(v[1].replace("&", "\\u0026")) + page.count(v[1]) == 1
                                                                                             for k, v in resume.items() if v[0] == "resume") and resume)
            fold = (re.search(r'<details class="about"><summary>.*?</details>', page, re.S) or [""])[0]
            add("resume · board: the fold of what the page reads names both folders, and that it reads file names and the first turn's folder, never what a "
                "session said", "~/.claude/projects" in fold and "~/.codex/sessions" in fold and html.escape(fm.LABELS["read.about.logs"], quote=False) in fold)
            script = page.split("<script>")[2] if page.count("<script>") >= 2 else ""
            add("resume · board: a parent's row carries the copy button with its words and its spoken name, the command hidden behind it, and a click on it "
                "never folds or unfolds the row; a member's row carries none",
                '${esc(g[2])})${rsm(g[0])}' in script and 'onclick="RSM(event,this)"' in script and '<code class="rsc" hidden onclick="event.preventDefault()">' in script
                and "function RSM(e,b){e.preventDefault();" in script and 'title="${l("resume.help")}"' in script and 'aria-label="${l("resume.spoken",id)}"' in script
                and "rsm(m[" not in script and 'l("answer.sign.nocopy")' in script.split("function RSM")[1][:900])
            drawn = rows_drawn(page, script, env, area)
            label = ("resume · board, the page's own script run by Node: a session with no entry draws its row with no button, no reason and no help "
                     "line, as the strip draws a row with none; each entry the build wrote draws its button and help line, or its reason alone")
            if drawn == "no Node here":
                add(label, None, drawn)
            else:
                rows = {g[0]: g[1:] for g in drawn} if isinstance(drawn, list) else {}
                kind = lambda k: (resume.get(k) or [None])[0]
                shown = {k: [v[0][:40], v[1][-120:]] for k, v in rows.items()} or drawn
                add(f"{label} (saw {shown})",
                    {A, B, C, E, F, H} <= set(rows)
                    and rows[C][0] == "" and rows[C][1] == rows[C][2] and rows[C][1].startswith(f'<details class="grp"><summary>{C} planner@seat (wt-{C})</summary>')
                    and all(v[0] == "" and v[1] == v[2] for k, v in rows.items() if kind(k) is None)
                    and all('onclick="RSM(event,this)"' in v[0] and '<p class="help">' in v[1] for k, v in rows.items() if kind(k) == "resume")
                    and all(v[0].startswith('<i class="rw') and '<p class="help">' not in v[1] for k, v in rows.items() if kind(k) not in (None, "resume")))
            add("resume · CANARY: no word of what a session said — its first turn's message content — is in the page", CANARY not in page)

        with step(add, "everywhere else"):
            texts = {}
            texts["--owner"] = "".join(run(tool, root, env, "--owner")[1:])
            texts["--standup"] = "".join(run(tool, root, env, "--standup")[1:])
            code_, _o, plain_err = run(tool, root, env)
            texts["INDEX.md"] = (root / "docs/work-tracker/INDEX.md").read_text(encoding="utf-8") if (root / "docs/work-tracker/INDEX.md").is_file() else "\0none"
            for f in sorted((root / "docs/work-tracker/view").glob("*")):
                texts[f"view/{f.name}"] = f.read_text(encoding="utf-8")
            git(root, "config", "seat.session", A, env=env)
            git(root, "config", "seat.harness", UUID[A], env=env)
            msg = area / "MSG"
            msg.write_text("a subject\n", encoding="utf-8")
            hook = run(tool, root, env, "--session-trailer", str(msg))
            texts["the hook's message"] = msg.read_text(encoding="utf-8")
            texts["the history"] = git(root, "log", "--all", "--format=%B", env=env)
            leaks = {k: [m for m in MARKS if m in v] for k, v in texts.items()}
            add(f"resume · nowhere else: the digest, --standup, INDEX.md, the views and built.json of a plain run, the commit hook's message and the history "
                f"hold no command and no full id (saw {({k: v for k, v in leaks.items() if v})}, plain run exit {code_}, {plain_err.strip()[-160:]!r})",
                code_ == 0 and texts["INDEX.md"] != "\0none" and "view/built.json" in texts and not any(leaks.values())
                and "SESSIONS WITH A COMMIT IN THE LAST 24 HOURS" in texts["--owner"])

            who = run(tool, root, env, "--whoami")
            first, lines = who[1].splitlines()[:1], who[1].splitlines()
            add(f"resume · --whoami: the folder its session was launched in is its first turn's, and the model and effort its newest turn's "
                f"(saw exit {who[0]}, {lines})",
                who[0] == 0 and bool(first) and first[0].endswith("· claude-newest-2 · max") and len(lines) > 1
                and lines[1].endswith(f"— its session was launched in {home / 'work' / 'first'}"))
            trailers = texts["the hook's message"].splitlines()[2:]
            add(f"resume · the commit hook: `Model:` and `Effort:` are the newest turn's (saw exit {hook[0]}, {trailers})",
                hook[0] == 0 and trailers == [f"Session: {A}", f"Worktree: {root.name}", "Model: claude-newest-2", "Effort: max"])
            seen_ = who[1] + who[2] + texts["--owner"] + texts["the hook's message"]
            add("resume · CANARY: no word of what a session said is in what --whoami prints, the digest or the hook's message", CANARY not in seen_)
    return results


def run_mutants(add, results):
    """Each of MUTANTS, as a copy of the tool beside its VERSION and vendored renderer, run under this test: each must fail it."""
    source = (HERE / "shoalmark.py").read_text(encoding="utf-8")
    unread_here = can_unread()
    for name, old, new in MUTANTS:
        if name == UNREAD_MUTANT and not unread_here:
            add(f"resume · the mutant that {name}", None, "this machine opens a file nothing may open, so the test cannot hold a log unreadable")
            continue
        with tempfile.TemporaryDirectory(prefix="shoalmark-resume-mutant-") as tmp:
            tool = Path(tmp).resolve() / "tool" / "shoalmark.py"
            (tool.parent / "vendor").mkdir(parents=True)
            shutil.copy(HERE / "VERSION", tool.parent / "VERSION")
            for f in (HERE / "vendor").glob("marked-*.js"):
                shutil.copy(f, tool.parent / "vendor" / f.name)
            once = source.count(old) == 1
            tool.write_text(source.replace(old, new), encoding="utf-8")
            r = subprocess.run([sys.executable, str(HERE / "test_resume_command.py")], cwd=str(HERE), capture_output=True, text=True, encoding="utf-8",
                               errors="replace", env=dict(os.environ, SHOALMARK_RESUME_TOOL=str(tool)), timeout=900) if once else None
            failed = [line.strip()[len("FAIL  "):][:90] for line in (r.stdout.splitlines() if r else []) if line.strip().startswith("FAIL  ")]
            add(f"resume · the mutant that {name} fails the test (saw {'its text not once in the tool' if not once else f'exit {r.returncode}, failing: {failed}'})",
                once and r.returncode == 1 and failed)
    return results


if __name__ == "__main__":
    failed = 0
    for label, ok, detail in run_checks("--mutants" in sys.argv[1:]):
        print(("  ok    " if ok else "  skip  " if ok is None else "  FAIL  ") + label + ("" if ok else f"\n        {detail}" if detail else ""))
        failed += ok is False
    print(f"FAILED: {failed}" if failed else "all green")
    sys.exit(1 if failed else 0)
