"""An answer with the changes the Owner names: an option of `ask-options:` that reads *with the changes I name* opens the board's box,
`--answer <id> accept "<the option>" "<the changes>"` writes both in the one signed line, `accepted - <the option>: <the changes>`, and
the relation reads the option chosen with its changes quoted.

Four groups of rows — the rule, the relation, the command and the dialog — and a mutant for each, which must turn a row of its group
red. The command's rows build their history in scratch repositories through test_ask_ids.py's fixture: a bare `origin`, the Owner's
SSH key, made here, in the default branch's signers file. The dialog's rows run the board's own script in Node, and each command it
builds through `sh`, and are skipped where either is missing.

Run: `python3 test_answer_changes.py` — exit 1 on a failure. test_shoalmark.py runs it as it runs test_ask_ids.py. No browser and no
network.
"""
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))
import shoalmark as fm  # noqa: E402
import test_ask_ids as ids  # noqa: E402

NAMING = "yes, with the changes I name"
OPTIONS = ["yes, as proposed", NAMING, "no"]
CHANGES = 'drop "the third" and $HOME `id`\n  then rename it'
WRITTEN = "drop 'the third' and $HOME `id` then rename it"          # as the line holds it: one line, `"` as `'`


# --- the rule ------------------------------------------------------------------------------------------------------------------

RULE = (
    (NAMING, True), ("Yes — WITH THE CHANGES I NAME.", True), ("with  the changes\n I name", True), ("with the changes I name", True),
    ('"yes, with the changes I name"', True), ("ship it (with the changes I name)", True), ("yes, with the changes I name, then ship", True),
    ("with the change I name", False), ("with changes I name", False), ("with the changes I named", False), ("with the changes I name_x", False),
    ("rewith the changes I name", False), ("yes, as proposed", False), ("", False), (None, False),
)


def rows_rule(area, add):
    for option, want in RULE:
        add(f"the rule · {option!r} {'names' if want else 'does not name'} changes", fm.names_changes(option) is want, f"saw {fm.names_changes(option)}")
    t = {"ask_proposal": "yes, as proposed", "ask_options": OPTIONS + ["no, with the changes I name"]}
    add("the rule · an ask's choices that name changes are its options that do, each with its place in `ask-options:`",
        fm.changes_options(t) == [(2, NAMING), (4, "no, with the changes I name")], f"saw {fm.changes_options(t)}")
    add("the rule · with no `ask-options:`, the proposal alone is the one choice, at place 0",
        fm.changes_options({"ask_proposal": "ship, with the changes I name"}) == [(0, "ship, with the changes I name")]
        and fm.changes_options({"ask_proposal": "ship"}) == [], f"saw {fm.changes_options({'ask_proposal': 'ship, with the changes I name'})}")


# --- the relation --------------------------------------------------------------------------------------------------------------

def reference(t):
    """The relation as it was read before an option could carry its changes — every answer that is no option that names changes
    followed by its changes reads as this still."""
    answer = fm.answer_norm(t.get("answer"))
    if not answer:
        return None
    m = fm.ANSWER_WORD_RE.fullmatch(answer)
    if not m:
        return ("unknown", 0, "")
    word, text = m.group(1).lower(), (m.group(2) or "").strip()
    if word != "accepted":
        return (word, 0, fm.first_words(text))
    proposal, options = fm.answer_norm(t.get("ask_proposal")), [fm.answer_norm(o) for o in t.get("ask_options") or []]
    if proposal and text in ("", proposal):
        return ("proposal", 0, "")
    if text and text in options:
        return ("option", options.index(text) + 1, fm.first_words(text))
    return ("changed", 0, "") if text and (proposal or options) else ("unknown", 0, "")


LONG = "drop the third option and rename the second one before the release"
# (what the row says, the answer, the proposal, the options, the relation as read, whether it reads as before)
RELATIONS = (
    ("bare, the proposal", "accepted", "yes, as proposed", OPTIONS, "accepted the proposal", True),
    ("the proposal's text", "accepted - yes, as proposed", "yes, as proposed", OPTIONS, "accepted the proposal", True),
    ("a plain option", "accepted - no", "yes, as proposed", OPTIONS, "chose option 3: no", True),
    ("the option that names changes, alone, as answers before this were written", f"accepted - {NAMING}", "yes, as proposed", OPTIONS,
     f"chose option 2: {NAMING}", True),
    ("the option and its changes", f"accepted - {NAMING}: drop the third", "yes, as proposed", OPTIONS,
     f'chose option 2: {NAMING} — "drop the third"', False),
    ("the option and its changes, spelled as a hand might — runs of spaces, double quotes, the em dash",
     'accepted —  yes,  with the changes I name:   drop  "it"', "yes, as proposed", OPTIONS, f'chose option 2: {NAMING} — "drop \'it\'"', False),
    ("long changes: their first words, cut between two", f"accepted - {NAMING}: {LONG}", "yes, as proposed", OPTIONS,
     f'chose option 2: {NAMING} — "{fm.first_words(LONG)}"', False),
    ("the option and a colon with nothing after it", f"accepted - {NAMING}:", "yes, as proposed", OPTIONS, "accepted with a change", True),
    ("a plain option, a colon and more: a change, as before", "accepted - no: because", "yes, as proposed", OPTIONS, "accepted with a change", True),
    ("free text", "accepted - something else", "yes, as proposed", OPTIONS, "accepted with a change", True),
    ("the proposal that names changes, with its changes", f"accepted - {NAMING}: x", NAMING, OPTIONS, f'accepted the proposal: {NAMING} — "x"', False),
    ("a proposal alone that names changes, with its changes", "accepted - ship, with the changes I name: x", "ship, with the changes I name", [],
     'accepted the proposal: ship, with the changes I name — "x"', False),
    ("an option that is itself another option and a colon: the option as written wins", "accepted - a, with the changes I name: none", "b",
     ["a, with the changes I name", "a, with the changes I name: none", "b"], "chose option 2: a, with the changes I name: none", True),
    ("two options that name changes, one the other's start: the longer wins", "accepted - x, with the changes I name: y, with the changes I name: z", "b",
     ["x, with the changes I name", "x, with the changes I name: y, with the changes I name", "b"],
     f'chose option 2: {fm.first_words("x, with the changes I name: y, with the changes I name")} — "z"', False),
    ("rejected", f"rejected - {NAMING}: no", "yes, as proposed", OPTIONS, f"rejected: {fm.first_words(NAMING + ': no')}", True),
    ("revoked", "revoked - asked again", "yes, as proposed", OPTIONS, "revoked: asked again", True),
    ("nothing to compare with", f"accepted - {NAMING}: x", "", [], "relation not computable", True),
)


def rows_relation(area, add):
    for label, answer, proposal, options, want, as_before in RELATIONS:
        t = {"answer": answer, "ask_proposal": proposal, "ask_options": list(options)}
        said = fm.relation_text(fm.answer_relation(t))
        add(f"the relation · {label}: {want}", said == want, f"saw {said!r}")
        if as_before:
            add(f"the relation · {label}: reads as it did before", fm.answer_relation(t) == reference(t), f"saw {fm.answer_relation(t)} for {reference(t)}")
    fm.configure(HERE)
    here = [t for t in fm.load_trackers() if t.get("answer")]
    text = lambda t: ((fm.ANSWER_WORD_RE.fullmatch(fm.answer_norm(t["answer"])) or [None, None, ""])[2] or "").strip()
    moved = [t["id"] for t in here if fm.answer_relation(t) != reference(t) and not fm.split_changes(t, text(t))]
    add(f"the relation · every answer this repository's trackers hold that carries no changes reads as it did before ({len(here)} read)",
        not moved, f"read otherwise: {moved}")


# --- the command ---------------------------------------------------------------------------------------------------------------

ASKS = {
    "FM-001": {}, "FM-002": {}, "FM-003": {"proposal": NAMING}, "FM-004": {}, "FM-005": {}, "FM-006": {}, "FM-007": {},
}


def asked_repo(area, name):
    """A repository whose `main` holds one put ask per tracker of ASKS — options OPTIONS, the proposal *yes, as proposed* unless named —
    and a branch `ans` cut from it."""
    r = ids.Repo(area / name, {tid: ids.text(tid) for tid in ASKS})
    for tid, kw in ASKS.items():
        r.write(tid, ids.text(tid, ids.ask(aid=f"{tid}-Q1", q=f"Ship {tid}?", options=" | ".join(OPTIONS), **dict({"proposal": "yes, as proposed"}, **kw))))
    r.commit("the asks, put")
    ids.git(r.root, "push", "-q", "origin", "main")
    r.switch("-c", "ans")
    return r


def state(r):
    return (r.head(), ids.git(r.root, "status", "--porcelain"), {tid: r.read(tid) for tid in ASKS})


def line(r, tid):
    return next((l for l in r.read(tid).split("\n") if l.startswith("answer:")), "")


def rows_command(area, add):
    r = asked_repo(area, "cmd")
    before = state(r)
    for args, what in (((NAMING,), "the option alone"), ((NAMING, ""), "the option and an empty text"), ((NAMING, "  \n "), "the option and blank text"),
                       (("yes,  with the changes\nI name",), "the option alone, its spaces otherwise")):
        said = r_ = ids.run(r.root, "--answer", "FM-002-Q1", "accept", *args)
        add(f"the command · {what}: refused, naming why, and nothing written",
            ids.refused(said, "names changes, and none are given", "Nothing was written", "accept", "<the changes>") and state(r) == before, ids.seen(r_))
    said = ids.run(r.root, "--answer", "FM-003-Q1", "accept")
    add("the command · a bare accept whose proposal names changes: refused, naming why, and nothing written",
        ids.refused(said, f"{NAMING!r} names changes, and none are given") and state(r) == before, ids.seen(said))
    said = ids.run(r.root, "--answer", "FM-001-Q1", "accept", NAMING, CHANGES)
    want, typed = f"accepted - {NAMING}: {WRITTEN}", f"accepted - {NAMING}: " + " ".join(CHANGES.split())      # the subject keeps `"` as typed, as every answer's
    log = [ids.git(r.root, "log", "-1", f"--format={f}").strip() for f in ("%s", "%(trailers:key=Answers,valueonly)", "%G?")]
    count = ids.git(r.root, "rev-list", "--count", f"{before[0]}..HEAD").strip()
    add("the command · the option and its changes: one signed commit, its line `accepted - <the option>: <the changes>`, its subject and trailer as any answer's",
        said[0] == 0 and count == "1" and line(r, "FM-001") == f'answer: "{want}"' and log == [f"FM-001-Q1: {fm.first_words(typed, 60)}", "FM-001-Q1", "G"]
        and f"FM-001-Q1 answered: {typed}" in said[1], ids.seen(said) + f" · {log} · {count} · {line(r, 'FM-001')}")
    fm.configure(r.root)
    t = next(x for x in fm.load_trackers() if x["id"] == "FM-001")
    fm.configure(HERE)
    add("the command · …and its relation reads the option chosen, with its changes quoted",
        fm.relation_text(fm.answer_relation(t)) == f'chose option 2: {NAMING} — "{fm.first_words(WRITTEN)}"', fm.relation_text(fm.answer_relation(t)))
    said = r.check()
    add("the command · …and the gate passes it", ids.accepted(said), ids.seen(said))
    for tid, args, want in (("FM-004", ("no",), "accepted - no"), ("FM-005", ("no", "for now"), "accepted - no for now"),
                            ("FM-006", ("something else, with the changes I name",), "accepted - something else, with the changes I name"),
                            ("FM-007", ("reject", NAMING, "x"), f"rejected - {NAMING} x")):
        verdict, rest = (args[0], args[1:]) if args[0] == "reject" else ("accept", args)
        said = ids.run(r.root, "--answer", f"{tid}-Q1", verdict, *rest)
        add(f"the command · {verdict} {' '.join(repr(a) for a in rest)}: written as before, `{want}`", said[0] == 0 and line(r, tid) == f'answer: "{want}"',
            ids.seen(said) + " · " + line(r, tid))


# --- the dialog ----------------------------------------------------------------------------------------------------------------

NODE = r"""
const fs = require("fs"), inp = JSON.parse(fs.readFileSync(0, "utf8")), s = inp.script;
const grab = (re, what) => { const m = s.match(re); if (!m) throw new Error("not in the board's script: " + what); return m[1]; };
const NAMED = JSON.parse(grab(/,NAMED=(\[[^\n]*?\]),T=\[/, "NAMED"));
const sq = eval(grab(/\nconst sq=([^\n]*);\n/, "sq"));
const boxOf = eval(grab(/\nconst boxOf=([^\n]*);\n/, "boxOf"));
const answerOf = eval(grab(/\nconst answerOf=([\s\S]*?\]\});\n/, "answerOf"));
process.stdout.write(JSON.stringify({named: NAMED, box: inp.box.map(o => boxOf(o)), made: inp.made.map(a => answerOf(...a))}));
"""
CASES = (   # (what, [cmd, id, kind, the option picked — null for Other —, the box's text], the arguments after the command, or None, the line it writes)
    ("the option that names changes, with text holding quotes, a dollar sign, a backtick and a newline", ["argv", "FM-001-Q1", "accept", NAMING, CHANGES],
     ["--answer", "FM-001-Q1", "accept", NAMING, WRITTEN], f"accepted - {NAMING}: {WRITTEN}"),
    ("the option that names changes, the box empty", ["argv", "FM-001-Q1", "accept", NAMING, ""], None, None),
    ("the option that names changes, the box blank", ["argv", "FM-001-Q1", "accept", NAMING, " \n\t "], None, None),
    ("a plain option — what the box holds is not read", ["argv", "FM-001-Q1", "accept", "no", "stray"], ["--answer", "FM-001-Q1", "accept", "no"], "accepted - no"),
    ("Other, with text holding quotes, a dollar sign, a backtick and a newline", ["argv", "FM-001-Q1", "accept", None, CHANGES],
     ["--answer", "FM-001-Q1", "accept", CHANGES.replace('"', "'")], "accepted - " + WRITTEN),
    ("a rejection, its reason holding a dollar sign and a quote", ["argv", "FM-001-Q1", "reject", None, "not now: $x isn't set"],
     ["--answer", "FM-001-Q1", "reject", "not now: $x isn't set"], "rejected - not now: $x isn't set"),
)


def board_page(area):
    """The board of a plain folder whose two asks offer OPTIONS and a lone proposal that names changes, as `run` writes it."""
    root = area / "board"
    root.mkdir(parents=True)
    (root / "shoalmark.toml").write_text('name = "changes"\n[kinds]\nFM = "Work"\n', encoding="utf-8")
    ids.write(root, "FM-001", ids.text("FM-001", ids.ask(aid="FM-001-Q1", proposal="yes, as proposed", options=" | ".join(OPTIONS))))
    ids.write(root, "FM-002", ids.text("FM-002", ids.ask(aid="FM-002-Q1", proposal="ship it, with the changes I name")))
    ids.run(root)
    return (root / ids.REL / "index.html").read_text(encoding="utf-8")


def dialog_run(script):
    r = subprocess.run([shutil.which("node"), "-e", NODE], input=json.dumps({"script": script, "box": [None, NAMING, "no"], "made": [c[1] for c in CASES]}),
                       capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=60)
    try:
        return json.loads(r.stdout)
    except ValueError:
        return {"error": r.stderr.strip()[-300:]}


def shell_args(command):
    """The arguments `sh` hands the command's first word, as it reads the command."""
    r = subprocess.run(["sh", "-c", 'argv() { for a in "$@"; do printf "%s\\0" "$a"; done; }\n' + command], capture_output=True, text=True, encoding="utf-8", timeout=30)
    return r.stdout.split("\0")[:-1] if r.returncode == 0 else f"exit {r.returncode}: {r.stderr.strip()}"


def rows_dialog(area, add, script=None):
    page = board_page(area) if script is None else None
    script = script if script is not None else page
    if not (shutil.which("node") and shutil.which("sh")):
        add("the dialog · Node and sh run the board's script and its commands", None, "Node or sh is not installed here")
        return
    o = dialog_run(script)
    if "error" in o:
        add("the dialog · the board's script ran in Node", False, o["error"])
        return
    if page is not None:
        add("the dialog · the page's NAMED list is the rule's choices, as the rows carry them: an option, and a proposal alone",
            o["named"] == sorted([NAMING, "ship it, with the changes I name"]), f"saw {o['named']}")
        add("the dialog · Other opens the box for the answer, an option that names changes for its changes, and a plain option opens none",
            o["box"] == ["answer.change.hint", "answer.changes.hint", ""], f"saw {o['box']}")
        add("the dialog · the radios open the box by that one answer, and OK with no command marks the box and stops",
            "r.onchange=()=>{const b=boxOf(pick());ta.disabled=!b;ta.required=!!b;" in page and "const made=answerOf(cmd,id,kind,pick(),ta.value);" in page
            and 'if(!made){ta.setCustomValidity(L["answer.changes.missing"]??"answer.changes.missing");ta.reportValidity();return}' in page)
    for (what, _a, want, said), made in zip(CASES, o["made"]):
        if want is None:
            add(f"the dialog · {what}: no command", made is None, f"saw {made}")
            continue
        got = shell_args(made[0]) if made else "no command"
        add(f"the dialog · {what}: the command's arguments survive the shell", got == want, f"saw {got!r} from {made}")
        add(f"the dialog · {what}: the line it says it writes", made is not None and made[1] == said, f"saw {made}")


# --- the mutants ---------------------------------------------------------------------------------------------------------------

MUTANTS = (
    ("the rule read as a substring", "names_changes", "return bool(NAMES_CHANGES_RE.search(answer_norm(option)))",
     'return "with the changes" in str(option or "").lower()', rows_rule),
    ("the split read with no rule: any option, a colon and more", "changes_options", "if o and names_changes(o)]", "if o]", rows_relation),
    ("the changes left out of the relation", "answer_relation", """said = f'{first_words(named[0])} — "{first_words(named[1])}"'""",
     "said = first_words(named[0])", rows_relation),
    ("the option let through alone", "answer_cmd", "    if alone:\n", "    if False:\n", rows_command),
)
PAGE_MUTANTS = (
    ("the dialog builds a command with the box empty", "return named&&!changes?null:[", "return ["),
    ("the dialog leaves the changes out", '${changes?" "+sq(changes):""}', ""),
)


def run_mutants(*, results=None):
    """Each mutant, as (label, whether it turned a row of its group red, what it saw)."""
    results = [] if results is None else results
    for label, name, old, new, rows in MUTANTS:
        reds, broke = [], ""
        try:
            with ids.mutated(name, old, new), tempfile.TemporaryDirectory(prefix="shoalmark-changes-m-") as tmp:
                rows(Path(tmp).resolve(), lambda l, ok, saw="": reds.append(l) if ok is False else None)
        except AssertionError as e:
            broke = str(e)
        except Exception as e:                                        # a mutant that crashes a row turned it red
            reds.append(f"a row crashed: {type(e).__name__}: {str(e)[:120]}")
        finally:
            fm.configure(HERE)
        results.append((f"mutant · {label}: at least one row turns red", bool(reds) and not broke, broke or "no row turned red"))
    if not (shutil.which("node") and shutil.which("sh")):
        results.append(("mutant · the dialog's mutants", None, "Node or sh is not installed here"))
        return results
    with tempfile.TemporaryDirectory(prefix="shoalmark-changes-p-") as tmp:
        page = board_page(Path(tmp).resolve())
    fm.configure(HERE)
    for label, old, new in PAGE_MUTANTS:
        reds = []
        if page.count(old) == 1:
            rows_dialog(None, lambda l, ok, saw="": reds.append(l) if ok is False else None, script=page.replace(old, new))
        results.append((f"mutant · {label}: at least one row turns red", page.count(old) == 1 and bool(reds),
                        "not in the page's script once" if page.count(old) != 1 else "no row turned red"))
    return results


ROWS = (rows_rule, rows_relation, rows_command, rows_dialog)


def run_checks(*, results=None, mutants=True):
    """Every row, then every mutant, as (label, ok, what it saw); ok None where a row is skipped."""
    results = [] if results is None else results
    add = lambda label, ok, saw="": results.append((label, ok if ok is None else bool(ok), "" if ok else saw))
    with tempfile.TemporaryDirectory(prefix="shoalmark-changes-") as tmp:
        area = Path(tmp).resolve()
        for n, rows in enumerate(ROWS):
            try:
                rows(area / f"r{n}", add)
            except Exception as e:
                add(f"{rows.__name__}: a fixture step failed — {type(e).__name__}: {str(e)[:300]}", False, getattr(e, "stderr", "") or "")
            finally:
                fm.configure(HERE)
    if mutants:
        run_mutants(results=results)
    return results


if __name__ == "__main__":
    failed = 0
    for label, ok, detail in run_checks(mutants="--no-mutants" not in sys.argv):
        print(("  skip  " if ok is None else "  ok    " if ok else "  FAIL  ") + label + ("" if ok else f"\n        {detail}" if detail else ""))
        failed += ok is False
    print(f"FAILED: {failed}" if failed else "all green")
    sys.exit(1 if failed else 0)
