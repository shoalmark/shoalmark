# v0.19.1 — A1, a merge a merge brings: the review at efd500c

Verdict: **READY WITH FINDINGS**. Two P3s; nothing holds READY. RV-2326 to RV-2339 are unused.
Reviewed: efd500ce694ca14a3b3c9c673c3dc6c47af602f3 — `git diff 1f73865 efd500c`, the Builder's `d6c27c5`, `3222566` and `efd500c`, against the Owner's ruling of 2026-10-03: *every merge's own result is judged against each parent under that merge's author, nested merges included.*
Reviewer: b3bdb000/reviewer-84 (claude-opus-5-5, xhigh), at the reviewer's bot address, unsigned, in worktree shoalmark-review-10, on 2026-10-03 and 2026-10-04. Independence: the change's session (b3bdb000), so not independent. Tier: critical — security, and what a commit is judged by; `shoalmark.py`, `test_shoalmark.py` and `README.md` change.

## What holds

- **Every merge a merge brings** is judged by its own change, at any depth, at `--check` and through `MERGE_HEAD`: the trackers that differ from every parent, each move read against each parent, under that merge's author and, under `signed`, its signature. A clean nested merge adds nothing; an ordinary commit is read against its own parent.
- **`-c`** lists the same files as the per-parent intersection on all 235 merges of `1f73865`, and on an octopus, an evil add, an evil delete and a delete on one side.
- **The consumers:** the rights, the Shipped rule and the session rule read the one list, and each is right to: a nested merge by a seat is a seat's commit and names its session.
- **`3222566` stays.** The ruling judges a made merge's own `next: owner` under that merge's author, at HEAD and nested. A merge being committed is refused once, under the author git will write.
- **The cost:** one `git log` walks what a merge brings. Per merge it adds at most one trailer read, plus one `git show` per parent and one for the result, for each tracker of its own. At `d9c154b`, which brings 15 merges, it adds 19 git calls to 314. `--check` medians of three runs, 1f73865's tool against efd500c's: 13.25 s against 12.95 s at `1f73865`, and 17.71 s against 18.64 s at `d9c154b` (00:05:44–00:08:55, 2026-10-04).
- **`efd500c`'s sentence** (README.md:342–346) holds, but see RV-2324. The commit messages and the test names are lean, but see RV-2325.

## Findings

- **RV-2324 · P3:** a merge with no conflicts that combines two parents' edits of different `triage` keys in one tracker is refused as the merger's `triage`, nested or at HEAD. So README.md:345–346's *a clean merge adds nothing* holds only for a merge that equals a parent in every tracker. Fix — README.md:345–346: "A merge that equals a parent in every tracker adds nothing, and never launders a commit that was made without the hook." Or, for the Owner: read a merge's moves per key, not per right.
- **RV-2325 · P3:** `seat_problems`' docstring, `rights_problems`' docstring and its `on_line` comment say more than what is asserted. Fix, each in full: "A made merge's own `next: owner` is judged on its change as well, under that merge's author (`rights_problems`)."; "…and a made merge's own `next: owner`, which no parent carries, read from that merge's own change under its author — the Owner's ruling of 2026-10-03, v0.19.1."; and `# a made merge's own \`next: owner\` is judged on its change, under its author`. `3222566`'s body carries the same clause, and it stays as committed.

## Commands — 2026-10-03 and 2026-10-04, CEST, each time as `date` printed it

- At `efd500c`: `py_compile` exit 0 (23:40:26); `test_core.py` all green, 158 ok, exit 0 (23:40:40); `--check` exit 0 (23:40:59); `--session-check` exit 0 (23:41:00).
- The 51 `test_shoalmark.py` blocks the change reaches — every block that makes a merge, the seats, Shipped and session blocks, and the hooks' merge cases: 307 ok, 0 failed, exit 0 (23:40:46–00:05:26).
- Replay, `--check` with both tools at 8 of the last 30 merges on main, the 8 that bring the 40 nested merges: same exits and lines, 0 differences (23:50:42–23:53:29).

## Controls

- The 8 new checks: at HEAD, 8 ok, exit 0 (23:53:05). Beside `1f73865`'s tool, 8 FAIL, exit 1 (23:54:53).
- Probes, inert identities: a merge two deep whose own result closes a tracker, by a seat without `close`, with an ordinary commit and then the forge's merge on top: exit 4, naming that merge; beside `1f73865` exit 0. A nested octopus: exit 4; beside `1f73865` exit 0. A made merge's own `next: owner`, at HEAD and nested: exit 4; beside `1f73865` exit 0 (23:42:52–23:45:15).

Quality read: the two defects are RV-2324 and RV-2325; the rest reads clean.
