# 2026-06-03 - Agent Closeout Check Proof Packets

## What Changed

Added proof-packet verification to
[`agent-closeout-check`](https://github.com/manuelsampedro1/agent-closeout-check).

The CLI now accepts `--proof-packet` for `agent-proof-packet.v1` JSON. It checks
that the packet is `complete`, has passing checks, includes changed-file
evidence, has no missing evidence, and covers files cited by the closeout.

The packet can supply changed-path evidence, but it does not replace the
closeout's own `Verification` section with an exact command or check.

## Why It Matters

A final answer can look reviewable while pointing at a stale or incomplete proof
packet. That creates a second-order evidence problem: the closeout appears to
have proof, but nobody checked whether the proof packet was valid for this
answer.

This change makes closeout review stricter:

- a complete proof packet can supply changed-path evidence;
- an incomplete, invalid, or evidence-missing packet fails the closeout;
- a packet that does not cover closeout file references fails the closeout;
- text and JSON output expose packet status for reviewers.

## Verification Evidence

- Added `--proof-packet` parsing and `agent-proof-packet.v1` validation.
- Added tests for complete packets, incomplete packets, wrong schemas, file
  reference coverage, and CLI JSON output.
- Added a public proof-packet fixture and smoke coverage.
- Verified the public repo with tests, lint, build, smoke, whitespace checks,
  local Git identity audit, `repo-flightcheck` at `100/100`, raw GitHub source
  URLs, and GitHub Actions success for commit `8984a86`.

## Reusable Lesson

Treat proof packets as closeout evidence only after checking that they are
complete and aligned with the files the final answer cites. A closeout should
not launder stale packet evidence into a confident handoff.
