# 2026-06-03 - Agent Release Note Check Proof Packets

## What Changed

Added proof-packet validation to
[`agent-release-note-check`](https://github.com/manuelsampedro1/agent-release-note-check).

The CLI now accepts `--proof-packet` for `agent-proof-packet.v1` JSON. It checks
that packets are complete, include passing checks, have changed-file evidence,
have no missing evidence, and match the provided diff before using packet
checks as evidence for strong verification claims in release notes.

## Why It Matters

Release notes are public maintainer-facing claims. A proof packet can make those
claims more inspectable, but it should not turn stale or unrelated evidence into
a release stamp.

This change keeps the boundary explicit:

- diff-derived findings still cover breaking, security, dependency, CI, tests,
  docs-only contradictions, and unsupported no-risk claims;
- complete, diff-aligned proof packets can support verification language such
  as `fully tested`;
- incomplete, invalid, missing-evidence, failing-check, or diff-mismatched
  packets fail the CLI;
- packet checks never suppress release-note coverage findings outside
  verification evidence.

## Verification Evidence

- Added `--proof-packet` parsing and `agent-proof-packet.v1` validation.
- Added report output for proof-packet status, verdict, passing checks, and
  packet issues.
- Added tests for packet-backed verification claims, incomplete packets, diff
  mismatches, CLI JSON output, and default JSON shape.
- Added a public proof-packet fixture and smoke coverage.
- Verified the public repo with tests, lint, build, smoke, whitespace checks,
  local Git identity audit, `repo-flightcheck` at `100/100`, raw GitHub source
  URLs, and the public CI badge for commit `5c3327e`.

## Reusable Lesson

Treat proof packets as verification evidence for release-note claims, not as a
release-risk waiver. The packet can show what was checked; the diff remains the
source of truth for release-note coverage and contradiction findings.
