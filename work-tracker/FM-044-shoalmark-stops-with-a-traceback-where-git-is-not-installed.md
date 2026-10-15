---
id: FM-044
status: In Progress
considered: FM-003
tags: bug
next: owner
triaged: 2026-10-13
rank: 3
tier: P1
hook: "A Subversion team without git could not run the reviewed copy: every command but --session-check and --queue stopped with a traceback before it wrote anything."
ask: "Which disposition should the B readers take after RV-3092–RV-3094 exhausted their review rounds?"
ask-kind: ruling
ask-since: 2026-10-13
ask-proposal: "Keep the readers held; prepare structural XML validation for Owner disposition without a third review, while local components continue."
---

# FM-044 — shoalmark stops with a traceback where git is not installed, on Subversion too

## What is true now

**2026-10-15 — PR #173's second fix round READY `3932e7f` (round 2 of 2); the Owner's run `38614474342` on it is green on Linux and macOS, and on Windows 3.12 `test_shoalmark.py` is all green while `test_core.py` fails the launch ceiling; a third fix round, RV-3250–RV-3251, is built, and the Reviewer's first critical pass on it is next.**
Git converts both pinned launch files to CRLF at a Windows checkout, so the ceiling's working-tree bytes no longer hash to
its pin: six FAIL lines, then a `RatchetHistoryError` that `test_vcs_skeleton.py:860` let escape, ending `test_core.py`. A
CRLF checkout made by macOS Git reproduces both exactly. `.gitattributes` now keeps `test_vcs_launch_ceiling.json` and
`test_vcs_launch_allowlist.json` as committed (`-text`); the files and the pin are unchanged (RV-3250). The RV-3088 checks
that read history catch `RatchetHistoryError` alone and fail on their own line with its text (RV-3251). Windows 3.9's
FM-039 board render timed out against a 10.0 s control; #173 changes no render code, and a rerun or a budget is the
Owner's call (RV-3252, recorded only). Windows 3.9's `test_core.py` has never run. The second round answered run
`38589202689`: on Windows it counted 1867 ok, 5 FAIL and 47 checks skipped in 15 blocks; `test_core.py` was skipped after the failed
step, so it has still never run there at this branch. The five are new and Windows-only. A1's board link compared a raw
path with the URI the product prints (RV-3230); A1's reconfigure compared raw spellings with the product's normcased
inventory, its second clause passing vacuously (RV-3231). A2's ignore setup met a product defect: `proplist --xml` prints
an `svn:` value with Windows' line ends, `svn_local_properties` returned them, and `svn propset` refused the mixed value
that `svn_ignore_board` built. On Windows, where `proplist --xml` also prints an `svn:` value in the system's code page,
`svn_local_properties` alone now reads each `svn:` value with `propget --xml`, as stored (RV-3232, RV-3235). The
POSIX-shell CLI test skips by name on Windows (RV-3233), and the Git entry differential removes its consumer with a
helper that clears Git's read-only bit (RV-3234). RV-3220, the first round's last finding, made the entry and binding
fixtures' `svn add` quiet. The first round answered run `38539381661`:
Run `38539381661`: ubuntu 3.9 ended FAILED: 6, ubuntu 3.12 and macOS 3.12 FAILED: 4, and both Windows jobs a traceback after
25 FAIL lines. No board render failed: "headless Chrome did not return index.html within 5 s" is the saw-text of FM-035's
own control, inside an `ok` line. Windows did not run to the end: A1's `svn add` of a page no measured run had written
raised from a `check=True` setup step, so A1's later checks, A2, the A corrections and every stage block after them have
never run there. `test_core.py` has not run in CI at this head; it is the step after the failed one. This round: nine
answer and act checks expect each copied command as the accepted `printed_arg` spells it, written out for Windows and
POSIX; `--init` judges the key and the folder's name before its first metadata read, so a name with a line break is
refused by name again (`init` alone changed in production); A1's search folder holds svn as svn names itself, its DLLs
beside it on Windows, a fixture step that fails is a named FAIL and the next block runs, and A1's checks say what they
saw; Python 3.9's tempdir probe, written through a second open of its descriptor, is admitted in exactly that shape.
The second pass makes the suite's own observers read the start as Windows audits it, no program and one command line
(RV-3061's shape): each keeps the raw line, an exact check compares it with `subprocess.list2cmdline` of the expected
argv, and a check of a program or a subcommand reads the argv back with `split_cmdline`. Before, A1's exact status
check failed there, and A2's and the corrections' no-mutation checks passed with nothing read. A2 reads `svn:ignore`
back through `propget --xml`, since plain `propget` prints an `svn:` property with the system's line ends. The third
pass gives the Git entry differential's observer, the last in the suite that read a Windows start as a list, the same
reading: its exact `git diff` and `ls-remote` checks failed there, and "dirty default asks no origin" passed with nothing read.
Current Owner main `80b60c8` includes R12 READY `246ccdf` and #171. This branch carries its exact
AGENTS and signed TRIAGE changes through ordinary merge `2f373a8`; it adds no Owner ruling or consumer authority.
RV-3040: recorded privately. Common READY `ef77527`, Reviewed `b72b9ae`, closes RV-3085–RV-3088;
dispatch records READY `84c8a6b` remain ancestry. RV-3057 P3 was fixed forward without a re-pass.

A1/A2 READY `6fe35f5`, Reviewed `a9a36d4`, closes RV-3089–RV-3091, BOUNDED BOARD/INIT/INSTALL ONLY.
A caller final READY `4ab9341`, Reviewed `7063dac`, closes RV-3096 P2 in its second/final round;
RV-3097 is unused. Its four inherited-dot corrections pass 119 component controls, 303 core checks and
22 independent actual-function observations. The ordinary local seat merge retains its exact fifteen
caller functions and runtime controls. C final READY `f59a1c1`, Reviewed `05e02ac`, closes RV-3095,
BOUNDED CLI/PRESENTATION/DOCUMENTATION ONLY. Closed component findings are not reopened.

P final READY `2dbaa80`, Reviewed `f3bcca0`, closes RV-3098 in its second/final round, BOUNDED LOCAL P
INTEGRATION ONLY: the installed tool validates its complete configuration chain against the affected
directory's consumer before metadata queries, PATH contents, tracker/proof reads or writes. P composes actual
main/preflight/Tortoise binding and the once-per-invocation limitation:
"Subversion: this local run cannot verify commit signatures or server-authenticated authors; protected SVN acceptance remains held."
Local board/init/install/refusals run with Git absent and the server unavailable. Ordinary legacy-history
index/check/triage controls explicitly use available file:// history; their untrusted account strings establish
no authentication or adoption. Recursive applied triage prints the limitation once. Git retains its actual
mixed-flag ordering, origin-selection probe, process options and cleaned foreign hook environment.
P's production SHA-256 `344db0516be7876a796f19c40b3d4334208ae33524dee1a20b8dbdf489d9b1fe` passed compile,
unchanged core 303/303 and the stage runtime block 619/619 with zero skips; the whole `test_shoalmark.py`
had not run before CI. Component-only source assertions remain in their standalone accepted modules, and
unchanged core retains the production/every-parent history ratchet.

Owner PR #173 CI at `2dbaa80`, run 38523854934: all five suite jobs failed after check 168, the FM-006
tempfile check — exit 4 on Linux and macOS, 1 on Windows, as reported — with no traceback. The next block, FM-006's board run in Subversion, made a working copy
as an empty `.svn` and ran `--init` in process: accepted metadata validation refuses a `.svn` with no
`wc.db` or `entries` (exit 4), and the suite's in-process `run` captured that line, so the escaping exit
ended the suite silently. FM-045 C's Subversion case had the same fixture. Both, and FM-045's suite-end
runtime check, assumed the board's run starts no `svn`, where accepted A1 starts exactly one local
`svn status … --xml` in the working copy. FM-006's v0.19.1 `--tsvn-hook pre` check handed fake
TortoiseSVN paths, which P's accepted binding refuses before the gate.

The correction is test-only. Both fixtures are real file:// working copies, skipped by name without
svn/svnadmin (CI installs both). FM-006's check admits only that exact status in the working copy, with the
repository moved away; its stand-in opens its log before the run, as the tripwire refuses a file opened
inside the event. FM-045 C and the runtime check exclude only that argv; the `env git log` control stays.
The hook check gets a real path list, message file and working copy, as S2 does. Production, `ci.yml`,
list and ceiling are unchanged. On `2dbaa80` the two blocks exit 4 and the hook check fails; corrected,
all pass. The old tool's `svn blame` still fails FM-006's check; FM-045 C and the runtime check fail on the
status argv without their exclusion. FM-037's empty `.svn` guard block and the other old SVN blocks pass
unchanged.

The Owner's order on PR #173 adds one more test-only correction: the suite's in-process `run` returns a
refusal the tool ends with as the program ends — its exit status and both streams; a message is exit 1, on
stderr — so its check fails and the suite goes on, and the next CI run shows every remaining failure at
once. Product refusals are unchanged; two FM-037 checks read the message from the returned stderr. A new
regression compares each refusal with the program and runs these helpers as a program past one: with the
old helper it fails, its child suite ending with exit 4 as CI did; corrected, the child ends on its FAILED
line, exit 1.

First critical pass NOT READY `39abd8a`, Reviewed `b08f376`, judged both corrections sound and found three new
issues. RV-3061 P2, product: on Windows CPython audits the board's status start as no program and its command
line, and the board's judge admitted only `svn`, so every Subversion `--html-only` there would stop, exit 4 —
fail closed, nothing exposed. The judge now also admits that Windows shape, still only the exact status in
the working copy; no program with a list, any explicit program, other argv, cwd or spelling stays refused.
RV-3062 P3: six skip reasons now say "svn or svnadmin is not installed here"; counting is unchanged. RV-3063
P3: a new check requires a RuntimeError and a KeyboardInterrupt to leave `run` as raised, its state restored.
Simulated event shapes fail on `b08f376` and pass corrected; the event this system really audits for the
board's own status start is caught before anything starts and admitted — POSIX here, Windows only natively,
in CI. Predicate and helper mutants each fail their control. Only `board_judge` changed in production
(SHA-256 `fb4fde94142ca4bbb671d576d5b0fa3baffed259d0b33d39b74ea68465acbdd3`); scanner, list, ceiling and
boundary hold; A1's 152 controls and unchanged core 303/303 pass. Round 2 of 2 by the same independent
reviewer found it READY `d0f0f24`; the Owner's CI run on it is the one above.

Composition preserves every parent's removal: 45 and 44 keys intersect to 29, and P's one migrated main call
removes the final exact key to 28. Common boundary/cache/source/history semantics, scanner, fixed ceiling,
digests and source-command options remain frozen. No held B reader or archive-source/check implementation is
imported.
RV-3099: recorded privately
RV-3003/RV-3004: recorded privately

B final NOT READY `99968f2`, Reviewed `eabbeef`, leaves RV-3092–RV-3094 P2 HELD after exhausted final rounds.
Structural XML text/tails can corrupt blame, pending Shipped status and log proof. The outside structural
validation proposal has 293/293 development checks versus 243/293 before, plus 538 real-read scenarios with
zero write opens. Its five reader changes and pure validator preserve the frozen common contract and forty
keys. The board asks for Owner disposition; no production repair, third verification or replacement finding.

Archive/common final NOT READY `eabee22`, Reviewed `284a4e8`, closes RV-3071 and leaves RV-3072 HELD after
its final round. The outside strict-classification proposal has 28/28 development checks versus 14/28 before,
changing only archive_source with the frozen command preserved. Unknown/translated diagnostics refuse;
native layout qualification remains due. Archive activation awaits Owner disposition. The earlier combined
`fm/044-stage-entry-integration` retains held archive ancestry and is not a local ready candidate.

Owner confirms no SVN consumer adoption proof exists. Full protected acceptance waits for an authenticating
consumer, recorded adoption and trial findings; held rulings return 20 October. Local CLI/board/init/install
continues without a policy anchor, authority substitute, new rights or blanket ordinary-operation refusal.
Native/full CI, protected-request/past-policy proof and actual release remain held or due. Claude covers
today's critical builds. Push DISABLED; Owner fetches, pushes and opens/merges PRs.

## Why

FM-003's S1 claims that a Subversion working copy "with no git at all" runs `--init`, `--new`, the gate, `INDEX.md`, the
board and `--triage`. Its check builds that working copy on a machine where `git` is installed, so the claim fails
exactly where a Subversion team has no `git`.

**Historical ruling, 2026-10-08.** The Owner ruled that Subversion and a plain folder are lanes of their own, and
neither ever needs `git`. The fix is a version-control abstraction layer, not one-line refusals, designed before
anything is built, and it comes before the probe's next version. Ruling 1's 'git required on every machine' is withdrawn
everywhere. R23 and FM-023's signed release allocation now bound the build to Subversion without git and the archive;
the older plain-folder and all-five-platform proof acceptance has been superseded by the D3/D4 holds.

## Done when

- **Stage 1's layer.** The tool reaches version control through one abstraction layer in `shoalmark.py`, dispatching
  Git and Subversion once per repository. Plain-folder scope remains held under D3.
- **Subversion never starts `git`.**
  - Shared tracker operations work in a Subversion working copy with no git installed.
  - Git-only operations, including signed answer branches and the pull-request queue, refuse in one line.
  - No supported Subversion run stops with a traceback or tells a person to install `git`.
- **No backend judges less.**
  - The write rule, the guard and the judgement of the tracker folder fail closed.
  - The board starts only read-only commands and asks no server on Subversion as on Git.
- **A ratchet check** finds every `git` or `svn` process started outside the layer and fails on any not on its list.
  The list may only shrink.
- **The bounded proof:**
  - Existing Git acceptance and all five code-suite CI jobs/check names are retained under R25.
  - Subversion acceptance establishes operation without git installed; D4 still holds the choice of platforms on
    which that proof must run, so this filing claims no completed platform trial.
  - FM-045's relevant board matrix covers Git and Subversion; plain-folder coverage waits for D3.
- **Fetching without `git`:** the release archive supplies the tool and archive vendoring with its SHA-256 and RELEASE
  manifest. The pending scoped archive re-review, stage-1 integration, release-script change and dry run remain due.
- **README and ADOPT** explain the supported Git/Subversion paths and the held plain-folder scope.

## Ship log

| Date | Event |
|---|---|
| 2026-10-15 08:11 CEST | Owner PR #173 CI run `38614474342` at `3932e7f`: Linux and macOS green; on Windows 3.12 `test_core.py` failed the launch ceiling under a CRLF checkout and ended in a traceback, and Windows 3.9's FM-039 board render timed out — and cost the Owner a CI run. Third fix round, Owner-approved: `-text` for the two pinned launch files (RV-3250); RV-3088's history checks catch `RatchetHistoryError` alone, on their own line (RV-3251). A macOS CRLF clone reproduces CI's six FAIL lines and the traceback at `3932e7f` and is all green corrected; RV-3252 stays the Owner's. The Reviewer's critical pass, then one Owner CI run, remain due. |
| 2026-10-14 19:02 CEST | Owner PR #173 CI run `38589202689` at `46f8732`: Linux and macOS green, `test_core.py` included; both Windows jobs ran the suite to its end with 5 FAIL and skipped `test_core.py` — and cost the Owner a CI run. Second fix round, Owner-approved: A1's board link and reconfigure checks compare as the product spells paths (RV-3230, RV-3231); `svn_local_properties` returns `svn:` values with LF as stored, which Windows' `proplist --xml` prints with CRLF (RV-3232, the one product change); the POSIX-shell CLI test skips by name on Windows (RV-3233); the differential clears Git's read-only bit before removing (RV-3234). Each control fails on `46f8732` and passes corrected; the stage tail gives 619/619. The Reviewer's critical pass, then one Owner CI run, remain due. |
| 2026-10-14 13:46 CEST | Owner PR #173 CI run `38539381661` at `d0f0f24` failed — FAILED: 6, 4 and 4 on ubuntu 3.9, ubuntu 3.12 and macOS 3.12, and both Windows jobs ended in A1's setup traceback — and cost the Owner a CI run. Fix round: nine checks expect the copied commands as `printed_arg` spells them; `init` refuses a folder name with a line break before its first metadata read; A1's Windows search folder names svn as `svn.exe`, and a failed fixture step is a named FAIL; 3.9's tempdir probe is admitted in its exact shape. Focused blocks fail on `d0f0f24` and pass corrected; the stage tail gives 619/619 and unchanged core 303/303. The Reviewer's first critical pass, then one Owner CI run, remain due. |
| 2026-10-14 10:09 CEST | The Owner's order on PR #173: the suite's in-process `run` returns a refusal as the program ends — exit status and both streams — so its check fails and the suite goes on. Its regression fails with the old helper (the child suite exits 4) and passes corrected; unchanged core 303/303 passes. Independent critical review, then one Owner CI run, remain due; earlier verdicts and holds stand. |
| 2026-10-14 09:20 CEST | Owner PR #173 CI at `2dbaa80` stopped with exit 4 on old suite fixtures: an empty `.svn`, a board run assumed to start no `svn`, fake Tortoise paths. Four checks are corrected, test-only: their focused blocks fail on `2dbaa80` and pass corrected; unchanged core 303/303 passes. Independent critical review and native CI on the Owner's push remain due; earlier verdicts and holds stand. |
| 2026-10-13 22:21 CEST | P first critical NOT READY `62ecf9c`, Reviewed `de17860`; RV-3098 source-binding correction and real controls are built. Current runtime 619/619 and unchanged core 303/303 pass. Sole final verification remains; component verdicts and exhausted B/archive/protected holds stand. |
| 2026-10-13 21:30 CEST | A caller final READY `4ab9341` closes RV-3096; ordinary local composition retains its exact functions and all parent reductions, leaving 28 keys. Actual local runtime 527/527 and unchanged core 303/303 pass. P critical review remains next; exhausted B/archive and protected-consumer holds remain. |
| 2026-10-13 20:36 CEST | B final NOT READY `99968f2` leaves RV-3092–RV-3094 HELD with final rounds exhausted; disposition ask proposes holding the readers and preparing structural validation outside. A caller `43b5600` is in its separate critical review; C is locally composed. Archive final hold remains separate; local entry/notice work continues. |
| 2026-10-13 20:08 CEST | Archive final NOT READY `eabee22`: RV-3071 CLOSED, RV-3072 HELD after the final round; strict-classification disposition proposed on the board. A1/A2 accepted component merged locally; C bounded READY `f59a1c1`; B final review and A caller migration continue. Local stage work proceeds separately; protected acceptance remains held. |
| 2026-10-13 19:48 CEST | R12 merged on current main `3cac843`; local entry branch incorporates it with generated INDEX, compile/core and affected R14 gate passing. A1/A2 critical READY closes RV-3089–RV-3091; B and C corrections/final reviews and archive final review continue. P prepares actual preflight/once limitation/Tortoise entries; protected acceptance stays held under Owner clarification. |
| 2026-10-13 18:48 CEST | RV-3003/RV-3004: recorded privately |
| 2026-10-13 18:18 CEST | Accepted common dispatch records READY `84c8a6b` retained; RV-3057 P3 corrected forward. A/B/C first bounded commits are moving in exclusive branches; P archive integration retains common guards and source confinement, with compile/302 core/55 archive controls passing. Separate affected integration review and full Stage 1 remain due. |
| 2026-10-13 17:42 CEST | **Common critical READY and dependent dispatch:** independent `ef77527` closes RV-3085–RV-3088, COMMON SKELETON ONLY. Ordinary #170 merge `1fc12b0` preserves the exact product; clean gate and all 26 ratchet controls pass. A/B/C receive exclusive bounded tasking; Planner owns serial integration. Full Stage 1, protected SVN acceptance and CI remain due. |
| 2026-10-13 | Independent records verdict ce014e4 merged in Owner PR #167 at e6d1e27; command-applied triage keeps P1 #3 build, and the seat sets In Progress before the common skeleton. Bounded Builder/dependent-seat brief recorded, with guard contract and D3/D4 holds explicit; no implementation or proof claimed. |
| 2026-10-08 | Filed, for 0.19.2. |
| 2026-10-13 | Filing recovered from `99050b9` on current main; RV-2735–RV-2737 fixed, acceptance bounded to signed R23 and FM-023, records review next. |
| 2026-10-13 | FM-044 common-layer neutral refactor: only git_out/svn_run launch mechanics moved behind vcs_process. Immutable-parent/refactor wrapper contracts and real Git/SVN positive/refusal fixtures pass; compile and test_core pass; metadata dispatch, ratchet, independent critical review and dependent migrations remain due. |
| 2026-10-13 | FM-044 bounded skeleton dispatch built after neutral refactor 4f1664d: cached ROOT selection, no-process SVN metadata, fail-closed administrative paths and constrained target/source process requests. Compile and 243 core checks pass; 63 retained direct starts and exact scanner/proof limits declared. Independent critical review next; dependent migrations, archive integration, CI and platform decisions remain due. |
| 2026-10-13 | Integrated only immutable current-main #168 records at ab7ed3f by ordinary local merge before the critical handoff, retaining the exact 6f00764 product blobs, command-applied FM-004 judgement, main's signed records and FM-044 implementation evidence; INDEX regenerated. |
| 2026-10-13 | Fixed forward round-1 RV-3085–RV-3088 after released e511d57: node-identity/class-scoped scanner, pre-fallible repository invalidation, original-path/canonical-HERE source confinement and complete checked reachable parent transitions with deliberate proof failures. Compile and 302 core checks pass; 59 targeted controls contrast 17 pass/42 fail on immutable 6d0c239 with 59 pass on the fix. Ceiling/list unchanged; critical verification remains due and dependent code held. |
| 2026-10-13 | Integrated only independently READY planning records 6134fae after corrective product 049637c by ordinary local merge. Retained all product/control/list/ceiling blobs and signed records/judgements exactly; exclusive dependent function/test ownership and current holds retained; INDEX regenerated. No dependent code or acceptance verdict supplied. |
