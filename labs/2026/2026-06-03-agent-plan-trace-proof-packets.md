# 2026-06-03 - Agent Plan Trace Proof Packets

## What Changed

Added proof-packet tracing to
[`agent-plan-trace`](https://github.com/manuelsampedro1/agent-plan-trace).

The CLI now accepts `--proof-packet` for `agent-proof-packet.v1` JSON. It checks
that proof packets are complete, have passing checks, include changed-file
evidence, have no missing evidence, and match the provided diff before using
them as structured plan evidence.

## Why It Matters

Plans are only useful when completed items stay tied to evidence. Before this
change, the plan trace could inspect diffs, command logs, and closeouts, but it
could not verify structured proof artifacts from the same run.

This change makes plan review stricter:

- complete proof packets can support completed plan items and verification
  steps;
- incomplete, invalid, missing-evidence, or failing-check packets create
  high-severity issues;
- packets that do not match the provided diff fail the trace;
- Markdown and JSON reports expose packet status for reviewers.

## Verification Evidence

- Added `--proof-packet` parsing and `agent-proof-packet.v1` validation.
- Added tests for structured packet evidence, incomplete packets, diff
  mismatches, and CLI JSON output.
- Added a public proof-packet fixture and smoke coverage.
- Verified the public repo with tests, lint, build, smoke, whitespace checks,
  local Git identity audit, `repo-flightcheck` at `100/100`, raw GitHub source
  URLs, and GitHub Actions success for commit `4e6af07`.

## Reusable Lesson

Treat proof packets as plan evidence only after verifying packet completeness and
diff alignment. Otherwise a completed plan can be supported by a stale artifact
that no longer describes the current work.
