# 2026-06-03 - Agent Diff Splitter Proof Packets

## What Changed

Added proof-packet validation to
[`agent-diff-splitter`](https://github.com/manuelsampedro1/agent-diff-splitter).

The CLI now accepts repeated `--proof-packet` flags for `agent-proof-packet.v1`
JSON. It verifies that packets are complete, include passing checks, carry
changed-file evidence, have no missing evidence, and match the provided diff
before attaching packet checks to the split plan.

## Why It Matters

`agent-diff-splitter` is supposed to make broad diffs reviewable. Evidence is
useful only if it does not blur that boundary.

This change keeps the split strategy explicit:

- split order still comes from risk-first lane routing;
- complete, diff-aligned proof packets can attach checks to matching split
  files;
- incomplete, invalid, missing-evidence, failing-check, or diff-mismatched
  packets make the command fail;
- packet checks never reorder lanes, merge splits, or mark risky splits as
  safe.

## Verification Evidence

- Added repeated `--proof-packet` parsing and `agent-proof-packet.v1`
  validation.
- Added split-level proof-packet evidence in Markdown and JSON output.
- Added tests for packet-backed split evidence, incomplete packets, CLI diff
  mismatches, JSON packet output, and preserving risk-first ordering.
- Added a public proof-packet fixture and smoke coverage.
- Fixed a README wording false positive so `repo-flightcheck` returns
  `100/100`.
- Verified the public repo with tests, lint, build, smoke, whitespace checks,
  local Git identity audit, raw GitHub source URLs, `repo-flightcheck` at
  `100/100`, and GitHub Actions success for commit `e70ae0b`.

## Reusable Lesson

Treat proof packets as evidence attached to the split plan, not as a reason to
skip splitting. The packet can show which checks already exist; the lane order
and split boundaries remain the source of truth for review sequencing.
