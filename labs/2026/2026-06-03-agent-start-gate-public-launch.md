# 2026-06-03 - Agent Start Gate Public Launch

## What Shipped

Published [`agent-start-gate`](https://github.com/manuelsampedro1/agent-start-gate), a dependency-free Python CLI that checks whether a coding-agent run should start before the first edit.

The tool reads a Markdown start packet and blocks when the packet lacks a concrete objective, explicit scope, input evidence, worktree state, context screening, verification commands, or stop conditions.

## Why It Matters

The existing stack already checks raw requests, task contracts, repo readiness, context safety, worktree drift, and closeout evidence. The missing step was a final pre-run gate that asks whether there is enough evidence to let this agent begin now.

`agent-start-gate` keeps that decision small and executable. It does not call other tools or require a hosted service; it verifies that their evidence is present before the run starts.

## Verification Evidence

- New public repo: [`manuelsampedro1/agent-start-gate`](https://github.com/manuelsampedro1/agent-start-gate).
- Local tests: `make test` ran 8 unit tests.
- Local checks: `make lint`, `make build`, and `make smoke`.
- Packaging check: editable install in a temporary virtual environment, then `agent-start-gate check examples/agent-start-packet.md`.
- Repo readiness: `repo-flightcheck --check-remote --strict --threshold 80` scored `100/100`.
- Public source checks: raw GitHub URLs for README, CLI source, tests, and CI workflow returned `200`.

## Reusable Lesson

Pre-run quality should not rely on a confident instruction block. A start packet should name the objective, allowed scope, input evidence, clean or documented worktree state, trusted and untrusted context, verification commands, and exact stop conditions before a coding agent touches files.

