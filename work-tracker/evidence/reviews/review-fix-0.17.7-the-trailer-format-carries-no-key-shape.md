# Review — 0.17.7, the trailer format carries no `key=` shape

- **Date:** 2026-09-23, 19:06 CEST (`date`)
- **Seat:** Reviewer (`reviewer@seat`) · **Session:** `8e509911/reviewer-1` · **Model:** Claude Opus 5.5
- **Tip reviewed:** `c699e6f` on `fix/0.17.7-the-trailer-format-carries-no-key-shape`
- **Base:** `4bb3f32` (`origin/main`, v0.17.6)
- **Commits:** `037d355` (the fix and two checks), `3318e46` (FM-024's open item), `c699e6f` (`VERSION`,
  `CHANGELOG.md`). All three carry `Session: 8e509911/implementer-2`, a row convened by *session 8e509911*.

## Cold start

1. **What virtue do I bring?** Doubt. The claim to test is "the same values, in the same order". A refactor of
   how trailers are read is exactly where a silent change of meaning hides.
2. **How does it turn into blindness?** By treating a passing secret scan as proof of behaviour, or a changed shape
   as a changed meaning.
3. **What would show that failure here?** The same fixtures and the same repository read by 0.17.6 and by the tip,
   compared line for line; the consumer's own detector on the files a pin stages; 0.17.6's tool as the negative
   control.
4. **Who gets the record, independently of me?** The Principal seat, then the Owner. This file disposes of nothing.

## What the change is

Four reads of commit trailers ask git for the plain trailer block, `%(trailers:only,separator=%x03)`, and pick the key
in Python with `trailer_values()` (case aside, in order, empty values dropped). The four are `trailers_of()`, the
abandoned-row log, the verdict log and the reviewed-range log (`shoalmark.py:2571–2590`, `:2677`, `:2721`, `:2739`).

## Behaviour — identical

- **This repository:** `--check` with 0.17.6 and with the tip gives the same output line for line, apart from the
  command path each prints. The three verdicts read *e6fac09954 on 8b5588e: same session*, *34ff6cea57 on acec312:
  same session* and *0dbdb3c396 on 0743a45: independent*, each with the same range sessions.
- **The planted fixtures** from the 0.17.6 pass, run under both tools and compared with hashes and times masked:
  - `fx2` (the reviewed range, the sibling before and after landing): identical.
  - `fx3` (the abandoned row, the trunk verdict *on trunk — not a branch verdict*, the `--owner` line, the `--triage`
    close): identical.
- **A body line shaped like a trailer is not read.** I planted a commit whose body carries `Reviewed: <tip>` and
  `Session: FAKE` in a paragraph of their own, above a trailer block `Session: K`. Git's trailer block is
  `[Session: K]`, and both tools still count one verdict, not two. The new check does the same with `Note:` in a body
  and a lower-case `session:` in the block.

## The consumer's detector

Run read-only in its `--paths` mode, from a scratch consumer layout so its path-keyed accepted list
applies.

| scanned | exit | findings |
|---|---|---|
| the tip's `shoalmark.py` | 0 | 0 |
| `VERSION`, `CHANGELOG.md`, `README.md`, `NOTICE`, `LICENSE-APACHE`, `LICENSE-MIT`, `PIN` | 0 each | 0 each |
| `vendor/marked-18.0.13.umd.js` | 0 | 0 — its two hits are counted as the consumer's `accepted_false_positives=2` |
| **negative control:** 0.17.6's `shoalmark.py` | **4** | `tools/shoalmark/shoalmark.py:2573:named-secret-field count=1`, the refusal that caused this release |

**What a pin stages.** In a scratch consumer, git-initialised and pinned at 0.17.6, `--vendor` from the tip rewrites
every file. `git add -A` then stages only the four whose bytes changed: `CHANGELOG.md`, `PIN`, `VERSION` and
`shoalmark.py`. `vendor/marked-18.0.13.umd.js` is **not staged**, and neither are `README.md`, `NOTICE` or the
licences. The detector's `--staged` on that stage: exit 0, 4 files scanned, 0 findings.

## `git grep -n 'key='`

- **`shoalmark.py`:** Python keyword and default arguments (`sorted(key=…)`, `init(key=None)`, `.format(key=key)`),
  and one JavaScript comparison in the embedded board, `e.key=="/"` (`:1306`, older than this release). No trailer
  filter remains; the tool asks git for one trailer form, `only,separator=%x03`.
- **Outside the tool:**
  - `README.md:245`;
  - a test, `test_shoalmark.py:562`, which is not vendored;
  - FM-024's examples (`:75`, `:150`), not vendored;
  - two evidence scripts under `evidence/FM-001/`, not vendored.

## FM-024

- The new *Open items* section is worded as this seat's delta note put it: the 8-character all-hex token, the date and
  hash examples, loud and avoidable, the silent 7-character and upper-case cases, the proposed fix, 0.17.8 or later.
- Nothing else in FM-024 moved: its diff is the seven added lines.
- `sessions.md`: `8e509911/implementer-1` is closed, and `8e509911/implementer-2` is open, its id derived from
  *session 8e509911*.

## Findings

### R1 · P3 · README still teaches the `key=` shape, in a file every pin ships

- **What:** README §6 (`:245`) tells a reader to read the trailer back with
  `git log --format='%h %ae %(trailers:key=Session,valueonly)'`. `README.md` is in `TOOL_FILES`.
- **Measured:** the consumer's detector passes it today (exit 0, 0 findings), and a pin that does not change README
  does not stage it. The tool's own source no longer carries the shape; its documentation still does.
- **Cost:** None today. If the consumer's ratchet ever reads `key=Session` as a named field, a README change would be
  refused in the same way `shoalmark.py:2573` was.
- **Confidence:** High on the fact; the risk is conditional.
- **What closes it:** Show the read-back without a filter, for example `git log --format='%h %ae
  %(trailers:only)'`, or `git log -1 --format=%B | git interpret-trailers --parse`. Or leave it, since the detector
  passes it.

## What survives the pass

- The fix does what the CHANGELOG says: the same values, in the same order, with the key's case ignored as git
  ignores it.
- The consumer's gate passes every file a pin stages.
- `CHANGELOG.md` `## 0.17.7` comes first, is dated today, and is true: *nothing to do: no setting, label or command
  changed*.
- `VERSION` = `__version__` = `0.17.7`.
- Two new checks:
  - **The format check** (the tool asks git for one trailer form only) **fails on 0.17.6**.
  - **The planted-commit read** (two keys, a multi-line body, case aside) **passes on both**, as a control of
    unchanged behaviour should.

## Gates on c699e6f

| Gate | Result |
|---|---|
| `python3 test_shoalmark.py` (3.14.3) | exit=0 · 260 ok |
| `python3 test_core.py` (3.14.3) | exit=0 · 148 ok |
| `/usr/bin/python3 test_shoalmark.py` (3.9.6) | exit=0 · 260 ok |
| `/usr/bin/python3 test_core.py` (3.9.6) | exit=0 · 148 ok |
| Chrome | ran; no skip line |
| `python3 shoalmark.py --check` | exit=0 |
| `python3 shoalmark.py --html-only` | exit=0 |
| `python3 -m py_compile` (the three `.py` files) | exit=0 each |
| the tip's tests against the 0.17.6 tool | `test_shoalmark.py` exit=1 — the format check fails · `test_core.py` exit=0 |
| `--vendor` onto a scratch 0.17.6 consumer | exit=0 · `(was 0.17.6)` · only `## 0.17.7 — 2026-09-23` · PIN `OK` × 8 |

- **Not run:** CI on Linux and Windows.

## Verdict

**READY WITH FINDINGS: R1 (P3).**

- The behaviour is identical on this repository and on every planted fixture.
- The consumer's detector passes every file a pin stages.
- R1 is documentation that the same detector passes today.
