"""FM-024, defect 7: a worktree a seat adds carries the seat's whole identity — one harness id is one session.

Run directly, or through test_shoalmark.py: `python3 test_worktree_identity.py [TOOL] [DOCS]` — TOOL the tool's file (default: shoalmark.py beside
this file), DOCS the folder whose README.md and AGENTS.md hold the setup step (default: this file's folder), so a mutant of either is run by naming
it. Every fixture is a throwaway repository with `extensions.worktreeConfig`; git reads no global or system configuration, and the harness's logs
are looked for under a home of the fixture's own.

The class (FM-024's *Test for the class*): a parent worktree carries every `user.*` and `seat.*` key and the signers path; a child is added from it
and then overwrites every subset of the four `user.*` and `seat.*` keys in turn. Each of the sixteen identities is held to one named outcome: its
own; named by the report (`--whoami` on both sides and the prepare-commit-msg hook); named by the session rule; or one of the named limits — a
full, unchanged copy, one session under two harness ids, the author's name alone. The setup step, as README.md and AGENTS.md print it, is run and
leaves no key inherited.
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
KEYS = ("user.name", "user.email", "seat.session", "seat.harness")          # every user.* and seat.* key a seat's worktree carries
SIGNERS = "gpg.ssh.allowedSignersFile"
PARENT = {"user.name": "Planner seat", "user.email": "planner@seat", "seat.session": "aaaaaaaa", "seat.harness": "parent-harness-0001",
          SIGNERS: "parent/allowed_signers"}
CHILD = {"user.name": "Builder seat", "user.email": "builder@seat", "seat.session": "aaaaaaaa/builder-1", "seat.harness": "child-harness-0001"}
SEATS = '\n[seats]\nowner = "owner@example.org"\nplanner = "planner@seat"\nbuilder = "builder@seat"\n'
REPORT = "one harness id is one session"
ORDER = ("seat.session", "user.email", "user.name")                         # the order the report names the keys in (`SEAT_IDENTITY_KEYS`)


def outcome(written):
    """The named outcome of a child that wrote the keys `written` and kept the parent's others: (named by the report, named by the session rule, label)."""
    shared = "seat.harness" not in written
    differ = [k for k in ORDER if k in written]
    report = shared and bool(differ)
    rule = "seat.session" in written and "user.email" not in written      # the parent's address under the child's `<parent>/builder-1`
    if len(written) == len(KEYS):
        label = "its own: every key written"
    elif report or rule:
        label = "named by " + " and ".join(w for w, on in (("the report", report), ("the session rule", rule)) if on)
    elif not written:
        label = "THE NAMED LIMIT: a full, unchanged copy, the same seat's second worktree to the tool"
    elif "seat.session" not in written:
        label = "a named limit: one session under two harness ids, which the report does not read"
    else:
        label = "a named limit: the author's name alone, which neither the report nor the session rule reads"
    return report, rule, label


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


def names(line, other, differ, mine, theirs):
    """Whether one report line names the worktree `other` and exactly the keys `differ`, each with its value there and here."""
    m = re.search(r" — (.+?) carries this worktree's seat\.harness ", line)
    same = bool(m) and os.path.normcase(os.path.realpath(m.group(1))) == os.path.normcase(os.path.realpath(str(other)))
    return same and all((f"{k} {theirs[k]} there, {mine[k]} here" in line) == (k in differ) for k in ORDER)


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

    # the setup line `--init` prints, and `--schema`: every key named, and the copy said
    line = next((l for l in init_out.splitlines() if l.startswith("next:")), "")
    schema = tool(fm, parent, "--schema")[1]
    check("`--init`'s setup line names every identity key of a seat's worktree and says that `git worktree add` copies them; `--schema` lists all five",
          all(f"`{k}`" in line for k in (*KEYS, SIGNERS)) and "`git worktree add` copies every one" in line
          and all(f"| `{k}` |" in schema for k in (*KEYS, SIGNERS)) and "`git worktree add` copies every one" in schema, line[-400:])

    # the defect's fact: git's own `worktree add` copies the parent's whole `config.worktree`
    git(parent, "worktree", "add", "-q", "--detach", str(child))
    copied = {k: git(child, "config", "--worktree", "--get", k).stdout.strip() for k in PARENT}
    if not any(copied[k] == PARENT[k] for k in PARENT):
        skip("`git worktree add` copies the parent's whole identity into the child", "this git's `worktree add` copies no `config.worktree`")
    else:
        check("`git worktree add` copies the parent's whole identity into the child — user.name, user.email, seat.session, seat.harness, the signers path",
              copied == PARENT, str(copied))

    # THE CLASS: the child overwrites every subset of the four keys in turn; the rest stay the parent's, as the copy left them
    msg, tally = base / "MSG", {}
    for n in range(len(KEYS) + 1):
        for written in itertools.combinations(KEYS, n):
            for k in KEYS:
                git(child, "config", "--worktree", k, CHILD[k] if k in written else PARENT[k])
            mine = {k: CHILD[k] if k in written else PARENT[k] for k in KEYS}
            want_report, want_rule, label = outcome(set(written))
            here, there = tool(fm, child, "--whoami"), tool(fm, parent, "--whoami")
            msg.write_text("a seat's subject\n", encoding="utf-8")
            hook = tool(fm, child, "--session-trailer", str(msg))
            rule = tool(fm, child, "--session-check")
            differ = [k for k in ORDER if k in written] if want_report else []
            lines = (reported(here[2]), reported(there[2]), reported(hook[2]))
            ok_report = (all(len(l) == 1 for l in lines) and names(lines[0][0], parent, differ, mine, PARENT) and names(lines[2][0], parent, differ, mine, PARENT)
                         and names(lines[1][0], child, differ, PARENT, mine)) if want_report else lines == ([], [], [])
            refused = rule[0] != 0 and f"names the seat builder" in rule[2]
            ok = ok_report and refused == want_rule and here[0] == 0 and there[0] == 0 and hook[0] == 0 and f"Session: {mine['seat.session']}" in msg.read_text(encoding="utf-8")
            kept = [k for k in KEYS if k not in written]
            tally.setdefault(label.split(":")[0], []).append(kept)
            check(f"the child that kept {', '.join(kept) or 'nothing'} of the parent's — {label}", ok,
                  f"report lines {lines}, the session rule {rule[0]} {rule[2].strip()[-160:]!r}")
    named = sum(len(v) for k, v in tally.items() if k.startswith("named by"))
    limits = {k: len(v) for k, v in tally.items() if "limit" in k.lower()}
    check("of the fourteen mixed identities nine are named — by the report or by the session rule — and five are named limits; the full copy is THE NAMED LIMIT",
          named == 9 and limits == {"a named limit": 5, "THE NAMED LIMIT": 1} and len(tally.get("its own", [])) == 1, f"{named} named, limits {limits}")

    # the child that kept only its harness id: the state the night met (2026-10-15) — the next checks start from it
    for k in KEYS:
        git(child, "config", "--worktree", k, CHILD[k] if k != "seat.harness" else PARENT[k])
    fm.configure(child)
    hid = PARENT["seat.harness"]

    # not known: git's exit 128 (no such folder) and 1 (no such key) read None; a worktree whose folder is gone matches nothing; a key set nowhere is said so
    gone = base / "gone"
    git(parent, "worktree", "add", "-q", "--detach", str(gone))
    shutil.rmtree(gone)
    third = base / "third"
    git(parent, "worktree", "add", "-q", "--detach", str(third))
    git(third, "config", "--worktree", "--unset", "seat.session")
    codes = (git(gone, "config", "--get", "seat.harness").returncode, git(child, "config", "--get", "no.such").returncode)
    says = reported(tool(fm, child, "--whoami")[2])
    check("a read git ends in 128 (the worktree's folder is gone) or in 1 (the key is set nowhere) is not known: it matches nothing, and a key not known is said so",
          codes == (128, 1) and fm.worktree_setting(str(gone), "seat.harness") is None and fm.worktree_setting(str(child), "no.such") is None
          and len(says) == 2 and not any(str(gone.name) in l for l in says) and any(f"{third.name} carries" in l and "seat.session not known there" in l for l in says),
          f"exits {codes}, lines {says}")

    # the reads: inside the read-only list, one `config --get seat.harness` a worktree, at most WORKTREE_READ_CAP of them, the rest said unread
    seen, real = [], subprocess.run
    def watch(*a, **k):
        seen.append([str(w) for w in a[0]] if a else [])
        return real(*a, **k)
    cap = fm.WORKTREE_READ_CAP
    subprocess.run, fm.WORKTREE_READ_CAP = watch, 2
    try:
        found, unread = fm.shared_harness(hid, str(child))
    finally:
        subprocess.run = real
    try:
        capped = fm.shared_harness_lines(hid, str(child))
    finally:
        fm.WORKTREE_READ_CAP = cap
    others = len([l for l in git(child, "worktree", "list", "--porcelain").stdout.splitlines() if l.startswith("worktree ")]) - 1
    harness_reads = [a for a in seen if a[-3:] == ["config", "--get", "seat.harness"]]
    left = f"not known for {others - 2} worktree{'' if others - 2 == 1 else 's'} past the first 2 that `git worktree list` names (`WORKTREE_READ_CAP`)"
    check(f"one run reads at most WORKTREE_READ_CAP other worktrees ({cap}), one `config --get seat.harness` each, every read on the read-only list, "
          "and names how many it left unread",
          cap == 32 and len(harness_reads) == 2 and unread == others - 2 and all(fm.read_only_git(a) for a in seen)
          and others > 2 and capped[-1].endswith(left),
          f"{len(harness_reads)} harness reads, unread {unread} of {others}, {[a for a in seen if not fm.read_only_git(a)]}, {capped[-1:]}")

    # the command line's `-c` scope names this commit's author, not another worktree's setting: it masks no difference
    os.environ.update(GIT_CONFIG_COUNT="1", GIT_CONFIG_KEY_0="user.email", GIT_CONFIG_VALUE_0="builder@seat")
    try:
        found, _ = fm.shared_harness(hid, str(child))
    finally:
        for k in ("GIT_CONFIG_COUNT", "GIT_CONFIG_KEY_0", "GIT_CONFIG_VALUE_0"):
            os.environ.pop(k, None)
    at_parent = next((d for o, d in found if os.path.realpath(o) == os.path.realpath(str(parent))), [])
    check("`git -c user.email=… commit` hands its `-c` to the hook; another worktree's setting is read without it, so it masks no difference",
          ("user.email", "planner@seat", "builder@seat") in at_parent, str(found))

    # the hook itself, installed in a scratch repository: a commit in the child is made, carries its own Session:, and the line is said
    code_hook = tool(fm, parent, "--install-hook")[0]
    c = git(child, "-c", "commit.gpgsign=false", "commit", "-q", "--allow-empty", "-m", "a seat's commit")
    body = git(child, "log", "-1", "--format=%B").stdout
    kept_harness = dict(CHILD, **{"seat.harness": hid})
    said = [l for l in reported(c.stderr) if l.startswith("--session-trailer: ") and names(l, parent, ORDER, kept_harness, PARENT)]
    check("the installed prepare-commit-msg hook says the shared harness id on a commit in the child, and the commit is made with the child's own Session:",
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
