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


# --- minting and reuse, read from each change -------------------------------------------------------------------------------------

def rows_minting(area, add):
    r = Repo(area / "c1", {"FM-001": text("FM-001")})
    r.write("FM-001", text("FM-001", ask()))
    r.commit("FM-001: put to the Owner, no id")
    said = r.check()
    add("C1 · a put with no id: refused, naming the next number", refused(said, "puts an ask with no `ask-id:`", "write `ask-id: FM-001-Q1`"), seen(said))
    r = Repo(area / "c1-before", {"FM-001": text("FM-001", ask())})
    r.write("FM-001", text("FM-001", ask(q="Ship it now?")))
    r.commit("FM-001: the ask before ids, reworded in place")
    said = r.check()
    add("C1 · an ask before ids reworded in place: refused the same way", refused(said, "writes a new `ask:` where `next: owner` stands", "write `ask-id: FM-001-Q1`"), seen(said))
    r = Repo(area / "c1-left", {"FM-001": text("FM-001", ask())})
    r.write("FM-001", text("FM-001", ask(), body="\nA line of its body.\n"))
    r.commit("FM-001: its body, the ask before ids untouched")
    said = r.check()
    add("C1 · an ask before ids that no change touches stays as it is: accepted", accepted(said, "ask-id"), seen(said))
    for what, change in (("question", dict(q="Ship it later?")), ("proposal", dict(proposal="no")), ("options", dict(options="yes | no")),
                         ("kind", dict(kind="determination"))):
        r = Repo(area / f"c2-{what}", {"FM-001": text("FM-001", ask(aid="FM-001-Q1", options="yes | later"))})
        r.write("FM-001", text("FM-001", ask(aid="FM-001-Q1", **{"options": "yes | later", **change})))
        r.commit(f"FM-001: its {what}, changed in place")
        said = r.check()
        add(f"C2 · the put ask's {what} changed under its id: refused, naming the withdrawal and the next number",
            refused(said, f"changes the put ask under FM-001-Q1 — its {what}", "put the changed ask as FM-001-Q2"), seen(said))
    r = Repo(area / "c2-renewed", {"FM-001": text("FM-001", ask(aid="FM-001-Q1"))})
    r.write("FM-001", text("FM-001", ask(aid="FM-001-Q2", q="Ship it later?"), asks=record("FM-001-Q1", "Ship it?")))
    r.commit("FM-001: FM-001-Q1 withdrawn, the changed ask put as FM-001-Q2")
    said = r.check()
    add("C2 · the same change made as a withdrawal and a new put — the old id's record, the changed ask under the next number: accepted", accepted(said), seen(said))
    r = Repo(area / "c3", {"FM-001": text("FM-001", ask(aid="FM-001-Q1"))})
    r.write("FM-001", text("FM-001", "next: build\n"))
    r.commit("FM-001: the ask dropped")
    said = r.check()
    add("C3 · an id dropped with no record: refused, naming `--clear-ask`", refused(said, "removes FM-001-Q1 with no record under `## Asks`", "--clear-ask FM-001-Q1"), seen(said))
    r = Repo(area / "no-file", {"FM-001": text("FM-001", ask(aid="FM-001-Q1"))})
    (r.root / "shoalmark.toml").write_text('name = "ids"\n[kinds]\nFM = "Work"\n', encoding="utf-8")      # no seat: the rights walk reads no line
    r.write("FM-001", text("FM-001", ask(aid="FM-001-Q1"), body="\nA line of its body.\n"))
    r.commit("FM-001: its body, in a repository that names no seat")
    bare = {"id": "FM-999", "kind": "FM", "status": "Proposed", "hook": "a tracker held in memory", "links": [], "tags": []}
    fm.configure(r.root)
    try:
        with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
            fm.lint([bare, *fm.load_trackers()])
        broke = ""
    except Exception as e:
        broke = f"{type(e).__name__}: {e}"
    finally:
        fm.configure(HERE)
    add("a tracker a caller holds in memory, with no file, passes through the id rules on a change without an exception, as through the "
        "tool's other readers", not broke, broke)
    r = Repo(area / "c4-equal", {"FM-001": text("FM-001", asks=record("FM-001-Q1", "Ship it?", "accepted"))})
    r.write("FM-001", text("FM-001", ask(aid="FM-001-Q1", q="Ship the next?"), asks=record("FM-001-Q1", "Ship it?", "accepted")))
    r.commit("FM-001: a new ask under a used number")
    said = r.check()
    add("C4 · a new id equal to a record's: refused, naming the next number", refused(said, "puts FM-001-Q1, and its number is not above every number FM-001 has used", "put it as FM-001-Q2"), seen(said))
    r = Repo(area / "c4-below", {"FM-001": text("FM-001", asks=record("FM-001-Q3", "Ship it?", "accepted"))})
    r.write("FM-001", text("FM-001", ask(aid="FM-001-Q2", q="Ship the next?"), asks=record("FM-001-Q3", "Ship it?", "accepted")))
    r.commit("FM-001: a new ask below the highest number")
    said = r.check()
    add("C4 · a new id below the highest number in the records: refused, naming the next number", refused(said, "the highest is FM-001-Q3", "put it as FM-001-Q4"), seen(said))
    r = Repo(area / "c4-history", {"FM-001": text("FM-001")})
    r.write("FM-001", text("FM-001", ask(aid="FM-001-Q1")))
    r.commit("FM-001: put as FM-001-Q1")
    r.write("FM-001", text("FM-001", "next: build\n"))
    git(r.root, "add", "-A")
    git(r.root, "commit", "-q", "-m", "FM-001: the number lost, past the gate")
    git(r.root, "push", "-q", "origin", "main")
    r.switch("-c", "later")
    r.write("FM-001", text("FM-001", ask(aid="FM-001-Q1", q="Ship it again?")))
    r.commit("FM-001: the lost number minted again")
    said = r.check()
    add("C4 · a number written and removed in the file's history, minted again: refused on git, naming the next number",
        refused(said, "puts FM-001-Q1, and its number is not above every number FM-001 has used", "put it as FM-001-Q2"), seen(said))
    r = Repo(area / "c4-plain", {"FM-001": text("FM-001", ask(aid="FM-001-Q1", q="Ship it again?"))}, vcs="none")
    run(r.root, "--print-written")
    said = r.check()
    add("C4 · …and in a plain folder, where no history is read: accepted, with the limit line", accepted(said, "refused")
        and "note: ask ids are checked against the file alone — a number removed without its record" in said[2], seen(said))


# --- two branches that each mint the same number ------------------------------------------------------------------------------------

def two(area, name, start=None):
    """A repository and its two branches, A and B, cut from one commit of `main`."""
    r = Repo(area / name, {"FM-001": start or text("FM-001")})
    git(r.root, "branch", "A")
    git(r.root, "branch", "B")
    return r


def rows_branches(area, add):
    r = two(area, "c5-both")
    for b, q in (("A", "Ship A?"), ("B", "Ship B?")):
        r.switch(b)
        r.write("FM-001", text("FM-001", ask(aid="FM-001-Q1", q=q)))
        r.commit(f"FM-001: put on {b}")
    r.land("A")
    r.switch("B")
    said, waits = r.check(), r.queue("B")
    add("C5 · both mint Q1 and A merges: B refused by `--check`, naming what holds it and the next number, and in `--queue`",
        refused(said, "FM-001-Q1 is taken on origin/main — its open ask, another put ask", "renumber this branch's ask as FM-001-Q2")
        and waits[0].startswith("wait: ") and waits[1] == "wait: FM-001-Q1 is taken on origin/main — renumber", seen(said) + f" · {waits}")
    r.write("FM-001", text("FM-001", ask(aid="FM-001-Q2", q="Ship B?")))
    r.commit("FM-001: B's ask renumbered")
    said = r.check()
    add("C5 · …B renumbered Q2: accepted", accepted(said, "is taken on"), seen(said))
    r = two(area, "c5-record")
    r.switch("A")
    r.write("FM-001", text("FM-001", ask(aid="FM-001-Q1", q="Ship A?")))
    r.commit("FM-001: put on A")
    r.write("FM-001", text("FM-001", asks=record("FM-001-Q1", "Ship A?")))
    r.commit("FM-001: cleared on A")
    r.land("A")
    r.switch("B")
    r.write("FM-001", text("FM-001", ask(aid="FM-001-Q1", q="Ship B?")))
    r.commit("FM-001: put on B")
    said, waits = r.check(), r.queue("B")
    add("C5 · A clears Q1 and B's open Q1 would merge clean beside A's record: refused on B before the merge — C5 reads the default branch's records — by `--check` and in `--queue`",
        refused(said, "FM-001-Q1 is taken on origin/main — its record of", '"Ship A?"') and waits[0] == waits[1] == "wait: FM-001-Q1 is taken on origin/main — renumber", seen(said) + f" · {waits}")
    r.land("B")
    said = r.check()
    add("C5 · …and by F3 after a merge made without the check", refused(said, "`ask-id: FM-001-Q1` is also the id of the record of"), seen(said))
    r = two(area, "c5-twice")
    for b, q in (("A", "Ship A?"), ("B", "Ship B?")):
        r.switch(b)
        r.write("FM-001", text("FM-001", asks=record("FM-001-Q1", q, day=SINCE if b == "A" else TODAY)))
        r.commit(f"FM-001: an ask put and cleared on {b}")
    r.land("A")
    r.switch("B")
    said, waits = r.check(), r.queue("B")
    add("C5 · A and B each clear a Q1 of their own — duplicate archived ids: refused on B by C5, in `--check` and in `--queue`",
        refused(said, "FM-001-Q1 is taken on origin/main") and waits[0].startswith("wait: ") and waits[1].startswith("wait: FM-001-Q1 is taken"), seen(said) + f" · {waits}")
    r.switch("main")
    git(r.root, "merge", "-q", "--no-ff", "--no-edit", "B", check=False)
    r.write("FM-001", text("FM-001", asks=record("FM-001-Q1", "Ship A?") + "\n" + record("FM-001-Q1", "Ship B?", day=TODAY)))
    r.commit("the merge, made against the gate")
    git(r.root, "push", "-q", "origin", "main")
    git(r.root, "fetch", "-q", "origin")
    said = r.check()
    add("C5 · …after a merge made against the gate, a note on the default branch naming both, and the next number above both",
        "note: FM-001: two records under `## Asks` carry FM-001-Q1" in said[2] and "the next ask is FM-001-Q2" in said[2] and "FM-001-Q1 is taken" not in said[2], seen(said))
    r = two(area, "c5-carried", text("FM-001", ask(aid="FM-001-Q1")))
    r.switch("A")
    r.write("FM-001", text("FM-001", "next: build\n", asks=record("FM-001-Q1", "Ship it?")))
    r.commit("FM-001: cleared on A")
    r.land("A")
    r.switch("B")
    r.write("FM-001", text("FM-001", ask(aid="FM-001-Q1"), body="\nB's line.\n"))
    r.commit("FM-001: B's own line")
    said, waits = r.check(), r.queue("B")
    add("C5 · B carries Q1 from its merge base while A clears it: not proposed — accepted, and `--queue` waits on nothing of it",
        accepted(said, "is taken on") and "taken" not in waits[0] and not waits[1], seen(said) + f" · {waits}")
    r = two(area, "c5-higher")
    r.switch("A")
    r.write("FM-001", text("FM-001", ask(aid="FM-001-Q3")))
    r.commit("FM-001: put on A as Q3")
    r.land("A")
    r.switch("B")
    r.write("FM-001", text("FM-001", ask(aid="FM-001-Q2", q="Ship B?")))
    r.commit("FM-001: put on B as Q2")
    said = r.check()
    add("C5 · B proposes Q2 while the default branch's highest is Q3 and holds no Q2: refused, naming Q4", refused(said, "FM-001-Q2 is taken on origin/main", "FM-001-Q4"), seen(said))
    r = two(area, "c5-cherry")
    r.switch("A")
    r.write("FM-001", text("FM-001", ask(aid="FM-001-Q1")))
    pick = r.commit("FM-001: put")
    r.switch("B")
    git(r.root, "cherry-pick", pick)
    r.land("A")
    r.switch("B")
    said = r.check()
    add("C5 · one ask cherry-picked to both branches: accepted", accepted(said, "is taken on"), seen(said))


# --- the answer's commit, found by its id -------------------------------------------------------------------------------------------

def put_repo(area, name, q="Ship it?", **kw):
    """A repository whose `main` holds one tracker's ask, put by the seat under its first id, and a branch `ans` cut from it."""
    r = Repo(area / name, {"FM-001": text("FM-001")})
    r.write("FM-001", text("FM-001", ask(aid="FM-001-Q1", q=q, **kw)))
    r.commit("FM-001: put as FM-001-Q1")
    git(r.root, "push", "-q", "origin", "main")
    r.switch("-c", "ans")
    return r


def rows_binding(area, add):
    r = put_repo(area, "b-ok")
    said_a = run(r.root, "--answer", "FM-001-Q1", "accept")
    said = r.check()
    add("3b · the Owner's signed commit with `Answers:`: accepted on its branch", said_a[0] == 0 and accepted(said), seen(said_a) + " · " + seen(said))
    r.switch("main")
    git(r.root, "merge", "-q", "--no-ff", "--no-edit", "ans")
    git(r.root, "push", "-q", "origin", "main")
    git(r.root, "fetch", "-q", "origin")
    said = r.check()
    add("3b · …and on `main` after a merge commit a seat made: the answer is found by its id, never by the line", accepted(said), seen(said))
    cases = (("no trailer", ()), ("a trailer naming another id", ("Answers: FM-002-Q1",)), ("`Answers: FM-001-Q12` against FM-001-Q1", ("Answers: FM-001-Q12",)))
    for n, (what, trailers) in enumerate(cases):
        r = put_repo(area, f"b-trailer-{n}")
        r.write("FM-001", answered(r.read("FM-001"), by=OWNER[0]))
        r.commit("FM-001-Q1: accepted", who=OWNER, sign=True, trailers=trailers)
        said = r.check()
        add(f"3b · {what}: refused — the walk names the trailer, and no commit answers the id", refused(said, "does not name it", "no commit answers FM-001-Q1"), seen(said))
    r = put_repo(area, "b-seat")
    r.write("FM-001", answered(r.read("FM-001"), by=SEAT[0]))
    r.commit("FM-001-Q1: accepted", who=SEAT, trailers=("Answers: FM-001-Q1",))
    said = r.check()
    add("3b · a seat's unsigned answer: refused", refused(said, "no commit answers FM-001-Q1"), seen(said))
    r = put_repo(area, "b-key")
    r.signers(f"{OWNER[1]} " + r.keys["other"].with_suffix(".pub").read_text(encoding="utf-8"))
    r.commit("the branch's own signers file", who=SEAT)
    r.write("FM-001", answered(r.read("FM-001")))
    run(r.root, "--print-written")
    git(r.root, "add", "-A")
    git(r.root, "commit", "-q", "-S", "-m", "FM-001-Q1: accepted", "-m", "Answers: FM-001-Q1", who=OWNER, sign=r.keys["other"])
    said = r.check()
    add("3b · the Owner's email with a key only the branch's own signers file holds: refused", refused(said, "no commit answers FM-001-Q1"), seen(said))
    r = put_repo(area, "b-restore")
    run(r.root, "--answer", "FM-001-Q1", "accept")
    run(r.root, "--answer", "FM-001-Q1", "revoke", "not yet")
    t = r.read("FM-001").replace('answer: "revoked - not yet"', 'answer: "accepted"')
    r.write("FM-001", t)
    r.commit("FM-001: the answer put back", who=SEAT)
    said = r.check()
    add("3b · a seat's commit that restores an answer the Owner revoked: refused", refused(said, "FM-001"), seen(said))
    r = put_repo(area, "b-two")
    git(r.root, "branch", "ans2")
    run(r.root, "--answer", "FM-001-Q1", "accept")
    r.switch("ans2")
    run(r.root, "--answer", "FM-001-Q1", "accept", "the other way")
    git(r.root, "merge", "-q", "--no-edit", "ans", check=False)
    r.write("FM-001", r.read("FM-001") if "<<<<<<<" not in r.read("FM-001") else answered(text("FM-001", ask(aid="FM-001-Q1")), answer="accepted - the other way"))
    git(r.root, "add", "-A")
    git(r.root, "commit", "-q", "--no-edit", who=SEAT, check=False)
    said = r.check()
    add("3b · two Owner answers to one id on two branches, brought together: refused — two heads", refused(said, "FM-001-Q1 has 2 answers"), seen(said))
    run(r.root, "--answer", "FM-001-Q1", "accept", "the other way, settled", "--supersede")
    said = r.check()
    add("3b · …then one replaces the other, on the branch that holds both: accepted", accepted(said, "has 2 answers"), seen(said))
    r = put_repo(area, "b-rewrite")
    r.write("FM-001", answered(r.read("FM-001")).replace('ask: "Ship it?"', 'ask: "Ship it soon?"'))
    r.commit("FM-001-Q1: accepted", who=OWNER, sign=True, trailers=("Answers: FM-001-Q1",))
    said = r.check()
    add("3b · an answer commit that also rewrites the question: refused", refused(said, "changes its put ask in the same commit"), seen(said))
    for what, edit in (("question", ('ask: "Ship it?"', 'ask: "Ship it soon?"')), ("proposal", ('ask-proposal: "yes"', 'ask-proposal: "no"')), ("options", ('ask-proposal: "yes"\n', 'ask-proposal: "yes"\nask-options: "yes | no"\n')),
                       ("kind", ("ask-kind: ruling", "ask-kind: determination"))):
        r = put_repo(area, f"b-bare-{what}")
        run(r.root, "--answer", "FM-001-Q1", "accept")
        r.write("FM-001", r.read("FM-001").replace(*edit))
        r.commit(f"FM-001: its {what}, edited by a seat", who=SEAT)
        said = r.check()
        add(f"3b · the Owner's signed bare acceptance, then a seat's unsigned edit of its {what}: refused twice — by C2 on the seat's change and by the binding on the standing answer",
            refused(said, f"changes the put ask under FM-001-Q1 — its {what}", "the put ask here is not the one"), seen(said))
    r = put_repo(area, "b-since")
    run(r.root, "--answer", "FM-001-Q1", "accept")
    r.write("FM-001", r.read("FM-001").replace(f"ask-since: {SINCE}", f"ask-since: {TODAY}"))
    r.commit("FM-001: its ask-since, edited by a seat", who=SEAT)
    said = r.check()
    add("3b · …a seat's edit of its `ask-since:` alone: accepted", accepted(said), seen(said))
    r = put_repo(area, "b-by")
    r.write("FM-001", answered(r.read("FM-001"), by="Someone"))
    r.commit("FM-001-Q1: accepted", who=OWNER, sign=True, trailers=("Answers: FM-001-Q1",))
    said = r.check()
    add("3b · `answered-by:` not the head's author: refused", refused(said, "answered-by: Someone"), seen(said))
    r = put_repo(area, "b-squash")
    run(r.root, "--answer", "FM-001-Q1", "accept")
    r.switch("main")
    git(r.root, "merge", "-q", "--squash", "ans")
    git(r.root, "commit", "-q", "-m", "FM-001-Q1: accepted (#7)", "-m", "Answers: FM-001-Q1", who=SEAT)
    git(r.root, "branch", "-q", "-D", "ans")
    said = r.check()
    add("3b · a squash merge of the answer: refused — the Owner's signature is gone", refused(said, "no commit answers FM-001-Q1"), seen(said))


# --- the commands -------------------------------------------------------------------------------------------------------------------

def rows_commands(area, add):
    r = Repo(area / "c3-clear", {"FM-001": text("FM-001", ask(aid="FM-001-Q1"))})
    said_clear = run(r.root, "--clear-ask", "FM-001-Q1", "build", who=SEAT)
    r.commit("FM-001: FM-001-Q1 withdrawn")
    said = r.check()
    add("C3 · the same through `--clear-ask`: the record carries the id, withdrawn — accepted, and `--clear-ask` names the next id",
        accepted(said) and f"**FM-001-Q1** · {TODAY} · Ship it?\n**withdrawn** — no answer was given" in r.read("FM-001")
        and "the next ask on FM-001 is FM-001-Q2" in said_clear[1], seen(said) + " · " + said_clear[1][-200:])
    r = put_repo(area, "cmd")
    before = (r.head(), git(r.origin, "for-each-ref"), r.read("FM-001"))
    said = run(r.root, "--answer", "FM-001-Q9", "accept")
    add("3c · `--answer` with an unknown id refuses before writing, naming the open ask",
        said[0] == fm.EXIT_LINT and "FM-001 has no ask FM-001-Q9: it holds FM-001-Q1, open" in said[2] and (r.head(), git(r.origin, "for-each-ref"), r.read("FM-001")) == before, seen(said))
    said = run(r.root, "--answer", "FM-001", "accept")
    add("3c · a tracker id where the ask has an id: refused, naming the id", said[0] == fm.EXIT_LINT and "FM-001's ask carries its id, FM-001-Q1 — name the ask you read" in said[2], seen(said))
    said = run(r.root, "--answer", "FM-001-Q1", "accept")
    t = r.read("FM-001")
    log = [git(r.root, "log", "-1", f"--format={f}").strip() for f in ("%s", "%(trailers:key=Answers,valueonly)", "%G?")]
    add("3c · `--answer <ask-id>`: one signed commit on the branch it stands on, `<ask-id>: <answer>` with `Answers: <ask-id>`, nothing pushed, no `answer/*` ref, the branch unchanged",
        said[0] == 0 and log == ["FM-001-Q1: accepted", "FM-001-Q1", "G"] and git(r.root, "branch", "--show-current").strip() == "ans"
        and "answering FM-001-Q1 — 2/3 writing" in said[2]
        and git(r.root, "for-each-ref", "refs/heads/answer", "refs/remotes/origin/answer") == "" and git(r.origin, "for-each-ref") == before[1]
        and said[1].startswith("FM-001-Q1 answered: accepted\n  signed, committed on `ans` as ") and 'answer: "accepted"' in t, seen(said))
    said = run(r.root, "--answer", "FM-001-Q1", "reject", "no")
    add("3c · an id already answered: refused, naming revoke and `--supersede`", said[0] == fm.EXIT_LINT and "answered already" in said[2] and "--supersede" in said[2], seen(said))
    said = run(r.root, "--answer", "FM-001-Q1", "accept", "later", "--supersede")
    add("3c · …then `--supersede`: accepted, the answer replaced, its commit naming the id", said[0] == 0 and "Answers: FM-001-Q1" in git(r.root, "log", "-1", "--format=%B")
        and r.check()[0] == 0, seen(said))
    run(r.root, "--clear-ask", "FM-001-Q1", "build", who=SEAT)
    r.commit("FM-001: FM-001-Q1 cleared", who=SEAT)
    r.write("FM-001", r.read("FM-001").replace("next: build\n", ask(aid="FM-001-Q2", q="Ship the next?")))
    r.commit("FM-001: put as FM-001-Q2", who=SEAT)
    before = (r.head(), r.read("FM-001"))
    said = run(r.root, "--answer", "FM-001-Q1", "accept")
    add("3c · an id the tracker no longer holds open: refused before writing, in the design's words, the file as it was",
        said[0] == fm.EXIT_LINT and f'FM-001 holds another ask now: FM-001-Q2, since {SINCE}: "Ship the next?". FM-001-Q1 was answered and is in FM-001\'s record. '
        "Nothing was written. Read FM-001-Q2, then answer it by its id" in said[2] and (r.head(), r.read("FM-001")) == before, seen(said))


# --- asks before ids -------------------------------------------------------------------------------------------------------------

def rows_before(area, add):
    r = Repo(area / "before", {"FM-001": text("FM-001", ask(q="Ship the old one?")), "FM-002": text("FM-002", ask(aid="FM-002-Q1", q="Ship the new one?"))})
    owner, standup = run(r.root, "--owner")[1], run(r.root, "--standup")[1]
    run(r.root, "--html-only")
    page = (r.root / REL / "index.html").read_text(encoding="utf-8")
    add("2 · `--owner` names an ask with an id by its id, and an ask before ids by its tracker, *asked before ask ids*",
        "\nFM-002-Q1 · ruling · asked 2 day(s) ago" in owner and "\nFM-001 · ruling · asked 2 day(s) ago · asked before ask ids" in owner, owner[:400])
    add("2 · `--standup` the same", "FM-002-Q1 — Ship the new one?  [2 day(s)]" in standup and "FM-001 — Ship the old one?  [2 day(s) · asked before ask ids]" in standup, standup[:400])
    add("2 · the board's row carries the id as the ask cell's 13th item, and its label for an ask before ids",
        '"FM-002-Q1"]' in page and '"ask.legacy": "asked before ask ids"' in page, "")
    said = run(r.root, "--answer", "FM-001", "accept")
    gate = r.check()
    add("2 · an open ask without an id, answered by its tracker's id, verified as today", said[0] == 0 and accepted(gate), seen(said) + " · " + seen(gate))
    run(r.root, "--clear-ask", "FM-001", "build", who=SEAT)
    t = r.read("FM-001")
    add("2 · its record carries no id: `**<date>** · <question>`", f"**{TODAY}** · Ship the old one?\n**answered** — accepted · Owner" in t and "**FM-001-Q" not in t, t[-300:])


# --- a record whose id another record carries too, as every reading names it -----------------------------------------------------

def rows_record_names(area, add):
    twice = record("FM-004-Q1", "Ship it?", day=SINCE) + "\n" + record("FM-004-Q1", "Ship the other?", "accepted", day=TODAY)
    r = Repo(area / "names", {"FM-001": text("FM-001"), "FM-002": text("FM-002", ask(aid="FM-002-Q1", q="Ship the new one?")),
                              "FM-003": text("FM-003", ask(q="Ship the old one?")), "FM-004": text("FM-004", ask(aid="FM-004-Q2", q="Ship the next?"), asks=twice)})
    git(r.root, "branch", "A")
    git(r.root, "branch", "B")
    for b, q, day in (("A", "Ship A?", SINCE), ("B", "Ship B?", TODAY)):
        r.switch(b)
        r.write("FM-001", text("FM-001", ask(aid="FM-001-Q1", q=q)))
        r.commit(f"FM-001: put on {b}")
        r.write("FM-001", text("FM-001", "next: build\n", asks=record("FM-001-Q1", q, day=day)))
        r.commit(f"FM-001: cleared on {b}")
    r.land("A")
    git(r.root, "merge", "-q", "--no-ff", "--no-edit", "B", check=False)
    r.write("FM-001", text("FM-001", "next: build\n", asks=record("FM-001-Q1", "Ship A?", day=SINCE) + "\n" + record("FM-001-Q1", "Ship B?", day=TODAY)))
    r.commit("the merge, made against the gate")
    git(r.root, "push", "-q", "origin", "main")
    git(r.root, "fetch", "-q", "origin")
    for named in ("FM-002-Q1", "FM-003"):
        run(r.root, "--clear-ask", named, "build", who=SEAT)
    r.commit("FM-002 and FM-003: their asks cleared")
    short = git(r.root, "log", "-1", "--format=%h").strip()
    said = run(r.root, "--answered")
    acted = [l for l in said[1].splitlines() if " — acted on in `" in l]
    add("4 · `--answered` names an acted-on record whose id another record carries too by its id and its date, `FM-001-Q1 of <date>` — the newest record's",
        said[0] == 0 and any(l.startswith(f"  FM-001-Q1 of {TODAY} — acted on in `") for l in acted) and not any(l.startswith("  FM-001-Q1 —") for l in acted),
        seen(said) + f" · {acted}")
    add("4 · `--answered` names an acted-on record whose id no other record carries by the bare id",
        f"  FM-002-Q1 — acted on in `{short}`" in acted and "FM-002-Q1 of" not in said[1], f"{acted}")
    add("2 · `--answered` names an acted-on record of an ask before ask ids by its tracker", f"  FM-003 — acted on in `{short}`" in acted, f"{acted}")
    before = (r.head(), r.read("FM-004"))
    said = run(r.root, "--answer", "FM-004-Q1", "accept")
    add("4 · `--answer` on an id two records carry while another ask is open: refused before writing, naming each record by its id and its date",
        said[0] == fm.EXIT_LINT and f'FM-004 holds another ask now: FM-004-Q2, since {SINCE}: "Ship the next?". FM-004-Q1 of {SINCE} was withdrawn and is in FM-004\'s record. '
        f"FM-004-Q1 of {TODAY} was answered and is in FM-004's record. Nothing was written. Read FM-004-Q2, then answer it by its id" in said[2]
        and (r.head(), r.read("FM-004")) == before, seen(said))
    said = run(r.root, "--answer", "FM-004-Q9", "accept")
    add("4 · `--answer` with an unknown id: its list of the records names an id two records carry by its id and its date",
        said[0] == fm.EXIT_LINT and f"FM-004 has no ask FM-004-Q9: it holds FM-004-Q2, open; FM-004-Q1 of {SINCE}, FM-004-Q1 of {TODAY} are in its record" in said[2]
        and (r.head(), r.read("FM-004")) == before, seen(said))


# --- an answer an earlier `--answer` left half-written, given again as `--answer` takes it -----------------------------------------

def rows_given_again(area, add):
    r = Repo(area / "again", {"FM-001": text("FM-001", ask(aid="FM-001-Q1")), "FM-002": text("FM-002", ask(q="Ship the old one?")),
                              "FM-003": text("FM-003", ask(aid="FM-003-Q1", q="Ship the third?"))})
    for tid in ("FM-001", "FM-002"):
        write(r.root, tid, answered(r.read(tid)))
    before = r.head()
    said = run(r.root, "--answer", "FM-003-Q1", "accept")
    add("3c · a tree an earlier `--answer` left half-written, its ask carrying an id: the refusal gives the answer again by the ask's id",
        said[0] == fm.EXIT_LINT and "failed half-way" in said[2] and "--answer FM-001-Q1 accept" in said[2] and "--answer FM-001 accept" not in said[2]
        and r.head() == before, seen(said))
    add("2 · …and an ask before ask ids by its tracker's id", said[0] == fm.EXIT_LINT and "--answer FM-002 accept" in said[2], seen(said))


# --- a renumbering, and what the default branch holds ----------------------------------------------------------------------------

def rows_renumber(area, add):
    r = put_repo(area, "renumber-alone")
    r.write("FM-001", r.read("FM-001").replace("ask-id: FM-001-Q1", "ask-id: FM-001-Q2"))
    r.commit("FM-001: its ask renumbered, where no other ask holds its number")
    said = r.check()
    add("C3 · an id renumbered, its put ask unchanged, where no other ask holds the old number: refused, naming `--clear-ask` — the old number keeps its record",
        refused(said, "removes FM-001-Q1 with no record under `## Asks`", "--clear-ask FM-001-Q1"), seen(said))
    r = two(area, "renumber-landed")
    r.switch("A")
    r.write("FM-001", text("FM-001", ask(aid="FM-001-Q1", q="Ship A?")))
    r.commit("FM-001: put on A")
    r.write("FM-001", text("FM-001", asks=record("FM-001-Q1", "Ship A?")))
    r.commit("FM-001: cleared on A")
    r.land("A")
    r.switch("B")
    r.write("FM-001", text("FM-001", ask(aid="FM-001-Q1", q="Ship B?")))
    r.commit("FM-001: put on B")
    r.land("B")
    r.write("FM-001", text("FM-001", ask(aid="FM-001-Q2", q="Ship B?"), asks=record("FM-001-Q1", "Ship A?")))
    r.commit("FM-001: the open ask renumbered beside the record that holds its number")
    said = r.check()
    add("F3's repair on the default branch: the open ask renumbered, its put ask unchanged, beside the record that holds the old number — accepted, with no record of its own",
        accepted(said, "removes FM-001-Q1"), seen(said))


# --- `--revoke`: the argument names what it takes back -------------------------------------------------------------------------------

def act_repo(area, name):
    """`put_repo` with an action ask, which the Owner accepted and whose act they did (`--done`), on `ans`."""
    r = put_repo(area, name, kind="action", proposal="I do it")
    run(r.root, "--answer", "FM-001-Q1", "accept")
    run(r.root, "--done", "FM-001", "evidence/result.md")
    return r


def rows_revoke(area, add):
    r = act_repo(area, "revoke-forms")
    done = "\ndone: " in r.read("FM-001")
    said = run(r.root, "--revoke", "FM-001-Q1", "the promise is withdrawn")
    t = r.read("FM-001")
    log = [git(r.root, "log", "-1", f"--format={f}").strip() for f in ("%s", "%(trailers:key=Answers,valueonly)", "%G?")]
    add("3c · `--revoke <ask-id>` on an action whose act is done: the answer to that ask is revoked, one signed commit naming the id — the act done stays",
        done and said[0] == 0 and 'answer: "revoked - the promise is withdrawn"' in t and "\ndone: " in t
        and log == ["FM-001-Q1: revoked - the promise is withdrawn", "FM-001-Q1", "G"], seen(said) + " · " + " | ".join(log))
    said = r.check()
    add("3c · …and the gate counts the revocation: its commit is found by the id", accepted(said), seen(said))
    said = run(r.root, "--revoke", "FM-001", "not done after all")
    t = r.read("FM-001")
    add("3c · …then `--revoke <tracker id>` on the same tracker: the act done is revoked — `done:` leaves, the revocation is under `## Acts` — and the answer stands as the revocation left it",
        said[0] == 0 and "\ndone: " not in t and "done revoked — not done after all" in t and 'answer: "revoked - the promise is withdrawn"' in t
        and git(r.root, "log", "-1", "--format=%s").strip() == "FM-001: done revoked — not done after all", seen(said))
    r = act_repo(area, "revoke-stale")
    before = (r.head(), r.read("FM-001"))
    said = run(r.root, "--revoke", "FM-001-Q2", "not this one")
    add("3c · `--revoke` with an ask id the tracker does not hold, on an action whose act is done: refused before writing, naming the ask it holds — nothing revoked",
        said[0] == fm.EXIT_LINT and "FM-001 has no ask FM-001-Q2: it holds FM-001-Q1, open" in said[2] and (r.head(), r.read("FM-001")) == before, seen(said))


# --- where the answer's commit is made ------------------------------------------------------------------------------------------------

def rows_unborn(area, add):
    base = area / "unborn"
    wc = base / "wc"
    wc.mkdir(parents=True)
    key = base / "key-owner"
    subprocess.run(["ssh-keygen", "-q", "-t", "ed25519", "-N", "", "-f", str(key), "-C", "owner"], check=True, capture_output=True)
    git(wc, "init", "-q", "--initial-branch=main")
    for k, v in (("user.name", OWNER[0]), ("user.email", OWNER[1]), ("gpg.format", "ssh"), ("user.signingkey", str(key)),
                 ("gpg.ssh.allowedSignersFile", f"{REL}/allowed_signers"), ("commit.gpgsign", "false")):
        git(wc, "config", k, v)
    (wc / "shoalmark.toml").write_text(CONFIG, encoding="utf-8")
    (wc / REL).mkdir(parents=True)
    (wc / REL / "allowed_signers").write_text(f"{OWNER[1]} " + key.with_suffix(".pub").read_text(encoding="utf-8"), encoding="utf-8")
    write(wc, "FM-001", text("FM-001", ask(aid="FM-001-Q1")))
    state = lambda: (git(wc, "rev-parse", "--verify", "-q", "HEAD", check=False).strip(), git(wc, "ls-files", "--stage"), (wc / REL / "FM-001-x.md").read_bytes())
    before = state()
    said = run(wc, "--answer", "FM-001-Q1", "accept")
    add("3c · `--answer <ask-id>` on a branch with no commit yet: refused before writing — HEAD unborn, the index and the tracker's bytes as they were",
        said[0] == fm.EXIT_LINT and "this branch has no commit yet" in said[2] and state() == before and before[0] == "", seen(said))
    r = put_repo(area, "detached")
    git(r.root, "switch", "-q", "--detach")
    said = run(r.root, "--answer", "FM-001-Q1", "accept")
    add("3c · …on a detached HEAD the answer is made: one commit on it, still detached, the gate counting it",
        said[0] == 0 and "committed on a detached HEAD as " in said[1] and git(r.root, "branch", "--show-current").strip() == "" and accepted(r.check()), seen(said))


# --- the answer history, read once for every standing answer --------------------------------------------------------------------------

def counted(fn):
    """`fn()`, and how many `git log --grep=^Answers:` it started — every start of the module's process boundary watched."""
    real, seen_ = fm.vcs_process, []

    def watching(program, *a, **k):
        seen_.append((program, *a))
        return real(program, *a, **k)
    fm.vcs_process = watching
    try:
        out = fn()
    finally:
        fm.vcs_process = real
    return out, sum(1 for argv in seen_ if "--grep=^Answers:" in argv)


def heads_of(r):
    """`answer_commits` over the trackers of `r` as they stand: {ask id: (head, why)}."""
    fm.configure(r.root)
    try:
        with contextlib.redirect_stderr(io.StringIO()):
            return fm.answer_commits(fm.load_trackers())
    finally:
        fm.configure(HERE)


def rows_one_log(area, add):
    r = Repo(area / "one-log", {tid: text(tid) for tid in ("FM-001", "FM-002", "FM-003")})
    for tid in ("FM-001", "FM-002", "FM-003"):
        r.write(tid, text(tid, ask(aid=f"{tid}-Q1", q=f"Ship {tid}?")))
    r.commit("three asks, put")
    git(r.root, "push", "-q", "origin", "main")
    r.switch("-c", "ans")
    shas = {}
    for tid in ("FM-001", "FM-002"):
        run(r.root, "--answer", f"{tid}-Q1", "accept")
        shas[f"{tid}-Q1"] = r.head()
    said, logs = counted(r.check)
    heads = heads_of(r)
    add("3b · two standing answers, each beside its id: one `--check` reads the answer history once — one `git log --grep=^Answers:` — and finds each head, with no refusal",
        accepted(said) and logs == 1 and heads == {aid: (sha, "") for aid, sha in shas.items()}, seen(said) + f" · {logs} log(s) · {heads}")
    r.write("FM-003", answered(r.read("FM-003"), by=SEAT[0]))
    r.commit("FM-003-Q1: accepted", who=SEAT, trailers=("Answers: FM-003-Q1",))
    said, logs = counted(r.check)
    heads = heads_of(r)
    add("3b · …and with a third that does not count, a seat's unsigned answer: still one read; the third refused — no commit answers it — and the two others found",
        refused(said, "FM-003: no commit answers FM-003-Q1") and "FM-001: no commit" not in said[2] and "FM-002: no commit" not in said[2] and logs == 1
        and {aid: h for aid, h in heads.items() if aid != "FM-003-Q1"} == {aid: (sha, "") for aid, sha in shas.items()} and heads["FM-003-Q1"][0] == "",
        seen(said) + f" · {logs} log(s)")


ROWS = (rows_form, rows_records, rows_minting, rows_branches, rows_binding, rows_commands, rows_before, rows_record_names, rows_given_again,
        rows_renumber, rows_revoke, rows_unborn, rows_one_log)


# --- the mutants ------------------------------------------------------------------------------------------------------------------

MUTANTS = (
    ("the head found by `line_author`: the reader goes back to the line", "answer_commit",
     'return answer_commits([t]).get(t.get("ask_id") or "", ("", ""))',
     'return (line_author(TRACKER_DIR / t["file"], "answer:")[3], "")', (rows_binding,)),
    ("a trailer matched by its prefix: Q12 answers Q1", "answer_commits",
     "if value in found and len(parents.split()) == 1:",
     "value = next((a for a in found if value.startswith(a)), value)\n            if value in found and len(parents.split()) == 1:", (rows_binding,)),
    ("the question left out of the binding", "answer_commits",
     "elif put_ask_of(parse_frontmatter(at)[0]) != put_ask(t):", "elif put_ask_of(parse_frontmatter(at)[0])[1:] != put_ask(t)[1:]:", (rows_binding,)),
    ("the binding compares the question alone", "answer_commits",
     "elif put_ask_of(parse_frontmatter(at)[0]) != put_ask(t):", "elif put_ask_of(parse_frontmatter(at)[0])[0] != put_ask(t)[0]:", (rows_binding,)),
    ("no check for two heads", "answer_commits", "if len(heads) > 1:", "if False:", (rows_binding,)),
    ("C4 without the history read", "ask_numbers", 'if vcs() == "git" and rev:', 'if False:', (rows_minting,)),
    ("C5 against the branch's own base", "proposed_id_findings", "t_open, t_put, t_records = held_ids(there)", "t_open, t_put, t_records = held_ids(base)", (rows_branches,)),
    ("C5 without the default branch's records", "proposed_id_findings",
     "theirs = {n for n in (ask_number(a, tid) for a in [t_open, *t_records]) if n}", "t_records = {}\n        theirs = {n for n in (ask_number(a, tid) for a in [t_open]) if n}", (rows_branches,)),
    ("signers read from the checkout", "verified_as", 'v = vcs_process("git", *signers_args(), "log"', 'v = vcs_process("git", "log"', (rows_binding,)),
    ("the next number from the front matter alone", "file_numbers", '[t.get("ask_id") or ""] + [i for i, _d in t.get("asks_ids") or []]', '[t.get("ask_id") or ""]', (rows_records, rows_minting)),
    ("`--answer` by tracker id on an ask with an id", "answer_cmd", "if held and not by_id:", "if False:", (rows_commands,)),
    ("C2 off", "id_moves", "if which:", "if False:", (rows_minting, rows_binding)),
    ("the walk's id rules read a tracker with no file", "id_walk_problems", 'for t in trackers if t.get("file")}', "for t in trackers}", (rows_minting,)),
    ("the answer's change rule reads a tracker with no file", "answer_change_problems", 'for t in trackers if t.get("file")}', "for t in trackers}",
     (rows_minting,)),
    ("a renumbering passes with no record wherever it stands", "id_walk_problems",
     'if move[0] == "gone" and move[2] == "renumbered" and move[1] in renumber_repairs(t, rel, [blobs.get(f"{b}:{rel}") or "" for b in bases]):',
     'if move[0] == "gone" and move[2] == "renumbered":', (rows_renumber,)),
    ("`--revoke` chooses by `done:` alone", "revoke_cmd", "    if by_id:\n", "    if False:\n", (rows_revoke,)),
    ("an answer with an id made on an unborn branch", "answer_cmd", 'if held and vcs() == "git" and not head_commit():', "if False:", (rows_unborn,)),
    ("the gate reads each answer's history alone", "lint", "    answer_commits(trackers)  ", "    None  ", (rows_one_log,)),
    ("`--answered` names a record by its bare id", "newest_record_id", 'return record_name(m.group(1), m.group(2), record_ids(body)) if m else ""',
     'return m.group(1) if m else ""', (rows_record_names,)),
    ("a record named without its date", "record_name", 'return f"{aid} of {day}" if sum(i == aid for i, _d in records) > 1 else aid', "return aid",
     (rows_record_names,)),
    ("a half-written answer given again by its tracker", "dirty_refusal", '(now_fm.get("ask-id") or "").strip() or tid', "tid", (rows_given_again,)),
)


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
