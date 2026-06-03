# 2026-06-03 - Agent Task Contract Acceptance IDs

## What Changed

Added stable acceptance-criteria ID gating to
[`agent-task-contract`](https://github.com/manuelsampedro1/agent-task-contract).

The CLI can now run with:

```sh
agent-task-contract check AGENT_TASK.md --require-acceptance-ids
```

In that mode, every acceptance-criteria bullet needs a stable ID such as
`AC-1`, and duplicate IDs fail the contract.

## Why It Matters

Task contracts already check for objective, acceptance criteria, context,
constraints, expected changes, verification, risks, and out-of-scope work.
Reusable agent evidence needs criterion-level handles so later artifacts can
cite exactly what they prove.

This change helps separate:

- tasks with concrete acceptance bullets;
- tasks whose criteria can be referenced by stable IDs;
- criteria ready for acceptance traces and proof packets;
- completion claims that still need verification evidence.

## Verification Evidence

- Added opt-in `--require-acceptance-ids`.
- Added `acceptance_criteria_count`, `acceptance_id_count`,
  `acceptance_ids`, and `acceptance_ids_required` to JSON output.
- Added text output with `Acceptance ids`.
- Added duplicate-ID and missing-ID failures.
- Updated the template, sample contract, README, and smoke verification.
- Added regression tests for strict passing contracts, anonymous bullets,
  duplicate IDs, JSON output, and bracketed IDs.
- Verified the public repo with 10 tests, lint, build, smoke, whitespace
  checks, JSON smoke output, local Git identity audit, raw GitHub source URLs,
  `repo-flightcheck` at `100/100`, and GitHub Actions success for commit
  `701210e81a54c8556cd4b513c169d2058ae6cadb` in run `26874263424`.

## Reusable Lesson

Acceptance criteria should be traceable before work starts. Stable IDs do not
prove completion, but they make downstream traces, packets, ledgers, and
closeouts less ambiguous.
