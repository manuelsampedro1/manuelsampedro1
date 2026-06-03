# 2026-06-03 - Agent Proof Packet Command Receipts

## What Changed

Added receipt-backed command evidence to
[`agent-proof-packet`](https://github.com/manuelsampedro1/agent-proof-packet).

The CLI now accepts `--receipt` for `agent-command-receipt.v1` JSON and
`--receipt-base-dir` for resolving receipt evidence paths. Proof packets verify
receipt status, evidence file sizes, and SHA-256 hashes before turning a receipt
into a passing check.

## Why It Matters

A proof packet should not copy a command result into a review artifact without
checking the evidence behind it. This change makes the packet stricter:

- pass receipts become reviewable command evidence;
- failed, skipped, missing, or drifted receipts block the packet;
- receipt evidence can complete a packet without requiring duplicate manual
  check strings;
- JSON and Markdown output expose the receipt verdict and findings.

## Verification Evidence

- Added command-receipt parsing and hash verification to `agent-proof-packet`.
- Added tests for valid receipts, failed receipts, receipt base directories, and
  CLI rendering.
- Added public receipt and command-output fixtures.
- Verified the public repo with tests, lint, build, smoke, whitespace checks,
  `repo-flightcheck` at `100/100`, raw GitHub source URLs, and GitHub Actions
  success for commit `784c29e`.

## Reusable Lesson

Review packets should package evidence, not launder it. When a command result
matters, attach a verified receipt so the packet can block stale or non-passing
evidence before review.
