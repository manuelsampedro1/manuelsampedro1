# 2026-06-03 - Agent Start Gate Evidence Pointers

## What Changed

Added strict evidence-pointer gating to
[`agent-start-gate`](https://github.com/manuelsampedro1/agent-start-gate).

The CLI can now run with:

```sh
agent-start-gate check AGENT_START.md --require-evidence-pointers
```

In that mode, ready task, repo, and context evidence needs an inspectable
pointer such as a path, URL, command, run id, commit, receipt, report, or
artifact id.

## Why It Matters

The original start gate blocked missing sections, vague scope, dirty-worktree
ambiguity, missing verification, and weak stop conditions. Reusable handoffs
need one more property: the evidence behind `pass` should be traceable before
the first edit.

This change helps separate:

- packets that merely say readiness is passing;
- packets with task, repo, and context evidence a reviewer can inspect;
- pre-run gates that are ready for local use;
- pre-run gates strong enough to feed ledgers, review packets, or public proof
  notes.

## Verification Evidence

- Added opt-in `--require-evidence-pointers`.
- Added pointer detection for URLs, paths, commands, run ids, commits,
  receipts, reports, jobs, issues, PRs, and artifact ids.
- Added `has_pointer` on each evidence item and `evidence_pointer_count` in
  text and JSON output.
- Updated the example packet and smoke verification to exercise strict pointer
  mode.
- Added regression tests for strict passing packets, pass-only evidence
  failures, JSON output, and pointer detection.
- Verified the public repo with 11 tests, lint, build, smoke, whitespace
  checks, JSON smoke output, local Git identity audit, raw GitHub source URLs,
  `repo-flightcheck` at `100/100`, and GitHub Actions success for commit
  `8a65f0956a21789e97520262c4ee9cc618105450` in run `26873562122`.

## Reusable Lesson

Pre-run gates should not only ask whether evidence exists. They should require
evidence a later reviewer can inspect, especially when the packet will be
reused outside the immediate local run.
