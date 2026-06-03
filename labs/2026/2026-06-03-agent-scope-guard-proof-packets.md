# 2026-06-03 - Agent Scope Guard Proof Packets

## What Changed

Added proof-packet validation to
[`agent-scope-guard`](https://github.com/manuelsampedro1/agent-scope-guard).

The CLI now accepts repeated `--proof-packet` flags for `agent-proof-packet.v1`
JSON. It verifies that packets are complete, include passing checks, carry
changed-file evidence, have no missing evidence, and match the same diff or path
list before showing packet checks beside the scope report.

## Why It Matters

Scope guards are useful because they enforce the task boundary. Passing checks
should not become a reason to accept unrelated files.

This change keeps the boundary explicit:

- the scope verdict still comes from the declared allowlist;
- complete, diff-aligned proof packets can show checks for matching paths;
- incomplete, invalid, missing-evidence, failing-check, or diff-mismatched
  packets make the command fail;
- packet checks never authorize unexpected paths.

## Verification Evidence

- Added repeated `--proof-packet` parsing and `agent-proof-packet.v1`
  validation.
- Added proof-packet evidence in text and JSON output.
- Added tests proving valid packets do not override unexpected paths,
  incomplete packets fail even when scope passes, and mismatched packets fail.
- Added a public proof-packet fixture and smoke coverage.
- Verified the public repo with tests, lint, build, smoke, whitespace checks,
  local Git identity audit, raw GitHub source URLs, `repo-flightcheck` at
  `100/100`, and GitHub Actions success for commit `8effd0d`.

## Reusable Lesson

Treat proof packets as evidence about what was checked, not as authority to
widen the task. The allowlist remains the source of truth for whether a changed
path is in scope.
