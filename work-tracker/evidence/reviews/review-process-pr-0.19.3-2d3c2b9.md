# FM-032: the process PR after 0.19.3, the review at 2d3c2b9

Verdict: **READY WITH FINDINGS**. RV-2965 to RV-2969 are fixed, and one P3 stands: RV-2970. No P1 and no P2 stand.
Reviewed: 2d3c2b9549e99b465ec05b6570b43487da2ea452, `git diff origin/main 2d3c2b9`, origin/main being 3432566 (v0.19.3). Tier: critical, the full loop; it changes what the five required checks run. 2d3c2b9's tree is cf55f92c, the tree of the head as reviewed at 2c5a59a, and each rebuilt commit keeps its predecessor's tree.

## What holds
- **The tier step.** It reads the merge CI tests: its first parent must be the event's base and its second the head. It then diffs that merge against the base with `--no-renames --ignore-submodules=none`, in `LC_ALL=C` and without regard to case.
- **What counts as records.** A pull request is records-only where every entry is a regular file at mode 100644, added, changed or deleted, and is a top-level `*.md` of the tracker folder or a file under evidence/ that no suite reads. Everything else gives the full suites: a gitlink, a symlink, a mode change, `.gitmodules` or `.github/` anywhere, a non-ASCII byte, a Windows short name, any other path, an empty list, a failed command, a tag, a run by hand. The shas come in through `env:`.
- **The five check names are unchanged.** Records-only runs `--check` inside them, with the signers file named.
- **The time zones.** Pacific/Kiritimati runs on Ubuntu 3.9 and Pacific/Pago_Pago on 3.12, as `continue-on-error` steps after the UTC suites. Each writes a summary line, and records-only skips them.
- **The pins.** Both pins are `42ec6aa1…0b31`, the SHA-256 of `git show v0.19.3:shoalmark.py`. The pin check holds both notes to VERSION's tag and that tag's tool, and to the head's tool before the tag exists. shoalmark.py is byte-identical to v0.19.3's.
- **The records.** The independent files at 6828dba and 82edbf5 are byte-identical to the Owner's copies. Private items appear only as "recorded privately", and no GHSA id appears.

## The findings, and how each was fixed
- RV-2965 · P1: fixed in 1211347. The step now reads the merge CI tests, so a criss-crossed history that drops a fix gives the full suites in both date orders.
- RV-2966 · P1: fixed in 2db45d8. Paths compare without regard to case, and a non-ASCII path gives the full suites.
- RV-2967 · P2: fixed in 663b987. The suite writes the step's script as bytes, so Windows' bash reads it.
- RV-2968 · P3: fixed in dd4f783. A Windows short name gives the full suites.
- RV-2969 · P3: fixed in 2d3c2b9. FM-006 and FM-032 say what the pin check and the tier step hold.
- **RV-2970 · P3 · records.** Since the rebuild, FM-032's CI-tiers line and its 04:15 row, and the messages of e8eab6b and 2d3c2b9, name 41b1659, 36b3fa1, 4f90688, 9e7fc4a and 49e7831, which are not on the branch. Fix forward: in the next records change, a row in FM-032's ship log names each as the commit it became — 66ddd25, e8eab6b, 2db45d8, 663b987 and dd4f783.

## The controls
- The ci.yml check has 17 properties, 33 controls that fail and 2 that pass.
- The pin check has six controls: 3432566 fails with its tag and without it; v0.19.0, v0.19.1 and v0.19.2 pass, as does a head with a later tool.
- The step's own shell was run on each shape (03:01:41–03:02:35, 04:00:13–04:00:43, 04:21:27). Every shape gives the full suites except the tracker-only edit, INDEX.md and TRIAGE.md, and evidence no suite reads; this covers renames, deleted gitlinks, mode changes, symlinks, `.gitmodules`, a changed `tracker_dir`, case variants and short names.
- A merge GitHub authored gives `--check` 0 for a green record and 4 for a red one (04:08:29–04:08:40).

## Commands: 2026-10-11, CEST, as `date` printed each
- At 2d3c2b9: py_compile under 3.14.8 and 3.9.6, test_core all green, `--check` and `--session-check` exit 0 (09:16:32–09:16:56).
- run-one-check at 2d3c2b9: the ci.yml block passed 52 checks (09:16:32–09:19:55), and the pin block 7 (09:16:32–09:17:20).
- Earlier passes: 39b3e15 (03:01), 4f90688 (03:59–04:08) and 2c5a59a (04:21–04:25), the last with the same tree.

Quality read: the comments, check names and records claim only what holds, with the one exception RV-2970.
