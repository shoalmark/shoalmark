# GtM screen — FM-006, the pitch's second claim, facing the owner

- **Date:** 2026-09-23, 22:02–22:10 CEST (`date`)
- **Seat:** GtM (`gtm@seat`), Owner-convened 2026-09-23 22:02 · **Session:** `ee61f1fe` · **Model:** Claude Opus 5.5
- **Base:** `589d328` on `fm/006-the-human-pages-open-from-a-file`. The screen reads the pitch there
  (`docs/index.md`, `docs/de/index.md`).
- **Disclosure:** this runtime wrote the pool **and** screened it. It wore two hats in sequence, and no independent
  check has run on this file. The pool was not written blind to the gates.
- **This seat chooses nothing, ranks nothing and does not edit the pitch.** The Owner rules.
- **Second pass, 2026-09-23 22:24, session `2ab3afad`, appended below the first.** It corrects the first pass's third
  G2 anchor (*0 → 17 of 21 … independent* is not in the record). It screens the German claim (*Owner* vs *Eigner*,
  *leistungsstärkeren* vs *besseren*) and re-reads the second claim beside the new bar. The first pass stands as
  filed.

## Cold start

1. **What virtue do I bring?** Legibility to a stranger: an owner who owes this page nothing and reads one line.
2. **How does it turn into blindness?** Three ways. Writing to the Owner's taste. Falling for a line of my own. Arguing
   a line past a gate it has already failed.
3. **What would show that failure here?** The control surviving on deference. A favourite of mine surviving on charm. A
   row whose reason is written after its death.
4. **Who gets the record, independently of me?** A different seat on a different runtime, then a German native reader
   for G1, then the Owner.

## The direction, as given, and how it was applied

**The slot:** ONE second claim for the pitch, facing the owner. It stands beside the Owner's line, *How to get a
better-performing human owner* / *Wie man einen besser funktionierenden menschlichen Owner bekommt*. That line stands,
and it is the bar.

**The gates**, knockout before rationale. For each line the ledger records the **first** fatal gate, and the screen
stops there.

| Gate | Kills on |
|---|---|
| **G0** form | not one line · more than 12 words · not addressed to the owner · not a provocation he can take · jargon · internal ids |
| **G1** language | not native in German **and** in English (a German reader must not hear a translation) · an idiom slip |
| **G2** truth | anything the record cannot prove today. The record proves four things: one command = one signed answer; a fifteen-minute sitting; an independent review file before a pull request is opened; the board saying which review was independent. Any promise of delegation, speed or *no more merges* dies here |
| **G3** the Owner's never | the line degrades the owner to a push-a-button; it promotes rubber-stamping; it flatters him into pressing; it insults him |
| **G4** both ways | read beside the fleet's line (`docs/index.md:7`): it does not provoke the owner **and** tell the fleet what changes |
| **G5** the bar | read beside the Owner's line: the line is weaker, or it adds nothing his does not say |

**The four anchors G2 admits**, each read in the tool at `589d328`:

- *One command = one signed answer.* `shoalmark.py:829`, `answer_cmd`: it cuts the branch, writes the three lines,
  commits signed and pushes. Only a seat that holds `answer` may answer (`shoalmark.py:2210`, `may_answer`).
- *A fifteen-minute sitting.* `shoalmark.py:806, 810`: `standup_minutes`, which defaults to 15, and the `.ics` invite.
- *An independent review file before the pull request.* `docs/index.md:17`: **0 → 17 of 21**, cited as the page
  states it. **Not recounted.**
- *The board says which review was independent.* `shoalmark.py:2745`: independent · same session.

**How this seat read two clauses.** The Owner can overrule either reading.

- **G2** was applied to what a line says shoalmark does, did or will do for the owner. A line's picture of the reader
  (*you are the bottleneck*, *you are asked too often*) is not a product claim, so it was judged at G3. Read
  strictly, G2 would also kill that picture. **That reading changes one row:** C10 dies at G2.
- **Register:** every German line uses *Sie*, as the page does. No *du* line was written.

**Evidence classes:**

- **E** executed: a quote, a count or a read, with its path.
- **K** knowledge of this runtime, reproducible by any reader of the language.
- **I** inferred.

## The ledger

The control comes first. The candidates follow in the order of the gate that stopped them. **The order is not a rank.**
The word counts are executed (**E**, `python3`, split on whitespace). Every line is ≤ 12 words in both languages, so
no line died on its length.

| # | German | English | First fatal gate | One-line reason | Class |
|---|---|---|---|---|---|
| **C0** · control | Wie man einen besser funktionierenden menschlichen Owner bekommt | How to get a better-performing human owner | **G0** | It is not addressed to the owner. It speaks of him in the third person to whoever wants a better one. Its ruling says it *faces the fleet* (the FM-006 tracker, line 38), and it heads the page above both blocks (`docs/index.md:5`) | E |
| C8 | Fünfzehn Minuten am Tag, für das, was nur Sie entscheiden können. | Fifteen minutes a day, for what only you can decide. | **G0** | A reassurance, not a provocation: it asks nothing of him and questions nothing | I |
| C1 | Ihre Agenten warten nicht auf Werkzeuge. Sie warten auf Sie. | Your agents are not waiting for tools. They are waiting for you. | **G1** | *Sie warten auf Sie*: one capitalised word, two referents (*they*, then *you*), four words apart. Read aloud, it collapses. The page's own German has the same trap: *Sie holen* means the agents, and ***Sie** schreiben* means the owner, bolded to tell them apart (`docs/de/index.md:24, 29`). The fleet block avoids it with *ihr* (`:7`) | E |
| C2 | Machen Sie Ihre Agenten nicht zu Bittstellern. | Don't turn your agents into supplicants. | **G1** | The English twin is a translation. No English-speaking owner says *supplicants*, and English has no word that carries the German *Bittsteller* at a counter | K |
| C3 | Hören Sie auf, jede Frage selbst zu beantworten. Ihre Agenten können das. | Stop answering every question yourself. Your agents can. | **G2** | It promises delegation. Only a seat that holds `answer` may answer an ask (`shoalmark.py:2210`); agents that answer for him are what the tool refuses | E |
| C4 | Ihre fünfzehn Minuten am Tag – oder drei Tage Stillstand pro Frage. | Your fifteen minutes a day, or three days' standstill per question. | **G2** | It turns one observed question (*one question, open three days*, `README.md:6`) into a rate per question, and its *or* promises same-day speed | E |
| C5 | Unterschreiben statt abnicken. | Sign it. Don't nod it through. | **G3** | The one thing it asks of him is the signature. The command makes that signature from his key in one call (`docs/index.md:36`), and *a signature proves which key was used, not which hand* (`docs/signing.md:15`). The nod becomes a keystroke: the push-a-button in better clothes | E |
| C6 | Sie sind der Engpass. Und das ist richtig so. | You are the bottleneck. And rightly so. | **G3** | Flattery. It makes a virtue of the position everything waits on, and the record names that position as the root of the stamping: *Blocking and stamping have one root* (`README.md:9`) | E |
| C7 | Wann haben Sie zuletzt gelesen, was Sie freigegeben haben? | When did you last read what you approved? | **G4** | It provokes the owner, but its remedy is his own reading. Beside the fleet's line it changes nothing the fleet does | I |
| C9 | Ihre Agenten arbeiten an Ihnen. | Your agents are working on you. | **G5** | The bar turned to face him, and nothing more. It says what *How to get a better-performing human owner* already says, in the second person | I |
| C10 | Sie sind nicht zu langsam. Sie werden zu oft gefragt. | You are not too slow. You are asked too often. | survives | — | I |
| C11 | Ihr Nicken ist keine Entscheidung. | Your nod is not a decision. | survives | — | I |
| C12 | Wer hat eigentlich geprüft, was Sie freigegeben haben? | Who actually checked what you approved? | survives | — | I |

**What each gate killed:** G0 2 (the control and C8) · G1 2 · G2 2 · G3 2 · G4 1 · G5 1 · three survive. Every gate
killed at least one line.

## The survivors — three, unranked

They are listed in the order of their German line, and **the order is not a rank**. Their virtues are written down
only now that they have survived. Each carries its strongest counterfact.

### C10 · *Sie sind nicht zu langsam. Sie werden zu oft gefragt.* / *You are not too slow. You are asked too often.*

- **What it adds beside the bar:** the cause. The bar says the owner can perform better; this line says what stops
  him: the frequency of the asking, not his speed. That is the README's own diagnosis (*a person asked for many small
  decisions in the middle of the work*, `README.md:9`).
- **Both ways:** it provokes the owner, and it tells the fleet to ask less often, for one sitting a day (the
  fifteen-minute anchor).
- **Strongest counterfact:**
  - Beside the bar, it can read as a retraction: the headline says *better-performing*, the second line says *not too
    slow*.
  - Some owners keep up by stamping (`README.md:7–8`). To them, *not too slow* can sound like absolution.
  - **It dies at G2 if G2 is read strictly** (see *How this seat read two clauses*).

### C11 · *Ihr Nicken ist keine Entscheidung.* / *Your nod is not a decision.*

- **What it adds beside the bar:** what the bar's *performing* means. A decision is on record; a nod is not. It is
  true in the tool: an ask stays open until a written answer lands, and a rejection must carry its reason
  (`shoalmark.py:829–848`, `answer_cmd`).
- **Both ways:** it provokes the owner, and it tells the fleet that a nod, a chat *ok* or a merge is no longer an
  answer.
- **German:** *abnicken* stands behind *Nicken*, and a German reader hears the idiom, not a translation.
- **Strongest counterfact:**
  - The owner block right under the headline already says it: *Sie nicken ab* / *you stamp* (`docs/de/index.md:10`,
    `docs/index.md:10`). The page would say it twice.
  - Beside *One command per answer* (`docs/index.md:36`), a reader can fill in *the command is the decision*. That
    lets C5's G3 death back in by the side door.

### C12 · *Wer hat eigentlich geprüft, was Sie freigegeben haben?* / *Who actually checked what you approved?*

- **What it adds beside the bar:** what his approval rests on. The bar speaks of the owner's performance; this line
  speaks of the check under it.
- **Its answer is two of the four anchors:** the independent review file before the pull request (`docs/index.md:17`)
  and the board that says which review was independent (`shoalmark.py:2745`).
- **Both ways:** it provokes the owner, and it tells the fleet that every approval must now show who checked it, and
  whether that check came from the session that wrote the work.
- **German:** *eigentlich* makes the question native. It is the word a German asks this question with.
- **Strongest counterfact:**
  - The board's *independent* can become the new thing he approves on: a stamp with a better label.
  - The line's force rests on the 17 of 21, which this seat did not recount.

## What the control showed

**The Owner's line died at G0,** on the addressee clause: it speaks *about* the owner, to whoever wants a better one.

- **For the slot, this is the finding:** the bar and the second claim are different forms. A second claim in the bar's
  form would be a second headline, not a line to the owner.
- **The control proves that G0 fires on the Owner's own line.** The gate was not bent to his taste.
- **What the control does not prove:**
  - G1–G4 were not run on it, because the screen stops at the first fatal gate.
  - G5 cannot be run on the bar itself.
- **The ledger shows the other gates are real:** each killed at least one line, with its reason and its class.
- **This is no verdict on the Owner's line as a headline.** It stands where it is.

**Two of this seat's own favourites died in writing:**

- C5, *Unterschreiben statt abnicken*, at G3.
- C9, *Ihre Agenten arbeiten an Ihnen*, at G5.

## What this seat did not run

- **No native reader.** G1 is this runtime's knowledge (K) in both languages. No German native and no English native
  has read a line, so this is the gate most likely to be wrong.
- **No outside owner** has read a survivor. Whether he takes it as a provocation or as an insult (G3) is inference.
- **No web search for prior use.** No survivor was searched as someone else's slogan, though that search is the
  cheapest fatal.
- **The 0 → 17 of 21 was not recounted.** It is cited as `docs/index.md:17` states it.
- **The control stopped at G0.** G1–G4 were not run on it.
- **Nothing was rendered.** No survivor was set into the page or seen under the headline on the built site.
- **No *du* line** was generated.
- **No independent hostile review** has run. The pool and the screen are one runtime's.

## Handoff

- **Conclusion:** twelve candidates and the control were screened, knockout first. **Three survive: C10, C11 and C12,
  unranked.** The control died at G0, and every gate killed at least one line.
- **Strongest counterfact:** a German reader must not hear a translation, and the runtime that wrote the lines judged
  that. Any survivor may still die at G1.
- **Unresolved unknown:** does an outside owner take these lines as a provocation or as an insult?
- **Closure and reversal:** a survivor is out if:
  - a native German reader hears a translation;
  - a search finds it as someone else's line;
  - the Owner reads G2 strictly, which takes out C10.

  A death reverses only if the Owner rules the gate differently.
- **Seat shadow and its controls:**
  - *Taste-matching:* the Owner's line went through the gates and died at G0 in writing.
  - *Attachment to its own coinage:* two of this seat's favourites died in writing (C5, C9).
  - *The rescue reflex:* no row argues past its gate.
- **Authority boundary and next recipients:** this seat has not chosen, ranked or edited the pitch. The next readers
  are:
  1. an independent hostile review, by a different seat on a different runtime;
  2. a German native reader, for G1;
  3. the Owner, who rules.

**Provenance:** Seat: GtM · Session `ee61f1fe` · Model: Claude Opus 5.5 · 2026-09-23 · on the Owner's convening, under
the seat's charter (generate, screen, ledger; never choose).

---

## Second pass — 2026-09-23 22:24 CEST, session `2ab3afad`

The Owner convened this pass after his claim changed.

- **What was open for the screen:** *Owner* vs *Eigner* in German, *leistungsstärkeren* vs *besseren*, and the second,
  owner-facing claim.
- **Where it reads the pitch:** the tip of `fm/006-the-human-pages-open-from-a-file`, `32e92f8`, read there by `git
  show`. This branch stays cut from `589d328`, and none of its files moved on the pitch branch.
- **This session:** a new row in `sessions.md`. It runs in the same harness session as `ee61f1fe`, and the tool uses
  an id once (`shoalmark.py:2530`).

### What changed since the first pass

- **The claim is the Owner's.**
  - English: *Get a better-performing human Owner.*, from `82a20cb` (`docs/index.md:5`).
  - German: *Hol dir einen leistungsstärkeren menschlichen Eigner.*, from `53d4277`, which has landed
    (`docs/de/index.md:5`).
- **The register is ruled.** The claim commands the fleet (*du*) and provokes the owner by talking about him. The
  owner pages stay in *Sie*.
- **The German pages say *Eigner* for the person.** Counted here at `32e92f8` (**E**):
  - *Eigner* 7 times: `index` 4, `setup` 2, `signing` 1;
  - no capitalised *Owner*;
  - lower-case `owner` 5 times, all code or the seat name. The Reviewer's delta on `53d4277` counts the same.
- **The measured block is now the record's own:**
  - *Before:* the last 200 pull requests were merged unread.
  - *After, in just over a day:* 9 of 13 carried a Reviewer's file before they were opened (`docs/index.md:17–18`).
  - The board *reports*, for every review, whether it came from another session. *A report, not a proof: git cannot
    yet show it* (`:23–24`).

### Correction to the first pass

The first pass took four G2 anchors from its brief.

- **The third anchor was wrong.** It read *an independent review file before a pull request is opened*, cited as
  *0 → 17 of 21* from `docs/index.md:17` at `589d328`, and it is not in the record.
- **The Reviewer found it** (R3, P1, on `589d328`): the source holds **9 of 13** with a *Reviewer's* file, and in the
  same paragraph it says git cannot tell whether a pass was independent.
- **This seat flagged the number as not recounted, and used it anyway.** It should not have.

**The anchors, as the page states them at `32e92f8`:**

1. one command, one signed commit per question (`docs/index.md:22, 41`; `shoalmark.py:829`);
2. one sitting, fifteen minutes (`docs/index.md:40`; `shoalmark.py:806`);
3. before: the last 200 pull requests merged unread; after, in just over a day: 9 of 13 with a Reviewer's file
   before opening (`docs/index.md:17–18`);
4. the board reports whether a review came from another session than the code it judged. It is a report, not a proof
   (`docs/index.md:23–24`).

**What the correction moves:** no verdict. No line dies and none revives. C12's counterfact is rewritten below.

### The German claim — four variants

**The English line is not screened: it is the bar.** Three gates are adapted to the headline slot, and this is how:

- **G0:** the addressee clause turns. Per the ruled register, the headline commands the fleet (*du*) and provokes the
  owner by talking about him. The rest of G0 stands.
- **G2:** the German may promise no more than the English.
- **G5:** the German must carry what the Owner's English carries, and no less.

The word counts are executed (**E**). Every variant has 6 words; the English has 5.

| # | German | First fatal gate | One-line reason | Class |
|---|---|---|---|---|
| H1 | Hol dir einen leistungsstärkeren menschlichen Owner. (`82a20cb`) | **G0** | *Owner* in German is jargon. It is the Product-Owner loanword, as the Owner's own update calls it, and an English term of art to a reader outside agile work. The German pages have dropped it since `53d4277` (0 capitalised *Owner* in `docs/de/`, counted) | E |
| H3 | Hol dir einen besseren menschlichen Owner. | **G0** | The same jargon: *Owner* | E |
| H4 | Hol dir einen besseren menschlichen Eigner. | **G5** | A weaker twin. It drops the performance word, and that word makes the joke: the fleet speaks of its human as one speaks of hardware. *besser* judges him; *leistungsstärker* judges his output | I |
| H2 | Hol dir einen leistungsstärkeren menschlichen Eigner. (`53d4277`) | survives | — | K |

**H2, gate by gate, now that it has survived:**

- **G0:**
  - it has 6 words;
  - it speaks *du* to the fleet, as ruled;
  - it is a provocation the owner can take;
  - *Eigner* is plain German for an owner, above all of a ship or a company;
  - it carries no ids.
- **G1 (K):**
  - *Hol dir* with a comparative is the voice of German product advertising.
  - *leistungsstärker* is what one says of a battery or an engine, and that is the joke.
  - The Reviewer graded `index:5` as native (the delta on `53d4277`).
- **G2:** it promises what the English promises, no more.
- **G3:** it judges his output, not his person.
- **G4:** it commands the fleet, and the Eigner reads over its shoulder.
- **G5:**
  - *leistungsstärker* keeps the English's *better-performing*;
  - *Eigner* moves the role into German and into the chart the name draws (the *Schiffseigner*).

**H2's strongest counterfacts:**

- *Eigner* is the rarer, higher word. *Eigentümer* and *Inhaber* are the everyday ones, and some readers will hear the
  yacht club or the business pages before they hear *the one who decides*.
- The tool keeps `owner` in its commands (`--owner`, `[seats] owner`, `next: owner`). The pages bridge the two words
  with *(owner)* beside *Eigner* (`de/setup.md:55, 57`).
- *menschlich* also means *humane* (*ein menschlicher Chef*). Beside the agents, *human* reads first, but not for
  every reader.
- The claim says *du*, and the page says *ihr* to the fleet and *Sie* to the Eigner. That register is ruled, and the
  Reviewer noted it too.

**What the four show:** the two axes part cleanly. *Owner* dies at G0 with either adjective, and *besseren* dies at G5
with *Eigner*.

**The one survivor is the line the Owner had already ruled.** Taste-matching would have produced exactly this result.
Its control is H1: the Owner's own committed wording of `82a20cb`, which died at G0 in writing.

### The control, re-run on the new line

*Get a better-performing human Owner.* / *Hol dir einen leistungsstärkeren menschlichen Eigner.* dies at **G0** in
the owner-facing slot (**E**).

- It commands the fleet (*Get*, *Hol dir*) and talks about the owner, and the ruling says so in those words.
- It is the same finding as the first pass: the headline and the second claim are two forms.

### The second claim, beside the new bar

G0–G3 do not read the bar. G4 reads the fleet's line, which is unchanged in substance (`docs/index.md:7`). G5 reads
the bar. Every one of the twelve lines is in *Sie*, as the ruled owner pages are, and none uses *Owner* or *Eigner*.

| # | First pass | This pass | What moved |
|---|---|---|---|
| C1–C8 | G0–G4 as filed | the same | Citations were re-read at `32e92f8`. C1's *Sie holen* / ***Sie** schreiben* are now `docs/de/index.md:28, 33`. C5's command is `docs/index.md:41`, and `docs/signing.md:15` is unchanged |
| C9 | G5 | **G5** | The bar now tells the fleet to get a better human. C9 tells the human his fleet is at it, so it is the same sentence, turned |
| C10 | survives | **survives** | The counterfact is sharper: beside *better-performing*, *not too slow* reads closer to a retraction. It survives because performance is not speed, and it names a cause the bar does not |
| C11 | survives | **survives** | Nothing moved. The owner block still says *Sie nicken ab* (`docs/de/index.md:10`) |
| C12 | survives | **survives** | The counterfact is rewritten below |

**C12's counterfact, rewritten.** *Who actually checked what you approved?*

- **What the record can answer:** *who* checked. A Reviewer's file names its seat and its session.
- **What it cannot:** whether that check came from another session. The page itself calls that *a report, not a
  proof* (`docs/index.md:23`).
- *eigentlich* / *actually* leans on exactly what git cannot yet show.
- In the one project, 4 of 13 pull requests carried no Reviewer's file at all.
- **The line survives because it asserts nothing.** Its risk is a question the page can answer only in part.

**Survivors, second claim:** C10, C11 and C12, unranked.

### Jev — a third reader, outside this runtime's lineage

On the Owner's direction, this pass also scores the screen through TypeSafe's **Jev**, which reports a Score with a
confidence. The request is `jev-claim-screen-request-2026-09-23.json`, beside this file.

**It was committed before the call was run,** so the rubric cannot have been tuned to the answer. The Owner runs the
call, and this seat has no key.

- **The rubric:** one Score per line. It has seven levels:
  - level 0 means the line dies at G0, and so on to level 5, which means it dies at G5;
  - level 6 means it passes all six gates.

  Jev's most probable level therefore lines up with the ledger's *first fatal gate*. The four H variants carry the
  headline rubric: G0 and G5 adapted as above.
- **The gates are given as the brief wrote them**, with the corrected anchors, and **not in this seat's reading**. If
  Jev reads G2 strictly, C10 is where it will part from the ledger.
- **Jev sees no verdicts.** The questions carry neutral keys in shuffled order, and the mapping is below.
- **Only generic input leaves the machine:** the lines, the gates, the bar, the fleet's line and the four anchors as
  numbers. No tracker's text, and no name: the tool is *the tool*, and the project is *one project*.
- **Kept in the record:** each call's question, answer and confidence. The answer lands in a file beside the request,
  and in a *Jev* column added to this pass.
- **Unproven until run:** whether Jev's confidence is calibrated at all.
  - The control C0 has to come back at level 0.
  - H1 and H3 have to come back at level 0, on the jargon.

  If they do not, the column is read as noise.
- **Jev's own documentation** says non-English input *currently has lower accuracy*
  (`docs.typesafe.ai/concepts/state`). So G1 in German is the gate where its reading is weakest.

**The key mapping,** shuffled by hand so that the keys follow neither the ledger's order nor its verdicts:

| key | line |
|---|---|
| q01 | C11 |
| q02 | H4 |
| q03 | C3 |
| q04 | C9 |
| q05 | C0 |
| q06 | C6 |
| q07 | H2 |
| q08 | C12 |
| q09 | C1 |
| q10 | C7 |
| q11 | H1 |
| q12 | C4 |
| q13 | C10 |
| q14 | C2 |
| q15 | H3 |
| q16 | C8 |
| q17 | C5 |

**The Jev column is pending the call.**

### What this pass did not run

- **No native German reader.** H2's nativeness rests on this runtime and on the Reviewer's grading: another seat's
  reading, not a native speaker's.
- **Other German words were not screened:**
  - *Eigentümer*, *Inhaber*, *Chef*;
  - *stärkeren*, *fähigeren*;
  - a claim without *menschlichen*.
- **The 9 of 13 was not recounted.** It is cited as the page and the Reviewer state it. Its source belongs to another
  project, and this seat did not open it.
- **The English claim was not screened.** It is the bar.
- **As in the first pass:** no outside owner, no web search, nothing rendered, and no independent hostile review.

### Handoff, second pass

- **Conclusion:**
  - **The German claim:** of four variants, H2 survives, the landed line. *Owner* dies at G0, and *besseren* dies at
    G5.
  - **The second claim:** no verdict moved, and C10, C11 and C12 survive, unranked. One anchor is corrected, and
    C12's counterfact is rewritten.
- **Strongest counterfact:** the one headline survivor is the ruled line, the result taste-matching would also give.
  Its control is H1 dying at G0.
- **Unresolved unknown:** does a German owner hear *Eigner* as *the one who decides*, or in a yacht-club register?
- **Closure and reversal:**
  - H2 falls if a native German reader hears *Eigner* as the wrong register for a company's owner, or *menschlichen*
    as *humane*.
  - H1 and H3 revive only if the Owner rules *Owner* no jargon for his readers.
- **Seat shadow:**
  - *Taste-matching:* see above.
  - *The first pass used a number it had not verified:* corrected here, in writing.
- **Authority:** nothing chosen, and the pitch not edited. The Owner rules.

**Provenance:** Seat: GtM · Session `2ab3afad` · Model: Claude Opus 5.5 · 2026-09-23 · the second pass, on the
Owner's convening.
