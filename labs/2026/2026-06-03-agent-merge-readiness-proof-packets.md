# 2026-06-03 - Agent Merge Readiness Proof Packets

## What Changed

Added proof-packet verification to
[`agent-merge-readiness`](https://github.com/manuelsampedro1/agent-merge-readiness).

The CLI now accepts `--proof-packet` for `agent-proof-packet.v1` JSON. It checks
that each packet is `complete`, imports its checks, and confirms the proof
packet's changed files match the current diff before those checks can support a
merge verdict.

## Why It Matters

Merge readiness should not trust a review packet just because it exists. A
packet can be stale, blocked, or generated for a different diff.

This change makes the merge gate stricter:

- a complete proof packet can supply scope, test, secret-scan, runbook, and
  rollback checks;
- a blocked or needs-review proof packet blocks merge readiness;
- a proof packet whose changed files do not match the current diff blocks the
  merge;
- Markdown and JSON output expose proof-packet findings for review.

## Verification Evidence

- Added `--proof-packet` parsing and changed-file alignment checks.
- Added tests for complete packets, incomplete packets, mismatched packet diffs,
  and CLI rendering.
- Added a public proof-packet fixture.
- Verified the public repo with tests, lint, build, smoke, whitespace checks,
  `repo-flightcheck` at `100/100`, raw GitHub source URLs, and GitHub Actions
  success for commit `9e658aa`.

## Reusable Lesson

Treat review packets as evidence only after checking that they are complete and
still describe the current diff. Otherwise a merge gate can approve yesterday's
proof for today's change.
