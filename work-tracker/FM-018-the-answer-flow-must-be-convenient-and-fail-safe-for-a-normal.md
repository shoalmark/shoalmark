---
id: FM-018
status: Proposed
considered: FM-012, FM-013, FM-016, FM-017, FM-007, FM-005
tags: bug
next: owner
ask: "Your two dashboard requirements of 12:43 (evidence listed per tracker; a guided run-sheet dialog) are features. Your filing freeze (FM-032 S4) files only defects and sends the rest into an open tracker's body, or to wait. Which route for these two?"
ask-kind: ruling
ask-since: 2026-09-28
ask-options: "lift for one pass: `freeze_at` 24, then back to 8 — any seat's feature filing passes meanwhile | fold, the freeze's own route: slices of this tracker, built under its rank once its design is ruled | hold, the freeze's other route: raised lines here until fewer than 8 trackers are open"
ask-proposal: "lift for one pass: `freeze_at` 24, then back to 8 — any seat's feature filing passes meanwhile"
triaged: 2026-09-23
tier: P1
hook: "Answering takes a normal user through branch switches, a checkout a seat's worktree may hold, an older pinned tool on the wrong branch, leftovers from a failed run, a silent minute, a board that offers an answered ask again and a dialog ending in abort. The Owner: *\"Normal\" users won't like this — we have to make this convenient and fail-safe.* The requirement: he answers from wherever he stands, and his checkout is never switched, dirtied or left behind."
---

# FM-018 — The answer flow must be convenient and fail-safe for a normal user

## What is true now

**Filed 2026-09-23; nothing is built as this tracker, and no design is chosen — the Owner rules.** Four of its parts are
filed on their own: [FM-012](FM-012-a-load-spawns-git-once-per-tracker-and-answer-is-silent-for.md) (the silent
minute), [FM-013](FM-013-after-ok-the-answer-dialog-leaves-only-abort-and-says.md) (the dialog that ends in abort),
[FM-016](FM-016-an-answered-ask-still-shows-as-unanswered-on-the-branch-the.md) (the answered ask offered again) and
[FM-017](FM-017-a-failed-answer-leaves-its-writes-behind-and-the-next-answer.md) (the leftovers of a failed run). FM-012,
FM-013 and FM-017 are built for 0.17.4; FM-016 waits for a ruling. What none of them changes is the shape underneath:
`--answer` works **in the Owner's own checkout**, so it must switch his branch, it runs his checkout hook, and whatever it
writes lands in his tree.

The Owner, in his words: *"Keep in mind that "Normal" users won't like this - We have to make this convenient and
fail-safe."*

**One morning's evidence, as he met it:**

1. he had to switch branches by hand to reach the branch that carries the ask;
2. a seat's worktree held that branch, so his switch failed;
3. he answered from the wrong branch, running an older pinned copy of the tool, and the gate refused the answer;
4. the failed run's leftovers blocked his next answer, and he cleaned them up by hand (FM-017);
5. each answer ran about a minute with no output (FM-012);
6. the board on his main branch offered an ask he had already answered (FM-016);
7. the dialog's last button was *abort* (FM-013).

**Open, from [FM-013](FM-013-after-ok-the-answer-dialog-leaves-only-abort-and-says.md) (shipped in 0.17.4):** the
dialog's second screen is not proven with a real clipboard in the Owner's browser, at phone width, or against the live
signing page, which is served only once the documentation site is public.

**The Principal's candidate, NOT chosen:** `--answer` finds the branch that carries the ask, commits in a **temporary
`git worktree`** of that branch — signed, with the Owner's identity and key — pushes `answer/<id>`, and removes the
worktree whether it succeeded or failed. No switch, no checkout hook in his tree, nothing left behind; and a branch a
seat's worktree holds is no obstacle, because the answer never checks it out.

## Why

An answer is the Owner's one act in the whole flow, and every step above is a place where a normal user stops and
concludes the tool is broken. A process he has to nurse through git is a process he will route around — and an answer
routed around the gate is the one thing the gate exists to prevent.

## Done when

- The Owner has ruled on the design — the candidate above or another — and it is recorded here.
- He answers from whichever branch he stands on, and his checkout is never switched, never dirtied and never left
  behind, whether the answer succeeds or fails.
- The seven points above are each either gone or named here with why they remain.
- **A moved submodule pointer alone does not stop him.** When the only change in his checkout is a submodule pointer, a tracker-only write (`--answer`, `--done`, `--due`) either does not count it, or the refusal names the fix — `git submodule update <path>`; the builder chooses. Raised 2026-09-28 12:50:35 by the Auditor through the Owner (60 %).

## Merged in from FM-016 — the answered ask offered again (2026-09-23, the first triage pass)

*FM-016's state when merged:*

**Filed 2026-09-23; nothing is built, and no way forward is chosen — the Owner rules later.**

**What he sees.** `--answer <id>` cuts `answer/<id>` from the branch that carries the ask, commits the answer there and
pushes it. The Owner then goes back to his main branch. The board there is built from main's trackers, where the ask
has no answer yet — so `<id>` is still in *waiting for you*, with accept and reject, until a merge brings the answer
in. The Owner, in his words: *"A user would now be confused because <id> shows as unanswered while they just have
answered in the last step — this is something we have to figure out later."*

**What a second click does, reproduced here on 0.17.3** in a scratch repository — answer from the ask's branch, switch
to `main`, answer again:

```
--answer: `answer/ap-001` exists and its tip does not carry this ask — it was cut from another branch or the ask has
changed since. Delete it (`git branch -D answer/ap-001`) or answer from the branch that carries the ask
```

The refusal is right to stop, and wrong in what it says: the branch **does** carry the ask, and the advice is to delete
the branch holding the answer he just gave. One line on the way: the tip test compares the tip's raw `ask:` value,
quotes included, with the tracker's unquoted one, so a quoted ask never reads as carried — every existing
`answer/<id>` is refused this way, whichever branch it was cut from.

**Candidates, none chosen:**

- **(a)** the board reads the `answer/*` branches, local and remote-tracking, and in place of the buttons shows
  *answered on `answer/<id>`, not merged yet*;
- **(b)** `--answer` refuses when `answer/<id>` already exists and says what it is — an answer given and not yet
  merged — instead of advising its deletion;
- **(c)** the answer lands where the board is read.

## Raised

*One sourced line per raise — the date, who raised it, the fact, its source, what it undermines; no counts. The Auditor seat's words as the Owner pasted them, word for word.*

- 2026-09-28 12:43:02 · Auditor (8b91dba2), through the Owner (his paste headed *To: 8e509911 principal (shoalmark-principal-4)*, *The Owner's requirements for the dashboard*; the whole paste, six lines, saved word for word, sha256 `4a6f20c85637094e3528c3f5ef780e0c9e942115d93df572a255a22b02cc8a7a`; items 2 and 3 and the paste's closing line — the Auditor's, not the Owner's — are quoted here — item 1 went to FM-030) · his own words in it, as the Auditor normalised them: *"my guess is it's overkill to implement, but it's a requirement nonetheless"*; *2. Evidence inspectable per tracker: list evidence/<ID>/ on each tracker, rendered read-only. I found no such view (search only, 65%). 3. A guided run-sheet dialog, for non-technical users. Counsel (70%): a fixed step format first (command, expected output, stop rule, paste-back; lint-checked), then a one-step-at-a-time dialog whose paste-back fills the result table. Boundaries (90%): the dashboard never executes a command, and every paste is screened for secret shapes before it is written. File and rank them your way.* — the Principal, 2026-09-28: both are features; `--related` gives them no home (FM-013 4.8 and FM-002 4.0 are Shipped; FM-004 4.3 is research); the filing freeze — FM-032 S4, his signed *all four now* of 2026-09-24, `freeze_at = 8`, 22 open — admits bug filings only and checks no identity; a seat lifts no rule of his and tags no feature as a bug — so the ask above, on this tracker because FM-032's S5 exchange waits for its build and this is the normal user's tracker; after his answer the seat clears the exchange with `--clear-ask FM-018 wait` — this tracker's own design stays unruled and its `next:` returns to `wait`. The options' reach, kept out of the fields by the tool's length rule: the lift sets `freeze_at` to 24 by his word and back to 8 on the pass's branch that files the two — while it stands at 24 any seat's feature filing passes, and 24 stays his number until reset; fold and hold are the freeze's own two routes as `--new`'s refusal and `--schema` state them (anything but a defect goes as one line into the closest open tracker's body, or waits) — his rule as written, no count changes; the proposal is the lift, for one pass · source: the paste; `shoalmark.toml` line 4 and `shoalmark.py` :69–75 at `9e9fcb33` · undermines: no signed rule — it asks how his freeze meets his requirement
- 2026-09-28 12:50:35 · Auditor (8b91dba2), through the Owner (his message headed *To: 8e509911 principal (shoalmark-principal-4)*, two lines, saved word for word, sha256 `436b4c6a727058117fab253e56f698555ea4ccaadd390f3df6cbcd25627144d0`; quoted whole) · *The Auditor (60%): --done refused the Owner because the only change in his checkout was a moved submodule pointer (portdive-webhooks). The refusal should name the fix (git submodule update <path>) when that is all that differs, or not count it at all for a change that writes only a tracker. Another item for the non-technical path.* — checked by the Principal at `9e9fcb33`: `changed_paths` (:2018) reads `git status --porcelain -z --untracked-files=no`, where a moved submodule pointer is an `M` entry like any file, and `dirty_refusal` (:2031) lists it as changed; no line names a submodule or its fix · source: the paste; `shoalmark.py` at `9e9fcb33` · undermines: no signed rule — a case of this tracker's own subject (his checkout never dirtied, never left); the Done-when bullet below

## Ship log

| Date | Event |
|---|---|
| 2026-09-28 | The docs pass `992fb5d` on `3a417db` NOT READY (reviewer-48; RV-755 P2 — the options did not say what each does to his rule, and the lift read narrower than it is; RV-756…759 P3), closed in the next commit: the ask names the freeze's two routes — fold, hold — as his rule as written (`--new`'s refusal, `--schema`) and the lift's reach (any seat's feature filing while it stands at 24; set back to 8 on the pass's branch); the line numbers read at `9e9fcb33` (:2018, :2031 — the first commit cited the board build's tree); the paste's closing line is the Auditor's; after his answer the seat clears the exchange and `next:` returns to `wait` (RV-759). |
| 2026-09-28 | **Asked, kind ruling — the proposal *lift for one pass: `freeze_at` 24*** (`next: owner`; FEAT-190's ledger row 57 written first; after his answer the seat clears the exchange and `next:` returns to `wait`): where the Owner's two dashboard requirements of 12:43:02 — the evidence folder listed on each tracker; a guided run-sheet dialog for non-technical users (the Auditor's counsel, paste sha256 `4a6f20c85637094e3528c3f5ef780e0c9e942115d93df572a255a22b02cc8a7a`) — go under the filing freeze (FM-032 S4, his *all four now*; 22 open, bugs only): lift for them, fold here, or hold. Hosted here because FM-032's S5 exchange waits for its build and this is the normal user's tracker. **Raised, 12:50:35**: `--done` refused him on a moved submodule pointer alone (portdive-webhooks; the Auditor, 60 %, paste sha256 `436b4c6a727058117fab253e56f698555ea4ccaadd390f3df6cbcd25627144d0`) — the Done-when bullet *A moved submodule pointer alone does not stop him*. Item 1 of the 12:43:02 paste went to FM-030, the 12:49:43 counsel to FM-040. |
| 2026-09-23 | **FM-016 merged in by the first triage pass** — its open scope (part b: the answered ask still offered on the branch the Owner returns to) lives here now; E0 at the 09-24 sitting decides whether any of the flow is built. |
| 2026-09-23 | FM-013's three unproven points joined the open items (R9). |
| 2026-09-23 | Filed from the Owner's morning and his words; FM-012, FM-013, FM-016 and FM-017 named as its parts. The design is his to rule. |
