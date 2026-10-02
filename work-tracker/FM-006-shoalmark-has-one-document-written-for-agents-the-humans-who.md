---
id: FM-006
status: In Progress
considered: FM-005, FM-003
tags: process
next: build
triaged: 2026-09-26
rank: 6
tier: P2
ask: "When and how does shoalmark go public?"
ask-kind: action
ask-since: 2026-09-25
ask-options: "this repository, client names and the parent's traces public, the port evidence deleted — after the scoring, gates held | a snapshot as a new repository, client names and the parent's traces removed, this one the private archive, same gates | not yet"
ask-proposal: "this repository, client names and the parent's traces public, the port evidence deleted — after the scoring, gates held"
answer: "accepted - this repository, client names and the parent's traces public, the port evidence deleted — after the scoring, gates held"
answered: 2026-09-26
answered-by: holgo99
done: "2026-09-30T08:14:56+02:00 · Public repository: https://github.com/shoalmark/shoalmark/ · Documentation: https://shoalmark.github.io/shoalmark/ · Migration merged: 80d0811974a1d39b679cfd374c80109ddd62acce · Independent migration review: 5e26a88e75b992c243148c2786e44f443e0f7437 · Port-evidence cleanup merged: b041cb2dca136623ee9160d74ae5b39b0f1a7ba2 · Publication gates merged and deployed: 792dbca9caa74629d12645dcc5ae7f55a2bb2340 · Independent publication review: b9b3971c21f3b84f332249bbc976fe9af7580f0d · Scoring completed; publication preceded scoring under my previously recorded risk acceptance."
hook: "One README, written for the agent that has to use the tool, is the whole documentation. The people who own the repositories — the first two are German, one runs Windows and Subversion — have no page: not for setting up, not for signing an answer, not for what the first week looks like. And the README must stay the agents' contract, not become a website's copy."
---

# FM-006 — shoalmark has one document, written for agents — the humans who own the repositories have no page of their own

## What is true now

**2026-10-01 — what a stranger meets first in v0.19.0: resumed after FM-005's check merged.** The Owner's ruling is filed
below, in *What a stranger meets first — v0.19.0*, its A amended on 2026-10-01 (the ledes in both languages, one
description, link previews on every page, the preview image, the German start page's title and description), with *The
landing's player stats at the v0.19.0 cut* beside it. The branch `fm/006-what-a-stranger-meets-first`, cut from main
`1197e80` with the two screens it follows, merged main after PR 143. Two Builders — the English texts with the tool's
printed line and the theme override; the German texts with the English note — and the Designer, who builds the landing,
its preview image and the render, start now; D2 goes into the `[seats]` change after the Apps. The slice joins the v0.19.0
release bundle: its full local run and CI come once, on the bundle's tip. Next: the Designer's render to the Owner, the
phone's first screen first; the Reviewer's pass on the slice, English and German.

**2026-09-30 — fork queue hardening, code tier, critical review pending.** Reproduced on `2c00aba`: a fork's
self-declared READY reads as merge; its verdict or carried head also changes another PR's action. The slice excludes
forks from verdict/carry-over calculations and always says `wait: from a fork, read it yourself`. On the base, five
provenance/refusal controls fail and the same-repository merge control passes. Critical review remains due.
Left ([review R3](evidence/reviews/review-fm-006-fork-queue-c2027d2.md), pre-existing): forks can hide same-repository pushed branches by name, containment or a closed pull head; fix `pushed_branches` using open/closed PR provenance in a separate bug slice.

**2026-09-30 — public hardening executed by the Owner after #127 merged.** Tag rules, merge-only policy, repository Actions, CodeQL success and new-public security defaults verified; organisation Actions is browser-reported with the remaining readback limits stated in the [execution receipt](evidence/FM-006/public-hardening-owner-2026-09-30.md#execution-results--2026-09-30-owner-browser-actions). Existing repository protections remain active; the new default is not attached retroactively.

**2026-09-29 — publication review R1:** the independent Reviewer found that the font validator accepted extensionless cross-origin font sources (P2). Replaced filename inference with CSS parsing, with 18 regression scenarios passing on Python 3.9 and 3.14; independent re-verification pending. Fix proof is appended to the [publication evidence](evidence/FM-006/publication-gates-2026-09-29/README.md). Keep this slice unassociated with a PR, or draft, until its READY evidence is included; then run required PR CI.

**2026-09-29 — publication gates follow-through, on the Owner’s instruction:** latest existing tag `v0.18.6` has five green CI jobs; an explicit all-ref history Gitleaks scan reports zero findings with a deleted-secret positive control. The site’s font requests are replaced by local licensed assets, and EN/DE signing pages explicitly disclose the project’s last recorded tier 0. [Evidence and scope](evidence/FM-006/publication-gates-2026-09-29/README.md). Site changes await review, PR CI, merge and deployment; the separate port cleanup remains on `fm/006-remove-port-evidence`. Scoring is due tomorrow on the Owner’s latest word, and the signed publication act remains open. Existing tag CI does not satisfy the original after-scoring timing condition.

**2026-09-29 — independent review R1 (P2), relayed by the Owner:** the rendered README had four broken relative links (AGENTS.md and three licence/notice files), missed by the landing-only destination check. Fixed with public repository URLs and validation of contract destinations, including repository files against the checkout. Fixed in `4c638a8` and independently verified at `910c09f` by Reviewer session `01a0ed68`: **READY, R1 closed**, all four rendered destinations verified, each missing-target control refused on Python 3.9 and 3.14. Evidence: [`review-fm-006-repository-migration-910c09f.md`](evidence/reviews/review-fm-006-repository-migration-910c09f.md). Required CI on the final PR revision and the Owner’s merge remain.

**2026-09-29 — organization migration, on the Owner’s direct instruction.** The repository is public at `shoalmark/shoalmark`; GitHub Pages reports `https://shoalmark.github.io/shoalmark/`. Branch `fm/006-repository-migration` preserves his Zensical commit `d1a269b` unchanged. This slice updates active installation, documentation, signing-help and footer links, keeps historical evidence intact, and makes the Pages build clean without cancelling an active deploy. No version or tag changes. Obsolete: active links to the personal-account home and pre-publication workflow comments. The Owner then explicitly included public-repository hardening: PR triggers for every non-draft revision, a read-only CI token, pinned Zensical 0.0.66, weekly Dependabot configuration, SECURITY/CONTRIBUTING guidance and issue templates. The agents’ HTML contract was found rendering a literal include; snippets are now enabled and landing links target `agents/index.html`. The Pages workflow checks these outputs before upload. Independent critical-code review of `910c09f`, Reviewer session `01a0ed68`: **READY**, R1 closed after fix `4c638a8`; the original NOT READY verdict on `3fe27f3` is preserved at `91ba9f6`. The tracker-named isolated branch passes `--check`, including the preserved Owner commit. Remaining for this slice: green required PR CI, Owner merge and manual Pages deployment from merged main. The tracker’s `next: owner` remains for its standing publication act. Earlier publication prerequisites below remain historical claims, not certified as satisfied by this migration.

**A landing page is a requirement of the v0.18.5 release, alongside the restyle and rebrand of shoalmark's brand identity — the Owner's word in chat, 2026-09-26 10:25:41 (spelling normalised; sha256 `416d54ce…`; not a signed answer): the mock the GtM/Design session filed at `9704140` (PR 82, `evidence/FM-006/landing/`) is its starting point. The seat's reading, marked: the landing page is the site's start page unless he says otherwise; where it ships is decided with the 0.18.5 plan, and its build is judged by a pass before its first build commit (FM-033). The themes' ask moved to FM-002 (raised today on his word) and is answered there (`4e00f85`, PR 90, option 2); this tracker's one ask, *going public*, is answered too (`8defe63`, PR 91, the proposal: after the scoring, gates held), its act not yet recorded. The site is built at a release tag and live only at that act: `.github/workflows/docs.yml` deploys only when `github.event.repository.private == false`, and the repository is private until then — so the Google Fonts item below (IBM Plex, the open item of 2026-09-24; slice L's mock loads Plex Mono and Silkscreen from Google too, `evidence/FM-006/landing/index.html:11`) is due before publication.**

**The themes are filed on the Owner's word (2026-09-25, narrowed 2026-09-26): two, `monochrome` and `shoalmark`, each for the board and the site, each drawing a nautical chart behind the page (muted in `monochrome`); no setting — a theme is a file in a place. Nothing is built. Its drafted ask was re-made on 2026-09-26, on his word through the Auditor seat (AU-24): which theme shoalmark's own board and site wear, and whether the tool ships themes, asked apart, the cheap step first. It moved to FM-002 on 2026-09-26 and is answered there (`4e00f85`, PR 90), as the going-public ask is here (`8defe63`, PR 91); the slices are FM-002's to build, and the line below is the record as filed.**

**A landing page is mocked in the `shoalmark` theme on the Owner's word (2026-09-26), and built as the site's start page — slice L, the GtM seat, on `fm/006-the-landing-page`; merged as PR 95 on 2026-09-27 12:02:39, shipped at v0.18.5:** the mock as-is on his rule of 16:0x (full-bleed, no site chrome, nothing added), `overrides/landing.html` selected by `docs/index.md`, the nav and the other pages unchanged, with the four edits the rule allows — the facts dated (read from main at `bef2a1e`, 18:00 CEST: 24 wrecks, FM-038 added), R4's reports verbatim from each `hook:`, R3's names and figures above the CRT overlay (his to strike; the lowest chart text as drawn 2.65:1 before, 4.80:1 after), the fonts in one load the site's way; the German start page keeps its words and gains one line linking it (`evidence/FM-006/landing/start-page/`). Follow-ups, not built: the page's facts generated at build time (a CI change, critical under path line 3); a German landing page; the fonts self-hosted before publication (the open item above, Silkscreen with Plex); three qualifiers of `docs/index.md` now on no English page — the push-events note under the count, *a report, not a proof*, *every signature names the key* — the Owner's to rule; two west-edge figures under the title at 1440 px, covered by design.

**The page on his word in TRIAGE.md is built, in review — 2026-09-26, the GtM seat, after FM-037's guard merged (PR 83):** `docs/triage.md` and `docs/de/triage.md`, one nav line each, on `fm/006-the-page-on-his-word-in-triage-md-built`; every claim labelled *the tool*, *review* or *the text alone*; the guard's refusal run in scratch repositories (`evidence/FM-006/triage-page/`). A Reviewer checks every claim against evidence before the merge.

**The home at the flip is a GitHub organisation `shoalmark` — the Owner's word of 2026-09-26 through the Auditor seat, as pasted by him at 11:05:27, sha256 `19ca39d1794c67cf15e26399667d392cadc65fdb1c5c5d22fe44993277ad4ec5`; nothing moves before the flip; the line is filed in *Going public*, below.**

**2026-09-29 — port-evidence cleanup, after PR 117 merged.** On the Owner’s instruction, branch `fm/006-remove-port-evidence` removes the six archived files under `work-tracker/evidence/FM-001/port/` from the current tree, based on merged main `80d0811974a1d39b679cfd374c80109ddd62acce`. FM-001 and its exploration report link to that immutable historical tree. History is retained, as the accepted publication option permits. No runtime implementation, active configuration or test is removed. Validation and the six-file manifest: [cleanup evidence](evidence/FM-006/port-evidence-cleanup-2026-09-29.md). Remaining: review, required PR checks and Owner merge; the Owner records the publication act afterwards, once its other prerequisites are accounted for.

**Publication timing, Owner explanation in chat, 2026-09-29:** “yes, my risk accepted decision. My Clients approved going public `fb-sondermasch`, `msr-lager`. We had a potential contributer pitch today - this is why it went public without sticking to the coordinated plan.” This records his explanation and acceptance of the timing risk; it does not rewrite the earlier signed promise or claim deletion before publication. The signed Board act remains the Owner’s next record after cleanup.

**Every page names the tool — 0.18.2, 2026-09-24, on the Owner's word** (*"a micro icon and a tiny wordmark on every shoalmark page, and the version it is running behind it"*, relayed, normalised; then: the name links to the repository, the version to its release): the board and the tracker view end in one muted line, the Pricke at 16 px (its grid allows no smaller sharp size), `shoalmark` in the mono at 11 px, ` · v<VERSION>` — in every repository, whatever its brand.

**The board wears the site's mark — 0.18.2, 2026-09-24:** shoalmark's own board (`work-tracker/brand/`) shows the site's header lockup as one wordmark — the Pricke `d` at the ruled 16 px beside *shoalmark* in IBM Plex Mono 500, the site's proportions — drawn in `currentColor`, so on the dark scheme the mark takes the name's ink (the GtM's finding); its tab is the site's tab icon, its colours the site's light and dark palettes, its type IBM Plex (the ruled family, self-hosted beside the theme — the board fetches nothing from Google, R3's concern), and its tagline the German claim. The tool gained the fourth brand file this needed, `wordmark.svg`, for every consumer. No reader has seen the board.

**The mark's size ruled — 2026-09-24 ≈ 01:40, the Owner, having seen the built header and the lockup at ×1, ×2, ×4: *"the 16 px is the better fitting one. We could only try a 24 px variant but 16 px will do."* — the site wears `d` at 16 px in the header and in the tab, beside the wordmark in IBM Plex Mono; this supersedes the earlier lock of `a` in the header. **Open item, before the site is ever published:** the pages load IBM Plex from Google Fonts (as they did before this slice) — for a German-first site that sends every visitor's IP to Google, which LG München I held unlawful without consent in 2022 (the Reviewer's R3); the fix is to self-host Plex under `docs/assets/fonts/`, its own slice.**

**Ruled 2026-09-23 ≈ 23:35, the Owner, in chat, after the GtM's claim and mark screens:** the German claim is *"Dein Eigner bremst. Tunen statt tauschen."* (the screen's survivor for both readers; applied to `docs/de/index.md` here); the typeface family is **IBM Plex** (sans for the pages, mono for the board — the board's Berkeley Mono is mono-only and commercially licensed; the site change is the next slice); the mark: one survivor of thirteen, **B1, the isolated-danger beacon** (two balls on a stake), held until two or three stand-in readers and one sailor have seen the header and the 16 px tab — never the investor; if they read an *i* first, it dies. The GtM's seven findings on the pitch stand open for the next slice: the adopt note still pins v0.12.0 (P1, first), an internal id on the pitch (P2), the tagline's *on the chart* where the mark stands in the water (P4, the Owner's words), the record-before → reset → record-since frame and *the rule* unexplained (P3, on his *go*), dashes (P5), the last-message line stated as enforced (P6), no dark mode; P7 is closed by the claim above.**

**Ruled 2026-09-23 22:5x, the Owner, in chat: the pitch has two readers — an outside Owner of a fleet (the first two are German, one on Windows and Subversion) and a German tech investor fluent in English, *"indeed one of my audiences I am in contact with"*. Every gate of the claim screen is read for both; where they pull apart, the page says which reader a line is for.** The measured sentence now states its size — *one project, our own, its first day* — until the week's count exists (the GtM's flag, the Principal's edit).

**Filed 2026-09-22 on the Owner's direction:** *"shoalmark has a human- and agent-user facing documentation designed to
the needs of each party."* Ruled the same day, after a trial build: **Zensical** (the successors of Material for MkDocs;
Python, MIT, TOML configuration like the tool's own, no Node, search and dark mode built in; young — 0.0.x) *"because our
product profits from valuing another vendor we seem to align with, early"*; Material for MkDocs is the fallback, and reads
the same configuration.

**The rule that keeps two audiences from drifting apart:** the agents' document is `README.md` — vendored into every
repository, pinned, routed by situation — and it is **never duplicated**: the site renders it as one page and links to it.
Human pages are those with no agent reader: setting up, signing an answer, the standup, the board, the first week. The
site is `docs/`, built by CI to GitHub Pages; `llms.txt` at its root is the agents' index of the same source. German is a
full second language from the first page, because the first two outside owners are German.

**The first human page is the one the day demanded — signing an answer — and it names the risk the Owner found:** a
signature proves which key, not which hand. On a machine agents use, `commit.gpgsign true` makes every agent commit
verify as the Owner. The page says: sign on demand (`-S`), never by default, on such a machine.

**The Owner's requirement for the site, 2026-09-23** (quoted, spelling normalised): *"The site is for humans, so this
one has to be designed like a pitch and sell the idea. Easy, convenient and a one-shot integration mostly done through
your agents."*

**One claim, the Owner's:** the pitch carries *Get a better-performing human Owner.* (DE: *Hol dir einen
leistungsstärkeren menschlichen Eigner.* — in German prose the person is *der Eigner*, on his word), his wording, sharpened from *How to get a better-performing human owner*. It
faces the fleet and provokes the owner at once, and the page below it proves it for both readers. The README keeps its
own section title: it is the agents' contract, not the pitch. A second, owner-facing claim is open for a GtM screen the
Owner convenes; no seat writes it.

### Commit-hook split, 2026-09-29

The Owner encountered the silent full-suite pre-commit hook, approved the proposed local/CI split,
and aborted his pending commit on the seat’s request before this edit. The old hook ran both suites
under `python3` and `/usr/bin/python3`, hid passing output, and reran a failed suite to print it.
The replacement compiles staged Python blobs without executing them and runs `test_core.py` once,
unbuffered. Session, tracker and judgement gates remain; both full suites stay in all five required
CI matrix jobs and tag runs, now unbuffered too. Full local runs remain available explicitly.
This removes repeated cross-version work from every commit without claiming syntax/core checks
replace the full suite. The Principal stopped its own duplicate run; neither interrupted commit
completed. Its earlier hook had reached the second interpreter, so both suites on the first interpreter
passed for the initial migration snapshot, not a full-suite certification of the final branch.

### Migration settings verified, 2026-09-29

Principal `01a0ec25`, worktree `shoalmark-principal-migration`; changes authorized in the Owner’s migration request and explicit follow-up to include public-repo hardening. GitHub API reads/writes targeted only `shoalmark/shoalmark`.

- Owner commit `d1a269b` preserved unchanged; local `main` restored to fetched `1c344ed`. `origin` already named the organization repository. No remote main push.
- Pages: workflow source, URL `https://shoalmark.github.io/shoalmark/`; repository homepage already matches. Deployment awaits merge so main’s old URLs are not republished.
- Ruleset `24177420`: active, empty bypass; PR required with zero forge approvals, force-push/deletion restrictions retained. Removed `update` (it barred PR merges too), retained `creation`. Added the five existing `suites (OS, Python)` checks, bound to GitHub Actions app 15368. No requirement for Pages `build`/`deploy`, which do not run on PRs.
- Default Actions token was already read-only and cannot approve PRs. Fork workflow approval changed from first-time contributors to all external contributors.
- Enabled secret scanning, repository push protection, Dependabot vulnerability alerts/security updates and private vulnerability reporting. Read-back confirms the enabled security states. Secret-scanning API returned zero open alerts on its first page; this is an observation during enablement, not a historical secret or privacy audit.
- Local Zensical 0.0.66 clean build and `llms_txt.py`: 11 Markdown twins; generated English/German signing pages and agents contract checked. `check_site.py` rejects the observed broken include and a removed signing destination in negative controls. Historical tracker evidence and dated personal-account census prose remain unchanged.
- Obsolete: active personal-account URLs, unpublished-site workflow comments, unpinned Zensical installation and ready-transition-only CI. No release version or tag changed; consumers receive the tool’s new URLs when they next vendor a release containing this branch.


## Done when

The site builds in CI from `docs/` and is served; the README is rendered there and not copied; `llms.txt` and the
`.md` twins exist; the human pages exist in English and German — set up · sign · standup · board · the first week; and
one outside Owner has followed the setup page without asking anything.

## The landing page names the authority — the Owner's finding of 2026-09-25 09:52:49

**The Owner's finding (spelling normalised):** *the landing page in `site/` fails to name the product's core selling point now.* For the GtM seat the tasking is to decide the wording. His proposal, quoted: *"Your agents work on your mandate: a decision you signed. Nothing else counts, not a click, not a merge, not a line in chat."* — *"Ihre Agenten arbeiten auf Ihr Mandat hin: eine Entscheidung, die Sie unterschrieben haben."* His strongest counter-fact, in his words: *"mandate" can sound bureaucratic or political, especially in German; the morning's "bureaucratic nightmare" question makes that a real risk. "Your signed word" is the warmer fallback* (*a click is not your word* · *no build before a judged mandate*).

*The Auditor seat's assessment, filed word for word from the Owner's paste of 09:52:49; sha256 as filed, with one trailing newline: 65980cd066b83e1f399c616c75c01d7e87da44209478d9d4103842620d5e41d2.*

Yes, it's missing · 80%. It's also the product's core, not a side feature: your own TRIAGE intent promises "the signed decisions that authorised this work … rule sets that prevent agents from going rogue." The landing page describes the mechanics ("every answer is your own signed commit", "signs it with your key"). It never states the consequence: your agents act on your signed word, and nothing else counts as your word.

Three conditions for adding it · 85%:
1. Claim only what the tool enforces. The page's own headline is "Measured, not promised".
   - Enforced today: an answer counts only from a commit signed by a key in allowed_signers. An unsigned change to an answer is refused. A click or a merge can't write an answer.
   - Not enforced: the tool can't stop a seat from reading a click as an answer. That's what happened with PR 34, and path 5 is only a written rule. The "agents build only on judged work" gate isn't released until v0.18.3 is tagged. A readable log of who ruled what (--rulings) doesn't exist yet.
2. Pair "authority" with the tiers. At tier 0, the easy start, "signed by you" means signed by something on your account. The honest selling point is authority plus a signature whose strength you choose, which the record states. That's stronger than an overclaim, and it links straight to the new signing page.
3. The copy is the GtM seat's to write, under FM-006, which is In Progress, with a Reviewer checking each claim against evidence. Input it could start from, not final wording:
▎ "Your agents move on your word, and only on your signed word. In the record, an answer counts only as a commit signed by a key you trust. A click, a merge or a line in chat is not an answer. How strong that signature is, you choose; the record says which."

While the page is being edited, one more thing to check · 60%: the "Measured" section claims "9 of 13 pull requests carried a Reviewer's file before they were opened". It names no repository, window or source. My check 19 found the opposite in shoalmark yesterday: 8 of 14 seat PRs were opened before their review existed. It may be PortDive's count over a different window. Either way, a public measured claim needs its source cited: repository, time window, count method.

Verdict: yes, add the authority point. Keep it to what the tool enforces today, tie it to the signature tiers, have GtM word it and a Reviewer check it. Fix or source the "9 of 13" line in the same change.

## Going public — the Auditor seat's counsel, and the four gates

**Through the Owner at 16:26:24 on 2026-09-25, as pasted, revising its ask of 16:22:12:** *Ask on the board (ruling): "When and how does shoalmark go public?" options: "this repository, as it is, at the first tag after the 09-29 scoring with CI green on all three platforms, the signing tier stated or the hardware key live, and a gitleaks scan clean | a new repository from a snapshot, this one kept private as the archive, the client names removed, the same gates | not yet" · proposal: the first, if the client names may be public (the Auditor's counsel, 2026-09-25).* The ask above carries it, its options re-made declarative on the addendum below (17:23:39) — kind `action`: a yes switches the repository's visibility or creates a new one on his account, his hands (`--schema`: an ask whose yes needs the Owner's hands is `action`; the first version said `ruling`, the Reviewer's R1). An option is at most 120 characters on the board, so the options name the gates without listing them (*gates held*, *same gates*); they are here in the counsel's words, the fourth in its addendum's, and the seat's gloss stands apart in brackets:

1. *CI green on all three platforms* [on the tag that goes public; red on `v0.18.3`: FM-035, its fix in review].
2. *the signing tier stated or the hardware key live* [the tier on the site's signing page, FM-007; his answer: the key after the scoring, once delivered].
3. *a gitleaks scan clean* [of the whole history].
4. *the port evidence deleted or moved, as ruled on 09-22* [the Auditor seat's addendum of 17:23:39, below: `work-tracker/evidence/FM-001/port/`, six files on main].

**The fourth gate is the Owner's ruling of 2026-09-22** — the parent's ledger, `docs/work-tracker/evidence/FEAT-190/asks.md` row 10 (2026-09-22; the file's line 36): *delete or move the port evidence before shoalmark goes public*; his answer: *should consider this now* [normalised]. The act is FM-006's own: its form — deleted here, or removed in the snapshot — is what his answer to the ask picks, and the act's commit is judged under FM-006; the filing freeze (`--check`: 20 open, only bug filings) allows no new tracker, so this tracker holds the act. Nothing is deleted before his answer.

**The parent's traces, counted by the Implementer seat at `9555d2c` — its numbers beside the Auditor seat's corrected count (17:37:17, below).** The method, in one sentence: every blob `git rev-list --all --objects` lists is read with `git cat-file` and searched for the parent's name in any case, as the correction spells it, and the blobs that name it are counted, then placed at every path a tree gives them, against this branch's tip and `git ls-tree -r origin/main`. The scope: this repository's 91 refs and its 15 worktrees' HEADs, its pull heads not fetched as refs; then the forge's own refs from `git ls-remote` — 3 branches, 15 tags, 77 pull heads — read by their ids (PR 77's merge ref is not here); the Auditor seat's clone had 175 refs, its pull heads fetched. Each number, the Auditor seat's first:

- *28 versions name the parent project* — 28, in both scopes; all 28 are reachable from this branch's tip alone.
- *8 are the tip's files* — 8 at this branch's tip, and 8 at main's (`8b267b4`), whose FM-006 is an older version.
- *20 are older* — 20 (against main's tip: 18 older, and the two FM-006 versions of this branch).
- *The older versions sit at 7 paths: 5 still exist at the tip; 2 are FM-002's evidence before its move* — 7, 5 and 2: FM-006, FM-020, FM-022, `review-fix-0.17.5-…` and `review-fm-006-the-landing-page-names-the-authority.md`; `docs/work-tracker/evidence/FM-002/brand-layers-rd.md` and `…/FM-002/examples/origin.theme.css`.
- *3 files (FM-020, FM-022, review-fix-0.17.5) name it only in older versions* — 3, the same three; their tip versions do not name it.
- *The literal name is a lower bound* — so it is here: 3 of the 6 port files do not carry the name, and a name search does not find them — `wrapper.gen-tracker-index.py` and `derive.py` hold the parent's layout (`docs/work-tracker/`, `scripts/gen-tracker-index.py`, its submodules, its release axis), `run-origin-checks-statementwise.py` runs the origin's checks. The positive control first set, the wrapper, is one of them; the control that holds is main's own tree: `git grep -i -l` on it lists 8 files, the 8 found.

No number differs. The count is of `9555d2c`: each new version of this file adds one, because the file names the parent itself (the Auditor seat's assessment above, its *9 of 13* paragraph, and the correction below).

The proposal is the Auditor seat's counsel, disclosed as such: *the first — the Auditor seat's counsel; if either may not be public, the second* (its addendum's item 3, below; *either* is the client names or the parent's traces). Since 17:23:39 the options are declarative, in the Auditor seat's wording (the Reviewer's R4 on `1dea28b`): each says what it makes public or removes, so his pick decides the condition and no option carries an *if*; the condition stands here and in the ship log, not in an option's text. Until then it stood inside the first option (*this repository as it is, if its client names may be public — …*), because the board shows only the ask, the proposal and the title. The earlier ask of 16:22:12 (five gates, a license among them) was replaced by this one before it reached the board.

**Through the Owner at 17:23:39 on 2026-09-25, as pasted — the Auditor seat's addendum to its counsel, against its own miss:**
FM-006, before PR 77 merges — the Auditor seat's addendum to its go-public counsel, against its own miss:
1. The Owner's standing ruling of 09-22 (the parent project's ledger, its FEAT-190 row 36): "delete or move the port evidence before shoalmark goes public"; his answer: "Should consider this then now". work-tracker/evidence/FM-001/port/ is still on main (the parent's repository name, local paths, its tracker ids, brand files), and no tracker holds the act. A fourth gate: the port evidence deleted or moved, as ruled on 09-22 — and a tracker for the act.
2. "As it is" keeps the parent's traces in history after the deletion: 28 blobs across all refs name the parent project, 7 of their paths only in history. The choice turns on two facts: the client names, and the parent's traces.
3. The options, declarative (R4; the Reviewer's R3 wording): "this repository, client names and the parent's traces public, the port evidence deleted — after the scoring, gates held" (119) | "a snapshot as a new repository, client names and the parent's traces removed, this one the private archive, same gates" (118) | "not yet". Proposal: the first — the Auditor seat's counsel; if either may not be public, the second.
4. The parent's ledger row 47: an appended clause to match.
5. A 0.18.4 line on FM-030: the move after an answer follows the picked option, not the kind alone.

**Through the Owner at 17:37:17 on 2026-09-25, as pasted — the Auditor seat's correction to item 2, its own error:**
FM-006 — the Auditor seat's correction to item 2 of its addendum, before it is written (its own error):
"7 of their paths only in history" is wrong. The count (all 175 refs of a clone with refs/pull/*/head fetched; every blob; "portdive", any case): 28 versions name the parent project — 8 are the tip's files, 20 are older. The older versions sit at 7 paths: 5 still exist at the tip; 2 are FM-002's evidence before its move from docs/work-tracker/ to work-tracker/. Where the redaction took the name out of the tree, the history keeps it: 3 files (FM-020, FM-022, review-fix-0.17.5) name it only in older versions. The literal name is a lower bound: the redaction wrote "the origin" and "the parent project", so the parent's tracker ids, pull request numbers and incident detail stay under those words, in the tree and the history. Item 2's conclusion stands: "as it is" publishes the parent's traces.
On the Principal's call (FM-006 holds the act; nothing deleted before his answer): not struck. Name the act in FM-006's What is true now, not only in its Going public section.

**The home at the flip — the Owner's word of 2026-09-26, through the Auditor seat, as pasted at 11:05:27 (sha256 `19ca39d1794c67cf15e26399667d392cadc65fdb1c5c5d22fe44993277ad4ec5`):**

On the Owner's word (2026-09-26): shoalmark is a tool, not a company — its home becomes a GitHub organisation `shoalmark`, the Owner its only owner. He creates it (free, empty) now; the repository moves at the flip.
A line on FM-006's going-public plan: at the flip, transfer holgo99/shoalmark into the organisation — the history, the signed commits and the pull refs move with it, and GitHub redirects the old URLs. In the same slice:
- the vendoring sources and pins in PortDive, msr-lager and fb-sondermasch;
- shoalmark.toml's blob links;
- the docs site's address (with the domain the GtM line settles);
- CI;
- each seat's remote.
Then branch protection on main (free for a public repository). Nothing moves before the flip.

[The seat's gloss, not his word: the transfer is the mechanism of the ask's first option (*this repository … public*) and changes no option's text; the consumers' pins (PortDive PD-400, msr-lager, fb-sondermasch) are PortDive's and the two clients' own slices at the flip, named here so none is forgotten; nothing moves before his answer to the ask.]

## The page on his word in TRIAGE.md — filed 2026-09-25, the paste of 22:38:24, committed 22:40:18

**Through the Owner at 22:38:24 on 2026-09-25, as pasted — the Auditor seat, on the Owner's word (sha256 `be19a4100d73fc27f6d0015ac42a8c4ee152ebcfa751e9ec8fc523ac99933584`):**

From the Auditor seat, on the Owner's word: file the site/ page on his word in TRIAGE.md — a line on FM-006 (the freeze bars a new tracker; FM-022 is Shipped and left the site out on purpose). FM-006 is free now that PR 77 has merged.
The line:
- A page for people, English and German (docs/ and docs/de/, in the nav): what TRIAGE.md holds — the intent (for · so that · never) and the current path — and how an edit there changes what the fleet does.
- Built after FM-037 merges, so the page can say "only you change it" as enforced by the tool, with its tier-0 limit (FM-007): a commit signed with the Owner's key passes, and at tier 0 any process on his account holds that key.
- Each claim labelled by what enforces it: the tool, review, or the text alone.
- The term: the site says "your signed word" (the GtM decision against "mandate"). The page keeps it unless the Owner rules "mandate" or "Person-in-charge" in by an ask.
- Examples from shoalmark's own record or invented, never the parent project's state (its 09-22 ruling, row 10) or a client's:
  - path line 3's rewrite (fe36cc0) and the independence count --check prints;
  - FM-035 kept P1 at 42f4eca, re-judged P2 at c8939e3 with path line 1 quoted whole;
  - a raise naming "path 5" re-judges a tracker the same day;
  - FM-022's village-library intent for a first draft;
  - FM-037's refusal of a seat's edit, shown;
  - what an edit does not do.
- Worded by the GtM seat; a Reviewer checks every claim against evidence before the merge.

Filed here because the freeze (21 open) bars a new tracker and FM-022 (Shipped) left the site out on purpose; this tracker holds the page.
The build waits for FM-037's guard to merge, so the page's *only you change it* is the tool's, with its tier-0 limit stated; the GtM seat words it,
a Reviewer checks every claim against evidence before the merge; the term stays *your signed word* unless the Owner rules otherwise by an ask.

**Built 2026-09-26 by the GtM seat** (`8e509911/gtm-2`), cut from `main` at `88c7b0c`: `docs/triage.md` and `docs/de/triage.md`, in the nav.
The refusal quoted on each page is the output of `evidence/FM-006/triage-page/demo.sh` and `demo-de.sh` (their `.out` beside them): an
invented Owner, a seat, the tool of `88c7b0c`, the village library as the intent; the German run set up as `docs/de/setup.md` §2 says.

## The themes, for the board and the site — filed 2026-09-25 by the GtM seat, narrowed 2026-09-26

**On the Owner's word in chat** (quoted in the evidence, spelling normalised) — 2026-09-25: *"I agree to this
direction"*; *"we need a `shoalmark` theme besides the `monochrome` theme … a strong starter"*. 2026-09-26: *"Only
`monochrome` + `shoalmark + graticule` themes. The design must go also into `site/`"*; *"the graticule must look more
like on a real nautical chart and have also coordinates / degrees"*; *"the monochrome site shall also get the
graticule, but muted"*; *"move the claim, shoalmark and version outside the inner chart area into a footer"*. His
words, not a signed answer: the ask below makes them one.

**His word in chat of 2026-09-26 09:23:58** (spelling normalised; with it two screenshots of the committed renders, the
top of `monochrome-light.png` and the top of `shoalmark-dark.png`, not filed): *"For the dashboard I prefer this 'inline
header' (shoalmark logo + light/dark switch) variant [the first] over this variant used in the dark mode, where the
header sits outside the graticule [the second]. Align for both. All dashboards aligned over all themes. The `site/`
renderings are excluded."* The seat's reading, marked as such: on the board, the mark, the name and the switch stand
inside the graticule, as `monochrome`'s board has them, in both themes and every board view; the site keeps its header.
A word in chat, not a signed answer; the drafted ask is unchanged by it. **What it changed:** of the stylesheets, only
`shoalmark.css` — the navy band and its drying line left the board's top and stay the board's foot and the site's header
and foot; `shoalmark`'s eight renders were re-made; the site is untouched.

- **The two themes, each for the board and the documentation site** — which one shoalmark's own wear, and whether the
  tool ships them, is the ask's:
  - `monochrome`: the terminal cut, IBM Plex Mono on one grid;
  - `shoalmark`: the brand's own, a sea chart's ECDIS colours, magenta only for what is owed to the Owner, the status
    marks in the buoyage's shapes; on the board its header — the mark, the name, the switch — inline inside the
    chart's top border as `monochrome`'s (his word of 09:23:58), the navy band and its drying line the board's foot
    and the site's header and foot.
  - on the board, both: the last line — the claim, the mark, the name, the version — in a foot of its own below the
    chart, full width, as the site's.
- **The chart, in both:** a Mercator sheet of Neuwerk's Watt drawn behind the page — parallels every minute, meridians
  every two, a chart's graduated border, degrees and minutes along it; muted in `monochrome`, blue-grey in `shoalmark`.
  CSS only, never read aloud, shown only where the margins hold it.
- **How a theme is chosen:** choosing a theme is putting a file in a place — for shoalmark's own board,
  `work-tracker/brand/theme.css`; if the tool ships themes, `--brand DIR --from <theme>` writes a starter from one.
  FM-002's four places and its one rule stay, with no setting, and the tool's default look stays for every consumer.
  shoalmark's own board and site wear at most one theme; the ask says which, or none.
- **Dropped on 2026-09-26:** the mockups `catkin`, `bagels` and `seekarte`, on the Owner's *"only"*. They are in git at
  `96aa05e`.
- **How it was mocked:** CSS only, on the real board and the real site. Every text pair a rule uses is at 4.5:1 or more
  in both schemes, the chart's figures included. Markers and figures are never read aloud; Chrome's accessibility tree
  shows it, with a control run.
- **Evidence:** [`evidence/FM-006/themes/`](evidence/FM-006/themes/README.md) — the four stylesheets, the script that
  rebuilds the mocks from the board and the site, the renders, what was checked, what was not.
- **The Auditor seat's counsel (relayed by the Owner):** its three fixes are in every file. Its hold (file after v0.18.4
  is tagged) was lifted by the Owner's *"You file this"*. v0.18.4 was tagged on 2026-09-26 at 09:58 (`a7e5291`).
- **Filed here** because the freeze (21 open) bars a new tracker, FM-002 (Shipped) built the brand layers, and this
  tracker holds the board's and the site's brand since 0.18.2.
- **Slice A is the brand layer; slice B is code** — the cheap step first. Both are FM-002's since 2026-09-26: its
  answer (`4e00f85`, PR 90, option 2) rules both in, and the pass of 2026-09-26 judged the build before its first build
  commit (FM-033), the tier stated per slice, the markup hooks in slice B. FM-002's *What is true now* and *Done when* are
  the slices' home; the lines below are the record as filed.
  - *Slice A — shoalmark's own board and site:* `work-tracker/brand/theme.css` from the chosen theme; two Plex Mono
    cuts, SemiBold and Italic, Latin-1, from `@ibm/plex-mono` 1.1.0, hashed as the Regular is (`10d3c7fa…`); the site's
    theme in `docs/stylesheets/`. No `shoalmark.py` change, and none of the files `--vendor` copies: no consumer
    receives anything.
  - *Slice B — only if he rules the tool ships themes:* `brand/themes/` and `--brand DIR --from <theme>` in
    `shoalmark.py`; code, and every vendoring consumer receives the files. A consumer that chooses nothing keeps the
    tool's default look (FM-002's per-repository choice).
  - *In neither slice as his word draws them:* the three markup hooks the mocks work around in CSS (the owner's box
    title as a label, one footer element, a class on striped rows) are `shoalmark.py` changes. Slice A wears the mocks'
    CSS, workarounds and all, on the board the tool writes today; the pass says where the hooks go.
- **Moved to FM-002 on 2026-09-26** — the ask stood on FM-002's board, raised on the Owner's *go* of 10:25:41 and judged by the same-day pass (its worksheet `evidence/triage/triage-2026-09-26.md`), and is answered there (`4e00f85`, PR 90, option 2); this tracker keeps its one ask, going public, answered (`8defe63`, PR 91). The draft below is the record of the wording it took:
- **The ask, raised when this tracker's open ask is answered** (a tracker holds one ask; the Principal raises it) —
  still a draft, re-made on 2026-09-26 on the Owner's word through the Auditor seat (AU-24): the first draft asked two
  things in one and had no option for the cheap step.
  - kind: `ruling` — a decision of intent; no hands of his are needed for the answer.
  - ask: *Which theme do shoalmark's own board and site wear — the brand layer and the site's stylesheet, no tool
    change — and, separately, does the tool ship themes: `brand/themes/` and `--brand DIR --from <theme>`, code whose
    files every vendoring consumer receives?*
  - options: shoalmark's own board and site wear the shoalmark theme; the tool ships no themes yet | the tool ships
    monochrome and shoalmark as starters; shoalmark's own board and site wear the shoalmark theme | not yet —
    shoalmark's own board and site keep today's look; the tool ships no themes (85, 108 and 84 characters)
  - proposal: shoalmark's own board and site wear the shoalmark theme; the tool ships no themes yet — **the GtM seat's
    proposal**, because it is the cheap step: one Reviewer pass instead of adding the code tier (inline passes, tests,
    CHANGELOG), and none of the files `--vendor` copies changes, so no release after 0.18.4 hands a vendoring consumer a
    theme before he rules the tool ships them.
  - `monochrome` is not offered as the worn theme: the GtM seat does not propose it. Under the second option it ships
    as a starter.

## The landing page — mocked 2026-09-26 by the GtM seat

**On the Owner's word in chat, 2026-09-26** (quoted in the evidence, spelling normalised): *"a landing page for
`shoalmark` showing the current release version, its features and claims: For Agents, For People … the chart renders
ship wrecks, each with a tracker number, incident ID and a short incident report … make it count!"*; on the result,
*"you nailed it — file, commit and push"*. His words, not a signed answer.

- **What it is:** one HTML file in the `shoalmark` theme's night palette — an arcade's attract screen whose playfield
  is a pixel chart of the German Bight's Wadden coast, Borkum to Dithmarschen, with the themes' graduated border and
  graticule. Its wrecks are the 23 trackers tagged `bug` or `security`: tracker number, the commit that filed it as the
  incident ID, the filing day, the status, the report from `hook:`. The release is v0.18.4; 1P for agents, 2P for
  people, the high scores, the register, the stages — every claim read from `docs/index.md`, `README.md`,
  `CHANGELOG.md` and the trackers, each source named in the evidence.
- **Checked:** no script error at 1440, 1024 and 390 px; every text pair at 4.5:1 or more; the wrecks keyboard-reachable
  and named; nothing moves under reduced motion. Not verified: Firefox, Safari, a screen reader, print.
- **Evidence:** [`evidence/FM-006/landing/`](evidence/FM-006/landing/README.md) — the page and four renders.
- **Not built, not asked.** Where it would live — the site's start page, or a page of its own — and whether it ships
  are the Owner's to rule; nothing is drafted for the board while FM-006's asks wait. The statuses on the page are a
  snapshot of 2026-09-26.

## What a stranger meets first — v0.19.0

**The Owner's ruling, 2026-09-30.** One slice before the v0.19.0 tag (2026-10-02, 09:00 CEST): the branch
`fm/006-what-a-stranger-meets-first`, cut from main `1197e80`, carries the two screens this ruling follows — [the
seats'](evidence/FM-024/go-to-market-screen-v0-19-0-seats-2026-09-30.md) (`a410aef`) and [the first-screen
proposal's](evidence/FM-006/go-to-market-screen-first-screen-proposal-2026-09-30.md) (`87985b6`) — so their records land with
the change they justify, in one pull request. No further screen round. The Reviewer checks every new line for its truth
against the tool at the tree and for its language, English and German. The Owner judges the Designer's render, the phone's
first screen first, before the merge.

**A — the human lead.**
- **A1, the English landing** (`overrides/landing.html`). The H1 reads *The agents keep the work; the person keeps the word.*;
  the `<title>` reads *shoalmark — the agents keep the work; the person keeps the word*; the section subtitle that says it now
  (`:356`) goes. The lede under the H1 is the job line: *Ticket systems were built for people handing work to people. shoalmark
  is built for your agents: the work lives in your repository, no done gets through without a commit behind it, and what waits
  for your word comes first.* Its short form, without *the work lives in your repository*, is the fallback if the phone render
  pushes the action off the first screen. The agents' card keeps its opening sentence as FM-005's check rewrote it (`:361`),
  the proof beside the lede's promise. The first screen carries one action, *Hand your agents the note*, to the English note
  (B4).
- **One description** serves search, the link preview and `site_description` (`zensical.toml`): *A work tracker in your
  repository, built for your agents: no “done” gets through without a commit behind it, and what waits for your word comes
  first.*
- **Link previews.** The landing's own head carries `<link rel="canonical">`, `og:type` website, `og:site_name` shoalmark,
  `og:locale` en_GB, `og:url` `https://shoalmark.github.io/shoalmark/`, `og:title` (the H1), `og:description` (the description),
  `og:image` `https://shoalmark.github.io/shoalmark/assets/preview.png` (1200 × 630) with `og:image:alt` *A night chart of the
  German Bight, with defects from shoalmark's own tracker lying on the flats as wrecks.*, and `twitter:card`
  summary_large_image. The preview image is the Designer's: a 1200 × 630 PNG of the chart with the wordmark, without the headline
  or the counts, a real render of the page, committed as `docs/assets/preview.png`; the Owner judges it with the render. One
  theme override adds the same tags to every other page — `de_DE` under `de/`, the preview title from the page's front-matter
  `title:` — guarded for pages without front matter. The Markdown twin, `docs/index.md`, follows the landing.
- **A2, the German start page** (`docs/de/index.md`) leads with *Die Agenten tragen die Arbeit, der Mensch hat das letzte
  Wort.* and carries no claim: *Dein Eigner bremst. Tunen statt tauschen.* leaves it. Its job line: *Ticketsysteme wurden
  gebaut, damit Menschen einander Arbeit zuweisen. shoalmark ist für Ihre Agenten gebaut: Die Arbeit liegt in Ihrem Repository,
  nichts geht ohne Commit dahinter als fertig durch, und was auf Ihr Wort wartet, steht ganz oben.* — its short form without
  *Die Arbeit liegt in Ihrem Repository*, as the landing goes. The one action links `ADOPT.de.md`. Its front matter carries its
  own `title:` *Die Agenten tragen die Arbeit, der Mensch hat das letzte Wort* and `description:` *Ein Arbeits-Tracker in Ihrem
  Repository, für Ihre Agenten: Nichts geht ohne Commit dahinter als „fertig“ durch, und was auf Ihr Wort wartet, steht ganz
  oben.*
- **The gate clause** — *no done gets through without a commit behind it*, *nichts geht ohne Commit dahinter als fertig durch*
  — stands in the ledes and descriptions because FM-005's check is merged, on git and on Subversion; without it they would drop
  the clause, never saying *on git*.
- **A3, the Owner's card,** is unchanged in both languages.

**B — the tagline, where agents read.**
- **B1** The README's opening heading reads *Get a better-performing human Owner.*
- **B2** The summary line of `llms.txt` (`scripts/llms_txt.py`) opens with *Get a better-performing human Owner.*
- **B3** `ADOPT.de.md`, the note the Owner hands their agents, opens with *Euer Owner bremst. Tunen statt tauschen.*, and its
  line 5 reads *…und **euer Owner entscheidet***.
- **B4** `ADOPT.md`, the English note: a translation of `ADOPT.de.md` with the same fix (*your Owner decides*), opening with
  *Get a better-performing human Owner.* The landing links it as the note for trying it, with *(Deutsch)* beside it for
  `ADOPT.de.md`.

**C — the fleet, a section of its own on the landing,** placed early by the Designer and headed *The fleet*. Its first
line: *A seat is a role an agent takes, with its duties and its rights written down.* Below it four tiles, each with its
badge from `brand/seats/`, its name, its character from `brand/seats/README.md` and one line:
- **Planner**, the skipper: turns the Owner's direction into trackers, and puts the agents' open questions to the Owner,
  one sentence each.
- **Builder**, the shipwright: builds one change from its tracker, in a worktree of its own, and never accepts its own work.
- **Reviewer**, the inspector: reads a branch against its tracker and writes READY, or what must change. It never merges.
- **Specialists (customizable):** called in when the work needs them. Name your own in `[seats]`, with the rights
  `[rights]` gives them. The tile shows the four specialist badges — research, go-to-market, designer, auditor — small and
  unnamed.

The agents' card keeps its command list. *All seats* links `https://shoalmark.github.io/shoalmark/seats/`, absolute like
the page's other links: a root-relative `/seats/` 404s on the project site. The Designer renders desktop and phone.

**Acceptance.** The section sells the rights model, not agents: the tool ships no agents and enforces no duties. It makes
plain that the gate enforces the rights, that the tool knows three seats, and that everything else is practice the adopter
writes — in the README's own words (§*Seats*) where a clause is needed, not a new line. The characters are the seats'
brand, not features. On a phone the chart falls below the fold, so the H1 in the pixel face, the job line and the one action
carry the first screen alone: the render the Owner judges shows all three at phone width, above the fold.

**The Owner's judgment of the render (`70ffd5f`), 2026-10-01: accepted, with five changes.** The phone's first screen moves the
title block up so the chart's top edge shows in its last 100–150 px, hinting at what follows; the H1, the full lede and the action
stay above the fold. The agents' card is headed *For agents*; *The fleet* is the new section's. `preview.png` keeps the wreck
labels, without the highlighted wreck and its selection box — no single defect is singled out. The German pages declare
`lang="de"`, and the landing links the site's Pricke SVG as its icon. The desktop H1's cap, the anchors' removal and the rights
line stay as the Designer made them; if the configuration change (D2) falls back, the landing's rights line takes the fallback
text too. The Owner sees a re-render of the phone's first screen and the preview before the merge.

**The Owner accepted the re-render at `6ab480d`, 2026-10-01, and ruled RV-2189 into the bundle:** the landing must not scroll
sideways at 360, 375 or 390 px — the HUD made it 390 px wide at 360 and 375 — by the Reviewer's tested CSS rule; the render set
gains `phone-360-first.png`, which the Owner sees with the others. If the fix needs more than a CSS change, it moves after the tag.

**D — the Owner is not a seat.**
- **D1** The seats page (`docs/seats/index.md:3–4`), README §*Seats* and the tool's printed text read: *the Owner, and
  three seats with their rights built in — planner ask · close · triage, reviewer triage, builder none*. The seats page
  groups its rows under *The core seats* and *Specialists*, and carries C's definition.
- **D2** — attempted, not in this slice: the Owner's identity is configured outside `[seats]`, and `[seats] owner` is still
  read as its old spelling. It goes into the one `[seats]` change of 2026-10-01, after the Apps (11:00). If it threatens
  the 15:00 cut, D1 adds one line — *the Owner, whose identity `[seats]` still carries as `owner` until 0.19.1* — and the
  same fallback covers `docs/setup.md:53` and the refusal at `shoalmark.py:4520`, which lists the Owner under *The seats
  are:*.

**E — pronouns and wording.** `overrides/landing.html:411` (one *his*) and `:463` (*he* and four *his*);
`docs/requirements.md:39` (*his go*); `README.md:269` (*below their:* becomes *theirs*, or a noun); `AGENTS.md:86` (*he
said yes* becomes *they said yes*); the seats page's *as it likes* becomes *as the adopter chooses*. They stay, as history:
the eight in the landing's embedded tracker titles (`WRECKS`), which quote records, and the template's comment at `:3`.

**FM-005's check went first,** as a must for v0.19.0, in its own pull request (PR 143, merged 2026-10-01 08:10:46); this
slice merged main after it and runs CI again.

**Ruled with it:** the App lines keep *brief* when the Apps are made on 2026-10-01 — they describe how a seat works, and the
landing names the product's unit; both are revisited after the tag.

**After the tag:** a decision flow near the top of the landing; what the measured counts measure; *Eigner* against *Owner*
in German prose (*One claim, the Owner's*, above, records *der Eigner*; `ADOPT.de.md` says *Owner* ten times); the App
lines' *brief*; descriptions of their own for the other German pages — until then they preview with the site's
description; a release workflow — the notes from the CHANGELOG, the assets, an attestation; a light scheme — the page is dark
only; a picture of the board itself; the incident panel's cycle; how many
seats and review passes a one-Owner product carries; the way back on both start pages, and *What it is not* becoming *What
stays yours* — each screened first (the Owner's ruling, 2026-10-01); the Owner named *he*, *his* or *him* on 128 lines of
`shoalmark.py`'s comments and docstrings (the Auditor's count at `c830470`; no printed line) — filed, not fixed (the Owner's
ruling, 2026-10-01); from the cold audit of v0.19.0 (the Owner's rulings, 2026-10-01; filing is frozen): F3, the Markdown
twins' broken links (`scripts/llms_txt.py`); F6, the private measurement's source and date on the box; F7, the German
board's `lang`; and GitLab — by the code, all but `--queue` already works on any git host; the queue needs a reader for
GitLab; untested.

## The landing's player stats at the v0.19.0 cut

**The Owner's ruling, 2026-10-01.** The player stats are updated for v0.19.0 at the cut, in one commit: the last content commit
before the tag and the release bundle's last, after the site slice, D2 and the release commit, which cuts VERSION's CHANGELOG
section that the wreck script reads.
- **On the landing:** the top bar (release, hi-score, wrecks, open); the *High scores* table and its footnote; the `WRECKS` data and
  the register's summary; the board excerpt; the footer's release line and its *read at its cut* note. The *before it* row keeps
  *before the Owner's signed answer* (the site slice's fix).
- **Every place that carries the counts, and only those** — at `1197e80`: `overrides/landing.html:289`, `:410`, `:411` with the
  footnote at `:414`; `docs/index.md:31`, `:33`; `docs/de/index.md:27`, `:29` — the same numbers, read at the same cut, to the same
  end date (*to 1 October 2026*, *bis zum 1. Oktober 2026*, if the cut is today); `docs/index.md:31`'s *the owner* becomes *the
  Owner*. The footnotes under those counts (`docs/index.md:35`, `docs/de/index.md:31`) follow the landing's: the same date,
  source and method.
- **The numbers are the Auditor's,** re-read at the cut; no seat computes them; the Reviewer checks every page against them. **The
  method,** in the footnote as today: merged pull requests of `shoalmark/shoalmark`, numbers 1 to the last at the cut, without the
  Owner's answer branches; one counts when a non-merge commit adding or changing a file under `work-tracker/evidence/reviews/` is
  dated before the pull request was opened.
- **The Auditor's numbers at the cut `c830470`**, read 2026-10-01, 12:47–12:55 CEST:
  - the top bar: release `v0.19.0` · hi-score 71/82 · wrecks 27 · open 10;
  - *High scores*: 1st 71/82, *after the rule* — pull requests 47–144, from the Owner's signed answer of 24 September 2026, 11:07
    CEST, to 1 October 2026; 2nd 10/37, *before it* — pull requests 1–43;
  - the footnote: “Counted on 1 October 2026 with gh from pull requests 1–144 of shoalmark/shoalmark: merged ones only, without
    the Owner's own answer branches. One counts when a commit adding or changing a file under work-tracker/evidence/reviews/,
    merge commits excluded, is dated before the pull request was opened.”;
  - the wrecks: `WRECKS` from the script at `c830470` — 27: In Progress 7, Proposed 3, Shipped 16, Closed 1, so open 10, raised
    16, closed 1; all 27 links written as `shoalmark/shoalmark`;
  - the board's excerpt (`--owner` at `c830470`): *waiting for you* 1; *your acts, with their time* 1, the row “FM-007 after the
    scoring, once the key is delivered · promised 2026-09-25 · no date yet”; the caption “shoalmark's own board, 1 October 2026”;
  - the footer: the release line “v0.19.0, released 1 October 2026 — shoalmark 0.19.0 is the first public beta: …” — the date
    from the CHANGELOG's heading, as *The release day* below rules it, then a dash, so the CHANGELOG's headline stays word for
    word with one colon in the line (the Owner's ruling, 2026-10-01); the release read at its cut, 1 October 2026;
    the wrecks and the board's excerpt read on 1 October 2026, 12:47 CEST.
- **The wrecks** come from `evidence/FM-006/landing/start-page/facts.mjs` at the cut; the script stays as written — evidence is
  append-only — and its wreck links, which say `holgo99/shoalmark`, are written as `shoalmark/shoalmark` in the page; the commit
  says so.
- **The Reviewer's grep:** `git grep -E "12 of 15|12/15|10 of 37|10/37|12 von 15|10 von 37"` outside `work-tracker/` and
  `CHANGELOG.md`, and `25 September` (and the German `25. September`) in the three files — only the unchanged *before* rows' 10/37
  may remain.
- One Builder, or the Designer already on the landing; the Reviewer after; CI; then the tag.

## The v0.19.0 release commit

**The Owner's approval, 2026-10-01.** In the release bundle (`release/v0.19.0`), after main with the `[seats]` switch, the
`From:` fix, this slice and the bundle's carried findings, and before the player stats — prepared in commits of its own before
the switch merged, and the CHANGELOG's cut and the notes' checksum last, after it (the Owner's ruling of the same day):
- **README:** the first screen's lists to v0.19.0 — *the tracker, the gate (it refuses a done without a commit behind it), the
  board with waiting for you on top, …*, and the direction *…the rest of evidence-checked done…*; the FM-005 pointer as
  `https://github.com/shoalmark/shoalmark/blob/main/work-tracker/evidence/FM-005/design.md`; §6's `<shoalmark-url>` as
  `https://github.com/shoalmark/shoalmark`; §8 moved above §9, the anchors unchanged.
- **The workflows:** `docs.yml:4` — *Runs on a release tag, or by hand: the site is built and deployed per release. A pull
  request does not build the site; `zensical build` locally does.*; `ci.yml:9` — RV-2110's text.
- **The version:** `VERSION` and `__version__` 0.19.0; the CHANGELOG's `## 0.19.0 — 2026-10-01` (*The release day*, below), opening with a bold headline
  paragraph as 0.18.5's does (0.18.6's opens with a bullet) — the landing's facts script reads it — and saying that the hook judges more now, so `--install-hook`
  runs again (RV-2160); both setup pages `--branch v0.19.0`.
- **The notes:** `ADOPT.md` and `ADOPT.de.md` name `v0.19.0` and the checksum of the final `shoalmark.py`, computed last, after
  every merge that touches it, the switch's D2 included; the Reviewer checks it against the tagged file.
- **Shipped:** the trackers that move to `Shipped` at the cut, each naming its commit — the release Builder's list, approved by
  the Owner.
- **The first public beta** (the Owner's ruling, 2026-10-01): v0.19.0 is shoalmark's first official release, published on
  GitHub Releases as a pre-release; the tag stays `v0.19.0`. The 0.19.0 section's bold headline names it the first public beta —
  the release notes and the landing's release line read that line.
  The headline, as the Owner wrote it (the ids outside the bold, so the landing shows only the sentence): **shoalmark 0.19.0
  is the first public beta: the gate refuses a *done* without a commit behind it, the first screen speaks to the person who owns
  the repository, and a new English note, `ADOPT.md`, goes to their agents** (FM-005, FM-006, FM-024 — with FM-040, FM-041 and
  FM-032). The Owner configured apart, several identities and `From:` stay in the bullets.
- **The release day** (the Owner's ruling, 2026-10-01): the Owner releases v0.19.0 today, 2026-10-01. The CHANGELOG's heading
  carries that date, and the landing's footer says *v0.19.0, released 1 October 2026 —* and the headline from it; the player stats stay as read at
  the cut `c830470`; `shoalmark.py` is untouched, so the notes' checksum stands. After the stats commit, the Owner's cold audit,
  the full local run and the bundle's final review start at once; the Owner opens the pull request after the final review's
  verdict, as a draft. The final review's findings and the Owner's rulings on them go in one fix round, the cold audit's in a
  second, small round on top; the pull request stays a draft until both are in, so CI runs once, on the final head, and the
  final review's scoped check covers both rounds. The merge waits on CI and the cold audit's verdict. If the bundle is not merged
  by 22:00 CEST, the date goes back to 2026-10-02 and the tag moves to the next morning.
  **Moved** (the Owner's ruling, 2026-10-01, evening): v0.19.0 is not tagged on 2026-10-01; `main` carries the bundle untagged
  (`d9c154b`). The release day is 2026-10-02, the tag before 09:00 CEST, or later if a check needs it: the CHANGELOG's heading
  carries 2026-10-02 and the landing's footer *v0.19.0, released 2 October 2026 —*; the player stats stay as read at the cut.
  **No date** (the Owner's ruling, 2026-10-02, night): v0.19.0 is tagged when it is done (*The release bar*, under *The
  board's refresh, from a trusted copy*); the CHANGELOG's heading and the landing's footer carry the day of the tag.
- **The Owner's run sheet** — `work-tracker/evidence/FM-006/release-v0-19-0-owner-run-sheet.md`, about 40 lines of numbered
  copy-paste steps, each with its expected output and one line to paste back. Before the tag: `gh repo edit` with the site's
  description line, the homepage `https://shoalmark.github.io/shoalmark/` and topics (proposed there, the Owner's to set), and the
  manual upload of `docs/assets/preview.png` as the repository's social preview. After the tag: from a clean checkout at
  `v0.19.0`, `SHA256SUMS` for `shoalmark.py`; the notes — the 0.19.0 section verbatim and three lines (install pinned to the tag,
  `--install-hook` again, the checksum), generated, never committed; `gh release create v0.19.0 --prerelease --title "shoalmark
  0.19.0 — public beta" --notes-file <notes> shoalmark.py SHA256SUMS`. The Auditor verifies the published assets against the tag.
- **In this beta** (the Owner's ruling, 2026-10-01; built while the bundle waits for the switch; the bundle's final review
  covers it, no render round). English: *Not a migration tool: it imports no ticket system and starts from your repository's own
  work. A path for a fleet that already runs a system of its own is filed, not built.* · *For one person in charge and their agent
  fleet. Several people in charge are not tested in this beta; support for them may come later.* · “Not proof that work is right.
  The gate refuses a *done* without a commit behind it. Whether that commit did the job is what a review is for.” German (*Sie*):
  *Kein Migrationswerkzeug: Es importiert kein Ticketsystem und beginnt mit der eigenen Arbeit Ihres Repositorys. Ein Weg für eine
  Flotte, die schon ein eigenes System hat, ist erfasst, nicht gebaut.* · *Für eine Person mit dem letzten Wort und ihre
  Agenten-Flotte. Mehrere Menschen in der Verantwortung sind in dieser Beta nicht getestet; das kann später kommen.* · *Kein Beweis,
  dass die Arbeit stimmt. Das Gate lässt nichts ohne Commit dahinter als fertig durch; ob der Commit tut, was er soll, klärt ein
  Review.* — on the landing's start section in place of *…filed (FM-026) and coming*, untrue since FM-026 is Parked; in
  `docs/index.md` and `docs/de/index.md` under *What it is not* / *Was es nicht ist*, as *In this beta:* / *In dieser Beta:*; in
  the README after *What is the direction*. Before *Tell your Owner so and stop here* in `ADOPT.md`: *If your project has several
  people in charge, or a large ticket system to move, this beta is not for it yet.*; in `ADOPT.de.md`: *Wenn in eurem Projekt
  mehrere Menschen entscheiden oder ein großes Ticketsystem umzuziehen wäre, ist diese Beta noch nichts für euer Projekt.* *The
  Planner's reading:* the same untrue sentence in the two start pages' *You lose nothing* paragraphs (`docs/index.md:63`,
  `docs/de/index.md:65`) goes with the landing's.
  A fourth line, the Owner's ruling of the same day, wherever the three stand (the landing's box, the README, both start
  pages) — as built, with `git` as code (`ed58291`) and the ending of the final review's RV-2262 (the Owner's ruling, the same
  day: signed answers need only `git`): “Made and tested on `git` with GitHub. Subversion passes the test suite but has not been
  used in real work; signed answers need `git`, and the pull-request queue `git` and GitHub.” / “Gebaut und erprobt mit `git` und
  GitHub. Subversion besteht die Test-Suite, ist in echter Arbeit aber noch nicht erprobt; signierte Antworten brauchen `git`, die
  Pull-Request-Warteschlange `git` und GitHub.” In both notes *Tell your Owner so and stop here* / *Sagt das eurem Owner und hört
  hier auf* comes right after the *not for it yet* line (`ed58291`), and the Subversion line follows in a paragraph of its own:
  `ADOPT.md` *On Subversion it passes the test suite but has not been used in real work: say so in your report.*; `ADOPT.de.md`
  *Unter Subversion besteht es die Test-Suite, ist in echter Arbeit aber noch nicht erprobt: Sagt das in eurem Bericht.* — the
  capital after the colon, a whole sentence following (the final review's RV-2265, the Owner's ruling). The Reviewer checks the
  German, and that every clause holds at the tip. The cold audit's round rewrites the fourth line and the notes' Subversion
  paragraph once more (below, *Subversion*).
  The Owner approved the start section's render (`start-390.png`, `start-1440.png`, `b2683f2`); on desktop the box's text is
  capped at about 80 characters wide, to read faster — the Owner's cosmetic suggestion, taken.
- **Carried in from the reviews:** RV-2161 (FM-005's check: one test's three attempts share a history), RV-2162 (FM-005: one line —
  with the tool's root below the repository's top the hook never runs the gate), RV-2170 and RV-2171 (the `From:` fix: FM-024's
  PR 139 paragraph, `--help`'s order), RV-2184 (`--key`'s help: the first word cut to five characters).
- **Every public line stays true for two paths** (the Owner's ruling, 2026-10-01): a phone app, and a hosted path a person opts
  into — never a requirement; and no line ties shoalmark to one forge. Nothing is announced. One commit on the bundle, before the
  final review, with these texts as written:
  - *The rewording.* The landing's ticker, both copies (`overrides/landing.html:517–518`), in place of its first three items:
    “needs no server and no account · ids you can say out loud”. `docs/index.md:72`: “shoalmark needs no server and no account,
    and its ids are ones you can say out loud, like FM-012.” `docs/de/index.md:77`: “shoalmark braucht keinen Server und kein
    Konto, und seine IDs kann man aussprechen, etwa FM-012.” `README.md:40`: “It needs no server, no database and no dependency
    beyond Python 3.9.”
  - *No network.* `ADOPT.md:11`: “(standard library only, no dependency, needs no network: online, it reaches your repository's
    host through git, and through gh for the pull-request queue)”. `ADOPT.de.md:11`: “(nur Standardbibliothek, keine
    Abhängigkeit, braucht kein Netz: Online erreicht es den Host eures Repositorys über git und für die
    Pull-Request-Warteschlange über gh)” — *Online* upper case after the colon (the final review's RV-2265, the Owner's ruling).
  - *The way back* — amended the same day, in one more commit before the final review: everything that calls the tool goes
    first, the line added to a hook of one's own included (the installer leaves an existing hook alone and prints that line to
    add to it); and amended again in the final review's fix round (RV-2263, the Owner's ruling): the hooks folder is the one
    `core.hooksPath` names where it is set, and the text says what deleting the tool first does — post-merge and post-checkout
    hooks left behind refuse no commit. The way-back item in each note: “Way back: first remove from your hooks folder
    (`.git/hooks/`, or the one `core.hooksPath` names) everything that calls `tools/shoalmark/shoalmark.py`: the hooks marked
    `# shoalmark`, and the line you added to a hook of your own (on Subversion, the `tsvn:` hook properties). Delete the tool
    before that, and commits are refused. Then delete `tools/shoalmark/`, `shoalmark.toml` and the shoalmark block in
    `AGENTS.md`. The tracker folder can stay: its entries are plain Markdown.” / “Rückweg: zuerst aus eurem Hook-Ordner
    (`.git/hooks/` oder dem, den `core.hooksPath` nennt) alles entfernen, was `tools/shoalmark/shoalmark.py` aufruft: die mit
    `# shoalmark` markierten Hooks und die Zeile, die ihr einem eigenen Hook hinzugefügt habt (unter Subversion die
    `tsvn:`-Hook-Properties). Löscht ihr das Werkzeug vorher, werden Commits abgelehnt. Dann `tools/shoalmark/`,
    `shoalmark.toml` und den shoalmark-Block in `AGENTS.md` löschen. Der Tracker-Ordner kann bleiben: Seine Einträge sind
    einfaches Markdown.”

  The Reviewer checks the German and runs the way back in a scratch repository — the old order, the text as written, and a
  repository whose own hook carries the added line; the Auditor verifies each commit when it lands.
- **The cold audit's round** (the Owner's rulings, 2026-10-01): the second, small fix round, on top of the final review's,
  carries the cold audit's findings — its report on `1c62b13`, *TAG AFTER FIXES*: F1 P1, F2–F5 P2, F6–F8 P3 — the Owner's
  ruling on Subversion, and two items the first round found.
  - **Subversion:** anyone may try it; it is not guaranteed and not claimed; it appears only in the qualified lines. The texts,
    as written — the landing's ticker, both copies: “git and subversion” becomes “made and tested on git”. `README.md:17`: “—
    with git, on Windows, macOS and Linux, in any language.” `docs/index.md:73`: “Runs with git on Windows, macOS and Linux.”
    `docs/de/index.md:78–79`: “Läuft mit git auf Windows, macOS und Linux.” `ADOPT.md:14`: “It runs with git on Windows,
    macOS and Linux (CI proves all three).” `ADOPT.de.md:14`: “Läuft mit git auf Windows, macOS und Linux (CI beweist alle
    drei).” The fourth *In this beta* line, in the README, `docs/index.md` and the landing: “Made and tested on `git` with
    GitHub. Subversion passes the test suite but has not been used in real work: try it, without a guarantee. Signed answers
    need `git`, and the pull-request queue `git` and GitHub.” — in `docs/de/index.md`: “Gebaut und erprobt mit `git` und
    GitHub. Subversion besteht die Test-Suite, ist in echter Arbeit aber noch nicht erprobt: Probieren Sie es aus, ohne Gewähr.
    Signierte Antworten brauchen `git`, die Pull-Request-Warteschlange `git` und GitHub.” The notes' Subversion paragraph,
    which also closes F5, says F1's cost too (the Owner's ruling, the same day) — `ADOPT.md`: “On Subversion it reads its
    history from the server through svn, so offline its checks refuse; it passes the test suite, but it has not been used in
    real work and comes without a guarantee: say so in your report.” — `ADOPT.de.md`: “Unter Subversion liest es seine
    Historie über svn vom Server, offline lehnen seine Prüfungen deshalb ab; es besteht die Test-Suite, ist in echter Arbeit
    aber noch nicht erprobt und ohne Gewähr: Sagt das in eurem Bericht.”
  - **F1, P1, fixed now:** on Subversion, a done check that cannot read the history it needs refuses and says why; it never
    passes unread. The test is the cold audit's control: a committed `Shipped` tracker with no revision behind it exits 4 when
    connected, and 4, not 0, with the server stopped or the network denied. `shoalmark.py` changes, so its SHA-256 is computed
    again last, and both notes carry the new one. If F1 is not through the scoped check and the full local run by 20:30 CEST,
    the Owner decides between disclosure and a slip.
  - **F2:** the check at `test_shoalmark.py:564` clears the harness's variables (`CODEX_THREAD_ID` and the like) before it
    commits, so the suite passes inside Codex.
  - **F8:** `ADOPT.de.md:5` opens “**An Claude, Codex und alle, die das lesen:**”.
  - **F4** is closed by RV-2262 (`da144ef`). F3, F6 and F7 go after the tag (the list in *What a stranger meets first*).
  - **The board's link** (the Owner's ruling, the same day; `shoalmark.py` changes in this round anyway): when the default run
    or `--html-only` writes the board, the tool prints one line with the board's clickable file link — “board:
    file:///…/work-tracker/index.html” — correct on Windows, macOS and Linux; never in `--print-written`'s output, which the
    pre-commit hook pipes into `git add` as paths. Tests: `--html-only` prints the link and it names the written file;
    `--print-written`'s output is unchanged. One CHANGELOG line in 0.19.0. The notes' checksum is computed after this and
    F1, last.
  - **F1's cost is accepted** (the Owner's ruling, the same day): offline, on Subversion, a repository with a `Shipped` tracker
    gets exit 4 from `--check` and the default run; the notes' Subversion paragraph (above) says so.
  - **The second fail-open, fixed now by the same ruling** (found while F1 was built): when `svn blame` fails, the rights check
    refuses and says why; it never passes unread. F1's unreadable error is reused. The test, in F1's control style: a seat's
    `close`, `answer` or `triage` change judged with blame failing exits 4, not 0, and passes connected where it should. Then
    the notes' checksum is computed again, last.
  - **The scoped check's three** (the Owner's rulings, the same day, on the final review's scoped check at `3ed5268`):
    RV-2267, *option A* — where the newest revision cannot be read and nothing is pending, the gate refuses and says why, so
    *offline its checks refuse* holds exactly; then the notes' checksum again, last. RV-2268, with A — `CHANGELOG.md:33`
    reads “…, else the newest revision, read from the server — where it cannot be read, the gate refuses and says why.”
    RV-2269 — the reference lines that name Subversion stay; the fourth line and the notes carry the qualification.
  - **The stopping rule** (the Owner's ruling, the same day): after A, no further Subversion finding holds the tag unless it
    also breaks git; those go to 0.19.1.
  - **A private security report, P1, fixed before the tag** (the Owner's ruling, the same day): after a checkout or a merge,
    nothing shoalmark installed runs. `--install-hook` no longer writes `post-checkout` or `post-merge`; run again, it
    removes the two it wrote before (marked `# shoalmark`) and says so. `--html-only` never runs the deriver. Tests: the
    checkout case after `--install-hook` runs nothing; a re-run of `--install-hook` removes the old `post-*` hooks; the way
    back and the hook tests follow the new count. One CHANGELOG line in 0.19.0: “The installed hooks no longer run anything
    after a checkout or a merge, and `--html-only` no longer runs the deriver; run `--install-hook` again after upgrading to
    remove the old ones.” Commits and records name it a private security report: no reporter, no exploit recipe. Then the
    notes' checksum again, last; the final review's scoped check runs the checkout case; the final full run on that head;
    and the Owner marks the pull request ready. The report's other findings go to 0.19.1 through private advisories, not
    into public trackers.
  - **The private security report's second round** (the Owner's rulings, the same day): `docs/setup.md:75` and
    `docs/de/setup.md:76` drop “and checkout” / “und Checkout”. The code's comments stay as written — each says in one
    sentence why the code refuses, with no steps and no payload — and `shoalmark.py` does not change again. `lefthook.yml`'s
    `post-merge` tracker-board command goes: this repository is where outside forks arrive. The CHANGELOG line gains, at its
    end: “; if you added a line calling `--html-only` to a post-checkout or post-merge hook of your own, remove it.” Docs,
    config and the CHANGELOG only, so the checksum `22cd0e9e…` stands. The final review's scoped check covers this round;
    then the final full run, and the Owner marks the pull request ready. Two more lines follow, in one commit (the Owner's
    rulings, the same day): `README.md:284` reads “put back on the branch they started on, the board is rebuilt by the
    command itself (`--html-only`) where nothing else rebuilt it, and the command says which.”; `.gitignore:1` names “the
    board”, no longer *built on every checkout*. Then the final review's one verdict and the final full run on that head.
  - **The board's link's test, on Windows** (the Owner's ruling, the same day, on CI at `5ffa3d2`): the product is right; the
    test is wrong. `test_shoalmark.py:165` parses the whole printed line as the URI; it strips the `board: ` prefix first,
    and the read-back is strict — the path parsed from the URI equals the board file it wrote, on every OS, and the check
    fails on POSIX too before the fix. Test only: `shoalmark.py` and the notes are untouched, so the checksum `22cd0e9e…`
    stands. The final review checks that one change; CI on the new head runs every suite, so the local full run is skipped;
    the Owner merges when CI is 9/9.
  - **The board's refresh, from a trusted copy** (the Owner's ruling, 2026-10-01, evening; a private security report):
    refreshing the board after a pull, a merge or a checkout is a required feature, and it comes back in a form no branch
    can abuse.
    - *The design: a trusted copy that only reads.* The `post-checkout` and `post-merge` hooks run a copy of the tool kept in
      the common git directory, shared by every worktree and outside any working tree. Only `--install-hook` writes or
      replaces it, and only from a pinned copy whose files pass their checksum check; where the repository has no pinned
      copy, from the working tree's tool, and it says so. That run executes nothing from the tree — no deriver, no other
      program, nothing imported from it; read-only git only — runs as `--html-only` and prints the board's link. It reads
      only regular files inside the repository: the tracker folder must resolve inside it, and symlinks are not followed.
      It writes only the board's files inside the tracker folder, never through a symlink and never over a file git
      tracks. Everything rendered from a tracker is escaped for where it lands (HTML text, attributes, script data); links
      are limited to safe kinds, and `javascript:` and `data:` are refused. Where the repository pins another version than
      the copy's own, the hook still refreshes and prints one line: “the hooks' copy is <its>, the repository pins
      <pinned>: run --install-hook”. The hook never blocks a checkout or a merge; on failure it prints one line. The
      `pre-commit`, `prepare-commit-msg` and `commit-msg` hooks keep running the working tree's tool.
    - *Added the same evening* (the Owner's rulings): `--install-hook` says which commit and branch it copied the trusted
      copy from, and warns, without refusing, where that is not the repository's default branch — the PIN it checks
      against comes from the same tree. The board's run ends itself after 35 seconds, so a checkout or a merge never waits
      longer for it. The board's link prints only for a board the run wrote; where `index.html` is tracked or a symlink,
      the refusal prints instead. The board and its tracker pages reload themselves when the tab becomes visible again,
      keeping the scroll position, and never while a dialog is open or a field has input; nothing new is loaded — no
      polling, no second file, no server.
    - *This repository:* lefthook reads `lefthook.yml` from the working tree, so lefthook keeps its commit-time hooks —
      `pre-commit`, `prepare-commit-msg` and `commit-msg` — and runs nothing after a merge or a checkout; shoalmark's own
      hooks, with the trusted copy, do the refresh. After the merge, `--install-hook` on `main` writes them and the copy.
    - *Texts:* the CHANGELOG's line for the private security report is replaced — the checkout and merge hooks run a copy
      of the tool kept in the git directory, which runs nothing a branch brings; run `--install-hook` on your default
      branch again after upgrading. The setup pages say the board is rebuilt on every commit, and on every checkout and
      merge with git; on Subversion, on a commit through TortoiseSVN or when the tool runs — no new Subversion hook in
      this change. The README's hooks section and `--help` name the copy and say to run `--install-hook` on your default
      branch. Both notes' way back also removes the copy in the git directory. The date goes back (*The release day*,
      above).
    - *Tests:* one for each case the report names, each a branch checked out or merged that must run nothing and write
      nothing outside the tracker folder; a version drift prints its line; a re-run of `--install-hook` replaces the copy;
      worktrees share it; `--install-hook` on a branch that is not the default prints its warning; a branch committing
      `index.html` gets no link; the board's template carries the reload, and no reload path loads another file.
    - *Order:* a new branch from `main` `d9c154b`, one pull request; built on 2026-10-01; the final review at critical tier
      (seats and security) comes first, and the pull request is opened, as a draft, only after it is cleared; a cold
      review by another model family and an outside check the Owner arranges, on 2026-10-02 from 07:00; then the notes'
      checksum, last, the full local run, CI 9/9, the merge and the tag. The scope is frozen: nothing new joins this
      build unless it is a security finding in this change; everything else goes to 0.19.1.
    - *RV-2300, fixed in this build* (the Owner's ruling, 2026-10-02, night, on the final review's finding): one rule —
      no hook shoalmark installs runs anything the tree brought. It replaces the design's last sentence and *This
      repository* above. Every hook shoalmark installs runs the trusted copy: `pre-commit`, `prepare-commit-msg` and
      `commit-msg` as well as `post-checkout` and `post-merge`; no hook runs the tree's tool. A hook runs the tree's
      deriver only if it equals the one accepted at the last `--install-hook`, whose checksum is recorded with the copy;
      a changed or new deriver is skipped in hooks, with one line: “the deriver changed: not run; run --install-hook to
      accept it”. Where the tree's tool differs from the copy, the hook judges with the copy and prints the drift line.
      Explicit runs — a person, an agent, CI — run the tree's tool as today. This repository: lefthook's `pre-commit`,
      `prepare-commit-msg` and `commit-msg` are replaced by shoalmark's own installed hooks, because lefthook reads
      `lefthook.yml` from the merged tree; developing the tool means installing the branch's copy deliberately, with its
      warning. Tests, each in a throwaway repository with the copy installed: a merge (clean and conflicted), a
      cherry-pick, a revert, a rebase and `git am`, each bringing a changed tool and a changed deriver — nothing from the
      tree runs, and no hook writes the copy; an accepted deriver runs, and a changed one is skipped with its line. Texts:
      the README's hooks section, the CHANGELOG's line for the private security report, and the notes' way back where it
      changes. Then the final review at critical tier of the whole change, the cold review and the Owner's outside check,
      the notes' checksum last, the full local run, CI 9/9, the merge and the tag — the tag waits for the reviews, not for
      09:00.
    - *The refresh after a pull* (the Owner's rulings, 2026-10-02, night): `git pull --rebase` with local commits, and
      `git rebase`, run `post-checkout` before the local commits are replayed and no refresh hook after, so the board
      would show the remote's trackers without the local ones. `--install-hook` also installs `post-rewrite`, which runs
      the copy as `post-checkout` and `post-merge` do. A cherry-pick, a revert, `git am`, `reset --hard` and `stash pop`
      run no hook that writes the board, and on Subversion nothing refreshes it after `svn update`: the README's hooks
      section says so in one line, naming `--html-only` as the rebuild; hooks for these are 0.19.1's. The reload keeps
      the filter, as it keeps the scroll position, and the search box no longer holds it back. Tests, one per operation,
      that the board after it equals a fresh `--html-only` of the tree: a switch, a pull fast-forward, a pull with a
      merge, `pull --rebase` with local commits, a clean merge, a conflicted merge at its resolving commit, and a squash
      merge. RV-2300's `git am` case is `git am` followed by the next commit: `git am` runs none of the hooks, and a
      cherry-pick, a revert and a rebase's replay run only `prepare-commit-msg`.
    - *No deriver in hooks* (the Owner's rulings, 2026-10-02, night, on the Builder's findings at `fc5f197`): it
      replaces R2 under *RV-2300, fixed in this build*. No hook runs a deriver; `--install-hook` accepts none, and the
      copy's record has no `deriver:` field. In a repository with a deriver, the commit hook leaves `INDEX.md` and the
      derived files as staged — it never rewrites them without the derived columns — and prints one line: the deriver
      runs only in explicit runs; run the tool before committing; CI's `--check` holds it. Tests: in a repository with a
      deriver, no hook starts it after a commit, a clean and a conflicted merge, a cherry-pick and a rebase, and
      `INDEX.md` is left as staged. `--install-hook` refuses a hooks folder that resolves, symlinks resolved, inside the
      working tree and outside the git directory, with one line naming the README's hook-runner section; the default
      `.git/hooks` and a folder outside the repository stay accepted. A relative `core.hooksPath` resolves in the
      working tree of whichever worktree the hook runs in, so `--install-hook` judges the folder against every working
      tree `git worktree list` names, not only its own. Tests: an in-tree `core.hooksPath`, a symlink into the tree, the
      default, and a linked worktree with a relative `core.hooksPath`. The 35 seconds stay; the commit's refusal line
      names `SHOALMARK_BOARD_SECONDS` as the way to raise it. The warning off the default branch names a PIN only where
      the repository pins one. The drift line printed more than once on one commit is 0.19.1's.
    - *The fix round after the critical review* (the Owner's rulings, 2026-10-02, morning, on reviewer-80's findings at
      `1b65331`): in every run, the tool reads a tracker, its configuration and every file of the tree only as a regular
      file inside the repository, following no symlink. The board's refresh skips such a file with its line, as now;
      every other run — a hook's, or one started by hand — refuses in one line naming the file. Tests with an inert
      marker, for a hook's run and a run by hand. `--install-hook` refuses, in one line and writing nothing, where any
      git configuration value comes from a file inside a working tree, judged as the hooks folder is; with its test. The
      checks assert the filed lines as literal text, not the tool's constants; in the final recorded pass of the
      negative controls, the checkout and merge hooks' controls run against v0.18.6, whose hooks ran the tree's tool,
      and a row whose feature is new, or that checks something must stay accepted, says so. RV-2304: `AGENTS.md`'s
      *Checks* line becomes the Owner's text — “**Checks:** commits run shoalmark's own hooks, from the copy of the tool
      in the git directory: the session, tracker and judgement gates. Before committing Python, run `python3 -m
      py_compile` on the changed files and `python3 -u test_core.py`. Both full suites run in the required GitHub matrix
      for non-draft PRs when opened, updated, reopened or marked ready, on release tags, and when dispatched by hand.
      The Owner authorized these PR triggers on 2026-09-29 and these hooks on 2026-10-02. Say when a tag is due; never
      create one.” RV-2305, RV-2306 and RV-2307 are 0.19.1's. implementer-81 builds the round on Opus; then
      reviewer-80's scoped check and READY.
      Added to the round (the Owner's rulings, the same morning): every run writes only regular files inside the
      repository, never through a symlink, and otherwise refuses in one line, with a test; a deriver that is a symlink
      is refused in one line. One check's older Windows guard and the drift line printed more than once are 0.19.1's.
      RV-2313 (the Owner's ruling, the same morning): the configuration check judges the target of every include
      setting, conditional ones included, as written — resolved from the file that holds it, whether or not its
      condition holds and whether or not the target exists when `--install-hook` runs; a target inside a working tree is
      refused like any other configuration file there. Tests: a conditional include into the tree, and an include whose
      target does not exist yet.
      Also in this round (the Owner's rulings, the same morning, on the Builder's findings at `83eb0dc`): the tool's
      comments that call the Owner “he” or “his” say they/them — comments only. For 0.19.1: `--init`'s files written
      before a refusal; and, P3, the hooks-folder and configuration checks compare paths case-sensitively on macOS,
      whose default file system is not — their inputs come from the person's own configuration, never a branch.
      RV-2314 and RV-2315 (the Owner's rulings, the same morning, on reviewer-80's check at `f88546f`), in this build:
      `--vendor` reads only the files it copies, each judged by the reading rule; the configuration check judges the
      settings each worktree reads, its own configuration included, as the hooks folder is judged in every worktree. One
      commit each, with its test. On RV-2315 (the Owner's ruling, the same morning): a worktree that `git worktree list`
      marks prunable — its folder gone — is skipped by the configuration check, never refused and never a crash; it has
      no tree, and no hook runs there. Test: `--install-hook` succeeds beside a prunable worktree.
      RV-2316 (the Owner's ruling, the same morning, on reviewer-80's check at `4087e23`), in this build, with two more of
      the same rule (the Owner's rulings): the gate reads only the files a vendored copy's PIN names inside the copy, and
      a name outside it is refused in one line, unread; `--triage` skips a submodule path from `.gitmodules` that resolves
      outside the repository, and runs no git there; a destination a person names (`--vendor`, `--brand --from`, a
      calendar file) is resolved once, where it is named, and the write rule then judges every file under the resolved
      folder. One commit and one test each, each test failing beside `4087e23`'s tool. RV-2317 (the Owner's ruling, the
      same morning, on reviewer-80's check at `e8d2eea`), in this build, a fourth commit: `--brand DIR` without `--from`
      judges each file as named and under the resolved folder, before the folder is made; one more row in the
      destinations test, failing beside `4087e23`'s tool.
      *The Windows round* (the Owner's rulings, the same day, on CI run 36998106048 at `90abab9`, red on both Windows
      jobs): the three checks that fail there and the stop of the suite are fixed, each fix saying whether the tool or
      the test was wrong; a check that cannot observe on Windows skips there, visibly, with its reason, and no control
      may pass. `pin_report()` reads the running copy's PIN and VERSION under the reading rule, with a test. Notes: the
      CHANGELOG's line on commits says what `AGENTS.md:52` says, and 0.19.0 gains two security lines, as the Owner wrote
      them. Then reviewer-80's scoped check, the push, READY, and one CI run the Owner dispatches; the ledger names it.
    - *The release bar* (the Owner's rulings, 2026-10-02, night): v0.19.0 is tagged when it is done, with no date — a
      release whose next outside security scan finds nothing new, and where every finding of the private security report
      is fixed or visibly next.
      - *Added to this build — the signed identity:* a `signed` identity is an email, and it verifies by SSH only: the
        commit's signature is SSH, good under the default branch's signers file as today, and its principal equals the
        email exactly. A GPG signature on a signed line is refused with one line: “sign with SSH; GPG returns with a
        fingerprint binding”; so is any other kind that is not SSH. A `signed` identity that is not an email — under
        `owner`, `[seats]` or `answerers` — is refused at configuration, exit 1, with one line on how to migrate. Tests:
        a commit under the Owner's email signed with another trusted key is refused; a principal that contains the email
        without equalling it is refused; the exact one passes; a name-only `signed` identity is refused at
        configuration; a trusted GPG key whose user ID carries the Owner's email is refused. Texts: README §*Seats* and
        the `answerers` row, the signing pages (SSH for signed lines), the setup pages, and one CHANGELOG upgrade line.
        The change gets no advisory of its own, so the line says it is a security fix and opens with the reason:
        “Security, from a private report: a signed identity configured by name, or a signer whose identity merely
        contained the address, could let another trusted signer's commit count as that identity's. A signed identity is
        now an email address only, matched exactly against the SSH signer; …”, then the migration step as built. FM-037
        records its part as fixed here. `main`'s history is replayed under the new rule: every judgement of a signed
        line or a signature, by the tool before and after — no new refusal, GitHub's own PGP-signed merge commits
        included; the result is a row of the ledger.
      - *Added to this build — hook runners:* the README's entries for a repository with its own hook runner run the
        trusted copy, and the text says plainly that a hook runner reads its configuration from the tree, so a merged
        branch's configuration runs whatever it names; shoalmark's own `--install-hook` is the safe default. This
        repository's `lefthook.yml` goes: before its commit, lefthook's three commit-time hooks on the Owner's machine
        are set aside and `--install-hook` from this branch writes shoalmark's hooks and the copy, which judge every
        worktree's commits until `--install-hook` on `main` after the merge. The tests run explicitly and in CI.
      - *Next, no date:* the report's two remaining findings are 0.19.1's first work, in the private advisory set only.
      - *Evidence before the tag:* a ledger in `work-tracker/evidence/FM-006/` — one row per security claim in the
        CHANGELOG, the README and the notes, each naming its test, an executed check, or “cut”; no attack steps — built
        by the Planner after the code lands and checked by reviewer-80 and the Auditor; reviewer-80's critical review of
        the whole change; a cold review by another model family, with no time limit; the Auditor's re-run of the
        report's reproductions on the final head and of the common security scanners, every hit triaged.
      - *The tests:* every finding fixed in v0.19.0 has a test in `test_shoalmark.py` that must pass in full CI on the
        final head. The ledger shows for each security test the CI jobs it ran on, and where it skipped, with the
        reason; no security test may skip on every job, and nothing the release notes claim may rest on a test that ran
        on only some systems unless the claim says which. Each security test's negative control — the test failing
        against the tool as it was before its fix — is run once and recorded. The history replay, the scanners and the
        Auditor's re-run of the report's reproductions are rows of the ledger with their results. The report's two
        remaining findings get their tests with their fixes in 0.19.1, not before.
      - *Gate:* no open P1 or P2; every finding of the report carries a status; the advisories say only what was tested.
        Then the notes' checksum, last, the full local run, CI 9/9 and the merge.
      - *Order* (the Owner's rulings, 2026-10-02, night; it replaces the orders above): after the Builder's last push —
        the signed identity and the tests' record in — reviewer-80's critical review of the whole change, `d9c154b` to
        the final head, until READY with no open P1 or P2; then the draft pull request, which the Owner opens, and CI
        9/9 on it, dispatched by the Owner by hand; then the ledger, which names the CI run it reads (its URL) and the
        commit it ran on — every commit after that one is evidence or notes only — with reviewer-80's scoped check of
        it; then the Auditor's final-head checks — the commits against the rulings, the ledger, the re-run of the
        report's reproductions and the scanners; only then the cold review, on a head nobody expects to change: a fix
        after it gets reviewer-80's scoped check and the Auditor's verification, and a second cold round only for a P1.
        Then the notes' checksum, last, the full local run, and the final CI from marking the pull request ready for
        review, with no second dispatch; the merge and the tag.

  The final review's scoped check covers both rounds and runs F1's control; then the full local run. The second fail-open is
  built on top of `3ed5268` while that check and the full run continue there as the early warning; then a scoped check of the
  delta and the final full run on the final head; then the Owner marks the pull request ready. If this is not through by 20:30
  CEST, the Owner decides between disclosure and 0.19.1. After A: the final review's scoped check of A and the CHANGELOG line,
  the final full run on that head, and the Owner marks the pull request ready. The two items from the first round:
  - `docs/signing.md:240` and its German twin `docs/de/signing.md:261–262` name the seats that hold `answer` beside the Owner,
    as RV-2261's fix does on the triage pages. *The Planner's reading,* in RV-2261's words: “Where your `owner`, or a seat that
    holds `answer`, is not marked `signed`, …” / “Wo Ihr `owner` oder ein Sitz mit `answer` nicht `signed` ist, …”.
  - `docs/requirements.md:21` and `docs/triage.md:106` say “the Owner's signed answer”. The check's name at
    `test_shoalmark.py:3051` stays: it is a test name, not a page.

## Signals

- 2026-09-30 · the Owner's first pitch, through the Principal (paraphrased, no names) · a firmware developer took one idea from it: developer and tester work from one ground truth — requirements in the repository, tested as a contract, not by reading the implementation, because test plans drift; the same day a requirements folder went into that firmware repository, regulatory requirements first, the easiest to formulate, and two defects came out of it; a trial is planned for the weekend, most likely run by an agent · source: the Owner's word of 2026-09-30 · the layer is FM-042, Stage 0 its convention

## Acts

**2026-09-30** · done — Public repository: https://github.com/shoalmark/shoalmark/ · Documentation: https://shoalmark.github.io/shoalmark/ · Migration merged: 80d0811974a1d39b679cfd374c80109ddd62acce · Independent migration review: 5e26a88e75b992c243148c2786e44f443e0f7437 · Port-evidence cleanup merged: b041cb2dca136623ee9160d74ae5b39b0f1a7ba2 · Publication gates merged and deployed: 792dbca9caa74629d12645dcc5ae7f55a2bb2340 · Independent publication review: b9b3971c21f3b84f332249bbc976fe9af7580f0d · Scoring completed; publication preceded scoring under my previously recorded risk acceptance. · this repository, client names and the parent's traces public, the port evidence deleted — after the scoring, gates held · holgo99
## Ship log

| Date | Event |
|---|---|
| 2026-09-30 | **What a stranger meets first in v0.19.0 — filed** by the Planner on the Owner's ruling of that day, as one slice of this tracker (*What a stranger meets first — v0.19.0*): the human lead on the landing and the German start page, the tagline where agents read, an English note beside the German one, the fleet as a section of its own, the Owner not a seat — D2 with the `[seats]` change of 2026-10-01 — and the last gendered pronouns on current pages. The two screens it follows are merged into the branch (`a410aef`, `87985b6`). |
| 2026-09-30 | **Wording pass built — rewording, not product growth** (the Owner's rulings 3 and 4 and the renames that followed, 16:51 CEST): they/them/their for the Owner and any person; seats stay *it*, one sentence in AGENTS.md; seat names English only; Planner and Builder in prose, the `[seats]` keys and addresses unchanged. Lines of the Implementer's change `origin/main..77f7722`, records left out: product 140 added, 136 deleted (the tool and its test 62 of each, string assertions only; AGENTS.md's one sentence and three setup/README sentences on the keys the only new prose); records +8 (the CHANGELOG bullet 7, this row 1). |
| 2026-09-30 | **A signal filed** under *Signals*: the first pitch's one idea, requirements in the repository tested as a contract; the layer is FM-042, Stage 0 its convention. Nothing on the ask changes. |
| 2026-09-30 | The check outputs `checks.json`, `checks-r3-before.json` and `facts.json` of the start page replaced by their summaries under the Owner's ruling of 2026-09-30 (*if a check output regenerates, keep only its summary*): each regenerated by its results and is held at `08798a8`; FM-032's page names the rule. |
| 2026-09-26 | **Slice L built — the landing page is the site's start page**, by the GtM seat on `fm/006-the-landing-page` (off slice A's verdict tip `b9644b7`; main merged at `bef2a1e`, PR 93), on the Owner's word of 10:25:41 and his rule of 16:0x, *the mock as-is*: `9307cf8` the mock as a template `docs/index.md` selects, full-bleed, no site chrome, byte for byte; `ab69afb` R3 (`.name` and `.fig` above `.crt`: 0.93 % of the chart's pixels at 1440 px, the smallest change that meets 4.5:1 — his to strike, rendered before and after) and R4 (18 of 23 reports now their hook's first sentences, verbatim); `e26c648` the facts dated — the release (v0.18.4), the wrecks (24: FM-038 filed after the mock, placed by rule; FM-034 to FM-036 raised) and the board's excerpt read from main at `bef2a1e`, 18:00 CEST, said in the page's foot; `a0daf0c` the fonts in one Google Fonts load, the family from `[project.theme.font]`, the mock's six faces, the same pixels; `cb49101` the German start page's one line; `08798a8` the renders at 1440, 1024 and 390 px, the checks and the evidence README (`evidence/FM-006/landing/start-page/`, not `site/`, which the root `.gitignore` matches). No workflow, no `shoalmark.py`, no `brand/`, slice A's stylesheet untouched. One Reviewer pass due (docs tier); the Owner opens the pull request. |
| 2026-09-26 | **The home at the flip filed** — the Owner's word, through the Auditor seat, as pasted at 11:05:27, word for word in *Going public* (sha256 `19ca39d1794c67cf15e26399667d392cadc65fdb1c5c5d22fe44993277ad4ec5`): shoalmark is a tool, not a company; its home becomes a GitHub organisation `shoalmark`, the Owner its only owner, created by him now, free and empty. What it adds to the plan: at the flip, `holgo99/shoalmark` transfers into the organisation — the history, the signed commits and the pull refs move with it, and GitHub redirects the old URLs — and the same slice updates the vendoring sources and pins in PortDive, msr-lager and fb-sondermasch, `shoalmark.toml`'s blob links, the docs site's address (with the domain the GtM line settles), CI, and each seat's remote; then branch protection on main. Nothing moves before the flip; the ask and its options are unchanged. |
| 2026-09-26 | **The landing page made a requirement of v0.18.5 by the Owner's word (10:25:41), alongside the restyle; the themes' ask moved to FM-002** (raised the same hour on his *go*), so this tracker keeps its one ask, going public, which he answers now that v0.18.4 has landed. The seat's reading that the landing page is the site's start page is marked as such; where it ships is the 0.18.5 plan's. |
| 2026-09-26 | **A landing page mocked in the `shoalmark` theme** by the GtM seat on the Owner's word in chat: attract mode, a pixel chart of the German Wadden coast whose wrecks are this repository's 23 defects — tracker, filing commit, day, status, report — with v0.18.4, 1P for agents, 2P for people, the high scores and the register, every fact sourced in the evidence. `evidence/FM-006/landing/` (the page, four renders). Nothing built, nothing asked; nothing published outside the repository. |
| 2026-09-26 | **The board's header inline inside the graticule in both themes**, by the GtM seat on the Owner's word in chat of 09:23:58 (filed in the themes section, spelling normalised, the seat's reading marked; not a signed answer, and nothing on the ask changes): `shoalmark.css` takes the navy band and its drying line off the board's top — they stay the board's foot and the site's header and foot — and the mark, the name and the switch stand inside the chart's top border as `monochrome`'s, in the chart's ink on its ground, on the board and behind the dialog, both schemes; the tracker view, which shows no header on any board, starts inside the chart where `monochrome`'s does; the header's ten pairs measured, the lowest 5.41:1. `shoalmark`'s board, dialog, tracker view and foot re-made with the committed scripts, offline; `monochrome`'s and the sites' renders byte-identical. The themes pass's P3s fixed forward: R1 (`monochrome`'s foot 4.50:1 by day, no margin; the figures from 4.74:1; the sites' pairs from 4.74:1), R3 (a phone's 390px measured: the table scrolls to 505px themed, 905px today), R4 (*wear at most one; the ask says which, or none*; *a starter if the tool ships themes*); R2 a line for slice A; R5 left to the FM-033 pass. |
| 2026-09-26 | **The themes' drafted ask re-made before it reaches the board**, by the GtM seat on the Owner's word of 07:41:00 through the Auditor seat (AU-24; pasted by him at 07:55:40, sha256 `34ee13d1…`): the draft asked two things in one — whether the tool ships themes and which theme shoalmark's own board and site wear — and had no option for the cheap step. The ask, a ruling, now asks them apart; its three options each say both: the `shoalmark` theme worn and no themes shipped yet (85 characters), both themes shipped as starters and `shoalmark` worn (108), not yet — today's look, no themes shipped (84). The proposal is the first, disclosed as the GtM seat's: the cheap step, one Reviewer pass, and no release after 0.18.4 hands a vendoring consumer a theme before he rules it. `monochrome` is not offered as worn: the seat does not propose it. *The build is code* became *slice A is the brand layer; slice B is code*: slice A is `work-tracker/brand/theme.css`, two Plex Mono cuts and `docs/stylesheets/`, no `shoalmark.py` change; slice B only on his ruling. The three markup hooks are `shoalmark.py` changes, in neither slice as his word draws them; the pass places them. *What is true now*, the two themes' bullet and *How a theme is chosen* no longer state the tool's shipping as filed. The evidence's README carries the same words. Still a draft, raised when the going-public ask is answered. |
| 2026-09-26 | **The page re-made on its Reviewer's R3–R7** (`f4188ee`, NOT READY on `59febae`), in both languages: FM-007's raise quoted whole, *undermines: TRIAGE.md path 5, FM-033's answer* (R3); tier 2 as the signing page has it, stopping the accident while an agent that means harm can fake the prompt, and only tier 3 making the key the Owner's alone (R4); what a pass re-judges: its sheet lists work in progress not judged in seven days, new filings and raised trackers, nothing reacts to a path edit by itself, and a tracker judged this week keeps its tier until its next pass unless a raise names a path line (R5); the raise check named as the one place the tool reads the path's content, its line numbers only, beside `--triage`'s presence test and the guard's byte comparison (R6); the three lead-in sentences labelled (R7). |
| 2026-09-26 | **The page on his word in TRIAGE.md built** by the GtM seat after FM-037's guard merged (PR 83): `docs/triage.md` (*Your word in TRIAGE.md*) and `docs/de/triage.md` (*Ihr Wort in der TRIAGE.md*), one nav line each in `zensical.toml`, `uvx zensical build` green. What the file holds and what an edit changes, every claim labelled *the tool*, *review* or *the text alone* (DE: *das Werkzeug*, *das Review*, *nur der Text*); the term *your signed word* (*Ihr signiertes Wort*). Examples from this repository's record only: path line 3's rewrite (`fe36cc0`) and the independence line `--check` printed at `88c7b0c`; FM-035 P1 at `42f4eca`, P2 at `c8939e3` with path line 1 whole; FM-007's raise naming path 5, re-judged the same evening (`29466fc`, `c5696c5`); FM-022's village-library intent; FM-037's refusal of a seat's edit, run in a scratch repository and quoted as printed (`evidence/FM-006/triage-page/`, English and German), with the hook's refusal and the tier-0 limit shown (a commit signed with the Owner's passphrase-less key passes); what an edit does not do. The filing's review, R1 and R2 (P3) fixed: *21 open*; the section heading's times. |
| 2026-09-26 | **The themes narrowed to two, and the site added** by the GtM seat on the Owner's word: `monochrome` and `shoalmark` only, each for the board and the site, each drawing a nautical chart behind the page — a Mercator sheet of Neuwerk's Watt, its border graduated, its degrees and minutes figured — muted in `monochrome`. `catkin`, `bagels` and `seekarte` dropped (in git at `96aa05e`). The board's last line moved out of the chart into a foot band of its own. Evidence re-made: four stylesheets, 18 renders, 27 new contrast pairs, the figures absent from the accessibility tree. Nothing built; nothing published outside the repository, at his word. |
| 2026-09-25 | **The board's themes filed** by the GtM seat on the Owner's word: `monochrome` and `shoalmark` to ship as files in `brand/themes/`, `--brand DIR --from`; three more kept as mockups. Evidence: `evidence/FM-006/themes/` (five stylesheets, the rebuild script, 16 renders). The Auditor seat's hold lifted on his word; v0.18.4 not tagged. Nothing built. |
| 2026-09-25 | **The page on his word in TRIAGE.md filed** — the Auditor seat's line on the Owner's word, through him at 22:38:24, word for word (sha256 `be19a410…`): an English and German page on the intent and the current path and what an edit does, each claim labelled by what enforces it, worded by the GtM seat, every claim checked against evidence before the merge; built after FM-037 merges so *only you change it* is the tool's, with FM-007's tier-0 limit. |
| 2026-09-25 | **The Auditor seat's addendum to its go-public counsel, and its correction, filed word for word** through the Owner, before PR 77 merges — the addendum of 17:23:39 (sha256 as filed, after its opening line: `281f74bbe32c32f73ef993846f95f147b7f4be492ed251b97a081c3ea7932309`) and its correction to item 2 of 17:37:17, its own error (`a0b8244dbb6b1382d910df2dba91848db8cc8f53d34152d29b4a6d0d2f78ff01`). **A fourth gate**, in the addendum's words: the port evidence (`work-tracker/evidence/FM-001/port/`, six files on main) deleted or moved, as the Owner ruled on 2026-09-22 — the parent's ledger, `docs/work-tracker/evidence/FEAT-190/asks.md` row 10 (2026-09-22; the file's line 36); the act is this tracker's — the freeze allows no new one — named in *What is true now* too, its form picked by his answer, nothing deleted before it. **The count as found** at `9555d2c`, the Implementer seat's, beside the corrected one: 28 blob versions name the parent, 8 the tip's files and 20 older at 7 paths (5 still at the tip, 2 FM-002's before its move), 3 files naming it only in older versions — every number the Auditor seat's; the literal name a lower bound (3 of the 6 port files do not carry it). **The options re-made declarative** on the Auditor seat's wording (the Reviewer's R4): 119, 118 and 7 characters, the proposal the first; the condition leaves the option text — *if either may not be public, the second*, the Auditor seat's counsel, disclosed as such here and in *Going public*. FM-030 gains its 0.18.4 line: the move after an answer follows the picked option, not the kind alone. **Owed:** the parent's ledger row 47, an appended clause to match, in the parent's next ledger commit. |
| 2026-09-25 | Re-made on its Reviewer's R1–R3 before it reached the board: the ask is `action` (a yes is his hands), the condition on the proposal stands in the first option's text, the three gates are quoted in the counsel's words with the seat's gloss apart. The parent project's ledger row is corrected to the same text by an appended clause (its row had merged). |
| 2026-09-25 | Asked: when and how shoalmark goes public — a ruling; the proposal is the Auditor seat's counsel (through the Owner at 16:26:24, revising its 16:22:12 ask), disclosed as such and conditional on the client names being public; the three gates in the *Going public* section. The parent project's ledger row came first (`17daad27`, 16:27). |
| 2026-09-25 | The GtM seat's wording decision, on the Owner's tasking: *your signed word*, not *mandate* — *Mandat* reads bureaucratic and political in German, as his own counter-fact warned, while *your word* is a promise every owner understands and *signed* is what the tool checks; the German rests on the idiom *Ihr Wort gilt*. Stated once, high on the page, before the mechanics (`af5229e` English, `50a39b7` German); each claim tied to what v0.18.2 enforces, the tiers linked. The *9 of 13* and *200 merged unread* lines removed — both came from another project's record (`50a90e8`); in their place this repository's own count over its pull requests 1–69 (merged, without `answer/…`), method printed on the page — a commit adding or changing a file under `work-tracker/evidence/reviews/`, merge commits excluded, dated before the pull request was opened: 10 of 37 before the Owner's signed review rule (`ffa63b8`, 09-24 11:07), 12 of 15 after (the Reviewer's R1: the page first printed *adding*, which gives 9 of 37 and 9 of 15; corrected in `78b10da` and `9fd7837`). A commit's date is not its push: the forge's push events confirm the counted pull requests from 2026-09-24 05:18 UTC on and list none before (R3, on the page). The gate's refusal of an unsigned answer is qualified on the page: on git, with the owner's seat marked `signed`; under Subversion, the server-authenticated commit (R2). A Reviewer checks each claim against evidence before the merge. |
| 2026-09-25 | The Owner's finding of 09:52:49: the landing page names the mechanics, not the consequence — that agents act on his signed word and nothing else counts as it. His proposal and counter-fact recorded, the Auditor seat's assessment filed word for word (its three conditions: claim only what the tool enforces today, pair authority with the signature tiers, the GtM seat words it under this tracker with a Reviewer checking each claim; and the *9 of 13* measured line sourced — repository, window, method — or fixed, in the same change). The GtM seat's wording follows on this branch. |
| 2026-09-25 | A line under the freeze for 0.18.4, on the Owner's word of 09:21:19 (*I would like to have `site/` up-to-date after every pull so that I see locally how it is going to look when I deploy it* — spelling normalised): the local docs site is rebuilt as the board is — `post-merge` and `post-checkout` run the site build where a builder is found, `zensical` on the PATH or else `uvx zensical`, and where neither is found say in one line that the site was not rebuilt, never an error and never `sh: command not found` on every checkout (the Reviewer's R1: `zensical` is not installed on this machine, `uvx zensical build` is); `site/` stays gitignored, and the public site still deploys on a release tag only (his cost ruling, `docs.yml` — whose first-line comment still says *on every push to main*, a second line for 0.18.4). Until then, by hand after a pull: `uvx zensical build`, then open `site/signing.html`. |
| 2026-09-24 18:20 CEST | **The footer speaks the board's language.** The Owner (normalised): *"My board is English — why do I see German claims here?"* The German lines came from the Principal's brief, which carried the site's German page into an English board — the seat's error. The footer is now the English line he ruled at 07:51, *A Pricke on the Wadden flats keeps the fleet in the channel.*; a German board takes the D2 line. |
| 2026-09-24 18:16 CEST | **The tagline leaves the board's header on the Owner's word** (normalised: *"Let's remove the claim at the top — that one is agent-facing. The footer is fine."*): `labels.yaml` carries no `tagline`; the footer stays. The claim still opens the site's German page, where its reader is an agent. |
| 2026-09-24 17:48 CEST | **The Reviewer's R7–R9 at `3f4b4a4` fixed** (`31863fb`, 17:43; the second verdict is `6ab7681`, NOT READY): attribute values are read by a one-pass scanner, never a regex — numbers `-?digits(.digits)?`, one space or comma between two, ASCII, a budget of 200,000 steps for the file — so the Reviewer's `x="111 … !"` at 10 kB is refused in 0.2 ms (186 s at 170 B before); an id defined twice refuses the file, and every reference (`<use>`, mask, clip, paint) is followed as the browser draws it, ≤ 3 deep, ≤ 2,000 painted, counted as it goes. The grammar is stricter than SVG: a minifier's numbers (`.5`, `1e3`, `1-2`) are refused. This repository's wordmark passes as it is. |
| 2026-09-24 16:49 CEST | **The Reviewer's R1–R6 at `06d884e` fixed** (`a661c1d`, 16:44; the review is `552d6b4`, NOT READY): a wordmark is held to a grammar — an attribute list per element and a grammar per value, no `style`, no `class`, colours `#hex`/`currentColor`/`none`/a plain name, `(` only in `transform` and `url(#id)`; the `<use>` graph resolved first (no cycle, ≤ 3 deep, ≤ 2,000 drawn); the bytes checked before the parse (UTF-8, no BOM, no control character, no DOCTYPE); the depth walked without recursion, ≤ 32. One check per refusal; this repository's wordmark passes as it is. This row's time and the two below are git's: `06d884e` 15:42, `5622ff0` 16:23 (R6). |
| 2026-09-24 16:23 CEST | **The running line**, on the Owner's word relayed by the Principal, on the same branch: `<p id="r" class="m">` after the tracker view, outside the board, so every screen shows it, below the footer — the tool's Pricke inline in `currentColor` at 16 px (8 px would halve its 1-unit twigs; the tool carries the path as `PRICKE`, held to `pricke.svg` by a check) and `shoalmark`, one link to `https://github.com/holgo99/shoalmark` (`TOOL_PAGE`), then ` · ` and `v<VERSION>` linking to `…/releases/tag/v<VERSION>`; both `target="_blank" rel="noopener"`, named `shoalmark on GitHub` and `release v<VERSION>`; `--mute`, 11 px, no label. A vendored copy shows its own VERSION (checked with a copy set to 0.0.1-vendored). |
| 2026-09-24 15:42 CEST | **The board wears the mark — 0.18.2**, branch `fm/006-0-18-2-the-board-wears-the-mark`: a fourth brand file, `wordmark.svg` (the tool, `6fe9b11`), inlined in the header in place of the logo and the name, refused whole if it holds more than shapes and text. This repository's `work-tracker/brand/`: `wordmark.svg` composed from the site's header at 1x — the mark `overrides/.icons/shoalmark/pricke.svg` at x 0–16, the name at 18 px with the theme's −0.025 em tracking, its pen at x 36 and its baseline at y 14, its outlines IBM Plex Mono Medium turned into paths (`evidence/FM-006/mark/pricke/wordmark.py`, IBM's @ibm/plex-mono 1.1.0) — which Chrome draws with every glyph's ink box on the site header's own (`renders/site-header-light-1x.png`, read, no new render kept); `logo.svg` = `docs/assets/favicon.svg`; `theme.css` = Zensical's default and slate schemes flattened to hex (ink on ground 16.1:1 and 10.4:1, the secondary ink 4.7:1 and 5.3:1; slate's white for the name and the headings), IBM Plex Sans and Mono in IBM's Latin-1 cuts with their OFL; `labels.yaml` — the tagline *Dein Eigner bremst. Tunen statt tauschen.*, the footer the German start page's line *Eine Pricke im Watt – sie hält die Flotte im Fahrwasser.* (the seat's pick of a ruled line; the brief named none). The board's chrome stays English. |
| 2026-09-24 07:51 CEST | **The English tagline ruled — the withy question closed:** *"Go — and on withy: right, but 'A Pricke on the Wadden flats keeps the fleet in the channel.' is much stronger and gets the object right."* (the Owner, relayed by the Implementer hand, spelling normalised) — `docs/index.md:3` *A withy in the mud keeps the fleet in the channel.* → *A Pricke on the Wadden flats keeps the fleet in the channel.*; the German line stands as D2. The GtM files the ruling in its ledger. |
| 2026-09-24 07:48 CEST | **P4 closed by the Owner's ruling:** *"I am a sailor. D2 is the strongest one."* (relayed by the Implementer hand, spelling normalised) — the tagline names the Pricke and stands it in the water: `docs/de/index.md:3` *Eine Markierung auf der Seekarte, die die Flotte vor dem Auflaufen bewahrt.* → *Eine Pricke im Watt – sie hält die Flotte im Fahrwasser.*; `docs/index.md:3` *A mark on the chart that keeps the fleet off the shoal.* → *A withy in the mud keeps the fleet in the channel.* Nothing else in the copy. **Open, for the GtM and the Owner:** *withy* is the right English word but British, and a German reader of the English page may know neither word; the GtM's alternative is *Pricke* kept as a name in the English — his ruling ranked D2, not this. The Reviewer's R4 on the site slice fixed: the 16 px ruling row now carries *07:23 CEST*, as git has it (+0200). Carried verbatim from the closed branch `fm/006-the-mark-ruled-the-pricke` (916cd26), because neither is on `main` or the site tip: *The wordmark's face ruled: IBM Plex Mono* and *The mark ruled: … (a + d lock)* — the trial row mentions the lock, but not its quote, B1's retirement or the dropped reader test. Branch `fm/006-the-tagline-d2`, stacked on the site slice. |
| 2026-09-24 07:35 CEST | **The mark takes the name's ink on dark** — the GtM's finding: on the dark scheme the mark rendered 189 of 255 beside a name at 255. The cause, in the theme's slate palette: `[data-md-color-scheme=slate] .md-header__title{color:hsla(var(--md-hue),0%,100%,1)}` paints the title white, while the logo keeps the header's default `rgba(226, 228, 233, 0.82)`. The fix, one line in `docs/stylesheets/shoalmark.css`: `[data-md-color-scheme=slate] .md-header__button.md-logo{color:hsla(var(--md-hue),0%,100%,1)}`. Measured after, from the rebuilt site, browser preferring dark: the mark 255 and the name 255 at 1x and 2x, the mark still two levels (11, 255), the light header unchanged (33 on 255) — `evidence/FM-006/mark/pricke/renders/site-header-d-dark-fixed-{1x,2x}.png`. |
| 2026-09-24 07:23 CEST | **16 px `d` ruled as the site's mark** after the Owner saw the built header and `lockup-scale.png`; the Reviewer's R1 closed by this row and the paragraph above, R3 (Google Fonts on a German-first site) recorded as the open item that gates publication, R2 (the note's provenance footer) left for the next touch of the note. |
| 2026-09-24 | **The site wears `d` — as the Owner's trial** (*"wait. let's try d alone as proposed with the mono, this could be stellar"*, ≈ 01:05, chat, relayed); his lock of ≈ 00:55 — `a` in the header, `d` as the tab — stands until he has seen the built header and says which; `site-header-a-vs-d-2x.png` is what he decides on. Built on `fm/006-the-site-wears-the-pricke`: the pixel Pricke `d` inlined as the theme's logo icon at 16 px (×1: its 2 px stake is the Mono wordmark's stem), hard-edged at 1× and 2×; the tab icon `d`; the wordmark in IBM Plex Mono 500, the text in IBM Plex Sans; dark mode with the toggle. Evidence: `evidence/FM-006/mark/pricke/pricke-2026-09-23.md` (its last section) and `renders/site-*`. Committed with `TZ=UTC`: before 02:00 CEST the suite's board check fails on any change (the test dates by the local calendar, the board by UTC midnight); not yet filed. |
| 2026-09-24 | **The wordmark's face ruled: IBM Plex Mono** (his read, twice); running text Plex Sans. Same `TZ=UTC` commit as below, same bug. — carried from the closed branch fm/006-the-mark-ruled-the-pricke, 916cd26; the a + d lock was superseded by the 16 px d ruling of 2026-09-24 07:23 CEST |
| 2026-09-24 | **The mark ruled: the Pricke, `a` in the header and `d` as the tab** (*"agreed. a + d lock"*); B1 retired; the reader test for the mark dropped by the Owner. Committed with `TZ=UTC`: the pre-commit suite refuses every commit between 00:00 and 02:00 CEST (a timezone bug — the test dates by the local calendar, the board by UTC midnight; found by the Implementer at 00:33, to be filed in the morning). — carried from the closed branch fm/006-the-mark-ruled-the-pricke, 916cd26; the a + d lock was superseded by the 16 px d ruling of 2026-09-24 07:23 CEST |
| 2026-09-24 | **The Pricke drawn, on the Owner's ruling** (2026-09-23, relayed, spelling normalised): *"Do the broom also. Who cares if people know the meaning — I know it. It has to render visually attractive, then it is fine."* The meaning gate that killed A5 is waived for it, and his eye is the gate. Four variants, each drawn from committed SVG sources and rendered from main's own start page: `a`, *Besen nach oben* (port); `b`, *Besen nach unten* (starboard); `c`, `a` in a water line; `d`, `a` cut on the 16 px grid. They are rendered at 16 px ×8, in the header at 1x and 2x beside the wordmark in IBM Plex Sans, light and dark, and `a` beside B1. The seat proposes `a` with `d` as its tab; the Owner chooses. `evidence/FM-006/mark/pricke/pricke-2026-09-23.md` |
| 2026-09-23 | **The German claim ruled and applied** — *Dein Eigner bremst. Tunen statt tauschen.* — and IBM Plex ruled as the typeface family; the mark screen's survivor B1 held for the stand-in readers; the pitch's seven findings queued (P1 first). The GtM's ledgers: `evidence/FM-006/gtm-claim-screen-2026-09-23.md`, `gtm-mark-screen-2026-09-23.md` (branch `fm/006-gtm-mark-screen`, the Owner's PR). |
| 2026-09-23 | **Two readers ruled by the Owner** (an outside Owner; a German tech investor fluent in English) after the GtM's second pass screened for the investor without a ruling; the measured sentence cut to its real size in both languages — *one project, our own, its first day*. The GtM's ledger on `fm/006-gtm-claim-screen` (0d22563, ba43112): the current German claim fails its own G0 (two adjectives, HR German, mirrored order); two candidates survive every gate of the screen as the seat's judgment (its correction of this row's first wording, which said *G3 unrun* — the seat ran G3, the Owner's *never*; what is unrun is a search for existing use of the slogan, which the ladder never had as a gate, and any real reader); the reader question and *bremst* as provocation or insult are the Owner's to rule. Its third pass (f1e525a) says which reader each line works for and hands the Owner a reader test: five seconds on the top of the page, one claim each rotated, three questions the next day, the kill rules fixed before anyone reads. |
| 2026-09-23 | **Eigner for the person in German, on the Owner's word:** the seven German uses of *Owner* for the person — the claim (*Hol dir einen leistungsstärkeren menschlichen Eigner.*), the owner's block, the measured line, *start here*, two in `setup`, one in `signing` — now say *Eigner*; the seat name `owner`, the `[seats]` key, commands and quoted refusals stay English. |
| 2026-09-23 | **The claim sharpened on the Owner's word, his wording:** *Get a better-performing human Owner.* / *Hol dir einen leistungsstärkeren menschlichen Owner.* — in both pitches and the site's description; the line under it keeps *owner*; the README's title stays the agents'. |
| 2026-09-23 | R7: the span of the count is *just over a day* / *gut einem Tag* (27 h 50 min, the ruling to the count's tip), not a day and a half. R8: the English signing page says shoalmark lower-cases the branch it creates and git keeps the case it is given. |
| 2026-09-23 | R6: the German pages read natively — the Reviewer's sixteen rewordings, and one word each: *Standup* for the Owner's daily sitting, *Session* for an agent's run, never *Sitzung* for both. The board's German labels (`sessions.open`, `reviews.week`) still say *Sitzung*: aligning them is a tool change for the next release. |
| 2026-09-23 | R5: the signing pages name the answer branch as the tool cuts it, `answer/ap-007`. Proved on a scratch answer (`--answer AP-007 accept`, SSH-signed, pushed to a bare remote): `git log -1 --format=%G? answer/ap-007` prints `G` loose and after `git pack-refs --all`; `answer/AP-007` then fails, *unknown revision*. |
| 2026-09-23 | **Withdrawn on the Owner's word:** the seat's claim candidates are out; his line stands alone — *How to get a better-performing human owner.* (`589d328`); a second claim is a GtM screen he convenes. The row *The pitch built* below is restored as `76d1872` wrote it (R4): the ship log is append-only. |
| 2026-09-23 | R3: the pitch's measured paragraph cites what the consumer's record on its `main` holds — before, the last 200 pull requests merged unread, none reviewed; after, in a day and a half, 9 of 13 carried a Reviewer's file before they were opened — and no longer says *independent*: the board reports it, and git cannot yet prove it. |
| 2026-09-23 | **The pitch built**, on the Owner's ask (*"Can we get the site all pumped up for a pitch to somebody?"*): `index.md` in German first and English — the name, the line under it (*ein Zeichen auf der Karte, das die Flotte vom Grund fernhält* / *a mark on the chart that keeps the fleet off the shoal*), two claims side by side, *to the fleet* — *How to get a better-performing human owner.* — and *to the owner* — *Your agents are faster than you. Good. Now stop being the queue.*; the three measured numbers (no consumer named); the one-shot setup the agents run; what a day costs; what it is not; where to start. `setup`, `signing`, `standup` brought to 0.17.8 (`[seats]`, sessions, `--answer`, the verdict count), `de/standup.md` added. **The alternates, the Owner's to choose:** to the fleet — *Your owner is the slowest thing in the fleet, and the only one who may decide. Keep the second, fix the first.* · *Stop waiting for your human. Put what needs him first, and make his answer one command.*; to the owner — *Sign once. Read the digest. Press nothing you did not ask for.* · *Fifteen minutes a day, one signature, no stamping — and a record that shows who did what.* |
| 2026-09-23 | **The next slice is the pitch**, on the Owner's requirement above: one page an Owner reads in five minutes — the measured claim, the one-shot setup his agents run, what he signs, what an answer costs him; German first. Not built tonight. The pages are eight releases stale (0.17.0 → 0.17.8), and Pages deploys only for a public repository (D5). |
| 2026-09-23 | **The human pages open from a file** (the Owner's finding: *"clicking links does not work currently because it tries to open files"*): `use_directory_urls = false` — links are `setup.html`, not `setup/` — and `navigation.instant` dropped, whose page fetches `file://` blocks. Built with Zensical 0.0.64: the start page's local links are all `.html` and 133 of 145 local links across the site resolve to files on disk (the 12 others are `404.html`'s absolute `/shoalmark/…` paths, for Pages); a click on *Set up* in headless Chrome from `file://…/site/index.html` opens `setup.html`. The setup pages (EN, DE) say how to open or serve the built site. The content refresh is the next slice. |
| 2026-09-22 | The site builds green in CI; Pages refuses a private repository (*"Upgrade or make this repository public"*). The deploy step waits for the public release, by condition in the workflow. **Ruled the same hour: CI runs only on a ready pull request and on a release tag — minutes are paid for; the site builds on a tag.** |
| 2026-09-22 | Filed; Zensical tried on a scratch build first (0.3 s, search and dark mode in, four anchor warnings from the README); the signing page written. |
