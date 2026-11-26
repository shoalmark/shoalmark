"""What an import attests: the Owner's own signed import commit — it carries `Tracker-import: <repository> <commit>` and verifies as the
Owner's by the check the frozen rule makes — attests every guarded line of each open tracker it adds, as that commit holds them.

A tracker it adds is one that no file of its id stands for at any parent. Each rule that asks who set one of those lines reads the import's
verified Owner, and each rule that asks whether that one held the right takes it as held: an ask it brings stays in the Owner's queue, an
answer it brings counts with the import as its commit, the records it brings stand as written, and the numbers its copy shows are used.
A change after the import is judged as ever, by its own commit. A seat's import, an unsigned one, one signed with a key the signers file
does not hold, and one without the trailer in its form attest nothing: their lines are credited to their committer, as ever. A tracker an
import adds already Shipped or Closed is the frozen rule's, and is not attested.

Each row builds its history in a scratch repository — test_ask_ids' `Repo`: a bare `origin` whose `main` is the default branch, the Owner
named `signed`, their key in the default branch's signers file, a planner seat — where the seat has put two asks on `main`. On a branch
`import`, the Owner's signed import adds four open trackers as the repository they come from held them, their history left there: an open
ask a seat put there, above the record of one answered before it; a standing answer beside its ask id; two records whose signed lines name
commits this history does not hold; and one In Progress with its triage keys. Each row runs the tool in this process and states its
verdict as one check made of steps, each of which must hold. Each mutant patches one function of the imported module and must turn at
least one row red. A function this tool lacks fails the row that asks for it. One row puts the project one folder below the top of a
repository of its own and asks the import's reader alone, with the import's verification and its held-parents test stubbed: a run from
below the top is refused until such a project is read as one at the top, and that verification rests on the same reading.

A merge that is the import attests what its own change adds, in every rule: no commit's change holds the lines a merge wrote, so the
import sets them. An import whose parent's tree this clone cannot read — a partial clone whose origin is out of reach — attests nothing.

Run: `python3 test_import_attests.py` — exit 1 on a failure; `python3 test_import_attests.py rows_<name> …` runs those rows alone, without
the mutants, and with `--with-mutants` beside them, with the mutants that run those rows; `--no-mutants` runs every row and no mutant.
test_shoalmark.py runs it as it runs test_frozen_import.py. No network: every repository is a scratch one, `origin` a bare one beside it.
"""
import contextlib
import inspect
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
from test_ask_ids import CONFIG, OWNER, REL, SEAT, SINCE, Repo, answered, ask, git, record, run, text, write  # noqa: E402

FOREIGN = "766476abcaab912a1f752d67d28fa5cd5bc93d36"            # a commit of the repository the trackers come from: this one does not hold it
TRAILER = f"Tracker-import: shoalmark/shoalmark {FOREIGN}"
IMPORTED = ("FM-201", "FM-202", "FM-203", "FM-204")
ANSWER = "accepted - yes, as proposed"
STRANGER = ("Stranger", "stranger@example.invalid")             # an identity no seat holds
NO_ID = "changes the answer to {0} and does not name it"
NO_COMMIT = "no commit answers {0}"


class Steps:
    """One row made of several steps: every step must hold; what each saw is kept for the row's report."""

    def __init__(self):
        self.ok, self.saw = True, []

    def __call__(self, what, ok, said=None, extra=""):
        self.ok = self.ok and bool(ok)
        self.saw.append(f"{what}: {'ok' if ok else 'NO'}" + (f" {seen(said)}" if said else "") + (f" {extra}" if extra else ""))
        return ok

    def add(self, add, label):
        add(label, self.ok, " || ".join(self.saw))


def said_lines(said):
    return [l.strip() for l in said[2].splitlines() if l.strip()]


def seen(said):
    code, out, err = said
    return f"exit {code}: " + " | ".join(l.strip() for l in (err + out).splitlines() if l.strip() and "FM-" in l)[:900]


def named(said, ids):
    """The ids of `ids` that a line of the run's stderr names — a note refuses nothing, and is not counted."""
    return [tid for tid in ids if any(f"{tid}:" in l and not l.startswith("note:") for l in said_lines(said))]


def refusal(said, tid, *words):
    """The run refused (exit 4), and one line of its stderr names `tid` and carries every one of `words`."""
    return said[0] == fm.EXIT_LINT and any(f"{tid}:" in l and all(w in l for w in words) for l in said_lines(said))


# --- the fixture ------------------------------------------------------------------------------------------------------------------

def answer_lines(by=OWNER[0]):
    return f'answer: "{ANSWER}"\nanswered: {SINCE}\nanswered-by: {by}\n'


def imported():
    """The four open trackers as the repository they come from held them."""
    return {
        "FM-201": text("FM-201", ask(q="Ship the open one?", aid="FM-201-Q2"), asks=record("FM-201-Q1", "Ship its first part?", ANSWER, sha=FOREIGN[:7])),
        "FM-202": text("FM-202", ask(q="Ship the answered one?", aid="FM-202-Q1", move="build") + answer_lines()),
        "FM-203": text("FM-203", "next: build\n", asks=record("FM-203-Q1", "Ship the first?", ANSWER, sha=FOREIGN[:7]) + "\n"
                       + record("FM-203-Q2", "Ship the second?", ANSWER, sha="1234567")),
        "FM-204": text("FM-204", f"triaged: {SINCE}\ntier: P1\nrank: 2\nkind-of-problem: complicated\nnext: build\n"),
    }


def commit(r, message, who=SEAT, key=None, trailers=()):
    """Everything staged and committed by `who` — signed with `key`, one of the fixture's two keys, where one is named — with `trailers`
    as message lines. Its hash."""
    run(r.root, "--print-written", who=who)
    git(r.root, "add", "-A")
    extra = [x for t in trailers for x in ("-m", t)]
    git(r.root, "commit", "-q", "--allow-empty", "-m", message, *extra, *(["-S"] if key else []), who=who, sign=r.keys[key] if key else None)
    return r.head()


def made_import(r, who=OWNER, key="owner", trailer=TRAILER, bodies=None):
    """The import on a branch `import` cut from where `r` stands: each of `bodies` — the four trackers, where none are given — written,
    and committed by `who`, signed with `key` where one is named, carrying `trailer` where one is given. Its commit."""
    r.switch("-c", "import")
    for tid, body in (imported() if bodies is None else bodies).items():
        write(r.root, tid, body)
    return commit(r, "the trackers, imported", who, key, (trailer,) if trailer else ())


def before(area):
    """The ledger before the import, on `main` and pushed: two trackers, each with an ask the planner seat put."""
    r = Repo(area, {"FM-001": text("FM-001"), "FM-002": text("FM-002")})
    for tid in ("FM-001", "FM-002"):
        r.write(tid, text(tid, ask(q=f"Ship {tid}?", aid=f"{tid}-Q1")))
    commit(r, "the asks, put")
    git(r.root, "push", "-q", "origin", "main")
    return r


def copied(seed, area):
    """`seed` again under `area`, with an `origin` of its own: a Repo whose folders are the copy's."""
    shutil.copytree(seed.base, area)
    twin = Repo.__new__(Repo)
    twin.base, twin.root, twin.origin = area, area / "wc", area / "origin.git"
    twin.keys = {name: area / f"key-{name}" for name in seed.keys}
    git(twin.root, "remote", "set-url", "origin", str(twin.origin))
    git(twin.root, "config", "user.signingkey", str(twin.keys["owner"]))
    return twin


_SEEDS = {}


def seeded(area, kind):
    """A copy of the row area's seed: "before" the import, or "import" — the Owner's signed import of the four trackers on its branch
    `import`. Each seed is built once under the folder a run's rows share."""
    home = area.parent
    if (home, "before") not in _SEEDS:
        _SEEDS[(home, "before")] = before(home / "seed-before")
    if kind == "import" and (home, "import") not in _SEEDS:
        r = copied(_SEEDS[(home, "before")], home / "seed-import")
        made_import(r)
        _SEEDS[(home, "import")] = r
    return copied(_SEEDS[(home, kind)], area)


def with_rights(r, rights):
    """`main` with `rights` as the configuration's `[rights]` table: the Owner's signed commit, pushed."""
    (r.root / "shoalmark.toml").write_text(CONFIG + "[rights]\n" + rights, encoding="utf-8")
    commit(r, "the rights", OWNER, "owner")
    git(r.root, "push", "-q", "origin", "main")


@contextlib.contextmanager
def reading(root):
    """The tool configured on `root` in this process, as a run there reads it — its trackers by id — and on this folder again after."""
    saved = {k: os.environ.pop(k) for k in [k for k in os.environ if k.startswith("GIT_")]}
    mine = dict(GIT_CONFIG_GLOBAL=os.devnull, GIT_CONFIG_NOSYSTEM="1", GIT_TERMINAL_PROMPT="0")
    os.environ.update(mine)
    try:
        fm.configure(root)
        yield {t["id"]: t for t in fm.load_trackers()}
    finally:
        for k in mine:
            os.environ.pop(k, None)
        os.environ.update(saved)
        fm.configure(HERE)


def author_of(ts, tid, needle):
    """Who `line_author` says set the line `needle` of `tid`: (name, email, how, commit)."""
    return tuple(fm.line_author(fm.TRACKER_DIR / ts[tid]["file"], needle))


# --- the import attests the open trackers it adds: --check refuses nothing of theirs ------------------------------------------------

def rows_check(area, add):
    r = seeded(area, "import")
    s = Steps()
    said = r.check()
    s("on its branch: --check passes, and names none of the four", said[0] == 0 and not named(said, IMPORTED), said)
    r.land("import")
    said = r.check()
    s("landed on main: --check passes, and names none of the four", said[0] == 0 and not named(said, IMPORTED), said)
    s.add(add, "the Owner's signed import of four open trackers — an open ask, a standing answer beside its id, records whose signed lines "
               "name commits this history does not hold, triage keys — passes --check on its branch and landed")


def rows_modified(area, add):
    r = seeded(area, "before")
    r.switch("-c", "import")
    for tid, body in imported().items():
        write(r.root, tid, body)
    write(r.root, "FM-001", answered(r.read("FM-001"), ANSWER))
    moved = f"{REL}/FM-002-moved.md"
    body = answered(r.read("FM-002"), ANSWER)
    git(r.root, "mv", f"{REL}/FM-002-x.md", moved)
    with open(r.root / moved, "w", encoding="utf-8", newline="\n") as f:
        f.write(body)
    commit(r, "the trackers, imported", OWNER, "owner", (TRAILER,))
    s = Steps()
    said = r.check()
    s("FM-001, which the import changes, is judged: its answer names no id, and no commit gives it",
      refusal(said, "FM-001", NO_ID.format("FM-001-Q1")) and refusal(said, "FM-001", NO_COMMIT.format("FM-001-Q1")), said)
    s("FM-002, whose file the import moves while its id stands at the parent, is judged the same",
      refusal(said, "FM-002", NO_ID.format("FM-002-Q1")) and refusal(said, "FM-002", NO_COMMIT.format("FM-002-Q1")), said)
    s("none of the four it adds is named", not named(said, IMPORTED), said)
    s.add(add, "the Owner's signed import that also answers a tracker it changes, and one whose file it moves: those two are judged as ever "
               "and refused, the four it adds are not")


# --- who set a line: the import's verified Owner, each right taken as held ---------------------------------------------------------

def rows_queue(area, add):
    r = seeded(area, "import")
    sha = r.head()
    s = Steps()
    for where in ("on its branch", "landed on main"):
        with reading(r.root) as ts:
            queue = sorted(t["id"] for t, _age, _held in fm.owner_queue(list(ts.values())))
            bad = [t["id"] for t, _why in fm.malformed_asks(list(ts.values()))]
            who = author_of(ts, "FM-201", "next: owner")
        s(f"{where}: the Owner's queue, built offline, holds FM-201 beside the two asks put before", queue == ["FM-001", "FM-002", "FM-201"], extra=repr(queue))
        s(f"{where}: no ask is sent back", not bad, extra=repr(bad))
        s(f"{where}: FM-201's `next: owner` is the import's, by the Owner", who == (OWNER[0], OWNER[1], "git", sha), extra=repr(who))
        if where == "on its branch":
            r.land("import")
    s.add(add, "the open ask the import brings is in the Owner's queue, built offline, on its branch and landed: its `next: owner` is the "
               "import's own line, by its Owner")


def rows_owner(area, add):
    s = Steps()
    r = seeded(area.parent / f"{area.name}-by", "before")
    sha = made_import(r, bodies={"FM-206": text("FM-206", ask(q="Ship the sixth?", aid="FM-206-Q1", move="build") + answer_lines("Planner"))})
    said = r.check()
    s("an answer the import brings under another name is refused, naming the import's Owner as the one who gave it",
      refusal(said, "FM-206", f"`answered-by: Planner` but the commit that answers FM-206-Q1, {sha[:7]}, is `Owner`'s"), said)
    r = seeded(area.parent / f"{area.name}-ask", "before")
    with_rights(r, 'owner = ["answer"]\n')
    made_import(r)
    said = r.check()
    s("the Owner holding `answer` alone: the import's `next: owner`, ask lines, records and triage keys pass", said[0] == 0 and not named(said, IMPORTED), said)
    r = seeded(area.parent / f"{area.name}-answer", "before")
    with_rights(r, 'owner = ["ask", "close", "triage"]\nplanner = ["answer", "ask", "close", "triage"]\n')
    made_import(r, bodies={"FM-202": imported()["FM-202"],
                           "FM-205": text("FM-205", ask(q="Ship the old one?", move="build") + answer_lines())})
    said = r.check()
    s("the Owner without `answer`: the import's answer beside its id, and one given before ask ids, pass", said[0] == 0 and not named(said, ("FM-202", "FM-205")), said)
    s.add(add, "each rule that asks who set a line the import brings reads its Owner, and each right it asks is taken as held: an answer "
               "under another name is refused naming the Owner; with the Owner holding `answer` alone, or every right but `answer`, it passes")


# --- answers and records: the import's answer counts, with the import as its commit, and its records stand ----------------------------

def rows_answer_counts(area, add):
    r = seeded(area, "import")
    sha = r.head()
    s = Steps()
    for where in ("on its branch", "landed on main"):
        with reading(r.root) as ts:
            got = fm.answer_commit(ts["FM-202"])
            relations = [fm.record_relation(ts[tid]) for tid in ("FM-201", "FM-203")]
            newest = [fm.newest_record_id(ts[tid]) for tid in ("FM-201", "FM-203")]
        s(f"{where}: the answer beside FM-202-Q1 counts, the import its commit", got == (sha, ""), extra=repr(got))
        s(f"{where}: the records stand as written — each relation as its line says it, the newest named by its id",
          relations == [("accepted the proposal", "")] * 2 and newest == ["FM-201-Q1", "FM-203-Q2"], extra=repr((relations, newest)))
        if where == "on its branch":
            r.land("import")
    said = run(r.root, "--clear-ask", "FM-202-Q1", "build", who=SEAT)
    body = r.read("FM-202")
    s("the seat acts on it: --clear-ask writes its record, the signed line naming the import",
      said[0] == 0 and f"**answered** — {ANSWER} · Owner\n" in body and f"**signed** — {sha[:7]} · G\n" in body, said,
      repr(body[body.find("**FM-202-Q1**"):]))
    commit(r, "FM-202: acted on")
    said = r.check()
    s("…and --check passes it", said[0] == 0 and not named(said, IMPORTED), said)
    s.add(add, "the answer the import brings counts, the import its commit, on its branch and landed, and its record names the import; "
               "the records it brings stand as written")


# --- ask numbers: read from the imported file as the import holds it, beside the history after it -------------------------------------

def rows_ask_numbers(area, add):
    r = seeded(area, "import")
    s = Steps()
    with reading(r.root) as ts:
        nxt = fm.next_ask_id(ts["FM-203"], fm.ask_numbers(ts["FM-203"]))
    s("FM-203's next ask follows its records: FM-203-Q3", nxt == "FM-203-Q3", extra=nxt)
    r.write("FM-203", text("FM-203", "next: build\n"))
    commit(r, "FM-203: its records moved out")
    said = r.check()
    s("a seat's later commit takes FM-203's records out of the file, and passes", said[0] == 0 and not named(said, IMPORTED), said)
    with reading(r.root) as ts:
        nxt = fm.next_ask_id(ts["FM-203"], fm.ask_numbers(ts["FM-203"]))
    s("…and the next ask on FM-203 still follows the numbers the import's copy shows: FM-203-Q3", nxt == "FM-203-Q3", extra=nxt)
    r.write("FM-203", text("FM-203", ask(q="Ship the third?", aid="FM-203-Q1")))
    commit(r, "FM-203: an ask, put")
    said = r.check()
    s("an ask put after it as FM-203-Q1 is refused, naming FM-203-Q3",
      refusal(said, "FM-203", "puts FM-203-Q1, and its number is not above every number FM-203 has used — the highest is FM-203-Q2: put it as FM-203-Q3"), said)
    git(r.root, "reset", "-q", "--hard", "HEAD~1")
    r.write("FM-203", text("FM-203", ask(q="Ship the third?", aid="FM-203-Q3")))
    commit(r, "FM-203: an ask, put")
    said = r.check()
    s("…and put as FM-203-Q3, it passes", said[0] == 0 and not named(said, IMPORTED), said)
    s.add(add, "the numbers FM-203's ids used are read from the file as the import holds it: with its records taken out later, the next ask "
               "is still FM-203-Q3, and an ask put as FM-203-Q1 is refused")


# --- after the import: every change judged as today ---------------------------------------------------------------------------

def rows_after_import(area, add):
    r = seeded(area, "import")
    sha = r.head()
    s = Steps()
    said = r.check()
    s("the import's own lines pass", said[0] == 0 and not named(said, IMPORTED), said)
    write(r.root, "FM-201", answered(r.read("FM-201"), ANSWER))
    commit(r, "FM-201: answered by hand", OWNER, "owner")
    said = r.check()
    s("an answer to FM-201-Q2 the Owner writes by hand later, signed, with no `Answers:`, is refused",
      refusal(said, "FM-201", NO_ID.format("FM-201-Q2")) and refusal(said, "FM-201", NO_COMMIT.format("FM-201-Q2")), said)
    git(r.root, "reset", "-q", "--hard", "HEAD~1")
    said = run(r.root, "--answer", "FM-201-Q2", "accept")
    given = r.head()
    with reading(r.root) as ts:
        got = fm.answer_commit(ts["FM-201"])
    s("…given by `--answer`, its own `Answers:` commit, it counts", said[0] == 0 and got == (given, ""), said, repr(got))
    said = r.check()
    s("…and --check passes", said[0] == 0 and not named(said, IMPORTED), said)
    r.write("FM-202", r.read("FM-202").replace(f'answer: "{ANSWER}"', f'answer: "{ANSWER}, and more"'))
    later = commit(r, "FM-202: the answer, reworded")
    said = r.check()
    with reading(r.root) as ts:
        got, who = fm.answer_commit(ts["FM-202"]), author_of(ts, "FM-202", "answer:")
    s("the answer the import brought, changed later by a seat, is that seat's change: refused as one that names no id",
      refusal(said, "FM-202", NO_ID.format("FM-202-Q1")) and who == (SEAT[0], SEAT[1], "git", later), said, repr(who))
    s("…and the import no longer gives it", got[0] == sha and got[1].startswith(f"the answer here is not the one {sha[:7]} gave FM-202-Q1"), extra=repr(got))
    git(r.root, "reset", "-q", "--hard", "HEAD~1")
    r.write("FM-204", r.read("FM-204").replace("tier: P1", "tier: P2"))
    later = commit(r, "FM-204: its tier", STRANGER)
    said = r.check()
    with reading(r.root) as ts:
        who = author_of(ts, "FM-204", "tier:")
    s("a triage key changed later by an identity that is no seat is credited to its commit, and refused",
      refusal(said, "FM-204", "is not a seat") and who == (STRANGER[0], STRANGER[1], "git", later), said, repr(who))
    s.add(add, "after the import every change is judged as today: a later answer without its `Answers:` commit is refused and one with it "
               "counts; the imported answer changed later, and a triage key changed later by no seat, are each their own commit's, and refused")


# --- what attests nothing: a seat's import, an unsigned one, one with another key, one without the trailer -------------------------------

UNVERIFIED = (
    ("a seat's import, unsigned", SEAT, None, TRAILER),
    ("a seat's import, signed with the Owner's key", SEAT, "owner", TRAILER),
    ("the Owner's import, unsigned", OWNER, None, TRAILER),
    ("the Owner's import, signed with a key the signers file does not hold", OWNER, "other", TRAILER),
    ("the Owner's signed commit without the trailer", OWNER, "owner", None),
    ("the Owner's signed commit whose trailer names no commit", OWNER, "owner", "Tracker-import: shoalmark/shoalmark"),
)


def rows_attests_nothing(area, add):
    s = Steps()
    for n, (what, who, key, trailer) in enumerate(UNVERIFIED):
        r = seeded(area.parent / f"{area.name}-{n}", "before")
        sha = made_import(r, who=who, key=key, trailer=trailer)
        said = r.check()
        with reading(r.root) as ts:
            got, by = fm.answer_commit(ts["FM-202"]), author_of(ts, "FM-202", "answer:")
            queue = [t["id"] for t, _age, _held in fm.owner_queue(list(ts.values()))]
        s(f"{what}: the answer beside FM-202-Q1 is its committer's, refused as given by no commit and as a change that names no id",
          refusal(said, "FM-202", NO_ID.format("FM-202-Q1")) and refusal(said, "FM-202", NO_COMMIT.format("FM-202-Q1"))
          and got[0] == "" and by == (who[0], who[1], "git", sha), said, repr((got[0], by)))
        if who == SEAT:
            s(f"{what}: the seat's answer is refused for the right it lacks", refusal(said, "FM-202", "does not hold `answer`"), said)
        verified = who == OWNER and key == "owner"
        s(f"{what}: FM-201's ask is " + ("in the Owner's queue, as any the Owner puts in a signed commit" if verified or who == SEAT
                                         else "sent back: its commit does not verify as the Owner's"),
          ("FM-201" in queue) == (verified or who == SEAT)
          and (verified or who == SEAT or refusal(said, "FM-201", "that set `next: owner` does not verify as the seat `owner`")), said, repr(queue))
    s.add(add, "the same import by a seat — unsigned, or signed with the Owner's key —, by the Owner unsigned or with a key the signers file "
               "does not hold, or the Owner's signed commit without the trailer in its form attests nothing: each line is its committer's, "
               "and refused where it is refused today")


def done(tid, status):
    """A tracker the repository it comes from left `status`, Shipped or Closed, with its answer still beside its ask id."""
    return (f'---\nid: {tid}\nstatus: {status}\nconsidered: none\n{ask(q=f"Ship {tid}?", aid=f"{tid}-Q1", move="build")}{answer_lines()}hook: "h of {tid}"\n'
            f"---\n\n# {tid} — t\n\n## What is true now\n\nDone.\n\n## Done when\n\n- [x] it is.\n\n## Ship log\n\n| Date | Event |\n|---|---|\n| {SINCE} | Filed. |\n")


def rows_done_left(area, add):
    r = seeded(area, "before")
    made_import(r, bodies={"FM-207": done("FM-207", "Shipped"), "FM-208": done("FM-208", "Closed"), "FM-202": imported()["FM-202"]})
    said = r.check()
    s = Steps()
    for tid in ("FM-207", "FM-208"):
        s(f"{tid}, added already {'Shipped' if tid == 'FM-207' else 'Closed'}: its answer is judged as today, refused as given by no commit",
          refusal(said, tid, NO_COMMIT.format(f"{tid}-Q1")), said)
    s.add(add, "a tracker the import adds already Shipped or Closed is not attested: an answer standing beside its id is judged as today")


# --- below the top: the import's reader lists the whole tracker folder -------------------------------------------------------------

@contextlib.contextmanager
def stubbed(**names):
    """Each of `names` put in place of the module's function of that name, and the real one put back after."""
    real = {n: getattr(fm, n) for n in names}
    for n, f in names.items():
        setattr(fm, n, f)
    try:
        yield
    finally:
        for n, f in real.items():
            setattr(fm, n, f)


def rows_below_top_verification_stubbed(area, add):
    """A project one folder below the top of its repository, where the Owner's signed import adds the four open trackers. A run from
    there is refused until a project below the top is read as one at the top, and the import's verification rests on that reading, so
    this row stubs the verification and the held-parents test and asks the import's reader alone."""
    top, key = area / "repo", area / "key-owner"
    proj = top / "project"
    proj.mkdir(parents=True)
    subprocess.run(["ssh-keygen", "-q", "-t", "ed25519", "-N", "", "-f", str(key), "-C", "owner"], check=True, capture_output=True)
    git(top, "init", "-q", "--initial-branch=main")
    (proj / "shoalmark.toml").write_text(CONFIG, encoding="utf-8")
    write(proj, "FM-001", text("FM-001"))
    git(top, "add", "-A")
    git(top, "commit", "-q", "-S", "-m", "the start", who=OWNER, sign=key)
    for tid, body in imported().items():
        write(proj, tid, body)
    git(top, "add", "-A")
    git(top, "commit", "-q", "-S", "-m", "the trackers, imported", "-m", TRAILER, who=OWNER, sign=key)
    sha = git(top, "rev-parse", "HEAD").strip()
    with stubbed(import_verified=lambda commit, name, email: True, commits_held=lambda revs: True), reading(proj):
        got = {tid: [c for c, _name, _text in held] for tid, held in fm.import_attests().items()}
    s = Steps()
    s("the reader finds the four open trackers the import adds, each attested by the import, and not the one its parent holds",
      got == {tid: [sha] for tid in IMPORTED}, extra=repr(got))
    s.add(add, "below the top, with the import's verification and its held-parents test stubbed: the import's reader lists the whole "
               "tracker folder at the import and at its parent, and finds the four open trackers the Owner's signed import adds")


# --- a merge that is the import: it attests what its own change adds, in every rule -------------------------------------------------

LEGACY = text("FM-205", ask(q="Ship the old one?", move="build") + answer_lines())    # an answer given before ask ids: no `ask-id:` beside it


def merged(r, bodies, side=None):
    """On the branch `r` stands on, the Owner's signed merge of a side branch cut from there — whose own commit, a seat's, writes
    `side`'s trackers, or a note on FM-001 where none are given — that adds `bodies` in the merge's own change, with the trailer. Its
    commit."""
    here = git(r.root, "rev-parse", "--abbrev-ref", "HEAD").strip()
    r.switch("-c", f"side-of-{here}")
    for tid, body in (side or {"FM-001": r.read("FM-001").replace("One thing is left.", "One thing is left, on the side.")}).items():
        write(r.root, tid, body)
    commit(r, "side: a change of its own")
    r.switch(here)
    git(r.root, "merge", "-q", "--no-ff", "--no-commit", f"side-of-{here}", who=OWNER)
    for tid, body in bodies.items():
        write(r.root, tid, body)
    return commit(r, "the trackers, imported by a merge", OWNER, "owner", (TRAILER,))


def rows_merge_import(area, add):
    r = seeded(area, "before")
    sha = merged(r, dict(imported(), **{"FM-205": LEGACY}))
    s = Steps()
    said = r.check()
    s("--check passes, and names none of the five the merge adds", said[0] == 0 and not named(said, IMPORTED + ("FM-205",)), said)
    with reading(r.root) as ts:
        queue = sorted(t["id"] for t, _age, _held in fm.owner_queue(list(ts.values())))
        bad = [t["id"] for t, _why in fm.malformed_asks(list(ts.values()))]
        who = [author_of(ts, "FM-201", "next: owner"), author_of(ts, "FM-205", "answer:")]
        got = fm.answer_commit(ts["FM-202"])
    s("the Owner's queue, built offline, holds FM-201 beside the two asks put before, and no ask is sent back",
      queue == ["FM-001", "FM-002", "FM-201"] and not bad, extra=repr((queue, bad)))
    s("FM-201's `next: owner` and FM-205's answer with no ask id are the merge's own lines, set by the import, by the Owner",
      who == [(OWNER[0], OWNER[1], "git", sha)] * 2, extra=repr(who))
    s("the answer beside FM-202-Q1 counts, the merge its commit", got == (sha, ""), extra=repr(got))
    s.add(add, "the Owner's signed merge that adds the trackers in its own change is the import in every rule: the open ask stays in the "
               "Owner's queue, `next: owner` and an answer with no ask id pass as the import's, and the answer beside its id counts")


def rows_parent_unread(area, add):
    """The import on its branch, on top of a seat's commit `main` does not hold. A clone that holds no tree it did not check out
    (`--filter=tree:0`) reads `main`'s history in full while `origin` is there; then `origin` is out of reach, and git can read the
    import's parent's tree no more, while the import still verifies and its parent is held."""
    r = seeded(area, "before")
    r.switch("-c", "import")
    (r.root / "notes.txt").write_text("a note\n", encoding="utf-8")
    parent = commit(r, "a note, before the import")
    for tid, body in imported().items():
        write(r.root, tid, body)
    sha = commit(r, "the trackers, imported", OWNER, "owner", (TRAILER,))
    git(r.root, "push", "-q", "origin", "import")
    with reading(r.root):
        full = {tid: [c for c, _name, _text in held] for tid, held in fm.import_attests().items()}
    for k, v in (("uploadpack.allowFilter", "true"), ("uploadpack.allowAnySHA1InWant", "true")):
        git(r.origin, "config", k, v)
    pc = area / "partial"
    git(area, "clone", "-q", "--filter=tree:0", "--no-local", "--branch", "import", f"file://{r.origin}", str(pc))
    for k, v in (("user.name", OWNER[0]), ("user.email", OWNER[1]), ("gpg.ssh.allowedSignersFile", f"{REL}/allowed_signers")):
        git(pc, "config", k, v)
    git(pc, "remote", "set-head", "origin", "main")
    git(pc, "log", "-p", "--format=%H", "origin/main")
    r.origin.rename(r.origin.with_name("origin-out-of-reach.git"))
    unread = subprocess.run(["git", "-C", str(pc), "cat-file", "-e", f"{parent}^{{tree}}"], capture_output=True).returncode != 0
    with reading(pc):
        verified, held = fm.import_verified(sha, *OWNER), fm.commits_held([parent])
        got = {tid: [c for c, _name, _text in held_] for tid, held_ in fm.import_attests().items()}
    s = Steps()
    s("in the full clone the import attests the four it adds", full == {tid: [sha] for tid in IMPORTED}, extra=repr(full))
    s("in the partial clone, origin out of reach, the import verifies and its parent is held, while the parent's tree cannot be read",
      verified and held and unread, extra=repr((verified, held, unread)))
    s("…and the import attests nothing", got == {}, extra=repr(got))
    s.add(add, "an import whose parent's tree this clone cannot read — a partial clone whose origin is out of reach — attests nothing, "
               "though it verifies and its parent is held")


ROWS = (rows_check, rows_modified, rows_queue, rows_owner, rows_answer_counts, rows_ask_numbers, rows_after_import, rows_attests_nothing,
        rows_done_left, rows_below_top_verification_stubbed, rows_merge_import, rows_parent_unread)


@contextlib.contextmanager
def mutated(name, *pairs):
    """`fm.<name>` replaced by a copy of its own source with each (old, new) of `pairs` replaced — each old text in it exactly once —,
    compiled in the module's namespace, and put back after."""
    real = getattr(fm, name)
    src = textwrap.dedent(inspect.getsource(real))
    for old, new in pairs:
        if src.count(old) != 1:
            raise AssertionError(f"{name}: {old[:60]!r} is not in its source exactly once")
        src = src.replace(old, new)
    exec(compile(src, fm.__file__, "exec"), fm.__dict__)
    try:
        yield
    finally:
        setattr(fm, name, real)


# Each mutant: (what it breaks, the function it patches, its (old, new) replacements, the rows that must catch it).
MUTANTS = (
    ("the attestation taken for a commit that does not verify", "import_attests",
     (("or not import_verified(sha, name, email) ", ""),), (rows_attests_nothing,)),
    ("a trailer read in any form", "import_attests",
     (('if not import_value(block.strip("\\n"))', 'if not trailer_values(block.strip("\\n"), IMPORT_TRAILER)'),), (rows_attests_nothing,)),
    ("any of the Owner's signed commits attesting, without the trailer", "import_attests",
     (('"-i", f"--grep=^{IMPORT_TRAILER}:", ', ""), ('not import_value(block.strip("\\n")) or ', "")), (rows_attests_nothing,)),
    ("a tracker the import changes counted as one it adds", "import_attests", (("if tid not in before}", "}"),), (rows_modified,)),
    ("a tracker the import adds already Shipped or Closed attested too", "import_attests",
     (('extract(ROOT / rel, text)["status"] in OPEN_STATUSES', "True"),), (rows_done_left,)),
    ("a tracker counted as added by its file, not its id", "import_attests",
     (("before = set().union(*(ids(p) for p in parents))", "before = set().union(*(ids(p).values() for p in parents))"),
      ("if tid not in before}", "if n not in before}")), (rows_modified,)),
    ("what an import attests kept from one repository to the next", "configure",
     (("    _ATTESTS = None ", "    pass "),), (rows_check, rows_attests_nothing)),
    ("the import's numbers held against its own change", "imported_numbers", ((" if reaches(sha, rev)", ""),), (rows_check,)),
    ("the numbers read from the file as it is now, not as the import holds it", "imported_numbers",
     (("file_numbers(fresh_tracker(t, text))", "file_numbers(t)"),), (rows_ask_numbers,)),
    ("ask numbers read from the history alone, as before", "ask_numbers", (("        used |= imported_numbers(t, rev)\n", ""),), (rows_ask_numbers,)),
    ("the import's answer no candidate: no commit gives it, as before", "answer_commits", (('import_attests().get(t["id"], ())', "()"),),
     (rows_check, rows_answer_counts)),
    ("the import's answer credited to the name its line gives", "answer_commits",
     (("keep.append((sha, name, held))", 'keep.append((sha, t.get("answered_by"), held))'),), (rows_owner,)),
    ("the attestation taken for an answer changed after the import", "answer_commits",
     (("keep.append((sha, name, held))", 'keep.append((sha, name, (TRACKER_DIR / t["file"]).read_text(encoding="utf-8")))'),), (rows_after_import,)),
    ("the import's own answer judged as a change that names no id, as before", "answer_change_problems",
     (("if import_adds(rels[rel], commit):", "if False:"),), (rows_check,)),
    ("an answer changed after the import passed as the import's", "answer_change_problems",
     (("if import_adds(rels[rel], commit):", 'if import_attests().get(rels[rel]["id"]):'),), (rows_after_import,)),
    ("the import's own change judged for the rights its Owner lacks, as before", "rights_problems",
     (("if import_adds(t, commit):", "if False:"),), (rows_owner,)),
    ("a change after the import taken as the Owner's, each right held", "rights_problems",
     (("if import_adds(t, commit):", 'if import_attests().get(t["id"]):'),), (rows_after_import,)),
    ("an answer with no ask id that the import wrote judged for the right, as before", "lint",
     (('attested = how == "git" and import_adds(t, commit)', "attested = False"),), (rows_owner,)),
    ("the tracker folder listed without `--full-tree`: below the top it lists nothing", "import_attests",
     (('"--full-tree", ', ""),), (rows_below_top_verification_stubbed,)),
    ("`line_author`'s readers without the import: a line a merge that is the import wrote names no commit", "line_author",
     (('out = import_setter(rel, key, line) or (None, None, "unattributed", "")', 'out = (None, None, "unattributed", "")'),), (rows_merge_import,)),
    ("an import whose parent's tracker folder this clone cannot read attests what that folder's listing misses", "import_attests",
     (("if any(names(p) is None for p in parents):", "if False:"),), (rows_parent_unread,)),
)


def run_mutants(*, results=None, only=None):
    """Each mutant, as (label, whether it turned a row red, what it saw): its rows run under it, and at least one must fail — with `only`,
    the mutants whose rows `only` names."""
    results = [] if results is None else results
    for label, name, pairs, rows in MUTANTS:
        if only and not any(rows_.__name__ in only for rows_ in rows):
            continue
        reds, broke = [], ""
        try:
            with mutated(name, *pairs), tempfile.TemporaryDirectory(prefix="shoalmark-attests-m-") as tmp:
                area = Path(tmp).resolve()
                for n, rows_ in enumerate(rows):
                    rows_(area / f"m{n}", lambda l, ok, saw="": reds.append(l) if not ok else None)
        except AssertionError as e:
            broke = str(e)
        except Exception as e:
            reds.append(f"a row crashed: {type(e).__name__}: {str(e)[:120]}")
        finally:
            fm.configure(HERE)
        results.append((f"mutant · {label}: at least one row turns red", bool(reds) and not broke, broke or "no row turned red"))
    return results


def run_checks(*, results=None, mutants=True, rows=None):
    """Every row — or the row functions `rows` names — then every mutant, as (label, ok, what it saw)."""
    results = [] if results is None else results
    add = lambda label, ok, saw="": results.append((label, bool(ok), "" if ok else saw))
    with tempfile.TemporaryDirectory(prefix="shoalmark-attests-") as tmp:
        area = Path(tmp).resolve()
        for n, rows_ in enumerate(ROWS):
            if rows and rows_.__name__ not in rows:
                continue
            try:
                rows_(area / f"r{n}", add)
            except (AttributeError, NameError) as e:
                add(f"{rows_.__name__}: this tool lacks what the row asks for — {type(e).__name__}: {e}", False)
            except Exception as e:
                add(f"{rows_.__name__}: a fixture step failed — {type(e).__name__}: {str(e)[:300]}", False, getattr(e, "stderr", "") or "")
    fm.configure(HERE)
    if mutants:
        run_mutants(results=results, only=rows)
    return results


if __name__ == "__main__":
    failed = 0
    picked = [a for a in sys.argv[1:] if a.startswith("rows_")]
    with_mutants = "--with-mutants" in sys.argv or ("--no-mutants" not in sys.argv and not picked)
    for label, ok, detail in run_checks(mutants=with_mutants, rows=picked or None):
        print(("  ok    " if ok else "  FAIL  ") + label + ("" if ok else f"\n        {detail}" if detail else ""), flush=True)
        failed += not ok
    print(f"FAILED: {failed}" if failed else "all green")
    sys.exit(1 if failed else 0)
