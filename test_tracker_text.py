"""FM-046: parsed committed text and physical Git reads.

Run directly, or through test_shoalmark.py. Fixtures write bytes explicitly and use
local repositories and disposable signing keys. No released history is changed.
Optional arguments: tool path, then all/physical/guard/attribution/converted.
"""

import contextlib
import datetime
import importlib.util
import io
import os
import pathlib
import re
import shutil
import subprocess
import tempfile


HERE = pathlib.Path(__file__).resolve().parent
TODAY = datetime.date.today().isoformat()
REL = "docs/work-tracker/"
CONFIG = ('name = "text fixture"\nowner = "owner@example.invalid"\n'
          '[kinds]\nTX = "Work"\n[seats]\nreader = "reader@example.invalid"\n'
          '[rights]\nreader = []\n')
TRIAGE_TEXT = "# Triage\n\n## The intent\n\nKeep one reading.\n\n## The current path\n\nRead text.\n\n## Passes\n\nNone.\n"


def text(tid, status="In Progress", extra="", log=""):
    return (f'---\nid: {tid}\nstatus: {status}\nconsidered: none\n{extra}'
            f'hook: "one reading of {tid}"\n---\n\n# {tid} — text fixture\n\n'
            '## What is true now\n\nOne reading.\n\n## Done when\n\nIt is consistent.\n\n'
            f'## Ship log\n\n| Date | Event |\n|---|---|\n{log}')


def write(path, value, ending):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(value.replace("\n", ending).encode("utf-8"))


def command(root, *args, env=None):
    return subprocess.run(args, cwd=root, env=env, check=True, capture_output=True)


def git(root, *args):
    env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
    return command(root, "git", *args, env=env).stdout.decode("utf-8", "replace").strip()


def commit(root, subject):
    git(root, "add", "-A")
    git(root, "-c", "commit.gpgsign=false", "commit", "-qm", subject)
    return git(root, "rev-parse", "HEAD")


def init_git(root):
    root.mkdir()
    git(root, "init", "-q")
    for key, value in (("user.name", "reader"), ("user.email", "reader@example.invalid"),
                       ("core.autocrlf", "false"), ("core.safecrlf", "false")):
        git(root, "config", key, value)
    (root / ".gitattributes").write_bytes(b"* -text\n")


def stable(lines):
    return [re.sub(r"\b[0-9a-f]{7,64}\b", "COMMIT", line) for line in lines]


def git_readings(fm, root, ending):
    init_git(root)
    write(root / "shoalmark.toml", CONFIG, ending)
    write(root / REL / "TRIAGE.md", TRIAGE_TEXT, ending)
    (root / "product.py").write_bytes(b"value = 1\n")
    initial = {
        "TX-001": text("TX-001"),
        "TX-002": text("TX-002", extra="next: build\n"),
        "TX-003": text("TX-003"),
        "TX-004": text("TX-004"),
        "TX-005": text("TX-005"),
        "TX-006": text("TX-006"),
        "TX-007": text("TX-007", extra=f"triaged: {TODAY}\ntier: P1\n"),
    }
    for tid, value in initial.items():
        write(root / REL / (tid + "-x.md"), value, ending)
    before = commit(root, "the text fixtures")
    git(root, "branch", "-M", "main")
    git(root, "update-ref", "refs/remotes/origin/main", before)
    git(root, "symbolic-ref", "refs/remotes/origin/HEAD", "refs/remotes/origin/main")
    git(root, "switch", "-q", "-c", "tx/007-text")
    after_texts = {
        "TX-001": text("TX-001", "Shipped", log=f"| {TODAY} | Built in {before}. |\n"),
        "TX-002": text("TX-002", extra=f'next: owner\nask: "Read text?"\nask-kind: ruling\nask-since: {TODAY}\nask-proposal: "yes"\n'),
        "TX-003": text("TX-003", extra=f'answer: "yes"\nanswered: {TODAY}\nanswered-by: reader\n'),
        "TX-004": text("TX-004", extra="tier: P1\n"),
        "TX-005": text("TX-005", "Closed"),
    }
    for tid, value in after_texts.items():
        write(root / REL / (tid + "-x.md"), value, ending)
    write(root / REL / "TRIAGE.md", TRIAGE_TEXT.replace("Read text.", "Read committed text."), ending)
    after = commit(root, "TX-007: consistent text")
    # Check the stored bytes, independently of the worktree and platform newline handling.
    raw = command(root, "git", "show", f"{after}:{REL}TX-001-x.md").stdout
    assert raw == after_texts["TX-001"].replace("\n", ending).encode("utf-8")
    fm.configure(root)
    specs = [f"{rev}:{REL}{tid}-x.md" for rev in (before, after) for tid in initial]
    specs += [f"{after}:shoalmark.toml", f"{after}:missing"]
    types = {}
    blobs = fm.cat_blobs(specs, types=types)
    at = lambda rev, tid: blobs[f"{rev}:{REL}{tid}-x.md"]
    trackers = [fm.extract(root / REL / (tid + "-x.md")) for tid in initial]
    moves = list(fm.shipped_moves({REL + t["file"]: t for t in trackers}))
    n, guarded = fm.guard_walk(after, "^" + before)
    rights = stable(fm.rights_problems(trackers))
    asks = stable(fm.seat_problems(next(t for t in trackers if t["id"] == "TX-002")))
    parsed = [fm.extract(root / REL / (tid + "-x.md"), at(after, tid)) for tid in initial]
    answer_lint = stable([p for p in fm.lint(parsed) if "an answer counts only from a seat" in p])
    judged = fm.judge_commits([(after, before, {"product.py"}, "TX-007: build")], "tx/007-text")
    git(root, "update-ref", "refs/remotes/origin/answer/tx-003", after)
    fm.configure(root)
    travelling = fm.on_their_way(trackers)
    fm.configure(root)
    write(root / REL / "TX-007-x.md", initial["TX-007"].replace("One reading.", "A staged reading."), ending)
    git(root, "add", REL + "TX-007-x.md")
    (root / REL / "TX-007-x.md").unlink()
    fm.COMMITTING = True
    try:
        staged = fm.staged_absent({})
    finally:
        fm.COMMITTING = False
    return {
        "boundary": all("\r" not in b for b in blobs.values() if b is not None)
                    and blobs[specs[-1]] is None and all(types[s] == "blob" for s in specs[:-1]),
        "status": fm.is_shipped(at(after, "TX-001")),
        "Shipped": [(t["id"], bool(rows), len(fm.commits_named(rows))) for t, _where, rows, _judge in moves],
        "answer": fm.transitions(at(before, "TX-003"), at(after, "TX-003")),
        "ask": fm.transitions(at(before, "TX-002"), at(after, "TX-002")),
        "triage": fm.transitions(at(before, "TX-004"), at(after, "TX-004")),
        "close": fm.transitions(at(before, "TX-005"), at(after, "TX-005")),
        "rights verdicts": (rights, asks),
        "guard": (n, [row[3] for row in guarded]),
        "index": fm.render(parsed, "Work"),
        "answer gate": answer_lint,
        "judgement": judged,
        "answer branches": {tid: (r["kind"], r["answered"]) for tid, r in travelling.items()},
        "staged trackers": [(t["id"], t["status"], t.get("triaged")) for t in staged.values()],
    }


def svn_readings(fm, base, ending):
    command(base, "svnadmin", "create", str(base / "repository"))
    root = base / "wc"
    command(base, "svn", "checkout", "-q", (base / "repository").as_uri(), str(root))
    config = CONFIG.replace("owner@example.invalid", "owner").replace("reader@example.invalid", "reader")
    write(root / "shoalmark.toml", config, ending)
    write(root / REL / "TRIAGE.md", TRIAGE_TEXT, ending)
    (root / "product.py").write_bytes(b"value = 1\n")
    for tid in range(1, 7):
        write(root / REL / f"TX-00{tid}-x.md", text(f"TX-00{tid}"), ending)
    command(root, "svn", "add", "--force", ".")
    command(root, "svn", "commit", "-qm", "the text fixtures", "--username", "owner")
    command(root, "svn", "update", "-q")
    values = {
        "TX-001": text("TX-001", "Shipped", log=f"| {TODAY} | Built in r1. |\n"),
        "TX-002": text("TX-002", extra=f'next: owner\nask: "Read text?"\nask-kind: ruling\nask-since: {TODAY}\nask-proposal: "yes"\n'),
        "TX-003": text("TX-003", extra=f'answer: "yes"\nanswered: {TODAY}\nanswered-by: reader\n'),
        "TX-004": text("TX-004", extra="tier: P1\n"),
        "TX-005": text("TX-005", "Closed"),
    }
    for tid, value in values.items():
        write(root / REL / (tid + "-x.md"), value, ending)
    write(root / REL / "TRIAGE.md", TRIAGE_TEXT.replace("Read text.", "Read committed text."), ending)
    command(root, "svn", "commit", "-qm", "consistent text", "--username", "reader")
    command(root, "svn", "update", "-q")
    raw = command(root, "svn", "cat", "-r", "2", REL + "TX-001-x.md").stdout
    assert raw == values["TX-001"].replace("\n", ending).encode("utf-8")
    fm.configure(root)
    before = {tid: fm.svn_run("cat", "-r", "1", REL + tid + "-x.md") for tid in values}
    after = {tid: fm.svn_run("cat", "-r", "2", REL + tid + "-x.md") for tid in values}
    trackers = [fm.extract(root / REL / (tid + "-x.md")) for tid in values]
    moves = list(fm.shipped_moves({REL + t["file"]: t for t in trackers}))
    parsed = [fm.extract(root / REL / (tid + "-x.md"), value) for tid, value in after.items()]
    lint = fm.lint(parsed)
    return {
        "boundary": all("\r" not in value for value in (*before.values(), *after.values())),
        "status": fm.is_shipped(after["TX-001"]),
        "Shipped": [(t["id"], bool(rows), len(fm.commits_named(rows))) for t, _where, rows, _judge in moves],
        **{right: fm.transitions(before[tid], after[tid]) for right, tid in
           (("answer", "TX-003"), ("ask", "TX-002"), ("triage", "TX-004"), ("close", "TX-005"))},
        "rights verdicts": (fm.rights_problems(trackers), fm.seat_problems(trackers[1])),
        "guard": (fm.guarded_sections(fm.svn_run("cat", "-r", "2", REL + "TRIAGE.md"), fm.HEAD), fm.triage_guard()[1]),
        "index": fm.render(parsed, "Work"),
        "answer gate": [p for p in lint if "an answer counts only from a seat" in p],
    }


def signature_reading(fm, root, ending):
    init_git(root)
    config = CONFIG.replace('owner = "owner@example.invalid"', 'owner = "owner@example.invalid signed"')
    write(root / "shoalmark.toml", config, ending)
    write(root / REL / "TX-001-x.md", text("TX-001"), ending)
    key = root / "disposable-key"
    command(root, "ssh-keygen", "-q", "-t", "ed25519", "-N", "", "-f", str(key))
    public = key.with_suffix(".pub").read_text(encoding="utf-8").strip()
    write(root / REL / "allowed_signers", "owner@example.invalid " + public + "\n", ending)
    (root / ".gitignore").write_bytes(b"disposable-key*\n")
    before = commit(root, "the trusted signing page")
    git(root, "branch", "-M", "main")
    git(root, "update-ref", "refs/remotes/origin/main", before)
    git(root, "symbolic-ref", "refs/remotes/origin/HEAD", "refs/remotes/origin/main")
    git(root, "switch", "-q", "-c", "answer/tx-001")
    for k, v in (("user.name", "owner"), ("user.email", "owner@example.invalid"),
                 ("gpg.format", "ssh"), ("user.signingkey", str(key)),
                 ("gpg.ssh.allowedSignersFile", REL + "allowed_signers")):
        git(root, "config", k, v)
    write(root / REL / "TX-001-x.md", text("TX-001", extra=f'answer: "yes"\nanswered: {TODAY}\nanswered-by: owner\n'), ending)
    git(root, "add", "-A")
    git(root, "commit", "-qS", "-m", "TX-001: answer")
    fm.configure(root)
    sha = git(root, "rev-parse", "HEAD")
    trusted = fm.trusted_signers()
    return (fm.verified_as(sha, "owner@example.invalid"),
            pathlib.Path(trusted["file"]).read_bytes() == command(root, "git", "show", f"{before}:{REL}allowed_signers").stdout)


def tool_run(fm, root, *args):
    out, err = io.StringIO(), io.StringIO()
    with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
        code = fm.main(["--root", str(root), *args])
    return code, out.getvalue(), err.getvalue()


def signed_fixture(fm, root):
    """A signed Owner, two signing rows, a tracker and the Owner's two sections."""
    init_git(root)
    write(root / "shoalmark.toml", CONFIG.replace('owner@example.invalid"', 'owner@example.invalid signed"'), "\n")
    (root / ".gitignore").write_bytes(b"disposable-key*\ndocs/work-tracker/INDEX.md\ndocs/work-tracker/index.html\ndocs/work-tracker/view/\n")
    keys = []
    for who in ("reader", "owner"):
        key = root / ("disposable-key-" + who)
        command(root, "ssh-keygen", "-q", "-t", "ed25519", "-N", "", "-f", str(key))
        keys.append((who, key, key.with_suffix(".pub").read_text().strip()))
    write(root / REL / "allowed_signers", "".join(who + "@example.invalid " + public + "\n" for who, _, public in keys), "\n")
    write(root / REL / "TRIAGE.md", TRIAGE_TEXT, "\n")
    asked = text("TX-001", extra=f'next: owner\nask: "Read text?"\nask-kind: ruling\nask-since: {TODAY}\nask-proposal: "yes"\n')
    write(root / REL / "TX-001-x.md", asked, "\n")
    for k, v in (("user.name", "owner"), ("user.email", "owner@example.invalid"),
                 ("gpg.format", "ssh"), ("user.signingkey", str(keys[1][1])),
                 ("gpg.ssh.allowedSignersFile", REL + "allowed_signers")):
        git(root, "config", k, v)
    tool_run(fm, root)
    git(root, "add", "-A")
    git(root, "commit", "-qS", "-m", "the signed text fixtures")
    before = git(root, "rev-parse", "HEAD")
    git(root, "branch", "-M", "main")
    git(root, "update-ref", "refs/remotes/origin/main", before)
    git(root, "symbolic-ref", "refs/remotes/origin/HEAD", "refs/remotes/origin/main")
    tool_run(fm, root)
    assert tool_run(fm, root, "--check")[0] == 0
    assert command(root, "git", "verify-commit", before).returncode == 0
    return before, asked


def physical_checks(fm, base, check, group="physical"):
    for target in (() if group == "attribution" else ("signers", "intent", "path")):
        for name, ending in (("CRLF", "\r\n"), ("CR", "\r")):
            root = base / (target + "-" + name)
            before, _ = signed_fixture(fm, root)
            git(root, "switch", "-q", "-c", "tx/001-text")
            git(root, "config", "user.name", "reader")
            git(root, "config", "user.email", "reader@example.invalid")
            if target == "signers":
                p = root / REL / "allowed_signers"
                p.write_bytes(p.read_bytes().replace(b"\n", ending.encode()))
            else:
                p = root / REL / "TRIAGE.md"
                section = {"intent": "## The intent\n\nKeep one reading.\n\n", "path": "## The current path\n\nRead text.\n\n"}[target]
                p.write_bytes(TRIAGE_TEXT.replace(section, section.replace("\n", ending)).encode())
            commit(root, "TX-001: text separators")
            direct = subprocess.run(["git", "verify-commit", before], cwd=root, capture_output=True).returncode
            tool_run(fm, root)
            gate = tool_run(fm, root, "--check")
            check(f"Git {target} LF to {name} signed-history gate", gate[0] == fm.EXIT_LINT and bool(fm.triage_guard()[0]) and direct == (1 if target == "signers" and name == "CR" else 0),
                  f"--check={gate[0]}; git verify-commit={direct}")
    for name, ending in (() if group == "guard" else (("LF", "\n"), ("CRLF", "\r\n"), ("CR", "\r"))):
        root = base / ("owner-" + name)
        _, asked = signed_fixture(fm, root)
        git(root, "switch", "-q", "-c", "answer/tx-001")
        value = asked.replace('hook:', f'answer: "accepted"\nanswered: {TODAY}\nanswered-by: owner\nhook:', 1)
        write(root / REL / "TX-001-x.md", value, ending)
        tool_run(fm, root)
        git(root, "add", "-A")
        git(root, "commit", "-qS", "-m", "TX-001: answer")
        sha = git(root, "rev-parse", "HEAD")
        tool_run(fm, root)
        gate = tool_run(fm, root, "--check")
        author = fm.line_author(root / REL / "TX-001-x.md", "answer")
        check(f"Git Owner-signed {name} tracker attribution and gate", gate[0] == 0 and author == ("owner", "owner@example.invalid", "git", sha) and fm.verified_as(sha, "owner@example.invalid"),
              f"--check={gate[0]}; author={author}")


def converted_readings(fm, root, ending, missing=False):
    """Committed answer, refusal record and unmerged act; absent snapshots use the same paths."""
    init_git(root)
    write(root / "shoalmark.toml", CONFIG, "\n")
    absent = commit(root, "the configured repository")
    p, rel = root / REL / "TX-001-x.md", REL + "TX-001-x.md"
    plain = text("TX-001")
    answered = text("TX-001", extra=f'next: owner\nask: "Read text?"\nask-kind: action\nask-since: {TODAY}\nask-proposal: "yes"\nanswer: "accepted"\nanswered: {TODAY}\nanswered-by: reader\n')
    if not missing:
        write(p, plain, ending)
    before = absent if missing else commit(root, "the text fixture")
    git(root, "branch", "-M", "main")
    git(root, "update-ref", "refs/remotes/origin/main", before)
    git(root, "symbolic-ref", "refs/remotes/origin/HEAD", "refs/remotes/origin/main")
    git(root, "switch", "-q", "-c", "answer/tx-001")
    if not missing:
        write(p, answered, ending)
    (root / "answer-note").write_bytes(b"answer fixture\n")
    answer = commit(root, "TX-001: answer")
    if not missing:
        record = answered.replace("## Ship log", f"## Acts\n\n**{TODAY} 12:00** · --done refused — fixture\n\n## Ship log")
        write(p, record, ending)
    (root / "record-note").write_bytes(b"record fixture\n")
    after = commit(root, "TX-001: record")
    fm.configure(root)
    t = fm.extract(p, plain)
    t.update(asks_answers=[("Read text?", "accepted")], asks_key=("Read text?", "accepted"))
    fm.recover_relations([t])
    recovered = t["asks_recovered"]
    values = {"recover_from_log": (recovered[0] == fm.RELATION_TEXT["unknown"] and recovered[1] == "") if missing else (recovered[0] == fm.RELATION_TEXT["proposal"] and answer.startswith(recovered[1]) and bool(recovered[1])),
              "refusal_record_in_place": fm.refusal_record_in_place(answer, after, rel) is (not missing)}
    g = lambda *a: subprocess.run(["git", *a], cwd=root, capture_output=True, text=True, encoding="utf-8", env=fm.nested_git_env())
    advice = fm.unmerged_advice(g, "answer/tx-001", "refs/remotes/origin/main", rel, "TX-001", dict(flag="--done", again="shoalmark --done TX-001 result"), "reader", "reader@example.invalid")
    values["unmerged_advice"] = ("merge it first" in advice if missing else "act is open there" in advice) and "git branch -D" not in advice
    git(root, "switch", "-q", "main")
    git(root, "reset", "--hard", "-q", after)
    # The working answer differs from the committed one, or is a new file.
    write(p, answered.replace('answer: "accepted"', 'answer: "rejected - fixture"'), ending)
    dirty = fm.dirty_refusal(g, [rel])
    values["dirty_refusal"] = "failed half-way" in dirty and "--answer TX-001 reject" in dirty and (("--supersede" in dirty) is (not missing))
    # HEAD and committed merge-parent snapshots supply the old answer.
    git(root, "reset", "--hard", "-q", after)
    write(p, plain, ending)
    git(root, "add", rel)
    fm.configure(root)
    fm.COMMITTING = True
    current = fm.extract(p)
    values["record_problems HEAD"] = bool(fm.record_problems(current)) is (not missing)
    merge_file = root / git(root, "rev-parse", "--git-path", "MERGE_HEAD")
    merge_file.write_text(answer + "\n")
    fm.configure(root); fm.COMMITTING = True
    values["record_problems merge parents"] = bool(fm.record_problems(current)) is (not missing)
    merge_file.write_text(before + "\n")
    fm.configure(root); fm.COMMITTING = True
    values["record_problems parent without answer"] = fm.record_problems(current) == []
    merge_file.write_text(absent + "\n")
    fm.configure(root); fm.COMMITTING = True
    values["record_problems missing merge-parent file"] = fm.record_problems(current) == []
    merge_file.unlink()
    fm.COMMITTING = False
    git(root, "reset", "--hard", "-q", before)
    # Read the unmerged branch, capturing the command before its downstream write.
    fm.configure(root)
    current = fm.extract(p, plain)
    out = io.StringIO()
    with contextlib.redirect_stderr(out):
        result = fm.done_cmd(["TX-001", "result"], [current])
    values["done_cmd"] = result == fm.EXIT_LINT and ("owes the Owner no act" in out.getvalue() if missing else "act is on `answer/tx-001`" in out.getvalue())
    old_answer, old_change = fm.answer_cmd, fm.owner_change
    calls = []
    fm.answer_cmd = lambda words, trackers, **kw: calls.append((words, trackers[0]["answer"], kw.get("onto"))) or 0
    fm.owner_change = lambda *a, **kw: calls.append("owner_change") or 0
    try:
        with contextlib.redirect_stderr(io.StringIO()):
            result = fm.revoke_cmd(["TX-001", "fixture"], [current])
    finally:
        fm.answer_cmd, fm.owner_change = old_answer, old_change
    values["revoke_cmd"] = (result == fm.EXIT_LINT and calls == []) if missing else (result == 0 and calls == [(["TX-001", "revoke", "fixture"], "accepted", "refs/heads/answer/tx-001")])
    return values


def converted_checks(fm, base, check):
    readings = [converted_readings(fm, base / name, ending, missing) for name, ending, missing in
                (("reads-lf", "\n", False), ("reads-crlf", "\r\n", False), ("reads-missing", "\n", True))]
    for consumer in readings[0]:
        check(f"Git {consumer} committed LF, CRLF and missing snapshots", all(r[consumer] for r in readings),
              "LF/CRLF/missing=" + "/".join(str(r[consumer]) for r in readings))
    source = base / "reads-lf"
    git(source, "config", "uploadpack.allowFilter", "true")
    for filt in ("blob:none", "tree:0"):
        root = base / ("partial-" + filt.replace(":", "-"))
        git(base, "clone", "-q", "--no-checkout", "--filter=" + filt, source.as_uri(), str(root))
        git(root, "branch", "answer/tx-001", "origin/answer/tx-001")
        write(root / "shoalmark.toml", CONFIG, "\n")
        p, rel = root / REL / "TX-001-x.md", REL + "TX-001-x.md"
        write(p, text("TX-001", extra='answer: "accepted"\n'), "\n")
        fm.configure(root)
        fm.lazy_fetch_off()
        problem = fm.lazy_fetch_problem()
        if problem:
            check("Git " + filt + " filtered-clone reads", False, problem)
            continue
        sha = git(root, "rev-parse", "answer/tx-001")
        packs = {f.name: f.read_bytes() for f in (root / ".git/objects/pack").iterdir()}
        t = fm.extract(p)
        t.update(asks_answers=[("Read text?", "accepted")], asks_key=("Read text?", "accepted"))
        fm.recover_relations([t])
        check("Git " + filt + " unavailable answer history", t["asks_recovered"] == (fm.RELATION_TEXT["unknown"], "") and bool(fm.BOARD_UNREAD))
        try:
            fm.refusal_record_in_place(sha + "^", sha, rel)
        except fm.Unread:
            unread = True
        else:
            unread = False
        check("Git " + filt + " unavailable refusal-record snapshot", unread)
        check("Git " + filt + " unavailable physical tracker lines", fm.line_author(p, "answer") == (None, None, "unread", ""))
        check("Git " + filt + " reads retain the filtered object store", packs == {f.name: f.read_bytes() for f in (root / ".git/objects/pack").iterdir()})


def run_checks(fm, group="all", *, results=None):
    if group not in ("all", "physical", "guard", "attribution", "converted"):
        raise ValueError("unknown committed-text control group: " + group)
    results = [] if results is None else results
    def check(label, ok, detail=""):
        results.append(("FM-046 · " + label, bool(ok), detail))
    saved = fm.ROOT
    try:
        with tempfile.TemporaryDirectory() as tmp:
            base = pathlib.Path(tmp).resolve()
            if group in ("all", "physical", "guard", "attribution"):
                physical_checks(fm, base, check, group)
            if group in ("all", "converted"):
                converted_checks(fm, base, check)
            if group != "all":
                return results
            lf = git_readings(fm, base / "lf", "\n")
            crlf = git_readings(fm, base / "crlf", "\r\n")
            expected = {"boundary": True, "status": True, "Shipped": [("TX-001", True, 1)],
                        **{r: {r} for r in ("answer", "ask", "triage", "close")},
                        "judgement": [], "answer branches": {"TX-003": ("answer", True)}}
            for rule in lf:
                ok = lf[rule] == crlf[rule] and (rule not in expected or lf[rule] == expected[rule])
                if rule == "guard":
                    ok = ok and lf[rule][0] == 1 and len(lf[rule][1]) == 1 and lf[rule][1][0][0][0] == "path"
                elif rule == "answer gate":
                    ok = ok and len(lf[rule]) == 1
                elif rule == "rights verdicts":
                    ok = ok and all(f"`{r}`" in "\n".join(lf[rule][0]) for r in ("answer", "triage", "close")) and bool(lf[rule][1])
                elif rule == "staged trackers":
                    ok = ok and ("TX-007", "In Progress", TODAY) in lf[rule]
                check("Git " + rule + " reads LF and committed CRLF identically", ok)
            for ending, name in (("\n", "LF"), ("\r\n", "CRLF"), ("\r", "CR")):
                check("Git " + name + " configuration and trusted signers verify an SSH signature",
                      signature_reading(fm, base / ("signed-" + name), ending) == (True, True))
            if not (shutil.which("svn") and shutil.which("svnadmin")):
                results.append(("SKIP FM-046 · Subversion committed text", None, "svn and svnadmin are required; unavailable on this host"))
            else:
                (base / "svn-lf").mkdir(); (base / "svn-crlf").mkdir()
                try:
                    slf = svn_readings(fm, base / "svn-lf", "\n")
                    scrlf = svn_readings(fm, base / "svn-crlf", "\r\n")
                except fm.SvnUnreadable as error:      # an unreadable answer is this block's FAIL line, never a traceback that ends the suite (#182)
                    check("Subversion committed text is read, LF and CRLF", False, f"svn said: {error}")
                    slf = scrlf = {}
                for rule in slf:
                    ok = slf[rule] == scrlf[rule] and (rule not in expected or slf[rule] == expected[rule])
                    if rule == "guard":
                        ok = ok and "Read committed text." in slf[rule][0]["path"] and slf[rule][1] == fm.GUARD_SVN
                    elif rule == "answer gate":
                        ok = ok and len(slf[rule]) == 1
                    elif rule == "rights verdicts":
                        ok = ok and all(f"`{r}`" in "\n".join(slf[rule][0]) for r in ("answer", "triage", "close")) and bool(slf[rule][1])
                    check("Subversion " + rule + " reads LF and committed CRLF identically", ok)
    finally:
        fm.configure(saved)
    return results


if __name__ == "__main__":
    import sys
    spec = importlib.util.spec_from_file_location("tracker_tool", sys.argv[1] if len(sys.argv) > 1 else HERE / "shoalmark.py")
    fm = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(fm)
    fm.HERE, fm.MARKED = HERE, HERE / "vendor/marked-18.0.13.umd.js"
    fm.__version__ = (HERE / "VERSION").read_text().strip()
    results = run_checks(fm, sys.argv[2] if len(sys.argv) > 2 else "all")
    for label, ok, detail in results:
        print(("  skip  " if ok is None else "  ok    " if ok else "  FAIL  ") + label + (" — " + detail if detail else ""))
    print(f"{sum(ok is True for _, ok, _ in results)} passed; {sum(ok is False for _, ok, _ in results)} failed; {sum(ok is None for _, ok, _ in results)} skipped")
    sys.exit(any(ok is False for _, ok, _ in results))
