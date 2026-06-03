# 2026-06-03 - Agent Command Receipt Strict Verification

## What Changed

Added strict verification gates to
[`agent-command-receipt`](https://github.com/manuelsampedro1/agent-command-receipt).

The `verify` command now supports:

- `--require-status` to fail unless the receipt has the expected command status.
- `--min-evidence` to fail unless enough evidence files verify.
- JSON/Markdown reports that include receipt status and verification
  requirements.

## Why It Matters

Hash verification proves evidence files did not drift. It does not, by itself,
prove the command passed or that the receipt has enough evidence to reuse in a
closeout.

Strict gates make the command-receipt layer useful as an automation boundary:

- a `fail`, `skipped`, or `unknown` receipt can stay valid history without
  becoming pass evidence;
- a receipt with zero verified evidence cannot satisfy a strict proof gate;
- downstream tools can distinguish evidence integrity from claim readiness.

## Verification Evidence

- Added `verify --require-status` and `verify --min-evidence`.
- Added regression tests for failed receipts and insufficient evidence.
- Updated smoke checks to use strict receipt verification.
- Verified the public repo with tests, lint, build, smoke, whitespace checks,
  `repo-flightcheck` at `100/100`, raw GitHub source URLs, and GitHub Actions
  success for commit `2bd6795`.

## Reusable Lesson

Treat receipt integrity and claim acceptance as separate gates. A durable
receipt should be able to record any outcome, but a proof workflow should
explicitly require the outcome and evidence strength it needs.
