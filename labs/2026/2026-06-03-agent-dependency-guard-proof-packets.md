# 2026-06-03 - Agent Dependency Guard Proof Packets

## What Changed

Added proof-packet validation to
[`agent-dependency-guard`](https://github.com/manuelsampedro1/agent-dependency-guard).

The CLI now accepts `--proof-packet` for `agent-proof-packet.v1` JSON. It checks
that packets are complete, include passing checks, have changed-file evidence,
have no missing evidence, and match the provided diff before mapping packet
checks to required dependency-review checks.

## Why It Matters

Dependency changes alter trust boundaries even when test output is green. A
proof packet should help reviewers inspect evidence, but it should not make a
floating version, direct URL, install script, or missing lockfile look safe.

This change keeps the boundary explicit:

- dependency findings, severity, and score still come from the diff;
- complete, diff-aligned proof packets can mark required checks as
  `evidence-found`;
- incomplete, invalid, missing-evidence, failing-check, or diff-mismatched
  packets fail the CLI;
- packet checks never lower dependency risk or remove findings.

## Verification Evidence

- Added `--proof-packet` parsing and `agent-proof-packet.v1` validation.
- Added required-check evidence mapping for dependency review checks.
- Added tests for packet-backed check evidence, incomplete packets, diff
  mismatches, JSON output, and default JSON shape.
- Added a public proof-packet fixture and smoke coverage.
- Verified the public repo with tests, lint, build, smoke, whitespace checks,
  local Git identity audit, `repo-flightcheck` at `100/100`, raw GitHub source
  URLs, and GitHub Actions success for commit `90c6339`.

## Reusable Lesson

Treat proof packets as evidence attached to dependency-review checks, not as a
dependency-risk waiver. The packet can show what was checked; the diff remains
the source of truth for dependency findings.
