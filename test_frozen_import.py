"""The frozen rule's class test, and the refusal of a project below the top of its git repository.

A tracker that the Owner's own signed import commit adds already `Shipped` — the commit carries `Tracker-import: <repository> <commit>` —
is frozen: the Shipped rule finds no move for it, and `--check` says in one line how many trackers are frozen and by which import commit.
The same commit unsigned, by a seat, or with a trailer out of its form freezes nothing, and each tracker it adds is refused; a tracker the
import modifies is judged; a later move of a tracker that is not frozen is judged as ever; a frozen tracker reopened and shipped again is
judged, and stays unfrozen. With the hooks on, the commit hook runs before the commit's trailer and signature exist: it leaves the trackers a
commit adds already `Shipped` to `--check` and says so in one line, so the Owner's signed import is made and frozen, a seat's same commit is
made and refused by `--check`, and a move of a tracker present at a parent is refused by the hook as before. A run whose project root is
below the top of its git repository is refused in one line, a run at the top is not, and `--version` and `--help` still run below the top.

Each row builds its history in a scratch repository — test_ask_ids' `Repo`: a bare `origin` whose `main` is the default branch, the Owner
named `signed`, their key in the default branch's signers file, a planner seat — runs the tool in this process, and states its verdict as
one check made of steps, each of which must hold: every row fails on a tool without the rule. Each mutant patches one function of the
imported module — and of the hooks' copy of the tool, where a row runs the hooks — and must turn at least one row red. A function this tool
lacks fails the row that asks for it.

Run: `python3 test_frozen_import.py` — exit 1 on a failure; `python3 test_frozen_import.py rows_<name> …` runs those rows alone, without the
mutants, and with `--with-mutants` beside them, with the mutants that run those rows; `--no-mutants` runs every row and no mutant.
test_shoalmark.py runs it as it runs test_filed_state.py. No network: every repository is a scratch one, `origin` a bare one beside it.
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
from test_ask_ids import ENV, OWNER, REL, SEAT, Repo, git, mutated, run, seen, text, write  # noqa: E402

FOREIGN = "766476abcaab912a1f752d67d28fa5cd5bc93d36"            # a commit of the code repository the trackers come from: this one does not hold it
TRAILER = f"Tracker-import: shoalmark/shoalmark {FOREIGN}"
IMPORTED = [f"FM-{n}" for n in range(101, 149)]                 # 48 trackers, Shipped where they were built
NAMING = IMPORTED[:39]                                          # 39 name a commit only the code repository holds, the other 9 name none
REFUSED = "moved to `Shipped` with no commit behind it"
NOT_VERIFIED = "and does not verify as the Owner's own signed commit, so it freezes nothing"


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


def shipped(tid, row):
    """A tracker as the code repository shipped it: `Shipped`, a ticked done item, and `row` its ship log's one row."""
    return (f'---\nid: {tid}\nstatus: Shipped\nconsidered: none\nhook: "h of {tid}"\n---\n\n# {tid} — t\n\n'
            f"## What is true now\n\nShipped.\n\n## Done when\n\n- [x] it is.\n\n## Ship log\n\n| Date | Event |\n|---|---|\n| 2026-09-30 | {row} |\n")


def imported(tid):
    return shipped(tid, f"built in {FOREIGN[:7]}" if tid in NAMING else "Filed.")


def frozen_said(said):
    """The frozen rule's line on `--check`'s stdout, or ""."""
    return next((l for l in said[1].splitlines() if l.startswith("frozen trackers:")), "")


def refused_for(said, ids, saying=""):
    """Each of `ids` refused by the Shipped rule's own line — a line that also says `saying`, where given."""
    lines = said[2].splitlines()
    return all(any(l.strip().startswith(f"lint: {tid}:") and REFUSED in l and saying in l for l in lines) for tid in ids)


def named(said, ids):
    """The ids of `ids` any refusal line names."""
    return [tid for tid in ids if any(f"{tid}:" in l for l in said[2].splitlines())]


def repo(area):
    """The ledger before the import: two open trackers, and a product file, on `main`, the Owner's signed commit."""
    r = Repo(area, {"FM-001": text("FM-001"), "FM-002": text("FM-002")})
    (r.root / "src").mkdir()
    (r.root / "src" / "app.py").write_text("v0\n", encoding="utf-8")
    r.commit("the product", who=OWNER, sign=True)
    git(r.root, "push", "-q", "origin", "main")
    git(r.root, "fetch", "-q", "origin")
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
    """A copy of the row area's seed: "before" the import, or "import" — the Owner's signed import on its branch `import`, every one of
    `IMPORTED` added already Shipped. Each seed is built once under the folder a run's rows share."""
    home = area.parent
    if (home, "before") not in _SEEDS:
        _SEEDS[(home, "before")] = repo(home / "seed-before")
    if kind == "import" and (home, "import") not in _SEEDS:
        r = copied(_SEEDS[(home, "before")], home / "seed-import")
        made_import(r)
        _SEEDS[(home, "import")] = r
    return copied(_SEEDS[(home, kind)], area)


def made_import(r, who=OWNER, sign=True, trailer=TRAILER, modify=()):
    """The import on the branch `import`: every one of `IMPORTED` added already Shipped — and each of `modify`, an open tracker, moved to
    Shipped — committed by `who`, signed with the Owner's key where `sign`, carrying `trailer`. Its commit."""
    r.switch("-c", "import")
    for tid in IMPORTED:
        write(r.root, tid, imported(tid))
    for tid in modify:
        write(r.root, tid, r.read(tid).replace("status: In Progress", "status: Shipped"))
    return r.commit("the trackers, imported from the code repository", who=who, sign=sign, trailers=(trailer,) if trailer else ())


# --- the Owner's signed import passes, and --check says what it froze ------------------------------------------------------------

def rows_signed_import(area, add):
    r = seeded(area, "import")
    sha = r.head()
    s = Steps()
    said = r.check()
    s("the import on its branch passes, no tracker it adds refused", said[0] == 0 and not named(said, IMPORTED), said)
    want = f"frozen trackers: 48 — added already `Shipped` by the import commit {sha[:7]} (Tracker-import: shoalmark/shoalmark {FOREIGN})"
    s("--check names 48 frozen, and the import commit's short hash with its trailer", frozen_said(said).startswith(want), extra=repr(frozen_said(said)))
    r.land("import")
    said = r.check()
    s("landed on main: passes, and still 48 frozen by that commit", said[0] == 0 and frozen_said(said).startswith(want), said, repr(frozen_said(said)))
    s.add(add, "the Owner's signed import adding 48 Shipped trackers passes — 39 naming a commit only the code repository holds, 9 naming none — "
               "on its branch and landed, and --check names 48 frozen and the import commit with its trailer")


def rows_modified_by_import(area, add):
    r = seeded(area, "before")
    made_import(r, modify=("FM-002",))
    s = Steps()
    said = r.check()
    s("the tracker the import modifies to Shipped is refused by the Shipped rule", said[0] == fm.EXIT_LINT and refused_for(said, ["FM-002"]), said)
    s("no tracker the import adds is refused", not named(said, IMPORTED), said)
    s("--check names the 48 it adds as frozen, not the one it modifies", frozen_said(said).startswith("frozen trackers: 48 —"), extra=repr(frozen_said(said)))
    s.add(add, "the Owner's signed import that also moves an open tracker to Shipped: that one is judged and refused, the 48 it adds are frozen")


# --- the same commit unsigned, by a seat, or with its trailer out of form freezes nothing ------------------------------------------

def rows_unverified_import(area, add):
    s = Steps()
    for n, (what, who, sign, trailer, note) in enumerate((
            ("the Owner's commit, unsigned", OWNER, False, TRAILER, True),
            ("a seat's commit, unsigned", SEAT, False, TRAILER, True),
            ("a seat's commit, signed with the Owner's key", SEAT, True, TRAILER, True),
            ("the Owner's signed commit whose trailer names no commit", OWNER, True, "Tracker-import: shoalmark/shoalmark", False))):
        r = seeded(area.parent / f"{area.name}-{n}", "before")
        sha = made_import(r, who=who, sign=sign, trailer=trailer)
        said = r.check()
        s(f"{what}: each of the 48 refused by the Shipped rule", said[0] == fm.EXIT_LINT and refused_for(said, IMPORTED), said)
        if note:
            s(f"{what}: each refusal says the import freezes nothing", refused_for(said, IMPORTED, NOT_VERIFIED), said)
            s(f"{what}: --check names none frozen, and the commit that does not verify",
              frozen_said(said).startswith("frozen trackers: none —") and f"{sha[:7]} carries `{TRAILER}` {NOT_VERIFIED}" in frozen_said(said),
              extra=repr(frozen_said(said)))
        else:
            s(f"{what}: --check names none frozen, and no import commit", frozen_said(said).startswith("frozen trackers: none —") and sha[:7] not in frozen_said(said),
              extra=repr(frozen_said(said)))
    s.add(add, "the same import unsigned, by a seat — unsigned or signed with the Owner's key —, or with a trailer that names no commit freezes "
               "nothing: each of the 48 is refused, and --check names none frozen")


# --- after the import: a tracker not frozen is judged as ever, and a frozen one reopened and shipped again is judged -----------------

def product(r, v):
    """A commit that builds something — it changes the product file — by the seat: its hash."""
    (r.root / "src" / "app.py").write_text(f"{v}\n", encoding="utf-8")
    return r.commit(f"the product, {v}")


def ship(r, tid, row, status_from="In Progress"):
    r.write(tid, r.read(tid).replace(f"status: {status_from}", "status: Shipped").rstrip("\n")
            + ("\n\n## Ship log\n\n| Date | Event |\n|---|---|\n" if "## Ship log" not in r.read(tid) else "\n") + f"| 2026-11-25 | {row} |\n")
    return r.commit(f"{tid}: shipped")


def rows_later_move(area, add):
    r = seeded(area, "import")
    s = Steps()
    ship(r, "FM-001", "Done.")
    said = r.check()
    s("a later move of an open tracker naming no commit is refused, as ever", said[0] == fm.EXIT_LINT and refused_for(said, ["FM-001"]) and "its ship log names no commit" in said[2], said)
    s("…and it alone: no tracker the import added is refused", not named(said, IMPORTED), said)
    git(r.root, "reset", "-q", "--hard", "HEAD~1")
    built = product(r, "v1")
    ship(r, "FM-001", f"built in {built[:7]}")
    said = r.check()
    s("the same move naming the commit that built it passes, as ever", said[0] == 0 and not named(said, ["FM-001", *IMPORTED]), said)
    s("--check still names 48 frozen", frozen_said(said).startswith("frozen trackers: 48 —"), extra=repr(frozen_said(said)))
    s.add(add, "after the signed import, a later move to Shipped of a tracker that is not frozen is judged as today: refused naming no commit, "
               "passed naming the commit that built it; the 48 stay frozen")


def rows_reopened(area, add):
    r = seeded(area, "import")
    s = Steps()
    tid = IMPORTED[0]
    r.write(tid, r.read(tid).replace("status: Shipped", "status: In Progress"))
    said = r.check()
    s("a frozen tracker reopened in the working tree: passes, and --check names 47 frozen", said[0] == 0 and frozen_said(said).startswith("frozen trackers: 47 —"),
      said, repr(frozen_said(said)))
    r.commit(f"{tid}: reopened")
    said = r.check()
    s("a frozen tracker reopened: passes, and --check names 47 frozen", said[0] == 0 and frozen_said(said).startswith("frozen trackers: 47 —"), said, repr(frozen_said(said)))
    r.write(tid, r.read(tid).replace("status: In Progress", "status: Shipped"))
    r.commit(f"{tid}: shipped again")
    said = r.check()
    s("shipped again on the commit only the code repository holds: refused, it alone", said[0] == fm.EXIT_LINT and refused_for(said, [tid])
      and f"`{FOREIGN[:7]}` is not in the history" in said[2] and named(said, IMPORTED) == [tid], said)
    s("…and --check still names 47 frozen: the freeze ended for good", frozen_said(said).startswith("frozen trackers: 47 —"), extra=repr(frozen_said(said)))
    git(r.root, "reset", "-q", "--hard", "HEAD~1")
    built = product(r, "v2")
    ship(r, tid, f"built again in {built[:7]}")
    said = r.check()
    s("shipped again naming the commit that built it: passes, as any move does", said[0] == 0 and not named(said, IMPORTED), said)
    s("…and --check still names 47 frozen", frozen_said(said).startswith("frozen trackers: 47 —"), extra=repr(frozen_said(said)))
    s.add(add, "a frozen tracker reopened and shipped again is judged: refused on the commit only the code repository holds, passed on the "
               "commit that built it — and it stays unfrozen, so --check names 47")


# --- a project below the top of its git repository is refused; at the top it is not; --version and --help still run ----------------

def below(area):
    """A git repository at `top` whose one project sits below it, in `teams/tool`, with a tracker committed: (top, the project)."""
    top = area / "top"
    sub = top / "teams" / "tool"
    (sub / REL).mkdir(parents=True)
    git(top, "init", "-q", "--initial-branch=main")
    (sub / "shoalmark.toml").write_text('name = "tool"\n[kinds]\nFM = "Work"\n', encoding="utf-8")
    write(sub, "FM-001", text("FM-001"))
    git(top, "add", "-A")
    git(top, "commit", "-q", "-m", "the team's trackers")
    return top, sub


def program(cwd, *argv):
    """The tool as a program started in `cwd`, with no `--root`: (exit, stdout, stderr)."""
    done = subprocess.run([sys.executable, "-B", str(HERE / "shoalmark.py"), *argv], cwd=cwd, capture_output=True, text=True, encoding="utf-8",
                          errors="replace", env=dict(ENV, GIT_AUTHOR_NAME=SEAT[0], GIT_AUTHOR_EMAIL=SEAT[1], GIT_COMMITTER_NAME=SEAT[0], GIT_COMMITTER_EMAIL=SEAT[1]))
    return done.returncode, done.stdout, done.stderr


def rows_below_top(area, add):
    top, sub = below(area)
    real_top = Path(git(top, "rev-parse", "--show-toplevel").strip())
    s = Steps()
    one = lambda said: [l for l in said[2].splitlines() if l.strip()]
    line = lambda said: (one(said) or [""])[0]
    refusal = lambda said: (said[0] != 0 and len(one(said)) == 1 and "FM-161" in line(said) and str(sub) in line(said) and f", {real_top}:" in line(said))
    for argv in (("--check",), (), ("--html-only",), ("--next",)):
        said = run(sub, *argv, who=SEAT)
        s(f"below the top, {' '.join(argv) or 'the default run'}: refused in one line naming FM-161, the project root and the top", refusal(said), said, repr(line(said)))
    s("…and the default run wrote nothing", not (sub / REL / "INDEX.md").exists())
    said = program(sub, "--check")
    s("below the top, as a program started there: refused in that line", refusal(said), said, repr(line(said)))
    said = program(sub, "--version")
    s("below the top, --version runs", said[0] == 0 and said[1].strip() == fm.__version__, said)
    said = program(sub, "--help")
    s("below the top, --help runs", said[0] == 0 and said[1].startswith("usage:"), said)
    said = run(sub, "--version", who=SEAT)
    s("below the top, --version runs with --root naming the project", said[0] == 0 and said[1].strip() == fm.__version__, said)
    at = area / "at-top"
    (at / REL).mkdir(parents=True)
    git(at, "init", "-q", "--initial-branch=main")
    (at / "shoalmark.toml").write_text('name = "tool"\n[kinds]\nFM = "Work"\n', encoding="utf-8")
    write(at, "FM-001", text("FM-001"))
    run(at, who=SEAT)
    git(at, "add", "-A")
    git(at, "commit", "-q", "-m", "the team's trackers")
    said = run(at, "--check", who=SEAT)
    s("at the top, --check is not refused: it passes, and says none is frozen", said[0] == 0 and "FM-161" not in said[2]
      and frozen_said(said).startswith("frozen trackers: none —"), said, repr(frozen_said(said)))
    s.add(add, "a run from a project below the top of its git repository is refused in one line naming FM-161, the project root and the top — "
               "--check, the default run, the board's run, --next, and the program started there; a run at the top is not; --version and --help run below the top")


# --- the import made with the hooks on: the commit hook leaves the trackers a commit adds already Shipped to --check -----------------

LEFT = ("48 trackers this commit adds already `Shipped` are left to `--check`: this hook runs before the commit's trailer and signature exist. "
        "`--check` freezes them where the commit is the Owner's own signed import, carrying `Tracker-import:`, and refuses each of them otherwise")
_ACTIVE = []                                                    # the mutant running now, (function, old, new): the hooks' copy carries it too


def install(r):
    """The tool's hooks installed in the row's clone, from the default branch — their copy of the tool patched as the mutant running now
    patches the module, each function it names in place, since the hooks run that copy and not this process."""
    said = run(r.root, "--install-hook", who=OWNER)
    if said[0] != 0:
        raise RuntimeError(f"--install-hook exited {said[0]}: {said[2][-300:]}")
    copy = r.root / ".git" / fm.COPY_DIR / "shoalmark.py"
    tool = copy.read_text(encoding="utf-8")
    for name, old, new in _ACTIVE:
        at = tool.index(f"\ndef {name}(") + 1
        end = tool.index("\n\n\n", at)
        if tool[at:end].count(old) != 1:
            raise AssertionError(f"{name}: {old[:60]!r} is not in the hooks' copy exactly once")
        tool = tool[:at] + tool[at:end].replace(old, new) + tool[end:]
    with open(copy, "w", encoding="utf-8", newline="\n") as f:
        f.write(tool)


def hooked(r, who, message, *more, sign=False):
    """`git commit` in the row's clone as `who`, the hooks on, with `message` and `more` as its message lines — signed with the Owner's key
    where `sign`: (exit, what git and the hooks printed). The hooks' copy names the tool as this process does, so the INDEX.md it writes is
    the one `--check` here expects."""
    fm.configure(r.root)
    try:
        cmd = fm.CMD
    finally:
        fm.configure(HERE)
    env = dict(ENV, SHOALMARK_CMD=cmd, GIT_AUTHOR_NAME=who[0], GIT_AUTHOR_EMAIL=who[1], GIT_COMMITTER_NAME=who[0], GIT_COMMITTER_EMAIL=who[1])
    lines = [x for m in (message, *more) for x in ("-m", m)]
    done = subprocess.run(["git", "-C", str(r.root), "-c", "commit.gpgsign=false", "commit", "-q", *lines, *(["-S"] if sign else [])],
                          capture_output=True, text=True, encoding="utf-8", errors="replace", env=env)
    return done.returncode, done.stdout + done.stderr


def staged_import(r):
    """The 48 trackers written on the branch `import`, INDEX.md as the tool writes it, and everything staged: the import, not yet made."""
    r.switch("-c", "import")
    for tid in IMPORTED:
        write(r.root, tid, imported(tid))
    run(r.root, "--print-written", who=OWNER)
    git(r.root, "add", "-A")


def rows_hooked_import(area, add):
    s = Steps()
    r = seeded(area, "before")
    install(r)
    staged_import(r)
    said = r.check()
    s("--check on the import staged, not yet made: each of the 48 refused as before, and no tracker left to it",
      said[0] != 0 and refused_for(said, IMPORTED) and "left to `--check`" not in said[2], said)
    before = r.head()
    code, printed = hooked(r, OWNER, "the trackers, imported from the code repository", TRAILER, sign=True)
    sha = r.head()
    s("the Owner's signed import, made with the hooks on: the commit is made", code == 0 and sha != before, extra=f"exit {code}: {printed[-600:]!r}")
    s("…and the commit hook prints the line: 48 left to --check, why, and what --check does with them", printed.count(LEFT) == 1, extra=repr(printed[-600:]))
    s("…and the commit carries its trailer", TRAILER in git(r.root, "log", "-1", "--format=%B"))
    said = r.check()
    want = f"frozen trackers: 48 — added already `Shipped` by the import commit {sha[:7]} (Tracker-import: shoalmark/shoalmark {FOREIGN})"
    s("--check on the made import passes, and names 48 frozen by that commit", said[0] == 0 and not named(said, IMPORTED) and frozen_said(said).startswith(want),
      said, repr(frozen_said(said)))
    r.write("FM-001", r.read("FM-001").replace("status: In Progress", "status: Shipped").rstrip("\n") + "\n\n## Ship log\n\n| Date | Event |\n|---|---|\n| 2026-11-25 | Done. |\n")
    git(r.root, "add", "-A")
    code, printed = hooked(r, OWNER, "FM-001: shipped", sign=True)
    s("a move to Shipped of a tracker present at the parent, no commit behind it, is refused by the commit hook as before: the commit is not made",
      code != 0 and r.head() == sha and f"FM-001: {REFUSED} — its ship log names no commit" in printed and "left to `--check`" not in printed,
      extra=f"exit {code}: {printed[-600:]!r}")
    git(r.root, "reset", "-q", "--hard")
    seat = seeded(area.parent / f"{area.name}-seat", "before")
    install(seat)
    staged_import(seat)
    before = seat.head()
    code, printed = hooked(seat, SEAT, "the trackers, imported from the code repository", TRAILER)
    sha = seat.head()
    s("a seat's commit adding the same 48 Shipped trackers, with the hooks on: the commit is made, with the line",
      code == 0 and sha != before and printed.count(LEFT) == 1, extra=f"exit {code}: {printed[-600:]!r}")
    said = seat.check()
    s("…and --check refuses each of the 48, saying the import freezes nothing", said[0] == fm.EXIT_LINT and refused_for(said, IMPORTED, NOT_VERIFIED)
      and frozen_said(said).startswith("frozen trackers: none —"), said, repr(frozen_said(said)))
    s.add(add, "the import made with the hooks on: the Owner's signed import is made, the commit hook says 48 are left to --check, and --check "
               "passes naming 48 frozen; a seat's same commit is made with that line and --check refuses each; a move of a tracker present at the "
               "parent is refused by the hook as before; --check on the import not yet made refuses each")


ROWS = (rows_signed_import, rows_modified_by_import, rows_unverified_import, rows_later_move, rows_reopened, rows_below_top, rows_hooked_import)


# Each mutant: (what it breaks, the function it patches, the text it replaces, its replacement, the rows that must catch it).
MUTANTS = (
    ("the freeze not applied: the import's trackers judged as moves", "shipped_moves", "if frozen and rel in added:", "if False:", (rows_signed_import,)),
    ("a later move frozen once any import that verifies is on the history", "shipped_moves", "if frozen and rel in added:",
     "if (frozen and rel in added) or bool(tracker_imports() and tracker_imports()[0]):", (rows_later_move,)),
    ("the trailer accepted from any committer", "import_freezes", "    if not import_verified(commit, name, email):\n", "    if False:\n",
     (rows_unverified_import,)),
    ("any signed commit counted, whoever authored it", "import_verified",
     '_IMPORTS[commit] = bool(theirs) and theirs[1] == "signed" and verified_as(commit, theirs[0], theirs[2])', '_IMPORTS[commit] = signature_kind(commit) == "ssh"',
     (rows_unverified_import,)),
    ("a trailer read in any form", "import_value", "if IMPORT_VALUE_RE.fullmatch(v)", "if v", (rows_unverified_import,)),
    ("a tracker modified, not added, by the import also frozen", "shipped_moves",
     "added = {rel for rel in shipped if all(before.get(spec(base, rel)) is None for base in bases)}", "added = set(shipped)", (rows_modified_by_import,)),
    ("the unfreeze not lasting", "frozen_left", "    return set(froze) - {", "    return set(froze) or {", (rows_reopened,)),
    ("a tracker reopened in the working state counted frozen", "frozen_line", "for sha, _v, froze in held)) & now", "for sha, _v, froze in held))", (rows_reopened,)),
    ("the refusal below the top skipped", "main_run", "    refused = below_top()                                   #", "    refused = ''                                            #",
     (rows_below_top,)),
    ("the board's run below the top not refused", "board_run", "refused = below_top() or tracker_folder_problem()", "refused = tracker_folder_problem()",
     (rows_below_top,)),
    ("a run at the top refused too", "below_top", '    if not prefix:\n        return ""\n', "", (rows_below_top,)),
    ("the commit hook's deferral applied to a tracker present at a parent", "shipped_moves", "later = added if COMMITTING and not commit else set()",
     "later = set(shipped) if COMMITTING and not commit else set()", (rows_hooked_import,)),
    ("the commit hook's deferral with no line", "shipped_moves", "    if left:\n", "    if False:\n", (rows_hooked_import,)),
    ("the deferral in --check too, not only in the commit hook's run", "shipped_moves", "if COMMITTING and not commit else set()", "if not commit else set()",
     (rows_hooked_import,)),
)


def run_mutants(*, results=None, only=None):
    """Each mutant, as (label, whether it turned a row red, what it saw): its rows run under it, and at least one must fail — with `only`,
    the mutants whose rows `only` names."""
    results = [] if results is None else results
    for label, name, old, new, rows in MUTANTS:
        if only and not any(rows_.__name__ in only for rows_ in rows):
            continue
        reds, broke = [], ""
        _ACTIVE[:] = [(name, old, new)]
        try:
            with mutated(name, old, new), tempfile.TemporaryDirectory(prefix="shoalmark-frozen-m-") as tmp:
                area = Path(tmp).resolve()
                for n, rows_ in enumerate(rows):
                    rows_(area / f"m{n}", lambda l, ok, saw="": reds.append(l) if not ok else None)
        except AssertionError as e:
            broke = str(e)
        except Exception as e:
            reds.append(f"a row crashed: {type(e).__name__}: {str(e)[:120]}")
        finally:
            _ACTIVE[:] = []
            fm.configure(HERE)
        results.append((f"mutant · {label}: at least one row turns red", bool(reds) and not broke, broke or "no row turned red"))
    return results


def run_checks(*, results=None, mutants=True, rows=None):
    """Every row — or the row functions `rows` names — then every mutant, as (label, ok, what it saw)."""
    results = [] if results is None else results
    add = lambda label, ok, saw="": results.append((label, bool(ok), "" if ok else saw))
    with tempfile.TemporaryDirectory(prefix="shoalmark-frozen-") as tmp:
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
