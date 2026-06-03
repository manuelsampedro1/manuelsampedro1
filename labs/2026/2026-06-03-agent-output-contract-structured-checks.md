# 2026-06-03 - Agent Output Contract Structured Checks

## What Changed

Added structured-check gating to
[`agent-output-contract`](https://github.com/manuelsampedro1/agent-output-contract).

The CLI can now run with:

```sh
agent-output-contract check output.json --require-checks
```

In that mode, a passing output needs a non-empty `checks` list. Each check must
be a structured object with a name and outcome, and a passing output cannot
include a non-passing check.

## Why It Matters

Agent workflow outputs often become inputs to CI summaries, ledgers, review
packets, profile proof, or merge gates. A bare `status: pass` can be too weak
for automation because it does not show what actually passed.

This change helps separate:

- outputs with valid JSON shape;
- outputs with a clear outcome;
- outputs with blocking evidence when they fail;
- passing outputs that also carry structured check evidence.

## Verification Evidence

- Added opt-in `--require-checks`.
- Added `check_count` to text and JSON file reports.
- Added validation for structured check objects with non-empty names and exactly
  one outcome field.
- Added a blocker when a passing output includes a failed, blocked, partial, or
  needs-review check.
- Updated smoke verification and the passing fixture to exercise structured
  checks.
- Added regression tests for missing checks, non-object checks, missing check
  names, missing check outcomes, failed checks inside passing outputs, and JSON
  CLI output.
- Verified the public repo with tests, lint, build, smoke, whitespace checks,
  local Git identity audit, raw GitHub source URLs, `repo-flightcheck` at
  `100/100`, and GitHub Actions success for commit
  `aa3be512f2f637c161a731c93bdc81b33244c091` in run `26871070810`.

## Reusable Lesson

Structured outputs should not only say whether they passed. When another agent,
ledger, CI job, or proof packet will consume the output, it should expose which
checks were evaluated and whether any of them contradicted the overall outcome.
