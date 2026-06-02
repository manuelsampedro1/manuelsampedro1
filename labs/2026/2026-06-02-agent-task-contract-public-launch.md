# 2026-06-02 - Agent Task Contract Public Launch

## Context

`agent-task-contract` was the missing pre-run project in the agent reliability stack: before checking repo readiness, generating review packets, or recording run ledgers, the task brief itself needs to be specific enough to execute.

The local repo was already prepared, but publication was blocked until the empty GitHub repository could be created.

## Useful Artifact

`agent-task-contract` is now public as a dependency-free Python CLI that validates Markdown task briefs for:

- objective,
- acceptance criteria,
- context,
- constraints,
- expected changes,
- verification,
- risks,
- out-of-scope boundaries.

It supports human-readable output and JSON output for automation.

## Source Linkage

- Public repo: <https://github.com/manuelsampedro1/agent-task-contract>
- Commit: <https://github.com/manuelsampedro1/agent-task-contract/commit/3b78889e1b25de9b2450187f1b8ffadd737bf2fb>
- README: <https://raw.githubusercontent.com/manuelsampedro1/agent-task-contract/main/README.md>
- CLI: <https://raw.githubusercontent.com/manuelsampedro1/agent-task-contract/main/src/agent_task_contract/cli.py>
- Tests: <https://raw.githubusercontent.com/manuelsampedro1/agent-task-contract/main/tests/test_cli.py>
- Example contract: <https://raw.githubusercontent.com/manuelsampedro1/agent-task-contract/main/examples/AGENT_TASK.md>
- CI badge: <https://github.com/manuelsampedro1/agent-task-contract/actions/workflows/ci.yml/badge.svg?branch=main>

## Verification

Local checks:

```sh
make test
make lint
make build
git diff --check
PYTHONPATH=src python3 -m agent_task_contract check examples/AGENT_TASK.md
PYTHONPATH=src python3 -m agent_task_contract check examples/AGENT_TASK.md --format json
node /path/to/repo-flightcheck/bin/repo-flightcheck.js . --check-remote --strict --threshold 80
```

Results:

- `make test`: 5 tests passed.
- `make lint`: compile check passed.
- `make build`: compile check passed.
- CLI text output reported `Status: pass` and `Score: 100/100`.
- CLI JSON output reported `status: pass`, `score: 100`, and no issues.
- `repo-flightcheck --check-remote --strict --threshold 80`: `100/100`.
- Public repo, commit, README, CLI source, tests, and example raw URLs returned `200`.
- Public CI badge reports `CI - passing`.

## Takeaway

Agent reliability starts before code generation. A task-contract CLI turns vague handoffs into an executable preflight, so downstream tools can rely on a clearer objective, acceptance criteria, constraints, verification plan, and non-goals.
