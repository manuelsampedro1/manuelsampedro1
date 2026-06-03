# 2026-06-03 - Agent Acceptance Trace Proof Packets

## What Changed

Added proof-packet validation to
[`agent-acceptance-trace`](https://github.com/manuelsampedro1/agent-acceptance-trace).

The CLI now accepts `--proof-packet` for `agent-proof-packet.v1` JSON. It checks
that packets are complete, include passing checks, have changed-file evidence,
have no missing evidence, and match the provided diff before using packet checks
as structured acceptance evidence.

## Why It Matters

Acceptance criteria are the contract between a requested task and a final
closeout. If the trace can only read prose, a stale proof artifact can sit beside
the closeout without being checked against the current diff.

This change makes acceptance review stricter:

- complete proof packets can support criterion evidence;
- incomplete, invalid, missing-evidence, or failing-check packets fail the CLI;
- packets whose changed files do not match the diff fail the CLI;
- Markdown and JSON output expose packet status for reviewers.

## Verification Evidence

- Added `--proof-packet` parsing and `agent-proof-packet.v1` validation.
- Added tests for packet-supported criteria, incomplete packets, diff
  mismatches, JSON output, and proof-packet CLI reporting.
- Added a public proof-packet fixture and smoke coverage.
- Verified the public repo with tests, lint, build, smoke, whitespace checks,
  local Git identity audit, `repo-flightcheck` at `100/100`, raw GitHub source
  URLs, and GitHub Actions success for commit `10ac282`.

## Reusable Lesson

Treat proof packets as acceptance evidence only after verifying packet
completeness and diff alignment. Otherwise a criterion can look covered by an
artifact that no longer describes the current task.
