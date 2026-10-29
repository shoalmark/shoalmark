"""R9's class test — the ruling signed on 2026-10-12: invites, notifications and their scheduler state go; owed acts, `due:`,
`done:` and their signed history stay.

- Each removed flag — `--invite <id>`, `--notify`, `--standup FILE.ics` — says so in one line, exits 2 and writes nothing.
- What they left — a calendar file `--invite` or `--standup FILE.ics` wrote (one the base itself wrote below the root among
  them), the state `--notify` kept, the log of the README's cron line, the README's launchd agent and its log — is named by
  `--standup` and `--owner`, each piece, and stays byte for byte as it was: nothing is removed, nothing is added. A calendar
  file of a person's own, at the top or nested, and one reached through a symlinked file or folder, are not named.
- `--standup`, `--owner`, `--due` and `--done` print, on a fixture with nothing left over, what they printed at 36d4961, the
  tool R9 joins in PR B (the d-batch's head), and `--due` and `--done` write the same record.
- The acts are compared as they are said now that each commits on the branch the Owner stands on and pushes nothing, where the
  base cut `answer/<id>` and pushed it.

Run: `python3 test_r9_removals.py` — exit 1 on a failure. `SHOALMARK_R9_TOOL=<path>` runs it against another copy of the tool:
that is how its mutants are run (a leftover deleted; a leftover not named), and each must fail it. test_shoalmark.py runs it at
its end. No browser, no network: every repository is a scratch one, `origin` a bare one beside it.
"""

import datetime
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile


HERE = Path(__file__).resolve().parent
BASE = "36d4961"                    # the tool R9 joins in PR B: the d-batch's head, before R9 as b84b8af was, which R9 was built on
FM054_SAID = ("\n  signed, on `answer/", "\n  author only, on `answer/")
# an act commits on the branch the Owner stands on and pushes nothing — the base's cut, push and switch back, as the joined tool says each
R4_SAID = (re.compile(r"\n  author only, on `answer/[a-z0-9-]+`, pushed\n"),
           "\n  author only, committed on `main` as <SHA>\n  it counts once this commit is on origin/main: push it, or merge the branch that carries it\n")
R4_STEPS = ((re.compile(r" — 1/4 reading the trackers"), " — 1/3 reading the trackers"),
            (re.compile(r" — 2/4 cutting `answer/[a-z0-9-]+` from `main` …\n"), None),
            (re.compile(r" — 3/4 committing"), " — 3/3 committing"),
            (re.compile(r"[^\n]* — 4/4 pushing to `origin` …\n"), ""))


FM053_AGENDA = (("\nRULINGS — ", "\nDECISIONS — "), ("\nBUTTONS — ", "\nONE CLICK — "))
# the board reads no answer branch: the base's line that the board was older than what it shows, where the answer branches alone had changed
R4_BASIS = re.compile(r"\nthe board is older than what it shows — the answer branches changed since it was built: `[^`\n]*` rebuilds it\n\Z")


def as_proved(entry):
    """A base run's (flag, exit, stdout, stderr) as the joined tool says it: for `--due` and `--done`, the one line naming how the commit is
    proved, once; for `--standup`, the two kinds the board renames; for `--standup` and `--owner`, the line naming the answer branches alone
    as what changed since the board was built, which the board no longer reads; anything else as it was."""
    if entry[0] in ("--standup", "--owner") and isinstance(entry[2], str):
        out = R4_BASIS.sub("", entry[2], count=1)
        for old, new in FM053_AGENDA if entry[0] == "--standup" else ():
            out = out.replace(old, new) if out.count(old) == 1 else out
        return entry[:2] + (out,) + entry[3:]
    if entry[0] not in ("--due", "--done") or not isinstance(entry[2], str) or entry[2].count(FM054_SAID[0]) != 1:
        return entry
    out = R4_SAID[0].sub(R4_SAID[1], entry[2].replace(*FM054_SAID), count=1)
    out = out.replace("\n  back on `main`\n", "\n").replace("the board is rebuilt — it reads the branch just pushed", "the board is rebuilt")
    err, tid = entry[3], entry[4]
    for rx, new in R4_STEPS:
        err = rx.sub(new if new is not None else f" — 2/3 writing docs/work-tracker/{tid}-x.md on `main` …\n", err, count=1)
    return entry[:2] + (out, err) + entry[4:]
OWNER = "owner@example.invalid"
REMOVED = (("--invite", ["--invite", "AP-001"]), ("--notify", ["--notify"]), ("--standup FILE.ics", ["--standup", "cal.ics"]))
ACT_ICS = (b"BEGIN:VCALENDAR\r\nVERSION:2.0\r\nPRODID:-//shoalmark//act//EN\r\nBEGIN:VEVENT\r\nUID:act-ap-001-0000000000000000@shoalmark\r\n"
           b"SUMMARY:r9 \xe2\x80\x94 AP-001: the read\r\nEND:VEVENT\r\nEND:VCALENDAR\r\n")
STANDUP_ICS = (b"BEGIN:VCALENDAR\r\nVERSION:2.0\r\nPRODID:-//shoalmark//standup//EN\r\nBEGIN:VEVENT\r\n"
               b"RRULE:FREQ=WEEKLY;BYDAY=MO,TU,WE,TH,FR\r\nEND:VEVENT\r\nEND:VCALENDAR\r\n")
OWN_ICS = b"BEGIN:VCALENDAR\r\nVERSION:2.0\r\nPRODID:-//someone else//EN\r\nEND:VCALENDAR\r\n"


def write(path, text):
    """A fixture file in UTF-8 with `\\n` line ends on every system (`Path.write_text` takes `newline` only from 3.10)."""
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)


def tool_path():
    return Path(os.environ.get("SHOALMARK_R9_TOOL") or HERE / "shoalmark.py").resolve()


def environment(home, xdg=None):
    """A run's environment: this process's, without git's own variables and any state folder, with `home` as every system's home."""
    env = {k: v for k, v in os.environ.items() if not k.startswith(("GIT_", "SHOALMARK_")) and k not in ("XDG_STATE_HOME", "LOCALAPPDATA")}
    env.update(HOME=str(home), USERPROFILE=str(home), LOCALAPPDATA=str(home / "AppData" / "Local"), GIT_CONFIG_GLOBAL=os.devnull,
               GIT_CONFIG_NOSYSTEM="1", GIT_TERMINAL_PROMPT="0", SHOALMARK_CMD="shoalmark", PYTHONIOENCODING="utf-8")
    if xdg:
        env["XDG_STATE_HOME"] = str(xdg)
    return env


def run(tool, root, env, *argv):
    r = subprocess.run([sys.executable, str(tool), "--root", str(root), *argv], cwd=str(root), capture_output=True, text=True,
                       encoding="utf-8", errors="replace", env=env, timeout=300)
    return r.returncode, r.stdout, r.stderr


def git(cwd, *a, env, dated=False):
    if dated:                                                    # the fixture's own commits: the same bytes, so the same shas, in each copy
        env = dict(env, GIT_AUTHOR_DATE="2026-10-14T08:00:00+00:00", GIT_COMMITTER_DATE="2026-10-14T08:00:00+00:00")
    return subprocess.run(["git", *a], cwd=str(cwd), capture_output=True, text=True, encoding="utf-8", errors="replace", env=env, check=True).stdout


def tracker(root, tid, extra, title):
    d = root / "docs" / "work-tracker"
    d.mkdir(parents=True, exist_ok=True)
    write(d / f"{tid}-x.md", f'---\nid: {tid}\nstatus: In Progress\nconsidered: none\n{extra}hook: "h of {tid}"\n---\n\n# {tid} — {title}\n\n'
                             "## What is true now\n\n**One thing is left.**\n\n## Done when\n\nit is.\n")


def fixture(base, tool, env, clock):
    """A repository with acts owed to the Owner and one open ruling, committed and pushed to a bare `origin`: the board built by `tool`."""
    root, origin = base / "wc", base / "origin.git"
    root.mkdir(parents=True)
    git(base, "init", "-q", "--bare", str(origin), env=env)
    git(root, "init", "-q", env=env)
    git(root, "symbolic-ref", "HEAD", "refs/heads/main", env=env)
    for k, v in (("user.name", "owner"), ("user.email", OWNER), ("commit.gpgsign", "false"), ("core.autocrlf", "false")):
        git(root, "config", k, v, env=env)
    git(root, "remote", "add", "origin", str(origin), env=env)
    write(root / "shoalmark.toml", f'name = "r9"\nowner = "{OWNER}"\nstandup = "09:00"\n[kinds]\nAP = "Work"\n')
    write(root / ".gitignore", "docs/work-tracker/index.html\ndocs/work-tracker/view/\n")
    since, at = clock
    ask = lambda q, answer: (f'next: owner\nask: "{q}"\nask-kind: action\nask-since: {since}\nask-proposal: "yes"\n'
                             f'answer: "{answer}"\nanswered: {since}\nanswered-by: owner\n')
    tracker(root, "AP-001", ask("Will you read production at seven?", "accepted - at seven") + f"due: {at(60)}\n", "the read")
    tracker(root, "AP-002", f"next: run\ndue: {at(-10)}\n", "the overdue run")
    tracker(root, "AP-003", f'next: owner\nask: "Shall the launcher ship first?"\nask-kind: ruling\nask-since: {since}\nask-proposal: "the launcher"\n', "a ruling")
    tracker(root, "AP-004", ask("Will you set up the key?", "accepted - this week"), "the key")
    (root / "docs/work-tracker/evidence/AP-001").mkdir(parents=True)
    write(root / "docs/work-tracker/evidence/AP-001/read.md", "the read, done\n")
    run(tool, root, env)                                         # INDEX.md and the board, as this tool writes them
    git(root, "add", "-A", env=env)
    git(root, "commit", "-qm", "the acts", env=env, dated=True)
    git(root, "push", "-q", "-u", "origin", "HEAD:main", env=env)
    git(root, "remote", "set-head", "origin", "main", env=env)
    return root


def normal(text, base):
    """A run's words with what differs between two copies of one fixture taken out: the folder, a commit's sha, a time of day."""
    for p in sorted({str(base), base.as_posix(), str(base.resolve()), base.resolve().as_posix()}, key=len, reverse=True):
        text = text.replace(p, "<BASE>")
    text = re.sub(r"\b[0-9a-f]{7,40}\b", "<SHA>", text)
    text = re.sub(r"\d{4}-\d{2}-\d{2}[T ]\d{2}:\d{2}(?::\d{2})?(?:Z|[+-]\d{2}:?\d{2})?", "<TIME>", text)
    return re.sub(r"\b\d{2}:\d{2}(?::\d{2})?\b", "<CLOCK>", text)


def snapshot(*folders):
    """Every file under each folder, by its path, with its bytes — a symlink as where it points."""
    seen = {}
    for folder in folders:
        for dirpath, dirnames, filenames in os.walk(folder):
            if ".git" in dirnames:
                dirnames.remove(".git")
            for name in filenames + [d for d in dirnames if os.path.islink(os.path.join(dirpath, d))]:
                p = os.path.join(dirpath, name)
                seen[p] = ("->", os.readlink(p)) if os.path.islink(p) else Path(p).read_bytes()
    return seen


def can_symlink(where):
    try:
        os.symlink(where / "nowhere", where / "probe")
        os.unlink(where / "probe")
        return True
    except (OSError, NotImplementedError):
        return False


def base_tool(area, env):
    """The tool at BASE, beside its renderer and VERSION, in `area/old-tool` — or None where this clone does not hold BASE."""
    shown = subprocess.run(["git", "-C", str(HERE), "show", f"{BASE}:shoalmark.py"], capture_output=True, env=env)
    if shown.returncode != 0:
        return None
    old = area / "old-tool"
    (old / "vendor").mkdir(parents=True)
    (old / "shoalmark.py").write_bytes(shown.stdout)
    for f in (HERE / "vendor").glob("marked-*.js"):
        shutil.copy(f, old / "vendor" / f.name)
    shutil.copy(HERE / "VERSION", old / "VERSION")
    return old / "shoalmark.py"


def leftovers(root, home, xdg, away, base=None, env=None):
    """What invites and notifications left, as the tool wrote it or the README told a person to add it: {path: as `--standup` names it},
    and with `base`, the stand-up's calendar the base itself writes below the root, `--standup calendar/agenda.ics`. Beside them, what is not
    the tool's: a person's own calendar files, at the top and nested, and the tool's calendars reached through a symlink to a file and
    through a symlinked folder (`away`). Returns (shown, the symlinked file or None, whether the base wrote its calendar, or None without it)."""
    left = {
        root / "docs/work-tracker/evidence/AP-001/AP-001-act.ics": ACT_ICS,
        root / "standup.ics": STANDUP_ICS,
        home / ".local/state/shoalmark/notified.json": b'{\n "/somewhere/else": [\n  "AP-1 2026-10-01T09:00:00+02:00 missed"\n ]\n}\n',
        home / ".local/state/shoalmark/notify.log": b"--notify: 0 posted \xc2\xb7 1 posted before\n",
        xdg / "shoalmark/notified.json": b"{}\n",
        home / "Library/LaunchAgents/app.shoalmark.notify.plist": b'<plist version="1.0"><dict><key>Label</key><string>app.shoalmark.notify</string></dict></plist>\n',
        home / "Library/Logs/shoalmark-notify.log": b"--notify: 1 posted\n",
    }
    for p, data in left.items():
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_bytes(data)
    (root / "mine.ics").write_bytes(OWN_ICS)
    (root / "notes/deep").mkdir(parents=True)
    (root / "notes/deep/mine-too.ics").write_bytes(OWN_ICS)
    wrote = None
    if base:
        (root / "calendar").mkdir()
        code, _o, _e = run(base, root, env, "--standup", "calendar/agenda.ics")
        nested = root / "calendar/agenda.ics"
        wrote = code == 0 and nested.is_file() and nested.read_bytes().startswith(b"BEGIN:VCALENDAR\r\nVERSION:2.0\r\nPRODID:-//shoalmark//standup//EN\r\n")
        if nested.is_file():
            left[nested] = nested.read_bytes()
    linked = None
    if can_symlink(away):
        (away / "AP-004-act.ics").write_bytes(ACT_ICS)
        (root / "docs/work-tracker/evidence/AP-004").mkdir(parents=True, exist_ok=True)
        linked = root / "docs/work-tracker/evidence/AP-004/AP-004-act.ics"
        os.symlink(away / "AP-004-act.ics", linked)
        (away / "elsewhere").mkdir()
        (away / "elsewhere/agenda.ics").write_bytes(STANDUP_ICS)
        os.symlink(away / "elsewhere", root / "linked-folder", target_is_directory=True)
    shown = {p: (p.relative_to(root).as_posix() if root in p.parents else str(p)) for p in left}
    return shown, linked, wrote


def run_checks(*, results=None):
    """[(label, ok, detail)] — ok None where a part cannot run here, with why."""
    tool = tool_path()
    results = [] if results is None else results
    add = lambda label, ok, detail="": results.append((label, ok, detail))
    now = datetime.datetime.now(datetime.timezone.utc).astimezone().replace(microsecond=0)
    clock = ((datetime.date.today() - datetime.timedelta(days=1)).isoformat(), lambda minutes: (now + datetime.timedelta(minutes=minutes)).isoformat())
    with tempfile.TemporaryDirectory(prefix="shoalmark-r9-") as tmp:
        area = Path(tmp).resolve()
        home, xdg, away = area / "home", area / "xdg", area / "away"
        for d in (home, xdg, away):
            d.mkdir()
        env = environment(home)
        root = fixture(area / "now", tool, env, clock)
        old = base_tool(area, env)                               # the base's own tool: it writes the nested calendar, and part 3 compares with it

        # 1. each removed flag: one line, exit 2, nothing written — in a clean home, and where leftovers are
        before = snapshot(root, home)
        for flag, argv in REMOVED:
            code, out, err = run(tool, root, env, *argv)
            lines = err.splitlines()
            add(f"R9 · {flag} says in one line that R9 removed it, names what lists the acts now, and exits 2; it writes nothing (saw exit {code}, {err.strip()[:160]!r})",
                code == 2 and out == "" and len(lines) == 1 and lines[0].startswith(f"{flag}: removed by R9 — ") and "`--standup`" in lines[0]
                and "`--owner`" in lines[0] and snapshot(root, home) == before and not (root / "cal.ics").exists())
        shown, linked, wrote = leftovers(root, home, xdg, away, old, env)
        before = snapshot(root, home, xdg, away)
        if wrote is None:
            add(f"R9 · the stand-up's calendar {BASE} writes below the root", None, f"this clone does not hold {BASE}")
        else:
            add(f"R9 · the fixture's nested leftover: {BASE} itself writes `--standup calendar/agenda.ics`, a stand-up calendar below the root", wrote)

        # 2. the leftovers: each named by `--standup` and `--owner`, byte for byte as it was, nothing added or removed — with and without XDG_STATE_HOME
        for label, run_env, named in (("XDG_STATE_HOME unset", env, [p for p in shown if xdg not in p.parents]),
                                      ("XDG_STATE_HOME set", environment(home, xdg), list(shown))):
            for argv in (["--standup"], ["--owner"]):
                code, out, err = run(tool, root, run_env, *argv)
                block = out[out.find("LEFT BY INVITES AND NOTIFICATIONS"):] if "LEFT BY INVITES AND NOTIFICATIONS" in out else ""
                missing = [shown[p] for p in named if f"  {shown[p]} — " not in block]
                add(f"R9 · {argv[0]} ({label}) names every leftover under its title — the calendar files `--invite` and `--standup FILE.ics` wrote, "
                    f"`notified.json`, the cron line's log, the launchd agent and its log — each with what to do (missing {missing})",
                    code == 0 and bool(block) and not missing and "`--standup` and `--owner` list each act owed with its time" in block)
                add(f"R9 · {argv[0]} ({label}) names no calendar file of a person's own, at the top or nested, and none reached through a symlinked "
                    f"file or folder",
                    "mine.ics" not in out and "mine-too.ics" not in out and "AP-004-act.ics" not in out and "linked-folder" not in out)
                add(f"R9 · after {argv[0]} ({label}) every leftover is byte for byte as it was, and nothing was added or removed beside it",
                    snapshot(root, home, xdg, away) == before, f"changed: {sorted(set(before) ^ set(snapshot(root, home, xdg, away)))[:4]}")
        for flag, argv in REMOVED:
            code, out, err = run(tool, root, env, *argv)
            add(f"R9 · {flag}, where leftovers are, still says only its one line, exit 2, and leaves each byte for byte",
                code == 2 and out == "" and len(err.splitlines()) == 1 and snapshot(root, home, xdg, away) == before)
        if linked is None:
            add("R9 · a calendar file reached through a symlink is not named", None, "this system makes no symlink here")

        # 3. on a fixture with nothing left over, `--standup`, `--owner`, `--due` and `--done` print what they printed at the base, and write the same record
        if old is None:
            add(f"R9 · `--standup`, `--owner`, `--due` and `--done` as at {BASE}", None, f"this clone does not hold {BASE}")
            return results
        clean = area / "clean-home"
        clean.mkdir()
        cenv = environment(clean)
        pair = {}
        for name, t in (("then", old), ("now", tool)):
            base = area / f"same-{name}"
            r = fixture(base, t, cenv, clock)
            # the base cut `answer/<id>` and pushed each act there, and its digests read those branches; this tool commits each act on `main`:
            # the digests before the acts are compared, the acts as this tool says them, and each record where each tool committed it
            seq = (["--standup"], ["--owner"], ["--due", "AP-002", clock[1](120)], ["--done", "AP-001", "evidence/AP-001/read.md"])
            got = [(argv[0],) + tuple(normal(x, base) if isinstance(x, str) else x for x in run(t, r, cenv, *argv)) + ((argv[1],) if argv[0] in ("--due", "--done") else ())
                   for argv in seq]
            got.append(("records",) + tuple(normal(git(r, "show", f"{f'origin/answer/{tid}' if name == 'then' else 'HEAD'}:docs/work-tracker/{tid.upper()}-x.md", env=cenv), base)
                                            for tid in ("ap-002", "ap-001")))
            pair[name] = got
        for a, b in zip(pair["then"], pair["now"]):
            a = as_proved(a)
            add(f"R9 · {a[0]} prints what it printed at {BASE} — exit, both streams" + (", its proof as FM-054 says it" if a[0] in ("--due", "--done") else
                                                                                         ", its kinds as A2 names them" if a[0] == "--standup" else "")
                if a[0] != "records" else f"R9 · `--due` and `--done` write the record they wrote at {BASE} — there on `answer/<id>`, here on `main`", a == b,
                "" if a == b else f"then {a!r}\nnow  {b!r}")
        acted = pair["now"][3]
        add("R9 · …and on that fixture `--done` did its act — the control that the comparison compared a run that worked",
            acted[1] == 0 and "AP-001" in acted[2] + acted[3], f"saw {acted!r}"[:300])
    return results


if __name__ == "__main__":
    failed = 0
    for label, ok, detail in run_checks():
        print(("  ok    " if ok else "  skip  " if ok is None else "  FAIL  ") + label + ("" if ok else f"\n        {detail}" if detail else ""))
        failed += ok is False
    print(f"FAILED: {failed}" if failed else "all green")
    sys.exit(1 if failed else 0)
