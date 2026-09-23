---
id: FM-012
status: Proposed
considered: FM-007, FM-008, FM-010
tags: bug
next: build
hook: "Reading the trackers spawns `git config user.name` once for every tracker that has no `answered-by:` — nearly all of them. On a 505-tracker corpus that is 504 subprocesses and 15.2 s of a 16.8 s load. `--answer` loads the corpus about four times and prints nothing until the end, so an Owner stopped it believing it had hung."
---

# FM-012 — A load spawns git once per tracker, and --answer is silent for a minute

## What is true now

**Filed 2026-09-23; nothing is built.** Profiled by the Principal with cProfile on a consumer's 505-tracker corpus and
re-measured here, read-only, before anything changed.

**The cost is one line in `extract()`** (`shoalmark.py:568` at 0.17.3):

```python
"answered_by": (lambda v: git_user() if v in ("", "<you>") else v)((fm.get("answered-by") or "").strip()),
```

`git_user()` is a `git config user.name` subprocess. The default was meant for the one tracker the Owner is answering
by hand — `answered-by: <you>` — but the condition is *the key is empty*, and on a tracker with no answer at all the key
is always empty. So every tracker without an answer pays one process start.

| on a 505-tracker corpus | measured |
|---|---|
| `git config user.name` calls in one `load_trackers()` | **504** |
| their share of `load_trackers()`, cProfile | **15.2 s of 16.8 s** |
| `load_trackers()`, wall clock, median of 3 runs here | **16.4 s** |

**`--answer` pays it about four times** and says nothing while it does: once in the command itself, once in the
post-checkout hook that refreshes the board when it cuts `answer/<id>`, and in the pre-commit gate when it commits. The
first line it prints is the last one. The Owner, in his words: *"It not hung it only took very long - too long without
any feedback within ther terminal so i thought it must be hanging"*. He stopped it.

**Pre-registered claim, to be measured the same way after the fix:** `load_trackers()` on the same 505-tracker corpus
drops from ~16.8 s to **under 2 s**, and the `git config user.name` calls from **504 to at most 1**.

## Why

The Owner's one command is the only supported way to answer. A command he stops half-way is worse than a slow one: it
may have cut the branch and not committed, or committed and not pushed. And a gate that costs seconds per hundred
trackers is a gate a larger repository learns to skip.

## Done when

- `answered-by:` is defaulted **only where the tracker carries an `answer:`** and the key is empty or `<you>`, and the
  committer's name is read **at most once per run** (memoised, reset when the tool is pointed at another repository).
- `--answer` prints each step to stderr, **flushed, as the step starts**: reading the trackers · cutting
  `answer/<id>` from `<branch>` (the checkout hook refreshes the board) · committing, signed (the gate runs) · pushing
  to `<remote>`. Today's final lines are unchanged.
- The claim above is measured after the fix on the same corpus, both numbers recorded here.
- A check holds each half: a load with no answers spawns no `git config user.name`, a load with several asks it once;
  and `--answer` names its steps in order.

## Ship log

| Date | Event |
|---|---|
| 2026-09-23 | Filed. Profiled on a 505-tracker corpus: 504 `git config user.name` calls, 15.2 s of a 16.8 s load. |
