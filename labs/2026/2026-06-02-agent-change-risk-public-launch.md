# 2026-06-02 - Agent Change Risk Public Launch

## Context

`agent-change-risk` is the gate-routing layer for the agent workflow stack. Scope guards, secret scans, runbook drift checks, CI failure packets, rollback packets, eval cases, verification checklists, and closeout checks are useful, but a reviewer still needs a consistent way to decide which gates apply to a mixed diff.

The local repo needed agent instructions, Make targets, explicit `.env` hygiene, README command alignment, CI/local command parity, and a public GitHub remote before it could become profile proof.

## Useful Artifact

`agent-change-risk` is now public as a dependency-free Python CLI that classifies coding-agent diffs into:

- changed files,
- risk tags,
- a low, medium, or high risk level,
- required proof gates,
- reviewer questions.

It does not replace review. It routes review: low-risk changes stay lightweight, while CI, database, release, security, config, documentation, or test-heavy changes get the matching evidence gates before merge.

## Source Linkage

- Public repo: <https://github.com/manuelsampedro1/agent-change-risk>
- Commit: <https://github.com/manuelsampedro1/agent-change-risk/commit/49dc92d624906a9523af60188b3a30936a79037e>
- README: <https://raw.githubusercontent.com/manuelsampedro1/agent-change-risk/main/README.md>
- CLI: <https://raw.githubusercontent.com/manuelsampedro1/agent-change-risk/main/src/agent_change_risk/cli.py>
- Tests: <https://raw.githubusercontent.com/manuelsampedro1/agent-change-risk/main/tests/test_cli.py>
- Sample diff: <https://raw.githubusercontent.com/manuelsampedro1/agent-change-risk/main/examples/sample.diff>
- CI badge: <https://github.com/manuelsampedro1/agent-change-risk/actions/workflows/ci.yml/badge.svg?branch=main>
- Recipe: [`../../recipes/change-risk-matrix-for-agent-diffs.md`](../../recipes/change-risk-matrix-for-agent-diffs.md)

## Verification

Local checks:

```sh
make test
make lint
make build
make smoke
git diff --check
node /path/to/repo-flightcheck/bin/repo-flightcheck.js . --check-remote --strict --threshold 80
```

Results:

- `make test`: 4 tests passed.
- `make lint`: compile check passed.
- `make build`: compile check passed.
- `make smoke`: rendered Markdown and JSON risk packets from the sample diff.
- `repo-flightcheck --check-remote --strict --threshold 80`: `100/100`.
- Public repo, commit, README, CLI source, tests, and sample raw URLs returned `200`.
- Public CI badge reports `CI - passing`.

## Takeaway

The reliability stack needs routing, not ritual. `agent-change-risk` makes the next proof gates explicit from the diff before a reviewer accepts agent-generated work as safe.
