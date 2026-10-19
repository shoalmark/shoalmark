# v0.20.0 — the Owner's run sheet

The tag is due Wednesday 21 October 2026, Friday 23 at the latest. Run these blocks in the Owner's zsh shell on macOS, from the release clone. Replace the quoted placeholders first. A failed command or an unexpected result stops that step: paste it back before continuing. Only the Owner pushes, merges, signs and publishes.

Sources: [the release's upgrade notes](../../../CHANGELOG.md#0200--2026-10-21), [the archive builder](../../../scripts/build_release_archive.py), [release.yml](../../../.github/workflows/release.yml), [docs.yml](../../../.github/workflows/docs.yml), and [the merge rule](../../TRIAGE.md#the-current-path). The workflow pins Zensical through [requirements-docs.txt](../../../requirements-docs.txt) (`zensical==0.0.67`); use that file, not an unpinned install.

## 1. Before the PR — the final reviewed head

B2 has merged main, including the signers change, and the records branch at the Auditor's named commit. Round 2 has approved that final tree; any review commit on top has an identical tree. No content changes follow its READY. Keep the required check results and the Reviewer's verdict commit beside the four full SHAs below.

```sh
RELEASE_HEAD='REPLACE_WITH_FINAL_40_HEX_BRANCH_HEAD' &&
REVIEWED_HEAD='REPLACE_WITH_40_HEX_COMMIT_ROUND_2_REVIEWS' &&
REVIEW_COMMIT='REPLACE_WITH_40_HEX_READY_VERDICT_COMMIT' &&
RECORDS_HEAD='REPLACE_WITH_40_HEX_RECORDS_COMMIT_FROM_ADDENDUM' &&
git fetch origin --tags &&
test "$(git rev-parse release/v0.20.0)" = "$RELEASE_HEAD" &&
git merge-base --is-ancestor origin/main "$RELEASE_HEAD" &&
git merge-base --is-ancestor 9409d3bd1a17a13bfc03829732c902be7fbf37d2 "$RELEASE_HEAD" &&
git merge-base --is-ancestor "$RECORDS_HEAD" "$RELEASE_HEAD" &&
git show -s --format=full "$REVIEW_COMMIT" &&
git diff --exit-code "$REVIEWED_HEAD" "$RELEASE_HEAD" &&
git diff --exit-code "$REVIEW_COMMIT" "$RELEASE_HEAD" &&
python3 shoalmark.py --check &&
printf '%s\n' 'OK: the final head holds main, the signers change and the records commit, and both trees are equal'
```

**Expect:** the final head holds main and the specified records commit; round 2's READY names its reviewed commit, base, critical tier and checks in `Reviewed:`. Both tree comparisons are empty; `--check` exits 0. The one full non-browser run belongs to this final tree and reports 0 FAIL with every skip named. The board alone is never permission to merge.

**Paste back:** the four full SHAs, the READY subject and `Reviewed:` line, the final `--check` result, and the `OK:` line.

## 2. Push and open the release PR — freeze main

No merge to main from the PR's opening until the tag, including answer branches. v0.20.1 and v0.20.2 continue on their own branches. PR C merges after this tag.

```sh
git push -u origin release/v0.20.0
MAIN_AT_OPEN="$(git rev-parse origin/main)"
gh pr create --base main --head release/v0.20.0 --title '0.20.0 — Subversion without git and the release archive' --body-file - <<'BODY'
Prepares v0.20.0 for 21 October 2026. Upgrade, run --install-hook again in every committing clone, remove retired settings and schedules, then run --check.

Changes and upgrade messages: [CHANGELOG.md, lines 5–40](CHANGELOG.md#0200--2026-10-21). Publication steps: [the Owner's run sheet](work-tracker/evidence/FM-006/release-v0-20-0-owner-run-sheet.md).

Sources at fixed commits: [Subversion entry](https://github.com/shoalmark/shoalmark/commit/484e27454e77f5a579ca26c0cb9bc27b2c29da2a), [history readers](https://github.com/shoalmark/shoalmark/commit/9218885a926e9fcddf383ff570d354765b25cbc9), [archive](https://github.com/shoalmark/shoalmark/commit/11481149010fcc091349104dbe1fa56a0f0eb845), [removals and board evidence](https://github.com/shoalmark/shoalmark/commit/01014bb53904f59dcfbf5fd30e91d1defe11531d), [agenda and prompts](https://github.com/shoalmark/shoalmark/commit/7acb42d6ea95ee1695ea2a3c77b5291c3eb03495).

Merge only with round 2's critical READY on the final tree and every required check green. Main stays frozen through the tag. The release tag and publication are the Owner's steps after merge.
BODY
RELEASE_PR="$(gh pr view release/v0.20.0 --json number --jq .number)"
gh pr view "$RELEASE_PR" --json url,headRefOid,baseRefName,isDraft
printf '%s\n' "$MAIN_AT_OPEN"
```

**Expect:** one ready release PR to main at `RELEASE_HEAD`. Its opening runs the required CI matrix once on this final revision. Main is frozen now.

**Paste back:** the PR URL, head SHA and `MAIN_AT_OPEN`.

## 3. Before merge — the archive dry run and local docs checks

If the tag moves past 21 October, first change the CHANGELOG and landing dates together in one commit, get that head's CI and a one-line addendum review, and reset the head variables to that approved revision before the dry run and local docs checks below.

```sh
test "$(git ls-remote origin refs/heads/release/v0.20.0 | cut -f1)" = "$RELEASE_HEAD" &&
gh workflow run release.yml --ref release/v0.20.0 -f "ref=$RELEASE_HEAD" &&
DOCS_DIR="$(mktemp -d)" &&
mkdir "$DOCS_DIR/tree" &&
git archive "$RELEASE_HEAD" | tar -x -C "$DOCS_DIR/tree" &&
uv venv -q --python 3.12 "$DOCS_DIR/venv" &&
uv pip install -q --python "$DOCS_DIR/venv/bin/python" -r "$DOCS_DIR/tree/requirements-docs.txt" &&
(cd "$DOCS_DIR/tree" && "$DOCS_DIR/venv/bin/python" scripts/test_check_site.py && "$DOCS_DIR/venv/bin/zensical" build --clean && "$DOCS_DIR/venv/bin/python" scripts/llms_txt.py site && "$DOCS_DIR/venv/bin/python" scripts/check_site.py site) &&
gh run list --workflow release.yml --commit "$RELEASE_HEAD" --event workflow_dispatch --limit 5 --json databaseId,headSha,status,conclusion,url &&
printf '%s\n' 'OK: the dry run is dispatched, the four docs.yml steps pass locally, and nothing is deployed'
```

**Expect:** `release.yml` receives the final 40-hex SHA as its `ref` input and keeps `release-archive` as the run's artifact, attaching nothing to a release. `docs.yml`'s four steps pass locally at `RELEASE_HEAD` with its pinned requirements, and nothing is deployed: the site deploys from the tag (step 10).

**Paste back:** the release run's URL, exact `headSha` and id, and the `OK:` line.

```sh
DRY_RUN_ID='REPLACE_WITH_RELEASE_DRY_RUN_ID'
gh run watch "$DRY_RUN_ID" --exit-status
DRY_ARTIFACT_DIR="$(mktemp -d)"
gh run download "$DRY_RUN_ID" --name release-archive --dir "$DRY_ARTIFACT_DIR"
(cd "$DRY_ARTIFACT_DIR" && shasum -a 256 -c shoalmark-0.20.0.zip.sha256)
```

**Expect:** the dry run succeeds and the two archive files are kept and their checksum verifies. This dry run's `RELEASE` says `tag none`; compare its bytes only with another build of the same commit, not the later tag build.

**Paste back:** the successful dry-run conclusion, the artifact link and checksum result.

## 4. Merge only on READY and every required check green

```sh
gh pr checks "$RELEASE_PR" --required --watch &&
gh pr view "$RELEASE_PR" --json headRefOid,mergeStateStatus,url &&
test "$(gh pr view "$RELEASE_PR" --json headRefOid --jq .headRefOid)" = "$RELEASE_HEAD" &&
test "$(git ls-remote origin refs/heads/main | cut -f1)" = "$MAIN_AT_OPEN" &&
git show -s --format=full "$REVIEW_COMMIT" &&
gh pr merge "$RELEASE_PR" --merge --match-head-commit "$RELEASE_HEAD"
```

**Expect:** every required check is green, the archive dry run and local docs checks succeeded, and round 2 is READY on the final tree. Verify that verdict yourself before the merge command; never infer it from the board or CI. Main has not moved since the PR opened. GitHub makes the release PR's merge commit.

**Paste back:** the check results, the READY and `Reviewed:` lines, and the merged PR URL.

## 5. Show and check what the signed tag signs

Run this on main after the PR merges. It shows GitHub's release-PR merge SHA, main's SHA and the merge subject before signing. If the two SHAs differ, nothing is tagged: stop and paste back both.

```sh
git fetch origin &&
git switch main &&
git merge --ff-only origin/main &&
m="$(gh pr view "$RELEASE_PR" --json mergeCommit --jq .mergeCommit.oid)" &&
printf '%s\n' "$m" &&
git rev-parse origin/main &&
git log -1 --format='%H %s' "$m" &&
if test "$m" = "$(git rev-parse origin/main)"
then
  git tag -s v0.20.0 "$m" -m "v0.20.0" &&
  git tag -v v0.20.0 &&
  test "$(git rev-parse 'v0.20.0^{commit}')" = "$m" &&
  git push origin v0.20.0
else
  printf '%s\n' 'STOP: the release PR merge and origin/main differ. Paste back both SHAs.'
fi
```

**Expect:** the PR's merge SHA and `origin/main` are the same SHA; the subject is the release PR's merge. `git tag -v` verifies the Owner's signature on that SHA, and only then is the tag pushed. A failed signing or verification command prevents the push. Never move an existing tag.

**Paste back:** the merge SHA and the verification line from `git tag -v`; if comparison fails, both SHAs instead.

## 6. After the tag — wait for the draft and its two assets

```sh
gh run list --workflow release.yml --branch v0.20.0 --event push --limit 5 --json databaseId,headSha,status,conclusion,url
TAG_RUN_ID='REPLACE_WITH_TAG_RELEASE_RUN_ID'
gh run watch "$TAG_RUN_ID" --exit-status
gh release view v0.20.0 --json url,isDraft,assets
```

**Expect:** `release.yml` has made a draft with exactly `shoalmark-0.20.0.zip` and `shoalmark-0.20.0.zip.sha256`. Nothing is published yet.

**Paste back:** the successful tag run, draft URL and two asset names.

## 7. Rebuild the tag in a clean clone and compare

```sh
VERIFY_DIR="$(mktemp -d)"
git clone --branch v0.20.0 --single-branch https://github.com/shoalmark/shoalmark.git "$VERIFY_DIR/clone"
TAG_SHA="$(git -C "$VERIFY_DIR/clone" rev-parse 'v0.20.0^{commit}')"
python3 "$VERIFY_DIR/clone/scripts/build_release_archive.py" --repo "$VERIFY_DIR/clone" --out "$VERIFY_DIR/rebuilt" -- v0.20.0
gh release download v0.20.0 --dir "$VERIFY_DIR/downloaded" --pattern 'shoalmark-0.20.0.zip*'
(cd "$VERIFY_DIR/downloaded" && shasum -a 256 -c shoalmark-0.20.0.zip.sha256)
cmp "$VERIFY_DIR/rebuilt/shoalmark-0.20.0.zip" "$VERIFY_DIR/downloaded/shoalmark-0.20.0.zip"
cmp "$VERIFY_DIR/rebuilt/shoalmark-0.20.0.zip.sha256" "$VERIFY_DIR/downloaded/shoalmark-0.20.0.zip.sha256"
printf '%s\n' "$TAG_SHA"
```

**Expect:** the clean clone is at the signed tag's merge SHA; the rebuilt tag archive and checksum file equal the draft assets byte for byte. The zip contains CHANGELOG's `0.20.0` section.

**Paste back:** `TAG_SHA`, the archive's SHA-256 and both empty, successful comparisons.

## 8. Check ADOPT's pin and prepare the notes from the tag

```sh
python3 - "$VERIFY_DIR/clone" "$VERIFY_DIR/release-notes.md" <<'PYTHON' &&
import hashlib, pathlib, re, subprocess, sys
repo, output = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2])
def blob(name):
    return subprocess.check_output(['git', '-C', str(repo), 'show', 'v0.20.0:' + name])
version = blob('VERSION').decode().strip()
assert version == '0.20.0'
pin = hashlib.sha256(blob('shoalmark.py').replace(b'\r\n', b'\n')).hexdigest()
for name in ('ADOPT.md', 'ADOPT.de.md'):
    text = blob(name).decode()
    assert re.findall(r'`(v\d+\.\d+\.\d+)`', text) == ['v' + version]
    assert re.findall(r'\b[0-9a-f]{64}\b', text) == [pin]
section = re.search(r'^## 0\.20\.0 — .*?(?=^## |\Z)', blob('CHANGELOG.md').decode(), re.M | re.S)
assert section
archive = (repo.parent / 'rebuilt/shoalmark-0.20.0.zip.sha256').read_text().strip()
output.write_text(section[0].rstrip() + '\n\n### Pins\n\n- Tag: `v0.20.0`\n- `shoalmark.py` (LF), SHA-256: `' + pin + '`\n- Archive, SHA-256: `' + archive + '`\n', encoding='utf-8')
print('both ADOPT pins:', pin)
print(output.read_text())
PYTHON
gh release edit v0.20.0 --notes-file "$VERIFY_DIR/release-notes.md" &&
printf '%s\n' 'OK: both ADOPT pins match the tag, and the draft notes are updated'
```

**Expect:** both ADOPT pins equal the tag's `shoalmark.py`. The notes contain exactly CHANGELOG's `0.20.0` section plus the tag, tool and archive pins. Read the printed notes before publishing.

**Paste back:** the tool pin, the draft notes, and the `OK:` line.

## 9. Publish the draft, then the Auditor checks the published assets

```sh
gh release edit v0.20.0 --draft=false
gh release view v0.20.0 --json url,isDraft,assets
```

**Expect:** the draft is published with its checked assets. The Auditor independently downloads the published files, rebuilds at `v0.20.0`, and compares the published zip and checksum against the tag, not just this session's downloaded files. Wait for that check's receipt before the final manual docs step.

**Paste back:** the published release URL and the Auditor's identity, tag SHA, asset SHA-256 and comparison result.

## 10. Confirm the site from the tag, then refresh each committing clone

The tag also starts `docs.yml` automatically. This step confirms that deployment or reruns the same tag after the published-asset check; it does not defer a deployment already triggered by the tag.

```sh
gh workflow run docs.yml --ref v0.20.0
gh run list --workflow docs.yml --branch v0.20.0 --limit 5 --json databaseId,headSha,status,conclusion,url
FINAL_DOCS_RUN_ID='REPLACE_WITH_FINAL_TAG_DOCS_RUN_ID'
gh run watch "$FINAL_DOCS_RUN_ID" --exit-status
```

**Expect:** the site is built and checked with pinned Zensical, then deployed from `TAG_SHA`. The release line and setup tags name `v0.20.0`.

**Paste back:** the tag SHA, successful docs run URL and deployment URL.

In every committing clone, on its default branch after vendoring the new release (replace the tool path with that clone's invocation):

```sh
python3 tools/shoalmark/shoalmark.py --install-hook
python3 tools/shoalmark/shoalmark.py --check
```

**Expect:** the hooks' copy is updated, unchanged old global refresh hooks are removed with a line, and `--check` exits 0. Use `--html-only` after checkouts and pulls when the board needs rebuilding.

**Paste back:** each clone's hook-install lines and final check result. Main's freeze ends at the tag; subsequent work targets the next release.
