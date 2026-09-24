# GtM — the pitch on main verified, and the mark screened (wordmark and icon)

- **Date:** 2026-09-23, 23:28–23:50 CEST (`date`)
- **Seat:** GtM (`gtm@seat`), Owner-convened · **Session:** `e0be0fa0` · **Model:** Claude Opus 5.5
- **Base:** `595fc80` (`main`, after PR #25). The site was built from it with Zensical 0.0.64 in a scratch venv:
  *No issues found*.
- **Disclosure:** one runtime wrote the candidates, rendered them and screened them. **Every picture named below
  was produced by `mark/marks.py` from a source committed beside it, and none was drawn by hand.** Rendering is
  headless Chrome at device-pixel-ratio 1, unless a file says `dpr2`, and the enlargements are nearest-neighbour.
- **This seat chooses nothing, ranks nothing and edits neither the pitch nor the site.** The Owner chooses.

## Part 1 — the pitch on main, verified

**Checked against `main`:** your pasted text matches `docs/de/index.md` and `docs/index.md` at every line that
changed since the claim screen (E):

- the claim;
- the tagline;
- *unserem eigenen* / *our own*;
- *28 Stunden* / *28 hours*;
- *9 von 13* / *9 of 13*;
- the *FM-026* line;
- the adopt-note link.

The rest was not re-compared word for word.

| # | Finding | Where | Class |
|---|---|---|---|
| P1 | **The adopt note the page sends an outside fleet to is five minor releases stale.** It pins `v0.12.0` and that release's SHA-256, while `VERSION` is `0.17.8`. An outside fleet that follows it runs a tool without `[seats]`, sessions or `--answer`, so the *one-shot integration* the pitch sells starts on a version the page does not describe | `ADOPT.de.md:27–29`, `VERSION` | E |
| P2 | **An internal id is on the pitch:** *als FM-026 erfasst* / *filed (FM-026)*. Neither reader knows what FM-026 is | `docs/de/index.md:38`, `docs/index.md:36` | E |
| P3 | **The measured paragraph does not carry the Owner's frame:** the record before, the reset, the record since. The page says *before* and *after, in the first 28 hours under the rule*. It does not say that *before* is nine months of record, it does not name the reset, and *the rule* is a rule the reader has not been told | `docs/index.md:15–18`, and DE | E |
| P4 | **The tagline puts the mark on paper.** A shoal mark stands in the water, and the chart draws it. *Eine Markierung auf der Seekarte* / *A mark on the chart* says the chart is marked. A reader who sails will notice; the seaman's German word is *Seezeichen* | `docs/de/index.md:3`, `docs/index.md:3` | K |
| P5 | **The German page mixes dash styles.** The new line uses the English em dash (*Projekt — unserem eigenen —,*), while the rest of the German page uses the German en dash (*– ein Satz pro Frage, einmal am Tag –,*) | `docs/de/index.md:15` vs `:7–8` | E |
| P6 | **One line promises more than the tool enforces.** *Die letzte Nachricht jeder Session endet mit dem, was auf Sie wartet* / *every session's last message ends with what waits for you*: the tool supplies `--owner`, and the agents' contract asks for it, but nothing enforces it. Said as a promise, it is the kind of line this reader tests | `docs/index.md:42` | I |
| P7 | **The German claim on the page is still the mirrored line** that the claim screen's third pass kills at G0. The Owner's choice among the survivors is pending | `docs/de/index.md:5` | E |

None of these is edited here.

### Corrections to the claim screen, on the Owner's words

The Owner's words, 23:20, relayed:

> *"shoalmark is the 'reset' that sets the record straight."* The diagnosis rests on nine months of record in the
> author's own project: about 10,000 contributions in a year, 200 merges unread in 22 days, and one incident. Only the
> remedy's measurement is 28 hours old.

1. **"Anecdote" is withdrawn.** The claim screen's reader addendum wrote that an investor *reads n = 13 in one day, in
   the founder's own repository, as an anecdote*.
   - The project is not an anecdote: its diagnosis is nine months of record.
   - What is young is only the remedy's count: 28 hours, 13 pull requests.
   - The *Measured, not promised* paragraph should read: the record before, the reset, the record since (P3).
2. **The investor is never a test reader.** The claim screen's reader-test protocol listed *the investor or investors
   the Owner is in contact with*. That is struck: **proxies only**, readers who are like the investor (German,
   fluent in English, technical, well educated) but are not the investor.

The same two corrections are appended to `gtm-claim-screen-2026-09-23.md`.

## Part 2 — the mark

### The brief, as given

- **What the name means, literally:** a shoal mark is a beacon (a stake or spar with a topmark) or a buoy standing
  in shallow water. It is read in one glance from a moving deck.
- **The register:** a warning, not a decoration; a provocation the owner can take; no mascot.
- **Where the mark lives:** the site header, the browser tab at 16 px, the board's header, a README and a terminal.
  So it must work first in one colour, on a light and on a dark ground. **German first:** no English pun.
- **Three directions:**
  1. the chart symbol itself;
  2. the isolated-danger topmark, two balls on a stake;
  3. a typographic mark with no separate icon.
- **The gates**, knockout before rationale:

  | Gate | Kills on |
  |---|---|
  | G0 | does not read at 16 px in one colour |
  | G1 | a sailor would not recognise it as a shoal or danger mark. An anchor, wheel, wave, lighthouse or lifebuoy is dead on sight, as is an octopus or anything of its kind |
  | G2 | it reads as a badge, not a warning, or it softens the claim beside it |
  | G3 | an existing developer-tool or nautical mark has the same shape |
  | G4 | the wordmark is not one typeface family that lives in the board's monospace world without being monospace on the page |
  | G5 | icon and wordmark do not read as one thing at header size and as two at favicon |

**Two corrections to the brief's own sentence,** for the reason given to someone who sails (K):

- Marks are laid by the authority that keeps the aids to navigation (in Germany, the WSV). The chart-maker (the BSH)
  surveys them and draws them.
- A mark stands over a known danger, not necessarily where a ship ran aground. As metaphor the brief holds; as fact
  it would be corrected by a reader who sails.

### How the renders were made (E)

- **The icons:** `mark/marks.py sheet` writes each candidate's SVG, then renders every candidate at exactly 16 px, in
  one colour, black on white and white on black.
  - `renders/sheet-16px.png` is the real 16 px raster, with 64 px beside it.
  - `renders/sheet-16px-x8.png` is each 16 px crop shown ×8, nearest-neighbour.
  - `renders/<id>-16px-{light,dark}.png` are the crops themselves.
- **The first draw is kept** as `renders/sheet-16px-first-draw.png`. B1 and A6 were redrawn on the pixel grid after
  it: a 1 px gap on a half pixel blurred both. It was the same fix for both, and the first draw is the record of
  the fault.
- **The headers:** `mark/marks.py header` takes **the built site's own start page** (from `595fc80`), puts the
  candidate in the logo slot and the typeface on the name, and screenshots it at 1440 px. The logo slot shows only
  from 1220 px up.
  - **Main has no dark scheme:** the built page loads no palette stylesheet, so the site as configured has no dark
    mode. The `slate` renders inject Zensical's own palette stylesheet and are marked as a preview.
- **The typefaces:** `renders/type-sheet.html` is a committed source, rendered by `marks.py type`. Its fonts came from
  Google Fonts, and the page itself reported them loaded: Plex, Geist, Recursive, Inter, JetBrains Mono.
- **Every render in this ledger was looked at by this runtime at true size and enlarged.** The verdicts below are
  read off the pixels, not off the SVG.

### The ledger

The controls come first, and the candidates follow in the order of the gate that stopped them. The order is not a
rank.

| # | Candidate | First fatal gate | One-line reason | Class |
|---|---|---|---|---|
| K0 · control | a filled square (the render pipeline) | **G1** | It renders crisp at 16 px, so the pipeline is sound (G0 passes), and a square is no mark | E |
| K1 · control | the site's placeholder, lucide *book-open* | **G1** | It reads as a book at 16 px | E |
| K2 · control | a lighthouse | **G1** | Dead on sight, by the brief's own list | E |
| A3 | chart beacon as drawn: position circle, thin stake, small topmark | **G0** | The 1 px stake falls on a half pixel and renders grey, and the topmark smears. At 16 px it is a dotted grey line | E |
| A4 | chart danger symbol: dotted danger line around a cross | **G0** | The dotted ring breaks into speckle at 16 px. What is left is a crosshair | E |
| A1 | chart beacon: north cardinal, two cones up | **G1** | It reads as an up-arrow (*scroll to top*), at 16 px and at 64 px alike | E |
| A2 | chart beacon: west cardinal, cones point to point | **G1** | It reads as an hourglass over an up-arrow | E |
| A5 | the German *Pricke*: a withy stake with its twigs | **G1** | It reads as a broom, or a Y. Only a Wadden sailor sees a *Pricke* | E |
| A6 | chart beacon as drawn, pixel-aligned: two balls, stake, position circle | **G1** | Crisp once it is drawn on the pixel grid, but the ring and shaft read as a key or a thermometer | E |
| B2 | two balls on a stake, with a water line | **G1** | The stake crossing the line near its foot reads as an inverted cross | E |
| B3 | the pillar buoy with its topmark | **G1** | It reads as a chess pawn | E |
| B4 | the two balls alone | **G1** | They read as an *8*, or a colon | E |
| C2 | typographic: the *l* as a stake through a water line (its 16 px form) | **G1** | It reads as a †, which in German print marks a death | E |
| C1 | typographic: the *l* of the wordmark carries the topmark; its favicon is B1's glyph | **G1** | At header size the two dots are 3 px squares stacked on the *l* (`renders/header-C1-*`). They read as a dotted top to the letter, not as two balls | E |
| C1b | typographic: the *l* cut to x-height, the topmark inside the ascender | **G1** | The cut *l* reads as an *i*, so the word reads *shoaimark*, and the topmark reads as its dot (`renders/type-sheet.png`) | E |
| **B1** | isolated danger: two balls on a stake, pixel-aligned | **survives** | — | E / I |

**What each gate killed:**

| Gate | Candidates killed |
|---|---|
| G0 | 2 |
| G1 | 10, and all three controls |
| G2 | 0 |
| G3 | 0 |
| G4 | 0 among the marks (the typeface sub-ledger is below) |
| G5 | 0 |

**One survives.** This seat's favourite, A5 *die Pricke* (the German-first idea), died in writing at G1.

### The wordmark's typeface — G4, screened on its own

Rendered in `renders/type-sheet.png`.

| # | Family | G4 | Reason | Class |
|---|---|---|---|---|
| T1 | IBM Plex: Sans and Mono | **survives** | One superfamily, OFL: the Mono lives on the board, the Sans on the page | E |
| T2 | Geist: Sans and Mono | **survives** | One family, OFL, the same split | E |
| T3 | Recursive | **survives** | One variable family, OFL, with a `MONO` axis from 0 to 1. The page and the board are one font on one axis | E |
| T4 | Inter with JetBrains Mono (the site today) | **dies** | Two families, not one | E |
| T5 | Berkeley Mono (the board today) | **dies** | Monospace only, and a commercial licence that cannot ship in an Apache-2.0/MIT repository | K |
| T6 | JetBrains Mono alone | **dies** | Monospace on the page | E |

**Each survivor's strongest counterfact:**

- Plex is IBM's corporate face.
- Geist is Vercel's house face, and among developer tools it reads as Vercel's.
- Recursive is the least known, with a character of its own.

Choosing among them changes the board's monospace, which is FM-002's brand layer. The header renders below use T1
throughout, **for comparability only; any of T1–T3 pairs with the survivor.**

### The survivor

#### B1 · the isolated-danger beacon: two balls on a stake

**Renders (E):**

- 16 px, one colour: `renders/B1-16px-light.png`, `renders/B1-16px-dark.png`, and ×8 in `renders/sheet-16px-x8.png`.
- The header beside the claim, built from main:
  - `renders/header-B1-ibm-de-default.png`
  - `renders/header-B1-ibm-de-slate.png` (the dark-scheme preview)
  - `renders/header-B1-ibm-en-default.png`
  - `renders/header-B1-ibm-de-default-dpr2.png` (retina)

**Gate by gate:**

- **G0:** crisp at 16 px on both grounds, the two balls separated by a clean pixel row.
- **G1:** it *is* the mark (K). The IALA isolated-danger topmark is two black spheres, one above the other, on a
  mark over a danger of limited extent with navigable water all round: *here, exactly here*.
- **G2:** at DPR 2 it reads as two balls on a stake. Not fatal as established, but see the counterfact.
- **G3:** no object observed (E), in three web searches on 2026-09-23 (US index only):
  - *"isolated danger mark" logo app icon*;
  - *developer tool logo two dots on a stake beacon buoy icon*;
  - *"shoalmark" OR "shoal mark" logo software*.

  A search that finds nothing is not a clearance. Nautical apps' icons were not checked one by one.
- **G4:** any of T1–T3.
- **G5:** in the header, icon and name read as one lockup, and at favicon the glyph stands alone.

**Why it means "shoal mark" to someone who sails:** a shoal mark is *a mark set to indicate shoal water, as a stake
or buoy* (Wordnik, the dictionary sense, found in the search above). The two balls are the topmark every sailor
trained on IALA buoyage learns as *isolated danger*: the one mark that says the danger is right here, and the water
around it is safe.

**Strongest counterfact, fatal if confirmed:** at DPR 1, in the header, the lower ball fuses into the top of the
stake, and the figure reads as the letter **i**, the information sign (`renders/header-B1-ibm-de-default.png`).

- An *i* beside the name is a help badge, not a warning, and that fails G2.
- At DPR 2 the two balls read, and an investor on a laptop sees DPR 2. One of the first two outside owners, on
  Windows, likely sees DPR 1.
- **This seat cannot settle which reading a stranger takes first,** so B1 survives narrowly, on the record.

### What the controls and gates showed

- **The pipeline is sound:** K0 renders crisp, so the G0 kills are the candidates' own.
- **The site's placeholder and the tempting wrong answer die where they should:** K1 and K2 at G1.
- **At 16 px the chart vocabulary collides with the alphabet and the interface.** Topmarks become *i*, arrows, an
  hourglass, a key or a cross. **G1 did most of the work,** and it did it on rendered pixels, not on intentions.

### What this seat did not run

- **No sailor and no proxy reader has seen any render,** and G1 and G2 are this runtime's reading of the pixels.
  - The decisive test for B1 is cheap: show `header-B1-ibm-de-default.png` and the 16 px tab to two or three proxy
    readers and ask what the mark is. If *i* or *info* comes first, B1 dies at G2.
  - Ask one reader who sails too.
- **No trademark or registry search, and no check of individual nautical app icons.** G3 is three web searches,
  US-indexed.
- **No render in the board's header or in a terminal.**
- **No colour version.** The brief sequences one colour first.
- **No second typeface in the header renders.** T1 only, for comparability.

### Handoff

- **Conclusion:**
  - Sixteen marks were screened: three controls, ten icon candidates and three typographic ones. **One survives,
    B1, narrowly.** Direction 1 and direction 3 have no survivor.
  - Three typefaces survive G4.
  - The pitch on main has seven findings, P1 (the stale adopt note) the heaviest. Two corrections to the claim screen
    are made in writing.
- **Strongest counterfact:** B1 may read as *i*, and that would leave this field empty.
- **Unresolved unknown:** what a stranger, and what a sailor, calls B1 at first sight.
- **Closure and reversal:**
  - B1 dies at G2 if proxy readers say *i* first.
  - A dead candidate revives only if the Owner rules a gate differently. For example, he may accept the *Pricke*'s
    German-only recognition at G1.
- **Seat shadow:** this seat's own drawing blurred B1 and A6 on the first pass. The same correction was applied to
  both, and the first draw is kept. No candidate was redrawn after its death to rescue it; A6 is a new candidate, and
  A3 stays dead.
- **Authority:** nothing is chosen, and nothing in the pitch or the site is edited. **The Owner chooses.**

**Provenance:** Seat: GtM · Session `e0be0fa0` · Model: Claude Opus 5.5 · 2026-09-23 · on the Owner's brief for the
wordmark and icon.

---

## Outcome — the Owner's rulings, recorded 2026-09-24 07:35 CEST, session `6cecddb3`

**This ledger ends with *B1 survives, narrowly* and *A5 (the Pricke) dies at G1*.** The mark was decided afterwards,
by the Owner, and this note points to his rulings. **Nothing above is rewritten.**

1. **G1 waived for the Pricke** (2026-09-23, relayed, spelling normalised): *"Do the broom also. Who cares if people
   know the meaning — I know it. It has to render visually attractive, then it is fine."*
   - The Implementer drew it as `a`–`d`, in `mark/pricke/pricke-2026-09-23.md` (`683e7b8`, merged in PR #30).
   - The meaning gate that killed A5 here does not apply to it.
2. **The mark is `d`, at 16 px.**
   - At ≈ 00:55 the Owner locked `a` in the header, with `d` as the tab.
   - At ≈ 01:05 he tried `d` alone: *"let's try d alone as proposed with the mono, this could be stellar"* (`69c14b2`).
   - On 2026-09-24 he ruled: *"16 px is the better-fitting one; we could try a 24 px variant, but 16 px will do"*
     (`9875bfc`, `mark/pricke/renders/lockup-scale.png`).
   - At the time of writing these three commits are on `fm/006-the-site-wears-the-pricke`, not yet merged.
3. **The wordmark is IBM Plex Mono.**
   - IBM Plex was ruled as the family in `3f8ab19`.
   - **G4 here read *without being monospace on the page*, and the Owner ruled that clause away.** Its other clause,
     one family, holds: Plex Sans for the page text, Plex Mono for the name.
4. **B1** was held for the stand-in readers in `3f8ab19`. The Owner's choice of `d` makes that test moot for the mark.

**A fact this ledger's A5 row missed, recorded now (E, de.wikipedia *Pricke*):**

- The port-hand Pricke's crown is the ***Besen nach oben***, and a channel marked with them is a ***Besenstraße***.
  *Broom* is the sailors' own word.
- A5 died here with *"it reads as a broom … Only a Wadden sailor sees a Pricke"*. A stranger who sees a broom is
  seeing what the sailors call it. The verdict stands as recorded at the time; this is the fact it lacked.
- `d` is the port form: twigs bound below, splaying upward. That is the Pricke used most, per the same article.

**What this seat sees in the finalized lockup** (`lockup-scale.png`, the 16 px tab ×10, `d.svg`; **E** unless marked):

- **At 16 px, `d` holds exactly two values, full ink or empty, on light and on dark.** No other mark drawn in these
  screens did.
- **The stake matches the name's stems** at ×1, ×2 and ×4, as the Implementer's table prints.
- **Three things to watch; none of them is a verdict:**
  1. **At ×4 the 1 px diagonals are visible stair-steps beside smooth type.** A slide or a projector shows exactly
     that. Either own it as pixel art, or use the vector `a` above about 48 px.
  2. **On dark, the theme draws the mark at 189 of 255 and the name at 255,** so the mark is dimmer than the name
     (visible in the dark rows). One CSS line would give them the same ink.
  3. **A stranger's first reading is a Y, an antenna or a Ψ (I).** The Owner has ruled that meaning does not matter.
     It follows that the page should say *Pricke* once, so the investor hears it before thinking *antenna*. The
     tagline is the place for it, and it is also finding P4.

## The tagline, naming the Pricke — drafts, screened

The Owner asked for this 2026-09-24; it is a draft until he rules. **The bar is the tagline on the page:** *Eine
Markierung auf der Seekarte, die die Flotte vor dem Auflaufen bewahrt.* / *A mark on the chart that keeps the fleet off
the shoal.* That is P4's line: it puts the mark on the chart.

**The facts every draft is held to (E):**

- A Pricke is *"meist junge Birken oder Stangen mit Zweigbüscheln"*. It marks *"ein schmales und flaches Fahrwasser
  (meistens im Wattenmeer)"* (de.wikipedia, *Pricke*).
- Its English counterpart is the ***withy***, used *"to mark minor tidal channels in UK harbours and estuaries … to
  indicate where the deeper water lies"* (en.wikipedia, *Withy*).
- Which side of a channel a mark stands on depends on the direction of travel.

**The gates:**

| Gate | Kills on |
|---|---|
| G0 | more than one line · more than 12 German words (counted in code) · does not name the Pricke · jargon or ids |
| G1 | not native German, or an English twin that is not native English |
| G2 | not true to the facts above, or it still puts the mark on the chart |
| G3 | a register that is not the claim's: a warning mark, not a postcard |
| G4 | it clashes with the page: it repeats or pre-empts the claim, or breaks the fleet that the next line addresses |
| G5 | weaker than the bar: it must keep what the bar does, the fleet kept off the shoal |

| # | German | English | First fatal gate | One-line reason | Class |
|---|---|---|---|---|---|
| D4 | Birke im Schlick: Wer an der falschen Seite fährt, sitzt auf dem Watt. | Birch in the mud: pass it on the wrong side and you are on the flats. | **G0** | 13 words | E |
| D5 | Eine Pricke im Watt – links Fahrwasser, rechts Grund. | A withy in the mud: channel to the left, ground to the right. | **G2** | Left and right depend on the direction of travel. The line is false half the time | E |
| D3 | Die Pricke steht, wo das Watt beginnt. | The withy stands where the flats begin. | **G5** | True and terse, but it says where the mark stands, not what it does for the fleet. It drops what the bar carries. *This seat's favourite, killed in writing* | I |
| D1 | Die Pricke im Watt: Sie zeigt der Flotte, wo das Fahrwasser endet. | A withy on the flats shows the fleet where deep water ends. | survives | — | I |
| D2 | Eine Pricke im Watt – sie hält die Flotte im Fahrwasser. | A withy in the mud keeps the fleet in the channel. | survives | — | I |
| D6 | Eine Pricke im Watt, die die Flotte vor dem Auflaufen bewahrt. | A withy on the flats that keeps the fleet off the shoal. | survives | — | I |

**The survivors, unranked:**

- **D1** says what a Pricke does: it shows where the navigable water ends. It carries the fleet.
  - *Counterfact:* it is at the 12-word limit, and *endet* can be misread as the channel's end, not its edge.
- **D2** is the shortest that keeps the fleet, and it says it positively: *im Fahrwasser*.
  - *Counterfact:* it guides rather than warns. The danger is only implied.
- **D6** is the bar with P4 fixed: the chart becomes *eine Pricke im Watt*, and the rest is kept word for word.
  - *Counterfact:* it keeps the bar's *die die*, which a reader stumbles on when reading aloud.

**Common to all three English twins:**

- *withy* is the native word, but it is British. A German reading the English page may know neither *withy* nor
  *Pricke*. Keeping *Pricke* in the English, as a name, is the alternative.
- A Pricke marks a narrow, shallow channel. A *fleet* in it stretches the picture, and it stretches it for the bar
  just as much.

**Not run:** no native German or English reader, no sailor. Nothing on the page is edited. **The Owner chooses, or
keeps the bar.**

**Provenance:** Seat: GtM · Session `6cecddb3` · Model: Claude Opus 5.5 · 2026-09-24 · on the Owner's approval of the
Principal's recommendation.

---

## The tagline — ruled, 2026-09-24 07:50 CEST, session `0cbdba3f`

**The Owner, in chat:** *"D2 shall then be renamed for the english variant to 'A Pricke on the Wadden flats …'"*

This followed the seat's answer that *withy* is the British counterpart, a plain stick in UK estuaries, and not the
German Pricke with its twig crown (en.wikipedia, *Withy*; de.wikipedia, *Pricke*).

| | Line |
|---|---|
| **DE** | *Eine Pricke im Watt – sie hält die Flotte im Fahrwasser.* |
| **EN** | ***A Pricke on the Wadden flats keeps the fleet in the channel.*** (the Owner's opening, completed with the rest of D2's English: 12 words, counted in code) |

- ***Pricke* is kept in English as a name.** It matches the mark `d`, it is German-first, and it is the word said
  aloud in the pitch. D2's *withy* twin above is superseded.
- **D2's counterfact stands:** it guides rather than warns, and the danger is implied.
- **This seat does not edit the page.** Applying the line to `docs/de/index.md:3` and `docs/index.md:3`, in place of
  the tagline that P4 flagged, is the Implementer's slice.
