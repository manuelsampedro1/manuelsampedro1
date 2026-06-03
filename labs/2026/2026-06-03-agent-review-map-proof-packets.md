# 2026-06-03 - Agent Review Map Proof Packets

## What Changed

Added proof-packet validation to
[`agent-review-map`](https://github.com/manuelsampedro1/agent-review-map).

The CLI now accepts `--proof-packet` for `agent-proof-packet.v1` JSON. It checks
that packets are complete, include passing checks, have changed-file evidence,
have no missing evidence, and match the provided diff before showing packet
checks as evidence beside matching review lanes.

## Why It Matters

Review maps should route mixed diffs to the right owners even when a proof
packet exists. Evidence can help reviewers see which checks already happened,
but it should not flatten security, release, automation, docs, tests, and
application lanes into one generic approval path.

This change keeps the boundary explicit:

- the diff still determines review lanes, owners, questions, and handoff order;
- complete, diff-aligned proof packets can attach passing checks to matching
  lane files;
- incomplete, invalid, missing-evidence, failing-check, or diff-mismatched
  packets fail the CLI;
- packet checks never remove lanes, change owners, or change handoff order.

## Verification Evidence

- Added `--proof-packet` parsing and `agent-proof-packet.v1` validation.
- Added lane-level proof-packet evidence in Markdown and JSON output.
- Added tests for packet-backed lane evidence, incomplete packets, diff
  mismatches, JSON output, and default JSON shape.
- Added a public proof-packet fixture and smoke coverage.
- Verified the public repo with tests, lint, build, smoke, whitespace checks,
  local Git identity audit, `repo-flightcheck` at `100/100`, raw GitHub source
  URLs, and GitHub Actions success for commit `a7f7e9f`.

## Reusable Lesson

Treat proof packets as evidence attached to review lanes, not as review routing
replacement. The packet can show what was checked; the diff remains the source
of truth for who needs to review the change.
