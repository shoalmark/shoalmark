---
description: "A week with shoalmark in four steps: your part in it, what it does not do, and how to try it with your agents."
---

# How it works

shoalmark keeps your project's work as plain files inside the project, so every agent that works on it reads the same current state. It shows you first what is waiting for your answer, and it counts work as done only when a saved change (a commit) in the project's history backs it.

## A week in four steps

**What needs your word waits for it; no agent answers for you.**

1. **The agents work and record where the work stands.** Each work item is a Markdown file with what is true now and what comes next. A *done* with no commit behind it is refused by the gate.
2. **What only you can decide becomes a question.** When an agent needs your decision it writes it down as one sentence, with the options and its own proposal, and carries on with other work. Between standups nobody interrupts you, except for what cannot be undone.
3. **Once a day, you sit.** At the time you chose, the standup prints the agenda: your decisions first, each with how long it has waited and what it holds up. You answer with one command per question; it writes the answer, signs it with your key and pushes it.
4. **The agents act on your answer, and a reviewer judges before the merge.** A seat that holds the right to do so records your answer in the work item and moves on. Before work reaches a merge, a reviewer checks it; the board says whether that pass was independent, meaning it came from another session than the code. That is a report, not a proof. `--queue` lists the open pull requests in the order to merge them.

<figure class="week" markdown="0">
<div class="week-card"><h3 class="t">FM-024</h3><p class="src">work-tracker/FM-024-….md · 2026-09-28</p>
<pre lang="en">next: owner
ask: "Do the status-line scripts for Claude and Codex and the addressing rule ship with shoalmark, so a pinned copy carries them?"
ask-kind: ruling
ask-since: 2026-09-28
ask-options: "all three: --statusline, … | the status line only: … | the rule only: …"
ask-proposal: "all three: --statusline, --install-statusline for Claude and Codex, and the AGENTS.md rule with --whoami"</pre></div>
<p class="week-arrow" aria-hidden="true">↓</p>
<div class="week-card board"><h3 class="t">board</h3>
<div class="wk-board" lang="en"><p><i>##</i> <b class="hot">waiting for you: 3</b></p>
<p><span class="id">FM-024</span> Do the status-line scripts for Claude and Codex and the addressing rule ship with shoalmark, so a pinned copy carries them? · a ruling <span class="chip">accept</span><span class="chip">reject</span></p></div></div>
<p class="week-arrow" aria-hidden="true">↓</p>
<div class="week-card"><h3 class="t">4127dba</h3><p class="src">git commit · 2026-09-28</p>
<pre lang="en"><span class="del">-next: owner</span>
<span class="add">+next: build</span>
<span class="add">+answer: "accepted - all three: --statusline, --install-statusline for Claude and Codex, and the AGENTS.md rule with --whoami"</span>
<span class="add">+answered: 2026-09-28</span>
<span class="add">+answered-by: …</span></pre></div>
<figcaption>From shoalmark's own repository: one question, from the work item through the board to the Owner's answer — a signed commit that adds three lines to the work item and sets <code>next</code> from <code>owner</code> to <code>build</code>. The excerpts are verbatim; each … marks a cut.</figcaption>
</figure>

**Not everything needs you.** A seat that holds the right to close closes work without asking you. Shipped with the tool are three seats with fixed rights: the planner may ask, close and triage, the reviewer may triage, the builder holds none of the four. For any other seat you set the rights yourself. Only a seat you give the right may answer, and by default that is you alone.

**How firmly "no agent answers for you" holds is set by your signature.** A signature proves the key, not the hand: whoever can use your key can answer as you. There are four tiers, from a key anything on your account can use to one that needs your touch. [Your answer is your commit](signing.md) helps you choose.

## Your part

- **Once:** you write three lines in your own words in `TRIAGE.md` (what the repository is for, what is true when it works, and what nobody may do to get there) and the current path, what comes first. And you set up your signature, in about ten minutes.
- **Each week:** one standup each weekday, fifteen minutes at the time you chose (that is what the calendar invite says; the length can be set), and one command per answer.
- **The rest comes to you:** every session's last message ends with what waits for you. You open nothing.

## What shoalmark does not do

- It does not scan your code for security problems or data leaks.
- It does not prove that work is right. The gate refuses a *done* with no commit behind it; whether that commit did the job is what a review is for.
- It is not a migration tool: it imports no ticket system and starts from your repository's own work.
- Today it fits a project with one person in charge. Several people in charge are not tested in this beta.
- It needs Python 3.9 or newer, and `git` installed — on Subversion too, today.
  It needs no server or account of its own.

## Try it

--8<-- "how-it-works.en.md"

## Read on

- [Set up in ten minutes](setup.md)
- [Your answer is your commit](signing.md)
- [Your word in TRIAGE.md](triage.md)
- [The standup](standup.md)
