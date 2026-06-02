# 2026-06-02 - Agent Context Budget Public Launch

## Source

- Public repo: https://github.com/manuelsampedro1/agent-context-budget
- Published HEAD: `c8c566ecb9015c34816ea37125d742d8a54cc508`
- CI run: https://github.com/manuelsampedro1/agent-context-budget/actions/runs/26840064454

## What Changed

Built and published `agent-context-budget`, a dependency-free Python CLI for
estimating and trimming context bundles before coding-agent handoffs.

The tool reads files or directories and checks for:

- total context budget pressure,
- single files that are too large for a useful handoff,
- exact or near-duplicate context files,
- low-signal generated paths,
- missing high-priority brief, instruction, README, or task-context files.

It emits Markdown for reviewers, JSON for automation, score gates via
`--min-score`, severity gates via `--fail-on`, and optional reports via
`--write-report`.

## Why It Matters

Long agent sessions often fail because the next run inherits too much context,
not because the task is impossible. A handoff can include the right files, stale
duplicates, generated logs, and missing task state at the same time.

`agent-context-budget` turns that ambiguity into a concrete keep, summarize, or
drop plan. It complements repo maps, handoff briefs, continuation notes, and
context-injection checks by making attention budget part of the preflight.

## Verification

Ran locally:

```sh
make test
make lint
make build
make smoke
git diff --check
```

Additional checks:

- editable install in a temporary virtualenv after upgrading `pip`, `setuptools`, and `wheel`,
- installed CLI smoke run against `examples/context/task-brief.txt`,
- `agent-instruction-audit AGENTS.md --min-score 80` at `100/100`,
- `repo-flightcheck . --check-remote --strict --threshold 80` at `100/100`,
- public raw README/source/test/example URLs returned `200`,
- GitHub Actions run `26840064454` completed with `success`.

## Takeaway

Treat context as a budget, not a pile. Before another agent continues, decide
what must be kept verbatim, what should be summarized, and what should be
dropped.
