# Review — FM-031 filed, at 3c72e84 (2026-09-24 08:48 CEST, Reviewer, session `8e509911/reviewer-1`)

- **Chain:** `d935807` … `df5b672` (implementer-10), then `993a8d9` … `001ee70` (implementer-11), then `3c72e84`
  (the principal seat).
- **Already merged:** PR #39 merged the chain through `001ee70` into `main` at 08:41 CEST, before any verdict. The tip
  is PR #40.

**Re-derived here, and true:**
- **Sessions:** the id count is 21 (9 GtM, 8 Implementer, 2 Principal, 2 Reviewer), from `sessions.md` on every
  remote branch, window 09-23 18:00 → 09-24 08:20 CEST. But see R2.
- **Pull requests:** 22 opened in the window (#17–#38), and 13 merged by 08:20 (`gh pr list`).
- **The six open pull requests' states** (#33 ready; #37 inside #33; #38 carried into #33; #35 conflicting in
  `sessions.md`; #34 and #36 without a verdict) match what this seat recorded on them this morning.
- **Closed:** 15 on `main` (2 on 09-22, 13 on 09-23). **Filed on 09-23:** 16.
- **Not re-derived:** the parent project's two conflicts, and the five questions to one session.

**The rest checked:**
- **The ask:** one `?`, at the end; 287 characters; the proposal is option 1 of 4, offered first.
- **The parent project** is cited only by its pull-request numbers (806, 807) and *its registry*. No name, and no id.
- **`considered:`** gives a reason for each of the four (ship-log row 08:24).
- **Session ids `-10` and `-11`** are unique across `origin/main` and every remote branch.
- **`--session-check`, run at each commit as that commit's session:**

  | commit | session | exit |
  |---|---|---|
  | `6f31995` | `-10` | 0 |
  | `df5b672` | `-10` | 4, *no open row*, by design after the close |
  | `6592744` | `-11` | 0 |
  | `001ee70` | `-11` | 4, by design |
  | `3c72e84` | `8e509911` | 0 |

- **Gates at `3c72e84`:** `--check` 0; `test_shoalmark.py` 0 (264 ok); `test_core.py` 0 (148 ok). It merges
  cleanly into `origin/main` `3ba7383`.

## Findings

**R1 · P2 · The answer to the Owner's filing question counts five filings from before its window.**
- **What:** *The record starts 2026-09-22 11:09*. That is `ae1f05e`, the commit that **moved** the trackers from
  `docs/work-tracker/` to `work-tracker/`. FM-001–FM-005 were filed on 2026-09-21: `8cbe3a4` 13:13 … `8947caf`
  20:21.
- **So:** the table's *11 filed* on 09-22 is 6. Within the 1.89-day window the numbers are:

  | | the tracker says | in the window |
  |---|---|---|
  | filed | 16.4 a day | 13.8 a day (26 filed) |
  | closed | 8.0 a day | 7.9 a day |
  | ratio | 2.07 | 1.73 |
  | open count grows | about 8 a day | about 5.8 a day |

  Over the true span from 09-21 13:13 (2.80 days) it is 11.1 against 5.4, a ratio of 2.07.
- **Why it matters:** *about two to one* survives, but every per-day figure is inflated by 20–50 %. Through #39 this
  text is already on `main`.
- **What closes it:** date a filing by the first commit of its **id** under either path, and state one window.

**R2 · P3 · 21 sessions is 21 ids.** 22 sessions began in the window. `8e509911/implementer-6` named two of them: the
site slice at 01:02, and FM-028 at 07:41. That is FM-028's R1, the class of FM-027.

**R3 · P3 · *At 08:10 six were open* is timed wrong.** At 08:10 only #33 was open. #34–#38 were opened 08:17–08:18, so
six were open from 08:18. The count is right; the time is not.

**R4 · P3 · Should this be a new tracker at all?**
- S1 (one file per session) reshapes FM-024's registry, so it is arguably an FM-024 slice.
- S2 (the queue) is the Owner's many small decisions, FM-005's ground.
- The reasons given say why each is not *this*, but not why this is not a slice of one of them. The default is a slice.

**Verdict:** NOT READY. R1 (P2) is open; R2, R3 and R4 are P3.
