# 2026-06-02 - Agent Eval Runner Public Launch

## Context

`agent-eval-runner` is the regression scoring layer for the agent workflow stack. `diff-to-eval` can turn a real diff into a saved case, but the workflow also needs a transparent way to check whether later proof packets, closeouts, or review notes still cover the expected files, checks, risks, and outcome.

The local repo needed agent instructions, Make targets, explicit `.env` hygiene, README command alignment, CI/local command parity, and removal of generated package metadata before it could stand as public proof.

## Useful Artifact

`agent-eval-runner` is now public as a dependency-free Python CLI that scores a candidate artifact against saved `diff-to-eval` JSON cases for:

- changed files mentioned,
- suggested checks covered,
- risk tags represented,
- expected outcome coverage,
- average score,
- pass/fail using a threshold.

It does not call a model and does not grade writing quality. The score is deliberately narrow so a reviewer can inspect and challenge it.

## Source Linkage

- Public repo: <https://github.com/manuelsampedro1/agent-eval-runner>
- Commit: <https://github.com/manuelsampedro1/agent-eval-runner/commit/8c7960e28d8e964db05d16e249369af7d507dc52>
- README: <https://raw.githubusercontent.com/manuelsampedro1/agent-eval-runner/main/README.md>
- CLI: <https://raw.githubusercontent.com/manuelsampedro1/agent-eval-runner/main/src/agent_eval_runner/cli.py>
- Tests: <https://raw.githubusercontent.com/manuelsampedro1/agent-eval-runner/main/tests/test_cli.py>
- Example case: <https://raw.githubusercontent.com/manuelsampedro1/agent-eval-runner/main/examples/cases/publish-guard.json>
- Example candidate: <https://raw.githubusercontent.com/manuelsampedro1/agent-eval-runner/main/examples/candidate.md>
- CI badge: <https://github.com/manuelsampedro1/agent-eval-runner/actions/workflows/ci.yml/badge.svg?branch=main>
- Recipe: [`../../recipes/agent-eval-runner.md`](../../recipes/agent-eval-runner.md)

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

- `make test`: 5 tests passed.
- `make lint`: compile check passed.
- `make build`: compile check passed.
- `make smoke`: rendered Markdown and JSON eval outputs; the example case scored `100/100`.
- `repo-flightcheck --check-remote --strict --threshold 80`: `100/100`.
- Public repo, commit, README, CLI source, tests, example case, and example candidate raw URLs returned `200`.
- Public CI badge reports `CI - passing`.

## Takeaway

Agent evals should be tied to real diffs and scored against inspectable proof. `agent-eval-runner` makes the saved-case loop testable without hiding judgment inside a model call.
