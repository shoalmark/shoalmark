# FM-024 — the seven seat Apps: Owner run sheet, a dry run for Thursday 2026-10-01 before 11:00

Prepared 2026-09-30, 14:47–15:06 CEST, by the go-to-market seat (`gtm@seat`), session `8e509911/gtm-2` (Claude Opus 5.5), on `fm/024-the-seat-apps-run-sheet`
off main `297896b`. Scope: seven GitHub Apps owned by the organisation `shoalmark`. **The seat created nothing and changed no setting;** every forge read below
is a GET. The Owner creates the Apps in GitHub's browser UI, logged in as `holgo99` (org role `admin`, read 14:51). The Owner's plan (normalised): *"seven Apps
(principal, implementer, reviewer, gtm, auditor, datascientist, designer), no permissions, webhook inactive, no private key, no client secret, not installed,
icon uploaded. A seat reads the bot ids."* Their pre-decision, relayed 2026-09-30 (normalised): *"If a bot id does not resolve after creation, install that App
on the shoalmark organisation, only select repositories: shoalmark, with its permissions still none, and still no private key and no client secret. The inert
credential is what the condition protects, not the installation."* Their rulings on seats (15:29, relayed) rename two Apps: research, go-to-market.

## 1. The names — checked free
The name is the slug's source. GitHub shows the name *"converted to lowercase, with spaces replaced by `-`"*, caps it at 34 characters, and refuses the name of
*"an existing GitHub account"* (Sources). So the display name stays `shoalmark <seat>`, with the seat's English name (the Owner's rule 3), and the slug stays
plain, since any added word changes it. The character lives in the description and the icon, and `go-to-market` keeps its hyphens.

| Seat | Display name → slug | `/apps/<slug>` | `/users/<slug>%5Bbot%5D` | `/users/<slug>` | Free? | Checked at (CEST) |
|---|---|---|---|---|---|---|
| principal | shoalmark principal → `shoalmark-principal` | 404 | 404 | 404 | yes | 14:51:15–14:51:39 |
| implementer | shoalmark implementer → `shoalmark-implementer` | 404 | 404 | 404 | yes | 14:51:16–14:51:39 |
| reviewer | shoalmark reviewer → `shoalmark-reviewer` | 404 | 404 | 404 | yes | 14:51:17–14:51:40 |
| research | shoalmark research → `shoalmark-research` | 404 | 404 | 404 | yes | 15:32:44–15:32:45 |
| go-to-market | shoalmark go-to-market → `shoalmark-go-to-market` | 404 | 404 | 404 | yes | 15:32:46–15:32:47 |
| designer | shoalmark designer → `shoalmark-designer` | 404 | 404 | 404 | yes | 14:51:20–14:51:42 |
| auditor | shoalmark auditor → `shoalmark-auditor` | 404 | 404 | 404 | yes | 14:51:18–14:51:41 |

Controls, same token, 14:51:37–14:51:39 and 15:32:47: `/apps/github-actions`, `/users/github-actions%5Bbot%5D` (id 41898282), `/users/dependabot%5Bbot%5D`,
`/orgs/shoalmark`: 200. **Limit:** `/apps/<slug>` answers 404 for another account's *private* App too, so that column is necessary, not sufficient; the other
two 404s are the stronger half, and **Create GitHub App** is the proof. The rulings retire `shoalmark-gtm` and `shoalmark-datascientist` (free at 14:51).

## 2. The one-line descriptions — the six gates of `evidence/FM-006/gtm-claim-screen-2026-09-23.md`, adapted to an App's line, by hand
| Gate | Kills on |
|---|---|
| **G0** form | more than one line · over 120 characters (counted in code) · not English · jargon or an internal id · not what the seat does · read aloud, a job ad or a slogan |
| **G1** language | a native English reader hears a translation, or an idiom slips |
| **G2** truth | anything the record cannot show today: a promise (speed, safety, quality), a compliance word, another project or product named |
| **G3** the Owner's never | it makes them a push-a-button, invites rubber-stamping, flatters or insults them |
| **G4** both ways | beside the fleet's line (`docs/index.md`: a question put to them, their answer one command) and the four rights (README §*Seats*), a seat answers, decides or merges for them |
| **G5** the bar | beside the other six, it could sit under another seat's name, or it does not end with the seat's limit (the Owner's rule 6, relayed 15:29: first person, one line) |

| Seat | Line (characters) | G0 | G1 | G2 | G3 | G4 | G5 | Why: what the record shows |
|---|---|---|---|---|---|---|---|---|
| principal | I put the agents' open questions to the Owner, one sentence each, and brief each seat I call up. Only the Owner answers. (120) | pass | pass | pass | pass | pass | pass | the Owner's text; README *drafting an ask*: the Principal puts an ask in front of the Owner; `principal` holds no `answer` (§*Seats*) |
| implementer | I build one change from my brief, in a worktree of my own. A Reviewer reads it; I never judge my own work. (106) | pass | pass | pass | pass | pass | pass | the Owner's text; `.claude/agents/implementer.md`: one scoped change from the brief, its own worktree; code gets a Reviewer's loop (AGENTS.md) |
| reviewer | I read a branch against its brief and write my verdict into the repository: READY, or what must change. I never merge. (118) | pass | pass | pass | pass | pass | pass | the Owner's text; `.claude/agents/reviewer.md`: one pass, the verdict committed on the branch; AGENTS.md: the Owner merges |
| research | I check a claim against its sources, or work out what evidence would settle it, before anyone builds. I build nothing. (118) | pass | pass | pass† | pass | pass | pass | G0 cut *on it* (124 → 118); the Owner's rulings 1–2: the Data Scientist folds in; *Type: sources* or *Type: measurement*; may not build |
| go-to-market | I check public sentences against what the repository can prove and hand the Owner the ones that hold. The Owner picks. (118) | pass | pass | pass | pass | pass | pass | G2 cut *every* (as RV-2091; 123 → 118); the claim screen: G0–G5, *this seat chooses nothing, ranks nothing*. **Character, named by this seat for the Designer's README: the herald — it announces only what passed.** |
| designer | I draw what people see of shoalmark (the board, the brand, these badges) from sources in the repository. No mock-ups. (117) | pass | pass | pass† | pass | pass | pass | the Owner's text; the Owner's ruling 5: *from sources in the repository*, may not *present a mock-up as a render*; the badges on `130fc7c` |
| auditor | I check what the record claims against what it can show and take each finding, sourced, only to the Owner. (106) | pass | pass | pass | pass | pass | pass | the Owner's correction (relayed 15:5x): the trim's *never to a seat* failed G2, since findings reach seats through the Owner's relay; FM-024 *Raised*: one sourced line per raise, through the Owner |

Controls: *"Reviews every pull request so your merges are safe, fast and compliant."* dies at **G2**, on a promise and a compliance word. *"Helps the team get
its work done."* dies at **G5**, since it could sit under any seat. The seven lines are the Owner's starting points (rule 6, relayed 15:29), word for word where
they pass; two lost words to a gate, and the auditor's is the Owner's own correction. † G2 rests on the Owner's rulings, relayed and not yet in the repository,
and for the designer on its badges. **Disclosure:** this seat screened the Owner's lines and made the two cuts; no independent reader has read them. G1 is this
runtime's English (K). The Designer's README (`d72b8e0`, 15:39) names the same herald.

## 3. The Owner's steps — about 45 minutes (≈ 6 per App), then 10 for the icons; stop on an unexpected screen or value
**Read-only baseline, first.** No REST endpoint lists the Apps an organisation owns. The GitHub Apps reference has `/apps/{app_slug}`, the app's own `/app…`
and installations. So the list is the page, and installations are the GET:
```sh
open 'https://github.com/organizations/shoalmark/settings/apps'
gh api /orgs/shoalmark/installations --jq .total_count
```
Expected: no GitHub App listed, and `0` (read `0` at 14:51:51). Stop if an App named `shoalmark-…` is there already. Paste back: `apps page empty; installations 0`.
1. **Create `shoalmark-principal`.** Organisation Settings → Developer settings → GitHub Apps → **New GitHub App**:
   ```sh
   open 'https://github.com/organizations/shoalmark/settings/apps/new'
   ```
   *GitHub App name* `shoalmark principal` · *Description* the line of §2 · *Homepage URL* `https://shoalmark.github.io/shoalmark/seats/`: it goes live with the
   v0.19.0 tag (404 at 15:47), and the gap until Friday is the Owner's accepted choice. Leave *Callback URL* and *Setup URL* empty. Clear *Request user authorization
   (OAuth) during installation* and *Enable Device Flow*. *Expire user authorization tokens* as it comes. *Webhook*: clear **Active**. *Permissions*: every dropdown
   in every group the form shows (Repository, Organization, Account, and Enterprise if listed) **No access**, as they come: a GitHub App has none by default. *Where
   can this GitHub App be installed?* **Only on this account**. Click **Create GitHub App**. On the App's page: **generate no private key and no client secret**, and
   click no *Install App*. Expected: the App's page, `…/settings/apps/shoalmark-principal`, with an App ID and no key or secret listed. Stop on a refused name, a
   payment, a permission dialog, a key or a secret generated; *Confirm access* is no stop. Paste back: `shoalmark-principal`, its App ID.
2. **Read its bot id**, and install only on a 404, as their pre-decision says:
   ```sh
   gh api "/users/shoalmark-principal%5Bbot%5D" --jq .id
   ```
   Expected: a number. **On 404**: **Install App** → **Install** beside `shoalmark` → **Only select repositories** → `shoalmark` where the screen offers it (GitHub
   omits it for an App with no repository permission, see Sources) → **Install**; then the GET again. Their pre-decision names that choice, so the Principal asks them
   before 09:00 whether it holds when the screen offers none, and their word goes here. Without it, a screen with no repository choice is a stop: paste back
   `no repository choice`. Stop too on any access listed (*Read access to metadata* included), a key, a secret or a payment. Paste back: the id, `installed` or not.
3. **The six others:** steps 1–2 again, each with its name, and its line from §2:

   | Seat | implementer | reviewer | research | go-to-market | designer | auditor |
   |---|---|---|---|---|---|---|
   | *GitHub App name* | shoalmark implementer | shoalmark reviewer | shoalmark research | shoalmark go-to-market | shoalmark designer | shoalmark auditor |
   | Slug to expect | `shoalmark-implementer` | `shoalmark-reviewer` | `shoalmark-research` | `shoalmark-go-to-market` | `shoalmark-designer` | `shoalmark-auditor` |
4. **The icons**, once the Designer's `fm/024-the-seat-icons` carries its READY verdict (due by 11:00). Until then the Apps keep GitHub's identicon:
   ```sh
   git fetch && git switch --detach origin/fm/024-the-seat-icons && rm -rf brand/seats/out && python3 brand/seats/export.py && open brand/seats/out
   ```
   Per App: its page → *Display information* → **Upload a logo** → that App's `<seat>-200.png` from the Designer → **Set new avatar**. GitHub takes a PNG, JPG
   or GIF under 1 MB and recommends 200 × 200 pixels. Expected: the badge shows the stake. Stop if the export exits 1 or 2 (it prints why): the icons wait, the
   Apps stand. Paste back: `7 icons set`. Either way, `rm -rf brand/seats/out; git switch main`: main does not ignore its 21 PNGs yet.
5. **Read back:** the loop of §4, and `gh api /orgs/shoalmark/installations --jq '[.installations[] | {app_slug, repository_selection}]'`. Expected: seven ids;
   installed, only what step 2 installed. Paste back: slugs, App IDs, bot ids, each install's `repository_selection`, to the Principal for FM-024.

## 4. What a seat reads after
```sh
for s in principal implementer reviewer research go-to-market designer auditor; do
  id=$(gh api "/users/shoalmark-$s%5Bbot%5D" --jq .id) && echo "$s $id+shoalmark-$s[bot]@users.noreply.github.com"
done
```
The address is `<id>+shoalmark-<seat>[bot]@users.noreply.github.com`, with the bot **user's** id, not the App ID (Sources). **The switch itself is the next
slice:** `[seats]` (today `principal`, `implementer`, `reviewer`, `gtm`; the rulings add `research@seat` and `datascientist@seat` for research, with its bot
address, and give `gtm@seat` the App `shoalmark-go-to-market`), each worktree's `user.email` and `user.name`, one test commit per seat, a Reviewer pass. The
parent project needs no installation: GitHub attributes a commit by its email, across repositories (the Owner's line, untested until that test commit).

## Agent boundary, recovery, unproven
Owner decisions only: the creation, the install of step 2, the icons; an App showing a key or a secret is wrong. Recovery: the App's page edits name,
description and homepage; *GitHub Apps* → *Configure* → **Uninstall** removes an install. **Unproven:** the bot user before an install; a no-permission App
installing without a key; attribution by email; the Designer's export and README; a reader other than this runtime for G1.

## Preparation checks and sources
All five shell blocks passed `zsh -n`. Four ran in `zsh -f` at 15:04 (the renamed §4 loop again at 15:39), a stand-in `open` first on PATH, the GETs for real:
`0` and seven bot 404s, as expected before creation. Both `open` URLs route (302 to login; a bogus path 404). Step 4's block switches a checkout: syntax only.
[Registering a GitHub App](https://docs.github.com/en/apps/creating-github-apps/registering-a-github-app/registering-a-github-app) · [Creating a custom badge](https://docs.github.com/en/apps/creating-github-apps/registering-a-github-app/creating-a-custom-badge-for-your-github-app) · [Installing your own GitHub App](https://docs.github.com/en/apps/using-github-apps/installing-your-own-github-app) · [REST: GitHub Apps](https://docs.github.com/en/rest/apps/apps) · [REST: org installations](https://docs.github.com/en/rest/orgs/orgs) · the bot user on install, secondary:
[DEV, agent_paaru](https://dev.to/agent_paaru/each-ai-agent-gets-its-own-github-identity-how-we-gave-every-bot-its-own-bot-commit-signature-1197), [actions/create-github-app-token#172](https://github.com/actions/create-github-app-token/issues/172)
(a comment: installing resolved the 404) · the id form: [josh-ops](https://josh-ops.com/posts/github-apps-commit-email/). Records: the claim screen; `evidence/FM-006/public-hardening-owner-2026-09-30.md` (the form).
