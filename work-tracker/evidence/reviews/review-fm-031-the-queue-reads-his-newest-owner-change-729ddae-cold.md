Reviewed: 729ddaef6c851d88c96ad769968e032e0c951d20
Tier: critical under TRIAGE.md path line 3 — the queue's reader interprets the Owner's own acts.
Independence: cold — a session the Owner started, no part of session 8e509911.

# FM-031 — cold re-check of 729ddae

The RV-715 fix rejects the cold review's exact placement above `## Acts`, but its new structural comparison does not
bound the Acts section at the next Markdown heading. A tracker in this repository already has the decisive ordinary
shape: FM-024 has `## Acts`, then `## Asks`. On that tracker the helper rejects the tool's own correctly placed refusal
record and accepts the same line forged at the end of Asks. A signed Owner act above the forgery still reads
`merge: your answer`.

## Runs

The four suites were deliberately not rerun, at the Owner's instruction to accept the already-green runs and focus this
pass on code. The Principal reported the hook's four suite runs green in 1309 seconds and a separate 547-check run with
0 skipped; those are inputs to this pass, not runs by this Reviewer.

- Read the full `b73d8f0..729ddae` diff and `refusal_record_in_place`, `append_record`, the RV-715 check, and every live
  tracker containing `## Acts`. FM-024 has another level-two section after Acts; the added check's fixture does not.
- Focused scratch repository at `729ddae`, with its own SSH key and signed Owner act, using the live FM-024 tracker:
  - the tool's exact `append_record` placement at the end of Acts, before Asks, produced commit `fcb633d` and
    `refusal_record(fcb633d) == False`;
  - after resetting to the same base, an unsigned commit in the Owner's name appended the same refusal-shaped line at
    EOF, inside Asks; commit `c97b9b4` produced `refusal_record(c97b9b4) == True`;
  - signed Owner `due:` commit `5ee5169` above that forgery produced
    `('merge', 'merge: your answer', 'signed 5ee5169')`.
- `python3 shoalmark.py --check`: exit 0, 20:59:40–21:00:05 CEST.
- `python3 shoalmark.py --session-check`: exit 0, 21:00:05–21:00:06 CEST.
- `python3 shoalmark.py --queue`: exit 0, 21:00:06–21:00:14 CEST. Its branch line was
  `branch fm/031-the-queue-reads-his-newe… @ 729ddae  wait: no pull request — no verdict on 729ddae`.
- `git merge-tree --write-tree origin/main HEAD`: exit 0 at 21:00:18 CEST, tree
  `8741bb949ee4b4e533e859e853cbe7143defc413`; no conflict.

## Findings

### RV-716 · P1 · confidence high (99%) — content after Acts is treated as Acts, preserving the false merge

`refusal_record_in_place.split` divides each body only at the first `ACTS_HEAD_RE` match and returns the entire remaining
document as the Acts value. It never cuts that value at the next level-two or level-three heading, although
`append_record` does. Its prefix test therefore recognizes a refusal line appended after all later sections as the one
new line "under Acts". The scratch branch carries an unsigned seat-forged line inside Asks, yet `stray_below` exempts
the commit and the queue calls the whole pull request the Owner's signed answer.

The inverse result confirms the same boundary error rather than a fixture artifact: when `append_record` puts the
genuine record before the following Asks heading, the later content shifts within the helper's unbounded list and the
record is rejected. The intended workflow is broken while the P1 route remains open.

Before merge, split the body into three independently compared parts: everything through the Acts heading, the Acts
section ending at the next Markdown heading, and the untouched suffix. Require the prefix and suffix byte-identical and
the bounded Acts content to gain exactly the one refusal line. Pin both FM-024-shaped cases: genuine insertion before
Asks is admitted; insertion inside Asks waits as an unverified commit in the Owner's name.

## Verdict

**NOT READY.** The exact RV-715 fixture is closed and the lightweight gates are green, but RV-716 is the same critical
false-merge path through any tracker whose Acts section is followed by another section.

Path 5 — a merge rules nothing.
