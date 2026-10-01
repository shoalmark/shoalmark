# Your word in TRIAGE.md

*For the owner. Five minutes to read. You write it once, in your own words, and your agents do the rest.*

Your agents can run a task from start to finish without asking you, if they know two things first: what the work is
for, and what comes first. You write both once, in one file, `TRIAGE.md`: three lines and a short numbered list. Your
agents run `--init`, which writes the file with an example in it (*the tool*). Every pass judges its trackers against
your words (*review*), and **only your signed word changes them** (*the tool*, up to a limit whose strength you
choose). You don't repeat yourself in chat: the tool prints your words for your agents. All of it is below.

## What holds each claim

Every claim on this page is labelled with what holds it:

| Label | What it means |
|---|---|
| **The tool** | shoalmark checks it: it prints the text, or it refuses the commit. |
| **Review** | a Reviewer checks it against the record before a merge. Nothing refuses it on its own. |
| **The text alone** | a written rule. Seats keep it because it is written down, and nothing checks it. |

## What the file holds

`TRIAGE.md` sits in the tracker directory (`docs/work-tracker/` unless you chose another). It has three sections, and
two of them are yours.

- **The intent — *for · so that · never*.** Three lines about the repository as a whole, never one feature of it:
  what it is for, what is true when it works, and what no pass or seat may do to get there.
- **The current path.** A numbered list of what comes first and the rules the work runs by. A pass judges the
  trackers on its sheet against it (*review*; which trackers, below).
- **Passes.** One paragraph per triage pass, written by the seat that ran it. This section belongs to your agents.

**A first draft: the village library.** `--init` writes an example in italics, and it is a whole product on purpose.
The owner's own first draft once came out the size of one feature, after a seat had shown them a feature-sized example
(FM-022). So the example looks like this:

> - **for** — *e.g. a village library's lending, all of it: members, loans, returns and the shelf in one record the librarian trusts*
> - **so that** — *e.g. a member finds a book and a librarian finds a member in one look, and nothing on loan is lost*
> - **never** — *e.g. lend what the catalogue does not hold, or drop a member's record before their last loan is back*

Write over it in your own words.

- **The tool.** A pass reads everything you write there. It leaves out only the lead-in and the examples as they stand,
  so an untouched example reads as *no intent written*.

## What an edit changes

Once your commit is in, your agents see the new words at their next command, printed by *the tool* as the first two
points below say. You don't need a meeting or a message.

- **The tool.** `--next`, where a session starts, prints your current path before the ranked work. `INDEX.md` carries it
  word for word near its top, and your board shows it below what waits for you.
- **The tool.** `--triage` prints your intent above its rules: *"Where the mechanics below leave you a choice, this
  decides it"*. It prints your path below them: *"THE CURRENT PATH is the Owner's, printed below — judge against it."*
  With no path written, it refuses to start: *"tiers cannot be judged; the Owner writes it first."*
- **The tool.** A pass does not re-judge everything, and nothing in the tool reacts to a change in your path by
  itself. A pass's sheet lists work in progress that no pass has judged in the last seven days (`triage_days`), new
  filings, and raised trackers (next point). Work already judged that is not in progress (proposed, parked or reserved)
  stays in the backlog with its tier. So a tracker judged this week keeps its tier until its next pass, unless a raise
  names a line of your path.
- **Review.** The trackers on the sheet are judged against your new words, as the pass's rules say: *"P1 on the
  current path · P2 next · P3 someday."* The tool writes the verdicts; whether they follow your words is what the
  pass's Reviewer checks.
- **The tool.** A *raise* is a seat's sourced line under a tracker, and it can name a line of your path as undermined
  (`path 5`). A raise dated after the tracker's last judgement that names a line your path has puts the tracker back
  on the triage sheet, marked RAISED, however fresh its tier. This raise check is the one place the tool reads what
  your path contains, and it reads only the numbers: it collects the numbers of your path's lines and matches the
  raise's `path N` against them, never what a line says. The two other checks on your path look only at whether one
  is written (`--triage` and `--next`, above) and whether its bytes changed (the guard, below).

### From shoalmark's own record

**Path line 3, rewritten.** On 25 September 2026 at 10:37, the owner rewrote line 3 in their own signed commit
(`fe36cc0`, `%G?` G), which also reworded lines 1, 2 and 5 and added line 6. Line 3 before:

> 3\. A pull request without an independent review's evidence file cannot merge - checked, not asked.

After:

> 3\. A pull request merges only with a review's evidence file on its head: a Reviewer from another independent
> session for critical changes (critical = a release, the gate or hooks, signing and rights, TRIAGE.md or AGENTS.md
> rules changed by a seat, anything tagged security or P1); inline Reviewer passes on other code; one Reviewer pass
> for documentation; a review of the Owner's own answers and TRIAGE lines reports and never blocks, until FM-007's
> hardware key signs them. The Owner merges on a ready line, or over any other verdict with a signed reason.

- **Review.** The same day, the seats sorted their work by the new line. The pass that took in the CI fix wrote
  *"the Owner's line 3 names a release critical, so its fix's review is the cold session's"* (`42f4eca`). FM-037, the
  guard described below, was reviewed in two other sessions before it merged, and `--check` lists both verdicts as
  *independent*.
- **The tool.** `--check` prints how independent the week's reviews were. At `88c7b0c` on 26 September 2026 it
  printed `reviews this week · 104 verdict(s) · independent 10 · same session 89 · untraced 5`. That is a report,
  not a gate: most of that week's verdicts came from the same session as the work, and nothing refuses a same-session
  verdict yet (FM-024's second slice is not built). The line shows you what you are merging.

**One phrase decides a tier.** CI went red on the release tag `v0.18.3` on 25 September 2026. The first pass
(`42f4eca`, 12:15) kept FM-035 at P1: *"a red release tag on two of three platforms is a failed command on the
current path, line 1"*. Its Reviewer found the quotation cut short. Line 1 in full reads: *"The daily sitting runs on
a tagged release with a signed answer and no failed command in the sitting."* The pass was re-made (`c8939e3`, 12:30)
and judged P2: *"the sitting's commands ran green here, so a red CI is not that command"*.

- **Review.** Three words, *in the sitting*, moved the tier. No check acts on what your words say, so the Reviewer
  holds the pass to them. If a red release tag should be P1 for you, write that into your path. It's your line.

**A raise that names your path.** On 24 September 2026 the Auditor seat raised FM-007 with a sourced line under it.
The key that signs the owner's answers was a software key in the shared ssh-agent, used by every seat's push without
a prompt, and the line ended *"undermines: TRIAGE.md path 5, FM-033's answer"*: it named two signed rules, line 5
of the path and the owner's signed answer on FM-033. The same evening a pass judged FM-007 again
(`29466fc`). Re-made on its Reviewer's findings (`c5696c5`), it set P1: *"on the current path, line 5: an answer is
written and signed, and the raise shows the signature proves the account, not the hand"*.

- **The text alone,** for *the same day*: that is the owner's rule, their signed answer on FM-033, and a pass keeps it
  by running.
- **The tool,** since 0.18.3: a raise that names a line your path has puts the tracker under *triage* until a pass
  has judged it again. On 24 September the tool couldn't list a raised tracker yet, so the seat wrote the row by hand.
- **Review.** The reason for the new tier is the seat's own; its Reviewer checks that reason against your line.

## Only you change it

- **The tool.** On a branch, `--check` refuses any commit that changes the text under *The intent* or *The current
  path*: a word, a line, even a blank line, because whitespace counts. It also refuses a commit that renames or
  removes those headings, deletes or moves `TRIAGE.md`, or points the tracker directory somewhere else. The one
  exception is your signed commit: `%G?` G, the signer the author's email, and the author you, as `owner` in the
  default branch's configuration names you — or a seat that `[rights]` there gives `answer`. A merge is judged only on a
  text that no parent had.
- **The tool.** The commit hook refuses such a commit from a seat before it is made, and `--queue` reads its pull
  request as `wait: TRIAGE.md changed unsigned`.
- **The tool.** The keys your signature is checked against are kept the same way. They come from the default
  branch's signers file, never a branch's own copy, so a branch that adds its own key under your email proves nothing.
- **The tool.** *Passes* stays open to the seats that record a pass.

**Shown.** We ran this in a scratch repository with the tool from shoalmark's `main` (`88c7b0c`). The repository had
the village library as its intent, two path lines, an invented owner with their key, and a seat. Nothing of it left the
scratch directory. On its own branch, the seat changed path line 2 from *"A pull request merges only with a review's
evidence file on its head."* to *"A pull request merges when its tests pass."* `--check` on that branch exited 4, and
these are the refusal's lines as the tool printed them (the script and its whole output are in
[FM-006's evidence](https://github.com/shoalmark/shoalmark/tree/main/work-tracker/evidence/FM-006/triage-page)):

```text
  lint: refused: commit 1063448 "LIB-001: path line 2, shorter" changes the text under `## The current path` in docs/work-tracker/TRIAGE.md — its author `implementer@seat` is not the Owner (`you@example.org`): not the Owner's signed commit — only the Owner changes his intent and his current path (FM-037). The way through: the Owner commits it signed; a seat proposes the change as an ask — `ask:` in its tracker, one sentence he can answer, with `ask-kind: ruling`, `ask-since:` and `next: owner`
  the limit: a commit signed with the Owner's key passes; at tier 0 any process on his account holds that key (FM-007)
FAILED: 1 ledger-integrity violation(s) — fix the tracker; regenerating will not clear these.
```

With the hooks installed (`--install-hook`), a seat's change to the intent was not made at all: the hook printed the
same refusal for *this commit*, and before the limit it added *"the hook proves the author only: git signs a commit
after its hooks have run — `--check` on the branch is the gate, and it judges the signature"*.

**The way through is yours.** A seat that wants a line changed asks you, in the form the refusal names (*the tool*):
an `ask:` in its tracker, `ask-kind: ruling`. You answer on your board. If you agree, you make the edit yourself:
edit the file, `git commit -S`, push. `git log -1 --format='%G? %GS %ae'` then prints `G` and your email twice. That
is the check on [the signing page](signing.md).

**The limit,** in the words the tool prints after every refusal: *a commit signed with the Owner's key passes; at tier 0 any
process on their account holds that key (FM-007)*.

- **The tool** cannot tell the difference. At tier 0, *only you* means *only your account*. In the scratch
  repository, a commit made with the owner's key, which had no passphrase, passed `--check` exactly like their own. A
  passphrase at every signature (tier 2) stops a stray signature, but an agent that means harm can fake the prompt and
  catch it. As [the signing page](signing.md) says: *Tier 2 stops the agent that signs by mistake; tier 3 also stops
  the one that means to.* Tier 3 is a hardware key with a PIN and a touch, or a key in a Mac's Secure Enclave with
  Touch ID; only there is the key yours alone.
- **The tool.** Where your `owner`, or a seat that holds `answer`, is not marked `signed`, the guard proves the author
  only, a string anyone can type, and it says so.
- **The tool.** Under Subversion the guard is out of scope, and it says so in one line: a working copy carries no
  signature.

## What an edit does not do

- **It changes no check.** The gate's refusals, `--queue`'s reading of a pull request, the filing freeze and each
  seat's rights come from the tool's code and `shoalmark.toml`. Path line 3 asks for a review's evidence file, and
  `--queue` asks for a verdict on the head because its code does. Deleting line 3 wouldn't change that. *The tool:*
  no check reads what your lines say; the raise check reads their numbers (above).
- **It moves no tier and no rank by itself.** A tracker's tier moves only when the tracker is on a pass's sheet and
  the command applies its row: work in progress not judged in the last seven days, a new filing, or a tracker whose
  raise names a line of your path (*the tool*). The pass's rules say a raised tracker is judged again the same day
  (FM-033's rule); that it is, is *the text alone*. Every other tracker keeps its tier until its next pass, and your
  board shows the old judgement until then. *The tool* refuses a tier or a rank from a seat that lacks the `triage`
  right; that no seat edits them by hand is *the text alone*.
- **It answers no question.** An ask on your board is answered by `--answer`, signed (*the tool*). An edit to
  `TRIAGE.md` answers nothing, and neither does a merge or a click. That no seat reads one as your answer is a line
  of the path (shoalmark's own line 5), and that is *the text alone*: the tool cannot stop a seat from reading a click
  as your word.
- **It doesn't reach a branch cut before it.** *The tool* reads the file in the checkout it runs in. A seat on an
  older branch reads your old lines until its branch takes in your commit.
- **It doesn't rewrite a past pass.** Each pass was judged against the words of its day. *The tool* writes each new
  pass to a worksheet of its own day, so an earlier one stays as it was, and git keeps your old text.
