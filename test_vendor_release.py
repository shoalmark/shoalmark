"""FM-061 — R17: `--vendor` takes only a tagged, verified, complete release.

The class test of the Owner's ruling R17 (signed 12 October): no seat chooses a weaker trusted pin.

- `--partial` and `--allow-untagged`, given, are each refused in one line saying R17 removed them, exit 2, nothing written —
  before and after `--help` and `--version` too (RV-3367).
- `--vendor` refuses an untagged source and a partial one, each in one line with its reason, exit 4, nothing written: a
  Git checkout past its tag, one at its tag with a change, one at its tag that lacks a file of the tool, and an unpacked
  archive whose RELEASE names no tag.
- A copy vendored through either flag before runs as pinned: its `--check` names each flag it came through and what to
  do, exit 0; the next `--vendor` that meets it names it too, refused or not, and replaces it with a release.
- From a Git source the copy holds the tag's own bytes, read from the tag's tree (RV-3364: recorded privately): a file
  whose bytes on disk are not the tag's is named and the run refused, nothing written, whatever `git status` reports; a
  file beside the tool that the tag does not hold, an ignored one included, is named and never copied; an untouched
  source vendors byte for byte from the tag, and so does a checkout whose line ends git converted to CRLF.
- A checkout's line ends are judged by git's own rules: a mixed-end, a binary or a lone-CR file is accepted only as the tag
  holds it (RV-3366: recorded privately).
- A source refused because a committed attribute converts the tag's own file on checkout is told to vendor from that
  release's unpacked archive (RV-3376: recorded privately).
- Every read of a Git source sees git's own objects, with no replacement object and no graft (RV-3365: recorded privately):
  a replacement commit or tree with another file on disk vendors only the tag's bytes, or is refused before writing — with
  core.useReplaceRefs true in the source's configuration or a global one too, and every source read starts with
  core.useReplaceRefs=false as its last configuration parameter (RV-3369: recorded privately).

Every run is the tool as a program, started from a release made of it: the files `--vendor` copies, committed in a
scratch repository tagged `v<VERSION>`, or laid out as an unpacked release archive with its RELEASE. Run it directly,
`python3 test_vendor_release.py [tool]`, or through test_shoalmark.py. With `--mutants` it also runs against each mutant
of the tool and against the tool before R17, and each of them must fail it; under each of the three mutants of the tag's
bytes, the case it is paired with fails and the clean control passes.
"""

import datetime
import hashlib
import importlib.util
import os
import pathlib
import re
import subprocess
import sys
import tempfile


HERE = pathlib.Path(__file__).resolve().parent
ENV = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
ENV.update(GIT_AUTHOR_NAME="t", GIT_AUTHOR_EMAIL="t@t", GIT_COMMITTER_NAME="t", GIT_COMMITTER_EMAIL="t@t")
EARLIER = "2026-10-01"                      # the day an earlier `--vendor` wrote a PIN through a bypass, in the fixtures
BEFORE_R17 = "1148114"                      # main before R17: both bypasses open, and a copy made through one not named in R17's terms
SAYS = "R17 removed that flag: the copy runs as pinned; vendor again from a tagged, verified, complete release to replace it"

# Each mutant: its name, a line of the tool as it stands and what the mutant puts there. Each must FAIL the class test.
MUTANTS = (
    ("--partial still accepted: given, it is ignored",
     '    return [flag for flag in R17_FLAGS if flag in given]',
     '    return [flag for flag in R17_FLAGS if flag in given and flag != "--partial"]'),
    ("--allow-untagged still accepted: given, it is ignored",
     '    return [flag for flag in R17_FLAGS if flag in given]',
     '    return [flag for flag in R17_FLAGS if flag in given and flag != "--allow-untagged"]'),
    ("the removed flags read after argparse again: --help and --version end the run first",
     '    removed = r17_removed(r17_given(sys.argv[1:] if argv is None else list(argv)))',
     '    args = parse_args(argv); removed = r17_removed(r17_given(sys.argv[1:] if argv is None else list(argv)))'),
    ("a partial source vendored again",
     "        missing = [rel for rel in TOOL_FILES if not (HERE / rel).is_file()]",
     "        missing = []"),
    ("an untagged source vendored again",
     "            tag, sha, _dirty, why = source_provenance()",
     '            tag, sha, _dirty, why = (*source_provenance()[:3], "")'),
    ("a dry run's archive vendored again",
     '        if not release["tag"]:',
     '        if not release["tag"] and False:'),
    ("the leftover not named by --check",
     '        + ["warning: " + line for line in bypass_lines(m, "this copy")]',
     "        + []"),
    ("the leftover not named by --vendor",
     '        print("note: " + line)',
     "        pass"),
    ("the advice without the release's unpacked archive",
     "    return f\"Check out {tag} again in a clean clone and vendor from there, or vendor from that release's unpacked archive.\"",
     "    return f\"Check out {tag} again in a clean clone and vendor from there.\""),
    ("the leftover broken: --vendor refuses it",
     '        print("note: " + line)',
     '        print("--vendor: " + line, file=sys.stderr); return EXIT_LINT'),
)
# The mutants of the tag's bytes: each with the case that must FAIL under it; the clean control must pass under each.
CLEAN = "the clean control:"
TAG_MUTANTS = (
    ("copy from disk again", "        data[rel] = blob.stdout", "        data[rel] = disk",
     "a checkout whose line ends git converted to CRLF"),
    ("trust git status again", "        if disk != blob.stdout and disk != crlf_checkout(", "        if False and disk != blob.stdout and disk != crlf_checkout(",
     "changed on disk behind `git update-index"),
    ("the wide CRLF rule again", "disk != crlf_checkout(blob.stdout)", 'disk != re.sub(rb"(?<!\\r)\\n", b"\\r\\n", blob.stdout)',
     "with every lone LF made CRLF on disk"),
    ("copy a path outside the tag again", "        copied = [rel for rel in copied if rel in data]",
     "        data.update((rel, (HERE / rel).read_bytes()) for rel in beside)",
     "a file beside the tool that the tag does not hold"),
    ("read with replacement objects on again: the two variables and the fixed parameter dropped together",
     '        options["env"] = dict(source_env, GIT_CONFIG_PARAMETERS=inherited + (" " if inherited else "") + SOURCE_GIT_PARAMETER, **SOURCE_GIT_ENV)',
     '        options["env"] = source_env',
     "a replacement "),
    ("the fixed parameter dropped", 'GIT_CONFIG_PARAMETERS=inherited + (" " if inherited else "") + SOURCE_GIT_PARAMETER', "GIT_CONFIG_PARAMETERS=inherited",
     "an actual source read starts with"),
    ("the fixed parameter before the inherited ones", 'GIT_CONFIG_PARAMETERS=inherited + (" " if inherited else "") + SOURCE_GIT_PARAMETER',
     'GIT_CONFIG_PARAMETERS=SOURCE_GIT_PARAMETER + (" " if inherited else "") + inherited',
     "an actual source read starts with"),
)


def load(path):
    spec = importlib.util.spec_from_file_location("vendor_release_tool", str(path))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def git(cwd, *args):
    return subprocess.run(["git", "-C", str(cwd), "-c", "commit.gpgsign=false", "-c", "tag.gpgsign=false", "-c", "core.hooksPath=/dev/null",
                           "-c", "core.autocrlf=false", *args],          # a fixture's blobs are the bytes it wrote, on every system
                          check=True, capture_output=True, text=True, encoding="utf-8", errors="replace", env=ENV).stdout.strip()


def show(repo, rel):
    """The bytes of `rel` as the tag's tree holds them: its blob at HEAD."""
    return subprocess.run(["git", "-C", str(repo), "cat-file", "blob", f"HEAD:{rel}"], check=True, capture_output=True, env=ENV).stdout


def program(tool, *args, cwd, env=None):
    """The tool as a program, as a consumer starts it — `env` beside the suite's own: (exit, stdout, stderr)."""
    done = subprocess.run([sys.executable, str(tool), *args], cwd=str(cwd), capture_output=True, text=True, encoding="utf-8", errors="replace",
                          env=dict(ENV, **(env or {})))
    return done.returncode, done.stdout, done.stderr


def lay_out(into, files):
    for rel, data in files.items():
        (into / rel).parent.mkdir(parents=True, exist_ok=True)
        (into / rel).write_bytes(data)


def tool_files(fm, tool_bytes, leave_out=()):
    """The files `--vendor` copies, as this tree holds them and `shoalmark.py` as `tool_bytes`: {path: bytes}."""
    return {rel: tool_bytes if rel == "shoalmark.py" else (HERE / rel).read_bytes() for rel in fm.vendor_files() if rel not in leave_out}


def release(into, fm, tool_bytes, leave_out=(), shape=lambda data: data, extra=None, raw=None):
    """A release: the tool's files, each as `shape` gives it, the files `extra` names, and the files `raw` names committed as their bytes with no
    attribute applied, in a scratch repository tagged `v<VERSION>`, `leave_out` never committed. Its commit."""
    into.mkdir(parents=True)
    lay_out(into, dict({rel: shape(data) for rel, data in tool_files(fm, tool_bytes, leave_out).items()}, **(extra or {}), **(raw or {})))
    git(into, "init", "-q")
    git(into, "add", "-A")
    for rel in raw or {}:
        git(into, "update-index", "--add", "--cacheinfo", "100644," + git(into, "hash-object", "-w", "--no-filters", rel) + "," + rel)
    git(into, "commit", "-qm", "the release")
    git(into, "tag", f"v{fm.__version__}")
    return git(into, "rev-parse", "HEAD")


def archive(into, fm, tool_bytes, tag):
    """An unpacked release archive: the tool's files and the probe's, and its RELEASE naming each with its SHA-256; `tag` "none" is a dry run's."""
    into.mkdir(parents=True)
    files = dict(tool_files(fm, tool_bytes), **{rel: (HERE / rel).read_bytes() for rel in fm.ARCHIVE_FILES})
    lay_out(into, files)
    head = f"# shoalmark release manifest\nversion {fm.__version__}\ntag {tag}\ncommit {hashlib.sha1(tag.encode('ascii')).hexdigest()}\n"
    (into / "RELEASE").write_bytes((head + "".join(f"{hashlib.sha256(files[rel]).hexdigest()}  {rel}\n" for rel in sorted(files))).encode("utf-8"))


def one_line(err):
    return err.count("\n") == 1 and err.endswith("\n")


def said_for(lines, lead, named):
    """Whether `lines` hold, for each (flag, what) in `named`, the line `lead` + `vendored through <flag>, from <what> — ` + SAYS — and no other such line."""
    found = [l for l in lines if l.startswith(lead + " was vendored through ")]
    return len(found) == len(named) and all(any(l == f"{lead} was vendored through {flag}, from {what} — {SAYS}" for l in found) for flag, what in named)


def run_checks(fm, tool=None):
    """The class test against the tool at `tool`, by default `fm`'s own file; `fm` gives the constants: [(label, ok, what it saw)]."""
    tool_bytes = pathlib.Path(tool or fm.__file__).read_bytes()
    results = []

    def check(label, ok, saw=""):
        results.append(("FM-061 · R17 · " + label, bool(ok), saw))

    try:
        with tempfile.TemporaryDirectory() as d:
            steps(check, fm, tool_bytes, pathlib.Path(d).resolve())
        with tempfile.TemporaryDirectory() as d:
            tag_steps(check, fm, tool_bytes, pathlib.Path(d).resolve())
        env_steps(check, pathlib.Path(tool or fm.__file__))
    except Exception as error:                               # a fixture step that fails is a named FAIL with what it saw, never a traceback that ends the run
        check("the class test ran to its end", False, f"{type(error).__name__}: {error}")
    return results


def steps(check, fm, tool_bytes, base):
    """The class test's steps, in `base`: each finding through `check`."""
    ver, lint, today = fm.__version__, fm.EXIT_LINT, datetime.date.today().isoformat()
    src = base / "release"
    tagged = release(src, fm, tool_bytes)
    root = base / "consumer"
    root.mkdir()
    git(root, "init", "-q")
    copy = root / "tools" / "shoalmark"
    mine = lambda *a: program(copy / "shoalmark.py", "--root", str(root), *a, cwd=root)

    # the controls: from a release, `--vendor` vendors, and the consumer's copy runs and is read as a release
    c, o, e = program(src / "shoalmark.py", "--vendor", str(copy), cwd=root)
    pin = (copy / "PIN").read_text(encoding="utf-8") if (copy / "PIN").is_file() else ""
    check("the control: from a clean clone at its release tag, --vendor vendors the whole tool, its PIN's manifest tagged and complete",
          c == 0 and pin.startswith(f"# shoalmark {ver} · tag v{ver} · commit {tagged} · vendored {today} · complete\n"), f"exit {c}, {pin[:100]!r}, {e.strip()[-160:]!r}")
    mine("--init", "--key", "msr")
    mine()
    c, o, e = mine("--check")
    check("the control: the consumer's --check reads where its copy came from and warns of nothing, exit 0",
          c == 0 and f"pinned {ver} from tag v{ver} (commit {tagged[:10]})" in o and "warning" not in o and "R17" not in o + e, f"exit {c}, {(o + e).strip()[-200:]!r}")

    # each removed flag, given: one line saying R17 removed it, exit 2, nothing written — from a release that would otherwise vendor
    for flags in (("--partial",), ("--allow-untagged",), ("--partial", "--allow-untagged")):
        dest = base / ("with" + "".join(flags)) / "tools" / "shoalmark"
        c, o, e = program(src / "shoalmark.py", "--vendor", str(dest), *flags, cwd=base)
        it = "it" if len(flags) == 1 else "them"
        check(f"`--vendor DIR {' '.join(flags)}` from a release is refused in one line saying R17 removed {it}, exit 2, nothing written",
              c == 2 and o == "" and one_line(e) and e.startswith(f"{' and '.join(flags)}: R17 removed {it} — --vendor takes only a tagged, verified, complete release")
              and not dest.parent.parent.exists(), f"exit {c}, {(o + e).strip()[-160:]!r}")
    pinned = (copy / "PIN").read_bytes()
    c, o, e = mine("--check", "--allow-untagged")
    check("given with any other run — the consumer's --check — `--allow-untagged` is refused the same way, exit 2, its copy as pinned",
          c == 2 and o == "" and one_line(e) and e.startswith("--allow-untagged: R17 removed it — ") and (copy / "PIN").read_bytes() == pinned, f"exit {c}, {(o + e).strip()[-160:]!r}")

    # each removed flag before and after `--help` and `--version` (RV-3367): named before argparse can end the run
    for flag in ("--partial", "--allow-untagged"):
        for action in ("--help", "--version"):
            for words in ((flag, action), (action, flag)):
                c, o, e = program(src / "shoalmark.py", *words, cwd=base)
                check(f"`{' '.join(words)}` is refused in one line saying R17 removed {flag}, exit 2 — the flag is named before {action} can end the run",
                      c == 2 and o == "" and one_line(e) and e.startswith(f"{flag}: R17 removed it — "), f"exit {c}, {(o + e).strip()[:120]!r}")

    # an untagged source: past its tag, or at it with a change — refused with its reason, and no flag offered
    git(src, "commit", "-q", "--allow-empty", "-m", "past the tag")
    moved = git(src, "rev-parse", "HEAD")
    dest = base / "past" / "tools" / "shoalmark"
    c, o, e = program(src / "shoalmark.py", "--vendor", str(dest), cwd=base)
    check("an untagged source — a clean checkout one commit past its release tag — is refused in one line naming HEAD and the tag, exit 4, nothing written; no flag offered",
          c == lint and o == "" and one_line(e) and f"HEAD {moved[:10]} is not at the tag v{ver}" in e and "--allow-untagged" not in e
          and not dest.parent.parent.exists(), f"exit {c}, {(o + e).strip()[-160:]!r}")
    git(src, "checkout", "-q", f"v{ver}")
    (src / "README.md").write_bytes((src / "README.md").read_bytes() + b"\na local change\n")
    dest = base / "changed" / "tools" / "shoalmark"
    c, o, e = program(src / "shoalmark.py", "--vendor", str(dest), cwd=base)
    check("an untagged source — a checkout at its release tag with a change — is refused in one line naming the path, exit 4, nothing written; no flag offered",
          c == lint and o == "" and one_line(e) and "the tree has changes: README.md" in e and "--allow-untagged" not in e
          and not dest.parent.parent.exists(), f"exit {c}, {(o + e).strip()[-160:]!r}")
    git(src, "checkout", "-q", "--", "README.md")

    # a partial source: a clean clone at its tag that lacks a file of the tool
    part = base / "partial-release"
    release(part, fm, tool_bytes, leave_out=("NOTICE",))
    dest = base / "partial" / "tools" / "shoalmark"
    c, o, e = program(part / "shoalmark.py", "--vendor", str(dest), cwd=base)
    check("a partial source — a clean clone at its release tag that lacks a file of the tool — is refused in one line naming it, exit 4, nothing written; no flag offered",
          c == lint and o == "" and one_line(e) and "is not the whole tool — missing NOTICE" in e and "--partial" not in e
          and not dest.parent.parent.exists(), f"exit {c}, {(o + e).strip()[-160:]!r}")

    # an unpacked archive: a release's vendors; a dry run's, whose RELEASE names no tag, is refused however whole
    whole, dry = base / "archive", base / "dry-run"
    archive(whole, fm, tool_bytes, f"v{ver}")
    archive(dry, fm, tool_bytes, "none")
    seen = {}
    for name, unpacked in (("release", whole), ("dry", dry)):
        p = base / f"from-{unpacked.name}"
        p.mkdir()
        git(p, "init", "-q")
        seen[name] = (p,) + program(unpacked / "shoalmark.py", "--root", str(p), "--vendor", str(p / "tools" / "shoalmark"), cwd=p)
    p, c, o, e = seen["release"]
    apin = (p / "tools/shoalmark/PIN").read_text(encoding="utf-8") if (p / "tools/shoalmark/PIN").is_file() else ""
    check("the control: from an unpacked release archive whose RELEASE names its tag, --vendor vendors, its PIN naming that tag",
          c == 0 and apin.startswith(f"# shoalmark {ver} · vendored from an archive whose manifest names v{ver}, commit "), f"exit {c}, {apin[:100]!r}, {e.strip()[-160:]!r}")
    p, c, o, e = seen["dry"]
    check("an untagged source — an unpacked archive whose RELEASE names no tag, a dry run's, whole and matched — is refused in one line, exit 4, nothing written; no flag offered",
          c == lint and o == "" and one_line(e) and "names no release tag" in e and "--allow-untagged" not in e and not (p / "tools").exists(),
          f"exit {c}, {(o + e).strip()[-160:]!r}")

    # a copy vendored through a bypass before: its PIN as that `--vendor` wrote it, and the files it lacked absent from the copy and its PIN
    body = [l for l in pin.splitlines() if not l.startswith("#")]
    forms = (("--allow-untagged, from a working copy", f"# shoalmark {ver} · untagged {moved[:10]} (dirty) · vendored {EARLIER} · complete", (),
              [("--allow-untagged", f"a working copy, untagged {moved[:10]} (dirty)")]),
             ("--allow-untagged, from a dry run's archive",
              f"# shoalmark {ver} · vendored from an archive whose manifest names no tag, commit {'1' * 40}, every file matched · {EARLIER}", (),
              [("--allow-untagged", "an archive whose manifest names no release tag")]),
             ("--partial", f"# shoalmark {ver} · tag v{ver} · commit {tagged} · vendored {EARLIER} · partial\n# missing: NOTICE", ("NOTICE",),
              [("--partial", "a source missing NOTICE")]),
             ("both flags", f"# shoalmark {ver} · untagged {moved[:10]} · vendored {EARLIER} · partial\n# missing: NOTICE", ("NOTICE",),
              [("--allow-untagged", f"a working copy, untagged {moved[:10]}"), ("--partial", "a source missing NOTICE")]))
    for name, head, gone, named in forms:
        for rel in gone:
            (copy / rel).unlink(missing_ok=True)       # already gone where a run before left the copy so
        (copy / "PIN").write_bytes((head + "\n" + "".join(l + "\n" for l in body if l.partition("  ")[2] not in gone)).encode("utf-8"))
        earlier = (copy / "PIN").read_bytes()
        ran = mine()[0]
        c, o, e = mine("--check")
        check(f"a copy vendored before through {name} runs as pinned, and its --check names each flag it came through, with what to do — exit 0",
              ran == 0 and c == 0 and said_for(o.splitlines(), "warning: this copy", named), f"run {ran}, exit {c}, {(o + e).strip()[-260:]!r}")
        c, o, e = program(dry / "shoalmark.py", "--root", str(root), "--vendor", str(copy), cwd=root)
        check(f"…the next --vendor that meets it names it the same way, refused or not: from a dry run's archive, one line, exit 4, the copy as it was ({name})",
              c == lint and one_line(e) and said_for(o.splitlines(), f"note: the copy in {copy}", named) and (copy / "PIN").read_bytes() == earlier,
              f"exit {c}, {(o + e).strip()[-260:]!r}")
        c, o, e = program(src / "shoalmark.py", "--vendor", str(copy), cwd=root)
        now = (copy / "PIN").read_text(encoding="utf-8") if (copy / "PIN").is_file() else ""
        c2, o2, e2 = mine("--check")
        check(f"…and --vendor from a release names it once more and replaces it: the PIN tagged and complete, the files it lacked back, --check warning of nothing ({name})",
              c == 0 and said_for(o.splitlines(), f"note: the copy in {copy}", named) and now.startswith(f"# shoalmark {ver} · tag v{ver} · commit {tagged} · vendored {today} · complete\n")
              and all((copy / rel).is_file() for rel in gone) and c2 == 0 and "warning" not in o2 and "R17" not in o2 + e2,
              f"exit {c}, {(o + e).strip()[-200:]!r} · --check {c2}, {(o2 + e2).strip()[-120:]!r}")
        body = [l for l in now.splitlines() if not l.startswith("#")] or body


def tag_steps(check, fm, tool_bytes, base):
    """From a Git source the copy holds the tag's own bytes (RV-3364: recorded privately): each case in its own release, in `base`."""
    lint = fm.EXIT_LINT
    crlf = lambda data: data if b"\0" in data else data.replace(b"\r\n", b"\n").replace(b"\n", b"\r\n")

    def vend(src, name):
        p = base / name
        p.mkdir()
        git(p, "init", "-q")
        copy = p / "tools" / "shoalmark"
        c, o, e = program(src / "shoalmark.py", "--vendor", str(copy), cwd=p)
        pin = (copy / "PIN").read_text(encoding="utf-8") if (copy / "PIN").is_file() else ""
        return copy, c, o, e, [l for l in pin.splitlines() if not l.startswith("#")]

    def from_tag(src, copy, body):
        """Whether the copy holds exactly the tag's files, each byte for byte its blob, each pinned by its hash."""
        kept = lambda rel: rel in fm.TOOL_FILES or rel in {f"brand/{n}" for n in fm.BRAND_FILES} or (
            rel.startswith("brand/themes/") and not any(s.startswith(".") for s in rel[len("brand/themes/"):].split("/")))
        held = {rel: show(src, rel) for rel in git(src, "ls-tree", "-r", "--name-only", "HEAD").splitlines() if kept(rel)}
        pins = {hashlib.sha256(data.replace(b"\r\n", b"\n")).hexdigest() + "  " + rel for rel, data in held.items()}
        return bool(held) and set(body) == pins and all((copy / rel).read_bytes() == data for rel, data in held.items())

    # the clean control: an untouched release at its tag
    clean = base / "clean"
    release(clean, fm, tool_bytes)
    copy, c, o, e, body = vend(clean, "from-clean")
    check(CLEAN + " an untouched source at its release tag vendors as before — each file byte for byte the tag's, each pinned by its hash, nothing named",
          c == 0 and e == "" and from_tag(clean, copy, body), f"exit {c}, {(o + e).strip()[-200:]!r}")

    # a checkout whose line ends git converted: LF in the tag, CRLF on disk, `git status` clean
    lf = base / "crlf-checkout"
    release(lf, fm, tool_bytes, shape=lambda data: data if b"\0" in data else data.replace(b"\r\n", b"\n"))
    git(lf, "config", "core.autocrlf", "true")
    texts = [rel for rel in fm.vendor_files() if b"\0" not in (lf / rel).read_bytes()]
    for rel in texts:
        (lf / rel).unlink()
    git(lf, "-c", "core.autocrlf=true", "checkout", "--", ".")
    converted = all((lf / rel).read_bytes() == crlf(show(lf, rel)) for rel in texts) and b"\r\n" in (lf / "shoalmark.py").read_bytes()
    status = git(lf, "-c", "core.autocrlf=true", "status", "--porcelain", "--untracked-files=all")
    copy, c, o, e, body = vend(lf, "from-crlf-checkout")
    check("a checkout whose line ends git converted to CRLF, `git status` clean, vendors the tag's own bytes — LF as the tag holds them — each pinned by its hash",
          converted and status == "" and c == 0 and e == "" and from_tag(lf, copy, body), f"converted {converted}, status {status!r}, exit {c}, {(o + e).strip()[-200:]!r}")

    # a file beside the tool that the tag does not hold: an ignored brand file
    ign = base / "ignored"
    release(ign, fm, tool_bytes)
    (ign / ".git" / "info").mkdir(exist_ok=True)
    with open(ign / ".git" / "info" / "exclude", "a", encoding="utf-8") as f:
        f.write("/brand/theme.css\n")
    (ign / "brand" / "theme.css").write_bytes(b":root{--ink:#010203}\n")
    status = git(ign, "status", "--porcelain", "--untracked-files=all")
    copy, c, o, e, body = vend(ign, "from-ignored")
    check("a file beside the tool that the tag does not hold — an ignored brand/theme.css — is named in one line and never copied or pinned; the tag's files are",
          status == "" and c == 0 and one_line(e) and e.startswith("--vendor: not copied — brand/theme.css beside the tool, which the tag does not hold")
          and not (copy / "brand" / "theme.css").exists() and not any(l.endswith("  brand/theme.css") for l in body) and from_tag(ign, copy, body),
          f"status {status!r}, exit {c}, {(o + e).strip()[-200:]!r}")

    # a tracked file changed on disk while `git status` reports the tree clean
    for flag, rel in (("--assume-unchanged", "README.md"), ("--skip-worktree", "NOTICE")):
        hid = base / ("hidden" + flag)
        release(hid, fm, tool_bytes)
        git(hid, "update-index", flag, rel)
        (hid / rel).write_bytes((hid / rel).read_bytes() + b"\nchanged on disk\n")
        status = git(hid, "status", "--porcelain", "--untracked-files=all")
        dest = base / ("from-hidden" + flag) / "tools" / "shoalmark"
        c, o, e = program(hid / "shoalmark.py", "--vendor", str(dest), cwd=base)
        check(f"a tracked file changed on disk behind `git update-index {flag}`, `git status` clean, is refused in one line naming it, exit 4, nothing written",
              status == "" and c == lint and o == "" and one_line(e) and f"on disk, {rel} is not the tag's own bytes" in e and not dest.parent.parent.exists(),
              f"status {status!r}, exit {c}, {(o + e).strip()[-200:]!r}")

    # git's own checkout leaves these blobs as the tag holds them (RV-3366: recorded privately): a mixed-end file, a NUL-bearing binary, a lone CR
    kinds = {"brand/themes/samples/mixed.txt": b"one\r\ntwo\nthree\n", "brand/themes/samples/binary.bin": b"\0bin\nary\n",
             "brand/themes/samples/lonecr.txt": b"one\rtwo\nthree\n"}
    wide = lambda data: re.sub(rb"(?<!\r)\n", b"\r\n", data)
    real = base / "kinds-checkout"
    release(real, fm, tool_bytes, extra=kinds)
    git(real, "config", "core.autocrlf", "true")
    for rel in kinds:
        (real / rel).unlink()
    git(real, "-c", "core.autocrlf=true", "checkout", "--", ".")
    written = {rel: (real / rel).read_bytes() for rel in kinds}
    status = git(real, "-c", "core.autocrlf=true", "status", "--porcelain", "--untracked-files=all")
    copy, c, o, e, body = vend(real, "from-kinds-checkout")
    check("git's own checkout (core.autocrlf) of a mixed-end file, a NUL-bearing binary and a lone-CR file, each left as the tag holds it, vendors the "
          "tag's own bytes, each pinned by its hash",
          status == "" and all(written[rel] == data != wide(data) for rel, data in kinds.items()) and c == 0 and e == "" and from_tag(real, copy, body),
          f"status {status!r}, git wrote {[written[rel] == data for rel, data in kinds.items()]}, exit {c}, {(o + e).strip()[-200:]!r}")
    for rel, data in kinds.items():
        alt = base / ("wide-" + rel.rsplit("/", 1)[1])
        release(alt, fm, tool_bytes, extra=kinds)
        git(alt, "update-index", "--assume-unchanged", rel)
        (alt / rel).write_bytes(wide(data))
        status = git(alt, "status", "--porcelain", "--untracked-files=all")
        dest = base / ("from-wide-" + rel.rsplit("/", 1)[1]) / "tools" / "shoalmark"
        c, o, e = program(alt / "shoalmark.py", "--vendor", str(dest), cwd=base)
        check(f"{rel} with every lone LF made CRLF on disk, which is not git's checkout of it, behind `git update-index --assume-unchanged` is refused "
              "in one line naming it, exit 4, nothing written",
              status == "" and written[rel] != wide(data) and c == lint and one_line(e) and f"on disk, {rel} is not the tag's own bytes" in e
              and not dest.parent.parent.exists(), f"status {status!r}, exit {c}, {(o + e).strip()[-200:]!r}")

    # a committed attribute converts the tag's own file on checkout (RV-3376: recorded privately): `text eol=crlf` on the mixed-end blob 41 0d0a 42 0a,
    # which git writes as 41 0d0a 42 0d0a — refused, its one line naming the release's unpacked archive; once as `git status` sees it, once behind
    # `git update-index --assume-unchanged`
    mixed = "brand/themes/samples/attributed.txt"
    for quiet in (False, True):
        att = base / ("attributed" + ("-quiet" if quiet else ""))
        release(att, fm, tool_bytes, extra={".gitattributes": f"{mixed} text eol=crlf\n".encode("ascii")}, raw={mixed: b"A\r\nB\n"})
        (att / mixed).unlink()
        git(att, "checkout", "--", mixed)
        if quiet:
            git(att, "update-index", "--assume-unchanged", mixed)
        seen = (show(att, mixed) == b"A\r\nB\n", (att / mixed).read_bytes() == b"A\r\nB\r\n",
                (git(att, "status", "--porcelain", "--untracked-files=all") == "") == quiet)
        dest = base / ("from-attributed" + ("-quiet" if quiet else "")) / "tools" / "shoalmark"
        c, o, e = program(att / "shoalmark.py", "--vendor", str(dest), cwd=base)
        check("a committed `text eol=crlf` attribute on a mixed-end file, which git checks out converted"
              + (", behind `git update-index --assume-unchanged`" if quiet else ", `git status` naming it")
              + ", is refused in one line naming the release's unpacked archive, exit 4, nothing written",
              all(seen) and c == lint and o == "" and one_line(e) and "or vendor from that release's unpacked archive" in e and not dest.parent.parent.exists(),
              f"preconditions {seen}, exit {c}, {(o + e).strip()[-220:]!r}")

    # a replacement object (RV-3365: recorded privately): HEAD and the tag are the originals, `git status` is clean, and the disk and the index hold
    # another README.md, which a replacement commit, or a replacement of the tag's tree, carries
    global_config = base / "global.gitconfig"              # a private global configuration, never the real one
    global_config.write_text("[core]\n\tuseReplaceRefs = true\n", encoding="utf-8")
    for kind, where in [(k, w) for k in ("commit", "tree") for w in ("", "source", "global")]:
        rep = base / ("replaced-" + kind + "-" + (where or "plain"))
        tagged = release(rep, fm, tool_bytes)
        if where == "source":
            git(rep, "config", "core.useReplaceRefs", "true")
        original = show(rep, "README.md")
        (rep / "README.md").write_bytes(original + b"\nanother README\n")
        git(rep, "add", "README.md")
        tree = git(rep, "write-tree")
        if kind == "commit":
            git(rep, "replace", tagged, git(rep, "commit-tree", tree, "-m", "the replacement"))
        else:
            git(rep, "replace", git(rep, "rev-parse", tagged + "^{tree}"), tree)
        git(rep, "reset", "-q", "--hard")
        seen = (git(rep, "rev-parse", "HEAD") == tagged, f"v{fm.__version__}" in git(rep, "tag", "--points-at", "HEAD").split(),
                git(rep, "status", "--porcelain", "--untracked-files=all") == "", (rep / "README.md").read_bytes() != original)
        dest = base / ("from-replaced-" + kind + "-" + (where or "plain")) / "tools" / "shoalmark"
        c, o, e = program(rep / "shoalmark.py", "--vendor", str(dest), cwd=base, env={"GIT_CONFIG_GLOBAL": str(global_config)} if where == "global" else None)
        copied = (dest / "README.md").read_bytes() if (dest / "README.md").is_file() else None
        said = {"": "", "source": ", core.useReplaceRefs true in the source's configuration",
                "global": ", core.useReplaceRefs true in a private global configuration (GIT_CONFIG_GLOBAL)"}[where]
        check(f"a replacement {kind}{said} — HEAD and the tag the originals, `git status` clean, another README.md on disk — vendors only the tag's own "
              "bytes or is refused before anything is written",
              all(seen) and ((c == lint and one_line(e) and not dest.parent.parent.exists()) or (c == 0 and copied == original)),
              f"preconditions {seen}, exit {c}, README the tag's: {copied == original}, {(o + e).strip()[-200:]!r}")


def env_steps(check, tool):
    """The environment an actual source read of the tool at `tool` starts with (RV-3369: recorded privately): read in process, at `subprocess.run`, with
    a parameter in `GIT_CONFIG_PARAMETERS` that turns replacement on."""
    inherited, seen, saved = "'core.useReplaceRefs=true'", [], os.environ.get("GIT_CONFIG_PARAMETERS")
    os.environ["GIT_CONFIG_PARAMETERS"] = inherited
    try:
        module = load(tool)
        real = module.subprocess.run

        def watch(argv, **options):
            seen.append(options.get("env") or {})
            return real(argv, **options)
        module.subprocess.run = watch
        try:
            module.git_out("rev-parse", "HEAD", cwd=module.HERE, source=True)
        finally:
            module.subprocess.run = real
        env = seen[-1] if seen else {}
        params = env.get("GIT_CONFIG_PARAMETERS", "")
        check("an actual source read starts with the inherited parameters as they were, then core.useReplaceRefs=false as the last parameter, "
              "GIT_NO_REPLACE_OBJECTS=1 and GIT_GRAFT_FILE the null device",
              len(seen) == 1 and params.startswith(inherited) and params[len(inherited):].strip() == "'core.useReplaceRefs=false'"
              and env.get("GIT_NO_REPLACE_OBJECTS") == "1" and env.get("GIT_GRAFT_FILE") == os.devnull,
              f"{len(seen)} start(s), GIT_CONFIG_PARAMETERS {params!r}, {env.get('GIT_NO_REPLACE_OBJECTS')!r}, {env.get('GIT_GRAFT_FILE')!r}")
    except Exception as error:                               # a tool that cannot be read this way fails the control by name
        check("an actual source read starts with the inherited parameters as they were, then core.useReplaceRefs=false as the last parameter, "
              "GIT_NO_REPLACE_OBJECTS=1 and GIT_GRAFT_FILE the null device", False, f"{type(error).__name__}: {error}")
    finally:
        if saved is None:
            os.environ.pop("GIT_CONFIG_PARAMETERS", None)
        else:
            os.environ["GIT_CONFIG_PARAMETERS"] = saved


def mutants(fm):
    """Each mutant of `fm`'s file, and the tool before R17 where this clone holds it, as each is run: (name, the labels it fails, or None where it cannot
    run, and for a mutant of the tag's bytes the case it is paired with)."""
    source = pathlib.Path(fm.__file__).read_bytes()
    with tempfile.TemporaryDirectory() as d:
        for n, (name, old, new, paired) in enumerate([m + (None,) for m in MUTANTS] + list(TAG_MUTANTS)):
            if source.count(old.encode("utf-8")) != 1:
                yield name, None, paired                    # the line it changes is not in the tool once: named, never a silent pass
                continue
            path = pathlib.Path(d) / f"mutant-{n}.py"
            path.write_bytes(source.replace(old.encode("utf-8"), new.encode("utf-8")))
            yield name, [label for label, ok, _ in run_checks(fm, path) if not ok], paired
        before = subprocess.run(["git", "-C", str(HERE), "show", f"{BEFORE_R17}:shoalmark.py"], capture_output=True, env=ENV)
        name = f"the tool before R17, main at {BEFORE_R17}"
        if before.returncode:
            yield name, None, None
        else:
            path = pathlib.Path(d) / "before-r17.py"
            path.write_bytes(before.stdout)
            yield name, [label for label, ok, _ in run_checks(fm, path) if not ok], None


if __name__ == "__main__":
    tools = [a for a in sys.argv[1:] if a != "--mutants"]
    fm = load(HERE / "shoalmark.py")
    results = run_checks(fm, tools[0] if tools else None)
    for label, ok, saw in results:
        print(("  ok    " if ok else "  FAIL  ") + label + ("" if ok else f" (saw {saw})"))
    failed = sum(not ok for _, ok, _ in results)
    print(f"{len(results) - failed} passed; {failed} failed")
    survived = 0
    if "--mutants" in sys.argv[1:]:
        for name, labels, paired in mutants(fm):
            held = labels is not None and (paired is None or (any(paired in l for l in labels) and not any(CLEAN in l for l in labels)))
            if labels is None:
                print(f"  FAIL  mutant: {name} — it cannot run here")
            elif labels and held:
                print(f"  ok    mutant: {name} — killed: {len(labels)} check(s) fail it"
                      + (f"; its paired case fails and the clean control passes" if paired else ""))
                for label in labels:
                    print(f"          fails: {label}")
            elif labels:
                print(f"  FAIL  mutant: {name} — killed, but not as paired: its case ({paired}) passes, or the clean control fails")
                for label in labels:
                    print(f"          fails: {label}")
            else:
                print(f"  FAIL  mutant: {name} — SURVIVED: every check passes it")
            survived += not (labels and held)
        print(f"mutants: {len(MUTANTS) + len(TAG_MUTANTS) + 1 - survived} killed as required; {survived} not")
    sys.exit(1 if failed or survived else 0)
