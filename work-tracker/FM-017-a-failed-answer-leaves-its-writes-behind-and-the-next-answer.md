---
id: FM-017
status: Shipped
considered: FM-012, FM-016, FM-013
tags: bug
hook: "When the pre-commit gate refuses the commit, `--answer` returns and leaves everything it wrote: the tracker staged with the Owner's answer, the INDEX.md the hook rewrote, and a new `answer/<id>` with no commit of its own, checked out. His next `--answer`, on another ask, is refused with *the working tree has changes* — no paths, no word that the changes are the tool's own, and his answer text nowhere on screen."
---

# FM-017 — A failed --answer leaves its writes behind, and the next --answer cannot say why it refuses

## What is true now

**Built 2026-09-23 on `fix/0.17.4-the-answer-says-what-it-does`; merged 2026-09-23 (#12), released as 0.17.4.** It hit the
Owner the same day.

**A failure after the first write now leaves nothing behind.** `--answer` refuses a tree with tracked changes before it
touches anything, so every tracked path that differs when a later step fails is the run's own. On a refused commit — and
on any failure after the branch is cut — it restores each of those paths from `HEAD`, switches back to the branch it
started on, and deletes an `answer/<id>` it cut if that branch carries no commit. It prints what refused the commit (the
tail of the hook's own output, not git's last line), what it undid, **the answer text, and the exact command that
gives it again** — a refusal never costs the Owner his words. A signature that fails to verify after a *successful*
commit is unchanged: the answer is committed, not lost, and the message says how to amend it.

**The dirty-tree refusal names the paths.** Where one of them is a tracker carrying an `answer:` that is not committed,
it says that looks like an earlier `--answer` that failed half-way, gives **one** command that undoes exactly the
tool's leftovers — that tracker and the generated files — and the command that gives the answer again. What is not the
tool's is named apart: *commit or stash it*.

Four checks, in a scratch repository whose pre-commit hook rewrites INDEX.md and exits 1: after `--answer` the tree is
clean, the run is on its starting branch, no `answer/<id>` is left, the hook's words and the answer are printed, the exit
is non-zero; the refusal names the paths, calls the leftover what it is, and its command restores the tool's files and
leaves the Owner's own change. **What is left:** nothing.

**What happened, at 0.17.3.** `--answer` checked the tree was clean, cut `answer/<id>`, wrote the three lines, staged
them and committed. The gate refused the commit (exit 4) and the command returned `the commit failed — <git's last
line>`: the tracker staged with the answer, INDEX.md rewritten by the hook, the empty branch checked out. The next
`--answer` on another id was refused with *"the working tree has changes … commit or stash first"* — not which paths,
not that they were its own leftovers, not the answer they held.

## Why

The Owner's one command is the only way to answer. A command that fails and leaves its own writes behind turns one
refusal into two, and the second one blames the Owner's tree for the tool's mess — while the answer he gave sits in a
staged file he has no reason to look at.

## Done when

- A commit the gate refuses, and any failure after the first write, restores every tracked path the run changed,
  switches back to the branch the run started on, and deletes `answer/<id>` if this run created it and it carries no
  commit.
- The failure prints the gate's refusal as the hook printed it, the answer text, and the exact command to run again.
- The dirty-tree refusal names the dirty paths; a tracker carrying an uncommitted `answer:` is called a failed earlier
  `--answer`, with the one command that undoes it.
- Checks hold both: a hook that exits 1 leaves a clean tree on the starting branch with no `answer/<id>`, the answer
  printed and a non-zero exit; the refusal names the paths.

## Ship log

| Date | Event |
|---|---|
| 2026-09-23 | Merged (#12), released as 0.17.4. |
| 2026-09-23 | Filed and built: a failed run restores its paths, goes back, deletes its empty branch, prints the hook's words and the answer; the dirty-tree refusal names the paths and the undo. Four checks. |
