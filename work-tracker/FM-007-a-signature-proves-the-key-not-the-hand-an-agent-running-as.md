---
id: FM-007
status: In Progress
considered: FM-005, FM-006
tags: security
tier: P1
next: owner
triaged: 2026-09-25
ask: "Which day this week do you set up the hardware key that needs a touch — your answer of 09-22 — so that the key signing your answers stops being a software key in the shared agent?"
ask-kind: action
ask-since: 2026-09-25
ask-options: "today, 2026-09-25, after the sitting | 2026-09-26 | 2026-09-27 or later, before the week's scoring on 09-29"
ask-proposal: "today, 2026-09-25, after the sitting"
answer: "accepted - after the scoring, once the key is delivered."
answered: 2026-09-25
answered-by: holgo99
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

*Filed word for word by the Principal seat from the Owner's paste of 2026-09-25 07:59:21, on his word (*file this into documentation*). sha256 of the section below as filed, from its heading to its last line: 36afa8150b311725418d832994b9b9765e414f547e4ddc185af85d0816768ecb (with one trailing newline); the Auditor seat stated `846ba2bb…` for its own copy and matches it against its record — no seat reads that record.*

## Tiers — what an answer's signature proves (the Auditor seat, session 8b91dba2, 2026-09-25, on the Owner's word)

The threat this tracker names: a process running as the Owner, on his machine, signs as him. A signature proves the key, not the hand. A tier counts only by what the agent cannot do or cannot know.

| Tier | Setup | Stops an agent signing as the Owner? | Confidence |
|---|---|---|---|
| 0 | A software SSH key whose passphrase the Keychain holds (UseKeychain, AddKeysToAgent), or none at all | No. It is unlocked at login, and every process on the account signs silently. It protects the key file only. | 95% |
| 1 | A software key held in the agent with a per-use confirmation (ssh-add -c) | Partly. A reflex click signs, and macOS needs an askpass helper that it does not ship. | 75% |
| 2 | A separate signing key whose passphrase is typed by hand at each signature and never stored or cached (not in the Keychain, not in the agent) | Against accidents, yes (the commit.gpgsign case, a seat's commit carrying his signature). Against a malicious agent, no: code running as him can fake the prompt or wrap ssh-keygen. | 80% |
| 3 | A FIDO2 hardware key with Ed25519, touch and PIN (ed25519-sk, -O verify-required), with a second key as backup | Yes, for both. The private key never leaves the device, and each signature needs his touch and PIN. | 90% |

What each tier requires:
- Tier 2: its own key, used only to sign, never the push key.
- Tier 3: a key sold as FIDO2/CTAP2 with Ed25519 (EdDSA), a PIN set, and two keys registered.
- Tier 3 on macOS: Apple's bundled OpenSSH cannot enrol a security key. Probed on macOS 26.6 with OpenSSH 10.3p1: ssh-keygen -t ed25519-sk answers "No FIDO SecurityKeyProvider specified". A build with libfido2 (Homebrew's openssh) and gpg.ssh.program pointing at it are required.
- Every tier above 0: the old key is retired as a signer. Its line leaves allowed_signers, and it is removed as a Signing key on the forge. Otherwise any process still signs with it and verifies.

What the tool should say: the tier, not a bare "verified". allowed_signers shows the key type (sk-… is a hardware key), so the board and the answer's record can state "signed with a software key — anything on the owner's account can produce it" or "signed with a hardware key — needs the owner's touch". A trial user starts at tier 0 or 2 with an honest record. Tier 3 is the visible step up.

The site contradicts this today: docs/signing.md (and docs/de/signing.md), Route A: "The same key may sign; it proves the same thing either way" recommends tier 0 on a machine agents use. Its risk section says "An agent never passes -S", but FM-007's own text records that an agent can pass -S itself.

The Owner's own state, 2026-09-25: tier 0 (S1). FM-007 was answered "after the scoring, once the key is delivered". Until then his signed answers prove "a process on his account", and FM-032's review pass stays in force.

*Addendum, filed word for word from the Owner's paste of 2026-09-25 08:13:57 (*paste it after the main block, so FM-007 and the site get both*); sha256 of the addendum as filed, with one trailing newline: 438890dcf1575d86c0d8061fce9d7edf4a50dc2b5c2190ccce21bde59d0ab49d; the Auditor seat stated `ea32e5d4…` for its copy and matches it against its own record.*

Tiers, addendum (the Auditor seat, session 8b91dba2, 2026-09-25): a phone passkey, and the Mac's Secure Enclave.
- A passkey on a phone: not an option for signing today (70%). OpenSSH signs through libfido2 over USB/NFC and cannot reach a phone's passkey, which is made for website sign-in. If it could, it would rank below tier 3, because synced passkeys live on every device of the account instead of one.
- Tier 3 without buying, on a Mac with a Secure Enclave and Touch ID (Apple Silicon, or Intel with a T2; the Owner's MacBookPro16,1 has both): a signing key generated inside the Secure Enclave, with Touch ID at each signature (e.g. the open-source Secretive agent) (75%). The key cannot be exported. Each signature needs his finger, and each use is announced.
  - Limits: P-256 ECDSA only, which the forge accepts. Bound to one Mac, so a second signer must be registered.
  - The tool cannot tell it from a software ECDSA key by its type, so the tier must be declared beside the key in allowed_signers.
  - Verify that no approval is cached between signatures.

*The site conversion — the Auditor seat's five points for `docs/signing.md` and `docs/de/signing.md`, the second block of the Owner's paste of 2026-09-25 07:59:21, filed word for word (the Reviewer's R2); sha256 as filed, with one trailing newline: 07c31fa5e2fa7b7ac5c3b41847123cba7235c24e9f0ad2603ef6370496d191d5.*

2. The site conversion: what docs/signing.md and docs/de/signing.md must say · 85%. The wording is the GtM seat's job, which is legibility to a stranger. The content:
1. Open with the threat and the four tiers in plain words, before any setup steps.
2. Rewrite Route A. Drop "the same key may sign; it proves the same thing". Replace it with: a separate signing key. Tier 2 becomes the easy route and tier 3 the strong route. Tier 0 is labelled "for trying the tool; your record will say so".
3. A tier 3 walk-through: what to buy (FIDO2, Ed25519, PIN, two keys), the macOS OpenSSH note, adding both keys as GitHub Signing Keys, allowed_signers, and retiring the old key.
4. Correct "an agent never passes -S". Say instead that an agent can pass it, and that only tier 2 or 3 stops that.
5. Nothing of your own setup on a public page: no fingerprints, no configs.

## Raised

*One sourced line per raise — the date, who raised it, the fact, its source, what it undermines; no counts. The Auditor seat's
proposal of 2026-09-24 (its draft, sha256 `39690e54…`), applied under the freeze as a line, not a command.*

- 2026-09-24 · Auditor (8b91dba2), through the Owner · the key that signs the Owner's answers (ED25519 SHA256:uNcUULP20UyJ7Iyv3xImxOrg9cXTcRqIxbWsekBYzCQ, 65f37a4, 7dd6ba6) is a software key in the shared ssh-agent, used by every seat push without a prompt — ssh-add -l, ~/.ssh/config (AddKeysToAgent, UseKeychain) · undermines: TRIAGE.md path 5, FM-033's answer

## Done when

The Owner's answers are signed by something an agent on his machine cannot operate (1 or 2, recorded here with what
was chosen), the tripwire (3) is in the tool with a mutation witness, and the signing page says all three.

## Asks

**2026-09-22** · Which closure for the signing doorway do you want first, knowing that the first two are enforcement and the third only a tripwire?
**answered** — accepted - a hardware key that needs a touch · holgo99
**relation** — accepted the proposal

## Ship log

| Date | Event |
|---|---|
| 2026-09-25 | The Reviewer's R4 on PR 69, fixed forward: the filed *site conversion* block begins at *2.* because the Owner's paste did — the numbering is the paste's, and the board renders the five points after it as 3–7; the text stays word for word. |
| 2026-09-25 | The Auditor seat's five points for the site conversion filed word for word (the Reviewer's R2 on this branch: the record named them as the GtM seat's and listed three); main merged after PR 68 (the Reviewer's R1: INDEX.md conflicted, regenerated). |
| 2026-09-25 | The site's signing pages rewritten by the GtM seat under this tracker (`56d08bb` English, `007f279` German): the threat and the four tiers first, Route A a separate signing key, tier 3 walked through — two FIDO2 keys, or the Mac's Secure Enclave — a phone passkey ruled out, *an agent can pass -S* corrected, the old key retired last. Two lines under the freeze for 0.18.4, found by that seat: the tool's link to the page (`…/signing/`, and `…/de/signing/` in the German labels) will 404 on the deployed site, which builds `signing.html` (`use_directory_urls = false`); and the tier of a Secure Enclave key cannot be read from its type, so the pages declare it as a comment line above the key in `allowed_signers` (`# tier 3: …`) — the tool's coming tier line reads that form or the pages change. |
| 2026-09-25 | **Tiers, addendum** filed word for word (the Owner's paste of 08:13:57): a phone passkey is no signing option today; a Mac's Secure Enclave with Touch ID gives a tier 3 without buying — P-256 only, bound to one Mac, the tier declared beside the key in `allowed_signers`. The site pages take both blocks. |
| 2026-09-25 | In Progress — the seat's work under this tracker is the record and the site's signing pages (the tiers), set here in a tracker-only commit before the first documentation commit (the FM-033 rule); the key itself stays his act, after the scoring. |
| 2026-09-25 | **The tiers of a signature** filed word for word from the Auditor seat's text, through the Owner (paste 07:59:21): four tiers, what each stops, what each requires, what the tool should say, and where the site contradicts it today. The site pages `docs/signing.md` and `docs/de/signing.md` are rewritten under this tracker on his word (the GtM seat, its five points). |
| 2026-09-25 | A line under the freeze for 0.18.4, this tracker's: the tool says the tier, not a bare *verified* — from the key type in `allowed_signers` (`sk-…` is a hardware key) the board and the answer's record say *signed with a software key — anything on the owner's account can produce it* or *signed with a hardware key — needs the owner's touch*. |
| 2026-09-25 | His answer of 07:29:54 (`1034602`, PR 67, one Reviewer docs pass): *accepted - after the scoring, once the key is delivered.* — changed text, no day this week: the key comes after 09-29 once delivered; until then the software key signs (tier 0) and FM-032's docs pass on every answer pull request stays in force. Not yet cleared: the act is his and open. |
| 2026-09-25 | The day of the key asked on the board, kind action: his answer of 09-22 stands in the record as his promise and the act is open; the ask slot held that exchange, so the board and `--owner` showed him nothing to answer and FM-007 sat under *backlog* — found by him at the sitting of 09-25 (07:00:34); the parent project's ledger row (row 43) came first. |
| 2026-09-24 | Correcting the Reason of the evening worksheet row: whether a hand that was not his has ever signed is not shown by the record either way — the tier P1 rests on path 5 being undermined, not on that; and rank #2 behind #1 is a judgement of order, not of whether an owner move is work (it is). |
| 2026-09-24 | **Raised** by the Auditor seat through the Owner, the line above word for word from its draft; the day of the hardware key put to him in the parent project's ledger (kind B, before the sitting of 09-25). Rank #2 stands; the act is his. |
| 2026-09-22 | Filed from the Owner's finding; `commit.gpgsign` unset the same day, on his word. |
