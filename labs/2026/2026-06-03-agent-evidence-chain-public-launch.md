# 2026-06-03 - Agent Evidence Chain Public Launch

## What Shipped

Published [`agent-evidence-chain`](https://github.com/manuelsampedro1/agent-evidence-chain), a dependency-free Python CLI that checks whether multiple JSON evidence artifacts from one coding-agent run can be treated as one proof chain.

The tool validates shared task, repository, and commit identity; requires schema versions; catches blocking outcomes; and fails when blocker-like fields such as `blocking_findings` or `missing_evidence` are still populated.

## Why It Matters

The existing stack emits evidence from different tools: review packets, verification envelopes, ledger summaries, proof packets, output contracts, and closeout checks. Each artifact can be valid by itself while the chain is still unsafe to trust because it points at a different commit or preserves unresolved evidence.

`agent-evidence-chain` makes that boundary executable. It complements `agent-output-contract`: one validates the shape of a single output, while the other validates whether several outputs can be combined without identity drift.

## Verification Evidence

- New public repo: [`manuelsampedro1/agent-evidence-chain`](https://github.com/manuelsampedro1/agent-evidence-chain).
- Local tests: `make test` ran 8 unit tests.
- Local checks: `make lint`, `make build`, and `make smoke`.
- Packaging check: editable install in a Python 3.11 virtual environment, then `agent-evidence-chain check examples/review-packet.json examples/verification-envelope.json examples/ledger-summary.json --require-task-id --format json`.
- Repo readiness: `repo-flightcheck --check-remote --strict --threshold 80` scored `100/100`.
- Public source checks: raw GitHub URLs for README, AGENTS.md, .gitignore, CLI source, tests, CI workflow, and example JSON files returned `200`.
- CI: GitHub Actions run `26857336869` completed successfully.

## Reusable Lesson

Do not combine evidence artifacts just because each file is well-formed. Before a ledger, proof packet, or closeout reuses several outputs, check that they share task, repository, and commit identity, and fail the chain if any artifact still carries blockers or missing evidence.
