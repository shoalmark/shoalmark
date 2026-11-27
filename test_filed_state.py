"""The filed state's class test: a commit the default branch holds is judged by who that branch named as its Owner, and which keys it
held for them, when the commit was filed there — never by what the branch says now; and a commit it does not hold yet, by the state in
force there now — the last one it accepted, never a change it did not accept.

Each row builds its history in a scratch repository — a bare `origin` with `main` as its default branch, the Owner named by two
addresses or one, a test key in the default branch's signers file, pull requests landed by merge commits as a forge's button makes them — runs
the tool in this process, and states its verdict: refused, with the refusal's words, or accepted. The change the rows walk is an
address of the Owner's leaving `owner` and the signers file in two commits: the address that stays enrolled beside it and the key listed for both, then the
other address taken out. `LEAVES` is the address that leaves and `STAYS` the one that stays; `STRANGER` is never named by a state the
default branch accepted, and `NEWCOMER` only by a branch of its own. A row holds its setup and the outcome it shows together, and a row
that refuses something also holds that every earlier answer still counts: each row fails on a tool that judges every commit by the default
branch as it stands, and a function this tool lacks fails the row that asks for it. Each mutant patches one function of the imported
module and must turn at least one row red.

Run: `python3 test_filed_state.py` — exit 1 on a failure; `python3 test_filed_state.py rows_<name> …` runs those rows alone, without the
mutants, and with `--with-mutants` beside them, with the mutants that run those rows. test_shoalmark.py runs it as it runs test_ask_ids.py. No browser and no network: every repository is a scratch one, `origin` a
bare one beside it, and every key is made here.
"""
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))
import shoalmark as fm  # noqa: E402
from test_ask_ids import REL, accepted, answered, ask, git, heads_of, mutated, refused, run, seen, text, write  # noqa: E402

LEAVES = ("Owner", "owner.leaves@example.com")
STAYS = ("Owner", "12345+owner@users.noreply.example.com")
STRANGER = ("Owner", "stranger@example.com")
FORGE = ("Owner", "1234+owner@users.noreply.example.invalid")
NEWCOMER = ("Owner", "newcomer@example.com")
ALICE = ("Alice", "alice@example.com")
BOB = ("Bob", "bob@example.com")
SEAT = ("Planner", "planner@example.com")
TRIAGE = "# Triage\n\n## The intent\n\n- **for** — {0}\n\n## The current path\n\n1. The rows.\n\n## Passes\n\n*None yet.*\n"
EARLIER = ("FM-001", "FM-002", "FM-003", "FM-004", "FM-005", "FM-006")


class Ledger:
    """A scratch clone of a bare `origin` whose `main` is the default branch. `start` commits the configuration, the signers file,
    TRIAGE.md and six trackers under the address that leaves, signed: the first, third, fourth and sixth each with an ask that has an
    id, the second and the fifth each with an ask that has none — every one put by the Owner."""

    def __init__(self, base):
        self.base, self.root, self.origin = base, base / "wc", base / "origin.git"
        self.keys = {name: base / f"key-{name}" for name in ("owner", "second", "branch", "stranger")}
        self.signed, self.plain = True, False

    def start(self, owner=(LEAVES, STAYS), signers=((LEAVES, "owner"),), signed=True, plain=False, who=LEAVES):
        """`signed`: `owner` asks for a signature; `plain`: no `owner` and no `[seats]`, the names of `owner` as `answerers`; `who`: whose commits start it."""
        self.signed, self.plain = signed, plain
        self.root.mkdir(parents=True)
        for name, key in self.keys.items():
            subprocess.run(["ssh-keygen", "-q", "-t", "ed25519", "-N", "", "-f", str(key), "-C", name], check=True, capture_output=True)
        git(self.base, "init", "-q", "--bare", "--initial-branch=main", str(self.origin))
        git(self.root, "init", "-q", "--initial-branch=main")
        for k, v in (("user.name", STAYS[0]), ("user.email", STAYS[1]), ("gpg.format", "ssh"),
                     ("gpg.ssh.allowedSignersFile", f"{REL}/allowed_signers"), ("commit.gpgsign", "false")):
            git(self.root, "config", k, v)
        git(self.root, "remote", "add", "origin", str(self.origin))
        (self.root / ".gitignore").write_text(f"{REL}/index.html\n{REL}/view/\n", encoding="utf-8")
        self.config(owner)
        (self.root / REL).mkdir(parents=True)
        if signers:
            self.signers(*signers)
        self.triage("the rows of a change of the Owner's address")
        for n, aid in ((1, "FM-001-Q1"), (2, ""), (3, "FM-003-Q1"), (4, "FM-004-Q1"), (5, ""), (6, "FM-006-Q1")):
            write(self.root, f"FM-00{n}", text(f"FM-00{n}", ask(q=f"Ship part {n}?", aid=aid)))
        self.commit("the start", who=who, key="owner")
        git(self.root, "push", "-q", "-u", "origin", "main")
        git(self.root, "remote", "set-head", "origin", "main")
        run(self.root, "--print-written")
        if git(self.root, "status", "--porcelain"):
            self.commit("the index, with the default branch known", who=who, key="owner")
            git(self.root, "push", "-q", "origin", "main")
        return self

    def copy(self, base):
        """This ledger again under `base`, with an `origin` of its own."""
        shutil.copytree(self.base, base)
        twin = Ledger(base)
        twin.signed, twin.plain = self.signed, self.plain
        git(twin.root, "remote", "set-url", "origin", str(twin.origin))
        return twin

    def config(self, owner):
        if self.plain:
            names = ", ".join(f'"{who[0]}"' for who in owner)
            (self.root / "shoalmark.toml").write_text(f'name = "filed"\nanswerers = [{names}]\n[kinds]\nFM = "Work"\n', encoding="utf-8")
            return
        line = ", ".join(f'"{who[1]}' + (' signed"' if self.signed else '"') for who in owner)
        (self.root / "shoalmark.toml").write_text(f'name = "filed"\n' + (f"owner = [{line}]\n" if owner else "")
                                                  + f'[kinds]\nFM = "Work"\n[seats]\nplanner = "{SEAT[1]}"\n', encoding="utf-8")

    def signers(self, *pairs, text_=None):
        """The signers file: one line for each (address, key name), in the order given — or `text_`, with `{key}` for a key's text."""
        pub = lambda name: " ".join(self.keys[name].with_suffix(".pub").read_text(encoding="utf-8").split()[:2])
        (self.root / REL / "allowed_signers").write_text(
            text_.format(**{name: pub(name) for name in self.keys}) if text_ is not None else "".join(f"{who[1]} {pub(name)}\n" for who, name in pairs),
            encoding="utf-8")

    def triage(self, words):
        (self.root / REL / "TRIAGE.md").write_text(TRIAGE.format(words), encoding="utf-8")

    def read(self, tid):
        return (self.root / REL / f"{tid}-x.md").read_text(encoding="utf-8")

    def commit(self, message, who, key=None, trailers=()):
        """Everything staged and committed under `who` — signed with the key `key` names — with `trailers` as message lines."""
        run(self.root, "--print-written", who=who)
        git(self.root, "add", "-A")
        extra = [x for t in trailers for x in ("-m", t)]
        git(self.root, "commit", "-q", "--allow-empty", "-m", message, *extra, *(["-S"] if key else []), who=who, sign=self.keys[key] if key else None)
        return git(self.root, "rev-parse", "HEAD").strip()

    def answer(self, tid, who, key, aid="", branch=None, trailers=(), by=None):
        """The answer to `tid`'s ask, committed on a branch of its own under `who`, signed with `key`: its commit. `by`: its `answered-by:`."""
        self.switch("-c", branch or f"answer-{tid.lower()}", "main")
        write(self.root, tid, answered(self.read(tid)) if by is None else answered(self.read(tid), by=by))
        return self.commit(f"{aid or tid}: accepted", who=who, key=key, trailers=((f"Answers: {aid}",) if aid else ()) + tuple(trailers))

    def land(self, branch):
        """`branch` merged into `main` by a merge commit as a forge's button makes one — authored under the address that stays, unsigned —
        `main` pushed, and `origin/main` fetched back."""
        self.switch("main")
        git(self.root, "merge", "-q", "--no-ff", "--no-edit", branch, who=STAYS)
        git(self.root, "push", "-q", "origin", "main")
        git(self.root, "fetch", "-q", "origin")

    def forward(self, branch):
        """`branch` put on `main` as it is — a fast-forward, no merge commit — and `main` pushed."""
        self.switch("main")
        git(self.root, "merge", "-q", "--ff-only", branch, who=STAYS)
        git(self.root, "push", "-q", "origin", "main")
        git(self.root, "fetch", "-q", "origin")

    def settle(self):
        """INDEX.md as it reads on `main` now, committed and pushed where a landing changed what it says."""
        run(self.root, "--print-written")
        if git(self.root, "status", "--porcelain"):
            self.commit("the index, as the default branch reads now", who=STAYS, key=None)
            git(self.root, "push", "-q", "origin", "main")
            git(self.root, "fetch", "-q", "origin")

    def switch(self, *a):
        git(self.root, "switch", "-q", *a)

    def check(self):
        return run(self.root, "--check", who=SEAT)


class Steps:
    """One row made of several runs: every run must hold; what each saw is kept for the row's report."""

    def __init__(self):
        self.ok, self.saw = True, []

    def __call__(self, what, ok, said=None, extra=""):
        self.ok = self.ok and bool(ok)
        self.saw.append(f"{what}: {'ok' if ok else 'NO'}" + (f" {seen(said)}" if said else "") + (f" {extra}" if extra else ""))
        return ok

    def add(self, add, label):
        add(label, self.ok, " || ".join(self.saw))


def stands(said, *besides):
    """The earlier answers — FM-001's by its id, FM-002's by its line — and the asks the Owner put at the start still count: no line the run
    printed, a note aside, names one of their trackers, besides the trackers `besides` names."""
    lines = [l for l in said[2].splitlines() if "note:" not in l]
    return all(not any(f"{tid}:" in l or f"{tid} `" in l for l in lines) for tid in EARLIER if tid not in besides)


def missing(add, label, e):
    """A row whose function this tool lacks: failed, with what it lacks — never a fixture that stops the rows after it."""
    add(label, False, f"this tool lacks it: {type(e).__name__}: {e}")


_SEEDS = {}


def seed(area, state):
    """The ledger `before` the change or `after` it, built once under the folder a run's rows share and copied for each of them: (the
    ledger, the commit of the answer that has an id). Before: the Owner's two answers under the address that leaves, each landed by a
    merge — the first tracker's by its id, the second's by its line, that commit carrying a `Session:` too. After: both steps of the
    change landed as well."""
    root = area.parent
    if (root, "before") not in _SEEDS:
        r = Ledger(root / "seed-before").start()
        head = r.answer("FM-001", LEAVES, "owner", aid="FM-001-Q1")
        r.land("answer-fm-001")
        r.answer("FM-002", LEAVES, "owner", trailers=("Session: 1234abcd",))
        r.land("answer-fm-002")
        _SEEDS[(root, "before")] = (r, head)
    if state == "after" and (root, "after") not in _SEEDS:
        r, head = _SEEDS[(root, "before")]
        r = r.copy(root / "seed-after")
        listed_again(r)
        r.land("key-listed-again")
        taken_out(r)
        r.land("address-leaves")
        _SEEDS[(root, "after")] = (r, head)
    return _SEEDS[(root, state)]


def before(base):
    r, head = seed(base, "before")
    return r.copy(base), head


def after(base):
    r, head = seed(base, "after")
    return r.copy(base), head


def listed_again(r, first=LEAVES):
    """Step 1: both addresses enrolled, and the key listed under both, `first`'s line first — the Owner's commit under the address that leaves."""
    r.switch("-c", "key-listed-again", "main")
    r.config((LEAVES, STAYS))
    r.signers(*((who, "owner") for who in ((LEAVES, STAYS) if first is LEAVES else (STAYS, LEAVES))))
    r.commit("the key is listed under the address that stays too", who=LEAVES, key="owner")


def taken_out(r):
    """Step 2: the address that leaves is in neither `owner` nor the signers file — the Owner's commit under the address that stays."""
    r.switch("-c", "address-leaves", "main")
    r.signers((STAYS, "owner"))
    r.config((STAYS,))
    r.commit("an address leaves owner and the signers file", who=STAYS, key="owner")


no_answer = lambda tid: f"{tid}: no commit answers {tid}-Q1"


def rows_steps(area, add):
    r, _head = before(area / "steps")
    s = Steps()
    said = r.check()
    s("before the change", accepted(said), said)
    listed_again(r)
    said = r.check()
    s("step 1 on its branch", accepted(said), said)
    r.land("key-listed-again")
    said = r.check()
    s("step 1 landed", accepted(said), said)
    taken_out(r)
    said = r.check()
    s("step 2 on its branch", accepted(said), said)
    s.add(add, "the two steps · two answers under the address that will leave, FM-001-Q1 by its id and FM-002 by its line; step 1, the key listed again "
               "under the address that stays, on its branch and landed; step 2, the other address taken out — the Owner's commit under the address that "
               "stays, whose key git names for the other address on the first line that holds it — on its branch: each accepted")


def rows_after(area, add):
    r, head = after(area / "after")
    said = r.check()
    add("after the change · every earlier answer counts — FM-001-Q1 by its id, FM-002 by its line — and the asks the Owner put under the address "
        "that left stand: accepted", accepted(said, "FM-00"), seen(said))
    heads = heads_of(r)
    add("after the change · `answer_commits` finds FM-001-Q1's head, the commit under the address that left", heads.get("FM-001-Q1") == (head, ""), str(heads))
    label = ("after the change · the state FM-001-Q1's commit is judged by names both addresses, each signed, and a commit of the default branch that "
             "holds their keys; a commit that branch does not hold is judged by the state in force there now, which names the address that stays alone")
    fm.configure(r.root)
    try:
        then, unfiled = fm.filed_state(head), fm.filed_state("0" * 40)
        add(label, bool(then) and then[0] == {LEAVES[1]: "signed", STAYS[1]: "signed"} and then[1] == then[0] and bool(then[2])
            and bool(unfiled) and unfiled[0] == {STAYS[1]: "signed"} and unfiled[1] == unfiled[0] and bool(unfiled[2]), f"{then} · {unfiled}")
    except AttributeError as e:
        missing(add, label, e)
    finally:
        fm.configure(HERE)
    fm.configure(r.root)
    try:
        seats = [s for row in fm.session_rows() for s in row["seats"]]
    finally:
        fm.configure(HERE)
    add("after the change · the session registry reads the Owner's commit under the address that left as the Owner's, never as that address",
        seats == ["owner"], str(seats))


def rows_new_answer(area, add):
    r, _head = after(area / "new")
    s = Steps()
    r.answer("FM-003", STAYS, "owner", aid="FM-003-Q1")
    said = r.check()
    s("on its branch", accepted(said), said)
    r.land("answer-fm-003")
    said = r.check()
    s("landed", accepted(said), said)
    s.add(add, "after the change · a new answer under the address that stays, on its branch and landed: accepted, every earlier answer counting")


def rows_other_order(area, add):
    r, _head = before(area / "order")
    listed_again(r, first=STAYS)
    r.land("key-listed-again")
    said = r.check()
    add("the other order · the key listed under the address that stays FIRST, landed: every earlier answer still counts — accepted", accepted(said), seen(said))


def rows_one_line(area, add):
    r, _head = before(area / "comma")
    r.switch("-c", "key-listed-again", "main")
    r.signers(text_=f"{LEAVES[1]},{STAYS[1]} {{owner}}\n")
    r.commit("the key is listed under both addresses, on one line", who=LEAVES, key="owner")
    r.land("key-listed-again")
    r.answer("FM-003", STAYS, "owner", aid="FM-003-Q1")
    said = r.check()
    add("one line for both · a key listed for two addresses on one line verifies for each: an answer under the second, on its branch — accepted", accepted(said), seen(said))


def rows_refused(area, add):
    r, _head = after(area / "stranger")
    r.answer("FM-003", STRANGER, "stranger", aid="FM-003-Q1")
    said = r.check()
    add("refused · an answer under an identity the default branch never named, on its branch — every earlier answer still counting",
        refused(said, no_answer("FM-003")) and stands(said, "FM-003"), seen(said))
    r.land("answer-fm-003")
    said = r.check()
    add("refused · …and landed by a merge all the same — every earlier answer still counting", refused(said, no_answer("FM-003")) and stands(said, "FM-003"), seen(said))

    r, _head = after(area / "late")
    r.answer("FM-004", LEAVES, "owner", aid="FM-004-Q1")
    said = r.check()
    add("refused · an answer under the address that left, made after the change and signed with the Owner's own key, on its branch — every earlier answer still counting",
        refused(said, no_answer("FM-004"), "`a former Owner identity` is not a seat") and stands(said, "FM-004"), seen(said))
    r.land("answer-fm-004")
    said = r.check()
    add("refused · …and landed by a merge all the same: it was filed when the default branch no longer named that address — every earlier answer still counting",
        refused(said, no_answer("FM-004")) and stands(said, "FM-004"), seen(said))

    r, _head = after(area / "late-line")
    r.answer("FM-005", LEAVES, "owner")
    r.land("answer-fm-005")
    said = r.check()
    add("refused · an answer by its line under the address that left, landed after the change: the default branch did not name its author then — every earlier answer still counting",
        refused(said, "FM-005: the answer's commit", "did not name that author as one who may answer when the commit was filed there") and stands(said, "FM-005"), seen(said))

    r, _head = after(area / "late-guard")
    r.switch("-c", "intent", "main")
    r.triage("whatever the address that left writes after the change")
    r.commit("the intent, under the address that left", who=LEAVES, key="owner")
    said = r.check()
    add("refused · a change to the Owner's two sections under the address that left, after the change — every earlier answer still counting",
        refused(said, "its author `a former Owner identity` is not the Owner") and stands(said), seen(said))

    r, _head = after(area / "unknown-key")
    r.answer("FM-003", STAYS, "stranger", aid="FM-003-Q1")
    said = r.check()
    add("refused · a signature by a key the signers file never held, under the Owner's address — on its branch, every earlier answer still counting",
        refused(said, no_answer("FM-003")) and stands(said, "FM-003"), seen(said))
    r.land("answer-fm-003")
    said = r.check()
    add("refused · …and landed by a merge all the same — every earlier answer still counting", refused(said, no_answer("FM-003")) and stands(said, "FM-003"), seen(said))


def rows_refused_branches(area, add):
    r, _head = after(area / "newcomer")
    r.switch("-c", "answer-fm-003", "main")
    r.signers((STAYS, "owner"), (NEWCOMER, "branch"))
    r.config((STAYS, NEWCOMER))
    r.commit("owner and the signers file name a newcomer", who=NEWCOMER, key="branch")
    write(r.root, "FM-003", answered(r.read("FM-003")))
    r.commit("FM-003-Q1: accepted", who=NEWCOMER, key="branch", trailers=("Answers: FM-003-Q1",))
    said = r.check()
    add("refused · a branch that adds an identity to `owner` and its key to the signers file, and answers under it — on the branch, every earlier answer still counting",
        refused(said, no_answer("FM-003"), "changes the signers file") and stands(said, "FM-003"), seen(said))
    r.land("answer-fm-003")
    said = r.check()
    add("refused · …and landed by a merge all the same: the answer was filed while the default branch named no such identity — every earlier answer still counting",
        refused(said, no_answer("FM-003")) and stands(said, "FM-003"), seen(said))

    r, _head = after(area / "branch-key")
    r.switch("-c", "answer-fm-003", "main")
    r.signers((STAYS, "owner"), (STAYS, "branch"))
    r.commit("a second key under the Owner's address", who=STAYS, key="branch")
    write(r.root, "FM-003", answered(r.read("FM-003")))
    r.commit("FM-003-Q1: accepted", who=STAYS, key="branch", trailers=("Answers: FM-003-Q1",))
    said = r.check()
    add("refused · a branch that adds its own key under the Owner's address, and answers under that address with it — on the branch, every earlier answer still counting",
        refused(said, no_answer("FM-003"), "changes the signers file") and stands(said, "FM-003"), seen(said))
    r.land("answer-fm-003")
    said = r.check()
    add("refused · …and landed by a merge all the same: the answer was filed while the default branch's signers file held no such key — every earlier answer still counting",
        refused(said, no_answer("FM-003")) and stands(said, "FM-003"), seen(said))


def rows_key_later(area, add):
    r, _head = after(area / "key-later")
    r.answer("FM-005", STAYS, "second")
    r.land("answer-fm-005")
    r.switch("-c", "second-key", "main")
    r.signers((STAYS, "owner"), (STAYS, "second"))
    r.commit("a second key, by the Owner's signed commit", who=STAYS, key="owner")
    r.land("second-key")
    r.settle()
    said = r.check()
    add("never again · an answer by its line, signed with a key that reached the signers file only after the answer was filed: still refused — a key that "
        "arrives later verifies nothing filed before it; every earlier answer still counting",
        refused(said, "FM-005: the answer's commit", "held no such key for that identity then") and stands(said, "FM-005"), seen(said))
    r.answer("FM-004", STAYS, "second", aid="FM-004-Q1")
    r.land("answer-fm-004")
    said = r.check()
    add("never again · …and an answer signed with that key after it arrived counts: FM-004 is not refused", "FM-004" not in said[2] and "FM-005" in said[2]
        and stands(said, "FM-005"), seen(said))


def rows_named_later(area, add):
    r, _head = after(area / "named-later")
    r.answer("FM-005", STRANGER, "stranger")
    r.land("answer-fm-005")
    r.switch("-c", "named", "main")
    r.signers((STAYS, "owner"), (STRANGER, "stranger"))
    r.config((STAYS, STRANGER))
    r.commit("a second identity, by the Owner's signed commit", who=STAYS, key="owner")
    r.land("named")
    r.settle()
    said = r.check()
    add("never again · an answer by its line under an identity the default branch named only after the answer was filed: still refused — every earlier answer still counting",
        refused(said, "FM-005: the answer's commit", "did not name that author as one who may answer when the commit was filed there") and stands(said, "FM-005"), seen(said))


def rows_key_left(area, add):
    r, _head = after(area / "key-left")
    r.switch("-c", "rotated", "main")
    r.signers((STAYS, "second"))
    r.commit("the key is replaced, by the Owner's signed commit", who=STAYS, key="owner")
    r.land("rotated")
    said = r.check()
    add("never again · the key every earlier answer was signed with has left the signers file: each still counts, verified against the file as the "
        "default branch held it when the answer was filed — accepted", accepted(said, "FM-00"), seen(said))
    r.answer("FM-003", STAYS, "owner", aid="FM-003-Q1")
    said = r.check()
    add("never again · …and that key signs nothing new: an answer signed with it after it left, on its branch — refused, every earlier answer still counting",
        refused(said, "FM-003: no commit answers FM-003-Q1") and stands(said, "FM-003"), seen(said))


def rows_first_state(area, add):
    r = Ledger(area / "first").start(owner=(), signers=())
    r.answer("FM-001", LEAVES, "owner", aid="FM-001-Q1")
    r.land("answer-fm-001")
    r.switch("-c", "named", "main")
    r.config((LEAVES, STAYS))
    r.signers((LEAVES, "owner"))
    r.commit("the default branch names its Owner, and holds their key", who=LEAVES, key="owner")
    r.land("named")
    r.settle()
    s = Steps()
    said = r.check()
    s("named", accepted(said, "FM-00"), said)
    listed_again(r)
    r.land("key-listed-again")
    taken_out(r)
    r.land("address-leaves")
    said = r.check()
    s("after the address left", accepted(said, "FM-00"), said)
    s.add(add, "the first state · an answer filed before the default branch named anyone is judged by the first state that names someone, and its keys by the "
               "first signers file from there on: accepted — and after the address left, it still counts by that first state")


def rows_lines(area, add):
    cases = (("an address and its key", 'a@example.com ssh-ed25519 AAAA c', (["a@example.com"], "ssh-ed25519 AAAA c")),
             ("an option before the key", 'a@example.com namespaces="git" ssh-ed25519 AAAA', (["a@example.com"], 'namespaces="git" ssh-ed25519 AAAA')),
             ("two addresses, one line", "a@example.com,b@example.com ssh-ed25519 AAAA", (["a@example.com", "b@example.com"], "ssh-ed25519 AAAA")),
             ("a quoted field", '"a@example.com" ssh-ed25519 AAAA', (["a@example.com"], "ssh-ed25519 AAAA")),
             ("a tab between the fields", "a@example.com\tssh-ed25519 AAAA", (["a@example.com"], "ssh-ed25519 AAAA")),
             ("a comment", "# a@example.com ssh-ed25519 AAAA", ([], "")), ("an empty line", "  \r", ([], "")))
    for what, line, want in cases:
        label = f"a signers line · {what}: its identities and the rest of the line"
        try:
            add(label, fm.signers_named(line) == want, repr(fm.signers_named(line)))
        except AttributeError as e:
            missing(add, label, e)
    key = "ssh-ed25519 AAAA"
    listed = (("one line", f"a@example.com {key}\n", [key]), ("two lines, one for another identity", f"b@example.com {key}\na@example.com {key} c\n", [key + " c"]),
              ("one line for two identities", f"b@example.com,a@example.com {key}\n", [key]), ("a line with CRLF", f"a@example.com {key}\r\n", [key]),
              ("a list that negates an identity", f"a@example.com,!a@example.com {key}\n", []), ("a pattern", f"*@example.com {key}\n", []),
              ("another identity alone", f"b@example.com {key}\n", []), ("no key after the identity", "a@example.com\n", []), ("no text", None, []))
    for what, text_, want in listed:
        label = f"the keys a signers file lists for one identity · {what}"
        try:
            add(label, fm.signers_rows(text_, "a@example.com") == want, repr(fm.signers_rows(text_, "a@example.com")))
        except AttributeError as e:
            missing(add, label, e)
    r, _head = after(area / "lines")
    label = ("the lines of one identity · the file a signature is verified against holds that identity's lines alone, and there is none for an identity "
             "the signers file does not list")
    fm.configure(r.root)
    try:
        held, none = fm.signers_held(STAYS[1]), fm.signers_held(LEAVES[1])
        rows = Path(held).read_text(encoding="utf-8").splitlines() if held else []
        add(label, len(rows) == 1 and rows[0].startswith(STAYS[1] + " ssh-ed25519 ") and none is None, f"{rows} · {none}")
    except AttributeError as e:
        missing(add, label, e)
    finally:
        fm.configure(HERE)


def rows_cost(area, add):
    r, _head = after(area / "cost")
    real, seen_ = fm.vcs_process, []

    def watching(program, *a, **k):
        seen_.append((program, *a))
        return real(program, *a, **k)
    fm.vcs_process = watching
    try:
        said = r.check()
    finally:
        fm.vcs_process = real
    line, turns = sum(1 for argv in seen_ if "--format=%H %P%x00%an%x00%ae" in argv), sum(1 for argv in seen_ if "--full-history" in argv and "--format=%H" in argv)
    add("the cost · one `--check` reads the default branch's line once — one `git log` for its commits, one for where its configuration or its signers "
        "file changes — however many answers stand", accepted(said) and (line, turns) == (1, 1), seen(said) + f" · {line} · {turns}")


def rows_single_start(area, add):
    r = Ledger(area / "single").start(owner=(LEAVES,))
    r.answer("FM-001", LEAVES, "owner", aid="FM-001-Q1")
    r.land("answer-fm-001")
    s = Steps()
    listed_again(r)
    said = r.check()
    s("step 1 on its branch", accepted(said), said)
    r.land("key-listed-again")
    said = r.check()
    s("step 1 landed", accepted(said), said)
    taken_out(r)
    said = r.check()
    s("step 2 on its branch", accepted(said), said)
    r.land("address-leaves")
    said = r.check()
    s("step 2 landed", accepted(said), said)
    s.add(add, "one initial identity · both steps from a configuration that names the address that leaves alone, each on its branch and landed: accepted, "
               "FM-001-Q1 counting throughout")


def private_outputs(r, add, label, *besides):
    said = r.check()
    generated = run(r.root, "--print-written")
    board = (r.root / REL / "index.html").read_text(encoding="utf-8")
    index = (r.root / REL / "INDEX.md").read_text(encoding="utf-8")
    add(label + " · stderr, INDEX and Board omit the former identity, and every earlier answer still counts",
        said[0] == fm.EXIT_LINT and LEAVES[1] not in said[2] + generated[2] + index + board and stands(said, *besides), seen(said))


def rows_display(area, add):
    for n, (tid, aid, land) in enumerate((("FM-004", "FM-004-Q1", False), ("FM-004", "FM-004-Q1", True), ("FM-005", "", True))):
        r, _head = after(area / f"display-{n}")
        r.answer(tid, LEAVES, "owner", aid=aid, trailers=("Session: abcdef12",))
        if land:
            r.land("answer-" + tid.lower())
        private_outputs(r, add, "former identity answer " + str(n), tid)
    r, _head = after(area / "display-guard")
    r.switch("-c", "intent", "main")
    r.triage("an edit under the former identity")
    r.commit("the intent", who=LEAVES, key="owner")
    private_outputs(r, add, "former identity protected edit")
    r, _head = after(area / "display-key")
    r.switch("-c", "bad-answer", "main")
    write(r.root, "FM-005", answered(r.read("FM-005")))
    r.commit("a line answer with a different key", who=STAYS, key="stranger")
    r.land("bad-answer")
    private_outputs(r, add, "historical signature refusal", "FM-005")


def rows_current_ask(area, add):
    r, _head = after(area / "current-ask")
    s = Steps()
    r.switch("-c", "fresh-ask", "main")
    write(r.root, "FM-007", text("FM-007", ask(aid="FM-007-Q1")))
    r.commit("a fresh open ask", who=STAYS, key="owner")
    r.land("fresh-ask")
    said = r.check()
    s("before rotation", accepted(said), said)
    r.switch("-c", "rotation", "main")
    r.signers((STAYS, "second"))
    r.commit("replace the key", who=STAYS, key="owner")
    said = r.check()
    s("rotation branch", accepted(said), said)
    r.land("rotation")
    said = r.check()
    s("after rotation", accepted(said), said)
    s.add(add, "current identity ask · an ask the Owner puts under the address that stays, before a key rotation, beside the rotation's branch and after "
               "it lands: accepted, the asks put under the address that left standing too")


def rows_state_selection(area, add):
    for merged in (False, True):
        r, _head = after(area / ("selection-merge" if merged else "selection-line"))
        r.switch("-c", "candidate", "main")
        r.signers((STAYS, "owner"), (STAYS, "branch"))
        r.commit("a candidate file", who=STAYS, key="branch")
        write(r.root, "FM-003", answered(r.read("FM-003")))
        r.commit("FM-003-Q1: accepted", who=STAYS, key="branch", trailers=("Answers: FM-003-Q1",))
        said = r.check()
        add("state selection · candidate branch " + ("merge" if merged else "line") + ", every earlier answer still counting",
            refused(said, no_answer("FM-003")) and stands(said, "FM-003"), seen(said))
        if merged:
            r.land("candidate")
        else:
            r.forward("candidate")
        r.switch("-c", "restore", "main")
        r.signers((STAYS, "owner"))
        r.commit("restore the file", who=STAYS, key="owner")
        r.land("restore")
        r.settle()
        said, heads = r.check(), heads_of(r)
        add("state selection · restored " + ("merge" if merged else "line") + ", every earlier answer still counting",
            refused(said, no_answer("FM-003")) and not heads.get("FM-003-Q1", ("",))[0] and stands(said, "FM-003"), seen(said) + str(heads))


def rows_state_gaps(area, add):
    for n, cfg in enumerate(('', 'owner = 7\n', 'owner = []\n')):
        r, _head = after(area / f"gap-{n}")
        r.switch("-c", "gap", "main")
        (r.root / "shoalmark.toml").write_text(cfg + '[kinds]\nFM = "Work"\n', encoding="utf-8")
        git(r.root, "add", "shoalmark.toml")
        git(r.root, "commit", "-q", "-m", "a candidate configuration", who=STAYS)
        r.land("gap")
        r.switch("-c", "new-answer", "main")
        write(r.root, "FM-005", answered(r.read("FM-005")))
        git(r.root, "add", "-A")
        git(r.root, "commit", "-q", "-m", "a candidate answer", "-S", who=STRANGER, sign=r.keys["stranger"])
        r.land("new-answer")
        r.switch("-c", "restore", "main")
        r.config((STAYS, STRANGER))
        r.signers((STAYS, "owner"), (STRANGER, "stranger"))
        r.commit("restore the configuration", who=STAYS, key="owner")
        r.land("restore")
        said = r.check()
        add("state selection · gap " + str(n) + ", every earlier answer still counting", refused(said, "FM-005: the answer's commit") and stands(said, "FM-005"), seen(said))


def rows_same_landing(area, add):
    r, _head = after(area / "same-landing")
    r.switch("-c", "together", "main")
    r.signers((STAYS, "owner"), (STAYS, "second"))
    r.commit("another key", who=STAYS, key="owner")
    write(r.root, "FM-003", answered(r.read("FM-003")))
    r.commit("FM-003-Q1: accepted", who=STAYS, key="second", trailers=("Answers: FM-003-Q1",))
    r.land("together")
    said = r.check()
    add("state selection · two changes arrive together, every earlier answer still counting", refused(said, no_answer("FM-003")) and stands(said, "FM-003"), seen(said))


def rows_state_inherited(area, add):
    r, _head = after(area / "inherited")
    r.switch("-c", "candidate", "main")
    r.signers((STAYS, "owner"), (STAYS, "branch"))
    r.commit("a candidate file", who=STAYS, key="branch")
    r.forward("candidate")
    r.switch("-c", "name", "main")
    config = r.root / "shoalmark.toml"
    config.write_text(config.read_text().replace('name = "filed"', 'name = "renamed"'), encoding="utf-8")
    r.commit("a repository name", who=SEAT)
    r.land("name")
    r.answer("FM-003", STAYS, "branch", aid="FM-003-Q1")
    r.land("answer-fm-003")
    r.switch("-c", "restore", "main")
    r.signers((STAYS, "owner"))
    r.commit("restore the file", who=STAYS, key="owner")
    r.land("restore")
    r.settle()
    said = r.check()
    add("state selection · a repository name, every earlier answer still counting", refused(said, no_answer("FM-003")) and stands(said, "FM-003"), seen(said))


def rows_state_material(area, add):
    r, _head = after(area / "material")
    r.switch("-c", "without-file", "main")
    (r.root / REL / "allowed_signers").rename(r.base / "saved-signers")
    r.commit("a file is absent", who=STAYS, key="owner")
    r.land("without-file")
    r.answer("FM-005", STAYS, "owner")
    r.land("answer-fm-005")
    r.switch("-c", "restore", "main")
    r.signers((STAYS, "owner"))
    r.commit("the file is present", who=STAYS, key="owner")
    r.land("restore")
    r.settle()
    said = r.check()
    add("state selection · unavailable material, every earlier answer still counting", refused(said, "FM-005: the answer's commit") and stands(said, "FM-005"), seen(said))


def rows_state_boundary(area, add):
    r, head = after(area / "boundary")
    r.switch("-c", "candidate", "main")
    r.signers((STAYS, "owner"), (STAYS, "branch"))
    boundary = r.commit("a candidate file", who=STAYS, key="branch")
    write(r.root, "FM-003", answered(r.read("FM-003")))
    r.commit("FM-003-Q1: accepted", who=STAYS, key="branch", trailers=("Answers: FM-003-Q1",))
    r.forward("candidate")
    r.switch("-c", "restore", "main")
    r.signers((STAYS, "owner"))
    r.commit("restore the file", who=STAYS, key="owner")
    r.land("restore")
    r.settle()
    whole = heads_of(r)
    (r.root / ".git/shallow").write_bytes((boundary + "\n").encode("ascii"))
    heads = heads_of(r)
    add("state selection · a boundary: with the whole history, FM-001-Q1's commit under the address that left counts; with a boundary in it, "
        "FM-003-Q1's has no head", whole.get("FM-001-Q1") == (head, "") and not heads.get("FM-003-Q1", ("",))[0], f"{whole} · {heads}")


def rows_state_unread(area, add):
    r, earlier = after(area / "unread")
    head = r.answer("FM-003", STAYS, "owner", aid="FM-003-Q1")
    r.land("answer-fm-003")
    real = fm.git_out
    label = "state selection · an unavailable history"

    def unavailable(*args, **kwargs):
        if "--format=%H %P%x00%an%x00%ae" in args:
            return None
        return real(*args, **kwargs)
    fm.configure(r.root)
    fm.git_out = unavailable
    try:
        state = fm.filed_state(head)
        heads = fm.answer_commits(fm.load_trackers())
        said = r.check()
        add(label, state == ({}, {}, None) and not heads.get("FM-003-Q1", ("",))[0] and LEAVES[1] not in said[1] + said[2], str(state) + str(heads) + seen(said))
    except AttributeError as e:
        missing(add, label, e)
    finally:
        fm.git_out = real
        fm.configure(HERE)
    heads = heads_of(r)
    add("state selection · the history is readable: FM-003-Q1 and FM-001-Q1, the commit under the address that left, each have their head",
        heads.get("FM-003-Q1") == (head, "") and heads.get("FM-001-Q1") == (earlier, ""), str(heads))


def rows_state_prelude(area, add):
    r = Ledger(area / "prelude").start(owner=(LEAVES,))
    first = git(r.root, "rev-list", "--max-parents=0", "main").strip()
    blob = git(r.root, "rev-parse", first + ":shoalmark.toml").strip()
    head = r.answer("FM-001", LEAVES, "owner", aid="FM-001-Q1")
    r.land("answer-fm-001")
    listed_again(r)
    r.land("key-listed-again")
    taken_out(r)
    r.land("address-leaves")
    r.settle()
    original = r.root / ".git/objects" / blob[:2] / blob[2:]
    saved = r.base / "saved-config"
    original.rename(saved)
    try:
        heads = heads_of(r)
        said = r.check()
        add("state selection · initial material is unavailable", not heads.get("FM-001-Q1", ("",))[0]
            and LEAVES[1] not in said[1] + said[2], str(heads) + seen(said))
    finally:
        saved.rename(original)
    heads = heads_of(r)
    add("state selection · initial material is readable", heads.get("FM-001-Q1") == (head, ""), str(heads))


def rows_unsigned_owner(area, add):
    r = Ledger(area / "unsigned").start(owner=(LEAVES,), signed=False)
    r.switch("-c", "key-listed-again", "main")
    r.config((LEAVES, STAYS))
    r.signers((LEAVES, "owner"), (STAYS, "owner"))
    r.commit("both addresses, unsigned", who=LEAVES)
    r.land("key-listed-again")
    r.switch("-c", "address-leaves", "main")
    r.config((STAYS,))
    r.signers((STAYS, "owner"))
    r.commit("an address leaves, unsigned", who=STAYS)
    r.land("address-leaves")
    r.answer("FM-003", STAYS, None, aid="FM-003-Q1")
    said = r.check()
    add("an Owner who does not sign · after the two steps, a new answer under the address that stays, on its branch: accepted", accepted(said), seen(said))
    r.land("answer-fm-003")
    said = r.check()
    add("an Owner who does not sign · …and landed: accepted — the change of who may answer took effect", accepted(said), seen(said))
    r.switch("-c", "fresh-ask", "main")
    write(r.root, "FM-007", text("FM-007", ask(aid="FM-007-Q1")))
    r.commit("a fresh ask, unsigned", who=STAYS)
    r.land("fresh-ask")
    said = r.check()
    add("an Owner who does not sign · an ask the Owner puts under the address that stays, landed: accepted", accepted(said), seen(said))


def rows_answerers(area, add):
    r = Ledger(area / "answerers").start(owner=(ALICE,), signed=False, plain=True, who=ALICE)
    for tid, aid in (("FM-001", "FM-001-Q1"), ("FM-002", "")):
        r.answer(tid, ALICE, None, aid=aid, by=ALICE[0])
        r.land("answer-" + tid.lower())
    r.switch("-c", "answerer-added", "main")
    r.config((ALICE, BOB))
    r.commit("an answerer is added", who=ALICE)
    r.land("answerer-added")
    r.answer("FM-003", BOB, None, aid="FM-003-Q1", by=BOB[0])
    r.land("answer-fm-003")
    s = Steps()
    said = r.check()
    s("an answerer added later answers", accepted(said), said)
    r.switch("-c", "answerer-removed", "main")
    r.config((BOB,))
    r.commit("the first answerer is removed, by the one added later", who=BOB)
    r.land("answerer-removed")
    said = r.check()
    s("the first answerer removed", accepted(said), said)
    s.add(add, "`answerers` · an answerer added later by an answerer's commit gives an answer, landed; then the first answerer is removed by the one "
               "added later: every answer counts — FM-001 by its id and FM-002 by its line, each given by the answerer removed, and FM-003 — accepted")


def rows_removed_owner(area, add):
    r, _head = before(area / "removed-owner")
    s = Steps()
    r.switch("-c", "nobody", "main")
    r.config(())
    r.commit("nobody may answer from now on, by the Owner's signed commit", who=LEAVES, key="owner")
    said = r.check()
    s("on its branch", accepted(said), said)
    r.land("nobody")
    said = r.check()
    s("landed", accepted(said, "FM-00"), said)
    r.answer("FM-003", LEAVES, "owner", aid="FM-003-Q1")
    said = r.check()
    s("a new answer by the Owner after it", refused(said, "FM-003:") and stands(said, "FM-003"), said)
    s.add(add, "the last Owner removed · the Owner's signed commit takes every identity out of `owner`, on its branch and landed: FM-001 by its id and FM-002 "
               "by its line still count, by the state they were filed in — accepted; and an answer the Owner gives after it is refused")


def rows_current_state(area, add):
    r, _head = after(area / "current-state")
    r.switch("-c", "stranger-adds-owner", "main")
    config = r.root / "shoalmark.toml"
    config.write_text(config.read_text(encoding="utf-8").replace(f'owner = ["{STAYS[1]} signed"]', f'owner = ["{STAYS[1]} signed", "{STRANGER[1]}"]'), encoding="utf-8")
    r.commit("an unsigned identity adds itself to owner", who=STRANGER)
    r.land("stranger-adds-owner")
    for n, what in enumerate(("by its id, on its branch", "by its id, landed", "by its line, on its branch", "an ask it puts, on its branch")):
        twin = r.copy(area / f"current-state-{n}")
        if n < 2:
            twin.answer("FM-003", STRANGER, None, aid="FM-003-Q1")
            if n == 1:
                twin.land("answer-fm-003")
            said = twin.check()
            ok = refused(said, no_answer("FM-003")) and stands(said, "FM-003") and "the author only" not in said[1] + said[2]
        elif n == 2:
            twin.answer("FM-005", STRANGER, None)
            said = twin.check()
            ok = refused(said, "FM-005: the answer's commit", "does not name that author as one who may answer in the state in force") and stands(said, "FM-005")
        else:
            twin.switch("-c", "stranger-asks", "main")
            write(twin.root, "FM-007", text("FM-007", ask(aid="FM-007-Q1")))
            twin.commit("a fresh ask, under the identity that added itself", who=STRANGER)
            said = twin.check()
            ok = refused(said, "FM-007:", "does not name as the Owner in the state in force") and stands(said)
        add("the state in force · an unsigned identity that added itself to `owner`, its change landed by a merge and never accepted: its unsigned "
            f"answer or ask, {what}, is refused, the Owner read as signed, and every earlier answer still counts", ok, seen(said))


NOT_IN_FORCE = "is not the one in force"   # where the default branch holds a signers file its state in force does not


def rows_current_signers(area, add):
    r, _head = after(area / "current-signers")
    r.switch("-c", "candidate", "main")
    r.signers((STAYS, "owner"), (STAYS, "branch"))
    r.commit("a key under the Owner's address, by a seat", who=SEAT)
    r.forward("candidate")
    r.switch("-c", "intent", "main")
    r.triage("a change signed with the key a seat put in the signers file")
    r.commit("the intent", who=STAYS, key="branch")
    said = r.check()
    add("the state in force · a key a seat's unsigned commit put in the signers file, fast-forwarded and never accepted: the Owner's change to the two "
        "sections signed with it is refused, by the guard and by R14, on its branch — every earlier answer still counting",
        refused(said, "does not verify", "refused: Owner commit") and stands(said), seen(said))
    r, _head = after(area / "current-deleted")
    r.switch("-c", "no-file", "main")
    (r.root / REL / "allowed_signers").rename(r.base / "saved-signers")
    r.commit("the signers file deleted, by a seat", who=SEAT)
    r.land("no-file")
    r.switch("-c", "intent", "main")
    r.triage("a change signed with the key the state in force holds")
    r.commit("the intent", who=STAYS, key="owner")
    said = r.check()
    s = Steps()
    s("the Owner's change to the two sections", accepted(said), said)
    r.answer("FM-003", STAYS, "owner", aid="FM-003-Q1")
    said = r.check()
    s("a new answer", accepted(said), said)
    s.add(add, "the state in force · the signers file deleted by a seat's unsigned commit, landed and never accepted: the Owner's signed change to the "
               "two sections, and a new signed answer, each on its branch, verify against the file the state in force holds — accepted")
    r = Ledger(area / "current-first-file").start(owner=(STAYS,), signers=(), who=STAYS)
    r.switch("-c", "first-file", "main")
    r.signers((STAYS, "owner"))
    r.commit("a first signers file, by a seat", who=SEAT)
    r.forward("first-file")
    r.switch("-c", "intent", "main")
    r.triage("a change signed with the key a seat's first signers file lists")
    r.commit("the intent", who=STAYS, key="owner")
    said = r.check()
    add("the state in force · a first signers file a seat's unsigned commit put on the default branch, fast-forwarded and never accepted: the Owner's "
        "change to the two sections signed with the key it lists is not verified here — the file is not the one in force", refused(said, NOT_IN_FORCE),
        f"exit {said[0]}; the file said not to be the one in force: {NOT_IN_FORCE in said[2]}")


def rows_tip_unread(area, add):
    r, _head = after(area / "tip-unread")
    r.switch("-c", "rotated", "main")
    r.signers((STAYS, "second"))
    r.commit("the key is replaced, by the Owner's signed commit", who=STAYS, key="owner")
    r.land("rotated")
    r.answer("FM-003", STAYS, "owner", aid="FM-003-Q1")
    blob = git(r.root, "rev-parse", f"origin/main:{REL}/allowed_signers").strip()
    original = r.root / ".git/objects" / blob[:2] / blob[2:]
    saved = r.base / "saved-signers-blob"
    original.rename(saved)
    try:
        said = r.check()
        heads = heads_of(r)
    finally:
        saved.rename(original)
    add("the state in force · the change at the default branch's tip cannot be read: a new answer signed with the key it replaced is refused on its branch — "
        "every earlier answer still counting", refused(said, no_answer("FM-003")) and stands(said, "FM-003") and not heads.get("FM-003-Q1", ("",))[0]
        and bool(heads.get("FM-001-Q1", ("",))[0]), seen(said) + str(heads))


def rows_signers_deleted(area, add):
    r, head = after(area / "signers-deleted")
    s = Steps()
    r.switch("-c", "no-file", "main")
    (r.root / REL / "allowed_signers").rename(r.base / "saved-signers")
    r.commit("every key retired: the signers file deleted, by the Owner's signed commit", who=STAYS, key="owner")
    said = r.check()
    s("on its branch", accepted(said), said)
    r.land("no-file")
    said, heads = r.check(), heads_of(r)
    s("landed", accepted(said, "FM-00") and heads.get("FM-001-Q1") == (head, ""), said, str(heads))
    r.answer("FM-003", STAYS, "owner", aid="FM-003-Q1")
    said = r.check()
    s("a new answer signed with a retired key", refused(said, no_answer("FM-003")) and stands(said, "FM-003"), said)
    r.answer("FM-004", LEAVES, "owner", aid="FM-004-Q1")
    said = r.check()
    s("a new answer under the address that left", refused(said, no_answer("FM-004")) and stands(said, "FM-004"), said)
    s.add(add, "the signers file deleted · the Owner's signed commit deletes it, on its branch and landed: every earlier answer and ask still verifies "
               "against the file as the default branch held it when each was filed — accepted; and a key it retired signs nothing new")


def rows_first_key(area, add):
    r = Ledger(area / "first-key").start(owner=(LEAVES,), signers=())
    s = Steps()
    r.switch("-c", "first-key", "main")
    r.signers((LEAVES, "owner"))
    r.commit("the first key, under the configured Owner's address", who=LEAVES, key="owner")
    r.land("first-key")
    head = r.answer("FM-001", LEAVES, "owner", aid="FM-001-Q1")
    heads = heads_of(r)
    s("on its branch", heads.get("FM-001-Q1") == (head, ""), None, str(heads))
    r.land("answer-fm-001")
    heads = heads_of(r)
    s("landed", heads.get("FM-001-Q1") == (head, ""), None, str(heads))
    listed_again(r)
    r.land("key-listed-again")
    taken_out(r)
    r.land("address-leaves")
    said, heads = r.check(), heads_of(r)
    s("after the address left", heads.get("FM-001-Q1") == (head, "") and stands(said, *EARLIER[1:]), said, str(heads))
    s.add(add, "a first key · a configuration first, its Owner's first key enrolled later by their own signed commit: an answer signed with that key "
               "counts on its branch and landed, and still counts after the address leaves")


def rows_first_key_narrow(area, add):
    r = Ledger(area / "key-replaced").start(owner=(LEAVES,), signers=())
    r.switch("-c", "first-key", "main")
    r.signers((LEAVES, "owner"))
    r.commit("the first key", who=LEAVES, key="owner")
    r.land("first-key")
    r.switch("-c", "replaced", "main")
    r.signers((LEAVES, "second"))
    r.commit("the key replaced, signed with the new key alone", who=LEAVES, key="second")
    r.land("replaced")
    r.answer("FM-001", LEAVES, "second", aid="FM-001-Q1")
    r.land("answer-fm-001")
    r.settle()
    said, heads = r.check(), heads_of(r)
    add("a first key · never a replacement: a commit that replaces an enrolled key, signed with the new key alone, is not the state in force — an answer "
        "signed with the new key, landed after it, is refused", refused(said, no_answer("FM-001")) and not heads.get("FM-001-Q1", ("",))[0], seen(said) + str(heads))
    r = Ledger(area / "key-named").start(owner=(LEAVES,), signers=())
    r.switch("-c", "first-key", "main")
    r.signers((LEAVES, "owner"))
    r.config((LEAVES, NEWCOMER))
    r.commit("the first key, and another identity in owner", who=LEAVES, key="owner")
    r.land("first-key")
    r.answer("FM-001", LEAVES, "owner", aid="FM-001-Q1")
    r.land("answer-fm-001")
    r.settle()
    said, heads = r.check(), heads_of(r)
    add("a first key · never a new identity: a commit that enrolls the first key and names another identity in `owner` is not the state in force — an "
        "answer signed with that key, landed after it, is refused", refused(said, no_answer("FM-001")) and not heads.get("FM-001-Q1", ("",))[0], seen(said) + str(heads))


def rows_merge_rejected(area, add):
    r, _head = after(area / "merge-rejected")
    r.switch("-c", "candidate", "main")
    r.signers((STAYS, "owner"), (STAYS, "branch"))
    rejected = r.commit("a key under the Owner's address", who=STAYS, key="branch")
    r.forward("candidate")
    r.switch("-c", "repair", "main")
    r.signers((STAYS, "owner"))
    r.commit("the signers file repaired", who=STAYS, key="owner")
    r.land("repair")
    r.switch("main")
    r.signers((STAYS, "owner"), (STAYS, "branch"))
    git(r.root, "add", "-A")
    tree = git(r.root, "write-tree").strip()
    merge = git(r.root, "commit-tree", tree, "-p", "HEAD", "-p", rejected, "-m", "a merge of the rejected change", who=SEAT).strip()
    git(r.root, "merge", "-q", "--ff-only", merge, who=SEAT)
    git(r.root, "push", "-q", "origin", "main")
    r.answer("FM-003", STAYS, "branch", aid="FM-003-Q1")
    s = Steps()
    said = r.check()
    s("on its branch", refused(said, no_answer("FM-003")) and stands(said, "FM-003"), said)
    r.land("answer-fm-003")
    r.settle()
    said = r.check()
    s("landed", refused(said, no_answer("FM-003")) and stands(said, "FM-003"), said)
    s.add(add, "a merge whose tree is a rejected change's state, by a seat, unsigned, fast-forwarded: never the state in force — an answer signed with that "
               "change's key, on its branch and landed after it, is refused; every earlier answer still counting")


def rows_unhealed(area, add):
    r, _head = after(area / "unhealed")
    r.switch("-c", "candidate", "main")
    r.signers((STAYS, "owner"), (STAYS, "branch"))
    r.commit("a key under the Owner's address", who=STAYS, key="branch")
    r.forward("candidate")
    r.switch("-c", "named", "main")
    r.config((STAYS, NEWCOMER))
    r.commit("another identity in `owner`, by the Owner's signed commit that leaves the signers file as it is", who=STAYS, key="owner")
    r.land("named")
    r.answer("FM-003", STAYS, "branch", aid="FM-003-Q1")
    r.land("answer-fm-003")
    r.settle()
    said = r.check()
    add("the Owner's signed commit that changes the configuration alone does not adopt a rejected change to the signers file: an answer signed with "
        "that change's key, landed after both, is refused — every earlier answer still counting", refused(said, no_answer("FM-003")) and stands(said, "FM-003"), seen(said))


def private_pages(r):
    """What the tool prints and writes for one ledger: `--check`, `--owner`, `--print-written` and `--html-only`, stdout and stderr, then
    the pages under the tracker folder — INDEX.md, the Board and every view."""
    texts = []
    for flags in (("--check",), ("--owner",), ("--print-written",), ("--html-only",)):
        texts += list(run(r.root, *flags)[1:])
    for page in sorted((r.root / REL).rglob("*")):
        if page.is_file() and (page.name in ("INDEX.md", "index.html") or "view" in page.relative_to(r.root / REL).parts):
            texts.append(page.read_text(encoding="utf-8", errors="replace"))
    return texts


def rows_order_private(area, add):
    """Through the Owner's order — both addresses named, signed, the key under each; then the Owner's signed commit that takes one out — an
    answer and an ask under each address at each step, and one answer refused: no refusal and no page names the address that leaves."""
    for step in (1, 2):
        r, _head = before(area / f"order-{step}")
        listed_again(r)
        r.land("key-listed-again")
        if step == 2:
            taken_out(r)
            r.land("address-leaves")
        for n, (who, tid, new) in enumerate(((LEAVES, "FM-003", "FM-007"), (STAYS, "FM-004", "FM-008"))):
            r.answer(tid, who, "owner", aid=f"{tid}-Q1")
            r.land("answer-" + tid.lower())
            r.switch("-c", f"ask-{n}", "main")
            write(r.root, new, text(new, ask(aid=f"{new}-Q1")))
            r.commit(f"an ask under address {n + 1}", who=who, key="owner")
            r.land(f"ask-{n}")
        r.answer("FM-005", LEAVES, "stranger")
        texts = private_pages(r)
        hits = sum(LEAVES[1] in s for s in texts)
        add(f"the order's step {step} · " + ("both addresses named, signed, the key under each" if step == 1 else "the Owner's signed commit has taken one out")
            + ": an answer and an ask under each address, one answer refused — no refusal and no page names the address that leaves",
            hits == 0, f"{hits} of {len(texts)} outputs and pages name it")


def rows_form_free(area, add):
    """What a refusal prints for an Owner identity is chosen by what `owner` says, never by the identity's form."""
    seen_ = {}
    for name, owner in (("alone", (FORGE,)), ("beside", (FORGE, STAYS))):
        r = Ledger(area / f"form-{name}").start(owner=owner, signers=tuple((w, "owner") for w in owner), who=FORGE)
        r.switch("-c", "unsigned", "main")
        (r.root / "notes.md").write_text("one line\n", encoding="utf-8")
        r.commit("an unsigned commit of the Owner's", who=FORGE)
        said = r.check()
        seen_[name] = (said[0] == fm.EXIT_LINT, FORGE[1] in said[2], "the Owner's identity 1 of 2" in said[2], "noreply address" in said[2])
    add("the form apart · an Owner identity is printed by what `owner` says, never by its form: named alone, an address that holds `noreply` "
        "prints as it is; named beside another, by its place", seen_["alone"] == (True, True, False, False) and seen_["beside"] == (True, False, True, False),
        f"refused, printed, placed, labelled by form — alone {seen_['alone']}, beside {seen_['beside']}")


CLOSED_WORDS = ("refused: Owner commit", "cannot be verified", "fetch it whole")


def rows_closed_history(area, add):
    """R14 where a clone cannot read the default branch's history whole. The default branch names the Owner, signed, and lists their key;
    every commit on its line is the Owner's, signed. Each clone of it carries one commit under the Owner's address on a branch of its own: a
    clone of depth 2, one with the root alone cut, one of depth 2 whose commit is signed with the Owner's key, one of depth 1 on a branch
    whose fork point it does not hold, and one made by `git init` and `git fetch --depth 2`. Each is refused, the signed one too, and says
    the way through; the clones that hold the whole history judge as before."""
    r = Ledger(area / "closed").start(owner=(STAYS,), signers=((STAYS, "owner"),), who=STAYS)
    for n in (1, 2, 3):
        (r.root / "notes.md").write_text("".join(f"line {i}\n" for i in range(1, n + 1)), encoding="utf-8")
        r.commit(f"notes, line {n}", who=STAYS, key="owner")
    r.switch("-c", "cut-owner", "main~1")
    (r.root / "notes.md").write_text("a line on a branch whose fork point a cut clone lacks\n", encoding="utf-8")
    git(r.root, "add", "-A")
    git(r.root, "commit", "-q", "-m", "a commit under the Owner's address, unsigned", who=STAYS)
    r.switch("main")
    git(r.root, "push", "-q", "origin", "main", "cut-owner")
    count = int(git(r.root, "rev-list", "--count", "main").strip())

    def clone(name, *how):
        c = area / name
        if how == ("fetch",):
            c.mkdir()
            git(c, "init", "-q", "--initial-branch=main")
            git(c, "remote", "add", "origin", f"file://{r.origin}")
            git(c, "fetch", "-q", "--depth", "2", "origin", "main")
            git(c, "remote", "set-head", "origin", "main")
        else:
            git(area, "clone", "-q", *how, f"file://{r.origin}", str(c))
        for k, v in (("gpg.format", "ssh"), ("gpg.ssh.allowedSignersFile", f"{REL}/allowed_signers"), ("commit.gpgsign", "false")):
            git(c, "config", k, v)
        return c

    def owner_commit(c, branch, key=None):
        git(c, "switch", "-q", "-c", branch, "origin/main")
        with open(c / "notes.md", "a", encoding="utf-8", newline="\n") as f:
            f.write("a line under the Owner's address\n")
        git(c, "add", "-A")
        git(c, "commit", "-q", "-m", "a commit under the Owner's address", *(["-S"] if key else []), who=STAYS, sign=r.keys[key] if key else None)
        return c

    check = lambda c: run(c, "--check", who=SEAT)
    shallow = lambda c: git(c, "rev-parse", "--is-shallow-repository").strip() == "true"
    whole, two = owner_commit(clone("full"), "unsigned-owner"), owner_commit(clone("shallow2", "--depth", "2"), "unsigned-owner")
    kept, said = check(whole), check(two)
    add("R14 on a closed history · a clone of depth 2: the Owner's unsigned commit is refused with the way through, fetch the history whole — and "
        "with the whole history the same commit is refused as before", shallow(two) and refused(said, *CLOSED_WORDS)
        and refused(kept, "carries no verified signature of the Owner's") and not shallow(whole), seen(said) + " · " + seen(kept))
    deep = owner_commit(clone("deep", "--depth", str(count - 1)), "unsigned-owner")
    said = check(deep)
    add(f"R14 on a closed history · a clone whose cut is the root commit alone (depth {count - 1} of {count}): the Owner's unsigned commit is refused, "
        "with the way through", shallow(deep) and refused(said, *CLOSED_WORDS), seen(said))
    signed, kept = owner_commit(clone("signed2", "--depth", "2"), "signed-owner", "owner"), check(owner_commit(clone("full-signed"), "signed-owner", "owner"))
    said = check(signed)
    add("R14 on a closed history · a clone of depth 2: the Owner's commit signed with their own key is refused too, nothing verifying there, with "
        "the way through — and with the whole history the same commit passes", shallow(signed) and refused(said, *CLOSED_WORDS)
        and accepted(kept, "refused: Owner commit"), seen(said) + " · " + seen(kept))
    cut = clone("cut1", "--depth", "1", "--no-single-branch")
    git(cut, "switch", "-q", "cut-owner")
    said = check(cut)
    add("R14 on a closed history · a clone of depth 1 on a branch whose fork point it does not hold: the Owner commit range cannot be read, and is "
        "refused so", shallow(cut) and refused(said, "refused: the Owner commit range cannot be read"), seen(said))
    fetched = owner_commit(clone("fetched", "fetch"), "unsigned-owner")
    said = check(fetched)
    add("R14 on a closed history · a clone made by `git init` and `git fetch --depth 2`: the Owner's unsigned commit is refused, with the way through",
        shallow(fetched) and refused(said, *CLOSED_WORDS), seen(said))


ASK_CLOSED = "the commit that set `next: owner` cannot be verified — this clone cannot verify: origin/main: its history"


def rows_closed_asks(area, add):
    """The open asks where a clone cannot read the default branch's history whole. The default branch names the Owner, signed, and lists
    their key; it holds six open asks put under the Owner's identity, and every commit on its line is the Owner's, signed. A clone of depth 1
    and one of depth 2, nothing added to either: each still refuses, each ask's line names the closed history and the way through, fetch it
    whole, as this clone's own finding — the summary does not send the reader to the trackers — and with the whole history the same asks
    pass."""
    r = Ledger(area / "asks").start(owner=(STAYS,), signers=((STAYS, "owner"),), who=STAYS)
    for n in (1, 2, 3):
        (r.root / "notes.md").write_text("".join(f"line {i}\n" for i in range(1, n + 1)), encoding="utf-8")
        r.commit(f"notes, line {n}", who=STAYS, key="owner")
    git(r.root, "push", "-q", "origin", "main")

    def clone(name, *how):
        c = area / name
        git(area, "clone", "-q", *how, f"file://{r.origin}", str(c))
        for k, v in (("gpg.format", "ssh"), ("gpg.ssh.allowedSignersFile", f"{REL}/allowed_signers"), ("commit.gpgsign", "false")):
            git(c, "config", k, v)
        return c

    whole = clone("whole")
    kept = run(whole, "--check", who=SEAT)
    for depth in ("1", "2"):
        c = clone(f"depth{depth}", "--depth", depth)
        said = run(c, "--check", who=SEAT)
        lines = said[2].splitlines()
        named = all(any(f"{tid}: {ASK_CLOSED}" in l and l.rstrip().endswith("fetch it whole") for l in lines) for tid in EARLIER)
        add(f"open asks on a closed history · a clone of depth {depth}, nothing added: it still refuses, each ask's line names the closed history "
            "and says fetch it whole, and the summary does not say fix the tracker — and with the whole history the same asks pass",
            git(c, "rev-parse", "--is-shallow-repository").strip() == "true" and said[0] == fm.EXIT_LINT and named and "fix the tracker" not in said[2]
            and accepted(kept, "next: owner"), seen(said) + " · " + seen(kept))


ROWS = (rows_single_start, rows_display, rows_current_ask, rows_state_selection, rows_state_gaps, rows_same_landing, rows_state_inherited, rows_state_material,
        rows_state_boundary, rows_state_unread, rows_state_prelude, rows_steps, rows_after, rows_new_answer, rows_other_order, rows_one_line, rows_refused,
        rows_refused_branches, rows_key_later, rows_named_later, rows_key_left, rows_first_state, rows_lines, rows_cost, rows_unsigned_owner, rows_answerers,
        rows_removed_owner, rows_current_state, rows_current_signers, rows_tip_unread, rows_signers_deleted, rows_first_key, rows_first_key_narrow,
        rows_merge_rejected, rows_unhealed, rows_closed_history, rows_closed_asks, rows_order_private, rows_form_free)


MUTANTS = (
    ("alternate initial selection", "filed_line", "enrolled = enrolled or filed_material(landing)[4]", "enrolled = enrolled", (rows_state_prelude,)),
    ("alternate missing material", "filed_read", 'unavailable = out is None or any(modes.get(path) in ("100644", "100755") and got.get(f"{rev}:{path}") is None for path in paths)', "unavailable = False", (rows_state_prelude,)),
    ("alternate boundary selection", "filed_line", ' and (git_out("rev-parse", "--is-shallow-repository") or "").strip() == "false"', "", (rows_state_boundary,)),
    ("alternate unavailable history", "filed_tip", "if not line[3]:\n        return None, True", "if not line[3]:\n        return None, False", (rows_state_unread,)),
    ("alternate material selection", "filed_state", 'at if trusted_signers()["rel"] else None', "at if held else None", (rows_state_material,)),
    ("an alternate supplied state", "filed_line", "not candidate[3] and (not different or supplied)", "not candidate[3]", (rows_state_inherited,)),
    ("one initial identity remains alone", "owners_of", "out.update(seat_identities(value))", "out.update(seat_identities(value)[:1])", (rows_single_start,)),
    ("display uses the literal identity", "identity_label", "if identity in before:", "if False:", (rows_display, rows_order_private)),
    ("the label chosen by the address's form", "identity_label", "    named, before, unread = owner_named()\n",
     "    named, before, unread = owner_named()\n    if \"noreply\" in identity:\n        return \"the Owner's forge noreply address\"\n", (rows_form_free,)),
    ("the current Owner path uses the current key", "seat_problems", "if theirs:", 'if theirs and seat_of(name, email) != "owner":', (rows_current_ask,)),
    ("alternate state selection", "filed_line", "if all(filed_transition(c, parents[c], accepted, produced, c in vouched) for c in candidates) and not candidate[3]", "if not candidate[3]", (rows_state_selection, rows_state_gaps)),
    ("an answer with an id judged by the default branch's tip", "answer_commits", "then = filed_state(sha)", "then = None", (rows_after,)),
    ("an answer by its line judged by the default branch's tip", "lint", 'then = filed_state(commit) if how == "git" else None', "then = None", (rows_after,)),
    ("a filed commit's keys read from the tip", "answer_commits", "not verified_as(sha, identity, at)", "not verified_as(sha, identity)", (rows_after,)),
    ("the state the landing commit itself leaves", "filed_state", "at = _FILED_STATES.get(chain[position - 1]) if position else None", "at = _FILED_STATES.get(landing)", (rows_same_landing,)),
    ("an author the default branch did not name then passes by what it says now", "lint", "elif then and not filed and not attested:", "elif False:", (rows_named_later,)),
    ("a key the signers file did not hold then verifies by the file as it is now", "lint", "if not verified_as(commit, filed[0], then[2]):",
     "if not verified_as(commit, filed[0]):", (rows_key_later,)),
    ("a state that names nobody is not passed over", "filed_state", "if position <= place[first]:",
     "if False:", (rows_first_state,)),
    ("the identity git names first decides", "verified_as", '"-c", f"gpg.ssh.allowedSignersFile={signers_held(identity, at)}"',
     '"-c", f"gpg.ssh.allowedSignersFile={signers_now()[\'file\']}"', (rows_steps,)),
    ("the guard reads the identity git names first", "guard_verdicts", "(signer.strip() == identity or verified_as(c, identity))", "signer.strip() == identity", (rows_steps,)),
    ("a line that lists two identities holds its key for neither", "signers_rows", "if identity in names and rest and", "if names == [identity] and rest and", (rows_one_line,)),
    ("a line whose list negates an identity is read", "signers_rows", ' and not any(w.startswith("!") for w in names)]', "]", (rows_lines,)),
    ("the Owner's own ask read by the checkout's seats alone", "seat_problems", "if theirs:", "if False and theirs:", (rows_after,)),
    ("the session registry prints the address", "session_rows", '("owner" if filed_owner(full.get(sha), name, email) else identity_label(email or name))', "identity_label(email or name)", (rows_after,)),
    ("the default branch's line read for every commit", "filed_line", "if _FILED is None:", "if True:", (rows_cost,)),
    ("an identity of the state in force that is not `signed` changes nothing", "filed_vouched",
     'mode != "signed" or (keys is not None and verified_as(commit, who, keys))', "keys is not None and verified_as(commit, who, keys)", (rows_unsigned_owner, rows_answerers)),
    ("a merge counts where its state equals any parent's", "filed_transition",
     "return len(parents) > 1 and (state == filed_material(at) or state in produced)", "return len(parents) > 1 and any(state == filed_material(p) for p in parents)", (rows_merge_rejected,)),
    ("a verified commit is taken whatever paths it leaves unhealed", "filed_line", "made[c] and made[c] >= unhealed and ", "made[c] and ", (rows_unhealed,)),
    ("a commit the default branch does not hold judged by that branch as it stands", "filed_state", "        return filed_now()", "        return None", (rows_current_state,)),
    ("the Owner the guard and R14 read taken from the default branch's tip", "owners_now", "if len(said) > seen or (at is None and not closed):", "if True:", (rows_current_state,)),
    ("an ask by an Owner the checkout names and the state in force does not", "seat_problems", 'if how == "git" and seat == "owner" and filed_state(commit) is not None:',
     "if False:", (rows_current_state,)),
    ("the signers file the guard reads taken from the default branch's tip", "signers_args", 'held = signers_now()["file"]',
     'held = trusted_signers()["file"]', (rows_current_signers,)),
    ("an identity's keys in force taken from the default branch's tip", "signers_held", 'text, now = None, signers_now()["file"] if not key[2] else None',
     'text, now = None, trusted_signers()["file"] if not key[2] else None', (rows_current_signers,)),
    ("whether a signers file is in force asked of the default branch's tip", "signers_gap", 'return signers_now()["why"]', 'return trusted_signers()["why"]', (rows_current_signers,)),
    ("a change at the tip that cannot be read leaves the state before it in force", "filed_tip", "(tip and (tip[3] or tip[4])) or ", "", (rows_tip_unread,)),
    ("a state's own signers file stopped by the tip's missing one", "verified_as", "(at is None and signature_gap(commit))", "signature_gap(commit)", (rows_signers_deleted,)),
    ("a state's signers file read only where the tip holds one", "signers_held", "        if key[2]:", '        if key[2] and trusted_signers()["file"]:', (rows_signers_deleted,)),
    ("today's answerers asked before the state an answer was filed in", "lint", "if judged is None and not allowed:", "if not allowed:", (rows_removed_owner,)),
    ("today's `answerers` list asked before the state an answer was filed in", "lint", 'elif judged is None and not SEATS and t.get("answered_by") not in allowed:',
     'elif not SEATS and t.get("answered_by") not in allowed:', (rows_answerers,)),
    ("a first key proved by the state that holds none", "filed_vouched", "keys = filed_keys(commit, at)", "keys = at", (rows_first_key,)),
    ("a commit's own key proves it where a key is enrolled", "filed_keys", 'if not trusted_signers()["rel"] or filed_keyed(filed_material(at)[2]):', 'if not trusted_signers()["rel"]:', (rows_first_key_narrow,)),
    ("a first key proves a commit that names another identity", "filed_keys", "mine[:2] == filed_material(at)[:2] and ", "", (rows_first_key_narrow,)),
    ("R14 on a closed history names no Owner again", "owner_signature_problems", "owners = owners_at(trunk, [], owner_only=True)", "return []",
     (rows_closed_history,)),
    ("R14 on a closed history verifies against the default branch's tip", "owner_signature_problems", "(not closed and verified_owner(commit))",
     "(verified_as(commit, email, trunk) if closed else verified_owner(commit))", (rows_closed_history,)),
    ("an ask on a closed history refused as one the state in force does not name", "seat_problems", "if filed_tip()[1]:", "if False:",
     (rows_closed_asks,)),
)


def run_mutants(*, results=None, only=None):
    """Each mutant, as (label, whether it turned a row red, what it saw): its rows run under it, and at least one must fail — with `only`,
    the mutants whose rows `only` names."""
    results = [] if results is None else results
    for label, name, old, new, rows in MUTANTS:
        if only and not any(rows_.__name__ in only for rows_ in rows):
            continue
        reds, broke = [], ""
        try:
            with mutated(name, old, new), tempfile.TemporaryDirectory(prefix="shoalmark-filed-m-") as tmp:
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
    with tempfile.TemporaryDirectory(prefix="shoalmark-filed-") as tmp:
        area = Path(tmp).resolve()
        for n, rows_ in enumerate(ROWS):
            if rows and rows_.__name__ not in rows:
                continue
            try:
                rows_(area / f"r{n}", add)
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
