---
template: landing.html
---

<!-- FM-006 slice L: the site renders this page with overrides/landing.html, the landing page — the start page. This prose
     is its source, the German start page's original and llms.txt's Markdown twin of the start page; the site does not show it. -->

# shoalmark

*A Pricke on the Wadden flats keeps the fleet in the channel.*

## Get a better-performing human Owner.

**To the fleet:** you do not wait for tools, you wait for your human. Put to him what only he can decide, as one
sentence per question, once a day, and make his answer one command.

**To the owner:** your agents ask mid-flight, and you stamp what you had no time to read. shoalmark collects those
questions and puts them to you once a day.

**Your agents move on your word — and only your signed word counts.** In the record, an answer counts only as a commit
signed by a key you trust, and the gate refuses an unsigned one: on git, once your seat is marked `signed`, as
[the set-up page](setup.md) does it. Under Subversion, it counts only as a commit the server authenticated as you. A
click, a merge or a line in chat is not an answer. How strong that signature is, you choose — [four tiers](signing.md),
from a key anything on your account can use to one that needs your touch — and every signature names the key that
made it.

## Measured, not promised

In shoalmark's own repository, which runs on shoalmark:

- **Before the owner signed the review rule** (every change gets a Reviewer's pass): 10 of 37 pull requests carried a
  Reviewer's file when they were opened.
- **After it, to 25 September 2026:** 12 of 15.

*Counted on 25 September 2026 with `gh` from pull requests 1–69 of holgo99/shoalmark: merged ones only, without the
owner's own answer branches (`answer/…`). One counts when a commit adding or changing a file under
`work-tracker/evidence/reviews/`, merge commits excluded, is dated before the pull request was opened. A commit's date
is when it was made, not when it was pushed: the forge's push events confirm the counted pull requests from
24 September 2026, 05:18 UTC on, and it no longer lists older ones. The rule is the owner's signed answer of
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

**You lose nothing.** What you keep today stays where it is: shoalmark changes only what it wrote itself. The path for
a fleet of agents that already runs a system of its own is filed (FM-026) and coming.

## What a day costs you

- **One sitting, fifteen minutes**, at the time you choose. The invite comes as a calendar file.
- **One command per answer:** `--answer AP-007 accept`. It writes the answer, signs it with your key and pushes it.
- **The rest comes to you:** every session's last message ends with what waits for you. You open nothing.

## What it is not

No server, no account, no UUIDs. One Markdown file per work item, one Python file, and a gate on every commit that
refuses what contradicts itself. Runs on git and Subversion, on Windows, macOS and Linux. Licence: Apache-2.0 or MIT.

## Start here

| | |
|---|---|
| **You, the owner** | [Set up in ten minutes](setup.md) · [Your answer is your commit](signing.md) · [The standup](standup.md) |
| **Your project's agents** | the [note for trying it](https://github.com/shoalmark/shoalmark/blob/main/ADOPT.de.md) (German): a measurement, not an instruction. They report to you at the end, and you decide |
| **An agent at work** | the contract is `tools/shoalmark/README.md` in your repository, [rendered here](agents/README.md). `llms.txt` is at this site's root |
