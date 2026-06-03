# 2026-06-03 - Agent Evidence Chain Run Identity

## What Changed

Added run-identity gating to
[`agent-evidence-chain`](https://github.com/manuelsampedro1/agent-evidence-chain).

The CLI can now run with:

```sh
agent-evidence-chain check review-packet.json verification-envelope.json ledger-summary.json \
  --require-task-id \
  --require-run-id
```

In that mode, each artifact needs a shared run id from `run_id`, `runId`,
`agent_run_id`, `execution_id`, `session_id`, or `run`. Missing or mismatched
run ids block strict evidence reuse.

## Why It Matters

Evidence-chain checks already protect shared task, repository, and commit
identity. Reruns can still produce several artifacts for the same task and
commit, so proof chains also need a stable execution identity when they will be
reused in ledgers, closeouts, or public proof notes.

This change helps separate:

- artifacts from the same task;
- artifacts from the same commit;
- artifacts from the same agent run;
- artifacts that still need separate command, authorization, or completeness
  evidence.

## Verification Evidence

- Added opt-in `--require-run-id`.
- Added `run_id` to artifact summaries and shared identity output.
- Added optional warnings for mismatched run ids when strict mode is not active.
- Added strict failures for missing or mismatched run ids.
- Updated examples and smoke verification to exercise run identity.
- Added regression tests for matching run ids, missing run ids, mismatched run
  ids, and optional warning behavior.
- Verified the public repo with 11 tests, lint, build, smoke, whitespace checks,
  JSON smoke output, local Git identity audit, raw GitHub source URLs,
  `repo-flightcheck` at `100/100`, and GitHub Actions success for commit
  `5e6b0196b06100c9bbde4ee45291eed69330f0d5` in run `26872624681`.

## Reusable Lesson

Task and commit identity are necessary but not sufficient for multi-artifact
proof chains. Add run identity whenever reruns can produce parallel review
packets, verification envelopes, or ledger summaries.
