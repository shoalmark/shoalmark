---
id: FM-160
status: Proposed
considered: FM-024, FM-123, FM-139, FM-156
tags: process
epic: FM-139
next: build
hook: "The coordinator, the Owner's lead seat, has no icon: SEAT_ICONS holds the seven, so a coordinator session's row keeps an empty slot and its avatar has no picture. The imagery round of 13 November names it the radio operator, with an icon brief for a two-way headset, and variant B, the sea bag, stays unassigned. The Designer draws it, and FM-160-Q2 is put on the rendered preview."
---

# FM-160 — the coordinator seat has no icon, so its session row keeps an empty slot

Seat: the Planner (27f31560) · filed 2026-11-12, on the Auditor's word of that day.

## What is true now

**2026-11-13 — decided from the imagery round, on the Auditor's word.** FM-160-Q1 is withdrawn with no answer given.
The go-to-market round of 13 November ([its record](evidence/FM-160/go-to-market-round-imagery-and-the-owners-act-2026-11-13.md)) failed *the tender* at the legibility gate, read cold as an
offer, and passed *the radio operator*. So:

- **the epithet is *the radio operator*:** ashore, it sends and receives the word between the fleet's vessels; it
  informs and advises, and instructs none of them;
- **the icon follows the record's icon brief:** a two-way headset, the boom inside the head's outline, with the brief's
  must-nots and its tell-apart checks at 20 px. The Designer draws it;
- **variant B, the sea bag, stays unassigned,** as the record has it. The items of 12 November below say what was drawn
  then;
- **the imagery round's option 2 joins this lane:** the two settings, at sea and in the yard, named where the seats
  show (decision 4);
- **the skipper stays;**
- **no ask is put until the Designer's render exists:** FM-160-Q2 is put on the rendered preview, as the Designer's
  row requires.

**2026-11-12 — filed, Proposed, with FM-160-Q1; nothing is built.** Its epithet and variant B are superseded by the
block above. Read at main `ec8479c`:

1. **The seat.** `coordinator`, the Owner's lead seat, epithet *the tender*: a tender serves a fleet at anchor, carrying
   people, stores and word between the ships and the shore, and commands none of them. Its pull request adds it to
   `[seats]`; it is not merged yet.
2. **No icon.** `SEAT_ICONS` holds the seven, and "any other word keeps an empty slot"
   ([`shoalmark.py` L4903–L4976](https://github.com/shoalmark/shoalmark/blob/ec8479c68ffceb8afb545a3a745c58b310781b63/shoalmark.py#L4903-L4976);
   the design guide, [§4, L118](https://github.com/shoalmark/shoalmark/blob/ec8479c68ffceb8afb545a3a745c58b310781b63/brand/design-guide.md#L118)).
   So a coordinator session's row keeps an empty slot, and the seat has no avatar.
3. **The drawing.** The Designer drew it on `ec8479c` in the family's rule
   ([`brand/seats/README.md`](https://github.com/shoalmark/shoalmark/blob/ec8479c68ffceb8afb545a3a745c58b310781b63/brand/seats/README.md)),
   in three rounds. Round 1 slung a sea bag behind the head; at 20 px, in grey, it was the weakest of the eight. Round 2
   made two more variants, and the icon goes ahead on **variant B**:
   - a bag in the owl's grey (`#8595a2`) beside a bare head of the land's buff, tied at the neck with one light lashing,
     and never touching the head;
   - nothing in it reads as command or rank: no cap, badge or wheel; the skipper's cap stays the planner's.
4. **B as drawn,** 11 lines, 750 bytes, sha256 `97e3ce61fbba286acd21c431f340bd76b38a178703e1b45f20ccef0c1eda28f9`:

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" shape-rendering="crispEdges">
<title>coordinator — the tender</title>
<rect width="20" height="20" fill="#15293d"/>
<path fill="#34546c" d="M4 17h3v1h-3ZM13 17h3v1h-3Z"/><!-- the water -->
<path fill="#bccd8f" d="M9 14h2v6h-2Z"/><!-- the stake -->
<path fill="#8595a2" d="M7 4h2v1h-2ZM5 6h4v1h-4ZM4 7h5v1h-5ZM3 8h5v5h-5ZM4 13h4v2h-4ZM5 15h2v1h-2Z"/><!-- the sea bag -->
<path fill="#d9e4ec" d="M6 5h2v1h-2Z"/><!-- its lashing -->
<path fill="#e8d4a0" d="M10 7h5v1h-5ZM9 8h7v5h-7ZM9 13h6v1h-6Z"/><!-- the head, the land's buff -->
<path fill="#15293d" d="M10 9h1v2h-1ZM13 9h1v2h-1Z"/><!-- the eyes, on what it carries -->
<path fill="#f38a80" d="M14 11h1v1h-1Z"/><!-- the blush -->
</svg>
```

5. **What the Designer measured:**
   - `export.py`'s rule check, with all eight: exit 0, 24 PNGs; the farthest drawn cell is 7.81 of the safe circle's 8;
     11 lines of 40; no colour outside the seven's;
   - at 20 px, grey, without the ground: 6.1:1 against the dark board and 4.8:1 against the light, the clearest of the
     three variants;
   - told from the herald (go-to-market), its mirror, flipped beside it: by tone, in the opposite order; by height,
     12 rows against the horn's 5; and by never touching the head;
   - what it gives up at 200 px: round 1's slung pose and the sea's blue.

## Why

A seat with no icon shows an empty slot in each of its session rows, and has no picture as an avatar. The coordinator's
icon has to carry its job, *sends and receives between the vessels*, and claim no command, beside a planner whose cap is the skipper's.

## Decisions, for the Owner

1. **The epithet is *the radio operator*.** The record draws the line where a traffic service's INSTRUCTION binds;
   information, warnings and advice leave the decision with the ship. The coordinator sits on the informing side: it
   informs and advises, and instructs none of them, and its words never say *control*.
2. **The icon follows the record's icon brief:**
   - a head, two eyes, a blush, and a **two-way headset**: a band over the crown, an ear cup on each side, and a short
     boom microphone from one ear cup to the mouth, inside the head's outline;
   - the family's rule unchanged ([`brand/seats/README.md`](https://github.com/shoalmark/shoalmark/blob/22ccfc83baea11cc78ae044f0f072abdb40ca136/brand/seats/README.md) and the design guide, §4);
   - *ashore* said in words, not drawn;
   - **never:** a cap, badge, peak or wheel; anything held out from the head; the sea bag; flags; a hand-held marine
     set; a tower, mast or screen that reads as traffic control;
   - **told apart at 20 px, in grey, without the ground:** from the skipper's cap, the owl's ear tufts and spectacles,
     the herald's horn, and the reviewer's monocle and cord;
   - `brand/seats/coordinator.svg` is the drawing FM-160-Q2 takes, byte for byte.
3. **The README row,** the record's proposed words. The third column is the Designer's judgment, from the render:

| Seat | Its character, and why it fits the job | At 20 px, grey included — the Designer's judgment |
|---|---|---|
| coordinator | the radio operator: a two-way headset, the microphone at its mouth. Ashore, it sends and receives the word between the fleet's vessels; it informs and advises, and instructs none of them | the Designer's, from the render |

   It goes after the auditor's row, and the preview's row says the same.
4. **The imagery round's option 2 joins this lane:**
   - the README's family line ([`brand/seats/README.md` L3](https://github.com/shoalmark/shoalmark/blob/22ccfc83baea11cc78ae044f0f072abdb40ca136/brand/seats/README.md#L3)) names the two settings:
     at sea, and in the yard, where its own crew repairs and refits the ship;
   - the builder's row, in the README ([L12](https://github.com/shoalmark/shoalmark/blob/22ccfc83baea11cc78ae044f0f072abdb40ca136/brand/seats/README.md#L12)) and in the preview
     ([`preview.html` L71](https://github.com/shoalmark/shoalmark/blob/22ccfc83baea11cc78ae044f0f072abdb40ca136/brand/seats/preview.html#L71)), reads as the crew's refit rather than new-building, where
     it says "as a yard builds the fleet" today;
   - the landing's fleet section gains one line naming both settings
     ([`overrides/partials/landing/en.html` L72–L73](https://github.com/shoalmark/shoalmark/blob/22ccfc83baea11cc78ae044f0f072abdb40ca136/overrides/partials/landing/en.html#L72-L73)), in English now;
     the German line follows a native read;
   - the Designer proposes the words, and the Owner rules them with FM-160-Q2;
   - the skipper stays: the planner's row and icon do not change.
5. **The other words an eighth seat touches,** as the Designer proposes:

   - **counts that become eight:** [`brand/seats/README.md`](https://github.com/shoalmark/shoalmark/blob/ec8479c68ffceb8afb545a3a745c58b310781b63/brand/seats/README.md) lines 3, 16 and 29;
     [`brand/seats/preview.html`](https://github.com/shoalmark/shoalmark/blob/ec8479c68ffceb8afb545a3a745c58b310781b63/brand/seats/preview.html) lines 7, 56, 60 and 83, with the coordinator's image in
     the three strips (lines 57–59) and its row before `</tbody>`; the comments at `shoalmark.py`
     [L4195](https://github.com/shoalmark/shoalmark/blob/ec8479c68ffceb8afb545a3a745c58b310781b63/shoalmark.py#L4195) and [L4903](https://github.com/shoalmark/shoalmark/blob/ec8479c68ffceb8afb545a3a745c58b310781b63/shoalmark.py#L4903);
   - **a judgment that still holds of eight:** the reviewer's "the clearest of the seven" (README line 13) becomes "the
     clearest of the eight". In the row page with all eight, the monocle is still the one closed light ring;
   - **a measured claim:** README line 22 says the 21 PNGs match the browser's rendering. That was measured for the
     seven alone, so the line says so until the coordinator's three are compared too;
   - **the approval line:** the preview's footer (line 89) says the family is the one the Owner approved on 2026-09-30.
     It is to say that the seven are, and the eighth stands on the answer to FM-160-Q2;
   - **the design guide,** which changes only by a signed answer: §4's "seven hand-drawn icons" and "a seat outside the
     seven" ([L110](https://github.com/shoalmark/shoalmark/blob/ec8479c68ffceb8afb545a3a745c58b310781b63/brand/design-guide.md#L110), [L118](https://github.com/shoalmark/shoalmark/blob/ec8479c68ffceb8afb545a3a745c58b310781b63/brand/design-guide.md#L118)) become eight;
   - **ids:** the lines that carry FM-024 keep it, and no line gains an id;
   - **not this lane:** the seats page's "seven development seats" counts seats, not icons, so it moves with the seat's
     pull request.

   The Designer weighed dropping the count in L118 and L4195, so that a ninth seat would not touch them, and proposes
   the plain count, which keeps each line's meaning.

6. **The lane:**
   - `brand/seats/coordinator.svg` lands from the Designer's hashed copy, byte for byte, as FM-160-Q2 takes it;
   - `SEAT_ICONS` gets its entry, the file but for the ground square, as the seven's. Its comment's "The seven seat
     icons" becomes eight, and the row rule's "a word outside the seven"
     ([L4195](https://github.com/shoalmark/shoalmark/blob/ec8479c68ffceb8afb545a3a745c58b310781b63/shoalmark.py#L4195)) matches;
   - `preview.html` and `export.py` say eight, and the preview's designer line "these seven" becomes eight;
   - the README row, and the pins that count or pin seven: `_SEAT_PINS`, which gains its sha256, `_SEAT_WORDS`, which
     gains an eighth session, and the checks and messages beside them in `test_shoalmark.py`
     ([L8114](https://github.com/shoalmark/shoalmark/blob/ec8479c68ffceb8afb545a3a745c58b310781b63/test_shoalmark.py#L8114)),
     and `SEAT_ICON_EDITS` in `test_git_entry_differential.py`, whose pinned CSS text changes with L4195
     ([L1486](https://github.com/shoalmark/shoalmark/blob/ec8479c68ffceb8afb545a3a745c58b310781b63/test_git_entry_differential.py#L1486));
   - option 2's lines (decision 4);
   - a rendered-surface lane: the Designer's check of the page beside its review.
7. **Order:** it is built only after the coordinator seat's pull request merges and FM-160-Q2 is answered.
8. **Allocation:** v0.20.3, a chapter of FM-139.

## Done when

Each item names its commit or pull request when it lands.

- [ ] **The Designer's render exists,** on the record's icon brief and option 2's lines, and FM-160-Q2 is put on the
  rendered preview.
- [ ] **The Owner has answered FM-160-Q2.**
- [ ] **`brand/seats/coordinator.svg` is the drawing FM-160-Q2 takes, byte for byte,** and `export.py` exits 0 for all
  eight.
- [ ] **A coordinator session's row shows its icon,** 20 px, grey, without the ground, and the seven's rows are
  unchanged.
- [ ] **The README row stands in the Owner's words,** and every "seven" the eighth seat touches reads as decision 3
  sets out.
- [ ] **Option 2's lines stand** in the README, the preview and the landing, in English; the German landing line after a
  native read.
- [ ] **The pins hold the eight,** and a page whose coordinator icon differs fails them.
- [ ] **The Designer's check and the review are READY.**

## Asks

**FM-160-Q1** · 2026-11-13 · Do you take variant B as the coordinator's icon, as drawn, with the README row and the other words FM-160 proposes, and the lane in v0.20.3?
**withdrawn** — no answer was given

## Ship log

| Date | Event |
|---|---|
| 2026-11-13 | Decided from the imagery round, on the Auditor's word: FM-160-Q1 withdrawn with no answer given; the epithet is the radio operator, the icon follows the round's icon brief, variant B stays unassigned, and the round's option 2 joins this lane. FM-160-Q2 waits for the Designer's render. Records only. |
| 2026-11-12 | Filed, Proposed, with FM-160-Q1, on the Auditor's word: `epic: FM-139`, under v0.20.3's epic until the Owner decides whether it goes in. Nothing is built. |
