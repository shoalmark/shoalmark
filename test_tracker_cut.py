"""FM-161: the code CI refuses added tracker paths and runs the product suites."""
import ast
import importlib.util
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile

HERE = Path(__file__).resolve().parent


def signer_checks(workflow, check):
    match = re.search(r"^        id: suite-signers\n(?P<settings>.*?)^        run: \|\n(?P<script>(?:^          [^\n]*\n|^\n)+)", workflow, re.M | re.S)
    check("the signers step uses bash on every system and precedes both suites", match is not None
          and "shell: bash" in match["settings"] and "if:" not in match["settings"]
          and match.start() < workflow.index("      - run: python -u test_shoalmark.py"))
    if not match:
        return
    check("signers come from the pull request base, or origin/main on tags and manual runs",
          'env: {BASE: "${{ github.event.pull_request.base.sha || \'origin/main\' }}"}' in match["settings"])
    script = "\n".join(line[10:] for line in match["script"].splitlines())
    check("the signers step never selects the head", not any(word in match["settings"] + script
          for word in ("HEAD", "github.sha", "pull_request.head")))
    bash = shutil.which("bash")
    check("the signers step's shell is available", bool(bash))
    if not bash:
        return
    with tempfile.TemporaryDirectory(prefix="suite-signers-") as directory:
        area = Path(directory).resolve()
        root = area / "repo"
        root.mkdir()
        env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
        env.update(GIT_CONFIG_GLOBAL=os.devnull, GIT_CONFIG_NOSYSTEM="1")

        def git(*args):
            return subprocess.check_output(["git", "-C", str(root), *args], env=env, stderr=subprocess.STDOUT).decode().strip()

        def commit(message):
            git("add", "-A"); git("commit", "-qm", message)
            return git("rev-parse", "HEAD")

        git("init", "-q", "-b", "main")
        git("config", "user.name", "fixture")
        git("config", "user.email", "fixture@example.invalid")
        git("config", "commit.gpgsign", "false")
        (root / "file").write_text("fixture\n", encoding="utf-8")
        empty = commit("Fixture without signers.")
        old = root / "work-tracker/allowed_signers"
        old.parent.mkdir()
        old.write_text("base old path\n", encoding="utf-8")
        old_base = commit("Fixture with the old signers path.")
        top = root / "allowed_signers"
        top.write_text("base top path\n", encoding="utf-8")
        top_base = commit("Fixture with both signers paths.")
        old.write_text("untrusted old head\n", encoding="utf-8")
        top.write_text("untrusted top head\n", encoding="utf-8")
        commit("Fixture head replaces both files.")
        git("update-ref", "refs/remotes/origin/main", top_base)
        for label, base, expected in (("old base", old_base, "base old path\n"),
                                      ("top base", top_base, "base top path\n"),
                                      ("default branch", "origin/main", "base top path\n"),
                                      ("no file", empty, None), ("missing base", "missing-ref", None)):
            where = area / label
            where.mkdir()
            exported = where / "environment"
            exported.touch()
            subprocess.run(["git", "-C", str(root), "config", "--unset-all", "gpg.ssh.allowedSignersFile"], env=env, capture_output=True)
            result = subprocess.run([bash, "--noprofile", "--norc", "-eo", "pipefail", "-c", script], cwd=root,
                                    env=dict(env, BASE=base, RUNNER_TEMP=str(where), GITHUB_ENV=str(exported)), capture_output=True, text=True)
            named = subprocess.run(["git", "-C", str(root), "config", "--get", "gpg.ssh.allowedSignersFile"], env=env,
                                   capture_output=True, text=True).stdout.strip()
            fields = dict(line.split("=", 1) for line in exported.read_text(encoding="utf-8").splitlines())
            if expected is not None:
                path = fields.get("SHOALMARK_SUITE_SIGNERS", "")
                check("signers step: " + label + " uses the base outside the checkout and exports it to later steps",
                      result.returncode == 0 and bool(path) and Path(path).is_absolute() and Path(path).parent == where
                      and named == path and Path(path).read_text(encoding="utf-8") == expected)
            else:
                check("signers step: " + label, not fields and not named
                      and (result.returncode != 0 if label == "missing base" else result.returncode == 0
                           and "no signers file" in result.stdout))


def run_checks():
    rows = []

    def check(label, ok, detail=""):
        rows.append(("FM-161 · " + label, bool(ok), detail))

    workflow = (HERE / ".github/workflows/ci.yml").read_text(encoding="utf-8")
    check("every matrix job runs both product suites", all(
        f"      - run: python -u {name}\n" in workflow for name in ("test_shoalmark.py", "test_core.py")))
    check("the tracker gate, tier and records pass-through are absent",
          not any(word in workflow for word in ("id: gate", "id: tier", "steps.tier", "shoalmark.py --check", "Records validation")))
    check("all five matrix entries remain", len(re.findall(r"^          - \{system:", workflow, re.M)) == 5)
    check("additional time-zone results remain visible", "if: matrix.tz\n" in workflow and "continue-on-error: true" in workflow)
    signer_checks(workflow, check)
    match = re.search(r"^        id: tracker-path\n(?P<settings>.*?)^        run: \|\n(?P<script>(?:^          [^\n]*\n|^\n)+)", workflow, re.M | re.S)
    check("the path check runs for pull requests", match is not None and "if: github.event_name == 'pull_request'" in match["settings"])
    if match:
        script = "\n".join(line[10:] for line in match["script"].splitlines())
        bash = shutil.which("bash")
        if not bash:
            check("the workflow shell is available", False, "Git Bash is needed for this check")
        else:
            with tempfile.TemporaryDirectory(prefix="tracker-cut-") as directory:
                area = Path(directory).resolve()
                root, programs = area / "repo", area / "bin"
                root.mkdir(); programs.mkdir()
                launcher = programs / "python"
                import shlex
                launcher.write_text("#!/bin/sh\nexec " + shlex.quote(sys.executable) + ' -I "$@"\n', encoding="utf-8")
                launcher.chmod(0o755)
                env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
                env.update(GIT_CONFIG_GLOBAL=os.devnull, GIT_CONFIG_NOSYSTEM="1", GIT_TERMINAL_PROMPT="0",
                           PATH=str(programs) + os.pathsep + env.get("PATH", ""))

                def git(*args):
                    return subprocess.check_output(["git", "-C", str(root), *args], env=env, stderr=subprocess.STDOUT).decode().strip()

                def write(path):
                    target = root / path
                    target.parent.mkdir(parents=True, exist_ok=True)
                    target.write_text("synthetic fixture\n", encoding="utf-8")

                git("init", "-q", "-b", "main")
                git("config", "user.name", "fixture")
                git("config", "user.email", "fixture@example.invalid")
                git("config", "commit.gpgsign", "false")
                write("app.py"); write("work-tracker/old.md")
                git("add", "-A"); git("commit", "-qm", "Fixture baseline.")
                base = git("rev-parse", "HEAD")
                cases = (("tracker", "work-tracker/new.md", False),
                         ("evidence", "work-tracker/evidence/note.txt", False),
                         ("example", "examples/work-tracker/example.md", True),
                         ("adopter", "docs/work-tracker/example.md", True),
                         ("similar", "work-tracker-copy/note.md", True),
                         ("newline", "work-tracker/line\nbreak.md", False),
                         ("delete", None, True), ("rename", None, False))
                for label, path, accepted in cases:
                    git("checkout", "-q", "-b", label, base)
                    if path:
                        write(path)
                    elif label == "delete":
                        (root / "work-tracker/old.md").rename(area / "old.md")
                    else:
                        (root / "app.py").rename(root / "work-tracker/moved.py")
                    git("add", "-A"); git("commit", "-qm", "Fixture change.")
                    head = git("rev-parse", "HEAD")
                    result = subprocess.run([bash, "--noprofile", "--norc", "-eo", "pipefail", "-c", script],
                                            cwd=root, env=dict(env, BASE=base, HEAD_SHA=head), capture_output=True, text=True)
                    check("path check: " + label, result.returncode == (0 if accepted else 1), result.stderr.strip() if result.returncode != (0 if accepted else 1) else "")
                result = subprocess.run([bash, "--noprofile", "--norc", "-eo", "pipefail", "-c", script],
                                        cwd=root, env=dict(env, BASE="missing-ref", HEAD_SHA=head), capture_output=True, text=True)
                check("an unreadable diff fails closed", result.returncode != 0)

    spec = importlib.util.spec_from_file_location("cut_landing_facts", HERE / "scripts/landing_facts.py")
    landing = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(landing)
    check("landing readers no longer read current trackers", not any(hasattr(landing, name) for name in ("read_wrecks", "read_excerpt", "Chart")))
    template = (HERE / "overrides/landing.html").read_text(encoding="utf-8")
    check("the landing has no tracker chart or board excerpt", not any(token in template for token in
          ("F.wrecks_json", "F.excerpt", "F.counts", 'id="wrecks"', 'id="register"', 'class="peek"', 'id="chart"')))
    used_words = set(re.findall(r"\bw\.(\w+)", template)) - {"key"}
    languages = {}
    for lang in ("en", "de"):
        text = (HERE / f"overrides/partials/landing/{lang}.html").read_text(encoding="utf-8")
        languages[lang] = ast.literal_eval(re.search(r"{% set w = (.*?) %}", text, re.S)[1])
        check("all template words exist in " + lang, used_words <= languages[lang].keys())
        check("the footer names only the remaining figures in " + lang,
              not any(word in languages[lang]["foot_fine"] for word in ("wrecks", "excerpt", "Wracks", "Auszug")))
    check("the two landing dictionaries have the same keys", languages["en"].keys() == languages["de"].keys())
    return rows


if __name__ == "__main__":
    results = run_checks()
    for label, ok, detail in results:
        print(("ok " if ok else "FAIL ") + label + (": " + detail if detail else ""))
    raise SystemExit(any(not ok for _label, ok, _detail in results))
