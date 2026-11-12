---
id: FM-160
status: Proposed
considered: FM-024, FM-123, FM-139, FM-156
tags: process
epic: FM-139
next: owner
hook: "The coordinator, the Owner's lead seat, has no icon: SEAT_ICONS holds the seven, so a coordinator session's row keeps an empty slot and its avatar has no picture. The Designer drew one in three rounds, and the icon goes ahead on variant B."
ask-id: FM-160-Q1
ask: "Do you take variant B as the coordinator's icon, as drawn, with the README row and the other words FM-160 proposes, and the lane in v0.20.3?"
ask-kind: ruling
ask-since: 2026-11-12
ask-options: "yes, B and the words as proposed | yes, B, with my words for the row | not B: another round of drawing | no icon for the coordinator"
ask-proposal: "yes, B and the words as proposed"
---

# FM-160 — the coordinator seat has no icon, so its session row keeps an empty slot

Seat: the Planner (27f31560) · filed 2026-11-12, on the Auditor's word of that day.

## What is true now

**2026-11-12 — filed, Proposed, with FM-160-Q1; nothing is built.** Read at main `ec8479c`:

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
icon has to carry its job, *carries between*, and claim no command, beside a planner whose cap is the skipper's.

## Decisions, for the Owner

1. **The icon is variant B, as drawn:** `brand/seats/coordinator.svg` is the file above, byte for byte.
2. **The README row,** the Designer's proposal. The Owner rules the words:

| Seat | Its character, and why it fits the job | At 20 px, grey included — the Designer's judgment |
|---|---|---|
| coordinator | the tender: a sea bag at its side, lashed at the neck, eyes on the load — it carries people, stores and word between the ships and the shore, and commands none of them | the tall bag at the left, a gap from the head: clear; in grey the bag is darker than its head, where the herald's horn is lighter |

   It goes after the auditor's row. The preview's row says the same: its job line *coordinates, prepares and files*, and
   "A grey sea bag at its side, lashed at the neck in white, and eyes on the load: it carries people, stores and word
   between the ships and the shore, and commands none of them."

3. **The other words an eighth seat touches,** as the Designer proposes:

   - **counts that become eight:** [`brand/seats/README.md`](https://github.com/shoalmark/shoalmark/blob/ec8479c68ffceb8afb545a3a745c58b310781b63/brand/seats/README.md) lines 3, 16 and 29;
     [`brand/seats/preview.html`](https://github.com/shoalmark/shoalmark/blob/ec8479c68ffceb8afb545a3a745c58b310781b63/brand/seats/preview.html) lines 7, 56, 60 and 83, with the coordinator's image in
     the three strips (lines 57–59) and its row before `</tbody>`; the comments at `shoalmark.py`
     [L4195](https://github.com/shoalmark/shoalmark/blob/ec8479c68ffceb8afb545a3a745c58b310781b63/shoalmark.py#L4195) and [L4903](https://github.com/shoalmark/shoalmark/blob/ec8479c68ffceb8afb545a3a745c58b310781b63/shoalmark.py#L4903);
   - **a judgment that still holds of eight:** the reviewer's "the clearest of the seven" (README line 13) becomes "the
     clearest of the eight". In the row page with all eight, the monocle is still the one closed light ring;
   - **a measured claim:** README line 22 says the 21 PNGs match the browser's rendering. That was measured for the
     seven alone, so the line says so until the coordinator's three are compared too;
   - **the approval line:** the preview's footer (line 89) says the family is the one the Owner approved on 2026-09-30.
     It is to say that the seven are, and the eighth stands on the answer to FM-160-Q1;
   - **the design guide,** which changes only by a signed answer: §4's "seven hand-drawn icons" and "a seat outside the
     seven" ([L110](https://github.com/shoalmark/shoalmark/blob/ec8479c68ffceb8afb545a3a745c58b310781b63/brand/design-guide.md#L110), [L118](https://github.com/shoalmark/shoalmark/blob/ec8479c68ffceb8afb545a3a745c58b310781b63/brand/design-guide.md#L118)) become eight;
   - **ids:** the lines that carry FM-024 keep it, and no line gains an id;
   - **not this lane:** the seats page's "seven development seats" counts seats, not icons, so it moves with the seat's
     pull request.

   The Designer weighed dropping the count in L118 and L4195, so that a ninth seat would not touch them, and proposes
   the plain count, which keeps each line's meaning.

4. **The lane:**
   - `brand/seats/coordinator.svg` lands from the hashed copy, B byte for byte;
   - `SEAT_ICONS` gets its entry, the file but for the ground square, as the seven's. Its comment's "The seven seat
     icons" becomes eight, and the row rule's "a word outside the seven"
     ([L4195](https://github.com/shoalmark/shoalmark/blob/ec8479c68ffceb8afb545a3a745c58b310781b63/shoalmark.py#L4195)) matches;
   - `preview.html` and `export.py` say eight, and the preview's designer line "these seven" becomes eight;
   - the README row, and the pins that count or pin seven: `_SEAT_PINS`, which gains B's sha256, `_SEAT_WORDS`, which
     gains an eighth session, and the checks and messages beside them in `test_shoalmark.py`
     ([L8114](https://github.com/shoalmark/shoalmark/blob/ec8479c68ffceb8afb545a3a745c58b310781b63/test_shoalmark.py#L8114)),
     and `SEAT_ICON_EDITS` in `test_git_entry_differential.py`, whose pinned CSS text changes with L4195
     ([L1486](https://github.com/shoalmark/shoalmark/blob/ec8479c68ffceb8afb545a3a745c58b310781b63/test_git_entry_differential.py#L1486));
   - a rendered-surface lane: the Designer's check of the page beside its review.
5. **Order:** it is built only after the coordinator seat's pull request merges and FM-160-Q1 is answered.
6. **Allocation:** v0.20.3, a chapter of FM-139.

## Done when

Each item names its commit or pull request when it lands.

- [ ] **`brand/seats/coordinator.svg` is B byte for byte,** and `export.py` exits 0 for all eight.
- [ ] **A coordinator session's row shows its icon,** 20 px, grey, without the ground, and the seven's rows are
  unchanged.
- [ ] **The README row stands in the Owner's words,** and every "seven" the eighth seat touches reads as decision 3
  sets out.
- [ ] **The pins hold the eight,** and a page whose coordinator icon differs fails them.
- [ ] **The Designer's check and the review are READY.**

## Ship log

| Date | Event |
|---|---|
| 2026-11-12 | Filed, Proposed, with FM-160-Q1, on the Auditor's word: `epic: FM-139`, under v0.20.3's epic until the Owner decides whether it goes in. Nothing is built. |
