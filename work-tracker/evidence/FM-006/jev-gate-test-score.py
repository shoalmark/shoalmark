"""Score the Jev gate test — the decision rule, committed before either call was run.

    python3 jev-gate-test-score.py RUN1.json [RUN2.json]

Per answer, p_pass is the probability that the line PASSES that gate: a two-level Score's probability of level 1,
or 1 - noul for G2 (the Noul asks the failing condition). A gate passes when p_pass >= 0.5. G0 also fails when the
line has more than 12 words, counted in code (the keys file carries the count). A line's first fatal gate is the
first of G0..G5 that does not pass; a line that fails none survives.

The rule, fixed before the call:
  - controls: E0 (the Owner's English line, in its own slot) passes every gate; H1 (German, "Owner") dies at G0;
    H2 (German, "Eigner") passes every gate — in BOTH runs;
  - repeat: every one of the 102 p_pass values differs between the runs by at most 0.10;
  - the column counts only if both hold. Otherwise it is noise, and the record blames:
      the MODEL    when the repeat fails — the same question gave different numbers (and an unstable answer
                   cannot indict the question, so this wins when both fail);
      the QUESTION when the repeat holds and a control fails — the model answers it the same way twice, and that
                   stable answer misses the control; the control and the gate it fell at are named.
"""
import json
import pathlib
import sys

HERE = pathlib.Path(__file__).parent
KEYS = json.loads((HERE / "jev-gate-test-keys-2026-09-23.json").read_text(encoding="utf-8"))
GATES = ["G0", "G1", "G2", "G3", "G4", "G5"]
LEDGER = {"C1": "G1", "C2": "G1", "C3": "G2", "C4": "G2", "C5": "G3", "C6": "G3", "C7": "G4", "C8": "G0",
          "C9": "G5", "C10": "survives", "C11": "survives", "C12": "survives",
          "E0": "survives", "H1": "G0", "H2": "survives", "H3": "G0", "H4": "G5"}
CONTROLS = {"E0": "survives", "H1": "G0", "H2": "survives"}
ORDER = list(LEDGER)
REPEAT_TOLERANCE = 0.10


def p_pass(answer):
    if answer["type"] == "noul":
        return 1 - answer["noul"]
    return answer["probabilities"]["1"]


def read(path):
    run = json.loads(pathlib.Path(path).read_text(encoding="utf-8"))
    assert set(run["answers"]) == set(KEYS["keys"]), "the answer's keys are not the request's"
    grid = {}                                                   # (line, gate) -> (p_pass, confidence or None)
    for k, a in run["answers"].items():
        who = KEYS["keys"][k]
        grid[(who["line"], who["gate"])] = (p_pass(a), a.get("confidence"))
    return run, grid


def first_fatal(grid, line):
    for g in GATES:
        passed = grid[(line, g)][0] >= 0.5 and not (g == "G0" and KEYS["words"][line] > 12)
        if not passed:
            return g
    return "survives"


def report(grid, name):
    print(f"\n{name}: line · first fatal gate · ledger · p_pass per gate G0..G5 (confidence of the Scores)")
    for line in ORDER:
        ff = first_fatal(grid, line)
        cells = " ".join(f"{grid[(line, g)][0]:.2f}" + (f"({grid[(line, g)][1]:.2f})" if grid[(line, g)][1] is not None else "(n)")
                         for g in GATES)
        print(f"  {line:4} {ff:9} ledger {LEDGER[line]:9} {'agree' if ff == LEDGER[line] else '     '}  {cells}")
    return {line: first_fatal(grid, line) for line in ORDER}


def main(paths):
    runs = [read(p) for p in paths]
    fates = [report(grid, f"run {i + 1} ({run['model']}, {run.get('request_id', '?')})") for i, (run, grid) in enumerate(runs)]
    failed = [(i + 1, c, fates[i][c]) for i in range(len(runs)) for c, want in CONTROLS.items() if fates[i][c] != want]
    print("\ncontrols:", "all hold" if not failed else "; ".join(f"run {r}: {c} came back {got}, wanted {CONTROLS[c]}" for r, c, got in failed))
    for i in range(len(runs)):
        print(f"  run {i + 1}: agrees with the ledger on {sum(fates[i][l] == LEDGER[l] for l in ORDER)} of {len(ORDER)} lines")
    if len(runs) < 2:
        print("repeat: not run — the column cannot count on one run")
        return
    (_, g1), (_, g2) = runs
    diffs = sorted(((abs(g1[k][0] - g2[k][0]), k) for k in g1), reverse=True)
    worst = diffs[0]
    repeat_ok = worst[0] <= REPEAT_TOLERANCE + 1e-9
    same_fate = sum(fates[0][l] == fates[1][l] for l in ORDER)
    print(f"repeat: max |p_pass run1 - run2| = {worst[0]:.3f} at {worst[1][0]} {worst[1][1]}; "
          f"{sum(d <= REPEAT_TOLERANCE + 1e-9 for d, _ in diffs)} of {len(diffs)} within {REPEAT_TOLERANCE}; "
          f"first fatal gate identical on {same_fate} of {len(ORDER)} lines -> {'holds' if repeat_ok else 'FAILS'}")
    if not failed and repeat_ok:
        print("VERDICT: the column counts")
    elif not repeat_ok:
        print("VERDICT: noise — the record blames the MODEL: the identical question gave different numbers")
    else:
        print("VERDICT: noise — the record blames the QUESTION: the answers repeat, and the stable answer misses "
              + ", ".join(sorted({f"{c} (at {got})" for _, c, got in failed})))


if __name__ == "__main__":
    main(sys.argv[1:])
