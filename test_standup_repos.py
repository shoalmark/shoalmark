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
import shutil
import stat
import subprocess
import sys
import tempfile


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


def environment(home, path=None):
    """A run's environment: this process's, without git's own variables, with `home` as every system's home and no global or system git configuration."""
    env = {k: v for k, v in os.environ.items() if not k.startswith(("GIT_", "SHOALMARK_")) and k not in ("XDG_STATE_HOME",)}
    env.update(HOME=str(home), USERPROFILE=str(home), GIT_CONFIG_GLOBAL=os.devnull, GIT_CONFIG_NOSYSTEM="1", GIT_TERMINAL_PROMPT="0",
               SHOALMARK_CMD="shoalmark", PYTHONIOENCODING="utf-8", PYTHONDONTWRITEBYTECODE="1")
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
    write(path, f'#!/bin/sh\necho "$(basename "$0") $*" >> "{log}"\ncase "$1" in clean|smudge) cat ;; textconv) cat "$2" ;; esac\nexit 0\n')
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
    canary(d / "derive", log)
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
    canary(d / "derive", log)
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
        canary(gamma / "docs" / "work-tracker" / "derive", log)
        own_tool(gamma, log)
        config = Path(env["HOME"]) / ".subversion" / "config"           # the user's own: every helper a canary, which a local status names none of
        write(config, f"[helpers]\ndiff-cmd = {prog}\ndiff3-cmd = {prog}\neditor-cmd = {prog} editor\nmerge-tool-cmd = {prog}\n")
        out["gamma"] = gamma

    # delta: a plain folder, no version control, no name of its own — the folder's
    delta = area / "delta-plain"
    write(delta / "shoalmark.toml", '[kinds]\nPL = "Work"\n')
    tracker(delta / "docs" / "work-tracker", "PL-001", ask("Will you rotate delta's key?", "action", ago(1)), "delta's hands")
    canary(delta / "docs" / "work-tracker" / "derive", log)
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
            write(folder / program, f'#!/bin/sh\nprintf "%s|%s\\n" "$(pwd -P)" "$*" >> "{log}.{program}"\nexec "{real}" "$@"\n')
            (folder / program).chmod(0o755)
    return str(folder) + os.pathsep + os.environ.get("PATH", "")


def starts(log, program):
    path = Path(f"{log}.{program}")
    return [l.partition("|") for l in path.read_text(encoding="utf-8").splitlines()] if path.is_file() else []


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


def run_checks():
    """[(label, ok, detail)] — ok None where a part cannot run here, with why."""
    tool, results = tool_path(), []
    add = lambda label, ok, detail="": results.append((label, ok, detail))
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
            write(log, "")
            locked_ok = os.name != "nt" and not os.access(str(named["locked"]), os.R_OK)
            watch = os.name != "nt"
            run_env = environment(home, shims(area, logs / "starts") if watch else None)
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
