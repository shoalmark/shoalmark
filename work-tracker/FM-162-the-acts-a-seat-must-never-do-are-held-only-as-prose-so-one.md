---
id: FM-162
status: Proposed
considered: FM-019, FM-024, FM-028, FM-031, FM-037, FM-062, FM-078, FM-104, FM-119, FM-121, FM-125
tags: process
epic: FM-139
next: owner
hook: "Five acts a seat must never do are held only as prose: removing files instead of moving them to the Trash, killing processes by name, bypassing hooks, reading or writing in the person's own checkout, and fetching into another seat's repository. One slips through now and then and is caught after the fact. The proposal, put to the Owner as FM-162-Q2: the tool ships a seat guard that refuses each act before it runs, through each harness's own hooks installed in its administrator layer, where a seat cannot change them, and names the rule and a safe alternative."
ask-id: FM-162-Q2
ask: "Do you take FM-162's decisions as proposed: the five acts refused in their plain forms, the person's checkouts listed in ~/.config/shoalmark/, the guard on by default for seats and installed in each harness's administrator layer, a critical review, and the lane in v0.20.3?"
ask-kind: ruling
ask-since: 2026-11-13
ask-options: "yes, as proposed | yes, with the changes I name | no, not now"
ask-proposal: "yes, as proposed"
---

# FM-162 — the acts a seat must never do are held only as prose, so one slips through now and then and is caught after the fact

Seat: the Planner (27f31560) · filed 2026-11-12, on the Auditor's word of that day.

## What is true now

**2026-11-13 — FM-162-Q1 withdrawn with no answer given, and FM-162-Q2 put,** on the Auditor's word of that day.
Decision 6 is added: the guard is installed in each harness's administrator layer, not in project settings a seat
can change. Decision 3 and the limits follow it. The other decisions are unchanged.

**Filed 2026-11-12, Proposed for v0.20.3, with FM-162-Q1 put; nothing is built.** It is a chapter of
[FM-139](FM-139-v0-20-3-s-rows-sit-in-fm-023-fm-006-and-fm-053-so-no-one.md), v0.20.3's epic, until the Owner
decides whether it goes in.

- **The five acts, and where each rule stands today.** Each is written as prose: in this repository's documents where
  shown, else in the seats' briefs and notes. Nothing refuses any of them before it runs.
  1. **Removing files instead of moving them to the Trash:** briefs and notes. A loss is found when the file is missed.
  2. **Killing processes by name** (`pkill`, `killall`): briefs and notes. A name can match another session's processes.
  3. **Bypassing hooks** (`--no-verify`): [README L239](https://github.com/shoalmark/shoalmark/blob/7c93c835d6ac9842bb28a37118822f4a6b8a661b/README.md#L239)
     and the stand-up prompt's line 6.2
     ([`shoalmark.py` L5222](https://github.com/shoalmark/shoalmark/blob/7c93c835d6ac9842bb28a37118822f4a6b8a661b/shoalmark.py#L5222)).
     `--check` catches the commit afterwards
     ([README L509](https://github.com/shoalmark/shoalmark/blob/7c93c835d6ac9842bb28a37118822f4a6b8a661b/README.md#L509)).
  4. **Reading or writing in the person's own checkout:**
     [AGENTS.md L102–L103](https://github.com/shoalmark/shoalmark/blob/7c93c835d6ac9842bb28a37118822f4a6b8a661b/AGENTS.md#L102-L103)
     (FM-031). The stand-up prompt's step 0 reads there by design, and allows only `--standup` and read-only git
     ([`shoalmark.py` L5214](https://github.com/shoalmark/shoalmark/blob/7c93c835d6ac9842bb28a37118822f4a6b8a661b/shoalmark.py#L5214)).
  5. **Fetching into another seat's repository:** briefs and notes.
- **What each harness offers, as its own pages say:**
  - **Claude Code** ([its hooks page](https://code.claude.com/docs/en/hooks)): a `PreToolUse` hook runs "Before a
    tool call executes. Can block it". It blocks by exiting 2, its stderr the message, or by JSON with
    `"permissionDecision": "deny"` and a reason, which it shows to Claude. Its input carries the session id, the
    working folder, the tool's name and its input. Project settings, `.claude/settings.json`, can be committed.
  - **Codex** ([its hooks page](https://developers.openai.com/codex/hooks)): "PreToolUse can intercept Bash, file
    edits performed through `apply_patch`, MCP tool calls, and other local function tools", and blocks the same two
    ways. The project's hooks sit in `<repo>/.codex/hooks.json` or `.codex/config.toml`, and "Project-local hooks
    load only when the project `.codex/` layer is trusted." The page adds: "Treat tool hooks as a useful guardrail,
    not a complete enforcement boundary." Its [rules page](https://developers.openai.com/codex/rules) adds
    `prefix_rule` with the decision `forbidden`, in `<repo>/.codex/rules/`: it matches a command's argument list,
    applies to commands run outside the sandbox, and is marked experimental.
- **Where a seat is set up:** the seat's worktree, in the one step that writes its keys
  ([README L412](https://github.com/shoalmark/shoalmark/blob/7c93c835d6ac9842bb28a37118822f4a6b8a661b/README.md#L412);
  [docs/setup.md L74](https://github.com/shoalmark/shoalmark/blob/7c93c835d6ac9842bb28a37118822f4a6b8a661b/docs/setup.md#L74),
  "Sessions"). A seat's worktree carries `seat.session`; the person's own sessions carry none.

## Why

A rule held only as prose holds while every agent remembers it, as [FM-119](FM-119-five-rules-held-only-as-prose-are-not-checks.md)
says of its five. These five are single acts: one can lose a file, stop another session, or reach the person's own
checkout, and nothing caught afterwards undoes it. Refused before it runs, with the rule's name and a safe
alternative, the slip becomes a corrected command.

## Decisions, for the Owner

The ask, FM-162-Q2, asks for all of these at once. An answer of "yes, with the changes I name" names each change by
its number.

1. **The guard refuses the five acts in their plain forms,** and each refusal names the rule and a safe alternative.
   The design round settles the exact commands; the candidates:
   - **removing:** `rm`, `rmdir`, `unlink`, `find … -delete`, `git clean -f`. Instead: move it to the system's Trash,
     for example `mv <path> ~/.Trash/<folder>`.
   - **killing by name:** `pkill`, `killall`, and `kill` given `pgrep`'s output. Instead: stop a process by the id it
     was started under, or by the harness's own handle for a task it started.
   - **bypassing hooks:** `--no-verify` on `git commit`, `git push` or `git merge`, `-n` on `git commit`, and
     `core.hooksPath` set on the command line. Instead: fix what the hook refused, or put it to the Owner as an ask.
   - **the person's checkout:** a tool call whose working folder or any path it names lies in a checkout the person
     has listed. Every write is refused there, git's fetch, pull and switch among them. Reads are allowed only as the
     stand-up's step 0 allows them, `--standup` and read-only git, and the person can refuse reads too. Instead: the
     seat's own worktree, `git fetch && git switch --detach origin/<branch>`, as AGENTS.md says.
   - **another seat's repository:** `git fetch` or `git pull` run in, or pointed at with `-C`, a worktree whose
     `seat.session` is not the running seat's own. Instead: fetch in your own worktree, or ask that seat.
2. **The person's checkouts are listed in `~/.config/shoalmark/`,** where the tool already reads the person's own
   labels and logo
   ([README L662](https://github.com/shoalmark/shoalmark/blob/7c93c835d6ac9842bb28a37118822f4a6b8a661b/README.md#L662)),
   in a file of their own. They are never read from a committed file, and the guard never prints them: a refusal
   says "a checkout the person has listed" and names the file. If
   [FM-104](FM-104-the-person-s-own-files-are-spread-over-the-repository-and.md)'s layout moves the person's own
   files, this file moves with them.
3. **On by default for seats.**
   - The hook entries are installed where decision 6 says. The worktree step names them, and `--whoami` says
     whether they are in place.
   - The guard acts only for a seat. A session with no `seat.session` passes, so the person's own sessions run as
     before. The design round settles how each harness tells the guard where the session started, so that a seat
     that changes folder is still a seat.
   - This guard's design round joins
     [FM-121](FM-121-a-seat-can-change-the-seat-definitions-and-the-skills-folder.md)'s, which guards the seat
     definitions and the skills folder the same way.
4. **The review is critical:** the guard decides what a seat may run.
5. **The lane is in v0.20.3,** after FM-121's design round.
6. **Where the guard lives: each harness's administrator layer.**
   - The entries are installed in the settings a harness takes from the machine's administrator, which a seat
     cannot edit and no other layer can widen. They are never in project settings, which a seat can change.
   - The person installs them, as the machine's administrator. The tool prints the entries and where each
     harness reads them, and writes nothing there itself.
   - The layer applies to every session on the machine. The guard still acts only for a seat, so the person's own
     sessions run as before (decision 3).
   - Where a harness has no such layer, or its layer cannot hold the entries, the guard is not installed for it.
     That harness is named under the limits below.

**The limits, stated plainly.**
- **A harness with no administrator layer.** The design round checks each harness's administrator layer and names
  here each one that has none, or whose layer cannot hold the entries. A seat on such a harness runs unguarded.
- **Plain forms only.** A command built at run time, an alias, a script that removes files, another language's file
  calls, or a shell started inside the shell is not seen.
- **What each hook sees.** Codex's page names Bash, `apply_patch`, MCP and other local function tools, not its own
  file reads, so a read refusal may not reach them. The design round checks which file tools each harness's hook sees.
- **Loading.** `--whoami` reports whether the entries are in place, not whether a harness loaded them.
- **A guardrail, not a complete boundary,** in Codex's own words. Installed by the administrator, the entries are out
  of a seat's reach only while the seat's OS user cannot act as the administrator. `--check` still catches a
  bypassed hook after the fact.

## Done when

Each item names its commit or pull request when it lands.

- [ ] **The Owner has answered the ask,** FM-162-Q2.
- [ ] **The design round** settles the exact commands, which file tools each harness's hook sees, and how a session
  is known as a seat, with FM-121's design round.
- [ ] **The guard** reads a tool call from either harness's hook input and refuses each act's plain forms, naming
  the rule and a safe alternative. A class test for each act, each with a mutant the tests kill; a test that a
  session with no `seat.session` passes; and a test that a seat which changes into a listed checkout is refused.
- [ ] **The person's checkouts** are read only from `~/.config/shoalmark/`: a test shows a committed list is ignored
  and that no refusal prints a path, run with a scratch home.
- [ ] **The entries** are installed in each harness's administrator layer, as the setup page says. The worktree step
  names them, `--whoami` reports them, and a test pins the entries the tool prints. Each harness without such a layer is named under the
  limits.
- [ ] **README, `docs/setup.md` and `docs/de/setup.md`** describe the guard and its limits, and their pair check
  passes. `CHANGELOG.md` has its entry.
- [ ] **The critical review is READY.**

## Asks

**FM-162-Q1** · 2026-11-13 · Do you take FM-162's decisions as proposed: the five acts refused in their plain forms, the person's checkouts listed in ~/.config/shoalmark/, the guard on by default in seat worktrees, a critical review, and the lane in v0.20.3?
**withdrawn** — no answer was given

## Ship log

| Date | Event |
|---|---|
| 2026-11-13 | FM-162-Q1 withdrawn with no answer given; FM-162-Q2 put, with decision 6 added: the guard is installed in each harness's administrator layer, and a harness without one is named as a limit. Records only. |
| 2026-11-12 | Filed, Proposed for v0.20.3, with FM-162-Q1 put: a seat guard refuses five acts before they run. Records only. |
