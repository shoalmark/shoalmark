# FM-024 — the Reviewer's code pass on `fm/024-the-seats-switch` at 87e2e1b, phase 1: D2, the Owner configured outside `[seats]`

Verdict: **READY WITH FINDINGS** — seven P3 (RV-2200 … RV-2206), no P2. D2 is built as ruled. The configuration reads as ruled, and no way around it was found. This repository and the four adopters' configurations on this machine read exactly as before, and the tests bite. The findings are lines that still put the Owner, when named at the top, under `[seats]` or call them a seat, the upgrade note, two messages, `--schema`'s seats row, and one reader defect older than this change. Every fix below was tried on a scratch copy of this tip. There the blocks it touches pass (116 ok, 1 skipped for want of this repository's history), test_core.py passes (158), and beside this tip's tool the new and moved checks fail (6).
Reviewed: 87e2e1be6d9024b40e4f06738b357e16a7479f83, on origin/main ea70e5e, which is its merge base.
Reviewer: b3bdb000/reviewer-78 (claude-opus-5-5, max), `reviewer@seat` unsigned, worktree shoalmark-review-11, 08:58–09:52 CEST on 2026-10-01. Independence: the same session as the build (b3bdb000/implementer-77), so not independent.
Tier: code. `git diff --name-only origin/main...HEAD` lists shoalmark.py, test_shoalmark.py, shoalmark.toml, README.md, CHANGELOG.md, docs/setup.md, docs/signing.md, docs/triage.md, their three German twins, and FM-024.
Read: the Owner's ruling filed in FM-024, *The `[seats]` switch — v0.19.0* (D2 with its tests; this branch owns every line about how the Owner is configured), and FM-006's *What a stranger meets first*, D (D1's phrase, D2, the fallback line), as filed on `fm/006-what-a-stranger-meets-first`. Also AGENTS.md, and `git diff b269cdc 87e2e1b` whole: implementer-77's ca8f7f4 (the tool, 14 checks), 321fddc (the texts and this repository's `shoalmark.toml`) and 87e2e1b (FM-024).

## Findings
- **RV-2200 · P3 · Six lines the tool prints still put the Owner named at the top under `[seats]`, or call them a seat.** ca8f7f4 moved the lines that point at where the Owner's signature is asked, but these were missed. Each was run on this tip with `owner` at the top:
  - (a) `configure` (shoalmark.py:233–235). With `owner = ["you@example.org signed", "you@example.org"]` it prints *`[seats]` — `you@example.org` is listed twice under `owner`*. With `owner = "planner@seat"` beside `[seats] planner = "planner@seat"` it prints *`[seats]` — `planner@seat` is listed under two seats, `owner` and `planner`*. Both refusals are right (exit 1, one line). But they name a table the line is not in, and the second calls the Owner a seat.
  - (b) Subversion (:6602–6604). `owner = "holgo signed"` at the top of a working copy prints *`[seats]` — owner asks for a signature, and Subversion has none to give …*. It misleads: the reader looks under `[seats]` and finds no `owner` there. Its way through, *name the SVN account alone*, is right.
  - (c) The Owner's own commands (`owner_change`, :2154). With the Owner at the top and no `user.signingkey`, `--answer` prints *`[seats]` asks for a signed answer and no `user.signingkey` is set*. `--done`, `--due` and `--revoke` share the line, and it is the first line an Owner meets on a new machine.
  - (d) `answerers_problems` (:4555–4558). With `owner = "alice"` at the top and `answerers = ["alice signed"]`, it prints *… — the seat that answers for it — is not signed. `[seats]` alone decides who may answer (from 0.17.1) … Add `signed` to the seat (`owner = "alice signed"`)*. The D2 check at test_shoalmark.py:946 pins *Add `signed` to the seat*.
  - (e) The `answerers` notes (:6611–6612, :6616–6618). With only a top-level `owner`, the first says *`[seats]` decides who may answer*. To a repository wholly on `answerers`, the second says *move it into `[seats]` and `[rights]`*, which is the old spelling for the Owner.
  - (f) `--done`'s help (:6787) says *signed where their seat is `signed`*.
  - (g) Two FM-037 check names did not move with their pins. test_shoalmark.py:5603 still says *the default branch's `[seats]`*, and :5611 still says *the Owner's seat*.
  - **Fix:**
    - (a) Before the check at :233, add:

      ```python
                  if who and who in seen and at_top(seen[who]):   # the Owner named at the top is no seat and no line of `[seats]` (FM-024, D2)
                      raise SystemExit(f"{CONFIG_NAME}: " + (f"`owner` lists `{who}` twice" if seen[who] == name else f"`{who}` is the Owner's (`owner`, at the top) and the seat `{name}`'s (`[seats]`)")
                                       + "; an identity is the Owner's or one seat's, listed once")
      ```

      The `[seats]` messages and their pins (:751–756, :840) stay.
    - (b) At :6603: `` problems.append(f'{CONFIG_NAME}: {", ".join("`owner`" if at_top(s) else f"`[seats] {s}`" for s in sorted(s for s in SEATS if any(mode == "signed" for _who, mode in SEATS[s])))} asks for a signature, and ' ``. The next line stays.
    - (c) At :2154: `` `{("owner" if at_top(seat) else "[seats]") if SEATS else "answerers"}` asks for a signed {noun} … ``.
    - (d) At :4555–4558:
      - `` advice = f'Add `signed` to {"`owner`" if at_top(s) else "the seat"} (`{s} = "{who} signed"`)' if … ``.
      - The middle clause becomes `` (("the Owner, who answers for it" if at_top(s) else "the seat that answers for it") if same else ("the Owner, who holds `answer`" if at_top(s) else "a seat holding `answer`") + f"; no seat is spelled `{name}`, so each stands in for it") ``.
      - The sentence after it starts with `` {"`owner` and `[seats]` alone decide" if CONFIG.get("owner") is not None else "`[seats]` alone decides"} who may answer (from 0.17.1) ``.
      - The pin at test_shoalmark.py:946 moves with the line: *Add `signed` to `owner` (`owner = \"alice signed\"`), or remove `answerers`*, plus *`owner` and `[seats]` alone decide who may answer* and *the Owner, who answers for it*.
    - (e) At :6611: `` … not read for answers — {"`owner` and `[seats]` decide" if CONFIG.get("owner") is not None else "`[seats]` decides"} who may answer … ``. At :6616: `` … and still works — name the Owner at the top instead (`owner = "<email> signed"`, before any table), and give any other name that answers `answer` in `[rights]`. `` The rest of that note, the anchoring to 0.17.3, stays. Every pin on these notes still holds.
    - (f) At :6787: *signed where their `owner` is `signed`*.
    - (g) :5603 reads *… from the default branch's configuration, never the branch's: …*, and :5611 begins *FM-037 · clause 5 · with the Owner's `owner` not `signed`, …*.
    - Checks to add:
      - At the end of the D2 block: the top-level list that repeats an identity, the Owner's identity under a seat, and both notes, each naming `owner` and never `[seats]`. Then RV-2204's tag clause. Then `--answer` with the Owner at the top and no signing key, which must say *`owner` asks for a signed answer*.
      - In S4: `owner = "holgo signed"` at the top is refused as *shoalmark.toml: `owner` asks for a signature, and Subversion has none to give*.
  - Tried: the three checks pass on the scratch copy. Beside this tip's tool all three fail, and so does the moved pin. Under the old spelling the messages read as before: the FM-008 seats, FM-015 and who-may-answer blocks pass unchanged.
- **RV-2201 · P3 · The pages keep stale second copies of how the Owner is configured.** 321fddc rewrote the setup, signing and triage lines. These copies of the same facts were left:
  - README.md:170 (the refusal table) reads *`answerers = ["x signed"]` asks for a signed answer, and `[seats] …` … is not signed* | *add `signed` to that seat, or remove `answerers` — with `[seats]` it is not read for answers*. **Fix:** *… and `owner = …` (or `[seats] …`) … is not signed* | *add `signed` to that line, or remove `answerers` — with `owner` or `[seats]` it is not read for answers*.
  - README.md:200 reads *the author the seat holding `answer` in the **default branch's** configuration*. **Fix:** *the author the Owner — or a seat `[rights]` gives `answer` — in the **default branch's** configuration*.
  - docs/triage.md:121–122 reads *the author the seat that holds `answer` in the default branch's configuration*. **Fix:** *the author you, as `owner` in the default branch's configuration names you*.
  - docs/de/triage.md:150 reads *als Autor der Sitz, der in der Konfiguration des Standard-Branchs das Recht `answer` hält*. **Fix:** *als Autor Sie, wie `owner` in der Konfiguration des Standard-Branchs Sie nennt*.
  - README.md:217 reads *Where their seat is not `signed`*. **Fix:** *Where their `owner` is not `signed`*, as docs/signing.md:241 now says.
  - README.md:274 reads *signed where their seat is `signed`*. **Fix:** *signed where their `owner` is `signed`*.
  - README.md:318 says an `owner` key is refused *inside any other table*. At this tip `[rights] owner = ["answer"]` is read as the Owner's rights, and the D2 check 5 pins it. **Fix:** *… inside any other table (in `[rights]`, a list of rights is the Owner's own), which is where …*.
  - README.md:329, the toml example's comment, reads `# only for a name that is not one of the four`. The sentence that named the four (*Four names carry theirs built in*) is gone, so *the four* now reads as the paragraph's *Four rights*. **Fix:** `# only for a name of your own — not owner, planner, reviewer or builder`.
  - docs/index.md:21 reads *once your seat is marked `signed`, as [the set-up page](setup.md) does it*. **Fix:** *once your `owner` line is marked `signed`, as [the set-up page](setup.md) writes it*.
  - docs/de/index.md:16–17 reads *sobald Ihr Sitz als `signed` markiert ist*. **Fix:** *sobald Ihre `owner`-Zeile als `signed` markiert ist*.
  - The two index pages are the landing's Markdown twins, and FM-006's slice owns the landing. Its branch leaves these two lines as they are, and the edit merges clean with `fm/006-what-a-stranger-meets-first` (`git merge-tree`, tried). The Planner says whose lines they are.
  - Tried: every change applied on the scratch copy. No check pins these lines.
- **RV-2202 · P3 · The CHANGELOG's upgrade note leaves out what an older tool does with the new line, and gives no way through.**
  - Falsifiers, each run on this tip:
    - b269cdc's tool reads `owner = "me@x signed"` at the top, beside `[seats] planner`, as no Owner: `may_answer()` and `owners_of` are both `{}`. There the Owner's committed answer fails b269cdc's `--check` (exit 4, *an answer, but no seat in `[seats]` holds the `answer` right*), and so does their close (*`me@x` is not a seat*); this tip's passes both (exit 0).
    - In a scratch repository, `origin/main` names the Owner at the top. A seat's branch running b269cdc's tool changes TRIAGE.md's intent. Its `--check` says *not guarded — origin/main's `[seats]` gives no seat `answer`* and refuses nothing: it exits 3, on INDEX.md alone, which a newer tool wrote. The same branch, read by this tip's tool, is refused (exit 4).
    - A top-level `owner` with no `[seats]` turns the seats gate on, and `answerers` is no longer read. Beside `answerers = ["someone"]`, `owner = "me@x"` makes `may_answer()` `{me@x}`; b269cdc reads `{someone}`.
    - The note says only *a top-level `owner` that older tools ignored now names the Owner*.
  - This repository: five branches are open besides this one (`fm/006-the-go-to-market-screen-of-the-first-screen-proposal`, `fm/006-what-a-stranger-meets-first`, `fm/024-a-report-opens-with-from`, `fm/024-the-go-to-market-screen-of-the-seats`, `release/v0.19.0`). After this merge, each one's `--check` and hook read main's Owner as nobody until it merges main. `--queue` on main still reads the Owner.
  - **Fix:** CHANGELOG.md:9–12 reads:

    ```markdown
    - **The Owner is configured outside `[seats]` (FM-024).** A top-level `owner = "you@example.org signed"`, before any table, names the Owner,
      who is not a seat and holds all four rights; `[seats] owner` still reads, as its old spelling. *On upgrade:* both present and different, or an
      `owner` key inside any other table (a list of rights under `[rights]` aside), is refused at configuration in one line (exit 1); a top-level
      `owner` that older tools ignored now names the Owner — and where there is no `[seats]`, it turns the seats gate on and `answerers` is no longer
      read. A tool older than this one ignores the top-level line: there the Owner is nobody — their answers are refused, and the TRIAGE.md guard of a
      branch that runs it reads no Owner on a default branch that names them only at the top. While any copy older than this one reads the
      repository, keep `[seats] owner` beside the new line, the same: this version reads the two once. The refusal that lists the seats names the
      Owner apart; `--schema`, the README and the setup pages say so.
    ```

    And one line in FM-024's *What is true now*: *Branches open at the merge run their own older copy: until each merges main, its `--check` and hook read main's top-level `owner` as no Owner (not guarded); `--queue` on main still reads the Owner.* Keeping this repository's `[seats] owner` beside the top-level line until then is the other way, and it is the Planner's call.
  - Tried: the bullet on the scratch copy. Every claim in it is one of the runs above.
- **RV-2203 · P3 · The guard reads a default branch whose configuration this tool refuses as one that names no Owner.**
  - Falsifier: in a scratch repository, `origin/main` names the Owner twice, differently (`owner = "other@x signed"` at the top, `[seats] owner = "h@x signed"`). A seat's branch fixes its own copy and changes the intent. `--check` exits 0, and says *the Owner's two sections: not guarded — origin/main's configuration names no Owner: name them (`owner = "<email> signed"`, before any table)*. That configuration names an Owner twice, so the advice is wrong. b269cdc's tool reads its `[seats] owner` and guards.
  - D2's two new refusals (named twice; `owner` inside another table) make such a default branch reachable. A configuration an older tool took, such as a stray top-level `owner` or a tag named `owner`, is refused by this one while the branch that vendors it has fixed only its own copy. Staying unguarded is the Builder's choice (check 4: *rather than guess*), and that is how a malformed configuration has always been read. But the line must say why.
  - Cause: `owners_at` (:5814–5817) turns every refusal into `{}`, and `triage_guard` (:5964–5965) reads `{}` as *names no Owner*.
  - **Fix:**
    - `def owners_at(rev, refused=None):`, with this added to the docstring: *Where this tool refuses that configuration, nobody — and the refusal is appended to `refused`, so the caller says so rather than that it names no Owner (FM-024, D2).*
    - The handler becomes `except SystemExit as e:` + `if refused is not None: refused.append(str(e))` + `return {}`.
    - In `triage_guard`: `why = []`, then `owners = owners_at(trunk, why)`, then `` _GUARD = ([], f"the Owner's two sections: not guarded — " + (f"{trunk}'s configuration is refused here, so it names nobody — {why[0]}" if why else f"{trunk}'s configuration names no Owner: name them (`owner = \"<email> signed\"`, before any table)")) ``.
    - Add to FM-037's block, after the no-Owner check (:5603–5605): main named twice, differently; a seat's branch that fixes its own copy and changes the intent; and the line starting *not guarded — origin/main's configuration is refused here, so it names nobody — shoalmark.toml: the Owner is named twice, and differently*.
  - Tried: the check passes on the scratch copy and fails beside this tip's tool. The no-Owner line is unchanged.
- **RV-2204 · P3 · A tag named `owner` is refused with a way through that fits only a misplaced Owner line.**
  - The judgement asked for: the refusal is the ruling's (*an `owner` key inside an unrelated table is refused*). It also catches the likeliest slip: `[tags]` is the last table `--init` writes, so a line appended at the end of the file lands there.
  - Against adopters' files: the four configurations on this machine carry no tag named `owner` and no top-level `owner`. Each reads the same under b269cdc's tool and this tip's: the seats, the rights, who may answer and the tags. The refusal costs no known adopter, so it stays.
  - The defect: for a real tag of that name, the only way through offered is *put it at the top of the file, before any table: `owner = "<identity> signed"`*. That turns the tag's description into the Owner. Beside `[seats] owner` it is then refused as named twice. With no `[seats]`, it switches the seats gate on and makes the description the Owner.
  - **Fix:** in `seats_of` (:4483–4484), after the way through, add `` + ("; if it is a tag, give it another name: `owner` names the Owner" if "tags" in where else "") ``. The D2 check 5's pins still hold, and RV-2200's new check asserts the clause.
  - Tried: as RV-2200.
- **RV-2205 · P3 · `--schema`: the `[seats] <seat>` row closes on the former names, not on D1's phrase, and the `owner` entry says every other table refuses `owner`.**
  - (a) The row (:4151) carries D1's phrase word for word, the seat names in code marks as the first-screen slice's seats page writes them. It then goes on: *`principal` and `implementer`, their former names, still read and hold the same*. The row does not say whose former names these are (the planner's and the builder's), and it ends on them instead of on the seats' rights.
  - (b) The `owner` entry (:4142) says *and so is an `owner` key inside any other table*, but `[rights]` reads a list of rights there as the Owner's own.
  - **Fix:**
    - (a) :4151 becomes `` "`principal` and `implementer`, the former names of `planner` and `builder`, still read and hold the same. " `` + `` "The tool knows the Owner, and three seats with their rights built in — `planner` ask · close · triage, `reviewer` triage, `builder` none" ``.
    - (a) The D2 check's pin at :950 moves with it: the new clause is in the row, and the row's text ends with D1's phrase (`` t.split("| `[seats] <seat>` |")[1].split("\n")[0].rstrip(" |").endswith(…) ``).
    - (b) :4142 reads *… and so is an `owner` key inside any other table, naming this place (in `[rights]`, a list of rights is the Owner's own) — a key after a `[table]` header belongs to that table*.
  - Tried: the row ends *… `builder` none |*. The slice-2 `--schema` check (:841–842) still passes.
- **RV-2206 · P3 · Found on the way, older than this change: `read_config` keeps the last of two lines with one key, and a key followed by a table of its name stops in a traceback.**
  - `owner = "a@x"` then `owner = "b@x"` at the top reads `b@x`, without a word, and the same pair under `[seats]` reads the same way. Yet the two spellings, different, are refused, and TOML refuses a key set twice.
  - `owner = "me@x"` with an `[owner]` table below stops every run in `TypeError: 'str' object does not support item assignment` (`read_config`, :132–142). b269cdc does the same for any name, such as `name = …` with `[name]`.
  - None of the five configurations here sets a key twice.
  - **Fix**, by AGENTS.md rule 6 one line in FM-024's body, not a side-fix here: *Found on the way (RV-2206): `read_config` keeps the last of two lines that set one key — `owner` twice at the top, or under `[seats]`, names the later without a word, where the two spellings, different, are refused — and a key with a table of its own name below stops in a traceback; 0.19.1 or later: refuse both at the line, as TOML does.*

## What holds
1. **The configuration as ruled.** 25 configurations went through `--check` (exit code, stderr) and `configure` (seats, the Owner's rights, `may_answer()`, `owners_of`), on scratch repositories with this tip's tool:
   - The top-level `owner` alone and `[seats] owner` alone read the same: one identity, `signed`, all four rights, who may answer, and `owners_of`.
   - A list reads `signed` per identity. With no `[seats]`, the Owner alone turns the gate on.
   - Both present and the same are read once, a string against a one-item list included.
   - Both present and different are refused at configuration, exit 1, one line, naming both and the way through. That includes the same identity with `signed` on one only, and the same list in another order (order is read by `seat_mode`).
   - An `owner` key is refused in `[tags]`, `[paths]`, `[ratio]`, `[kinds]`, `[headings]`, `[considered_from]`, an unknown table, and as a string under `[rights]`. A table `[owner]`, `owner = true` and `owner = 7` are refused.
   - `[rights] owner = [<rights>]` still redefines the Owner's rights, as it did under `[seats]`. The ruling's test, *the Owner keeps all four rights*, is the move losing none, and that holds (check 6, through the gate).
   - `answerers` reads as before wherever the Owner is not named at the top.
   - The refusal at the old `:4520` (now :4563) lists the seats and names the Owner apart, under either spelling, and leaves out the badge line on Subversion.
   - FM-006's fallback line is absent, as it should be now that D2 is built.
2. **Ways around it, refused or read as before.**
   - An `owner` written after `[seats]` when `[seats]` is the last table is the old spelling, and names the Owner.
   - A list that repeats an identity, and an identity both the Owner's and a seat's, are refused (wording: RV-2200 a).
   - `owner = ""` or `[]` turns the gate on with nobody, as `[seats] owner = ""` did.
3. **The Owner's commands and the queue, under the new spelling.** The suite's answer, act, queue and guard blocks were run with every `shoalmark.toml` they write rewritten to name the Owner at the top (a shim on the suite's own writer; 25 and 28 writes moved): test_shoalmark.py 2805–3521, 3827–3932, 4118–5115, 5160–5196, 5464–5935 and 6004–6291. That covers `--answer` with its revoke and supersede, `--done`, `--due`, `--revoke`, `--clear-ask`, *merge: your answer* and the waits beside it, `--queue`'s TRIAGE.md reading, the guard, and the merges. The outcome is the plain run's, check for check, except four checks that pin the old wording (`[seats] owner = "alice"`, *`[seats]` asks this seat*). Those pass with `owner` in their place.
4. **The default branch's Owner, spelled differently.** With this tip's tool:
   - Trunk on `[seats] owner`, branch moved to the top: a seat's change to the intent is refused, and the Owner's signed change passes.
   - The reverse holds too.
   - A branch that makes a seat the Owner, in either spelling, is still judged by the trunk's Owner and refused.
   - Older tools and refused trunks: RV-2202 and RV-2203.
5. **Subversion.** With `owner = "holgo"` at the top:
   - An ask committed by an account that is no seat is refused, with *The Owner, who is not a seat, is holgo* and no badge line.
   - The Owner's answer, committed by the account `holgo`, passes under both spellings (exit 0), and the same answer committed by `principal` is refused.
   - `signed` is refused (wording: RV-2200 b).
6. **This repository after the move.**
   - `--check`, `--session-check` and `--owner` exit 0 in this worktree. The guard reads origin/main's `[seats] owner` and guards.
   - In a scratch clone at this tip, b269cdc's tool with b269cdc's `shoalmark.toml` against this tip's pair: `--owner` is byte-identical, and `--check` is identical. Both exit 4 there, on the clone's own unset `gpg.ssh.allowedSignersFile`.
   - Read in process, both pairs give identical seats, rights, `holds`, `may_answer()`, `answerers` and `owners_of`: the Owner `holgoijo@gmail.com`, `signed`, with all four rights, and every seat's rights as before.
7. **Upgrade.** The four adopters' configurations on this machine, one of them on `[seats] owner`, read the same under both tools. The note: RV-2202.
8. **The texts.** Read at this tree, in English and German: the README rows and §*Seats*, setup (`docs/setup.md:53`, the line the ruling names), signing and triage, the CHANGELOG, this repository's toml and its comment, `--schema` and `--help`. They are true apart from RV-2200, RV-2201, RV-2202 and RV-2205.
   - The German reads natively.
   - README §*Seats*'s rights sentence is true now: the tool knows `planner`, `reviewer` and `builder` built in, and reads `principal` and `implementer` as their old spellings.
   - Phase 2 must change:
     - README:318, *this repository's `[seats]` keeps the keys `principal` and `implementer` until the key rename …*;
     - the badge lines with `principal@seat` (README:332, :369);
     - `docs/setup.md`'s example keys (:50–51), its `user.email implementer@seat` (:58) and *keep their names until the key rename* (:60), with the German twins at :51–52, :59 and :60;
     - this repository's `[seats]` keys and its comment.
   - The rights sentence and `--schema`'s seats row stay true after the rename while the old spellings read.
9. **The tests bite.**
   - Beside b269cdc's tool, 12 of the 14 D2 checks fail. The two that pass are *1 of 7, the old spelling alone* and *3 of 7, both the same*, and both guard the old spelling.
   - At this tip all 14 pass, on Python 3.14 and on 3.9.6 with the 18 identity checks (32).
   - The two edited pins are right. They pin the moved lines whole: `GUARD_AUTHOR_ONLY`'s *mark `owner` signed* holds under either spelling, and the not-guarded line holds. Beside b269cdc's tool exactly those two of the FM-037 block fail, while 19 pass and 1 is skipped.
10. **FM-024** says what is built and what is left, and leaves `next: build` as it was. No ship-log row is due before it ships.

## Controls, one line each
- Setup, 08:58:36: `git status --short` empty. One fetch. Detached at 87e2e1b, which equals `ls-remote`. `--whoami`: `To: b3bdb000/reviewer-78 reviewer (shoalmark-review-11) · claude-opus-5-5 · max`.
- The configuration and seat blocks at the tip, in this worktree, ended 09:08:55: test_shoalmark.py 1–108, 192–209, 540–969, 2805–3173, 3522–3597 (W, S1–S4), 3696–3702 and 5464–5704 (FM-037, with the real history). 128 ok, 0 failed.
- test_core.py at the tip, ended 09:09:10: 158 ok, all green, exit 0.
- The D2 block beside b269cdc's tool, ended 09:09:45: 2 ok, 12 failed.
- The identity and D2 blocks on Python 3.9.6, ended 09:12:01: 32 ok.
- The configuration matrix, ended 09:13:01; the same matrix beside b269cdc's tool for the upgrade side.
- `--check` (exit 0, 09:17:23), `--session-check` (exit 0) and `--owner` (exit 0, 09:17:32) in this worktree.
- Before and after the move in a scratch clone, ended 09:18:15, and in process, 09:18:31: identical.
- Subversion, ended 09:19:25, plus the principal's answer as a control: refused.
- The mutation, round 1, ended 09:20:26: plain 164 ok, mutated 160 ok. Both fail FM-029's real-history check, which an archive has no history for, and the mutated run also fails the four wording pins. Three blocks were cut short by helpers that were not loaded.
- The mutation, round 2, with those helpers, ended 09:28:36: 145 ok, both runs, 1 skipped each. Identical check for check.
- The guard with the trunk and branch spelled differently, older tools and a refused trunk, ended 09:22:33.
- The FM-037 block beside b269cdc's tool, ended 09:37:46: 19 ok, 2 failed (the edited pins), 1 skipped.
- The adopters' configurations under both tools, 09:43:19: identical, all four.
- The Owner's answer and close with the Owner at the top, 09:49:19 and 09:49:59: b269cdc's `--check` exits 4 on each, and this tip's exits 0.
- The fixes on a scratch copy of the tip:
  - The touched blocks, ended 09:41:49: 116 ok, 0 failed, 1 skipped.
  - FM-037 again after the check names moved, ended 09:45:43: 22 ok.
  - test_core.py, 09:42:07: 158 ok.
  - On 3.9.6, 09:42:29: 34 ok.
  - Beside this tip's tool, ended 09:41:45: 6 failed, the four new checks and the two moved pins.
  - It merges clean with `fm/006-what-a-stranger-meets-first`, as this tip does.
- This worktree stays clean throughout. Every scratch repository is in this session's scratch directory.

Quality read: the change is placed and built well. `seats_of` is one reader for `configure` and the default branch's Owner. The refusals are one line each, exit 1, with the way through. The guard reads the new spelling where the trunk carries it. The checks run the CLI, the configuration and the gate itself, and they bite. Its quality defect is that the wording for an Owner at the top is decided message by message, with an inline `at_top` in five places. That is how RV-2200's six lines were missed. RV-2203's `{}` for a refused configuration is the same shortcut, and it hides the reason. The rest reads clean.
Four numbers for this verdict: records +179, product +0, records deletions 0, product deletions 0.
Next: the Builder fixes RV-2200 … RV-2205 on this branch and writes RV-2206's line in FM-024. The Reviewer verifies at code tier. Then come phase 2, the full local run before the pull request is marked ready, and the Owner's cold session.
