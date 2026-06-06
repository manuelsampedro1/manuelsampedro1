# 2026-06-06 - Expected Paths Stop at Preflight

## Context

This repo already documents the `expected_paths` contract for
[`scripts/commit_daily_update.sh`](../../scripts/commit_daily_update.sh), but
that left one practical question open: does the contract constrain the final
commit, or only the preflight before the refresh scripts run?

That distinction matters for Codex or Claude Code automation because publish
helpers often regenerate indexes or latest-proof surfaces after the initial
artifact exists. If the path contract stops too early, a later script can still
expand the final commit beyond what the automation intended to ship.

## Useful Artifact

Treat `expected_paths` in this publish flow as a preflight gate, not as a final
staging allowlist.

The current reusable rule is:

- pass the exact artifact paths you expect before publish,
- assume generated surfaces such as `labs/README.md` and `README.md` can still
  be added later by the refresh scripts,
- do not assume the final commit is limited to `expected_paths` unless you also
  validate paths after refresh or stage only an explicit post-refresh file set.

## Source Linkage

- Repo / tool / workflow: this profile repo's daily publish flow
- Supporting prompt, script, or file:
  [`../../scripts/commit_daily_update.sh`](../../scripts/commit_daily_update.sh),
  [`../../docs/automation-runbook.md`](../../docs/automation-runbook.md), and
  [`../../labs/2026/2026-06-01-expected-paths-contract-for-agent-publish-runs.md`](../../labs/2026/2026-06-01-expected-paths-contract-for-agent-publish-runs.md)

## Notes

- Observation: in a temp repo with a tracked `labs/README.md` and an existing
  file under `labs/2026/`, passing the exact new note path satisfied the
  publish preflight as expected.
- Observation: I then made the temp repo's `scripts/update_docs_index.sh`
  append one line to `docs/README.md` during the publish step, after preflight
  but before the final `git add`.
- Observation: the run succeeded and the resulting local commit included
  `docs/README.md`, the new lab note, and `labs/README.md`, even though
  `docs/README.md` was never part of `expected_paths`.
- Tradeoff: this design keeps the caller contract simple because artifact
  automations do not need to predict every generated surface file up front.
  The downside is that refresh scripts become part of the trust boundary.
- Failure mode: if a refresh script widens its edits or picks up unrelated
  managed-path changes after preflight, the final whole-surface staging step can
  still publish them.
- Practical mitigation: add a second path check after the refresh scripts run,
  or replace whole-surface staging with an explicit allowlist of the expected
  artifact plus known generated files.

## Verification

Local temp-repo verification completed for this note:

- initialized a temp Git repo with tracked `labs/README.md`, `docs/README.md`,
  and an older note under `labs/2026/`,
- copied in the real
  [`scripts/commit_daily_update.sh`](../../scripts/commit_daily_update.sh),
  configured a throwaway local Git identity, and left `origin` unset so the run
  stayed local,
- created `labs/2026/2026-06-06-preflight-only-expected-paths.md`,
  passed that exact path to the publish script, and made the temp
  `scripts/update_docs_index.sh` append to `docs/README.md`,
- inspected `git show --name-only HEAD` and confirmed the resulting commit
  contained `docs/README.md`,
  `labs/2026/2026-06-06-preflight-only-expected-paths.md`, and
  `labs/README.md`.

## Next Step

Tighten `scripts/commit_daily_update.sh` or its test fixtures so the final
staged path set cannot exceed the intended artifact plus explicitly allowed
generated surfaces.
