To: 8b77530d gtm (shoalmark-go-to-market-2) · claude-fable-5-1 · xhigh

# Go-to-market screen — the first-screen proposal for v0.19.0 (2026-09-30)

**Read:** main `e5e7197`; the wording branch `fm/006-they-them-and-english-seat-names` @ `c6678a8` (the proposal read `131d5c3`, five commits
behind it: PR 141 merged, so README §*Seats*, the seats page and the tool already say `planner`/`builder`); the proposal itself; the live site
and `llms.txt` (both 200, 2026-09-30 20:00 UTC); the earlier screen `a410aef` — read only after the findings below were written; it screened the seat names and the App lines, not these texts.
**Method:** the brief's ladder L0–L5, knockout first; the first fatal gate is recorded and nothing more. F = form measurement, K = knowledge
anyone can reproduce, E = executed here. Lines marked *mine* are this seat's proposals and went through the same ladder. Nothing here selects.

## Ledger

| Item | Line | First fatal gate, or survives | Evidence |
|---|---|---|---|
| A1 | *The agents keep the work; the person keeps the word.* — H1 `:314`, `<title>` `:11`, `docs/index.md:12` | survives | F 52 chars; E only a signed answer counts where `[seats]` marks the Owner `signed` (README:317) |
| A1 control | *Get a better-performing human Owner.* as H1, title and `zensical.toml:6` | L3 — the Owner, reading first, is the one who underperforms | K; agrees with ruling 1 |
| A1 | `site_description` *…the word. A work tracker that puts what needs the Owner first.* | survives | F 105 chars, a description not a lead |
| A2 DE-a | *Die Agenten tragen die Arbeit, der Mensch hat das letzte Wort.* | survives | F 62 chars, two over "about 60"; K *das letzte Wort haben* = the final say |
| A2 DE-b | *Die Arbeit machen die Agenten. Das Wort hat der Mensch.* | L1 — *das Wort haben* means to have the floor, the speaker of the moment, not the say | K |
| A2 DE-c | *Die Agenten behalten die Arbeit, der Mensch behält das Wort.* | L1 — *das Wort behalten* carries no sense of the say; *die Arbeit behalten* reads as keeping one's job | K; the proposal was right |
| A2 control | *Dein Eigner bremst. Tunen statt tauschen.* on `docs/de/index.md`, at `:7` or over *An die Flotte* | L3 — on the human start page the Owner is the brake, to be tuned or swapped | K |
| A3 control | *Your agents ask mid-flight, and you stamp what you had no time to read.* `:382` | survives | F 71; K the cause is named first, the stamp is its consequence |
| A3 OC-1 | *Your agents' questions reach you once a day, each with what it takes to answer.* | survives | F 79; E `--standup` is the one sitting, an ask carries options and a proposal (README:266, :271) |
| A3 control DE | *Ihre Agenten fragen mitten im Lauf, und Sie nicken ab, …* `docs/de/index.md:12` | survives | F 91; Sie |
| A3 mine | *Die Fragen Ihrer Agenten erreichen Sie einmal am Tag, jede mit dem, was es zur Antwort braucht.* (OC-1 in German; the proposal gives none) | survives | F 97; Sie |
| B1 | *Get a better-performing human Owner.* as the README's opening heading | survives L3 narrowly — the agent is addressed and `:9` puts the root on the process | K |
| B1 control | *How to get a better-performing human owner* `README.md:3` | L5 — lowercase *owner* against *Owner* everywhere else (`:6`) | K |
| B2 | the `llms.txt` summary (`scripts/llms_txt.py:20`) opening with the tagline | survives | E live `llms.txt` 200; K agents read it |
| B3 | the English tagline atop `ADOPT.de.md` | L1 — an English slogan's tone over a German note that calls itself *eine Einladung zu einer Messung, keine Anweisung* (`:3–4`) | K |
| B3 | `:5` *…und **euer Owner entscheidet*** | survives | K |
| B3 control | `:5` *…und **er entscheidet*** | L3 — gendered | K |
| B3 mine | *Euer Owner bremst. Tunen statt tauschen.* atop `ADOPT.de.md`, in the note's own address and name | survives as far as B1 does — the same L3 edge | F 40; K ihr-form, the note's *Owner* |
| C def | *A seat is a role an agent takes, with explicit responsibilities and permissions.* | L5 — the product's word is *rights* (README:313, seats page `:4`) | K |
| C Planner | *…turns the Owner's direction into briefs …* | L5 — *briefs*: the tracker is canonical (AGENTS.md:9, README:54); the seats page's builder *takes a tracker* | K |
| C Builder | *…builds one change from its brief …* | L5 — as above | K |
| C Reviewer | *…reads a branch against its brief …* | L5 — as above | K |
| C Specialists | *Specialists: called in when the work needs them.* | survives | F 48; E the word is on no tree today (`git grep`, 0 hits) — it lands only with D1 |
| C mine | *A seat is a role an agent takes, with its duties and its rights written down.* · Planner *…into trackers, and puts the agents' open questions to the Owner, one sentence each.* · Builder *…from its tracker, in a worktree of its own, and never accepts its own work.* · Reviewer *…against its tracker and writes READY, or what must change. It never merges.* | survive | F 74/109/95/92; E one sentence per ask is the gate's rule (README:266) |
| D1 | *the Owner and three seats with built-in rights — planner, reviewer, builder* | L2 — `builder` holds no right (`BUILTIN_RIGHTS`, `shoalmark.py:189` @ `c6678a8`; README:316 *builder none*) | E |
| D1 control | seats page `:3–4`, README `:315–316` *Four names carry theirs built in — owner …* | L5 — *the Owner, who is not a seat* (`:3`), then `owner` among the four names the tool knows (`:4`) | K; agrees with ruling 2 |
| D1 mine | *the Owner, and three seats with their rights built in — planner ask · close · triage, reviewer triage, builder none* | survives | F 104; E |

**Placement.** A1 on the landing, its title and the Markdown twin: does what ruling 4 intends. B1, B2: the tagline where agents read — yes.
B3: the note is where the Owner's agents read German, so the German claim belongs there, not the English line (F2). A2: moving the claim
down the human page keeps it on a human page (F2). C: the fleet on the agents' card of a human page is what ruling 3 and 5 intend; its link is F6.
D1: yes, with F5. The `docs/index.md` twin that `llms.txt` lists *For the Owner* carries the human lead — consistent with ruling 1.

## Findings, most severe first

1. **P1 · C, all four lines · L5.** *brief(s)* and *permissions* are not the product's words: the landing, README and seats page say *tracker* and
   *rights*; a stranger meets *brief* nowhere else. Replacements in the ledger (*C mine*). 70 % — the App lines (`.claude/agents/builder.md`) do
   say *from the Planner's brief*, so the seats' own texts disagree with each other already; the stranger never reads those. — **new**; the earlier screen's Q5 accepts *briefs* as charter-anchored in the App lines: **contradicts** it for a stranger's page.
2. **P1 · A2 placement · L3.** The German claim dies anywhere on the human start page; its home is the German note for agents, where the English
   tagline dies at L1 (B3). Proposal (mine): `ADOPT.de.md` opens *Euer Owner bremst. Tunen statt tauschen.*; `docs/de/index.md` leads with DE-a and
   carries no claim. 65 % — ruling 1's reason (a 09-23 line, meant for agents) covers this line too, but the Owner ruled it for the English one. — **new**.
3. **P1 · A2 DE-b · L1.** *Das Wort hat der Mensch* says the human has the floor (*Sie haben das Wort*), not the last word. Off the list. 80 %. — **new**.
4. **P2 · D1 · L2.** *three seats with built-in rights — planner, reviewer, builder*: `builder` holds none at every tree. Say so, as README:316 does. 90 %. — **new**.
5. **P2 · D1 against D2's fallback · L5.** If D2 slips to 0.19.1, *the Owner is not a seat* stands over `[seats] owner = …`, which `docs/setup.md:53`
   tells the adopter to write, and the tool's refusal (`shoalmark.py:4520` @ `c6678a8`) still lists the Owner under *The seats are:*. One line for
   the fallback: *the Owner, whose identity `[seats]` still carries as `owner` until 0.19.1*. 75 %. — **new**; its Q4 marks the key rename a transition, not this.
6. **P2 · C, "All seats →" links `/seats/` · placement.** Root-relative, that is `shoalmark.github.io/seats/` — 404 (E 20:05:55 UTC); the project site
   lives under `/shoalmark/` and `use_directory_urls = false` (`zensical.toml:13`). Write it as the landing's other links do:
   `https://shoalmark.github.io/shoalmark/seats/index.html` — 404 today too, the site builds at the tag. 60 % that `/seats/` is meant literally. — **new**.
7. **P2 · E's public count.** The landing carries six gendered pronouns, not four: `:411` one *his*, `:463` *he* and four *his* (E, `grep -w`). 95 %. — **agrees with** its T5 on `:411`/`:463`; the count against the proposal is new.
8. **P2 · A3 OC-1, if picked.** The card's second sentence (`:382`) already says *puts them to you once a day*; OC-1 says it again. Change both or
   neither; the control names the pain OC-1 drops (*mid-flight*, the root README:9 names). 85 %. — **new**.
9. **P3 · B1–B3 · L3 edge.** The tagline survives only where the agent is addressed, yet the landing hands the README to the Owner as *the contract,
   rendered here* (`:449`). The Owner reads that they underperform anyway; ruling 1 accepts this, the record should say so. 60 %. — **new**.
10. **P3 · A1 form.** Under the claim line (`:313` *…keeps the fleet in the channel.*) the H1 makes three *keep*s in two lines; *keeps the word*
    reads first as a promise kept, the say arrives by the parallel. `<title>` with the site's prefix is 64 chars. The page's own `<meta
    name="description">` (`:12`) is untouched while `site_description` changes: two descriptions of one page. 50 %. — **new**.
11. **P3 · L5 in German.** The Owner is *Eigner* on `docs/de/index.md` (7) and `de/setup.md` (2), *Owner* in `ADOPT.de.md` (10), both on `de/signing.md`
    and `de/triage.md` (E, word counts @ `e5e7197`). FM-006 records the Owner's word: *in German prose the person is der Eigner* (`:87`). 80 %. — **new**; its Q3 covers *Sie*, not the noun.

**Verdict.** Survivors — A1: the proposed line and description; A2: DE-a alone; A3: both openings, in both languages; B1, B2: the tagline, narrowly;
B3: the `:5` fix, not the English opening; C: *Specialists* as written, the other four only as reworded; D1: only as reworded. Three P1s before the build.
