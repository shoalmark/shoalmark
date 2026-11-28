# Historical check fixtures

## Summary — the check output, regenerable

```json
{
  "file": "work-tracker/evidence/FM-006/landing/start-page/checks.json",
  "tested": "cb49101",
  "command": "git archive cb49101 | tar -x -C stage-cb49101 && (cd stage-cb49101 && uvx zensical@0.0.65 build); node work-tracker/evidence/FM-006/landing/start-page/checks.mjs stage-cb49101/site checks.json work-tracker/evidence/FM-006/landing/index.html",
  "checks": 18,
  "failing": [
    "chart 1440 R 54°10'N (under the title)", "chart 1440 S 54°00'N (under the title)",
    "chart 1440 S 54°10'N (under the title)"
  ],
  "generated_by": "node work-tracker/evidence/FM-006/landing/start-page/checks.mjs"
}
```

```json
{
  "file": "work-tracker/evidence/FM-006/landing/start-page/checks-r3-before.json",
  "tested": "9307cf8",
  "command": "git archive 9307cf8 | tar -x -C stage-9307cf8 && (cd stage-9307cf8 && uvx zensical@0.0.65 build); node work-tracker/evidence/FM-006/landing/start-page/checks.mjs stage-9307cf8/site checks-r3-before.json",
  "checks": 4,
  "failing": [
    "chart 1024 R 53°30'N", "chart 1024 R 53°30'N", "chart 1024 R 53°40'N", "chart 1024 R 53°40'N",
    "chart 1024 R 54°10'N", "chart 1024 R 54°10'N", "chart 1024 R 7°00'E", "chart 1024 R 7°00'E",
    "chart 1024 R 7°20'E", "chart 1024 R 8°20'E", "chart 1024 R 8°40'E", "chart 1024 R 8°40'E",
    "chart 1024 R BUTJADINGEN", "chart 1024 R Bremerhaven", "chart 1024 R DITHMARSCHEN", "chart 1024 R Ems",
    "chart 1024 R LAND WURSTEN", "chart 1024 R Norddeich", "chart 1024 R OSTFRIESLAND", "chart 1024 S 53°30'N",
    "chart 1024 S 53°30'N", "chart 1024 S 53°40'N", "chart 1024 S 53°40'N", "chart 1024 S 54°10'N",
    "chart 1024 S 7°00'E", "chart 1024 S 8°20'E", "chart 1024 S 8°40'E", "chart 1024 S BUTJADINGEN",
    "chart 1024 S Bremerhaven", "chart 1024 S DITHMARSCHEN", "chart 1024 S LAND WURSTEN", "chart 1024 S Norddeich",
    "chart 1440 R 53°30'N", "chart 1440 R 53°30'N", "chart 1440 R 53°40'N", "chart 1440 R 53°40'N",
    "chart 1440 R 54°10'N", "chart 1440 R 54°10'N (under the title)", "chart 1440 R 7°00'E", "chart 1440 R 7°00'E",
    "chart 1440 R 7°20'E", "chart 1440 R 8°00'E", "chart 1440 R 8°20'E", "chart 1440 R 8°40'E",
    "chart 1440 R 8°40'E", "chart 1440 R BUTJADINGEN", "chart 1440 R Bremerhaven", "chart 1440 R DITHMARSCHEN",
    "chart 1440 R Ems", "chart 1440 R LAND WURSTEN", "chart 1440 R Norddeich", "chart 1440 R OSTFRIESLAND",
    "chart 1440 S 53°30'N", "chart 1440 S 53°30'N", "chart 1440 S 53°40'N", "chart 1440 S 53°40'N",
    "chart 1440 S 54°00'N (under the title)", "chart 1440 S 54°10'N", "chart 1440 S 54°10'N (under the title)",
    "chart 1440 S 7°00'E", "chart 1440 S 7°20'E", "chart 1440 S 8°20'E", "chart 1440 S 8°40'E",
    "chart 1440 S BUTJADINGEN", "chart 1440 S Bremerhaven", "chart 1440 S DITHMARSCHEN", "chart 1440 S LAND WURSTEN",
    "chart 1440 S Norddeich"
  ],
  "generated_by": "node work-tracker/evidence/FM-006/landing/start-page/checks.mjs (chart part)"
}
```

```json
{
  "file": "work-tracker/evidence/FM-006/landing/start-page/facts.json",
  "tested": "bef2a1e",
  "command": "node work-tracker/evidence/FM-006/landing/start-page/facts.mjs bef2a1e work-tracker/evidence/FM-006/landing/index.html",
  "wrecks": 24,
  "failing": [],
  "generated_by": "node work-tracker/evidence/FM-006/landing/start-page/facts.mjs",
  "fields": {"sha": "bef2a1e2b84565f2533bc4acb9903e9de206252f", "release": "0.18.4", "counts": {"In Progress": 5, "Proposed": 3, "Shipped": 15, "Closed": 1}, "wrecks": 24},
  "sha256_without_read": "ba1abc26ca797e3aeb2deb46d93cafd4cda40dc3b8b7862ab63a639de4de1942"
}
```
