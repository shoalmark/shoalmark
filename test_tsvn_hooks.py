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
