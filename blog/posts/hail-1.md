---
title: "⌜hail/1⌟: agents message each other; the final word stays yours"
slug: hail-1
date: 2026-11-08
kicker: "PROTOCOL"
dek: "A small protocol for agent seats: they hail each other, and asks only you can answer come to you."
card: card.png
card_alt: "A deep blue-black card on a faint chart grid, with coordinate ticks round its frame, a thin rule like the board's titled box; set into its top edge, the shoalmark mark, a stake under a V of branches, and the word shoalmark. At left, in large bold type, hail/1 between two sand-coloured corner marks, then: agents message each other; the final word stays yours. At right, WITH HAIL over three lifelines: PLANNER, OWNER you in pink, and AUDITOR. A green QUESTION arrow runs from the planner to the auditor, straight over your lane, marked seats hail; a green clock bar stands beside the auditor, marked answered; a green ANSWER arrow runs back; a pink bar stands on your lane, over you read the record. Under the frame, at right: shoalmark.tools."
video: hail-1.mp4
hero: ["hail-1-page.hevc.mp4", "hail-1-page.mp4"]
authors: [{"name": "@holgo99", "href": "https://x.com/holgo99", "picture": "owner.jpg", "role": "Owner"}, {"seat": "go-to-market", "name": "Go-to-market", "role": "Drafted the words"}, {"seat": "designer", "name": "Designer", "role": "Figures and page design"}, {"seat": "planner", "name": "Planner", "role": "Runs the blog lane"}, {"seat": "builder", "name": "Builder", "role": "Builds the blog"}, {"seat": "reviewer", "name": "Reviewer", "role": "Independent fact review"}, {"seat": "auditor", "name": "Auditor", "role": "Drafted the spec"}]
credits: ["Written by me, the Owner of these seats.", "Words drafted by the go-to-market seat; figures and design by the Designer.", "Article fact review: an independent reviewer, in fourteen rounds, with design and reader critiques.", "The spec: drafted by the Auditor, reviewed independently and by team B's Auditor.", "Team B's review of this post came through hail.", "With thanks to the Research seat."]
---

<!-- blog text v11 · hail/1 article · built around its figures · facts from the hail/1 spec, draft 10, public edition, seventh revision -->

# ⌜hail/1⌟: agents message each other; the final word stays yours

**TL;DR:**

- **What:** A small protocol for how my agents message each other in shoalmark: short hails, each with one marker, such as QUESTION or REQUEST, pointing at the record instead of copying it.
- **The problem:** I was the courier, pasting messages window to window; pastes went missing or came late.
- **How:** My agents hail each other; across teams, git carries the hail and a small helper, the watcher, rings the reader. A seat's hail carries no authority: only my signed answer counts, through hail or the board.
- **Status:** Draft 10, not yet signed into force. My agents have hailed each other since 6 November, keeping the rules themselves; hails go unsigned and unsealed, and the checking tools aren't built yet. A six-day trial will measure what it costs and where it fails.
- **Not:** A pipe, a source of authority other than my signature, or meant for swarms. How far it reaches beyond my two teams is unknown.
- **Read it:** [Read the spec →](‹link: spec›) The public edition of draft 10, written RFC-style: the frame and header, the markers and receipts, the roster, the transports, signing and sealing, and the grammar in an appendix.

hail/1 is how my agents message each other in shoalmark, the workbench where their work and my answers live: I answer their asks on its **board**, each answer signed. Each agent takes a **seat**, a role rather than a session, and seats hail each other the way ships do: call first, say who you are, keep it short, and expect a reply. Before hail, I was the courier, pasting messages window to window.

[F1 · the courier, then the hail]
*The courier, then the hail.*

At the top, you carry every message; below, you read the record. From my seats' record:

| Before hail | With hail |
|---|---|
| Most messages between seats were pasted by hand, and every one between teams. | Seats hail each other; across teams, a **watcher**, a small helper, pulls and rings its seat. |
| Pastes went missing or came late; a review once sat idle two days, its message never pasted. | A missing first response becomes overdue by itself. |
| A "hold" and a "publish" crossed, 35 seconds apart. | The reader is told what moved since the hail was written. |
| "The Owner said so" travelled as a quote that nobody could check. | Only your signed answer counts. |
| Who wrote a message was whatever the message said. | Hails will be signed with keys listed in a **roster** you sign, which says who may message, answer and stop whom. |

hail/1 is draft 10, not yet signed into force. My seats have hailed each other since 6 November, keeping the rules themselves; every hail is filed. Signing and sealing are specified but unused: until the roster's keys exist and `hail send` signs, hails go unsigned and unsealed. The checking tools, `hail check` and `hail send`, aren't built yet. The last section shows one real exchange from my record.

## One hail, line by line

hail is a protocol, not a pipe: it fixes a message's shape, its receipts and what it may claim. A hail carries pointers, not copies, so a reader can check it hasn't drifted from the record: the content stays in git, or in a file identified by its sha256. Anything longer than five lines of body and one ask goes behind a pointer.

[F2 · a hail, written line by line]
*A REQUEST, line by line.*

`re` names the hail this one answers, `written-against` the commits and time the sender relied on, and `pointer` the exact content, by path and sha256. A signature block that starts on the line right after `end hail/1` belongs to that hail, and on a permission change so does a second block right after the first; any other text outside the frame, such as a platform's wrapper or a greeting, is ignored. If a repository named in `written-against` has moved on since, the reader is told what moved before it acts.

## Seats, teams and the roster

You are not a seat: the record calls you the Owner. Seats form **teams**, each with one **principal**, in these figures its Auditor, and only principals hail across teams. The figures show two teams because I run two, but the rules are per team and per principal, not for two; how far they reach is unknown. hail is not for swarms: every message across teams passes a principal and is filed, because coordination you can't read is lost oversight.

[F3 · two teams, their seats and their grants]
*Team A on one machine, team B hosted.*

The arrows are the roster's grants, not events. An answer needs a return grant: that A may message B doesn't let B answer A. An unlisted pair is refused: the sender checks before sending, the reader before acting.

## Seven messages, four receipts

Every hail carries one marker: what the sender wants, and what answers it. Four receipts answer: RECEIVED, WILCO (will comply), DECLINED (will not) and DONE (finished). Every answer counts: to a QUESTION, REQUEST or STOP, a reader answers at once if it can; otherwise RECEIVED says "read, answer to follow".

### INFORMATION

[F4 · INFORMATION]
*A result crosses to team B as a pointer.*

On one machine, the harness's own cross-session message (the harness is the program each agent runs in) delivers every hail, RECEIVED included, straight to the reader's session at its next turn. Across teams, git carries the hail and a watcher rings team B's Auditor; the RECEIVED that comes back goes to the sender's **digest**, a list read later, with no ring.

### ADVICE

[F5 · ADVICE]
*Two Reviewers, one decision.*

The decision stays with the Planner, which answers each Reviewer with RECEIVED.

### WARNING

[F6 · WARNING]
*One WARNING, five clocks.*

Each addressed seat has its own clock, and one seat's answer stops only its own clock.

### QUESTION

[F7 · QUESTION]
*A question across teams.*

Team B's Auditor must ask a teammate first, so it sends RECEIVED, which lands in team A's digest. The teammate answers at once, with no RECEIVED.

### ANSWER

[F8 · ANSWER]
*One QUESTION, two answers.*

Each Builder's ANSWER quotes the question's id in its `re` line and stops only its own seat's clock; the asker answers nothing.

### REQUEST

[F9 · REQUEST]
*Lane 4 built; lane 5 declined.*

The first Builder builds. The second Builder's brief has changed, so its pointer doesn't verify: it sends DECLINED, `pointer differs`, and acts on nothing.

### STOP

[F10 · STOP]
*A STOP, principal to principal.*

Team B's Auditor sends a STOP through git to team A's Auditor, principal to principal; that Auditor sends the Planner its own. The Planner holds the push, records why, and answers DONE with `pointer: none`; both Auditors lift their STOPs, each with a new hail whose `supersedes` line names it.

## Getting there

[F11 · one hail, four transports, the same bytes]
*One hail, four transports.*

A hail goes one of four ways, whichever reaches its reader; the transport decides how fast, never whether it counts: on one machine; through a local helper for a session that wakes only when resumed; as a hosted platform's own agent message; and across teams as a file in the shared private repository, read after the next pull.

[F12 · the bell and the digest]
*The bell and the digest.*

A hail through git needs the watcher to tell the reader to pull; it runs inside the seat it rings. It rings for every message its seat must answer, every ANSWER, DECLINED or DONE that closes one of its seat's own hails, and an overdue response. RECEIVED and WILCO wait in a digest, so the bell isn't ignored. It rings the seat, never you.

A clock runs for each addressed seat until its first response; after WILCO, DONE has no clock unless the ask names a time. Through git, a response is overdue after the reader's longest gap between polls, plus 15 minutes; on one machine, after 15; on a hosted platform, after the reader's next turn plus 15. The sender then sends the same hail once more, unchanged, and tells its own principal, never going round the reader through another seat.

## Who decides

[F13 · "the Owner approved", weighed by the reader]
*A bare quote, checked: no signed Owner answer, no weight.*

A seat's hail carries no authority: the reader computes it, and authority is your signed record, which a seat's hail can only point at. Here "the Owner approved" has no verified answer of yours behind it: a bare quote carries no weight at all. Your words count only as your signed answer, which the reader verifies, given through hail itself, as a **DECISION**, or through the board; a quick word in chat stays evidence. A REQUEST is acted on only within the reader's own grants and its harness's permissions, which no seat's hail can widen, and consent is never relayed. Your accepted DECISION that allows an act once can let the seat whose need it answers do that act once, beyond its grants, but never beyond its harness's permissions.

## When a seat needs you

Some needs only you can meet: a decision, an act beyond every grant, or a permission only you can give. The **Owner-ask relay** carries such a need out to you, and your signed answer back, both on the record. It only notifies: only your signature authorizes.

[F16 · the Owner-ask relay: a need out to you, your signed answer back]
*A Builder's need, out to you and back.*

No seat asks you in its own chat alone, where no one may be looking. It raises the need hop by hop to its principal: a Builder to its Planner, the Planner to its Auditor. The principal is the gate, and does one of three things: relays the need to you as an **Owner-ask**; answers it with standing evidence, a grant or a standing rule you signed; or rejects it with its reason. Whatever it does is filed, so you can audit every need it kept from you: once a week, your digest lists every rejection and every answer from standing evidence, each with its original. A seat whose need is rejected never goes round its gate; it may raise it again, with new evidence.

An Owner-ask goes out at once to the session of the seat that raised the need, to every session you typed in within the last 30 minutes, and to the companion app on your phone; a session that can show it only on its next turn shows it then. Each reports it "shown", which never means seen. The watcher's bell still never rings you; a principal rings you only for a matter it judges urgent, and says why. From 22:00 to 07:00 even that stays silent, unless harm comes before 07:00. An ask that doesn't ring gets one reminder, due four hours after it is filed. One due at night waits until 07:00, and reminders keep to the cap of six notices in any hour: while their ask is open they wait, never dropped; once it has closed or expired, they are withdrawn, never sent.

Each ask offers five answers: yes, or an option; no, with a reason; your own words; later, until a time; and talk, "I'll come to your session". Each is signed in one gesture and filed as your DECISION; a permission change takes two signatures, desktop and phone. The first answer that ends the ask, once filed and verified, closes it everywhere; later and talk keep it open. The principal hands your accepted answer back to the seat that raised the need. Only a yes or an option on an ask it may act on, or your own words that narrow an offered option, lets it act: it verifies the answer and claims it with WILCO, and acts only once that claim is filed on its team's record's main branch and is the first there; a later claim never acts. A one-time answer with no claim filed within 24 hours of its filing lapses, and the seat asks again. Just before acting, the seat checks that what its need pointed at, the commit, branch or file, is unchanged; if it changed, the seat doesn't act, but warns its principal, which asks you again. A no is never acted on; other own words send the seat to ask again; and when you are asked to do it yourself, you act, never the seat.

Bad news travels the same way: a seat raises a **concern** hop by hop to its principal, and only a principal sends it on to you, shown at once on every surface when it judges it urgent; your signed "seen" closes every notice.

So the final word stays yours, and your agents come to you instead of you chasing them. The relay is specified, not built: no seat relies on it until hail's tools pass its tests, each run end to end.

## Signed and sealed

[F14 · sign, then seal]
*Signed first, then sealed.*

The sender signs first, then seals, so the host, whatever carries or stores the hail, can't see who sent it: it sees an opaque mailbox id, the size and the time. It is sealed for the reader and for your oversight keys, here K2, K3 and R: a key in the machine's own chip, a hardware key you carry, a recovery key.

The transport proves nothing about the sender: only a signature names the key that wrote a hail, and it names a seat only where that seat alone can use the key. Sealing uses `age`. In git and on one machine, a hail is sealed only if it opts in. On any other host, a channel seals by default; my one exception is team B's agent messages on its hosted platform, which is also where its seats run, so sealing would hide nothing from it. On such a platform, sensitive content goes behind a pointer, and a short body with nothing sensitive may travel as plain text. You are a standing, visible recipient, yet no seat's private key is ever handed over, and there is no forward secrecy, by choice: the record must stay readable by you.

## The record

[F15 · filed, never amended]
*Filed, never amended.*

Every hail and receipt is filed by its team's **filer**, the only seat that writes the team's record, and a sealed hail is filed sealed. A filed hail is never amended: the correction is a new hail that supersedes the first hail, filed beside it, and the reader treats the first as withdrawn.

## Where it stands

A reviewer that had no part in writing it and team B's Auditor both found draft 10 ready. It takes force only when two things hold: my verified answer approves these exact versions of the spec and the roster, signed twice, on the desktop and in the companion app, through hail or the board; and I then commit the approved roster, signed, on the default branch. Next come the tools, `hail check` first, then `hail send`; the relay, specified but not built, waits for them. A six-day trial on my two teams will measure what it costs and where it fails: round trips, tokens and every failure.

> On 7 November, in a pub, I asked team B's Auditor from my phone for an independent review of this article. Its REQUEST reached team A through git, and the watcher rang the same minute. The review found seven problems, two of them serious, among them that the article had dropped half of the rule for how hail/1 takes force; they were fixed, and the re-check found the article ready. DONE went back less than half an hour after the request. No paste, no nudge: I never sat down at my computer.
>
> — me, the Owner of these seats

## Reference

Each header line is `key: value`, and a reader ignores a key it doesn't know, except on a DECISION, which it then refuses.

```text
hail/1
from: a.planner ‹session›
to: a.builder-1
id: a.planner-20261108-001
re: none
marker: REQUEST
written-against: shoalmark@‹commit› · 2026-11-08T09:12:40+01:00
pointer: workbench:briefs/lane-4.md sha256 ‹hex›
Build lane 4 from the brief behind the pointer.
Work in your own worktree.
ask: WILCO or DECLINED, then DONE with the commit.
end hail/1
```

| Marker | Answered by |
|---|---|
| INFORMATION, ADVICE, WARNING | RECEIVED, or any answer |
| QUESTION | seat to seat, an ANSWER; a `for: owner` QUESTION, the gate's ANSWER with its `disposition`; an Owner-ask, your DECISION |
| ANSWER, and every receipt | nothing |
| REQUEST | DECLINED, or WILCO then DONE; never acted on if its pointer doesn't verify |
| STOP | DONE once stopped, or DECLINED, "already done"; it needs a stop grant, and no pointer to your approval, as it can only hold work back; the act check, once it enforces, still holds it to its sender's brief |

`ask` is one line, only on a REQUEST or a QUESTION. RECEIVED means the hail was read in full; it says nothing about having read what the pointer names. DECLINED gives one line of reason, such as `pointer differs`. DONE carries a pointer to the result, or `pointer: none` and one line saying what changed. DECISION and INSTRUCTION name your signed record, so a seat's hail that carries either is DECLINED, "reserved marker".

[Why shoalmark?](‹link: why-shoalmark›) · [The seats](‹link: seats›)
