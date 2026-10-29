"""The ask ids' class test: an ask's own id, and the answer that names it — every way an id could be reused or mismatched, across two
branches included.

Each row builds its history in a scratch repository — a bare `origin` with `main` as its default branch, the Owner's SSH key in the
default branch's signers file, a seat's identity — runs the tool in this process, and states its verdict: refused, with the refusal's
words, or accepted. Each mutant patches one function of the imported module and must turn at least one row red.

Run: `python3 test_ask_ids.py` — exit 1 on a failure. test_shoalmark.py runs it as it runs test_owner_exemption.py. No browser and no
network: every repository is a scratch one, `origin` a bare one beside it.
"""
import contextlib
import datetime
import inspect
import io
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import textwrap

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))
import shoalmark as fm  # noqa: E402

OWNER = ("Owner", "owner@example.invalid")
SEAT = ("Seat", "seat@example.invalid")
REL = "docs/work-tracker"
TODAY = datetime.date.today().isoformat()
SINCE = (datetime.date.today() - datetime.timedelta(days=2)).isoformat()
CONFIG = f'name = "ids"\nowner = "{OWNER[1]} signed"\n[kinds]\nFM = "Work"\n[seats]\nplanner = "{SEAT[1]}"\n'
ENV = {k: v for k, v in os.environ.items() if not k.startswith(("GIT_", "SSH_", "SHOALMARK_"))}
ENV.update(GIT_CONFIG_GLOBAL=os.devnull, GIT_CONFIG_NOSYSTEM="1", GIT_TERMINAL_PROMPT="0", SHOALMARK_CMD="shoalmark")


def git(cwd, *a, who=SEAT, check=True, sign=None):
    """git in `cwd` as `who`, the hooks off; `sign`: the key a commit is signed with."""
    env = dict(ENV, GIT_AUTHOR_NAME=who[0], GIT_AUTHOR_EMAIL=who[1], GIT_COMMITTER_NAME=who[0], GIT_COMMITTER_EMAIL=who[1])
    head = ["git", "-C", str(cwd), "-c", "core.hooksPath=/dev/null", "-c", "commit.gpgsign=false"]
    if sign:
        head += ["-c", "gpg.format=ssh", "-c", f"user.signingkey={sign}"]
    r = subprocess.run(head + list(a), capture_output=True, text=True, encoding="utf-8", errors="replace", env=env)
    if check and r.returncode:
        raise subprocess.CalledProcessError(r.returncode, head + list(a), r.stdout, r.stderr)
    return r.stdout


def run(root, *argv, who=OWNER):
    """The tool in this process, as `who` would run it in `root`: (exit, stdout, stderr)."""
    out, err = io.StringIO(), io.StringIO()
    saved = {k: os.environ.pop(k) for k in [k for k in os.environ if k.startswith("GIT_")]}
    mine = dict(GIT_AUTHOR_NAME=who[0], GIT_AUTHOR_EMAIL=who[1], GIT_COMMITTER_NAME=who[0], GIT_COMMITTER_EMAIL=who[1],
                GIT_CONFIG_GLOBAL=os.devnull, GIT_CONFIG_NOSYSTEM="1", GIT_TERMINAL_PROMPT="0")
    os.environ.update(mine)
    try:
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            try:
                code = fm.main(["--root", str(root), *argv])
            except SystemExit as e:
                code = e.code if isinstance(e.code, int) else 0 if e.code is None else 1
                if not isinstance(e.code, int) and e.code is not None:
                    print(e.code, file=err)
    finally:
        for k in mine:
            os.environ.pop(k, None)
        os.environ.update(saved)
        fm.configure(HERE)
    return code, out.getvalue(), err.getvalue()


def text(tid, front="", body="", asks=""):
    """A tracker's text: its front matter with `front` inside it, a body, and `asks`, the records under `## Asks`."""
    return (f'---\nid: {tid}\nstatus: In Progress\nconsidered: none\n{front}hook: "h of {tid}"\n---\n\n# {tid} — t\n\n'
            f"## What is true now\n\nOne thing is left.\n{body}\n## Done when\n\nit is.\n" + (f"\n## Asks\n\n{asks}" if asks else ""))


def ask(q="Ship it?", proposal="yes", kind="ruling", options="", aid="", since=SINCE, move="owner"):
    """The front-matter lines of a put ask — its id first where it has one."""
    return ((f"ask-id: {aid}\n" if aid else "") + f'next: {move}\nask: "{q}"\nask-kind: {kind}\nask-since: {since}\nask-proposal: "{proposal}"\n'
            + (f'ask-options: "{options}"\n' if options else ""))


def record(aid, q, answer=None, by=OWNER[0], sha="0000000", day=SINCE):
    """A record under `## Asks` as `--clear-ask` writes one: answered, or withdrawn; with no `aid`, an ask before ask ids."""
    head = f"**{aid}** · {day} · {q}\n" if aid else f"**{day}** · {q}\n"
    if answer is None:
        return head + "**withdrawn** — no answer was given\n"
    return head + f"**answered** — {answer} · {by}\n**relation** — accepted the proposal\n**signed** — {sha} · G\n"


def answered(text_, answer="accepted", by=OWNER[0], move="build"):
    """`text_` with the three answer lines written under its ask's lines and its move set, as `--answer` writes them."""
    lines = text_.split("\n")
    at = next(i for i, l in enumerate(lines) if l.startswith("ask:"))
    while lines[at + 1].startswith("ask-"):
        at += 1
    lines[at + 1:at + 1] = [f'answer: "{answer}"', f"answered: {TODAY}", f"answered-by: {by}"]
    return "\n".join(lines).replace("next: owner", f"next: {move}", 1)


class Repo:
    """A scratch clone of a bare `origin` whose `main` is the default branch: the configuration naming the Owner `signed` and a planner
    seat, the Owner's key in the signers file on `main`, and the trackers given, committed by the Owner, signed, and pushed. The clone's
    own identity is the Owner's, with their key, as the Owner's checkout is; a seat's commits are made with its identity, unsigned."""

    def __init__(self, base, trackers=None, vcs="git"):
        self.base, self.root, self.origin = base, base / "wc", base / "origin.git"
        self.root.mkdir(parents=True)
        self.keys = {}
        for name in ("owner", "other"):
            key = base / f"key-{name}"
            subprocess.run(["ssh-keygen", "-q", "-t", "ed25519", "-N", "", "-f", str(key), "-C", name], check=True, capture_output=True)
            self.keys[name] = key
        (self.root / "shoalmark.toml").write_text(CONFIG if vcs == "git" else 'name = "ids"\n[kinds]\nFM = "Work"\n', encoding="utf-8")
        if vcs != "git":
            for tid, body in (trackers or {}).items():
                write(self.root, tid, body)
            return
        git(base, "init", "-q", "--bare", "--initial-branch=main", str(self.origin))
        git(self.root, "init", "-q", "--initial-branch=main")
        for k, v in (("user.name", OWNER[0]), ("user.email", OWNER[1]), ("gpg.format", "ssh"), ("user.signingkey", str(self.keys["owner"])),
                     ("gpg.ssh.allowedSignersFile", f"{REL}/allowed_signers"), ("commit.gpgsign", "false")):
            git(self.root, "config", k, v)
        git(self.root, "remote", "add", "origin", str(self.origin))
        (self.root / ".gitignore").write_text(f"{REL}/index.html\n{REL}/view/\n", encoding="utf-8")
        self.signers(f"{OWNER[1]} " + self.keys["owner"].with_suffix(".pub").read_text(encoding="utf-8"))
        for tid, body in (trackers or {}).items():
            write(self.root, tid, body)
        self.commit("the start", who=OWNER, sign=True)
        git(self.root, "push", "-q", "-u", "origin", "main")
        git(self.root, "remote", "set-head", "origin", "main")
        run(self.root, "--print-written")                         # INDEX.md as it reads once `origin/main` is there
        if git(self.root, "status", "--porcelain"):
            self.commit("the index, with the default branch known", who=OWNER, sign=True)
            git(self.root, "push", "-q", "origin", "main")

    def signers(self, line):
        p = self.root / REL / "allowed_signers"
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(line, encoding="utf-8")

    def write(self, tid, body):
        """A tracker written, and INDEX.md as the tool writes it."""
        p = write(self.root, tid, body)
        run(self.root, "--print-written")
        return p

    def read(self, tid):
        return (self.root / REL / f"{tid}-x.md").read_text(encoding="utf-8")

    def commit(self, message, who=SEAT, sign=False, trailers=()):
        """Everything staged and committed by `who` — signed with the Owner's key where `sign` — with `trailers` as message lines."""
        run(self.root, "--print-written", who=who)
        git(self.root, "add", "-A")
        extra = [x for t in trailers for x in ("-m", t)]
        git(self.root, "commit", "-q", "--allow-empty", "-m", message, *extra, *(["-S"] if sign else []), who=who, sign=self.keys["owner"] if sign else None)
        return git(self.root, "rev-parse", "HEAD").strip()

    def check(self, who=SEAT):
        return run(self.root, "--check", who=who)

    def head(self, ref="HEAD"):
        return git(self.root, "rev-parse", ref).strip()

    def switch(self, *a):
        git(self.root, "switch", "-q", *a)

    def land(self, branch):
        """`branch` merged into `main` by a merge commit a seat makes, `main` pushed, and `origin/main` fetched back."""
        self.switch("main")
        git(self.root, "merge", "-q", "--no-ff", "--no-edit", branch)
        git(self.root, "push", "-q", "origin", "main")
        git(self.root, "fetch", "-q", "origin")

    def queue(self, branch):
        """`--queue`'s reading of one pull request — `branch` onto `main` — with its head and base as this clone holds them: (its action,
        and what the reading of the ids it proposes says alone — where git's own conflict on the front matter is the queue's reading, that
        reading is still asked)."""
        git(self.root, "push", "-q", "-f", "origin", f"{branch}:refs/heads/{branch}")
        git(self.root, "fetch", "-q", "origin")
        fm.configure(self.root)
        try:
            pr = {"number": 7, "title": branch, "headRefName": branch, "headRefOid": self.head(branch), "baseRefName": "main",
                  "mergeable": "MERGEABLE", "createdAt": "2026-10-01T00:00:00Z", "isCrossRepository": False}
            with contextlib.redirect_stderr(io.StringIO()):
                rows = fm.queue_actions([pr])
                alone = fm.proposed_id_reading(pr["headRefOid"], "refs/remotes/origin/main")
            return rows[0][2], (alone[0] if alone else "")
        finally:
            fm.configure(HERE)


def write(root, tid, body):
    p = root / REL / f"{tid}-x.md"
    p.parent.mkdir(parents=True, exist_ok=True)
    with open(p, "w", encoding="utf-8", newline="\n") as f:
        f.write(body)
    return p


def refused(said, *words):
    """The run refused (exit 4), and its stderr carries every one of `words`."""
    code, _out, err = said
    return code == fm.EXIT_LINT and all(w in err for w in words)


def accepted(said, *absent):
    """The run passed (exit 0), and its stderr carries none of `absent`."""
    code, _out, err = said
    return code == 0 and not any(w in err for w in absent)


def seen(said):
    code, out, err = said
    return f"exit {code}: " + " | ".join(l.strip() for l in (err + out).splitlines() if l.strip() and ("FM-0" in l or "refused" in l or "note" in l or "STALE" in l))[:700]


# --- the form of an id, read from the file ----------------------------------------------------------------------------------------

def rows_form(area, add):
    cases = (
        ("an id naming another tracker", ask(aid="FM-002-Q1"), "`ask-id: FM-002-Q1` is not an id of FM-001's"),
        ("`Q0`", ask(aid="FM-001-Q0"), "`ask-id: FM-001-Q0` is not an id of FM-001's"),
        ("a leading zero", ask(aid="FM-001-Q01"), "`ask-id: FM-001-Q01` is not an id of FM-001's"),
        ("a capitalised key", ask().replace("next: owner", "Ask-Id: FM-001-Q1\nnext: owner"), "spelled `Ask-Id:`"),
        ("two `ask-id:` lines", "ask-id: FM-001-Q1\n" + ask(aid="FM-001-Q1"), "the front matter carries `ask-id:` on lines"),
        ("an id with no question", "ask-id: FM-001-Q1\nnext: build\n", "`ask-id: FM-001-Q1` stands with no `ask:`"),
    )
    for n, (what, front, words) in enumerate(cases):
        r = Repo(area / f"form-{n}", {"FM-001": text("FM-001")})
        r.write("FM-001", text("FM-001", front))
        said = r.check()
        add(f"F1–F2 · {what}: refused, naming it", refused(said, words), seen(said))
    r = Repo(area / "form-ok", {"FM-001": text("FM-001")})
    r.write("FM-001", text("FM-001", ask(aid="FM-001-Q1")))
    r.commit("FM-001: the ask, put as FM-001-Q1")
    said = r.check()
    add("F1 · an id in its form, `FM-001-Q1` on FM-001, beside its question, put by the seat that asks: accepted", accepted(said, "ask-id"), seen(said))


def rows_records(area, add):
    r = Repo(area / "f3-open", {"FM-001": text("FM-001")})
    r.write("FM-001", text("FM-001", ask(aid="FM-001-Q1"), asks=record("FM-001-Q1", "Ship it?", "accepted")))
    said = r.check()
    add("F3 · the open ask's id is also a record's: refused, naming the record and the next number",
        refused(said, "`ask-id: FM-001-Q1` is also the id of the record of", "put this ask as FM-001-Q2"), seen(said))
    both = record("FM-001-Q2", "Ship it?", "accepted") + "\n" + record("FM-001-Q2", "Ship the other?", "accepted", day=TODAY)
    r = Repo(area / "f3-new", {"FM-001": text("FM-001")})
    r.switch("-c", "b")
    r.write("FM-001", text("FM-001", asks=both))
    r.commit("two records with one id, on a branch")
    said = r.check()
    add("F3 · two records that carry one id, new on the branch — the default branch holds neither: refused, naming both and the next number",
        refused(said, "two records under `## Asks` carry FM-001-Q2", f"FM-001-Q2 of {SINCE} and FM-001-Q2 of {TODAY}", "FM-001-Q3"), seen(said))
    r = Repo(area / "f3-landed", {"FM-001": text("FM-001", asks=both)})
    said = r.check()
    add("F3 · two records that carry one id, both landed on the default branch: a note naming both by their dates, and the next number above both — not a refusal",
        accepted(said, "refused") and "note: FM-001: two records under `## Asks` carry FM-001-Q2" in said[2] and "the next ask is FM-001-Q3" in said[2], seen(said))


ROWS = (rows_form, rows_records)


# --- the mutants ------------------------------------------------------------------------------------------------------------------

MUTANTS = ()


@contextlib.contextmanager
def mutated(name, old, new):
    """`fm.<name>` replaced by a patched copy of its own source, compiled in the module's namespace — and put back after."""
    real = getattr(fm, name)
    src = textwrap.dedent(inspect.getsource(real))
    if src.count(old) != 1:
        raise AssertionError(f"{name}: {old[:60]!r} is not in its source exactly once")
    exec(compile(src.replace(old, new), fm.__file__, "exec"), fm.__dict__)     # the module's own namespace: the configuration it reads is the live one
    try:
        yield
    finally:
        setattr(fm, name, real)


def run_mutants(*, results=None):
    """Each mutant, as (label, whether it turned a row red, what it saw): its rows run under it, and at least one must fail."""
    results = [] if results is None else results
    for label, name, old, new, rows in MUTANTS:
        reds, broke = [], ""
        try:
            with mutated(name, old, new), tempfile.TemporaryDirectory(prefix="shoalmark-ask-ids-m-") as tmp:
                area = Path(tmp).resolve()
                for n, rows_ in enumerate(rows):
                    rows_(area / f"m{n}", lambda l, ok, saw="": reds.append(l) if not ok else None)
        except AssertionError as e:
            broke = str(e)
        except Exception as e:                                        # a mutant that crashes a row turned it red
            reds.append(f"a row crashed: {type(e).__name__}: {str(e)[:120]}")
        finally:
            fm.configure(HERE)
        results.append((f"mutant · {label}: at least one row turns red", bool(reds) and not broke, broke or "no row turned red"))
    return results


def run_checks(*, results=None, mutants=True):
    """Every row, then every mutant, as (label, ok, what it saw)."""
    results = [] if results is None else results
    add = lambda label, ok, saw="": results.append((label, bool(ok), "" if ok else saw))
    with tempfile.TemporaryDirectory(prefix="shoalmark-ask-ids-") as tmp:
        area = Path(tmp).resolve()
        for n, rows in enumerate(ROWS):
            try:
                rows(area / f"r{n}", add)
            except Exception as e:
                add(f"{rows.__name__}: a fixture step failed — {type(e).__name__}: {str(e)[:300]}", False, getattr(e, "stderr", "") or "")
    fm.configure(HERE)
    if mutants:
        run_mutants(results=results)
    return results


if __name__ == "__main__":
    failed = 0
    for label, ok, detail in run_checks(mutants="--no-mutants" not in sys.argv):
        print(("  ok    " if ok else "  FAIL  ") + label + ("" if ok else f"\n        {detail}" if detail else ""))
        failed += not ok
    print(f"FAILED: {failed}" if failed else "all green")
    sys.exit(1 if failed else 0)
