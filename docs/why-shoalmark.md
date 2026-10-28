---
title: Why shoalmark?
description: "shoalmark on one page: a trust layer for AI coding agents, inside your repository. The agents do the work; you have the final word."
template: why.html
---

# Why shoalmark?

**The agents do the work; you have the final word.**

**TL;DR:**

- **What:** shoalmark is a trust layer for AI coding agents, and it lives inside your repository. Your agents keep the work record. You have the final word, recorded as your own commits.
- **The problem:** Agents build faster than you can decide. The bottleneck isn't the agents. It's you, pulled into small decisions in the middle of their work.
- **How:** Their questions wait on the board instead of interrupting you. When it suits you, copy the stand-up prompt: it asks a session to take you through them. Each answer is a commit you can sign.
- **Simple:** One Python file. No server, no database, no account, and nothing that locks you in.
- **Status:** Open source (Apache-2.0 or MIT), in beta, and built with shoalmark itself.
- **Try it:** [Copy the prompt](index.md#top) and let your agent check whether shoalmark fits your project. The prompt asks it to try the setup on a copy, in a throwaway folder outside your repo, and only to read your repo itself, changing nothing in it without your yes. In up to 45 minutes your agent tells you whether shoalmark fits, and "no fit" is an answer too. You decide from there.

## The mark

In the Wadden Sea, a Pricke, a simple birch stake, marks the edge of a channel across the tidal flats. It doesn't steer. The person at the helm still chooses the course. That is the whole idea of shoalmark: let the marks do their work, and keep the course in human hands.

## What I saw

I started with what I measured. In my last repository, **200** pull requests were merged in **22** days, **85 %** of them within a minute of opening, and **none** of them reviewed. Asked separately what slowed them down most, three agents gave the same answer: questions still waiting on their human. One question, open for three days, held up three pieces of work. Speed was never the problem. Small decisions, asked in the middle of the work, were.

> *"On 13 July, I took myself out of the loop: my planner agents got access to gh and took over the orchestration, and the speed-up was unreal. A month later I posted ['Bottleneck removed.'](https://x.com/Holgo99/status/2088153757792043485)*
>
> *But I hadn't removed myself at all. I'd become their message relay, their rubber stamp and their decision engine, and the context-switching was brutal. On 29 September my GitHub showed 9,946 contributions for the year, and I posted ['What a hell of a ride.'](https://x.com/Holgo99/status/2104854591032484007)*
>
> *shoalmark is how I came back in. Since its first commit on 21 September, its agents have made most of its commits, and mine are mostly merges and answers."*
>
> — [@Holgo99](https://x.com/holgo99), I build portdive with shoalmark, and shoalmark with itself

![A pixel-grid calendar of 10,259 GitHub contributions in 2026 on one maker's account, as of 23 October, in shoalmark's night look: quiet from January to early July, a bright band from mid-July to late September, quieter again in October. Three labels: 13 July, "my planner agents get gh. I become their rubber stamp and message relay."; a bracket over the 22 days before 21 September, "200 pull requests in 22 days, none reviewed: the repository shoalmark came from"; and 21 and 24 September, "shoalmark's first commit" and "every pull request gets a reviewer's file". Source: github.com/holgo99.](https://shoalmark.tools/assets/why/contributions-2026-en.png)

## What it's for

I believe your agents should run at full speed and check in with you when it matters, that only your verified word should decide, and that every decision should be readable later, straight from the repository. shoalmark is built for exactly that.

![A mockup of the shoalmark board of a sample repository, notes-app. Under the header, the page says when it was read from main, that it reads its file again when you come back to it, and that nothing polls, beside a button that copies the rebuild command. In the box titled yours, two decisions wait for you, the oldest first: NA-009-Q1, may the sync drop devices unseen for 90 days, which holds up NA-019 and was asked by the research session; and NA-012-Q2, ship the export as CSV only or as CSV and JSON, which holds up NA-014 and was asked by the planner session. Each has accept and reject buttons, and your answers here are signed. Below, your day: a button that copies your stand-up prompt; the three sessions with a commit in the last 24 hours, research and planner in Claude Code and builder in Codex, the two that asked you first, each with a button that copies its resume command; and a button that copies your close-out prompt. Reviews, receipts and your current path are folded.](https://shoalmark.tools/assets/why/board-mockup-dark.png)

*A mockup of the board, from a sample repository: your agents' questions wait at the top, oldest first; below, the session that asked each one, with a button that copies its resume command.*

## Why it's built this way

Trust starts with things you can check. So shoalmark stays small, and stays out of your way:

- **One file.** Python 3.9 or newer. No pip, no server, no database, no account. Your repo keeps a pinned, checksummed copy, and it never updates itself behind your back.
- **Your record.** Plain Markdown, one file per work item, right in your repo. shoalmark never overwrites a file it didn't write.
- **Your word.** One command per answer, recorded as your own commit. A click or a chat message doesn't count.
- **Your stand-up.** The questions wait on the board, oldest first. The stand-up prompt is one click away, whenever it suits you.
- **Written rights.** Each agent takes a seat: a role with its permissions written down. The checks see every permission used, in the diff.
- **Reports, not proofs.** shoalmark is not proof that work is right. That's what a review is for.

## What it holds itself to

I hold shoalmark to its own stated intent, printed at the top of every triage pass in its repository. It names what must never happen: a false pass, a claim without a source, an act you didn't agree to, an agent's word counted as yours.

## Your move

If you build with agents, try it on your own repository. Your agents set it up, and the record stays yours.

Let your agents run. The final word is yours.

[Your agents set it up](index.md#start) · [Set up in ten minutes](setup.md) · [Back to shoalmark](index.md)

Built in the open: [github.com/shoalmark/shoalmark](https://github.com/shoalmark/shoalmark) · Follow me building it on X: [@holgo99](https://x.com/holgo99)
