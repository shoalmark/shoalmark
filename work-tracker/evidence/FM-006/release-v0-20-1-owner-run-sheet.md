# v0.20.1 — the Owner's run sheet, up to the merge

Run these blocks in the Owner's zsh shell on macOS, from the release clone. Replace the quoted placeholders first. A failed command or an unexpected result stops that step: paste it back before continuing. Only the Owner pushes, merges, signs and publishes.

This sheet stops at the merge. The tag is the Owner's own signed act, and the steps after it are in [the after-the-tag sheet](release-v0-20-1-after-the-tag.md).

**Main is frozen from the release pull request's opening until the switch commit's merge**, answer branches included. ADOPT's pins follow the tag: up to the tagged commit the notes pin v0.20.0, and every commit after it on main must pin v0.20.1. The switch commit is the first such commit, so any other merge between the tag and the switch would turn ADOPT's pin check red on main and on every branch cut from it.

Sources: [CHANGELOG.md](../../../CHANGELOG.md), [the archive builder](../../../scripts/build_release_archive.py), [release.yml](../../../.github/workflows/release.yml), [ADOPT.md's pin line](../../../ADOPT.md), [the pin test's order, `_pinned_release`](../../../test_shoalmark.py), and [the merge rule](../../TRIAGE.md#the-current-path).

## 1. The final head, the one the release review judges

The release review's verdict names the commit it judged. Any verdict commit on top of it has the same tree. Keep the three full SHAs beside the required check results.

```sh
RELEASE_HEAD='REPLACE_WITH_THE_40_HEX_HEAD_OF_RELEASE_V0.20.1' &&
REVIEWED_HEAD='REPLACE_WITH_THE_40_HEX_COMMIT_THE_REVIEW_JUDGED' &&
REVIEW_COMMIT='REPLACE_WITH_THE_40_HEX_READY_VERDICT_COMMIT' &&
git fetch origin --tags &&
test "$(git rev-parse release/v0.20.1)" = "$RELEASE_HEAD" &&
git merge-base --is-ancestor origin/main "$RELEASE_HEAD" &&
git show -s --format=full "$REVIEW_COMMIT" &&
git diff --exit-code "$REVIEWED_HEAD" "$RELEASE_HEAD" &&
git diff --exit-code "$REVIEW_COMMIT" "$RELEASE_HEAD" &&
test "$(git show "$RELEASE_HEAD:VERSION")" = '0.20.1' &&
git show "$RELEASE_HEAD:ADOPT.md" | grep '^The pin: release `v0.20.0`' &&
python3 shoalmark.py --check &&
printf '%s\n' 'OK: the final head holds main, its tree is the one the review judged, VERSION is 0.20.1 and ADOPT still pins v0.20.0'
```

**Expect:** the release head holds main, and both tree comparisons are empty. The verdict reads READY and names its reviewed commit, base, critical tier and checks in `Reviewed:`. VERSION reads `0.20.1`, while ADOPT's pin line still names `v0.20.0`: the release keeps the earlier pin until the switch commit. `--check` exits 0. The board alone is never permission to merge.

**Paste back:** the three full SHAs, the verdict's subject and `Reviewed:` line, the pin line `grep` printed, and the `OK:` line.

## 2. Push, open the release pull request, and freeze main

```sh
git push -u origin release/v0.20.1 &&
MAIN_AT_OPEN="$(git rev-parse origin/main)" &&
gh pr create --base main --head release/v0.20.1 --title '0.20.1' --body-file - <<BODY &&
Prepares v0.20.1. Upgrade, then run --install-hook again in every committing clone (the refresh hooks come back), and run --check.

Changes and upgrade lines: [CHANGELOG.md at this head](https://github.com/shoalmark/shoalmark/blob/$RELEASE_HEAD/CHANGELOG.md). Publication steps: [the Owner's run sheet](https://github.com/shoalmark/shoalmark/blob/$RELEASE_HEAD/work-tracker/evidence/FM-006/release-v0-20-1-owner-run-sheet.md) and [the after-the-tag sheet](https://github.com/shoalmark/shoalmark/blob/$RELEASE_HEAD/work-tracker/evidence/FM-006/release-v0-20-1-after-the-tag.md).

ADOPT's pins stay on v0.20.0 in this release: the pin follows the tag, and one commit on main after the release is published moves it to v0.20.1.

Merge only with the critical READY on the final tree and every required check green. Main stays frozen from this pull request's opening until that switch commit's merge.
BODY
RELEASE_PR="$(gh pr view release/v0.20.1 --json number --jq .number)" &&
gh pr view "$RELEASE_PR" --json url,headRefOid,baseRefName,isDraft &&
printf '%s\n' "$MAIN_AT_OPEN"
```

**Expect:** one ready pull request to main at `RELEASE_HEAD`. Its opening runs the required CI matrix once on this revision. Main is frozen from now until the switch commit's merge.

**Paste back:** the pull request's URL, its head SHA and `MAIN_AT_OPEN`.

## 3. The dry run: release.yml with the head's 40-hex commit

```sh
test "$(git ls-remote origin refs/heads/release/v0.20.1 | cut -f1)" = "$RELEASE_HEAD" &&
gh workflow run release.yml --ref release/v0.20.1 -f "ref=$RELEASE_HEAD" &&
gh run list --workflow release.yml --commit "$RELEASE_HEAD" --event workflow_dispatch --limit 5 --json databaseId,headSha,status,conclusion,url
```

```sh
DRY_RUN_ID='REPLACE_WITH_THE_DRY_RUN_ID' &&
gh run watch "$DRY_RUN_ID" --exit-status &&
DRY_DIR="$(mktemp -d)" &&
gh run download "$DRY_RUN_ID" --name release-archive --dir "$DRY_DIR" &&
(cd "$DRY_DIR" && shasum -a 256 -c shoalmark-0.20.1.zip.sha256)
```

**Expect:** `release.yml` takes the full 40-hex SHA as its `ref` input, keeps `release-archive` as the run's artifact and attaches nothing to a release. The dry run succeeds, and the checksum verifies. Its `RELEASE` file says `tag none`, so compare its bytes only with another build of the same commit, never with the tag's build.

**Paste back:** the run's URL, its `headSha` and id, the conclusion, and the checksum line.

## 4. The sitting: the public step, then the CHANGELOG commit

The sitting's public step runs by the Auditor's run sheet, not this one. Then the release Builder adds one commit on `release/v0.20.1`: the CHANGELOG lines that step brings. That commit gets its own check before the merge.

```sh
FINAL_HEAD='REPLACE_WITH_THE_40_HEX_CHANGELOG_COMMIT' &&
test "$(git rev-parse release/v0.20.1)" = "$FINAL_HEAD" &&
test "$(git rev-parse "$FINAL_HEAD^")" = "$RELEASE_HEAD" &&
git diff --stat "$RELEASE_HEAD" "$FINAL_HEAD" &&
git push origin release/v0.20.1 &&
gh pr view "$RELEASE_PR" --json headRefOid --jq .headRefOid
```

**Expect:** the CHANGELOG commit sits directly on `RELEASE_HEAD`, and its diff names `CHANGELOG.md` alone. After the push, the pull request's head is `FINAL_HEAD`, and the required CI matrix runs on it. The commit's check names `FINAL_HEAD`, or a verdict commit with the same tree.

**Paste back:** `FINAL_HEAD`, the diff's one line, and the check's verdict subject and `Reviewed:` line.

## 5. The merge, only on READY and every required check green

```sh
CHECK_COMMIT='REPLACE_WITH_THE_40_HEX_VERDICT_COMMIT_OF_THE_CHANGELOG_CHECK' &&
gh pr checks "$RELEASE_PR" --required --watch &&
MERGE_HEAD="$(gh pr view "$RELEASE_PR" --json headRefOid --jq .headRefOid)" &&
git fetch origin &&
git diff --exit-code "$FINAL_HEAD" "$MERGE_HEAD" &&
git show -s --format=full "$CHECK_COMMIT" &&
test "$(git ls-remote origin refs/heads/main | cut -f1)" = "$MAIN_AT_OPEN" &&
gh pr merge "$RELEASE_PR" --merge --match-head-commit "$MERGE_HEAD" &&
MERGE_SHA="$(gh pr view "$RELEASE_PR" --json mergeCommit --jq .mergeCommit.oid)" &&
git fetch origin &&
test "$(git rev-parse origin/main)" = "$MERGE_SHA" &&
git log -1 --format='%H %s' "$MERGE_SHA"
```

**Expect:** every required check is green, the release review is READY on `RELEASE_HEAD`'s tree and the CHANGELOG commit's check is READY on `FINAL_HEAD`'s. Verify both verdicts yourself before the merge command; never infer them from the board or CI. Main has not moved since the pull request opened. GitHub makes the merge commit, and `origin/main` is that commit.

**Paste back:** the check results, both verdicts' subjects and `Reviewed:` lines, the merged pull request's URL, and `MERGE_SHA` with its subject.

The tag is yours: read the merge commit on GitHub, then sign it with `git tag -s`.
