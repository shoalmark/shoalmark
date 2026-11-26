"""The frozen rule's class test, and a project below the top of its git repository judged as one at the top.

A tracker that the Owner's own signed import commit adds already `Shipped` — the commit carries `Tracker-import: <repository> <commit>` —
is frozen: the Shipped rule finds no move for it, and `--check` says in one line how many trackers are frozen and by which import commit.
The same commit unsigned, by a seat, or with a trailer out of its form freezes nothing, and each tracker it adds is refused; a tracker the
import modifies is judged; a later move of a tracker that is not frozen is judged as ever; a frozen tracker reopened and shipped again is
judged, and stays unfrozen. `--check` counts what the rule freezes: a tracker the import renames onto `Shipped` is present at the parent
by its id, so the rule judges it and the count leaves it out; a later file named for a frozen tracker below the tracker folder, even one
that reads `Shipped`, is no tracker's, so the count keeps that tracker. The count ends a freeze only where the rule judges a move, merges
included: a side branch's deletion that the merge does not keep moves nothing back, so the count stays 48 and nothing is refused; a merge
that deletes a frozen tracker, then the seat's commit or the seat's own merge that adds it back `Shipped`, is a move the rule refuses, and
the count says 47. With the hooks on, the commit hook runs before the commit's trailer and signature exist: it leaves the trackers a
commit adds already `Shipped` to `--check` and says so in one line, so the Owner's signed import is made and frozen, a seat's same commit is
made and refused by `--check`, and a move of a tracker present at a parent is refused by the hook as before. A run whose project root is
below the top of its git repository is judged as the same project at the top is: the same exit, the same lines and the same INDEX.md,
and `--version` and `--help` run there. Below the top, the tracker folder at a revision is read whole, as at the top: `--check` counts the
48 the Owner's signed import freezes, a tracker the import renames onto `Shipped` is found at the parent by its id and refused, and a
later commit that renames a frozen tracker is no move. Four rules more: an import with no parent here, the root of an unrelated history merged in,
freezes nothing; an act run such as `--install-hook` does below the top what it does at the top; the commit hook judges what a merge
being made brings, and leaves to `--check` only what the commit being made adds; and the freeze needs an Owner whom the configuration
marks `signed`.

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
from test_ask_ids import CONFIG, ENV, OWNER, REL, SEAT, Repo, git, mutated, run, seen, text, write  # noqa: E402

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


class Below(Repo):
    """test_ask_ids' Repo with its project below the top of its git repository, in `teams/tool`: the clone at `wc`, the project — its
    configuration, its signers file and its trackers — at `wc/teams/tool`, and every git command and run made from the project."""

    def __init__(self, base, trackers=None):
        top = base / "wc"
        self.base, self.root, self.origin = base, top / "teams" / "tool", base / "origin.git"
        self.root.mkdir(parents=True)
        self.keys = {}
        for name in ("owner", "other"):
            key = base / f"key-{name}"
            subprocess.run(["ssh-keygen", "-q", "-t", "ed25519", "-N", "", "-f", str(key), "-C", name], check=True, capture_output=True)
            self.keys[name] = key
        (self.root / "shoalmark.toml").write_text(CONFIG, encoding="utf-8")
        git(base, "init", "-q", "--bare", "--initial-branch=main", str(self.origin))
        git(top, "init", "-q", "--initial-branch=main")
        for k, v in (("user.name", OWNER[0]), ("user.email", OWNER[1]), ("gpg.format", "ssh"), ("user.signingkey", str(self.keys["owner"])),
                     ("gpg.ssh.allowedSignersFile", f"teams/tool/{REL}/allowed_signers"), ("commit.gpgsign", "false")):
            git(top, "config", k, v)
        git(top, "remote", "add", "origin", str(self.origin))
        (self.root / ".gitignore").write_text(f"{REL}/index.html\n{REL}/view/\n", encoding="utf-8")
        self.signers(f"{OWNER[1]} " + self.keys["owner"].with_suffix(".pub").read_text(encoding="utf-8"))
        for tid, body in (trackers or {}).items():
            write(self.root, tid, body)
        self.commit("the start", who=OWNER, sign=True)
        git(top, "push", "-q", "-u", "origin", "main")
        git(top, "remote", "set-head", "origin", "main")
        run(self.root, "--print-written")
        if git(top, "status", "--porcelain"):
            self.commit("the index, with the default branch known", who=OWNER, sign=True)
            git(top, "push", "-q", "origin", "main")


def repo(area, below=False):
    """The ledger before the import: two open trackers, and a product file, on `main`, the Owner's signed commit — its project below the
    top of its repository where `below`."""
    r = (Below if below else Repo)(area, {"FM-001": text("FM-001"), "FM-002": text("FM-002")})
    (r.root / "src").mkdir()
    (r.root / "src" / "app.py").write_text("v0\n", encoding="utf-8")
    r.commit("the product", who=OWNER, sign=True)
    git(r.root, "push", "-q", "origin", "main")
    git(r.root, "fetch", "-q", "origin")
    return r


def copied(seed, area):
    """`seed` again under `area`, with an `origin` of its own: a Repo, or a Below, whose folders are the copy's."""
    shutil.copytree(seed.base, area)
    twin = type(seed).__new__(type(seed))
    twin.base, twin.root, twin.origin = area, area / seed.root.relative_to(seed.base), area / "origin.git"
    twin.keys = {name: area / f"key-{name}" for name in seed.keys}
    git(twin.root, "remote", "set-url", "origin", str(twin.origin))
    git(twin.root, "config", "user.signingkey", str(twin.keys["owner"]))
    return twin


_SEEDS = {}


def seeded(area, kind, below=False):
    """A copy of the row area's seed: "before" the import, or "import" — the Owner's signed import on its branch `import`, every one of
    `IMPORTED` added already Shipped —, its project below the top of its repository where `below`. Each seed is built once under the
    folder a run's rows share."""
    home, where = area.parent, "-below" if below else ""
    if (home, "before" + where) not in _SEEDS:
        _SEEDS[(home, "before" + where)] = repo(home / f"seed-before{where}", below)
    if kind == "import" and (home, "import" + where) not in _SEEDS:
        r = copied(_SEEDS[(home, "before" + where)], home / f"seed-import{where}")
        made_import(r)
        _SEEDS[(home, "import" + where)] = r
    return copied(_SEEDS[(home, kind + where)], area)


def made_import(r, who=OWNER, sign=True, trailer=TRAILER, modify=(), rename=()):
    """The import on the branch `import`: every one of `IMPORTED` added already Shipped — each of `modify`, an open tracker, moved to
    Shipped, and each of `rename`, an open tracker, moved to Shipped under a new file name — committed by `who`, signed with the Owner's
    key where `sign`, carrying `trailer`. Its commit."""
    r.switch("-c", "import")
    for tid in IMPORTED:
        write(r.root, tid, imported(tid))
    for tid in modify:
        write(r.root, tid, r.read(tid).replace("status: In Progress", "status: Shipped"))
    for tid in rename:
        was = r.read(tid)
        git(r.root, "mv", f"{REL}/{tid}-x.md", f"{REL}/{tid}-renamed-by-the-import.md")
        with open(r.root / REL / f"{tid}-renamed-by-the-import.md", "w", encoding="utf-8", newline="\n") as f:
            f.write(was.replace("status: In Progress", "status: Shipped"))
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


# --- an import with no parent here freezes nothing, nor one by an Owner whom the configuration does not mark signed --------------------

def rows_root_import(area, add):
    r = seeded(area, "before")
    r.switch("--orphan", "roots")
    for tid in IMPORTED:
        write(r.root, tid, imported(tid))
    git(r.root, "add", "--", *(f"{REL}/{tid}-x.md" for tid in IMPORTED))
    git(r.root, "commit", "-q", "-m", "the trackers, imported from the code repository", "-m", TRAILER, "-S", who=OWNER, sign=r.keys["owner"])
    root = r.head()
    r.switch("main")
    git(r.root, "merge", "-q", "--no-ff", "--no-edit", "--allow-unrelated-histories", "roots")
    r.commit("the index, with the imported trackers")
    s = Steps()
    s("the import is the root of its history: it has no parent", git(r.root, "rev-list", "--parents", "-n", "1", root).split() == [root])
    said = r.check()
    s("the Owner's signed import as the root of an unrelated history, merged into main: each of the 48 refused by the Shipped rule",
      said[0] == fm.EXIT_LINT and refused_for(said, IMPORTED), said)
    s("…each refusal says the import freezes nothing, its parent unread", refused_for(said, IMPORTED, "its parent cannot be read here, so it freezes nothing"), said)
    s("…and --check names none frozen, and the import with no parent here",
      frozen_said(said).startswith("frozen trackers: none —") and f"{root[:7]} carries `{TRAILER}` and has no parent here" in frozen_said(said),
      extra=repr(frozen_said(said)))
    s.add(add, "the Owner's signed import made as the root of an unrelated history and merged into main freezes nothing: it has no parent here to "
               "tell what it adds from what it changes, so each of the 48 is refused, and --check names none frozen")


def rows_owner_unmarked(area, add):
    r = seeded(area, "before")
    toml = r.root / "shoalmark.toml"
    was = toml.read_text(encoding="utf-8")
    with open(toml, "w", encoding="utf-8", newline="\n") as f:
        f.write(was.replace(f'owner = "{OWNER[1]} signed"', f'owner = "{OWNER[1]}"'))
    r.commit("the Owner, not marked signed", who=OWNER, sign=True)
    git(r.root, "push", "-q", "origin", "main")
    git(r.root, "fetch", "-q", "origin")
    s = Steps()
    s("the default branch's owner line names the Owner, not marked signed", f'owner = "{OWNER[1]}"\n' in git(r.root, "show", "origin/main:shoalmark.toml"))
    sha = made_import(r)
    said = r.check()
    s("the Owner's signed import, where the owner line does not mark the Owner signed: each of the 48 refused by the Shipped rule",
      said[0] == fm.EXIT_LINT and refused_for(said, IMPORTED), said)
    s("…each refusal says the import does not verify, so it freezes nothing", refused_for(said, IMPORTED, NOT_VERIFIED), said)
    s("…and --check names none frozen, and the commit that does not verify",
      frozen_said(said).startswith("frozen trackers: none —") and f"{sha[:7]} carries `{TRAILER}` {NOT_VERIFIED}" in frozen_said(said),
      extra=repr(frozen_said(said)))
    s.add(add, "where the owner line does not mark the Owner signed, the Owner's signed import freezes nothing: each of the 48 is refused, and "
               "--check names none frozen")


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


# --- --check counts what the rule freezes: a tracker the import renames is not frozen, and a note below the tracker folder is no tracker's

def rows_renamed_by_import(area, add):
    r = seeded(area, "before")
    made_import(r, rename=("FM-001",))
    s = Steps()
    said = r.check()
    s("the tracker the import renames and moves to Shipped is refused by the Shipped rule, it alone",
      said[0] == fm.EXIT_LINT and refused_for(said, ["FM-001"]) and named(said, ["FM-001", *IMPORTED]) == ["FM-001"], said)
    s("--check names the 48 it adds as frozen, not the one it renames", frozen_said(said).startswith("frozen trackers: 48 —"), extra=repr(frozen_said(said)))
    s.add(add, "the Owner's signed import that also renames an open tracker and moves it to Shipped: the rule finds that tracker at the parent "
               "by its id and refuses it, and --check counts the 48 the import adds, not that one")


def rows_later_note(area, add):
    r = seeded(area, "import")
    s = Steps()
    tid = IMPORTED[0]
    note = r.root / REL / "evidence" / f"{tid}-note.md"
    note.parent.mkdir(parents=True)
    with open(note, "w", encoding="utf-8", newline="\n") as f:
        f.write(imported(tid))                          # the tracker as the import brought it, quoted: it reads Shipped, and is still no tracker's
    r.commit(f"{tid}: a note on what the import brought", who=OWNER, sign=True)
    said = r.check()
    s("a later commit adds a note named for a frozen tracker, below the tracker folder, that quotes it as the import brought it: passes",
      said[0] == 0 and not named(said, IMPORTED), said)
    s("…and --check still names 48 frozen: the note is no tracker's file", frozen_said(said).startswith("frozen trackers: 48 —"), extra=repr(frozen_said(said)))
    s.add(add, "after the signed import, a later commit adds a note named for a frozen tracker under evidence/: that tracker stays frozen, and "
               "--check still names 48")


# --- the count ends a freeze only where the rule judges a move, merges included ---------------------------------------------------

def merged(r, branch, *, then=None):
    """`branch` merged into the branch checked out, as the seat, with a merge commit: `then(r)` runs before it is made, with the merge's
    result in the working tree, and INDEX.md is written as the tool writes it. Where the merge stops on a conflict, the working tree's
    files are taken as they are. Its commit."""
    git(r.root, "merge", "-q", "--no-ff", "--no-commit", branch, check=False)
    if then:
        then(r)
    run(r.root, "--print-written", who=SEAT)
    git(r.root, "add", "-A")
    git(r.root, "commit", "-q", "--no-edit")
    return r.head()


def rows_side_deletion_kept(area, add):
    r = seeded(area, "import")
    s = Steps()
    tid = IMPORTED[0]
    r.switch("-c", "side")
    git(r.root, "rm", "-q", f"{REL}/{tid}-x.md")
    r.commit(f"{tid}: deleted on a side branch")
    r.switch("import")
    r.write(tid, r.read(tid) + "\nA note after the import.\n")
    r.commit(f"{tid}: a note")
    m = merged(r, "side")                               # the modify/delete conflict, resolved by keeping the edited file
    kept = len(git(r.root, "log", "-1", "--format=%P", m).split()) == 2 and (r.root / REL / f"{tid}-x.md").exists()
    said = r.check()
    s("a side branch deletes a frozen tracker while the line edits it, and the merge keeps the edited file: passes, no tracker refused",
      kept and said[0] == 0 and not named(said, IMPORTED), said)
    s("…and --check still names 48 frozen: the deletion the merge did not keep moves nothing back", frozen_said(said).startswith("frozen trackers: 48 —"),
      extra=repr(frozen_said(said)))
    r.switch("side")
    merged(r, "import", then=lambda r: r.write(tid, r.read(tid) + "Merged into the side branch.\n"))
    said = r.check()
    s("the side branch, where it is deleted, then takes the line in a merge that also edits it: passes, no tracker refused",
      said[0] == 0 and not named(said, IMPORTED), said)
    s("…and --check still names 48 frozen: the tracker is Shipped at the merge's second parent, so the merge is no move",
      frozen_said(said).startswith("frozen trackers: 48 —"), extra=repr(frozen_said(said)))
    s.add(add, "after the signed import, a side branch deletes a frozen tracker and the merge keeps the edited file: nothing moves back, so "
               "nothing is refused and --check still names 48; nor when the side branch takes the line in a merge that edits the tracker")


def rows_merge_deletes(area, add):
    r = seeded(area, "import")
    s = Steps()
    tid = IMPORTED[0]
    r.switch("-c", "side")
    (r.root / "src" / "side.py").write_text("side\n", encoding="utf-8")
    r.commit("a side change")
    r.switch("import")
    m = merged(r, "side", then=lambda r: git(r.root, "rm", "-q", f"{REL}/{tid}-x.md"))
    said = r.check()
    s("a merge that deletes a frozen tracker itself: passes, and --check names 47 frozen", said[0] == 0 and not named(said, IMPORTED)
      and frozen_said(said).startswith("frozen trackers: 47 —"), said, repr(frozen_said(said)))
    r.write(tid, imported(tid))
    git(r.root, "add", "-A")
    said = r.check()
    s("the seat adds it back Shipped, staged and not yet committed: refused, it alone, and --check names 47 frozen, since it is not Shipped at HEAD",
      said[0] == fm.EXIT_LINT and refused_for(said, [tid]) and named(said, IMPORTED) == [tid] and frozen_said(said).startswith("frozen trackers: 47 —"),
      said, repr(frozen_said(said)))
    r.commit(f"{tid}: added again")
    said = r.check()
    s("…committed: refused, it alone, and --check names 47 frozen", said[0] == fm.EXIT_LINT and refused_for(said, [tid]) and named(said, IMPORTED) == [tid]
      and frozen_said(said).startswith("frozen trackers: 47 —"), said, repr(frozen_said(said)))
    git(r.root, "reset", "-q", "--hard", m)
    r.switch("-c", "side-2")
    (r.root / "src" / "side.py").write_text("side 2\n", encoding="utf-8")
    r.commit("a second side change")
    r.switch("import")
    merged(r, "side-2", then=lambda r: write(r.root, tid, imported(tid)))
    said = r.check()
    s("…and added back Shipped in the seat's own merge instead: refused, it alone, and --check names 47 frozen",
      said[0] == fm.EXIT_LINT and refused_for(said, [tid]) and named(said, IMPORTED) == [tid] and frozen_said(said).startswith("frozen trackers: 47 —"),
      said, repr(frozen_said(said)))
    s.add(add, "after the signed import, a merge deletes a frozen tracker and the seat adds it back Shipped, in a commit or in a merge of its "
               "own: the rule refuses that move and --check names 47; before the commit, the staged move is refused and --check names 47")


# --- a project below the top of its git repository is judged as the same project at the top; --version and --help run there ---------

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


def at_top(area):
    """The same project at the top of a git repository of its own, with the same tracker committed: its root, which is the top."""
    at = area / "at-top"
    (at / REL).mkdir(parents=True)
    git(at, "init", "-q", "--initial-branch=main")
    (at / "shoalmark.toml").write_text('name = "tool"\n[kinds]\nFM = "Work"\n', encoding="utf-8")
    write(at, "FM-001", text("FM-001"))
    git(at, "add", "-A")
    git(at, "commit", "-q", "-m", "the team's trackers")
    return at


def placed(said, *paths):
    """(exit, stdout, stderr), each path in `paths` — the project root, then the top — written as one placeholder: what a run says, where
    it ran aside."""
    def put(text):
        for path in paths:
            text = text.replace(str(path), "<place>")
        return text
    return said[0], put(said[1]), put(said[2])


def rows_below_top(area, add):
    top, sub = below(area)
    at = at_top(area)
    s = Steps()
    for argv in (("--check",), (), ("--html-only",), ("--next",), ("--check",)):
        here, there = run(sub, *argv, who=SEAT), run(at, *argv, who=SEAT)
        s(f"below the top, {' '.join(argv) or 'the default run'}: judged as at the top, the same exit and the same lines, where each ran aside",
          placed(here, sub, top) == placed(there, at), here, f"at the top: {seen(there)}")
    s("…and the default run wrote below the top the INDEX.md it wrote at the top, byte for byte",
      (sub / REL / "INDEX.md").read_bytes() == (at / REL / "INDEX.md").read_bytes())
    here, there = program(sub, "--check"), program(at, "--check")
    s("below the top, as a program started there: --check says what it says at the top, its frozen line too",
      placed(here, sub, top) == placed(there, at) and frozen_said(here).startswith("frozen trackers: none —"), here, repr(frozen_said(here)))
    said = program(sub, "--version")
    s("below the top, --version runs", said[0] == 0 and said[1].strip() == fm.__version__, said)
    said = program(sub, "--help")
    s("below the top, --help runs", said[0] == 0 and said[1].startswith("usage:"), said)
    said = run(sub, "--version", who=SEAT)
    s("below the top, --version runs with --root naming the project", said[0] == 0 and said[1].strip() == fm.__version__, said)
    s.add(add, "a run from a project below the top of its git repository is judged as the same project at the top is — --check, the default "
               "run, the board's run, --next, and the program started there: the same exit, the same lines and the same INDEX.md; --version and "
               "--help run there")


def rows_act_below_top(area, add):
    top, sub = below(area)
    at = at_top(area)
    s = Steps()
    prefix = sub.relative_to(top).as_posix() + "/"
    for argv in (("--install-hook",), ("--init",)):
        here, there = run(sub, *argv, who=SEAT), run(at, *argv, who=SEAT)
        s(f"below the top, {argv[0]}: does what it does at the top, the same exit and the same lines, where each ran aside",
          placed(here, sub, top) == placed(there, at), here, f"at the top: {seen(there)}")
    hooks = lambda base: sorted(p.name for p in (base / ".git" / "hooks").glob("*") if not p.name.endswith(".sample"))
    s("…and the hooks and their copy of the tool are written in the top's git directory, as at the top",
      hooks(top) == hooks(at) and "pre-commit" in hooks(top) and (top / ".git" / fm.COPY_DIR).is_dir() and (at / ".git" / fm.COPY_DIR).is_dir(),
      extra=f"{hooks(top)} · {hooks(at)}")
    status = lambda base, cut: sorted(l[3:].removeprefix(cut) for l in git(base, "status", "--porcelain", "--untracked-files=all").splitlines() if l.strip())
    s("…and the same files are written in the project, below the top as at the top", status(top, prefix) == status(at, ""),
      extra=f"{status(top, prefix)} · {status(at, '')}")
    s.add(add, "an act run from a project below the top of its git repository — --install-hook, --init — does what it does at the top: the "
               "same exit and lines, the hooks and their copy of the tool in the top's git directory, and the same files in the project")


# --- below the top, the tracker folder at a revision is read whole: the frozen count, an import's rename, and a later rename ------------

def rows_frozen_below_top(area, add):
    r = seeded(area, "import", below=True)
    sha = r.head()
    s = Steps()
    said = r.check()
    s("below the top, the import on its branch passes, no tracker it adds refused", said[0] == 0 and not named(said, IMPORTED), said)
    want = f"frozen trackers: 48 — added already `Shipped` by the import commit {sha[:7]} (Tracker-import: shoalmark/shoalmark {FOREIGN})"
    s("…and --check names 48 frozen, as at the top, and the import commit with its trailer", frozen_said(said).startswith(want), extra=repr(frozen_said(said)))
    r.land("import")
    said = r.check()
    s("landed on main: passes, and still 48 frozen by that commit", said[0] == 0 and frozen_said(said).startswith(want), said, repr(frozen_said(said)))
    s.add(add, "below the top of its git repository, the Owner's signed import adding 48 Shipped trackers: --check counts the 48 it counts at "
               "the top, on the import's branch and landed, and names the import commit with its trailer")


def rows_renamed_by_import_below_top(area, add):
    r = seeded(area, "before", below=True)
    made_import(r, rename=("FM-001",))
    s = Steps()
    said = r.check()
    s("below the top, the tracker the import renames and moves to Shipped is refused by the Shipped rule, it alone",
      said[0] == fm.EXIT_LINT and refused_for(said, ["FM-001"]) and named(said, ["FM-001", *IMPORTED]) == ["FM-001"], said)
    s("…and --check names the 48 it adds as frozen, not the one it renames", frozen_said(said).startswith("frozen trackers: 48 —"), extra=repr(frozen_said(said)))
    s.add(add, "below the top, the Owner's signed import that also renames an open tracker and moves it to Shipped freezes nothing of it: the "
               "rule finds that tracker at the parent by its id and refuses it, and --check counts the 48 the import adds, not that one")


def rows_renamed_later_below_top(area, add):
    r = seeded(area, "import", below=True)
    r.land("import")
    tid = NAMING[0]
    git(r.root, "mv", f"{REL}/{tid}-x.md", f"{REL}/{tid}-renamed.md")
    r.commit(f"{tid}: renamed")
    s = Steps()
    said = r.check()
    s(f"below the top, a seat's commit renames {tid}, frozen and still Shipped, its ship log naming a commit only the code repository holds: "
      "passes, nothing refused", said[0] == 0 and not named(said, IMPORTED), said)
    s("…and --check still names 48 frozen", frozen_said(said).startswith("frozen trackers: 48 —"), extra=repr(frozen_said(said)))
    s.add(add, "below the top, a later commit that renames a Shipped tracker is no move: the rule finds the tracker at the parent by its id, "
               "Shipped, so a seat's rename of a frozen tracker passes, and --check still counts 48")


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


def rows_hooked_merge(area, add):
    s = Steps()
    r = seeded(area, "before")
    install(r)
    r.switch("-c", "filed")
    write(r.root, "FM-160", shipped("FM-160", "Filed."))
    r.commit("FM-160: filed, already Shipped")
    r.switch("main")
    git(r.root, "merge", "-q", "--no-ff", "--no-commit", "filed")
    before = r.head()
    code, printed = hooked(r, SEAT, "the branch filed, merged")
    s("a merge being made, with the hooks on, that brings a seat's commit adding a tracker already Shipped: the commit hook refuses that "
      "tracker, and the merge is not made", code != 0 and r.head() == before
      and any(l.strip().startswith("lint: FM-160: in `") and "which the merge brings" in l and REFUSED in l for l in printed.splitlines()),
      extra=f"exit {code}: {printed[-600:]!r}")
    s("…and the hook leaves nothing to --check: the commit the merge brings is made, so it is judged there", "left to `--check`" not in printed,
      extra=repr(printed[-600:]))
    s.add(add, "a merge being made with the hooks on, bringing a seat's commit that adds a tracker already Shipped: the commit hook judges that "
               "commit, refuses the tracker and leaves nothing to --check, so the merge is not made")


ROWS = (rows_signed_import, rows_modified_by_import, rows_unverified_import, rows_later_move, rows_reopened, rows_renamed_by_import, rows_later_note,
        rows_root_import, rows_owner_unmarked, rows_below_top, rows_act_below_top, rows_frozen_below_top, rows_renamed_by_import_below_top,
        rows_renamed_later_below_top, rows_hooked_import, rows_hooked_merge, rows_side_deletion_kept, rows_merge_deletes)


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
    ("a later move to Shipped not ending the freeze", "frozen_left", "    return set(froze) - moved", "    return set(froze)", (rows_reopened,)),
    ("a tracker reopened in the working state counted frozen", "frozen_line", "for sha, _v, froze in held)) & now", "for sha, _v, froze in held))", (rows_reopened,)),
    ("the count read by path: a tracker the import renames onto Shipped counted frozen", "tracker_imports",
     " and not any(tracker_name(tid, names) for names in there)", "", (rows_renamed_by_import,)),
    ("a later file below the tracker folder read as a frozen tracker's", "frozen_left", " if path.parent.as_posix() == home else None", "", (rows_later_note,)),
    ("the commit hook's deferral applied to a tracker present at a parent", "shipped_moves", "later = added if COMMITTING and not commit else set()",
     "later = set(shipped) if COMMITTING and not commit else set()", (rows_hooked_import,)),
    ("the commit hook's deferral with no line", "shipped_moves", "    if left:\n", "    if False:\n", (rows_hooked_import,)),
    ("the deferral in --check too, not only in the commit hook's run", "shipped_moves", "if COMMITTING and not commit else set()", "if not commit else set()",
     (rows_hooked_import,)),
    ("an import with no parent here freezing what it adds", "import_freezes", "    if not commits_held(bases):\n", "    if False:\n", (rows_root_import,)),
    ("the commit hook's deferral reaching what a merge being made brings", "shipped_moves", "later = added if COMMITTING and not commit else set()",
     "later = added if COMMITTING else set()", (rows_hooked_merge,)),
    ("the freeze held by an Owner whom the configuration does not mark signed", "import_verified",
     'bool(theirs) and theirs[1] == "signed" and verified_as(', "bool(theirs) and verified_as(", (rows_owner_unmarked,)),
    ("the history read as before, by --name-only of each commit, with no merge's own change", "frozen_left", '"log", "-z", "-c", ', '"log", "-z", ',
     (rows_merge_deletes,)),
    ("the Shipped at HEAD test dropped", "frozen_line", "    frozen = {tid for tid, spec in at_head.items() if is_shipped(texts.get(spec))}\n", "",
     (rows_merge_deletes,)),
    ("a move judged against the first parent alone", "frozen_left", "for p in parents)}", "for p in parents[:1])}", (rows_side_deletion_kept,)),
    ("the tracker folder at a revision listed without --full-tree: below the top, only what lies below the working directory's place in it",
     "folder_names", '"--name-only", "--full-tree", ', '"--name-only", ', (rows_frozen_below_top, rows_renamed_by_import_below_top, rows_renamed_later_below_top)),
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
