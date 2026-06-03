# 2026-06-03 - Agent Change Risk Proof Packets

## What Changed

Added proof-packet validation to
[`agent-change-risk`](https://github.com/manuelsampedro1/agent-change-risk).

The CLI now accepts `--proof-packet` for `agent-proof-packet.v1` JSON. It checks
that packets are complete, include passing checks, have changed-file evidence,
have no missing evidence, and match the provided diff before mapping packet
checks to recommended gates.

## Why It Matters

Risk classification should not end at a static list of gates. Reviewers also
need to know whether a proof packet already contains evidence for those gates
without letting that evidence hide the original risk.

This change keeps the boundary explicit:

- the diff still determines risk tags, risk score, and required gates;
- complete, diff-aligned proof packets can mark gate evidence as found;
- incomplete, invalid, missing-evidence, failing-check, or diff-mismatched
  packets fail the CLI;
- packet checks never lower the risk level or remove reviewer questions.

## Verification Evidence

- Added `--proof-packet` parsing and `agent-proof-packet.v1` validation.
- Added gate-evidence mapping for recommended gates.
- Added tests for packet-backed gate evidence, incomplete packets, diff
  mismatches, JSON output, and default JSON shape.
- Added a public proof-packet fixture and smoke coverage.
- Verified the public repo with tests, lint, build, smoke, whitespace checks,
  local Git identity audit, `repo-flightcheck` at `100/100`, raw GitHub source
  URLs, and GitHub Actions success for commit `cbe3084`.

## Reusable Lesson

Treat proof packets as evidence attached to risk gates, not as risk reduction.
The packet can show which gates have supporting checks, but the diff remains the
source of truth for risk classification.
