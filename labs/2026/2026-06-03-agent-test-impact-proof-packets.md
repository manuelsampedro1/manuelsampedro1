# 2026-06-03 - Agent Test Impact Proof Packets

## What Changed

Added proof-packet validation to
[`agent-test-impact`](https://github.com/manuelsampedro1/agent-test-impact).

The CLI now accepts `--proof-packet` for `agent-proof-packet.v1` JSON. It checks
that packets are complete, include passing checks, have changed-file evidence,
have no missing evidence, and match the provided diff before using packet checks
as broad test-impact evidence.

## Why It Matters

Test-impact review should distinguish nearby changed tests from broad test
passes. Before this change, proof packets could sit outside the report and a
reviewer had to manually decide whether their test checks described the same
diff.

This change keeps the distinction explicit:

- related changed tests still count as direct `covered` evidence;
- complete, diff-aligned proof packets can move a source from `missing` to
  packet-backed `partial`;
- incomplete, invalid, missing-evidence, or failing-check packets fail the CLI;
- Markdown and JSON output expose packet status and packet-backed checks.

## Verification Evidence

- Added `--proof-packet` parsing and `agent-proof-packet.v1` validation.
- Added tests for packet-backed partial evidence, incomplete packets, diff
  mismatches, JSON output, and default JSON shape.
- Added a public proof-packet fixture and smoke coverage.
- Verified the public repo with tests, lint, build, smoke, whitespace checks,
  local Git identity audit, `repo-flightcheck` at `100/100`, raw GitHub source
  URLs, and GitHub Actions success for commit `fc58abe`.

## Reusable Lesson

Treat proof-packet checks as broad test evidence, not direct coverage. They can
reduce missing evidence to partial only after packet completeness and diff
alignment are verified.
