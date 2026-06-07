# 2026-06-07 - Publish Guard Coverage Stops at No-Op

## Context

This repo now has public guidance for two important
[`scripts/commit_daily_update.sh`](../../scripts/commit_daily_update.sh)
contracts:

- callers must pass exact `expected_paths` for the intended artifact, and
- that path contract stops at preflight unless the flow checks paths again
  after refresh.

Those rules are documented in public notes and recipes, but I wanted to check
whether the repo's executable verification actually guards them.

## Useful Artifact

Treat documented publish-guard rules as test obligations, not only as notes.

For a recurring coding-agent publish flow, the minimum fixture set should cover:

- unexpected managed-path changes failing preflight,
- the exact intended artifact path passing preflight, and
- post-refresh path widening either failing explicitly or being asserted as a
  known limitation until the script changes.

Without those fixtures, green repo verification only proves the script parses
and the no-op path still behaves, not that the publish boundary is trustworthy.

## Source Linkage

- Repo / tool / workflow: this profile repo's daily publish and verification
  flow
- Supporting prompt, script, or file:
  [`../../scripts/commit_daily_update.sh`](../../scripts/commit_daily_update.sh),
  [`../../scripts/verify_profile.sh`](../../scripts/verify_profile.sh),
  [`../../tests/test_commit_daily_update.sh`](../../tests/test_commit_daily_update.sh),
  [`2026-06-01 - Expected Paths Contract for Agent Publish Runs`](./2026-06-01-expected-paths-contract-for-agent-publish-runs.md),
  and
  [`2026-06-06 - Expected Paths Stop at Preflight`](./2026-06-06-expected-paths-stop-at-preflight.md)

## Notes

- Observation: [`../../scripts/verify_profile.sh`](../../scripts/verify_profile.sh)
  does run syntax checks, Python checks, unit tests, and
  [`../../tests/test_commit_daily_update.sh`](../../tests/test_commit_daily_update.sh)
  before treating the repo as verified.
- Observation:
  [`../../tests/test_commit_daily_update.sh`](../../tests/test_commit_daily_update.sh)
  builds a temp repo, copies
  [`../../scripts/commit_daily_update.sh`](../../scripts/commit_daily_update.sh),
  creates no-op refresh scripts, adds `README.md`, leaves `scratch.log`
  untracked, and asserts the output contains `No useful changes to commit.` plus
  the residual-change warning.
- Observation: the test never passes `expected_paths`, never creates a managed
  public-path change that should be rejected, and never mutates a tracked file
  after preflight to inspect the final committed path set.
- Tradeoff: this current test is cheap and stable because it avoids mutating
  public surfaces, but it only locks in one narrow branch of the publish flow.
- Failure mode: a future edit can weaken or break exact-path enforcement, or
  keep widening final staged paths after refresh, while `make test`, `make
  lint`, and `make build` still pass because they all funnel through the same
  narrow fixture.
- Practical mitigation: add temp-repo cases for `expected_paths` rejection,
  `expected_paths` success, and a post-refresh mutation that asserts whether the
  current known limitation still exists or has been fixed.

## Verification

Checked locally for this note:

- read
  [`../../scripts/commit_daily_update.sh`](../../scripts/commit_daily_update.sh)
  to confirm where `expected_paths` preflight runs and where whole-surface
  staging still happens,
- read [`../../scripts/verify_profile.sh`](../../scripts/verify_profile.sh) to
  confirm all repo verification routes through the same publish-script fixture,
- read
  [`../../tests/test_commit_daily_update.sh`](../../tests/test_commit_daily_update.sh)
  and confirmed it only exercises the no-op plus residual-warning path,
- compared the current test coverage against the already published behavior
  notes from
  [`2026-06-01 - Expected Paths Contract for Agent Publish Runs`](./2026-06-01-expected-paths-contract-for-agent-publish-runs.md)
  and
  [`2026-06-06 - Expected Paths Stop at Preflight`](./2026-06-06-expected-paths-stop-at-preflight.md).

## Next Step

Extend [`../../tests/test_commit_daily_update.sh`](../../tests/test_commit_daily_update.sh)
with explicit fixtures for `expected_paths` pass/fail behavior and the
post-refresh path-widening boundary.
