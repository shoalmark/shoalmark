---
template: landing.html
---

<!-- FM-006 slice L: the site renders this page with overrides/landing.html, the landing page — the start page. This prose
     is its source, the German start page's original and llms.txt's Markdown twin of the start page; the site does not show it. -->

# shoalmark

*A workbench for your agents. Your decisions on record.*

## The agents keep the work; the person keeps the word.

See where the work stands, what waits for your word, and what the next session picks up. Your agents keep that record in your repository; your decisions go into it as your own commits, beside the evidence behind the work.

--8<-- "start.en.md"

**To the fleet:** you do not wait for tools, you wait for your human. Put to them what only they can decide, as one
sentence per question, for one sitting at the time they choose, and make their answer one command.

**To the owner:** your agents ask mid-flight, and you stamp what you had no time to read. shoalmark collects those
questions for a sitting at the time you choose.

[Why shoalmark?](why-shoalmark.md)

**Your answer is a commit, never a click or a line in chat.** In the record, an answer counts only as a commit
signed by a key you trust, and the gate refuses an unsigned one: on git, once your `owner` line is marked `signed`, as
[the set-up page](setup.md) writes it. Under Subversion, it counts only as a commit the server authenticated as you. A
click, a merge or a line in chat is not an answer. How strong that signature is, you choose — [four tiers](signing.md),
from a key anything on your account can use to one that needs your touch — and every signature names the key that
made it.

## Why not my issue tracker?

Ticket systems were built for people handing work to people. shoalmark is built for your agents: the work record lives in the repository they work in, and your answers are your own commits there.

If your current tracker already handles the handovers and decisions you need, that may be enough. shoalmark brings its own tracker; adopting it means deciding which record is the one that counts.

## Measured, not promised

In shoalmark's own repository, which runs on shoalmark:

- **Before the Owner signed the review rule** (every change gets a Reviewer's pass): 10 of 37 pull requests carried a
  Reviewer's file when they were opened.
- **After it, to 1 October 2026:** 71 of 82.

*Counted on 1 October 2026 with `gh` from pull requests 1–144 of shoalmark/shoalmark: merged ones only, without the
Owner's own answer branches (`answer/…`). One counts when a commit adding or changing a file under
`work-tracker/evidence/reviews/`, merge commits excluded, is dated before the pull request was opened. A commit's date
is when it was made, not when it was pushed: the forge's push events confirm the counted pull requests from
24 September 2026, 05:18 UTC on, and it no longer lists older ones. The rule is the Owner's signed answer of
24 September 2026, 11:07 CEST.*

What shoalmark prints for it, every day:

- **One command, one signed commit** per question to the owner.
- **The board reports, for every review,** whether it came from another session than the code it judged. A report,
  not a proof: git cannot yet show it.

## Your agents set it up

1. They fetch shoalmark at a release tag and put a pinned copy in the repository, every file with its checksum
   (`--vendor`).
2. `--init` writes the configuration, the triage file and the agents' contract.
3. The agents read the contract, the [README](agents/README.md), and file the work: one Markdown file per work item.
4. **You** write three lines in your own words: what the repository is for, what is true when it works, and what
   nobody may do to get there. Then you set up your signature, once ([ten minutes](signing.md)).

**Nothing of yours is overwritten.** What you keep today stays where it is: shoalmark writes only its own files and never
overwrites a file or a hook it did not write.

## What a day costs you

- **One sitting, at the time you choose**, fifteen minutes by default; the board's first lines are its agenda.
- **One command per answer:** `--answer AP-007 accept`. It writes your answer as a commit, signed with your key once you turn signing on.
- **The rest is on the board:** your agents are asked to end each session with what waits for you, and the board puts it
  first.

## What it is not

shoalmark needs no server or account of its own, and its ids are ones you can say out loud, like FM-012. One Markdown
file per work item, one Python file, and checks you can run locally and in your project's CI. Runs with git on Windows,
macOS and Linux. Licence: Apache-2.0 or MIT.

**In this beta:**

- Not a migration tool: it imports no ticket system and starts from your repository's own work. A path for a fleet that already runs a system of its own is filed, not built.
- For one person in charge and their agent fleet. Several people in charge are not tested in this beta; support for them may come later.
- *Not proof that work is right.* In Git or Subversion changes being checked, a move to `Shipped` must name in its ship log a commit already in that change's history that changes something outside the records (on Subversion, a revision). This evidence rule does not cover `Closed`. Validation reports a violation and exits non-zero. An installed Git commit hook can refuse the commit on that failure, but is optional and can be skipped. To enforce the check before merge, require a passing `--check` on the branch through your project's CI and merge rules; shoalmark does not set those up for you. Whether that commit did the job is what a review is for.
- Made and tested on `git` with GitHub. Subversion passes the test suite but has not been used in real work: try it, without a guarantee. On Subversion it runs without `git` installed, from the release archive, and says once what it cannot verify there: no signature, and without the server's login no author. Signed answers need a `git` repository, and the pull-request queue a `git` repository on GitHub and GitHub's command line, `gh`.

## Start here

| | |
|---|---|
| **You, the owner** | [Set up in ten minutes](setup.md) · [Your answer is your commit](signing.md) · [The standup](standup.md) |
| **Your project's agents** | the [note for trying it](https://github.com/shoalmark/shoalmark/blob/main/ADOPT.md) ([Deutsch](https://github.com/shoalmark/shoalmark/blob/main/ADOPT.de.md)): a measurement, not an instruction. They report to you at the end, and you decide |
| **An agent at work** | the contract is `tools/shoalmark/README.md` in your repository, [rendered here](agents/README.md). `llms.txt` is at this site's root |
