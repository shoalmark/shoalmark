import contextlib
import io
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

import test_vcs_entry as entry


HERE = Path(__file__).resolve().parent


def project_property(value, kind):
    # CString::Tokenize skips empty LF-delimited tokens; the parser consumes a type even in release builds.
    lines = [line for line in value.split("\n") if line]
    if len(lines) < 4 or lines[0] != kind + "_commit_hook":
        return None
    command = lines[1]
    start = command.find("%REPOROOT%")
    if start < 0:
        return None
    end = command.find('"' if start and command[start - 1] == '"' else " ", start)
    if end < 0:
        end = len(command)
    script = command[start:end]
    return script, command.replace(script, "C:\\working copy\\" + script[len("%REPOROOT%/"):].replace("/", "\\")), lines[2].lower() == "true", lines[3].lower() == "show"


def installed_properties(source, base):
    server = base / "server"; root = base / "working copy"
    entry.command(base, "svnadmin", "create", str(server))
    entry.command(base, "svn", "checkout", "-q", server.as_uri(), str(root))
    entry.corpus(root)
    entry.command(root, "svn", "add", "-q", "shoalmark.toml", "work-tracker")
    tool = entry.tool_copy(root, source, HERE)
    tool.parent.rename(tool.parent.with_name("field tool"))
    tool = tool.parent.with_name("field tool") / tool.name
    env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
    def install():
        return subprocess.run([sys.executable, str(tool), "--root", str(root), "--install-hook"],
                              cwd=base, env=env, capture_output=True, text=True, encoding="utf-8", timeout=30)
    first = install()
    if first.returncode:
        raise AssertionError(first.stderr)
    properties = {kind: entry.command(root, "svn", "propget", "--strict", "tsvn:" + kind + "commithook", ".") for kind in ("start", "pre")}
    return root, tool, install, properties


def property_contract(properties):
    import shoalmark
    for kind, value in properties.items():
        parsed = project_property(value, kind)
        if parsed is None:
            return False
        script, command, wait, show = parsed
        if (script != "%REPOROOT%/tools/field tool/shoalmark.py" or not wait or show
                or shoalmark.split_cmdline(command) != ["python", r"C:\working copy\tools\field tool\shoalmark.py", "--tsvn-hook", kind]):
            return False
    return True


def four_line_upgrade(source, base):
    root, tool, install, properties = installed_properties(source, base)
    for kind, value in properties.items():
        old = value.replace('"', "")
        if kind == "start":
            old = " \n" + old + " \n"
        entry.command(root, "svn", "propset", "--", "tsvn:" + kind + "commithook", old, ".")
    upgraded = install()
    actual = {kind: entry.command(root, "svn", "propget", "--strict", "tsvn:" + kind + "commithook", ".") for kind in properties}
    repeated = install()
    return upgraded.returncode == 0 and actual == properties and repeated.returncode == 0 and "set " not in repeated.stdout


@unittest.skipUnless(shutil.which("svn") and shutil.which("svnadmin"), "svn and svnadmin are required")
class PropertyControls(unittest.TestCase):
    def test_unquoted_four_line_upgrade_and_repeat(self):
        with tempfile.TemporaryDirectory(prefix="tsvn-four-line-") as temp:
            self.assertTrue(four_line_upgrade(HERE / "shoalmark.py", Path(temp).resolve()))

    def test_unquoted_four_line_mutant_fails_same_control(self):
        with tempfile.TemporaryDirectory(prefix="tsvn-four-line-mutant-") as temp:
            base = Path(temp).resolve()
            source = (HERE / "shoalmark.py").read_text(encoding="utf-8")
            before = "(legacy.strip(), unquoted.strip(), value.strip())"
            self.assertEqual(source.count(before), 1)
            mutant = base / "mutant.py"
            mutant.write_text(source.replace(before, "(legacy.strip(), value.strip())"), encoding="utf-8")
            self.assertFalse(four_line_upgrade(mutant, base))

    def test_installed_properties_and_legacy_upgrade(self):
        with tempfile.TemporaryDirectory(prefix="tsvn-properties-") as temp:
            base = Path(temp).resolve()
            root, tool, install, properties = installed_properties(HERE / "shoalmark.py", base)
            self.assertTrue(property_contract(properties))
            self.assertNotIn("set tsvn:", install().stdout)
            for kind, value in properties.items():
                old = value.split("\n", 1)[1].replace('"', "")
                entry.command(root, "svn", "propset", "--", "tsvn:" + kind + "commithook", old, ".")
            self.assertEqual(install().returncode, 0)
            self.assertEqual({kind: entry.command(root, "svn", "propget", "--strict", "tsvn:" + kind + "commithook", ".") for kind in properties}, properties)
            foreign = "pre_commit_hook\nwscript other.js --tsvn-hook pre\ntrue\nhide\n"
            entry.command(root, "svn", "propset", "--", "tsvn:precommithook", foreign, ".")
            refusal = install()
            self.assertEqual(refusal.returncode, 4)
            self.assertIn("tsvn:precommithook is set and is not shoalmark's — left alone.", refusal.stderr)
            self.assertNotIn("Add to it", refusal.stderr)
            self.assertNotIn("--tsvn-hook", refusal.stderr)
            self.assertEqual(entry.command(root, "svn", "propget", "--strict", "tsvn:precommithook", "."), foreign)

    def test_three_line_installer_mutant_fails_same_contract(self):
        with tempfile.TemporaryDirectory(prefix="tsvn-three-line-") as temp:
            base = Path(temp).resolve()
            source = (HERE / "shoalmark.py").read_text(encoding="utf-8")
            before = 'value = f"{kind}_commit_hook\\n{command}\\ntrue\\nhide\\n"'
            self.assertEqual(source.count(before), 1)
            mutant = base / "mutant.py"
            mutant.write_text(source.replace(before, 'value = f"{command}\\ntrue\\nhide\\n"'), encoding="utf-8")
            properties = installed_properties(mutant, base)[3]
            self.assertFalse(property_contract(properties))


NOTICE = "Subversion: this local run cannot verify commit signatures or server-authenticated author identities."


def notice_observations(source, base):
    root, tool, install, properties = installed_properties(source, base)
    env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
    def run(*args):
        return subprocess.run([sys.executable, str(tool), "--root", str(root), *args], cwd=base,
                              env=env, capture_output=True, text=True, encoding="mbcs" if os.name == "nt" and "--tsvn-hook" in args else "utf-8", timeout=30)
    paths = base / "paths.txt"; message = base / "message.txt"
    paths.write_text(str(root / "work-tracker") + "\n", encoding="utf-8")
    message.write_text("local fixture\n", encoding="utf-8")
    hook = lambda kind: run("--tsvn-hook", kind, str(paths), *(["3"] if kind == "pre" else []), str(message), str(root))
    results = {"init": run("--init"), "write": run()}
    results["check"] = run("--check")
    results["start"] = hook("start")
    results["pre"] = hook("pre")
    results["binding-refusal"] = run("--tsvn-hook", "pre", "not-an-absolute-path")
    results["board"] = run("--html-only")
    results["schema"] = run("--schema")
    tracker = root / "work-tracker" / "WORK-001-local.md"
    tracker.write_text(tracker.read_text(encoding="utf-8").replace("status: Proposed", "status: Broken"), encoding="utf-8")
    results["check-refusal"] = run("--check")
    results["start-refusal"] = hook("start")
    results["pre-refusal"] = hook("pre")
    results["init-refusal"] = run("--init", "--key", "!bad")
    return results


def notice_contract(results):
    for name, result in results.items():
        wanted = name in ("init", "check", "check-refusal", "init-refusal")
        if (result.stdout + result.stderr).count(NOTICE) != int(wanted):
            return False
        if wanted and (not result.stderr.endswith(NOTICE + "\n") or NOTICE in result.stdout):
            return False
        if result.returncode != (4 if "refusal" in name else 0):
            return False
    return True


@unittest.skipUnless(shutil.which("svn") and shutil.which("svnadmin"), "svn and svnadmin are required")
class NoticeControls(unittest.TestCase):
    def test_notice_modes_and_order_after_refusals(self):
        with tempfile.TemporaryDirectory(prefix="tsvn-notice-") as temp:
            self.assertTrue(notice_contract(notice_observations(HERE / "shoalmark.py", Path(temp).resolve())))

    def test_notice_mutants_fail_same_contract(self):
        source = (HERE / "shoalmark.py").read_text(encoding="utf-8")
        selection = 'notice = _notice and not args.tsvn_hook and cli_operation(args) in ("init", "check")'
        final = '''    try:
        return main_run(args)
    finally:
        if notice and vcs() == "svn":
            print(SVN_VERIFY_LIMIT, file=sys.stderr)'''
        mutants = {
            "missing-init": (selection, selection.replace('("init", "check")', '("check",)')),
            "missing-check": (selection, selection.replace('("init", "check")', '("init",)')),
            "hook-notice": (selection, selection + ' or bool(args.tsvn_hook)'),
            "duplicate": ('            print(SVN_VERIFY_LIMIT, file=sys.stderr)', '            print(SVN_VERIFY_LIMIT, file=sys.stderr)\n            print(SVN_VERIFY_LIMIT, file=sys.stderr)'),
            "before-violations": (final, '''    if notice and vcs() == "svn":
        print(SVN_VERIFY_LIMIT, file=sys.stderr)
    return main_run(args)'''),
        }
        for name, (before, after) in mutants.items():
            with self.subTest(mutant=name), tempfile.TemporaryDirectory(prefix="tsvn-notice-mutant-") as temp:
                self.assertEqual(source.count(before), 1)
                base = Path(temp).resolve(); mutant = base / "mutant.py"
                mutant.write_text(source.replace(before, after), encoding="utf-8")
                self.assertFalse(notice_contract(notice_observations(mutant, base)))


def hook_bytes(fm, codepage=1252, platform="nt"):
    out_bytes, err_bytes = io.BytesIO(), io.BytesIO()
    class AnsiStream(io.TextIOWrapper):
        # The Windows-only mbcs codec maps CP_ACP; simulate that mapping on hosts without the codec.
        requested = None
        def reconfigure(self, *, encoding, **kwargs):
            self.requested = encoding
            return super().reconfigure(encoding="cp" + str(codepage) if encoding == "mbcs" else encoding, **kwargs)
    out = AnsiStream(out_bytes, encoding="utf-8")
    err = AnsiStream(err_bytes, encoding="utf-8")
    with patch.object(fm.os, "name", platform), \
            contextlib.redirect_stdout(out), contextlib.redirect_stderr(err), \
            patch.object(fm, "tsvn_arguments", side_effect=ValueError("sample — 漢")):
        code = fm.main(["--tsvn-hook", "pre"])
        print("sample — 漢")
        out.flush(); err.flush()
    data = code, out_bytes.getvalue(), err_bytes.getvalue(), out.requested == err.requested == "mbcs"
    out.close(); err.close()
    return data


def watchdog_bytes(fm):
    raw = io.BytesIO(); stream = io.TextIOWrapper(raw, encoding="cp1252")
    with contextlib.redirect_stderr(stream), patch.object(fm, "BOARD_RUN_SECONDS", 1), \
            patch.object(fm.threading, "Timer") as timer, patch.object(fm.os, "write") as write, patch.object(fm.os, "_exit") as stop:
        fm.board_watchdog(board=False)
        timer.call_args.args[1]()
        stop.assert_called_once_with(4)
        data = write.call_args.args
    stream.close()
    return data


class EncodingControls(unittest.TestCase):
    def test_windows_hook_uses_ansi_bytes_and_replacement(self):
        import shoalmark as fm
        for cp in (1252, 932, 65001):
            with self.subTest(codepage=cp):
                code, out, err, read = hook_bytes(fm, cp)
                self.assertEqual(code, 4)
                self.assertTrue(read)
                self.assertEqual(out, "sample — 漢\n".encode("cp" + str(cp), errors="replace"))
                self.assertEqual(err, "--tsvn-hook: sample — 漢 — nothing is written\n".encode("cp" + str(cp), errors="replace"))

    def test_other_modes_keep_utf8(self):
        import shoalmark as fm
        for platform, argv in (("nt", ["--print-written"]), ("nt", ["--check"]), ("posix", ["--tsvn-hook", "pre"])):
            raw = io.BytesIO(); stream = io.TextIOWrapper(raw, encoding="ascii")
            with patch.object(fm.os, "name", platform), contextlib.redirect_stdout(stream):
                fm.configure_output(argv)
                print("path — 漢")
                stream.flush()
            self.assertEqual(raw.getvalue(), "path — 漢\n".encode("utf-8"))
            stream.close()

    def test_utf8_hook_mutant_fails_same_byte_contract(self):
        import shoalmark as fm
        source = (HERE / "shoalmark.py").read_text(encoding="utf-8")
        before = 'encoding = "mbcs"'
        self.assertEqual(source.count(before), 1)
        namespace = dict(fm.__dict__)
        import ast
        function = next(node for node in ast.parse(source.replace(before, 'encoding = "utf-8"')).body
                        if isinstance(node, ast.FunctionDef) and node.name == "configure_output")
        exec(compile(ast.Module(body=[function], type_ignores=[]), str(HERE / "shoalmark.py"), "exec"), namespace)
        with patch.object(fm, "configure_output", namespace["configure_output"]):
            code, out, err, read = hook_bytes(fm)
        self.assertNotEqual(err, "--tsvn-hook: sample — 漢 — nothing is written\n".encode("cp1252", errors="replace"))
        self.assertIn("—".encode("utf-8"), err)

    def test_watchdog_bytes_use_configured_ansi_stream(self):
        import shoalmark as fm
        line = "shoalmark: the hook's run took longer than 1 s and was stopped — the commit is refused; SHOALMARK_BOARD_SECONDS gives it longer\n"
        self.assertEqual(watchdog_bytes(fm), (2, line.encode("cp1252")))

    def test_utf8_watchdog_mutant_fails_same_byte_contract(self):
        import ast
        import shoalmark as fm
        source = (HERE / "shoalmark.py").read_text(encoding="utf-8")
        before = '.encode(getattr(sys.stderr, "encoding", None) or "utf-8", errors="replace")'
        self.assertEqual(source.count(before), 1)
        namespace = dict(fm.__dict__)
        namespace["BOARD_RUN_SECONDS"] = 1
        function = next(node for node in ast.parse(source.replace(before, '.encode("utf-8")')).body
                        if isinstance(node, ast.FunctionDef) and node.name == "board_watchdog")
        exec(compile(ast.Module(body=[function], type_ignores=[]), str(HERE / "shoalmark.py"), "exec"), namespace)
        with patch.object(fm, "board_watchdog", namespace["board_watchdog"]):
            fd, data = watchdog_bytes(fm)
        self.assertEqual(fd, 2)
        line = "shoalmark: the hook's run took longer than 1 s and was stopped — the commit is refused; SHOALMARK_BOARD_SECONDS gives it longer\n"
        self.assertNotEqual(data, line.encode("cp1252"))
        self.assertIn("—".encode("utf-8"), data)
        self.assertNotIn(b"\x97", data)


def run_controls(check):
    for test in unittest.defaultTestLoader.loadTestsFromModule(sys.modules[__name__]):
        for case in test:
            result = unittest.TestResult()
            case.run(result)
            if result.skipped:
                print("  skip  " + case.id() + ": " + result.skipped[0][1])
            else:
                check(case.id(), result.wasSuccessful())
                for _, detail in result.errors + result.failures:
                    print(detail)


if __name__ == "__main__":
    unittest.main()
