# FM-005 — the Reviewer's code pass on `fm/005-a-shipped-tracker-names-its-commit` at 6890292

Verdict: **NOT READY** — two P2, eight P3 (RV-2150 … RV-2159). Every fix below was tried on a scratch copy of this tip. There, each attack it names is refused, and the new checks (44), the blocks holding the changed older checks (41 and 72) and test_core.py (158) pass.
Reviewed: 6890292b2d9336482eb5617fcd62727804141af0, on origin/main 1197e80, which is its merge base.
Reviewer: b3bdb000/reviewer-74 (claude-opus-5-5, max), `reviewer@seat` unsigned, worktree shoalmark-review-9, 00:39–01:40 CEST on 2026-10-01. Independence: the same session as the build (b3bdb000/implementer-73), so not independent.
Tier: code. `git diff --name-only origin/main...HEAD` lists shoalmark.py, test_core.py, test_shoalmark.py, README.md, CHANGELOG.md, overrides/landing.html, examples/de/labels.yaml, FM-005 and INDEX.md.
Read: FM-005's section *A shipped tracker names its commit — v0.19.0* (the ruling, and the Planner's reading of four terms), AGENTS.md, and `git diff 1197e80...6890292` whole. That is d4d1ac2 and 6e59fd5 (the Planner's filing), then 047d3e1, 5562476, 3bb9251, 1467792 and 6890292 (implementer-73).

## Findings
- **RV-2150 · P2 · On Subversion, in a working copy at the repository's root, a revision that changed only the records counts as one behind the move.**
  - Falsifier: `svnadmin create repo`, then `svn checkout file://…/repo wc` (no `/trunk`), `--init --key c5`, and C5-001…011 committed. r3 adds only `docs/work-tracker/evidence/n.md`. C5-001 moves to `Shipped` with the row `a note in r3` and is committed: `--check` exits 0. In a `/trunk` working copy the same move exits 4 (*`r4` changes nothing outside the records*), and `/trunk` is the only layout the FM-005 S block tests.
  - Cause: at the root, `svn_ship_verdicts` (shoalmark.py:4831) sets `base` to `/`. `startswith(base + "/")` then tests `//`, no changed path is made relative, and `/docs/work-tracker/evidence/n.md` is read as product.
  - **Fix:** at :4831, `base = ("/" + urllib.parse.unquote((svn_run("info", "--show-item", "relative-url", ".") or "^/").strip()[2:]).strip("/")).rstrip("/")   # the working copy's own path in the repository — "" at its root`. Add to the FM-005 S block a second working copy checked out at `url` itself. There, a move naming a records-only revision is refused with *changes nothing outside the records*, and one naming the feature's revision passes.
  - Tried: at the root r3 is refused and the feature's revision passes. `/trunk` is unchanged.
- **RV-2151 · P2 · A path git quotes gets past the rule.** In `--name-only` output, git quotes a name that holds a non-ASCII byte, a `"`, a `\` or a control character (`"docs/work-tracker/AP-600-\303\274ber.md"`). The rule compares that quoted name with the plain one.
  - (1) A tracker filed as `docs/work-tracker/AP-600-über.md` is accepted by the gate (exit 0). Moved to `Shipped` with only *Filed.* in its log: the installed hook commits it (exit 0), `--check` exits 0, and `--check` on a merge that brings the move also exits 0. The same move of `AP-500-x.md` exits 4. `AP-601-say "hi".md` behaves the same. Cause: `staged_now()` (:4430), `read_changes()` (:4636–4662) and the hook's `grep '^({dir}/…'` (:7149) never match the quoted name.
  - (2) A commit that adds only `docs/work-tracker/evidence/say "hi".md` (or a name with a tab), named in a ship-log row, passes. Cause: `git_ship_verdicts`'s `git log --name-only` (:4770) hands `ratio_class` a name that starts with `"`, and it is read as product. An umlaut is refused there, because of `core.quotepath=off`. `--ratio` in the same file reads its paths with `-z` (:5006, :5008).
  - **Fix:** read every path list the rule rests on NUL-separated:
    - `read_changes()`: `names = lambda r: set(r.stdout.split("\x00")) - {""} if r.returncode == 0 else set()`, and `"-z"` in the three `git("diff", …, "--name-only", …)` calls that `names` reads (:4653, :4655, :4662).
    - `brought()` (:4643–4648): `git("log", "-z", "--no-merges", "--reverse", "--relative", "--name-only", "--format=%x01%H%x02%an%x02%ae", *tips, "--not", first)`. For each `record` of `log.stdout.split("\x01")[1:]`: `head, _, files = record.partition("\x00")`, `c, an, ae = (head.split("\x02") + ["", ""])[:3]`, and the files are `set(files.lstrip("\n").split("\x00")) - {""}`.
    - `staged_now()`: `"-z"`, and `split("\x00")`.
    - `git_ship_verdicts()` (:4770–4773): `git("log", "-z", …, "--format=%x01%H", …)`, records split on `"\x01"`, `sha, _, files = record.partition("\x00")`, and the files are `[f for f in files.lstrip("\n").split("\x00") if f]`.
    - The hook (:7149): `if git -c core.quotePath=false diff --cached --name-only | grep -q -E '^"?({dir}/.*\\.md|{config}|{tool}/)'; then`.
  - Checks to add: `AP-600-über.md` and `AP-601-say "hi".md` moved to `Shipped` are refused by the installed hook and by `--check`, and a records-only commit under `evidence/say "hi".md` is refused. The rights read the same lists and miss these names today. Tested: a seat without `close` closes `AP-600-über.md` and `--check` exits 0, while the same close of `AP-500-x.md` exits 4. The fix lets the rights see these names, and one line in FM-005's *What is true now* says so.
  - Tried: every case is refused, including a merge that brings the move. The control is unchanged.
- **RV-2152 · P3 · The hook judges `.git/index` and the working tree, not the commit being made.**
  - The reproduction commits through the installed hook, exit 0, with `git commit -a` and with `git commit <path>`: git hands the hook an index of its own, and `staged_now()` strips `GIT_INDEX_FILE`.
  - A move staged with nothing named passes while the unstaged working tree names the feature, because `shipped_moves` reads the working tree (:4854).
  - A `git commit --amend` that drops the named row also passes, because it is read against the commit it replaces, as FM-033's hook reads it.
  - `--check` refuses each afterwards (exit 4), so this is a hook-only miss: P3 by AGENTS.md.
  - **Fix:** in `staged_now()`, pass `env = dict(nested_git_env(), **({"GIT_INDEX_FILE": os.environ["GIT_INDEX_FILE"]} if os.environ.get("GIT_INDEX_FILE") else {}))` to its `git diff --cached`. This is `pending_judgement`'s own line. In `shipped_moves`, before the working-tree read, add `if result is None and COMMITTING: texts = cat_blobs([f":./{rel}" for rel in touched], <that env>); now = {rel: texts.get(f":./{rel}") for rel in touched}`, and read the working tree only `elif result is None`. Add a check that the reproduction through the installed hook is refused, both with `git commit -a` and with `git commit <path>`.
  - Tried: both are refused, and so is the partly staged move.
- **RV-2153 · P3 · A `Shipped` tracker that is renamed is refused as a move to `Shipped`,** where the ruling says *nothing shipped before breaks*.
  - Falsifier: AP-500 is `Shipped` in an old commit with no commit named. It is renamed with `git mv` to `AP-500-a-better-slug.md` and committed: `--check` exits 4, *its ship log names no commit*. This was the Builder's unproven case; it is now proven.
  - **Fix:** in `shipped_moves`, after `before = cat_blobs(…)` (:4860), when the tracker is absent at a base, read that base's file of the same id:

    ```python
            for base, rel in [(b, r) for r in shipped for b in bases if before.get(spec(b, r)) is None]:     # absent at a base: new, or the same tracker renamed — its id says which
                d = pathlib.PurePath(rel).parent.as_posix()
                was = next((n for n in (git_out("ls-tree", "--name-only", f"{base}:./{d}") or "").split("\n") if n.startswith(rels[rel]["id"] + "-") and n.endswith(".md")), None)
                before[spec(base, rel)] = cat_blobs([f"{base}:./{d}/{was}"]).get(f"{base}:./{d}/{was}") if was else None
    ```

    Add checks that the rename passes, and that a rename which also moves the tracker to `Shipped` is refused.
  - Tried: both hold, and a new tracker filed as `Shipped` is still refused.
- **RV-2154 · P3 · A tracker linked from outside the repository stops every run in a traceback.**
  - Falsifier: a tracker file that is a symlink to a file outside the root makes `--check` exit 1 with `ValueError: '…/outside-AP-590.md' is not in the subpath of …`. It comes from `ship_problems`'s `relative_to(ROOT)` (:4871). The rule runs without `[seats]`, so every repository meets it. On the same tree the base's `--check` answers without a traceback (exit 3, INDEX.md drift). `in_this_commit` (:4435–4443) guards the same expression.
  - **Fix:** at :4871, write `rels = {}`, then `for t in trackers:` with `try: rels[(TRACKER_DIR / t["file"]).resolve().relative_to(ROOT).as_posix()] = t` and `except (KeyError, ValueError): continue   # no file, or a link to one outside the repository — as in_this_commit reads it`.
  - Tried: exit 0, no traceback.
- **RV-2155 · P3 · How a commit is named: a SHA-256 hash, and an ambiguous abbreviation.**
  - (a) In a `git init --object-format=sha256` repository the full 64-character hash is not read (*its ship log names no commit*); 12 characters pass. `GIT_NAME_RE` (:4725) stops at 40, while the Planner's reading says *seven hex characters or more*.
  - (b) Seven characters that two commits share are refused as *is not in the history (no such commit)*, yet both commits are in it. With the `^{commit}` peel `cat-file` answers `missing`; git says `ambiguous` only for the name as written.
  - **Fix:**
    - (a) `{7,64}`.
    - (b) At :4762–4763, ask each name twice in the one call: `found = git("cat-file", "--batch-check=%(objectname) %(objecttype)", input="".join(f"{n}\n{n}^{{commit}}\n" for n in names))`, `lines = found.stdout.split("\n") + [""] * (2 * len(names))`, `shas = {n: lines[2 * i + 1].partition(" ")[0] for i, n in enumerate(names) if lines[2 * i + 1].partition(" ")[2] == "commit"}`, and `ambiguous = {n for i, n in enumerate(names) if n not in shas and lines[2 * i].endswith(" ambiguous")}`. At :4777, `out[n] = "names more than one commit — write more of its hash" if n in ambiguous else` the line as it is now.
  - Tried: the 64-character name passes, the shared seven now read *names more than one commit*, and the cost check still counts three calls.
- **RV-2156 · P3 · Six refused cases do not assert the way through,** which the brief asks of each one: AP-520 (a new tracker filed as `Shipped`), AP-507 (the Owner's move), AP-513 and AP-515 (a merge brings the move), C5-003 (the move's own revision) and C5-012 (a new tracker on Subversion). **Fix:** add `and way5_(err)` to each of those checks (`way5_(err_s)` for C5-003), and to the checks RV-2150, RV-2151, RV-2152 and RV-2153 add.
- **RV-2157 · P3 · Stale second copies of *done* → *ended*, and one German comma.**
  - test_core.py:381 names the board *done · triage · progress · backlog*, :394 says *triage and done keep their rules*, and :546 says *done ones included*.
  - shoalmark.py:3781 (`triage_worksheet`'s docstring) says *done ones included*, where the printed rule (:3688) now says *shipped and closed ones included*. :2503 says *A done tracker's raise*, and :3937 says *done work*.
  - `desc.ended: ausgeliefert, oder ohne Auslieferung geschlossen` carries the English comma; German sets none before this *oder*.
  - **Fix:**
    - test_core.py:381: *ended · triage · progress · backlog*.
    - test_core.py:394: *triage and ended keep their rules*.
    - test_core.py:546 and shoalmark.py:3781: *shipped and closed ones included*.
    - shoalmark.py:2503: *A shipped or closed tracker's raise*.
    - shoalmark.py:3937: *rank or re-date ended work*.
    - `desc.ended: ausgeliefert oder ohne Auslieferung geschlossen` in examples/de/labels.yaml:35 and test_shoalmark.py:1666.
- **RV-2158 · P3 · README §5's new row: the Subversion wording, and squash or rebase merges.**
  - (a) The row is keyed by the git refusal only. On Subversion the refusal reads *with no revision behind it — its ship log names no revision*.
  - (b) A squash or rebase merge leaves the named commit out of the default branch's history. The pull request's tip passes `--check`, and `--check` on the default branch then refuses the same move (tested: `merge --no-ff` passes; `--squash` and a rebase exit 4). This repository merges with merge commits, but an adopter that squashes meets it.
  - **Fix:** after `` moved to `Shipped` with no commit behind it ``, add ``(on Subversion `… no revision behind it`)``. At the row's end, add: *A squash or rebase merge rewrites the commits a ship log names, and `--check` on the default branch then refuses the move: there, ship in a later pull request, naming the commit the default branch holds.*
- **RV-2159 · P3 · Three records misstate the rule's calls or its source.**
  - (a) `047d3e1`'s message cites the Owner's ruling for holding the hook's time. The ruling filed in FM-005 has no clause on it.
  - (b) `5562476`'s message says *three git calls for every commit a ship log names*. The code makes three for each tracker a change moves to `Shipped`, whatever it names, and the check pins 3.
  - (c) `svn_shipped_moves`'s docstring (:4806) says *`svn status`, else `svn log -l 1`, and one `svn cat` for each tracker that is Shipped after*. Where nothing is pending it makes both, plus one `svn cat` for each tracker the newest revision changed. Counted: 3 calls with nothing moved to `Shipped`, 7 for a move naming three revisions.
  - **Fix:** the next fixing commit's message states (a) and (b), since git is its record (AGENTS.md). The docstring becomes: *The calls: `svn status`; where nothing is pending, `svn log -l 1` and one `svn cat` for each tracker the newest revision changed; and one more `svn cat` for each that is Shipped after.*

## What holds
1. **Where it sits and what one run judges.**
   - `ship_problems` comes right after `rights_problems` in `lint`, and reads `shipped_moves`, which reads `changes_under_review()`.
   - The commit being made is judged against HEAD and `MERGE_HEAD`. `--check` on a clean tree judges HEAD against its parents.
   - A merge is judged as each commit it brings against its own parent, plus its own change against every parent. A conflict resolution that ships a tracker is refused both at commit time and in `--check`.
   - The default branch after a merge commit judges the commits the merge brings. A repository with no `origin` changes nothing, and every scratch repository here had none.
   - A tracker that no change moves is never read. The Owner's move is refused like any other, with and without `[seats]`, and `Closed` is not judged.
2. **Ways around it, refused at this tip** (scratch repositories, the tip's tool):
   - A dangling commit; a commit on another branch; a tree or blob hash (*no such commit*).
   - An annotated tag's hash is read as the commit it peels to: a tag on a records-only commit is refused.
   - An uppercase hash (*names no commit*), and a hash that appears only in *What is true now*.
   - A ship log under `[headings] log = "Protokoll"` is read, and the English heading still is.
   - `status: done` and `status: merged`: the schema refuses the word and the rule refuses the move. `shipped` and `SHIPPED` are refused.
   - A new tracker filed as `Shipped`, and `Closed` → `Shipped`.
   - On Subversion: a revision past HEAD; a revision that touched only another branch (*not in the history*); a move committed and not updated to (judged). A revision newer than the working copy's BASE, named on a pending move, is read correctly.
3. **The refactor 047d3e1 is identical in behaviour.**
   - `read_changes`'s body is byte-identical to the base's `changes_under_review` body (diffed).
   - The memo is keyed by `COMMITTING` and dropped by `configure()`, which every `--root` run and the tests call.
   - No caller mutates what it gets, and a CLI run reaches `lint` once.
   - The three older checks now move to `Closed`, which `transitions()` reads as the same `close`. Their assertions are unchanged.
4. **The refusal** is one line: the tracker, which of the three misses, `git log --oneline -- . ':(exclude,top)<records>'` (which finds the feature and leaves out the note; the Builder's check), or `svn log -v -l 20`, and *mark it `Closed`, not `Shipped`*. README §5's row says the same, apart from RV-2158.
5. **Cost, and whether it holds the hook's time.**
   - git: three batched calls for a tracker a change moves to `Shipped`, and none of those three for any other. On a clean tree, one batched `cat-file` per change reads the trackers it touched, which is the only way to see a move. The pre-commit run makes none.
   - Subversion: see RV-2159 (c), plus one `info`, and one `log` per revision named below the move.
   - Timed in a scratch clone of 6890292, with 1197e80's tool placed beside `vendor/`, three runs each:

     | Run | Tip | Base |
     |---|---|---|
     | Pre-commit, a tracker edit staged | 2.63–2.66 s | 2.67–2.70 s |
     | Pre-commit, a move to `Shipped` naming 5562476 staged | 2.76–2.84 s | 2.67–2.71 s |
     | `--check` | 3.13–3.18 s | 3.24–3.27 s |

   - It holds: only the commit that moves a tracker pays, about 0.1 s, and one reading of the changes now serves the rights and the sessions too.
6. **The board.**
   - A story reads *3 chapters: 1 shipped · 1 closed · 1 open*, in German *3 Kapitel: 1 ausgeliefert · 1 geschlossen · 1 offen*, and its own page *1 shipped · 1 closed*. All three are rendered and checked.
   - `t[2]` is the classified status, so every chapter falls in exactly one of the three counts.
   - The fifth section, `desc.ended` and INDEX.md's 19 Board values read `ended`: 18 Shipped and FM-016, which is Closed. `--check` in this worktree exits 0.
7. **The grep for *done*** (`git grep -n -i -P '\bdone\b'`; `-E '\b'` finds nothing with this git) covers shoalmark.py (139 hits), README, `docs/` and examples/de/labels.yaml (27). What remains is *done* as the claim's word, the *Done when* heading and its `[headings]` key, `done:` acts and `--done`, the answer dialog's **Done**, the status rule that reads *done* as Shipped, and code names. No label or printed text calls a `Closed` tracker done. The docstrings, comments and test names are in RV-2157. The German labels read natively, apart from RV-2157's comma.
8. **The claim.**
   - README:13–14 and overrides/landing.html:361 read *a gate that refuses a done without a commit behind it*.
   - `git grep -n -E 'false \*done|false <em>done|refuses a false'` finds only FM-005's two quotations and `work-tracker/evidence/FM-006/landing/index.html:356`, the three records the brief leaves. A wider grep, German included, finds nothing else.
   - §3's *Done?* and the `--schema` status line changed with the rule, and `--help` says nothing the rule makes false.
   - The CHANGELOG bullet is the first under the one `## Unreleased — 0.19.0` heading.
9. **FM-005** says what is built and what is left, with `next: review`. Its ship-log row names the four build commits, and no status line changes on the branch.
10. **The Planner's reading, judged.** It holds to the ruling's words.
    - *Named*: seven hex characters or more; the build stops at 40 (RV-2155).
    - *In the history*: an ancestor of the commit being judged; squash and rebase merges fall outside it (RV-2158).
    - *The records*: `[ratio] records`, else the tracker directory, prefixed where the working copy is below the top (the Builder's check).
    - *Shipped as the tool classifies it*: the schema allows only the six words, so the front matter the rule reads is the status the tool shows.
11. **Recorded, not findings.**
    - Any commit in the history that changes a product path meets the rule, the root commit included (tested: it passes). That is the ruling's test, and a reader of the ship log does the rest.
    - On Subversion, a move committed without running the tool is judged only while it is the newest revision and no tracker edit is pending. A pending edit of another tracker masks it, and the next revision buries it. That is the design §5 states: *the uncommitted one, else the newest revision*.
    - A new `Shipped` tracker in a tracker directory not yet `svn add`ed is not judged until the directory is added (the Builder's unproven case, proven). `--init` adds the directory, so only a working copy set up by hand meets it.
    - The server-side Subversion hook remains unproven, as the Builder says.

## Controls, one line each
- Setup, 00:39: `git status --short` empty; one fetch; detached at 6890292, which equals `ls-remote`. `--whoami`: `To: b3bdb000/reviewer-74 reviewer (shoalmark-review-9) · claude-opus-5-5 · max`.
- The new checks and the suite's Subversion part (story ×3, FM-005 ×20, W1–W3 and S1–S4 ×11, FM-005 S ×10): the tip's lines beside the tip's tool, 00:47:01–00:48:28, 44 ok, 0 failed, 0 skipped.
- The same lines beside 1197e80's tool, 00:48:38–00:49:54: 21 ok, 23 failed. Every refused case and the story's three fail; every control and every W and S check passes.
- test_core.py at the tip, 00:50:09–00:50:17: 158 ok, all green, exit 0.
- The blocks holding the three checks moved to `Closed` and the `ended` pins (test_shoalmark.py 210–263, 2697–2775, 3066–3162, 3722–3772), ~01:13: 41 ok, 0 failed.
- The German block (1554–2000), 01:14:24: 72 ok. Beside 1197e80's tool, 01:15:21: 70 ok and 2 failed, both C4, so the label rename bites.
- The runs fell inside FM-028's 00:00–02:00 window, but no rendered check failed at the tip, so none needed a base run beside it.
- `--check` in this worktree: exit 0, and the tree stays clean.
- The fixes above, on a scratch copy of the tip: every attack named is refused; 44, 41, 72 and 158 ok, 0 failed.

Quality read: the rule is placed and built well. It reuses the gate's one reading of a change, reads nothing of a tracker no change moves, batches its git calls, names in its refusal the tracker, the miss, the command and *Closed, not Shipped*, and its tests bite. Its quality defects are RV-2151, where git's quoted names are read as plain ones although `--ratio` in the same file reads `-z`, and RV-2159 (c), a docstring that under-counts its calls. The rest reads clean.
Four numbers for this verdict: records +147, product 0.
Next: the Builder fixes RV-2150 … RV-2159 on this branch; the Reviewer verifies the fixes at code tier; then the Owner opens the pull request.
