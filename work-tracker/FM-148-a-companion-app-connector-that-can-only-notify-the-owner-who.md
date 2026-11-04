---
id: FM-148
status: Proposed
considered: FM-147, FM-007, FM-059, FM-115, FM-054, FM-030, FM-008
tags: process, security
epic: FM-147
next: build
blocked-by: Owner — which keys may sign on mobile
ask-id: FM-148-Q3
ask: "Which keys may sign in the companion app on mobile, weighed against the risks under Decisions, for the Owner, and does the bots' connector stay notify-only?"
ask-kind: ruling
ask-since: 2026-11-04
ask-proposal: "(a) defer to a design round; (b) yes, notify-only"
ask-options: "(a) both, Owner chooses; (b) yes, notify-only | (a) biometric only; (b) yes, notify-only | (a) hardware key only; (b) yes, notify-only | (a) desktop only; (b) yes, notify-only | (a) defer to a design round; (b) yes, notify-only"
answer: "accepted - (a) both, Owner chooses; (b) yes, notify-only"
answered: 2026-11-04
answered-by: holgo99
hook: "A companion connector that can only notify the Owner — list, read, ask, check status — with no tool to answer, sign, merge or change rights; whether, and with which keys, the Owner signs on mobile is the Owner's ruling."
---

# FM-148 — a companion app connector that can only notify the Owner, who signs on their own device

Seat: Planner · filed 2026-11-04 · chapter of FM-147.

## What is true now

**2026-11-04 — filed; nothing is built.** Need: a remote connector that can only **notify** the Owner — list, read, ask and check status — with **no** tool to answer, sign, merge or change rights. Signing stays the Owner's act on their own device; whether that may include the phone, and with which keys, is the open ruling. Held against FM-007 and FM-059 (both Shipped; neither is reopened), FM-115 (Proposed: the Board's one answer dialog), FM-054, FM-030 and FM-008.

**Open ruling (ask FM-148-Q3 above):** one ruling over the two decisions under *Decisions, for the Owner*: which keys may sign in the companion app on mobile, and whether the bots' connector stays notify-only.

**The Owner's direction in chat, 2026-11-03 — logged, not an answer.** The value of mobile is signing, the board and the guided answer together; which keys are enough is the Owner's choice. The risks below are what that choice is weighed against.

**First step (not done in this filing): file the counsel.** The companion-app counsel is held privately; it lands in this tracker's evidence only after a privacy check — no names, no home paths, no private finding.

**Review tier.** The ask concerns signing: this tracker's review is **critical** — the Auditor's START file, an independent Reviewer.

## Why

FM-007 and FM-008 put answering and signing in the Owner's hands. A remote connector that could answer or sign would open a new door to both. A connector that only notifies keeps the signing act on the Owner's device.

## Decisions, for the Owner

FM-148-Q3 asks for both at once. Each option names one choice for (a) with yes to (b); an answer under *Other* names its change by its label, a no to (b) included.

**What the public record already says, before you rule** (`docs/signing.md`, *Tier 3, the strong route*; FM-007, *Tiers, addendum*):

- **A phone passkey cannot sign today.** OpenSSH signs through libfido2 over USB or NFC, and it cannot reach a phone's passkey. If it could, it would still rank below tier 3, because a synced passkey lives on every device of the account, not on one.
- **The Secure Enclave route is a Mac's, not a phone's.** A key made inside a Mac's Secure Enclave, with Touch ID at each signature, reaches tier 3, with limits: P-256 ECDSA only; bound to that one Mac; its type reads like a software key, so its tier is declared beside it in the signers file; and no approval may be cached between signatures — sign twice, and both must ask.
- **Two hardware keys already sign.** `work-tracker/allowed_signers` holds two `sk-ssh-ed25519@openssh.com` keys. A new key counts only once the Owner's signed change to the signers file is merged on the default branch (`docs/signing.md`, *Then, for any tier*, step 2); a branch cannot prove a key the default branch does not hold.
- **Recovery needs a second signer.** A key bound to one device locks the Owner out of answering if that device is lost, unless a second signer is registered (`docs/signing.md`: the backup security key; the Secure Enclave's second signer).

**The proposal, and why.** *Defer to a design round*: no mobile signing route in the record reaches tier 3 today, and any new key needs the Owner's signed change to the signers file first; a design round names each candidate key's tier, its signer and its second signer before keys are chosen. Until then the Owner signs on the desktop, as today.

- **(a) Which keys may sign in the companion app on mobile.** One of:
  - **both, Owner chooses:** a biometric-gated phone key and a hardware security key are both supported; the Owner chooses which to enroll. The phone key carries the first risk above.
  - **biometric only:** a biometric-gated phone key; no hardware security key. Carries the first risk above, and needs a second signer.
  - **hardware key only:** a hardware security key; no biometric-gated phone key.
  - **desktop only:** no signing in the companion app on mobile; the Owner signs on the desktop, as today.
  - **defer to a design round:** no choice now; the keys are chosen after a design round that names each candidate's tier, signer and second signer. The proposal.
- **(b) The bots' connector stays notify-only:** it lists, reads, asks and checks status, with no tool to answer, sign, merge or change rights. Proposed: yes.

Whatever is chosen, a new key counts only after the Owner's signed change to the signers file is merged on the default branch.

## Done when

- The Owner has ruled on FM-148-Q3.
- The counsel has passed the privacy check and is filed under this tracker's evidence.
- A companion connector exists that can list, read, ask and check status, and has no tool to answer, sign, merge or change rights — or a later ruling parks the work.
- Per the ruling, the Owner signs on their own device with the enrolled key or keys, each in the signers file on the default branch, with a second signer registered.

## Ship log

| Date | Event |
|---|---|
| 2026-11-04 | Filed under FM-147 on the Auditor's direction (relayed by the Owner), with ask FM-148-Q3 put as a ruling over *Decisions, for the Owner*; the Owner's chat direction of 2026-11-03 logged, not an answer. Critical review tier. |
