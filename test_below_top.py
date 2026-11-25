"""A project below the top of its git repository, judged exactly as one at the top: the class test of the reads that name a path at a
revision, the lists of changed paths, the signers file, the records list, and the commits of another project below the root.

Each row builds its history in a scratch repository — a bare `origin` with `main` as its default branch, the Owner's SSH key in the
default branch's signers file — and lays the same project out twice: at the top of its repository, and in `teams/tool/` of a larger
one whose top holds other files. It runs the tool in this process and states each layout's verdict, which must be the same. The
acceptance shapes put an outer project at the top beside a team project in `teams/tool/`, each with its own `shoalmark.toml` and
tracker folder. Each mutant patches one function of the imported module, putting back what the reads did before, and must turn at
least one row red.

Run: `python3 test_below_top.py` — exit 1 on a failure; `--no-mutants` runs the rows alone. test_shoalmark.py runs it as it runs
test_ask_ids.py. No browser and no network: every repository is a scratch one, `origin` a bare one beside it.
"""
import contextlib
import inspect
import io
import json
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
import test_ask_ids as ids  # noqa: E402

git, run, text, ask, record, answered = ids.git, ids.run, ids.text, ids.ask, ids.record, ids.answered
refused, accepted, seen = ids.refused, ids.accepted, ids.seen
OWNER = ids.OWNER
LEAD = ("Lead", "lead@example.invalid")             # the team project's planner seat: ask, close, triage
BUILDER = ("Builder", "builder@example.invalid")    # the team project's builder seat: no right
PROBE = ("probe", "probe@scratch.invalid")          # in no `[seats]` table
COORD = ("Coord", "coord@example.invalid")          # the outer project's planner seat
REL = ids.REL
TODAY, SINCE = ids.TODAY, ids.SINCE
TEAM = "teams/tool"
LAYOUTS = (("at the top", ""), ("below the top", TEAM))


def config(name, kind, seats, top="", tables=""):
    """A `shoalmark.toml`: the Owner signed, one kind, the seats given; `top` holds more top-level lines, `tables` more tables."""
    return (f'name = "{name}"\nowner = "{OWNER[1]} signed"\n{top}[kinds]\n{kind} = "Work"\n[seats]\n'
            + "".join(f'{seat} = "{who[1]}"\n' for seat, who in seats) + tables)


def team_config(top="", tables=""):
    return config("tool", "FM", (("planner", LEAD), ("builder", BUILDER)), top, tables)


def org_config(top=""):
    return config("org", "OR", (("planner", COORD),), top)


class Repo:
    """A scratch clone of a bare `origin` whose `main` is the default branch, holding one project or several: `projects` maps each
    project's folder from the top ("" for the top itself) to its `shoalmark.toml`. `files` are more files of the repository, from the
    top. The clone's identity is the Owner's, with their key; `gpg.ssh.allowedSignersFile` names `signers` — a path from the top, as
    git reads a relative one — and the Owner's key is in it. Everything is committed by the Owner, signed, and pushed."""

    def __init__(self, base, projects, trackers=None, files=None, signers=None):
        self.base, self.top, self.origin = base, base / "wc", base / "origin.git"
        self.projects = dict(projects)
        made = run_area()
        self.keys = made["keys"]
        main = next(iter(self.projects))
        self.signers_rel = signers or self.at(main, REL + "/allowed_signers")
        start = (tuple(self.projects.items()), tuple(sorted((trackers or {}).items())), tuple(sorted((files or {}).items())), self.signers_rel)
        held = made["starts"].get(start)
        if held is not None:                                 # the same start, made before in this run: copied, `origin` named where it now is
            shutil.copytree(held, base, symlinks=True)
            git(self.top, "remote", "set-url", "origin", str(self.origin))
            return
        self.top.mkdir(parents=True)
        for folder, cfg in self.projects.items():
            (self.root(folder)).mkdir(parents=True, exist_ok=True)
            (self.root(folder) / "shoalmark.toml").write_text(cfg, encoding="utf-8")
        for rel, body in (files or {}).items():
            p = self.top / rel
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text(body, encoding="utf-8")
        git(base, "init", "-q", "--bare", "--initial-branch=main", str(self.origin))
        git(self.top, "init", "-q", "--initial-branch=main")
        for k, v in (("user.name", OWNER[0]), ("user.email", OWNER[1]), ("gpg.format", "ssh"), ("user.signingkey", str(self.keys["owner"])),
                     ("gpg.ssh.allowedSignersFile", self.signers_rel), ("commit.gpgsign", "false")):
            git(self.top, "config", k, v)
        git(self.top, "remote", "add", "origin", str(self.origin))
        (self.top / ".gitignore").write_text("".join(f"{self.at(f, REL)}/index.html\n{self.at(f, REL)}/view/\n" for f in self.projects), encoding="utf-8")
        self.signers(f"{OWNER[1]} " + self.keys["owner"].with_suffix(".pub").read_text(encoding="utf-8"))
        for (folder, tid), body in (trackers or {}).items():
            self.write(folder, tid, body)
        self.commit("the start", who=OWNER, sign=True, index=False)
        git(self.top, "push", "-q", "-u", "origin", "main")
        git(self.top, "remote", "set-head", "origin", "main")
        self.written()                                       # INDEX.md as it reads once `origin/main` is there
        if git(self.top, "status", "--porcelain"):
            self.commit("the index, with the default branch known", who=OWNER, sign=True, index=False)
            git(self.top, "push", "-q", "origin", "main")
        keep = made["dir"] / f"start-{len(made['starts'])}"
        shutil.copytree(base, keep, symlinks=True)
        made["starts"][start] = keep

    @staticmethod
    def at(folder, rel):
        """`rel`, written from the project in `folder`, as a path from the top."""
        return f"{folder}/{rel}" if folder else rel

    def root(self, folder):
        return self.top / folder if folder else self.top

    def signers(self, line):
        p = self.top / self.signers_rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(line, encoding="utf-8")

    def written(self, who=OWNER):
        """`--print-written` in every project: each INDEX.md as the tool writes it."""
        for folder in self.projects:
            run(self.root(folder), "--print-written", who=who)

    def path(self, folder, tid):
        return self.root(folder) / REL / f"{tid}-x.md"

    def write(self, folder, tid, body, index=False):
        p = self.path(folder, tid)
        p.parent.mkdir(parents=True, exist_ok=True)
        with open(p, "w", encoding="utf-8", newline="\n") as f:
            f.write(body)
        if index:
            self.written()
        return p

    def read(self, folder, tid):
        return self.path(folder, tid).read_text(encoding="utf-8")

    def put(self, rel, body):
        """A file of the repository, from the top."""
        p = self.top / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(body, encoding="utf-8")
        return p

    def commit(self, message, who=LEAD, sign=False, trailers=(), paths=None, index=True):
        """What is changed staged — every path, or `paths` from the top — and committed by `who`, signed with the Owner's key where `sign`;
        each INDEX.md written first, where `index` and every path is staged: a commit of `paths` alone leaves the tree as it was beside them."""
        if index and not paths:
            self.written(who)
        git(self.top, "add", "-A", *(["--", *paths] if paths else []))
        extra = [x for t in trailers for x in ("-m", t)]
        git(self.top, "commit", "-q", "--allow-empty", "-m", message, *extra, *(["-S"] if sign else []), who=who, sign=self.keys["owner"] if sign else None)
        return git(self.top, "rev-parse", "HEAD").strip()

    def check(self, folder, who=LEAD):
        return run(self.root(folder), "--check", who=who)

    def head(self, ref="HEAD"):
        return git(self.top, "rev-parse", ref).strip()

    def switch(self, *a):
        git(self.top, "switch", "-q", *a)

    def land(self, branch):
        self.switch("main")
        git(self.top, "merge", "-q", "--no-ff", "--no-edit", branch)
        git(self.top, "push", "-q", "origin", "main")
        git(self.top, "fetch", "-q", "origin")

    def configured(self, folder):
        """The module bound to the project in `folder`, for a direct call; `fm.configure(HERE)` after."""
        fm.configure(self.root(folder))
        return fm


_RUN = {}


def run_area():
    """This run's own folder, made once: the Owner's key and another, and each start a `Repo` made, kept to be copied."""
    if not _RUN:
        tmp = tempfile.TemporaryDirectory(prefix="shoalmark-below-top-run-")
        folder = Path(tmp.name).resolve()
        keys = {}
        for name in ("owner", "other"):
            keys[name] = folder / f"key-{name}"
            subprocess.run(["ssh-keygen", "-q", "-t", "ed25519", "-N", "", "-f", str(keys[name]), "-C", name], check=True, capture_output=True)
        _RUN.update(tmp=tmp, dir=folder, keys=keys, starts={})
    return _RUN


def layout(area, name, below, trackers=None, top="", tables="", files=None, signers=None):
    """One project — the team's — at the top (`below` ""), or in `below` of a larger repository whose top holds other files."""
    more = {"README.md": "the larger repository\n", "src/app.py": "print('app')\n"} if below else {}
    return Repo(area / name, {below: team_config(top, tables)}, {(below, tid): body for tid, body in (trackers or {}).items()},
                {**more, **(files or {})}, signers)


def api(name):
    """The module's function `name` — a function the tool under test may not have: a row that needs one it lacks fails, and says so."""
    found = getattr(fm, name, None)
    if found is None:
        raise LookupError(f"the tool has no `{name}`")
    return found


_PICK = {"cases": None, "below": False}     # a mutant's own rows: the cases it names, and where it only reads below the top, that layout alone


def picked(name):
    return _PICK["cases"] is None or name in _PICK["cases"]


def each(area, add, name, label, case, trackers=None, **kw):
    """`case(repo, folder)` → (ok, what it saw), once for each layout — a row each, named for its layout. A step that fails is that row's
    failure, and the other layout still runs."""
    if not picked(name):
        return
    for where, below in LAYOUTS[1:] if _PICK["below"] else LAYOUTS:
        try:
            r = layout(area, f"{name}-{'below' if below else 'top'}", below, trackers, **kw)
            ok, saw = case(r, below)
        except Exception as e:                              # a missing function or a fixture step: this row fails, the next one runs
            ok, saw = False, f"{type(e).__name__}: {str(e)[:300]}"
        finally:
            fm.configure(HERE)
        add(f"{label} · {where}", ok, saw)


# --- the rights rule ------------------------------------------------------------------------------------------------------------------

def closed(t):
    return t.replace("status: In Progress", "status: Closed", 1)


def rows_rights(area, add):
    def stranger_close(r, f):
        r.write(f, "FM-001", closed(r.read(f, "FM-001")))
        r.commit("FM-001: closed", who=PROBE)
        said = r.check(f)
        return refused(said, "FM-001: this change is a `close`", "is not a seat"), seen(said)
    each(area, add, "rights-stranger", "rights · a close by an identity no `[seats]` lists: refused, naming the right", stranger_close,
         {"FM-001": text("FM-001")})

    def builder_close(r, f):
        r.write(f, "FM-001", closed(r.read(f, "FM-001")))
        r.commit("FM-001: closed", who=BUILDER)
        said = r.check(f)
        return refused(said, "this change is a `close`", "is the seat `builder`, which does not hold `close`"), seen(said)
    each(area, add, "rights-builder", "rights · a close by a seat that does not hold `close`: refused", builder_close, {"FM-001": text("FM-001")})

    def lead_triage_close(r, f):
        r.write(f, "FM-001", text("FM-001", f"tier: P2\ntriaged: {TODAY}\n"))
        r.commit("FM-001: triaged")
        triage = r.check(f)
        r.write(f, "FM-001", closed(r.read(f, "FM-001")))
        r.commit("FM-001: closed")
        close = r.check(f)
        return accepted(triage, "this change is a") and accepted(close, "this change is a"), seen(triage) + " · " + seen(close)
    each(area, add, "rights-lead", "rights · the planner seat's triage, then its close: each accepted", lead_triage_close, {"FM-001": text("FM-001")})

    def staged_close(r, f):
        r.write(f, "FM-001", closed(r.read(f, "FM-001")), index=True)
        git(r.top, "add", "-A")
        said = run(r.root(f), "--print-written", who=PROBE)
        return refused(said, "this change is a `close`", "is not a seat"), seen(said)
    each(area, add, "rights-staged", "rights · the commit being made: a close staged by an identity no `[seats]` lists, refused at commit time",
         staged_close, {"FM-001": text("FM-001")})

    def staged_edit(r, f):
        r.write(f, "FM-001", r.read(f, "FM-001").replace("One thing is left.", "One thing is left, and in hand."), index=True)
        git(r.top, "add", "-A")
        said = run(r.root(f), "--print-written", who=BUILDER)
        return accepted(said, "this change is a"), seen(said)
    each(area, add, "rights-staged-edit", "rights · the commit being made: the builder seat, which holds no right, edits a triaged tracker's body and "
         "moves no guarded key — accepted", staged_edit, {"FM-001": text("FM-001", f"tier: P2\ntriaged: {SINCE}\n")})


# --- the Shipped rule ----------------------------------------------------------------------------------------------------------------

def shipped(t, row):
    return t.replace("status: In Progress", "status: Shipped", 1) + f"\n## Ship log\n\n| Date | Event |\n|---|---|\n| {TODAY} | {row} |\n"


def rows_shipped(area, add):
    def no_commit(r, f):
        r.write(f, "FM-001", shipped(r.read(f, "FM-001"), "Shipped. Nothing built."))
        r.commit("FM-001: shipped")
        said = r.check(f)
        return refused(said, "FM-001: moved to `Shipped` with no commit behind it — its ship log names no commit"), seen(said)
    each(area, add, "ship-none", "Shipped · a move to Shipped whose ship log names no commit: refused", no_commit, {"FM-001": text("FM-001")})

    def with_commit(r, f):
        r.put(r.at(f, "src/tool.py"), "print('built')\n")
        built = r.commit("FM-001: built", paths=[r.at(f, "src/tool.py")])
        r.write(f, "FM-001", shipped(r.read(f, "FM-001"), f"Built in {built[:10]}."))
        r.commit("FM-001: shipped")
        said = r.check(f)
        return accepted(said, "with no commit behind it"), seen(said)
    each(area, add, "ship-built", "Shipped · a move to Shipped naming the commit that built it: accepted", with_commit, {"FM-001": text("FM-001")})

    if picked("ship-outside"):
        rows = []
        try:
            r = org(area, "ship-outside")
            r.commit("the import: the tool team's project", who=OWNER, sign=True)

            def moved(folder, tid, sha, who):
                r.write(folder, tid, shipped(r.read(folder, tid), f"Built in {sha[:10]}."))
                r.commit(f"{tid}: shipped", who=who)
                said = r.check(folder, who=who)
                git(r.top, "reset", "-q", "--hard", "HEAD~1")
                return said
            r.put("src/app.py", "print('app, changed')\n")
            outside = r.commit("the outer project's app", who=COORD, paths=["src/app.py"])
            team, outer = moved(TEAM, "FM-002", outside, LEAD), moved("", "OR-001", outside, COORD)
            r.put("src/app.py", "print('app, again')\n")
            r.put(r_at(TEAM, REL + "/evidence/note.md"), "a note\n")
            noted = r.commit("the app, and a note of the team's", who=LEAD, paths=["src/app.py", r_at(TEAM, REL + "/evidence/note.md")])
            team_noted = moved(TEAM, "FM-002", noted, LEAD)
            r.put("src/app.py", "print('app, a third time')\n")
            r.put(r_at(TEAM, "src/tool.py"), "print('tool')\n")
            built = r.commit("the app, and the team's tool", who=LEAD, paths=["src/app.py", r_at(TEAM, "src/tool.py")])
            team_built = moved(TEAM, "FM-002", built, LEAD)
            why = f"`{outside[:10]}` changes nothing outside the records ({TEAM}/{REL}/) under the project root, `{TEAM}/`"
            rows = [("Shipped · below the top: a move naming a commit whose every path lies outside the project root — the outer project's "
                     "`src/app.py` — is refused: it changes nothing outside the records, under the root",
                     refused(team, "FM-002: moved to `Shipped` with no commit behind it — " + why), seen(team)),
                    ("Shipped · below the top: a commit with a path outside the root and, under it, only a record of the team's — refused",
                     refused(team_noted, f"`{noted[:10]}` changes nothing outside the records ("), seen(team_noted)),
                    ("Shipped · below the top: a commit with a path outside the root and a path of the team's product — accepted",
                     accepted(team_built, "with no commit behind it"), seen(team_built)),
                    ("Shipped · at the top: the outer project's move naming the commit that changed its `src/app.py` — accepted, as before",
                     accepted(outer, "with no commit behind it"), seen(outer))]
        except Exception as e:
            rows.append(("Shipped · a commit outside the project root: a fixture step failed", False, f"{type(e).__name__}: {str(e)[:300]}"))
        finally:
            fm.configure(HERE)
        for row in rows:
            add(*row)


# --- `[ratio] records`: written from the project root -------------------------------------------------------------------------------

RATIO = '[ratio]\nrecords = ["docs/", "notes/"]\n'


def rows_records(area, add):
    def records_only(r, f):
        r.put(r.at(f, "notes/plan.md"), "the plan\n")
        noted = r.commit("FM-001: the plan", paths=[r.at(f, "notes/plan.md")])
        r.write(f, "FM-001", shipped(r.read(f, "FM-001"), f"Planned in {noted[:10]}."))
        r.commit("FM-001: shipped")
        said = r.check(f)
        return refused(said, f"`{noted[:10]}` changes nothing outside the records ("), seen(said)
    each(area, add, "records-only", "`[ratio] records` · a move to Shipped naming a commit that changed only `notes/`, a record: refused",
         records_only, {"FM-001": text("FM-001")}, tables=RATIO)

    def product(r, f):
        r.put(r.at(f, "src/tool.py"), "print('built')\n")
        built = r.commit("FM-001: built", paths=[r.at(f, "src/tool.py")])
        r.write(f, "FM-001", shipped(r.read(f, "FM-001"), f"Built in {built[:10]}."))
        r.commit("FM-001: shipped")
        said = r.check(f)
        return accepted(said, "with no commit behind it"), seen(said)
    each(area, add, "records-product", "`[ratio] records` · a move to Shipped naming a commit that changed `src/`, outside the records: accepted",
         product, {"FM-001": text("FM-001")}, tables=RATIO)

    def listed(r, f):
        got = r.configured(f).ship_records()
        want = [r.at(f, "docs/"), r.at(f, "notes/")]
        return got == want, f"ship_records() = {got}, not {want}"
    each(area, add, "records-list", "`[ratio] records` · the prefixes held against `git log`'s paths: each written from the project root, "
         "then named from the top", listed, {"FM-001": text("FM-001")}, tables=RATIO)

    def no_list(r, f):
        (r.root(f) / "shoalmark.toml").write_text(team_config(tables='[ratio]\nrecords = "docs/"\n'), encoding="utf-8")
        r.put(r.at(f, "src/tool.py"), "print('built')\n")
        built = r.commit("FM-001: built", paths=[r.at(f, "src/tool.py")])
        r.write(f, "FM-001", shipped(r.read(f, "FM-001"), f"Built in {built[:10]}."))
        r.commit("FM-001: shipped")
        said = r.check(f)
        return (refused(said, "FM-001: moved to `Shipped`, which needs the records told from the product",
                        "`[ratio] records` is a list of prefixes written from the project root") and "repository-relative" not in said[2]), seen(said)
    each(area, add, "records-no-list", "`[ratio] records` · a value that is no list: the move's refusal says the prefixes are written from the "
         "project root", no_list, {"FM-001": text("FM-001")})

    def from_top(r, f):
        entry = r.at(f, "notes/")
        (r.root(f) / "shoalmark.toml").write_text(team_config(tables=f'[ratio]\nrecords = ["docs/", "{entry}"]\n'), encoding="utf-8")
        r.put(r.at(f, "notes/plan.md"), "the plan\n")
        noted = r.commit("FM-001: the plan", paths=[r.at(f, "notes/plan.md")])
        r.write(f, "FM-001", shipped(r.read(f, "FM-001"), f"Planned in {noted[:10]}."))
        r.commit("FM-001: shipped")
        said = r.check(f)
        if not f:                                       # at the top the entry is the root's own words: read as written
            return refused(said, f"`{noted[:10]}` changes nothing outside the records (docs/, notes/)"), seen(said)
        hook = run(r.root(f), "--print-written", who=LEAD)
        line = f'shoalmark.toml: `[ratio] records` is written from the project root, `{f}/` — "{entry}" starts with the root\'s own folder: write it "notes/"'
        return (said[0] == 1 and said[2].strip() == line and not said[1].strip() and hook[0] == 1 and hook[2].strip() == line,
                f"--check exit {said[0]}: {said[2].strip()[:300]!r} · --print-written exit {hook[0]}: {hook[2].strip()[:300]!r}")
    each(area, add, "records-from-top", "`[ratio] records` · an entry written from the top of the repository: at the top, the root's own words, read "
         "as written; below the top, the run is refused in one line — the records are written from the project root, the entry, and the "
         "entry as it should read", from_top, {"FM-001": text("FM-001")})

    if picked("records-schema"):
        code, out, err = run(HERE, "--schema")
        ratio = [line for line in out.split("\n") if line.startswith(("| `[ratio] records` |", "| `[ratio] exclude` |"))]
        add("`[ratio]` · `--schema`'s two rows say each list's prefixes are written from the project root, and that an entry of `records` "
            "written from the top is refused below it",
            code == 0 and len(ratio) == 2 and all("| a list of prefixes written from the project root; " in line for line in ratio)
            and "repository-relative" not in "".join(ratio) and "an entry that starts with the root's own folder is refused" in ratio[0],
            f"exit {code}: {ratio}")


# --- asks and answers --------------------------------------------------------------------------------------------------------------

def put(r, f, q="Ship it?", aid="FM-001-Q1", who=LEAD):
    """The ask put under `aid` by `who`, committed and pushed to `main`, and a branch `ans` cut from it."""
    r.write(f, "FM-001", text("FM-001", ask(aid=aid, q=q)))
    r.commit(f"FM-001: put as {aid}", who=who)
    git(r.top, "push", "-q", "origin", "main")
    r.switch("-c", "ans")


def rows_asks(area, add):
    def lead_asks(r, f):
        r.write(f, "FM-001", text("FM-001", ask(aid="FM-001-Q1")))
        r.commit("FM-001: put as FM-001-Q1")
        said = r.check(f)
        return accepted(said, "unattributed", "is not a seat"), seen(said)
    each(area, add, "ask-lead", "ask · the planner seat puts an ask under its id: accepted, its `next: owner` line read as the seat's", lead_asks,
         {"FM-001": text("FM-001")})

    def builder_asks(r, f):
        r.write(f, "FM-001", text("FM-001", ask(aid="FM-001-Q1")))
        r.commit("FM-001: put as FM-001-Q1", who=BUILDER)
        said = r.check(f)
        return refused(said, "FM-001", "`builder`"), seen(said)
    each(area, add, "ask-builder", "ask · a seat that does not hold `ask` puts one: refused", builder_asks, {"FM-001": text("FM-001")})

    def owner_answers(r, f):
        put(r, f)
        said_a = run(r.root(f), "--answer", "FM-001-Q1", "accept")
        said = r.check(f)
        signed = git(r.top, "log", "-1", "--format=%G?", "HEAD").strip()
        return said_a[0] == 0 and accepted(said) and signed == "G", f"--answer {seen(said_a)} · %G? {signed} · {seen(said)}"
    each(area, add, "answer-owner", "answer · the Owner's `--answer`, signed with the key the default branch's signers file holds: accepted",
         owner_answers, {"FM-001": text("FM-001")})

    def seat_answers(r, f):
        put(r, f)
        r.write(f, "FM-001", answered(r.read(f, "FM-001"), by=LEAD[0]))
        r.commit("FM-001-Q1: accepted", trailers=("Answers: FM-001-Q1",))
        said = r.check(f)
        return refused(said, "no commit answers FM-001-Q1"), seen(said)
    each(area, add, "answer-seat", "answer · a seat's unsigned answer by its id: refused — no commit answers it", seat_answers, {"FM-001": text("FM-001")})

    def unsigned_owner(r, f):
        put(r, f)
        r.write(f, "FM-001", answered(r.read(f, "FM-001")))
        r.commit("FM-001-Q1: accepted", who=OWNER, trailers=("Answers: FM-001-Q1",))
        said = r.check(f)
        return refused(said, "no commit answers FM-001-Q1"), seen(said)
    each(area, add, "answer-unsigned", "answer · the Owner's identity, unsigned, answering by its id: refused", unsigned_owner, {"FM-001": text("FM-001")})

    def changed_ask(r, f):
        put(r, f)
        r.write(f, "FM-001", answered(r.read(f, "FM-001").replace('ask: "Ship it?"', 'ask: "Ship the other?"')))
        r.commit("FM-001-Q1: accepted", who=OWNER, sign=True, trailers=("Answers: FM-001-Q1",))
        said = r.check(f)
        return refused(said, "FM-001: answers FM-001-Q1 and changes its put ask in the same commit"), seen(said)
    each(area, add, "answer-changes-ask", "answer · the Owner's signed answer whose commit also changes the put ask: refused", changed_ask,
         {"FM-001": text("FM-001")})

    def wrong_trailer(r, f):
        put(r, f)
        r.write(f, "FM-001", answered(r.read(f, "FM-001")))
        r.commit("FM-001-Q1: accepted", who=OWNER, sign=True, trailers=("Answers: FM-001-Q2",))
        said = r.check(f)
        return refused(said, "names `Answers: FM-001-Q2`, and FM-001 does not carry FM-001-Q2 at that commit"), seen(said)
    each(area, add, "answer-trailer", "answer · a commit naming `Answers:` for an id its tracker does not carry at that commit: refused, naming it",
         wrong_trailer, {"FM-001": text("FM-001")})

    def held_trailer(r, f):
        put(r, f)
        said_a = run(r.root(f), "--answer", "FM-001-Q1", "accept")
        said = r.check(f)
        return said_a[0] == 0 and accepted(said, "names `Answers:"), seen(said)
    each(area, add, "answer-trailer-held", "answer · `Answers: FM-001-Q1` on the commit whose tracker carries it: not refused for its trailer",
         held_trailer, {"FM-001": text("FM-001")})


def rows_ids(area, add):
    def renumbered(r, f):
        put(r, f)
        r.write(f, "FM-001", r.read(f, "FM-001").replace("ask-id: FM-001-Q1", "ask-id: FM-001-Q2"))
        r.commit("FM-001: its ask renumbered")
        said = r.check(f)
        return refused(said, "removes FM-001-Q1 with no record under `## Asks`", "--clear-ask FM-001-Q1"), seen(said)
    each(area, add, "id-renumbered", "ask ids · a put ask renumbered with no record of its old number: refused, naming `--clear-ask`", renumbered,
         {"FM-001": text("FM-001")})

    def changed_under_id(r, f):
        put(r, f)
        r.write(f, "FM-001", r.read(f, "FM-001").replace('ask: "Ship it?"', 'ask: "Ship the other?"'))
        r.commit("FM-001: the put ask changed")
        said = r.check(f)
        return refused(said, "changes the put ask under FM-001-Q1", "put the changed ask as FM-001-Q2"), seen(said)
    each(area, add, "id-changed", "ask ids · a put ask changed under its id: refused, naming the next number", changed_under_id,
         {"FM-001": text("FM-001")})

    def low_number(r, f):
        r.write(f, "FM-001", text("FM-001", ask(aid="FM-001-Q2"), asks=record("FM-001-Q1", "Ship it?", "accepted")))
        r.commit("FM-001: put as FM-001-Q2, the record of FM-001-Q3 dropped")
        said = r.check(f)
        return refused(said, "puts FM-001-Q2, and its number is not above every number FM-001 has used — the highest is FM-001-Q3"), seen(said)
    held = record("FM-001-Q1", "Ship it?", "accepted") + "\n" + record("FM-001-Q3", "Ship the next?")
    each(area, add, "id-low", "ask ids · an ask put under a number below one a record held before this commit: refused, naming the highest",
         low_number, {"FM-001": text("FM-001", asks=held)})

    def taken_on_main(r, f):
        git(r.top, "branch", "A")
        git(r.top, "branch", "B")
        for b, q in (("A", "Ship A?"), ("B", "Ship B?")):
            r.switch(b)
            r.write(f, "FM-001", text("FM-001", ask(aid="FM-001-Q1", q=q)))
            r.commit(f"FM-001: put on {b}")
        r.land("A")
        r.switch("B")
        said = r.check(f)
        git(r.top, "push", "-q", "-f", "origin", "B:refs/heads/B")
        git(r.top, "fetch", "-q", "origin")
        m = r.configured(f)
        reading = m.proposed_id_reading(r.head("B"), "refs/remotes/origin/main")
        return (refused(said, "FM-001-Q1 is taken on origin/main", "renumber this branch's ask as FM-001-Q2")
                and reading is not None and reading[0] == "wait: FM-001-Q1 is taken on origin/main — renumber"), f"{seen(said)} · queue: {reading}"
    each(area, add, "id-taken", "ask ids · both branches put FM-001-Q1 and one lands: the other refused by `--check`, and its pull request "
         "waits in the queue's reading", taken_on_main, {"FM-001": text("FM-001")})

    def taken_repaired(r, f):
        git(r.top, "branch", "A")
        git(r.top, "branch", "B")
        for b, q in (("A", "Ship A?"), ("B", "Ship B?")):
            r.switch(b)
            r.write(f, "FM-001", text("FM-001", ask(aid="FM-001-Q1", q=q)))
            r.commit(f"FM-001: put on {b}")
        r.land("A")
        r.switch("B")
        r.write(f, "FM-001", text("FM-001", ask(aid="FM-001-Q2", q="Ship B?")))
        r.commit("FM-001: B's ask renumbered")
        said = r.check(f)
        return accepted(said, "is taken on", "removes FM-001-Q1"), seen(said)
    each(area, add, "id-taken-repair", "ask ids · …and the other branch's ask renumbered FM-001-Q2, its put ask unchanged, with no record of the number "
         "the default branch holds: accepted", taken_repaired, {"FM-001": text("FM-001")})

    def repaired(r, f):
        git(r.top, "branch", "A")
        git(r.top, "branch", "B")
        r.switch("A")
        r.write(f, "FM-001", text("FM-001", ask(aid="FM-001-Q1", q="Ship A?")))
        r.commit("FM-001: put on A")
        r.write(f, "FM-001", text("FM-001", asks=record("FM-001-Q1", "Ship A?")))
        r.commit("FM-001: cleared on A")
        r.land("A")
        r.switch("B")
        r.write(f, "FM-001", text("FM-001", ask(aid="FM-001-Q1", q="Ship B?")))
        r.commit("FM-001: put on B")
        r.land("B")
        r.write(f, "FM-001", text("FM-001", ask(aid="FM-001-Q2", q="Ship B?"), asks=record("FM-001-Q1", "Ship A?")))
        r.commit("FM-001: the open ask renumbered beside the record that holds its number")
        said = r.check(f)
        return accepted(said, "removes FM-001-Q1"), seen(said)
    each(area, add, "id-repair", "ask ids · on the default branch, the open ask renumbered beside the record that holds its old number: "
         "accepted, with no record of its own", repaired, {"FM-001": text("FM-001")})

    def twice_new(r, f):
        both = record("FM-001-Q2", "Ship it?", "accepted") + "\n" + record("FM-001-Q2", "Ship the other?", "accepted", day=TODAY)
        r.switch("-c", "b")
        r.write(f, "FM-001", text("FM-001", asks=both))
        r.commit("two records with one id, on a branch")
        said = r.check(f)
        return refused(said, "two records under `## Asks` carry FM-001-Q2", "FM-001-Q3"), seen(said)
    each(area, add, "id-twice-new", "ask ids · two records with one id, new on a branch: refused", twice_new, {"FM-001": text("FM-001")})

    def twice_landed(r, f):
        said = r.check(f)
        return accepted(said) and "two records under `## Asks` carry FM-001-Q2" in said[2] and "each is kept as signed" in said[2], seen(said)
    both = record("FM-001-Q2", "Ship it?", "accepted") + "\n" + record("FM-001-Q2", "Ship the other?", "accepted", day=TODAY)
    each(area, add, "id-twice-landed", "ask ids · two records with one id that the default branch holds: kept with a note, not refused", twice_landed,
         {"FM-001": text("FM-001", asks=both)})


def rows_lost_answer(area, add):
    def lost(r, f):
        put(r, f)
        run(r.root(f), "--answer", "FM-001-Q1", "accept")
        t = r.read(f, "FM-001")
        r.write(f, "FM-001", "\n".join(l for l in t.split("\n") if not l.startswith(("answer:", "answered:", "answered-by:"))), index=True)
        git(r.top, "add", "-A")
        said = run(r.root(f), "--print-written", who=OWNER)
        return refused(said, "FM-001: the answer is being removed"), seen(said)
    each(area, add, "answer-lost", "answer · the commit being made drops the committed answer and writes it nowhere: refused", lost,
         {"FM-001": text("FM-001")})


# --- INDEX ---------------------------------------------------------------------------------------------------------------------------

def rows_index(area, add):
    def stale(r, f):
        r.write(f, "FM-001", text("FM-001").replace('hook: "h of FM-001"', 'hook: "a new hook"'), index=False)
        git(r.top, "add", "-A")
        git(r.top, "commit", "-q", "-m", "FM-001: the hook, INDEX.md not written", who=LEAD)
        said = r.check(f)
        return said[0] == fm.EXIT_DRIFT and f"{REL}/INDEX.md is STALE" in said[2], seen(said)
    each(area, add, "index-stale", "INDEX · a commit that changes a hook and leaves INDEX.md as it was: refused, naming INDEX.md", stale,
         {"FM-001": text("FM-001")})

    def fresh(r, f):
        r.write(f, "FM-001", text("FM-001").replace('hook: "h of FM-001"', 'hook: "a new hook"'))
        r.commit("FM-001: the hook")
        said = r.check(f)
        index = (r.root(f) / REL / "INDEX.md").read_text(encoding="utf-8")
        return accepted(said, "INDEX.md") and "a new hook" in index, seen(said)
    each(area, add, "index-fresh", "INDEX · the same change with INDEX.md as the tool writes it: accepted", fresh, {"FM-001": text("FM-001")})


# --- the signers file ----------------------------------------------------------------------------------------------------------------

def signers_of(r, f):
    m = r.configured(f)
    m._SIGNERS = None
    return m.trusted_signers()


def rows_signers(area, add):
    def found(r, f):
        s = signers_of(r, f)
        want = r.at(f, REL + "/allowed_signers")
        held = Path(s["file"]).read_text(encoding="utf-8") if s["file"] else ""
        return s["why"] == "" and s["rel"] == want and OWNER[1] in held, f"{s}"
    each(area, add, "signers-found", "signers · a relative `gpg.ssh.allowedSignersFile` read from the top, as git reads it: the default branch's copy "
         "verifies", found, {"FM-001": text("FM-001")})

    def link(r, f):
        real = r.top / r.at(f, REL)
        (r.top / r.at(f, "lnk")).symlink_to(real, target_is_directory=True)
        git(r.top, "config", "gpg.ssh.allowedSignersFile", r.at(f, "lnk/allowed_signers"))
        s = signers_of(r, f)
        return s["file"] is None and f"wc/{r.at(f, 'lnk')}` on the way to it is a symlink in a checkout" in s["why"], f"{s}"
    each(area, add, "signers-link", "signers · the file named through a symlink in the checkout: refused, naming the link", link,
         {"FM-001": text("FM-001")})

    def other(r, f):
        elsewhere = r.base / "other"
        git(r.base, "init", "-q", str(elsewhere))
        (elsewhere / "allowed_signers").write_text(f"{OWNER[1]} key\n", encoding="utf-8")
        git(r.top, "config", "gpg.ssh.allowedSignersFile", "../other/allowed_signers")
        s = signers_of(r, f)
        return s["file"] is None and "inside another checkout" in s["why"], f"{s}"
    each(area, add, "signers-other", "signers · `../other/allowed_signers`, read from the top, inside another clone: refused", other,
         {"FM-001": text("FM-001")})

    def missing(r, f):
        git(r.top, "config", "gpg.ssh.allowedSignersFile", r.at(f, REL + "/nope"))
        s = signers_of(r, f)
        return s["file"] is None and f"`{r.at(f, REL + '/nope')}` is not on origin/main" in s["why"], f"{s}"
    each(area, add, "signers-missing", "signers · a file the default branch does not hold: nothing verifies, and it is named from the top", missing,
         {"FM-001": text("FM-001")})

    def no_trunk(r, f):
        git(r.top, "remote", "remove", "origin")
        s = signers_of(r, f)
        want = (r.top / r.at(f, REL + "/allowed_signers")).resolve()
        return s["why"] == "" and s["file"] is not None and Path(s["file"]).resolve() == want, f"{s}"
    each(area, add, "signers-no-trunk", "signers · no default branch to read: the clone's own file, found where git finds it, verifies", no_trunk,
         {"FM-001": text("FM-001")})


# --- the reads beside the rules: the queue, the tree, a partial clone -------------------------------------------------------------

def rows_reads(area, add):
    def addendum(r, f):
        m = r.configured(f)
        is_addendum = m.review_addendum()
        inside = [r.at(f, REL + "/sessions.md"), r.at(f, REL + "/evidence/reviews/x.md")]
        own = r.at(f, REL + "/evidence/b/review-1.md")
        outside = [r.at(f, "src/tool.py")] + ([REL + "/sessions.md"] if f else ["elsewhere/" + REL + "/sessions.md"])
        ok = all(is_addendum(x, False) for x in inside) and is_addendum(own, True) and not is_addendum(own, False) \
            and not any(is_addendum(x, True) for x in outside)
        return ok, f"inside {[is_addendum(x, False) for x in inside]} own {is_addendum(own, True)} outside {[is_addendum(x, True) for x in outside]}"
    each(area, add, "queue-addendum", "queue · a review addendum's paths, as `git log` names them from the top: the registry, the review folder "
         "and the verdict's own file, and nothing beside the project", addendum, {"FM-001": text("FM-001")})

    def owner_pr(r, f):
        r.switch("-c", "answers")
        run(r.root(f), "--answer", "FM-001-Q1", "accept")
        git(r.top, "push", "-q", "origin", "answers")
        git(r.top, "fetch", "-q", "origin")
        m = r.configured(f)
        reading = m.owner_reading(r.head("answers"), "refs/remotes/origin/main", [r.head("answers")])
        return reading == ("merge", "merge: yours — signed", ""), f"owner_reading = {reading}"
    each(area, add, "queue-owner", "queue · the Owner's own pull request of answers, its tracker paths read from the top: read as the Owner's answers",
         owner_pr, {"FM-001": text("FM-001", ask(aid="FM-001-Q1"))})

    def tree(r, f):
        r.write(f, "FM-001", closed(r.read(f, "FM-001")), index=False)
        git(r.top, "add", "--", r.at(f, REL + "/FM-001-x.md"))
        r.write(f, "FM-001", r.read(f, "FM-001") + "\nOne more line.\n", index=False)
        m = r.configured(f)
        got = m.tree_changes()
        return got == 1, f"tree_changes() = {got}"
    each(area, add, "tree-staged", "the working tree · a tracker staged, then changed again, and nothing else: one path changed, counted once",
         tree, {"FM-001": text("FM-001")})

    def unread(r, f):
        m = r.configured(f)
        saved = m.unread_here
        m.unread_here = lambda: True                        # as a partial clone would say: the clone may lack an object it names
        try:
            have = REL + "/FM-001-x.md"
            got = m.specs_unread([f"HEAD:./{have}", "HEAD:./missing.md"])
        finally:
            m.unread_here = saved
        return got == [f"HEAD:./{have}"], f"specs_unread = {got}"
    each(area, add, "partial-unread", "a partial clone · a spec written from the project root that the tree holds is named unread; one it does not "
         "hold is not", unread, {"FM-001": text("FM-001")})

    def prefix(r, f):
        m = r.configured(f)
        got = (api("root_prefix")(), Path(api("git_top")()).resolve())
        want = (f + "/" if f else "", r.top.resolve())
        return got == want, f"root_prefix, git_top = {got}, not {want}"
    each(area, add, "root-prefix", "the root's folder below the top, and the top: as git names them", prefix, {"FM-001": text("FM-001")})


# --- the acceptance shapes: an outer project at the top, a team project in teams/tool/ --------------------------------------------

def org(area, name, top_team="", top_org=""):
    """The outer project at the top, its planner the coordinator, and the team project in `teams/tool/`, its own planner the lead: the
    team's trackers added by the Owner's signed import. The signers file is the outer project's, which git reads from the top."""
    r = Repo(area / name, {"": org_config(top_org)}, {("", "OR-001"): text("OR-001")}, {"src/app.py": "print('app')\n"})
    r.projects[TEAM] = team_config(top_team)
    r.root(TEAM).mkdir(parents=True)
    (r.root(TEAM) / "shoalmark.toml").write_text(r.projects[TEAM], encoding="utf-8")
    with open(r.top / ".gitignore", "a", encoding="utf-8") as g:
        g.write(f"{TEAM}/{REL}/index.html\n{TEAM}/{REL}/view/\n")
    r.write(TEAM, "FM-001", text("FM-001"))
    r.write(TEAM, "FM-002", text("FM-002"))
    return r


def rows_acceptance(area, add):
    r = org(area, "accept-import")
    r.commit("the import: the tool team's project", who=OWNER, sign=True)
    said = r.check("")
    add("acceptance 1 · the outer project's own check names no change for the import of the team's project", accepted(said, "this change is a"),
        seen(said))
    r.write(TEAM, "FM-002", shipped(r.read(TEAM, "FM-002"), "Built in 0123456789ab, in the code repository."))
    r.commit("FM-002: shipped, its commit in the code repository", who=LEAD)
    said = r.check(TEAM)
    add("acceptance 2 · the shape of check 2: a move to Shipped in the team project naming a commit this repository lacks is judged as at the "
        "top — refused, not in the history", refused(said, "FM-002: moved to `Shipped` with no commit behind it — `0123456789ab` is not in the history"),
        seen(said))
    git(r.top, "reset", "-q", "--hard", "HEAD~1")

    r.write(TEAM, "FM-001", r.read(TEAM, "FM-001").replace("status: In Progress", "status: Shipped", 1))
    r.commit("accept: a non-seat closes FM-001", who=PROBE)
    said = r.check(TEAM)
    add("acceptance 3 · the control: an identity the team's `[seats]` does not list sets FM-001 Shipped — the team project's check names "
        "\"this change is a `close`\"", refused(said, "this change is a `close`", "is not a seat"), seen(said))
    git(r.top, "reset", "-q", "--hard", "HEAD~1")

    r.write(TEAM, "FM-001", text("FM-001", f"tier: P2\ntriaged: {TODAY}\n"))
    r.commit("FM-001: triaged", who=LEAD)
    r.write(TEAM, "FM-001", closed(r.read(TEAM, "FM-001")))
    r.commit("FM-001: closed", who=LEAD)
    team, outer = r.check(TEAM), r.check("", who=COORD)
    add("acceptance O1 · the team lead's triage and close: the team project's check exits 0, and the outer project's on the same commits",
        accepted(team) and accepted(outer), seen(team) + " · " + seen(outer))

    r = org(area, "accept-answer")
    r.commit("the import: the tool team's project", who=OWNER, sign=True)
    git(r.top, "push", "-q", "origin", "main")
    r.write(TEAM, "FM-002", text("FM-002", ask(aid="FM-002-Q1")))
    r.commit("FM-002: put as FM-002-Q1", who=LEAD)
    git(r.top, "push", "-q", "origin", "main")
    r.switch("-c", "ans")
    said_a = run(r.root(TEAM), "--answer", "FM-002-Q1", "accept")
    team, outer = r.check(TEAM), r.check("", who=COORD)
    fm.configure(r.root(TEAM))
    try:
        t = next(t for t in fm.load_trackers() if t["id"] == "FM-002")
        head, why = fm.answer_commit(t)
    finally:
        fm.configure(HERE)
    add("acceptance O2 · the Owner's `--answer` in the team project, with a scratch key enrolled as the Owner's: the answer's commit is found, "
        "signed, and `--check` accepts it in both projects", said_a[0] == 0 and bool(head) and not why and accepted(team) and accepted(outer),
        f"--answer {seen(said_a)} · answer_commit {head[:10] if head else None} {why!r} · {seen(team)} · {seen(outer)}")
    board = run(r.root(TEAM), "--html-only")
    page = r.root(TEAM) / REL / "index.html"
    html = page.read_text(encoding="utf-8") if page.is_file() else ""
    at = html.find(",PROOF=")
    proof = json.JSONDecoder().raw_decode(html, at + len(",PROOF="))[0] if at >= 0 else None
    fm.configure(r.root(TEAM))
    try:
        t = next(t for t in fm.load_trackers() if t["id"] == "FM-002")
        line = fm.signed_line(r.path(TEAM, "FM-002"), t)
    finally:
        fm.configure(HERE)
    add("acceptance O2 · …and the Board built for the team project proves answers by signature, and the answer's record names its commit, "
        "signed `G`", board[0] == 0 and bool(proof) and proof.get("state") == "signed" and line == f"**signed** — {r.head()[:7]} · G\n",
        f"board {seen(board)} · proof {proof and proof.get('state')} · {line!r}")


# --- the commits of another project below the root ----------------------------------------------------------------------------------

GATED = "judged_before_build = true\n"


def gated(area, name, outer="", before=False, trailers=(), team_signers=False):
    """The acceptance shape with the build gate on in both projects — the outer project at the top, or itself in `outer` below it — the
    team's FM-001 triaged and In Progress, and a branch `work` cut from `main`. With `before`, the import is the branch's second commit:
    its first, a seat's, builds in the team's folder while no commit holds that folder's `shoalmark.toml`. With `team_signers`, the
    import also brings the team's own signers file, holding the Owner's key, and git's configuration names that file: both projects
    read it as their signers file."""
    if outer:
        r = Repo(area / name, {outer: org_config(GATED)}, {(outer, "OR-001"): text("OR-001", f"tier: P2\ntriaged: {TODAY}\n")},
                 {"README.md": "the larger repository\n", r_at(outer, "src/app.py"): "print('app')\n"})
    else:
        r = Repo(area / name, {"": org_config(GATED)}, {("", "OR-001"): text("OR-001", f"tier: P2\ntriaged: {TODAY}\n")}, {"src/app.py": "print('app')\n"})
    team = r_at(outer, TEAM)
    if before:
        r.switch("-c", "work")
        r.put(r_at(team, "src/tool.py"), "print('team, before its project')\n")
        r.commit("build in the folder, before its project", paths=[r_at(team, "src/tool.py")])
    r.projects[team] = team_config(GATED)
    r.root(team).mkdir(parents=True, exist_ok=True)
    (r.root(team) / "shoalmark.toml").write_text(r.projects[team], encoding="utf-8")
    with open(r.top / ".gitignore", "a", encoding="utf-8") as g:
        g.write(f"{team}/{REL}/index.html\n{team}/{REL}/view/\n")
    r.write(team, "FM-001", text("FM-001", f"tier: P2\ntriaged: {TODAY}\n"))
    if team_signers:
        r.put(r_at(team, REL + "/allowed_signers"), (r.top / r.signers_rel).read_text(encoding="utf-8"))
        r.signers_rel = r_at(team, REL + "/allowed_signers")
    r.commit("the import: the tool team's project", who=OWNER, sign=True, trailers=trailers)
    if team_signers:
        git(r.top, "config", "gpg.ssh.allowedSignersFile", r.signers_rel)
    if not before:
        git(r.top, "push", "-q", "origin", "main")
        r.switch("-c", "work")
    return r, outer, team


def r_at(folder, rel):
    return Repo.at(folder, rel)


def other_layouts():
    return (("the outer project at the top", ""), ("the outer project itself below the top", "org"))


GATE = "names no tracker"          # the build gate's refusal of a build commit that names none
SIGNERS = "changes the signers file"   # the guard's words for a commit that changes the signers file


def a_key_for_the_lead(r, team):
    """A line added to the team's signers file, which git's configuration names: a change the guard of both projects watches."""
    p = r.top / r_at(team, REL + "/allowed_signers")
    p.write_text(p.read_text(encoding="utf-8") + f"# {LEAD[1]}'s key is to come\n", encoding="utf-8")
    return r_at(team, REL + "/allowed_signers")


def rows_other_project(area, add):
    def one(name, label, build):
        """One case: `build()` → [(label, ok, saw)]; a step that fails is its row's failure, and the next case runs."""
        if not picked(name):
            return
        try:
            rows = build()
        except Exception as e:
            rows = [(label, False, f"{type(e).__name__}: {str(e)[:300]}")]
        finally:
            fm.configure(HERE)
        for row in rows:
            add(*row)

    for where, outer_at in other_layouts():
        tag = "below" if outer_at else "top"

        def skip():
            r, outer, team = gated(area, f"skip-{tag}", outer_at)
            r.put(r_at(team, "src/tool.py"), "print('team')\n")
            r.commit("build the team's tool", paths=[r_at(team, "src/tool.py")])
            o, t = r.check(outer, who=COORD), r.check(team)
            return [(f"another project · {where}: a build commit whose every path lies in the team project — the outer check skips it", accepted(o), seen(o)),
                    (f"another project · {where}: …and the team project's own check judges it, as a build commit naming no tracker", refused(t, GATE), seen(t))]
        one("skip", f"another project · {where}: a build commit whose every path lies in the team project", skip)

        def both():
            r, outer, team = gated(area, f"both-{tag}", outer_at)
            r.put(r_at(team, "src/tool.py"), "print('team')\n")
            r.put(r_at(outer, "src/app.py"), "print('app, changed')\n")
            r.commit("build both", paths=[r_at(team, "src/tool.py"), r_at(outer, "src/app.py")])
            o = r.check(outer, who=COORD)
            return [(f"another project · {where}: a build commit with paths in both projects — the outer check judges it as before", refused(o, GATE), seen(o))]
        one("both", f"another project · {where}: a build commit with paths in both projects", both)

        def plain():
            r, outer, team = gated(area, f"plain-{tag}", outer_at)
            r.put(r_at(outer, "vendor/lib/x.py"), "print('lib')\n")
            r.commit("vendor a library", paths=[r_at(outer, "vendor/lib/x.py")])
            o = r.check(outer, who=COORD)
            return [(f"another project · {where}: a build commit wholly in a folder with no `shoalmark.toml` — judged by the outer check", refused(o, GATE), seen(o))]
        one("plain", f"another project · {where}: a build commit wholly in a folder with no `shoalmark.toml`", plain)

        def staged():
            r, outer, team = gated(area, f"staged-{tag}", outer_at)
            r.put(r_at(team, "src/tool.py"), "print('team')\n")
            git(r.top, "add", "--", r_at(team, "src/tool.py"))
            msg = r.base / "msg"
            msg.write_text("build the team's tool\n", encoding="utf-8")
            o, t = run(r.root(outer), "--commit-msg", str(msg), who=COORD), run(r.root(team), "--commit-msg", str(msg), who=LEAD)
            return [(f"another project · {where}: the commit being made, every path in the team project, whose `shoalmark.toml` the index holds — the "
                     f"outer commit-msg check skips it, the team's judges it", o[0] == 0 and refused(t, GATE), seen(o) + " · " + seen(t))]
        one("staged", f"another project · {where}: the commit being made, every path in the team project", staged)

        def guard():
            r, outer, team = gated(area, f"guard-{tag}", outer_at, team_signers=True)
            r.commit("a key for the lead", paths=[a_key_for_the_lead(r, team)])
            o, t = r.check(outer, who=COORD), r.check(team)
            return [(f"another project · {where}: a seat's change to the signers file git names, the file in the team project — the outer check's guard "
                     f"skips it, the team's refuses it", accepted(o, SIGNERS) and refused(t, SIGNERS), seen(o) + " · " + seen(t))]
        one("guard", f"another project · {where}: a seat's change to the signers file git names, in the team project", guard)

        def guard_both():
            r, outer, team = gated(area, f"guard-both-{tag}", outer_at, team_signers=True)
            r.put(r_at(outer, "src/app.py"), "print('app, changed')\n")
            r.commit("a key for the lead, and the app", paths=[a_key_for_the_lead(r, team), r_at(outer, "src/app.py")])
            o = r.check(outer, who=COORD)
            return [(f"another project · {where}: a seat's change to that signers file with a path of the outer project's too — the outer check's guard "
                     f"refuses it, as before", refused(o, SIGNERS), seen(o))]
        one("guard-both", f"another project · {where}: a seat's change to that signers file with a path of the outer project's too", guard_both)

        def guard_staged():
            r, outer, team = gated(area, f"guard-staged-{tag}", outer_at, team_signers=True)
            git(r.top, "add", "--", a_key_for_the_lead(r, team))
            msg = r.base / "msg"
            msg.write_text("a key for the lead\n", encoding="utf-8")
            o, t = run(r.root(outer), "--commit-msg", str(msg), who=LEAD), run(r.root(team), "--commit-msg", str(msg), who=LEAD)
            return [(f"another project · {where}: the commit being made changes only that signers file, in the team project — the outer commit-msg "
                     f"check's guard skips it, the team's refuses it", o[0] == 0 and refused(t, SIGNERS), seen(o) + " · " + seen(t))]
        one("guard-staged", f"another project · {where}: the commit being made changes only that signers file", guard_staged)

    def before():
        r, outer, team = gated(area, "before-toml", before=True)
        o = r.check(outer, who=COORD)
        return [("another project · a commit in a folder whose `shoalmark.toml` that commit's tree does not hold, though the working tree does — "
                 "judged by the outer check", refused(o, GATE), seen(o))]
    one("before-toml", "another project · a commit in a folder before its `shoalmark.toml` was committed", before)

    def session():
        r, outer, team = gated(area, "session", trailers=("Session: aaaaaaaa",))
        r.put(r_at(team, "src/tool.py"), "print('team')\n")
        r.commit("build the team's tool", who=COORD, paths=[r_at(team, "src/tool.py")])
        o, t = r.check(outer, who=COORD), r.check(team)
        return [("another project · a commit by the outer project's seat with no `Session:` trailer, where the history carries them, every path in the "
                 "team project: the outer check skips it, the team's judges it", accepted(o, "Session") and refused(t, GATE), seen(o) + " · " + seen(t))]
    one("session", "another project · a seat's commit with no `Session:` trailer, every path in the team project", session)

    def r14():
        r, outer, team = gated(area, "r14")
        r.put(r_at(team, "src/tool.py"), "print('team')\n")
        r.write(team, "FM-001", r.read(team, "FM-001").replace("One thing is left.", "One thing is left, built."))
        r.commit("FM-001: built, unsigned, by the Owner's identity", who=OWNER)
        o, t = r.check(outer, who=COORD), r.check(team)
        return [("another project · an unsigned commit by the Owner's identity, wholly in the team project: the outer check skips it, the team's "
                 "refuses it", accepted(o, "Owner commit") and refused(t, "Owner commit"), seen(o) + " · " + seen(t))]
    one("r14", "another project · an unsigned commit by the Owner's identity, wholly in the team project", r14)

    def r14_both():
        r, outer, team = gated(area, "r14-both")
        r.put(r_at(team, "src/tool.py"), "print('team')\n")
        r.write("", "OR-001", r.read("", "OR-001").replace("One thing is left.", "One thing is left, too."))
        r.commit("OR-001: both projects, unsigned, by the Owner's identity", who=OWNER)
        o = r.check(outer, who=COORD)
        return [("another project · an unsigned commit by the Owner's identity with paths in both projects: the outer check refuses it, as before",
                 refused(o, "Owner commit"), seen(o))]
    one("r14-both", "another project · an unsigned commit by the Owner's identity with paths in both projects", r14_both)


ROWS = (rows_rights, rows_shipped, rows_records, rows_asks, rows_ids, rows_lost_answer, rows_index, rows_signers, rows_reads, rows_acceptance,
        rows_other_project)


# --- mutants: each read put back as it read before -----------------------------------------------------------------------------------

DOT = ":./{"
ALL = None          # every occurrence, at least one: only where the function had no `./` read before
BELOW = True        # the old path form reads the same at the top: its rows run below the top alone
# (label, function, [(old, new, count)], row groups, the cases it runs — None for all —, below the top alone)
MUTANTS = (
    ("the walk's id rules read each tracker from the top", "id_walk_problems",
     [('f"{rev}:./{rel}"', 'f"{rev}:{rel}"', 1), ('f"{result}:./{rel}"', 'f"{result}:{rel}"', 1), ('f"{base}:./{rel}"', 'f"{base}:{rel}"', 1),
      ('f"{b}:./{rel}"', 'f"{b}:{rel}"', 2)], (rows_ids,), {"id-changed", "id-renumbered"}, BELOW),
    ("the walk's id rules read each result from the top", "id_walk_problems", [('blobs.get(f"{result}:./{rel}")', 'blobs.get(f"{result}:{rel}")', 1)],
     (rows_ids,), {"id-changed", "id-renumbered"}, BELOW),
    ("the walk's id rules read each parent from the top", "id_walk_problems", [('blobs.get(f"{base}:./{rel}")', 'blobs.get(f"{base}:{rel}")', 1)],
     (rows_ids,), {"id-changed"}, BELOW),
    ("the walk's renumbering reads its parents from the top", "id_walk_problems",
     [('renumber_repairs(t, rel, [blobs.get(f"{b}:./{rel}")', 'renumber_repairs(t, rel, [blobs.get(f"{b}:{rel}")', 1)], (rows_ids,), {"id-taken-repair"}, BELOW),
    ("the walk's numbers used read its parents from the top", "id_walk_problems",
     [('[(b, blobs.get(f"{b}:./{rel}") or "")', '[(b, blobs.get(f"{b}:{rel}") or "")', 1)], (rows_ids,), {"id-low"}, BELOW),
    ("a renumbering's repair reads the default branch from the top", "renumber_repairs", [(DOT, ":{", ALL)], (rows_ids,), {"id-taken-repair"}, BELOW),
    ("the answer's change rule reads each tracker from the top", "answer_change_problems",
     [('f"{rev}:./{rel}"', 'f"{rev}:{rel}"', 1), ('f"{result}:./{rel}"', 'f"{result}:{rel}"', 1), ('f"{b}:./{rel}"', 'f"{b}:{rel}"', 1)],
     (rows_asks,), {"answer-changes-ask"}, BELOW),
    ("an answer's trailer read from the top", "answer_change_problems", [('f"{c}:./{by_id', 'f"{c}:{by_id', 2)], (rows_asks,), {"answer-trailer-held"}, BELOW),
    ("an id taken on the default branch read from the top", "proposed_id_problems", [(DOT, ":{", ALL)], (rows_ids,), {"id-taken"}, BELOW),
    ("the queue's reading of proposed ids from the top", "proposed_id_reading", [(DOT, ":{", ALL)], (rows_ids,), {"id-taken"}, BELOW),
    ("the queue's reading of proposed ids lists its paths from the top", "proposed_id_reading",
     [('"--no-renames", "--relative", mb', '"--no-renames", mb', 1)], (rows_ids,), {"id-taken"}, BELOW),
    ("an answer's commit read from the top", "answer_commits", [(DOT, ":{", ALL)], (rows_asks,), {"answer-owner"}, BELOW),
    ("the rights read each tracker from the top", "rights_problems", [('f"{rev}:./{rel}"', 'f"{rev}:{rel}"', 2)], (rows_rights,), {"rights-stranger"}, BELOW),
    ("the rights' lookups read from the top", "rights_problems", [('show = lambda rev, rel: blobs.get(f"{rev}:./{rel}")', 'show = lambda rev, rel: blobs.get(f"{rev}:{rel}")', 1)],
     (rows_rights,), {"rights-stranger"}, BELOW),
    ("a line's author read at each tip from the top", "line_author", [('f"{rev}:./{rel}"', 'f"{rev}:{rel}"', 1)], (rows_asks,), {"ask-lead"}, BELOW),
    ("two records with one id read from the top", "duplicate_record_problems", [(DOT, ":{", ALL)], (rows_ids,), {"id-twice-landed"}, BELOW),
    ("a lost answer read from the top", "record_problems", [(DOT, ":{", ALL)], (rows_lost_answer,), {"answer-lost"}, BELOW),
    ("the gate's committed answer read from the top", "lint", [("HEAD:./{(TRACKER_DIR", "HEAD:{(TRACKER_DIR", 2)], (rows_asks,), {"answer-seat", "answer-unsigned"}, BELOW),
    ("a partial clone's specs listed as written", "specs_unread", [('full = {p: root_prefix() + p[2:] if p.startswith("./") else p for p in paths}',
                                                                   "full = {p: p for p in paths}", 1)], (rows_reads,), {"partial-unread"}, BELOW),
    ("a review addendum's paths from the project root", "review_addendum", [("rel = root_prefix() + TRACKER_DIR", "rel = TRACKER_DIR", 1)], (rows_reads,),
     {"queue-addendum"}, BELOW),
    ("the Owner's pull request's paths from the project root", "owner_reading", [("rel = root_prefix() + TRACKER_DIR", "rel = TRACKER_DIR", 1)], (rows_reads,),
     {"queue-owner"}, BELOW),
    ("the index's paths taken as the tree's", "tree_changes", [('held = {p[len(prefix):] for p in staged.stdout.split("\\0") if p and p.startswith(prefix)}',
                                                               'held = {p for p in staged.stdout.split("\\0") if p}', 1)], (rows_reads,), {"tree-staged"}, BELOW),
    ("the signers resolved from the project root", "trusted_signers", [("else git_top() / conf", "else ROOT / conf", 1)], (rows_signers,),
     {"signers-found", "signers-link", "signers-other", "signers-missing", "signers-no-trunk"}, BELOW),
    ("this working tree named by the project root", "worktree_tops", [("tops = {os.path.realpath(git_top())}", "tops = {os.path.realpath(ROOT)}", 1)],
     (rows_signers,), {"signers-found", "signers-missing"}, BELOW),
    ("`[ratio] records` read from the top", "ship_records", [("return [prefix + p for p in records]",
                                                            "return records if isinstance(section, dict) else [prefix + p for p in records]", 1)],
     (rows_records,), {"records-only", "records-list"}, BELOW),
    ("the commit behind a move counted by its paths outside the project root", "git_ship_verdicts",
     [("any(f.startswith(prefix) and ratio_class(", "any(ratio_class(", 1)], (rows_shipped,), {"ship-outside"}, False),
    ("`[ratio]`'s refusal says repository-relative prefixes", "ratio_paths",
     [("is a list of prefixes written from the project root", "is a list of repository-relative prefixes", 1)], (rows_records,), {"records-no-list"}, False),
    ("`--schema`'s `[ratio]` rows say repository-relative prefixes", "CONFIG_KEYS",
     [("a list of prefixes written from the project root;", "a list of repository-relative prefixes;", 2)], (rows_records,), {"records-schema"}, False),
    ("a records entry written from the top read as written, below the top", "records_from_top", [("if entry.startswith(prefix):", "if False:", 1)],
     (rows_records,), {"records-from-top"}, BELOW),
    ("a records entry refused at the top too, where the root's folder is empty", "records_from_top",
     [("if not prefix or not isinstance(records, list)", "if not isinstance(records, list)", 1)], (rows_records,), {"records-from-top", "records-only"}, False),
    ("another project's skip taken where only some paths lie in it", "other_project_changes", [("if rels and all(", "if rels and any(", 1)],
     (rows_other_project,), {"both"}, False),
    ("another project's skip taken for a folder with no `shoalmark.toml`", "other_project_changes",
     [("if f.parts and os.path.lexists(ROOT / f / CONFIG_NAME)]", "if f.parts]", 1), ("held.get(spec(rev, home)) is not None", "True", 1)],
     (rows_other_project,), {"plain"}, False),
    ("another project's skip taken by the working tree alone", "other_project_changes", [("held.get(spec(rev, home)) is not None", "True", 1)],
     (rows_other_project,), {"before-toml"}, False),
    ("another project's `shoalmark.toml` read from the top", "other_project_changes",
     [('f"{rev}:./{home}/{CONFIG_NAME}"', 'f"{rev}:{home}/{CONFIG_NAME}"', 1)], (rows_other_project,), {"skip", "staged"}, False),
    ("another project's commits judged by the rights, the sessions and the Shipped rule", "changes_under_review",
     [("[c for n, c in enumerate(changes) if n not in theirs]", "changes", 1)], (rows_other_project,), {"session"}, False),
    ("another project's commits judged by the build gate", "judge_commits", [("if n in theirs or (", "if (", 1)], (rows_other_project,), {"skip", "staged"}, False),
    ("another project's Owner commits judged by the Owner's signature rule", "owner_signature_problems", [("if c not in theirs]", "]", 1)], (rows_other_project,), {"r14"}, False),
    ("another project's commits judged by the guard", "guard_walk", [("[row for n, row in enumerate(rows) if n not in theirs]", "rows", 1)],
     (rows_other_project,), {"guard"}, False),
    ("another project's paths in the guard's walk taken as written from the top", "guard_walk",
     [("[f[len(prefix):] for f in paths[row[0]] if f.startswith(prefix)]", "paths[row[0]]", 1)], (rows_other_project,), {"guard"}, False),
    ("another project's commit being made judged by the commit-time guard", "triage_pending", [("if what and other_project_changes(", "if False and other_project_changes(", 1)],
     (rows_other_project,), {"guard-staged"}, False),
)


@contextlib.contextmanager
def mutated(name, pairs):
    """`fm.<name>` replaced by a patched copy of its own source, compiled in the module's namespace — and put back after. A table of the
    module's (a dict of tuples of words) is patched in its words instead, value by value."""
    real = getattr(fm, name)
    if isinstance(real, dict):
        table = dict(real)
        for old, new, count in pairs:
            found = sum(w.count(old) for v in table.values() for w in v)
            if (found < 1) if count is None else (found != count):
                raise AssertionError(f"{name}: {old[:60]!r} is in its words {found} times, not {count or 'one or more'}")
            table = {k: tuple(w.replace(old, new) for w in v) for k, v in table.items()}
        setattr(fm, name, table)
        try:
            yield
        finally:
            setattr(fm, name, real)
        return
    src = textwrap.dedent(inspect.getsource(real))
    for old, new, count in pairs:
        if (src.count(old) < 1) if count is None else (src.count(old) != count):
            raise AssertionError(f"{name}: {old[:60]!r} is in its source {src.count(old)} times, not {count or 'one or more'}")
        src = src.replace(old, new)
    exec(compile(src, fm.__file__, "exec"), fm.__dict__)
    try:
        yield
    finally:
        setattr(fm, name, real)


def run_mutants(*, results=None, only=None):
    """Each mutant, as (label, whether it turned a row red, what it saw): its rows run under it, and at least one must fail."""
    results = [] if results is None else results
    for label, name, pairs, rows, cases, below in MUTANTS:
        if only and not any(o in label for o in only):
            continue
        reds, broke = [], ""
        _PICK.update(cases=cases, below=below)
        try:
            with mutated(name, pairs), tempfile.TemporaryDirectory(prefix="shoalmark-below-top-m-") as tmp:
                area = Path(tmp).resolve()
                for n, rows_ in enumerate(rows):
                    rows_(area / f"m{n}", lambda l, ok, saw="": reds.append(l) if not ok else None)
        except AssertionError as e:
            broke = str(e)
        except (Exception, SystemExit) as e:                          # a mutant that crashes a row, or refuses the run itself, turned it red
            reds.append(f"a row crashed: {type(e).__name__}: {str(e)[:120]}")
        finally:
            _PICK.update(cases=None, below=False)
            fm.configure(HERE)
        results.append((f"mutant · {label}: at least one row turns red", bool(reds) and not broke,
                        broke or ("no row turned red" if not reds else "")))
    return results


def run_checks(*, results=None, mutants=True, only=None):
    """Every row, then every mutant, as (label, ok, what it saw)."""
    results = [] if results is None else results
    add = lambda label, ok, saw="": results.append((label, bool(ok), "" if ok else saw))
    with tempfile.TemporaryDirectory(prefix="shoalmark-below-top-") as tmp:
        area = Path(tmp).resolve()
        for n, rows in enumerate(ROWS):
            if only and rows.__name__ not in only:
                continue
            try:
                rows(area / f"r{n}", add)
            except Exception as e:
                add(f"{rows.__name__}: a fixture step failed — {type(e).__name__}: {str(e)[:300]}", False, getattr(e, "stderr", "") or "")
            finally:
                fm.configure(HERE)
    if mutants:
        run_mutants(results=results)
    return results


if __name__ == "__main__":
    chosen = [a for a in sys.argv[1:] if a.startswith("rows_")]
    failed = 0
    for label, ok, detail in run_checks(mutants="--no-mutants" not in sys.argv and not chosen, only=chosen or None):
        print(("  ok    " if ok else "  FAIL  ") + label + ("" if ok else f"\n        {detail}" if detail else ""))
        failed += not ok
    print(f"FAILED: {failed}" if failed else "all green")
    sys.exit(1 if failed else 0)
