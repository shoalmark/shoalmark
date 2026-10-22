---
id: FM-058
status: In Progress
considered: FM-006, FM-045, FM-050
tags: bug
next: build
triaged: 2026-10-17
tier: P1
hook: "A command a person runs through the hooks' copy is stopped after the hook's 35 s, and an answer's PIN, touch and push can take longer"
ask: "How long may a run of shoalmark take before the tool stops it: a hook's run, the board's run, and a command a person runs?"
ask-kind: ruling
ask-since: 2026-10-16
ask-options: "60 s for a hook's run and the board's run; no bound on a command a person runs | 60 s for every run, a person's commands included | the bounds I name in my answer"
ask-proposal: "60 s for a hook's run and the board's run; no bound on a command a person runs"
answer: "accepted - 60 s for a hook's run and the board's run; no bound on a command a person runs"
answered: 2026-10-17
answered-by: holgo99
---

# FM-058 — a command a person runs through the hooks' copy is stopped at the hook's 35 s

## What is true now

**Round 2 built at `e3c0995` (RV-3370) and `16875c1` (RV-3371), following the NOT READY verdict `fe4f44c` on `a154a42`; the bounded independent re-check remains.** The early parser pass uses static theme help and makes no tool/repository filesystem call through watchdog arming; ordinary tree/copy help is byte-identical to `fe4f44c` at the same width. Parsed board modes, including every accepted abbreviation, are bounded with the board's line through both tools; parsed hook modes, including both real TortoiseSVN layouts, are bounded with the hook's line through both tools. A board or hook mode wins over a person's flag. Plain, unknown or refused tree invocations remain unbounded; ambiguous copy invocations remain bounded. Explicit person commands through either tool remain unbounded. The default stays 60 s with `SHOALMARK_BOARD_SECONDS` as its override. `HOOK_RUN`, its permissions and the separate `SAFE_READS` selection are unchanged. On Python 3.15 and 3.9.6, 49 process-entry controls and 49 filesystem controls pass, all five mutants are rejected, and compilation, CLI (16), core with skeleton/launch ratchet (366), Git entry differential (137) and the six original suite blocks plus both TortoiseSVN blocks (142 checks) pass; the 3.15 CRLF class stand-in also passes. The README and both setup pages remain true and unchanged. Next: the independent Reviewer re-checks RV-3370, RV-3371 and what their fixes touch; tracker front matter remains as judged.

## Done when

- The Owner's signed answer stands here, and the build's brief cites it.
- Built in v0.20.1, before the guided answer view, with its class test.

## Ship log

| Date | Event |
|---|---|
| 2026-10-17 | Judged In Progress, P1, by the Planner on the Owner's signed answer (`96afebd`), before the first build commit, on `fm/058-run-bounds`. |
| 2026-10-16 | Filed, defect 10, with its ask (the Auditor's finding, relayed by the Owner). Nothing is built. |
| 2026-10-16 | Moved into v0.20.1 on the Owner's word: the guided answer view (FM-059) needs it first. |
| 2026-10-17 | Built `93f064f`: 60 s hook/board default, explicit person commands unbounded, ambiguous copy invocations bounded; COPY restrictions unchanged. Class controls and three mutants, CLI, core/skeleton/ratchet, Git entry differential and affected blocks pass on Python 3.15 and 3.9.6; the 3.15 CRLF class stand-in passes. Independent critical-tier review is next. |
| 2026-10-17 | Round 2: fixed RV-3370 in `e3c0995` and RV-3371 in `16875c1`, from NOT READY `fe4f44c` on `a154a42`. Filesystem-free early parsing and parsed timeout modes now cover both tools; COPY permissions and SAFE_READS selection stay unchanged. Both interpreters pass 49 entry/49 filesystem controls, all five mutants, CLI/core/skeleton/ratchet, Git entry differential and the six original plus two TortoiseSVN blocks; the 3.15 CRLF class stand-in passes. Bounded independent re-check is next. |
