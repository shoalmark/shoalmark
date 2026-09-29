# FM-006 — independent publication-gates review

Date: 2026-09-29.
Reviewed: `a9703d9b7037bc4af27fc555b5b7afb19fb774cb`.
Branch: `fm/006-publication-gates` (remote head verified).
Base: fetched `origin/main`, `b041cb2dca136623ee9160d74ae5b39b0f1a7ba2`.
Merge base: `80d0811974a1d39b679cfd374c80109ddd62acce`.
Reviewer: `reviewer@seat`, independent session `01a0edae`.
Review branch: `fm/006-review-publication-a9703d9`.
Worktree: `/private/tmp/shoalmark-review-publication-a9703d9`.

**Tier: code, critical. Verdict: NOT READY. One open P2 finding, R1.**

The tier comes from `git diff --name-only origin/main...HEAD`: the deployment
validator and site configuration change, alongside fonts, signing disclosures
and publication evidence. The implementation commit's session is `01a0ec25`,
different from this Reviewer's root. This review changes only this evidence file.

## R1 — P2: validate font sources regardless of their URL's extension

Location: `scripts/check_site.py:54` (the condition governing lines 55–59).

The new validator checks a font's origin and existence only when its URL path
ends in `.woff`, `.woff2`, `.ttf` or `.otf`. A valid `@font-face` source does not
need such a suffix. Consequently an external source such as
`https://example.invalid/font?id=plex` passes, as does a missing local font named
`../assets/fonts/missing-font`. The Google hostname check does not cover other
hosts. A subsequent font-source change can therefore restore a visitor request
to a third-party font host while the pre-upload gate reports success.

Reproduced independently on **Python 3.14.3 and 3.9.6**, using disposable copies
of the clean built site and appending this rule to `stylesheets/fonts.css`:

```css
@font-face {
  font-family: "Review";
  src: url("https://example.invalid/font?id=plex") format("woff2");
}
body { font-family: "Review"; }
```

Run `python3 scripts/check_site.py <copy-of-site>` (also `/usr/bin/python3`).
Both return **0**, printing the success line. Substituting
`../assets/fonts/missing-font` also returns **0** on both interpreters.
The positive rejection control, `https://example.invalid/font.woff2`, returns
**1**, naming the external font, on both.

A Chromium reproduction establishes browser behavior, not just a string match:
two temporary localhost servers used different ports, one serving the site and
one serving the existing Plex Mono WOFF2 with a font content type and CORS.
An added `@font-face` used the second origin's `/font?id=plex` URL. The checker
returned **0**; `document.fonts.load('16px "Review Remote"', 'shoalmark')`
requested `/font?id=plex` from the second server and returned the face with
`status: "loaded"`. No third-party service was needed for this control.

Required fix: validate URL sources in `@font-face` declarations independently
of their filename suffix. Reject external sources and verify local destinations;
replace the suffix-dependent decision and add regression controls for an
extensionless remote font and a missing extensionless local font. Keep the
existing Google-reference controls. Re-review the fix under the code loop.

The checked-in fonts currently load locally. R1 concerns the new deployment
gate's failure to enforce its stated restriction, not an observed external font
request from the unmodified reviewed site.

## Changes and evidence verified

Read FM-006, its four publication gates, FM-007's recorded state, and
[`publication-gates-2026-09-29/README.md`](../FM-006/publication-gates-2026-09-29/README.md)
with all three evidence data files. Reviewed the complete source/configuration
diff and checked the binary assets against their manifest and upstream bytes.

- **Build:** pinned Zensical **0.0.66**, `zensical build --clean`: exit 0,
  no issues. `python3 scripts/llms_txt.py site`: exit 0, 11 Markdown twins.
  The unmodified site checker passes on Python 3.14.3 and 3.9.6.
- **Existing validator behavior:** 68 checks pass across those interpreters:
  baseline and restored site; each of 28 font files removed separately;
  Google CSS import; Google HTML preconnect; external `.woff2`; and
  protocol-relative `.woff2`. These controls demonstrate the implemented
  protections but do not close R1.
- **Browser:** Chromium on `/shoalmark/` renders landing, setup, EN/DE signing
  and agents contract. All actual font requests on all five pages go to local
  `assets/fonts/`; no local HTTP failures, script errors or Google font requests.
  Landing loads seven faces, each documentation page eight. The existing GitHub
  repository/version lookup is reproduced, including `releases/latest` 404;
  the evidence correctly discloses it. No zero-network claim is made.
- **Font provenance:** all 28 WOFF2 signatures, SHA-256 values and sizes match
  `sources.json`, totaling **539380 bytes**. There are 20 distinct payloads/URLs;
  all 20 upstream downloads match, covering the 28 declared files. All three OFL
  files are byte-identical to `google/fonts` at the recorded revision
  `23e54b51ddffbc7713c583748e3bd86f62b1fa4a`. Google configuration, the landing
  request/preconnect and the stylesheet import are removed. The replacement
  stylesheet supplies the font variables and required faces.
- **Signing:** the EN/DE additions state the recorded date and tier 0, and
  distinguish trusted-key use from the Owner's presence. These match FM-007's
  2026-09-25 record and unfinished hardware-key act. Both added paragraphs are
  present in the independently built browser pages. No signing configuration
  changes, hardware-key completion or live deployment is inferred.
- **Tag CI:** a fresh GitHub API read confirms run
  [36483645765](https://github.com/shoalmark/shoalmark/actions/runs/36483645765)
  is successful at `1c344ed89ca1c0e1dd714c8beb737f92fc2983c4`, branch/tag
  `v0.18.6`, with all five listed Linux/macOS/Windows jobs successful. This is
  historical tag evidence, not CI for the reviewed branch or an after-scoring tag.
- **History scan:** all 142 captured refs exactly match the retained non-shallow
  audit mirror, including 121 pull refs; reachable commit count is **835**.
  Manifest SHA-256 is
  `4cf6fc30a1290369dca19b6a28018481cd886d00e40e05fc1c3948db9dcc32f6`.
  GitHub's official Gitleaks v8.30.1 release API confirms the archive and
  checksum-manifest digests; the retained executable matches the archive.
  Independently reran the documented command over that mirror with both config
  environment variables removed, the empty ignore file, no baseline and inline
  allow comments disabled: **exit 0, 671 scanned commits, 5677245 bytes, zero
  findings**. The empty JSON report reproduces SHA-256
  `37517e5f3dc66819f61f5a7bb8ace1921282415f10551d2defa5c3eb0985b570`.
  A new disposable repository containing a synthetic token committed and then
  deleted is rejected, **exit 1**, by the `github-pat` rule. A separate scan of
  `80d0811..a9703d9` also exits 0 with zero findings. No credential or finding
  content is included in this verdict.

The history rerun verifies the captured scope; it is not a fresh census of every
remote ref at the time of this verdict. The original evidence correctly excludes
unreachable objects, deleted refs, external forks and unpushed local branches.

## Repository gates and next move

`python3 shoalmark.py --check` at the reviewed head exits **0**, including the
judged-before-build and Owner-section guards. Git's merge simulation against
the fetched base is clean (tree `d17b2d0dba17e6df1eba4f1ee6ca8ddcf59a6325`).
`git diff --check` flags upstream whitespace/CRLF in the three unchanged OFL
copies; excluding those byte-preserved license files, it exits 0. This is not a
review finding. No full tool-suite rerun is claimed: this pass exercised the
changed deployment validator, build, browser behavior and evidence directly.

Fetched main already contains port-cleanup PR 119 (`b041cb2`); the branch's
earlier statement that it awaits merge describes its captured base. No open
publication PR was returned for this head during review.

Next: fix R1 on FM-006, then independent verification of the revised head.
Required PR CI, the Owner's merge, deployment and live verification remain.
The after-scoring timing condition and standing signed publication act remain
open. This verdict authorizes neither publication nor a release; no tag is
created or requested by this review. No merge, deployment, push or repository
setting change was performed.
