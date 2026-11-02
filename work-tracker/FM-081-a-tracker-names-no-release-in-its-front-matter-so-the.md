---
id: FM-081
status: Proposed
considered: FM-062, FM-023
tags: process
hook: "a tracker names no release in its front matter, so the release commit cannot check what it holds"
---

# FM-081 — a tracker names no release in its front matter, so the release commit cannot check what it holds

## What is true now

**Filed 2026-10-27, Proposed, as a candidate check from FM-062's entry of 27 October, on the Auditor's word, for the Owner's allocation; nothing is built.**

A tracker says which release holds it only in FM-023's tables and in dated entries. Its front matter has no release field, so the release commit cannot check that each tracker it ships, or leaves out, was allocated so. v0.20.1 reached its tag with five quick wins neither shipped nor moved.

## Why

An allocation that no check reads drifts unseen, as the five quick wins did.

## Done when

- Each tracker's front matter can name its release.
- The release commit checks it: every tracker that names the release is shipped or moved by a dated entry.

## Ship log

| Date | Event |
|---|---|
| 2026-10-27 | Filed, Proposed, a candidate check from FM-062's entry of 27 October, for the Owner's allocation. |
