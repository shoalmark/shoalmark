# v0.20.1 — the Owner's run sheet, after the tag

This sheet begins once the Owner has signed `v0.20.1` on the release pull request's merge commit and pushed it, as [the run sheet up to the merge](release-v0-20-1-owner-run-sheet.md) ends. It holds no tag command. Run these blocks in the Owner's zsh shell on macOS, from the release clone. Replace the quoted placeholders first. A failed command or an unexpected result stops that step: paste it back before continuing. Only the Owner pushes, merges and publishes.

**Main stays frozen until step 8's `docs.yml` run from the switch commit has deployed, to GitHub Pages and to Cloudflare.** ADOPT's pins follow the tag: the tagged commit keeps v0.20.0, and every commit after it on main must pin v0.20.1. The switch commit is the first commit on main after the tag; any other merge before it would turn ADOPT's pin check red on main and on every branch cut from it. A merge after the switch and before step 8 would change what step 8 deploys.

Sources: [CHANGELOG.md](../../../CHANGELOG.md), [the archive builder](../../../scripts/build_release_archive.py), [release.yml](../../../.github/workflows/release.yml), [docs.yml](../../../.github/workflows/docs.yml), [ADOPT.md's pin line](../../../ADOPT.md), and [the pin test's order, `_pinned_release`](../../../test_shoalmark.py). The site's tools are pinned by [requirements-docs.txt](../../../requirements-docs.txt); use that file, not an unpinned install.

## 1. The tag's check: its signature, and the commit it names

```sh
RELEASE_PR='REPLACE_WITH_THE_RELEASE_PULL_REQUEST_NUMBER' &&
git fetch origin --tags &&
MERGE_SHA="$(gh pr view "$RELEASE_PR" --json mergeCommit --jq .mergeCommit.oid)" &&
git tag -v v0.20.1 &&
test "$(git rev-parse 'v0.20.1^{commit}')" = "$MERGE_SHA" &&
test "$(git ls-remote origin 'refs/tags/v0.20.1^{}' | cut -f1)" = "$MERGE_SHA" &&
test "$(git rev-parse origin/main)" = "$MERGE_SHA" &&
git show "$MERGE_SHA:ADOPT.md" | grep '^The pin: release `v0.20.0`' &&
printf '%s\n' "OK: v0.20.1 is signed, names the merge commit $MERGE_SHA, and its notes still pin v0.20.0"
```

**Expect:** `git tag -v` verifies the Owner's signature. The tag names the release pull request's merge commit, here and on GitHub, and main has not moved past it. The tagged commit's notes still pin `v0.20.0`, as the order requires. The tag starts three builds: CI, `release.yml`'s draft, and `docs.yml`, which deploys the taped site to GitHub Pages and to Cloudflare, since the probe switch is still off. A probe build of the tagged commit would stop at the pins' check 5, because it names v0.20.0 while v0.20.1 is the newest release the commit holds.

**Paste back:** the verification lines of `git tag -v`, `MERGE_SHA`, the pin line `grep` printed, and the `OK:` line.

## 2. The draft and its two assets

```sh
gh run list --workflow release.yml --branch v0.20.1 --event push --limit 5 --json databaseId,headSha,status,conclusion,url
```

```sh
TAG_RUN_ID='REPLACE_WITH_THE_TAG_RELEASE_RUN_ID' &&
gh run watch "$TAG_RUN_ID" --exit-status &&
gh release view v0.20.1 --json url,isDraft,assets
```

**Expect:** the tag's run succeeds on `MERGE_SHA`. `release.yml` has made a draft holding exactly `shoalmark-0.20.1.zip` and `shoalmark-0.20.1.zip.sha256`. Nothing is published yet.

**Paste back:** the run's URL and conclusion, the draft's URL and the two asset names.

## 3. A clean clone at the tag rebuilds the archive, and the hashes are equal

```sh
VERIFY_DIR="$(mktemp -d)" &&
git clone --branch v0.20.1 --single-branch https://github.com/shoalmark/shoalmark.git "$VERIFY_DIR/clone" &&
TAG_SHA="$(git -C "$VERIFY_DIR/clone" rev-parse 'v0.20.1^{commit}')" &&
test "$TAG_SHA" = "$MERGE_SHA" &&
python3 "$VERIFY_DIR/clone/scripts/build_release_archive.py" --repo "$VERIFY_DIR/clone" --out "$VERIFY_DIR/rebuilt" -- v0.20.1 &&
gh release download v0.20.1 --dir "$VERIFY_DIR/downloaded" --pattern 'shoalmark-0.20.1.zip*' &&
(cd "$VERIFY_DIR/downloaded" && shasum -a 256 -c shoalmark-0.20.1.zip.sha256) &&
cmp "$VERIFY_DIR/rebuilt/shoalmark-0.20.1.zip" "$VERIFY_DIR/downloaded/shoalmark-0.20.1.zip" &&
cmp "$VERIFY_DIR/rebuilt/shoalmark-0.20.1.zip.sha256" "$VERIFY_DIR/downloaded/shoalmark-0.20.1.zip.sha256" &&
shasum -a 256 "$VERIFY_DIR/rebuilt/shoalmark-0.20.1.zip" &&
printf '%s\n' "OK: the rebuild at $TAG_SHA equals the draft's two assets byte for byte"
```

**Expect:** the clean clone is at the signed tag's commit. The rebuilt archive and its checksum file equal the draft's assets byte for byte, and the archive holds CHANGELOG's `0.20.1` section. Keep the archive's SHA-256: the switch commit's pin line carries it.

**Paste back:** `TAG_SHA`, the archive's SHA-256, and the `OK:` line.

## 4. The notes are CHANGELOG's 0.20.1 section

```sh
python3 - "$VERIFY_DIR/clone" "$VERIFY_DIR/release-notes.md" <<'PYTHON' &&
import pathlib, re, subprocess, sys
repo, output = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2])
changelog = subprocess.check_output(['git', '-C', str(repo), 'show', 'v0.20.1:CHANGELOG.md']).decode('utf-8')
section = re.search(r'^## 0\.20\.1 — .*?(?=^## |\Z)', changelog, re.M | re.S)
assert section, 'no 0.20.1 section in the tag\'s CHANGELOG'
output.write_text(section[0].rstrip() + '\n', encoding='utf-8')
print(output.read_text(encoding='utf-8'))
PYTHON
gh release edit v0.20.1 --notes-file "$VERIFY_DIR/release-notes.md" &&
printf '%s\n' 'OK: the draft notes are the CHANGELOG section for 0.20.1, as the tag holds it'
```

**Expect:** the notes are exactly CHANGELOG's `0.20.1` section as the tag holds it, with nothing added. Read the printed notes before publishing.

**Paste back:** the printed notes and the `OK:` line.

## 5. Publish the draft, then the Auditor checks the published assets against the tag

```sh
gh release edit v0.20.1 --draft=false &&
gh release view v0.20.1 --json url,isDraft,publishedAt,assets
```

**Expect:** the release is published with its two checked assets. The Auditor then downloads the published files, rebuilds at `v0.20.1`, and compares the published zip and checksum with the tag. Wait for that receipt before the switch commit's merge.

**Paste back:** the published release's URL and time, and the Auditor's receipt: its identity, the tag's SHA, the asset's SHA-256 and the comparison's result.

## 6. The switch commit: its bounded check, then the merge to main

The switch commit comes from a branch cut from main after the tag. It moves both notes' pin to `v0.20.1`, with the tag's tool's SHA-256 and the published archive's SHA-256, and it lifts the tape and turns the probe switch on. The Auditor's bounded check judges it before the merge.

```sh
SWITCH_PR='REPLACE_WITH_THE_SWITCH_PULL_REQUEST_NUMBER' &&
SWITCH_HEAD='REPLACE_WITH_THE_40_HEX_SWITCH_HEAD_THE_CHECK_JUDGED' &&
SWITCH_CHECK='REPLACE_WITH_THE_40_HEX_VERDICT_COMMIT_OF_THE_BOUNDED_CHECK' &&
git fetch origin --tags &&
test "$(gh pr view "$SWITCH_PR" --json headRefOid --jq .headRefOid)" = "$SWITCH_HEAD" &&
test "$(git rev-parse origin/main)" = "$MERGE_SHA" &&
git show "$SWITCH_HEAD:ADOPT.md" | grep '^The pin: release `v0.20.1`' &&
git show -s --format=full "$SWITCH_CHECK" &&
gh pr checks "$SWITCH_PR" --required --watch &&
gh pr merge "$SWITCH_PR" --merge --match-head-commit "$SWITCH_HEAD" &&
git fetch origin &&
SWITCH_MERGE="$(git rev-parse origin/main)" &&
test "$(git rev-list --first-parent --count v0.20.1..origin/main)" = 1 &&
git log -1 --format='%H %s' "$SWITCH_MERGE" &&
printf '%s\n' "OK: the switch merged as the first commit on main after the tag: $SWITCH_MERGE"
```

**Expect:** main still stands at the tagged commit before the merge. The switch head pins `v0.20.1`, its bounded check is READY on it, and every required check is green; verify the verdict yourself. After the merge, the switch is the first commit on main after the tag. **Main stays frozen:** the freeze ends only once step 8's deploys are green. Step 8 stops if main has moved.

**Paste back:** the check results, the verdict's subject and `Reviewed:` line, `SWITCH_MERGE` with its subject, and the `OK:` line.

## 7. The four clean runs, from the switch commit's probe build

Build the probe site from `SWITCH_MERGE` in a scratch clone, as `docs.yml` builds it, and serve it on this machine. The Auditor sets up the two invented test projects, one Git and one Subversion without git, and gives each run a fresh copy.

```sh
PROBE_DIR="$(mktemp -d)" &&
git clone --quiet https://github.com/shoalmark/shoalmark.git "$PROBE_DIR/clone" &&
git -C "$PROBE_DIR/clone" switch --quiet --detach "$SWITCH_MERGE" &&
uv venv -q --python 3.12 "$PROBE_DIR/venv" &&
uv pip install -q --python "$PROBE_DIR/venv/bin/python" -r "$PROBE_DIR/clone/requirements-docs.txt" &&
(cd "$PROBE_DIR/clone" && "$PROBE_DIR/venv/bin/python" scripts/test_check_site.py && "$PROBE_DIR/venv/bin/python" scripts/landing_facts.py && "$PROBE_DIR/venv/bin/zensical" build --clean && "$PROBE_DIR/venv/bin/python" scripts/llms_txt.py site && "$PROBE_DIR/venv/bin/python" scripts/check_site.py site && "$PROBE_DIR/venv/bin/python" scripts/landing_facts.py --check site) &&
printf '%s\n' "OK: the probe build of $SWITCH_MERGE is built and checked" &&
python3 -m http.server --bind 127.0.0.1 --directory "$PROBE_DIR/clone/site" 8000
```

Open `http://127.0.0.1:8000/` and run the four runs, two at a time:

| Pair | Run | Test project | Harness |
|---|---|---|---|
| First | 1 | Git | Claude Code |
| First | 2 | Subversion | Codex |
| Second | 3 | Git | Codex |
| Second | 4 | Subversion | Claude Code |

Each run goes from the probe build's button to the feedback file. The Owner starts each run, and the Auditor records it. Any failure restarts all four. Stop the server with Ctrl-C after the fourth run.

**Expect:** the build passes every step, and the landing's button copies the probe prompt. Each run ends with its feedback file written, and no outside run happens before step 8.

**Paste back:** the `OK:` line, and for each run its number, project and harness, its start and end times, and the Auditor's record of it.

## 8. `docs.yml`, by hand, from the switch commit

```sh
git fetch origin &&
test "$(git rev-parse origin/main)" = "$SWITCH_MERGE" &&
gh workflow run docs.yml --ref main &&
gh run list --workflow docs.yml --event workflow_dispatch --limit 5 --json databaseId,headSha,status,conclusion,url
```

```sh
DOCS_RUN_ID='REPLACE_WITH_THE_DOCS_RUN_ID' &&
test "$(gh run view "$DOCS_RUN_ID" --json headSha --jq .headSha)" = "$SWITCH_MERGE" &&
gh run watch "$DOCS_RUN_ID" --exit-status &&
gh run view "$DOCS_RUN_ID" --json jobs --jq '.jobs[] | "\(.name): \(.conclusion)"'
```

**Expect:** the run builds `SWITCH_MERGE` once and deploys that build twice: to GitHub Pages (the job `deploy`) and to Cloudflare (the job `cloudflare`). Both deploys are green. As a deploy build it also runs the pins' checks 6 and 9: the commit is on main, and the published archive downloads and matches the pin line. The tape comes off, and the button and the probe go live. **Main's freeze ends here, once both deploys are green.** Only after this run may any outside run happen.

**Paste back:** the run's URL, its `headSha` and conclusion, both deploy jobs' lines (`deploy: success` and `cloudflare: success`), and the GitHub Pages deployment's URL.

## 9. Then: `--install-hook` again in every committing clone

In every committing clone, on its default branch, after vendoring v0.20.1 (replace the tool's path with that clone's own):

```sh
python3 tools/shoalmark/shoalmark.py --install-hook &&
python3 tools/shoalmark/shoalmark.py --check
```

**Expect:** the hooks' copy is updated, the refresh hooks are installed again, and `--check` exits 0.

**Paste back:** each clone's hook-install lines and its `--check` result.
