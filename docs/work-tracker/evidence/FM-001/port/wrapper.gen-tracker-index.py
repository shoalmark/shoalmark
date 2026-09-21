#!/usr/bin/env python3
"""The tracker's command, where every page, hook and habit expects it. The tool itself is the vendored, pinned
shoalmark under tools/; the release axis is docs/work-tracker/derive. This wrapper owns one thing: a flag the
deriver can only take from the environment."""
import os, pathlib, subprocess, sys
root = pathlib.Path(__file__).resolve().parent.parent
args = sys.argv[1:]
if "--allow-missing-submodules" in args:
    args.remove("--allow-missing-submodules")
    os.environ["ALLOW_MISSING_SUBMODULES"] = "1"
os.environ["SHOALMARK_CMD"] = "python3 scripts/gen-tracker-index.py"
sys.exit(subprocess.call([sys.executable, str(root / "tools" / "shoalmark" / "shoalmark.py"), "--root", str(root), *args]))
