"""The history replay for the signed identity (FM-024; the Owner's ruling filed in FM-006, *The release bar*, on a private security report).

Over the default branch's whole history, every judgement the gate makes of a signed line or a signature is run twice — by the tool as it was
before the change (79be49d) and by the tool after it (HEAD) — and compared. A judgement that passed before and is refused after is a NEW
REFUSAL; there must be none. What it runs, per tool:

- `verified_as`'s callers in the lint — every answer line, every `next: owner` line and every rights change `--check` judges at the branch's
  tip — read as the refusal lines `--check` prints about a signature;
- `answer_reading`, which `--queue` reads an answer branch by and the board and `--owner` say *signed* by (`on_their_way`), on every signed
  commit of the history;
- FM-037's guard of the Owner's two sections and the signers file, with its real-history walk (`guard_walk`, then `guard_verdicts` against
  the Owner the branch's configuration names).

It reads git and writes nothing in this repository: the work happens in a temporary clone, checked out at the branch, whose signers file is
the repository's own. Run from the repository's root:

    python3 work-tracker/evidence/FM-006/signed-history-replay.py [--main origin/main] [--before 79be49d] [--after HEAD]

It prints the signed commits it saw by kind, each judgement's counts and the new refusals, and exits 0 where there are none, 1 otherwise.
"""

import argparse
import contextlib
import importlib.util
import io
import os
import pathlib
import re
import subprocess
import sys
import tempfile

HERE = pathlib.Path(__file__).resolve()
REPO = pathlib.Path(subprocess.run(["git", "-C", str(HERE.parent), "rev-parse", "--show-toplevel"], capture_output=True, text=True, check=True).stdout.strip())
ENV = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
SIGNATURE_LINE = re.compile(r"verify|signed|signature|SSH|GPG", re.I)


def git(*a, cwd=REPO, text=True):
    return subprocess.run(["git", *a], cwd=cwd, capture_output=True, text=text, env=ENV, check=True).stdout


def tool_at(rev, into):
    """The tool as `rev` had it — `worktree`: as the working tree has it — laid out as it runs (its file, VERSION, vendored `marked` and themes),
    loaded as a module of its own."""
    into.mkdir(parents=True)
    for rel in git("ls-tree", "-r", "--name-only", "HEAD" if rev == "worktree" else rev).split("\n"):
        if rel in ("shoalmark.py", "VERSION") or rel.startswith(("vendor/", "brand/themes/")):
            (into / rel).parent.mkdir(parents=True, exist_ok=True)
            (into / rel).write_bytes((REPO / rel).read_bytes() if rev == "worktree" else git("show", f"{rev}:{rel}", text=False))
    spec = importlib.util.spec_from_file_location(f"shoalmark_{rev}", into / "shoalmark.py")
    module = importlib.util.module_from_spec(spec)
    with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
        spec.loader.exec_module(module)
    return module


def judge(tool, clone, main, signed):
    """Every judgement of a signed line or a signature `tool` makes over the history: {name: {key: (passed, what it said)}}."""
    tool.configure(clone)
    out = {}
    err = io.StringIO()
    with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(err):
        tool.main(["--root", str(clone), "--check"])
    lines = [l.strip() for l in err.getvalue().splitlines() if SIGNATURE_LINE.search(l) and ("lint:" in l or "checkout:" in l or "refused" in l)]
    key = lambda l: re.sub(r"^(lint|checkout): ", "", l).split(":")[0] + (" · cannot verify" if "cannot verify" in l else " · refused")     # by tracker and kind, not wording
    out["lint at the tip (answers, asks, rights)"] = {key(l): (False, l) for l in lines}
    tool.configure(clone)
    out["answer_reading (--queue, the board, --owner)"] = {c: (r[0] == "merge", r[1]) for c in signed for r in [tool.answer_reading(c)]}
    tool.configure(clone)
    _n, changed = tool.guard_walk(main)
    verdicts = tool.guard_verdicts(changed, tool.owners_at(main))
    out["FM-037's guard (guard_walk, guard_verdicts)"] = {c: (v != "refused", f"{v} {w}".strip()) for c, _s, _h, _w, v, w in verdicts}
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--main", default="origin/main", help="the default branch to replay (default origin/main)")
    ap.add_argument("--before", default="79be49d", help="the tool before the change (default 79be49d)")
    ap.add_argument("--after", default="HEAD", help="the tool after it (default HEAD; `worktree` for the working tree's)")
    args = ap.parse_args()
    main_sha = git("rev-parse", args.main).strip()
    with tempfile.TemporaryDirectory() as d:
        base = pathlib.Path(d)
        clone = base / "clone"
        subprocess.run(["git", "clone", "--quiet", "--no-checkout", "--shared", str(REPO), str(clone)], check=True, env=ENV, capture_output=True)
        git("checkout", "--quiet", "--detach", main_sha, cwd=clone)
        git("update-ref", "refs/remotes/origin/main", main_sha, cwd=clone)
        git("symbolic-ref", "refs/remotes/origin/HEAD", "refs/remotes/origin/main", cwd=clone)
        git("config", "gpg.ssh.allowedSignersFile", str(clone / "work-tracker" / "allowed_signers"), cwd=clone)
        commits = git("rev-list", main_sha, cwd=clone).split()
        kinds, github = {}, 0
        signed = []
        for c in commits:
            head = git("cat-file", "commit", c, cwd=clone).split("\n\n", 1)[0]
            m = re.search(r"^gpgsig(?:-sha256)? (.*)$", head, re.M)
            if not m:
                continue
            kind = "ssh" if "SSH SIGNATURE" in m.group(1) else "pgp" if "PGP SIGNATURE" in m.group(1) else "other"
            kinds[kind] = kinds.get(kind, 0) + 1
            github += kind == "pgp" and "\ncommitter GitHub <noreply@github.com>" in "\n" + head
            signed.append(c)
        os.chdir(clone)
        before = judge(tool_at(args.before, base / "before"), clone, main_sha, signed)
        after = judge(tool_at(args.after, base / "after"), clone, main_sha, signed)
    print(f"{args.main} at {main_sha[:10]}: {len(commits)} commits, {len(signed)} signed — "
          + ", ".join(f"{n} {k.upper()}" for k, n in sorted(kinds.items())) + f"; {github} of the PGP ones committed by GitHub (noreply@github.com)")
    new = []
    for name in before:
        b, a = before[name], after[name]
        if name.startswith("lint"):
            fresh = sorted(set(a) - set(b))
            print(f"- {name}: {len(b)} signature line(s) before, {len(a)} after; new: {len(fresh)}")
            new += [f"{name}: {l}" for l in fresh]
            continue
        passed_b, passed_a = sum(p for p, _w in b.values()), sum(p for p, _w in a.values())
        fresh = sorted(k for k in b if b[k][0] and not a.get(k, (True, ""))[0])
        print(f"- {name}: {len(b)} judged; passed {passed_b} before, {passed_a} after; new refusals: {len(fresh)}")
        new += [f"{name}: {k[:10]} — before: {b[k][1]} · after: {a[k][1]}" for k in fresh]
    print("new refusals: none" if not new else "NEW REFUSALS:\n  " + "\n  ".join(new))
    return 1 if new else 0


if __name__ == "__main__":
    sys.exit(main())
