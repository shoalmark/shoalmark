# Review — FM-007's tiers and the site's signing pages, at b38d321 (2026-09-25 08:47 CEST, Reviewer, session `8e509911/reviewer-7`)

- **Branch:** `fm/007-the-tiers-of-a-signature-and-the-site`, tip `b38d321` (`b38d321d306d71bb1f2f990c5c7c17f75bee2a40`).
  Six commits on `6e98d73` (PR 67's merge, 07:36:53). The fork point is **not** `origin/main` `7f492a5`: PR 68 landed
  there at 08:05:26, after the branch's first two commits, and the branch has not taken it in (R1).
  - `a2015e5` 08:01:53, principal: the *Tiers* section filed, the 07:29:54 row, the 0.18.4 tier line.
  - `eaf617c` 08:02:14, principal: `status: In Progress`, INDEX.
  - `c97332d` 08:15:00, principal: the addendum filed.
  - `56d08bb` 08:18:13, GtM (`8e509911/gtm-1`): `docs/signing.md`.
  - `007f279` 08:21:40, GtM: `docs/de/signing.md`.
  - `b38d321` 08:23:39, principal: the site pages' ship-log row and two 0.18.4 lines.
- **Tier: docs, one pass.** `git diff --name-only origin/main...HEAD` names four paths: `docs/de/signing.md`,
  `docs/signing.md`, FM-007 and `INDEX.md`. There is no `shoalmark.py`, no test, no configuration and no hook. No
  front-matter key changes meaning, and neither `shoalmark.toml` nor `zensical.toml` is touched. A finding below P2 is
  fixed forward; a P2 sends the branch back.
- **The FM-033 order holds.** Two commits touch files outside `work-tracker/`: `56d08bb` and `007f279`. At each one's
  parent, FM-007 reads `status: In Progress`, `triaged: 2026-09-24`, `tier: P1`, `rank: 2`. `eaf617c` set In Progress
  at 08:02:14, before `c97332d` and `56d08bb`. `status:` is the seat's key (`--schema`).
- **Independence:** this seat is a sub-agent of `8e509911`, the session of every commit on the branch (the principal
  `8e509911`, the GtM seat `8e509911/gtm-1`). `--check` will count this verdict as *same session*. Reported, not refused.

## What I ran

| run | result |
|---|---|
| the Principal's transcript: a Python filter on the `user` records stamped `2026-09-25T05:59:21` and `2026-09-25T06:13:57`, nothing else read | two records, both string content: `05:59:21.045Z`, the main block in its first `<pasted_content>` with the five site points in its second; `06:13:57.684Z`, the addendum |
| the two blocks against FM-007 at the tip, as bytes | main block 2955 bytes, identical; addendum 1068 bytes, identical; no CR, no trailing blanks |
| `sha256` of each filed block with one trailing newline | `36afa8150b311725418d832994b9b9765e414f547e4ddc185af85d0816768ecb` and `438890dcf1575d86c0d8061fce9d7edf4a50dc2b5c2190ccce21bde59d0ab49d`, the values FM-007 states |
| `grep` of both pages for fingerprints, the machine model, the probe's versions, session ids, the Owner's name, address and paths, other repositories | nothing |
| a structural diff of the English and German pages | 14 headings each, in the same order; 9 code blocks each; 13 table rows each; the same three link targets |
| `curl -sI` on every external link on both pages | all four answer 200: `man.openbsd.org/ssh-keygen.1`, `github.com/maxgoedjen/secretive`, GitHub's steps in `en` and in `de` |
| `uvx zensical build` in a scratchpad clone at `b38d321` | exit 0, *No issues found*; `scripts/llms_txt.py site` exit 0, 9 pages. The site has `signing.html` and `de/signing.html`, and no `signing/` directory |
| Apple's `ssh-keygen -t ed25519-sk -O verify-required` on this machine | *No FIDO SecurityKeyProvider specified*, then *Key enrollment failed: invalid format* on the next line; exit 255; no file written |
| Homebrew's formula (`homebrew-core` `Formula/o/openssh.rb`) and OpenSSH's 8.4 release notes | `depends_on "libfido2"` and `--with-security-key-builtin`; 8.4 (2020-09-27): *FIDO keys that require a PIN for each use … a new "verify-required" option* |
| a scratchpad clone with throwaway keys and a scratch signers file | ed25519 signer present: `G`; its line removed: `U`, with an empty `%GS`. A P-256 ECDSA signer with `# tier 3: Secure Enclave, Touch ID at each signature` on the line above it: `G` |
| `python3 shoalmark.py --check` | exit 0; *INDEX.md is up to date — 34 trackers*; *67 verdict(s)*; *filing freeze: 18 open* |
| `python3 shoalmark.py --session-check` | exit 0 |
| `python3 shoalmark.py` | 34 trackers; `git status --short` empty after it |
| `test_shoalmark.py`, `test_core.py` | exit 0, 355 ok and 148 ok, all green, on Python 3.14.3 and 3.9.6 |
| `git merge-tree --write-tree origin/main HEAD` | **exit 1: CONFLICT (content) in `work-tracker/INDEX.md`**, and in no other file (R1) |
| replay: the scratchpad clone at `b38d321`, `7f492a5` merged, `python3 shoalmark.py`, signers file set | INDEX then differs from main's by FM-007's two rows alone; `--check` exit 0 |

## The checks

**1. The *Tiers* section and its addendum are the Owner's pastes, word for word — ✓; confidence high (99%).**
- The main block runs from `## Tiers — what an answer's signature proves …` to *… FM-032's review pass stays in force.*
  It equals the first `<pasted_content>` of the 05:59:21Z record, byte for byte.
- The addendum runs from *Tiers, addendum (the Auditor seat …* to *  - Verify that no approval is cached between
  signatures.* It equals the 06:13:57Z record from *Tiers, addendum* to its last line, byte for byte.
- Both hashes, with one trailing newline, are the ones FM-007 states: `36afa815…6768ecb` and `438890dc…0ab49d`.
- The Auditor seat's prefixes, `846ba2bb…` and `ea32e5d4…`, come from none of the seven forms I hashed. Those forms
  were raw, with one or two newlines, CRLF, stripped, and without the heading. FM-007 keeps the two values apart and
  leaves the match to the Auditor's record. The filed text is the paste. The paste has no backticks around its code
  words, so it may be a rendered copy of the Auditor's text. That is not verified, and it is not this branch's to settle.

**2. The pages carry the five points and the addendum's two — ✓; confidence high (95%).** FM-007's body does not
record the five points (R2). I checked the pages against the 05:59:21Z record's second block, the Auditor seat's
*2. The site conversion … 85%*.
- **Open with the threat and the four tiers, before any setup.** *First, what a signature proves* comes before any
  command: the threat, the table and *Where you are*. Only the introduction and the Subversion line come before it.
- **Route A rewritten.** *The same key may sign; it proves the same thing* is gone from both pages. So is the German
  *Derselbe Schlüssel darf signieren*. The route is now *a separate signing key*, never the push key. Tier 2 is *the
  easy route* and tier 3 *the strong route*. Tier 0 reads *for trying the tool — your record will say so* twice:
  under *Which to choose*, and as Route A's *Only trying the tool?*
- **Tier 3 walked through.** What to buy: FIDO2 (CTAP2), Ed25519 (EdDSA), a PIN on each, two keys. The macOS OpenSSH
  note, with Homebrew and `gpg.ssh.program`. *Both signers* in the signers file and on the forge as a Signing Key.
  The old key retired as step 4.
- **`-S` corrected.** *An agent can pass `-S` itself. Only tier 2 or 3 stops that.* *Ein Agent übergibt nie `-S`* is
  gone from the German page.
- **Nothing of the Owner's setup.** See check 3.
- **The addendum.** The phone passkey is ruled out, with the reason (libfido2 over USB or NFC) and the ranking had it
  worked (a synced passkey is on every device). The Secure Enclave is tier 3 without buying, on Apple silicon or an
  Intel Mac with a T2 and Touch ID. Its limits are there: P-256 only and accepted by the forge; bound to one Mac, so a
  second signer; the tier declared beside the key; no approval cached between signatures.

**3. Nothing of the Owner's setup — ✓; confidence high (95%).**
- The pages carry no fingerprint, no config line of his, no hostname and no machine model. The addendum's model
  appears only in FM-007.
- They carry no session id, and neither the macOS nor the OpenSSH version of the Auditor's probe.
- They carry nothing from another repository that this branch added. `AP-007` and the `docs/work-tracker/` path are
  on `main` in unchanged lines.
- `~/.ssh/signing_ed25519` is a generic name, not the key file this repository's configuration names.
- `IgnoreUnknown UseKeychain` is general advice: any config that says `UseKeychain` stops Homebrew's `ssh`. It quotes
  no config of his.

**4. The German page says what the English says, in the site's register — ✓; confidence high (90%).**
- **The same structure.** The same sections in the same order, the same tiers, table and *Wo Sie stehen*, and the
  same two routes.
- **The same warnings.** The passkey, `IgnoreUnknown`, the cached approval, the order of the retire step, and *Tier 3:
  both* on the forge.
- **The code blocks** differ only by the example address (`sie@`), one comment and the test message.
- **The register.** *Sie* throughout, with no *du*. *Eigner*, *Tafel* and *Arbeitspaket* are used as in
  `de/index.md` and `de/setup.md`. The tool's messages stay English, as the refusal table had them. GitHub's steps
  link to its German documentation, and the two English targets are marked *(englisch)*.
- **Two differences are older than this branch,** and these commits leave them unchanged. *A seat that edits this
  file* reads *Ein Agent, der diese Datei ändert*. The branch-case parenthesis is worded differently.

**5. Links, the build, and the tool's link — ✓; confidence high (90%) on the 404.**
- All four external links answer 200. The manual has the *FIDO authenticator* section the page names
  (`id="FIDO_AUTHENTICATOR"`).
- `zensical build` exits 0 with *No issues found*.
- With `use_directory_urls = false`, the build writes `signing.html` and `de/signing.html`, and nothing at
  `signing/`. Two links point at `signing/`:
  - `SIGNING_PAGE` (`shoalmark.py:51`, `…/shoalmark/signing/`);
  - the German label `answer.sign.url` (`examples/de/labels.yaml:129`, `…/de/signing/`, pinned again at
    `test_shoalmark.py:977`).
- So both will 404 once the site deploys. The site is not deployed today: every URL under it answers 404, the root
  included. The 404 is therefore read from the build, not seen live.
- FM-007's top ship-log row records it for 0.18.4, with the German labels.

**6. The pages' claims about tools — ✓ as far as software checks reach; confidence high (85%).**
- **Homebrew's openssh is built with libfido2:** the formula shows it.
- **`verify-required` since 8.4:** the release notes say so. *Every signature asks for the PIN, not only the touch*
  is what they describe.
- **Apple's error text:** reproduced on this machine. Both lines appear, in the page's order. So *the invalid format
  on the next line* is exact.
- **Removing a signer's line turns `%G?` to `U`:** reproduced. The gate's `verified_as` (`shoalmark.py:2943`)
  requires `G`, and the answer rule (`:3680`) re-verifies every `answer:` still in a tracker. So an open answer the
  old key signed fails the gate once its line is gone. That is why step 4 must clear answers first (R3 is on its
  wording).
- **The pages' comment-line form for the Secure Enclave tier:** it verifies. The manual reads lines starting with `#`
  as comments.
- **Secretive:** its README says the key sits in the Secure Enclave and cannot be exported, that Touch ID or the Watch
  can be required per access, and that every access is notified. Its FAQ says 256-bit EC keys only, and names
  `SSH_AUTH_SOCK`.
- **Not checkable without hardware:** a FIDO2 enrolment, a Touch ID prompt per signature, and the forge accepting a
  P-256 or `sk-` signing key (not tried).

**7. Gates — ✓ except merge-tree (R1); confidence high.**
- `--check` exits 0, and INDEX is up to date. `--session-check` exits 0.
- The generator is clean.
- Both suites are green on two Pythons.
- `merge-tree` against `origin/main` conflicts in `INDEX.md`.

**8. The ship-log rows' times are sourced — ✓; confidence high.**
- *07:59:21* is the record's 05:59:21Z plus two hours. *08:13:57* is 06:13:57Z plus two hours.
- *07:29:54* is `1034602`'s author and committer time, merged as PR 67 (`6e98d73`, 07:36:53).
- The rows cite `56d08bb` and `007f279`, and those are the page commits.
- *In Progress … before the first documentation commit* is true: 08:02:14, then 08:18:13.
- *07:00:34* is in an older row, not this branch's. No `≈` appears in any added line.

## Findings

**R1 · P2 · confidence high on the fact, 80% on the grade · The branch does not merge with `main`: `INDEX.md`
conflicts.**
- **The fact.** The branch forks at `6e98d73` (PR 67). PR 68 (`7f492a5`, 08:05:26) moved FM-030 to #3 and took FM-018's
  rank. The rows it changed sit next to the FM-007 rows this branch changes, in the triage table and in the bucket
  list. `git merge-tree --write-tree origin/main HEAD` exits 1 on `work-tracker/INDEX.md` and on no other file. Main's
  other paths (FM-018, FM-030, TRIAGE.md, a review, a worksheet) are not touched here.
- **Why P2.** It cannot be fixed forward. The Owner cannot land this pull request by merging until the branch carries
  `main`. The only other way through is GitHub's conflict editor, which means a hand edit of a generated file (rule 7).
- **The fix is mechanical.** Replayed in the scratchpad: merge `origin/main`, then `python3 shoalmark.py`. INDEX then
  differs from main's by FM-007's two rows alone, and `--check` exits 0.
- **Fix:** merge `origin/main` into the branch and regenerate INDEX. That merge takes one pass, as `7a1bbc2` did.

**R2 · P3 · confidence high · The five points the pages answer to are not in FM-007's record.**
- **Where they are.** They are the Auditor seat's, in the same paste of 07:59:21 (its second block, *2. The site
  conversion … 85%*). FM-007 files only the first block.
- **What the record says instead.** The ship-log row names them only as *(the GtM seat, its five points)*, and *its*
  reads as the GtM seat's. The site-pages row lists what was done but not two of the five: *tier 0 labelled for
  trying* (it is in `56d08bb`'s message) and *nothing of your own setup*.
- **Why it matters.** The tracker is canonical (rule 1), and the spec the pages were held to lives only in the
  Principal's transcript. The next reader cannot check the pages against it from the record.
- **Fix forward:** file the five points, word for word or as a complete list, with their source time. Attribute them
  to the Auditor seat.

**R3 · P3 · confidence medium (70%) · The retire step asks the agents to clear the old key's answers, and
`--clear-ask` says *acted on*.**
- **What the step says.** Step 4 on both pages: *First have your agents clear the answers it signed (`--clear-ask`)*.
- **The precondition is right** (check 6). But `--clear-ask` records the answer as acted on, and an answer not yet
  acted on cannot honestly be cleared.
- **This repository now.** Four open answers are signed by the Owner's current key: FM-007 `1034602`, FM-024
  `64f843e`, FM-032 `97fa87a` and FM-033 `9e48ee8`. FM-007's act is the key itself, so clearing it with the key is
  honest. For the others, it depends on whether they have been acted on.
- **Fix forward, both pages:** *retire it once no answer it signed is still open — `--answered` lists them, and your
  agents clear each as they act on it*.

## Verdict — NOT READY (R1 P2), 85%

**NOT READY.** R1 is the one P2, and it is mechanical: the branch must take `main` in before it can be landed. The
content itself is sound:
- The *Tiers* section and the addendum are the Owner's pastes, byte for byte, under the hashes FM-007 states.
- Both pages carry the five points and the addendum's two.
- The pages say nothing of the Owner's setup, and the German says what the English says.
- The links answer 200, and the build is clean.
- Every tool claim I could check holds.
- The 0.18.4 link line is true and recorded.
- The FM-033 order holds.

R2 and R3 are P3, fixed forward under the docs tier. The pass on the merge that closes R1 need only confirm that
nothing but main's paths and INDEX's regeneration came in.

Not verified:
- The Auditor seat's own record and its prefixes (sealed, and barred by the brief).
- Hardware: a FIDO2 enrolment, Touch ID per signature, and the forge accepting a P-256 or `sk-` signing key.
- The live 404: the site is not deployed.

The Owner lands this by merging; a merge rules nothing.
