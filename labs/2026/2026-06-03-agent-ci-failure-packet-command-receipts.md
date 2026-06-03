# 2026-06-03 - Agent CI Failure Packet Command Receipts

## What Changed

Added failed command-receipt verification to
[`agent-ci-failure-packet`](https://github.com/manuelsampedro1/agent-ci-failure-packet).

The CLI now accepts `--receipt` for `agent-command-receipt.v1` JSON. It verifies
the receipt schema, requires status `fail`, checks that evidence files exist and
are non-empty, and compares each evidence file's size and SHA-256 hash before
turning the failed log into a CI failure packet.

## Why It Matters

Failed CI output often gets copied between tools, chats, and retries. Without a
receipt, the next agent cannot tell whether the log came from the command being
debugged or whether the evidence changed after the packet was written.

This change keeps the retry handoff tighter:

- the failing command can come from a verified receipt;
- stale, passing, missing, empty, or drifted receipt evidence fails the CLI;
- the generated packet still extracts commands, error signals, referenced files,
  summaries, suggested checks, and the next-agent prompt;
- receipt metadata is included in Markdown and JSON output for review.

## Verification Evidence

- Added `--receipt` and `--receipt-base-dir` support.
- Added strict `agent-command-receipt.v1` validation for failed receipts.
- Added evidence size and SHA-256 drift checks.
- Added tests for receipt-backed packet generation, non-failed receipt rejection,
  evidence drift rejection, and missing input handling.
- Added a public failed-receipt fixture and smoke coverage.
- Verified the public repo with tests, lint, build, smoke, whitespace checks,
  local Git identity audit, `repo-flightcheck` at `100/100`, raw GitHub source
  URLs, and GitHub Actions success for commit `c6c61df`.

## Reusable Lesson

Treat failed CI logs as evidence artifacts, not loose paste. A retry packet is
stronger when it proves which command failed and that the referenced log has not
changed.
