# Organization migration and public-repository hardening — validation

Principal session `01a0ec25`, `shoalmark-principal-migration`, 2026-09-29.
This is the author's validation record, **not a Reviewer verdict**.

## Scope and authority

The Owner requested moving his last Zensical commit onto a migration branch, then explicitly
included public-repository hardening, a header Docs link to setup.html, and the lighter commit hook.
His commit `d1a269b` is preserved unchanged. The branch starts at `1c344ed` plus that commit.
No release tag, remote-main push, PR opening or merge is performed by this seat.
The FM-006 tracker records the live GitHub settings and the earlier interrupted commits.

## Checks

- Zensical 0.0.66 clean build: no issues; `llms_txt.py` produces 11 Markdown twins.
- `scripts/check_site.py site`: required entry pages, rendered README contract, landing destinations
  and absence of old public URLs pass. A literal include substituted into the contract and a removed
  signing page each cause failure in copied build fixtures.
- Hook YAML and all GitHub YAML files parse. The exact syntax-hook command was extracted from YAML
  and exercised in a disposable repository: invalid staged source with a valid worktree copy fails;
  valid staged source with an invalid worktree copy passes; the filename contains a space.
- The focused core suite passed before the hook split; the replacement hook runs it again at commit.
  Both full suites stay in the required five-job PR/release matrix, with unbuffered output.
- The earlier author commit reached Python 3.9 after its Python 3.14 suites passed for the initial
  migration snapshot. Both the author's duplicate commit and the Owner's subsequent commit were
  interrupted. These are not complete full-suite results for the final branch.
- Read-back verified the organization's Pages URL and public repository state, active PR ruleset
  with five Actions-bound suite contexts, empty bypass, force-push/deletion protections, read-only
  default workflow token, all-external-contributor workflow approval, enabled secret scanning/push
  protection/Dependabot security fixes/private vulnerability reporting.
- Secret scanning returned zero open alerts on the first API page during enablement. A filename
  screen across 481 unique paths in reachable local-ref history found no credential-shaped names.
  Neither establishes a full secret/privacy audit of historical content or attachments.

## Review boundary and handoff

A same-parent-session preparatory Reviewer found the broken contract include and confirmed the fix;
it did not issue final clearance. Two independent-session attempts could not complete:
Claude session `42d5df91-1a1b-46f4-a942-00163c0ff3a5` refused at the weekly usage limit;
Codex session `01a0ed51-f223-7341-8d4a-4fe08b53f395` started a read and then hit its usage limit.
There is **no independent critical-change verdict**. A fresh Reviewer must inspect the final pushed
head before this branch is called ready. CI, once the Owner opens a non-draft PR, must pass all five
required suite checks. After merge, manually run the docs workflow on main; do not deploy the old
main's personal-account links. Consumers get the tool link changes at a future release/vendor.

Conclusion: implemented and locally checked; review and PR CI remain. The counterfact is that a
successful site build did not originally prove the contract rendered; the negative controls now
reject that failure. No output here grants merge authority or certifies unrun CI.

## Independent review R1 follow-up

The Owner relayed the independent Reviewer's P2: four README links broke in the newly rendered
agent contract, while the landing-only check passed. README now links AGENTS.md, LICENSE-APACHE,
LICENSE-MIT and NOTICE to `https://github.com/shoalmark/shoalmark/blob/main/` destinations.
The checker parses both landing and contract pages, resolving relative site links from each page
and checking same-repository blob/main files against the source checkout (no network needed in CI).

Validation on 2026-09-29:
- Pinned Zensical clean build, llms generation and site check passed.
- All four exact rendered URLs passed `curl --fail --location` HTTP checks.
- For each URL separately, a temporary `-missing` target in generated contract HTML made the checker
  fail with `broken repository link`; restoring the original relative AGENTS.html made it fail with
  `broken link`. Generated HTML was restored in a finally block; the site check passes again.
- Independent re-verification and full required PR CI remain pending; this is fix evidence, not a verdict.
