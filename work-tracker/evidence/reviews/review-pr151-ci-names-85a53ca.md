# FM-006: PR 151, the CI names, the review as merged at 85a53ca

Verdict: **READY WITH FINDINGS**: one P3, RV-2755; no P1, no P2.
Reviewed: 85a53caec3b43aca5d1a11fdc78ae327e9ca7a8c, `git diff f84ad4a 85a53ca`: one commit, 9c89c0d, against the Owner's rulings (the five checks named by OS family, each image pinned in `runs-on`, the pin held until 0.19.3). Tier: code (`git diff --name-only`: `.github/workflows/ci.yml`, `.github/workflows/docs.yml`). Scope: the job's name, the matrix, `runs-on` in both workflows, the runs, and the records.

## What holds

- The names: the matrix expands to exactly `suites (ubuntu, 3.9)`, `suites (ubuntu, 3.12)`, `suites (macos, 3.12)`, `suites (windows, 3.9)` and `suites (windows, 3.12)`, which are the five checks that main's ruleset requires.
- The images: run 37723667636 is the last ci run before PR 151's, and its jobs ran on ubuntu-24.04 (20260927.320.1, 20261004.327.1), macos-26-arm64 (20260907.0351.1) and windows-2025-vs2026 (20260925.250.1). In actions/runner-images' README (a99056a), `ubuntu-24.04`, `macos-26` and `windows-2025-vs2026` are labels of those three images: Ubuntu 24.04 x64, macOS 26 Arm64 and Windows Server 2025.
- Nothing else: the diff changes only `name:`, one comment, the five rows (same order) and `runs-on` in ci.yml, and the two `runs-on` lines in docs.yml. The steps, which key on `runner.os`, and `if:`, `on:`, the permissions and the concurrency are unchanged.
- The runs: `gh pr checks 151` shows the five suites passing under the new names in run 37741941703, on the pinned images. Four later pull-request runs (37746189041, 37746223795, 37746260913 and 37746496112) carry the same five names. 85a53ca's tree is 9c89c0d's (007bd9e).
- docs.yml: `build` and `deploy` both run on `ubuntu-24.04`. No docs run has started since the merge; the newest, 37726599002 at f84ad4a, succeeded with both jobs on image ubuntu-24.04.
- Records: CHANGELOG, README and AGENTS name no current check name. `CHANGELOG.md:529`, `:539` and `:543` name the runners of 0.18.x's runs, as history.

## Findings

- **RV-2755 · P3 · configuration comment:** the two pins in docs.yml carry no word that they hold until 0.19.3; the comment at `ci.yml:17` is the only record of that end, and it covers only ci.yml's images. Fix: add `# The image is pinned until 0.19.3, as ci.yml's are.` above `jobs:` (`docs.yml:10`).

## Commands and controls: 2026-10-08, CEST, as `date` printed each

- The matrix expanded by a short script: 85a53ca's equals the five ruled names, exit 0. Control: f84ad4a's expansion equals run 37723667636's five job names, `suites (ubuntu-latest, 3.9)` and the rest (10:06:37–10:06:39).
- `gh run view 37723667636 --log`, read for its Runner Image groups (10:02:23). `gh api repos/actions/runner-images/readme`, exit 0 (10:02:47). `gh pr checks 151`: nine pass, five of them suites, exit 0 (10:02:54). Four later runs' jobs read with `gh run view` (10:03:09). `gh run list --workflow docs.yml` (10:03:33). `git grep` for the old names (10:03:44). `gh api repos/shoalmark/shoalmark/rules/branches/main`: exit 0, the five names (10:03:57).
- `--check` exit 0 and `--session-check` exit 0, with this file in place, before the commit (10:08:25–10:08:33).

Quality read: the defect is RV-2755; the rest reads clean.
