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

### Jev's answer — 2026-09-23, session `2ab3afad`

**The call.** The Owner ran it in TypeSafe's playground.

- **Model:** `jev-1.13.0`; request `playground_1dc13a5396120604295ac49453f6fbbe7fe`.
- **Size and time:** 7,361 tokens in, 259 out, 174 ms.
- **Kept verbatim:** the answer is in `jev-claim-screen-response-2026-09-23.json`, beside the request.
- **Checked here (E):** every answer's legend is the rubric the committed request carried, level for level.

**The controls, set before the call:** C0, H1 and H3 must come back at level 0.

| control | came back at | p(level 0) | confidence |
|---|---|---|---|
| C0, the Owner's line in the owner-facing slot | **level 1** (p 0.35; level 5 at 0.34) | 0.12 | 0 |
| H1, *… leistungsstärkeren … Owner* | level 0 (p 0.44) | 0.44 | 0.09 |
| H3, *… besseren … Owner* | level 0 (p 0.45) | 0.45 | 0.18 |

**C0 failed, so, by the rule written before the call, the column is read as noise. No verdict in this ledger moves.**

**The two controls that passed separate nothing.** H2 (*… leistungsstärkeren … Eigner*), which the ledger passes, came
back at level 0 more surely than either: p 0.59, confidence 0.36. Jev puts every German headline twin at G0 or G1.
Its level 0 for H1 and H3 therefore does not show that it read *Owner* as jargon.

**The Jev column** (E, from the response). *Level* is Jev's most probable level. *Score* is its expected level, 0–6.

| # | Ledger: first fatal gate | Jev: level (p) | p of the ledger's level | Score | Confidence |
|---|---|---|---|---|---|
| C0 · control | G0 | 1 (0.35) | 0.12 | 2.70 | 0 |
| C1 | G1 | 0 (0.38) | 0.07 | 2.47 | 0 |
| C2 | G1 | 6 (0.24) | 0.18 | 3.23 | 0 |
| C3 | G2 | 0 (0.36) | 0.19 | 1.82 | 0 |
| C4 | G2 | 0 / 2 (0.35 each) | 0.35 | 1.51 | 0.12 |
| C5 | G3 | 3 (0.30) | 0.30 | 2.94 | 0.12 |
| C6 | G3 | 3 (0.27) | 0.27 | 2.76 | 0.16 |
| C7 | G4 | 1 (0.22) | 0.17 | 2.90 | 0 |
| C8 | G0 | 0 (0.24) | 0.24 | 2.76 | 0 |
| C9 | G5 | 1 (0.37) | 0.05 | 1.68 | 0.28 |
| C10 | survives (6) | 0 / 4 (0.22 each) | 0.12 | 2.65 | 0 |
| C11 | survives (6) | 3 (0.49) | 0.14 | 3.27 | 0.36 |
| C12 | survives (6) | 3 (0.42) | 0.10 | 2.96 | 0.28 |
| H1 | G0 | 0 (0.44) | 0.44 | 1.56 | 0.09 |
| H2 | survives (6) | 0 (0.59) | 0.06 | 1.09 | 0.36 |
| H3 | G0 | 0 (0.45) | 0.45 | 1.41 | 0.18 |
| H4 | G5 | 1 (0.39) | 0.03 | 1.41 | 0.32 |

**How the answers spread:**

- 7 of 17 answers carry confidence 0, and the highest is 0.36.
- On 6 of 17 lines, Jev's most probable level includes the ledger's; on one of the six it is a tie. Guessing at
  random over seven levels would match about 2.4 lines.
- None of this is claimed as signal: the rule has already read the column as noise.

**The likely cause is this seat's request, not only the model.**

- The rubric packs six gates into one Score. Jev's documentation says the opposite (`docs.typesafe.ai/primitives/score`,
  read 2026-09-23, **E**):
  - *"Keep each question to one dimension"*;
  - for complex judgments, *"split into multiple Score questions … then combine with weights in code"*.
- Its state documentation adds that non-English input *currently has lower accuracy*.
- **The fair test is one yes-or-no question per gate per line:** 6 × 17 = 102 questions in one call. The code then
  computes the first fatal gate, and the same three controls run first. **It has not been run, and running it is the
  Owner's call.**

**What the answer would say, were it read.** None of this is used; it is recorded so that nobody finds it in the raw
file and takes it for news.

- **The most confident answer of the call puts H2, the landed German claim, at G0** (p 0.59, confidence 0.36).
- **The two most confident owner-claim answers put C11 (p 0.49) and C12 (p 0.42) at G3,** the owner's never. That is
  the unknown this ledger already names: provocation, or insult. It goes to the native reader and to the hostile
  review as a question, not as evidence.

**What this seat did not run:**

- Jev's known-issues page for `jev-1.13` (`docs.typesafe.ai/model-jaggedness/jev-1.13`);
- a second call, so whether the same request gives the same numbers is unknown;
- the per-gate design above.

**The guard held.** The request file is the whole of what left the machine: lines, gates, the bar, the fleet's line
and four facts as numbers. It carries no tracker's text and no name.

**The session closes.** The screen is filed: the Jev column is recorded and read as noise by its own rule, the
verdicts stand as the seat ledgered them, and the Owner rules.

---

## The gate test — recorded 2026-09-23 22:42 CEST, before either call; session `c1652143`

**The Owner's direction.**

- One yes-or-no question per gate per line: 17 lines × 6 gates = 102.
- Each gate is its own Score with a one-sentence rubric. G2 (truth) is a Noul.
- The first failed gate is computed in code.
- Three controls come first.
- The identical call runs twice.
- The column counts only if all three controls hold and the repeat agrees within 0.1. Otherwise it is noise, and the
  record says whether it blames the question or the model.
- Both runs are ledgered raw.

**The seventeen lines.**

- **C1–C12** in the owner-facing slot.
- **E0**, the Owner's English line *Get a better-performing human Owner.*, in its own slot, the headline. It is the
  positive control and must pass every gate.
- **H1–H4**, the German twins, in the headline slot.
- **C0 is out:** it was the Owner's line in the owner-facing slot. *Must pass every gate* only makes sense in the
  line's own slot, because in the owner-facing slot the ledger kills it at G0 by the slot's own definition.

**The questions:** 85 two-level Scores (level 0 fails, level 1 passes) and 17 Nouls. The G2 Noul asks the failing
condition directly: *does the line say or promise something the facts do not prove?*

**Jev's known issues for `jev-1.13`**, read before the call (`docs.typesafe.ai/model-jaggedness/jev-1.13`, **E**),
and what the request does about each:

- **#2, it cannot count:** the ≤ 12-word check is done in code, from the keys file. The first request asked Jev to
  count, which may be one more reason that call was noise.
- **#1, literal reading:** each instruction states the exact condition, and the criteria hold the boundaries.
- **#7, irrelevant state:** each question names the state field it reads.
- **#4, Scores serve thresholds only:** every gate passes at p ≥ 0.5.
- **What stays against the page:** G0 and G3 each still bundle several conditions in one question. The page says
  *avoid hiding multiple judgments in one question*, but the Owner's design is one question per gate. **If the record
  blames the question, look there first.**

**Two design choices, said:**

- **Jargon is defined in general terms** (*a term of art … a general reader would not use*), never for a particular
  line. Writing *Owner* into the boundary would make the H1 control circular.
- **E0's G2 and G5 are identities, because E0 is the bar.** They test whether Jev recognises one; G0, G1, G3 and G4
  are E0's real test.

**The decision rule is code:** `jev-gate-test-score.py`, committed with this section and before either call.

- **p_pass:** a Score's probability of level 1, or 1 − noul for G2. A gate passes when p_pass ≥ 0.5.
- **Controls:** E0 survives, H1 dies at G0, and H2 survives, in both runs.
- **Repeat:** all 102 p_pass values agree within 0.10.
- **The blame:**
  - *the model*, when the repeat fails. This wins when both fail, because an unstable answer cannot indict the
    question.
  - *the question*, when the repeat holds and a control fails.

**The scorer was tested on three synthetic answer sets before any real one existed (E).**

| synthetic set | verdict it returned |
|---|---|
| the ledger's own verdicts, with a +0.05 shift between runs | *the column counts* |
| a +0.25 shift between runs | *blames the MODEL* |
| E0 broken in both runs | *blames the QUESTION* |

**The rule's limit:** a stable answer that misses a control cannot tell a badly posed question from a model that
judges otherwise. The Owner's rule calls it the question, and the ledger will say so.

**Files, beside this ledger:**

- `jev-gate-test-build.py` builds the request and the keys.
- `jev-gate-test-request-2026-09-23.json` is the request, identical for both runs.
- `jev-gate-test-keys-2026-09-23.json` holds the key → (line, gate) map, shuffled with seed 20260923, and the word
  counts. It is never sent.
- The answers will land as `jev-gate-test-response-run1-2026-09-23.json` and `…-run2-…`.

### The gate test — both runs, 2026-09-23 22:51 CEST

**The runs.** The Owner ran both in TypeSafe's playground, identical input, one after the other.

| run | request | model | tokens in / out | time |
|---|---|---|---|---|
| 1 | `playground_1dc9fe6fc4e608e44bc98e357345d244217` | `jev-1.13.0` | 15,032 / 1,687 | 813 ms |
| 2 | `playground_1dc7760c638be244e659b0b89dae78cd99a` | `jev-1.13.0` | 15,032 / 1,687 | 440 ms |

- **Kept raw:** `jev-gate-test-response-run1-2026-09-23.json` and `…-run2-…`, as returned.
- **Checked here (E):** every answer's type and legend match the committed request, 102 of 102 in each run.
- **The scorer's output** is `jev-gate-test-score-output-2026-09-23.txt`. The script and the rule are as committed in
  `e6518e8`, before either call.

**The controls failed, in both runs.**

| control | wanted | run 1 | run 2 |
|---|---|---|---|
| E0 · *Get a better-performing human Owner.* | survives | **G1** (p_pass 0.24) | **G1** (0.21) |
| H1 · *… leistungsstärkeren … Owner* | G0 | G1 (G0 at exactly 0.50 passes under the rule; G1 0.13) | G0 (0.42) |
| H2 · *… leistungsstärkeren … Eigner* | survives | **G1** (0.12) | **G1** (0.14) |

**The repeat failed, by one answer.**

- 101 of 102 p_pass values agree within 0.10. The one outside is C2 G4: 0.47 → 0.58, a move of 0.11.
- The mean move is 0.027, and the median 0.02.

**VERDICT, by the rule committed before the call: noise. The record blames the MODEL.** The identical question gave
different numbers, and under the rule an unstable answer cannot indict the question. **No verdict in this ledger
moves.**

**What else the record shows.** The verdict stands as the rule gives it; the rest is here so that it is not taken for
the whole story.

1. **The numbers mostly repeat. The verdicts do not.**
   - 10 of the 102 answers sit on opposite sides of 0.5 in the two runs.
   - The first fatal gate changes on 5 of 17 lines: C3, C4, C8, C10 and H1.
   - Four of those five flip at **G0**, the gate that bundles four conditions and was named before the call as the
     first place to look.
   - The 0.10 tolerance is wider than the margin these answers have from 0.5.
2. **The controls fail the same way in both runs, and in the same place.** Every headline line fails G1, the Owner's
   English line included, at p_pass 0.12–0.24 in both runs. **On its own, that pattern would blame the question.**
   - A likely cause, **inferred and not tested**: the state calls the German lines the English line's *twins*. That
     tells a model the lines are translations, and then asks it whether a native reader hears a translation.
3. **Jev agrees with the ledger on 1 of 17 lines in run 1, and 2 of 17 in run 2.**

**What the record blames, then:**

- **Under the rule, the model:** the repeat failed.
- **The stable part of the answer also carries the question's fingerprint:** the controls fail at the headline's G1
  in both runs, and the unstable part sits at the bundled G0.

The record does not separate the two further. Separating them would take a third call with the headline's G1
stripped of *twins* and G0 split into four. **That is not run, and it is the Owner's call.**

**Not run:** a third call; the revised question above; any line or gate the ledger does not carry.

**The session closes.** Both runs are ledgered raw, the rule's verdict is noise, the screen's verdicts stand as the
seat ledgered them, and the Owner rules.

**Provenance:** Seat: GtM · Session `c1652143` · Model: Claude Opus 5.5 · 2026-09-23 · the Jev gate test, on the
Owner's direction.

---

## Third pass — the German claim, re-provoked — 2026-09-23 22:57 CEST, session `ad81b142`

**The Owner's direction, relayed with Jev dropped:**

- **The critique.** The German claim reads weak because it is a translation: it mirrors the English word order,
  stacks two adjectives before the noun, and *leistungsstark* is performance-review German.
- **The ask:** re-provoke in German instead of translating. Use short words, one adjective at most, an imperative or
  a stark noun phrase, and idiom a person would say aloud. The human-versus-agent contrast may come from the verb or
  the setting, not from *menschlich*.
- **What stays:** *Eigner* and the bar, the English line.
- **The new test:** read every line aloud. If it sounds like a job ad or a LinkedIn post, it dies at G0.
- **Twelve new German lines, no translations, controls first, ledgered as before. The Owner chooses.**

**The page as built** (`site/index.html` and `site/de/index.html`, 22:49, read as text, **E**):

- The claim is *Get a better-performing human Owner.* / *Hol dir einen leistungsstärkeren menschlichen Eigner.*
- The German fleet block says *ihr*; the claim says *du*.
- The German page carries the English meta description.

### Correction to the second pass

**The second pass passed *Hol dir einen leistungsstärkeren menschlichen Eigner.* at G1 on this runtime's knowledge,
and it should not have.** The line mirrors the English slot for slot (**F**):

| *Hol dir* | *einen* | *leistungsstärkeren* | *menschlichen* | *Eigner* |
|---|---|---|---|---|
| *Get* | *a* | *better-performing* | *human* | *Owner* |

**Method lesson, carried with its corpse:** before a German twin is called native, lay it word for word against its
source. A mirror is a translation, however idiomatic its parts.

### The gates for this pass

| Gate | Kills on |
|---|---|
| **G0** form | any of these: more than one line; more than 12 words (counted in code); does not command the fleet in *du* and is not a stark noun phrase the fleet reads; not a provocation the owner can take; does not name the owner *Eigner*; **more than one adjective**; jargon or ids; **read aloud, it sounds like a job ad or a LinkedIn post** |
| **G1** language | a German reader hears a translation (the English word order mirrored) · an idiom slip · nothing a person would say aloud |
| **G2** truth | it promises more than the bar |
| **G3** the Owner's never | it degrades him to a push-a-button, promotes rubber-stamping, flatters him into pressing, or insults him |
| **G4** both ways | it does not both put the fleet in the act and provoke the owner, or, read beside the fleet's line (`docs/index.md:7`), the act runs against it |
| **G5** the bar | it does not carry what the English bar says (the fleet gets a better-performing human), or it says it more weakly. A re-provocation, not a translation |

**"Read aloud" is this runtime's judgment of register (K),** and no voice read any line. Adverbs do not count as
adjectives. The word counts are executed (**E**), and every line names the *Eigner*.

### The controls

| # | Line | First fatal gate | One-line reason | Class |
|---|---|---|---|---|
| **K1** · positive | *Get a better-performing human Owner.* (the bar, English) | survives G0, G1, G3 and G4 in its own language; G2 and G5 are identities | Read aloud, it is a product ad whose product is a human, and that is the provocation. It is not a job ad or a post | I |
| **K2** · negative | *Hol dir einen leistungsstärkeren menschlichen Eigner.* (on the page) | **G0** | It has two adjectives before the noun (**F**), and read aloud *leistungsstärker* is performance-review German (**K**). The new clauses fire on the line the second pass passed | F |

**What the controls show:**

- The new G0 clauses kill the German line on the page.
- They do not kill the English bar, which carries the same performance word. It carries it as an ad imperative about
  a human; in German, the same word became the whole line.

### The ledger — twelve new German lines

The glosses are there for the reader. **They are not twins, and nothing here is translated.**

| # | German | Gloss | First fatal gate | One-line reason | Class |
|---|---|---|---|---|---|
| N1 | Dein Eigner kann mehr. | Your owner can do more. | **G0** | Read aloud, it is the job-ad and coaching formula (*Du kannst mehr*, *Da geht mehr*) | K |
| N2 | Hol das Beste aus deinem Eigner heraus. | Bring out the best in your owner. | **G0** | Read aloud, it is leadership-seminar German (*das Beste aus Ihren Mitarbeitern herausholen*) | K |
| N3 | Mach deinen Eigner scharf. | Make your owner sharp. | **G1** | Idiom slip. *Jemanden scharf machen* means to arouse him, or to set a dog on attack | K |
| N4 | Erzieh deinen Eigner. | Raise your owner. | **G3** | Insult. *Erziehen* is what one does to a child or a dog | I |
| N5 | Schleif deinen Eigner. | Hone your owner. | **G3** | With a person as its object, *schleifen* means to drill him hard (*Rekruten schleifen*). The knife loses to the barracks | K |
| N6 | Dein Eigner ist lahm. Mach ihm Beine. | Your owner is slow. Get him moving. | **G3** | *Beine machen* hurries him, and an owner hurried presses sooner: rubber-stamping. *Lahm* insults him besides | I |
| N7 | Weck deinen Eigner. | Wake your owner. | **G4** | The act runs against the fleet's line. Waking him is interrupting him mid-flight, and the line says *once a day* (`docs/index.md:7`) | E |
| N8 | Frag deinen Eigner seltener. Dafür richtig. | Ask your owner less often. But properly. | **G5** | It is the fleet's line in brief, the how. It does not carry the bar's claim | I |
| N9 | Mach deinen Eigner besser. | Make your owner better. | **G5** | Plain *besser* drops the performance the bar's joke rests on. It is the same death as the second pass's *besseren* (H4) | I |
| N10 | Hol mehr aus deinem Eigner raus. | Get more out of your owner. | survives | — | I |
| N11 | Dein Eigner bremst. Tunen statt tauschen. | Your owner is the brake. Tune him, don't swap him. | survives | — | I |
| N12 | Bring deinem Eigner das Entscheiden bei. | Teach your owner to decide. | survives | — | I |

**What each gate killed:**

| Gate | Lines killed |
|---|---|
| G0 | 2, and K2 |
| G1 | 1 |
| G2 | 0 |
| G3 | 3 |
| G4 | 1 |
| G5 | 2 |

**Three survive.**

- **G2 killed nothing:** none of the twelve promises more than the bar.
- **This seat's favourite, N5 *Schleif deinen Eigner*, the knife the critique asked for, died in writing at G3.**

### The survivors — three, unranked, in the order they were written

#### N10 · *Hol mehr aus deinem Eigner raus.*

- **What it carries:** the bar's irony, in German a person says aloud. The fleet speaks of its human as one speaks of
  an engine: *mehr rausholen*. The performance comes as *mehr*, not as an HR word, and the human-versus-agent
  contrast comes from the setting.
- **Strongest counterfacts:**
  - *Hol mehr aus deinem … raus* is also the electronics-flyer formula, and some readers will hear a phone ad.
  - *Das Letzte aus jemandem rausholen* sits one word away. That is squeezing, not tuning.
  - *raus* is spoken register on a pitch page.

#### N11 · *Dein Eigner bremst. Tunen statt tauschen.*

- **What it carries:** the bar, plus what the bar leaves open. *Get a better … Owner* can be read as *replace him*;
  this line says tune him, don't swap him.
- **German:** *X statt Y* is the native slogan form (*Reparieren statt wegwerfen*). *Bremsen*, said of a person,
  means holding things back.
- **Strongest counterfacts:**
  - *tauschen* puts replacing him on the table, in a line he reads over the fleet's shoulder. To some owners it is a
    threat.
  - *tunen* is the car-tuning scene, and a *Mittelstand* owner may hear the scene before the engineering.
  - The second sentence has no verb. It is a slogan, which is what it is meant to be.

#### N12 · *Bring deinem Eigner das Entscheiden bei.*

- **What it carries:** the inversion. The fleet teaches the human, on the pattern of *jemandem das Schwimmen
  beibringen*. It also names the performance the bar leaves open: deciding.
- **Strongest counterfacts:**
  - *beibringen* is what one does for children. G3 (insult) is where it can die with an owner reading it.
  - It loses the machine irony of the bar.
  - *das Entscheiden* as a noun is one step from office German.

### What this pass did not run

- **No native German reader, and no voice.** Both G0's read-aloud test and G1 are this runtime's knowledge. Its own
  G1 was wrong one pass ago.
- **No outside owner** has read a survivor.
- **No search for prior use.** *Tunen statt tauschen*, above all, may already be a workshop's slogan.
- **No stark noun phrase survived, and only three were written** (N1, and the openings of N6 and N11). That form is
  under-sampled.
- **No Jev,** on the Owner's word.

### Handoff, third pass

- **Conclusion:** the controls behaved as intended. The bar survives, and the German line on the page dies at G0.
  Three new German lines survive, unranked: N10, N11 and N12.
- **Strongest counterfact:** this runtime called the page's German native one pass ago, and the critique showed it
  to be a mirror. Its read-aloud judgment on these twelve is the same kind of knowledge.
- **Unresolved unknown:** which of the three a German owner says aloud without wincing.
- **Closure and reversal:** a survivor falls when:
  - a native reader hears it as a flyer (N10), a threat (N11) or a lesson for a child (N12);
  - a search finds it in use.
- **Authority:** this seat has not chosen, and has not edited the pitch. **The Owner chooses.**

**Provenance:** Seat: GtM · Session `ad81b142` · Model: Claude Opus 5.5 · 2026-09-23 · the third pass, on the Owner's
direction.

---

## The reader, stated — 2026-09-23 22:59 CEST, session `d578f49e`

**The Owner, quoted with his spelling normalised:** *"I have to pitch this and it must stick. German audience but
English-fluent. Tech investor and well educated, so make this one count, no BS."*

- **Until now,** every pass read the claim as the repository's owner and his fleet would read it.
- **This addendum re-reads the survivors for the reader the Owner named.** It changes no verdict above, and it ranks
  nothing.

### What this reader changes

1. **The German line has to beat the English, not just carry it.** A reader fluent in both hears a German line that
   is weaker than the English as a translation. That costs the German page more than having no German line at all.
2. **So the null candidate is live: the English bar on the German page too.**
   - It passes G1 by construction, because nothing is translated.
   - It costs FM-006's rule that German is *a full second language from the first page*, a rule written for the
     first two outside owners, not for an investor.
   - **That conflict is the Owner's to rule, not this seat's.**

### The survivors, read by this reader

| # | Line | What this reader hears | Class |
|---|---|---|---|
| N10 | *Hol mehr aus deinem Eigner raus.* | The consumer-flyer formula. It says *get more out of the human*, and not why that is a business | I |
| N11 | *Dein Eigner bremst. Tunen statt tauschen.* | To a tech reader, *tunen* is performance tuning, and fine-tuning, before it is the car scene; the third pass's counterfact weighs less here. The line also meets this reader's first question, *why not replace the human with more autonomy?*, with a thesis: keep him, tune him. **Held to "no BS":** what the tool tunes is his intake (once a day, one sentence per question, one command per answer), and the page proves that | I |
| N12 | *Bring deinem Eigner das Entscheiden bei.* | A clever inversion that states a mechanism the tool does not have. Nothing in the tool teaches anyone to decide; it batches and phrases the questions. **Read for this reader, it dies at G2:** an investor asks *how does it teach?*, and the page has no answer | I |

**Survivors for this reader: N10 and N11, unranked, and the null candidate beside them.**

### "No BS": what this reader will probe on the page, beyond the claim

This is flagged here, not edited; the pitch is not this seat's to edit.

- ***Measured, not promised* rests on one project,** the author's own, over *just over a day*, with 9 of 13 (`docs/index.md:13–18`).
  - An educated investor reads n = 13 in one day, in the founder's own repository, as an anecdote.
  - A heading that says *measured* over an anecdote is the overclaim this reader looks for first.
  - **What would hold:** saying it at its size (*one project, our own, 9 of 13 in the first day*), or waiting for the
    week's count.
- **The *before* is a confession:** the author's own last 200 pull requests were merged unread. That is honest, and
  it may be the strongest line on the page for this reader, *if* it is presented as the founder's own problem.
- **One page, three registers.** The German page says *du* in the claim, *ihr* to the fleet and *Sie* to the Eigner.
  An educated reader notices; it was ruled, and it is noted again only because this reader is new.

### Not run

- No investor has read anything.
- No German native has read anything either.
- No search for prior use of *Tunen statt tauschen*.

**The Owner chooses.**

**Provenance:** Seat: GtM · Session `d578f49e` · Model: Claude Opus 5.5 · 2026-09-23 · an addendum, on the Owner's
statement of the reader.

---

## Both readers, per line, and what would be data — 2026-09-23 23:06 CEST, session `63f5b126`

**The Owner's ruling** (`a3eb298`, FM-006): the pitch has **two readers**.

- An outside Owner of a fleet: the first two are German, one on Windows and Subversion.
- A German tech investor fluent in English, *"indeed one of my audiences I am in contact with"*.

Every gate is read for both, and where they pull apart, the page says which reader a line is for.

**The Owner, to this seat, the same hour** (spelling normalised): *"Must impress, must resonate with the audience. The
claim from the agent perspective I personally liked, but OK, you're the GtM: you must know better than me and have
data to prove it."*

**What this seat answers, in writing:**

- **It has no data that proves resonance, and it does not know the audience better than the Owner,** who is in
  contact with it.
- **Every verdict in this ledger is a filter.** It kills lines for stated reasons, most of them this runtime's
  knowledge or inference. The only executed evidence is word counts, the mirror check and reads of the record. Jev
  came back as noise by its own rule.
- **No reader of either kind has read a line.** A survivor is *not dead*; that is not the same as *resonates*.
- **Nothing here overruled the agent perspective:**
  - the English bar, in the fleet's voice, survives every pass;
  - every German survivor speaks to the fleet (*dein Eigner*);
  - what died was a translation.
- **A correction to the Principal's ship-log row in `a3eb298`, for the Reviewer:** it says the two survivors stand
  *"with G3 unrun"*.
  - G3 was run on both, as this runtime's inference (I), and both passed.
  - What is unrun is any reader.
  - Whether *bremst* is a provocation he can take is the Owner's to say, because he is the one it provokes.

### Per line, per reader

| Line | Outside Owner | German tech investor | The line is for |
|---|---|---|---|
| *Get a better-performing human Owner.* (the bar) | survives | survives | both |
| The bar, in English, on the German page too | **pulls apart:** it breaks FM-006's German-first rule, written for these readers | survives: a fluent reader hears no translation | the investor |
| N10 · *Hol mehr aus deinem Eigner raus.* | survives | survives. Counterfact: the consumer-flyer register | both |
| N11 · *Dein Eigner bremst. Tunen statt tauschen.* | survives. Counterfacts: *tauschen* heard as a threat; *tunen* heard as the car scene | survives: *tunen* reads as performance tuning, and it answers *why not replace the human?* | both |
| N12 · *Bring deinem Eigner das Entscheiden bei.* | survives: he hears it as rhetoric. Counterfact: condescension | **dies at G2:** he hears it as a product claim, and the tool teaches no one | the owner |

**The split is honest, but arguable.** G2 asks what a line *says*, and the same words say rhetoric to one reader and
a mechanism to the other. A Reviewer may hold that truth is reader-independent. If so, N12 dies for both.

### What would be data

The only evidence that a line *sticks* is a reader of the kind named remembering it. **This seat can write the
protocol; it cannot run it.** A proposal:

- **Who:**
  - the investor or investors the Owner is in contact with;
  - two or three German native readers, at least one an outside Owner.
- **What:** the top of the page (the name, the tagline, one claim), shown for five seconds, with no explanation. One
  claim per reader, rotated.
- **What is measured, next day:**
  - *"What did it say?"*: gist recall is *sticks*.
  - *"Would you repeat it to someone?"*: yes is *resonates*.
  - *"Did anything grate?"*: an insult or a translation heard.
- **The rule, fixed before anyone is shown anything:**
  - a line no reader recalls in gist dies;
  - a line one reader hears as an insult dies at G3;
  - a line a native reader hears as a translation dies at G1.
- **Its size:** three to five readers kill lines; they do not prove one. That limit is said in advance. The Data
  Scientist seat can set the numbers if the Owner wants more than a kill test.

**The Owner chooses.**

**Provenance:** Seat: GtM · Session `63f5b126` · Model: Claude Opus 5.5 · 2026-09-23 · on the Owner's two-readers
ruling and his question to the seat.

---

## Corrections — 2026-09-23 23:50 CEST, session `e0be0fa0`

These are appended on the Owner's words, 23:20, relayed: *"shoalmark is the 'reset' that sets the record straight."*
The diagnosis rests on nine months of record in the author's own project: about 10,000 contributions in a year, 200
merges unread in 22 days, and one incident. Only the remedy's measurement is 28 hours old.

1. **"Anecdote" is withdrawn** (the reader addendum, 22:59).
   - The project is not an anecdote; the remedy's count is young.
   - The *Measured, not promised* paragraph should read: the record before, the reset, the record since.
2. **The investor is never a test reader** (the reader-test protocol, 23:06). *"The investor or investors the Owner
   is in contact with"* is struck. The protocol uses **proxies only**: readers like the investor who are not the
   investor.

Both corrections are repeated where they bear on new work: `gtm-mark-screen-2026-09-23.md`, Part 1.
