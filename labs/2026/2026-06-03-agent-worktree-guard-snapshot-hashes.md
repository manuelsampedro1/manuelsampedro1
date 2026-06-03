# 2026-06-03 - Agent Worktree Guard Snapshot Hashes

## What Changed

Added snapshot-integrity verification to
[`agent-worktree-guard`](https://github.com/manuelsampedro1/agent-worktree-guard).

The CLI now prints a SHA-256 digest when `snapshot --output` writes the
pre-agent dirty-tree snapshot. The later `check` command can require that
digest with `--expect-snapshot-sha256` before it trusts the snapshot contents.
Markdown and JSON reports also include the actual snapshot hash used for the
comparison.

## Why It Matters

Worktree guards protect user edits only if the baseline snapshot is the same
artifact captured before the agent run. A changed snapshot can hide a protected
dirty file and make a later check look safe.

This change makes the baseline reusable as evidence:

- the pre-run handoff can store the snapshot digest;
- the post-run guard blocks tampered or stale snapshot files;
- the report carries the digest for ledgers, closeouts, and review packets;
- existing flows still work when the hash gate is not needed.

## Verification Evidence

- Added snapshot-file hashing and strict 64-character SHA-256 validation.
- Added `--expect-snapshot-sha256` for the `check` command.
- Added `snapshot_sha256` to JSON output and a `Snapshot Evidence` section to
  Markdown output.
- Added regression tests for valid hashes, tampered snapshots, invalid hashes,
  and JSON report evidence.
- Updated smoke coverage so the example flow records and reuses the snapshot
  hash.
- Verified the public repo with tests, lint, build, smoke, whitespace checks,
  local Git identity audit, raw GitHub source URLs, `repo-flightcheck` at
  `100/100`, and GitHub Actions success for commit `b99edb5`.

## Reusable Lesson

Snapshot files are authority-bearing artifacts. If a guard relies on a baseline
captured before an agent run, preserve a digest beside the handoff and require
that digest before the post-run check.
