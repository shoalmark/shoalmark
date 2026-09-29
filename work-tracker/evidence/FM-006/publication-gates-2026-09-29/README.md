# FM-006 — publication gate evidence, 2026-09-29

Principal session `01a0ec25`, branch `fm/006-publication-gates`, base `80d0811`.
The Owner instructed verification and closure of all feasible remaining publication obligations.
Scoring remains due tomorrow on his latest instruction; no signed act, release tag or merge is made here.

## CI

[v0.18.6 CI](https://github.com/shoalmark/shoalmark/actions/runs/36483645765), head
`1c344ed89ca1c0e1dd714c8beb737f92fc2983c4`: all five jobs passed (Linux 3.9/3.12,
macOS 3.12, Windows 3.9/3.12). Structured read-back: `results.json`.
This establishes the latest existing tag's platform checks; it does not claim that tag followed
scoring. The original after-scoring timing condition remains separate. Migration PR 117's final
head also passed all five jobs before its merge. This branch still requires its own PR checks.

## Whole-history Gitleaks

Gitleaks 8.30.1, official Darwin binary checked against the release SHA-256 manifest.
A fresh non-shallow mirror of the public repository was fetched, with advertised PR head and merge
refs explicitly fetched. Exact 142-ref manifest: `scanned-refs.txt` (121 PR refs); 835 reachable
commits. Gitleaks reports 671 scanned commits with patches, approximately 5.68 MB; the two counts
measure different things. This is all history reachable from those refs, not unreachable objects,
external forks, local unpushed branches or deleted remote refs.

Command (temporary paths omitted):

```sh
gitleaks git history.git --log-opts='--all --full-history' --redact=100   --ignore-gitleaks-allow --gitleaks-ignore-path=empty.ignore   --no-banner --report-format=json --report-path=gitleaks-redacted.json
```

GITLEAKS_CONFIG and GITLEAKS_CONFIG_TOML were removed from the scanner environment; default rules,
no baseline, empty ignore file, inline allow comments disabled. Exit 0, zero findings. A disposable
repository with a synthetic GitHub-shaped token committed and then deleted is rejected (exit 1),
proving the scan sees deleted history. No credential value or scanner finding is published here.
This is a clean result for these rules and this captured scope, not proof that no secret ever existed.

## Signing disclosure

Live English and German signing pages were fetched successfully. They explain software-key exposure,
four tiers, and the current tool's inability to distinguish key tiers. The site's project-specific
state was not explicit: new EN/DE paragraphs state the last recorded project tier (0, 2026-09-25,
FM-007), and do not claim the planned hardware-key move completed. The hardware key is the alternative
to disclosure in this gate; it is not required to publish the disclosure. No signing configuration changed.
These new paragraphs require merge, deployment and live verification before this gate is closed as live.

## Self-hosted fonts

Removed Google font configuration, landing stylesheet request/preconnect, and CSS import. IBM Plex
Sans, IBM Plex Mono and Silkscreen now load from docs/assets/fonts, preserving used faces/weights and
Latin/Latin-extended coverage. 28 WOFF2 faces, 539380 bytes. Upstream URLs, checksums and pinned OFL
licence provenance are in docs/assets/fonts/sources.json and the three licence files.
Clean pinned Zensical 0.0.66 build, llms generation and site validation pass. Removing a generated
font asset and reintroducing a Google Fonts import each makes validation fail; restoring them passes.
No generated HTML/CSS references fonts.googleapis.com or fonts.gstatic.com.
Chromium renders landing, setup, EN/DE signing and contract pages under the /shoalmark/ prefix:
local fonts load, no local HTTP errors, no Google font requests. `browser-fonts.json` records loaded
families/weights and external requests. The existing theme requests GitHub releases/latest and
receives HTTP 404 (tags exist, but no release is returned); that pre-existing version lookup is
outside this font/privacy slice. No claim of a zero-network site is made.
The site validator also passes under Python 3.9.

## Closure

Review, required PR CI, Owner merge and Pages deployment remain. The port deletion has its separate
READY branch `fm/006-remove-port-evidence`; this branch does not duplicate that deletion. Once the
changes are live, verify their disclosure and font requests. The Owner's Board act remains open;
scoring and its timing cannot be certified by this work.
