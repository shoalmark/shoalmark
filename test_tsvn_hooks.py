import contextlib
import io
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

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


@unittest.skipUnless(shutil.which("svn") and shutil.which("svnadmin"), "svn and svnadmin are required")
class PropertyControls(unittest.TestCase):
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
            self.assertIn("left alone", refusal.stderr)
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
                              env=env, capture_output=True, text=True, encoding="utf-8", timeout=30)
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
