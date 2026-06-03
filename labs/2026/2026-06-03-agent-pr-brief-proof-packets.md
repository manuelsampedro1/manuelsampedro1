# 2026-06-03 - Agent PR Brief Proof Packets

## What Changed

Added proof-packet validation to
[`agent-pr-brief`](https://github.com/manuelsampedro1/agent-pr-brief).

The CLI now accepts `--proof-packet` for `agent-proof-packet.v1` JSON. It checks
that packets are complete, include passing checks, have changed-file evidence,
have no missing evidence, and match the provided diff before using packet checks
as structured PR-description evidence.

## Why It Matters

PR descriptions are reviewer-facing. A polished description can still be wrong
if it cites stale proof or treats an incomplete packet as verification.

This change makes the PR brief gate stricter:

- complete proof packets can support verification-shaped PR claims;
- incomplete, invalid, missing-evidence, or failing-check packets block the
  audit;
- packets whose changed files do not match the diff block the audit;
- Markdown and JSON output expose packet status for reviewers.

## Verification Evidence

- Added `--proof-packet` parsing and `agent-proof-packet.v1` validation.
- Added tests for packet-supported verification claims, incomplete packets,
  diff mismatches, dotfile path preservation, and CLI JSON output.
- Added a public proof-packet fixture and smoke coverage.
- Verified the public repo with tests, lint, build, smoke, whitespace checks,
  local Git identity audit, `repo-flightcheck` at `100/100`, raw GitHub source
  URLs, and GitHub Actions success for commit `240b7fb`.

## Reusable Lesson

Treat proof packets as PR-description evidence only after checking packet
completeness and diff alignment. Otherwise a PR body can look verified while
describing a different or unfinished change.
