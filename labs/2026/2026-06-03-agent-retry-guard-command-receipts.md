# 2026-06-03 - Agent Retry Guard Command Receipts

## What Changed

Added failed command-receipt verification to
[`agent-retry-guard`](https://github.com/manuelsampedro1/agent-retry-guard).

The CLI now accepts repeated `--receipt` inputs for `agent-command-receipt.v1`
JSON. Each receipt is verified before it becomes a failed retry event: the
receipt must have status `fail`, include non-empty evidence, and match every
evidence file's recorded size and SHA-256 hash.

## Why It Matters

Retry loops often happen after the same command fails in separate agent turns.
If the evidence is only copied text, a reviewer cannot tell whether the agent
really retried the same failed command or whether the log changed between runs.

This change keeps retry-loop review stricter:

- verified failed receipts can be analyzed alongside plain transcripts;
- repeated receipt-backed commands produce the same retry-loop findings as
  transcript events;
- missing, passing, empty, or drifted receipt evidence fails the CLI;
- Markdown and JSON output keep receipt paths visible next to failed events.

## Verification Evidence

- Added `--receipt` and `--receipt-base-dir` support.
- Added strict `agent-command-receipt.v1` validation for failed receipts.
- Added evidence size and SHA-256 drift checks.
- Added tests for repeated failed receipts, non-failed receipts, evidence drift,
  and existing transcript behavior.
- Added public failed-receipt fixtures and smoke coverage.
- Verified the public repo with tests, lint, build, smoke, whitespace checks,
  local Git identity audit, `repo-flightcheck` at `100/100`, raw GitHub source
  URLs, and GitHub Actions success for commit `f714653`.

## Reusable Lesson

Treat repeated command failures as an evidence chain. A retry guard is stronger
when it proves that each failed event came from an intact command receipt, not
from unverified pasted logs.
