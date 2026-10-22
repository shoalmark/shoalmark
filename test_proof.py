"""FM-054's class table: how the Owner's answer is proved, said as the gate reads it. Run: `python3 test_proof.py`.

Every mode — `signed` or not on the default branch, and `signed` or not in this checkout — by every surface that says how
an answer, a `done:` or a `due:` is proved: the board's second screen line by line (its title, its intro, the commit step,
the end it previews, its check, where to go when it fails), the terminal's line after `--answer`, `--done`, `--due` and
`--revoke`, and whether `--answer` passes `-S`. *Signed* appears only where the default branch's configuration asks for it,
and `-S` is passed only there. Where the default branch asks for a signature this checkout does not, `--answer` says so in
one line; where this checkout asks for one its default branch does not, it is refused before anything changes, and every
answer it reports given passes `--check` on its branch. Two mutants —
a surface that reads this checkout's configuration, and `-S` decided from it — each fail the table.

Standalone, or staged from `test_shoalmark.py` (`run_proof_controls`). Every fixture is a throwaway repository.
"""

import contextlib
import io
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from unittest.mock import patch

HERE = Path(__file__).resolve().parent
ENV = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
OWNER, SEAT = ("holgo", "h@x"), ("seat", "s@x")
SIGNED_WORDS = re.compile(r"\bsign(ed)?\b|%G\?|touch|\bsigniert\b|signieren|Berührung", re.I)


def git(cwd, *a, author=SEAT):
    env = dict(ENV, GIT_AUTHOR_NAME=author[0], GIT_AUTHOR_EMAIL=author[1], GIT_COMMITTER_NAME=author[0], GIT_COMMITTER_EMAIL=author[1])
    return subprocess.run(["git", "-C", str(cwd), "-c", "commit.gpgsign=false", "-c", "core.hooksPath=/dev/null", *a],
                          check=True, capture_output=True, text=True, encoding="utf-8", env=env).stdout


def run(fm, root, *argv):
    """The tool in process, with no ambient `GIT_*` variable: (exit status, stdout, stderr)."""
    out, err = io.StringIO(), io.StringIO()
    saved = {k: os.environ.pop(k) for k in [k for k in os.environ if k.startswith("GIT_")]}
    try:
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            try:
                code = fm.main(["--root", str(root), *argv])
            except SystemExit as e:
                code = e.code if isinstance(e.code, int) else 0 if e.code is None else 1
                if not isinstance(e.code, int) and e.code is not None:
                    print(e.code, file=err)
    finally:
        os.environ.update(saved)
    return code, out.getvalue(), err.getvalue()


def config(owner):
    """The configuration with the Owner's line as given — `owner = "h@x signed"`, `owner = "h@x"`, or a refused one."""
    return f'owner = "{owner}"\nname = "p"\n[kinds]\nAP = "Work"\n[seats]\nplanner = "s@x"\n'


ASK = ('---\nid: AP-001\nstatus: In Progress\nconsidered: none\nnext: owner\nask: "Ship it?"\nask-kind: ruling\nask-since: 2026-10-01\n'
       'ask-proposal: "yes"\nhook: "h"\n---\n\n# AP-001 — the ask\n\n## What is true now\n\nOne thing is left.\n\n## Done when\n\nit is.\n')


def fixture(base, trunk, here):
    """A clone whose default branch, `origin/main`, names the Owner with `trunk` and whose branch `pd/001`, checked out, with
    `here` — the ask AP-001 waiting on both. The Owner's SSH key signs, and the signers file outside the clone lists it."""
    origin, root = base / "origin.git", base / "wc"
    subprocess.run(["git", "init", "-q", "--bare", str(origin)], check=True, env=ENV, capture_output=True)
    subprocess.run(["git", "init", "-q", str(root)], check=True, env=ENV, capture_output=True)
    git(root, "symbolic-ref", "HEAD", "refs/heads/main")
    key = base / "k"
    subprocess.run(["ssh-keygen", "-q", "-t", "ed25519", "-N", "", "-f", str(key)], check=True, capture_output=True)
    (base / "signers").write_text("h@x " + key.with_suffix(".pub").read_text(encoding="utf-8"), encoding="utf-8")
    for k, v in (("user.name", OWNER[0]), ("user.email", OWNER[1]), ("gpg.format", "ssh"), ("user.signingkey", str(key)),
                 ("gpg.ssh.allowedSignersFile", str(base / "signers")), ("commit.gpgsign", "false")):
        git(root, "config", k, v)
    git(root, "remote", "add", "origin", str(origin))
    (root / "shoalmark.toml").write_text(config(trunk), encoding="utf-8")
    (root / "docs/work-tracker").mkdir(parents=True)
    (root / "docs/work-tracker/AP-001-x.md").write_text(ASK, encoding="utf-8")
    git(root, "add", "-A")
    git(root, "commit", "-qm", "the ask")
    git(root, "push", "-q", "origin", "main")
    git(root, "remote", "set-head", "origin", "main")
    git(root, "checkout", "-q", "-b", "pd/001")
    if here != trunk:
        (root / "shoalmark.toml").write_text(config(here), encoding="utf-8")
        git(root, "commit", "-qam", "the branch's own owner line")
    return root


def page_proof(fm, root):
    """(the board's `PROOF`, as its run wrote it into the page, the run's exit status and stderr)."""
    code, _out, err = run(fm, root, "--html-only")
    page = (root / "docs/work-tracker/index.html").read_text(encoding="utf-8") if (root / "docs/work-tracker/index.html").is_file() else ""
    at = page.find(",PROOF=")
    return (json.JSONDecoder().raw_decode(page, at + len(",PROOF="))[0] if at >= 0 else None), code, err


def screen_lines(fm, proof, german):
    """Each line of the second screen that says how the commit is proved, as its labels read — English, and the German table
    the tool ships — with the end it previews and the check it names: {surface: text}."""
    out = {}
    for lang, labels in (("en", fm.LABELS), ("de", {**fm.LABELS, **german})):
        for surface, key in proof["keys"].items():
            out[f"{lang} {surface}"] = labels.get(key, "") if key else ""
        word = labels.get(proof["word"], "")              # FM-007: the proof line, before *accept* — the heading, the answer dialog, the consequence
        out[f"{lang} heading"] = labels.get("proof.here", "").replace("{0}", word)
        out[f"{lang} dialog"] = labels.get("proof.dialog", "").replace("{0}", word)
        out[f"{lang} consequence"] = labels.get(proof["why"], "") if proof["why"] else ""
    out["end"] = f"  {proof['said']}, on `answer/ap-001`, pushed" if proof["said"] else ""
    out["check"] = f"git log -1 --format={proof['format']} answer/ap-001" if proof["format"] else ""
    return out


def said_lines(fm, word):
    """The terminal's line after `--done`, `--due` and `--revoke`, as each command hands it to `owner_change` (`how["said"]`),
    given `word`: {command: text}. `--answer`'s own is read from its run."""
    t = {"id": "AP-001", "file": "AP-001-x.md", "title": "t", "status": "In Progress", "ask": "Ship it?", "ask_kind": "ruling",
         "next": "owner", "due": "2026-10-14T12:00Z"}
    got = {}
    with patch.object(fm, "vcs", return_value="git"), patch.object(fm, "result_facts", return_value=""), \
            patch.object(fm, "owner_change", side_effect=lambda _id, _t, how: got.setdefault(how["flag"], how) and 0), \
            patch.object(fm.subprocess, "run", return_value=subprocess.CompletedProcess([], 128, "", "")):
        fm.done_cmd(["AP-001", "the result"], [t])
        fm.due_cmd(["AP-001", "2026-10-14T12:00Z"], [t])
        fm.revoke_cmd(["AP-001", "the wrong result"], [{**t, "done": "2026-10-13T12:00Z · result"}])
    return {flag: how["said"]("answer/ap-001", ", pushed", word) for flag, how in got.items()}


def state(root):
    """What a refused `--answer` leaves as it found it: HEAD and the branch it is on, the tree (untracked files too), every
    tracker's bytes, every branch here, and origin's refs."""
    return {"HEAD": git(root, "rev-parse", "HEAD").strip(), "branch": git(root, "branch", "--show-current").strip(),
            "tree": git(root, "status", "--porcelain", "--untracked-files=all"),
            "trackers": {p.name: p.read_bytes() for p in sorted((root / "docs/work-tracker").glob("*.md"))},
            "branches": git(root, "for-each-ref", "--format=%(refname) %(objectname)", "refs/heads", "refs/remotes"),
            "remote": subprocess.run(["git", "--git-dir", str(root.parent / "origin.git"), "for-each-ref", "--format=%(refname) %(objectname)"],
                                     check=True, capture_output=True, text=True, encoding="utf-8", env=ENV).stdout}


def table(fm, rows=((True, True), (True, False), (False, True), (False, False))):
    """FM-054's table: for each (default branch signed, checkout signed), every surface — the page's state and its second
    screen's lines, `--answer`'s step and last line, its commit's signature, its one line where the two differ — against
    the default branch's reading alone. Where the checkout asks for a signature its default branch does not (RV-3309),
    `--answer` is refused before anything changes: HEAD, the trackers, the branches and the remote are as they were. Where it
    reports an answer given, `--check` on that answer's branch finds no signing or rights refusal. Returns every mismatch,
    as a line; [] where the table holds."""
    german = fm.read_flat((HERE / "examples/de/labels.yaml").read_text(encoding="utf-8"))
    bad = []
    for trunk_signed, here_signed in rows:
        name = f"origin/main {'signed' if trunk_signed else 'not signed'}, checkout {'signed' if here_signed else 'not signed'}"
        with tempfile.TemporaryDirectory() as tmp:
            root = fixture(Path(tmp).resolve(), "h@x signed" if trunk_signed else "h@x", "h@x signed" if here_signed else "h@x")
            want = "signed" if trunk_signed else "author"
            proof, code, err = page_proof(fm, root)
            if code != 0 or proof is None:
                bad.append(f"{name}: the board's run ended {code} with no PROOF ({err.strip()[-200:]!r})")
                continue
            if proof["state"] != want or proof["keys"] != fm.PROOF_KEYS[want]:
                bad.append(f"{name}: the page reads {proof['state']!r}, the default branch {want!r}")
            if proof["word"] != f"proof.{want}" or proof["why"] != ("proof.author.why" if want == "author" else ""):
                bad.append(f"{name}: the proof line reads {proof['word']!r}, its consequence {proof['why']!r}")
            lines = screen_lines(fm, proof, german)
            for surface, text in lines.items():
                if not trunk_signed and text and SIGNED_WORDS.search(text):
                    bad.append(f"{name}: the second screen's {surface} reads {text!r}")
            if trunk_signed and not (lines["end"].startswith("  signed, on") and "%G?" in lines["check"] and "signed" in lines["en commit"]
                                     and lines["en heading"] == "your answers here: signed" and lines["en dialog"] == "your answer here: signed"
                                     and not lines["en consequence"]):
                bad.append(f"{name}: the board does not say signed where origin/main asks for it ({lines['en heading']!r}, {lines['end']!r}, {lines['check']!r})")
            if not trunk_signed and not (lines["en heading"] == "your answers here: author only" and lines["en consequence"].startswith("an answer here proves the author only")):
                bad.append(f"{name}: the board's proof line reads {lines['en heading']!r} — {lines['en consequence']!r}")
            before = state(root)
            code, out, err = run(fm, root, "--answer", "AP-001", "accept")
            word = fm.PROOF_SAID[want]
            if here_signed and not trunk_signed:            # RV-3309: refused in the shared preflight, before any branch, switch or write
                after = state(root)
                if code != fm.EXIT_LINT or out or "the signing configuration must reach origin/main first" not in err or after != before:
                    bad.append(f"{name}: --answer was not refused before any change (exit {code}, said {out[:80]!r}, {err.strip()[-200:]!r}; "
                               f"changed: {[k for k in before if before[k] != after[k]]})")
            else:
                if code != 0 or not out.startswith(f"AP-001 answered: accepted\n  {word}, on `answer/ap-001`, pushed\n"):
                    bad.append(f"{name}: --answer ended {code} and said {out[:120]!r} ({err.strip()[-200:]!r})")
                if ("3/4 committing, signed" in err) != trunk_signed:
                    bad.append(f"{name}: --answer's commit step reads {[l for l in err.splitlines() if '3/4' in l]}")
                head = git(root, "cat-file", "commit", "refs/heads/answer/ap-001") if code == 0 else ""
                if ("\ngpgsig" in head) != trunk_signed:
                    bad.append(f"{name}: the answer's commit is {'signed' if 'gpgsig' in head else 'not signed'}")
                differs = [l for l in err.splitlines() if "and this checkout's does not" in l]
                if len(differs) != (trunk_signed and not here_signed) or (differs and not differs[0].rstrip().endswith("signed, as the gate reads origin/main")):
                    bad.append(f"{name}: the line where the checkout differs reads {differs}")
                if code == 0:                               # the answer it reports given passes the signing and rights checks on its branch
                    git(root, "switch", "-q", "answer/ap-001")
                    c2, _o2, e2 = run(fm, root, "--check")
                    git(root, "switch", "-q", "pd/001")
                    lint = [l.strip()[:160] for l in e2.splitlines() if "lint:" in l]
                    if c2 not in (0, fm.EXIT_DRIFT) or lint:     # drift: INDEX.md, which no hook here regenerates; any lint or refusal ends 4
                        said = lint or [l.strip()[:160] for l in e2.splitlines() if "refused" in l]
                        bad.append(f"{name}: the answer --answer reported pushed fails --check on its branch (exit {c2}: {said[:2]})")
            for flag, text in said_lines(fm, word).items():
                if f"\n  {word}, on `answer/ap-001`, pushed" not in text or (bool(SIGNED_WORDS.search(text)) != trunk_signed):
                    bad.append(f"{name}: {flag} would say {text[:120]!r}")
    return bad


def mutant_surface(fm):
    """Mutant 1: the page reads this checkout's configuration — `may_answer()` — for how an answer is proved."""
    real = fm.answer_proof

    def checkout_proof():
        if fm.vcs() != "git":
            return real()
        allowed = fm.may_answer()
        theirs = {w: m for w, m in allowed.items() if w in dict(fm.SEATS.get("owner") or [])} or allowed
        return "signed" if theirs and all(m == "signed" for m in theirs.values()) else "author"
    return patch.object(fm, "answer_proof", checkout_proof)


def mutant_sign(fm):
    """Mutant 2: `-S` decided from this checkout's configuration, as `--answer` decided it before FM-054."""
    def checkout_signing(name, email):
        hit = next((w for w, m in fm.may_answer().items() if m == "signed" and w in (email, name)), None)
        return hit is not None, hit, None, ""
    return patch.object(fm, "answer_signing", checkout_signing)


def other_backends(fm):
    """The page's state off git: the server's login on Subversion, no author with no version control — no `signed`, no
    preview, no check. Returns every mismatch."""
    bad = []
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp).resolve()
        (root / "shoalmark.toml").write_text(config("h@x"), encoding="utf-8")
        (root / "docs/work-tracker").mkdir(parents=True)
        (root / "docs/work-tracker/AP-001-x.md").write_text(ASK, encoding="utf-8")
        proof, code, err = page_proof(fm, root)
        if code != 0 or not proof or proof["state"] != "none" or proof["said"] or proof["format"] or proof["keys"] != fm.PROOF_KEYS["none"] \
                or proof["word"] != "proof.none" or proof["why"] or fm.LABELS["proof.none"] != "no author":
            bad.append(f"no version control: the page reads {proof} ({code}, {err.strip()[-160:]!r})")
    if shutil.which("svn") and shutil.which("svnadmin"):
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp).resolve()
            subprocess.run(["svnadmin", "create", str(base / "server")], check=True, capture_output=True)
            subprocess.run(["svn", "checkout", "-q", (base / "server").as_uri(), str(base / "wc")], check=True, capture_output=True)
            root = base / "wc"
            (root / "shoalmark.toml").write_text(config("h@x"), encoding="utf-8")
            (root / "docs/work-tracker").mkdir(parents=True)
            (root / "docs/work-tracker/AP-001-x.md").write_text(ASK, encoding="utf-8")
            subprocess.run(["svn", "add", "-q", "shoalmark.toml", "docs"], cwd=root, check=True, capture_output=True)
            subprocess.run(["svn", "commit", "-q", "-m", "the ask", "--username", "s@x"], cwd=root, check=True, capture_output=True)
            proof, code, err = page_proof(fm, root)
            if code != 0 or not proof or proof["state"] != "login" or proof["said"] or proof["format"] or proof["keys"] != fm.PROOF_KEYS["login"] \
                    or proof["word"] != "proof.login" or proof["why"] or fm.LABELS["proof.login"] != "server login":
                bad.append(f"Subversion: the page reads {proof} ({code}, {err.strip()[-160:]!r})")
    else:
        bad.append(None)                               # no svn here: said by the caller as a skip
    return bad


GIT_ONLY = (("--answer", ["AP-001", "accept"]), ("--done", ["AP-001", "the result"]), ("--due", ["AP-001", "2026-10-20T09:00:00+02:00"]),
            ("--revoke", ["AP-001", "the wrong result"]))


def git_only_refusals(fm):
    """RV-3310: off git — with no version control, and on Subversion — the four answer-branch commands are refused, as the command
    line runs them and as `owner_change`, the flow they share, refuses them itself: sixteen refusals. Each says the capability
    and the Subversion signature limitation in `CLI_GIT_ONLY`'s words, exits with its code, and never calls the branch signed.
    Returns (every mismatch, how many refusals were read); Subversion's eight are left out where svn is not installed."""
    bad, read = [], 0
    with tempfile.TemporaryDirectory() as tmp:
        base, roots = Path(tmp).resolve(), []
        plain = base / "plain"
        (plain / "docs/work-tracker").mkdir(parents=True)
        (plain / "shoalmark.toml").write_text(config("h@x"), encoding="utf-8")
        (plain / "docs/work-tracker/AP-001-x.md").write_text(ASK, encoding="utf-8")
        roots.append(("no version control", plain))
        if shutil.which("svn") and shutil.which("svnadmin"):
            subprocess.run(["svnadmin", "create", str(base / "server")], check=True, capture_output=True)
            subprocess.run(["svn", "checkout", "-q", (base / "server").as_uri(), str(base / "wc")], check=True, capture_output=True)
            (base / "wc/docs/work-tracker").mkdir(parents=True)
            (base / "wc/shoalmark.toml").write_text(config("h@x"), encoding="utf-8")
            (base / "wc/docs/work-tracker/AP-001-x.md").write_text(ASK, encoding="utf-8")
            subprocess.run(["svn", "add", "-q", "shoalmark.toml", "docs"], cwd=base / "wc", check=True, capture_output=True)
            subprocess.run(["svn", "commit", "-q", "-m", "the ask", "--username", "s@x"], cwd=base / "wc", check=True, capture_output=True)
            roots.append(("Subversion", base / "wc"))
        for where, root in roots:
            for flag, words in GIT_ONLY:
                said, code = fm.CLI_GIT_ONLY[flag[2:]]
                c1, _o1, e1 = run(fm, root, flag, *words)                       # the command line, as the Owner runs it
                fm.configure(root)
                e2 = io.StringIO()
                with contextlib.redirect_stderr(e2):
                    c2 = fm.owner_change("AP-001", {}, {"flag": flag})          # the shared flow's own refusal
                fm.configure(HERE)
                for how, c, err in (("the command line", c1, e1), ("owner_change", c2, e2.getvalue())):
                    read += 1
                    lines = [l for l in err.splitlines() if l.startswith(f"{flag}:")]      # on Subversion the line goes on with that backend's own limit
                    if (c != code or len(lines) != 1 or not (lines[0] == said or lines[0].startswith(said + " — Subversion: "))
                            or re.search(r"\bsigned\b", err) or f"{flag}: answer" not in said
                            or "require Git" not in said or "Subversion does not provide a commit signature" not in said):
                        bad.append(f"{where}, {flag}, {how}: exit {c}, said {err.strip()[-200:]!r}")
    return bad, read


def unread_row(fm):
    """The default branch's configuration refused here (a `signed` identity that is not an email): the gate that judges an
    answer is `lint`'s, which reads this checkout's — the page and `-S` read it too, and `--answer` names the refusal in one line."""
    bad = []
    with tempfile.TemporaryDirectory() as tmp:
        root = fixture(Path(tmp).resolve(), "holgo signed", "h@x signed")
        proof, code, err = page_proof(fm, root)
        if code != 0 or not proof or proof["state"] != "signed":
            bad.append(f"refused on origin/main, signed here: the page reads {proof} ({code}, {err.strip()[-160:]!r})")
        code, out, err = run(fm, root, "--answer", "AP-001", "accept")
        head = git(root, "cat-file", "commit", "refs/heads/answer/ap-001") if code == 0 else ""
        if code != 0 or "\n  signed, on `answer/ap-001`, pushed" not in out or "\ngpgsig" not in head \
                or "origin/main's `shoalmark.toml` cannot be read here — " not in err or "the commit is made as this checkout's reads it: signed" not in err:
            bad.append(f"refused on origin/main, signed here: --answer ended {code}, said {out[:100]!r} ({err.strip()[-240:]!r})")
    return bad


def template_reads_proof(fm):
    """The second screen takes each line that says how the commit is proved from PROOF, and none from a literal: no
    `signed, on`, no fixed `answer.sign.*` key for those lines, no touch. Returns every mismatch."""
    two = re.split(r'd\.querySelector\("\.copy"\)|clip\(d,line\)', fm.HTML_PAGE.split("const sign=")[1])[0]
    bad = [f"the second screen still names {w!r}" for w in ('"answer.sign.title"', '"act.sign.title"', '"answer.sign.intro"', '"answer.sign.step.commit"',
                                                            '"answer.sign.check.text"', '"answer.sign.fail.text"', "signed, on", "%G?", "touch") if w in two]
    bad += [f"the second screen does not read {w}" for w in ("P.title", "P.act", "P.intro", "P.commit", "P.check", "P.fail", "PROOF.said", "PROOF.format") if w not in two]
    if "touch" in fm.LABELS["answer.sign.step.commit"] or "Berührung" in fm.read_flat((HERE / "examples/de/labels.yaml").read_text(encoding="utf-8"))["answer.sign.step.commit"]:
        bad.append("the signed commit step still promises a touch")
    # FM-007: the proof line said before *accept* — once, in the heading of *waiting for you*, and in the answer dialog before OK —
    # from PROOF and its labels, a state in ink, its consequence the line beneath in the warning colour, never a box
    page = fm.HTML_PAGE
    heading, dialog = page.split('l("waiting.title")}: ${w.length}</b>`')[-1].split("w.slice(0,14)")[0], page.split("const act=")[1].split("const sign=")[0]
    if 'lh("proof.here",`<b class="pw${PROOF.state=="author"?" au":""}">${l(PROOF.word)}</b>`)' not in heading or "l(PROOF.why)" not in heading or 'class="cq"' not in heading:
        bad.append("the heading of *waiting for you* does not say the proof from PROOF")
    if dialog.find('lh("proof.dialog",`<b class="pw${PROOF.state=="author"?" au":""}">${l(PROOF.word)}</b>`)') < 0 or not -1 < dialog.find("proof.dialog") < dialog.find('l("answer.ok")') \
            or "l(PROOF.why)" not in dialog:
        bad.append("the answer dialog does not say the proof before OK")
    if page.count("proof.here") != 1 or any(w in page for w in ("your answers here", "your answer here", '"author only', ">author only", "`author only")):
        bad.append("the proof line is said more than once on one repository's board, or as a literal, not a label")
    cq = re.findall(r"\.cq\{[^}]*\}", page)
    if not cq or any("border" in c or "background" in c for c in cq) or ".cq{color:var(--amber)}" not in page:
        bad.append(f"the consequence is not a line in the warning colour (saw {cq})")
    return bad


def run_proof_controls(fm, check):
    """FM-054's class table, its two mutants, the other backends, the refused default branch, and the template."""
    try:
        fm.configure(HERE)
        check("FM-054 · the second screen reads every line that says how the commit is proved from PROOF — none from a literal, no touch",
              template_reads_proof(fm) == [])
        held = table(fm)
        check(f"FM-054 · the class table: every mode, default branch and checkout, by every surface — *signed* only where origin/main asks for it, `-S` only there; a checkout that asks for more than origin/main refused before any change, every answer reported given clean under `--check` (saw {held})",
              held == [])
        with mutant_surface(fm):
            m1 = table(fm)
        check(f"FM-054 · mutant 1, a surface that reads this checkout's configuration, fails the table ({len(m1)} mismatches: {m1[:2]})", bool(m1))
        with mutant_sign(fm):
            m2 = table(fm)
        check(f"FM-054 · mutant 2, `-S` decided from this checkout's configuration, fails the table ({len(m2)} mismatches: {m2[:2]})", bool(m2))
        off = other_backends(fm)
        if None in off:
            print("  skip  FM-054 · Subversion's row — svn or svnadmin is not installed here")
        check(f"FM-054 · off git the page says the server's login, or no author — no signed, no preview, no check (saw {[o for o in off if o]})",
              [o for o in off if o] == [])
        refusals, read = git_only_refusals(fm)
        if read < 16:
            print(f"  skip  FM-054 · RV-3310 · Subversion's {16 - read} refusals — svn or svnadmin is not installed here")
        check(f"FM-054 · RV-3310 · off git the answer-branch commands are refused in one line that says the capability and the Subversion "
              f"limitation, never *signed* — the command line and `owner_change`, {read} refusals (saw {refusals})", refusals == [] and read in (8, 16))
        unread = unread_row(fm)
        check(f"FM-054 · origin/main's configuration refused here: the page and `-S` read this checkout's, as the gate's `lint` does, and `--answer` names the refusal (saw {unread})",
              unread == [])
    finally:
        fm.configure(HERE)


if __name__ == "__main__":
    import importlib.util
    for _s in (sys.stdout, sys.stderr):
        _s.reconfigure(encoding="utf-8", errors="replace")
    spec = importlib.util.spec_from_file_location("fm", HERE / "shoalmark.py")
    tool = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(tool)
    fails = []

    def _check(name, ok):
        print(("  ok    " if ok else "  FAIL  ") + name)
        if not ok:
            fails.append(name)
    run_proof_controls(tool, _check)
    print()
    if fails:
        print(f"FAILED: {len(fails)}")
        sys.exit(1)
    print("all green")
