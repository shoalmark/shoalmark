# The Owner's run sheet — v0.19.0, shoalmark's first public beta (FM-006)

Copy each block, compare with *Expect*, paste back the one line named. Steps 1–2 come before the tag, 3–7 after it. The tag is yours, on `main` after the merge. The topics in step 1 are proposed; you set them.

## Before the tag
1. **Description, homepage, topics** (the description is the site's, `zensical.toml`).
   ```
   gh repo edit shoalmark/shoalmark --description "A work tracker in your repository, built for your agents: no “done” gets through without a commit behind it, and what waits for your word comes first." --homepage https://shoalmark.github.io/shoalmark/ --add-topic ai-agents --add-topic agent-workflow --add-topic work-tracker --add-topic issue-tracker --add-topic human-in-the-loop --add-topic git --add-topic markdown --add-topic python
   gh repo view shoalmark/shoalmark --json description,homepageUrl,repositoryTopics --jq '.description, .homepageUrl, (.repositoryTopics | map(.name) | join(" "))'
   ```
   Expect: no error from the first command; the second prints the description, `https://shoalmark.github.io/shoalmark/`, and the eight topics. Paste back: the topics line.
2. **Social preview** (GitHub has no command for it).
   ```
   git clone --depth 1 https://github.com/shoalmark/shoalmark /tmp/shoalmark-preview && open /tmp/shoalmark-preview/docs/assets/preview.png
   ```
   Then github.com/shoalmark/shoalmark → Settings → General → Social preview → Edit → Upload an image → that file. Expect: the image opens (1200 × 630 px, about 165 kB); after the upload GitHub shows it under *Social preview*. Paste back: `preview set`.

## After the tag
3. **A clean clone at the tag.**
   ```
   git clone --branch v0.19.0 https://github.com/shoalmark/shoalmark /tmp/shoalmark-0.19.0 && cd /tmp/shoalmark-0.19.0 && git describe --tags && cat VERSION
   ```
   Expect: `v0.19.0`, then `0.19.0` (git's note about a detached HEAD above them is fine). Paste back: both lines.
4. **The checksum.**
   ```
   shasum -a 256 shoalmark.py > SHA256SUMS && cat SHA256SUMS && grep -c "$(cut -d' ' -f1 SHA256SUMS)" ADOPT.md ADOPT.de.md
   ```
   Expect: `<64 hex characters>  shoalmark.py`, then `ADOPT.md:1` and `ADOPT.de.md:1` — both notes name this file's checksum. Paste back: those three lines.
5. **The release notes** — CHANGELOG's 0.19.0 section verbatim and three lines; written to `/tmp`, never committed.
   ```
   awk '/^## 0\.19\.0 /{f=1;next} /^## /{f=0} f' CHANGELOG.md > /tmp/notes-0.19.0.md
   printf '\nInstall pinned to the tag: `git clone --branch v0.19.0 https://github.com/shoalmark/shoalmark`, then `--vendor` from that clone.\nAfter upgrading, run `python3 tools/shoalmark/shoalmark.py --install-hook` again: the hook judges more now.\nSHA-256 of shoalmark.py: %s\n' "$(cut -d' ' -f1 SHA256SUMS)" >> /tmp/notes-0.19.0.md
   head -3 /tmp/notes-0.19.0.md; tail -3 /tmp/notes-0.19.0.md
   ```
   Expect: a blank line, then the section's bold headline naming the first public beta; the last three lines are the three above, the checksum ending the file. Paste back: the headline's first line.
6. **The release — a pre-release, with the two assets.**
   ```
   gh release create v0.19.0 --prerelease --title "shoalmark 0.19.0 — public beta" --notes-file /tmp/notes-0.19.0.md shoalmark.py SHA256SUMS
   gh release view v0.19.0 --json isPrerelease,assets --jq '.isPrerelease, (.assets[].name)'
   ```
   Expect: `https://github.com/shoalmark/shoalmark/releases/tag/v0.19.0`; then `true`, `SHA256SUMS` and `shoalmark.py` (assets in either order). Paste back: the URL line.
7. **The Auditor checks the published assets against the tag** (run by the Auditor, or by you for it, in `/tmp/shoalmark-0.19.0`).
   ```
   gh release download v0.19.0 --dir /tmp/release-assets && shasum -a 256 /tmp/release-assets/shoalmark.py && git show v0.19.0:shoalmark.py | shasum -a 256 && diff /tmp/release-assets/SHA256SUMS SHA256SUMS && echo same
   ```
   Expect: two equal hashes, equal to step 4's, and `same`. Paste back: the Auditor's one line, *assets equal the tag* or what differs.
