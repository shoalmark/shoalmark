# v0.20.1 — the Owner's run sheet, up to the merge

Run these blocks in the Owner's zsh shell on macOS, from the release clone, one block at a time. Each block pastes as it stands: it reads what it needs from git and gh, and where a value must come from you, such as a commit a verdict names or a value an earlier step printed, it asks with `read -r` and checks the answer before it uses it. A failed command or an unexpected result stops that step: paste it back before continuing. Only the Owner pushes, merges, signs and publishes.

Every git command here that reaches the network names the repository's HTTPS address and runs with gh's credential helper alone, set for that command only, and never asks at the terminal. No configuration file is changed.

The release goes up in one push and one CI run: the final local head of `release/v0.20.1`, its pull request, and the merge. This sheet stops at the merge. The tag is the Owner's own signed act, and the steps after it are in [the after-the-tag sheet](release-v0-20-1-after-the-tag.md).

**Main is frozen from the push of step 2 until the `docs.yml` run from the switch commit has deployed, to GitHub Pages and to Cloudflare**, answer branches included. ADOPT's pins follow the tag: up to the tagged commit the notes pin v0.20.0, and every commit after it on main must pin v0.20.1. The switch commit is the first such commit, so any other merge between the tag and the switch would turn ADOPT's pin check red on main and on every branch cut from it. Until that `docs.yml` run, any merge would also change what it deploys.

Sources: [CHANGELOG.md](../../../CHANGELOG.md), [ADOPT.md's pin line](../../../ADOPT.md), [the pin test's order, `_pinned_release`](../../../test_shoalmark.py), and [the merge rule](../../TRIAGE.md#the-current-path).

## 1. The final local head of `release/v0.20.1`

Every lane has joined `release/v0.20.1` locally, and the release commit is on it. This head is the one the critical review judges, and the one that is pushed. The block checks it in a clean, detached checkout of its own, with that checkout's own tool, and removes the checkout when it passes.

```sh
REPO='https://github.com/shoalmark/shoalmark.git' &&
G() { GIT_TERMINAL_PROMPT=0 git -c credential.helper= -c 'credential.helper=!gh auth git-credential' "$@"; } &&
read -r 'RELEASE_HEAD?The 40-hex final local head of release/v0.20.1, as it was handed to you: ' &&
[[ $RELEASE_HEAD =~ ^[0-9a-f]{40}$ ]] &&
test "$(git rev-parse --verify 'release/v0.20.1^{commit}')" = "$RELEASE_HEAD" &&
G fetch --tags "$REPO" '+refs/heads/main:refs/remotes/origin/main' &&
git merge-base --is-ancestor origin/main "$RELEASE_HEAD" &&
CHECK_DIR="$(mktemp -d)/release-head" &&
git worktree add --detach "$CHECK_DIR" "$RELEASE_HEAD" &&
test "$(git -C "$CHECK_DIR" rev-parse HEAD)" = "$RELEASE_HEAD" &&
test -z "$(git -C "$CHECK_DIR" status --porcelain --untracked-files=no)" &&
test "$(cat "$CHECK_DIR/VERSION")" = '0.20.1' &&
grep '^## 0\.20\.1 — ' "$CHECK_DIR/CHANGELOG.md" &&
grep '^The pin: release `v0.20.0`' "$CHECK_DIR/ADOPT.md" &&
python3 "$CHECK_DIR/shoalmark.py" --root "$CHECK_DIR" --check &&
git worktree remove "$CHECK_DIR" &&
printf '%s\n' "OK: $RELEASE_HEAD holds main, its own clean checkout passes --check, VERSION is 0.20.1 with its CHANGELOG section, and ADOPT still pins v0.20.0"
```

**Expect:** the release head holds main. Its own clean, detached checkout is at `RELEASE_HEAD` with no tracked change, and its tool's `--check` exits 0 there. VERSION reads `0.20.1`, and CHANGELOG has its `0.20.1` section. ADOPT's pin line still names `v0.20.0`: the release keeps the earlier pin until the switch commit.

**Paste back:** `RELEASE_HEAD`, the CHANGELOG heading and the pin line `grep` printed, and the `OK:` line.

## 2. The one push, the release pull request, and the freeze

```sh
REPO='https://github.com/shoalmark/shoalmark.git' &&
G() { GIT_TERMINAL_PROMPT=0 git -c credential.helper= -c 'credential.helper=!gh auth git-credential' "$@"; } &&
read -r 'RELEASE_HEAD?The 40-hex RELEASE_HEAD that step 1 checked: ' &&
[[ $RELEASE_HEAD =~ ^[0-9a-f]{40}$ ]] &&
test "$(git rev-parse --verify 'release/v0.20.1^{commit}')" = "$RELEASE_HEAD" &&
G push "$REPO" "$RELEASE_HEAD:refs/heads/release/v0.20.1" &&
MAIN_AT_PUSH="$(G ls-remote "$REPO" refs/heads/main | cut -f1)" &&
[[ $MAIN_AT_PUSH =~ ^[0-9a-f]{40}$ ]] &&
gh pr create --repo shoalmark/shoalmark --base main --head release/v0.20.1 --title '0.20.1' --body-file - <<BODY &&
Prepares v0.20.1. Upgrade, then run --install-hook again in every committing clone (the refresh hooks come back), and run --check.

Changes and upgrade lines: [CHANGELOG.md at this head](https://github.com/shoalmark/shoalmark/blob/$RELEASE_HEAD/CHANGELOG.md). Publication steps: [the Owner's run sheet](https://github.com/shoalmark/shoalmark/blob/$RELEASE_HEAD/work-tracker/evidence/FM-006/release-v0-20-1-owner-run-sheet.md) and [the after-the-tag sheet](https://github.com/shoalmark/shoalmark/blob/$RELEASE_HEAD/work-tracker/evidence/FM-006/release-v0-20-1-after-the-tag.md).

ADOPT's pins stay on v0.20.0 in this release: the pin follows the tag, and one commit on main after the release is published moves it to v0.20.1.

Merge only with the critical READY on the final tree and every required check green. Main stays frozen from this push until the docs.yml run from that switch commit has deployed, to GitHub Pages and to Cloudflare.
BODY
RELEASE_PR="$(gh pr view release/v0.20.1 --repo shoalmark/shoalmark --json number --jq .number)" &&
[[ $RELEASE_PR =~ ^[0-9]+$ ]] &&
test "$(gh pr view "$RELEASE_PR" --repo shoalmark/shoalmark --json headRefOid --jq .headRefOid)" = "$RELEASE_HEAD" &&
gh pr view "$RELEASE_PR" --repo shoalmark/shoalmark --json url,number,headRefOid,baseRefName,isDraft &&
printf '%s\n' "MAIN_AT_PUSH $MAIN_AT_PUSH"
```

**Expect:** one ready pull request to main at `RELEASE_HEAD`. Main is frozen from this push.

**Paste back:** the pull request's URL and number, its head SHA and `MAIN_AT_PUSH`.

## 3. The dry run: release.yml with the pushed head's 40-hex commit

It proves that the archive builds from the pushed head before the tag exists.

```sh
REPO='https://github.com/shoalmark/shoalmark.git' &&
G() { GIT_TERMINAL_PROMPT=0 git -c credential.helper= -c 'credential.helper=!gh auth git-credential' "$@"; } &&
read -r 'RELEASE_HEAD?The 40-hex RELEASE_HEAD that step 2 pushed: ' &&
[[ $RELEASE_HEAD =~ ^[0-9a-f]{40}$ ]] &&
test "$(G ls-remote "$REPO" refs/heads/release/v0.20.1 | cut -f1)" = "$RELEASE_HEAD" &&
gh workflow run release.yml --repo shoalmark/shoalmark --ref release/v0.20.1 -f "ref=$RELEASE_HEAD" &&
sleep 15 &&
DRY_RUN_ID="$(gh run list --repo shoalmark/shoalmark --workflow release.yml --event workflow_dispatch --commit "$RELEASE_HEAD" --limit 1 --json databaseId --jq '.[0].databaseId')" &&
[[ $DRY_RUN_ID =~ ^[0-9]+$ ]] &&
gh run watch "$DRY_RUN_ID" --repo shoalmark/shoalmark --exit-status &&
gh run view "$DRY_RUN_ID" --repo shoalmark/shoalmark --json url,headSha,conclusion &&
test "$(gh run view "$DRY_RUN_ID" --repo shoalmark/shoalmark --json headSha --jq .headSha)" = "$RELEASE_HEAD" &&
DRY_DIR="$(mktemp -d)" &&
gh run download "$DRY_RUN_ID" --repo shoalmark/shoalmark --name release-archive --dir "$DRY_DIR" &&
(cd "$DRY_DIR" && shasum -a 256 -c shoalmark-0.20.1.zip.sha256) &&
unzip -p "$DRY_DIR/shoalmark-0.20.1.zip" RELEASE | grep -x 'tag none'
```

**Expect:** `release.yml` takes the full 40-hex SHA as its `ref` input, runs on `RELEASE_HEAD` and succeeds. It keeps `release-archive` as the run's artifact and attaches nothing to a release. The checksum verifies. The archive's `RELEASE` says `tag none`, so compare its bytes only with another build of the same commit, never with the tag's build.

**Paste back:** the run's URL, its `headSha` and conclusion, the checksum line, and the `tag none` line.

## 4. The one CI run

```sh
read -r 'RELEASE_HEAD?The 40-hex RELEASE_HEAD that step 2 pushed: ' &&
[[ $RELEASE_HEAD =~ ^[0-9a-f]{40}$ ]] &&
RELEASE_PR="$(gh pr view release/v0.20.1 --repo shoalmark/shoalmark --json number --jq .number)" &&
[[ $RELEASE_PR =~ ^[0-9]+$ ]] &&
test "$(gh pr view "$RELEASE_PR" --repo shoalmark/shoalmark --json headRefOid --jq .headRefOid)" = "$RELEASE_HEAD" &&
gh pr checks "$RELEASE_PR" --repo shoalmark/shoalmark --required --watch &&
test "$(gh pr view "$RELEASE_PR" --repo shoalmark/shoalmark --json headRefOid --jq .headRefOid)" = "$RELEASE_HEAD"
```

**Expect:** the pull request's opening runs the required CI matrix once, on `RELEASE_HEAD`, and every required check is green. Nothing is pushed to the branch after it.

**Paste back:** the check results.

## 5. The merge, only on the critical READY and every required check green

The critical review's verdict names the commit it judged, and its tree must be `RELEASE_HEAD`'s. This step has two blocks. The first shows the verdict, the trees and main, and merges nothing. Read what it prints, and run the second block, which merges, only after that.

```sh
REPO='https://github.com/shoalmark/shoalmark.git' &&
G() { GIT_TERMINAL_PROMPT=0 git -c credential.helper= -c 'credential.helper=!gh auth git-credential' "$@"; } &&
read -r 'REVIEWED_HEAD?The 40-hex commit the critical review judged, as its verdict names it: ' &&
[[ $REVIEWED_HEAD =~ ^[0-9a-f]{40}$ ]] &&
read -r 'REVIEW_COMMIT?The 40-hex READY verdict commit: ' &&
[[ $REVIEW_COMMIT =~ ^[0-9a-f]{40}$ ]] &&
read -r 'MAIN_AT_PUSH?The 40-hex MAIN_AT_PUSH that step 2 printed: ' &&
[[ $MAIN_AT_PUSH =~ ^[0-9a-f]{40}$ ]] &&
RELEASE_PR="$(gh pr view release/v0.20.1 --repo shoalmark/shoalmark --json number --jq .number)" &&
[[ $RELEASE_PR =~ ^[0-9]+$ ]] &&
PR_HEAD="$(gh pr view "$RELEASE_PR" --repo shoalmark/shoalmark --json headRefOid --jq .headRefOid)" &&
[[ $PR_HEAD =~ ^[0-9a-f]{40}$ ]] &&
G fetch "$REPO" "+refs/heads/release/v0.20.1:refs/remotes/origin/release/v0.20.1" &&
git show -s --format=full "$REVIEW_COMMIT" &&
git diff --exit-code "$REVIEWED_HEAD" "$PR_HEAD" &&
test "$(G ls-remote "$REPO" refs/heads/main | cut -f1)" = "$MAIN_AT_PUSH" &&
printf '%s\n' "INSPECT: pull request $RELEASE_PR at $PR_HEAD, the reviewed tree equal to it, main still at $MAIN_AT_PUSH; nothing is merged yet"
```

**Expect:** the verdict reads READY and names its reviewed commit, base, critical tier and checks in `Reviewed:`. The reviewed tree is the pull request's head's, and main has not moved since the push. Verify the verdict yourself now; never infer it from the board or CI. Nothing is merged by this block.

**Paste back:** the verdict's subject and `Reviewed:` line, and the `INSPECT:` line.

Only once you have read it, the merge:

```sh
REPO='https://github.com/shoalmark/shoalmark.git' &&
G() { GIT_TERMINAL_PROMPT=0 git -c credential.helper= -c 'credential.helper=!gh auth git-credential' "$@"; } &&
read -r 'REVIEWED_HEAD?The 40-hex commit the critical review judged, again: ' &&
[[ $REVIEWED_HEAD =~ ^[0-9a-f]{40}$ ]] &&
read -r 'MAIN_AT_PUSH?The 40-hex MAIN_AT_PUSH that step 2 printed, again: ' &&
[[ $MAIN_AT_PUSH =~ ^[0-9a-f]{40}$ ]] &&
RELEASE_PR="$(gh pr view release/v0.20.1 --repo shoalmark/shoalmark --json number --jq .number)" &&
[[ $RELEASE_PR =~ ^[0-9]+$ ]] &&
PR_HEAD="$(gh pr view "$RELEASE_PR" --repo shoalmark/shoalmark --json headRefOid --jq .headRefOid)" &&
[[ $PR_HEAD =~ ^[0-9a-f]{40}$ ]] &&
G fetch "$REPO" "+refs/heads/release/v0.20.1:refs/remotes/origin/release/v0.20.1" &&
git diff --exit-code "$REVIEWED_HEAD" "$PR_HEAD" &&
test "$(G ls-remote "$REPO" refs/heads/main | cut -f1)" = "$MAIN_AT_PUSH" &&
gh pr checks "$RELEASE_PR" --repo shoalmark/shoalmark --required &&
gh pr merge "$RELEASE_PR" --repo shoalmark/shoalmark --merge --match-head-commit "$PR_HEAD" &&
MERGE_SHA="$(gh pr view "$RELEASE_PR" --repo shoalmark/shoalmark --json mergeCommit --jq .mergeCommit.oid)" &&
[[ $MERGE_SHA =~ ^[0-9a-f]{40}$ ]] &&
G fetch "$REPO" '+refs/heads/main:refs/remotes/origin/main' &&
test "$(git rev-parse origin/main)" = "$MERGE_SHA" &&
git log -1 --format='%H %s' "$MERGE_SHA"
```

**Expect:** the reviewed tree is still the pull request's head's, main has still not moved since the push, and every required check is green. GitHub makes the merge commit, and `origin/main` is that commit.

**Paste back:** the merged pull request's URL, and `MERGE_SHA` with its subject.

The tag is yours: read the merge commit on GitHub, then sign it with `git tag -s`.
