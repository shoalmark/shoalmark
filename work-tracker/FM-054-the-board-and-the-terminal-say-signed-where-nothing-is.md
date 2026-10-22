---
id: FM-054
status: In Progress
considered: FM-007, FM-015, FM-030, FM-037
tags: bug
next: build
tier: P1
triaged: 2026-10-15
hook: "The board's answer dialog and the terminal say signed on every repository, though --answer signs only where the owner line asks for it"
---

# FM-054 — the board and the terminal say signed where nothing is signed

## What is true now

**Judged 2026-10-15: In Progress, P1.** It is built on `fm/054-proof` for v0.20.1, first, with the board's proof line
beside it (FM-007).

**Built 2026-10-15 on `fm/054-proof`, not merged** (`e80d080`; the Git entry differential's allowance for it, `e110989`); *nothing is built*,
below, dates from the filing. Every surface listed under *Facts* reads the mode as the gate does, from the default branch's
configuration through `owners_at` (`proof_reading`), and says *signed* only where it asks for a signature: *author only*
elsewhere, the server's login on Subversion, no author with no version control. `--answer`, `--done`, `--due` and `--revoke`
pass `-S` from the same reading (`answer_signing`) and say in one line where this checkout's configuration differs. The class
table and its two mutants are `test_proof.py`, staged in `test_shoalmark.py` for CI.

**Filed 2026-10-15; nothing is built.** Held against FM-007, *a signature proves the key, not the hand*: a claim of
*signed* where nothing is signed is the same honesty, from the other side.

**Facts,** read at main `272e374`.
- **`--answer` signs only where `signed` holds** (`-S`, `shoalmark.py:3189`). It reads `signed` from this
  checkout's configuration (`:3065`).
- **The gate verifies against the default branch's `owner` line** (`owners_at` `:7775`; `:5656`). An unsigned
  answer where signing is required is refused, so no bypass is known.
- **What is claimed regardless of `signed`:**
  - the answer dialog's step "commits them, signed with your key — a hardware key waits for your touch" (`:3929`,
    used `:3738`);
  - its title and intro (`:3922`, `:3923`), its success preview (`:3739`), and its `%G?` check (`:3740`, `:3933`);
  - the terminal's "signed, on `<branch>`" after `--answer`, `--done`, `--due` and revoke (`:2812`, `:8529`,
    `:8564`, `:8608`).

**Fix:**
- every one of these lines reads the mode as the gate does, from the default branch's `owner` line, and says *signed*
  only there. Elsewhere it says *author only*, and on Subversion it says what the server's login shows;
- `--answer` decides `-S` from the same reading, and says so when this checkout's configuration differs.

**Test for the class.** A table over every mode (`signed` or not, on the default branch and in the checkout) and every
surface (each dialog line, each terminal line):
- *signed* appears only where the default branch requires it;
- a mutant that reads the checkout's configuration fails the table.

**Tier:** critical: signing and rights. It ships in v0.20.1 with the board's proof line, said before *accept* (FM-023's
table of 2026-10-15).

## Done when

Every surface says *signed* only where the default branch's `owner` line requires it, `--answer` decides `-S` from
the same reading and says so where this checkout's configuration differs, and the class table with its mutant is in CI.

## Ship log

| Date | Event |
|---|---|
| 2026-10-15 | Filed. |
| 2026-10-15 | Judged In Progress, P1, for v0.20.1, on `fm/054-proof`. |
| 2026-10-15 | Built on `fm/054-proof` by the Builder seat (27f31560/builder-11): `e80d080` defect 8, `970c9fd` the proof line (FM-007), `e110989` the Git entry differential's allowance for both; not merged. |
