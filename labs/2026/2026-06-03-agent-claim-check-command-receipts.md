# 2026-06-03 - Agent Claim Check Command Receipts

## What Changed

Added verified command-receipt support to
[`agent-claim-check`](https://github.com/manuelsampedro1/agent-claim-check).

The CLI now accepts `--receipt` for `agent-command-receipt.v1` JSON, verifies
the receipt's evidence file sizes and SHA-256 hashes, and only uses valid pass
receipts as command evidence for closeout claims.

## Why It Matters

`--ran-command` is useful, but it is still a caller-provided string. A reviewer
gets stronger evidence when the command claim is tied to hashed output files.

This closes another gap in the closeout chain:

- `agent-command-receipt` records hashed command output.
- `agent-claim-check` verifies that receipt before accepting the command claim.
- `agent-run-ledger` can preserve the same receipt as durable run evidence.

If receipt evidence drifts, goes missing, has no evidence files, or records a
non-pass status, the closeout stays blocked.

## Verification Evidence

- Added receipt parsing and evidence hash verification to `agent-claim-check`.
- Added tests for valid receipts, drifted evidence, and CLI `--receipt` usage.
- Added a public command-output and receipt fixture.
- Verified the public repo with tests, lint, build, smoke, whitespace checks,
  `repo-flightcheck` at `100/100`, raw GitHub source URLs, and GitHub Actions
  success for commit `56773df`.

## Reusable Lesson

Do not let closeout claims rely only on a repeated command string. Let a receipt
prove the command evidence still matches, then let the claim checker decide
whether the closeout is supported.
