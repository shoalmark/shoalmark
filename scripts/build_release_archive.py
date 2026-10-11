"""The release archive (FM-004, item 8): `shoalmark-<version>.zip` and its `.sha256`, built from a tag — or, for the dry run, a commit.

    python3 scripts/build_release_archive.py [--out DIR] [--repo DIR] -- <v<x.y.z> | 40-hex commit>

The one build: `.github/workflows/release.yml` runs it on a pushed tag and on its dry run, and the suite's check runs this same file.

- **What it holds:** the files `--vendor` copies — `TOOL_FILES`, the brand's own files beside the tool and the themes it ships — read from the commit's git
  objects, never from the working tree, at the zip's root with no folder around them (D7); and `RELEASE`, a manifest of the version, the tag, the commit
  and each file's SHA-256. The manifest proves the set complete, not its origin: whoever changes the zip can rewrite it. The origin is the zip's own
  SHA-256 against a pin published outside it.
- **Reproducible:** entries sorted, stored and not deflated (its SHA-256 rests on no zlib version), one timestamp — the commit's committer time read in
  UTC — fixed modes, no extra field. Built again from the same commit, anywhere and in any time zone, it gives the same bytes.
- **Its input is checked before use:** a tag `v<x.y.z>` or a 40-hex commit, nothing else, so no value reaches git as an option. For a tag, `VERSION` at
  its commit must be the tag less its `v`, or nothing is written.

It writes `<out>/shoalmark-<version>.zip` and `<out>/shoalmark-<version>.zip.sha256` — `<hex>  shoalmark-<version>.zip` and a line end, the form
`shasum -a 256 -c` reads — and prints the zip's name, its size and its SHA-256. Exit 0 when written; 2 for an input it refuses; 1 for a commit it cannot
build from. Nothing is written unless everything is.
"""

import argparse
import ast
import hashlib
import io
import os
import pathlib
import re
import subprocess
import sys
import time
import zipfile

REF_RE = re.compile(r"v[0-9]+\.[0-9]+\.[0-9]+|[0-9a-f]{40}")          # ASCII digits only: `\d` would take any script's digits
RELEASE_NAME = "RELEASE"
RELEASE_HEAD = "# shoalmark release manifest"          # the line `release_manifest` in shoalmark.py reads first
THEMES = "brand/themes/"
MODE = 0o100644                                         # every entry a regular file, rw-r--r--


class Refused(Exception):
    """What the build will not do, in one line; nothing is written."""


def git(repo, *args):
    """One read of git in `repo`, its bytes — the environment's git variables dropped, so it reads `repo` and nothing a caller's hook set."""
    env = {k: v for k, v in os.environ.items() if k not in ("GIT_DIR", "GIT_WORK_TREE", "GIT_INDEX_FILE", "GIT_PREFIX", "GIT_LITERAL_PATHSPECS",
                                                             "GIT_GLOB_PATHSPECS", "GIT_NOGLOB_PATHSPECS", "GIT_ICASE_PATHSPECS")}
    r = subprocess.run(["git", *args], cwd=repo, stdin=subprocess.DEVNULL, capture_output=True, env=env)
    if r.returncode != 0:
        raise Refused(f"git {args[0]} failed: {r.stderr.decode('utf-8', 'replace').strip().splitlines()[-1:] or ['(no message)']}")
    return r.stdout


def literal(source, name, needed=True):
    """The tuple of strings `name` is bound to at the top of the tool's source, read without running it — () where it binds none and none is `needed`."""
    for node in ast.parse(source).body:
        if isinstance(node, ast.Assign) and any(isinstance(t, ast.Name) and t.id == name for t in node.targets):
            value = ast.literal_eval(node.value)
            if isinstance(value, tuple) and all(isinstance(v, str) for v in value):
                return value
    if needed:
        raise Refused(f"shoalmark.py at the commit binds no tuple of names to {name}")
    return ()


def vendored_set(paths, tool_source):
    """What `--vendor` copies from a tool whose tree holds `paths`, as `vendor_files` in shoalmark.py reads it: `TOOL_FILES`, each required; the brand's
    own files beside the tool there are; and every file under `brand/themes/` whose name has no part that starts with a dot — `THEME_FILES`, where the
    tool binds it, each required too: an unpacked archive is vendored only whole (`archive_check`)."""
    tool_files, brand_files = literal(tool_source, "TOOL_FILES"), literal(tool_source, "BRAND_FILES")
    missing = [rel for rel in tool_files + literal(tool_source, "THEME_FILES", needed=False) if rel not in paths]
    if missing:
        raise Refused(f"the commit lacks {', '.join(missing)}: it is not the whole tool")
    brand = [f"brand/{n}" for n in brand_files if f"brand/{n}" in paths]
    themes = [p for p in paths if p.startswith(THEMES) and not any(part.startswith(".") for part in p[len(THEMES):].split("/"))]
    return sorted(set(tool_files) | set(brand) | set(themes))


def build(repo, ref):
    """(version, the zip's bytes) for `ref`, read from git in `repo`; `Refused` before anything is written where it cannot be built."""
    if not REF_RE.fullmatch(ref or ""):
        raise Refused(f"{ref!r} is neither a tag v<x.y.z> nor a 40-hex commit")
    rev = f"refs/tags/{ref}" if ref.startswith("v") else ref
    commit = git(repo, "rev-parse", "--verify", "--quiet", f"{rev}^{{commit}}").decode("ascii").strip()
    version = git(repo, "cat-file", "blob", f"{commit}:VERSION").decode("utf-8").strip()
    if ref.startswith("v") and version != ref[1:]:
        raise Refused(f"VERSION at {ref} is {version!r}, not {ref[1:]!r}: nothing is written")
    if not re.fullmatch(r"[0-9]+\.[0-9]+\.[0-9]+", version):
        raise Refused(f"VERSION at {commit[:12]} is {version!r}, no release version")
    tree = {}
    for entry in git(repo, "ls-tree", "-r", "-z", "--full-tree", commit).split(b"\0"):
        if entry:
            meta, _, path = entry.partition(b"\t")
            mode, kind, obj = meta.decode("ascii").split()
            tree[path.decode("utf-8")] = (mode, kind, obj)
    names = vendored_set(set(tree), git(repo, "cat-file", "blob", f"{commit}:shoalmark.py").decode("utf-8"))
    odd = [n for n in names if tree[n][1] != "blob" or tree[n][0] not in ("100644", "100755")]
    if odd:
        raise Refused(f"{', '.join(odd)} at the commit is no regular file")
    files = {n: git(repo, "cat-file", "blob", tree[n][2]) for n in names}
    stamp = time.gmtime(int(git(repo, "show", "-s", "--format=%ct", commit).decode("ascii").strip()))[:6]     # the committer time, read in UTC
    tag = ref if ref.startswith("v") else "none"
    manifest = "".join([f"{RELEASE_HEAD}\n", f"version {version}\n", f"tag {tag}\n", f"commit {commit}\n"]
                       + [f"{hashlib.sha256(files[n]).hexdigest()}  {n}\n" for n in names]).encode("utf-8")
    out = io.BytesIO()
    with zipfile.ZipFile(out, "w", compression=zipfile.ZIP_STORED) as z:
        for name in sorted(names + [RELEASE_NAME]):
            info = zipfile.ZipInfo(name, date_time=stamp)
            info.compress_type, info.create_system, info.external_attr, info.extra, info.comment = zipfile.ZIP_STORED, 3, MODE << 16, b"", b""
            z.writestr(info, manifest if name == RELEASE_NAME else files[name])
    return version, out.getvalue()


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("ref", help="a tag v<x.y.z>, or a 40-hex commit for the dry run")
    ap.add_argument("--out", default=".", help="the folder the two files are written to (default: here)")
    ap.add_argument("--repo", default=".", help="the git repository read (default: here)")
    try:
        args = ap.parse_args(argv)
    except SystemExit as e:
        return 2 if e.code else 0
    try:
        if not REF_RE.fullmatch(args.ref or ""):
            raise Refused(f"{args.ref!r} is neither a tag v<x.y.z> nor a 40-hex commit")
        version, data = build(pathlib.Path(args.repo), args.ref)
    except Refused as e:
        print(f"build_release_archive: {e}", file=sys.stderr)
        return 2 if not REF_RE.fullmatch(args.ref or "") else 1
    name, digest = f"shoalmark-{version}.zip", hashlib.sha256(data).hexdigest()
    out = pathlib.Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    (out / name).write_bytes(data)
    (out / f"{name}.sha256").write_bytes(f"{digest}  {name}\n".encode("ascii"))
    print(f"{name} {len(data)} bytes sha256 {digest}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
