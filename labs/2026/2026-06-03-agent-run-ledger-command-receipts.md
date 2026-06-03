# 2026-06-03 - Agent Run Ledger Command Receipts

## What Changed

Added command-receipt import support to
[`agent-run-ledger`](https://github.com/manuelsampedro1/agent-run-ledger).

The new `import-receipt` command accepts `agent-command-receipt.v1` JSON,
checks referenced evidence file sizes and SHA-256 hashes, then imports the
command outcome into the ledger.

## Why It Matters

Agent closeouts often reuse command claims after the original terminal output
has disappeared from context. A run ledger is stronger when it can preserve not
only the command sentence, but also the hashed files behind that command claim.

This closes a useful gap in the proof stack:

- `agent-command-receipt` records hashed command evidence.
- `agent-run-ledger` now verifies and preserves that receipt as durable run
  evidence.
- `doctor --strict` keeps the run open when the receipt is unknown, missing, or
  drifted.

## Verification Evidence

- Added parser and evidence-verification coverage for `agent-command-receipt.v1`.
- Added CLI coverage for `import-receipt`.
- Added a public fixture under `examples/` and verified the README command
  path imports it cleanly.
- Verified the public repo with direct Node tests, lint, build, whitespace
  checks, raw GitHub source URLs, `repo-flightcheck`, and GitHub Actions success
  for commit `df86dc8`.

## Reusable Lesson

Treat command output as evidence with integrity, not as chat prose. If a closeout
claims a command passed, preserve a receipt and make the ledger verify that the
referenced evidence still matches.
