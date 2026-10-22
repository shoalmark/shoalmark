# The board's design guide

This guide holds the rules the v0.20.x board is built from: its look, its words, and its sections' command-line output. It
does not cover the landing page. The Owner's signed answer on FM-053 adopts it, as it stands at the commit that filed that ask. A rule here
changes only by the Owner's signed answer.

---

## 1. What the board is for

> **The Owner opens the board to answer what waits for their word, and to find the session they need to get back to.**

Everything else supports that, folds, or goes.

| Part of the board | Its job | Default |
|---|---|---|
| **waiting for you** | **What the Owner came for:** each ask, its type, its state, its proof, and the *accept* and *reject* buttons | first, open |
| your acts, with their time | what the Owner owes, by the clock | open where any exist; absent where none |
| **the day** | **A frame, the last 24 hours:** it holds three parts at one level, `h3`, their text on one column: `### stand-up` with its copy button in the heading, the day's sessions as a fold, and `### close-out` with its copy button. No row rule runs between them, and no type word stands in for *begins* or *ends*: the order says it. Its heading carries only its own summary: *the last 24 hours* | open; it never folds, because it holds both actions |
| sessions, inside the day | the way back into a session: one fold, *sessions* | open on a desktop, folded on a phone, its heading carrying the counts and its caveat in a few words (*at work or closed: not known*). Opened, a row that holds something for the Owner, such as a session *waiting for your answer*, is open, and the others are closed |
| reviews | the week's verdicts and who gave them: before a merge, whether each READY came from another session than the branch's (`README.md`, *Verdicts*, says *independent*: the older word). Opened, what needs a look, one row each: every verdict that is not READY, has findings, came from the branch's own session or cannot be traced. The rest, READY by another session, fold into one line, *and n more verdicts by another session this week*, which opens to them in the same rows. A row is two lines: the verdict's id, *on <branch> @ <commit>*; then its word as a type and who gave it, *by another session · <its session>, the branch's <session>*; a branch or a session not known says so, with its reason. The week is one list: it is never paged | folded after the day, its heading carrying the week's counts in words, *6 by another session · 2 by the same session*, and *reports, not proofs*, led by *n not ready* in coral and *n with findings* in amber where there are any; never inside the day, which is the last 24 hours |
| receipts | counts, read on request | folded, its heading carrying the range and *counts the record holds, not a cause*, **never a total**: a total in a heading reads as a result in any picture of the board. The counts appear opened, each with its definition |
| your current path | your own words, known by heart; titled *your current path*, never *only you change it* while FM-037 is open | folded, its heading carrying its line count |
| the work, by rank | the table below the box | as today |

**The decision tree, applied to every new element:**
1. Is it what the Owner came for? It goes first.
2. Does it support that? It sits beside it, visible.
3. Is it needed only sometimes? It folds, and its heading says what is inside, with counts, so no click is needed to know.
4. Does it repeat something already there? It goes.

---

## 2. Principles

1. **Answer first.** The first line of every view is what the Owner came for. The page's state, such as when it was read,
   stands quietly in its header.
2. **One look: `monochrome`.** One monospaced face, one grid, a 104-character frame, every marker drawn in text. No chrome:
   the theme's margin chart stays on the landing and the docs pages, never on a board.
3. **Words carry the meaning.** Remove every icon and every colour, and each row must still say what it is, what is true of
   it, and what can be done (§11, test 1).
4. **Type, state and action look different** (§6). A type is never framed. A state is never a button. An action is never
   coloured as a warning.
5. **A box means an action; information is never boxed** (the Owner's rule). A button is a word in a 1px frame. Nothing
   else is framed like a chip: no pill, no badge, no boxed label (§8, *Why boxes, not brackets*). One action is not boxed:
   help's own mark, `[×]`, which hides a help line (§8, *Help*).
6. **Three meanings, one colour each, inside the Owner's box:** teal for done or success, amber for a warning, coral for a
   failure. Everything else is grey, except the tool's own voice: **help**, in violet behind a dashed rule, which is never a
   state, a value, an action or a warning (§8, *Help*). A meaning may also stand on a tinted surface (§8, *A surface*),
   always beside its word. Colour marks a state the tool computed, or a verdict's word as the reviewer gave it; never a
   confidence, a handover's prose, a total or a live state.
7. **Never claim what the page cannot show.**
   - Every view says what it read and when.
   - Every unknown says why.
   - A shared session id is shown as ambiguous, never as one session.
   - The page never says *live*, *current*, *running*, *ended*, *all*, *every agent*, or *proves* of a report (§10).
8. **Nothing moves.** There is no motion but a fold opening. Nothing pulses. The board reads its file again when you come
   back to it; nothing polls.

---

## 3. After R10: what stays, what goes

R10 removes the *runtime brand cascade, font machinery and theme copying*, and keeps *the static mark, labels and semantic
headings*. Its look half lands with the board's v2 build. The theme layering (`theme.css` from the brand folders), the
inlined font files and their `@font-face`, theme copying with `--brand DIR --from <theme>`, and the inline wordmark go. The
Owner's palette, by name or by a few tokens in `shoalmark.toml` (§5), replaces the theme's colours. Nothing is copied, and
no font ships. The logo and the labels are read where they are read today.

| | Stays, built into the one file | Goes |
|---|---|---|
| **Look** | `monochrome`'s rules, folded into the board's own CSS as static rules on the base tokens; the Owner's palette, by name or by a few tokens in `shoalmark.toml` (§5), in place of a theme's colours | `theme.css` and its layering from the brand folders; theme copying, `--brand DIR --from <theme>` |
| **Type** | the system's monospace (§5) | the inlined font files, the IBM Plex Mono cuts, and their `@font-face`: no font ships |
| **Mark** | the Pricke, `PRICKE`, in the running line and as the page's icon; **a logo of the Owner's own**, beside the repository's name in the header, read where it is read today (§4) | the inline wordmark, `wordmark.svg`; nothing is copied |
| **Words** | every label in the label table, and `labels.yaml` for another language (R10's *labels*), read where it is read today | — |
| **Structure** | semantic headings: `h2` for the box's sections, `h3` inside a section | headings set as CSS content |
| **The margin chart** | — | `monochrome`'s nautical chart: chrome, so it leaves the board. It stays on the landing and the docs pages |

**Never a silent loss:** a board build names, file by file, each brand file it no longer reads and the setting that replaces
it; `--check` never fails on them.

From the release that lands this look on, this section, §5 and §13 take over from `brand/themes/README.md`: nothing is
copied, `monochrome` is the board's own look and `shoalmark` a palette by name, and one system face replaces its font table.

---

## 4. Marks and icons

### The Pricke, shoalmark's mark

- **Source:** `PRICKE` in `shoalmark.py`, a 16-unit pixel drawing.
- **Use:** the running line at 16 px, the smallest size its grid stays sharp at, with the name *shoalmark* and the version.
  It is also the page's icon. It is never enlarged into a logo on the board; the landing does that.
- **Colour:** `currentColor` (the running line's grey). It is never tinted.

### The Owner's logo

- **Kept** (R10): one logo of the Owner's own, 22px high before the repository's name, as today's header draws a logo. It
  is checked for size only, within the tool's size limit, and shown only as an image, never inline. It is never
  recoloured.
- Where there is none, the header is the name alone.

### The repository's name

- The header's first element is the configured `name`, in ink at weight 600, followed by the search line.
- It is identity, so it stands quietly. It is never framed and never coloured.

### The seat icons

- **Source:** `brand/seats/<seat>.svg` (FM-024), seven hand-drawn icons on a 20-unit grid. They would become static
  constants in the tool, as `PRICKE` is.
- **In a row: 20 px, in grey, without the icon's ground; on the light board and on paper, inverted**
  (`filter: grayscale(1)`, with `invert(1)` there). The row leaves out the icon's ground square, so no seat sits on a
  tile; the icon files and their use as avatars keep it. The family was drawn to read without colour, and its README judges
  each icon at 20 px *"grey included"*. Grey keeps colour for state: several icons' details, every blush among them, use
  the same coral that means a failure.
- **In colour** only where the icons themselves are the subject: a gallery, the README, a forge avatar.
- **Never alone:** the seat's word always stands beside its icon (`aria-hidden="true"`). A seat outside the seven gets an
  empty 20-pixel slot, never a borrowed icon.
- **No harness logos.** Harnesses are words: CLAUDE CODE, CODEX.

### The UI icons

Four icons, drawn for the board. Their sources are `brand/icons/`: `copy.svg`, `check.svg`, `cross.svg` and `out.svg`. In
the tool they would be static constants, as `PRICKE` is.

| Icon | Means | Where |
|---|---|---|
| **copy**, two sheets | this button copies what it names; it never runs it | before the noun on every copy button: *stand-up prompt*, *close-out prompt*, *resume command*, *rebuild command*, *claude --resume*, *codex resume*, and *prompt* or *command* in a dialog |
| **check** | copied: the clipboard confirmed it | before *copied:*, and before *the prompt is on your clipboard* |
| **cross** | not copied | before *not copied*, and before *copying did not work* |
| **out**, an arrow leaving a box | a link that leaves the board | after the link's text: the running line's *shoalmark*, the signing page, the forge |

- **Drawing:** a 12-unit grid, whole-unit rectangles only, `shape-rendering: crispEdges`, filled with `currentColor`. No
  stroke, no curve, no transform: the Pricke's pixel style, and the seat icons' rule (`brand/seats/README.md`), so each
  rasterises crisp at 12, 24 and 48 px.
- **Size and place:** 12 px on the 14 px text, one unit below the baseline, `.7ch` before its word. It takes its colour
  from the text it stands in: grey in a button, ink under the pointer, teal in *copied*, coral in *not copied*. It is never
  coloured on its own.
- **Never alone:** an icon always stands beside its word, and is `aria-hidden`. Nothing is an icon-only button.
- **Only these four.** A new icon joins the set only when a word cannot carry its meaning alone, and on the same grid.

### Drawn markers

`monochrome` draws these in text. Each is drawn, never read: its alt text is empty (`content: "## " / ""`). The theme's
fourth marker, the bracketed button `[ word ]`, is not used: on the board an action is a box (§8).

| Marker | Means | Where |
|---|---|---|
| `## ` | a section heading | the box's sections (`h2`), the dialog's (`h4`) |
| `### ` | a part of a section | the day's *stand-up* and *close-out* (`h3`) |
| `// ` | a group | the work table's groups |
| `> ` and `v ` | folded and open | every fold's heading, every expandable row. A fold's marker is padded to its level's width (2ch beside `##`, 3ch beside `###`), so every heading's text at one level starts on one column |
| ` · ` | a separator between facts | quiet lines |
| `> ` before the search | a prompt line | the search field |

---

## 5. Colour and type

### Colour tokens

The base board's own tokens. `monochrome` keeps them and adds `--box` and `--raise`. Contrast is measured with the WCAG
formula, against the page.

| Token | Role | Light | Dark | Contrast, light / dark |
|---|---|---|---|---|
| `--bg` | the page | `#f7f7f5` | `#0e0e0e` | — |
| `--raise` | an action, or a folded section's band, under the pointer | `#ececea` | `#1d1f24` | ink on it 15.3 / 14.3 |
| `--ink` | what the row is; the deciding word in a state | `#161616` | `#efefef` | 16.9 / 16.8 |
| `--dim` | states, quiet lines, types | `#565656` | `#ababab` | 6.8 / 8.4 |
| `--mute` | markers, column heads, *not known*, and **every action's frame and the search field's**: the frame carries the meaning, so it needs 3:1 (WCAG 1.4.11) | `#6a6a6a` | `#8f8f8f` | 5.0 / 6.0 |
| `--line` | row rules | `rgba(0,0,0,.14)` | `rgba(255,255,255,.15)` | — |
| `--box` | the one titled frame, the Owner's box, and the rule on each band's top edge (§7): structure, so no contrast floor | `rgba(0,0,0,.28)` | `rgba(240,241,244,.26)` | 2.0 / 2.1 |
| `--coral` | **a failure:** NOT READY, *not copied*, *not verified*, a missed act, a failed handover, a removed line, a consequence that names a failure | `#b3402f` | `#ff7b66` | 5.3 / 7.6 |
| `--teal` | **done, success:** *copied*, READY, *verified*, an added line, the command's left rule in a dialog | `#187953` | `#4fd1a1` | 5.0 / 10.1 |
| `--amber` | **a warning:** asks waiting for you and every count of them, READY WITH FINDINGS, *ambiguous*, *author only*, an act overdue within its window, a consequence line | `#8a5600` | `#f0b44c` | 5.7 / 10.4 |
| `--help` | **the tool's voice:** help text and its dashed rule. Not an accent: it marks no row, value or action. A violet no state uses | `#7b3fbf` | `#c09cff` | 5.9 / 8.7 |
| `--secbg` | a section heading's band, and a table's heads: structure, not state. Named apart from the landing theme's `--band`, its navy claim band | `#efefeb` | `#18191c` | ink 15.7 / 15.3 · `--mute` 4.7 / 5.4 · amber 5.3 / 9.5 |
| `--okbg` | teal's tint | `#e1f0e7` | `#10271d` | ink 15.4 / 13.7 · `--mute` 4.6 / 4.9 · teal 4.6 / 8.2 |
| `--warnbg` | amber's tint | `#fbf0d6` | `#2a200d` | ink 16.0 / 13.9 · `--mute` 4.8 / 5.0 · amber 5.4 / 8.6 |
| `--failbg` | coral's tint | `#faeae6` | `#2c1612` | ink 15.5 / 14.8 · `--mute` 4.6 / 5.3 · coral 4.9 / 6.7 |
| `--blue`, `--yellow` | the work table's status squares only, a data colour outside the box | `#2f62d6`, `#946c0f` | `#6f9bff`, `#e8cf5a` | 5.1, 4.4 / 7.2, 12.4 |

- **`--raise` departs from the theme's `#f9f9f9` and `#16181d`:** those sit within 1 % of the page and a hover could
  not be seen.
- **The budget:** inside the Owner's box, the three meanings and their tints, plus help's violet as a voice and the
  neutral band. Blue and yellow are the work table's 5-pixel status squares only, where the word stands beside them.
  Help's violet is a colour no state uses, so help can never be read as a status. By day yellow reaches 4.4:1, enough for
  a square (3:1) but not for text, so it is never text; amber is darker by day, so it carries text (5.7:1). A verdict's
  word, 12 px on its tint, measures teal 4.6 / 8.2, amber 5.4 / 8.6 and coral 4.9 / 6.7.
- **Colour is never the only carrier.** Each accented thing also has its word: *overdue*, *ambiguous*, *not copied*,
  *copied*.
- **Every colour is a token on `:root`,** so a palette is a token swap.

### The Owner's palette

An Owner chooses the board's colours, directly or through an agent: a palette by name, or a few colour tokens in
`shoalmark.toml`, refused by the tool below a set contrast.

- **By name:** `monochrome`, every board's default, or `shoalmark`, the palette of the public pages: the landing and the
  docs (§13). A board wears `monochrome` unless its `shoalmark.toml` names another.
- **By tokens:** a few of the role tokens, each with its light and its dark value:

  ```toml
  [palette]
  name = "monochrome"                  # or "shoalmark"; the tokens below override it
  bg   = ["#f7f7f5", "#0e0e0e"]        # light, dark
  ink  = ["#161616", "#efefef"]
  ok   = ["#187953", "#4fd1a1"]        # --teal: done, success
  warn = ["#8a5600", "#f0b44c"]        # --amber: a warning
  fail = ["#b3402f", "#ff7b66"]        # --coral: a failure
  owed = ["#a0156e", "#ee92d4"]        # what waits on you; warn's value where unset
  # secbg, okbg, warnbg, failbg = [light, dark]: optional, as below
  help = ["#7b3fbf", "#c09cff"]        # the tool's voice
  ```

  `dim`, `mute`, `line`, `box` and `raise` are derived from `bg` and `ink`. `secbg`, `okbg`, `warnbg` and `failbg` may be named
  like the tokens above; where a palette names none, the tool takes `monochrome`'s and checks them against the palette's
  `bg` and accents, refusing the palette in one line naming the pair. The status colours stay the palette's.
- **The set contrast, checked by the tool, which refuses the palette in one line naming the pair:**
  - every text token, help included, at least 4.5:1 against `bg`, against `raise`, and on every surface (`secbg`, `okbg`,
    `warnbg`, `failbg`);
  - `mute`, the action's frame, at least 3:1 against `bg`;
  - in light and in dark, each.
- **Nothing is copied and no font ships.** The palette is read where the board is built, and its values go into the page's
  `:root`.

### Type

- **One face:** `"Berkeley Mono", ui-monospace, "SF Mono", Menlo, Consolas, "DejaVu Sans Mono", monospace`. The first name is
  the base board's own; it is used where it is installed. No font file ships.
- **One grid:** 14 px on a 21 px line, so a character is a cell. The frame is 104ch plus the page's padding, so the Owner's
  box holds 100 characters of prose.
- **Hierarchy comes from weight and markers, not size.**
  - Weight 600 marks a heading, the deciding word in a state (*waiting for your answer*, **signed**) and a verdict's
    word (§6, *TYPE*), nothing else.
  - Weight 400 is everything else, ids and seat names included: an id is told by its underline, a seat by its icon.
  - There are two exceptions to the one size, both 12 px:
    - a **type**, in capitals with letter-spacing `.06em` (§6): a label, set slightly apart from the prose;
    - **the running line** (the Pricke, the name, the version), as `monochrome` sets it.
- **Italic** means a value that is not known, in place of that value (*not known*, *resume not known*), and nothing else.
  A deliberate absence (*resumes with its parent*, *no resume*, *asked before ask ids*) and an explanation are plain
  `--mute`.

---

## 6. The row grammar: type, state, action

Every row reads in one order:

> **what it is** · TYPE · state … **action** **action**, each action in its box

| Part | Looks like | Examples |
|---|---|---|
| **What it is** | ink: the id at weight 400, underlined and linked; the question or the seat | `NA-012-Q2` Ship the export as CSV only, or as CSV and JSON? · **planner** `<session id>` |
| **TYPE**: what kind of thing | 12 px capitals in `--dim`, never framed. Coloured once only: a verdict's word, in its meaning's colour at weight 600, on its row's tint | DECISION · YOUR HANDS · ONE CLICK · ACT · CLAUDE CODE · CODEX |
| **State**: what is true of it now | the quiet line in `--dim`, facts separated by ` · `, the deciding word in ink, what waits on you in amber, *not known* in italics | 1 day · holds up NA-014 · your answer here: **signed** · last commit 12 min ago · NA-014 |
| **Action**: what you can do | a word in a 1px `--mute` frame, `--dim`, ink on `--raise` under the pointer; last on the row; a pair never splits across lines | verbs, with no icon: accept · reject · done · reschedule. Nouns, with the copy icon: stand-up prompt · resume command. Each boxed |
| **Consequence**: a warning about this row | its own line beneath, indented 2ch, in amber; in coral where it names a failure | an answer here proves the author only: any session that can commit here can write one in your name |

- **Ordering inside a section** keeps the board's rule for each section (oldest ask first; for sessions, those waiting
  for the Owner first, then the newest last commit, ambiguous ids last).
- **The proof is a state:** *your answer here: signed*, *author only*, *server login*, *no author*. It is never *proves:
  signed*, because a signature proves the key, not the hand.
  - **On one repository's board** it is the same for every ask, so it is stated once, in *waiting for you*'s heading. Its
    consequence, if any, is the line beneath the heading.
  - **Across repositories** it differs, so it stands in each row, with its consequence beneath. The row starts with its
    repository, in ink, before the id: the repository is part of what it is.
- **The harness column holds a type or *not known*, nothing else.** A sub-session runs in its parent's harness, so it shows
  the parent's type; *resumes with its parent* stands in the resume column.
- **One phrasing:** what waits on the Owner is *waiting for you* everywhere: *2 waiting for you* in a heading, *waiting for
  your answer* on a session.
- **One action, one place.** *Asked by planner `<session id>`* on an ask is state, linked to that session's row. The resume
  button stands only in the session list, never twice.
- **Two ask kinds take plainer words:** `ruling` reads DECISION, as the German board's *Entscheidung* already does, and
  `ceremony`, *a button* today (`ask.ceremony`), reads ONE CLICK, as the German *Knopfdruck*. A type beside real buttons
  must never read as one.
- **Rows line up:** the id stands in a column of its own (10ch). The question or title, and the state line under it,
  start on one column after it.

---

## 7. Layout

- **One column, one frame:** `max-width: calc(104ch + 32px)`. There is no sidebar and no tabs. The header line is the page's
  identity card: the name, the search, the light-or-dark setting (*◉ dark*, §8 *A setting*), what was read and when,
  and the *rebuild command* copy button.
- **Vertical rhythm** comes in lines of 21 px:
  - a section of the Owner's box opens on its band (§8, *A surface*), 16 px below the section before it. The band's top
    edge is a 1px `--box` rule, so the band is the divider: it holds where a band's faint fill does not, on a dim
    screen, in print and in forced colours. The first band has none, since the box's frame is right above it. The parts
    of a section, such as the day's stand-up, sessions and close-out, keep spacing only;
  - rows sit 3 px apart, separated by a `--line` rule.
- **Widths** come in `ch`. The session row's columns are 20 px for the icon, then seat and session, harness, worktree, and
  last commit with its work item, then the action, right-aligned.
- **Breakpoints:**
  - **The README's 880 px:** the desktop row still holds, unstacked and untruncated: the README's picture of the board is
    shown at that width. Its columns' least widths add up to about 87ch.
  - **800 px and narrower:** a session row stacks. The icon and the seat come first, then harness · worktree · last commit,
    then the action. *Last commit* names itself, because the column heads are gone.
  - **640 px and narrower, a phone:** *waiting for you* first; the sessions folded, their heading carrying *n waiting for
    you*; receipts folded. The copy buttons stay: a phone can reach a remote terminal, but the fold keeps them out of the
    way.
- **The order of a board, top to bottom:**
  1. the name and the search;
  2. *read from … at …*;
  3. the Owner's box: waiting for you, your acts, *the day* (stand-up, its sessions, close-out), reviews, receipts, the
     current path;
  4. the work table;
  5. the running line, at the right.

---

## 8. Components

| Component | Rule |
|---|---|
| **The Owner's box** | One titled frame (`--box`, 1px), *yours* set into its top border, as `monochrome` draws it. It is the only element that holds information inside a frame. Inside, sections are `## ` headings with counts, each on its band (*A surface*) |
| **A section heading** | `## the day · the last 24 hours`, or a fold inside it, `> sessions · 4 with a commit in the last 24 hours (8 with their sub-sessions) · 2 waiting for you · 1 id ambiguous`. The counts are the state that makes a fold scannable. Its help line beneath names only what the section reads beyond the header's read-at line, and what cannot be seen: the header already says when |
| **A heading's line** | Three parts, in this order: the title (never wraps), its state (the only part that wraps, hanging beside the title), and its action at the right edge, which never drops below. On a phone the whole heading may wrap. A heading's state stays short: the help line beneath carries the rest |
| **A fold** | A `details` element: the heading is its `summary`, `> ` closed and `v ` open. Its default follows §1. On a phone, a script may close it at load |
| **A row** | §6. A row that opens shows its details in quiet lines indented 4ch: commit counts, the last commit's subject, model, effort. A session's sub-sessions stand on one line of their own under its row (*+ builder 1–3 · reviewer 1, who resume with it*), never inside the seat's cell |
| **A button** | A box, in `monochrome`: the word in the grid's face and `--dim`, lowercase, inside a 1px `--mute` frame (5.0:1 and 6.0:1: the frame carries the meaning) with 1px by 1ch of padding, 17px of line inside, so a button keeps the 21px line. Under the pointer: ink on `--raise`, the frame in ink. A visible focus ring (1px ink outline, offset 2px). At least 24px high on a phone (3px by 1ch of padding). In a dialog the one button that goes ahead is filled in ink. A pair stays on one line. **A copy button** carries the copy icon before its noun (*stand-up prompt*); its accessible name keeps the verb, *copy the stand-up prompt*, which contains the visible label (WCAG 2.5.3). A verb button has no icon |
| **A setting** | A radio or a switch, unboxed, drawn as the guided answer view's radios: its mark, *◉* on and *○* off, then its word, in `--dim`, and in ink when on. A setting holds a state, so it is never a button (§6). **A switch** is one `<input type="checkbox" role="switch">` with its word, on where what it names holds: the header's *◉ dark* is on where the board is dark. The page starts from the system's scheme; a pick is kept, and a pick equal to the system's is forgotten, so the page follows the system again. Paper stays light. **A choice** of two or more is a named `role="radiogroup"`, its options on one line after its word, *by ◉ board ○ story*, and the arrow keys move within it. On a phone each label is at least 24px high |
| **Copy feedback** | Under the row, in the state line, on teal's tint from frame to frame: *copied:* in teal after the check icon, then the command, then the limit on a line of its own (*whether it still runs is not known here*). Or *not copied* in coral after the cross icon: *this page has no clipboard here … select the command*. *Copied* is said only when the clipboard confirms it |
| **A dialog** | A window: a 1px ink frame, its title set into the top border. Sections are `## ` headings. The command or prompt stands behind a 1ch teal rule at its left edge, on the page ground, never in a tinted box; the change a command commits may stand as a diff (*A surface*). The status line comes first (*the prompt is on your clipboard*), then the text, then *what it asks the session to run* and *what it does not ask for*. A dialog promises the prompt's words, never a session's conduct |
| **Help** | The tool's own voice: one short line that says how to read a section (*begins with your stand-up, ends with your close-out, at the times you choose*). **One help line per view, not per section:** a fold's caveat is a few words in its heading's state, and the page's fuller limits stand once, folded under the read-at line (*The page's limits*). Violet (`--help`) behind a 2px dashed rule at its left edge, 1ch in, on the page ground. **Never a value, a state, an action or a warning:** a row's reason stays its grey state line, a consequence stays amber, or coral where it names a failure, a button never sits inside help. At most one help line per section, under its heading or in an empty state; never one per row. In a dialog the dialog itself is the help, so its text stays ink and grey, except the guided answer view's one help line (*The guided answer view*). The same words rules as everything else (§10). Recognised without colour by its dashed rule (§11, test 1). **Hiding:** help that only explains how to read carries its own mark, `[×]`: superscript, 11 px, in help's violet, underlined under the pointer, spoken *hide this help*. It stands after the last word of a one-line help, and top-right, at the end of the first line, of a help that wraps. It is the one action not in a box: it belongs to help's voice, not to the page's actions. The × sign, never the letter x: `[x]` is a done checkbox in Markdown. Pressed, the line is hidden in this browser, and a quiet line under the read-at line says *some help is hidden in this browser* with *show help again*. **The page's limits never hide:** the read-at line, *what this page reads, and what it cannot see*, an empty state's reason and a count's definition. Hiding is a viewer's convenience, kept in the browser, never in the repository |
| **The page's limits** | One fold under the read-at line, closed: *what this page reads, and what it cannot see*. Opened, one help line: what was read and when, what was read beyond it (this machine's worktree settings), that a session that never committed is not seen, and that whether a session still runs is not known. The limits stay on the page, said once |
| **No column heads in the day's folds** | A session row's type words and formats describe themselves (CLAUDE CODE, *22 min ago · NA-014*); heads repeated per fold are chrome. On narrow screens *last commit* names itself |
| **A table** (the work table, receipts) | No outer box. Column heads as types (12 px capitals, `--mute`), on a band; `--line` rules between rows; numbers right-aligned in the same face |
| **The read-at line** | `read from main @ <commit> at 10-15 09:41 · it reads its file again when you come back to it; nothing polls`, and the *rebuild command* copy button at the line's right edge. The line is state, in `--dim` |
| **Unknown** | *not known*, in italics, always with its reason: *resume not known — no worktree on this machine names this session now* |
| **Ambiguous** | A 2px solid amber rule at the left of the block, on amber's tint (a dashed rule is help's), the word *ambiguous* in amber, one line per worktree, no action, and *counted as no session* in the heading |
| **Empty** | It says why, and what the backend cannot give: *Subversion keeps no session in its revisions here … an empty list here is not a quiet day*. It offers the way that remains: the *claude --resume* and *codex resume* copy buttons |
| **Command-line output** | The same words as the board. Section titles in capitals as `--standup` prints them, with the board's words (*DECISIONS — answer; …*, *ONE CLICK — …*), two-space indents, ` · ` between facts, ages and *not known* as on the board. Its first line says what was read and when. The three meanings as text colours only: a terminal has no surfaces |
| **A surface** | **A band:** `--secbg` behind a section heading of the box, from frame to frame, its text on the box's column, its top edge a 1px `--box` rule (§7). A folded section is its band alone, `--raise` under the pointer. A table's heads stand on a band too. **A tint:** `--okbg`, `--warnbg` or `--failbg` behind a whole row or a band, from frame to frame, beside the word that carries its meaning without it (§11, test 1). It is used for: *waiting for you*'s band while asks wait; *copied*; *ambiguous*; a verdict's row, READY on teal's, READY WITH FINDINGS on amber's, NOT READY on coral's, the verdict's word in its colour at 600 and nothing else on the row coloured, the heading counting the amber and the coral; a signature's result. Never a frame, a chip or a single word. **A diff:** the path and `+n −m` on a band, old and new line numbers, `+` lines on teal's tint and `−` lines on coral's |
| **The guided answer view** | A view of the board that a prepared run opens for one ask, and nothing else. **The header:** the name and why it opened (*your answer is needed · 2 of 2 in the run you started*, the first words amber); the read-at line with the branch and head; under it the tool's own commit, *written by shoalmark @ <sha>, main*; the limits folded. **One window,** as wide as the frame, titled *your answer · <ask id>*. **The ask:** the question and its state. **`## your choice` on a band:** one row per choice: a radio, a letter, the words. The proposal comes first, with PROPOSED and the seat's confidence; *because* and *then* stand in the label column. *In your own words* and *reject the question* each have a typed box, three lines high, on its own line, in the search field's frame. Nothing is picked; your pick stands on a neutral band, *not signed yet* in amber. **`## where you sign` on a band:** empty until a pick, then the change as a diff, *how you sign* in three steps, and at the window's foot the *reply* copy button, filled, with its copy feedback (the foot on teal's tint once copied). **One help line,** inside the window under *your choice*. **The view signs and runs nothing** (R5). **The result is a new view:** the change as signed, then COMMIT, SIGNER, SIGNATURE and TOOL, the signature on its meaning's tint. **Each commit links to its forge where one is known:** the repository's from `commit_url` where it is set, else from its configured prefix (`blob`) where that gives a commit link, the tool's to the public shoalmark repository. Where there is no link, the line says why: not pushed, no forge configured, or Subversion with no viewer. The key *asks you to confirm*, and only if it asks: some keys never ask. Never *touch*. A confirmation is never called *your signature*, nor proof that you were there. *Verified* is said of a signature only: it verifies against a key the signers file lists |

---

### Why boxes, not brackets

Buttons were first drawn as `monochrome` does, as a bracketed word. The Owner asked for boxes, and the reasons hold:
- **Brackets already mean something else in the tool's output.** `--standup` prints `[3 days]` and `[frees NA-014]` around
  state, so *brackets mean an action* could not hold across the board and its commands.
- **Target size.** A bracketed word has about 1px of padding; a boxed one reaches 24px on a phone (WCAG 2.5.8).
- **The Owner's rule says it in its own words:** *a box means an action; information is never boxed*.

The theme's other drawn markers stay: they label structure, never an action.

## 9. Responsive story

| Width | What the Owner sees first | What folds |
|---|---|---|
| Desktop | the box, open: waiting for you and the sessions | receipts; each session's details |
| 800 px | the same, with session rows stacked | as desktop |
| Phone | waiting for you, its buttons kept together | sessions and receipts, their headings still carrying their counts |

**The work table on a phone** (640 px and narrower) stacks each row: the id, tier and status share a line, wrapping
under the id where they must, and the title takes the full width under them, hanging at the id's column. The column
heads go, and the rule moves to the row. Nothing scrolls sideways: the page is never wider than the screen.

---

## 10. Words

- **Voice:** lowercase labels, plain words, no exclamation marks. A seat is *it*.
- **The person is *you*.** On the board the Owner is always *you*: *yours*, *your current path*, *where you keep the
  count*, *the repositories you name*. *The Owner* appears only in record text, such as a tracker excerpt or an answer's
  *answered-by*, and in the record they are *they*. `owner` appears only in code font, as a setting (`owner` line) or a
  command (`--owner`), never as a role.
- **The labels this changes,** in English and in German in one pass:

  | Key | Was | Becomes | German |
  |---|---|---|---|
  | `owner.title` | owed to the owner | yours | German after the native read |
  | `path.title` | the current path | your current path | the same |
  | `ask.ruling` | a ruling | decision | *Entscheidung*, as the German board already reads |
  | `ask.ceremony` | a button | one click | *Knopfdruck* |
  | `--standup` headings | RULINGS · BUTTONS | DECISIONS · ONE CLICK | the same labels |
  | reviews' heading and rows | independent *n* · same session *m* | *n* by another session · *m* by the same session | German after the native read. The README's line that quotes the old label changes with it, and so do the tests that pin it |
  | `sessions.recent`, `sessions.none.day` | {0} in the last 24 hours · none in the last 24 hours | {0} with a commit in the last 24 hours · none with a commit in the last 24 hours | German after the native read. It says what a row is and what *12 min ago* measures, so a resume button beside it never reads as a live view; it is the README's own *with a commit in the last day* |
  | receipts' relay line | where the Owner keeps the count | where you keep the count | the same |
  | `viewer.handover` | hand-over | handover | *Übergabe*, unchanged |
- **Help** is one plain sentence, or facts joined by ` · `. It explains how to read, or names a limit; it never instructs
  an agent and never promises an outcome.
- **Formats:**
  - an age as *12 min ago*, *3 h ago*, *2 days*;
  - on the board, a time as *10-15 09:41* in the machine's local time;
  - in a command's output, a full date as *2026-10-15*;
  - ids in the mono face, linked.
- **Never on a board:** *live*, *running*, *active*, *ended*, *current*, *up to date*, *all your projects*, *every agent*,
  *all sessions*, *verified* or *proves* of a report, *independent* of a session, *less work*, *faster*, any *touch*.
  *Signed* means a commit that verifies against a key the signers file lists, never *by the Owner*.
- **A button names its act or its thing.** A verb does the act: *accept*, *reject*, *done*, *reschedule*. A noun is copied:
  *stand-up prompt*, *resume command*, *rebuild command*, with the copy icon. Never *resume* alone, which would read as
  *resume now*.
- **A prompt's words, never an agent's conduct:** *the prompt asks the session to read …*, never *the session reads …*.
- **Always on a board:**
  - what was read and when;
  - *not known*, with its reason;
  - *a report, not a proof*, where a seat's words are shown;
  - *in {n} repositories you named* across repositories.
- **Labels** live in the label table, with keys such as `sessions.recent` and `resume.copy`. `labels.yaml` gives another
  language, and the German board takes them there. Site copy is German first; the board is not site copy.

---

## 11. Acceptance tests for every screen

1. **The five-second test.** Remove the icons and every colour. Each row must still say what it is, its type, its state and
   its actions, in that order; a noun button must still read as something to copy, and help is still told apart by its
   dashed rule.
2. **The meanings.** Inside the Owner's box, teal only for done or success, and the 1ch rule beside a command in a
   dialog (§8); amber only for a warning, coral only for a failure, each beside its word, as text or as a tint; violet
   only on help. No tint on a confidence, a handover's prose, a total or a live state.
3. **Nothing framed but actions.** A box only on what is clickable, and on a field you type in (the search, the guided
   answer's typed boxes). One titled frame, the Owner's box, and the dialog's window. No chip, pill or boxed label.
   Every action's frame at least 3:1 against the page. Every button at least 24px high on a phone.
4. **Said, not implied.** The view names what it read and when, once; no limit can be hidden. Each *not known* has its
   reason. No word from §10's *never* list appears, and no line promises what a session will do.
5. **Answer first.** The first thing under the header is what waits for you. On a phone, nothing comes before it.
6. **No duplicates.** If two elements show the same fact in the same view, one goes, unless the Owner ruled the repeat
   (the proof on the row and again in the dialog is ruled: the Owner's ruling, recorded privately). A count in a heading is
   not said again on a row: the row says the thing itself (*FAILED the Windows suite …*).
7. **The first screen.** On a desktop, the board above the work table fits about thirty lines with its one *sessions* fold
   open.
8. **You, never the owner.** No screen shows *owner* outside code font or a record excerpt.

---

## 12. Decided

FM-053's answer settles what this guide once left open. No decision is open here:
- **The palette:** every board defaults to `monochrome`. `shoalmark` is the palette of the public pages, the landing and
  the docs.
- **The chart:** the nautical chart is chrome. It leaves every board, `monochrome`'s included; the landing and the docs
  keep their own.
- **The box:** the Owner's box keeps its titled frame, as `monochrome` draws it (§8).
- **The current path** folds (§1).

---

## 13. The `shoalmark` palette

`shoalmark` is the palette of the public pages, the landing and the docs. No board wears it by default; an Owner may name
it for a board. It is the same grid and markers, in a sea
chart's colours:
- **deep water** for the page;
- **shallow tints** for the box;
- the **Watt's drying green** for headings and the mark;
- **land's buff** for ids;
- **chart magenta** for *what is owed to the Owner, and nothing else*;
- teal for done, its own amber for a warning (`#7d5000`, `#f1c26a`; 6.7:1 and 10.9:1), coral for a failure, and the
  chart's blue for help (`#1f5ca8`, `#8fb9f3`; 6.4:1 and 9.0:1): violet would sit beside the chart's magenta, which means
  *owed*. Its band and tints are its own, under the same contrast check.

Inside the box it carries magenta for the owed count, amber for a warning, coral for a failure, teal for done and its
blue for help: one colour more than `monochrome`'s budget, which a landing palette can carry and a board named
`shoalmark` takes with it. The nautical chart and the claim's band belong to the landing's first screen and the docs
pages: a board named `shoalmark` takes its colours, never its chrome. No board rule depends on this palette.
