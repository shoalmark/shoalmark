"""The repository under test, with its own tree as the default branch."""
import atexit
import importlib.util
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile


_REPOSITORIES = {}


def repository_tree(source):
    """Clone once per source; record working changes only in the fixture's commit."""
    source = Path(source).resolve()
    if source in _REPOSITORIES:
        return _REPOSITORIES[source]
    env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
    env.update(GIT_AUTHOR_NAME="fixture", GIT_AUTHOR_EMAIL="fixture@example.invalid",
               GIT_COMMITTER_NAME="fixture", GIT_COMMITTER_EMAIL="fixture@example.invalid",
               GIT_CONFIG_NOSYSTEM="1", GIT_CONFIG_GLOBAL=os.devnull)

    def git(root, *args, **kwargs):
        return subprocess.run(["git", "-C", str(root), "-c", "core.hooksPath=" + os.devnull,
                               "-c", "commit.gpgsign=false", "-c", "core.autocrlf=false", *args],
                              env=env, capture_output=True, check=True, **kwargs).stdout

    held = tempfile.TemporaryDirectory(prefix="shoalmark-repository-")
    root = Path(held.name).resolve() / "repo"
    try:
        head = git(source, "rev-parse", "HEAD").decode().strip()
        git(source, "clone", "--quiet", "--shared", "--no-checkout", str(source), str(root))
        git(root, "checkout", "--quiet", "--detach", head)
        git(root, "config", "--local", "gpg.ssh.allowedSignersFile", "work-tracker/allowed_signers")
        changes = git(source, "diff", "--binary", "--no-ext-diff", "--no-textconv", "HEAD", "--")
        if changes:
            git(root, "apply", "--binary", "--whitespace=nowarn", "-", input=changes)
        for name in git(source, "ls-files", "--others", "--exclude-standard", "-z").split(b"\0"):
            if not name:
                continue
            rel = os.fsdecode(name)
            target = root / rel
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source / rel, target, follow_symlinks=False)
        git(root, "add", "-A")
        if git(root, "diff", "--cached", "--name-only", "-z"):
            git(root, "commit", "--quiet", "-m", "Record the tree under test.")
        head = git(root, "rev-parse", "HEAD").decode().strip()
        git(root, "update-ref", "refs/remotes/origin/main", head)
        git(root, "symbolic-ref", "refs/remotes/origin/HEAD", "refs/remotes/origin/main")
    except BaseException:
        held.cleanup()
        raise
    _REPOSITORIES[source] = _REPOSITORIES[root] = root
    atexit.register(held.cleanup)
    return root


def suite_repository(file):
    """Run imports, configuration resets and child programs in the same fixture."""
    root = repository_tree(Path(file).resolve().parent)
    previous = Path.cwd()
    os.chdir(root)
    atexit.register(os.chdir, previous)
    sys.path.insert(0, str(root))
    return root


def check_repository(root, config, check):
    """A code tree whose trackers moved must leave no former tracker folder behind."""
    left = bool(config.get("trackers")) and os.path.lexists(root / "work-tracker")
    label = "FM-161 · the repository's work-tracker/ folder is absent when trackers live elsewhere"
    check(label, not left)
    if left:
        print("work-tracker/ is still present in the tree under test")


def run_checks(check):
    """Hold the fixture to the source's bytes and history, without changing the source."""
    with tempfile.TemporaryDirectory(prefix="shoalmark-snapshot-control-") as directory:
        source = Path(directory).resolve() / "source"
        source.mkdir()
        env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
        env.update(GIT_CONFIG_GLOBAL=os.devnull, GIT_CONFIG_NOSYSTEM="1")

        def git(*args):
            return subprocess.check_output(["git", "-C", str(source), "-c", "core.hooksPath=" + os.devnull,
                                            "-c", "user.name=fixture", "-c", "user.email=fixture@example.invalid",
                                            "-c", "commit.gpgsign=false", *args], env=env, stderr=subprocess.STDOUT)

        git("init", "--quiet", "--initial-branch=main")
        (source / "keep").write_bytes(b"before\n")
        (source / "gone").write_bytes(b"deleted in the working tree\n")
        git("add", "-A")
        git("commit", "--quiet", "-m", "Fixture baseline.")
        head = git("rev-parse", "HEAD")
        clean = repository_tree(source)
        clean_head = subprocess.check_output(["git", "-C", str(clean), "rev-parse", "HEAD"])
        check("FM-161 · a clean snapshot keeps the commit under test", clean_head == head)
        named = subprocess.run(["git", "-C", str(clean), "config", "--local", "--get", "gpg.ssh.allowedSignersFile"],
                               env=env, capture_output=True, text=True).stdout.strip()
        check("FM-161 · the snapshot names its repository-relative signers path",
              named == "work-tracker/allowed_signers")
        _REPOSITORIES.pop(source)
        (source / "keep").write_bytes(b"staged\n")
        git("add", "keep")
        (source / "keep").write_bytes(b"working bytes\n")
        (source / "gone").rename(source.parent / "gone")
        (source / "work-tracker").mkdir()
        (source / "work-tracker/TRIAGE.md").write_bytes(b"left behind\n")
        before = git("status", "--porcelain=v1", "-z")
        dirty = repository_tree(source)

        def read(*args):
            return subprocess.check_output(["git", "-C", str(dirty), *args], env=env)

        check("FM-161 · a dirty snapshot records working bytes, deletions and untracked tracker files",
              (dirty / "keep").read_bytes() == b"working bytes\n" and not (dirty / "gone").exists()
              and (dirty / "work-tracker/TRIAGE.md").read_bytes() == b"left behind\n")
        check("FM-161 · working changes make one fixture commit and both default refs name it",
              read("rev-parse", "HEAD^") == head
              and read("rev-parse", "HEAD") == read("rev-parse", "origin/main") == read("rev-parse", "origin/HEAD")
              and read("show", "-s", "--format=%ae").strip() == b"fixture@example.invalid"
              and read("status", "--porcelain=v1", "-z") == b"")
        check("FM-161 · the source index, tree, head and branch stay untouched; the snapshot is reused",
              before == git("status", "--porcelain=v1", "-z") and git("rev-parse", "HEAD") == head
              and git("symbolic-ref", "HEAD").strip() == b"refs/heads/main"
              and git("show", ":keep") == b"staged\n" and (source / "keep").read_bytes() == b"working bytes\n"
              and repository_tree(source) == repository_tree(dirty) == dirty)
        verdicts = []
        check_repository(dirty, {"trackers": {"elsewhere": "fixture"}}, lambda label, ok: verdicts.append(ok))
        check("FM-161 · a leftover tracker folder fails the repository check", verdicts == [False])


if __name__ == "__main__":
    failures = []

    def check(label, ok):
        print(("  ok    " if ok else "  FAIL  ") + label)
        if not ok:
            failures.append(label)

    root = suite_repository(__file__)
    spec = importlib.util.spec_from_file_location("repository_tool", root / "shoalmark.py")
    tool = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(tool)
    check_repository(root, tool.CONFIG, check)
    run_checks(check)
    raise SystemExit(bool(failures))
