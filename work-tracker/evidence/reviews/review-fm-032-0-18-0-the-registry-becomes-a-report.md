# Review — release 0.18.0 at 37c73d0 (2026-09-24 13:51 CEST, Reviewer, session `8e509911/reviewer-1`)

**Scope.** Branch `fm/032-0-18-0-the-registry-becomes-a-report`, tip `37c73d0`
(`37c73d0403b475d96e98dfa8c944545a44a1c526`), on `origin/main` `ed11081`. It is release **0.18.0**: `VERSION` says
0.18.0, and the CHANGELOG's §0.18.0 is the contract checked below.
- The registry branch: `3c0754f`, `6a14704`, `2fcd15b` and `a2956a5`, by the Implementer under
  `8e509911/implementer-9`.
- The queue branch: `90d3d6f`, `43e6815`, `bd7d5ea`, `fbc2697`, `66f4b7b` and `636f56e`, by the Implementer under
  `8e509911/implementer-16`.
- The Principal's merges and commits, under `8e509911`: `8eaff7d`, `b1f9d3f` (`main` after PR 46), `fd6ddd2` and
  `37c73d0`.
- **Tier: code.** `git diff --name-only origin/main...37c73d0` includes `shoalmark.py`, both suites and
  `shoalmark.toml`. The full loop applies.
- **Independence:** this is the same session. The Reviewer is `8e509911/reviewer-1`, and every commit in the range is
  under the root `8e509911`. This is reported, not refused, and `--check` will count this verdict as *same session*.

## What I ran, and what came back

**Gates and suites at `37c73d0`.**
- `--check` exits 0. It prints `filing freeze: 16 open, at or above 8 — only bug filings`.
- `--session-check` exits 0.
- `test_shoalmark.py` is all green: 281 ok, in 2:34.
- `test_core.py` is all green: 148 ok.
- `/usr/bin/python3` (3.9.6) gives the same results: 281 and 148, both green.
- `python3 shoalmark.py` writes 32 trackers, and `git status --porcelain` stays empty. The run is idempotent.
- `work-tracker/sessions.md` is gone from the tree.

**The registry as a report.** Tested here and in a temporary repository with `[seats]`.
- `--sessions` here reports 29 ids and 151 commits, in 0.22 s. I checked three ids against
  `git log --grep '^Session: <id>$'`:
  - `8e509911`: 25 commits, `830a08a` → `37c73d0`, worktree `shoalmark-principal`.
  - `8e509911/implementer-9`: 8 commits, `ee152ef` → `a2956a5`, worktree `shoalmark-impl-2`.
  - `e8e309df/reviewer-7`: 2 commits, `58c232a` → `8067d80`, worktree `—`.

  All three match: the count, the first and last commit, and the worktree.
- `--session open …` and `--session close …` each print one line and exit 2.
- `--session new` prints a fresh id. `--session new x` and `--session bogus` exit 4, with the usage line.
- **The gate's one rule, tested in a temporary repository:**
  - A seat's commit with no `Session:` exits 0 while the history carries none, and exits 4 once it carries one.
  - Mismatched seat parts are refused, exit 4: `1234abcd/reviewer-1` on the implementer. So are ids of the wrong shape:
    `foo`, `1234ABCD`, and the nested `1234abcd/implementer-1/reviewer-2`.
  - `1234abcd` and `1234abcd/implementer-2` pass.
  - The Owner's commit, and a commit by an author outside `[seats]`, are not judged.
  - On a clean tree, `--check` refuses a made seat commit with no trailer. It also refuses a mismatched commit that the
    Owner's `--no-ff` merge brings in (*in `<sha>` … which the merge brings*).
- `--session-trailer` appends `Session:` and `Worktree: t1`. A message that already carries `Session:` gets only the
  `Worktree:`. Without `seat.session`, nothing is appended.
- A leftover `sessions.md` makes `--check` print one `warning:` line and exit 0. `--session-check` and `--owner` are
  silent about it.
- A `labels.yaml` that sets `sessions.open` or `sessions.abandoned` is told they are not labels.
- `--triage` runs on a scratch clone at the tip, exit 0. The worksheet is written, and nothing refers to a registry.

**`--queue`.** Tested in a temporary repository whose `origin` is a bare repository reached through a fake `ssh`, so
the URL reads as GitHub. A fake `gh` on `PATH` serves ten pull requests, and the forge's `refs/pull/N/head` are set in
the bare repository.
- **Each pull-request action came out as it should:**
  - `merge`: READY WITH FINDINGS on the head.
  - `closes with PR 6`: its head is inside PR 6's.
  - `close: carried into PR 8`: by a cherry-pick.
  - `wait: conflict in shared.txt`.
  - `wait: no verdict on <sha>`.
  - `wait: NOT READY (<sha>)`.
- **The `answer/*` readings:**
  - `merge: your answer` for an SSH-signed commit by the Owner that verifies.
  - `wait: unsigned answer` for an unsigned one.
  - `wait: answer not verified here — …` when `gpg.ssh.allowedSignersFile` is unset, or names a file that is
    missing.
- **Pushed branches:**
  - `no verdict on`, `verdict <sha> READY: open it`, `conflict in shared.txt` and `NOT READY (<sha>)` come out as they
    should.
  - These are excluded, as they should be: `main`, a merged head, a head inside an open pull request, `answer/fm-025`,
    and a head that `refs/pull/99/head` (a closed pull request) carries.
- **Order and count:** actionable pull requests come first, oldest first, then the waiting ones, then the branches by
  name. The count line reads `14 waiting on you: 2 merge, 2 close, 6 wait, 4 pushed without a pull request`.
- **Without a forge,** each case prints one line and exits 3: no `gh`, `gh` failing, an `origin` that is not GitHub, no
  `origin`, and not git.
- `--owner` and `--standup` end with the section where the forge can be read, and leave it out without `gh`.
  `--standup FILE.ics` does not add it.
- **The real `--queue` here** (4.5 s) prints three lines, `fm/029…`, `fm/031…` and `fm/032…`, and
  `3 waiting on you: … 3 pushed without a pull request`. The forge agrees: `gh pr list --state open` is empty, and
  `git ls-remote --heads origin` lists `main` and those three. See R2 for `fm/031`.

**The freeze and `--tags`.** Tested in a temporary repository with `freeze_at = 2`.
- **Under the line,** the first two filings are written.
- **At the line:**
  - A third filing without `--tags bug` exits 4, with the count, the line and the rule's words, and nothing is written.
  - `--tags bug` is written, as `tags: bug`.
  - `--tags bug,process,bug` gives `tags: bug, process`.
  - `--tags process` is refused.
  - `--tags bug,nope` is refused, naming the vocabulary.
  - Four tags are refused.
  - In each refusal, the file count is unchanged.
- `--check` prints the freeze line, and its exit is unchanged.
- `freeze_at` values of `-1`, `"8"` and `true` stop the run and name the key.
- `--schema` has a `freeze_at` row that names `--tags bug`.

**`--answer`, revoke, supersede.** Tested in a temporary repository with a bare remote and a real signing setup: an
SSH key, `gpg.format ssh`, and an allowed-signers file. Every answer commit verified as `G owner@x`.
- The first answer cut `answer/fm-001`, signed and pushed, and printed `back on fm/001-importer`.
- A second answer, while `answer/fm-001` was unmerged, exited 4, naming `git branch -D answer/fm-001`. The branch was
  kept.
- After the merge into `main`, a second `accept` without `--supersede` exited 4, naming both forms.
- `revoke` without a reason exited 4.
- `revoke "the audit found a hole"` deleted the merged branch and cut it fresh, which it said in one line. It wrote
  `revoked - …` and put this row first in the ship log:
  `Answer of 2026-09-24 superseded: *"accepted - the importer now"* (792dc80) — revoked: …`.
  `792dc80` is the commit that wrote the first answer.
- `accept "wait for the audit" --supersede` replaced it, with the row
  `… *"revoked - …"* (0a89cdd) — replaced by: …`.
- `--check` then exited 0. The tracker's `supersedes` reads `0a89cdd`, and the board's data row carries it, with
  `viewer.supersedes`.

**The verification message.** Checked in a fresh clone of that repository, where `gpg.ssh.allowedSignersFile` is
unset.
- Both lines say *it is signed, but this clone cannot verify: `gpg.ssh.allowedSignersFile` is not set — see …/signing/*.
  With a signers path that does not exist, they say *names ./nope, which does not exist*.
- An unsigned answer commit is still told *sign it (`git commit -S`)*. The exit is 4 in every case, as before.

**The consumer.** I made a `--shared` scratch clone of the parent project at its `main` tip, copied 0.18.0 over its
`tools/shoalmark/` with a regenerated PIN, and ran everything through its own wrapper.
- `--check` works as it should:
  - The two old *sign it* lines, on two of its answered trackers, now say *signed, but this clone cannot verify*.
  - With its `allowed_signers` set, lint is clean, apart from the one `sessions.md` warning.
  - It exits 3 only for the derived pages that need the submodules, which is also the result with 0.17.7 there.
- `--session-check` refuses a principal with no `seat.session`, and passes `8e509911/principal-3`.
- `--session-trailer` appends both trailers.
- **`--sessions` on the parent project's principal clone** (read-only, 3737 commits): 0.33 s, 12 ids,
  77 commits.

**Performance.**
- `--check` takes 6.1 s here at the tip, against 6.3 s at `ed11081` on its own tree. `verdict_reports` is 5.1 s of it,
  and it was not changed in this release.
- The default run takes 6.1 s against 6.3 s.
- `--owner` takes 9.9 s with the forge, against 4.1 s without `gh`.

**Not verified.**
- The GPG branch of `signature_gap` (*not in this clone's GPG keyring*): `gpg-agent` cannot make its socket under this
  sandbox's long scratch path.
- `--queue` against GitHub itself with open pull requests: none are open. The forge was faked as described above.
- The Windows and Subversion paths were read, not run.

## The CHANGELOG's claims, one by one

| # | Claim (§0.18.0) | |
|---|---|---|
| 1 | `sessions.md` deleted; nothing reads or writes it; `--check` warns in one line and passes | ✓ |
| 2 | `--sessions`: one row per id — seat, first and last commit, count, worktree — Markdown on stdout, written nowhere | ✓ |
| 3 | `--session open` and `close`: one line each, exit 2; `--session new` stays | ✓ |
| 4 | The gate's one rule: shape and seat part; not the Owner, not outside `[seats]`; a history with no `Session:` not judged | ✓ |
| 5 | `Worktree:` appended by the same hook; `—` before; the hook lines unchanged | ✓ |
| 6 | The board's strip **and the digest's line** name the last day's sessions *with their worktree* | ✗ the digest drops the worktree (R5) |
| 7 | `sessions.recent` new; `sessions.open` and `sessions.abandoned` gone, and a `labels.yaml` that sets them is told | ✓ |
| 8 | `--queue`: `gh`, fetched once, six actions, order, count, the verdict word from the subject; exit 3 without a forge; `--owner` and `--standup` end with it | ✓ (R3: not in a single-branch clone) |
| 9 | The freeze: `--new` refuses without `tags: bug`, exit 4; `--tags` writes `tags:`, deduplicated, from `[tags]`; `--check` line; `--schema` key; off by default | ✓ (R4: impossible where `[tags]` has no `bug`) |
| 10 | A merged `answer/<id>` cut fresh; an unmerged one refused, naming `git branch -D`; back to the starting branch after the push | ✓ |
| 11 | Revoke or supersede: the old answer into the ship log with its commit; the board shows *supersedes <sha>* | ✓ |
| 12 | Pushed branches: the exclusions, the three readings, the count's clause | ✓ (R2: a branch inside another branch is its own line) |
| 13 | `answer/*`: `merge: your answer` when its head's author may answer and the commit verifies, else `wait: unsigned answer` | ✗ a seat keyed by name reads *unsigned* (R1); the third reading is undocumented (R5) |
| 14 | A signed commit this clone cannot verify is said to be that; an unsigned one is still asked to sign; the exit unchanged | ✓ SSH, unset and missing · GPG not run |

## Findings

**R1 · P2 · confidence high · `--queue` calls a signed, verifying answer *unsigned* when `[seats]` names the Owner by
name.** This is the parent project's own configuration.
- **The mismatch.** `answer_reading` (`shoalmark.py:924`) tests `(email if SEATS else name) in may_answer()`, so under
  `[seats]` it tests the email alone. The gate matches a seat on email or name (`seat_of`), and so does `--answer`. The
  parent project keys its `owner` seat by his git name, marked `signed`.
- **What it does there.** In the scratch clone, on its two signed answer commits of this week:
  - `seat_of` gives `owner`, and `verified_as` on his email is `True`. The gate accepts both.
  - `answer_reading` returns `wait: unsigned answer` for both.
- **Reproduced here too.** With `owner = "Owner signed"`, PR 9 (signed, `G owner@x`) reads `wait: unsigned answer`.
- **Why it matters.** Once the parent vendors 0.18.0, every signed answer the Owner pushes there is shown to him as
  unsigned. That is the message this release set out to stop, and it is shown in the one view built for him. It
  contradicts claim 13.
- **Fix.** Read the author as the gate does: `seat = seat_of(name, email)`, then `holds(seat, "answer")` under
  `[seats]` (`name in may_answer()` without it), then `verified_as(head, email)`. Add a check with a seat keyed by name.

**R2 · P3 · confidence high · A pushed branch inside another pushed branch is listed as its own wait, and the line never
clears.**
- The real queue here shows `branch fm/031-… @ 636f56e  wait: no pull request — no verdict on 636f56e`. But `636f56e`
  is an ancestor of `37c73d0`, which is `fm/032`'s head, and it is not on `main`.
- Once this verdict lands on `fm/032`, that line says what to do. The `fm/031` line keeps asking for a verdict that
  will never name `636f56e`, until someone deletes the branch or opens a pull request that carries it.
- The pull requests get *closes with* and *carried into*, but the pushed branches are not read against each other.
- **Fix.** Leave out a pushed branch whose head is inside another pushed branch's head, or give it
  `closes with branch <name>`. Either way, add a check.

**R3 · P3 · confidence high on the mechanism · In a clone whose fetch refspec does not cover every head, one unknown
object wipes out every verdict.**
- **Where it breaks.** `forge_prs` fetches only the configured refspecs, plus the open pull requests' heads
  (`:882`). In a single-branch or shallow clone, a pushed branch's head is never fetched. The one verdict `git log`
  (`:989`) is handed that unknown sha, fails, and returns nothing.
- **What it does.** In a `--single-branch` clone of the test remote:
  - PR 1 went from `merge` to `wait: no verdict`.
  - PR 3's `NOT READY` became `no verdict`.
  - The pushed branch in conflict read `no verdict`.
  - The count fell to `1 merge … 7 wait`.
- The error is on the safe side, since nothing reads `merge` wrongly. But one stray head erases every verdict in the
  view.
- **Fix.** Fetch `+refs/heads/*:refs/remotes/origin/*` explicitly, or the pushed shas. Keep out of the verdict log any
  head that `git cat-file -e` cannot find, and say in its line that it was *not fetched here*.

**R4 · P3 · confidence high · The freeze's way through is the literal tag `bug`, and `[tags]` may not have it.**
- A repository's `[tags]` replaces the default vocabulary, and the parent project's has no `bug`.
- With `freeze_at` set there, `--tags bug` is refused as *not in the vocabulary*, and `--new` without it is refused as
  frozen. Nothing can be filed, not even a defect. I reproduced this with `[tags] research, process`.
- It is off by default, so vendoring alone breaks nothing. But the CHANGELOG's *a bug filing passes the freeze* is
  false in such a repository.
- **Fix.** `configure` refuses `freeze_at > 0` when `bug` is not in `[tags]`, in one line that names both keys. Or the
  CHANGELOG, README §2 and the schema row say that the freeze needs `bug` in `[tags]`.

**R5 · P3 · confidence high · Four places where the words fall short of the code.**
- **The digest.** CHANGELOG claim 6 says the digest's line names sessions *with their worktree*. `sessions_digest`
  drops it (`:3071`, `for sid, seat, _w`). Either the digest prints it, or the claim names the board alone.
- **The third `answer/*` reading.** `wait: answer not verified here — <why>` appears in neither the CHANGELOG nor the
  README's *what to merge* row, which ends *else `wait: unsigned answer`*.
- **`--help`.**
  - `--queue` (`:3370`) lists only the six pull-request actions: no pushed branches, and no `answer/*` readings.
  - `--answer` (`:3361`) still says `accept|reject` only. It does not say that it goes back to the starting branch, or
    that it cuts a merged `answer/<id>` fresh; `revoke` appears only under `--supersede`.
- **README §6 *Seen*** (`:328`). It says `--owner` *ends with one line, the sessions of the last day*. It now ends with
  the queue, as the *what to merge* row says.

**R6 · P3 · confidence high · Flags that mean nothing alone are silently ignored.**
- `--tags bug` without `--new`, and `--supersede` without `--answer`, each run the default regeneration and exit 0.
- `--tags ''` is refused with *at most 3 tags*, which is the wrong reason.
- `--tags Bug` is refused, although tags read from the template are lower-cased.
- **Fix.** Refuse `--tags` without `--new` and `--supersede` without `--answer`: one line, exit 4. Lower-case `--tags`.
  Make an empty list say that no tag was given.

**R7 · P3 · confidence high · FM-031's record is behind the tip.**
- *What is true now* (`:15`) dates the revocation *at 12:5x*. `7c97c5b` is 12:39:56, and PR 46 merged at 12:53:18, as
  AGENTS.md says.
- `:16` credits *pull requests and pushed branches alike* to `90d3d6f`. `90d3d6f` read pull requests only; the pushed
  branches are `636f56e`.
- Neither ship log has a row for `636f56e` (pushed branches, `answer/*` read as the Owner's, the unverifiable-signature
  message) or for the merge `37c73d0`. Each earlier build has one (`90d3d6f` at 12:18, `3c0754f` at 11:43).
- **Fix.** The time, the sha, and one row on FM-031.

**Checked, and not a finding.**
- No dead code is left from the registry. Every `def` and every new constant has a caller.
  - `SESSIONS_NAME` and `sessions_file()` remain only for the warning.
  - `addenda_only` still counts `sessions.md` as a review addendum. That is for history, and the README says so.
- The old ids pass the new shape: every `Session:` in this repository's history and in the parent's (14 ids) matches
  `SESSION_ID_RE`.
- **The house rules in AGENTS.md** check out against git:
  - `d20bc89` is 11:08:24 and `ffa63b8` is 11:07:43. `7c97c5b` was merged by `ed11081` at 12:53:18. All three are
    `G holgoijo@gmail.com`.
  - The cap paragraph cites his signed `7c97c5b` and nothing from chat, and it says the cap is not a rule.
- **The FM-031 and FM-032 trackers:**
  - Both have `next: build` and no ask lines.
  - Their `## Asks` sections carry the exchanges. FM-031's ship log rows the answer it superseded (12:55, `d20bc89`).
  - FM-032's 12:45 row names exactly the conflicts that replaying `8eaff7d` gives: `README.md`, `shoalmark.py`, FM-031,
    `INDEX.md` and `sessions.md`.
- The verdict word is unambiguous in every `Reviewed:` subject in both repositories (37 here, 24 there). The three with
  no word are skipped: `26af793` here and two in the parent. Where one follows a verdict, that verdict stands.

**What a consumer that vendors 0.18.0 must do.** Vendoring alone keeps it working. `--check` warns once and passes, and
the hooks and the wrapper's pass-through are unchanged. Then:
- `git rm docs/work-tracker/sessions.md`.
- Drop `--session open` from its AGENTS.md seat row, and update its lefthook `session` comment, which describes the
  old rule.
- Set `gpg.ssh.allowedSignersFile` in every fresh clone.
- Leave `freeze_at` unset until its `[tags]` has `bug` (R4).
- Until R1 is fixed, expect `--queue` to call each of the Owner's signed answers there *unsigned*.
- Expect `--owner` to fetch `origin` and call `gh` from now on: about 5 s more here.

**Verdict:** NOT READY. R1 is P2; R2–R7 are P3. The Owner may not tag this tip: R1's fix and a verification come
first.
