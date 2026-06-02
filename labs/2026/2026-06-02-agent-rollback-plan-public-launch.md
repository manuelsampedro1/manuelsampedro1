# 2026-06-02 - Agent Rollback Plan Public Launch

## Context

`agent-rollback-plan` is the operational-risk piece of the agent workflow stack: passing tests are not enough when a diff touches deploy scripts, CI workflows, migrations, configuration, or release behavior.

The local repo needed agent instructions, Make targets, explicit `.env` hygiene, README command alignment, and CI/local command parity before public launch.

## Useful Artifact

`agent-rollback-plan` is now public as a dependency-free Python CLI that turns unified diffs into Markdown or JSON rollback packets with:

- changed files,
- risk tags,
- rollback steps,
- post-rollback checks,
- reviewer questions.

It does not execute rollback commands. It writes a plan reviewers can challenge before a risky change ships.

## Source Linkage

- Public repo: <https://github.com/manuelsampedro1/agent-rollback-plan>
- Commit: <https://github.com/manuelsampedro1/agent-rollback-plan/commit/c1905c224e4813ddf01922dab50aa157529c8a25>
- README: <https://raw.githubusercontent.com/manuelsampedro1/agent-rollback-plan/main/README.md>
- CLI: <https://raw.githubusercontent.com/manuelsampedro1/agent-rollback-plan/main/src/agent_rollback_plan/cli.py>
- Tests: <https://raw.githubusercontent.com/manuelsampedro1/agent-rollback-plan/main/tests/test_cli.py>
- Example diff: <https://raw.githubusercontent.com/manuelsampedro1/agent-rollback-plan/main/examples/sample.diff>
- CI badge: <https://github.com/manuelsampedro1/agent-rollback-plan/actions/workflows/ci.yml/badge.svg?branch=main>

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
- `make smoke`: rendered the sample diff as JSON.
- `repo-flightcheck --check-remote --strict --threshold 80`: `100/100`.
- Public repo, commit, README, CLI source, tests, and example raw URLs returned `200`.
- Public CI badge reports `CI - passing`.

## Takeaway

Serious agent workflows need an undo answer before risky changes merge. `agent-rollback-plan` makes rollback review part of the same evidence loop as tests and CI.
