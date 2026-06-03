# 2026-06-03 - Agent Diff Budget Proof Packets

## What Changed

Added proof-packet validation to
[`agent-diff-budget`](https://github.com/manuelsampedro1/agent-diff-budget).

The CLI now accepts `--proof-packet` for `agent-proof-packet.v1` JSON. It checks
that packets are complete, include passing checks, have changed-file evidence,
have no missing evidence, and match the provided diff before attaching packet
checks to matching changed files in the budget report.

## Why It Matters

A diff budget is a reviewability gate. Passing checks can help reviewers see
what already ran, but they should not make an oversized or high-risk diff look
small.

This change keeps the boundary explicit:

- the budget verdict still comes from file count, line volume, and high-risk
  file count;
- complete, diff-aligned proof packets can attach passing checks to matching
  changed files;
- incomplete, invalid, missing-evidence, failing-check, or diff-mismatched
  packets fail the CLI;
- packet checks never raise budget limits or remove budget failures.

## Verification Evidence

- Added `--proof-packet` parsing and `agent-proof-packet.v1` validation.
- Added file-level proof-packet evidence in Markdown and JSON output.
- Added tests for packet-backed file evidence, incomplete packets, diff
  mismatches, invalid CLI packets, and preserving budget failures.
- Added a public proof-packet fixture and smoke coverage.
- Verified the public repo with tests, lint, build, smoke, whitespace checks,
  local Git identity audit, `repo-flightcheck` at `100/100`, raw GitHub source
  URLs, and GitHub Actions success for commit `c336a9b`.

## Reusable Lesson

Treat proof packets as evidence attached to changed files, not as a budget
waiver. The packet can show what was checked; the budget remains the source of
truth for whether the diff is reviewable as one unit.
