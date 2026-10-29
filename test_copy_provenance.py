"""The hooks' copy records the tool's full commit and its file comparison: its rows, older records read as written, and the four design mutants.

Requirements recorded privately. Every installation and Git write uses a disposable repository.
"""

import contextlib
import hashlib
import importlib.util
import io
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch


HERE = Path(__file__).resolve().parent


def load(path):
    spec = importlib.util.spec_from_file_location("copy_fixture", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class CopyProvenanceControls(unittest.TestCase):
    source = None

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name).resolve() / "repo"
        self.root.mkdir()
        self.env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
        self.env.update(GIT_CONFIG_NOSYSTEM="1", GIT_CONFIG_GLOBAL=os.devnull, GIT_TERMINAL_PROMPT="0",
                        GIT_AUTHOR_NAME="Fixture", GIT_COMMITTER_NAME="Fixture",
                        GIT_AUTHOR_EMAIL="fixture@example.invalid", GIT_COMMITTER_EMAIL="fixture@example.invalid")
        original = load(HERE / "shoalmark.py")
        self.payload = original.copy_files()
        for rel in self.payload:
            path = self.root / rel
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes((HERE / rel).read_bytes().replace(b"\r\n", b"\n"))
        if self.source is not None:
            (self.root / "shoalmark.py").write_bytes(self.source.encode("utf-8"))
        self.git("init", "-q")
        self.git("config", "core.autocrlf", "false")
        self.git("config", "core.hooksPath", os.devnull)
        self.fm = load(self.root / "shoalmark.py")
        self.fm.configure(self.root)
        self.fm.TRACKER_DIR.mkdir(parents=True)
        with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
            self.assertEqual(self.fm.main(["--root", str(self.root)]), 0)
        self.git("add", "-A")
        self.git("commit", "-qm", "copy fixture")
        self.head = self.git("rev-parse", "HEAD").strip()
        self.marker = self.root / ".git" / "shoalmark-trusted" / "COPY"

    def git(self, *args):
        return subprocess.run(["git", "-C", str(self.root), *args], check=True, capture_output=True,
                              text=True, encoding="utf-8", env=self.env).stdout

    def install(self):
        with patch.dict(os.environ, self.env, clear=True):
            code, lines = self.fm.install_copy()
        self.assertEqual(code, 0, lines)
        return self.read()

    def read(self):
        copied = load(self.marker.parent / "shoalmark.py")
        copied.configure(self.root)
        with patch.dict(os.environ, self.env, clear=True):
            return copied.copy_provenance()

    def test_clean_working_tree(self):
        self.assertEqual(self.install(), {"commit": self.head, "files": "equal", "incomplete": ""})

    def test_each_changed_copied_file(self):
        for rel in self.payload:
            with self.subTest(file=rel):
                path = self.root / rel
                original = path.read_bytes()
                path.write_bytes(original + b"\n# changed fixture\n")
                self.assertEqual(self.install(), {"commit": self.head, "files": "changed", "incomplete": ""})
                path.write_bytes(original)

    def test_clean_crlf_checkout(self):
        self.git("config", "core.autocrlf", "true")
        for rel in self.payload:
            (self.root / rel).unlink()
        self.git("checkout-index", "--all")
        self.assertTrue(any(b"\r\n" in (self.root / rel).read_bytes() for rel in self.payload))
        self.assertEqual(self.install(), {"commit": self.head, "files": "equal", "incomplete": ""})

    def test_only_crlf_is_normalized(self):
        path = self.root / "vendor/marked-18.0.13.umd.js"
        path.write_bytes(path.read_bytes().replace(b"\n", b"\r"))
        self.assertEqual(self.install()["files"], "changed")

    def test_source_commit_is_not_the_adopters(self):
        adopter = Path(self.tmp.name) / "adopter"
        adopter.mkdir()
        subprocess.run(["git", "init", "-q", str(adopter)], check=True, capture_output=True, env=self.env)
        self.fm.configure(adopter)
        self.marker = adopter / ".git/shoalmark-trusted/COPY"
        self.assertEqual(self.install(), {"commit": self.head, "files": "equal", "incomplete": ""})

    def pin(self, manifest):
        hashes = "".join(f"{hashlib.sha256((self.root / rel).read_bytes().replace(bytes([13, 10]), bytes([10]))).hexdigest()}  {rel}\n"
                         for rel in self.payload)
        (self.root / "PIN").write_text(f"# shoalmark {self.fm.__version__} · {manifest} · vendored 2026-10-16 · complete\n" + hashes,
                                       encoding="utf-8")

    def test_pinned_tagged_and_untagged_commit(self):
        commit = "1a" * 20
        for manifest in (f"tag v{self.fm.__version__} · commit {commit}", f"untagged {commit}", f"untagged {commit} (dirty)"):
            with self.subTest(manifest=manifest):
                self.pin(manifest)
                self.assertEqual(self.install(), {"commit": commit, "files": "", "incomplete": ""})

    def test_legacy_pin_keeps_the_recorded_prefix(self):
        prefix = self.head[:10]
        self.pin(f"untagged {prefix}")
        record = self.install()
        self.assertEqual(record["commit"], prefix)
        self.assertIn("short", record["incomplete"])
        self.assertIn(f"commit: {prefix}\n", self.marker.read_text(encoding="utf-8"))

    def test_legacy_copy_is_named_without_refusal_or_expansion(self):
        self.install()
        prefix = self.head[:10]
        self.assertEqual(self.git("rev-parse", prefix).strip(), self.head)
        self.marker.write_text(f"source: working tree\ncommit: {prefix}\ncmd: python3 shoalmark.py\n", encoding="utf-8")
        record = self.read()
        self.assertEqual(record["commit"], prefix)
        self.assertIn("short", record["incomplete"])
        self.assertIn("files", record["incomplete"])
        ran = subprocess.run([sys.executable, "-I", str(self.marker.parent / "shoalmark.py"), "--root", str(self.root), "--check"],
                             capture_output=True, text=True, encoding="utf-8", env=self.env)
        self.assertEqual(ran.returncode, 0, ran.stdout + ran.stderr)
        self.assertEqual(ran.stderr.count("COPY record is incomplete"), 1)
        self.assertIn("--install-hook", ran.stderr)

    def test_no_commit_or_comparison_is_incomplete(self):
        self.install()
        for text in ("", "source: working tree\ncommit: no commit yet\nfiles: changed\n",
                     f"source: working tree\ncommit: {self.head}\nfiles: unknown\n"):
            with self.subTest(record=text):
                self.marker.write_text(text, encoding="utf-8")
                self.assertTrue(self.read()["incomplete"])

    def test_legacy_notice_keeps_print_written_stdout(self):
        self.install()
        self.marker.write_text(f"source: working tree\ncommit: {self.head[:10]}\n", encoding="utf-8")
        ran = subprocess.run([sys.executable, "-I", str(self.marker.parent / "shoalmark.py"), "--root", str(self.root), "--print-written"],
                             capture_output=True, text=True, encoding="utf-8", env=self.env)
        self.assertEqual(ran.returncode, 0, ran.stdout + ran.stderr)
        self.assertEqual(ran.stderr.count("COPY record is incomplete"), 1)
        self.assertIn("--install-hook", ran.stderr)
        self.assertNotIn("COPY", ran.stdout)

    def test_source_boundary_admits_only_the_payload_blob_form(self):
        with patch.dict(os.environ, self.env, clear=True):
            blob = self.fm.vcs_process("git", "show", f"{self.head}:./VERSION", cwd=self.root, source=True, capture_output=True)
            self.assertEqual(blob.stdout, (self.root / "VERSION").read_bytes())
            for args in (("show", "HEAD:./VERSION"), ("show", f"{self.head}:VERSION"),
                         ("show", f"{self.head}:./other"), ("show", f"{self.head}:./../VERSION"),
                         ("show", "--textconv", f"{self.head}:./VERSION")):
                with self.subTest(args=args), patch.object(self.fm.subprocess, "run") as start, contextlib.redirect_stderr(io.StringIO()):
                    with self.assertRaises(SystemExit):
                        self.fm.vcs_process("git", *args, cwd=self.root, source=True, capture_output=True)
                    start.assert_not_called()


MUTANTS = (
    ("commit cut short", "test_clean_working_tree",
     'sha = (git_out("rev-parse", "HEAD", cwd=HERE, source=True) or "").strip() or "no commit yet"',
     'sha = (git_out("rev-parse", "HEAD", cwd=HERE, source=True) or "").strip()[:10] or "no commit yet"'),
    ("equal without comparison", "test_each_changed_copied_file",
     'compared = f"files: {\'equal\' if equal else \'changed\'}\\n"', 'compared = "files: equal\\n"'),
    ("raw comparison", "test_clean_crlf_checkout",
     'data.replace(b"\\r\\n", b"\\n") == blob.stdout.replace(b"\\r\\n", b"\\n")', 'data == blob.stdout'),
    ("prefix expanded in adopter", "test_legacy_copy_is_named_without_refusal_or_expansion",
     'commit, files = record.get("commit", ""), record.get("files", "")',
     'commit, files = record.get("commit", ""), record.get("files", "")\n    commit = (git_out("rev-parse", commit) or commit).strip()'),
)


def run_copy_provenance_controls(check):
    for test in unittest.defaultTestLoader.loadTestsFromTestCase(CopyProvenanceControls):
        result = unittest.TestResult()
        test.run(result)
        check("FM-059 COPY · " + test._testMethodName, result.wasSuccessful())
        for _, error in result.failures + result.errors:
            print(error)
    source = (HERE / "shoalmark.py").read_text(encoding="utf-8")
    for name, row, old, new in MUTANTS:
        if source.count(old) != 1:
            check("FM-059 COPY mutant · " + name + " · mutation site exists once", False)
            continue
        mutant = type("CopyMutant", (CopyProvenanceControls,), {"source": source.replace(old, new, 1)})
        result = unittest.TestResult()
        mutant(row).run(result)
        check("FM-059 COPY mutant · " + name + " · same row fails", bool(result.failures) and not result.errors)
        for _, error in result.failures + result.errors:
            print(error)


if __name__ == "__main__":
    failed = []

    def report(name, passed):
        print(("ok   " if passed else "FAIL ") + name, flush=True)
        if not passed:
            failed.append(name)

    run_copy_provenance_controls(report)
    raise SystemExit(bool(failed))
