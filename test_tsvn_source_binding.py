"""Actual local Tortoise source/consumer binding controls; no authority substitute.

The optional development baseline must be supplied explicitly. The permanent
runner needs current payloads, real SVN, and the additive observer fields proposed
in entry-observer.patch. It fetches no historical source.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import sys
import tempfile
import time

import test_vcs_entry as entry

HERE = Path(__file__).resolve().parent


def refusal_reads_confined(observed):
    root, tool, cwd = (Path(observed[key]) for key in ("root", "tool", "invocation_cwd"))
    runtime = Path(os.__file__).parent
    allowed = {str(tool), str(tool.parent / "VERSION"), str(root / "shoalmark.toml"),
               str(tool.parent / "shoalmark.toml"), str(tool.parent.parent / "shoalmark.toml"),
               str(cwd / "shoalmark.toml")}
    return all(event["path"] in allowed or event["path"].startswith(str(runtime) + os.sep)
               for event in observed["events"] if event["event"] == "open" and not event.get("write"))


def run_source_binding_controls(source, check, baseline=None, payload=None, report_path=None):
    source = Path(getattr(source, "__file__", source)).resolve()
    baseline = Path(baseline).resolve() if baseline is not None else None
    payload = Path(payload).resolve() if payload is not None else source.parent
    if not all(shutil.which(name) for name in ("git", "svn", "svnadmin")):
        raise RuntimeError("real Git/SVN fixture setup is required")
    started = time.monotonic(); observations = []; before_checks = []
    with tempfile.TemporaryDirectory(prefix="fm044-source-binding-") as temp:
        base = Path(temp).resolve(); launch = base / "unrelated"; launch.mkdir()
        search = entry.svn_search(base / "svn-only", shutil.which("svn"))
        server = base / "server"; seed = base / "seed"
        entry.command(base, "svnadmin", "create", str(server))
        entry.command(base, "svn", "checkout", "-q", server.as_uri(), str(seed))
        entry.corpus(seed)
        entry.command(seed, "svn", "add", "-q", "shoalmark.toml", "work-tracker", "documents")
        entry.command(seed, "svn", "commit", "-qm", "untrusted local fixture data", "--username", "fixture-only")
        message = base / "message.txt"; message.write_text("Keep this message exactly. ü\n", encoding="utf-8")
        original_message = message.read_bytes()
        cases = [
            ("healthy-start3", "start", False, False, False, None, False),
            ("healthy-pre4", "pre", True, False, False, None, False),
            ("healthy-legacy-start4", "start", True, False, False, None, False),
            ("healthy-subdirectory", "start", False, True, False, None, False),
            ("healthy-explicit-root", "start", False, False, True, None, False),
            ("healthy-explicit-subdirectory", "pre", True, True, True, None, False),
            ("conflict-source-start3", "start", False, False, False, "source", False),
            ("conflict-source-pre4", "pre", True, False, False, "source", False),
            ("conflict-source-legacy4", "start", True, False, False, "source", False),
            ("conflict-source-explicit-root", "start", False, False, True, "source", False),
            ("conflict-source-launch-directory", "start", False, False, False, "source", True),
            ("conflict-source-ancestor", "start", False, False, False, "ancestor", False),
            ("ambiguous-duplicate-configuration", "start", False, False, False, "duplicate", False),
        ]
        for number, (name, kind, depth, subdir, explicit, conflict, source_launch) in enumerate(cases):
            root = base / ("wc-%02d" % number)
            entry.command(base, "svn", "checkout", "-q", server.as_uri(), str(root))
            tool = entry.tool_copy(root, source, payload)
            affected = root / "documents" if subdir else root
            paths = base / ("paths-%02d.txt" % number)
            paths.write_text(str(root / "documents" / "O'Neil & ü.txt") + "\n", encoding="utf-8")
            original_paths = paths.read_bytes()
            flags = ["--tsvn-hook", kind, str(paths)] + (["3"] if depth else []) + [str(message), str(affected)]
            if explicit:
                flags = ["--root", str(affected), *flags]
            # PRE runs only after a real generation, while the source binding is healthy.
            # Available file:// history is explicit: no offline history acceptance is claimed.
            if kind == "pre":
                setup = entry.invoke(tool, root, ["--tsvn-hook", "start", str(paths), str(message), str(affected)], launch, search)
                assert setup["code"] == 0 and setup["notice_count"] == 0
            conflict_path = (tool.parent.parent if conflict == "ancestor" else tool.parent) / "shoalmark.toml"
            if conflict:
                conflict_path.write_bytes((root / "shoalmark.toml").read_bytes() if conflict == "duplicate" else
                    b'name = "source fixture"\ntracker_dir = "inner-records"\n[kinds]\nINNER = "Inner"\n')
            results = []
            for chosen in ((baseline, source) if baseline is not None else (source,)):
                # Reset only generated fixture output to identical pre-run consumer bytes.
                # The measured invocation never gets substituted handler/process results.
                if kind != "pre":
                    for path in (root / "work-tracker" / "INDEX.md", root / "work-tracker" / "index.html", root / "work-tracker" / "view"):
                        if path.exists():
                            shutil.rmtree(path) if path.is_dir() else path.unlink()
                tool = entry.tool_copy(root, chosen, payload)
                configs_before = {(root / "shoalmark.toml"): (root / "shoalmark.toml").read_bytes()}
                if conflict:
                    configs_before[conflict_path] = conflict_path.read_bytes()
                cwd = tool.parent if source_launch else launch
                got = entry.invoke(tool, root, flags, cwd, search)
                got.update(case=name, variant="immutable-before" if baseline is not None and chosen == baseline else "candidate",
                           conflict=bool(conflict), available_file_history=True,
                           configurations_unchanged=all(path.read_bytes() == data for path, data in configs_before.items()),
                           paths_message_unchanged=paths.read_bytes() == original_paths and message.read_bytes() == original_message)
                observations.append(got); results.append(got)
            current = results[-1]
            processes = [event for event in current["events"] if event["event"] == "subprocess.Popen"]
            writes = [event for event in current["events"] if event.get("write")]
            check("source binding: " + name + " has no verification notice", current["notice_count"] == 0)
            check("source binding: " + name + " preserves both configuration bytes and appended inputs", current["configurations_unchanged"] and current["paths_message_unchanged"])
            check("source binding: " + name + " never reads the message", not any(event.get("path") == str(message) for event in current["events"]))
            check("source binding: " + name + " uses SVN-only PATH and no alternate network/process API", current["git_absent"] and all(event["argv"][0] == "svn" for event in processes) and not any(event.get("alternate_process_or_network") for event in current["events"]))
            if conflict:
                refused = current["code"] == 4 and current["exception"] is None and current["normalized"] == [None]
                check("source binding: " + name + " refuses before preflight/process/handlers/writes", refused and not current["preflight_calls"] and not current["phases"] and not processes and not writes and not current["changed"])
                protected = [paths, message, root / "work-tracker", root / "proof", root / "evidence"]
                def protected_read(event):
                    value = event.get("path", "")
                    return event["event"] == "open" and any(value == str(path) or value.startswith(str(path) + os.sep) for path in protected)
                check("source binding: " + name + " reads no path-list/tracker/proof/message bytes", not any(protected_read(event) for event in current["events"]))
                check("source binding: " + name + " reads only startup/runtime and binding configuration", refusal_reads_confined(current))
                check("source binding: " + name + " actually inspects source-nearest configuration metadata", str(tool.parent) in current["binding_metadata"])
                if baseline is not None:
                    before = results[0]
                    before_pass = before["code"] == 4 and before["normalized"] == [None] and not before["preflight_calls"] and not before["phases"] and not before["changed"] and not any(e["event"] == "subprocess.Popen" or e.get("write") for e in before["events"])
                    before_checks.append({"case": name, "same_refusal_control_pass": bool(before_pass), "actual_code": before["code"], "actual_changed": before["changed"]})
                    check("source binding: " + name + " immutable-before really reaches the consumer", not before_pass and before["code"] == 0 and before["normalized"] == [["--root", str(root)] + (["--check"] if kind == "pre" else [])] and bool(before["phases"]) and (kind == "pre" or "work-tracker/index.html" in before["changed"]))
            else:
                expected = ["--root", str(root)] + (["--check"] if kind == "pre" else [])
                check("source binding: " + name + " keeps real normalized consumer and deliberate success", current["code"] == 0 and current["exception"] is None and current["normalized"] == [expected] and current["bindings"][-1]["root"] == str(root) and bool(current["preflight_calls"]))
                check("source binding: " + name + " confines local processes and consumer output", all(e["cwd"] == str(root) or (e["argv"][:4] == ["svn", "log", "-v", "--xml"] and e["cwd"] == str(cwd)) for e in processes) and (not current["changed"] if kind == "pre" else "work-tracker/index.html" in current["changed"]) and not any(p.startswith("tools/") for p in current["changed"]))
                if baseline is not None:
                    prior = results[0]
                    check("source binding: " + name + " matches real immutable-before output/result", (prior["code"], prior["out"], prior["err"]) == (current["code"], current["out"], current["err"]))
    proof = {"kind": "outside source-binding actual controls; no authority/verdict", "source_sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
             "development_baseline": str(baseline) if baseline is not None else None,
             "seconds": time.monotonic() - started, "observations": observations, "immutable_before_controls": before_checks}
    if report_path:
        Path(report_path).write_text(json.dumps(proof, indent=2) + "\n", encoding="utf-8")
    return proof


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, default=HERE / "shoalmark.py")
    parser.add_argument("--baseline", type=Path)
    parser.add_argument("--payload", type=Path)
    parser.add_argument("--report", type=Path)
    args = parser.parse_args(); rows = []
    def check(name, passed):
        rows.append({"name": name, "pass": bool(passed)}); print(("ok   " if passed else "FAIL ") + name, flush=True)
    proof = run_source_binding_controls(args.source, check, baseline=args.baseline, payload=args.payload)
    proof["checks"] = rows
    if args.report:
        args.report.write_text(json.dumps(proof, indent=2) + "\n", encoding="utf-8")
    print("%d/%d source-binding controls passed in %.3fs" % (sum(row["pass"] for row in rows), len(rows), proof["seconds"]))
    raise SystemExit(not all(row["pass"] for row in rows))
