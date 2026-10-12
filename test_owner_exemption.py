"""Synthetic Owner lists, signed histories, installed hooks and CI checkouts for FM-033 R14."""

import datetime
import os
from pathlib import Path
import re
import shlex
import shutil
import subprocess
import sys
import tempfile
import unittest


HERE = Path(__file__).resolve().parent
OWNER = "owner@example.invalid"
NOREPLY = "123456+synthetic-owner@users.noreply.github.com"
SEAT = "builder@example.invalid"


def ci_bash():
    if os.name == "nt":
        found = shutil.which("git")
        for up in ((Path(found).resolve().parents[1], Path(found).resolve().parents[2]) if found else ()):
            for sub in ("bin", "usr/bin"):
                if (up / sub / "bash.exe").is_file():
                    return str(up / sub / "bash.exe")
        return None
    return shutil.which("bash")


class OwnerExemption(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.TemporaryDirectory(prefix="shoalmark-r14-")
        cls.area = Path(cls.tmp.name).resolve()
        cls.env = {k: v for k, v in os.environ.items() if not k.startswith(("GIT_", "SSH_")) and k != "CODEX_THREAD_ID"}
        cls.env.update(GIT_CONFIG_GLOBAL=os.devnull, GIT_CONFIG_NOSYSTEM="1", GIT_TERMINAL_PROMPT="0", SHOALMARK_CMD="python3 shoalmark.py")
        programs = cls.area / "bin"
        programs.mkdir()
        python = programs / "python"
        python.write_text("#!/bin/sh\nexec " + shlex.quote(Path(sys.executable).as_posix()) + ' "$@"\n', encoding="utf-8")
        python.chmod(0o755)
        cls.env["PATH"] = str(programs) + os.pathsep + cls.env.get("PATH", "")
        cls.keys = cls.area / "keys"
        cls.keys.mkdir()
        for key in ("owner", "other", "forge", "untrusted"):
            cls.call(cls.keys, "ssh-keygen", "-q", "-t", "ed25519", "-N", "", "-f", cls.keys / key, required=True)
        cls.seed = cls.area / "seed"
        cls.seed.mkdir()
        cls.git(cls.seed, "init", "-q", "-b", "main", required=True)
        for key, value in {"user.name": "Synthetic Builder", "user.email": SEAT, "commit.gpgsign": "false",
                           "gpg.format": "ssh", "gpg.ssh.allowedSignersFile": "work-tracker/allowed_signers",
                           "seat.session": "1111aaaa", "seat.harness": "synthetic/harness"}.items():
            cls.git(cls.seed, "config", key, value, required=True)
        cls.tool(cls.seed, "--init", "--key", "AP", required=True)
        (cls.seed / "shoalmark.toml").write_text(
            f'name = "Synthetic R14"\nowner = ["{OWNER} signed", "{NOREPLY} signed"]\n'
            'tracker_dir = "work-tracker"\njudged_before_build = true\nfreeze_at = 8\n'
            '[kinds]\nAP = "Work"\n[tags]\nbug = "Defect"\nprocess = "Process"\n'
            f'[seats]\nbuilder = "{SEAT}"\nplanner = "planner@example.invalid"\n', encoding="utf-8")
        wt = cls.seed / "work-tracker"
        wt.mkdir()
        for n in range(1, 9):
            (wt / f"AP-{n:03}-work.md").write_text(
                f'---\nid: AP-{n:03}\nstatus: In Progress\nconsidered: none\ntriaged: {datetime.date.today()}\n'
                f'next: build\nhook: "Synthetic work {n}"\n---\n\n# AP-{n:03} — Work\n\n'
                '## What is true now\n\nReady.\n\n## Done when\n\nComplete.\n', encoding="utf-8")
        (wt / "allowed_signers").write_text("".join(
            f"{key}@example.invalid " + (cls.keys / (key + ".pub")).read_text(encoding="utf-8")
            for key in ("owner", "other", "forge")), encoding="utf-8")
        ignore = cls.seed / ".gitignore"
        ignore.write_text(ignore.read_text(encoding="utf-8") + "\nwork-tracker/index.html\nwork-tracker/view/\n", encoding="utf-8")
        shutil.copyfile(HERE / "shoalmark.py", cls.seed / "shoalmark.py")
        cls.tool(cls.seed)
        cls.git(cls.seed, "add", "-A", required=True)
        cls.commit(cls.seed, OWNER, "owner", "Synthetic policy\n\nSession: 0000aaaa", required=True)
        cls.git(cls.seed, "update-ref", "refs/remotes/origin/main", "HEAD", required=True)
        cls.git(cls.seed, "symbolic-ref", "refs/remotes/origin/HEAD", "refs/remotes/origin/main", required=True)
        cls.tool(cls.seed, "--install-hook", required=True)
        cls.serial = 0

    @classmethod
    def tearDownClass(cls):
        def writable(func, path, _exc):
            os.chmod(path, 0o700)
            func(path)
        shutil.rmtree(cls.area, onerror=writable)
        cls.tmp.cleanup()

    @classmethod
    def call(cls, root, *args, author=None, required=False, extra=None):
        env = dict(cls.env, **(extra or {}))
        if author:
            env.update(GIT_AUTHOR_NAME="Synthetic Author", GIT_AUTHOR_EMAIL=author)
        r = subprocess.run([str(a) for a in args], cwd=root, env=env, capture_output=True,
                           text=True, encoding="utf-8", errors="replace")
        if required and r.returncode:
            raise AssertionError(f"{args}: exit {r.returncode}\n{r.stdout}{r.stderr}")
        return r

    @classmethod
    def git(cls, root, *args, **kwargs):
        return cls.call(root, "git", *args, **kwargs)

    @classmethod
    def tool(cls, root, *args, **kwargs):
        return cls.call(root, sys.executable, HERE / "shoalmark.py", "--root", root, *args, **kwargs)

    @classmethod
    def commit(cls, root, author, key, subject, explicit=False, **kwargs):
        options = ["-c", "user.signingkey=" + str(cls.keys / key)] if key else []
        args = options + ["commit", "-q", "-S" if key else "--no-gpg-sign", "-m", subject]
        if explicit:
            args += ["--author=Synthetic Owner <" + author + ">"]
        return cls.git(root, *args, author=None if explicit else author, **kwargs)

    def fixture(self):
        type(self).serial += 1
        root = self.area / ("case-" + str(self.serial))
        shutil.copytree(self.seed, root)
        self.git(root, "switch", "-q", "-c", "work", required=True)
        return root

    def stage(self, root, path="app.py", text="synthetic content\n"):
        p = root / path
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(text, encoding="utf-8")
        self.git(root, "add", path, required=True)

    def gate(self, root, expected, *args):
        r = self.tool(root, "--check", *args)
        self.assertEqual(r.returncode, expected, r.stdout + r.stderr)
        return r

    def test_pending_owner_and_seat_authors(self):
        for author in (OWNER, NOREPLY, SEAT):
            for explicit in (False, True):
                for session in (None, "malformed", "1111aaaa/planner-1", "1111aaaa"):
                    with self.subTest(author=author, explicit=explicit, session=session):
                        root = self.fixture()
                        self.git(root, "config", "seat.session", session) if session else self.git(root, "config", "--unset", "seat.session")
                        self.stage(root)
                        r = self.commit(root, author, None, "Ordinary code", explicit=explicit)
                        if author == SEAT:
                            self.assertNotEqual(r.returncode, 0)
                            self.assertTrue("Session:" in r.stderr or "names no tracker" in r.stderr, r.stderr)
                        else:
                            self.assertEqual(r.returncode, 0, r.stdout + r.stderr)

    def test_freeze_entry_point(self):
        for freeze in (0, 8):
            for author in (OWNER, NOREPLY, SEAT):
                for tag in ("process", "bug"):
                    with self.subTest(freeze=freeze, author=author, tag=tag):
                        root = self.fixture()
                        p = root / "shoalmark.toml"
                        p.write_text(p.read_text(encoding="utf-8").replace("freeze_at = 8", f"freeze_at = {freeze}"), encoding="utf-8")
                        r = self.tool(root, "--new", "AP", "Synthetic filing", "--tags", tag, author=author)
                        expected = 4 if freeze == 8 and author == SEAT and tag == "process" else 0
                        self.assertEqual(r.returncode, expected, r.stdout + r.stderr)

    def test_owner_signatures_in_ordinary_history(self):
        for author in (OWNER, NOREPLY):
            for key in ("owner", None, "other", "untrusted", "forge"):
                for path in ("app.py", "work-tracker/evidence/note.txt"):
                    with self.subTest(author=author, key=key, path=path):
                        root = self.fixture()
                        self.stage(root, path)
                        self.commit(root, author, key, "AP-001: ordinary work", required=True)
                        r = self.gate(root, 0 if key == "owner" else 4)
                        if key != "owner":
                            self.assertIn("Owner", r.stderr)
                            self.assertIn("signature", r.stderr)
                            self.assertEqual(len(r.stderr.strip().splitlines()), 1, r.stderr)
                            if author == NOREPLY:
                                self.assertIn("GitHub", r.stderr)
                                self.assertIn("locally", r.stderr)
                        if key == "owner":
                            self.stage(root, "second.py")
                            self.commit(root, author, key, "Ordinary code", required=True)
                            self.gate(root, 0)

    def test_seat_authorship_with_owner_signature(self):
        for key in (None, "owner"):
            root = self.fixture()
            self.stage(root)
            self.assertNotEqual(self.commit(root, SEAT, key, "Ordinary code").returncode, 0)
            self.commit(root, SEAT, key, "AP-001: seat work", required=True)
            self.gate(root, 0)
            self.git(root, "config", "seat.session", "malformed", required=True)
            self.stage(root, "second.py")
            self.assertNotEqual(self.commit(root, SEAT, key, "AP-001: seat work").returncode, 0)

    def test_trusted_policy_and_signers(self):
        for change in ("signer", "owner"):
            with self.subTest(change=change):
                root = self.fixture()
                if change == "signer":
                    p = root / "work-tracker/allowed_signers"
                    self.stage(root, p.relative_to(root).as_posix(), p.read_text(encoding="utf-8") + OWNER + " " + (self.keys / "untrusted.pub").read_text(encoding="utf-8"))
                else:
                    p = root / "shoalmark.toml"
                    self.stage(root, "shoalmark.toml", p.read_text(encoding="utf-8").replace(OWNER + " signed", "replacement@example.invalid signed"))
                self.commit(root, OWNER, "untrusted", "AP-001: policy record", required=True)
                self.gate(root, 4)
                self.gate(root, 4, "--print-written")

    def test_unsigned_owner_under_later_commit(self):
        root = self.fixture()
        self.stage(root, "work-tracker/evidence/first.txt")
        self.commit(root, OWNER, None, "AP-001: first record", required=True)
        first = self.git(root, "rev-parse", "HEAD").stdout.strip()
        self.stage(root, "work-tracker/evidence/second.txt")
        self.commit(root, OWNER, "owner", "AP-001: second record", required=True)
        self.assertIn(first[:10], self.gate(root, 4).stderr)

    def test_main_and_nested_merges(self):
        root = self.fixture()
        self.git(root, "switch", "-q", "-c", "main-feature", "main", required=True)
        self.stage(root, "main.py")
        self.commit(root, SEAT, None, "AP-001: main work", required=True)
        self.git(root, "switch", "-q", "main", required=True)
        self.git(root, "-c", "user.signingkey=" + str(self.keys / "forge"), "merge", "--no-ff", "-S", "-m", "Merge main work", "main-feature", author=NOREPLY, required=True)
        self.git(root, "update-ref", "refs/remotes/origin/main", "HEAD", required=True)
        self.git(root, "switch", "-q", "-c", "above-main", required=True)
        self.stage(root, "own.py")
        self.commit(root, SEAT, None, "AP-001: own work", required=True)
        self.gate(root, 0)
        self.git(root, "switch", "-q", "main", required=True)
        self.stage(root, "updated-main.py")
        self.commit(root, NOREPLY, "forge", "AP-001: updated main", required=True)
        self.git(root, "update-ref", "refs/remotes/origin/main", "HEAD", required=True)
        self.git(root, "switch", "-q", "-c", "local-update", "above-main", required=True)
        self.git(root, "-c", "user.signingkey=" + str(self.keys / "owner"), "merge", "--no-ff", "-S", "-m", "Merge main locally", "main", author=NOREPLY, required=True)
        self.gate(root, 0)
        self.git(root, "switch", "-q", "above-main", required=True)
        self.git(root, "-c", "user.signingkey=" + str(self.keys / "forge"), "merge", "--no-ff", "-S", "-m", "Update branch", "main", author=NOREPLY, required=True)
        update = self.git(root, "rev-parse", "HEAD").stdout.strip()
        r = self.gate(root, 4)
        self.assertIn(update[:10], r.stderr)
        self.assertEqual(len(r.stderr.strip().splitlines()), 1)
        self.git(root, "switch", "-q", "-c", "outer", "main", required=True)
        self.stage(root, "outer.py")
        self.commit(root, SEAT, None, "AP-001: outer work", required=True)
        self.git(root, "merge", "--no-ff", "-m", "AP-001: nested work", "above-main", author=SEAT, required=True)
        r = self.gate(root, 4)
        self.assertIn(update[:10], r.stderr)
        self.assertEqual(len(r.stderr.strip().splitlines()), 1)

    def test_github_merge_commit(self):
        for key in (None, "forge"):
            with self.subTest(key=key):
                root = self.fixture()
                self.stage(root, "own.py")
                self.commit(root, SEAT, None, "AP-001: own work", required=True)
                self.git(root, "switch", "-q", "-c", "side", "main", required=True)
                self.stage(root, "side.py")
                self.commit(root, SEAT, None, "AP-001: side work", required=True)
                self.git(root, "switch", "-q", "work", required=True)
                options = ["-c", "user.signingkey=" + str(self.keys / key)] if key else []
                self.git(root, *options, "merge", "--no-ff", "-S" if key else "--no-gpg-sign", "-m", "Merge pull request", "side", author=NOREPLY, required=True)
                merge = self.git(root, "rev-parse", "HEAD").stdout.strip()
                r = self.gate(root, 4)
                self.assertIn(merge[:10], r.stderr)
                self.assertEqual(len(r.stderr.strip().splitlines()), 1)

    def two_merge_bases(self, author, key):
        root = self.fixture()
        tips = []
        for name in ("left", "right"):
            self.git(root, "switch", "-q", "-c", name, "main", required=True)
            self.stage(root, name + ".py")
            self.commit(root, NOREPLY, "forge", "Main code " + name, required=True)
            tips.append(self.git(root, "rev-parse", "HEAD", required=True).stdout.strip())
        self.git(root, "switch", "-q", "main", required=True)
        self.git(root, "merge", "--ff-only", "left", required=True)
        self.git(root, "-c", "user.signingkey=" + str(self.keys / "owner"), "merge", "--no-ff", "-S",
                 "-m", "Merge main siblings", "right", author=OWNER, required=True)
        self.git(root, "update-ref", "refs/remotes/origin/main", "HEAD", required=True)
        self.git(root, "switch", "-q", "work", required=True)
        self.git(root, "merge", "--ff-only", "right", required=True)
        options = ["-c", "user.signingkey=" + str(self.keys / key)] if key else []
        self.git(root, *options, "merge", "--no-ff", "-S" if key else "--no-gpg-sign", "-m",
                 "AP-001: merge branch siblings", "left", author=author, required=True)
        self.assertEqual(set(self.git(root, "merge-base", "--all", "origin/main", "HEAD", required=True).stdout.split()), set(tips))
        return root

    def test_owner_two_merge_bases(self):
        """Main and an Owner-signed branch independently merge sibling histories."""
        root = self.two_merge_bases(OWNER, "owner")
        self.stage(root)
        self.commit(root, OWNER, "owner", "Ordinary Owner code", required=True)
        self.assertEqual(self.git(root, "status", "--porcelain", required=True).stdout, "")
        own = self.git(root, "log", "--format=%G? %GS", "HEAD", "^origin/main", required=True).stdout.splitlines()
        self.assertTrue(own)
        self.assertTrue(all(line == "G " + OWNER for line in own), own)
        self.gate(root, 0)

    def test_seat_two_merge_bases(self):
        """Main and a seat branch independently merge sibling histories and carry seat work."""
        for named in (True, False):
            with self.subTest(named=named):
                root = self.two_merge_bases(SEAT, None)
                self.git(root, "branch", "-m", "ap/001-work", required=True)
                self.stage(root)
                self.commit(root, SEAT, None, "AP-001: seat code" if named else "Ordinary seat code", required=True)
                code = self.git(root, "rev-parse", "HEAD", required=True).stdout.strip()
                self.git(root, "branch", "-m", "work", required=True)
                self.assertEqual(self.git(root, "status", "--porcelain", required=True).stdout, "")
                r = self.gate(root, 0 if named else 4)
                if not named:
                    self.assertIn(code[:7], r.stderr)
                    self.assertIn("names no tracker", r.stderr)
                    self.assertNotIn("Main code", r.stderr)

    def test_unmerged_branch_with_two_merge_bases(self):
        """An Owner-signed branch with two merge bases also merges a separate seat branch."""
        root = self.two_merge_bases(OWNER, "owner")
        self.git(root, "switch", "-q", "-c", "ap/001-side", "left", required=True)
        self.stage(root, "side.py")
        self.commit(root, SEAT, None, "Separate seat code", required=True)
        side = self.git(root, "rev-parse", "HEAD", required=True).stdout.strip()
        self.git(root, "switch", "-q", "work", required=True)
        self.git(root, "branch", "-m", "ap/001-work", required=True)
        self.git(root, "-c", "user.signingkey=" + str(self.keys / "owner"), "merge", "--no-ff", "-S",
                 "-m", "AP-001: merge separate work", "ap/001-side", author=OWNER, required=True)
        self.git(root, "branch", "-m", "work", required=True)
        self.assertEqual(self.git(root, "status", "--porcelain", required=True).stdout, "")
        self.assertEqual(len(self.git(root, "merge-base", "--all", "origin/main", "HEAD", required=True).stdout.split()), 2)
        self.assertIn(side, self.git(root, "rev-list", "HEAD", "^origin/main", required=True).stdout.split())
        r = self.gate(root, 4)
        self.assertIn(side[:7], r.stderr)
        self.assertIn("names no tracker", r.stderr)

    def test_rv_3027(self):
        """A configuration-free default branch and a separately configured signed branch."""
        root = self.fixture()
        self.git(root, "switch", "-q", "main", required=True)
        self.git(root, "rm", "shoalmark.toml", required=True)
        self.commit(root, OWNER, "owner", "AP-001: default configuration", required=True)
        self.git(root, "update-ref", "refs/remotes/origin/main", "HEAD", required=True)
        self.git(root, "switch", "-q", "work", required=True)
        config = root / "shoalmark.toml"
        self.stage(root, "shoalmark.toml", config.read_text(encoding="utf-8").replace(
            f'owner = ["{OWNER} signed", "{NOREPLY} signed"]', 'owner = "other@example.invalid signed"'))
        self.stage(root)
        read = (
            "import importlib.util, sys\n"
            "s = importlib.util.spec_from_file_location('fm', sys.argv[1])\n"
            "fm = importlib.util.module_from_spec(s)\n"
            "s.loader.exec_module(fm)\n"
            "fm.configure(sys.argv[2])\n"
            "print(fm.pending_owner())\n"
            "print(fm.verified_owner('HEAD'))\n"
            "print(fm.owners_at('refs/remotes/origin/main'))\n"
            "print(fm.owners_at(None))\n"
        )
        pending = self.call(root, sys.executable, "-c", read, HERE / "shoalmark.py", root,
                            author="other@example.invalid", required=True).stdout.splitlines()
        with self.subTest(stage="pending"):
            self.assertEqual(pending[0], "False")
        r = self.commit(root, "other@example.invalid", "other", "Ordinary unjudged code")
        with self.subTest(stage="hook"):
            self.assertNotEqual(r.returncode, 0, r.stdout + r.stderr)
            self.assertIn("names no tracker", r.stderr)
        if r.returncode:
            self.git(root, "branch", "-m", "ap/001-work", required=True)
            self.commit(root, "other@example.invalid", "other", "Ordinary unjudged code", required=True)
            self.git(root, "branch", "-m", "work", required=True)
        self.assertEqual(self.git(root, "status", "--porcelain", required=True).stdout, "")
        self.assertNotEqual(self.git(root, "cat-file", "-e", "origin/main:shoalmark.toml").returncode, 0)
        self.assertEqual(self.git(root, "log", "-1", "--format=%G? %GS", required=True).stdout.strip(), "G other@example.invalid")
        committed = self.call(root, sys.executable, "-c", read, HERE / "shoalmark.py", root,
                              author="other@example.invalid", required=True).stdout.splitlines()
        with self.subTest(stage="verified"):
            self.assertEqual(committed[1], "False")
        with self.subTest(stage="legacy"):
            self.assertEqual(committed[2:], ["{'other@example.invalid': 'signed'}"] * 2)
        with self.subTest(stage="gate"):
            self.assertIn("names no tracker", self.gate(root, 4).stderr)

    def test_ci_gate_executes_on_pr_head(self):
        bash = ci_bash()
        if not bash:
            self.skipTest("the CI shell requires Git Bash")
        text = (HERE / ".github/workflows/ci.yml").read_text(encoding="utf-8")
        match = re.search(r"^        id: gate\n(?P<settings>.*?)^        run: \|\n(?P<script>(?:^          [^\n]*\n|^\n)+)", text, re.M | re.S)
        self.assertIsNotNone(match)
        settings = match["settings"]
        self.assertNotIn("continue-on-error", settings)
        self.assertNotRegex(settings, r"(?m)^        if:")
        command = re.search(r"\bSHOALMARK_CMD:\s*([^,}\n]+)", settings)
        command = command[1].strip().strip("\"'") if command else ""
        script = "\n".join(line[10:] for line in match["script"].splitlines())
        programs = self.area / "ci-python"
        programs.mkdir()
        launcher = programs / "launcher.py"
        launcher.write_text(
            "import importlib.util, os, sys\n"
            "if sys.argv[1] == '-I': del sys.argv[1]\n"
            "spec = importlib.util.spec_from_file_location('ci_tool', sys.argv[1])\n"
            "tool = importlib.util.module_from_spec(spec)\n"
            "spec.loader.exec_module(tool)\n"
            "tool.PY = os.environ['SHOALMARK_TEST_PY']\n"
            "tool.configure()\n"
            "raise SystemExit(tool.main(sys.argv[2:]))\n", encoding="utf-8")
        python = programs / "python"
        python.write_text("#!/bin/sh\nexec " + shlex.quote(Path(sys.executable).as_posix()) + " "
                          + shlex.quote(launcher.as_posix()) + ' "$@"\n', encoding="utf-8")
        python.chmod(0o755)
        for records in (True, False):
            for key in ("owner", None):
                with self.subTest(records=records, key=key):
                    root = self.fixture()
                    self.stage(root, "work-tracker/evidence/note.txt" if records else "app.py")
                    self.commit(root, OWNER, key, "AP-001: PR work", required=True)
                    head = self.git(root, "rev-parse", "HEAD").stdout.strip()
                    self.git(root, "switch", "-q", "main", required=True)
                    self.git(root, "merge", "--no-ff", "-m", "CI merge", "work", author=NOREPLY, required=True)
                    merge = self.git(root, "rev-parse", "HEAD").stdout.strip()
                    for naming in ("python3", "python"):
                        with self.subTest(naming=naming):
                            self.git(root, "checkout", "--detach", merge, required=True)
                            r = self.call(root, bash, "--noprofile", "--norc", "-eo", "pipefail", "-c", script,
                                          extra={"EVENT": "pull_request", "HEAD_SHA": head, "DEFAULT_BRANCH": "main",
                                                 "TRACKER": "work-tracker", "SHOALMARK_CMD": command,
                                                 "SHOALMARK_TEST_PY": naming,
                                                 "PATH": str(programs) + os.pathsep + self.env["PATH"]})
                            self.assertEqual(r.returncode, 0 if key else 4, r.stdout + r.stderr)
                            if key:
                                self.assertEqual(self.git(root, "rev-parse", "HEAD").stdout.strip(), merge)
                            else:
                                self.assertIn(head[:10], r.stderr)


def run_checks():
    return unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(OwnerExemption)).wasSuccessful()


if __name__ == "__main__":
    unittest.main(verbosity=2)
