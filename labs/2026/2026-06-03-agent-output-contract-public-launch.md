# 2026-06-03 - Agent Output Contract Public Launch

## What Shipped

Published [`agent-output-contract`](https://github.com/manuelsampedro1/agent-output-contract), a dependency-free Python CLI that validates JSON outputs from coding-agent workflow tools before automation trusts them as evidence.

The tool checks for valid JSON objects, non-placeholder `schema_version`, one clear outcome field, recognized outcomes, score range, list-shaped issue fields, blocker consistency, and obvious secret or local-path leakage.

## Why It Matters

The existing stack already creates many JSON envelopes: readiness reports, proof packets, verification outputs, ledgers, and closeout checks. A malformed output can make downstream automation treat weak evidence as usable, or hide a blocker behind a confident status field.

`agent-output-contract` keeps that boundary executable. A failing tool output can still be a valid contract if it includes actionable issues; the contract fails when the JSON itself is ambiguous, contradictory, or unsafe to reuse.

## Verification Evidence

- New public repo: [`manuelsampedro1/agent-output-contract`](https://github.com/manuelsampedro1/agent-output-contract).
- Local tests: `make test` ran 11 unit tests.
- Local checks: `make lint`, `make build`, and `make smoke`.
- Packaging check: editable install in a temporary virtual environment, then `agent-output-contract check examples/pass-output.json`.
- Repo readiness: `repo-flightcheck --check-remote --strict --threshold 80` scored `100/100`.
- Public source checks: raw GitHub URLs for README, CLI source, tests, CI workflow, and example JSON files returned `200`.

## Reusable Lesson

Structured output is only useful if downstream automation can trust its shape. Gate JSON evidence before it enters CI summaries, ledgers, or review packets: require a schema version, one outcome, clear blocker semantics, bounded score fields, and no obvious private local artifacts.

