"""Q7's class test (FM-031) — one stand-up across the repositories you name: `--standup DIR [DIR …]`.

The fixture: two git repositories, one with changes in its working tree; a Subversion working copy where `svn` and
`svnadmin` are here (else that part is a named limit); a plain folder; an unreadable folder; a folder that is no repository;
a name that is missing; and a second name for a repository already named. Each repository carries a canary for its own
tool, its deriver, every git hook, and the programs a configuration can name, and each records any run of it.

- One agenda: each folder named with its version control, or why it was not read — and then counted in nothing; the asks
  by kind, the acts owed, the asks sent back, each with its repository; what the view does not read or run.
- Counts are each repository's, then added: FM-001 in two repositories is two items.
- Each repository's rows are read under its own configuration — its name, its id prefixes, its tracker folder, its
  `[seats]` — never another's; and the run puts back the module's bindings as it found them (A13).
- It runs nothing of a repository's: no canary runs, and it starts no git but the three reads that name a branch and a
  commit, and no svn but the one local status (POSIX: git and svn are watched through a shim on PATH).
- It writes nothing: every file and folder of the fixture, the home among them, is byte for byte and time for time as it
  was (the snapshot before and after).
- It starts git and svn by their absolute paths, from PATH's first absolute entry outside the repositories named — never a
  relative entry, the current folder or an entry inside a listed repository (RV-3303: recorded privately) — with
  `NoDefaultCurrentDirectoryInExePath` set while it runs and put back after; where neither PATH entry holds the program, the
  folders that need it are named as not read, and counted in nothing. On Windows (CI), a `git.exe` and an `svn.exe` in a listed
  repository and in the run's own folder never run, through the CLI or `standup_across`, and the output is as without them.
- `--standup` alone prints what it printed at ac8899d, the commit Q7 was built on.

Run: `python3 test_standup_repos.py` — exit 1 on a failure. `SHOALMARK_Q7_TOOL=<path>` runs it against another copy of
the tool: that is how its mutants are run, and each must fail it. test_shoalmark.py runs it at its end. No browser, no
network: every repository is a scratch one.
"""

import contextlib
import datetime
import hashlib
import importlib.util
import io
import os
from pathlib import Path
import re
import shlex
import shutil
import stat
import subprocess
import sys
import tempfile
import zipfile


HERE = Path(__file__).resolve().parent
BASE = "ac8899d"                    # the commit Q7 was built on: R9's deletion
STANDUP_GIT = ("rev-parse --verify -q HEAD", "branch --show-current", "rev-parse --absolute-git-dir --git-common-dir")
SVN_STATUS = "status --verbose --no-ignore --ignore-externals --depth infinity . --xml"
HOOKS = ("applypatch-msg", "pre-applypatch", "post-applypatch", "pre-commit", "pre-merge-commit", "prepare-commit-msg", "commit-msg",
         "post-commit", "pre-rebase", "post-checkout", "post-merge", "pre-push", "pre-receive", "update", "proc-receive", "post-receive",
         "post-update", "reference-transaction", "push-to-checkout", "pre-auto-gc", "post-rewrite", "sendemail-validate",
         "fsmonitor-watchman", "p4-changelist", "p4-prepare-changelist", "p4-post-changelist", "p4-pre-submit", "post-index-change")


def write(path, text):
    """A fixture file in UTF-8 with `\\n` line ends on every system (`Path.write_text` takes `newline` only from 3.10)."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)


def tool_path():
    return Path(os.environ.get("SHOALMARK_Q7_TOOL") or HERE / "shoalmark.py").resolve()


def guard_value(env, *, fold=False):
    name = "NoDefaultCurrentDirectoryInExePath"
    if not fold:
        return env.get(name, "unset")
    # Windows upper-cases os.environ's keys; a plain dict can also hold conflicting spellings.
    matches = [(k, v) for k, v in env.items() if k.upper() == name.upper()]
    if len(matches) > 1:
        return f"multiple keys: {matches!r}"
    return matches[0][1] if matches else "unset"


def guard_value_controls():
    upper = {"NODEFAULTCURRENTDIRECTORYINEXEPATH": "1"}
    duplicate = dict(upper, NoDefaultCurrentDirectoryInExePath="1")
    return [
        ("Q7 · the environment lookup reads the upper-case guard with case folding", guard_value(upper, fold=True) == "1", ""),
        ("Q7 · the environment lookup keeps exact case without folding", guard_value(upper, fold=False) == "unset", ""),
        ("Q7 · the environment lookup rejects two spellings of the guard", guard_value(duplicate, fold=True) != "1", guard_value(duplicate, fold=True)),
    ]


def environment(home, path=None):
    """A run's environment: this process's, without git's own variables and `NoDefaultCurrentDirectoryInExePath`, with `home` as every system's home
    and no global or system git configuration."""
    env = {}
    guard = "NODEFAULTCURRENTDIRECTORYINEXEPATH" if os.name == "nt" else "NoDefaultCurrentDirectoryInExePath"
    for k, v in os.environ.items():
        name = k.upper() if os.name == "nt" else k
        if not name.startswith(("GIT_", "SHOALMARK_")) and name not in ("XDG_STATE_HOME", guard):
            env[k] = v
    env.update(HOME=str(home), USERPROFILE=str(home), GIT_CONFIG_GLOBAL=os.devnull, GIT_CONFIG_NOSYSTEM="1", GIT_TERMINAL_PROMPT="0",
               SHOALMARK_CMD="shoalmark", PYTHONIOENCODING="utf-8", PYTHONDONTWRITEBYTECODE="1")
    if os.name == "nt":
        env.update(APPDATA=str(home / "AppData" / "Roaming"), LOCALAPPDATA=str(home / "AppData" / "Local"))
    if path:
        env["PATH"] = path
    return env


def run(tool, cwd, env, *argv):
    r = subprocess.run([sys.executable, str(tool), *argv], cwd=str(cwd), capture_output=True, text=True, encoding="utf-8", errors="replace",
                       env=env, timeout=300, stdin=subprocess.DEVNULL)
    return r.returncode, r.stdout, r.stderr


def sh(cwd, *a, env):
    return subprocess.run(list(a), cwd=str(cwd), capture_output=True, text=True, encoding="utf-8", errors="replace", env=env, check=True,
                          stdin=subprocess.DEVNULL).stdout


def tracker(folder, tid, extra, title):
    write(folder / f"{tid}-x.md", f'---\nid: {tid}\nstatus: In Progress\nconsidered: none\n{extra}hook: "h of {tid}"\n---\n\n# {tid} — {title}\n\n'
                                  "## What is true now\n\n**One thing is left.**\n\n## Done when\n\nit is.\n")


def ask(question, kind, since, proposal="yes"):
    return f'next: owner\nask: "{question}"\nask-kind: {kind}\nask-since: {since}\n' + (f'ask-proposal: "{proposal}"\n' if proposal else "")


def canary(path, log):
    """A program that records that it ran, by its name and arguments, in `log` — a filter's or a text conversion's passes its input on."""
    write(path, f'#!/bin/sh\necho "$(basename "$0") $*" >> {shlex.quote(log.as_posix())}\ncase "$1" in clean|smudge) cat ;; textconv) cat "$2" ;; esac\nexit 0\n')
    path.chmod(0o755)


def deriver_canary(path, log):
    """Windows runs a deriver with Python; the same Python source is executable on POSIX."""
    write(path, f'#!/usr/bin/env python3\nwith open({str(log)!r}, "a") as f:\n    f.write("derive ran\\n")\nprint("{{}}")\n')
    path.chmod(0o755)


def own_tool(root, log):
    """The repository's own copy of a tool, which records that it ran."""
    write(root / "shoalmark.py", f"#!/usr/bin/env python3\nopen({str(log)!r}, 'a').write('its own tool ran in {root.name}\\n')\n")
    (root / "shoalmark.py").chmod(0o755)


def plant_git(root, prog, log, env):
    """Every hook a canary, and every program a configuration can name for a read: the file-system monitor, a filter, a text conversion, an
    external diff, the signature programs, the pager, the editor, a credential helper, ssh — set after the fixture's commits."""
    for name in HOOKS:
        canary(root / ".git" / "hooks" / name, log)
    prog = shlex.quote(prog.as_posix())                 # Git's shell, including Git for Windows, must receive one path without backslash escapes
    for key, value in (("core.fsmonitor", f"{prog} fsmonitor"), ("filter.canary.clean", f"{prog} clean"), ("filter.canary.smudge", f"{prog} smudge"),
                       ("filter.canary.process", f"{prog} process"), ("diff.canary.textconv", f"{prog} textconv"), ("diff.canary.command", f"{prog} diffcmd"),
                       ("diff.external", f"{prog} external"), ("gpg.program", f"{prog} gpg"), ("gpg.ssh.program", f"{prog} ssh-program"),
                       ("gpg.x509.program", f"{prog} x509"), ("core.pager", f"{prog} pager"), ("core.editor", f"{prog} editor"),
                       ("credential.helper", f"!{prog} credential"), ("core.sshCommand", f"{prog} ssh"), ("log.showSignature", "true")):
        sh(root, "git", "config", key, value, env=env)


def fixture(area, env, log, prog):
    """The folders the stand-up is named, as (names in order, {what: path}, with svn or not)."""
    ago = lambda n: (datetime.date.today() - datetime.timedelta(days=n)).isoformat()
    due = (datetime.datetime.now(datetime.timezone.utc).astimezone() + datetime.timedelta(hours=3)).replace(microsecond=0).isoformat()
    git = lambda root, *a: sh(root, "git", *a, env=env)
    out = {}

    # alpha: git, its tree clean — a ruling that frees another tracker, and an act owed
    alpha = area / "alpha"
    alpha.mkdir()
    git(alpha, "init", "-q")
    git(alpha, "symbolic-ref", "HEAD", "refs/heads/main")
    for k, v in (("user.name", "owner"), ("user.email", "owner@example.invalid"), ("commit.gpgsign", "false"), ("core.autocrlf", "false")):
        git(alpha, "config", k, v)
    write(alpha / "shoalmark.toml", 'name = "alpha"\nstandup = "09:00"\n[kinds]\nFM = "Work"\n')
    write(alpha / ".gitattributes", "* filter=canary diff=canary\n")
    d = alpha / "docs" / "work-tracker"
    tracker(d, "FM-001", ask("Shall alpha ship the launcher first?", "ruling", ago(3)), "alpha's ruling")
    tracker(d, "FM-002", ask("Will you read alpha's production log?", "action", ago(2)) + f'answer: "accepted - tonight"\nanswered: {ago(1)}\nanswered-by: owner\ndue: {due}\n',
            "alpha's act")
    tracker(d, "FM-004", "next: build\nblocked-by: FM-001\n", "waits on the ruling")
    deriver_canary(d / "derive", log)
    own_tool(alpha, log)
    git(alpha, "add", "-A")
    git(alpha, "commit", "-qm", "alpha's trackers")
    out["alpha"] = alpha

    # beta: git, a branch of its own, with changes in its tree; its own tracker folder, id prefixes and `[seats]`. FM-001 again: another item
    beta = area / "beta"
    beta.mkdir()
    git(beta, "init", "-q")
    git(beta, "symbolic-ref", "HEAD", "refs/heads/work")
    for k, v in (("user.name", "planner"), ("user.email", "planner@example.invalid"), ("commit.gpgsign", "false"), ("core.autocrlf", "false")):
        git(beta, "config", k, v)
    write(beta / "shoalmark.toml", 'name = "beta"\ntracker_dir = "tracking"\n[kinds]\nFM = "Work"\nBB = "Bench"\n[seats]\nplanner = "planner@example.invalid"\n')
    write(beta / ".gitattributes", "* filter=canary diff=canary\n")
    d = beta / "tracking"
    tracker(d, "FM-001", ask("May beta drop the old importer?", "ruling", ago(1)), "beta's ruling")
    tracker(d, "BB-003", ask("Merge beta's bench change?", "ceremony", ago(0)), "beta's button")
    tracker(d, "BB-005", ask("Is beta's sent-back ask a question?", "ruling", ago(0), proposal=""), "beta's ask without a proposal")
    deriver_canary(d / "derive", log)
    own_tool(beta, log)
    write(beta / "README.md", "beta\n")
    git(beta, "add", "-A")
    git(beta, "commit", "-qm", "beta's trackers")
    write(beta / "README.md", "beta, changed and not committed\n")
    write(beta / "untracked.txt", "new\n")
    out["beta"] = beta

    for root in (alpha, beta):
        plant_git(root, prog, log, env)

    # gamma: a Subversion working copy, at r1 after its update
    with_svn = bool(shutil.which("svn") and shutil.which("svnadmin"))
    if with_svn:
        repo, gamma = area / "svnrepo", area / "gamma-wc"
        sh(area, "svnadmin", "create", str(repo), env=env)
        sh(area, "svn", "checkout", "-q", repo.as_uri(), str(gamma), env=env)
        write(gamma / "shoalmark.toml", 'name = "gamma"\n[kinds]\nSV = "Work"\n')
        tracker(gamma / "docs" / "work-tracker", "SV-001", ask("Shall gamma measure the import before it is ruled?", "determination", ago(4)), "gamma's question")
        sh(gamma, "svn", "add", "-q", "shoalmark.toml", "docs", env=env)
        sh(gamma, "svn", "commit", "-q", "-m", "gamma's trackers", env=env)
        sh(gamma, "svn", "update", "-q", env=env)
        deriver_canary(gamma / "docs" / "work-tracker" / "derive", log)
        own_tool(gamma, log)
        config_home = Path(env["APPDATA"]) / "Subversion" if os.name == "nt" else Path(env["HOME"]) / ".subversion"
        config = config_home / "config"                       # the fixture user's own configuration, under the home that the snapshot covers
        helper = prog
        if os.name == "nt":                                 # Subversion's native helpers cannot execute a shell script's shebang
            helper = prog.with_name("svn-helper.exe")
            problem = launcher(helper, log)
            assert not problem, problem
            sh(area, str(helper), env=env)
            assert "ran\n" in log.read_text(encoding="utf-8"), "the native Subversion helper did not record its control start"
        editor = subprocess.list2cmdline([str(helper), "editor"]) if os.name == "nt" else shlex.quote(str(helper)) + " editor"
        write(config, f"[helpers]\ndiff-cmd = {helper}\ndiff3-cmd = {helper}\neditor-cmd = {editor}\nmerge-tool-cmd = {helper}\n")
        out["gamma"] = gamma

    # delta: a plain folder, no version control, no name of its own — the folder's
    delta = area / "delta-plain"
    write(delta / "shoalmark.toml", '[kinds]\nPL = "Work"\n')
    tracker(delta / "docs" / "work-tracker", "PL-001", ask("Will you rotate delta's key?", "action", ago(1)), "delta's hands")
    deriver_canary(delta / "docs" / "work-tracker" / "derive", log)
    own_tool(delta, log)
    out["delta-plain"] = delta

    locked = area / "locked"                                # a folder that cannot be listed
    write(locked / "shoalmark.toml", 'name = "locked"\n')
    locked.chmod(0)
    out["locked"] = locked
    notes = area / "notes"                                  # a folder that is no repository: no configuration, no tracker folder
    write(notes / "README.txt", "notes\n")
    out["notes"] = notes
    out["gone"] = area / "gone"                             # a name that is missing
    out["alpha-again"] = alpha / "docs"                     # a second name for alpha: read once
    order = ["alpha", "beta"] + (["gamma"] if with_svn else []) + ["delta-plain", "locked", "notes", "gone", "alpha-again"]
    return order, out, with_svn


def snapshot(*folders):
    """Every file and folder under each folder — its type, mode, size, modification time and bytes; a symlink as where it points; a folder
    that cannot be listed as that."""
    seen = {}
    for folder in folders:
        for dirpath, dirnames, filenames in os.walk(folder, onerror=lambda e: seen.__setitem__(str(e.filename), ("unlistable",))):
            for name in dirnames + filenames:
                p = os.path.join(dirpath, name)
                st = os.lstat(p)
                if stat.S_ISLNK(st.st_mode):
                    seen[p] = ("link", os.readlink(p))
                elif stat.S_ISDIR(st.st_mode):
                    seen[p] = ("dir", st.st_mode, st.st_mtime_ns)
                else:
                    with open(p, "rb") as f:
                        seen[p] = ("file", st.st_mode, st.st_size, st.st_mtime_ns, hashlib.sha256(f.read()).hexdigest())
    return seen


def shims(area, log):
    """`git` and `svn` first on PATH, each recording where it was started and with what, then starting the real one (POSIX only)."""
    folder = area / "shims"
    for program in ("git", "svn"):
        real = shutil.which(program)
        if real:
            write(folder / program, f'#!/bin/sh\nprintf "%s|%s|%s\\n" "$(pwd -P)" "${{NoDefaultCurrentDirectoryInExePath-unset}}" "$*" >> "{log}.{program}"\n'
                                    f'exec "{real}" "$@"\n')
            (folder / program).chmod(0o755)
    return str(folder) + os.pathsep + os.environ.get("PATH", "")


def starts(log, program):
    """Each start the shim recorded: (where, `NoDefaultCurrentDirectoryInExePath` as it was set or `unset`, the arguments)."""
    path = Path(f"{log}.{program}")
    return [tuple(l.split("|", 2)) for l in path.read_text(encoding="utf-8").splitlines()] if path.is_file() else []


def plant(folder, names, log):
    """A program of each name in `folder` that records any run of it in `log`."""
    for name in names:
        canary(folder / name, log)


def launcher(path, marker):
    """A Windows console program at `path` that appends a line to `marker` when it runs — pip's vendored distlib launcher, then this Python
    as its interpreter, then a zipped `__main__.py`, as distlib builds a script's `.exe` — or "" where it was made, else why not."""
    try:
        from pip._vendor.distlib.scripts import ScriptMaker
        head = ScriptMaker(None, None)._get_launcher("t")
    except Exception as e:                                  # no pip, or a distlib without its launchers
        return f"pip's distlib launcher is not here ({type(e).__name__}: {e})"
    body = io.BytesIO()
    with zipfile.ZipFile(body, "w") as z:
        z.writestr("__main__.py", f"open({str(marker)!r}, 'a').write('ran\\n')\n")
    exe = sys.executable.encode("utf-8")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(head + b"#!" + (b'"' + exe + b'"' if b" " in exe else exe) + b"\r\n" + body.getvalue())
    return ""


def stamped(text):
    """The stand-up's output without the minute it was read."""
    return re.sub(r" · read \d{4}-\d{2}-\d{2} \d{2}:\d{2}", " · read <TIME>", text)


def first_difference(clean, actual):
    left, right = clean.splitlines(keepends=True), actual.splitlines(keepends=True)
    for n in range(max(len(left), len(right))):
        a = left[n] if n < len(left) else None
        b = right[n] if n < len(right) else None
        if a != b:
            return f"line {n + 1}: clean {a!r}; actual {b!r}"
    return ""


def section(out, title):
    """The lines under a title of the output, up to the next blank line."""
    at = out.find("\n" + title)
    return out[at + 1:].split("\n\n")[0].splitlines()[1:] if at >= 0 else []


def normal(text, base):
    """A run's words with what differs between two copies of one fixture taken out: the folder, a commit's sha, a time of day."""
    for p in sorted({str(base), base.as_posix(), str(base.resolve()), base.resolve().as_posix()}, key=len, reverse=True):
        text = text.replace(p, "<BASE>")
    text = re.sub(r"\b[0-9a-f]{7,40}\b", "<SHA>", text)
    text = re.sub(r"\d{4}-\d{2}-\d{2}[T ]\d{2}:\d{2}(?::\d{2})?(?:Z|[+-]\d{2}:?\d{2})?", "<TIME>", text)
    return re.sub(r"\b\d{2}:\d{2}(?::\d{2})?\b", "<CLOCK>", text)


def load(tool):
    """The tool as a module of its own, as test_shoalmark.py loads it."""
    spec = importlib.util.spec_from_file_location("q7_standup_tool", tool)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def bindings(module):
    """What `configure` binds in `module`, as it stands: each name's object, and what each container among them holds."""
    space = vars(module)
    return {n: (space[n], dict(space[n]) if isinstance(space[n], dict) else list(space[n]) if isinstance(space[n], list)
                else set(space[n]) if isinstance(space[n], set) else None) for n in module.configure.__code__.co_names if n in space}


def run_checks(*, results=None):
    """[(label, ok, detail)] — ok None where a part cannot run here, with why."""
    tool = tool_path()
    results = [] if results is None else results
    add = lambda label, ok, detail="": results.append((label, ok, detail))
    results.extend(guard_value_controls())
    with tempfile.TemporaryDirectory(prefix="shoalmark-q7-") as tmp:
        area = Path(tmp).resolve()
        home, cwd, logs = area / "home", area / "cwd", area / "logs"
        for d in (home, cwd, logs):
            d.mkdir()
        log, prog = logs / "canary.log", logs / "canary"
        canary(prog, log)
        env = environment(home)
        order, named, with_svn = fixture(area, env, log, prog)
        try:
            # Prove both kinds of canary can record a run before measuring silence; Git starts its helper through its own shell.
            sh(named["alpha"], "git", "-c", f"alias.canary=!{shlex.quote(prog.as_posix())} control", "canary", env=env)
            sh(named["alpha"], sys.executable, str(named["alpha"] / "docs" / "work-tracker" / "derive"), env=env)
            live = log.read_text(encoding="utf-8")
            add(f"Q7 · the fixture's shell helper and Python deriver canaries both record a deliberate start (saw {live!r})",
                "canary control\n" in live and "derive ran\n" in live)
            write(log, "")
            locked_ok = os.name != "nt" and not os.access(str(named["locked"]), os.R_OK)
            watch = os.name != "nt"
            if watch:                                       # programs named git and svn in the run's own folder and in a listed root, both on PATH first
                plant(cwd, ("git", "svn"), log)
                plant(named["alpha"] / "tools", ("git", "svn"), log)
            run_env = environment(home, os.pathsep.join([".", str(named["alpha"] / "tools"), shims(area, logs / "starts")]) if watch else None)
            folders = [area / n for n in ("alpha", "beta", "gamma-wc", "delta-plain", "notes", "cwd", "home", "svnrepo") if (area / n).exists()]
            before = snapshot(*folders)
            argv = ["--standup", *[str(named[n]) for n in order]]
            code, out, err = run(tool, cwd, run_env, *argv)
            after = snapshot(*folders)
            sha = lambda root: sh(root, "git", "rev-parse", "HEAD", env=env).strip()[:7]
            lines = out.splitlines()
            row = lambda name: next((l for l in lines[1:] if l.startswith(f"  {name} ")), "")
            n_named, n_read = len(order), 3 + with_svn

            # 1. one agenda: the header counts what was named and read; each folder's line
            add(f"Q7 · `--standup DIR …` exits 0 with nothing on stderr, and its first line counts the {n_named} repositories named and the {n_read} read, "
                f"and the items and acts of those read, added (saw exit {code}, {lines[:1]}, stderr {err.strip()[:200]!r})",
                code == 0 and not err.strip() and bool(lines) and lines[0].startswith(f"STANDUP · in the {n_named} repositories you named, {n_read} read · "
                                                                                       f"{4 + with_svn} item(s) · 1 act(s) · read "))
            add(f"Q7 · each git repository is named with its branch and its commit, and its own counts (saw {row('alpha')!r}, {row('beta')!r})",
                f"git · main @ {sha(named['alpha'])} · 1 item(s) · 1 act(s)" in row("alpha") and f"git · work @ {sha(named['beta'])} · 2 item(s)" in row("beta"))
            if with_svn:
                add(f"Q7 · the Subversion working copy is named with its revision (saw {row('gamma')!r})", "Subversion · r1 · 1 item(s)" in row("gamma"))
            else:
                add("Q7 · the Subversion working copy is named with its revision", None, "svn or svnadmin is not installed here")
            add(f"Q7 · the plain folder is named as having no version control, under its folder's name (saw {row('delta-plain')!r})",
                "no version control · 1 item(s)" in row("delta-plain") and str(named["delta-plain"].name) in row("delta-plain"))
            if locked_ok:
                add(f"Q7 · a folder that cannot be read is named with why, and counted in nothing (saw {row('locked')!r})",
                    "not read: cannot be read: " in row("locked") and row("locked").endswith("— counted in nothing"))
            else:
                add("Q7 · a folder that cannot be read is named with why", None, "this system lets its owner list a folder of mode 000")
            add(f"Q7 · a folder that is no repository, a missing name and a second name for a repository read are each named with why, and counted in nothing "
                f"(saw {row('notes')!r}, {row('gone')!r}, {row('docs')!r})",
                "not read: no tracker folder" in row("notes") and "not read: the folder is missing" in row("gone")
                and f"not read: the same repository as {named['alpha']}, read once — counted in nothing" in row("docs"))

            # 2. never joined by id; each repository's rows under its own configuration
            rulings = section(out, "RULINGS")
            add(f"Q7 · FM-001 in two repositories is two items, each under its repository with its own question — never joined by id (saw {rulings})",
                any(re.match(r"  \d\. alpha +FM-001 — Shall alpha ship the launcher first\?  \[3 day\(s\)\]  \[frees FM-004\]$", l) for l in rulings)
                and any(re.match(r"  \d\. beta +FM-001 — May beta drop the old importer\?  \[1 day\(s\)\]$", l) for l in rulings) and len(rulings) == 2)
            rest = section(out, "BUTTONS") + section(out, "EVIDENCE COULD SETTLE") + section(out, "YOUR HANDS") + section(out, "ACTS")
            sent = section(out, "1 ASK(S) SENT BACK")
            add(f"Q7 · each repository's rows are read under its own configuration — its name, id prefixes and tracker folder: beta's BB-003 button and its "
                f"sent-back BB-005, {'gamma' + chr(39) + 's SV-001, ' if with_svn else ''}delta's PL-001 and alpha's act, each under its own name (saw {rest}, {sent})",
                any(re.match(r"  1\. beta +BB-003 — Merge beta's bench change\?", l) for l in rest)
                and any(re.match(r"  1\. delta-plain +PL-001 — Will you rotate delta's key\?", l) for l in rest)
                and (not with_svn or any(re.match(r"  1\. gamma +SV-001 — Shall gamma measure", l) for l in rest))
                and any(re.match(r"  alpha +FM-002 — ", l) for l in rest)
                and len(sent) == 1 and re.match(r"  beta +BB-005 — ", sent[0]) is not None)
            add(f"Q7 · only the repository with `[seats]` says who asked is not checked there (saw {row('alpha')!r}, {row('beta')!r})",
                "who asked is not checked here" in row("beta") and "who asked is not checked here" not in row("alpha"))
            add("Q7 · it says what it does not read — a git tree's changes, what is on its way, the queue — and what it does not run",
                "\nnot read here: whether a git working tree has changes" in out and "\nnot run here: a repository's own tool, its deriver" in out)

            # 3. it runs nothing of theirs, and starts no git or svn but its own reads
            ran = log.read_text(encoding="utf-8")
            add(f"Q7 · no repository's own tool, deriver, hook or configured program ran — every canary is silent (saw {ran.strip()[:300]!r})", ran == "")
            if watch:
                gits, svns = starts(logs / "starts", "git"), starts(logs / "starts", "svn")
                roots = {str(named["alpha"]), str(named["beta"])}
                add(f"Q7 · the only git it starts are the three reads that name a branch and a commit, each in its repository "
                    f"(saw {sorted({a for _w, _s, a in gits})})", bool(gits) and all(a in STANDUP_GIT and w in roots for w, _s, a in gits))
                if with_svn:
                    add(f"Q7 · the only svn it starts is the one local status, in the working copy (saw {[a for _w, _s, a in svns]})",
                        len(svns) == 1 and svns[0][2] == SVN_STATUS and svns[0][0] == str(named["gamma"]))
                add(f"Q7 · RV-3303: recorded privately · with `.` and a listed repository's folder first on PATH, each holding a git and an svn, it starts "
                    f"the ones on PATH's first absolute entry outside the repositories named, each with `NoDefaultCurrentDirectoryInExePath` set "
                    f"(saw {sorted({s_ for _w, s_, _a in gits + svns})}; the planted ones ran: {bool(ran)})",
                    bool(gits) and (bool(svns) or not with_svn) and {s_ for _w, s_, _a in gits + svns} == {"1"} and ran == "")
            else:
                add("Q7 · the only git and svn it starts are its own reads", None, "the shims that watch them are POSIX shell scripts")

            # 4. it writes nothing
            changed = sorted(set(before) ^ set(after)) + sorted(p for p in before if p in after and before[p] != after[p])
            add(f"Q7 · it writes nothing: every file and folder of the fixture and the home is as it was (changed: {changed[:4]})", before == after)

            # 5. the module's bindings put back, in process
            module = load(tool)
            module.configure(named["alpha"])
            kept = bindings(module)
            buffer = io.StringIO()
            with contextlib.redirect_stdout(buffer):
                module.standup_across([str(named[n]) for n in ("beta", "delta-plain", "alpha")])
            now = bindings(module)
            moved = [n for n, (obj, held) in kept.items() if now[n][0] is not obj or held != now[n][1]]
            add(f"Q7 · the run puts back every binding `configure` makes, as it found them: the module still reads alpha (moved: {moved[:6]})",
                not moved and module.ROOT == named["alpha"] and "beta" in buffer.getvalue())

            # 5b. RV-3303: recorded privately · where git and svn start from
            names = ("git.exe", "svn.exe") if os.name == "nt" else ("git", "svn")
            plants, first = area / "plants", area / "plants" / "first-outside"
            for folder in (cwd, cwd / "bin", named["alpha"] / "tools", first, plants / "later"):
                plant(folder, names, log)
            entries = ["", ".", "bin", str(named["alpha"] / "tools"), str(named["beta"]), str(cwd)]
            if os.name == "nt":                                 # a `.cmd` and a `.bat` of each, before the first `.exe`
                plant(plants / "scripts", ("git.cmd", "git.bat", "svn.cmd", "svn.bat"), log)
                entries.append(str(plants / "scripts"))
            try:                                                # an entry that resolves into a listed repository, and a program that does
                os.symlink(str(named["alpha"] / "tools"), str(plants / "link-in"), target_is_directory=True)
                (plants / "link-file").mkdir()
                for n in names:
                    os.symlink(str(named["alpha"] / "tools" / n), str(plants / "link-file" / n))
                entries += [str(plants / "link-in"), str(plants / "link-file")]
            except (OSError, NotImplementedError):
                pass
            entries += [str(first), str(plants / "later")]
            here = os.getcwd()
            try:
                os.chdir(str(cwd))                              # the run's own folder: the planted git and svn, and `bin` below it
                got = module.standup_programs([str(named["alpha"]), str(named["beta"])], path=os.pathsep.join(entries))
            finally:
                os.chdir(here)
            add(f"Q7 · RV-3303: recorded privately · the program it starts is the first on PATH's absolute entries outside the repositories named: never "
                f"an empty, `.` or relative entry, the current folder, an entry inside a listed repository or one that resolves there"
                + (", nor a `.cmd` or a `.bat`" if os.name == "nt" else "") + f" (saw {got})",
                got == {"git": str(first / names[0]), "svn": str(first / names[1])})
            bare = area / "bare-path"
            bare.mkdir()
            code_n, out_n, err_n = run(tool, cwd, environment(home, str(bare)), *argv)
            missing = [row_n for row_n in out_n.splitlines()[1:] if "is not found on PATH's absolute entries outside the repositories named" in row_n]
            add(f"Q7 · RV-3303: recorded privately · where PATH's absolute entries outside the repositories named hold no git and no svn, each folder that "
                f"needs one is named as not read, and counted in nothing; the plain folder is read (saw {out_n.splitlines()[:1]}, {len(missing)} such line(s))",
                code_n == 0 and out_n.startswith(f"STANDUP · in the {n_named} repositories you named, 1 read · 1 item(s) · ")
                and len(missing) == 2 + with_svn and all(m_.endswith("— counted in nothing") for m_ in missing))
            guard_seen, guard_on = [], [False]
            def guard_watch(event, a):
                if guard_on[0] and event == "subprocess.Popen" and isinstance(a[3], dict):
                    guard_seen.append(guard_value(a[3], fold=os.name == "nt"))
            sys.addaudithook(guard_watch)
            was = os.environ.get("NoDefaultCurrentDirectoryInExePath")
            after_ = []
            try:
                for before_ in (None, "0"):
                    if before_ is None:
                        os.environ.pop("NoDefaultCurrentDirectoryInExePath", None)
                    else:
                        os.environ["NoDefaultCurrentDirectoryInExePath"] = before_
                    guard_on[0] = True
                    with contextlib.redirect_stdout(io.StringIO()):
                        module.standup_across([str(named["alpha"])])
                    guard_on[0] = False
                    after_.append(os.environ.get("NoDefaultCurrentDirectoryInExePath"))
            finally:
                guard_on[0] = False
                if was is None:
                    os.environ.pop("NoDefaultCurrentDirectoryInExePath", None)
                else:
                    os.environ["NoDefaultCurrentDirectoryInExePath"] = was
            add(f"Q7 · RV-3303: recorded privately · `standup_across` sets `NoDefaultCurrentDirectoryInExePath` for every git it starts, and puts it back "
                f"as it found it — unset, and `0` (saw {sorted(set(guard_seen))} while it ran, {after_} after)",
                bool(guard_seen) and set(guard_seen) == {"1"} and after_ == [None, "0"])

            # 5c. RV-3303: recorded privately · Windows: a git.exe and an svn.exe in a listed repository and in the run's own folder never run
            if os.name != "nt":
                add("Q7 · RV-3303: recorded privately · on Windows, a git.exe and an svn.exe in a listed repository and in the run's own folder never run, "
                    "through the CLI and through `standup_across`, and the output is as without them", None, "it runs on Windows only: CI runs it")
            else:
                own, marker = area / "run-here", logs / "planted-ran.log"
                own.mkdir()
                listed = [str(named[n]) for n in order if n not in ("locked", "notes", "gone", "alpha-again")]
                clean = stamped(run(tool, own, env, "--standup", *listed)[1])
                made = launcher(own / "git.exe", marker) or launcher(own / "svn.exe", marker) or launcher(named["alpha"] / "git.exe", marker) \
                    or launcher(named["alpha"] / "svn.exe", marker)
                if made:
                    add("Q7 · RV-3303: recorded privately · on Windows, a git.exe and an svn.exe in a listed repository and in the run's own folder never run",
                        False, made)
                else:
                    here = os.getcwd()
                    was = os.environ.pop("NoDefaultCurrentDirectoryInExePath", None)
                    try:                                        # the control: started by its bare name from that folder, the planted git.exe runs
                        os.chdir(str(own))
                        subprocess.run(["git", "--version"], capture_output=True, timeout=60)
                    except (OSError, subprocess.SubprocessError):
                        pass
                    finally:
                        os.chdir(here)
                        if was is not None:
                            os.environ["NoDefaultCurrentDirectoryInExePath"] = was
                    live = marker.is_file()
                    if live:
                        marker.unlink()
                    outs = [stamped(run(tool, own, env, "--standup", *listed)[1]), stamped(run(tool, named["alpha"], env, "--standup", *listed)[1])]
                    buffer = io.StringIO()
                    saved_env = dict(os.environ)
                    try:
                        os.chdir(str(own))
                        os.environ.clear()
                        os.environ.update(env)
                        module.configure()
                        with contextlib.redirect_stdout(buffer):
                            module.standup_across(listed)
                    finally:
                        os.environ.clear()
                        os.environ.update(saved_env)
                        os.chdir(here)
                    env_restored = dict(os.environ) == saved_env
                    outs.append(stamped(buffer.getvalue()))
                    detail = "\n".join(f"{label}: {first_difference(clean, output)}" for label, output in
                                       zip(("CLI from the run folder", "CLI from alpha", "in-process"), outs) if output != clean)
                    add(f"Q7 · RV-3303: recorded privately · on Windows, a git.exe and an svn.exe in a listed repository and in the run's own folder never "
                        f"run, through the CLI and through `standup_across`, and the output is as without them; the control — the planted git.exe, started "
                        f"by its bare name from its folder, runs — holds (control {live}, ran after {marker.is_file()}, outputs as without them "
                        f"{[o_ == clean for o_ in outs]}, environment restored {env_restored})",
                        live and not marker.is_file() and all(o_ == clean for o_ in outs) and env_restored, detail)

            # 6. the refusals beside it
            code_r, out_r, err_r = run(tool, cwd, run_env, "--root", str(named["alpha"]), "--standup", str(named["beta"]))
            add(f"Q7 · `--root` with `--standup DIR` is refused in one line, exit 2 (saw {code_r}, {err_r.strip()[:120]!r})",
                code_r == 2 and out_r == "" and len(err_r.splitlines()) == 1)
        finally:
            named["locked"].chmod(0o700)

        # 7. `--standup` alone prints what it printed at the base
        shown_old = subprocess.run(["git", "-C", str(HERE), "show", f"{BASE}:shoalmark.py"], capture_output=True, env=environment(home))
        if shown_old.returncode != 0:
            add(f"Q7 · `--standup` alone as at {BASE}", None, f"this clone does not hold {BASE}")
            return results
        old = area / "old-tool"
        old.mkdir()
        (old / "shoalmark.py").write_bytes(shown_old.stdout)
        shutil.copy(HERE / "VERSION", old / "VERSION")
        pair = {}
        for name, t in (("then", old / "shoalmark.py"), ("now", tool)):
            base = area / f"same-{name}"
            base.mkdir()
            g = lambda *a: sh(base, "git", *a, env=env)
            g("init", "-q")
            g("symbolic-ref", "HEAD", "refs/heads/main")
            for k, v in (("user.name", "owner"), ("user.email", "owner@example.invalid"), ("commit.gpgsign", "false"), ("core.autocrlf", "false")):
                g("config", k, v)
            write(base / "shoalmark.toml", 'name = "same"\nstandup = "09:00"\n[kinds]\nAP = "Work"\n')
            d = base / "docs" / "work-tracker"
            tracker(d, "AP-001", ask("Shall the launcher ship first?", "ruling", "2026-10-12"), "a ruling")
            tracker(d, "AP-002", ask("Will you set up the key?", "action", "2026-10-13") + 'answer: "accepted - this week"\nanswered: 2026-10-13\nanswered-by: owner\n', "an act")
            tracker(d, "AP-003", "next: build\nblocked-by: AP-001\n", "held")
            tracker(d, "AP-004", ask("Is this a question", "ruling", "2026-10-14"), "sent back")
            g("add", "-A")
            g("commit", "-qm", "the trackers")
            pair[name] = tuple(normal(x, base) if isinstance(x, str) else x for x in run(t, base, env, "--standup"))
        add(f"Q7 · `--standup` alone prints what it printed at {BASE} — exit, both streams", pair["then"] == pair["now"],
            "" if pair["then"] == pair["now"] else f"then {pair['then']!r}\nnow  {pair['now']!r}")
        add("Q7 · …and on that fixture `--standup` printed an agenda — the control that the comparison compared a run that worked",
            pair["now"][0] == 0 and "AP-001" in pair["now"][1] and "AP-004" in pair["now"][1], f"saw {pair['now']!r}"[:300])
    return results


if __name__ == "__main__":
    failed = 0
    for label, ok, detail in run_checks():
        print(("  ok    " if ok else "  skip  " if ok is None else "  FAIL  ") + label + ("" if ok else f"\n        {detail}" if detail else ""))
        failed += ok is False
    print(f"FAILED: {failed}" if failed else "all green")
    sys.exit(1 if failed else 0)
