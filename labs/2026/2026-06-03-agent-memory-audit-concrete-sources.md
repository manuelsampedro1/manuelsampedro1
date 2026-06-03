# 2026-06-03 - Agent Memory Audit Concrete Sources

## What Changed

Added concrete-source checks to
[`agent-memory-audit`](https://github.com/manuelsampedro1/agent-memory-audit).

The CLI now distinguishes between source language and reusable source
evidence. A memory line such as `Sources: manual note.` no longer protects a
current-state claim from review. The nearby source must point to something a
future reviewer can inspect, such as a URL, file path, command/log, run ID,
issue/PR, receipt, report, or commit.

## Why It Matters

Agent memory often looks safer than it is because it contains words like
`verified` or `Sources:`. Those markers are useful only when they lead to
inspectable evidence.

This change helps catch:

- current-state claims backed only by vague source text;
- source lines that accidentally bleed into the next Markdown bullet;
- memory handoffs that need a concrete command, log, report, commit, or link
  before another agent treats the claim as reusable context.

## Verification Evidence

- Added a medium-severity `weak-source-evidence` finding.
- Added `concrete_source_mentions` to per-file JSON and Markdown summaries.
- Kept source lookup local to the same Markdown paragraph or list item so a
  source for one memory entry cannot cover the next entry.
- Updated the risky example to show generic source language.
- Added regression tests for weak source evidence, concrete source evidence,
  and source boundaries between adjacent list items.
- Verified the public repo with tests, lint, build, smoke, whitespace checks,
  local Git identity audit, raw GitHub source URLs, `repo-flightcheck` at
  `100/100`, and GitHub Actions success for commit
  `a415519ec418f2ab575ba444482870729b47a309` in run `26869899813`.

## Reusable Lesson

Memory audit output should not reward source-shaped prose. If a future agent is
expected to reuse a claim, the memory should point at evidence that can be
opened, checked, or hashed.
