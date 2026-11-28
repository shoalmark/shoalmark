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

                def git(*args, env=env, input=None):
                    return subprocess.check_output(["git", "-C", str(root), *args], env=env, input=input,
                                                   stderr=subprocess.STDOUT).decode().strip()

                def write(path):
                    target = root / path
                    target.parent.mkdir(parents=True, exist_ok=True)
                    target.write_text("synthetic fixture\n", encoding="utf-8")

                def working_tree():
                    return {p.relative_to(root): p.read_bytes() if p.is_file() else None
                            for p in root.rglob("*") if ".git" not in p.relative_to(root).parts}

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
                    try:
                        if label == "newline":
                            before_head = git("rev-parse", "HEAD")
                            before_index = (root / ".git/index").read_bytes()
                            before_tree = working_tree()
                            blob = git("hash-object", "-w", "--stdin", input=b"synthetic fixture\n")
                            entries = git("ls-tree", "-z", base + ":work-tracker")
                            tracker_tree = git("mktree", "-z", input=(entries + f"100644 blob {blob}\tline\nbreak.md\0").encode())
                            entries = git("ls-tree", "-z", base).split("\0")
                            entries = [f"040000 tree {tracker_tree}\twork-tracker" if entry.split("\t", 1)[1] == "work-tracker" else entry
                                       for entry in entries if entry]
                            tree = git("mktree", "-z", input=("\0".join(entries) + "\0").encode())
                            head = git("commit-tree", tree, "-p", base, "-m", "Fixture change.")
                            base_paths = git("ls-tree", "-r", "-z", "--name-only", base).split("\0")[:-1]
                            paths = git("ls-tree", "-r", "-z", "--name-only", head).split("\0")[:-1]
                            check("the newline commit contains exactly the base paths and the new path", sorted(paths) == sorted(base_paths + [path]))
                        else:
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
                        if label == "newline":
                            check("the newline case leaves HEAD unchanged", git("rev-parse", "HEAD") == before_head)
                            check("the newline case leaves the shared index unchanged", (root / ".git/index").read_bytes() == before_index)
                            check("the newline case leaves the working tree unchanged", working_tree() == before_tree)
                    except Exception as error:
                        output = getattr(error, "output", "")
                        if isinstance(output, bytes):
                            output = output.decode(errors="replace")
                        check("path check: " + label, False, f"{type(error).__name__}: {error}\n{output or ''}".strip())
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
