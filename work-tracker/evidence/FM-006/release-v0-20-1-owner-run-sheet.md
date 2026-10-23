# v0.20.1 — the Owner's run sheet, up to the merge

Run these blocks in the Owner's zsh shell on macOS, from the release clone. Replace the quoted placeholders first. A failed command or an unexpected result stops that step: paste it back before continuing. Only the Owner pushes, merges, signs and publishes.

The release goes up in one push and one CI run: the final local head of `release/v0.20.1`, its pull request, and the merge. This sheet stops at the merge. The tag is the Owner's own signed act, and the steps after it are in [the after-the-tag sheet](release-v0-20-1-after-the-tag.md).

**Main is frozen from the push of step 2 until the `docs.yml` run from the switch commit has deployed, to GitHub Pages and to Cloudflare**, answer branches included. ADOPT's pins follow the tag: up to the tagged commit the notes pin v0.20.0, and every commit after it on main must pin v0.20.1. The switch commit is the first such commit, so any other merge between the tag and the switch would turn ADOPT's pin check red on main and on every branch cut from it. Until that `docs.yml` run, any merge would also change what it deploys.

Sources: [CHANGELOG.md](../../../CHANGELOG.md), [ADOPT.md's pin line](../../../ADOPT.md), [the pin test's order, `_pinned_release`](../../../test_shoalmark.py), and [the merge rule](../../TRIAGE.md#the-current-path).

## 1. The final local head of `release/v0.20.1`

Every lane has joined `release/v0.20.1` locally, and the release commit is on it. This head is the one the critical review judges, and the one that is pushed.

```sh
RELEASE_HEAD='REPLACE_WITH_THE_40_HEX_FINAL_LOCAL_HEAD_OF_RELEASE_V0.20.1' &&
git fetch origin --tags &&
test "$(git rev-parse release/v0.20.1)" = "$RELEASE_HEAD" &&
git merge-base --is-ancestor origin/main "$RELEASE_HEAD" &&
test "$(git show "$RELEASE_HEAD:VERSION")" = '0.20.1' &&
git show "$RELEASE_HEAD:CHANGELOG.md" | grep '^## 0\.20\.1 — ' &&
git show "$RELEASE_HEAD:ADOPT.md" | grep '^The pin: release `v0.20.0`' &&
python3 shoalmark.py --check &&
printf '%s\n' 'OK: the final local head holds main, VERSION is 0.20.1 with its CHANGELOG section, and ADOPT still pins v0.20.0'
```

**Expect:** the release head holds main. VERSION reads `0.20.1`, and CHANGELOG has its `0.20.1` section. ADOPT's pin line still names `v0.20.0`: the release keeps the earlier pin until the switch commit. `--check` exits 0.

**Paste back:** `RELEASE_HEAD`, the CHANGELOG heading and the pin line `grep` printed, and the `OK:` line.

## 2. The one push, the release pull request, and the freeze

```sh
git push -u origin release/v0.20.1 &&
MAIN_AT_PUSH="$(git rev-parse origin/main)" &&
gh pr create --base main --head release/v0.20.1 --title '0.20.1' --body-file - <<BODY &&
Prepares v0.20.1. Upgrade, then run --install-hook again in every committing clone (the refresh hooks come back), and run --check.

Changes and upgrade lines: [CHANGELOG.md at this head](https://github.com/shoalmark/shoalmark/blob/$RELEASE_HEAD/CHANGELOG.md). Publication steps: [the Owner's run sheet](https://github.com/shoalmark/shoalmark/blob/$RELEASE_HEAD/work-tracker/evidence/FM-006/release-v0-20-1-owner-run-sheet.md) and [the after-the-tag sheet](https://github.com/shoalmark/shoalmark/blob/$RELEASE_HEAD/work-tracker/evidence/FM-006/release-v0-20-1-after-the-tag.md).

ADOPT's pins stay on v0.20.0 in this release: the pin follows the tag, and one commit on main after the release is published moves it to v0.20.1.

Merge only with the critical READY on the final tree and every required check green. Main stays frozen from this push until the docs.yml run from that switch commit has deployed, to GitHub Pages and to Cloudflare.
BODY
RELEASE_PR="$(gh pr view release/v0.20.1 --json number --jq .number)" &&
gh pr view "$RELEASE_PR" --json url,headRefOid,baseRefName,isDraft &&
printf '%s\n' "$MAIN_AT_PUSH"
```

**Expect:** one ready pull request to main at `RELEASE_HEAD`. Main is frozen from this push.

**Paste back:** the pull request's URL, its head SHA and `MAIN_AT_PUSH`.

## 3. The dry run: release.yml with the pushed head's 40-hex commit

It proves that the archive builds from the pushed head before the tag exists.

```sh
test "$(git ls-remote origin refs/heads/release/v0.20.1 | cut -f1)" = "$RELEASE_HEAD" &&
gh workflow run release.yml --ref release/v0.20.1 -f "ref=$RELEASE_HEAD" &&
sleep 15 &&
DRY_RUN_ID="$(gh run list --workflow release.yml --event workflow_dispatch --commit "$RELEASE_HEAD" --limit 1 --json databaseId --jq '.[0].databaseId')" &&
gh run watch "$DRY_RUN_ID" --exit-status &&
gh run view "$DRY_RUN_ID" --json url,headSha,conclusion &&
DRY_DIR="$(mktemp -d)" &&
gh run download "$DRY_RUN_ID" --name release-archive --dir "$DRY_DIR" &&
(cd "$DRY_DIR" && shasum -a 256 -c shoalmark-0.20.1.zip.sha256) &&
unzip -p "$DRY_DIR/shoalmark-0.20.1.zip" RELEASE | grep -x 'tag none'
```

**Expect:** `release.yml` takes the full 40-hex SHA as its `ref` input, runs on `RELEASE_HEAD` and succeeds. It keeps `release-archive` as the run's artifact and attaches nothing to a release. The checksum verifies. The archive's `RELEASE` says `tag none`, so compare its bytes only with another build of the same commit, never with the tag's build.

**Paste back:** the run's URL, its `headSha` and conclusion, the checksum line, and the `tag none` line.

## 4. The one CI run

```sh
gh pr checks "$RELEASE_PR" --required --watch &&
test "$(gh pr view "$RELEASE_PR" --json headRefOid --jq .headRefOid)" = "$RELEASE_HEAD"
```

**Expect:** the pull request's opening runs the required CI matrix once, on `RELEASE_HEAD`, and every required check is green. Nothing is pushed to the branch after it.

**Paste back:** the check results.

## 5. The merge, only on the critical READY and every required check green

The critical review's verdict names the commit it judged, and its tree must be `RELEASE_HEAD`'s.

```sh
REVIEWED_HEAD='REPLACE_WITH_THE_40_HEX_COMMIT_THE_CRITICAL_REVIEW_JUDGED' &&
REVIEW_COMMIT='REPLACE_WITH_THE_40_HEX_READY_VERDICT_COMMIT' &&
git show -s --format=full "$REVIEW_COMMIT" &&
git diff --exit-code "$REVIEWED_HEAD" "$RELEASE_HEAD" &&
test "$(git ls-remote origin refs/heads/main | cut -f1)" = "$MAIN_AT_PUSH" &&
gh pr merge "$RELEASE_PR" --merge --match-head-commit "$RELEASE_HEAD" &&
MERGE_SHA="$(gh pr view "$RELEASE_PR" --json mergeCommit --jq .mergeCommit.oid)" &&
git fetch origin &&
test "$(git rev-parse origin/main)" = "$MERGE_SHA" &&
git log -1 --format='%H %s' "$MERGE_SHA"
```

**Expect:** the verdict reads READY and names its reviewed commit, base, critical tier and checks in `Reviewed:`. The reviewed tree is `RELEASE_HEAD`'s. Verify the verdict yourself before the merge command; never infer it from the board or CI. Main has not moved since the push. GitHub makes the merge commit, and `origin/main` is that commit.

**Paste back:** the verdict's subject and `Reviewed:` line, the merged pull request's URL, and `MERGE_SHA` with its subject.

The tag is yours: read the merge commit on GitHub, then sign it with `git tag -s`.
