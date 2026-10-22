"""FM-044: bounded CLI capability and copied-command controls.

The pure API is not main-entry integration or full SVN qualification. Fixtures use real
Git and SVN for setup; a separate production process runs in an SVN WC without Git.
"""

import contextlib
import importlib.util
import io
import json
import os
from pathlib import Path
import shlex
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch


HERE = Path(__file__).resolve().parent
SPEC = importlib.util.spec_from_file_location("cli_fm", HERE / "shoalmark.py")
fm = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(fm)

# The signed scope retains this existing main order; the expectations are explicit,
# rather than read back from the implementation's declaration.
OPERATIONS = (
    ("vendor", ["--vendor", "tool"]), ("brand", ["--brand"]), ("init", ["--init"]),
    ("install_hook", ["--install-hook"]), ("session_trailer", ["--session-trailer", "message"]),
    ("whoami", ["--whoami"]), ("session_check", ["--session-check"]), ("commit_msg", ["--commit-msg", "message"]),
    ("session", ["--session", "new"]), ("sessions", ["--sessions"]), ("ratio", ["--ratio"]),
    ("ratio_window", ["--since", "2026-10-01"]), ("queue", ["--queue"]), ("schema", ["--schema"]),
    ("new", ["--new", "FM", "title"]), ("invite", ["--invite", "FM-044"]), ("notify", ["--notify"]),
    ("owner", ["--owner"]), ("answered", ["--answered"]), ("answer", ["--answer", "FM-044", "accept"]),
    ("done", ["--done", "FM-044", "where"]), ("due", ["--due", "FM-044", "2026-10-14T12:00Z"]),
    ("revoke", ["--revoke", "FM-044", "why"]), ("clear_ask", ["--clear-ask", "FM-044", "build"]),
    ("standup", ["--standup"]), ("next", ["--next"]), ("triage", ["--triage"]),
    ("related", ["--related", "FM-044"]),
)
GIT_ONLY = {"session_trailer": 4, "whoami": 4, "session_check": 4, "commit_msg": 4, "sessions": 4,
            "queue": 3, "answer": 4, "done": 4, "due": 4, "revoke": 4}
REMOVED = ("ratio", "ratio_window")       # R13 removed `--ratio`, `--since` and `--until`: each is named, exit 2, on every backend
TOKENS = ("", "FM-044", "two words", "O'Brien", 'say "yes"', "C:\\Program Files\\O'Brien\\result.txt",
          '$env:USERPROFILE; $(Write-Output "x")', "`a · Grüße", "a\nb\tc", "*?[x]", "--leading", "$(touch nope)")


class CliControls(unittest.TestCase):
    def tearDown(self):
        fm.configure(HERE)

    def test_selected_handlers_and_default_modes(self):
        for name, argv in OPERATIONS:
            with self.subTest(operation=name):
                self.assertEqual(fm.cli_operation(fm.parse_args(argv)), name)
        self.assertEqual(fm.cli_operation(fm.parse_args([])), "write")
        self.assertEqual(fm.cli_operation(fm.parse_args(["--check"])), "check")

    def test_earlier_selected_operation_retains_precedence(self):
        for position, (name, argv) in enumerate(OPERATIONS):
            for later_name, later_argv in OPERATIONS[position + 1:]:
                with self.subTest(selected=name, ignored=later_name):
                    args = fm.parse_args(argv + later_argv)
                    self.assertEqual(fm.cli_operation(args), name)
                    diagnostic, code = fm.cli_preflight(args, "svn")
                    expected = GIT_ONLY.get(name, 2 if name in REMOVED else 0)
                    self.assertEqual(code, expected)
                    self.assertEqual(diagnostic is None, expected == 0)

    def test_empty_and_nonempty_optional_values_remain_selected(self):
        for argv, expected in ((["--brand", "", "--queue"], "brand"),
                               (["--standup", "", "--next"], "standup"),
                               (["--standup", "agenda.ics", "--triage"], "standup")):
            self.assertEqual(fm.cli_operation(fm.parse_args(argv)), expected)
        self.assertEqual(fm.cli_operation(fm.parse_args(["--vendor", "", "--queue"])), "queue")

    def test_ratio_window_barrier_remains_after_earlier_handlers(self):
        for backend in ("git", "svn"):
            self.assertEqual(fm.cli_preflight(fm.parse_args(["--until", "2026-10-14", "--queue"]), backend),
                             ("--until: R13, the Owner's ruling of 12 October, removed it with --ratio — no counting view replaces it until the receipts ship", 2))
            self.assertEqual(fm.cli_preflight(fm.parse_args(["--ratio", "--queue"]), backend),
                             ("--ratio: R13, the Owner's ruling of 12 October, removed it — no counting view replaces it until the receipts ship", 2))
            self.assertEqual(fm.cli_preflight(fm.parse_args(["--init", "--until", "2026-10-14", "--queue"]), backend), (None, 0))

    def test_git_admission_continues_existing_handler_proof(self):
        for name, argv in OPERATIONS:
            if name not in REMOVED:
                self.assertEqual(fm.cli_preflight(fm.parse_args(argv), "git"), (None, 0))

    def test_each_selected_git_only_refusal_is_one_line_with_retained_code(self):
        for name, argv in OPERATIONS:
            if name in GIT_ONLY:
                diagnostic, code = fm.cli_preflight(fm.parse_args(argv), "svn")
                self.assertEqual(code, GIT_ONLY[name])
                self.assertEqual(len(diagnostic.splitlines()), 1)
                self.assertTrue(diagnostic.startswith("--" + name.replace("_", "-") + ":"))

    def test_pure_api_does_not_discover_read_start_print_or_write(self):
        arguments = [fm.parse_args(argv) for _, argv in OPERATIONS]
        out, err = io.StringIO(), io.StringIO()
        with patch.object(fm, "vcs", side_effect=AssertionError("backend discovery")), \
             patch.object(fm.subprocess, "run", side_effect=AssertionError("process")), \
             patch.object(Path, "read_text", side_effect=AssertionError("read")), \
             patch.object(Path, "write_text", side_effect=AssertionError("write")), \
             contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            for args in arguments:
                fm.cli_operation(args)
                fm.cli_preflight(args, "svn")
        self.assertEqual((out.getvalue(), err.getvalue()), ("", ""))

    def test_shared_session_removed_words_and_usage_remain(self):
        with patch.object(fm, "vcs", return_value="svn"), patch.object(fm, "session_rows", side_effect=AssertionError("Git history")):
            for words, expected in ((["new"], 0), (["open"], 2), (["close"], 2), (["nonsense"], 4), (["new", "extra"], 4)):
                out, err = io.StringIO(), io.StringIO()
                with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
                    self.assertEqual(fm.session_cmd(words), expected)
                if expected == 0:
                    self.assertRegex(out.getvalue(), r"^[0-9a-f]{8}\n$")

    def test_posix_spelling_matches_shlex_exactly(self):
        with patch.object(fm.sys, "platform", "darwin"):
            for token in TOKENS:
                self.assertEqual(fm.printed_arg(token), shlex.quote(token))

    def test_powershell_literal_spelling_and_literal_recovery(self):
        with patch.object(fm.sys, "platform", "win32"):
            for token in TOKENS:
                spelling = fm.printed_arg(token)
                self.assertEqual(spelling, "'" + token.replace("'", "''") + "'")
                self.assertEqual(spelling[1:-1].replace("''", "'"), token)

    @unittest.skipUnless(shutil.which("sh"), "POSIX shell unavailable")
    def test_real_posix_shell_preserves_single_argument_bytes(self):
        if sys.platform == "win32":                        # read here, before the patch below reports "darwin" (RV-3233)
            self.skipTest("a POSIX shell is what it means; Windows' `sh` is MSYS's, which rewrites path-like arguments")
        with tempfile.TemporaryDirectory() as directory:
            capture = Path(directory) / "capture argv.py"
            capture.write_text("import json,sys; print(json.dumps(sys.argv[1:],ensure_ascii=False))\n", encoding="utf-8")
            with patch.object(fm.sys, "platform", "darwin"):
                for token in TOKENS:
                    command = " ".join((shlex.quote(sys.executable), shlex.quote(str(capture)), fm.printed_arg(token)))
                    result = subprocess.run([shutil.which("sh"), "-c", command], capture_output=True, text=True, encoding="utf-8", check=True)
                    self.assertEqual(json.loads(result.stdout), [token])
            self.assertFalse((Path(directory) / "nope").exists())

    def test_retry_commands_keep_configured_prefix_and_normalized_arguments(self):
        prefix = "python3 tools/shoalmark.py"
        text = 'O\'Brien $HOME; $(echo yes) "same"'
        tracker = {"id": "FM-044", "file": "FM-044-test.md", "title": "test", "status": "In Progress",
                   "ask": "a decision", "ask_kind": "ruling", "next": "owner", "due": "2026-10-14T12:00Z"}
        captures = []
        with patch.object(fm, "CMD", prefix), patch.object(fm, "vcs", return_value="git"), \
             patch.object(fm, "owner_change", side_effect=lambda _id, _tracker, how: captures.append(how) or 0), \
             patch.object(fm, "result_facts", return_value=""), \
             patch.object(fm.subprocess, "run", return_value=subprocess.CompletedProcess([], 128, "", "")):
            for platform in ("darwin", "win32"):
                with patch.object(fm.sys, "platform", platform):
                    fm.answer_cmd(["fm-044", "accept", text], [tracker])
                    self.assertTrue(captures[-1]["again"].startswith(prefix + " --answer "))
                    self.assertEqual(captures[-1]["again"], f"{prefix} --answer {fm.printed_arg('FM-044')} accept {fm.printed_arg(text)}")
                    fm.done_cmd(["fm-044", text], [tracker])
                    self.assertEqual(captures[-1]["again"], f"{prefix} --done {fm.printed_arg('FM-044')} {fm.printed_arg(text.replace(chr(34), chr(39)))}")
                    fm.due_cmd(["fm-044", "2026-10-14T12:00Z"], [tracker])
                    self.assertEqual(captures[-1]["again"], f"{prefix} --due {fm.printed_arg('FM-044')} {fm.printed_arg('2026-10-14T12:00Z')}")
                    fm.revoke_cmd(["fm-044", text], [{**tracker, "done": "2026-10-13T12:00Z · result"}])
                    self.assertEqual(captures[-1]["again"], f"{prefix} --revoke {fm.printed_arg('FM-044')} {fm.printed_arg(text.replace(chr(34), chr(39)))}")

    def test_rv_3095_seed_report_preserves_existing_due_and_quotes_its_retry(self):
        """RV-3095: a differing existing due reports a retry rather than falling through."""
        prefix, tid = "python3 tools/shoalmark.py", "FM-044 O'Brien"
        when, words = "2026-10-14T12:30:00+02:00", "2026-10-14T12:30:00+02:00"
        cases = (("2026-10-13T12:30:00+02:00", "different"),
                 ("2026-10-14T10:30:00Z", "equal"), ("", "absent"))
        with patch.object(fm, "CMD", prefix):
            for platform in ("darwin", "win32"):
                quote = shlex.quote if platform == "darwin" else lambda token: "'" + token.replace("'", "''") + "'"
                for had, kind in cases:
                    with self.subTest(platform=platform, due=kind), patch.object(fm.sys, "platform", platform):
                        seed = {"when": when, "words": words, "had": had}
                        before = seed.copy()
                        report = fm.seed_said(tid, seed)
                        self.assertEqual(seed, before)
                        self.assertIsInstance(report, str)
                        if kind == "different":
                            retry = f"{prefix} --due {quote(tid)} {quote(when)}"
                            self.assertEqual(report, f"\n  your answer names {when} (`{words}`); `due:` is {had} already and is left — `{retry}` moves it")
                            if platform == "darwin":
                                self.assertEqual(shlex.split(retry), ["python3", "tools/shoalmark.py", "--due", tid, when])
                            else:
                                self.assertEqual(quote(tid)[1:-1].replace("''", "'"), tid)
                                self.assertEqual(quote(when)[1:-1].replace("''", "'"), when)
                        elif kind == "equal":
                            self.assertEqual(report, f"\n  due: {had} — your answer names the same time")
                            self.assertNotIn("--due", report)
                        else:
                            self.assertEqual(report, f"\n  due: {when} — read from your answer's `{words}`, written with it; `{prefix} --due {quote(tid)} <time>` moves it")

    def test_rv_3095_actual_answer_date_write_and_said_callbacks(self):
        """RV-3095: actual action-answer callbacks preserve a due already set and finish their report."""
        prefix, when = "python3 tools/shoalmark.py", "2026-10-14T12:30:00+02:00"
        cases = (("2026-10-13T12:30:00+02:00", "different"),
                 ("2026-10-14T10:30:00Z", "equal"), ("", "absent"))
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            path = root / "FM-044-test.md"
            for platform in ("darwin", "win32"):
                quote = shlex.quote if platform == "darwin" else lambda token: "'" + token.replace("'", "''") + "'"
                for had, kind in cases:
                    with self.subTest(platform=platform, due=kind):
                        original = ("---\nid: FM-044\nstatus: In Progress\nnext: owner\n"
                                    "ask: Will you act at the proposed hour?\nask-kind: action\n"
                                    + (f"due: {had}\n" if had else "") + "---\n\n# FM-044 — control\n")
                        path.write_text(original, encoding="utf-8")
                        tracker = {"id": "FM-044", "file": path.name, "status": "In Progress",
                                   "ask": "Will you act at the proposed hour?", "ask_kind": "action", "next": "owner"}
                        if had:
                            tracker["due"] = had
                        before = tracker.copy()
                        callbacks = []

                        def exercise_callbacks(tid, given, how):
                            self.assertEqual(tid, "FM-044")
                            self.assertIs(given, tracker)
                            self.assertEqual(how["check"](), "")
                            lines, why = how["write"](original.split("\n"), "Owner fixture", "answer/fm-044")
                            self.assertEqual(why, "")
                            front, _ = fm.parse_frontmatter("\n".join(lines))
                            self.assertEqual(front["due"], had or when)
                            self.assertEqual(front["answer"], f'"accepted - {when}"')
                            self.assertEqual(front["answered-by"], "Owner fixture")
                            self.assertEqual(front["next"], "owner")
                            callbacks.append("write")
                            report = how["said"]("answer/fm-044", " — not pushed in this control", fm.PROOF_SAID["author"])
                            self.assertIsInstance(report, str)
                            callbacks.append("said")
                            self.assertIn(f"FM-044 answered: accepted - {when}\n", report)
                            if kind == "different":
                                self.assertIn(f"`due:` is {had} already and is left", report)
                                retry = f"{prefix} --due {quote(tid)} {quote(when)}"
                                self.assertIn(f"`{retry}` moves it", report)
                                if platform == "darwin":
                                    self.assertEqual(shlex.split(retry), ["python3", "tools/shoalmark.py", "--due", tid, when])
                            elif kind == "equal":
                                self.assertIn(f"due: {had} — your answer names the same time", report)
                            else:
                                self.assertIn(f"due: {when} — read from your answer's", report)
                            return 0

                        with patch.object(fm, "ROOT", root), patch.object(fm, "TRACKER_DIR", root), \
                             patch.object(fm, "CMD", prefix), patch.object(fm.sys, "platform", platform), \
                             patch.object(fm, "vcs", return_value="git"), \
                             patch.object(fm, "owner_change", side_effect=exercise_callbacks), \
                             patch.object(fm.subprocess, "run", side_effect=AssertionError("answer control must not launch a process")):
                            self.assertEqual(fm.answer_cmd(["fm-044", "accept", when], [tracker]), 0)
                        self.assertEqual(callbacks, ["write", "said"])
                        self.assertEqual(tracker, before)
                        self.assertEqual(path.read_text(encoding="utf-8"), original)

    @unittest.skipUnless(shutil.which("git"), "Git fixture tool unavailable")
    def test_real_git_identity_cache_rebind_missing_objects_and_message_trailers(self):
        with tempfile.TemporaryDirectory() as directory:
            roots = [Path(directory) / "first", Path(directory) / "second"]
            env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
            for root, name in zip(roots, ("First identity", "Second identity")):
                subprocess.run([shutil.which("git"), "init", "-q", str(root)], check=True, capture_output=True, env=env)
                for key, value in (("user.name", name), ("user.email", "fixture@example.invalid"), ("seat.session", "12345678"),
                                   ("commit.gpgsign", "false")):
                    subprocess.run([shutil.which("git"), "-C", str(root), "config", key, value], check=True, capture_output=True, env=env)
                (root / "file.txt").write_text("fixture\n", encoding="utf-8")
                subprocess.run([shutil.which("git"), "-C", str(root), "add", "file.txt"], check=True, capture_output=True, env=env)
                subprocess.run([shutil.which("git"), "-C", str(root), "commit", "-qm", "fixture"], check=True, capture_output=True, env=env)
            with patch.dict(os.environ, env, clear=True):
                fm.configure(roots[0])
                self.assertEqual(fm.git_user(), "First identity")
                subprocess.run([shutil.which("git"), "-C", str(roots[0]), "config", "user.name", "Changed identity"], check=True, capture_output=True, env=env)
                self.assertEqual(fm.git_user(), "First identity")
                fm.configure(roots[1])
                self.assertEqual(fm.git_user(), "Second identity")
                fm.configure(roots[0])
                self.assertEqual(fm.git_user(), "Changed identity")
                head = subprocess.check_output([shutil.which("git"), "-C", str(roots[0]), "rev-parse", "HEAD"], env=env, text=True).strip()
                absent = "0" * 40
                self.assertEqual(fm.have_not([head, absent]), [absent])
                message = roots[0] / "commit message.txt"
                message.write_text("fixture subject\n", encoding="utf-8")
                with patch.object(fm, "harness_id", return_value=""), contextlib.redirect_stderr(io.StringIO()):
                    self.assertEqual(fm.session_trailer(str(message)), 0)
                    self.assertEqual(fm.session_trailer(str(message)), 0)
                text = message.read_text(encoding="utf-8")
                self.assertEqual(text.count("Session: 12345678"), 1)
                self.assertEqual(text.count("Worktree: first"), 1)
                out = io.StringIO()
                with patch.object(fm, "harness_reading", return_value=(None, "")), contextlib.redirect_stdout(out):
                    self.assertEqual(fm.whoami(), 0)
                self.assertIn("From: 12345678 fixture@example.invalid (first)", out.getvalue())

    @unittest.skipUnless(shutil.which("svn") and shutil.which("svnadmin"), "SVN fixture tools unavailable")
    def test_real_svn_wc_policy_and_session_new_without_git_or_any_process(self):
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            repo, wc, empty_path = base / "repository", base / "working copy", base / "empty PATH"
            empty_path.mkdir()
            subprocess.run([shutil.which("svnadmin"), "create", str(repo)], check=True, capture_output=True)
            subprocess.run([shutil.which("svn"), "checkout", repo.as_uri(), str(wc)], check=True, capture_output=True)
            script = base / "production_control.py"
            script.write_text("""import contextlib,importlib.util,io,json,sys
attempts=[]
def audit(event,args):
    if event=='subprocess.Popen':
        attempts.append(str(args[0])); raise AssertionError('unexpected production process')
sys.addaudithook(audit)
spec=importlib.util.spec_from_file_location('production',sys.argv[1])
fm=importlib.util.module_from_spec(spec); spec.loader.exec_module(fm)
assert fm.vcs()=='svn'
results=[]
for argv in json.loads(sys.argv[2]):
    results.append(fm.cli_preflight(fm.parse_args(argv),fm.vcs()))
class UnreadableTrackers:
    def __iter__(self): raise AssertionError('tracker iteration before capability refusal')
trackers=UnreadableTrackers()
handlers=[('session_trailer',lambda:fm.session_trailer('must not read or write')),
          ('whoami',fm.whoami),('sessions',fm.sessions_cmd),('queue',fm.queue_cmd),
          ('answer',lambda:fm.answer_cmd(['FM-044','accept'],trackers)),
          ('done',lambda:fm.done_cmd(['FM-044','result'],trackers)),
          ('due',lambda:fm.due_cmd(['FM-044','2026-10-14T12:00Z'],trackers)),
          ('revoke',lambda:fm.revoke_cmd(['FM-044','reason'],trackers)),
          ('answer',lambda:fm.owner_change('FM-044',None,{'flag':'--answer'}))]
direct=[]
for name,handler in handlers:
    stdout,stderr=io.StringIO(),io.StringIO()
    with contextlib.redirect_stdout(stdout),contextlib.redirect_stderr(stderr):
        result=handler()
    direct.append([name,result,stdout.getvalue(),stderr.getvalue()])
presentations=[]
for label in ('','<you>'):
    text='---\\nid: FEAT-001\\nstatus: Proposed\\nhook: test\\nanswer: accepted\\nanswered-by: '+label+'\\n---\\n\\n# FEAT-001 — test\\n'
    presentations.append(fm.extract(fm.TRACKER_DIR/'FEAT-001-test.md',text)['answered_by'])
out=io.StringIO()
with contextlib.redirect_stdout(out):
    code=fm.session_cmd(['new'])
print(json.dumps({'backend':fm.vcs(),'results':results,'direct':direct,'presentations':presentations,
                  'session':out.getvalue(),'code':code,'attempts':attempts}))
""", encoding="utf-8")
            before = {p.relative_to(wc).as_posix(): p.read_bytes() for p in wc.rglob("*") if p.is_file()}
            cases = [(name, argv) for name, argv in OPERATIONS if name in GIT_ONLY]
            env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
            env.update(PATH=str(empty_path), PYTHONDONTWRITEBYTECODE="1")
            result = subprocess.run([sys.executable, "-B", str(script), str(HERE / "shoalmark.py"), json.dumps([argv for _, argv in cases])],
                                    cwd=wc, env=env, capture_output=True, text=True, encoding="utf-8", check=True)
            observed = json.loads(result.stdout)
            self.assertEqual(observed["backend"], "svn")
            self.assertEqual(observed["attempts"], [])
            self.assertEqual([r[1] for r in observed["results"]], [GIT_ONLY[name] for name, _ in cases])
            for name, code, stdout, stderr in observed["direct"]:
                self.assertEqual(code, GIT_ONLY[name])
                self.assertEqual(stdout, "")
                self.assertEqual(len(stderr.splitlines()), 1)
            self.assertEqual(observed["presentations"], ["", ""])
            self.assertEqual(observed["code"], 0)
            self.assertRegex(observed["session"], r"^[0-9a-f]{8}\n$")
            after = {p.relative_to(wc).as_posix(): p.read_bytes() for p in wc.rglob("*") if p.is_file()}
            self.assertEqual(before, after)


if __name__ == "__main__":
    unittest.main(verbosity=2)
