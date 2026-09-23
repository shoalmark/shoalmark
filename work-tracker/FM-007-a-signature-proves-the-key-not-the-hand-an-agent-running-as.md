---
id: FM-007
status: Proposed
considered: FM-005, FM-006
tags: security
tier: P2
next: owner
ask: "Which closure for the signing doorway do you want first, knowing that the first two are enforcement and the third only a tripwire?"
ask-kind: ruling
ask-since: 2026-09-22
ask-options: "a hardware key that needs a touch | a signing key on a machine no agent runs on | a hook that refuses a signed commit carrying a seat co-author line"
ask-proposal: "a hardware key that needs a touch"
answer: "accepted - a hardware key that needs a touch"
answered: 2026-09-22
answered-by: holgo99
triaged: 2026-09-23
rank: 2
hook: "The gate accepts an answer only from a commit signed by the Owner's key. But a signature proves which key was used, not which hand: an agent running as the Owner on his machine, with his key loaded, signs as him — and with commit.gpgsign true set, every agent commit did, until it was caught. Nothing in git, the forge or the tool can tell the difference. Named by the Owner: a doorway for any rogue agent."
---

# FM-007 — A signature proves the key, not the hand — an agent running as the Owner on his machine signs as him

## What is true now

**Named 2026-09-22 by the Owner, the day the answer scheme went live.** The scheme (0.15.0): an `answer:` counts only from
a commit that verifies under a key the repository's signers file ties to the Owner's email. That refuses a forged author
string. It does not refuse **the Owner's own machine used by someone else**: an agent started from his shell holds his
`user.signingkey`; with `commit.gpgsign true` it signs *everything* as him, and with signing off it can still pass
`-S` itself. The tool saw this happen once — a seat's commit was about to carry the Owner's signature — and caught it
by discipline, not by a check. **Subversion has no such doorway** for the same reason it never needed signing: the
server authenticates the session, not the file.

**Closed today, by the Owner's hand:** `commit.gpgsign` unset on his machine; he signs answers on demand with `-S`. The
documentation says so. That is a habit, not an enforcement.

**Three closures, in strength order:**

1. **A hardware key that needs a touch** (FIDO2 SSH key `sk-ssh-ed25519`, or a GPG key on a token): the agent can invoke
   the key, and the commit waits for a finger that is not there. Real enforcement, one purchase, ten minutes.
2. **The signing key on a machine no agent runs on** — the Owner answers from a device agents never see. Real
   enforcement; the answer flow stays a click, a paste and a commit, because the board opens the forge editor.
3. **A tripwire in the tool:** the pre-commit hook refuses a signed commit whose message carries a seat's co-author
   line, and the gate refuses an answer whose commit's *committer* differs from its *signer*. Catches the accident and
   the lazy forgery; a rogue agent that strips the line and sets both names walks through. Cheap, and in every
   repository via `--install-hook`.

The honest order is 1 or 2 for the Owner, and 3 in the tool regardless — it costs nothing and it caught tonight's case.

## Done when

The Owner's answers are signed by something an agent on his machine cannot operate (1 or 2, recorded here with what
was chosen), the tripwire (3) is in the tool with a mutation witness, and the signing page says all three.

## Ship log

| Date | Event |
|---|---|
| 2026-09-22 | Filed from the Owner's finding; `commit.gpgsign` unset the same day, on his word. |
