"""A project below the top of its git repository, judged exactly as one at the top: the class test of the reads that name a path at a
revision, the lists of changed paths, the signers file, the records list, and the commits of another project below the root.

Each row builds its history in a scratch repository — a bare `origin` with `main` as its default branch, the Owner's SSH key in the
default branch's signers file — and lays the same project out twice: at the top of its repository, and in `teams/tool/` of a larger
one whose top holds other files. It runs the tool in this process and states each layout's verdict, which must be the same. The
acceptance shapes put an outer project at the top beside a team project in `teams/tool/`, each with its own `shoalmark.toml` and
tracker folder; in that layout, with the hooks installed once, the commit that creates a project below the top is the project's
around it, which judges it. In that layout, with the tool kept in the top's `tools/`, a run from the team project, a run with `--root` and the
hooks' run write one INDEX.md, the tool named by its path from the project's root. Each mutant patches one function of the imported module,
putting back what the reads did before — or, for the hooks and for the tool a row keeps in its repository, of the file they run in a process of
their own — and must turn at least one row red.

Run: `python3 test_below_top.py` — exit 1 on a failure; `--no-mutants` runs the rows alone. test_shoalmark.py runs it as it runs
test_ask_ids.py. No browser and no network: every repository is a scratch one, `origin` a bare one beside it.
"""
import contextlib
import hashlib
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


def layout(area, name, below, trackers=None, top="", tables="", files=None, signers=None, signers_in=None):
    """One project — the team's — at the top (`below` ""), or in `below` of a larger repository whose top holds other files. `signers_in` names
    the signers file from the project root, `signers` from the top."""
    more = {"README.md": "the larger repository\n", "src/app.py": "print('app')\n"} if below else {}
    return Repo(area / name, {below: team_config(top, tables)}, {(below, tid): body for tid, body in (trackers or {}).items()},
                {**more, **(files or {})}, Repo.at(below, signers_in) if signers_in else signers)


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
        named = Path("wc", r.at(f, "lnk"))                                  # the link as the platform writes a path, as the tool names it
        return s["file"] is None and f"{named}` on the way to it is a symlink in a checkout" in s["why"], f"{s}"
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
            return [(f"another project · {where}: the commit being made, every path in the team project, whose `shoalmark.toml` HEAD holds — the "
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
        return [("another project · a commit in a folder whose `shoalmark.toml` that commit's parent does not hold, though the working tree does — "
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

    def nested():
        rows, control = [], None
        for what, marker in NESTS:
            r = Repo(area / f"nest-{marker}", {"": org_config(GATED)}, {("", "OR-001"): text("OR-001", f"tier: P2\ntriaged: {TODAY}\n")},
                     {"src/app.py": "print('app')\n"})
            r.switch("-c", "work")
            folder = nest(r, marker)
            if marker:
                r.commit("OR-001: a folder of its own", who=COORD, index=False)         # under the outer project's judged tracker
            r.put(f"{folder}/app.py", "print('changed under no tracker')\n")
            r.commit("change the app", who=COORD, index=False, paths=[f"{folder}/app.py"])
            o = r.check("", who=COORD)
            if not marker:
                control = o
                continue
            rows.append((f"another project · the outer project's `{folder}/` holding {what}, committed under its tracker: a build commit there naming "
                         "no tracker is judged by the outer check, and refused, as the same commit in a folder with no `shoalmark.toml` is",
                         refused(o, GATE) and refused(control, GATE), seen(o) + " · the control: " + seen(control)))
        return rows
    one("nested", "another project · a folder that is no project", nested)

    def moved_in():
        r, outer, team = gated(area, "moved-in")
        (r.root(team) / "src").mkdir(parents=True, exist_ok=True)
        git(r.top, "mv", "src/app.py", r_at(team, "src/app.py"))
        r.commit("FM-001: the app moves into the team's project", index=False)
        o = r.check(outer, who=COORD)
        return [("another project · a commit that moves a file of the outer project into the team project, naming the team's tracker alone: the "
                 "outer check judges it by the path it leaves, and its build gate refuses it", refused(o, GATE), seen(o))]
    one("moved-in", "another project · a file moved from the outer project into the team project", moved_in)

    def moved_out():
        r, outer, team = gated(area, "moved-out")
        r.put(r_at(team, "src/moved.py"), "print('the team file')\n")
        r.commit("FM-001: the team's file", paths=[r_at(team, "src/moved.py")])
        git(r.top, "mv", r_at(team, "src/moved.py"), "src/moved.py")
        r.commit("OR-001: the team's file moves to the app", who=COORD, index=False)
        t = r.check(team)
        return [("another project · a commit that moves a file of the team project into the outer project, naming the outer project's tracker "
                 "alone: the team's check judges it by the path it leaves, and its build gate refuses it", refused(t, GATE), seen(t))]
    one("moved-out", "another project · a file moved from the team project into the outer project", moved_out)

    def moved_session(below_head):
        def build():
            r, outer, team = gated(area, f"moved-session{'-below' if below_head else ''}", trailers=("Session: aaaaaaaa",))
            (r.root(team) / "src").mkdir(parents=True, exist_ok=True)
            git(r.top, "mv", "src/app.py", r_at(team, "src/app.py"))
            r.commit("FM-001: the app moves into the team's project", who=COORD, index=False)
            if below_head:
                r.put("src/other.py", "print('another file')\n")
                r.commit("OR-001: another file", who=COORD, index=False, trailers=("Session: bbbbbbbb",), paths=["src/other.py"])
            o = r.check(outer, who=COORD)
            return [(f"another project · a commit by the outer project's seat with no `Session:` trailer, where the history carries them, that moves a "
                     f"file of the outer project into the team project{', with a later commit on top of it' if below_head else ''}: the outer check's "
                     "session rule judges it by the path it leaves, and refuses it", refused(o, "Session"), seen(o))]
        return build
    one("moved-session", "another project · a seat's move into the team project with no `Session:` trailer", moved_session(False))
    one("moved-session-below", "another project · a seat's move into the team project with no `Session:` trailer, below HEAD", moved_session(True))

    for where, outer_at in other_layouts():
        def moved_staged():
            r, outer, team = gated(area, f"moved-session-staged-{'below' if outer_at else 'top'}", outer_at, trailers=("Session: aaaaaaaa",))
            (r.root(team) / "src").mkdir(parents=True, exist_ok=True)
            git(r.top, "mv", r_at(outer, "src/app.py"), r_at(team, "src/app.py"))
            o = r.check(outer, who=COORD)
            return [(f"another project · {where}: the outer project's seat, its session not set, moves a file of the outer project into the team "
                     "project, staged and not committed, where the history carries `Session:` trailers: the outer check reads the working tree's "
                     "edits by the path the move leaves, and its session rule refuses them", refused(o, "carries no Session: trailer"), seen(o))]
        one("moved-session-staged", f"another project · {where}: a seat's move into the team project, staged and not committed", moved_staged)


NESTS = (("no `shoalmark.toml`", ""), ("a one-line `shoalmark.toml`", "file"), ("a folder named `shoalmark.toml`", "dir"),
         ("a dangling symlink named `shoalmark.toml`", "link"), ("a configuration the tool refuses, beside its tracker folder", "refused"),
         ("this repository's own `examples/de/shoalmark.toml`, a configuration with no tracker folder", "sample"))      # the first: the control
REFUSED = f'name = "mine"\nowner = "{COORD[1]}"\n[kinds]\nMY = "Work"\n[seats]\nplanner = "{COORD[1]}"\n'     # the Owner's identity is a seat's too


def nest(r, marker):
    """The outer project's folder that `marker` makes look like a project — `src/`, or `examples/de/` for this repository's sample — written,
    not committed: the folder, from the top."""
    folder = "examples/de" if marker == "sample" else "src"
    r.put(f"{folder}/app.py", "print('app')\n")
    if marker == "file":
        r.put(f"{folder}/shoalmark.toml", 'name = "mine"\n')
    elif marker == "dir":
        r.put(f"{folder}/shoalmark.toml/keep", "x\n")
    elif marker == "link":
        os.symlink("nowhere/at/all", r.top / folder / "shoalmark.toml")
    elif marker == "refused":
        r.put(f"{folder}/shoalmark.toml", REFUSED)
        r.put(f"{folder}/{REL}/MY-001-x.md", text("MY-001"))
    elif marker == "sample":
        r.put(f"{folder}/shoalmark.toml", (HERE / "examples/de/shoalmark.toml").read_text(encoding="utf-8"))
    return folder


# --- the hooks: one install per clone, the gate once for each project a staged path falls in ---------------------------------------

NO_TEAM, NO_OUTER = "no FM-N in its subject", "no OR-N in its subject"      # each project's build gate, by the kind it names
_COPY = {"source": None}           # a mutant of the hooks' copy: the tool's text with its pairs replaced, written over each copy a row installs


def install_once(r, outer):
    """`--install-hook`, once for the clone, run in the outer project — the copy it writes replaced by the mutant's text where one is set."""
    said = run(r.root(outer), "--install-hook", who=OWNER)
    if _COPY["source"] is not None:
        common = git(r.top, "rev-parse", "--git-common-dir").strip()
        (r.top / common / fm.COPY_DIR / "shoalmark.py").write_text(_COPY["source"], encoding="utf-8")
    return said


def hooked(r, message, who=LEAD, sign=False, trailers=(), shell=None):
    """`git commit` of what is staged, through the hooks the clone has installed, as `who` — signed with the Owner's key where `sign`, each of
    `trailers` a paragraph after the subject — in `shell`, the environment it runs in, else `ids.ENV`, whose `SHOALMARK_CMD` names the tool's
    command: (exit, what git and the hooks printed)."""
    env = dict(ids.ENV if shell is None else shell, GIT_AUTHOR_NAME=who[0], GIT_AUTHOR_EMAIL=who[1], GIT_COMMITTER_NAME=who[0], GIT_COMMITTER_EMAIL=who[1])
    extra = [x for t in trailers for x in ("-m", t)] + (["-S"] if sign else [])
    done = subprocess.run(["git", "-C", str(r.top), "-c", "commit.gpgsign=false", "commit", "-q", "-m", message, *extra], capture_output=True, text=True,
                          encoding="utf-8", errors="replace", env=env)
    return done.returncode, done.stdout + done.stderr


def rows_hooks(area, add):
    for where, outer_at in other_layouts():
        name = f"hooks-{'below' if outer_at else 'top'}"
        if not picked(name):
            continue
        rows = []
        try:
            r, outer, team = gated(area, name, outer_at)
            installed = install_once(r, outer)
            if installed[0] != 0:
                raise AssertionError(f"--install-hook: {seen(installed)}")
            cases = (("the team project only", [r_at(team, "src/tool.py")], {team: NO_TEAM}),
                     ("the outer project only", [r_at(outer, "src/app.py")], {outer: NO_OUTER}),
                     ("both projects", [r_at(team, "src/tool.py"), r_at(outer, "src/app.py")], {team: NO_TEAM, outer: NO_OUTER}))
            for what, paths, refusals in cases:
                for path in paths:
                    r.put(path, f"print('built in {what}')\n")
                git(r.top, "add", "--", *paths)
                code, said = hooked(r, f"build in {what}")
                git(r.top, "commit", "-q", "-m", f"build in {what}")                  # the same commit, made with the hooks off
                checks = {folder: r.check(folder, who=LEAD if folder == team else COORD) for folder in (team, outer)}
                git(r.top, "reset", "-q", "--hard", "HEAD~1")
                spared = {folder: words for folder, words in ((team, NO_TEAM), (outer, NO_OUTER)) if folder not in refusals}
                rules = " and ".join("the team's rule" if folder == team else "the outer project's" for folder in refusals)
                rows.append((f"hooks · {where}, installed once: a build commit staged in {what}, its subject naming no tracker, is refused in the "
                             f"hook by {rules} and no other, as each project's own --check judges it",
                             code != 0 and all(words in said for words in refusals.values()) and not any(words in said for words in spared.values())
                             and all(refused(checks[folder], words) for folder, words in refusals.items())
                             and not any(words in checks[folder][2] for folder, words in spared.items()),
                             f"hook exit {code}: {said.strip()[-500:]!r} · " + " · ".join(seen(c) for c in checks.values())))
            for path in (r_at(team, "src/tool.py"), r_at(outer, "src/app.py")):
                r.put(path, "print('built under its tracker')\n")
            git(r.top, "add", "-A")
            code, said = hooked(r, "FM-001, OR-001: build both, each under its judged tracker")
            rows.append((f"hooks · {where}, installed once: a build commit in both projects whose subject names each one's judged tracker passes "
                         "the hooks", code == 0, f"hook exit {code}: {said.strip()[-500:]!r}"))
            tracker = r.path(team, "FM-001")
            tracker.write_text(tracker.read_text(encoding="utf-8").replace('hook: "h of FM-001"', 'hook: "h of FM-001, reworded"'), encoding="utf-8")
            git(r.top, "add", "--", tracker.relative_to(r.top).as_posix())
            code, said = hooked(r, "FM-001: its hook, reworded")
            held, index = git(r.top, "show", "--name-only", "--format=", "HEAD").split(), r_at(team, REL + "/INDEX.md")
            rows.append((f"hooks · {where}, installed once: a tracker of the team's staged — the hook writes the team's INDEX.md and stages it, named "
                         "from the top, in the same commit", code == 0 and index in held and not git(r.top, "status", "--porcelain", "--", index).strip(),
                         f"hook exit {code}: {said.strip()[-300:]!r} · the commit holds {held}"))
        except Exception as e:
            rows.append((f"hooks · {where}: a fixture step failed", False, f"{type(e).__name__}: {str(e)[:300]}"))
        finally:
            fm.configure(HERE)
        for row in rows:
            add(*row)

    if picked("hooks-moved"):
        try:
            r, outer, team = gated(area, "hooks-moved", "")
            installed = install_once(r, outer)
            if installed[0] != 0:
                raise AssertionError(f"--install-hook: {seen(installed)}")
            (r.root(team) / "src").mkdir(parents=True, exist_ok=True)
            git(r.top, "mv", "src/app.py", r_at(team, "src/app.py"))
            code, said = hooked(r, "FM-001: the app moves into the team's project")
            ok, saw = code != 0 and NO_OUTER in said and NO_TEAM not in said, f"hook exit {code}: {said.strip()[-400:]!r}"
        except Exception as e:
            ok, saw = False, f"{type(e).__name__}: {str(e)[:300]}"
        finally:
            fm.configure(HERE)
        add("hooks · a commit being made that moves a file of the outer project into the team project, naming the team's tracker alone: the outer "
            "project's commit-msg check judges it by the path it leaves, and refuses it", ok, saw)

    for where, outer_at in other_layouts():             # the same move made inside a merge, by the outer project's seat with no session set
        if not picked("hooks-merge-moved"):
            continue
        try:
            r, outer, team = gated(area, f"hooks-merge-moved-{'below' if outer_at else 'top'}", outer_at, trailers=("Session: aaaaaaaa",))
            installed = install_once(r, outer)
            if installed[0] != 0:
                raise AssertionError(f"--install-hook: {seen(installed)}")
            r.switch("-c", "side")
            r.put(r_at(outer, "src/side.py"), "print('side')\n")
            r.commit("OR-001: a side file", who=COORD, trailers=("Session: bbbbbbbb",), paths=[r_at(outer, "src/side.py")])
            r.switch("work")
            git(r.top, "merge", "-q", "--no-ff", "--no-commit", "side")
            (r.root(team) / "src").mkdir(parents=True, exist_ok=True)
            git(r.top, "mv", r_at(outer, "src/app.py"), r_at(team, "src/app.py"))
            code, said = hooked(r, "FM-001: the app moves into the team's project, in the merge of side", who=COORD)
            made = len(git(r.top, "rev-list", "--parents", "-n", "1", "HEAD").split()) > 2
            ok, saw = code != 0 and "carries no Session: trailer" in said and not made, f"hook exit {code}, merge made: {made}: {said.strip()[-400:]!r}"
        except Exception as e:
            ok, saw = False, f"{type(e).__name__}: {str(e)[:300]}"
        finally:
            fm.configure(HERE)
        add(f"hooks · {where}: a merge being made by the outer project's seat, its session not set, where the history carries `Session:` trailers, "
            "that moves a file of the outer project into the team project: the session rule reads the merge's own change against each merge head "
            "by the path the move leaves, and the hooks refuse it", ok, saw)

    if picked("hooks-nested"):
        rows, control = [], None
        for what, marker in NESTS:
            try:
                r = org_hooked(area, f"hooks-nest-{marker or 'none'}")
                folder = nest(r, marker)
                git(r.top, "add", "-A")
                made = hooked(r, "OR-001: a folder of its own", who=COORD) if marker else (0, "")
                r.put(f"{folder}/app.py", "print('changed under no tracker')\n")
                git(r.top, "add", "--", f"{folder}/app.py")
                code, said = hooked(r, "change the app", who=COORD)
                if not marker:
                    control = (code, said)
                    continue
                rows.append((f"hooks · the outer project's `{folder}/` holding {what}, committed under its tracker: a build commit there naming no "
                             "tracker is judged by the outer project in the hooks, and refused, as the same commit in a folder with no `shoalmark.toml` is",
                             made[0] == 0 and code != 0 and NO_OUTER in said and control[0] != 0 and NO_OUTER in control[1],
                             f"the folder's commit: exit {made[0]} · the build: exit {code}: {said.strip()[-300:]!r} · the control: exit {control[0]}"))
            except Exception as e:
                rows.append((f"hooks · {what}: a fixture step failed", False, f"{type(e).__name__}: {str(e)[:300]}"))
            finally:
                fm.configure(HERE)
        for row in rows:
            add(*row)

    if picked("copy-tool"):                             # the copy judges each project with the repository's own tool, found once, from the top
        saved, got, want = fm._COPY_RECORD, None, None
        try:
            r = layout(area, "copy-tool", TEAM, {"FM-001": text("FM-001")})
            fm._COPY_RECORD, want = {"tool": "tools/shoalmark"}, r.top / "tools/shoalmark"
            got = r.configured(TEAM).tree_tool_dir()
        except Exception as e:
            got = f"{type(e).__name__}: {str(e)[:300]}"
        finally:
            fm._COPY_RECORD = saved
            fm.configure(HERE)
        add("hooks · the copy, judging the project below the top, finds the repository's own tool where its COPY says, from the top of the working "
            "tree — the folder it finds for every project", want is not None and got == want, f"tree_tool_dir() = {got}, not {want}")

    def first_refusal(r, outer, team):
        paths = [r_at(team, "src/tool.py"), r_at(outer, "src/app.py")]
        for path in paths:
            r.put(path, "print('built')\n")
        git(r.top, "add", "--", *paths)
        code, said = hooked(r, "FM-001: build both, naming the team's tracker only")
        return code != 0 and NO_OUTER in said and NO_TEAM not in said, f"hook exit {code}: {said.strip()[-400:]!r}"

    def refused_config(r, outer, team):
        cfg = r.root(team) / "shoalmark.toml"
        cfg.write_text(cfg.read_text(encoding="utf-8") + '[repositories]\ntool = ""\n', encoding="utf-8")
        git(r.top, "add", "--", r_at(team, "shoalmark.toml"))
        code, said = hooked(r, "FM-001: name the tool's repository")
        return code != 0 and "[repositories]" in said, f"hook exit {code}: {said.strip()[-400:]!r}"

    def moved_out(r, outer, team):
        src, dst = r_at(team, "src/moved.py"), r_at(outer, "src/moved.py")
        r.put(src, "print('the team file')\n")
        git(r.top, "add", "--", src)
        git(r.top, "commit", "-q", "-m", "FM-001: the team's file")                # the hooks off
        git(r.top, "mv", src, dst)
        code, said = hooked(r, "OR-001: the team's file moves to the app")
        return code != 0 and NO_TEAM in said and NO_OUTER not in said, f"hook exit {code}: {said.strip()[-400:]!r}"

    def config_out(r, outer, team):
        git(r.top, "rm", "-q", "--", r_at(team, "shoalmark.toml"))
        code, said = hooked(r, "take the team's configuration out, naming no tracker")
        theirs = [one for one in said.splitlines() if NO_OUTER in one]
        return (code != 0 and bool(theirs) and not any(one.startswith(f"{team}: ") for one in said.splitlines())
                and all(one.startswith(f"{outer}: ") if outer else not one.startswith(f"{team}") for one in theirs)), f"hook exit {code}: {said.strip()[-400:]!r}"

    for where, outer_at in other_layouts():             # four rules of the hooks, each in a clone of its own
        for name, label, build in (
                ("hooks-first", "a build commit staged in both projects whose subject names the team's judged tracker alone: the outer project "
                 "refuses it, the team passes it, and the commit is refused — the first refusal gives the exit", first_refusal),
                ("hooks-config", "a staged change that makes the team's configuration one the tool refuses refuses the commit, with its line",
                 refused_config),
                ("hooks-moved-out", "a file moved out of the team's project into the outer one, the subject naming the outer project's judged "
                 "tracker alone: the team judges the path it loses, and the commit is refused by the team's rule", moved_out),
                ("hooks-config-out", "a commit that takes the team's `shoalmark.toml` out, naming no tracker: the team, whose working tree no "
                 "longer holds it, is no project of that commit, and the outer project refuses it — no line is the team's", config_out)):
            if not picked(name):
                continue
            try:
                r, outer, team = gated(area, f"{name}-{'below' if outer_at else 'top'}", outer_at)
                installed = install_once(r, outer)
                if installed[0] != 0:
                    raise AssertionError(f"--install-hook: {seen(installed)}")
                ok, saw = build(r, outer, team)
            except Exception as e:
                ok, saw = False, f"{type(e).__name__}: {str(e)[:300]}"
            finally:
                fm.configure(HERE)
            add(f"hooks · {where}: {label}", ok, saw)

    if picked("each-alone"):
        try:
            r = layout(area, "each-alone", "", {"FM-001": text("FM-001")})
            got = [run(r.root(""), *argv, who=LEAD) for argv in (("--each-project", "--print-written", "--check"), ("--each-project", "--check"))]
            ok, saw = (all(g[0] == 2 and "--each-project goes with one of" in g[2] for g in got),
                       " · ".join(f"exit {g[0]}: {g[2].strip()[:160]!r}" for g in got))
        except Exception as e:
            ok, saw = False, f"{type(e).__name__}: {str(e)[:300]}"
        finally:
            fm.configure(HERE)
        add("hooks · `--each-project` with a flag besides the hooks' line, or with no hook line, is refused in one line, exit 2", ok, saw)

    if picked("drift-once"):
        try:
            r = org_tools(area, "drift-once", {"": org_config(), TEAM: team_config()}, {("", "OR-001"): text("OR-001"), (TEAM, "FM-001"): text("FM-001")})
            tool = r.top / TOOL_AT / "shoalmark.py"
            tool.write_text(tool.read_text(encoding="utf-8") + "# the repository's tool, edited\n", encoding="utf-8")
            line, counts = "the repository's tool differs from it", []
            for n, paths in enumerate(([r_at(TEAM, "src/tool.py")], [r_at(TEAM, "src/tool2.py"), "src/app2.py"])):
                for path in paths:
                    r.put(path, "print('built')\n")
                git(r.top, "add", "--", *paths)
                code, said = hooked(r, f"FM-001, OR-001: build, step {n}")
                counts.append((code, said.count(line), said))
            ok = counts[0][1] >= 1 and counts[0][1] == counts[1][1]
            saw = (f"one project: exit {counts[0][0]}, said {counts[0][1]} times · two projects: exit {counts[1][0]}, said {counts[1][1]} times · "
                   f"{counts[1][2].strip()[-300:]!r}")
        except Exception as e:
            ok, saw = False, f"{type(e).__name__}: {str(e)[:300]}"
        finally:
            fm.configure(HERE)
        add("hooks · the drift line, where the repository's tool differs from the copy, is said once in each hook's run, however many projects "
            "the commit stages", ok, saw)

    for where, outer_at in other_layouts():             # what a project below the top says in the hooks starts with its folder from the top
        name = f"hooks-named-{'below' if outer_at else 'top'}"
        if not picked("hooks-named"):
            continue
        try:
            r, outer, team = gated(area, name, outer_at)
            installed = install_once(r, outer)
            if installed[0] != 0:
                raise AssertionError(f"--install-hook: {seen(installed)}")
            r.put(r_at(team, "src/tool.py"), "print('built in the team project')\n")
            git(r.top, "add", "--", r_at(team, "src/tool.py"))
            alone = hooked(r, "build in the team project, naming no tracker")
            r.put(r_at(outer, "src/app.py"), "print('built in the outer project')\n")
            git(r.top, "add", "--", r_at(outer, "src/app.py"))
            both = hooked(r, "build in both projects, naming no tracker")
            git(r.top, "reset", "-q", "--hard", "HEAD")
            cfg = r.root(team) / "shoalmark.toml"
            cfg.write_text(cfg.read_text(encoding="utf-8") + '[repositories]\ntool = ""\n', encoding="utf-8")
            git(r.top, "add", "--", r_at(team, "shoalmark.toml"))
            refused_cfg = hooked(r, "FM-001: name the tool's repository")
            lines = lambda said, words: [one for one in said.splitlines() if words in one]
            mine = lambda one, folder: one.startswith(f"{folder}: ") if folder else not one.startswith(f"{team}:") and one.lstrip().startswith("refused")
            own = lambda said: [one for one in said.splitlines() if one.strip() and not one.startswith("the hooks' COPY record is incomplete")]
            ok = (alone[0] != 0 and lines(alone[1], NO_TEAM) and all(one.startswith(f"{team}: ") for one in own(alone[1]))
                  and both[0] != 0 and lines(both[1], NO_TEAM) and lines(both[1], NO_OUTER)
                  and all(mine(one, team) for one in lines(both[1], NO_TEAM)) and all(mine(one, outer) for one in lines(both[1], NO_OUTER))
                  and refused_cfg[0] != 0 and lines(refused_cfg[1], "[repositories]")
                  and all(one.startswith(f"{team}: shoalmark.toml: ") for one in lines(refused_cfg[1], "[repositories]")))
            saw = (f"the team alone: exit {alone[0]} {alone[1].strip()[-300:]!r} · both: exit {both[0]} {both[1].strip()[-500:]!r} · "
                   f"the team's refused configuration: exit {refused_cfg[0]} {refused_cfg[1].strip()[-300:]!r}")
        except Exception as e:
            ok, saw = False, f"{type(e).__name__}: {str(e)[:300]}"
        finally:
            fm.configure(HERE)
        add(f"hooks · {where}: each line a project below the top says starts with its folder from the top — the team's build refused alone, "
            "then beside the outer project's, whose lines name its own folder, or none at the top, and the team's configuration refused", ok, saw)


# --- a new project: the project around it judges the commit that creates it ----------------------------------------------------------

RUST, SIDE = "teams/rust", "teams/side"
IMPORTS = ("Tracker-import: shoalmark/tool 0123456789abcdef0123456789abcdef01234567", "Tracker-import: shoalmark/rust 89abcdef0123456789abcdef0123456789abcdef")


def org_hooked(area, name):
    """Org's layout before its imports: the outer project at the top with its own tracker folder and the build gate on, OR-001 triaged and
    In Progress, the hooks installed once from it, and a branch `import` cut from `main`."""
    r = Repo(area / name, {"": org_config(GATED)}, {("", "OR-001"): text("OR-001", f"tier: P2\ntriaged: {TODAY}\n")}, {"src/app.py": "print('app')\n"})
    installed = install_once(r, "")
    if installed[0] != 0:
        raise AssertionError(f"--install-hook: {seen(installed)}")
    r.switch("-c", "import")
    return r


def laid(r, folder, cfg, tids, signers=True):
    """A project written into `folder` as an import brings it, every path inside that folder — its `shoalmark.toml`, its trackers, In
    Progress and none `Shipped`, where `signers` a signers file in its tracker folder holding the Owner's key, its board's files ignored,
    and its INDEX.md as the tool writes it — and staged. Its staged paths, from the top."""
    r.projects[folder] = cfg
    r.put(r_at(folder, "shoalmark.toml"), cfg)
    r.put(r_at(folder, ".gitignore"), f"{REL}/index.html\n{REL}/view/\n")
    for tid in tids:
        r.write(folder, tid, text(tid))
    if signers:
        r.put(r_at(folder, REL + "/allowed_signers"), (r.top / r.signers_rel).read_text(encoding="utf-8"))
    run(r.root(folder), "--print-written", who=OWNER)
    git(r.top, "add", "-A")
    return git(r.top, "diff", "--cached", "--name-only").split()


@contextlib.contextmanager
def as_run(who=COORD):
    """The environment `run` gives the tool, for a call of its functions in this process."""
    saved = {k: os.environ.pop(k) for k in [k for k in os.environ if k.startswith("GIT_")]}
    os.environ.update(GIT_AUTHOR_NAME=who[0], GIT_AUTHOR_EMAIL=who[1], GIT_COMMITTER_NAME=who[0], GIT_COMMITTER_EMAIL=who[1],
                      GIT_CONFIG_GLOBAL=os.devnull, GIT_CONFIG_NOSYSTEM="1", GIT_TERMINAL_PROMPT="0")
    try:
        yield
    finally:
        for k in [k for k in os.environ if k.startswith("GIT_")]:
            del os.environ[k]
        os.environ.update(saved)


def judged(root, commits):
    """Whether the check of the project at `root` holds each of `commits` among the changes it judges, none skipped as another project's;
    and the first ten characters of each it holds."""
    with as_run():
        fm.configure(root)
        try:
            held = {c[4] for c in fm.changes_under_review()}
        finally:
            fm.configure(HERE)
    return all(c in held for c in commits), sorted(c[:10] for c in held if c)


def top_created(area, name):
    """A repository whose `main` holds no project, a README and the app, and a branch `start`: its first commit, the Owner's, signed, creates
    the project at the top — its `shoalmark.toml` with the build gate on, its tracker folder with OR-001, and the signers file holding the
    Owner's key, which git's configuration names; its second, by the planner that configuration names, builds in `src/`, naming no tracker.
    (the top, the commit that creates the project, the build commit)"""
    keys = run_area()["keys"]
    base = area / name
    top, origin = base / "wc", base / "origin.git"
    top.mkdir(parents=True)
    git(base, "init", "-q", "--bare", "--initial-branch=main", str(origin))
    git(top, "init", "-q", "--initial-branch=main")
    for k, v in (("user.name", OWNER[0]), ("user.email", OWNER[1]), ("gpg.format", "ssh"), ("user.signingkey", str(keys["owner"])),
                 ("gpg.ssh.allowedSignersFile", REL + "/allowed_signers"), ("commit.gpgsign", "false")):
        git(top, "config", k, v)
    git(top, "remote", "add", "origin", str(origin))
    (top / "README.md").write_text("a repository with no project yet\n", encoding="utf-8")
    (top / "src").mkdir()
    (top / "src/app.py").write_text("print('app')\n", encoding="utf-8")
    git(top, "add", "-A")
    git(top, "commit", "-q", "-m", "the start, with no project", "-S", who=OWNER, sign=keys["owner"])
    git(top, "push", "-q", "-u", "origin", "main")
    git(top, "remote", "set-head", "origin", "main")
    git(top, "switch", "-q", "-c", "start")
    (top / "shoalmark.toml").write_text(org_config(GATED), encoding="utf-8")
    (top / ".gitignore").write_text(f"{REL}/index.html\n{REL}/view/\n", encoding="utf-8")
    (top / REL).mkdir(parents=True)
    (top / REL / "OR-001-x.md").write_text(text("OR-001", f"tier: P2\ntriaged: {TODAY}\n"), encoding="utf-8")
    (top / REL / "allowed_signers").write_text(f"{OWNER[1]} " + keys["owner"].with_suffix(".pub").read_text(encoding="utf-8"), encoding="utf-8")
    run(top, "--print-written", who=OWNER)
    git(top, "add", "-A")
    git(top, "commit", "-q", "-m", "the project, created", "-S", who=OWNER, sign=keys["owner"])
    created = git(top, "rev-parse", "HEAD").strip()
    (top / "src/app.py").write_text("print('app, built')\n", encoding="utf-8")
    git(top, "commit", "-q", "-am", "build the app", who=COORD)
    return top, created, git(top, "rev-parse", "HEAD").strip()


def rows_new_project(area, add):
    def one(name, label, build):
        """One case: `build()` → (ok, what it saw); a step that fails is its row's failure, and the next case runs."""
        if not picked(name):
            return
        try:
            ok, saw = build()
        except Exception as e:
            ok, saw = False, f"{type(e).__name__}: {str(e)[:300]}"
        finally:
            fm.configure(HERE)
        add(label, ok, saw)

    def owner():
        r = org_hooked(area, "import-owner")
        paths, before = laid(r, TEAM, team_config(GATED), ("FM-001", "FM-002")), r.head()
        code, said = hooked(r, "the tool team's trackers, imported", who=OWNER, sign=True, trailers=IMPORTS[:1])
        made, o = r.head(), r.check("", who=COORD)
        sig = git(r.top, "log", "-1", "--format=%G?").strip()
        trailer = git(r.top, "log", "-1", "--format=%(trailers:key=Tracker-import,valueonly)").strip()
        held, got = judged(r.root(""), [made])
        return (code == 0 and made != before and sig == "G" and trailer == IMPORTS[0].split(": ", 1)[1]
                and all(p.startswith(TEAM + "/") for p in paths) and accepted(o, "refused") and held,
                f"hook exit {code}: {said.strip()[-400:]!r} · signature {sig!r} · trailer {trailer!r} · paths {paths} · {seen(o)} · judged {got}")
    one("import-owner", "a new project · the Owner's import of a team project, signed, carrying `Tracker-import:`, every path in the team's "
        "folder, made with the hooks on: the commit that creates the team project is the outer project's — its check judges it and refuses "
        "nothing in it", owner)

    def two():
        r = org_hooked(area, "import-two")
        laid(r, TEAM, team_config(GATED), ("FM-001", "FM-002"))
        before = r.head()
        first = hooked(r, "the tool team's trackers, imported", who=OWNER, sign=True, trailers=IMPORTS[:1])
        one_ = r.head()
        paths = laid(r, RUST, config("rust", "RS", (("planner", LEAD), ("builder", BUILDER)), GATED), ("RS-001",))
        second = hooked(r, "the rust team's trackers, imported", who=OWNER, sign=True, trailers=IMPORTS[1:])
        two_, o = r.head(), r.check("", who=COORD)
        held, got = judged(r.root(""), [one_, two_])
        return (first[0] == 0 and second[0] == 0 and len({before, one_, two_}) == 3 and all(p.startswith(RUST + "/") for p in paths)
                and accepted(o, "refused") and held,
                f"hooks exit {first[0]}, {second[0]}: {(first[1] + second[1]).strip()[-400:]!r} · {seen(o)} · judged {got}")
    one("import-two", "a new project · two teams' imports on one branch, the second on top of the first, each the Owner's, signed, made with "
        "the hooks on: the outer project's check judges each and refuses neither", two)

    def seat():
        r = org_hooked(area, "import-seat")
        laid(r, TEAM, team_config(GATED), ("FM-001", "FM-002"))
        before = r.head()
        code, said = hooked(r, "the tool team's trackers, imported", who=COORD, trailers=IMPORTS[:1])
        kept = r.head() == before
        if kept:                                                # the same commit, the hooks off, where the hook kept it out
            git(r.top, "commit", "-q", "-m", "the tool team's trackers, imported", "-m", IMPORTS[0], who=COORD)
        o = r.check("", who=COORD)
        return (code != 0 and kept and NO_OUTER in said and NO_TEAM not in said and refused(o, GATE),
                f"hook exit {code}, commit kept out {kept}: {said.strip()[-400:]!r} · {seen(o)}")
    one("import-seat", "a new project · a seat's import: the same commit by the outer project's planner, unsigned, under no `In Progress` "
        "tracker of the outer project — the outer hook refuses it by the outer project's build gate, and so does the outer check", seat)

    def own():
        r = org_hooked(area, "import-side")
        laid(r, SIDE, config("side", "SD", (("planner", COORD),)), ("SD-001", "SD-002"), signers=False)
        before = r.head()
        code, said = hooked(r, "a project of my own", who=COORD)
        kept = r.head() == before
        if kept:                                                # the same commit, the hooks off, where the hook kept it out
            git(r.top, "commit", "-q", "-m", "a project of my own", who=COORD)
        o = r.check("", who=COORD)
        return (code != 0 and kept and NO_OUTER in said and refused(o, GATE), f"hook exit {code}, commit kept out {kept}: {said.strip()[-400:]!r} · {seen(o)}")
    one("import-side", "a new project · a seat's own project: the outer project's planner creates a project below the top, its trackers in "
        "it, no build gate and no signers file, unsigned, under no `In Progress` tracker of the outer project — the outer hook refuses it by the outer "
        "project's build gate, and so does the outer check", own)

    def top():
        root, created, built = top_created(area, "top-created")
        said = run(root, "--check", who=COORD)
        real = fm.other_project_changes
        fm.other_project_changes = lambda items: set()          # no folder another project: the reading at the top before any was below it
        try:
            plain = run(root, "--check", who=COORD)
        finally:
            fm.other_project_changes = real
        held, got = judged(root, [created, built])
        return said == plain and held, f"{seen(said)} · with no project below {seen(plain)} · judged {got}"
    one("top-created", "a new project · at the top: on a branch whose first commit creates the project at the top, its check reads every "
        "commit as it reads them with no project below it, the commit that creates it and the build commit after it both judged", top)

    def self_named():
        r = Repo(area / "self-named", {"": org_config(GATED)}, {("", "OR-001"): text("OR-001", f"tier: P2\ntriaged: {TODAY}\n")},
                 {"src/app.py": "print('app')\n"})
        r.switch("-c", "work")
        laid(r, MINE, MINE_CONFIG, ("MY-001",), signers=False)
        created = r.commit("OR-001: a project of my own", who=COORD, index=False)     # under the outer project's judged tracker
        r.put(f"{MINE}/src/x.py", "print('built under no tracker')\n")
        built = r.commit("build, no tracker", who=COORD, index=False, paths=[f"{MINE}/src/x.py"])
        r.put(f"{MINE}/src/y.py", "print('the Owner, unsigned')\n")
        unsigned = r.commit("the Owner's identity, unsigned", who=OWNER, index=False, paths=[f"{MINE}/src/y.py"])
        o = r.check("", who=COORD)
        held, got = judged(r.root(""), [created, built, unsigned])
        return refused(o, GATE) and refused(o, "Owner commit") and held, f"{seen(o)} · judged {got}"
    one("self-named", "a new project · a seat creates a project on a branch, naming itself its Owner: the outer check judges every commit of "
        "that branch — a build commit in it under no tracker, and an unsigned commit there by the Owner's identity, are refused", self_named)

    def self_named_hooks():
        r = org_hooked(area, "self-named-hooks")
        laid(r, MINE, MINE_CONFIG, ("MY-001",), signers=False)
        made = hooked(r, "OR-001: a project of my own", who=COORD)
        r.put(f"{MINE}/src/x.py", "print('built under no tracker')\n")
        git(r.top, "add", "--", f"{MINE}/src/x.py")
        code, said = hooked(r, "build, no tracker", who=COORD)
        return made[0] == 0 and code != 0 and NO_OUTER in said, f"the creating commit: exit {made[0]} · the build: exit {code}: {said.strip()[-400:]!r}"
    one("self-named-hooks", "a new project · the same with the hooks on: the creating commit passes under the outer project's tracker, and the "
        "build commit after it, under no tracker, is refused by the outer project", self_named_hooks)

    def amended():
        r = org_hooked(area, "amended")
        laid(r, TEAM, team_config(), ("FM-001",))
        made = hooked(r, "the tool team's trackers, imported", who=OWNER, sign=True, trailers=IMPORTS[:1])
        r.put(f"{TEAM}/src/tool.py", "print('slipped into the import')\n")
        git(r.top, "add", "-A")
        env = dict(ids.ENV, GIT_AUTHOR_NAME=COORD[0], GIT_AUTHOR_EMAIL=COORD[1], GIT_COMMITTER_NAME=COORD[0], GIT_COMMITTER_EMAIL=COORD[1])
        done = subprocess.run(["git", "-C", str(r.top), "-c", "commit.gpgsign=false", "commit", "-q", "--amend", "--reset-author", "-m",
                               "the import, amended"], capture_output=True, text=True, encoding="utf-8", errors="replace", env=env)
        said = done.stdout + done.stderr
        return made[0] == 0 and done.returncode != 0 and NO_OUTER in said, f"the import: exit {made[0]} · the amend: exit {done.returncode}: {said.strip()[-400:]!r}"
    one("amended", "a new project · a seat amends the Owner's import that creates the team project, adding a build file and naming no tracker, "
        "with the hooks on: the outer project judges the amend, and refuses it", amended)

    def landed():
        r = org_hooked(area, "landed")
        laid(r, TEAM, team_config(GATED), ("FM-001",))
        made = hooked(r, "the tool team's trackers, imported", who=OWNER, sign=True, trailers=IMPORTS[:1])

        def build():
            r.put(f"{TEAM}/src/tool.py", "print('built in the team project')\n")
            git(r.top, "add", "--", f"{TEAM}/src/tool.py")
            git(r.top, "commit", "-q", "-m", "build the team's tool", who=LEAD)        # the hooks off: each check judges it
        build()
        before = r.check("", who=COORD)
        git(r.top, "reset", "-q", "--hard", "HEAD~1")
        r.land("import")
        r.switch("-c", "work")
        build()
        o, t = r.check("", who=COORD), r.check(TEAM)
        return (made[0] == 0 and refused(before, GATE) and accepted(o) and refused(t, GATE),
                f"the import: exit {made[0]} · on the import's branch: {seen(before)} · landed: {seen(o)} · {seen(t)}")
    one("landed", "a new project · a build commit wholly in the team project, naming no tracker, is the outer project's while the team's "
        "configuration is on a branch alone — the outer check refuses it — and once the default branch holds it, the team's own: the outer check "
        "skips it, and the team's check refuses it", landed)

    def landed_refused():
        r = Repo(area / "landed-refused", {"": org_config(GATED), MINE: REFUSED}, {("", "OR-001"): text("OR-001", f"tier: P2\ntriaged: {TODAY}\n"),
                 (MINE, "MY-001"): text("MY-001")}, {"src/app.py": "print('app')\n"})
        r.switch("-c", "work")
        r.put(f"{MINE}/shoalmark.toml", MINE_CONFIG)
        r.commit("OR-001: the project's configuration, mended", who=COORD, index=False)
        r.put(f"{MINE}/src/x.py", "print('built under no tracker')\n")
        r.commit("build, no tracker", who=COORD, index=False, paths=[f"{MINE}/src/x.py"])
        o = r.check("", who=COORD)
        return refused(o, GATE), seen(o)
    one("landed-refused", "a new project · the default branch holds the folder's `shoalmark.toml` as a configuration the tool refuses, and a branch "
        "mends it: a build commit there after the mend, under no tracker, is judged by the outer check, and refused", landed_refused)

    def taken_out(name):
        r, outer, team = gated(area, name, "")
        git(r.top, "rm", "-q", "--", r_at(team, "shoalmark.toml"))
        r.commit("take the team's configuration out", who=COORD, index=False)
        git(r.top, "checkout", "-q", "main", "--", r_at(team, "shoalmark.toml"))
        r.put(r_at(team, "src/evil.py"), "print('built as the project comes back')\n")
        return r, outer, team

    def recreated():
        r, outer, team = taken_out("re-created")
        r.commit("put the team's configuration back, and build", who=COORD, index=False)
        said = r.check(outer, who=COORD)
        return refused(said, NO_OUTER, "put the team's configuration back"), seen(said)
    one("re-created", "a new project · the default branch holds the team project, and a branch takes its configuration out, then puts it back "
        "beside a build under no tracker: at that commit's parent the folder is no project, so the outer check judges the commit, and refuses "
        "it", recreated)

    def recreated_hooks():
        r, outer, team = taken_out("re-created-hooks")
        installed = install_once(r, outer)
        git(r.top, "add", "-A")
        code, said = hooked(r, "put the team's configuration back, and build", who=COORD)
        return (installed[0] == 0 and code != 0 and NO_OUTER in said and NO_TEAM not in said,
                f"--install-hook exit {installed[0]} · hook exit {code}: {said.strip()[-400:]!r}")
    one("re-created-hooks", "a new project · the same commit made with the hooks on: HEAD holds no configuration in the team's folder, so the "
        "outer project judges the commit being made, by its own rule, and refuses it", recreated_hooks)

    def tracker_out(name):
        r, outer, team = gated(area, name, "")
        git(r.top, "rm", "-q", "-r", "--", r_at(team, REL))
        r.commit("take the team's tracker folder out", who=COORD, index=False)
        r.put(r_at(team, "src/evil.py"), "print('built where the project lost its tracker folder')\n")
        return r, outer, team

    def tracker_gone():
        r, outer, team = tracker_out("tracker-out")
        r.commit("build where the team's tracker folder was", who=COORD, index=False)
        said = r.check(outer, who=COORD)
        return refused(said, NO_OUTER, "build where the team's tracker folder was"), seen(said)
    one("tracker-out", "a new project · the default branch holds the team project, and a branch takes its tracker folder out, then builds in "
        "its folder under no tracker: at that commit's parent the folder holds no tracker folder, so it is no project, and the outer check "
        "judges the commit, and refuses it", tracker_gone)

    def tracker_gone_hooks():
        r, outer, team = tracker_out("tracker-out-hooks")
        installed = install_once(r, outer)
        git(r.top, "add", "-A")
        code, said = hooked(r, "build where the team's tracker folder was", who=COORD)
        return (installed[0] == 0 and code != 0 and NO_OUTER in said and NO_TEAM not in said,
                f"--install-hook exit {installed[0]} · hook exit {code}: {said.strip()[-400:]!r}")
    one("tracker-out-hooks", "a new project · the same commit made with the hooks on: HEAD holds no tracker folder in the team's folder, so "
        "the outer project judges the commit being made, and refuses it", tracker_gone_hooks)


MINE = "teams/mine"
MINE_CONFIG = f'name = "mine"\nowner = "{COORD[1]}"\n[kinds]\nMY = "Work"\n[seats]\nplanner = "{LEAD[1]}"\n'     # a seat names itself the Owner


# --- the tool's command: a project below the top names the tool from its own root, so every run writes one INDEX.md -------------------

_TREE = {"source": None}           # a mutant of the tool a row keeps in its repository: the tool's text with its pairs replaced, written where it is kept
TOOL_AT = "tools/shoalmark"        # where org's layout keeps the tool: the top's `tools/`
PERSON = {k: v for k, v in ids.ENV.items() if k != "SHOALMARK_CMD"}    # a person's shell: no wrapper names the command


def vendored(r, at=TOOL_AT):
    """The tool written into `at` from the top, the top's `tools/shoalmark/` unless named — the files the hooks' copy holds, `shoalmark.py` the
    mutant's text where one is set — each pinned in its PIN as `--vendor` pins it, committed by the Owner, signed, and pushed."""
    dest, lines = r.top / at, []
    for rel in fm.copy_files():
        data = _TREE["source"].encode("utf-8") if rel == "shoalmark.py" and _TREE["source"] is not None else (HERE / rel).read_bytes()
        (dest / rel).parent.mkdir(parents=True, exist_ok=True)
        (dest / rel).write_bytes(data)
        normalized = data.replace(b"\r\n", b"\n")
        lines.append(f"{hashlib.sha256(normalized).hexdigest()}  {rel}")
    (dest / "PIN").write_text("\n".join(lines) + "\n", encoding="utf-8")
    r.commit("the tool, vendored", who=OWNER, sign=True, paths=[at])
    git(r.top, "push", "-q", "origin", "main")


def by_hand(cwd, path, *argv, who=LEAD):
    """The tool at `path`, run in a process of its own from `cwd`, as `who` runs it in a shell: (exit, stdout, stderr)."""
    env = dict(PERSON, GIT_AUTHOR_NAME=who[0], GIT_AUTHOR_EMAIL=who[1], GIT_COMMITTER_NAME=who[0], GIT_COMMITTER_EMAIL=who[1])
    done = subprocess.run([sys.executable, "-I", str(path), *argv], cwd=cwd, capture_output=True, text=True, encoding="utf-8", errors="replace", env=env)
    return done.returncode, done.stdout, done.stderr


def org_tools(area, name, projects, trackers):
    """Org's layout with the tool in the top's `tools/shoalmark/`: `projects` as `Repo` takes them, the tool vendored on `main`, and the hooks
    installed once, at the top, with that tool — the copy it writes replaced by the mutant's text where one is set."""
    r = Repo(area / name, projects, trackers, {"src/app.py": "print('app')\n"})
    vendored(r)
    said = by_hand(r.top, f"{TOOL_AT}/shoalmark.py", "--install-hook", who=OWNER)
    if said[0] != 0:
        raise AssertionError(f"--install-hook: {seen(said)}")
    if _COPY["source"] is not None:
        common = git(r.top, "rev-parse", "--git-common-dir").strip()
        (r.top / common / fm.COPY_DIR / "shoalmark.py").write_text(_COPY["source"], encoding="utf-8")
    return r


def written_thrice(r, folder, tid, who):
    """INDEX.md of the project in `folder`, once one of its trackers is reworded, as three runs write it over a placeholder: a run from the
    project, by the tool's path from there; a run with `--root`, from outside the repository; and the hooks' pre-commit run of the commit that
    stages the change. (the three as bytes, the tool's path from the project, the exits of the first two, the commit's exit and what it printed)"""
    index, t = r.root(folder) / REL / "INDEX.md", r.path(folder, tid)
    t.write_text(t.read_text(encoding="utf-8").replace(f'hook: "h of {tid}"', f'hook: "h of {tid}, reworded"'), encoding="utf-8")
    typed = os.path.relpath(r.top / TOOL_AT / "shoalmark.py", r.root(folder)).replace(os.sep, "/")
    got, exits = [], []
    for cwd, argv in ((r.root(folder), (typed,)), (r.base, (r.top / TOOL_AT / "shoalmark.py", "--root", r.root(folder)))):
        index.write_bytes(b"placeholder\n")
        exits.append(by_hand(cwd, *argv, who=who)[0])
        got.append(index.read_bytes())
    index.write_bytes(b"placeholder\n")
    git(r.top, "add", "-A")
    code, said = hooked(r, f"{tid}: its hook, reworded", who=who, shell=PERSON)
    got.append(subprocess.run(["git", "-C", str(r.top), "show", f"HEAD:{r_at(folder, REL + '/INDEX.md')}"], capture_output=True, env=ids.ENV).stdout)
    return got, typed, exits, code, said


def rows_command(area, add):
    def one(name, label, build):
        """One case: `build()` → (ok, what it saw); a step that fails is its row's failure, and the next case runs."""
        if not picked(name):
            return
        try:
            ok, saw = build()
        except Exception as e:
            ok, saw = False, f"{type(e).__name__}: {str(e)[:300]}"
        finally:
            fm.configure(HERE)
        add(label, ok, saw)

    def thrice(name, folder, tid, who, named):
        def build():
            r = org_tools(area, name, {"": org_config(), TEAM: team_config()}, {("", "OR-001"): text("OR-001"), (TEAM, "FM-001"): text("FM-001")})
            got, typed, exits, code, said = written_thrice(r, folder, tid, who)
            header = [next((l for l in g.decode("utf-8", "replace").splitlines() if "GENERATED" in l), "") for g in got]
            return (code == 0 and got[0] == got[1] == got[2] and typed == named and f"Run `{fm.PY} {named}` after" in header[0],
                    f"exits {exits}, hook exit {code}: {said.strip()[-300:]!r} · the same bytes {got[0] == got[1]}, {got[1] == got[2]} · headers {header}")
        return build

    one("command-below", "the tool's command · below the top, the tool in the top's `tools/`: a run from the team project, a run with `--root` and "
        "the hooks' pre-commit run write one INDEX.md, byte for byte, whose header names the tool from the project's root, "
        "`../../tools/shoalmark/shoalmark.py`", thrice("command-below", TEAM, "FM-001", LEAD, "../../tools/shoalmark/shoalmark.py"))
    one("command-top", "the tool's command · at the top, the tool in its `tools/`: the same three runs write one INDEX.md, byte for byte, whose "
        "header names `tools/shoalmark/shoalmark.py` as it did", thrice("command-top", "", "OR-001", COORD, "tools/shoalmark/shoalmark.py"))

    def imported():
        r = org_tools(area, "command-import", {"": org_config(GATED)}, {("", "OR-001"): text("OR-001", f"tier: P2\ntriaged: {TODAY}\n")})
        r.switch("-c", "import")
        laid(r, TEAM, team_config(), ("FM-001", "FM-002"))         # no build gate: the team's own reading of the commit that creates it is not this row's
        wrote = by_hand(r.top, f"{TOOL_AT}/shoalmark.py", "--root", TEAM, "--print-written", who=OWNER)      # the creating commit's hooks write none of its files
        git(r.top, "add", "-A")
        code, said = hooked(r, "the tool team's trackers, imported", who=OWNER, sign=True, trailers=IMPORTS[:1], shell=PERSON)
        git(r.top, "push", "-q", "origin", "import")
        elsewhere = r.base / "elsewhere"                     # the team's own clone of the same repository, at another path
        git(r.base, "clone", "-q", "--branch", "import", str(r.origin), str(elsewhere))
        git(elsewhere, "config", "gpg.ssh.allowedSignersFile", r.signers_rel)      # set up as the Owner's clone is
        checks = [by_hand(top / TEAM, f"../../{TOOL_AT}/shoalmark.py", "--check", who=LEAD) for top in (r.top, elsewhere)]
        stale = [[l for l in (c[1] + c[2]).splitlines() if "STALE" in l or l.lstrip().startswith(("-> **GENERATED", "+> **GENERATED"))] for c in checks]
        return (wrote[0] == 0 and code == 0 and not any(stale),
                f"--root exit {wrote[0]}, hook exit {code}: {said.strip()[-200:]!r} · the team's --check in the Owner's clone and in its own: exits "
                f"{[c[0] for c in checks]}, {stale}")
    def from_below():
        r = Repo(area / "command-from-below", {"": org_config(), TEAM: team_config()}, {("", "OR-001"): text("OR-001"), (TEAM, "FM-001"): text("FM-001")},
                 {"src/app.py": "print('app')\n"})
        vendored(r)
        installed = by_hand(r.root(TEAM), f"../../{TOOL_AT}/shoalmark.py", "--install-hook", who=OWNER)
        index, t = r.top / REL / "INDEX.md", r.path("", "OR-001")
        t.write_text(t.read_text(encoding="utf-8").replace('hook: "h of OR-001"', 'hook: "h of OR-001, reworded"'), encoding="utf-8")
        index.write_bytes(b"placeholder\n")
        direct = by_hand(r.top, f"{TOOL_AT}/shoalmark.py", who=COORD)
        by_run = index.read_bytes()
        index.write_bytes(b"placeholder\n")
        git(r.top, "add", "-A")
        code, said = hooked(r, "OR-001: its hook, reworded", who=COORD, shell=PERSON)
        by_hook = subprocess.run(["git", "-C", str(r.top), "show", f"HEAD:{REL}/INDEX.md"], capture_output=True, env=ids.ENV).stdout
        header = lambda b: next((l for l in b.decode("utf-8", "replace").splitlines() if "GENERATED" in l), "")
        return (installed[0] == 0 and direct[0] == 0 and code == 0 and by_run == by_hook,
                f"--install-hook from {TEAM}/: exit {installed[0]} · the direct run at the top: exit {direct[0]}, header {header(by_run)!r} · "
                f"the hook: exit {code} {said.strip()[-200:]!r}, header {header(by_hook)!r} · the same bytes {by_run == by_hook}")
    one("command-from-below", "the tool's command · the hooks installed from the team project below the top, by the tool in the top's `tools/`: "
        "the outer project's INDEX.md, as the hooks write it at the top, is the same bytes as a direct run's there", from_below)

    def copy_outside():
        r = org_tools(area, "command-copy-outside", {"": org_config(), TEAM: team_config()}, {("", "OR-001"): text("OR-001"), (TEAM, "FM-001"): text("FM-001")})
        common = Path(git(r.top, "rev-parse", "--git-common-dir").strip())
        record = (common if common.is_absolute() else r.top / common) / fm.COPY_DIR / "COPY"
        lines = record.read_text(encoding="utf-8").splitlines()
        record.write_text("".join(("tool: ../outside" if one.startswith("tool: ") else one) + "\n" for one in lines), encoding="utf-8")
        t = r.path(TEAM, "FM-001")
        t.write_text(t.read_text(encoding="utf-8").replace('hook: "h of FM-001"', 'hook: "h of FM-001, reworded"'), encoding="utf-8")
        git(r.top, "add", "-A")
        code, said = hooked(r, "FM-001: its hook, reworded", who=LEAD, shell=PERSON)
        got = subprocess.run(["git", "-C", str(r.top), "show", f"HEAD:{TEAM}/{REL}/INDEX.md"], capture_output=True, env=ids.ENV).stdout
        header = next((l for l in got.decode("utf-8", "replace").splitlines() if "GENERATED" in l), "")
        return (any(one.startswith("tool: ") for one in lines) and code == 0 and f"Run `{fm.PY} {TOOL_AT}/shoalmark.py` after" in header,
                f"hook exit {code}: {said.strip()[-200:]!r} · header {header!r}")
    one("command-copy-outside", "the tool's command · a COPY whose `tool:` climbs out of the working tree, `../outside`, is not taken: the hooks "
        "name the team project by the command `--install-hook` recorded, and no path outside the working tree", copy_outside)

    def own_tool():
        r = org_tools(area, "command-own", {"": org_config(), TEAM: team_config()}, {("", "OR-001"): text("OR-001"), (TEAM, "FM-001"): text("FM-001")})
        vendored(r, f"{TEAM}/{TOOL_AT}")                     # the team keeps its own tool, at its root's `tools/shoalmark/`
        own, t = f"{TOOL_AT}/shoalmark.py", r.path(TEAM, "FM-001")
        header = lambda b: next((l for l in b.decode("utf-8", "replace").splitlines() if "GENERATED" in l), "")
        ok, saw = True, []
        for n, (old, new) in enumerate((("h of FM-001", "h of FM-001, reworded"), ("h of FM-001, reworded", "h of FM-001, reworded again"))):
            t.write_text(t.read_text(encoding="utf-8").replace(f'hook: "{old}"', f'hook: "{new}"'), encoding="utf-8")
            direct = by_hand(r.root(TEAM), own, who=LEAD)[0] if n == 0 else None     # first by the team's own run, then by the hooks alone
            wrote = (r.root(TEAM) / REL / "INDEX.md").read_bytes()
            git(r.top, "add", "-A")
            code, said = hooked(r, f"FM-001: its hook, reworded, step {n}", who=LEAD, shell=PERSON)
            got = subprocess.run(["git", "-C", str(r.top), "show", f"HEAD:{TEAM}/{REL}/INDEX.md"], capture_output=True, env=ids.ENV).stdout
            check = by_hand(r.root(TEAM), own, "--check", who=LEAD)
            ok = (ok and code == 0 and check[0] == 0 and f"Run `{fm.PY} {own}` after" in header(got) and (n or got == wrote))
            saw.append(f"step {n}: run exit {direct}, hook exit {code} {said.strip()[-160:]!r}, header {header(got)!r}, "
                       f"the team's --check exit {check[0]} {(check[1] + check[2]).strip()[-200:]!r}")
        return ok, " · ".join(saw)
    one("command-own", "the tool's command · a team project that keeps its own tool at its root's `tools/`, the hooks installed at the top: "
        "each commit the hooks write names the team's own tool, `tools/shoalmark/shoalmark.py`, in its INDEX.md — the same bytes as the team's "
        "own run — and the team's `--check`, by its own tool, passes after each", own_tool)

    one("command-import", "the tool's command · after the Owner's import of a team project without a build gate — its INDEX.md written by a run "
        "with `--root` from the top, the commit made with the hooks on — the team's `--check`, run from the project by the tool's path from there, "
        "prints no STALE line, in the Owner's clone and in another", imported)


# --- after the move: a team project's ship-log row names its code repository's commit; a code repository names where its trackers live ---

CODE = '[repositories]\ntool = "https://example.invalid/tool.git"\n'
ELSEWHERE = '[trackers]\nelsewhere = "https://example.invalid/planning.git, teams/tool/"\n'
OTHER = "0123456789abcdef0123456789abcdef01234567"      # a commit of the code repository, which this repository does not hold
CODE_LINE = ("the Shipped rule: 1 move to `Shipped` rests on a ship-log row naming `<repository>@<commit>` for a code repository "
             "`[repositories]` names (tool) — taken as the commit behind the move, that repository unread: FM-001")
ELSEWHERE_SAID = "this repository's trackers live elsewhere — https://example.invalid/planning.git, teams/tool/ (`[trackers] elsewhere` in shoalmark.toml)"
KEYS = "keys/allowed_signers"       # a code repository's signers file, from its root: it holds no tracker folder
NOT_NAMED = "names a code repository the default branch's `[repositories]` does not name, so it counts as no commit"
FOLDER_HELD = ("shoalmark.toml: `[trackers] elsewhere` is for a code repository whose trackers live in another, and this project holds a tracker "
               "folder, {} — its trackers live here: take the table out")


def rows_after_move(area, add):
    def named(r, f):
        r.write(f, "FM-001", shipped(r.read(f, "FM-001"), f"Built in tool@{OTHER[:12]}."))
        r.commit("FM-001: shipped")
        said = r.check(f)
        return accepted(said, "with no commit behind it"), seen(said)
    each(area, add, "code-named", "after the move · a ship-log row naming `tool@<commit>`, a code repository `[repositories]` names, the commit one "
         "this repository does not hold — accepted as the commit behind the move, the other repository unread", named, {"FM-001": text("FM-001")},
         tables=CODE)

    def not_named(r, f):
        r.put(r.at(f, "src/tool.py"), "print('built')\n")
        built = r.commit("FM-001: built", paths=[r.at(f, "src/tool.py")])
        r.write(f, "FM-001", shipped(r.read(f, "FM-001"), f"Built in web@{built[:12]}."))
        r.commit("FM-001: shipped")
        said = r.check(f)
        return refused(said, f"FM-001: moved to `Shipped` with no commit behind it — `web@{built[:12]}` " + NOT_NAMED), seen(said)
    each(area, add, "code-not-named", "after the move · a ship-log row naming `web@<commit>`, a repository `[repositories]` does not name — refused: "
         "it counts as no commit, though its hash is this repository's commit that built the change", not_named, {"FM-001": text("FM-001")},
         tables=CODE)

    def the_line(r, f):
        r.put(r.at(f, "src/tool.py"), "print('built')\n")
        built = r.commit("FM-002: built", paths=[r.at(f, "src/tool.py")])
        r.write(f, "FM-001", shipped(r.read(f, "FM-001"), f"Built in tool@{OTHER[:12]}."))
        r.write(f, "FM-002", shipped(r.read(f, "FM-002"), f"Built in {built[:12]}, and in tool@{OTHER[:12]}."))
        r.commit("FM-001, FM-002: shipped")
        said = r.check(f)
        lines = [line for line in said[1].splitlines() if line.startswith("the Shipped rule: ")]
        return accepted(said, "with no commit behind it") and lines == [CODE_LINE], f"{lines} · " + seen(said)
    each(area, add, "code-line", "after the move · `--check` says in one line how many moves rest on such a row: one, FM-001's — FM-002 names "
         "this repository's commit behind it as well, and rests on that", the_line, {"FM-001": text("FM-001"), "FM-002": text("FM-002")},
         tables=CODE)

    def unfit(r, f):
        said = {}
        for name, tables in (("repositories", '[repositories]\ntool = ""\n'), ("trackers", '[trackers]\nelsewhere = "x"\nwhere = "y"\n')):
            r.root(f).joinpath("shoalmark.toml").write_text(team_config(tables=tables), encoding="utf-8")
            said[name] = r.check(f)
        lines = {"repositories": "shoalmark.toml: `[repositories]` names each code repository a ship-log row may name as `<repository>@<commit>` — "
                                 "`<repository> = \"<where it is>\"`, its URL or its path, a non-empty string. Got {'tool': ''}",
                 "trackers": "shoalmark.toml: `[trackers]` holds one key, `elsewhere = \"<where>\"` — where this code repository's trackers live, a "
                             "non-empty string. Got {'elsewhere': 'x', 'where': 'y'}"}
        return (all(said[k][0] == 1 and said[k][2].strip() == lines[k] and not said[k][1].strip() for k in lines),
                " · ".join(f"exit {c}: {e.strip()[:300]!r}" for c, _o, e in said.values()))
    each(area, add, "code-unfit", "after the move · a `[repositories]` value that is empty, and a `[trackers]` with a key besides `elsewhere`, are "
         "each refused at configuration in one line, exit 1", unfit, {"FM-001": text("FM-001")})

    def elsewhere_check(r, f):
        r.switch("-c", "work")                          # off the default branch, where the build gate judges every commit
        r.put(r.at(f, "src/tool.py"), "print('built')\n")
        r.commit("build the tool", paths=[r.at(f, "src/tool.py")])
        said = r.check(f)
        want = ELSEWHERE_SAID + ": nothing here is judged, and the build gate, `judged_before_build`, is off\n"
        return said[0] == 0 and said[1] == want and not said[2], f"exit {said[0]}: stdout {said[1][:300]!r} · stderr {said[2][:300]!r}"
    each(area, add, "elsewhere-check", "trackers elsewhere · a code repository marked so: `--check` says so in one line and passes — a build commit "
         "on a branch, naming no tracker, under `judged_before_build = true`, is not judged", elsewhere_check, top=GATED, tables=ELSEWHERE, signers_in=KEYS)

    def refusal(argvs, line):
        def case(r, f):
            state = lambda: git(r.top, "status", "--porcelain", "--untracked-files=all", "--ignored")
            before = state()
            said = [run(r.root(f), *argv, who=LEAD) for argv in argvs]
            after = state()
            return (all(s[0] == fm.EXIT_LINT and s[2] == line + "\n" and not s[1] for s in said) and before == after,
                    " · ".join(f"exit {s[0]}: {s[2].strip()[:300]!r}" for s in said) + ("" if before == after else f" · wrote {after!r}"))
        return case
    for name, what, argvs, said in (("elsewhere-init", "`--init`", [("--init",)], "--init: {}: run it there"),
                                    ("elsewhere-new", "`--new`", [("--new", "a", "new", "tracker")], "--new: {}: file the tracker there"),
                                    ("elsewhere-board", "the board — `--html-only`, and the run that writes INDEX.md and the board —", [("--html-only",), ()],
                                     "the board: {}: its board is built there")):
        each(area, add, name, f"trackers elsewhere · a code repository marked so: {what} refuses in one line, exit 4, and writes nothing",
             refusal(argvs, said.format(ELSEWHERE_SAID) + " — nothing is written"), tables=ELSEWHERE, signers_in=KEYS)

    def gate_off(r, f):
        r.switch("-c", "work")
        r.put(r.at(f, "src/tool.py"), "print('built')\n")
        git(r.top, "add", "--", r.at(f, "src/tool.py"))
        msg = r.base / "msg"
        msg.write_text("build the tool\n", encoding="utf-8")
        said = run(r.root(f), "--commit-msg", str(msg), who=LEAD)
        return said[0] == 0 and GATE not in said[2], seen(said)
    each(area, add, "elsewhere-gate", "trackers elsewhere · a code repository marked so, with `judged_before_build = true`: the build gate is off — "
         "the commit being made on a branch, naming no tracker, passes the commit-msg check", gate_off, top=GATED, tables=ELSEWHERE, signers_in=KEYS)

    def hook_run(r, f):
        said = run(r.root(f), "--print-written", who=LEAD)
        want = ELSEWHERE_SAID + ": nothing here is judged, and the build gate, `judged_before_build`, is off\n"
        return said[0] == 0 and said[1] == "" and said[2] == want, f"exit {said[0]}: stdout {said[1][:200]!r} · stderr {said[2][:300]!r}"
    each(area, add, "elsewhere-hook", "trackers elsewhere · a code repository marked so: the pre-commit hook's run, `--print-written`, says so in "
         "one line on stderr, prints nothing on stdout and passes", hook_run, tables=ELSEWHERE, signers_in=KEYS)

    def on_a_branch(r, f):
        said = {}
        for name, extra in (("control", ""), ("table", '[trackers]\nelsewhere = "anywhere"\n')):
            git(r.top, "switch", "-q", "-c", f"work-{name}", "main")
            r.write(f, "FM-001", closed(r.read(f, "FM-001")))                  # a close by no seat: the rights rule refuses it
            r.put(r.signers_rel, (r.top / r.signers_rel).read_text(encoding="utf-8") + f"{PROBE[1]} ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIOnly\n")
            r.put(r.at(f, "src/evil.py"), "print('built under no tracker')\n")
            cfg = r.root(f) / "shoalmark.toml"
            cfg.write_text(cfg.read_text(encoding="utf-8") + extra, encoding="utf-8")
            r.commit("no tracker named", who=PROBE, index=False)
            said[name] = r.check(f, who=PROBE)
        ok = (said["control"][0] == fm.EXIT_LINT and refused(said["control"], "FM-001: this change is a `close`", "is not a seat")
              and said["table"][0] == 1 and said["table"][2] == FOLDER_HELD.format(REL + "/") + "\n" and not said["table"][1])
        return ok, " · ".join(f"{k}: exit {c}: {(o + e).strip()[:300]!r}" for k, (c, o, e) in said.items())
    each(area, add, "elsewhere-branch", "trackers elsewhere · a branch of a project that holds trackers adds the table, with a close by no seat, a key "
         "added to the signers file and a build under no tracker: refused at configuration in one line, exit 1, naming the tracker folder — the "
         "same commit without the table refused by the rights rule", on_a_branch, {"FM-001": text("FM-001", f"tier: P2\ntriaged: {TODAY}\n")}, top=GATED)

    def judged_on_a_branch(r, f):
        r.switch("-c", "work")
        cfg = r.root(f) / "shoalmark.toml"
        cfg.write_text(cfg.read_text(encoding="utf-8") + ELSEWHERE, encoding="utf-8")
        r.put(r.at(f, "src/tool.py"), "print('built')\n")
        r.commit("build the tool", index=False)
        check = r.check(f)
        r.put(r.at(f, "src/more.py"), "print('more')\n")
        git(r.top, "add", "--", r.at(f, "src/more.py"))
        msg = r.base / "msg"
        msg.write_text("build more\n", encoding="utf-8")
        gate = run(r.root(f), "--commit-msg", str(msg), who=LEAD)
        ok = check[0] != 0 and ELSEWHERE_SAID not in check[1] + check[2] and gate[0] != 0 and GATE in gate[2]
        return ok, f"--check: {seen(check)} · --commit-msg: {seen(gate)}"
    each(area, add, "elsewhere-branch-code", "trackers elsewhere · a code repository whose default branch does not hold the table, a branch that adds "
         "it: judged by every rule — `--check` does not pass it, and the commit-msg check refuses a build commit naming no tracker",
         judged_on_a_branch, top=GATED, signers_in=KEYS)

    def held_on_main(r, f):
        r.switch("-c", "work")
        git(r.root(f), "rm", "-q", "-r", "--", REL)
        if (r.root(f) / REL).exists():                                     # what git does not track in it, moved out of the working tree
            os.rename(r.root(f) / REL, r.base / "set-aside")
        cfg = r.root(f) / "shoalmark.toml"
        cfg.write_text(cfg.read_text(encoding="utf-8") + ELSEWHERE, encoding="utf-8")
        r.commit("the trackers live elsewhere now", index=False)
        said = r.check(f)
        return said[0] == 1 and said[2] == FOLDER_HELD.format(f"{REL}/ on origin/main") + "\n" and not said[1], seen(said)
    each(area, add, "elsewhere-folder-landed", "trackers elsewhere · a branch that takes the tracker folder out and adds the table: refused at "
         "configuration in one line, exit 1 — the default branch holds the tracker folder", held_on_main, {"FM-001": text("FM-001")}, signers_in=KEYS)

    def unread(r, f):
        git(r.top, "remote", "remove", "origin")
        said = r.check(f)
        return said[0] != 0 and ELSEWHERE_SAID not in said[1] + said[2], seen(said)
    each(area, add, "elsewhere-unread", "trackers elsewhere · where the default branch cannot be read — no `origin` — the table is not in force: "
         "`--check` does not pass", unread, top=GATED, tables=ELSEWHERE, signers_in=KEYS)

    def repositories_on_a_branch(r, f):
        said = {}
        for name, extra in (("control", ""), ("named", '[repositories]\nanything = "x"\n')):
            git(r.top, "switch", "-q", "-c", f"work-{name}", "main")
            r.write(f, "FM-001", shipped(r.read(f, "FM-001"), f"Built in anything@{OTHER[:12]}."))
            cfg = r.root(f) / "shoalmark.toml"
            cfg.write_text(cfg.read_text(encoding="utf-8") + extra, encoding="utf-8")
            r.commit("FM-001: shipped", who=LEAD)
            said[name] = r.check(f, who=LEAD)
        ok = (refused(said["control"], "FM-001: moved to `Shipped` with no commit behind it")
              and refused(said["named"], f"FM-001: moved to `Shipped` with no commit behind it — `anything@{OTHER[:12]}` " + NOT_NAMED)
              and "the Shipped rule: " not in said["named"][1])
        return ok, " · ".join(f"{k}: exit {c}: {(o + e).strip()[-300:]!r}" for k, (c, o, e) in said.items())
    each(area, add, "code-branch", "after the move · a branch that adds `[repositories]` and ships on a row naming that repository: refused — "
         "the repository counts once the default branch names it, and `--check` says nothing of rows resting on it; the same commit without "
         "the table refused too", repositories_on_a_branch, {"FM-001": text("FM-001")})

    def code_unread(r, f):
        git(r.top, "remote", "remove", "origin")
        r.write(f, "FM-001", shipped(r.read(f, "FM-001"), f"Built in tool@{OTHER[:12]}."))
        r.commit("FM-001: shipped")
        said = r.check(f)
        return refused(said, f"FM-001: moved to `Shipped` with no commit behind it — `tool@{OTHER[:12]}` " + NOT_NAMED), seen(said)
    each(area, add, "code-unread", "after the move · where the default branch cannot be read — no `origin` — no repository `[repositories]` "
         "names counts: a row naming `tool@<commit>` is refused as no commit", code_unread, {"FM-001": text("FM-001")}, tables=CODE)

    def taken_out(r, f):
        r.switch("-c", "work")
        cfg = r.root(f) / "shoalmark.toml"
        before = cfg.read_text(encoding="utf-8")
        cfg.write_text(before.replace(ELSEWHERE, ""), encoding="utf-8")
        r.put(r.at(f, "src/tool.py"), "print('built')\n")
        r.commit("build the tool", index=False)
        check = r.check(f)
        r.put(r.at(f, "src/more.py"), "print('more')\n")
        git(r.top, "add", "--", r.at(f, "src/more.py"))
        msg = r.base / "msg"
        msg.write_text("build more\n", encoding="utf-8")
        gate = run(r.root(f), "--commit-msg", str(msg), who=LEAD)
        ok = ELSEWHERE in before and check[0] != 0 and ELSEWHERE_SAID not in check[1] + check[2] and gate[0] != 0 and GATE in gate[2]
        return ok, f"--check: {seen(check)} · --commit-msg: {seen(gate)}"
    each(area, add, "elsewhere-removed", "trackers elsewhere · a code repository whose default branch holds the table, a branch that takes it out: "
         "judged by every rule — `--check` does not pass it, and the commit-msg check refuses a build commit naming no tracker", taken_out,
         top=GATED, tables=ELSEWHERE, signers_in=KEYS)

    def tip_out(r, f):
        r.switch("-c", "work")
        r.put(r.at(f, "src/tool.py"), "print('built')\n")
        r.commit("build the tool", index=False)
        r.switch("main")
        cfg = r.root(f) / "shoalmark.toml"
        before = cfg.read_text(encoding="utf-8")
        cfg.write_text(before.replace(ELSEWHERE, ""), encoding="utf-8")
        r.put(r.signers_rel, (r.top / r.signers_rel).read_text(encoding="utf-8") + f"{PROBE[1]} ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIOnly\n")
        r.commit("the table out, and a key added", index=False)                   # a seat's change of the signers file: the filed line does not accept it
        git(r.top, "push", "-q", "origin", "main")
        git(r.top, "fetch", "-q", "origin")
        r.switch("work")
        check = r.check(f)
        r.put(r.at(f, "src/more.py"), "print('more')\n")
        git(r.top, "add", "--", r.at(f, "src/more.py"))
        msg = r.base / "msg"
        msg.write_text("build more\n", encoding="utf-8")
        gate = run(r.root(f), "--commit-msg", str(msg), who=LEAD)
        ok = ELSEWHERE in before and check[0] != 0 and ELSEWHERE_SAID not in check[1] + check[2] and gate[0] != 0 and GATE in gate[2]
        return ok, f"--check: {seen(check)} · --commit-msg: {seen(gate)}"
    each(area, add, "elsewhere-tip-out", "trackers elsewhere · the Owner's start holds the table, and a seat's commit on the default branch that the "
         "filed line does not accept takes it out and adds a key to the signers file: the tip holds no table, so none is in force, though the state "
         "in force holds one — a branch that still holds it is judged by every rule: `--check` does not pass it, and the commit-msg check refuses a "
         "build commit naming no tracker", tip_out, top=GATED, tables=ELSEWHERE, signers_in=KEYS)

    if picked("code-schema"):
        code, out, err = run(HERE, "--schema")
        found = [line for line in out.split("\n") if line.startswith(("| `[repositories] <repository>` |", "| `[trackers] elsewhere` |"))]
        add("after the move · `--schema` names `[repositories]` — a ship-log row's `<repository>@<commit>` — and `[trackers] elsewhere`, a row each",
            code == 0 and len(found) == 2 and "`<repository>@<commit>`" in found[0] and "counts as no commit" in found[0]
            and "`judged_before_build` is off" in found[1], f"exit {code}: {found}")


ROWS = (rows_rights, rows_shipped, rows_records, rows_asks, rows_ids, rows_lost_answer, rows_index, rows_signers, rows_reads, rows_acceptance,
        rows_other_project, rows_hooks, rows_new_project, rows_command, rows_after_move)


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
    ("a records entry written from the top read as written, below the top", "records_problem", [("if entry.startswith(prefix):", "if False:", 1)],
     (rows_records,), {"records-from-top"}, BELOW),
    ("a records entry refused at the top too, where the root's folder is empty", "records_problem",
     [("if not prefix or not isinstance(records, list)", "if not isinstance(records, list)", 1)], (rows_records,), {"records-from-top", "records-only"}, False),
    ("another project's skip taken where only some paths lie in it", "other_project_changes", [("if rels and all(", "if rels and any(", 1)],
     (rows_other_project,), {"both"}, False),
    ("another project's skip taken for a folder with no `shoalmark.toml`", "other_project_changes",
     [("if f.parts and os.path.lexists(ROOT / f / CONFIG_NAME)]", "if f.parts]", 1), ("held.get(spec(rev, home)) is not None", "True", 1)],
     (rows_other_project,), {"plain"}, False),
    ("another project's skip taken by the working tree alone", "other_project_changes", [("held.get(spec(rev, home)) is not None", "True", 1)],
     (rows_other_project,), {"before-toml"}, False),
    ("another project's `shoalmark.toml` read from the top", "other_project_changes",
     [('f"{parent(rev)}:./{home}/{CONFIG_NAME}"', 'f"{parent(rev)}:{home}/{CONFIG_NAME}"', 1)], (rows_other_project,), {"skip", "staged"}, False),
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
    ("the hooks' copy judges every staged path by the top's project alone", "copy:staged_projects",
     [('homes.setdefault(top.joinpath(*parts[:at]), []).append("/".join(parts[at:]))', "homes.setdefault(top, []).append(path)", 1)],
     (rows_hooks,), {"hooks-top"}, False),
    ("the hooks' copy runs one project where the commit stages paths in two", "copy:each_project",
     [("for root, rels in (staged_projects(top, paths) or {top: []}).items():", "for root, rels in list((staged_projects(top, paths) or {top: []}).items())[:1]:", 1)],
     (rows_hooks,), {"hooks-top"}, False),
    ("the hooks' copy finds the repository's own tool from each project's root", "tree_tool_dir", [("return top / tool if tool else top", "return ROOT / tool if tool else ROOT", 1)],
     (rows_hooks,), {"copy-tool"}, False),
    ("the pre-commit hook's run in a code repository whose trackers live elsewhere judges as anywhere", "elsewhere_run",
     [('if operation == "check" or args.print_written:', 'if operation == "check":', 1)], (rows_after_move,), {"elsewhere-hook"}, False),
    ("the hooks' copy exits with the last project's run, not the first refusal", "copy:each_project",
     [("code = code or got or EXIT_OK", "code = got or EXIT_OK", 1)], (rows_hooks,), {"hooks-first"}, False),
    ("the hooks' copy passes a project whose configuration is refused", "copy:each_project",
     [("got = stop.code if isinstance(stop.code, int) else 0 if stop.code is None else 1", "got = 0", 1)], (rows_hooks,), {"hooks-config"}, False),
    ("`--each-project` taken with any other flag", "each_project", [("if alone is None or any(", "if alone is None and any(", 1)],
     (rows_hooks,), {"each-alone"}, False),
    ("the drift line said once for each project, in the hooks' copy", "copy:main_run", [("if drift and drift not in _DRIFT_SAID:", "if drift:", 1)],
     (rows_hooks,), {"drift-once"}, False),
    ("the hooks' copy reads the staged names with renames", "copy:each_project",
     [('"diff", "--cached", "-z", "--name-only", "--no-renames", "--ignore-submodules=none", cwd=top',
       '"diff", "--cached", "-z", "--name-only", "--ignore-submodules=none", cwd=top', 1)], (rows_hooks,), {"hooks-moved-out"}, False),
    ("`--install-hook` from the vendored tool records the tool's folder from the project root, not the top", "tree:install_copy",
     [('here_rel = os.path.relpath(HERE, top).replace(os.sep, "/") if inside else "-"',
       'here_rel = os.path.relpath(HERE, ROOT).replace(os.sep, "/") if in_tree(HERE) else "-"', 1)], (rows_command,), {"command-from-below"}, False),
    ("the hooks' copy takes a `tool:` folder that climbs out of the working tree", "copy:copy_tool_folder",
     [(' or ".." in tool.split("/")', '', 1)], (rows_command,), {"command-copy-outside"}, False),
    ("the hooks' copy takes a project HEAD holds but the working tree lacks", "copy:staged_projects",
     [("if os.path.lexists(top.joinpath(*parts[:n], CONFIG_NAME))", "if True", 1)], (rows_hooks,), {"hooks-config-out"}, False),
    ("the hooks' copy says a project's lines below the top without its folder", "copy:each_project",
     [("with lines_named(folder[:-1]):              # each line", 'with lines_named(""):              # each line', 1)], (rows_hooks,),
     {"hooks-named"}, False),
    ("the hooks' copy says a project's refused configuration below the top without its folder", "copy:each_project",
     [("with lines_named(folder[:-1]):\n                    print(stop.code, file=sys.stderr)", "if True:\n                    print(stop.code, file=sys.stderr)", 1)],
     (rows_hooks,), {"hooks-named"}, False),
    ("the hooks' copy names a line's project without its folder", "copy:_Named",
     [('self.out.write(f"{self.name}: {one}\\n" if one else "\\n")', 'self.out.write(f"{one}\\n")', 1)], (rows_hooks,), {"hooks-named"}, False),
    ("the hooks' copy names what it wrote from the project root, where the hook stages from the top", "copy:each_project",
     [('folder = "" if root == top else root.relative_to(top).as_posix() + "/"', 'folder = ""', 1)], (rows_hooks,), {"hooks-below"}, False),
    ("a new project decided on disk, not at the commit's parent, in the check", "other_project_changes",
     [("held.get(spec(rev, home)) is not None", "True", 1)], (rows_new_project,), {"import-owner", "import-seat"}, False),
    ("the hooks' copy, judging the commit being made, decides a new project in the index, not at HEAD", "copy:other_project_changes",
     [('parent = lambda rev: f"{rev}^" if rev else "HEAD"', 'parent = lambda rev: f"{rev}^" if rev else ""', 1),
      ("held = project_blobs(sorted({spec(r, h) for r, h in asked}))", "held = project_blobs(sorted({spec(r, h) for r, h in asked}), index_env())", 1)],
     (rows_new_project,), {"import-seat", "import-side", "re-created-hooks"}, False),
    ("a new project decided at the commit itself, not at its parent, in the check", "other_project_changes",
     [('parent = lambda rev: f"{rev}^" if rev else "HEAD"', 'parent = lambda rev: rev or "HEAD"', 1)], (rows_new_project,),
     {"import-two", "import-side", "re-created"}, False),
    ("the hooks' copy reads a new project's `shoalmark.toml` from the index, not from HEAD", "copy:staged_projects",
     [('spec = lambda folder: f"HEAD:{folder}/{CONFIG_NAME}"', 'spec = lambda folder: f":{folder}/{CONFIG_NAME}"', 1),
      ("held = project_blobs([spec(folder) for folder in on_disk]) if on_disk else {}",
       "held = project_blobs([spec(folder) for folder in on_disk], index_env()) if on_disk else {}", 1)],
     (rows_new_project,), {"import-owner", "import-seat", "import-side", "re-created-hooks"}, False),
    ("the hooks' copy decides a new project on disk, not at HEAD", "copy:staged_projects",
     [("projects = {folder for folder in on_disk if held.get(spec(folder)) is not None}", "projects = set(on_disk)", 1)],
     (rows_new_project,), {"import-two", "import-side"}, False),
    ("the project at the top decided at the parent too, as if it were a project below itself", "other_project_changes",
     [("if f.parts and os.path.lexists(ROOT / f / CONFIG_NAME)]", "if os.path.lexists(ROOT / f / CONFIG_NAME)]", 1),
      ('spec = lambda rev, home: f"{parent(rev)}:./{home}/{CONFIG_NAME}"', 'spec = lambda rev, home: f"{parent(rev)}:./{home}/{CONFIG_NAME}".replace("/./", "/")', 1)],
     (rows_new_project,), {"top-created", "re-created"}, False),
    ("another project taken whatever its `shoalmark.toml` is, a file or not, with or without its tracker folder", "project_blobs",
     [('if _rev == rev and modes.get(path) in ("100644", "100755") and modes.get(folder) == "040000" and path in landed:', "if _rev == rev and path in landed:", 1),
      ('if got.get(spec) is not None and types.get(spec, "blob") == "blob" else None', "if got.get(spec) is not None else {}", 1)],
     (rows_other_project, rows_new_project), {"nested", "tracker-out"}, False),
    ("another project taken whatever configuration its `shoalmark.toml` holds", "project_blobs",
     [("cfg = config_accepted(got[spec], path[:-len(CONFIG_NAME)])", "cfg = read_config(got[spec])", 1)], (rows_other_project,), {"nested"}, False),
    ("the hooks' copy takes a folder for another project whatever its `shoalmark.toml` is, with or without its tracker folder", "copy:project_blobs",
     [('if _rev == rev and modes.get(path) in ("100644", "100755") and modes.get(folder) == "040000" and path in landed:', "if _rev == rev and path in landed:", 1),
      ('if got.get(spec) is not None and types.get(spec, "blob") == "blob" else None', "if got.get(spec) is not None else {}", 1)],
     (rows_hooks, rows_new_project), {"hooks-nested", "tracker-out-hooks"}, False),
    ("another project taken before the default branch holds its configuration", "project_blobs",
     [(' and path in landed:', ':', 1)], (rows_new_project,), {"self-named", "amended"}, False),
    ("the hooks' copy takes another project before the default branch holds its configuration", "copy:project_blobs",
     [(' and path in landed:', ':', 1)], (rows_new_project,), {"self-named-hooks", "amended"}, False),
    ("the default branch's configuration of another project taken whatever it holds", "landed_projects",
     [(' and config_accepted(got[f"{trunk}:{path}"], path[:-len(CONFIG_NAME)]) is not None}', '}', 1)], (rows_new_project,), {"landed-refused"}, False),
    ("a project the default branch holds is taken for none", "landed_projects", [("return {path for path in paths if", "return {path for path in () if", 1)],
     (rows_new_project,), {"landed"}, False),
    ("the build gate's commits listed with renames", "commit_list", [('"--name-only", "--no-renames", "--ignore-submodules=none"', '"--name-only", "--ignore-submodules=none"', 1)],
     (rows_other_project,), {"moved-in", "moved-out"}, False),
    ("the branch's commits walked with renames", "read_changes",
     [('"--relative", "--name-only", "--no-renames", "--ignore-submodules=none", f"--format=', '"--relative", "--name-only", "--ignore-submodules=none", f"--format=', 1)],
     (rows_other_project,), {"moved-session-below"}, False),
    ("the commit at HEAD read against its parents with renames", "read_changes",
     [('"diff", "-z", "--name-only", "--no-renames", "--relative", "--ignore-submodules=none", parent, "HEAD"',
       '"diff", "-z", "--name-only", "--relative", "--ignore-submodules=none", parent, "HEAD"', 1)], (rows_other_project,), {"moved-session"}, False),
    ("the commit being made's names read with renames by the commit-msg check, in the hooks' copy", "copy:pending_judgement",
     [('"diff", "--cached", "--name-only", "--no-renames", "--relative"', '"diff", "--cached", "--name-only", "--relative"', 1)], (rows_hooks,), {"hooks-moved"}, False),
    ("the merge being made read against each merge head with renames, in the hooks' copy", "copy:read_changes",
     [('"diff", "-z", "--cached", "--name-only", "--no-renames", "--relative", "--ignore-submodules=none", h',
       '"diff", "-z", "--cached", "--name-only", "--relative", "--ignore-submodules=none", h', 1)], (rows_hooks,), {"hooks-merge-moved"}, False),
    ("the working tree's edits read with renames", "worktree_edits",
     [('"diff", "-z", "--name-only", "--no-renames", "--relative", "--ignore-submodules=dirty", rev',
       '"diff", "-z", "--name-only", "--relative", "--ignore-submodules=dirty", rev', 1)], (rows_other_project,), {"moved-session-staged"}, False),
    ("a `<repository>@<commit>` row counted as no commit, though `[repositories]` names its repository", "code_row_verdicts",
     [('"" if name in named else', '"" if False else', 1)], (rows_after_move,), {"code-named"}, False),
    ("a `<repository>@<commit>` row taken whatever repository it names", "code_row_verdicts", [('"" if name in named else', '"" if True else', 1)],
     (rows_after_move,), {"code-not-named"}, False),
    ("a `<repository>@<commit>` row's hash read as a commit of this repository", "ship_problems",
     [('names = commits_named(CODE_ROW_RE.sub(" ", rows))', "names = commits_named(rows)", 1)], (rows_after_move,), {"code-not-named"}, False),
    ("`--check` says no line of the moves that rest on such a row", "code_rows_report", [("if not named:", "if True:", 1)], (rows_after_move,),
     {"code-line"}, False),
    ("a move with this repository's commit behind it counted as resting on the other's", "ship_problems",
     [('if "" in verdicts.values():\n                continue\n', 'if "" in verdicts.values() and "" not in code.values():\n                continue\n', 1)],
     (rows_after_move,), {"code-line"}, False),
    ("`--check` in a code repository whose trackers live elsewhere judges as anywhere", "elsewhere_run",
     [('if operation == "check" or args.print_written:', "if False:", 1)], (rows_after_move,), {"elsewhere-check"}, False),
    ("`--init` in such a repository runs as anywhere", "elsewhere_run", [('if operation in ("init", "new", "write"):', 'if operation in ("new", "write"):', 1)],
     (rows_after_move,), {"elsewhere-init"}, False),
    ("`--new` in such a repository files the tracker here", "elsewhere_run",
     [('if operation in ("init", "new", "write"):', 'if operation in ("init", "write"):', 1)], (rows_after_move,), {"elsewhere-new"}, False),
    ("the board's own run, in such a repository, builds the board here", "board_run", [("        if trackers_elsewhere():", "        if False:", 1)],
     (rows_after_move,), {"elsewhere-board"}, False),
    ("the run that writes INDEX.md and the board, in such a repository, writes them here", "elsewhere_run",
     [('if operation in ("init", "new", "write"):', 'if operation in ("init", "new"):', 1)], (rows_after_move,), {"elsewhere-board"}, False),
    ("the build gate on in such a repository, where its configuration turns it on", "commit_msg_check",
     [('if not CONFIG.get("judged_before_build") or vcs() != "git" or trackers_elsewhere():', 'if not CONFIG.get("judged_before_build") or vcs() != "git":', 1)],
     (rows_after_move,), {"elsewhere-gate"}, False),
    ("`[trackers] elsewhere` read from this checkout's configuration, not the default branch's", "trackers_elsewhere",
     [('named = elsewhere_named((landed_config() or {}).get("trackers"))', 'named = elsewhere_named(CONFIG.get("trackers"))', 1)],
     (rows_after_move,), {"elsewhere-branch-code", "elsewhere-unread"}, False),
    ("`[trackers] elsewhere` taken where the project holds a tracker folder", "code_config_problem",
     [('held = tracker_folder_held() if section is not None else ""', 'held = ""', 1)], (rows_after_move,), {"elsewhere-branch"}, False),
    ("`[trackers]` read from the default branch where this checkout's configuration holds none", "trackers_elsewhere",
     [('if CONFIG.get("trackers") is None:\n        return ""', 'if False:\n        return ""', 1)], (rows_after_move,), {"elsewhere-removed"}, False),
    ("a state of the default branch read where its tip holds neither table", "landed_config",
     [('if tip and ("trackers" in tip or "repositories" in tip):', "if tip:", 1)], (rows_after_move,), {"elsewhere-tip-out"}, False),
    ("`[repositories]` read from this checkout's configuration, not the default branch's", "landed_repositories",
     [('theirs = (landed_config() or {}).get("repositories") if mine else None', "theirs = mine", 1)], (rows_after_move,),
     {"code-branch", "code-unread"}, False),
    ("a ship-log row's repository counted as this checkout's configuration names it", "code_row_verdicts",
     [("named = landed_repositories()", 'named = CONFIG.get("repositories") or {}', 1)], (rows_after_move,), {"code-branch", "code-unread"}, False),
    ("`--check`'s line on rows resting on a code repository counts this checkout's `[repositories]`", "code_rows_report",
     [("named = landed_repositories()", 'named = CONFIG.get("repositories")', 1)], (rows_after_move,), {"code-branch"}, False),
    ("the default branch's tracker folder not looked at", "tracker_folder_held",
     [('if path_mode(trunk, root_prefix() + folder) not in ("", "?"):', "if False:", 1)], (rows_after_move,), {"elsewhere-folder-landed"}, False),
    ("the tool named by its absolute path again where it lies outside the project root, in the root's working tree", "tree:tool_named",
     [("if inside(ROOT) or inside(top):", "if inside(ROOT):", 1)], (rows_command,), {"command-below", "command-import"}, False),
    ("the hooks' copy names a project that keeps its own tool by the top's tool", "copy:configure",
     [('CMD_OWN.startswith(PY + " ") and not root_holds_tool(CMD_OWN[len(PY) + 1:]):', 'CMD_OWN.startswith(PY + " "):', 1)], (rows_command,),
     {"command-own"}, False),
    ("the hooks' copy keeps the recorded command for every project", "copy:root_holds_tool",
     [("return in_tree(path) and os.path.isfile(path)", "return True", 1)], (rows_command,), {"command-below"}, False),
    ("the hooks' copy names the command `--install-hook` recorded, from the top, for a project below it", "copy:configure",
     [('CMD_OWN = PY + " " + tool_named(_VCS[1] / folder / pathlib.Path(__file__).name)', "pass", 1)], (rows_command,), {"command-below"}, False),
)


@contextlib.contextmanager
def mutated(name, pairs):
    """`fm.<name>` replaced by a patched copy of its own source, compiled in the module's namespace — and put back after. A table of the
    module's (a dict of tuples of words) is patched in its words instead, value by value."""
    if name.startswith(("copy:", "tree:")):                         # the hooks' copy, and the tool a row keeps in its repository, run in a process of their own:
        held = _COPY if name.startswith("copy:") else _TREE         # their file carries the mutant (`install_once`, `org_tools`; `vendored`)
        src, whole = textwrap.dedent(inspect.getsource(getattr(fm, name[5:]))), Path(fm.__file__).read_text(encoding="utf-8")
        for old, new, count in pairs:
            if src.count(old) != count or whole.count(old) != count:
                raise AssertionError(f"{name}: {old[:60]!r} is in its source {src.count(old)} times and in the tool {whole.count(old)}, not {count}")
            whole = whole.replace(old, new)
        held["source"] = whole
        try:
            yield
        finally:
            held["source"] = None
        return
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
