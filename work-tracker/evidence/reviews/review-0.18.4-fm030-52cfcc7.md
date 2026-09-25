# 0.18.4's second build — FM-030's acts on the Owner's board (A–G), the inline pass on `52cfcc7`

**Verdict: NOT READY. Tier: code, full loop.** Reviewed `52cfcc778483760e4eaa6a0cbbf0c2f59bebbd59` on
`fm/030-the-acts-owed-to-him-on-his-board`: ten commits over `44f908b`, PR 74's merge. I am the Reviewer seat
`8e509911/reviewer-8`, working in `shoalmark-review-4` detached at the tip. I read the Implementer's brief first. Its
items A–G are the claims, sourced from his signed path line 6, FM-030's two `## Raised` lines and ship-log rows, his
word at 13:33:29 (*Better than only invites would be invites + notifications*), FM-036's body and FM-029's AU-29
line. Every item below was run, not read. The runs used a scratch clone of the tip and a scratch repository (a bare
origin, an ssh signing key, `[seats]` with a `signed` owner, an implementer and a principal, hooks from
`--install-hook`, the tool run as a command). I fixed nothing.

**Independence:** same session — 8e509911's own sub-agent, reported; the gate and hooks untouched, so not critical.

## The gate and the hooks

I mapped every hunk of `git diff origin/main...HEAD -- shoalmark.py` to its enclosing definition. None falls in
`commit_msg_check`, `install_hook`, `install_hook_svn`, `session_check`, the `--check` block of `main`, or
`judged_before_build`'s handling. `configure`'s hunk adds `ACTS_HEAD_RE` to its `global` line and compiles it.
`lefthook.yml` and `scripts/` are not in the diff. The one gate-side change is the one item A asks for. There are three
`FRONT_MATTER` keys, and `schema_problems` refuses a `due:` or `done:` that names no real time. The pass stays inline.

## What I ran, per item

- **A.** `--schema` prints `due:`, `window:` and `done:`, each with its shape, who writes it and what it means. The
  `done:` line says `--done` sets `next: build` where his answer left `next: owner`. In the scratch clone, I gave FM-036
  each of these `due:` values: `tomorrow`, `2026-09-26T07:30` (no zone), `2026-13-01T07:30+02:00`,
  `2026-09-26 07:30+02:00`, `…07:30Z+02:00`, lower-case `…t07:30z`, and a quoted time. Each one made `--check` exit 4
  with a `lint: FM-036: due: …` ledger line. `2026-09-26T07:30:00+02:00`, and `2026-09-26T05:30Z` with `window: 45`,
  passed after regeneration (exit 0). `window: soon` and `done: yesterday` exited 4. R5 covers `T24:00`.
- **B.** In the scratch clone I set three `due:` times. FM-036 was due 10 minutes ago, FM-029 two hours ago with
  `window: 30`, and FM-030 tomorrow. I regenerated the board and dumped it through headless Chrome. It showed *your
  acts, with their time: 6*, with the heading marked `hot`:
  - FM-007, FM-024 and FM-032 as *no date yet*, each with its promise. All three are accepted `ask-kind: action`, so
    they are acts by the rule.
  - FM-030 as *due …* and FM-036 as *overdue — due …*.
  - FM-029 as *missed — due …, and 30 minutes passed with no result*.
  - Each row with *done* · *reschedule*.

  INDEX.md's *Acts owed to the Owner — with their time* gives each time as written. In the scratch clone at the tip,
  `python3 shoalmark.py` twice left `git status` empty; only the ignored `index.html` and `view/` changed.
- **C.** In the scratch repository, `implementer@seat` and `principal@seat` ran `--done` and `--due`. Both exited 4,
  naming the seat and *the result / the time of the Owner's act is an `answer` change*. No branch was cut. As the owner,
  four inputs were refused before anything was cut: a tracker with no act, `tomorrow`, a time with no zone, and an empty
  *where*.

  `--done AP-420 "evidence/AP-420/read.md"` gave:
  - `answer/ap-420`, pushed; `%G?` is `G` as `holgoijo@x`.
  - `done: "<time+zone> · evidence/AP-420/read.md"`.
  - `next: build`. His answer had left `next: owner`, so the ruling holds on this path.
  - The record under a new `## Acts`; he is back on `main`.
  - `--check` 0 on the branch. A second `--done` is refused: *`done:` is written already*.

  `--due AP-421` twice, the second time on its branch, made two `G` commits. The records are `scheduled — due …`, then
  `rescheduled — was due …, now due …`, newest last, and `--check` is 0. From `main` with `answer/ap-421` unmerged,
  `--done` and `--due` name his two commits and `git switch answer/ap-421`, never `git branch -D`. See R1 and R3.
- **D.** `--invite AP-421` wrote `work-tracker/evidence/AP-421/AP-421-act.ics` and printed its path. The file has:
  - CRLF throughout, no line over 75 octets, and one fold.
  - `DTSTART:…Z`, `DURATION:PT60M`, and a `VALARM` with `ACTION:DISPLAY` and `TRIGGER:-PT30M`.
  - `SEQUENCE:2` after two records.

  A second run wrote the same bytes. `icalendar` parses it: start, end at start + 60 minutes, alarm at −30 minutes.

  `--notify` ran with a stub `osascript` first on `PATH` and `XDG_STATE_HOME` in scratch:
  - It posted 3: due in 20 minutes, overdue, missed. A later act was counted, not posted; a dateless and a done act were
    absent.
  - The second run printed *0 posted · 3 posted before*.
  - Every file in the repository, and `git status --ignored`, was identical before and after.
  - The memory is `$XDG_STATE_HOME/shoalmark/notified.json`, keyed on the repository. A moved `due:` posts again; a
    failing notifier gives *NOT posted* and is not remembered.

  One real notice went through `/usr/bin/osascript` (exit 0, *posted*). The AppleScript line compiles with `"` and `\`
  in its text (`osacompile`). The README's plist passes `plutil -lint`. Its cron line, run under `env -i` with
  `PATH=/usr/bin:/bin`, finds `/usr/bin/python3` 3.9.6 and posts. See R6.
- **E.** On the real corpus, `--standup` and `--owner` print *ACTS — yours, with their time* after the asks. FM-007
  reads *no date yet*, promised 2026-09-25 *after the scoring, once the key is delivered*; FM-024 and FM-032 follow.
  `--owner` leads with *NO QUESTION FOR THE OWNER · 3 ACT(S) OWED*. In the scratch repository, the order after *YOUR
  HANDS* is missed, overdue, due (soonest first), no date yet.
- **F.** In the scratch clone, I put today's FM-030 case on today's sheet: `keep P1 #3 build` above the real
  `keep P1 #1 build`. Three `--triage` runs each gave:
  - FM-030 at rank 1; FM-036 kept its #3, because a superseded row claims no rank.
  - *Superseded on this sheet by the later row … `keep P1 #3 build` — superseded … `keep P1 #1 build`*.
  - The earlier row left on the sheet, and the rule *ONE TRACKER, TWO ROWS* printed.

  Positive control: `origin/main`'s tool on the same sheet first set rank 3 and freed FM-036's #3. The next run set
  rank 1 and refused FM-036.
- **G.** In the scratch repository, the principal ran `--clear-ask AP-420 build`. The record gained
  `**signed** — 906b1bb · G` under `**relation** —`. `906b1bb` is the commit that wrote its `answer:` (`git log -S`).
  No tier is printed. The commit went through the hooks, `--check` is 0, and `--answered` reads *accepted with a
  change*.
- **The rest.** `test_shoalmark.py` gave 426 `ok` and `test_core.py` 148 `ok`, both `all green`, on Python 3.14.3 and on
  `/usr/bin/python3` 3.9.6; the Chrome checks ran. `--check` exited 0: *every build commit under a judged In Progress
  tracker*. That covers FM-030, FM-036 and G's FM-029, each In Progress and triaged 2026-09-25 at its parent.
  `--session-check` exited 0. `git diff origin/main...HEAD --stat` lists 11 paths, each named by a commit. The 14 new
  `acts.*` and `act.*` labels are in `examples/de/labels.yaml`, with matching placeholders. `[headings]` has `acts`,
  with `Handlungen` in the German example. The CHANGELOG's `## Unreleased — 0.18.4` has seven bullets naming FM-030,
  FM-036, FM-029, line 6 and his 13:33:29 word. `VERSION` reads 0.18.3.
- **The merge.** The branch was cut from PR 74's merge, not after PR 76 as the brief says. PR 75 and PR 76 changed
  tracker text only, and `git merge-tree` against `8b267b4` was clean (`633a54e`). During the pass, origin/main moved
  to `b336a53`, PR 78, FM-035's CI fix: R2.

## Findings

**R1 · P2 · confidence high — `--done` hands the move to the seat over an unanswered ask.** `done_cmd` sets
`next: build` wherever the tracker reads `next: owner` (`{"next": "build"} if t.get("next") == "owner"`). The ruling,
`--schema` and the README all limit that to where *his answer* left it. The state that breaks it is the designed one:
the seat writes `due:` "with the action ask", before any answer. I reproduced it in the scratch repository with
AP-426, a pending ruling (*Does the launcher ship before the site?*) with a scheduled read. `--done AP-426 …` committed
`next: build`, signed and pushed, with `ask:` still unanswered. On that branch, `--owner` and the board no longer list
the question, and `--check` exits 0. AP-425, an unanswered action ask, behaves the same way. A question he still owes
leaves his list unanswered: line 6's harm, done by the command meant to serve it. Fix: set `next: build` only where the
act is a promise — an accepted action answer is on the tracker (`act_of`'s `promised`, `act[1]`). Otherwise leave
`next:` as it is. Add a test: an unanswered ruling with a `due:`, where `--done` keeps `next: owner` and the question
stays in `--owner`.

**R2 · P2 · confidence high — the branch no longer merges into main, and its browser checks bypass FM-035's helper.**
`git merge-tree --write-tree origin/main HEAD` against `b336a53` exits 1. Two content conflicts:

- `CHANGELOG.md` — both sides open `## Unreleased — 0.18.4`.
- `work-tracker/INDEX.md`.

`test_shoalmark.py` merges without a conflict, but B's rendered-board check and C's `_owe` still call
`subprocess.run([_CHROME, …], timeout=60)` under `if _CHROME:`. FM-035 routes every headless run through
`_browser(key)` and `_chrome_run`. Without them, a hang kills the suite in a traceback again, and a Chrome that cannot
start is skipped silently instead of by name. C's `_owe` also presses OK onto the second screen with no
`navigator.clipboard` stub, and that screen copies the command at once. FM-035's CHANGELOG names this path as the
inferred macOS hang. `635ff31` says this third ruling waits for the CI fix, and the fix has now landed.

I measured the merge in a scratch clone and pushed nothing. I resolved `CHANGELOG.md` by keeping both lists under one
heading and `INDEX.md` by regeneration. `--check` then exits 0, and both suites are green on this Mac: 431 `ok` and
148 `ok`, with *skipped here: 0 checks*. That count cannot see the two FM-030 blocks, because they skip outside it.
Chrome runs here, so the hang is not reproduced; it is the CI path FM-035 was filed for.

Fix:

1. Merge `origin/main`, with both bullet lists under one `## Unreleased — 0.18.4`, and regenerate INDEX.md.
2. Put the two FM-030 blocks on `_browser("…")` and `_chrome_run(…)`, with the clipboard stub `_owe`'s page needs.
3. Run both suites on the merged tip.

**R3 · P3 · confidence high — `--done` misreads an answer that is still on its branch.** In the scratch repository I
answered with `--answer AP-424 accept`; the answer is on `answer/ap-424`, unmerged. `--done AP-424 …` from `main` says
*AP-424 owes the Owner no act … there is nothing to record* and exits 4. `--due AP-424` in the same state names his
commit `11241d9` and `git switch answer/ap-424`. Fix: where no act is owed here and `answer/<id>` exists unmerged, give
`unmerged_advice`'s line (the act as that branch has it).

**R4 · P3 · confidence high — the copied `--done` line is double-quoted, so the shell expands the *where*.** The dialog
wraps the text in `"…"` and turns only `"` into `'`, so a backtick or a `$` survives. I pasted
``"the report in `docs/x.md`, cost $HOME"`` into zsh and into bash. Both ran `docs/x.md` as a command and printed
`the report in , cost /Users/hf.`, which `--done` would sign into `done:`. The answer dialog has quoted this way since
before this build. Fix: single-quote the argument in both dialogs (`'…'`, with a `'` written as `'\''`).

**R5 · P3 · confidence high — how the gate reads `T24:00` depends on the interpreter.**
`parse_due("2026-09-26T24:00+02:00")` returns `2026-09-27 00:00+02:00` on Python 3.14.3 and `None` on 3.9.6. So
`--check` passes that `due:` on one and refuses it on the other. DEFAULTS' own rule is that what the gate says is a
function of the repository alone. Fix: refuse hour 24 in `DUE_SHAPE` (`T([01]\d|2[0-3]):`), with a test.

**R6 · P3 — `--notify`'s failures are invisible where the README schedules it.**

- Confidence high: when every post fails (a stub `osascript` exiting 1), `--notify` exits 0. It still says
  *remembered in <path>* while the file holds `{}`. The cron line sends all output to `/dev/null`.
- Confidence about 70 %, not run here: on Linux, cron gives `notify-send` no `DBUS_SESSION_BUS_ADDRESS`, so the copied
  line likely posts nothing and tells no one.

Fix: exit non-zero when a notice was NOT posted, and then say *nothing remembered*. The cron line should set
`DBUS_SESSION_BUS_ADDRESS=unix:path=/run/user/$(id -u)/bus` and append to a log file.

**Unproven here:** `notify-send` on Linux and PowerShell's toast on Windows; I read their argv only. I cannot see
whether the one real `osascript` notice appeared on screen. I did not install the launchd agent, so macOS's folder
privacy for a repository under `~/Documents` is unchecked. I did not inspect the sealed directory of session
`8b91dba2`.

## Verdict

**NOT READY.** R1 and R2 are P2; R3–R6 are P3. On their main paths, A–G do what the brief claims, verified by running
them. R1 breaks the rule C was ruled under, on the state `due:` was designed for. R2 is the integration with the CI fix
that the build was told to wait for. The code tier's full loop applies: the Principal grades these findings and
re-briefs, and a pass on the new tip follows.

The Owner lands this by merging; a merge rules nothing.
