---
id: FM-052
status: Proposed
considered: FM-045, FM-039, FM-032
tags: bug
next: wait
hook: "A fixture that watches .git lets git's own housekeeping run inside the watch, so a green commit can fail once"
---

# FM-052 — a fixture that watches .git lets git's own housekeeping run inside the watch

## What is true now

**Filed 2026-10-15; nothing is built.** Held against FM-045, which is Shipped and owns the board matrix watched by
git's own trace.

**Facts.**
- #179's run `38744072206`, on `70e3b64`: Ubuntu 3.9 ended in a traceback from `rm_git` (`test_shoalmark.py:62`,
  called at `:6467`). `shutil.rmtree` lost a race with git's background housekeeping: a file under `.git/objects/`
  vanished, and the handler's `chmod` raised again. The suite stopped, so `test_core.py` did not run on 3.9. #179's fix
  round made `rm_git` skip a file that is already gone (`acc35ec`); this tracker's class fix remains.
- #176's run `38683460470`, attempt 1, on head `a36a91e`: Ubuntu 3.12 failed one check, *FM-045 · the board matrix,
  watched by git's own trace · answer branches · `git merge --no-ff`*.
  - It saw `.git changed by 1 run(s), 43 path(s)`, each `object objects/… gone`.
  - The other four jobs passed.
- Attempt 2 of the same commit passed on all five jobs.
- At main `aa482d4`, `test_shoalmark.py` sets neither `gc.auto` nor `maintenance.auto` anywhere.

**Likely cause (the Auditor's; 70 % here):** Git's automatic housekeeping packed the fixture's loose objects inside the
watched window. That would be `gc --auto` or `maintenance run --auto` after the merge, or a detached auto-gc that an
earlier setup command started and that was still running.

**Fix:** each fixture that watches `.git` sets `gc.auto=0` and `maintenance.auto=false` when it is created. It must be
at `git init`, not only before the watch, so that no detached gc from setup can still be running.

**Test for the class:**
- every fixture repository the suites watch for `.git` changes has Git's housekeeping off. The watcher asserts it
  before it records, and fails by name otherwise;
- a mutant that drops either setting fails;
- a probe that starts a background `git gc` during a watched run shows the watcher reporting it, so the watch stays
  sensitive.

**Tier:** code, with the full review loop; test code only. It ships in v0.20.1 (FM-023's table of 2026-10-15).

## Done when

Every fixture the suites watch for `.git` changes has git's housekeeping off from `git init`, the watcher asserts it
before it records, and the class test with its mutant and its background-gc probe is in CI.

## Ship log

| Date | Event |
|---|---|
| 2026-10-15 | Filed. |
