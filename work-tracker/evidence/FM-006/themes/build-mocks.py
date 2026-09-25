#!/usr/bin/env python3
"""Rebuild the theme mockups of FM-006 (2026-09-25) from the real board: CSS only, the markup as the tool writes it.

    python3 shoalmark.py --html-only                                    # the board: work-tracker/index.html, git-ignored
    python3 work-tracker/evidence/FM-006/themes/build-mocks.py OUT [--plex DIR]
    node work-tracker/evidence/FM-006/themes/render.mjs OUT [SHOTS]     # optional: the renders, both schemes

OUT gets one page per theme, and one with the answer dialog open, beside a copy of work-tracker/brand/ and view/ (the
tracker view reads view/<id>.js). --plex is @ibm/plex-mono 1.1.0's fonts/split/woff2: the SemiBold and Italic cuts the
themes load and the repository does not carry yet; without it the browser synthesises bold and italic. Nothing is
fetched, and nothing in the repository is written.
"""
import pathlib
import shutil
import sys

HERE = pathlib.Path(__file__).resolve().parent
TRACKERS = HERE.parents[2]                                  # work-tracker/
THEMES = {                                                  # a theme is its base, then itself — as the one rule stacks them
    "monochrome": ["monochrome.css"],
    "shoalmark": ["monochrome.css", "shoalmark.css"],
    "catkin": ["monochrome.css", "catkin.css"],
    "bagels": ["monochrome.css", "bagels.css"],
    "seekarte": ["monochrome.css", "seekarte.css"],
}
ANCHOR = '<div id="B">'                                     # the themes go in after the brand's own styles, before the board
DIALOG = ("<script>addEventListener('load',()=>setTimeout(()=>{const t=T.find(x=>x[29]&&x[29][0]&&!x[29][4]);"
          "if(t)ACT(t,'accept')},50))</script>")            # the first open ask, opened as the Owner would


def main(argv):
    if not argv or argv[0].startswith("-"):
        print(__doc__)
        return 2
    out = pathlib.Path(argv[0]).resolve()
    plex = pathlib.Path(argv[argv.index("--plex") + 1]) if "--plex" in argv else None
    board = TRACKERS / "index.html"
    if not board.is_file():
        print("no board: run python3 shoalmark.py --html-only first")
        return 1
    page = board.read_text(encoding="utf-8")
    if page.count(ANCHOR) != 1:
        print(f"the board's markup has changed: {ANCHOR} is not there exactly once")
        return 1
    out.mkdir(parents=True, exist_ok=True)
    for d in ("brand", "view"):
        if (TRACKERS / d).is_dir():
            shutil.copytree(TRACKERS / d, out / d, dirs_exist_ok=True)
    if plex:
        for cut in ("SemiBold", "Italic"):
            shutil.copy2(plex / f"IBMPlexMono-{cut}-Latin1.woff2", out / "brand" / "fonts")
    for name, files in THEMES.items():
        css = "".join(f"<style>/* {f} */\n{(HERE / f).read_text(encoding='utf-8')}</style>" for f in files)
        html = page.replace(ANCHOR, css + ANCHOR)
        (out / f"{name}.html").write_text(html, encoding="utf-8")
        (out / f"{name}-dialog.html").write_text(html + DIALOG, encoding="utf-8")
    print(f"{len(THEMES)} themes, each with its dialog, in {out}" + ("" if plex else " — without --plex, bold and italic are synthesised"))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
