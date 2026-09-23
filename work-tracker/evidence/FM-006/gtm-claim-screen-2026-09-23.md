# GtM screen — FM-006, the pitch's second claim, facing the owner

- **Date:** 2026-09-23, 22:02–22:10 CEST (`date`)
- **Seat:** GtM (`gtm@seat`), Owner-convened 2026-09-23 22:02 · **Session:** `ee61f1fe` · **Model:** Claude Opus 5.5
- **Base:** `589d328` on `fm/006-the-human-pages-open-from-a-file`. The screen reads the pitch there
  (`docs/index.md`, `docs/de/index.md`).
- **Disclosure:** this runtime wrote the pool **and** screened it. It wore two hats in sequence, and no independent
  check has run on this file. The pool was not written blind to the gates.
- **This seat chooses nothing, ranks nothing and does not edit the pitch.** The Owner rules.

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
