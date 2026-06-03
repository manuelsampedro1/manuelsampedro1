# 2026-06-03 - Agent Source Grounding Public Launch

## What Shipped

Published [`agent-source-grounding`](https://github.com/manuelsampedro1/agent-source-grounding), a dependency-free Python CLI that audits agent-written Markdown and JSON artifacts for explicit source and evidence grounding before public docs, decisions, review packets, or profile proof reuse their claims.

The tool checks for source/evidence sections, grounded claim rows, placeholder citation language, claim-like phrases without nearby grounding, JSON claim source fields, and optional HTTP link verification.

## Why It Matters

The agent workflow stack now produces review packets, ledgers, proof bundles, closeouts, recipes, and lab notes. Those artifacts can be structurally valid while still preserving ungrounded claims. That is a different failure mode from invalid JSON, mismatched evidence chains, or weak closeout wording.

`agent-source-grounding` makes the source boundary executable. It does not claim to verify truth; it checks whether a reviewer has something inspectable before a claim becomes public evidence.

## Verification Evidence

- New public repo: [`manuelsampedro1/agent-source-grounding`](https://github.com/manuelsampedro1/agent-source-grounding).
- Local tests: `make test` ran 8 unit tests.
- Local checks: `make lint`, `make build`, and `make smoke`.
- Packaging check: editable install in a Python 3.11 virtual environment, then `agent-source-grounding check examples/grounded-note.md examples/grounded-claims.json --require-sources --format json`.
- Repo readiness: `repo-flightcheck --check-remote --strict --threshold 80` scored `100/100`.
- Public source checks: raw GitHub URLs for README, AGENTS.md, .gitignore, CLI source, tests, CI workflow, and grounded/ungrounded examples returned `200`.
- CI: GitHub Actions run `26857728442` completed successfully.

## Reusable Lesson

Do not let a confident agent note become public proof unless its claims point to sources, commands, files, or links a reviewer can inspect. Source grounding is a separate gate from schema validity, chain consistency, and final-answer polish.
