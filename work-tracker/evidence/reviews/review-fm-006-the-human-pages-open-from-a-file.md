# Review — FM-006, the human pages open from a file

- **Date:** 2026-09-23, 21:49 CEST (`date`)
- **Seat:** Reviewer (`reviewer@seat`) · **Session:** `8e509911/reviewer-1` · **Model:** Claude Opus 5.5
- **Tip reviewed:** `efafa12` on `fm/006-the-human-pages-open-from-a-file`
- **Base:** `62db9f8` (`origin/main`)
- **Commits:** both `Session: 8e509911/implementer-4`.
  - `37f861c`: `zensical.toml` gains `use_directory_urls = false` and drops `navigation.instant`; `docs/setup.md` and
    `docs/de/setup.md` each gain one line.
  - `efafa12`: FM-006's *What is true now* quotes the Owner, and a ship-log row names the next slice.
- **Method:** the branch and `origin/main` are archived into scratch directories and built there with Zensical 0.0.64
  from a scratch venv. `site/` never touched this worktree, and it is git-ignored (`.gitignore:4`).

## Cold start

1. **What virtue do I bring?** Doubt. "Opens from a file" has to hold link by link, and dropping a theme feature must
   not break what the served site did.
2. **How does it turn into blindness?** By blaming the change for a failure that `main` has too. So every behaviour is
   measured on both builds.
3. **What would show that failure here?** An unresolved local link; a click from `file://` that goes nowhere; a search
   that answers on `main` and not here.
4. **Who gets the record, independently of me?** The Principal seat, then the Owner. This file disposes of nothing.

## (1) Every local link of the built site

I parsed every `href` and `src` in the nine built pages:

| kind | count |
|---|---|
| page links (`<a href>`): all end in `.html`, and all resolve to a file | **103** |
| resources (styles, scripts, images): all resolve to a file | **38** |
| pure anchors | 131 |
| external | 61 |
| `404.html`'s absolute `/shoalmark/…` paths (the known exception) | 13 |

**Unresolved: 0.** The ship log's *133 of 145, 12 others* counts differently; the claim holds by my count too.

- **The build's one warning is older than this slice:** `index.md:12` links
  `agents/README.md#how-to-get-a-better-performing-human-owner`, and that anchor does not exist. `main`'s build prints
  the same warning. The file resolves; the anchor does not.

## (2) Clicked from `file://`, headless Chrome

| from | click | lands on |
|---|---|---|
| `site/index.html` | *Set up* (`./setup.html`) | *Set up in ten minutes* |
| `site/index.html` | *Deutsch* (`./de/index.html`) | the German start page (*In zehn Minuten eingerichtet*, *Ihre Antwort ist Ihr Commit* in its DOM) |
| `site/de/index.html` | `setup.html` | *In zehn Minuten eingerichtet* |
| `site/de/index.html` | `../index.html` | back to the English start page |

## (3) The configuration, and search without instant navigation

- **The configuration:** `git diff origin/main -- zensical.toml` is the one added `use_directory_urls = false` and
  `navigation.instant` removed from `features`. Nothing else moved.
- **Search index:** `search.json` is built, with 35 items on both builds. Its locations are `setup.html#…` here and
  `setup/#…` on `main`.
- **Search, served** (`python3 -m http.server`): the search button opens its box, and a query typed there answers the
  same on both builds.

  | query | branch | `main` |
  |---|---|---|
  | *signature* | 3 results, first `signing.html?h=signature` | 3 results, `signing/?h=signature` |
  | *standup* | 8 results, `standup.html?h=standup` | 8 results |

  Twice each. A first, naive probe missed the results on both builds: a race between the typed query and the search
  worker, not a defect.
- **Search from `file://`:** the box never opens, on this branch and on `main` alike. See R1.

## (4) The docs workflow's steps

- `zensical build`: exit 0, one warning, the same as on `main`.
- `python3 scripts/llms_txt.py site`: exit 0, *8 pages, each with a Markdown twin*. All 8 links in `llms.txt`
  resolve in the built site.

## (5) The German line

*Diese Seiten, gebaut mit `zensical build`: die Website öffnet sich aus `site/index.html`, oder liefern Sie sie aus:
…* is understandable but stiff. See R2.

## (6) The quote

- It is marked *(quoted, spelling normalised)*.
- It carries the Owner's requirement as the coordinator relays it: *a pitch — easy, convenient, a one-shot integration
  mostly done through your agents*.
- This seat has not seen the Owner's original words, so the wording against his is unverified here.

## (7) The gates

`python3 shoalmark.py --check` exits 0, and `python3 shoalmark.py --session-check` exits 0.

## Findings

### R1 · P3 · Search does not work from `file://`, and the new line does not say so

- **What:** Both setup pages (EN, DE) now say the built site *opens from `site/index.html`, or serve it*, as if the two
  were equal. From `file://` the search box never opens: the button is there, and no input appears. That was so on
  `main` as well. Served, search works.
- **What closes it:** Add half a sentence to each line, for example *search needs the served site* / *die Suche nur
  über den Server*.

### R2 · P3 · The German line is stiff

- **What:** *öffnet sich aus* and *liefern Sie sie aus* read as translated.
- **A proposal:** *Diese Seiten, gebaut mit `zensical build`, lassen sich direkt aus `site/index.html` öffnen — oder
  lokal bereitstellen (die Suche braucht das): `python3 -m http.server -d site 8000`.*

## Verdict

**READY WITH FINDINGS: R1 and R2 (P3).**

- Every local link of the built site resolves and ends in `.html`, apart from 404's known absolute paths.
- Clicks from `file://` work in English and German.
- Served search answers exactly as on `main`.
- The workflow's two steps exit 0.
