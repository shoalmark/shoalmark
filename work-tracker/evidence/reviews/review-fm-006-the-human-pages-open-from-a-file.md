# Review — FM-006, the human pages open from a file

- **Date:** 2026-09-23, 21:49 CEST (`date`)
- **Seat:** Reviewer (`reviewer@seat`) · **Session:** `8e509911/reviewer-1` · **Model:** Claude Opus 5.5
- **Tip reviewed:** `efafa12` on `fm/006-the-human-pages-open-from-a-file`
- **Base:** `62db9f8` (`origin/main`)
- **Commits:** both `Session: 8e509911/implementer-4`.
  - `37f861c`: `zensical.toml` gains `use_directory_urls = false` and drops `navigation.instant`; `docs/setup.md` and
    `docs/de/setup.md` each gain one line.
  - `efafa12`: FM-006's *What is true now* quotes the Owner, and a ship-log row names the next slice.
- **Method:** the branch and `origin/main` are archived into scratch directories and built there with Zensical 0.0.64
  from a scratch venv. `site/` never touched this worktree, and it is git-ignored (`.gitignore:4`).

## Cold start

1. **What virtue do I bring?** Doubt. "Opens from a file" has to hold link by link, and dropping a theme feature must
   not break what the served site did.
2. **How does it turn into blindness?** By blaming the change for a failure that `main` has too. So every behaviour is
   measured on both builds.
3. **What would show that failure here?** An unresolved local link; a click from `file://` that goes nowhere; a search
   that answers on `main` and not here.
4. **Who gets the record, independently of me?** The Principal seat, then the Owner. This file disposes of nothing.

## (1) Every local link of the built site

I parsed every `href` and `src` in the nine built pages:

| kind | count |
|---|---|
| page links (`<a href>`): all end in `.html`, and all resolve to a file | **103** |
| resources (styles, scripts, images): all resolve to a file | **38** |
| pure anchors | 131 |
| external | 61 |
| `404.html`'s absolute `/shoalmark/…` paths (the known exception) | 13 |

**Unresolved: 0.** The ship log's *133 of 145, 12 others* counts differently; the claim holds by my count too.

- **The build's one warning is older than this slice:** `index.md:12` links
  `agents/README.md#how-to-get-a-better-performing-human-owner`, and that anchor does not exist. `main`'s build prints
  the same warning. The file resolves; the anchor does not.

## (2) Clicked from `file://`, headless Chrome

| from | click | lands on |
|---|---|---|
| `site/index.html` | *Set up* (`./setup.html`) | *Set up in ten minutes* |
| `site/index.html` | *Deutsch* (`./de/index.html`) | the German start page (*In zehn Minuten eingerichtet*, *Ihre Antwort ist Ihr Commit* in its DOM) |
| `site/de/index.html` | `setup.html` | *In zehn Minuten eingerichtet* |
| `site/de/index.html` | `../index.html` | back to the English start page |

## (3) The configuration, and search without instant navigation

- **The configuration:** `git diff origin/main -- zensical.toml` is the one added `use_directory_urls = false` and
  `navigation.instant` removed from `features`. Nothing else moved.
- **Search index:** `search.json` is built, with 35 items on both builds. Its locations are `setup.html#…` here and
  `setup/#…` on `main`.
- **Search, served** (`python3 -m http.server`): the search button opens its box, and a query typed there answers the
  same on both builds.

  | query | branch | `main` |
  |---|---|---|
  | *signature* | 3 results, first `signing.html?h=signature` | 3 results, `signing/?h=signature` |
  | *standup* | 8 results, `standup.html?h=standup` | 8 results |

  Twice each. A first, naive probe missed the results on both builds: a race between the typed query and the search
  worker, not a defect.
- **Search from `file://`:** the box never opens, on this branch and on `main` alike. See R1.

## (4) The docs workflow's steps

- `zensical build`: exit 0, one warning, the same as on `main`.
- `python3 scripts/llms_txt.py site`: exit 0, *8 pages, each with a Markdown twin*. All 8 links in `llms.txt`
  resolve in the built site.

## (5) The German line

*Diese Seiten, gebaut mit `zensical build`: die Website öffnet sich aus `site/index.html`, oder liefern Sie sie aus:
…* is understandable but stiff. See R2.

## (6) The quote

- It is marked *(quoted, spelling normalised)*.
- It carries the Owner's requirement as the coordinator relays it: *a pitch — easy, convenient, a one-shot integration
  mostly done through your agents*.
- This seat has not seen the Owner's original words, so the wording against his is unverified here.

## (7) The gates

`python3 shoalmark.py --check` exits 0, and `python3 shoalmark.py --session-check` exits 0.

## Findings

### R1 · P3 · Search does not work from `file://`, and the new line does not say so

- **What:** Both setup pages (EN, DE) now say the built site *opens from `site/index.html`, or serve it*, as if the two
  were equal. From `file://` the search box never opens: the button is there, and no input appears. That was so on
  `main` as well. Served, search works.
- **What closes it:** Add half a sentence to each line, for example *search needs the served site* / *die Suche nur
  über den Server*.

### R2 · P3 · The German line is stiff

- **What:** *öffnet sich aus* and *liefern Sie sie aus* read as translated.
- **A proposal:** *Diese Seiten, gebaut mit `zensical build`, lassen sich direkt aus `site/index.html` öffnen — oder
  lokal bereitstellen (die Suche braucht das): `python3 -m http.server -d site 8000`.*

## Verdict

**READY WITH FINDINGS: R1 and R2 (P3).**

- Every local link of the built site resolves and ends in `.html`, apart from 404's known absolute paths.
- Clicks from `file://` work in English and German.
- Served search answers exactly as on `main`.
- The workflow's two steps exit 0.

## Pass on the pitch — 589d328

- **Date:** 2026-09-23, 22:07 CEST (`date`) · **Seat:** Reviewer, session `8e509911/reviewer-1`
- **Tip reviewed:** `589d328` — `76d1872`, the pitch, the pages at 0.17.8, R1/R2; and `589d328`, the Owner's
  correction to one claim.
- **Method:** built in scratch as before, and read the consumer's source read-only: its tracker on every local ref,
  and the remote's copy through the forge API, with nothing fetched into the consumer.

### (1) The numbers

**The first number is not in its source.**
- *Measured, not promised* says *0 → 17 of 21 pull requests carried an independent review file before they were
  opened* (EN and DE, `docs/index.md:17`, `docs/de/index.md:17`).
- The source is the consumer's count tracker. On every local ref, on the remote's main and on its branch, its newest
  totals read *a Reviewer file before opening: **9 of 13** opened, 9 of 12 merged*.
- *17 of 21* appears nowhere in it. The forge shows 21 pull requests since the ruling up to the 21st, and 23 by now, so
  the denominator is plausible and the numerator is unrecorded.
- The same source says, in the same paragraph: *whether a pass was independent in fact, git cannot say — the Reviewer
  seats … were sub-agents of the Principal session that wrote what they judged*. So the word *independent* is the one
  thing the source says it cannot claim. shoalmark's own FM-024 count reads *same session* for this very pattern.

**The other two bullets** are true as descriptions of the tool: one `--answer` command, one signed commit, and the
board's *independent / same session* count since 0.17.6. But they are properties, not measurements. And the answer's
branch still has to be merged.

**No consumer named.** The diff and `docs/` carry no repository name and no consumer tracker id, `RV-` id or pull
request number. The only hits are shoalmark's own `holgo99/shoalmark` URLs.

### (2) The claim

- The Owner's wording stands exactly in both languages: `## How to get a better-performing human owner.` and `## Wie
  man einen besser funktionierenden menschlichen Owner bekommt.`
- No second headline: the other H2s are section headings.
- The italic line under the name (*A mark on the chart that keeps the fleet off the shoal.* / *Ein Zeichen auf der
  Karte …*) is a line, not a claim. It is for the Owner's eye, since he ruled *one* claim.

### (3) The ship log

See R4.

### (5) The three pages at 0.17.8, run at the real tag

I cloned this repository at `v0.17.8` (`62db9f8`) into scratch and ran into a scratch consumer:

| command | outcome |
|---|---|
| `--vendor tools/shoalmark` | exit 0, *from tag v0.17.8*; the manifest line is right |
| `--init --key AP` | exit 0 |
| `--install-hook` | exit 0, 4 hooks |
| `--standup` | exit 0 |
| `--standup standup.ics` | exit 0, once `standup =` sits above the config's first table |
| `--owner` | exit 0 |

- **The refusal texts** in *What the tool refuses* all exist in the tool (`:2972`, `:2976`, the `answered-by` line),
  paraphrased only where the page says so.
- **One exception**, R5: the answer branch is written `answer/AP-007`; the tool creates `answer/ap-007`.
- **The nav:** `docs/de/standup.md` is in it (*Der Standup*).
- **Not runnable here:** `git clone --branch v0.17.8 https://github.com/holgo99/shoalmark` fails without credentials
  while the repository is private. SSH works. That will stay so until it goes public.

### (6) *You lose nothing*

- **FM-026** exists on `origin/fm/026-…` only, not on `main` and not on this branch. *Filed … and coming* is true of
  a branch; a reader of the site cannot open it yet.
- **The note for trying it:** `ADOPT.de.md` is on `main`, so the forge link resolves for anyone with access.
- **The README** is included (`docs/agents/README.md` is `--8<-- "README.md"`), never copied.

### (7) The build and the gates

| check | result |
|---|---|
| `zensical build` | exit 0, **No issues found** (the old README-anchor warning is gone) |
| `llms_txt.py site` | exit 0, 9 pages |
| links | 130 page links, all `.html` and all resolving; 43 resources resolve; 0 unresolved; 404's 14 absolute paths the known exception |
| clicks from `file://` | *Set up*, *The standup* (EN), *Der Standup*, *Ihre Antwort ist Ihr Commit* (DE) open |
| served search | *signature* 5 results, *Standup* 10 |
| `--check` | exit 0 |
| `--session-check` | exit 0 |

### (8) Five minutes

Words, code blocks left out:

| page | EN | DE |
|---|---|---|
| the pitch (`index`) | 461 | 459 |
| `setup` | 522 | 519 |
| `signing` | 757 | 700 |
| `standup` | 352 | 347 |

- **The pitch** reads in about 2 minutes at 200–250 words a minute, well inside five.
- **The Owner's whole path**, all four pages: about 2,090 words, 8–10 minutes.
- **My own read** is no measure of a person's, and I give none.

### R3 · P1 · The pitch's measured claim states a count its source does not hold, and an independence the source disclaims

- **What:** *0 → 17 of 21 … independent review file* (EN and DE, line 17).
  - The source records 9 of 13, and *Reviewer file*, not *independent*.
  - It says outright that independence cannot be read from git, and that its reviewers were sub-agents of the author's
    session.
- **Cost:** The first proof on a page titled *Measured, not promised* is neither the measured number nor the measured
  thing. It would ship with the tag's site.
- **Confidence:** High. Every ref, the remote read through the forge API, the same paragraph.
- **What closes it:** Either
  - *0 → 9 of 13 pull requests carried a review file before they were opened* (the recorded count); or
  - record the 17-of-21 count, with its method, in the source first, and cite that.

  Either way, drop *independent*. The third bullet can then say, truly, that the board now counts which review was.

### R4 · P2 · The ship log was rewritten in place: it now says the pitch was *built* with one claim

- **What:** `589d328` rewrote the row `76d1872` added (`FM-006…md:51`). The row now reads *ONE claim, the Owner's*, but
  `76d1872` built two. The Owner's correction came after, in `589d328`. The ship log is append-only (AGENTS.md rule 1),
  and the row now misstates what that commit built.
- **What closes it:**
  - Restore the row as `76d1872` wrote it.
  - Append a new row: *the second claim withdrawn on the Owner's word; the pitch carries one* (`589d328`).
  - **Or,** if the Owner's *"rejected, not ledgered"* means the candidate's text must not stand: keep the rewritten
    row, and append one saying the row above was rewritten on his word and `76d1872` holds the original. That still
    records the rewrite, which is what the rule protects.

  Which of the two is the Owner's call, through the Principal.

### R5 · P3 · The answer branch is `answer/ap-007`, not `answer/AP-007`

- **What:** `--answer` creates `answer/{id.lower()}` (`shoalmark.py:895`). Both signing pages (EN `:92`, `:94`; DE
  `:93`, `:96`) name `answer/AP-007`, and give `git log -1 --format=%G? answer/AP-007` as the check.
- **Measured:** the check resolves only while the ref is loose on a case-insensitive disk. After `git pack-refs` it
  fails: *fatal: ambiguous argument 'answer/AP-007': unknown revision*. A clone or `gc` leaves packed refs, and Linux
  fails always.
- **What closes it:** `answer/ap-007` in both pages.

### R6 · P3 · The German reads translated in places — a native reading, each with a rewording

**One word for two things.** *Sitzung* is the Owner's daily sitting (*Eine Sitzung, fünfzehn Minuten*; *Der Standup
— eine Sitzung am Tag*) and also the agents' run (*aus derselben Sitzung*; *Sitzungen … `seat.session`*; *in einer
anderen Sitzung*). `index` uses *Session* for the agents in one line as well. Use *Termin* (or *Sitzung*) for the
Owner and *Session* for the agents, the same on every page.

**Line by line:**

| where | reads | better |
|---|---|---|
| `index` | *Ein Zeichen auf der Karte, das die Flotte vom Grund fernhält* | *Eine Markierung auf der Seekarte, die die Flotte vor dem Auflaufen bewahrt* |
| `index` | *als einen Satz pro Frage, einmal am Tag, und macht seine Antwort zu einem Befehl* (reads *an order*) | *– ein Satz pro Frage, einmal am Tag –, und macht aus seiner Antwort einen einzigen Befehl* |
| `index`, `setup` | *an einem Release-Tag* / *an seinem Tag* (*Tag* reads as *day*) | *beim Git-Tag eines Releases* / *genau auf seinem Git-Tag* |
| `index`, `setup` | *festgehaltene Kopie* | *festgeschriebene* (or *versionsfeste*) *Kopie* |
| `index` | *ist erfasst (FM-026) und kommt* | *ist als FM-026 erfasst und folgt* |
| `index` | *auf Englisch, denn Agenten lesen ihn so* · *an der Wurzel dieser Seite* | *auf Englisch – so lesen ihn die Agenten* · *im Stammverzeichnis dieser Website* |
| `setup` | *## 2. Deutsch, dann einrichten* | *## 2. Auf Deutsch umstellen, dann einrichten* |
| `setup` | *dann steht da, was sich geändert hat* | *und es zeigt Ihnen, was sich geändert hat* |
| `setup` | *Ihre erste Zeile ist, was Sie braucht* | *Ihre erste Zeile zeigt, was auf Sie wartet* |
| `signing` | *nicht als Sie verifiziert* / *verifiziert als Sie* | *sich nicht als Ihrer verifizieren lässt* / *gilt als von Ihnen signiert* |
| `signing` ×2, `standup` | *druckt* | *gibt … aus* |
| `signing` | *die Frage hat Ihre Liste verlassen* | *die Frage ist von Ihrer Liste verschwunden* |
| `standup` | *Je eines ein eigener Termin* | *Jedes bekommt einen eigenen Termin* |
| `standup` | *ihren Möglichkeiten, der, die der Agent empfiehlt,* | *ihren Möglichkeiten (die vom Agenten empfohlene zuerst)* |
| `standup` | *annehmen darf Ihre Änderung tragen, ablehnen sagt, warum* | *beim Annehmen können Sie eine Änderung mitgeben, beim Ablehnen sagen Sie, warum* |
| `standup` | *Bevor Arbeit Sie zum Mergen erreicht* | *Bevor Arbeit bei Ihnen zum Mergen ankommt* |

### Verdict on 589d328

**NOT READY: R3 (P1) and R4 (P2).** R5 and R6 are P3.

- **R3:** the pitch's one measured proof is not the source's number, and says *independent* where the source says it
  cannot. It closes with the recorded *9 of 13* and without the word.
- **R4:** restore the row and append.
- **What holds:** the build is clean, links and clicks hold, search works when served, and the claim is the Owner's
  in both languages.

## Delta on da84aa0

2026-09-23, 22:14 CEST. **READY WITH FINDINGS: R7 and R8 (P3).** R3–R6 are closed.

**R3 · closed.**
- *Before:* the consumer's count tracker on its `main`, read-only, says in *What is true now*: *the last 200 merged
  pull requests, 22 days, 85 % merged under a minute after opening, 0 reviewed*. The pitch's *200 … merged unread; none
  was reviewed* matches it.
- *After:* *9 of 13 with a Reviewer's file before opening* matches its totals.
- *Independent* is gone from the pitch in both languages.
- The board's line is worded as a report: *a report, not a proof: git cannot yet show it* / *eine Meldung, kein
  Beweis*.

**R7 · P3 · *In a day and a half* overstates the span.**
- **What:** From the ruling (2026-09-22 10:34:36Z) to the second count's tip (2026-09-23 14:24:13Z) is **27 h 50 min**:
  just over a day, not thirty-six hours. It errs against the page's own interest, but it is not the measured span.
- **What closes it:** *in just over a day* / *in gut einem Tag*, or *in 28 hours* / *in 28 Stunden*.

**R4 · closed.** `76d1872`'s row is present byte-identical to git's own copy. The withdrawal row stands above it,
newest first as the log is kept, and names `589d328`.

**R5 · closed, with one wrong reason (R8).** Both signing pages now say `answer/ap-007`.

**R8 · P3 · The English page's reason is wrong.**
- **What:** It says *(git refs are lower-case; …)*. Git refs are case-sensitive and may be any case; shoalmark
  lower-cases the branch it cuts (`shoalmark.py:895`). The German *(Branch-Namen klein: …)* is right in substance.
- **What closes it:** *(shoalmark writes the branch in lower case; `AP-007` is the tracker, `ap-007` the branch)*.

**R6 · closed.**
- All sixteen rewordings are in, and every flagged phrase is gone.
- *Sitzung* is absent from all four German pages. The Owner's sitting is *Standup* and an agent's run is *Session*,
  consistently.
- **The line under the name, graded as German:** *Eine Markierung auf der Seekarte, die die Flotte vor dem Auflaufen
  bewahrt.* It is correct and idiomatic: *vor dem Auflaufen bewahren* is the right nautical phrase. If the Owner wants
  it closer to the README's own image (*a stake or a buoy*): *Ein Seezeichen, das die Flotte vor dem Auflaufen
  bewahrt.* The words are his.

**Build and gates:**

| check | result |
|---|---|
| `zensical build` | exit 0, *No issues found* |
| `llms_txt.py site` | exit 0, 9 pages |
| links | 130 page links, all `.html` and resolving; 43 resources; 0 unresolved; 404's 14 absolute |
| clicks from `file://` | EN → *Your answer is your commit*; DE → *Ihre Antwort ist Ihr Commit*, *Der Standup* |
| served search | *signature*: 5 results |
| `--check` · `--session-check` | exit 0 each |

**The German pitch** is 493 words, code blocks left out: 2.0–2.5 minutes at 250–200 words a minute. That is an
estimate from the count. A model's reading time is not a person's, so I report none of my own.

**Delta on c5f1fcd, 2026-09-23 22:17 CEST — READY TO TAG.** R7 is closed: *just over a day* / *in gut einem Tag* in
both pitches. R8 is closed: the English signing page now says *shoalmark lower-cases the branch it creates; git keeps
the case it is given*, and FM-006 gains one ship-log row.

`zensical build` exits 0 with *No issues found*; `llms_txt.py site` exits 0 (9 pages); `--check` and `--session-check`
exit 0.

## Delta on 53d4277

2026-09-23, 22:22 CEST. **READY TO TAG.** Two observations follow, for the Owner, not as findings.

**The claim.**
- It is byte-exact: `## Get a better-performing human Owner.` (`docs/index.md:5`) and `## Hol dir einen
  leistungsstärkeren menschlichen Eigner.` (`docs/de/index.md:5`).
- `site_description` and the built `<meta name="description">` carry *Get a better-performing human Owner — …*.
- The old claim is gone from `docs/` and `zensical.toml`, and `README.md` is untouched, as ruled.

**What is left of *owner* in `docs/de/`** — five occurrences, all code or the seat name:
- `--owner` (`standup.md:32`);
- `owner = …` (`setup.md:49`, `signing.md:68`);
- `(owner)` beside *Eigner* (`setup.md:55`, `:57`).

No capitalised *Owner* remains.

**The seven *Eigner* lines, graded as German.**
- Six read natively: `index` 5, 10, 22 and 58; `setup` 57; `signing` 3. *Eigner* also carries the nautical sense,
  the Schiffseigner, which fits the fleet and the shoal.
- `setup:55`, *Unter Subversion steht für den Eigner (`owner`) Ihr Server-Konto*, is correct but stiff. *Unter
  Subversion ist der Eigner (`owner`) Ihr Server-Konto* is smoother.

**Observations for the Owner.**
- The claim addresses its reader as *du* (*Hol dir*), while the page says *ihr* to the fleet and *Sie* to the Eigner.
  That is a slogan's register and his words.
- The German page's meta description is the site-wide English one: Zensical has one `site_description`.

**Gates:**

| check | result |
|---|---|
| `zensical build` | exit 0, *No issues found* |
| `llms_txt.py site` | exit 0, 9 pages |
| `--check` | exit 0 |
| `--session-check` | exit 0 |

## Pass on a3eb298 (`fm/006-two-readers-and-the-number-at-its-real-size`)

2026-09-23, 23:05 CEST. **READY WITH FINDINGS: R9 and R10 (P3).**
- Only the two lines in `docs/` moved. *9 of 13* stands.
- FM-006's new paragraph quotes the Owner as marked. It names no client.
- `zensical build` exits 0 with *No issues found*; `--check` and `--session-check` exit 0.
- The week's report now reads 11 verdicts: 1 independent (0.17.6's first, known false) and 10 same session. This
  seat's reviews are counted as what they are.

**R9 · P3 · *On its first day* is neither the right size nor the right subject.**
- **The span:** the ruling (2026-09-22 10:34:36Z) to the second count (2026-09-23 14:24:13Z) is **27 h 50 min**.
  *Its first day* is about four hours short, and *its first day and a half* would be eight hours long.
- **The subject:** *its* reads as the project's first day, and the project had 200 pull requests before.
- **What closes it:** *in the first 28 hours after the rule* / *in den ersten 28 Stunden nach der Regel*.

**R10 · P3 · *In one project* is said twice in three lines.**
- **What:** The intro reads *In one project that runs shoalmark:* / *In einem Projekt, das shoalmark nutzt:*, and the
  bullet repeats *in one project — our own —*.
- **What closes it:** Move *our own* into the intro: *In one project — our own — that runs shoalmark:* / *In einem
  Projekt — unserem eigenen —, das shoalmark nutzt:*. Then the bullet is only *After, in the first 28 hours after the
  rule:* / *Danach, in den ersten 28 Stunden nach der Regel:*. Both lines read natively in German then.
