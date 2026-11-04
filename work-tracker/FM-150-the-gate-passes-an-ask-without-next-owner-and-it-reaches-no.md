---
id: FM-150
status: Proposed
considered: FM-008, FM-141, FM-149
tags: process
epic: FM-139
hook: "An open tracker can carry a put ask, `ask-id:` and `ask:`, without `next: owner`. The gate passes it, the Owner's queue never shows it, and `--answer` refuses it. FM-149 was filed that way and passed `--check`."
---

# FM-150 — the gate passes an ask without next: owner, and it reaches no one

## What is true now

**2026-11-04 — filed, Proposed, on the Auditor's brief; nothing is built.**

1. **An ask's id is minted with `next: owner`.**
   - The schema says so for `ask-id:`, "minted with `next: owner`; a draft (`next: review`) has none"
     ([`shoalmark.py` L992](https://github.com/shoalmark/shoalmark/blob/c43af896efaeefea1dde4fa790d4db269ae86410/shoalmark.py#L992)).
   - `--answer` refuses an ask without it: "an ask waits on the Owner with `next: owner`; the seat that asks sets it"
     ([L3410–L3412](https://github.com/shoalmark/shoalmark/blob/c43af896efaeefea1dde4fa790d4db269ae86410/shoalmark.py#L3410-L3412)).
2. **The gate does not hold that rule.**
   - `ask_problems` holds every open ask to its form. It asks for a recommendation, and runs the seats check, only
     under `next: owner`
     ([L1759–L1799](https://github.com/shoalmark/shoalmark/blob/c43af896efaeefea1dde4fa790d4db269ae86410/shoalmark.py#L1759-L1799)).
   - `ask_id_problems` checks the id's shape, that an `ask:` stands beside it, and that its number is not reused. It
     never reads `next:`
     ([L2413–L2434](https://github.com/shoalmark/shoalmark/blob/c43af896efaeefea1dde4fa790d4db269ae86410/shoalmark.py#L2413-L2434)).
   - So an open, unanswered tracker with `ask-id:` and `ask:` passes `--check` when its `next:` is missing or names
     another move
     ([L10525–L10529](https://github.com/shoalmark/shoalmark/blob/c43af896efaeefea1dde4fa790d4db269ae86410/shoalmark.py#L10525-L10529)).
3. **Nothing shows it.** These read only trackers with `next: owner`:
   - the Owner's queue, `owner_queue`
     ([L1811–L1821](https://github.com/shoalmark/shoalmark/blob/c43af896efaeefea1dde4fa790d4db269ae86410/shoalmark.py#L1811-L1821));
   - the asks sent back, `malformed_asks`
     ([L1824–L1833](https://github.com/shoalmark/shoalmark/blob/c43af896efaeefea1dde4fa790d4db269ae86410/shoalmark.py#L1824-L1833));
   - the Board's own queue
     ([L4418](https://github.com/shoalmark/shoalmark/blob/c43af896efaeefea1dde4fa790d4db269ae86410/shoalmark.py#L4418)).

   Such an ask is in none of them, so neither the Board, `--owner` nor `--standup` names it.
4. **It happened once.** [FM-149](FM-149-the-docs-the-board-s-prompts-and-the-skills-have-no-one-rule.md) was filed
   with FM-149-Q1 and no `next:` line, and `--check` passed it. Its branch's review found it as RV-4360
   ([`b8198a5`](https://github.com/shoalmark/shoalmark/commit/b8198a554e3b492c3eedb13c5d63395bfb6f680e)), and
   [`0bd95d1`](https://github.com/shoalmark/shoalmark/commit/0bd95d1769b92044d342a18aac7e2fe2c17bf005) set
   `next: owner` before the push.
5. **Main holds no such ask.** Read with the tool at `c43af89`: no open, unanswered tracker carries `ask:` or `ask-id:`
   without `next: owner`. None is sent back.

## Why

An ask is how the Owner rules, and the seat that files one believes it is asked. One without `next: owner` is asked of
no one, and nothing says so: the gate passes it, the Board does not list it, and `--answer` refuses it. The gate is
where every other ask rule is refused first, "the same rules the Owner's queue reads, refused here first"
([L10527](https://github.com/shoalmark/shoalmark/blob/c43af896efaeefea1dde4fa790d4db269ae86410/shoalmark.py#L10527)).

## Decisions, for the Owner

1. **The rule:** an open, unanswered `ask:` stands only with one of two moves, the two the schema names for `ask-id:`
   ([L992](https://github.com/shoalmark/shoalmark/blob/c43af896efaeefea1dde4fa790d4db269ae86410/shoalmark.py#L992)):
   - `next: owner`, a put ask, with its `ask-id:`;
   - `next: review`, a draft, with none.

   The gate refuses any other, and its message names both ways out.
2. **One rule, read everywhere.** It lives in `ask_problems`, and `malformed_asks` and the Board's sent-back list
   read every open, unanswered `ask:`, not only one under `next: owner`
   ([L1830](https://github.com/shoalmark/shoalmark/blob/c43af896efaeefea1dde4fa790d4db269ae86410/shoalmark.py#L1830),
   [L4418](https://github.com/shoalmark/shoalmark/blob/c43af896efaeefea1dde4fa790d4db269ae86410/shoalmark.py#L4418));
   so the gate, `owner_queue`, `malformed_asks` and the Board read the same rule. One that got in anyway, by a merge
   or under `--no-verify`, is listed as sent back on the Board, under `--owner` and under `--standup`, with its reason.
   [README section 5's table of refusals](https://github.com/shoalmark/shoalmark/blob/c43af896efaeefea1dde4fa790d4db269ae86410/README.md#L178-L206)
   gains its row, beside [FM-141](FM-141-the-readme-s-refusal-table-lacks-s1-s-ask-id-refusals-and.md)'s.
3. **The tests:**
   - the gate refuses `ask-id:` and `ask:` with no `next:`, with `next: build`, and with `next: review`, since a
     draft has no id;
   - it passes the same with `next: owner`, and a draft with `next: review`;
   - the refused one is listed as sent back;
   - a mutant that drops the rule fails.
4. **Allocation:** v0.20.3, under current path 5, "reliable and simpler first"
   ([TRIAGE.md L22](https://github.com/shoalmark/shoalmark/blob/c43af896efaeefea1dde4fa790d4db269ae86410/work-tracker/TRIAGE.md#L22)).

## Done when

Each item names its commit or pull request when it lands.

- [ ] **The gate refuses an open ask** that has neither `next: owner` nor `next: review`, or an `ask-id:` under `next: review`, and names the fix.
- [ ] **One that got in anyway is listed as sent back** on the Board, under `--owner` and under `--standup`.
- [ ] **The tests hold,** and the mutant that drops the rule fails.
- [ ] **The CHANGELOG names the rule,** since a repository holding such an ask is refused after it upgrades.

## Ship log

| Date | Event |
|---|---|
| 2026-11-04 | `epic: FM-139`: under v0.20.3's epic until the Owner decides whether it goes in. Records only. |
| 2026-11-04 | The standard review's P3s fixed forward: RV-4364, the gate loop's link; RV-4365, FM-149 and README section 5's table linked; RV-4366, decision 2's first sentence; RV-4367, decision 3's first test and the first Done-when item. Records only. |
| 2026-11-04 | Filed, Proposed, on the Auditor's brief. Nothing is built. |
