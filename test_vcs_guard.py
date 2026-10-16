"""FM-044 B guard controls: real consumer repositories, narrow adapter and retained Git proof.

Run directly, or call run_guard_controls(tool, check) from the integrating suite.
Local file:// SVN usernames are fixture mechanics, never deployed authentication proof.
These controls do not establish an adopted SVN consumer authority or public-entry wiring.
"""

import argparse
import builtins
import copy
from contextlib import ExitStack
from contextlib import redirect_stderr
import importlib.util
import io
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import urllib.parse
from unittest.mock import patch
import xml.etree.ElementTree as ET


HERE = Path(__file__).resolve().parent
TRIAGE = "# Triage\n\n## The intent\n\n- **never** — lose a loan\n\n## The current path\n\n1. Ship the trial.\n\n## Passes\n\n*None yet.*\n"


def run_guard_controls(fm, check):
    """FM-044: unavailable consumer authority cannot become protected SVN acceptance."""
    previous = fm.ROOT
    env = fm.nested_git_env()
    env.update(GIT_AUTHOR_NAME="fixture", GIT_AUTHOR_EMAIL="fixture@example.test",
               GIT_COMMITTER_NAME="fixture", GIT_COMMITTER_EMAIL="fixture@example.test")
    programs = {name: shutil.which(name) for name in ("git", "svn", "svnadmin", "ssh-keygen")}

    def run(name, *args, cwd=None, **options):
        return subprocess.run([programs[name], *args], cwd=cwd, env=env, check=True, capture_output=True, **options)

    def git_commit(root, subject, email="fixture@example.test", signed=False, name="fixture"):
        run("git", "add", "-A", cwd=root)
        run("git", "-c", "commit.gpgsign=false", "commit", "-qm", subject,
            *(["-S"] if signed else []), "--author=" + name + " <" + email + ">", cwd=root)

    def view(text):
        heads = fm.DEFAULTS["headings"]
        return ("docs/work-tracker", "docs/work-tracker/TRIAGE.md", text is not None,
                fm.guarded_sections(text, heads), heads, "", "docs/work-tracker")

    try:
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp).resolve()
            if programs["git"]:
                policies = (
                    ("owner", 'owner = "owner@example.test"\n', "owner@example.test"),
                    ("old-owner", '[seats]\nowner = "owner@example.test"\n', "owner@example.test"),
                    ("custom-answer", '[seats]\napprover = "approver@example.test"\n[rights]\napprover = ["answer"]\n', "approver@example.test"),
                    ("legacy-answerers", 'answerers = ["fixture"]\n', "fixture@example.test"),
                )
                for label, config, author in policies:
                    root = base / ("git-" + label); root.mkdir()
                    run("git", "init", "-q", cwd=root)
                    run("git", "branch", "-M", "main", cwd=root)
                    (root / "shoalmark.toml").write_text(config, encoding="utf-8")
                    home = root / "docs/work-tracker/TRIAGE.md"; home.parent.mkdir(parents=True)
                    home.write_text(TRIAGE, encoding="utf-8")
                    git_commit(root, "fixture accepted policy")
                    run("git", "update-ref", "refs/remotes/origin/main", "HEAD", cwd=root)
                    run("git", "symbolic-ref", "refs/remotes/origin/HEAD", "refs/remotes/origin/main", cwd=root)
                    run("git", "switch", "-qc", "change", cwd=root)
                    home.write_text(TRIAGE.replace("lose a loan", "lose a book"), encoding="utf-8")
                    git_commit(root, "authorized protected change", author)
                    fm.configure(root)
                    refused, report = fm.triage_guard()
                    check("FM-044 B: real Git " + label + " accepted-policy author retains acceptance", not refused and "each their own commit" in report)
                    home.write_text(TRIAGE.replace("lose a loan", "lose a key"), encoding="utf-8")
                    git_commit(root, "unauthorized protected change", "intruder@example.test", name="intruder")
                    fm.configure(root)
                    refused, report = fm.triage_guard()
                    check("FM-044 B: real Git " + label + " intruder still refuses", bool(refused) and "1 refused" in report)

                root = base / "git-passes"; root.mkdir()
                run("git", "init", "-q", cwd=root)
                run("git", "branch", "-M", "main", cwd=root)
                (root / "shoalmark.toml").write_text('owner = "owner@example.test"\n', encoding="utf-8")
                home = root / "docs/work-tracker/TRIAGE.md"; home.parent.mkdir(parents=True)
                home.write_text(TRIAGE, encoding="utf-8")
                git_commit(root, "fixture accepted policy")
                run("git", "update-ref", "refs/remotes/origin/main", "HEAD", cwd=root)
                run("git", "symbolic-ref", "refs/remotes/origin/HEAD", "refs/remotes/origin/main", cwd=root)
                home.write_text(TRIAGE.replace("*None yet.*", "2026-10-13: an ordinary pass."), encoding="utf-8")
                git_commit(root, "ordinary pass", "intruder@example.test")
                fm.configure(root)
                check("FM-044 B: real Git Passes-only change retains acceptance", fm.triage_guard()[0] == [])
                fm.COMMITTING = True
                with patch.object(fm.subprocess, "Popen", side_effect=AssertionError("pre-commit must not read the guard")):
                    check("FM-044 B: retained Git pre-commit contract starts nothing", fm.triage_guard() == ([], ""))

                run("git", "switch", "-qc", "side", "main", cwd=root)
                home.write_text(TRIAGE.replace("lose a loan", "lose a key"), encoding="utf-8")
                git_commit(root, "unauthorized intervening text", "intruder@example.test", name="intruder")
                home.write_text(TRIAGE, encoding="utf-8")
                git_commit(root, "restore accepted text", "owner@example.test")
                run("git", "switch", "-q", "main", cwd=root)
                (root / "ordinary.txt").write_text("ordinary work\n", encoding="utf-8")
                git_commit(root, "ordinary main work")
                run("git", "-c", "commit.gpgsign=false", "merge", "--no-ff", "-qm", "carry side without laundering it", "side", cwd=root)
                fm.configure(root)
                check("FM-044 B: actual Git merge and later revert do not erase an unauthorized parent change", bool(fm.triage_guard()[0]))
                run("git", "switch", "-qc", "self-grant", "refs/remotes/origin/main", cwd=root)
                (root / "shoalmark.toml").write_text('owner = "intruder@example.test"\n', encoding="utf-8")
                git_commit(root, "candidate grants itself authority", "intruder@example.test", name="intruder")
                home.write_text(TRIAGE.replace("lose a loan", "lose a key"), encoding="utf-8")
                git_commit(root, "use candidate authority", "intruder@example.test", name="intruder")
                fm.configure(root)
                check("FM-044 B: actual Git guard retains default-policy authority over candidate self-grant", bool(fm.triage_guard()[0]))

                if programs["ssh-keygen"]:
                    root = base / "git-signed"; root.mkdir()
                    run("git", "init", "-q", cwd=root)
                    run("git", "branch", "-M", "main", cwd=root)
                    key = base / "owner-key"
                    run("ssh-keygen", "-q", "-t", "ed25519", "-N", "", "-f", str(key))
                    (root / "allowed_signers").write_text("owner@example.test " + key.with_suffix(".pub").read_text(encoding="utf-8"), encoding="utf-8")
                    run("git", "config", "gpg.format", "ssh", cwd=root)
                    run("git", "config", "user.signingkey", str(key), cwd=root)
                    run("git", "config", "gpg.ssh.allowedSignersFile", "allowed_signers", cwd=root)
                    (root / "shoalmark.toml").write_text('owner = "owner@example.test signed"\n', encoding="utf-8")
                    home = root / "docs/work-tracker/TRIAGE.md"; home.parent.mkdir(parents=True)
                    home.write_text(TRIAGE, encoding="utf-8")
                    git_commit(root, "accepted signed policy fixture")
                    run("git", "update-ref", "refs/remotes/origin/main", "HEAD", cwd=root)
                    run("git", "symbolic-ref", "refs/remotes/origin/HEAD", "refs/remotes/origin/main", cwd=root)
                    home.write_text(TRIAGE.replace("lose a loan", "lose a book"), encoding="utf-8")
                    git_commit(root, "signed protected change", "owner@example.test", signed=True)
                    fm.configure(root)
                    check("FM-044 B: actual SSH-signed Git Owner change retains signature acceptance", fm.triage_guard()[0] == [])
                    check("FM-044 B: actual R14 signed Owner history accepts retained valid principal", fm.owner_signature_problems() == [])
                    home.write_text(TRIAGE.replace("lose a loan", "lose a key"), encoding="utf-8")
                    git_commit(root, "unsigned Owner protected change", "owner@example.test")
                    fm.configure(root)
                    check("FM-044 B: actual Git unsigned Owner still fails configured signature", bool(fm.triage_guard()[0]))
                    check("FM-044 B: actual R14 unsigned Owner history still refuses", bool(fm.owner_signature_problems()))
                else:
                    print("  SKIP FM-044 B: SSH-signed Git contrasts require ssh-keygen")

            if not (programs["svn"] and programs["svnadmin"]):
                print("  SKIP FM-044 B: real SVN guard fixtures require svn and svnadmin")
                return

            server, root = base / "svn-server", base / "svn-consumer"
            run("svnadmin", "create", str(server))
            run("svn", "checkout", "-q", server.as_uri(), str(root))
            home = root / "docs/work-tracker/TRIAGE.md"; home.parent.mkdir(parents=True)
            home.write_text(TRIAGE, encoding="utf-8")
            (root / "shoalmark.toml").write_text('owner = "fixture-owner"\n', encoding="utf-8")
            run("svn", "add", "shoalmark.toml", "docs", cwd=root)
            run("svn", "commit", "-q", "-m", "fixture committed policy is not adopted authority", "--username", "fixture-owner", cwd=root)
            info = run("svn", "info", "--xml", str(home))
            entry = ET.fromstring(info.stdout).find("entry")
            check("FM-044 B: guard target is a real committed SVN working copy", entry is not None and entry.find("commit").get("revision") == "1"
                  and entry.findtext("commit/author") == "fixture-owner" and entry.findtext("url").startswith(server.as_uri() + "/"))
            restricted = base / "no-git"; restricted.mkdir()
            check("FM-044 B: actual production PATH has neither Git nor SVN", shutil.which("git", path=str(restricted)) is None and shutil.which("svn", path=str(restricted)) is None)

            policies = (
                ("bare-owner", 'owner = "fixture-owner"\n', False),
                ("old-owner", '[seats]\nowner = "fixture-owner"\n', False),
                ("custom-answer", '[seats]\napprover = "fixture-owner"\n[rights]\napprover = ["answer"]\n', False),
                ("legacy-answerers", 'answerers = ["fixture-owner"]\n', False),
                ("signed-owner", 'owner = "owner@example.test signed"\n', True),
                ("signed-seat", '[seats]\nbuilder = "builder@example.test signed"\nowner = "fixture-owner"\n', True),
                ("legacy-only-signed", 'answerers = ["owner@example.test signed"]\n', True),
                ("self-grant", 'owner = "intruder"\n', False),
                ("suffix-removal", 'owner = "owner@example.test"\n', False),
                ("authority-removal", '', False),
                ("tracker-redirect", 'tracker_dir = "elsewhere"\nowner = "intruder"\n', False),
                ("heading-redirect", 'owner = "intruder"\n[headings]\nintent = "Other intent"\npath = "Other path"\n', False),
            )
            for label, config, signed in policies:
                (root / "shoalmark.toml").write_text(config, encoding="utf-8")
                home.write_text(TRIAGE.replace("lose a loan", "lose a key"), encoding="utf-8")
                before = {str(p.relative_to(root)): p.read_bytes() for p in (home, root / "shoalmark.toml")}
                starts, writes = [], []

                def start(*args, **kwargs):
                    starts.append((args, kwargs))
                    raise AssertionError("missing-policy refusal must precede every process")

                def write(*args, **kwargs):
                    writes.append((args, kwargs))
                    raise AssertionError("guard must not write")

                def watched_open(original):
                    def opened(file, mode="r", *args, **kwargs):
                        if any(flag in mode for flag in "wax+"):
                            return write(file, mode, *args, **kwargs)
                        return original(file, mode, *args, **kwargs)
                    return opened

                original_os_open = os.open

                def opened_fd(file, flags, *args, **kwargs):
                    if flags & (os.O_WRONLY | os.O_RDWR | os.O_CREAT | os.O_TRUNC | os.O_APPEND):
                        return write(file, flags, *args, **kwargs)
                    return original_os_open(file, flags, *args, **kwargs)

                with ExitStack() as stack:
                    stack.enter_context(patch.dict(os.environ, {"PATH": str(restricted)}))
                    stack.enter_context(patch.object(fm.subprocess, "Popen", side_effect=start))
                    stack.enter_context(patch.object(Path, "write_text", side_effect=write))
                    stack.enter_context(patch.object(Path, "write_bytes", side_effect=write))
                    stack.enter_context(patch.object(builtins, "open", watched_open(builtins.open)))
                    stack.enter_context(patch.object(io, "open", watched_open(io.open)))
                    stack.enter_context(patch.object(os, "open", opened_fd))
                    fm.configure(root)
                    guard = getattr(fm, "svn_guard", fm.triage_guard)
                    result = guard()
                    again = guard()
                refused, report = result
                check("FM-044 B: real SVN " + label + " protected adapter request refuses without adopted consumer policy", bool(refused) and "adopted committed consumer policy" in " ".join(refused) and result == again)
                check("FM-044 B: real SVN " + label + " starts no process and writes no guarded bytes", not starts and not writes and before == {str(p.relative_to(root)): p.read_bytes() for p in (home, root / "shoalmark.toml")})
                if signed:
                    check("FM-044 B: real SVN " + label + " cannot substitute an author for a requested signature", "signature" in " ".join(refused) and "signed" in " ".join(refused))

            # Direct Git-only history helpers must refuse at the actual boundary before Popen.
            git_only = (
                ("pending_author", lambda: fm.pending_author()),
                ("staged_now", lambda: fm.staged_now()),
                ("merge_heads", lambda: fm.merge_heads()),
                ("cat_blobs", lambda: fm.cat_blobs(["HEAD:shoalmark.toml"])),
                ("resolve_commits", lambda: fm.resolve_commits(["HEAD"])),
                ("tree_paths", lambda: fm.tree_paths("HEAD")),
                ("path_mode", lambda: fm.path_mode("HEAD", "shoalmark.toml")),
                ("owner_policy", lambda: fm.owner_policy()),
                ("origin_default", lambda: fm.origin_default()),
                ("trunk_ref", lambda: fm.trunk_ref()),
                ("read_changes", lambda: fm.read_changes()),
                ("git_ship_verdicts", lambda: fm.git_ship_verdicts(["HEAD"], ["HEAD"], ["docs/"])),
                ("staged_files", lambda: fm.staged_files([], fm.nested_git_env())),
            )
            for label, call in git_only:
                starts = []
                original_popen = subprocess.Popen

                def attempted(*args, **kwargs):
                    starts.append((args, kwargs))
                    return original_popen(*args, **kwargs)

                with patch.dict(os.environ, {"PATH": str(restricted)}), patch.object(fm.subprocess, "Popen", side_effect=attempted), redirect_stderr(io.StringIO()):
                    fm.configure(root)
                    try:
                        call()
                    except SystemExit as error:
                        refused = error.code == fm.EXIT_LINT
                    except OSError:
                        refused = False
                    else:
                        refused = False
                check("FM-044 B: actual SVN " + label + " refuses before a Git process attempt", refused and not starts)

            # CLI-only Git-hook applicability belongs to C/P; internal SVN checks remain harmless.
            fm.configure(root)
            with patch.object(fm.subprocess, "Popen", side_effect=AssertionError("internal non-Git hooks start nothing")):
                check("FM-044 B: normal SVN internal session problems retain empty result", fm.session_problems() == [])
                check("FM-044 B: normal SVN internal pending triage retains empty result", fm.triage_pending("ordinary work") == ([], []))

            # An explicit fixture policy tests existing attribution semantics, not consumer adoption.
            (root / "shoalmark.toml").write_text('owner = "fixture-owner"\n[seats]\nbuilder = "fixture-builder"\n', encoding="utf-8")
            home.write_text(TRIAGE, encoding="utf-8")
            original = root / "docs/work-tracker/original.txt"
            original.write_text('---\nid: FEAT-001\nstatus: Proposed\nanswer: keep\n---\n\n# Fixture\n', encoding="utf-8")
            run("svn", "add", str(original))
            run("svn", "commit", "-q", "-m", "fixture author-only policy and original", "--username", "fixture-owner", cwd=root)
            copied = original.with_name("intruder-copy.txt")
            run("svn", "copy", str(original), str(copied))
            run("svn", "commit", "-q", "-m", "intruder copies protected state", "--username", "intruder", cwd=root)
            permitted = original.with_name("owner-copy.txt")
            run("svn", "copy", str(original), str(permitted))
            run("svn", "commit", "-q", "-m", "fixture Owner copies its own state", "--username", "fixture-owner", cwd=root)
            bad_source = original.with_name("intruder-source.txt")
            bad_source.write_text(original.read_text(encoding="utf-8"), encoding="utf-8")
            run("svn", "add", str(bad_source))
            run("svn", "commit", "-q", "-m", "unauthorized original state", "--username", "intruder", cwd=root)
            laundered = original.with_name("owner-copies-intruder.txt")
            run("svn", "copy", str(bad_source), str(laundered))
            run("svn", "commit", "-q", "-m", "fixture Owner cannot cleanse original author", "--username", "fixture-owner", cwd=root)
            svn_only = base / "svn-only"; svn_only.mkdir()
            # The launcher path is real. No Git exists on the actual production PATH.
            if os.name == "nt":
                # Retain SVN's installation directory so its adjacent DLLs are loadable.
                svn_only = Path(programs["svn"]).parent
                if shutil.which("git", path=str(svn_only)) is not None:
                    print("  SKIP FM-044 B: installed SVN and Git share a Windows PATH directory")
                    return
            else:
                (svn_only / "svn").symlink_to(programs["svn"])
            check("FM-044 B: real attribution production PATH excludes Git", shutil.which("git", path=str(svn_only)) is None)
            for label, path, expected in (("original", original, "fixture-owner"), ("authorized original/unauthorized copier", copied, "intruder"),
                                           ("authorized original/authorized copier", permitted, "fixture-owner"),
                                           ("unauthorized original/authorized copier", laundered, "intruder")):
                starts = []
                original_popen = subprocess.Popen

                def observed(*args, **kwargs):
                    starts.append(args[0])
                    return original_popen(*args, **kwargs)

                with patch.dict(os.environ, {"PATH": str(svn_only)}), patch.object(fm.subprocess, "Popen", side_effect=observed):
                    fm.configure(root)
                    author = fm.line_author(path, "answer:")
                check("FM-044 B: real SVN " + label + " retains both author/copy rights", author[0] == expected and author[2] == "svn" and author[3].isdigit()
                      and bool(starts) and all(cmd[0] == "svn" for cmd in starts))

            # After real SVN reads, inject unusable required first-path log output; never replace it by empty success.
            relative = copied.relative_to(root).as_posix()
            broken_logs = (
                ("empty", b""), ("no-entry", b"<log/>"),
                ("missing-revision", b"<log><logentry><author>intruder</author></logentry></log>"),
                ("bad-revision", b'<log><logentry revision="bad"><author>intruder</author></logentry></log>'),
                ("zero-revision", b'<log><logentry revision="0"><author>intruder</author></logentry></log>'),
                ("missing-copy-author", b'<log><logentry revision="3"/></log>'),
            )
            for label, output in broken_logs:
                actual_run, starts = subprocess.run, []

                def injected(cmd, *args, **kwargs):
                    done = actual_run(cmd, *args, **kwargs)
                    starts.append(cmd)
                    if cmd[0] == "svn" and "--stop-on-copy" in cmd:
                        return subprocess.CompletedProcess(cmd, 0, output, done.stderr)
                    return done

                with patch.dict(os.environ, {"PATH": str(svn_only)}), patch.object(fm.subprocess, "run", side_effect=injected):
                    fm.configure(root)
                    errors = []
                    for _attempt in range(2):
                        try:
                            fm.svn_blame(relative)
                        except fm.SvnUnreadable as error:
                            errors.append(str(error))
                check("FM-044 B: actual SVN " + label + " required copy history refuses and keeps its failure", len(errors) == 2 and errors[0] == errors[1]
                      and sum("--stop-on-copy" in cmd for cmd in starts) == 1 and all(cmd[0] == "svn" for cmd in starts))

            broken_blames = (
                ("missing-revision", '<entry line-number="4"><commit><author>fixture-owner</author></commit></entry>'),
                ("bad-revision", '<entry line-number="4"><commit revision="bad"><author>fixture-owner</author></commit></entry>'),
                ("zero-revision", '<entry line-number="4"><commit revision="0"><author>fixture-owner</author></commit></entry>'),
                ("missing-author", '<entry line-number="4"><commit revision="3"/></entry>'),
                ("empty-author", '<entry line-number="4"><commit revision="3"><author> </author></commit></entry>'),
                ("zero-line", '<entry line-number="0"><commit revision="3"><author>fixture-owner</author></commit></entry>'),
                ("repeated-line", '<entry line-number="4"><commit revision="3"><author>fixture-owner</author></commit></entry>' * 2),
            )
            for label, entries in broken_blames:
                actual_run, starts = subprocess.run, []

                def injected_blame(cmd, *args, **kwargs):
                    done = actual_run(cmd, *args, **kwargs)
                    starts.append(cmd)
                    if cmd[0] == "svn" and "blame" in cmd:
                        return subprocess.CompletedProcess(cmd, 0, ("<blame><target>" + entries + "</target></blame>").encode("utf-8"), done.stderr)
                    return done

                with patch.dict(os.environ, {"PATH": str(svn_only)}), patch.object(fm.subprocess, "run", side_effect=injected_blame):
                    fm.configure(root)
                    errors = []
                    for _attempt in range(2):
                        try:
                            fm.svn_blame(relative)
                        except fm.SvnUnreadable as error:
                            errors.append(str(error))
                        except (AttributeError, TypeError, ValueError):
                            pass                          # old malformed-output traceback is not a bounded refusal
                check("FM-044 B: actual SVN " + label + " required blame metadata refuses without traceback", len(errors) == 2 and errors[0] == errors[1]
                      and sum("blame" in cmd for cmd in starts) == 1 and all(cmd[0] == "svn" for cmd in starts))

            # Shipped proof is scoped to the configured consumer, including when a revision changes another project.
            consumer, foreign = root / "consumer", root / "foreign"
            consumer_home = consumer / "docs/work-tracker/FEAT-001-proof.md"
            consumer_home.parent.mkdir(parents=True); foreign.mkdir()
            consumer_home.write_text('---\nid: FEAT-001\nstatus: Proposed\n---\n\n# Fixture\n', encoding="utf-8")
            (consumer / "product.txt").write_text("built\n", encoding="utf-8")
            (foreign / "product.txt").write_text("foreign work\n", encoding="utf-8")
            run("svn", "add", str(consumer), str(foreign))
            run("svn", "commit", "-q", "-m", "consumer product fixture", "--username", "fixture-owner", cwd=root)
            built_revision = run("svn", "info", "--show-item", "revision", "-r", "HEAD", server.as_uri()).stdout.decode().strip()
            consumer_home.write_text(consumer_home.read_text(encoding="utf-8") + "records-only consumer edit\n", encoding="utf-8")
            (foreign / "product.txt").write_text("foreign product edit\n", encoding="utf-8")
            run("svn", "commit", "-q", "-m", "consumer records and foreign product", "--username", "fixture-owner", cwd=root)
            foreign_revision = run("svn", "info", "--show-item", "revision", "-r", "HEAD", server.as_uri()).stdout.decode().strip()
            small = base / "consumer-subtree"
            run("svn", "checkout", "-q", server.as_uri() + "/consumer", str(small))
            tracker = {"id": "FEAT-001", "status": "Proposed", "file": "FEAT-001-proof.md"}
            rels = {"docs/work-tracker/FEAT-001-proof.md": tracker}
            with patch.dict(os.environ, {"PATH": str(svn_only)}):
                fm.configure(small)
                verdicts = fm.svn_ship_verdicts(["r" + built_revision, "r" + foreign_revision], None, ["docs/"])
                check("FM-044 B: real SVN own consumer product retains Shipped revision proof", verdicts["r" + built_revision] == "")
                check("FM-044 B: real SVN foreign product cannot prove a consumer records-only revision", bool(verdicts["r" + foreign_revision]))
                check("FM-044 B: real clean SVN newest non-Shipped change remains genuinely empty", list(fm.svn_shipped_moves(rels)) == [])

            broken_info = (("empty", b""), ("not-relative", b"/consumer\n"))
            for label, output in broken_info:
                actual_run = subprocess.run

                def injected_info(cmd, *args, **kwargs):
                    done = actual_run(cmd, *args, **kwargs)
                    if cmd[0] == "svn" and "relative-url" in cmd:
                        return subprocess.CompletedProcess(cmd, 0, output, done.stderr)
                    return done

                with patch.dict(os.environ, {"PATH": str(svn_only)}), patch.object(fm.subprocess, "run", side_effect=injected_info):
                    fm.configure(small)
                    try:
                        fm.svn_ship_verdicts(["r" + built_revision], None, ["docs/"])
                    except fm.SvnUnreadable:
                        refused = True
                    else:
                        refused = False
                check("FM-044 B: actual SVN " + label + " consumer path proof cannot fall back to repository root", refused)

            missing_changes = (
                ("empty-status", "status", b""),
                ("malformed-status", "status", b"<unrelated/>"),
                ("empty-newest-log", "log", b""),
                ("missing-newest-entry", "log", b"<log/>"),
                ("bad-newest-revision", "log", b'<log><logentry revision="bad"><paths><path action="M">/consumer/product.txt</path></paths></logentry></log>'),
                ("missing-newest-paths", "log", b'<log><logentry revision="8"/></log>'),
            )
            for label, operation, output in missing_changes:
                actual_run = subprocess.run

                def injected_change(cmd, *args, **kwargs):
                    done = actual_run(cmd, *args, **kwargs)
                    if cmd[0] == "svn" and cmd[1] == operation:
                        return subprocess.CompletedProcess(cmd, 0, output, done.stderr)
                    return done

                with patch.dict(os.environ, {"PATH": str(svn_only)}), patch.object(fm.subprocess, "run", side_effect=injected_change):
                    fm.configure(small)
                    try:
                        refused = bool(fm.ship_problems([tracker]))
                    except (TypeError, ValueError):
                        refused = False
                check("FM-044 B: actual SVN " + label + " required checked change refuses even when local tracker is open", refused)

            # This is the pure protected-text comparison seam, not public-entry acceptance.
            with patch.dict(os.environ, {"PATH": str(restricted)}), patch.object(fm.subprocess, "Popen", side_effect=AssertionError("local comparison must start nothing")):
                before = view(TRIAGE)
                passes = view(TRIAGE.replace("*None yet.*", "2026-10-13: an ordinary pass."))
                check("FM-044 B: real SVN local Passes-only comparison needs no server or authority claim", fm.section_changes(passes, [before]) == [])
                scaffold = fm.TRIAGE_HOME.format(cmd="shoalmark", **fm.DEFAULTS["headings"])
                check("FM-044 B: known scaffold comparison makes no protected statement", fm.section_changes(view(scaffold), [view(None)]) == [])
                check("FM-044 B: actual protected local text differs independently of missing authority", bool(fm.section_changes(view(TRIAGE.replace("lose a loan", "lose a key")), [before])))
        run_binding_controls(fm, check, env, programs)
        run_shape_controls(fm, check, env, programs)
    finally:
        fm.configure(previous)


def run_binding_controls(fm, check, env, programs):
    """RV-3092/3093/3094: real-read binding faults cannot become author or Shipped proof."""
    if not programs["svn"] or not programs["svnadmin"]:
        return
    actual_run, actual_popen = subprocess.run, subprocess.Popen

    def setup(*args, cwd=None):
        return actual_run([programs["svn"], *args], cwd=cwd, env=env, check=True, capture_output=True).stdout.decode()

    def xml_fault(operation, change, select=lambda cmd: True):
        def fault(cmd, data):
            if cmd[1] == operation and select(cmd):
                tree = ET.fromstring(data)
                change(tree)
                return ET.tostring(tree)
        return fault

    with tempfile.TemporaryDirectory() as temp:
        top = Path(temp).resolve(); server = top / "server"; root = top / "root"
        actual_run([programs["svnadmin"], "create", str(server)], env=env, check=True, capture_output=True)
        setup("checkout", "-q", server.as_uri(), str(root))
        original = "docs/work-tracker/FEAT-001-item.md"
        copied = "docs/work-tracker/FEAT-002-copy.md"
        text = '---\nid: FEAT-001\nstatus: Proposed\nanswer: keep\n---\n\n# Fixture\n'
        for name in ("alpha", "beta"):
            home = root / name
            (home / original).parent.mkdir(parents=True)
            (home / original).write_text(text, encoding="utf-8")
            (home / "empty.txt").write_text("", encoding="utf-8")
            (home / "product.txt").write_text("product\n", encoding="utf-8")
            (home / "shoalmark.toml").write_text('owner = "owner"\n', encoding="utf-8")
        setup("add", "alpha", "beta", cwd=root)
        setup("commit", "-qm", "fixture baseline", "--username", "owner", cwd=root)
        setup("copy", original, copied, cwd=root / "alpha")
        setup("commit", "-qm", "fixture copy", "--username", "copier", cwd=root / "alpha")
        (root / "alpha" / original).write_text(text + "records only\n", encoding="utf-8")
        (root / "beta/product.txt").write_text("foreign product\n", encoding="utf-8")
        setup("commit", "-qm", "own records and foreign product", "--username", "owner", cwd=root)
        consumer = top / "consumer"
        setup("checkout", "-q", server.as_uri() + "/alpha", str(consumer))
        svn_only = top / "bin"; svn_only.mkdir()
        if os.name == "nt":
            svn_only = Path(programs["svn"]).parent
            if shutil.which("git", path=str(svn_only)) is not None:
                print("  SKIP RV-3092/3093/3094: installed SVN and Git share a Windows PATH directory")
                return
        else:
            (svn_only / "svn").symlink_to(programs["svn"])
        tracker = {"id": "FEAT-001", "file": "FEAT-001-item.md", "status": "Proposed"}

        def exercise(label, call, expected, fault=None, home=consumer):
            """Measure production only: actual reads, confined cwd, no Git or Python writes."""
            starts, writes = [], []
            before = {p.relative_to(home).as_posix(): p.read_bytes() for p in home.rglob("*") if p.is_file() and ".svn" not in p.parts}

            def invoked(cmd, *args, **kwargs):
                done = actual_run(cmd, *args, **kwargs)
                output = fault(cmd, done.stdout) if fault is not None and done.returncode == 0 else None
                return subprocess.CompletedProcess(cmd, done.returncode, output, done.stderr) if output is not None else done

            def observed(*args, **kwargs):
                starts.append((args[0], kwargs.get("cwd")))
                return actual_popen(*args, **kwargs)

            def guarded_open(real):
                def opened(file, mode="r", *args, **kwargs):
                    if any(flag in mode for flag in "wax+"):
                        writes.append(file)
                        raise AssertionError("proof call attempted a write")
                    return real(file, mode, *args, **kwargs)
                return opened

            real_fd = os.open

            def opened_fd(file, flags, *args, **kwargs):
                if flags & (os.O_WRONLY | os.O_RDWR | os.O_CREAT | os.O_TRUNC | os.O_APPEND):
                    writes.append(file)
                    raise AssertionError("proof call attempted a write")
                return real_fd(file, flags, *args, **kwargs)

            with ExitStack() as stack:
                stack.enter_context(patch.dict(os.environ, {"PATH": str(svn_only)}))
                stack.enter_context(patch.object(fm.subprocess, "run", side_effect=invoked))
                stack.enter_context(patch.object(fm.subprocess, "Popen", side_effect=observed))
                stack.enter_context(patch.object(builtins, "open", guarded_open(builtins.open)))
                stack.enter_context(patch.object(io, "open", guarded_open(io.open)))
                stack.enter_context(patch.object(os, "open", side_effect=opened_fd))
                fm.configure(home)
                try:
                    value = call(fm)
                except fm.SvnUnreadable as error:
                    value = error
                except (AttributeError, TypeError, ValueError, KeyError, IndexError) as error:
                    value = error
            after = {p.relative_to(home).as_posix(): p.read_bytes() for p in home.rglob("*") if p.is_file() and ".svn" not in p.parts}
            check(label, expected(value, starts) and before == after and not writes and bool(starts)
                  and all(cmd[0] == "svn" and Path(cwd) == home for cmd, cwd in starts))

        def cached_blame(path):
            def call(tool):
                errors = []
                for _attempt in range(2):
                    try:
                        tool.svn_blame(path)
                    except tool.SvnUnreadable as error:
                        errors.append(error)
                return errors, ("first", path) in tool._SVN_BLAME, ("through", path) in tool._SVN_BLAME
            return call

        def cache_refused(value, starts):
            return (isinstance(value, tuple) and len(value[0]) == 2 and value[0][0] is value[0][1] and not value[1] and not value[2]
                    and sum(cmd[1] == "blame" for cmd, _cwd in starts) == 1)

        refused = lambda value, _starts: isinstance(value, fm.SvnUnreadable)
        outer_refused = lambda value, _starts: isinstance(value, list) and bool(value) and all(isinstance(line, str) for line in value)
        def formatted(tree):
            for node in tree.iter():
                node.tail = " \t\r\n"
                if len(node) or node.tag in ("blame", "target", "log", "status"):
                    node.text = " \t\r\n"

        def checked_view(tool):
            reads, actual_open = [], io.open
            def opened(file, *args, **kwargs):
                if isinstance(file, (str, os.PathLike)) and Path(file) == consumer / original:
                    reads.append(str(file))
                return actual_open(file, *args, **kwargs)
            with patch.object(io, "open", side_effect=opened):
                return tool.ship_problems([tracker]), reads

        def checked_before_selection(value, starts):
            return (isinstance(value, tuple) and outer_refused(value[0], starts) and not value[1]
                    and "could not be read" in " ".join(value[0])
                    and [cmd[1] for cmd, _cwd in starts] == ["info", "status"])

        exercise("RV-3092: real copied lines retain copier and source", lambda tool: tool.line_author(consumer / copied, "answer:"),
                 lambda value, _starts: isinstance(value, tuple) and value[0] == "copier" and value[2:] == ("svn", "2"))
        exercise("RV-3092: real committed empty blame is genuinely empty", lambda tool: tool.svn_blame("empty.txt"), lambda value, _starts: value == {})
        (consumer / "pending.txt").write_text("pending\n", encoding="utf-8")
        exercise("RV-3092: real unversioned blame remains pending", lambda tool: tool.svn_blame("pending.txt"), lambda value, _starts: value == {})
        setup("add", "pending.txt", cwd=consumer)
        exercise("RV-3092: real scheduled-add blame remains pending", lambda tool: tool.svn_blame("pending.txt"), lambda value, _starts: value == {})
        (consumer / copied).write_text(text + "pending line\n", encoding="utf-8")
        exercise("RV-3092: real uncommitted line retains no committed author", lambda tool: tool.svn_blame(copied),
                 lambda value, _starts: isinstance(value, dict) and value[max(value)] == (None, ""))
        setup("revert", copied, "pending.txt", cwd=consumer); (consumer / "pending.txt").unlink()

        blame_faults = (
            ("unrelated root", lambda _tree: None),
            ("foreign target", lambda tree: tree[0].set("path", "elsewhere/foreign.md")),
            ("duplicate target", lambda tree: tree.append(copy.deepcopy(tree[0]))),
            ("entry outside target", lambda tree: tree.append(copy.deepcopy(tree[0][0]))),
            ("duplicate commit", lambda tree: tree[0][0].append(copy.deepcopy(tree[0][0].find("commit")))),
            ("duplicate author", lambda tree: tree[0][0].find("commit").append(copy.deepcopy(tree[0][0].find("commit/author")))),
            ("duplicate date", lambda tree: tree[0][0].find("commit").append(copy.deepcopy(tree[0][0].find("commit/date")))),
            ("duplicate merged proof", lambda tree: tree[0][0].append(copy.deepcopy(tree[0][0].find("merged")))),
            ("missing merged commit", lambda tree: tree[0][0].find("merged").clear()),
            ("merged path alias", lambda tree: tree[0][0].find("merged").set("path", "/alpha/../beta/item.md")),
            ("merged newer than commit", lambda tree: tree[0][0].find("merged/commit").set("revision", "999999")),
            ("unordered line", lambda tree: tree[0][0].set("line-number", "2")),
        )
        for label, change in blame_faults:
            fault = (lambda cmd, _data: b"<unrelated/>" if cmd[1] == "blame" else None) if label == "unrelated root" else xml_fault("blame", change)
            exercise("RV-3092: " + label + " is one cached controlled blame refusal", cached_blame(copied), cache_refused, fault)
        exercise("RV-3092: blank successful committed blame cannot mean pending", cached_blame(copied), cache_refused,
                 lambda cmd, _data: b"" if cmd[1] == "blame" else None)
        exercise("RV-3092: target structural text cannot be cached as genuine empty blame", cached_blame(copied), cache_refused,
                 lambda cmd, _data: ('<blame><target path="' + copied + '">LOST ENTRY DATA</target></blame>').encode()
                 if cmd[1] == "blame" else None)
        for field in (".", "target", "target/entry", "target/entry/commit", "target/entry/merged", "target/entry/merged/commit"):
            for slot in ("text", "tail"):
                exercise("RV-3092: blame " + field + " structural " + slot + " is one cached refusal", cached_blame(copied), cache_refused,
                         xml_fault("blame", lambda tree, field=field, slot=slot: setattr(tree.find(field), slot, "LOST PROOF DATA")))
        for field in ("target/entry/commit/author", "target/entry/commit/date", "target/entry/merged/commit/author"):
            exercise("RV-3092: blame scalar " + field + " tail cannot escape its field", cached_blame(copied), cache_refused,
                     xml_fault("blame", lambda tree, field=field: setattr(tree.find(field), "tail", "LOST PROOF DATA")))
        exercise("RV-3092: formatting whitespace retains copied source/copier", lambda tool: tool.line_author(consumer / copied, "answer:"),
                 lambda value, _starts: value == ("copier", None, "svn", "2"), xml_fault("blame", formatted))
        exercise("RV-3092: formatted genuine empty blame remains empty", lambda tool: tool.svn_blame("empty.txt"),
                 lambda value, _starts: value == {}, xml_fault("blame", formatted))
        first_faults = (
            ("wrong first-log root", lambda tree: setattr(tree, "tag", "unrelated")),
            ("duplicate first revision", lambda tree: tree.append(copy.deepcopy(tree[0]))),
            ("mismatched last revision", lambda tree: tree[0].set("revision", "999999")),
            ("duplicate first author", lambda tree: tree[0].append(copy.deepcopy(tree[0].find("author")))),
            ("missing required copier author", lambda tree: tree[0].remove(tree[0].find("author"))),
            ("foreign changed path", lambda tree: tree[0].find("paths/path").__setattr__("text", "/beta/foreign.md")),
            ("no creation binding", lambda tree: [p.set("action", "M") for p in tree[0].find("paths")]),
        )
        for label, change in first_faults:
            exercise("RV-3092: " + label + " cannot certify a copy", cached_blame(copied), cache_refused,
                     xml_fault("log", change, lambda cmd: "--stop-on-copy" in cmd))
        for field in (".", "logentry", "logentry/paths"):
            for slot in ("text", "tail"):
                exercise("RV-3092: creation " + field + " structural " + slot + " cannot credit copier", cached_blame(copied), cache_refused,
                         xml_fault("log", lambda tree, field=field, slot=slot: setattr(tree.find(field), slot, "LOST PATH DATA"), lambda cmd: "--stop-on-copy" in cmd))
        exercise("RV-3092: formatted creation proof retains copied source/copier", lambda tool: tool.line_author(consumer / copied, "answer:"),
                 lambda value, _starts: value == ("copier", None, "svn", "2"), xml_fault("log", formatted, lambda cmd: "--stop-on-copy" in cmd))
        exercise("RV-3092: reversed multi-revision first-path history refuses", cached_blame(original), cache_refused,
                 xml_fault("log", lambda tree: tree.__setitem__(slice(None), list(reversed(list(tree)))), lambda cmd: "--stop-on-copy" in cmd))
        for label, change in (
                ("wrong merge root", lambda tree: setattr(tree, "tag", "unrelated")),
                ("mismatched merge revision", lambda tree: tree[0].set("revision", "999999")),
                ("duplicate merge revision", lambda tree: tree.append(copy.deepcopy(tree[0]))),
                ("missing nested revision", lambda tree: tree[0].append(ET.fromstring("<logentry/>"))),
                ("duplicate nested revisions", lambda tree: tree[0].extend([ET.fromstring('<logentry revision="1"/>'), ET.fromstring('<logentry revision="1"/>')]))):
            exercise("RV-3092: " + label + " cannot certify copy attribution", cached_blame(copied), cache_refused,
                     xml_fault("log", change, lambda cmd: "-g" in cmd))
        for label, change in (
                ("foreign info target", lambda tree: tree[0].set("path", "elsewhere/item.md")),
                ("duplicate info commit", lambda tree: tree[0].append(copy.deepcopy(tree[0].find("commit")))),
                ("foreign info namespace", lambda tree: setattr(tree[0].find("relative-url"), "text", "^/beta/foreign.md"))):
            exercise("RV-3092: " + label + " cannot bind first-path history", cached_blame(copied), cache_refused,
                     xml_fault("info", change, lambda cmd: "--show-item" not in cmd))
        retained_author = lambda value, _starts: isinstance(value, dict) and value.get(4) == ("owner", "1")
        for field in (".", "entry", "entry/repository", "entry/wc-info", "entry/commit"):
            for slot in ("text", "tail"):
                exercise("RV-3092: info " + field + " structural " + slot + " cannot certify blame", cached_blame(copied), cache_refused,
                         xml_fault("info", lambda tree, field=field, slot=slot: setattr(tree.find(field), slot, "LOST INFO DATA"), lambda cmd: "--show-item" not in cmd))
        exercise("RV-3092: nested relative URL scalar cannot certify blame", cached_blame(copied), cache_refused,
                 xml_fault("info", lambda tree: tree[0].find("relative-url").append(ET.fromstring("<rogue/>")), lambda cmd: "--show-item" not in cmd))
        exercise("RV-3092: unused info author is not required for the checked original blame", lambda tool: tool.svn_blame(original), retained_author,
                 xml_fault("info", lambda tree: tree[0].find("commit").remove(tree[0].find("commit/author")), lambda cmd: "--show-item" not in cmd))
        exercise("RV-3092: unused later path-log author cannot erase valid original attribution", lambda tool: tool.svn_blame(original), retained_author,
                 xml_fault("log", lambda tree: tree[0].remove(tree[0].find("author")), lambda cmd: "--stop-on-copy" in cmd))

        shipped = text.replace("status: Proposed", "status: Shipped") + "\n## Ship log\n\n| Date | What |\n| --- | --- |\n| 2026-10-13 | r1 |\n"
        for item in ("copied", "added", "replaced"):
            pending_path = original if item == "replaced" else "docs/work-tracker/FEAT-004-pending.md"
            if item == "copied":
                setup("copy", original, pending_path, cwd=consumer)
            elif item == "replaced":
                setup("delete", original, cwd=consumer)
            (consumer / pending_path).write_text(shipped, encoding="utf-8")
            if item != "copied":
                setup("add", pending_path, cwd=consumer)
            pending_tracker = dict(tracker, file=Path(pending_path).name)
            exercise("RV-3093: real pending " + item + " Shipped retains valid status and own-product proof", lambda tool, pending_tracker=pending_tracker: tool.ship_problems([pending_tracker]), lambda value, _starts: value == [])
            setup("revert", pending_path, cwd=consumer)
            if item != "replaced":
                (consumer / pending_path).unlink(missing_ok=True)
        setup("switch", "--ignore-ancestry", server.as_uri() + "/beta/" + original, original, cwd=consumer)
        exercise("RV-3093: real switched non-Shipped tracker refuses its foreign view", lambda tool: tool.ship_problems([tracker]), outer_refused)
        (consumer / original).write_text(shipped, encoding="utf-8")
        exercise("RV-3093: real switched pending Shipped tracker refuses before proof", lambda tool: tool.ship_problems([tracker]), outer_refused)
        setup("revert", original, cwd=consumer)
        setup("switch", "--ignore-ancestry", server.as_uri() + "/alpha/" + original, original, cwd=consumer)
        (consumer / original).write_text(shipped, encoding="utf-8")
        exercise("RV-3093/3094: ordinary own-product pending Shipped retains proof", lambda tool: tool.ship_problems([tracker]), lambda value, _starts: value == [])
        setup("changelist", "fixture-changes", original, cwd=consumer)
        exercise("RV-3093: real changelist pending Shipped retains its unique local binding", lambda tool: tool.ship_problems([tracker]), lambda value, _starts: value == [])
        setup("changelist", "--remove", original, cwd=consumer)
        (consumer / original).write_text(shipped.replace("r1", "no revision"), encoding="utf-8")
        exercise("RV-3093: actual pending move with no revision refuses", lambda tool: tool.ship_problems([tracker]), outer_refused)
        exercise("RV-3093: target text-only garbage cannot select newest history over pending content", checked_view, checked_before_selection,
                 lambda cmd, _data: b'<status><target path="docs/work-tracker">LOST ENTRY DATA</target></status>' if cmd[1] == "status" else None)
        for field in (".", "target", "target/entry", "target/entry/wc-status", "target/entry/wc-status/commit"):
            for slot in ("text", "tail"):
                exercise("RV-3093: status " + field + " structural " + slot + " refuses before selection/read", checked_view, checked_before_selection,
                         xml_fault("status", lambda tree, field=field, slot=slot: setattr(tree.find(field), slot, "LOST STATUS DATA")))
        status_faults = (
            ("foreign target", lambda tree: tree[0].set("path", "elsewhere/foreign")),
            ("duplicate target", lambda tree: tree.append(copy.deepcopy(tree[0]))),
            ("unknown item hides pending move", lambda tree: tree[0][0][0].set("item", "INVALID")),
            ("unknown props", lambda tree: tree[0][0][0].set("props", "INVALID")),
            ("foreign entry hides pending move", lambda tree: tree[0][0].set("path", "elsewhere/foreign.md")),
            ("confined absent entry hides pending move", lambda tree: tree[0][0].set("path", "docs/work-tracker/foreign.md")),
            ("dot path alias", lambda tree: tree[0][0].set("path", "./" + original)),
            ("parent path alias", lambda tree: tree[0][0].set("path", "docs/work-tracker/../work-tracker/FEAT-001-item.md")),
            ("case path alias", lambda tree: tree[0][0].set("path", original[:-3] + ".MD")),
            ("duplicate entry", lambda tree: tree[0].append(copy.deepcopy(tree[0][0]))),
            ("duplicate wc-status", lambda tree: tree[0][0].append(copy.deepcopy(tree[0][0][0]))),
            ("missing revision", lambda tree: tree[0][0][0].attrib.pop("revision", None)),
            ("invalid revision", lambda tree: tree[0][0][0].set("revision", "wrong")),
            ("invalid switched boolean", lambda tree: tree[0][0][0].set("switched", "maybe")),
            ("invalid external boolean", lambda tree: tree[0][0][0].set("file-external", "maybe")),
            ("external item", lambda tree: tree[0][0][0].set("item", "external")),
            ("inconsistent committed revision", lambda tree: tree[0][0][0].find("commit").set("revision", "999999")),
        )
        for label, change in status_faults:
            exercise("RV-3093: " + label + " refuses through outer gate", lambda tool: tool.ship_problems([tracker]), outer_refused, xml_fault("status", change))
        (consumer / original).write_text(shipped, encoding="utf-8")
        log_faults = (
            ("unrelated root", lambda tree: setattr(tree, "tag", "unrelated")),
            ("missing revision", lambda tree: tree[0].attrib.pop("revision", None)),
            ("mismatched revision", lambda tree: tree[0].set("revision", "999999")),
            ("duplicate entry", lambda tree: tree.append(copy.deepcopy(tree[0]))),
            ("duplicate paths container", lambda tree: tree[0].append(copy.deepcopy(tree[0].find("paths")))),
            ("duplicate changed path", lambda tree: tree[0].find("paths").append(copy.deepcopy(tree[0].find("paths/path")))),
            ("invalid action", lambda tree: tree[0].find("paths/path").set("action", "INVALID")),
            ("changed-path alias", lambda tree: setattr(tree[0].find("paths/path"), "text", "/alpha/../beta/product.txt")),
            ("changed-path separator", lambda tree: setattr(tree[0].find("paths/path"), "text", "/alpha//product.txt")),
            ("duplicate required author", lambda tree: tree[0].append(copy.deepcopy(tree[0].find("author")))),
        )
        for label, change in log_faults:
            fault = xml_fault("log", change)
            exercise("RV-3094: referenced " + label + " cannot prove product", lambda tool: tool.svn_ship_verdicts(["r1"], None, ["docs/"]), refused, fault)
            exercise("RV-3094: referenced " + label + " refuses through outer Shipped gate", lambda tool: tool.ship_problems([tracker]), outer_refused, fault)
        for field in (".", "logentry", "logentry/paths"):
            for slot in ("text", "tail"):
                fault = xml_fault("log", lambda tree, field=field, slot=slot: setattr(tree.find(field), slot, "LOST LOG DATA"))
                exercise("RV-3094: referenced " + field + " structural " + slot + " cannot prove product", lambda tool: tool.svn_ship_verdicts(["r1"], None, ["docs/"]), refused, fault)
                exercise("RV-3094: referenced " + field + " structural " + slot + " refuses through outer gate", lambda tool: tool.ship_problems([tracker]), outer_refused, fault)
        exercise("RV-3094: formatted scalar path/author/date and surrounding log preserve product", lambda tool: tool.ship_problems([tracker]),
                 lambda value, _starts: value == [], xml_fault("log", formatted))
        blank_log = lambda cmd, _data: b"" if cmd[1] == "log" else None
        exercise("RV-3094: blank successful existing-revision log is missing proof", lambda tool: tool.svn_ship_verdicts(["r1"], None, ["docs/"]), refused, blank_log)
        exercise("RV-3094: blank successful referenced log refuses through outer gate", lambda tool: tool.ship_problems([tracker]), outer_refused, blank_log)
        exercise("RV-3094: checked empty log remains explicit non-success", lambda tool: tool.svn_ship_verdicts(["r1"], None, ["docs/"]),
                 lambda value, _starts: isinstance(value, dict) and bool(value.get("r1")), lambda cmd, _data: b"<log/>" if cmd[1] == "log" else None)
        (consumer / original).write_text(shipped.replace("r1", "r3"), encoding="utf-8")
        exercise("RV-3094: own records plus foreign product refuses through outer gate", lambda tool: tool.ship_problems([tracker]), outer_refused)
        malformed = ("^//", "^/alpha/", "^/alpha//child", "^/./alpha", "^/alpha/..", "^/%2f", "^/%5c", "^/%2e%2e", "^/alpha%", "^/alpha%GG", "^/%FF", "^/%00", "^/alpha<", "^/alpha space", "^/alpha\n^/beta", "^/alpha\n")
        for value in malformed:
            fault = lambda cmd, _data, value=value: (value + "\n").encode() if "relative-url" in cmd else None
            exercise("RV-3094: malformed namespace " + repr(value) + " refuses before classification", lambda tool: tool.svn_ship_verdicts(["r3"], None, ["docs/"]), refused, fault)
            exercise("RV-3094: malformed namespace " + repr(value) + " cannot pass outer gate", lambda tool: tool.ship_problems([tracker]), outer_refused, fault)
        setup("revert", original, cwd=consumer)
        for label, change in log_faults:
            exercise("RV-3094: newest " + label + " refuses even with open local tracker", lambda tool: tool.ship_problems([tracker]), outer_refused, xml_fault("log", change))
        exercise("RV-3094: newest out-of-range product-only revision cannot disappear as a non-move", lambda tool: tool.ship_problems([tracker]), outer_refused,
                 lambda cmd, _data: b'<log><logentry revision="999999"><paths><path action="M">/alpha/product.txt</path></paths></logentry></log>' if cmd[1] == "log" else None)
        exercise("RV-3094: checked nonexistent revision remains explicit non-success", lambda tool: tool.svn_ship_verdicts(["r999999"], None, ["docs/"]),
                 lambda value, _starts: isinstance(value, dict) and bool(value.get("r999999")))
        exercise("RV-3094: genuine repository-root namespace retains own product proof", lambda tool: tool.svn_ship_verdicts(["r1"], None, ["alpha/docs/", "beta/docs/"]),
                 lambda value, _starts: value == {"r1": ""}, home=root)
        external = top / "external-consumer"
        setup("checkout", "-q", server.as_uri() + "/alpha", str(external))
        setup("propset", "svn:externals", "^/beta/docs/work-tracker external", "docs/work-tracker", cwd=external)
        setup("update", "-q", cwd=external)
        exercise("RV-3093: real directory external refuses the foreign tracker view", lambda tool: tool.ship_problems([tracker]), outer_refused, home=external)
        file_external = top / "file-external-consumer"
        setup("checkout", "-q", server.as_uri() + "/alpha", str(file_external))
        setup("propset", "svn:externals", "^/beta/" + original + " foreign.md", "docs/work-tracker", cwd=file_external)
        setup("update", "-q", cwd=file_external)
        exercise("RV-3093: real file external with normal status refuses the foreign view", lambda tool: tool.ship_problems([tracker]), outer_refused, home=file_external)
        if os.name != "nt":
            (consumer / original).unlink(); (consumer / original).symlink_to(root / "beta" / original)
            exercise("RV-3093: real local file alias refuses before reading pending content", lambda tool: tool.ship_problems([tracker]), outer_refused)
            (consumer / original).unlink(); setup("revert", original, cwd=consumer)
        nested_name = "nested space/consumer%name"
        nested = root / nested_name; (nested / original).parent.mkdir(parents=True)
        (nested / original).write_text(text, encoding="utf-8"); (nested / "product.txt").write_text("nested product\n", encoding="utf-8")
        setup("add", "nested space", cwd=root); setup("commit", "-qm", "encoded nested consumer fixture", "--username", "owner", cwd=root)
        revision = setup("info", "--show-item", "revision", "-r", "HEAD", server.as_uri()).strip()
        encoded = top / "encoded-consumer"
        setup("checkout", "-q", server.as_uri() + "/" + urllib.parse.quote(nested_name), str(encoded))
        exercise("RV-3094: legal encoded nested consumer names retain their exact product namespace", lambda tool: tool.svn_ship_verdicts(["r" + revision], None, ["docs/"]),
                 lambda value, _starts: value == {"r" + revision: ""}, home=encoded)
        exercise("RV-3094: nested encoded consumer cannot count another consumer's product", lambda tool: tool.svn_ship_verdicts(["r1"], None, ["docs/"]),
                 lambda value, _starts: isinstance(value, dict) and bool(value.get("r1")), home=encoded)
        # A real merge introduces a copied path; a later merge changes an existing path.
        branch_url = server.as_uri() + "/branch"
        setup("copy", server.as_uri() + "/alpha", branch_url, "-m", "branch fixture", "--username", "owner")
        branch = top / "branch"; setup("checkout", "-q", branch_url, str(branch))
        introduced = "docs/work-tracker/FEAT-003-introduced.md"
        (branch / introduced).write_text(text.replace("FEAT-001", "FEAT-003"), encoding="utf-8")
        setup("add", introduced, cwd=branch); setup("commit", "-qm", "branch introduction", "--username", "intruder", cwd=branch)
        added_revision = setup("info", "--show-item", "revision", "-r", "HEAD", server.as_uri()).strip()
        setup("update", "-q", cwd=consumer)
        setup("merge", "-c", added_revision, branch_url, ".", cwd=consumer)
        setup("commit", "-qm", "merge introduced path", "--username", "owner", cwd=consumer)
        merged_revision = setup("info", "--show-item", "revision", "-r", "HEAD", server.as_uri()).strip()
        exercise("RV-3092: real merge introducing a path retains merged-line refusal", lambda tool: tool.line_author(consumer / introduced, "answer:"),
                 lambda value, _starts: value == (None, None, "merged", merged_revision))
        exercise("RV-3092: unordered required merged revisions are a cached refusal", cached_blame(introduced), cache_refused,
                 xml_fault("log", lambda tree: tree[0].__setitem__(slice(None), [ET.fromstring('<logentry revision="1"/>'), ET.fromstring('<logentry revision="2"/>')]), lambda cmd: "-g" in cmd))
        (branch / original).write_text((branch / original).read_text(encoding="utf-8").replace("answer: keep", "answer: changed"), encoding="utf-8")
        setup("commit", "-qm", "branch guarded line", "--username", "intruder", cwd=branch)
        changed_revision = setup("info", "--show-item", "revision", "-r", "HEAD", server.as_uri()).strip()
        setup("update", "-q", cwd=consumer); setup("merge", "-c", changed_revision, branch_url, ".", cwd=consumer)
        setup("commit", "-qm", "merge existing guarded line", "--username", "owner", cwd=consumer)
        exercise("RV-3092: real merge into an existing path retains the original line author", lambda tool: tool.line_author(consumer / original, "answer:"),
                 lambda value, _starts: value == ("intruder", None, "svn", changed_revision))
        exercise("RV-3092: formatted merged blame retains original scalar author/date", lambda tool: tool.line_author(consumer / original, "answer:"),
                 lambda value, _starts: value == ("intruder", None, "svn", changed_revision), xml_fault("blame", formatted))
        lower = setup("info", "--show-item", "revision", "-r", "HEAD", server.as_uri()).strip()
        for step in ("one", "two"):
            (branch / "product.txt").write_text("branch product " + step + "\n", encoding="utf-8")
            setup("commit", "-qm", "branch product " + step, "--username", "owner", cwd=branch)
        upper = setup("info", "--show-item", "revision", "-r", "HEAD", server.as_uri()).strip()
        setup("update", "-q", cwd=consumer); setup("merge", "-r", lower + ":" + upper, branch_url, ".", cwd=consumer)
        setup("commit", "-qm", "multiple merged revisions", "--username", "owner", cwd=consumer)
        forward = setup("info", "--show-item", "revision", "-r", "HEAD", server.as_uri()).strip()
        exercise("RV-3092: real multi-revision merge keeps readable ordered merge proof", lambda tool: tool.svn_merged(int(forward)), lambda value, _starts: value is True)
        setup("update", "-q", cwd=consumer); setup("merge", "-r", upper + ":" + lower, branch_url, ".", cwd=consumer)
        setup("commit", "-qm", "reverse merged revisions", "--username", "owner", cwd=consumer)
        reverse = setup("info", "--show-item", "revision", "-r", "HEAD", server.as_uri()).strip()
        exercise("RV-3092: real reverse merge retains readable merge proof", lambda tool: tool.svn_merged(int(reverse)), lambda value, _starts: value is True)


INFO_115 = "<wc-compatible-version>1.15</wc-compatible-version><wc-format>32</wc-format><store-pristine>yes</store-pristine>"


def info_document(fields=""):
    """One `svn info --xml` entry in the shape svn 1.14.5 prints, `fields` placed after `wcroot-abspath` as 1.15.0's info.rnc orders them."""
    return ('<?xml version="1.0" encoding="UTF-8"?>\n<info>\n<entry kind="file" path="docs/work-tracker/FEAT-001-item.md" revision="3">\n'
            "<url>file:///srv/repo/alpha/docs/work-tracker/FEAT-001-item.md</url>\n<relative-url>^/alpha/docs/work-tracker/FEAT-001-item.md</relative-url>\n"
            "<repository>\n<root>file:///srv/repo</root>\n<uuid>0f1e2d3c-4b5a-6978-8796-a5b4c3d2e1f0</uuid>\n</repository>\n"
            "<wc-info>\n<wcroot-abspath>/srv/wc</wcroot-abspath>\n" + fields + "<schedule>normal</schedule>\n<depth>infinity</depth>\n"
            "<text-updated>2026-10-16T06:00:00.000000Z</text-updated>\n<checksum>0123456789abcdef0123456789abcdef</checksum>\n</wc-info>\n"
            '<commit revision="2">\n<author>owner</author>\n<date>2026-10-16T06:00:00.000000Z</date>\n</commit>\n</entry>\n</info>\n')


def with_info_fields(data, fields):
    """`svn info --xml` output as Subversion 1.15.0 prints it: `fields` in every `wc-info`, after its `wcroot-abspath`."""
    tree = ET.fromstring(data)
    for wc in tree.iter("wc-info"):
        at = next((i + 1 for i, child in enumerate(wc) if child.tag == "wcroot-abspath"), 0)
        for offset, field in enumerate(list(ET.fromstring("<f>" + fields + "</f>"))):
            wc.insert(at + offset, field)
    return ET.tostring(tree)


def run_shape_controls(fm, check, env, programs):
    """The structural proof accepts each Subversion output variant CI's runners print, exactly: one class row for each, and a
    mutant for each that a malformed variant is still refused. Subversion 1.15.0 (macOS, Homebrew): `svn info --xml` adds
    `wc-compatible-version`, `wc-format` and `store-pristine` to `wc-info` (its info.rnc; its status, log, blame and common
    schemas are 1.14.5's but for log's `reverse-merge` attribute, which the log reader already reads)."""
    def proved(document, kind="info"):
        try:
            fm.svn_xml_proof(ET.fromstring(document), kind)
        except fm.SvnUnreadable:
            return False
        return True

    check("FM-044 shape: Subversion 1.14.5 info, with none of the 1.15 fields, is accepted", proved(info_document()))
    for label, fields in (("1.15.0 info fields, store-pristine yes", INFO_115),
                          ("1.15.0 info fields, store-pristine no", INFO_115.replace(">yes<", ">no<")),
                          ("1.15.0 info fields of an older format", INFO_115.replace(">1.15<", ">1.8<").replace(">32<", ">31<")),
                          ("1.15.0 info fields with a three-part version", INFO_115.replace(">1.15<", ">1.15.0<"))):
        check("FM-044 shape: class row, Subversion " + label + ", is accepted", proved(info_document(fields)))
    for label, document, kind in (
            ("a format that is not a number", info_document(INFO_115.replace(">32<", ">32a<")), "info"),
            ("an empty format", info_document(INFO_115.replace(">32<", "><")), "info"),
            ("a pristine store neither yes nor no", info_document(INFO_115.replace(">yes<", ">maybe<")), "info"),
            ("a compatible version that is not a version", info_document(INFO_115.replace(">1.15<", ">one<")), "info"),
            ("a compatible version holding an element", info_document(INFO_115.replace(">1.15<", ">1.15<b/><")), "info"),
            ("a format field twice", info_document(INFO_115 + "<wc-format>31</wc-format>"), "info"),
            ("a format field outside wc-info", info_document().replace("<url>", "<wc-format>32</wc-format><url>"), "info"),
            ("text after a format field", info_document(INFO_115.replace("</store-pristine>", "</store-pristine>LOST FORMAT DATA")), "info"),
            ("an unknown field beside them", info_document(INFO_115 + "<wc-flavour>x</wc-flavour>"), "info"),
            ("a format field in svn status", '<status><target path="."><entry path="x.md"><wc-status item="normal" props="none" revision="1">'
                                             "<wc-format>32</wc-format></wc-status></entry></target></status>", "status")):
        check("FM-044 shape: mutant, Subversion 1.15.0 " + label + ", is refused", not proved(document, kind))
    if not programs["svn"] or not programs["svnadmin"]:
        print("  SKIP FM-044 shape: real Subversion reads with the 1.15.0 info fields need svn and svnadmin")
        return
    actual_run = subprocess.run
    with tempfile.TemporaryDirectory() as temp:
        top = Path(temp).resolve(); server = top / "server"; consumer = top / "consumer"
        setup = lambda *args, cwd=None: actual_run([programs["svn"], *args], cwd=cwd, env=env, check=True, capture_output=True)
        actual_run([programs["svnadmin"], "create", str(server)], env=env, check=True, capture_output=True)
        setup("checkout", "-q", server.as_uri(), str(consumer))
        original, copied = "docs/work-tracker/FEAT-001-item.md", "docs/work-tracker/FEAT-002-copy.md"
        (consumer / original).parent.mkdir(parents=True)
        (consumer / original).write_text("---\nid: FEAT-001\nstatus: Proposed\nanswer: keep\n---\n\n# Fixture\n", encoding="utf-8")
        (consumer / "shoalmark.toml").write_text('owner = "owner"\n', encoding="utf-8")
        setup("add", "docs", "shoalmark.toml", cwd=consumer); setup("commit", "-qm", "filed", "--username", "owner", cwd=consumer)
        setup("copy", original, copied, cwd=consumer); setup("commit", "-qm", "copied", "--username", "copier", cwd=consumer)
        setup("update", "-q", cwd=consumer)

        def read(fields):
            """The copy's blame and its answer line's author, and the original's `svn_new`, every `svn info --xml` answer given `fields`."""
            def answered(cmd, *args, **kwargs):
                done = actual_run(cmd, *args, **kwargs)
                if fields is not None and cmd[0] == "svn" and cmd[1] == "info" and "--xml" in cmd and done.returncode == 0:
                    return subprocess.CompletedProcess(cmd, 0, with_info_fields(done.stdout, fields), done.stderr)
                return done
            with patch.object(fm.subprocess, "run", side_effect=answered):
                fm.configure(consumer)
                try:
                    return fm.svn_blame(copied), fm.line_author(consumer / copied, "answer:")[:1], fm.svn_new(original)
                except fm.SvnUnreadable as error:
                    return error

        plain = read(None)
        check("FM-044 shape: real Subversion 1.14.5 reads credit the copy to its copier", isinstance(plain, tuple) and plain[1] == ("copier",) and plain[2] is False)
        check("FM-044 shape: class row, real reads with the 1.15.0 info fields read as 1.14.5's", read(INFO_115) == plain)
        check("FM-044 shape: mutant, real reads with a 1.15.0 format that is not a number are refused",
              isinstance(read(INFO_115.replace(">32<", ">x<")), fm.SvnUnreadable))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, default=HERE / "shoalmark.py")
    args = parser.parse_args()
    spec = importlib.util.spec_from_file_location("guard_tool", args.source)
    fm = importlib.util.module_from_spec(spec); spec.loader.exec_module(fm)
    failures, count = [], 0

    def check(label, ok):
        nonlocal count
        count += 1
        print("  " + ("ok  " if ok else "FAIL") + " " + label)
        if not ok:
            failures.append(label)

    run_guard_controls(fm, check)
    print(str(count - len(failures)) + "/" + str(count) + " B guard controls passed")
    return bool(failures)


if __name__ == "__main__":
    raise SystemExit(main())
