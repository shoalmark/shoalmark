"""FM-024, defect 7: a worktree a seat adds carries the seat's whole identity — one harness id is one session.

Run directly, or through test_shoalmark.py: `python3 test_worktree_identity.py [TOOL] [DOCS]` — TOOL the tool's file (default: shoalmark.py beside
this file), DOCS the folder whose README.md and AGENTS.md hold the setup step (default: this file's folder), so a mutant of either is run by naming
it. Every fixture is a throwaway repository with `extensions.worktreeConfig`; git reads no global or system configuration, and the harness's logs
are looked for under a home of the fixture's own.

The class (FM-024's *Test for the class*): a parent worktree carries every `user.*` and `seat.*` key and the signers path; a child is added from it
and then overwrites every subset of the four `user.*` and `seat.*` keys in turn. EACH MIXED IDENTITY IS REPORTED BY NAME — all fourteen, by the
child's `--whoami` and its prepare-commit-msg hook, each line naming the worktree and every key it shares and every key that differs. The one named
limit is the full, unchanged copy, pinned silent; a child that wrote every key is silent. The scan stays within its bound: at the 32-worktree cap,
at most 34 git processes, matching or not, each on the read-only list. The setup step, as README.md and AGENTS.md print it, is run and leaves no key
inherited.
"""

import contextlib
import importlib.util
import io
import itertools
import os
import pathlib
import re
import shlex
import shutil
import subprocess
import sys
import tempfile


HERE = pathlib.Path(__file__).resolve().parent
KEYS = ("user.name", "user.email", "seat.session", "seat.harness")          # every user.* and seat.* key a seat's worktree carries, in the report's order
SIGNERS = "gpg.ssh.allowedSignersFile"
PARENT = {"user.name": "Planner seat", "user.email": "planner@seat", "seat.session": "aaaaaaaa", "seat.harness": "parent-harness-0001",
          SIGNERS: "parent/allowed_signers"}
CHILD = {"user.name": "Builder seat", "user.email": "builder@seat", "seat.session": "aaaaaaaa/builder-1", "seat.harness": "child-harness-0001"}
SEATS = '\n[seats]\nowner = "owner@example.org"\nplanner = "planner@seat"\nbuilder = "builder@seat"\n'
REPORT = "one harness id is one session"
PAIR = re.compile(r"one harness id is one session — (.+?) carries this worktree's (.+?) under another identity: (.+?) — `git worktree add` ")
OWN = re.compile(r"one harness id is one session — this worktree's seat\.session (\S+) names the seat (\S+), and its user\.email (\S+) is the seat (\S+):")
CAP_PROCESSES = 34                                                           # the bound at the 32-worktree cap: the list, this worktree, 32 others


def oracle(kept):
    """FM-024's acceptance, restored: every mixed identity is named by the report, and the full, unchanged copy is the one named limit. For a child that
    kept the parent's keys `kept`: (a line naming the parent is due, a line naming the child's own session against its address is due, the label)."""
    kept = set(kept)
    mixed = 0 < len(kept) < len(KEYS)
    pair = mixed and (bool(kept & {"seat.session", "seat.harness"}) or ("user.name" in kept and "user.email" not in kept))
    own = mixed and "user.email" in kept and "seat.session" not in kept   # the parent's address under the child's `<parent>/builder-1`
    label = ("its own: every key written" if not kept else "THE NAMED LIMIT: a full, unchanged copy, the same seat's second worktree to the tool"
             if not mixed else "a mixed identity, named by the report")
    return pair, own, label


@contextlib.contextmanager
def isolated(home):
    """The process's environment for one block: no `GIT_*` from outside, no Codex thread, git's global and system configuration unread, and a
    home of its own — the harness's logs are looked for under it."""
    saved = dict(os.environ)
    for k in [k for k in os.environ if k.startswith("GIT_") or k == "CODEX_THREAD_ID"]:
        del os.environ[k]
    os.environ.update(HOME=str(home), USERPROFILE=str(home), XDG_CONFIG_HOME=str(home / ".config"), GIT_CONFIG_NOSYSTEM="1")
    try:
        yield
    finally:
        os.environ.clear()
        os.environ.update(saved)


def git(cwd, *a):
    return subprocess.run(["git", "-C", str(cwd), *a], capture_output=True, text=True, encoding="utf-8", errors="replace", env=dict(os.environ))


def tool(fm, root, *argv):
    """The tool, in process: (exit, stdout, stderr)."""
    out, err = io.StringIO(), io.StringIO()
    with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
        try:
            code = fm.main(["--root", str(root), *argv])
        except SystemExit as e:
            code = e.code if isinstance(e.code, int) else 1
    return code, out.getvalue(), err.getvalue()


def reported(stream):
    return [l for l in stream.splitlines() if REPORT in l and "past the first" not in l]


def shown(path):
    """A folder as the report shows it: resolved, a line break in its name written `\\n`."""
    return os.path.realpath(str(path)).replace("\r", "\\r").replace("\n", "\\n")


def pair_line(line, other, kept, mine, theirs):
    """Whether one report line names the worktree `other`, every key it shares with this one (`kept`, with this one's values) and every key that differs
    (its value there, this one's here) — exactly, in the report's order."""
    m = PAIR.search(line)
    return (bool(m) and os.path.normcase(m.group(1)) == os.path.normcase(shown(other))
            and m.group(2) == ", ".join(f"{k} {mine[k]}" for k in KEYS if k in kept)
            and m.group(3) == "; ".join(f"{k} {theirs[k]} there, {mine[k]} here" for k in KEYS if k not in kept))


def own_line(line, mine):
    """Whether one report line names this worktree's own session against its address: the seat each names."""
    m = OWN.search(line)
    return bool(m) and m.groups() == (mine["seat.session"], mine["seat.session"].split("/")[1].rsplit("-", 1)[0], mine["user.email"], mine["user.email"].split("@")[0])


def step_blocks(text):
    """The fenced ```bash blocks of a document that run `git worktree add "$w"` — the setup step."""
    return [b for b in re.findall(r"^```bash\n(.*?)^```", text, re.S | re.M) if 'git worktree add "$w"' in b]


def run_step(block, parent, target):
    """The setup step, run line by line from `parent` into a new worktree at `target`: `w=` names it, `"$w"` is it, and the add line adds it, detached,
    whatever branch the document names. Each other line is one git command; anything else is a line the test cannot read. [(argv, exit, stdout)]."""
    ran = []
    for raw in block.splitlines():
        words = shlex.split(raw, comments=True)
        if not words:
            continue
        if len(words) == 1 and words[0].startswith("w="):
            continue
        if words[0] != "git":
            raise ValueError(f"a line the test does not read: {raw!r}")
        words = [str(target) if w == "$w" else w for w in words]
        if words[1:3] == ["worktree", "add"]:
            words = ["git", "worktree", "add", "-q", "--detach", str(target)]
        r = subprocess.run(words, cwd=str(parent), capture_output=True, text=True, encoding="utf-8", errors="replace", env=dict(os.environ))
        ran.append((words, r.returncode, r.stdout))
    return ran


def step_checks(fm, base, parent, docs, check):
    """The setup step, as README.md and AGENTS.md print it: run from the parent, it leaves none of the five keys inherited and prints the list."""
    for doc in ("README.md", "AGENTS.md"):
        text = (docs / doc).read_text(encoding="utf-8")
        blocks = step_blocks(text)
        where = text.find(blocks[0]) if len(blocks) == 1 else -1
        outside = doc != "AGENTS.md" or not (text.find("<!-- BEGIN shoalmark") < where < text.find("<!-- END shoalmark -->"))
        target = base / ("step-" + doc.split(".")[0].lower())
        try:
            ran = run_step(blocks[0], parent, target) if len(blocks) == 1 else []
            why = ""
        except ValueError as e:
            ran, why = [], str(e)
        got = {k: (git(target, "config", "--worktree", "--get", k).stdout.strip() or None) for k in (*KEYS, SIGNERS)} if ran else {}
        inherited = sorted(k for k, v in got.items() if v is not None and v == PARENT[k])
        unwritten = sorted(k for k in ("user.name", "user.email", "seat.session", SIGNERS) if not got.get(k))
        listed = ran[-1][2].lower() if ran else ""
        prints = bool(ran) and ran[-1][0][-3:] == ["config", "--worktree", "--list"] and all(f"{k.lower()}=" in listed for k in ("user.name", "user.email", "seat.session", SIGNERS))
        clean = all(code == 0 or (argv[-2:] == ["--unset-all", "seat.harness"] and code == 5) for argv, code, _ in ran)
        check(f"the setup step in {doc} writes every identity key of a new seat's worktree — user.name, user.email, seat.session, seat.harness "
              f"and the signers path — none is the parent's, and it prints `git config --worktree --list`",
              len(blocks) == 1 and outside and not why and clean and not inherited and not unwritten and got.get("seat.harness") is None and prints,
              f"blocks {len(blocks)}, outside the markers {outside}, {why or 'read'}, inherited {inherited}, unwritten {unwritten}, "
              f"seat.harness {got.get('seat.harness')!r}, prints the list {prints}")


def run_checks(fm, docs=HERE):
    results = []

    def check(label, ok, detail=""):
        results.append(("FM-024 defect 7 · " + label, bool(ok), "" if ok else detail))

    saved, committing = fm.ROOT, fm.COMMITTING
    try:
        with tempfile.TemporaryDirectory() as tmp:
            base = pathlib.Path(tmp).resolve()
            (base / "home").mkdir()
            (base / "nohooks").mkdir()
            with isolated(base / "home"):
                identity_checks(fm, base, pathlib.Path(docs), check, lambda label, why: results.append(("FM-024 defect 7 · " + label, None, why)))
    finally:
        fm.configure(saved)
        fm.COMMITTING = committing
    return results


_WATCH = []                 # while a list is here, every process the run starts is appended to the newest one (`_audit`)
_HOOKED = [False]


def _audit(event, args):
    if event == "subprocess.Popen" and _WATCH:
        _WATCH[-1].append(args[1] if isinstance(args[1], str) else [str(a) for a in args[1]])


@contextlib.contextmanager
def watched():
    """Every process started inside, as its argv — through an audit hook (`sys.addaudithook`), so no start escapes it however it is made."""
    if not _HOOKED[0]:
        sys.addaudithook(_audit)
        _HOOKED[0] = True
    seen = []
    _WATCH.append(seen)
    try:
        yield seen
    finally:
        _WATCH.pop()


def identity_checks(fm, base, docs, check, skip):
    parent, child = base / "parent", base / "child"
    git(base, "init", "-q", str(parent))
    git(parent, "config", "extensions.worktreeConfig", "true")
    for k, v in PARENT.items():
        git(parent, "config", "--worktree", k, v)
    _, init_out, _ = tool(fm, parent, "--init", "--key", "msr")
    (parent / "shoalmark.toml").write_text((parent / "shoalmark.toml").read_text(encoding="utf-8") + SEATS, encoding="utf-8")
    git(parent, "add", "-A")
    git(parent, "-c", f"core.hooksPath={base / 'nohooks'}", "-c", "commit.gpgsign=false", "commit", "-q", "-m", "start\n\nSession: aaaaaaaa")

    # the setup line `--init` prints: every key named, and the copy said. (`--schema` keeps its text: FM-044's Git entry differential holds it to
    # its immutable baseline, byte for byte)
    line = next((l for l in init_out.splitlines() if l.startswith("next:")), "")
    check("`--init`'s setup line names every identity key of a seat's worktree and says that `git worktree add` copies them",
          all(f"`{k}`" in line for k in (*KEYS, SIGNERS)) and "`git worktree add` copies every one" in line, line[-400:])

    # the one read the scan adds to the read-only list: exactly as the tool sends it, and in no other form
    pattern = fm.SEAT_IDENTITY_KEYS
    bent = [["git", "config", "--get-regexp", pattern], ["git", "config", "-z", "--get-regexp", "."], ["git", "config", "-z", "--get-regexp", pattern, "x"],
            ["git", "config", "-z", "--get-regexp", pattern.replace("harness", "harnes.")], ["git", "config", "-z", "--list"], ["git", "config", "--get-all", "seat.harness"],
            ["git", "-c", "core.fsmonitor=x", "config", "-z", "--get-regexp", pattern], ["git", "config", "-z", "--get-regexp", pattern, "--replace-all"]]
    check("the scan's one added read — `config -z --get-regexp` with the four identity keys — is on the read-only list as the tool sends it, and in no other form",
          pattern == r"^(user\.(name|email)|seat\.(session|harness))$" and fm.read_only_git(["git", "-C", str(child), "config", "-z", "--get-regexp", pattern])
          and not any(fm.read_only_git(b_) for b_ in bent), str([b_ for b_ in bent if fm.read_only_git(b_)]))

    # the defect's fact: git's own `worktree add` copies the parent's whole `config.worktree`
    git(parent, "worktree", "add", "-q", "--detach", str(child))
    copied = {k: git(child, "config", "--worktree", "--get", k).stdout.strip() for k in PARENT}
    if not any(copied[k] == PARENT[k] for k in PARENT):
        skip("`git worktree add` copies the parent's whole identity into the child", "this git's `worktree add` copies no `config.worktree`")
    else:
        check("`git worktree add` copies the parent's whole identity into the child — user.name, user.email, seat.session, seat.harness, the signers path",
              copied == PARENT, str(copied))

    # THE CLASS: the child keeps every subset of the parent's four keys in turn and writes its own others
    msg, named, silent = base / "MSG", [], []
    for n in range(len(KEYS) + 1):
        for kept in itertools.combinations(KEYS, n):
            for k in KEYS:
                git(child, "config", "--worktree", k, PARENT[k] if k in kept else CHILD[k])
            mine = {k: PARENT[k] if k in kept else CHILD[k] for k in KEYS}
            pair, own, label = oracle(kept)
            here, there = tool(fm, child, "--whoami"), tool(fm, parent, "--whoami")
            msg.write_text("a seat's subject\n", encoding="utf-8")
            hook = tool(fm, child, "--session-trailer", str(msg))
            lines = {"--whoami here": reported(here[2]), "--whoami in the parent": reported(there[2]), "the hook here": reported(hook[2])}
            due = int(pair) + int(own)
            right = lambda ls: (len(ls) == due and (not pair or any(pair_line(l, parent, kept, mine, PARENT) for l in ls))
                                and (not own or any(own_line(l, mine) for l in ls)))
            ok = (right(lines["--whoami here"]) and right(lines["the hook here"]) and len(lines["--whoami in the parent"]) == int(pair)
                  and (not pair or pair_line(lines["--whoami in the parent"][0], child, kept, PARENT, mine))
                  and here[0] == 0 and there[0] == 0 and hook[0] == 0 and f"Session: {mine['seat.session']}" in msg.read_text(encoding="utf-8"))
            (named if lines["--whoami here"] and lines["the hook here"] else silent).append(kept)
            check(f"the child that kept {', '.join(kept) or 'nothing'} of the parent's — {label}", ok, f"lines {lines}")
    mixed = [k for k in named + silent if 0 < len(k) < len(KEYS)]
    check("FM-024's acceptance: each of the fourteen mixed identities is named by the report, in the child's `--whoami` and in its hook; the full, unchanged "
          "copy is THE NAMED LIMIT, silent, and so is the child that wrote every key",
          len(mixed) == 14 and all(k in named for k in mixed) and silent == [(), KEYS], f"named {len(named)}, silent {silent}")

    # the child that wrote its name, address and session and kept only the parent's harness id: the state the night met (2026-10-15)
    for k in KEYS:
        git(child, "config", "--worktree", k, PARENT[k] if k == "seat.harness" else CHILD[k])
    mine, hid = dict(CHILD, **{"seat.harness": PARENT["seat.harness"]}), PARENT["seat.harness"]
    kept = ("seat.harness",)
    fm.configure(child)

    # not known: git's exit 128 (no such folder) and 1 (none of the keys is set) read None; a worktree whose folder is gone, or that holds none of the
    # keys, matches nothing; a key set nowhere is said so
    gone, third, empty = base / "gone", base / "third", base / "empty"
    for w in (gone, third, empty):
        git(parent, "worktree", "add", "-q", "--detach", str(w))
    shutil.rmtree(gone)
    git(third, "config", "--worktree", "--unset", "seat.session")
    for k in KEYS:
        git(empty, "config", "--worktree", "--unset", k)
    codes = (git(gone, "config", "-z", "--get-regexp", pattern).returncode, git(empty, "config", "-z", "--get-regexp", pattern).returncode)
    says = reported(tool(fm, child, "--whoami")[2])
    nothing = dict.fromkeys(KEYS)
    check("a read git ends in 128 (the worktree's folder is gone) or in 1 (none of the four keys is set) is not known: it matches nothing, and a key not "
          "known is said so",
          codes == (128, 1) and fm.worktree_identity(str(gone)) == nothing and fm.worktree_identity(str(empty)) == nothing and len(says) == 2
          and any(pair_line(l, parent, kept, mine, PARENT) for l in says) and any(pair_line(l, third, kept, mine, dict(PARENT, **{"seat.session": "not known"})) for l in says),
          f"exits {codes}, lines {says}")

    # a folder whose name holds a line break is one worktree (`git worktree list --porcelain -z`), and its line stays one line, the break written `\n`:
    # in `--whoami` and in the hook
    if os.name == "nt":
        skip("a worktree folder whose name holds a line break is named, on one line", "Windows allows no line break in a folder's name")
    else:
        broken = base / "line\nbreak"
        git(parent, "worktree", "add", "-q", "--detach", str(broken))
        said_by = {}
        for how, run_ in (("--whoami", lambda: tool(fm, child, "--whoami")), ("the hook", lambda: tool(fm, child, "--session-trailer", str(msg)))):
            msg.write_text("a seat's subject\n", encoding="utf-8")
            out_ = run_()
            said_by[how] = [l for l in reported(out_[2]) if pair_line(l, broken, kept, mine, PARENT)]
        check("a worktree folder whose name holds a line break is one worktree, named in one line with the break written `\\n` — by `--whoami` and by the hook",
              broken.is_dir() and all(len(v) == 1 and "line\\nbreak carries" in v[0] for v in said_by.values()), str(said_by))

    # the command line's `-c` scope names this commit's author, not another worktree's setting: it masks no difference
    os.environ.update(GIT_CONFIG_COUNT="1", GIT_CONFIG_KEY_0="user.email", GIT_CONFIG_VALUE_0="builder@seat")
    try:
        found = fm.shared_harness(hid, str(child))[0]
    finally:
        for k in ("GIT_CONFIG_COUNT", "GIT_CONFIG_KEY_0", "GIT_CONFIG_VALUE_0"):
            os.environ.pop(k, None)
    at_parent = next((f["differ"] for f in found if f["folder"] and os.path.realpath(f["folder"]) == os.path.realpath(str(parent))), [])
    check("`git -c user.email=… commit` hands its `-c` to the hook; another worktree's setting is read without it, so it masks no difference",
          ("user.email", "planner@seat", "builder@seat") in at_parent, str(found))

    # THE BOUND: at the 32-worktree cap one scan starts at most 34 git processes — the list, this worktree's identity and one read of each of 32 others
    # — matching or not, each on the read-only list; counted through an audit hook, so no start escapes the count
    bound, wts = base / "bound", base / "bound-worktrees"
    git(base, "init", "-q", str(bound))
    git(bound, "config", "extensions.worktreeConfig", "true")
    for k, v in PARENT.items():
        git(bound, "config", "--worktree", k, v)
    git(bound, "-c", f"core.hooksPath={base / 'nohooks'}", "-c", "commit.gpgsign=false", "commit", "-q", "--allow-empty", "-m", "start")
    peers = [wts / f"w{i:02}" for i in range(34)]                       # the scanner and 33 more: with the main worktree, 34 others, two past the cap
    for w in peers:
        git(bound, "worktree", "add", "-q", "--detach", str(w))
    scanner = peers[0]
    fm.configure(scanner)
    seen_by = {}
    for case, written in (("every harness id matching", ("user.name", "user.email", "seat.session")), ("none matching", KEYS)):
        for k in written:
            git(scanner, "config", "--worktree", k, CHILD[k])
        hid_ = fm.harness_id()
        with watched() as seen:
            found, unread, listed = fm.shared_harness(hid_, str(scanner))
        argvs = [fm.split_cmdline(a) if isinstance(a, str) else a for a in seen]
        lists = [a for a in argvs if a[1:3] == ["worktree", "list"]]
        reads = [a for a in argvs if a[1:2] == ["-C"] and a[3:] == ["config", "-z", "--get-regexp", pattern]]
        seen_by[case] = (len(argvs), len(lists), len(reads), len(found), unread, all(fm.read_only_git(a) for a in argvs))
    check(f"one scan at the cap starts at most {CAP_PROCESSES} git processes, matching or not — the list, this worktree's identity, one read of each of 32 "
          "other worktrees — every one on the read-only list, and says the two past the cap unread",
          seen_by == {"every harness id matching": (34, 1, 33, 32, 2, True), "none matching": (34, 1, 33, 0, 2, True)}, str(seen_by))
    fm.configure(child)

    # the hook itself, installed in a scratch repository: a commit in the child is made, carries its own Session:, and the line is said
    code_hook = tool(fm, parent, "--install-hook")[0]
    c = git(child, "-c", "commit.gpgsign=false", "commit", "-q", "--allow-empty", "-m", "a seat's commit")
    body = git(child, "log", "-1", "--format=%B").stdout
    said = [l for l in reported(c.stderr) if l.startswith("--session-trailer: ") and pair_line(l, parent, kept, mine, PARENT)]
    check("the installed prepare-commit-msg hook names the mixed identity on a commit in the child, and the commit is made with the child's own Session:",
          code_hook == 0 and c.returncode == 0 and len(said) == 1 and "Session: aaaaaaaa/builder-1" in body,
          f"hook {code_hook}, commit {c.returncode} {c.stderr.strip()[-400:]!r}, {body!r}")

    # only the setup step closes the limit: run as the documents print it
    step_checks(fm, base, parent, docs, check)


def load(path):
    spec = importlib.util.spec_from_file_location("shoalmark_under_test", path)
    fm = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(fm)
    return fm


if __name__ == "__main__":
    tool_path = pathlib.Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else HERE / "shoalmark.py"
    docs_path = pathlib.Path(sys.argv[2]).resolve() if len(sys.argv) > 2 else HERE
    results = run_checks(load(tool_path), docs_path)
    for label, ok, detail in results:
        print(("  ok    " if ok else "  FAIL  ") + label + (" — " + detail if detail else ""))
    print(f"{sum(ok for _, ok, _ in results)} passed; {sum(not ok for _, ok, _ in results)} failed")
    sys.exit(any(not ok for _, ok, _ in results))
