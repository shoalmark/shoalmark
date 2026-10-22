"""The board's reads hold their fixed settings for every program a configuration can name.

Every git process the tool starts is one of the board's reads or an act. The board's reads run with the board's fixed settings, whatever the repository,
the user or the environment configures, and start no program a configuration names but the SSH signature check `%G?` asks for; an act runs git as the
person's own git runs. The class test of that promise:

- A repository configures each such program as a marker, a script that writes its name to a log: a clean filter and a process filter on files git must
  compare (stat-dirty, their content unchanged), with a driver in each scope that applies — the repository's own configuration, the worktree's, a private
  global one and a file an include brings —, the attribute in a tracked `.gitattributes` in one repository and in `.git/info/attributes` alone in the other;
  `core.fsmonitor`; a diff driver's `textconv` and `command`; `diff.external`; the three signature programs; a credential helper; `core.sshCommand`;
  `core.pager`; a hooks path; a required driver; a submodule whose own configuration names a driver.
- Each path that reaches a read of the board's runs there, the tool as a program: the board's own run, the plain run, `--check`, the commit's hooks as
  they run the hooks' copy, the digests and every other view. No marker starts in any of them; a read with git's own default in the same repository
  starts each one, so each shape is live.
- Through git's own trace, every git process of those paths reads the board's settings last, from the command scope, and every read that compares the
  working tree reads each configured driver emptied; an act's own git reads the person's settings.
- A count of changed paths is right, or it is not read: where git compared a file a configured driver stores, the board says the count is not read, and
  where none is compared the count is read and right. A required driver fails the comparison, which is not made again with it. `--check` says the same
  of the working tree's edits, and judges the branch's commits.
- Where the drivers listed after a comparison are not the ones it ran without, the comparison is not read.
- The digests' conflict preview, through `--owner` and `--standup`, is reported as not read where a merge driver is configured, or either driver list
  cannot be read before or after its `merge-tree`. A configured filter driver gives an unread preview unless `merge.renormalize` reads false, before and
  after, and no `-X renormalize` is passed; then each filter driver is emptied and the preview names the merge's result. No marker starts.
- `--check` and the plain run read the trunk from cached refs, and start no transport program over a local origin, SSH or HTTP; where `origin/HEAD` is
  absent and the cached `origin/main` and `origin/master` name different commits, each refuses in one line, whatever the working tree holds.

Every fixture is a throwaway repository under a scratch HOME, with GIT_CONFIG_GLOBAL a scratch file: no real global configuration is read or written.
Run it directly, `python3 test_board_settings.py [tool]`, or through test_shoalmark.py. With `--mutants` it also runs a byte-identical copy of the tool,
whose every row must pass, and each mutant of the tool: the one row the mutant names must pass in the copy and fail under the mutant.
"""

import importlib.util
import json
import os
import pathlib
import shutil
import subprocess
import sys
import tempfile


HERE = pathlib.Path(__file__).resolve().parent
TRACED = "log.showsignature,core.fsmonitor,core.hookspath,gpg.program,gpg.openpgp.program,gpg.x509.program,filter.*"
HOOK_NAMES = ("applypatch-msg", "pre-applypatch", "post-applypatch", "pre-commit", "pre-merge-commit", "prepare-commit-msg", "commit-msg", "post-commit",
              "pre-rebase", "post-checkout", "post-merge", "pre-push", "post-update", "reference-transaction", "pre-auto-gc", "post-rewrite",
              "post-index-change", "push-to-checkout")
MARKER = '#!/bin/sh\n# a marker program: it writes its name and its arguments to the log, then {does}\nprintf "%s %s\\n" "{name}" "$*" >> "{log}"\n{tail}'
ASK = 'next: owner\nask: "{q}"\nask-kind: ruling\nask-since: 2026-01-01\nask-proposal: "yes"\n'
DRIVER_FILES = ("data/a.txt", "proc/a.txt", "wt/a.txt", "glob/a.txt", "inc/a.txt")
NOT_READ_LINE = "the working tree: its edits were not read"
# git's long-running filter protocol: a process filter that answers the handshake with no capability is passed over, and git goes on without it
PROCESS_MARKER = """import sys
open(sys.argv[1], "a").write("process " + " ".join(sys.argv[2:]) + "\\n")
def packet():
    size = sys.stdin.buffer.read(4)
    return None if len(size) < 4 else b"" if size == b"0000" else sys.stdin.buffer.read(int(size, 16) - 4)
def say(*lines):
    for line in lines:
        sys.stdout.buffer.write(b"%04x" % (len(line) + 4) + line)
    sys.stdout.buffer.write(b"0000"); sys.stdout.buffer.flush()
while packet() not in (b"", None):
    pass
say(b"git-filter-server\\n", b"version=2\\n")
while packet() not in (b"", None):
    pass
say()
sys.stdin.buffer.read()
"""

MUTANTS = (
    ("the drivers' override left off",
     '''    return " ".join("'" + f"filter.{name}.{key}=".replace("'", "'\\\\''") + "'" for name in drivers for key in ("clean", "smudge", "process"))''',
     '''    return ""''',
     "the attribute in a tracked `.gitattributes` · a clean filter in the repository's own configuration: none"),
    ("only the local scope's drivers found",
     '''    r = vcs_process("git", "config", "-z", "--name-only", "--get-regexp", FILTER_KEYS,''',
     '''    r = vcs_process("git", "config", "--local", "-z", "--name-only", "--get-regexp", FILTER_KEYS,''',
     "the attribute in a tracked `.gitattributes` · a clean filter in the private global configuration: none"),
    ("`process` left out of the override",
     '''for name in drivers for key in ("clean", "smudge", "process"))''',
     '''for name in drivers for key in ("clean", "smudge"))''',
     "the attribute in a tracked `.gitattributes` · a process filter: none"),
    ("a failing read made again with the driver",
     '''    r = vcs_process("git", *args, cwd=ROOT, capture_output=True, text=True, encoding="utf-8", errors="replace", env=env)\n''',
     '''    r = vcs_process("git", *args, cwd=ROOT, capture_output=True, text=True, encoding="utf-8", errors="replace", env=env)\n'''
     '''    r = r if r.returncode == 0 else vcs_process("git", *args, cwd=ROOT, capture_output=True, text=True, encoding="utf-8", errors="replace", env=nested_git_env(board=True))\n''',
     "the attribute in `.git/info/attributes` alone · a required clean filter: none"),
    ("a count shown as read where a configured driver stores a compared file",
     "    if stored is None or stored:\n        return None\n    return len(held",
     "    if stored is None:\n        return None\n    return len(held",
     "the attribute in a tracked `.gitattributes` · a count of changed paths is right or not read"),
    ("an edit read where a configured driver stores a compared file",
     "            edits = paths if driver_paths(sorted(paths), got[1]) == set() else None",
     "            edits = paths",
     "the attribute in a tracked `.gitattributes` · `--check` says in one line that the working tree's edits were not read"),
    ("the drivers not listed again after the read",
     "    _DRIVERS = filter_drivers()\n    return (r, drivers) if _DRIVERS == drivers else None",
     "    _DRIVERS = drivers\n    return (r, drivers) if _DRIVERS == drivers else None",
     "a comparison after which the drivers listed again are not the ones it ran without is not read"),
    ("every run's reads without the settings, but the board's own run's and the digests'",
     "    BOARD_READS = not any(vars(args).get(flag) for flag in ACT_RUNS)",
     "    BOARD_READS = False",
     "the attribute in a tracked `.gitattributes` · `core.fsmonitor`: none"),
    ("`--check` without the settings",
     "    BOARD_READS = not any(vars(args).get(flag) for flag in ACT_RUNS)",
     "    BOARD_READS = not any(vars(args).get(flag) for flag in ACT_RUNS) and not args.check",
     "the attribute in a tracked `.gitattributes` · a diff driver's `textconv`: none"),
    ("the commit's hooks without the settings",
     "    BOARD_READS = not any(vars(args).get(flag) for flag in ACT_RUNS)",
     "    BOARD_READS = not any(vars(args).get(flag) for flag in ACT_RUNS) and not HOOK_RUN",
     "the attribute in a tracked `.gitattributes` · `core.fsmonitor`: none"),
    ("an act's run with the board's settings",
     "    BOARD_READS = not any(vars(args).get(flag) for flag in ACT_RUNS)",
     "    BOARD_READS = True",
     "the attribute in a tracked `.gitattributes` · an act's own git runs under the person's settings"),
    ("the board's own run and the digests without the settings",
     "    if board if board is not None else (LAZY_OFF or BOARD_READS):",
     "    if board if board is not None else BOARD_READS:",
     "the attribute in a tracked `.gitattributes` · `core.fsmonitor`: none"),
    ("the reading rule's git without the settings",
     '''encoding="utf-8", errors="replace", env=nested_git_env(board=True), **standup_program("git"))''',
     '''encoding="utf-8", errors="replace", env=nested_git_env(), **standup_program("git"))''',
     "the attribute in a tracked `.gitattributes` · the reading rule's first git runs with the board's settings even in an act"),
    ("textconv outside the board's own run",
     '''    return ["--no-textconv", "--text"] if LAZY_OFF else ["--no-textconv"] if BOARD_READS else []''',
     '''    return ["--no-textconv", "--text"] if LAZY_OFF else []''',
     "the attribute in a tracked `.gitattributes` · a diff driver's `textconv`: none"),
    ("a submodule's own working tree read",
     '''compared("diff", "-z", "--name-only", "--relative", "--ignore-submodules=dirty", rev)''',
     '''compared("diff", "-z", "--name-only", "--relative", "--ignore-submodules=none", rev)''',
     "the attribute in a tracked `.gitattributes` · a clean filter a submodule's own configuration names: none"),
    ("the digests' conflict preview under the person's settings, with no driver list read",
     '''        merges, filters = merge_drivers(), filter_drivers()\n'''
     '''        if merges is None or filters is None:\n'''
     '''            return ["(paths unread — the merge and filter drivers could not be listed)"]\n'''
     '''        if merges:\n'''
     '''            return ["(paths unread — a configured merge driver could change the merge)"]\n'''
     '''        renormalize = merge_renormalize() if filters else False\n'''
     '''        if renormalize is None:\n'''
     '''            return ["(paths unread — `merge.renormalize` could not be read)"]\n'''
     '''        if renormalize:\n'''
     '''            return ["(paths unread — `merge.renormalize` is on, and a configured filter driver could change the merge)"]\n'''
     '''        env = nested_git_env(board=True)\n'''
     '''        if filters:\n''',
     '''        filters = ()\n'''
     '''        env = nested_git_env(board=False)\n'''
     '''        if filters:\n''',
     "the digests' conflict preview starts no configured merge driver:"),
    ("the digests' conflict preview taking a filter list it cannot read as empty",
     '''        merges, filters = merge_drivers(), filter_drivers()\n''',
     '''        merges, filters = merge_drivers(), filter_drivers() or ()\n''',
     "the digests' conflict preview with a filter list that cannot be read:"),
    ("the digests' conflict preview run with each configured filter driver emptied where `merge.renormalize` is on",
     '''        if renormalize:\n'''
     '''            return ["(paths unread — `merge.renormalize` is on, and a configured filter driver could change the merge)"]\n'''
     '''        env = nested_git_env(board=True)\n'''
     '''        if filters:\n'''
     '''            env["GIT_CONFIG_PARAMETERS"] = " ".join(x for x in (env.get("GIT_CONFIG_PARAMETERS", "").strip(), driver_settings(filters)) if x)\n'''
     '''        r = vcs_process("git", "-c", "core.quotePath=false", "merge-tree", "--write-tree", "--name-only", "--no-messages", base(p), head(p),\n'''
     '''                        cwd=ROOT, capture_output=True, text=True, encoding="utf-8", errors="replace", env=env)\n'''
     '''        if merge_drivers() != () or filter_drivers() != filters or (filters and merge_renormalize() is not False):\n''',
     '''        env = nested_git_env(board=True)\n'''
     '''        if filters:\n'''
     '''            env["GIT_CONFIG_PARAMETERS"] = " ".join(x for x in (env.get("GIT_CONFIG_PARAMETERS", "").strip(), driver_settings(filters)) if x)\n'''
     '''        r = vcs_process("git", "-c", "core.quotePath=false", "merge-tree", "--write-tree", "--name-only", "--no-messages", base(p), head(p),\n'''
     '''                        cwd=ROOT, capture_output=True, text=True, encoding="utf-8", errors="replace", env=env)\n'''
     '''        if merge_drivers() != () or filter_drivers() != filters or (filters and merge_renormalize() != renormalize):\n''',
     "the digests' conflict preview where renormalizing through a configured filter merges clean"),
    ("the digests' conflict preview taking a list it cannot read after the merge-tree as empty",
     '''        if merge_drivers() != () or filter_drivers() != filters or (filters and merge_renormalize() is not False):\n''',
     '''        if merge_drivers() or (filter_drivers() or ()) != filters or (filters and merge_renormalize() is not False):\n''',
     "the digests' conflict preview whose filter list cannot be read after the merge-tree:"),
    ("the digests' conflict preview unread wherever a filter driver is configured",
     '''        renormalize = merge_renormalize() if filters else False\n''',
     '''        if filters:\n'''
     '''            return ["(paths unread — a configured filter driver could change the merge)"]\n'''
     '''        renormalize = False\n''',
     "the digests' conflict preview with a filter driver in git-lfs's shape in the private global configuration"),
    ("`merge.renormalize` read as false whatever it says",
     '''    return {"true": True, "false": False}.get(r.stdout.strip())\n''',
     '''    return False\n''',
     "the digests' conflict preview with a live clean-filter marker:"),
    ("the digests' conflict preview not reading `merge.renormalize` again after the merge-tree",
     '''        if merge_drivers() != () or filter_drivers() != filters or (filters and merge_renormalize() is not False):\n''',
     '''        if merge_drivers() != () or filter_drivers() != filters:\n''',
     "the digests' conflict preview whose `merge.renormalize` changes or cannot be read after the merge-tree:"),
    ("the trunk that cannot be told read as the cached `origin/main`",
     '''    _TRUNK_UNTOLD = ("the default branch cannot be told — this clone has no `origin/HEAD`, and its cached `origin/main` and `origin/master` name "\n'''
     '''                     "different commits: run `git remote set-head origin --auto` yourself, which asks origin, then run again")\n'''
     '''    return None\n''',
     '''    return "refs/remotes/origin/main"\n''',
     "the trunk that cannot be told:"),
    ("the default run's refusal of a trunk that cannot be told kept to a clean tree",
     '''    _ASK_ORIGIN = mode in ("check", "write") and not args.print_written and vcs() == "git"\n''',
     '''    _ASK_ORIGIN = mode in ("check", "write") and not args.print_written and vcs() == "git" and not worktree_edits()\n''',
     "the trunk that cannot be told, with the working tree edited:"),
)
ORIGIN_ASK = ('''    main = git("rev-parse", "--verify", "--quiet", "refs/remotes/origin/main^{commit}")\n''',
              '''    named = origin_default() if ask else None\n'''
              '''    if named and git("rev-parse", "--verify", "--quiet", f"refs/remotes/origin/{named}^{{commit}}").returncode == 0:\n'''
              '''        return f"refs/remotes/origin/{named}"\n'''
              '''    main = git("rev-parse", "--verify", "--quiet", "refs/remotes/origin/main^{commit}")\n''')
MUTANTS += tuple((f"the trunk read by asking origin, {over}", *ORIGIN_ASK, f"the trunk is read from cached refs {over}:")
                 for over in ("over a local origin", "over SSH", "over a localhost HTTP server that answers 401"))


def load(path):
    spec = importlib.util.spec_from_file_location("board_settings_tool", str(path))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def environment(base):
    home = base / "home"
    (home / ".config").mkdir(parents=True, exist_ok=True)
    env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_") and k not in ("PAGER", "LESS", "SSH_ASKPASS", "XDG_CONFIG_HOME", "PYTHONPATH")}
    env.update(HOME=str(home), USERPROFILE=str(home), XDG_CONFIG_HOME=str(home / ".config"), GIT_CONFIG_GLOBAL=str(base / "global.gitconfig"),
               GIT_CONFIG_NOSYSTEM="1", GIT_TERMINAL_PROMPT="0", GIT_AUTHOR_NAME="owner", GIT_AUTHOR_EMAIL="o@x", GIT_COMMITTER_NAME="owner",
               GIT_COMMITTER_EMAIL="o@x", SHOALMARK_CMD="shoalmark")
    (base / "global.gitconfig").touch()
    return env


def git(env, cwd, *args, data=None, check=True):
    r = subprocess.run(["git", "-C", str(cwd), *args], input=data, capture_output=True, env=env)
    if check and r.returncode:
        raise RuntimeError(f"git {' '.join(args)}: {r.stderr.decode('utf-8', 'replace').strip()[-300:]}")
    return r.stdout.decode("utf-8", "replace").strip()


def program(argv, env, cwd, trace=None):
    extra = {"GIT_TRACE2_EVENT": str(trace), "GIT_TRACE2_CONFIG_PARAMS": TRACED} if trace else {}
    r = subprocess.run([str(a) for a in argv], cwd=str(cwd), capture_output=True, text=True, encoding="utf-8", errors="replace", env=dict(env, **extra),
                       timeout=300)
    return r.returncode, r.stdout, r.stderr


def marker(base, name, does, tail):
    path = base / "markers" / name
    path.parent.mkdir(exist_ok=True)
    path.write_bytes(MARKER.format(does=does, name=name, log=(base / "markers.log").as_posix(), tail=tail).encode("utf-8"))
    path.chmod(0o755)
    return path.as_posix()


def process_marker(base):
    path = base / "markers" / "process.py"
    path.parent.mkdir(exist_ok=True)
    path.write_text(PROCESS_MARKER, encoding="utf-8")
    return f'"{pathlib.Path(sys.executable).as_posix()}" "{path.as_posix()}" "{(base / "markers.log").as_posix()}"'


def started(base):
    log = base / "markers.log"
    names = sorted({line.split(" ", 1)[0] for line in log.read_text(encoding="utf-8").splitlines() if line.strip()}) if log.is_file() else []
    log.write_text("", encoding="utf-8")
    return names


def tracker(root, tid, extra="", title="t"):
    d = root / "docs" / "work-tracker"
    d.mkdir(parents=True, exist_ok=True)
    p = d / f"{tid}-x.md"
    p.write_text(f'---\nid: {tid}\nstatus: In Progress\nconsidered: none\n{extra}hook: "h of {tid}"\n---\n\n# {tid} — {title}\n\n## What is true now\n\n'
                 "**One thing is left.**\n\n## Done when\n\nit is.\n", encoding="utf-8")
    return p


def touch(root, rels):
    for rel in rels:
        p = root / rel
        st = p.stat()
        os.utime(p, ns=(st.st_atime_ns, st.st_mtime_ns + 3_000_000_000))


def signed_by_hand(env, root, tid, head):
    git(env, root, "switch", "-q", "-c", f"answer/{tid.lower()}", "main")
    t = next(root.glob(f"docs/work-tracker/{tid}-*.md"))
    t.write_text(t.read_text(encoding="utf-8").replace('hook: "h of', 'done: "it is done · here"\nhook: "h of'), encoding="utf-8")
    git(env, root, "add", "--", t.relative_to(root).as_posix())
    tree, parent = git(env, root, "write-tree"), git(env, root, "rev-parse", "HEAD")
    body = f"tree {tree}\nparent {parent}\nauthor owner <o@x> 1700000000 +0000\ncommitter owner <o@x> 1700000000 +0000\ngpgsig {head}\n\n{tid}: done\n"
    sha = git(env, root, "hash-object", "-t", "commit", "-w", "--stdin", data=body.encode("utf-8"))
    git(env, root, "update-ref", f"refs/heads/answer/{tid.lower()}", sha)
    git(env, root, "push", "-q", "origin", f"answer/{tid.lower()}")
    git(env, root, "switch", "-q", "-f", "main")
    git(env, root, "branch", "-q", "-D", f"answer/{tid.lower()}")
    return sha


def lay_copy(fm, tool, root):
    at = root / ".git" / "shoalmark-trusted"
    for rel in fm.copy_files():
        (at / rel).parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(HERE / rel, at / rel)
    shutil.copyfile(tool, at / "shoalmark.py")
    (at / "COPY").write_text("# the hooks' copy of the tool\n", encoding="utf-8")
    return at / "shoalmark.py"


def build(base, fm, tool, info):
    env = environment(base)
    root, origin = base / "wc", base / "origin.git"
    root.mkdir()
    subprocess.run(["git", "init", "-q", "--bare", "--initial-branch=main", str(origin)], check=True, capture_output=True, env=env)
    subprocess.run(["git", "init", "-q", "--initial-branch=main", str(root)], check=True, capture_output=True, env=env)
    real = HERE / "shoalmark.py"
    program([sys.executable, real, "--root", root, "--init", "--key", "ap"], env, root)
    key = base / "key"
    subprocess.run(["ssh-keygen", "-q", "-t", "ed25519", "-N", "", "-f", str(key)], check=True, capture_output=True, env=env)
    signers = base / "allowed_signers"
    signers.write_text("o@x " + key.with_suffix(".pub").read_text(encoding="utf-8"), encoding="utf-8")
    for k, v in (("user.name", "owner"), ("user.email", "o@x"), ("gpg.format", "ssh"), ("user.signingkey", key.as_posix()),
                 ("gpg.ssh.allowedSignersFile", signers.as_posix()), ("commit.gpgsign", "false"), ("maintenance.auto", "false"), ("gc.auto", "0"),
                 ("core.autocrlf", "false"), ("seat.session", "abcd1234"), ("seat.harness", "fixture-harness-0001")):
        git(env, root, "config", k, v)
    git(env, root, "remote", "add", "origin", str(origin))
    (root / "shoalmark.toml").write_text('name = "m"\ntracker_dir = "docs/work-tracker"\n[kinds]\nAP = "Work"\n[seats]\nowner = "o@x signed"\n'
                                         'reviewer = "reviewer@seat"\n', encoding="utf-8")
    tracker(root, "AP-501", ASK.format(q="Does the importer ship first?"), "an ask")
    tracker(root, "AP-502"); tracker(root, "AP-503")
    tracker(root, "AP-504", ASK.format(q="Does the exporter ship first?"), "an ask")
    files = {"README.md": "readme\n", "notes.txt": "first\n", "data/a.txt": "lower case\n", "proc/a.txt": "process\n", "wt/a.txt": "worktree\n",
             "glob/a.txt": "global\n", "inc/a.txt": "included\n", **({"req/a.txt": "required\n"} if info else {})}
    for rel, text in files.items():
        (root / rel).parent.mkdir(parents=True, exist_ok=True)
        (root / rel).write_text(text, encoding="utf-8")
    attributes = ("data/*.txt filter=cleanprobe\nproc/*.txt filter=procprobe\nwt/*.txt filter=wtprobe\nglob/*.txt filter=globprobe\n"
                  "inc/*.txt filter=incprobe\n" + ("req/*.txt filter=reqprobe\n" if info else ""))
    (root / ".gitattributes").write_text("*.md diff=probe\n" + ("" if info else attributes), encoding="utf-8")
    if info:
        (root / ".git" / "info").mkdir(exist_ok=True)
        (root / ".git" / "info" / "attributes").write_text(attributes, encoding="utf-8")
    program([sys.executable, real, "--root", root], env, root)
    git(env, root, "add", "-A")
    blob = git(env, root, "hash-object", "-w", "--stdin", data=b"LOWER CASE\n")
    git(env, root, "update-index", "--cacheinfo", f"100644,{blob},data/a.txt")
    git(env, root, "commit", "-qm", "the trackers\n\nSession: abcd1234", "-S")
    first = git(env, root, "rev-parse", "HEAD")
    (root / "notes.txt").write_text("second\n", encoding="utf-8")
    t = root / "docs/work-tracker/AP-502-x.md"
    t.write_text(t.read_text(encoding="utf-8").replace("**One thing is left.**", "**Two things are left.**"), encoding="utf-8")
    git(env, root, "add", "notes.txt", "docs/work-tracker/AP-502-x.md")
    git(env, root, "commit", "-qm", "AP-502: a second line\n\nSession: abcd1234", "-S")
    second = git(env, root, "rev-parse", "HEAD")
    sub = None
    if not info:
        sub = root / "sub"
        sub.mkdir()
        subprocess.run(["git", "init", "-q", "--initial-branch=main", str(sub)], check=True, capture_output=True, env=env)
        git(env, sub, "config", "commit.gpgsign", "false")
        (sub / ".gitattributes").write_text("*.txt filter=subprobe\n", encoding="utf-8")
        (sub / "a.txt").write_text("in the submodule\n", encoding="utf-8")
        git(env, sub, "add", "-A"); git(env, sub, "commit", "-qm", "the submodule")
        (root / ".gitmodules").write_text('[submodule "sub"]\n\tpath = sub\n\turl = ./sub\n', encoding="utf-8")
        git(env, root, "add", ".gitmodules")
        git(env, root, "update-index", "--add", "--cacheinfo", f"160000,{git(env, sub, 'rev-parse', 'HEAD')},sub")
        git(env, root, "commit", "-qm", "the submodule\n\nSession: abcd1234", "-S")
    git(env, root, "push", "-q", "-u", "origin", "main")
    git(env, root, "remote", "set-head", "origin", "main")
    git(env, root, "switch", "-q", "-c", "answer/ap-501")
    t = root / "docs/work-tracker/AP-501-x.md"
    t.write_text(t.read_text(encoding="utf-8").replace("next: owner\n", 'next: build\nanswer: "accepted"\nanswered: 2026-01-02\nanswered-by: owner\n'),
                 encoding="utf-8")
    git(env, root, "add", "--", "docs/work-tracker/AP-501-x.md"); git(env, root, "commit", "-qm", "AP-501: answered", "-S")
    git(env, root, "push", "-q", "origin", "answer/ap-501"); git(env, root, "switch", "-q", "main"); git(env, root, "branch", "-q", "-D", "answer/ap-501")
    pgp = signed_by_hand(env, root, "AP-502", "-----BEGIN PGP SIGNATURE-----\n \n iQ==\n -----END PGP SIGNATURE-----")
    x509 = signed_by_hand(env, root, "AP-503", "-----BEGIN SIGNED MESSAGE-----\n MA==\n -----END SIGNED MESSAGE-----")
    git(env, root, "fetch", "-q", "origin")
    (root / "data/a.txt").write_text("lower case\n", encoding="utf-8")     # the checkouts above wrote the blob's text into the file
    copy = lay_copy(fm, tool, root)
    hooks = base / "hooks"
    hooks.mkdir()
    for name in HOOK_NAMES:
        (hooks / name).write_bytes(MARKER.format(does="ends", name="hook-" + name, log=(base / "markers.log").as_posix(), tail="exit 0\n").encode("utf-8"))
        (hooks / name).chmod(0o755)
    included = base / "included.gitconfig"
    included.write_text(f'[filter "incprobe"]\n\tclean = "{marker(base, "clean-include", "prints the file", "cat")}"\n', encoding="utf-8")
    local = (("filter.cleanprobe.clean", marker(base, "clean-local", "prints the file in capitals", "tr a-z A-Z")),
             ("filter.cleanprobe.smudge", marker(base, "smudge-local", "prints the file", "cat")),
             ("filter.procprobe.process", process_marker(base)),
             ("core.fsmonitor", marker(base, "fsmonitor", "fails", "exit 1")),
             ("core.hooksPath", hooks.as_posix()),
             ("include.path", included.as_posix()),
             ("diff.probe.textconv", marker(base, "textconv", "prints the file", 'cat "$1"')),
             ("diff.probe.command", marker(base, "diff-command", "ends", "exit 0")),
             *((("filter.reqprobe.clean", marker(base, "clean-required", "prints the file", "cat")), ("filter.reqprobe.required", "true")) if info else ()))
    for k, v in local:
        git(env, root, "config", k, v)
    git(env, root, "config", "extensions.worktreeConfig", "true")
    git(env, root, "config", "--worktree", "filter.wtprobe.clean", marker(base, "clean-worktree", "prints the file", "cat"))
    glob = (("filter.globprobe.clean", marker(base, "clean-global", "prints the file", "cat")),
            ("credential.helper", marker(base, "credential", "names no credential", "exit 0")),
            ("core.sshCommand", marker(base, "ssh", "fails", "exit 1")),
            ("core.pager", marker(base, "pager", "reads its input", "cat >/dev/null")),
            ("diff.external", marker(base, "diff-external", "ends", "exit 0")),
            ("gpg.x509.program", marker(base, "gpgsm", "fails, as no key verifies", "exit 1")),
            ("gpg.program", marker(base, "gpg", "fails, as no key verifies", "exit 1")) if info
            else ("gpg.openpgp.program", marker(base, "gpg-openpgp", "fails, as no key verifies", "exit 1")))
    for k, v in glob:
        git(env, root, "config", "--global", k, v)
    if sub is not None:
        git(env, sub, "config", "filter.subprobe.clean", marker(base, "clean-submodule", "prints the file", "cat"))
    dirty = list(DRIVER_FILES) + (["req/a.txt"] if info else []) + (["sub/a.txt"] if sub is not None else [])
    started(base)
    return dict(base=base, env=env, root=root, copy=copy, first=first, second=second, pgp=pgp, x509=x509, info=info, dirty=dirty,
                drivers=("cleanprobe", "globprobe", "incprobe", "procprobe", "wtprobe") + (("reqprobe",) if info else ()))


def controls(f):
    env, root, base = f["env"], f["root"], f["base"]
    seen = {}

    def read(*args, data=None):
        touch(root, f["dirty"])
        git(env, root, *args, data=data, check=False)
        return started(base)

    seen.update(dict.fromkeys(read("ls-files", "-m"), True))                     # git starts the drivers and the file-system monitor to compare
    seen.update(dict.fromkeys(read("diff", "--name-only", "--ignore-submodules=none", "HEAD"), True))    # git refreshes the index, and reads a submodule
    seen.update(dict.fromkeys(read("log", "-p", "-1", "--", "docs/work-tracker/AP-502-x.md"), True))
    seen.update(dict.fromkeys(read("diff", f["first"], f["second"], "--", "docs/work-tracker/AP-502-x.md", "notes.txt"), True))
    seen.update(dict.fromkeys(read("log", "-1", "--format=%G?", f["pgp"]), True))
    seen.update(dict.fromkeys(read("log", "-1", "--format=%G?", f["x509"]), True))
    seen.update(dict.fromkeys(read("credential", "fill", data=b"protocol=https\nhost=example.invalid\n\n"), True))
    seen.update(dict.fromkeys(read("ls-remote", "ssh://example.invalid/x.git"), True))
    if os.name != "nt":                                   # the pager starts only where git writes to a terminal
        import pty
        master, slave = pty.openpty()
        try:
            touch(root, f["dirty"])
            subprocess.run(["git", "-C", str(root), "log", "-1", "--format=%s"], stdin=subprocess.DEVNULL, stdout=slave, stderr=subprocess.DEVNULL,
                           env=dict(env, TERM="xterm"), timeout=60)
        finally:
            os.close(slave); os.close(master)
        seen.update(dict.fromkeys(started(base), True))
    else:
        seen["pager"] = None                            # Windows has no `pty`, and git starts the pager only for a terminal
    return seen


def processes(trace):
    procs, order = {}, []
    if not trace.is_file():
        return []
    for line in trace.read_text(encoding="utf-8", errors="replace").splitlines():
        try:
            e = json.loads(line)
        except ValueError:
            continue
        sid = e.get("sid")
        if e.get("event") == "start":
            procs[sid] = {"argv": e.get("argv") or [], "params": []}
            order.append(sid)
        elif e.get("event") == "def_param" and sid in procs:
            procs[sid]["params"].append((e.get("scope"), e.get("param"), e.get("value")))
    return [procs[s] for s in order]


def last(params, key):
    hits = [(scope, value) for scope, k, value in params if k == key]
    return hits[-1] if hits else None


def compares(argv):
    words, i = argv[1:], 0
    while i < len(words) and words[i] in ("-c", "-C"):
        i += 2
    words = words[i:]
    sub = words[0] if words else ""
    if sub == "ls-files":
        return "--modified" in words or "-m" in words
    if sub == "diff":
        rest = words[1:]
        return "--cached" not in rest and "--staged" not in rest and len([w for w in rest if not w.startswith("-")]) == 1
    return False


def settings_held(procs, tool, drivers):
    fixed = {"log.showsignature": "false", "core.fsmonitor": "false",
             "core.hookspath": str(pathlib.Path(tool).resolve() / "no-hooks"),
             "gpg.program": str(pathlib.Path(tool).resolve() / "no-signature-program"),
             "gpg.openpgp.program": str(pathlib.Path(tool).resolve() / "no-signature-program"),
             "gpg.x509.program": str(pathlib.Path(tool).resolve() / "no-signature-program")}
    norm = lambda v: os.path.normcase(str(v or "")).replace("\\", "/")
    wrong = []
    for p in procs:
        held = {k: last(p["params"], k) for k in fixed}
        bad = [k for k, v in fixed.items() if held[k] is not None and (held[k][0] != "command" or norm(held[k][1]) != norm(v))]
        bad += [k for k in ("log.showsignature", "core.fsmonitor", "core.hookspath") if held[k] is None]
        if compares(p["argv"]):
            for d in drivers:
                for key in ("clean", "smudge", "process"):
                    got = last(p["params"], f"filter.{d}.{key}")
                    if got != ("command", ""):
                        bad.append(f"filter.{d}.{key}")
        if bad:
            wrong.append((" ".join(p["argv"][1:5]), bad[:4]))
    return wrong


def run_paths(f, tool):
    env, root, base = f["env"], f["root"], f["base"]
    out = {}

    def one(name, argv, cwd=root):
        touch(root, f["dirty"])
        trace = base / f"trace-{len(out)}.json"
        code, o, e = program(argv, env, cwd, trace)
        out[name] = (code, o, e, started(base), processes(trace), built(root))

    tool_ = [sys.executable, tool, "--root", root]
    for name, args in (("the board's own run", ("--html-only",)), ("the plain run", ()), ("`--check`", ("--check",)), ("`--owner`", ("--owner",)),
                       ("`--standup`", ("--standup",)), ("`--next`", ("--next",)), ("`--answered`", ("--answered",)), ("`--related`", ("--related", "AP-501")),
                       ("`--sessions`", ("--sessions",)), ("`--whoami`", ("--whoami",)), ("`--schema`", ("--schema",)), ("`--queue`", ("--queue",))):
        one(name, tool_ + list(args))
    one("`--standup` across repositories", [sys.executable, tool, "--standup", root], cwd=base)
    one("an act, `--answer`", tool_ + ["--answer", "AP-504", "accept"])
    t = root / "docs/work-tracker/AP-503-x.md"
    t.write_text(t.read_text(encoding="utf-8").replace("**One thing is left.**", "**Nothing is left.**"), encoding="utf-8")
    git(env, root, "add", "--", t.relative_to(root).as_posix())
    started(base)
    message = root / ".git" / "COMMIT_EDITMSG"
    message.write_text("AP-503: nothing is left\n\nSession: abcd1234\n", encoding="utf-8")
    hook = [sys.executable, "-I", f["copy"], "--root", root]
    one("the pre-commit hook's `--session-check`", hook + ["--session-check"])
    one("the pre-commit hook's write, `--print-written`", hook + ["--print-written"])
    one("the commit-msg hook's `--commit-msg`", hook + ["--commit-msg", message])
    return out


ACT = "an act, `--answer`"
COPY_RUNS = ("the pre-commit hook's `--session-check`", "the pre-commit hook's write, `--print-written`", "the commit-msg hook's `--commit-msg`")


def built(root):
    try:
        return json.loads((root / "docs/work-tracker/view/built.json").read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None


def count_control(base, fm, tool):
    env = environment(base)
    root = base / "wc"
    root.mkdir()
    subprocess.run(["git", "init", "-q", "--initial-branch=main", str(root)], check=True, capture_output=True, env=env)
    real = HERE / "shoalmark.py"
    program([sys.executable, real, "--root", root, "--init", "--key", "ap"], env, root)
    for k, v in (("user.name", "owner"), ("user.email", "o@x"), ("commit.gpgsign", "false"), ("maintenance.auto", "false"), ("core.autocrlf", "false")):
        git(env, root, "config", k, v)
    tracker(root, "AP-501")
    (root / "data").mkdir()
    (root / "data/a.txt").write_text("lower case\n", encoding="utf-8")
    (root / "notes.txt").write_text("first\n", encoding="utf-8")
    (root / ".gitattributes").write_text("data/*.txt filter=cleanprobe\n", encoding="utf-8")
    for rel in ("data/a.txt", "notes.txt"):                 # older than the index git writes: it holds them as they are, never racily clean
        st = (root / rel).stat()
        os.utime(root / rel, ns=(st.st_atime_ns - 3_600_000_000_000, st.st_mtime_ns - 3_600_000_000_000))
    program([sys.executable, real, "--root", root], env, root)
    git(env, root, "config", "filter.cleanprobe.clean", marker(base, "clean-local", "prints the file in capitals", "tr a-z A-Z"))
    git(env, root, "add", "-A"); git(env, root, "commit", "-qm", "base\n\nSession: abcd1234")
    git(env, root, "status", "--porcelain")                  # git status refreshes the index
    (root / "data/new.txt").write_text("new\n", encoding="utf-8")
    (root / "notes.txt").write_text("second\n", encoding="utf-8")
    started(base)
    program([sys.executable, tool, "--root", root], env, root)
    count = (built(root) or {}).get("changes", "absent")
    c, o, e = program([sys.executable, tool, "--root", root, "--check"], env, root)
    return count, ("uncommitted edits" in o + e, NOT_READ_LINE in o + e), started(base)


def window_row(fm, base):
    env = environment(base)
    root = base / "wc"
    root.mkdir()
    subprocess.run(["git", "init", "-q", "--initial-branch=main", str(root)], check=True, capture_output=True, env=env)
    (root / "shoalmark.toml").write_text('name = "w"\n[kinds]\nAP = "Work"\n', encoding="utf-8")
    saved_env = {k: os.environ.get(k) for k in set(env) | {k for k in os.environ if k.startswith("GIT_")}}
    real = fm.filter_drivers
    try:
        for k in [k for k in os.environ if k.startswith("GIT_")]:
            os.environ.pop(k)
        os.environ.update(env)
        fm.configure(root)
        results = []
        for lists in ((("a",), ("a", "b")), (("a",), ("a",))):
            answers = iter(lists)
            fm.filter_drivers = lambda: next(answers)
            fm._DRIVERS = None
            results.append(fm.compared("ls-files", "-z", "--modified"))
        return results[0] is None and results[1] is not None, [r is None for r in results]
    finally:
        fm.filter_drivers = real
        for k, v in saved_env.items():
            if v is None:
                os.environ.pop(k, None)
            else:
                os.environ[k] = v
        fm.configure(HERE)


def merge_marker(base):
    return marker(base, "merge-driver", "leaves a conflict", "exit 1") + " %O %A %B"


def preview_repo(base, texts=("x\n", "pr\n", "main\n"), attributes=""):
    env = environment(base)
    root = base / "wc"
    root.mkdir()
    subprocess.run(["git", "init", "-q", "--bare", "--initial-branch=main", str(base / "origin.git")], check=True, capture_output=True, env=env)
    subprocess.run(["git", "init", "-q", "--initial-branch=main", str(root)], check=True, capture_output=True, env=env)
    real = HERE / "shoalmark.py"
    program([sys.executable, real, "--root", root, "--init", "--key", "ap"], env, root)
    for k, v in (("user.name", "owner"), ("user.email", "o@x"), ("commit.gpgsign", "false"), ("maintenance.auto", "false"), ("core.autocrlf", "false")):
        git(env, root, "config", k, v)
    (root / "shoalmark.toml").write_text('name = "m"\ntracker_dir = "docs/work-tracker"\n[kinds]\nAP = "Work"\n', encoding="utf-8")
    tracker(root, "AP-501")
    (root / "f.txt").write_text(texts[0], encoding="utf-8")
    if attributes:
        (root / ".gitattributes").write_text(attributes, encoding="utf-8")
    program([sys.executable, real, "--root", root], env, root)
    git(env, root, "add", "-A"); git(env, root, "commit", "-qm", "base\n\nSession: abcd1234")
    git(env, root, "remote", "add", "origin", str(base / "origin.git"))
    git(env, root, "switch", "-q", "-c", "pr", "main")
    (root / "f.txt").write_text(texts[1], encoding="utf-8"); git(env, root, "add", "f.txt"); git(env, root, "commit", "-qm", "pr\n\nSession: abcd1234")
    pr = git(env, root, "rev-parse", "HEAD")
    git(env, root, "switch", "-q", "main")
    (root / "f.txt").write_text(texts[2], encoding="utf-8"); git(env, root, "add", "f.txt"); git(env, root, "commit", "-qm", "main-change\n\nSession: abcd1234")
    git(env, root, "push", "-q", "-u", "origin", "main"); git(env, root, "remote", "set-head", "origin", "main")
    return env, root, pr


def person_merge(env, root, pr):
    r = subprocess.run(["git", "-C", str(root), "merge-tree", "--write-tree", "--name-only", "--no-messages", "main", pr], capture_output=True, env=env)
    return r.returncode, [l for l in r.stdout.decode("utf-8", "replace").splitlines()[1:] if l.strip()]


def preview_digests(module, base, env, root, pr, before=None, after_merge=None, more=()):
    import contextlib
    import io
    saved = {k: os.environ.get(k) for k in set(env) | {k for k in os.environ if k.startswith("GIT_")}}
    runs = []
    try:
        for k in [k for k in os.environ if k.startswith("GIT_")]:
            os.environ.pop(k)
        os.environ.update(env)
        module.configure(root)
        pr_meta = [dict(number=n, title="a change", headRefOid=sha, headRefName=branch, baseRefName="main", createdAt="", isCrossRepository=False,
                        mergeable="UNKNOWN") for n, (branch, sha) in enumerate((("pr", pr), *more), 1)]
        pr_meta[0]["mergeable"] = "CONFLICTING"
        real_forge, real_pushed, real_process = module.forge_prs, module.pushed_branches, module.vcs_process

        def process(*args, **options):
            r = real_process(*args, **options)
            if after_merge is not None and "merge-tree" in args:
                after_merge()
            return r
        module.forge_prs = lambda: (pr_meta, None)
        module.pushed_branches = lambda prs: []
        module.vcs_process = process
        try:
            for flag in ("--owner", "--standup"):
                if before is not None:
                    before()
                started(base)
                out = io.StringIO()
                with contextlib.redirect_stdout(out), contextlib.redirect_stderr(out):
                    code = module.main(["--root", str(root), flag])
                runs.append((code, out.getvalue(), started(base)))
        finally:
            module.forge_prs, module.pushed_branches, module.vcs_process = real_forge, real_pushed, real_process
    finally:
        for k, v in saved.items():
            os.environ.pop(k, None) if v is None else os.environ.__setitem__(k, v)
        module.configure(HERE)
    return runs


def unread_preview(runs):
    return bool(runs) and all(code == 0 and "paths unread" in said and "conflict in f.txt" not in said and not marks for code, said, marks in runs)


def merge_preview_row(module, base):
    env, root, pr = preview_repo(base, attributes="*.txt merge=probe\n")
    (root / ".git" / "info").mkdir(exist_ok=True)
    (root / ".git" / "info" / "attributes").write_text("*.txt merge=probe\n", encoding="utf-8")
    gattr = base / "global-attributes"
    gattr.write_text("*.txt merge=probe\n", encoding="utf-8")
    git(env, root, "config", "merge.probe.driver", merge_marker(base))
    git(env, root, "config", "--global", "core.attributesFile", gattr.as_posix())
    runs = preview_digests(module, base, env, root, pr)
    return unread_preview(runs), [marks for _c, _s, marks in runs]


def unread_filters_row(module, base):
    env, root, pr = preview_repo(base, attributes="*.txt filter=probe\n")
    git(env, root, "config", "filter.probe.clean", marker(base, "clean-preview", "prints the file", "cat"))
    git(env, root, "config", "filter.a=b.clean", "cat")
    git(env, root, "config", "merge.renormalize", "true")
    started(base)
    person_merge(env, root, pr)
    live = started(base)
    runs = preview_digests(module, base, env, root, pr)
    return "clean-preview" in live and unread_preview(runs), (live, [(c, marks, "paths unread" in s, "conflict in f.txt" in s) for c, s, marks in runs])


def renormalized_row(module, base):
    env, root, pr = preview_repo(base, texts=("abc\n", "Abc\n", "ABC\n"), attributes="*.txt filter=probe\n")
    git(env, root, "config", "filter.probe.clean", marker(base, "clean-renormalize", "prints the file in capitals", "tr a-z A-Z"))
    git(env, root, "config", "merge.renormalize", "true")
    started(base)
    person = person_merge(env, root, pr)
    live = started(base)
    bare = subprocess.run(["git", "-C", str(root), "-c", "filter.probe.clean=", "merge-tree", "--write-tree", "--name-only", "--no-messages", "main", pr],
                          capture_output=True, env=env).returncode
    runs = preview_digests(module, base, env, root, pr)
    ok = person == (0, []) and "clean-renormalize" in live and bare == 1 and unread_preview(runs)
    return ok, (person, live, bare, [(c, marks, "paths unread" in s, "conflict in f.txt" in s) for c, s, marks in runs])


def unread_after_row(module, base):
    env, root, pr = preview_repo(base)
    configured = lambda: git(env, root, "config", "filter.a=b.clean", "cat")
    gone = lambda: git(env, root, "config", "--remove-section", "filter.a=b", check=False)
    runs = preview_digests(module, base, env, root, pr, before=gone, after_merge=configured)
    gone()
    clean = person_merge(env, root, pr)
    return clean[0] == 1 and unread_preview(runs), (clean, [(c, marks, "paths unread" in s, "conflict in f.txt" in s) for c, s, marks in runs])


def queue_line(said, number):
    return next((l for l in said.splitlines() if l.strip().startswith(f"PR {number} ")), "")


def lfs_shape_row(module, base):
    env, root, pr = preview_repo(base, attributes="*.txt filter=lfs\n")
    git(env, root, "switch", "-q", "-c", "pr2", "main~1")
    (root / "g.txt").write_text("new\n", encoding="utf-8"); git(env, root, "add", "g.txt"); git(env, root, "commit", "-qm", "pr2\n\nSession: abcd1234")
    pr2 = git(env, root, "rev-parse", "HEAD")
    git(env, root, "switch", "-q", "main")
    for k, v in (("filter.lfs.clean", marker(base, "lfs-clean", "prints the file", "cat") + " %f"),
                 ("filter.lfs.smudge", marker(base, "lfs-smudge", "prints the file", "cat") + " %f"),
                 ("filter.lfs.process", process_marker(base)), ("filter.lfs.required", "true")):
        git(env, root, "config", "--global", k, v)
    started(base)
    person = (person_merge(env, root, pr), person_merge(env, root, pr2))
    live = started(base)
    runs = preview_digests(module, base, env, root, pr, more=(("pr2", pr2),))
    lines = [(queue_line(said, 1), queue_line(said, 2)) for _c, said, _m in runs]
    ok = (person == ((1, ["f.txt"]), (0, [])) and not live and len(runs) == 2
          and all(code == 0 and not marks for code, _s, marks in runs)
          and all("conflict in f.txt" in one and "unread" not in one and two and "conflict" not in two and "unread" not in two for one, two in lines))
    return ok, (person, live, [(c, m) for c, _s, m in runs], lines)


def live_filter_row(module, base):
    env, root, pr = preview_repo(base, attributes="*.txt filter=probe\n")
    git(env, root, "config", "filter.probe.clean", marker(base, "clean-live", "prints the file", "cat"))
    seen = {}
    for value in (None, "true", "maybe"):
        if value is None:
            git(env, root, "config", "--unset", "merge.renormalize", check=False)
        else:
            git(env, root, "config", "merge.renormalize", value)
        started(base)
        person = person_merge(env, root, pr) if value != "maybe" else None
        live = started(base)
        runs = preview_digests(module, base, env, root, pr)
        seen[value] = (person, live, [(c, m, queue_line(s, 1)[-90:]) for c, s, m in runs])
        named = all(code == 0 and not marks and "conflict in f.txt" in queue_line(said, 1) for code, said, marks in runs)
        if not (named if value is None else unread_preview(runs)):
            return False, seen
    return seen[None][0] == (1, ["f.txt"]) and not seen[None][1] and "clean-live" in seen["true"][1], seen


def renormalize_after_row(module, base):
    env, root, pr = preview_repo(base, attributes="*.txt filter=probe\n")
    git(env, root, "config", "filter.probe.clean", marker(base, "clean-after", "prints the file", "cat"))
    values = iter(("true", "maybe"))
    unset = lambda: git(env, root, "config", "--unset", "merge.renormalize", check=False)
    runs = preview_digests(module, base, env, root, pr, before=unset, after_merge=lambda: git(env, root, "config", "merge.renormalize", next(values, "true")))
    unset()
    person = person_merge(env, root, pr)
    return person == (1, ["f.txt"]) and unread_preview(runs), (person, [(c, m, queue_line(s, 1)[-90:]) for c, s, m in runs])


def unauthorized_server():
    import http.server
    import threading
    asked = []

    class Unauthorized(http.server.BaseHTTPRequestHandler):
        def answer(self):
            asked.append(self.path)
            self.send_response(401)
            self.send_header("WWW-Authenticate", 'Basic realm="fixture"')
            self.send_header("Content-Length", "0")
            self.end_headers()
        do_GET = do_POST = answer

        def log_message(self, *args):
            pass
    server = http.server.HTTPServer(("127.0.0.1", 0), Unauthorized)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    return server, thread, asked


TRANSPORTS = (("over a local origin", "uploadpack"), ("over SSH", "ssh"), ("over a localhost HTTP server that answers 401", "credential"))


def transport_row(base, tool, over):
    name = dict(TRANSPORTS)[over]
    env = environment(base)
    for k in ("http_proxy", "HTTP_PROXY", "https_proxy", "HTTPS_PROXY", "all_proxy", "ALL_PROXY"):
        env.pop(k, None)
    env.update(no_proxy="127.0.0.1,localhost", NO_PROXY="127.0.0.1,localhost")
    root = base / "wc"
    root.mkdir()
    subprocess.run(["git", "init", "-q", "--bare", "--initial-branch=main", str(base / "origin.git")], check=True, capture_output=True, env=env)
    subprocess.run(["git", "init", "-q", "--initial-branch=main", str(root)], check=True, capture_output=True, env=env)
    real = HERE / "shoalmark.py"
    program([sys.executable, real, "--root", root, "--init", "--key", "ap"], env, root)
    for k, v in (("user.name", "owner"), ("user.email", "o@x"), ("commit.gpgsign", "false"), ("maintenance.auto", "false"), ("core.autocrlf", "false"),
                 ("seat.session", "abcd1234")):
        git(env, root, "config", k, v)
    (root / "shoalmark.toml").write_text('name = "m"\ntracker_dir = "docs/work-tracker"\n[kinds]\nAP = "Work"\n[seats]\nbuilder = "o@x"\n', encoding="utf-8")
    tracker(root, "AP-501")
    program([sys.executable, real, "--root", root], env, root)
    git(env, root, "add", "-A"); git(env, root, "commit", "-qm", "base\n\nSession: abcd1234")
    git(env, root, "remote", "add", "origin", str(base / "origin.git"))
    git(env, root, "push", "-q", "-u", "origin", "main")
    git(env, root, "update-ref", "--no-deref", "-d", "refs/remotes/origin/HEAD")
    server, thread, asked = None, None, []
    try:
        if name == "uploadpack":
            git(env, root, "config", "remote.origin.uploadpack", marker(base, "uploadpack", "then fails, never serving", "exit 1"))
        elif name == "ssh":
            git(env, root, "remote", "set-url", "origin", "ssh://example.invalid/x.git")
            git(env, root, "config", "--global", "core.sshCommand", marker(base, "ssh", "fails", "exit 1"))
        else:
            server, thread, asked = unauthorized_server()
            git(env, root, "remote", "set-url", "origin", f"http://127.0.0.1:{server.server_address[1]}/x.git")
            git(env, root, "config", "--global", "credential.helper", marker(base, "credential", "names no credential", "exit 0"))
        started(base)
        git(env, root, "ls-remote", "origin", check=False)
        live, reached = started(base), len(asked)
        out = {}
        for run_name, args in (("--check", ("--check",)), ("the plain run", ())):
            before = len(asked)
            code, o, e = program([sys.executable, tool, "--root", root, *args], env, root)
            out[run_name] = (code, started(base), len(asked) - before, "no default branch was found" in o + e)
    finally:
        if server is not None:
            server.shutdown()
            server.server_close()
            thread.join(10)
    ok = (name in live and (name != "credential" or reached > 0)
          and all(code == 0 and not marks and not sent and not nodefault for code, marks, sent, nodefault in out.values()))
    return ok, {"live": live, "the server reached by the control": reached, **out}


UNTOLD_LINE = ("the default branch cannot be told — this clone has no `origin/HEAD`, and its cached `origin/main` and `origin/master` name different "
               "commits: run `git remote set-head origin --auto` yourself, which asks origin, then run again")


def trunk_fixture(base):
    env = environment(base)
    root = base / "wc"
    root.mkdir()
    subprocess.run(["git", "init", "-q", "--bare", "--initial-branch=master", str(base / "origin.git")], check=True, capture_output=True, env=env)
    subprocess.run(["git", "init", "-q", "--initial-branch=master", str(root)], check=True, capture_output=True, env=env)
    real = HERE / "shoalmark.py"
    program([sys.executable, real, "--root", root, "--init", "--key", "ap"], env, root)
    for k, v in (("user.name", "owner"), ("user.email", "o@x"), ("commit.gpgsign", "false"), ("maintenance.auto", "false"), ("core.autocrlf", "false"),
                 ("seat.session", "abcd1234")):
        git(env, root, "config", k, v)
    (root / "shoalmark.toml").write_text('name = "m"\ntracker_dir = "docs/work-tracker"\n[kinds]\nAP = "Work"\n[seats]\nbuilder = "o@x"\n', encoding="utf-8")
    tracker(root, "AP-501")
    (root / "notes.txt").write_text("first\n", encoding="utf-8")
    program([sys.executable, real, "--root", root], env, root)
    git(env, root, "add", "-A"); git(env, root, "commit", "-qm", "base\n\nSession: abcd1234")
    git(env, root, "remote", "add", "origin", str(base / "origin.git"))
    git(env, root, "push", "-q", "origin", "master")
    git(env, root, "switch", "-q", "-c", "work")
    (root / "later.txt").write_text("a later commit\n", encoding="utf-8")
    git(env, root, "add", "later.txt"); git(env, root, "commit", "-qm", "a later commit\n\nSession: abcd1234")
    git(env, root, "push", "-q", "origin", "work:refs/heads/main")
    git(env, root, "switch", "-q", "master")
    git(env, root, "fetch", "-q", "origin")
    git(env, root, "update-ref", "--no-deref", "-d", "refs/remotes/origin/HEAD")
    git(env, root, "config", "remote.origin.uploadpack", marker(base, "uploadpack", "then fails, never serving", "exit 1"))
    started(base)
    return env, root


def trunk_runs(env, root, base, tool):
    out = {}
    for name, args in (("--check", ("--check",)), ("the plain run", ())):
        started(base)
        code, o, e = program([sys.executable, tool, "--root", root, *args], env, root)
        out[name] = (code, o + e, e, started(base))
    return out


def trunk_rows(base, tool):
    env, root = trunk_fixture(base)
    told = lambda runs: all(code == 4 and [l.strip() for l in err.splitlines() if "cannot be told" in l] == ["checkout: " + UNTOLD_LINE] and not marks
                            for code, _said, err, marks in runs.values())
    apart = trunk_runs(env, root, base, tool)
    refused = told(apart)
    (root / "notes.txt").write_text("an edit not committed\n", encoding="utf-8")
    edited = trunk_runs(env, root, base, tool)
    refused_edited = told(edited) and git(env, root, "status", "--porcelain", "--untracked-files=no") == "M notes.txt"
    git(env, root, "checkout", "-q", "--", "notes.txt")
    git(env, root, "update-ref", "refs/remotes/origin/main", "refs/remotes/origin/master")
    same = trunk_runs(env, root, base, tool)
    read = all(code == 0 and "cannot be told" not in said and "no default branch was found" not in said and not marks
               for code, said, _err, marks in same.values())
    seen = lambda runs: {k: (c, m, [l.strip()[:90] for l in s.splitlines() if "cannot be told" in l or "no default branch" in l])
                         for k, (c, s, _e, m) in runs.items()}
    return (refused, seen(apart)), (refused_edited, seen(edited)), (read, seen(same))


PROGRAMS = (("clean-local", "a clean filter in the repository's own configuration"), ("clean-worktree", "a clean filter in the worktree's configuration"),
            ("clean-global", "a clean filter in the private global configuration"), ("clean-include", "a clean filter in a file an include brings"),
            ("process", "a process filter"), ("fsmonitor", "`core.fsmonitor`"), ("textconv", "a diff driver's `textconv`"),
            ("diff-command", "a diff driver's `command`"), ("diff-external", "`diff.external`"), ("gpgsm", "`gpg.x509.program`"),
            ("credential", "a credential helper"), ("ssh", "`core.sshCommand`"), ("pager", "`core.pager`"),
            ("hook-post-index-change", "a hooks path: the hook a refresh of the index starts"))


def run_checks(fm, tool=None, results=None):
    tool = pathlib.Path(tool or HERE / "shoalmark.py").resolve()
    rows = results if results is not None else []
    module = fm if tool == (HERE / "shoalmark.py").resolve() else load(tool)
    with tempfile.TemporaryDirectory(prefix="board-settings-") as d:
        top = pathlib.Path(d).resolve()
        for info in (False, True):
            where = "the attribute in `.git/info/attributes` alone" if info else "the attribute in a tracked `.gitattributes`"
            base = top / ("info" if info else "tracked")
            base.mkdir()
            try:
                f = build(base, fm, tool, info)
                live = controls(f)
                paths = run_paths(f, str(tool))
            except Exception as error:
                rows.append((f"the board's reads · {where} · the fixture is built and every path runs", False, f"{type(error).__name__}: {error}"))
                continue
            reads = {name: p for name, p in paths.items() if name != ACT}
            programs = PROGRAMS + ((("clean-required", "a required clean filter"), ("gpg", "`gpg.program`")) if info
                                   else (("gpg-openpgp", "`gpg.openpgp.program`"), ("clean-submodule", "a clean filter a submodule's own configuration names")))
            for name, what in programs:
                hit = [p for p, (_c, _o, _e, marks, _p, _b) in reads.items() if name in marks]
                rows.append((f"the board's reads · {where} · {what}: none of the board's paths starts it — {len(reads)} paths: the board's own run, the plain run, "
                             "`--check`, the commit's hooks as they run the hooks' copy, the digests and every view —, and a read with git's own default in the "
                             "same repository does, so the shape is live",
                             not hit and live.get(name, False) is not False, f"started by {hit[:3]}; live {live.get(name, False)}"))
            wrong = {p: settings_held(procs, f["copy"] if p in COPY_RUNS else tool, f["drivers"]) for p, (_c, _o, _e, _m, procs, _b) in reads.items()}
            counted = sum(len(procs) for (_c, _o, _e, _m, procs, _b) in reads.values())
            rows.append((f"the board's reads · {where} · through git's own trace, every git process of every path reads the board's settings last, from the "
                         "command scope, and every one that compares the working tree reads each configured driver emptied",
                         counted > 0 and not any(wrong.values()), f"{counted} processes; {[(p, w[:2]) for p, w in wrong.items() if w][:3]}"))
            act = paths.get(ACT)
            commits = [p for p in (act[4] if act else []) if p["argv"][1:2] == ["commit"]]
            person = [last(p["params"], "core.fsmonitor") for p in commits]
            rows.append((f"the board's reads · {where} · an act's own git runs under the person's settings: `--answer` reaches its commit, which reads the "
                         "person's `core.fsmonitor` last, not the board's",
                         act is not None and act[0] == 0 and bool(commits) and all(v is not None and v[0] != "command" for v in person),
                         f"exit {act[0] if act else None}; its commits read {person}; {(act[2] if act else '').strip()[-160:]!r}"))
            probe = next((p for p in (act[4] if act else []) if p["argv"][1:4] == ["rev-parse", "--absolute-git-dir", "--git-common-dir"]), None)
            rows.append((f"the board's reads · {where} · the reading rule's first git runs with the board's settings even in an act: `--answer`'s "
                         "`rev-parse --absolute-git-dir --git-common-dir` reads `core.fsmonitor` false from the command scope",
                         probe is not None and last(probe["params"], "core.fsmonitor") == ("command", "false"),
                         f"the probe read {last(probe['params'], 'core.fsmonitor') if probe else 'no probe in the act trace'}"))
            plain = paths["the plain run"]
            hooked = paths["the pre-commit hook's write, `--print-written`"]
            rows.append((f"the board's reads · {where} · a count of changed paths is right or not read: git compared a file a configured driver stores "
                         + ("— its driver required, so the comparison fails —" if info else "— it reads as changed without its driver —")
                         + " and the plain run's board and the commit's hook's say the count is not read",
                         plain[0] == 0 and hooked[0] == 0 and all("changes" in (r or {}) and r["changes"] is None for r in (plain[5], hooked[5])),
                         f"exits {plain[0]}, {hooked[0]}; the records {[(r or {}).get('changes', 'absent') for r in (plain[5], hooked[5])]}; {hooked[2].strip()[-160:]!r}"))
            check = paths["`--check`"]
            said = check[1] + check[2]
            rows.append((f"the board's reads · {where} · `--check` says in one line that the working tree's edits were not read, and judges the branch's commits",
                         said.count(NOT_READ_LINE) == 1 and "the tree has uncommitted edits" not in said,
                         f"exit {check[0]}; {[l for l in said.splitlines() if 'working tree' in l or 'uncommitted' in l][:2]}"))
        base = top / "control"
        base.mkdir()
        try:
            count, gate, marks = count_control(base, fm, tool)
            rows.append(("the board's reads · where no file a configured driver stores is compared — git holds it as clean, a new file its attribute names "
                         "is not compared —, the count is read and right, `--check` reads the edits, and no driver starts",
                         count == 2 and gate == (True, False) and not marks, f"count {count!r}; `--check` said edits {gate[0]}, not read {gate[1]}; markers {marks}"))
        except Exception as error:
            rows.append(("the board's reads · the count's control", False, f"{type(error).__name__}: {error}"))
        base = top / "window"
        base.mkdir()
        try:
            ok, saw = window_row(module, base)
            rows.append(("the board's reads · a comparison after which the drivers listed again are not the ones it ran without is not read; with the same "
                         "drivers before and after, it is", ok, f"not read: {saw}"))
        except Exception as error:
            rows.append(("the board's reads · the drivers listed again after a comparison", False, f"{type(error).__name__}: {error}"))
        base = top / "merge"
        base.mkdir()
        try:
            ok, saw = merge_preview_row(module, base)
            rows.append(("the board's reads · the digests' conflict preview starts no configured merge driver: through `--owner` and `--standup`, with the "
                         "driver's `merge` attribute in the working tree, in `.git/info/attributes` and in a scratch-global file, no marker starts and the "
                         "preview is reported as not read", ok, f"markers {saw}"))
        except Exception as error:
            rows.append(("the board's reads · the digests' conflict preview starts no configured merge driver", False, f"{type(error).__name__}: {error}"))
        for name, row, label in (
                ("unread-filters", unread_filters_row,
                 "the digests' conflict preview with a filter list that cannot be read: through `--owner` and `--standup`, with `merge.renormalize` on and a "
                 "clean filter an attribute selects, which the person's own merge-tree starts, no marker starts and the preview is reported as not read"),
                ("renormalized", renormalized_row,
                 "the digests' conflict preview where renormalizing through a configured filter merges clean and the same merge without it conflicts: "
                 "through `--owner` and `--standup` the preview is reported as not read, never as a conflict, and no marker starts"),
                ("unread-after", unread_after_row,
                 "the digests' conflict preview whose filter list cannot be read after the merge-tree: through `--owner` and `--standup`, where the same "
                 "merge conflicts, the preview is reported as not read"),
                ("lfs-shape", lfs_shape_row,
                 "the digests' conflict preview with a filter driver in git-lfs's shape in the private global configuration — its `clean`, `smudge`, "
                 "`process` and `required` — and `merge.renormalize` unset: through `--owner` and `--standup` it names the conflict the person's own "
                 "merge-tree names, reads the pull request that merges clean as clean, and starts no marker"),
                ("live-filter", live_filter_row,
                 "the digests' conflict preview with a live clean-filter marker: with `merge.renormalize` unset no filter starts and the preview names the "
                 "conflict; with it true, or no boolean, the preview is reported as not read; the marker never starts, where the person's own "
                 "renormalizing merge-tree starts it"),
                ("renormalize-after", renormalize_after_row,
                 "the digests' conflict preview whose `merge.renormalize` changes or cannot be read after the merge-tree: through `--owner` and "
                 "`--standup`, with a filter driver configured, the preview is reported as not read")):
            base = top / name
            base.mkdir()
            try:
                ok, saw = row(module, base)
                rows.append(("the board's reads · " + label, ok, f"{saw}"))
            except Exception as error:
                rows.append((f"the board's reads · the digests' conflict preview, the {name} fixture", False, f"{type(error).__name__}: {error}"))
        for n, (over, name) in enumerate(TRANSPORTS):
            base = top / f"transport-{n}"
            base.mkdir()
            does = {"uploadpack": "starts its `remote.origin.uploadpack` marker", "ssh": "starts the `core.sshCommand` marker",
                    "credential": "reaches the server and starts the credential helper's marker"}[name]
            try:
                ok, saw = transport_row(base, str(tool), over)
                rows.append((f"the board's reads · the trunk is read from cached refs {over}: `git ls-remote origin` {does}, and `--check` and the plain run, "
                             "with `origin/HEAD` deleted and `origin/main` cached, start no marker" + (", send the server nothing" if name == "credential" else "")
                             + " and exit 0", ok, f"{saw}"))
            except Exception as error:
                rows.append((f"the board's reads · the trunk read from cached refs, the fixture {over}", False, f"{type(error).__name__}: {error}"))
        base = top / "trunk"
        base.mkdir()
        try:
            (refused, saw_apart), (refused_edited, saw_edited), (read, saw_same) = trunk_rows(base, str(tool))
            rows.append(("the board's reads · the trunk that cannot be told: with `origin/HEAD` deleted and the cached `origin/main` and `origin/master` at "
                         "different commits, `--check` and the plain run each exit 4 with the one line that names `git remote set-head origin --auto`, and "
                         "start no marker", refused, f"{saw_apart}"))
            rows.append(("the board's reads · the trunk that cannot be told, with the working tree edited: the same, and `--check` and the plain run, an "
                         "edit of a tracked file not committed, each exit 4 with the one line and start no marker", refused_edited, f"{saw_edited}"))
            rows.append(("the board's reads · the trunk where the cached `origin/main` and `origin/master` name the same commit: with `origin/HEAD` deleted, "
                         "`--check` and the plain run each read it and exit 0", read, f"{saw_same}"))
        except Exception as error:
            rows.append(("the board's reads · the trunk where `origin/HEAD` is absent", False, f"{type(error).__name__}: {error}"))
    return rows


def copy_tool(where, source):
    for rel in load(HERE / "shoalmark.py").copy_files():
        (where / rel).parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(HERE / rel, where / rel)
    (where / "shoalmark.py").write_text(source, encoding="utf-8")
    return where / "shoalmark.py"


def clean_control(fm, d):
    copy = copy_tool(pathlib.Path(d) / "clean", pathlib.Path(fm.__file__).read_text(encoding="utf-8"))
    assert copy.read_bytes() == pathlib.Path(fm.__file__).read_bytes(), "the clean control is not byte-identical to the tool"
    return {label: ok for label, ok, _ in run_checks(fm, copy)}


def mutants(fm, control):
    source = pathlib.Path(fm.__file__).read_text(encoding="utf-8")
    with tempfile.TemporaryDirectory(prefix="board-settings-mutant-") as d:
        for n, (name, old, new, designated) in enumerate(MUTANTS):
            if source.count(old) != 1:
                yield name, designated, None
                continue
            copy = copy_tool(pathlib.Path(d) / f"mutant-{n}", source.replace(old, new))
            rows = {label: ok for label, ok, _ in run_checks(fm, copy)}
            hits = [label for label in rows if designated in label]
            killed = len(hits) == 1 and control.get(hits[0]) is True and rows[hits[0]] is False
            yield name, hits, killed


if __name__ == "__main__":
    tools = [a for a in sys.argv[1:] if a != "--mutants"]
    fm = load(HERE / "shoalmark.py")
    results = run_checks(fm, tools[0] if tools else None)
    for label, ok, saw in results:
        print(("  ok    " if ok else "  FAIL  ") + label + ("" if ok else f" (saw {saw})"))
    failed = sum(not ok for _, ok, _ in results)
    print(f"{len(results) - failed} passed; {failed} failed")
    survived = 0
    if "--mutants" in sys.argv[1:]:
        with tempfile.TemporaryDirectory(prefix="board-settings-control-") as _d:
            control = clean_control(fm, _d)
            control_failed = [label for label, ok in control.items() if not ok]
            if control_failed:
                print(f"  FAIL  the clean control: {len(control_failed)} row(s) of a byte-identical copy fail — the fixture's start state is not independent of the tool's place")
                for label in control_failed:
                    print(f"          fails: {label}")
            else:
                print(f"  ok    the clean control: every one of a byte-identical copy's {len(control)} rows passes")
            survived += bool(control_failed)
            for name, hits, killed in mutants(fm, control):
                if hits is None:
                    print(f"  FAIL  mutant: {name} — it cannot run here")
                elif killed:
                    print(f"  ok    mutant: {name} — killed: its designated row turns red: {hits}")
                else:
                    print(f"  FAIL  mutant: {name} — NOT killed as designated: {len(hits)} row(s) named {hits}; exactly one must turn from green (in the control) to red")
                survived += not killed
        print(f"mutants: {len(MUTANTS) + 1 - survived} killed as required; {survived} not")
    sys.exit(1 if failed or survived else 0)
