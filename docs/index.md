# shoalmark

*A mark on the chart that keeps the fleet off the shoal.*

| To the fleet | To the owner |
|---|---|
| **How to get a better-performing human owner.** | **Your agents are faster than you. Good. Now stop being the queue.** |

Agents do not wait for tools. They wait for their human. Mid-task they need a decision, they ask mid-flight, and the
owner stamps what he had no time to read. shoalmark collects those questions and puts them to him once a day. Every
answer is his own signed commit.

## Both claims, measured

In one project that runs shoalmark, in two days:

- **0 → 17 of 21** pull requests carried an independent review file before they were opened.
- **1 command, 1 signed commit** per question to the owner.
- **The board says which review was independent**, and which came from the same session as the code it judged.

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
| **Your project's agents** | the [note for trying it](https://github.com/holgo99/shoalmark/blob/main/ADOPT.de.md) (German): a measurement, not an instruction. They report to you at the end, and you decide |
| **An agent at work** | the contract is `tools/shoalmark/README.md` in your repository, [rendered here](agents/README.md). `llms.txt` is at this site's root |
