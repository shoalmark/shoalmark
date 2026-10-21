import json
from pathlib import Path
import re
import sys


HERE = Path(__file__).resolve().parent
PUBLIC_ID = re.compile(r"\b(?:FM|RV|SP|HL|FEAT|BUG)-\d+\b")
HOME_PATH = re.compile(r"(?i)(?:/(?:Users|home)/|[a-z]:[/\\]+Users[/\\]+|~[/\\]|%USERPROFILE%|\$(?:HOME\b|\{HOME\}))")


def _front_matter(text):
    lines = text.splitlines()
    if not lines or lines[0] != "---" or "---" not in lines[1:]:
        raise ValueError("expected front matter between --- lines")
    fields = {}
    for line in lines[1:lines.index("---", 1)]:
        if not line.strip() or line.startswith("#"):
            continue
        match = re.fullmatch(r"([a-z][a-z0-9-]*):[ ]+(.+)", line)
        if not match:
            raise ValueError("front matter must use flat, single-line string fields")
        key, value = match.groups()
        if key in fields:
            raise ValueError("duplicate front-matter key: " + key)
        value = value.strip()
        if value.startswith('"'):
            value = json.loads(value)
        elif value.startswith("'"):
            if not re.fullmatch(r"'(?:[^']|'')*'", value):
                raise ValueError("invalid single-quoted string: " + key)
            value = value[1:-1].replace("''", "'")
        elif (not re.fullmatch(r"[A-Za-z][^\t\r\n]*", value)
              or re.search(r":(?:\s|$)|\s#", value)
              or value.lower() in {"true", "false", "yes", "no", "on", "off", "null"}):
            raise ValueError("use a quoted string for: " + key)
        if not isinstance(value, str):
            raise ValueError("expected a string for: " + key)
        fields[key] = value
    return fields


def run_checks(results=None):
    if results is None:
        results = []

    def check(label, ok, detail=""):
        results.append((label, bool(ok), detail))

    def read_json(relative):
        try:
            value = json.loads((HERE / relative).read_text(encoding="utf-8"))
            check(relative + " is a JSON object", isinstance(value, dict))
            return value if isinstance(value, dict) else {}
        except (OSError, ValueError) as error:
            check(relative + " is a JSON object", False, str(error))
            return {}

    plugin = read_json(".claude-plugin/plugin.json")
    marketplace = read_json(".claude-plugin/marketplace.json")
    check("plugin name is shoalmark", plugin.get("name") == "shoalmark")
    check("plugin has a description", isinstance(plugin.get("description"), str) and bool(plugin["description"].strip()))
    check("plugin carries the repository's license", plugin.get("license") == "Apache-2.0 OR MIT")
    check("plugin uses the root skills directory", "skills" not in plugin or plugin["skills"] in ("./skills/", ["./skills/"]))
    version = (HERE / "VERSION").read_text(encoding="utf-8").strip()
    check("plugin version is absent or matches VERSION", "version" not in plugin or plugin["version"] == version)
    check("marketplace name is shoalmark", marketplace.get("name") == "shoalmark")
    owner = marketplace.get("owner")
    check("marketplace has an owner name", isinstance(owner, dict) and isinstance(owner.get("name"), str) and bool(owner["name"].strip()))
    entries = marketplace.get("plugins")
    check("marketplace lists only shoalmark from ./", isinstance(entries, list) and len(entries) == 1
          and isinstance(entries[0], dict) and entries[0].get("name") == "shoalmark" and entries[0].get("source") == "./")

    skills = HERE / "skills"
    folders = sorted(path for path in skills.iterdir() if path.is_dir()) if skills.is_dir() else []
    check("skills directory contains skills", bool(folders))
    for folder in folders:
        path = folder / "SKILL.md"
        relative = path.relative_to(HERE).as_posix()
        check(relative + " exists", path.is_file())
        if not path.is_file():
            continue
        try:
            fields = _front_matter(path.read_text(encoding="utf-8"))
        except (OSError, ValueError) as error:
            check(relative + " front matter parses", False, str(error))
            continue
        check(relative + " front matter parses", True)
        check(relative + " name matches its folder", fields.get("name") == folder.name)
        description = fields.get("description", "")
        check(relative + " description has 1 to 1024 characters", 0 < len(description) <= 1024)

    for folder in (skills, HERE / ".claude-plugin"):
        for path in sorted(folder.rglob("*")):
            if not path.is_file():
                continue
            relative = path.relative_to(HERE).as_posix()
            text = path.read_bytes().decode("utf-8", errors="replace")
            check(relative + " has no tracker or review id", PUBLIC_ID.search(text) is None)
            check(relative + " has no home folder path", HOME_PATH.search(text) is None)
    return results


if __name__ == "__main__":
    for stream in (sys.stdout, sys.stderr):
        stream.reconfigure(encoding="utf-8", errors="replace")
    checks = run_checks()
    for label, ok, detail in checks:
        print(("  ok    " if ok else "  FAIL  ") + label)
        if not ok and detail:
            print("        " + detail)
    failures = sum(not ok for _, ok, _ in checks)
    print("\n" + ("FAILED: " + str(failures) if failures else "all green"))
    sys.exit(1 if failures else 0)
