# v0.19.0 — the scoped check of the board's link's test, at aa4a07c

Verdict: **READY** — no finding; RV-2290 … RV-2294 unused.
Reviewed: aa4a07c954cd2550d68759058dddd3266fefbea9 — `git diff 1b69681 aa4a07c`, test_shoalmark.py +3 −3, on the Owner's ruling filed in FM-006 at 1b69681 (*The board's link's test, on Windows*).
Reviewer: b3bdb000/reviewer-80 (claude-opus-5-5, xhigh), the reviewer's bot address, unsigned, worktree shoalmark-review-11, 18:39–18:45 CEST on 2026-10-01. Independence: the builds' session (b3bdb000), so not independent. Tier: code (a test).

1. **The line and the check.** Line 165 parses only the URI after the `board: ` prefix, once, into `read_back_`. The check compares `read_back_ == board_` strictly: no second parse, no `.resolve()`. `board_` hangs from `root`, which the block makes as `Path(d).resolve()`.
2. **Run before and after, on macOS.** With the old line 165 under the new strict check, the check fails. It read back `' file:/private/var/folders/…/docs/work-tracker/index.html'` from `'board: file:///private/var/folders/…/index.html'`: `urlparse` takes `board` for the scheme. With the fix the block passes, 18 ok.
3. **Windows, by reading.** The tool prints `HTML_OUT.resolve().as_uri()`, which is `file:///C:/…`, and `url2pathname('/C:/…')` (`nturl2path`) gives `C:\…`. The old whole-line parse fed it `' file:///C:/…'`, two colons, hence *Bad URL*. 8.3 names in the runner's TEMP: `Path(d).resolve()` expands them on 3.9 and 3.12, and the tool resolves the same `--root` again, so both sides carry the long form. Case: `WindowsPath` compares without case, and `url2pathname` only upper-cases the drive. Percent-encoding round-trips through `quote` and `unquote`, and the runner's path needs none. Nothing I can see makes the two differ on the Windows runners; CI on this head is the proof.
4. **Nothing else.** The delta touches test_shoalmark.py only. `shoalmark.py` is `22cd0e9e…`, once in each note, and neither the tool nor the notes changed since 5ffa3d2. `--check` exits 0 at the tip.

Quality read: the fix makes the check stricter as well as right, and the message now shows what was read back. Clean.
Next: CI on this verdict's head, then the Owner's merge.
