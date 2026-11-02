---
id: FM-110
status: Proposed
epic: FM-107
considered: FM-006, FM-044
tags: process
hook: "A release attaches its archive and the archive's checksum, and no attestation. The checksum says the bytes are the ones uploaded, not which workflow run built them."
---

# FM-110 — a release carries no attestation of how its archive was built

## What is true now

**2026-11-03 — filed; nothing is built.** It is one of FM-006's checks after the v0.19.0 tag, kept on the Owner's word
of 2 November.
- `.github/workflows/release.yml` builds the archive, keeps it as an artifact and drafts the release. It has no
  attestation step.
- The archive and its `.sha256` are attached. The checksum is not an attestation.

## Why

An adopter who checks what they run needs to know where it was built, not only that the bytes arrived whole.

## Done when

- [ ] Each release's archive carries an attestation of the workflow run that built it.

## Ship log

| Date | Event |
|---|---|
| 2026-11-03 | Filed as a child of FM-107, on the Owner's word of 2 November. Records only. |
