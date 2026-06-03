# 2026-06-03 - Agent Source Grounding Concrete Pointers

## What Changed

Added concrete-pointer gating to
[`agent-source-grounding`](https://github.com/manuelsampedro1/agent-source-grounding).

The CLI can now run with:

```sh
agent-source-grounding check docs/*.md --require-sources --require-concrete
```

In that mode, source-shaped prose such as `Source: manual review` is not enough
to ground a claim. The artifact must point to something inspectable: a URL,
file path, command/log, run/job/artifact ID, issue/PR reference, receipt,
report, or commit.

## Why It Matters

Agent-written notes often include source language that looks reviewable but
does not let a reviewer open anything. That is risky when a Markdown note, JSON
claim file, review packet, or profile proof becomes reusable evidence.

This change helps separate:

- claims with no source or evidence;
- claims with placeholder citations;
- claims with vague source-shaped prose;
- claims with concrete pointers a reviewer can inspect.

## Verification Evidence

- Added opt-in `--require-concrete`.
- Added `concrete_source_count` to text and JSON artifact summaries.
- Added concrete-pointer detection for URLs, repo paths, commands/logs, run
  IDs, job/artifact IDs, issue/PR references, receipts, reports, and commits.
- Updated smoke verification to exercise `--require-concrete`.
- Added regression tests for grounded Markdown/JSON passing the concrete gate
  and vague Markdown/JSON sources failing it.
- Verified the public repo with tests, lint, build, smoke, whitespace checks,
  local Git identity audit, raw GitHub source URLs, `repo-flightcheck` at
  `100/100`, and GitHub Actions success for commit
  `e721d9151023e53fdaa13872a162dc33f5b2317c` in run `26870530391`.

## Reusable Lesson

Grounding should not reward source-shaped prose. If a claim will become public
proof or durable agent context, it should carry a pointer that another reviewer
can actually inspect.
