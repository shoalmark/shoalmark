Reviewed: 21852509fda2197065a952ad721c64bb3515e8f9
Tier: critical under TRIAGE.md path line 3 — the queue's reader interprets the Owner's own acts.
Independence: cold — a session the Owner started, no part of session 8e509911.

# FM-031 — cold re-check of 2185250

The RV-716 fix now partitions a tracker into the text before Acts, the Acts section bounded at the next level-two or
level-three heading exactly as `append_record` bounds it, and the suffix. For an existing section, the prefix and suffix
must be byte-identical and its nonblank lines may gain only the refusal line. With no existing Acts section, the new
heading and one refusal line are admitted only immediately before Ship log or at the body's end, the two placements
`append_record` can produce.

## Runs

The four suites were deliberately not rerun, at the Owner's instruction to accept the already-green run and focus this
pass on code. The Principal reported all four hook suite runs green in 1308 seconds; that is input to this pass, not a
run by this Reviewer.

- Read the full `dce3165..2185250` diff, `refusal_record`, `refusal_record_in_place`, `append_record`, all four new
  checks, and the live trackers' Acts/next-section layouts.
- Replayed RV-716 in a fresh scratch repository at this tip, with its own SSH key and a signed Owner act, using live
  FM-024 (`## Acts` followed by `## Asks`):
  - the tool's exact insertion before Asks, commit `3a91a9a`, produced `refusal_record == True`;
  - the same unsigned line forged at EOF inside Asks, commit `4966516`, produced `refusal_record == False`;
  - signed Owner `due:` commit `5928939` above the forgery read
    `wait: an unverified commit in your name on your answer branch (4966516)`, never merge.
- The added checks pin both bounded-section results and the no-Acts placements: a section forged before an ordinary
  heading waits; the tool's section immediately before Ship log merges; the existing body-end case remains admitted.
- `python3 shoalmark.py --check`: exit 0, 21:42:59–21:43:25 CEST.
- `python3 shoalmark.py --session-check`: exit 0 at 21:43:25 CEST.
- `python3 shoalmark.py --queue`: exit 0, 21:43:25–21:43:32 CEST. Its branch line was
  `branch fm/031-the-queue-reads-his-newe… @ 2185250  wait: no pull request — no verdict on 2185250`.
- `git merge-tree --write-tree origin/main HEAD`: exit 0 at 21:43:39 CEST, tree
  `d2da7dab1053400bc1796a1edd42ef5af734bd9c`; no conflict.

## Findings

None. RV-717 through RV-719 were not minted.

## Verdict

**READY.** RV-716 is closed: the accepted unsigned exception is now constrained to the exact structural mutation the
tool makes, both with an existing Acts section and when creating one. The previous false merge and false wait reproduce
correctly at this tip, and the lightweight gates are green.

Path 5 — a merge rules nothing.
