# Contributing to shoalmark

For a bug, open an issue with the version, expected and observed behavior, and a small reproduction
using synthetic data. Propose a feature in an issue before building it. Never include credentials
or private project records; report vulnerabilities through [the security policy](SECURITY.md).
The maintainer routes accepted work into `shoalmark/org` at `teams/tool/work-tracker/`; issues do not replace
its specifications. The tool team's project is `teams/tool/`, where its rules run from an org checkout as
`python3 tools/shoalmark/shoalmark.py --root teams/tool --check`. Code and tracker changes use paired pull requests,
with review evidence filed in org naming the code repository and full reviewed commit.

## Local checks

Run the focused `test_core.py` suite and compile changed Python before committing. The full suites below are
required in the PR/release CI matrix. Every code pull request runs the suites; CI refuses added paths under
`work-tracker/`. The tracker gate runs in org's team project. Code clones use the released hooks that understand
`[trackers] elsewhere`; the code-side build-judgement rule is off until the cross-repository join is available.

Clone `https://github.com/shoalmark/shoalmark`, create a branch, and read [AGENTS.md](AGENTS.md).
The tool uses Python’s standard library. Python 3.9 and 3.12 are exercised in CI; install Subversion
so its integration checks run. Chrome/Chromium enables the browser checks.

```sh
python3 -u test_shoalmark.py
python3 -u test_core.py
```

For documentation, use Python 3.12 and an isolated environment:

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements-docs.txt
.venv/bin/python scripts/landing_facts.py
.venv/bin/zensical build --clean
.venv/bin/python scripts/llms_txt.py site
.venv/bin/python scripts/build_blog.py site
.venv/bin/python scripts/check_site.py site
.venv/bin/python scripts/landing_facts.py --check site
```

On Windows, use `.venv\Scripts\python.exe` and `.venv\Scripts\zensical.exe` instead.
`scripts/landing_facts.py` writes the landing's figures from the repository's full history before the build. It reads the
pull requests from GitHub's API without a token, which allows 60 requests an hour, or offline with
`--pulls scripts/landing_facts.pulls-1-144.json`. A local build names the tagged release VERSION names; on a release's
branch, where VERSION runs ahead of the newest tag, build as its pull request does: `--event pull_request` on both runs.
The agents’ contract is included from README.md; edit its source, not a generated copy.

Keep a pull request focused and describe the behavior change and checks run. Link its issue and
tracker where assigned. Draft PRs skip CI; opening a ready PR, marking it ready, reopening it or
pushing a revision runs CI. Maintainers may need to approve workflow runs from outside contributors.
The Owner merges after the required checks and review. A public contribution is a proposal, not a
promise of acceptance or a support deadline.
