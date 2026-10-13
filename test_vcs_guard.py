"""FM-044 B guard controls: real consumer repositories, narrow adapter and retained Git proof.

Run directly, or call run_guard_controls(tool, check) from the integrating suite.
Local file:// SVN usernames are fixture mechanics, never deployed authentication proof.
These controls do not establish an adopted SVN consumer authority or public-entry wiring.
"""

import argparse
import builtins
from contextlib import ExitStack
from contextlib import redirect_stderr
import importlib.util
import io
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
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

            # This is the pure protected-text comparison seam, not public-entry acceptance.
            with patch.dict(os.environ, {"PATH": str(restricted)}), patch.object(fm.subprocess, "Popen", side_effect=AssertionError("local comparison must start nothing")):
                before = view(TRIAGE)
                passes = view(TRIAGE.replace("*None yet.*", "2026-10-13: an ordinary pass."))
                check("FM-044 B: real SVN local Passes-only comparison needs no server or authority claim", fm.section_changes(passes, [before]) == [])
                scaffold = fm.TRIAGE_HOME.format(cmd="shoalmark", **fm.DEFAULTS["headings"])
                check("FM-044 B: known scaffold comparison makes no protected statement", fm.section_changes(view(scaffold), [view(None)]) == [])
                check("FM-044 B: actual protected local text differs independently of missing authority", bool(fm.section_changes(view(TRIAGE.replace("lose a loan", "lose a key")), [before])))
    finally:
        fm.configure(previous)


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
