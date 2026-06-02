# 2026-06-02 - Agent Diff Budget Public Launch

## Context

`agent-diff-budget` covers a reviewability failure mode: a coding-agent diff can stay in scope and pass tests while still being too broad for one honest review pass.

Before public launch, the repo needed agent instructions, Make targets, `.env` hygiene, Python 3 README commands, and CI/local command parity. Local virtualenv and egg-info artifacts were present but ignored rather than versioned.

## Useful Artifact

`agent-diff-budget` is now public as a dependency-free Python CLI that reads a unified diff and reports:

- changed file count,
- additions, deletions, and total changed lines,
- high-risk file count,
- path-level risk tags,
- budget failures,
- reviewer questions.

It returns a non-zero exit when the configured budget is exceeded, making oversized agent diffs a concrete split/escalation signal instead of a subjective review complaint.

## Source Linkage

- Public repo: <https://github.com/manuelsampedro1/agent-diff-budget>
- Commit: <https://github.com/manuelsampedro1/agent-diff-budget/commit/1ce33d9cf6ba69c838bd3f29fd219dd2568b4870>
- README: <https://raw.githubusercontent.com/manuelsampedro1/agent-diff-budget/main/README.md>
- CLI: <https://raw.githubusercontent.com/manuelsampedro1/agent-diff-budget/main/src/agent_diff_budget/cli.py>
- Tests: <https://raw.githubusercontent.com/manuelsampedro1/agent-diff-budget/main/tests/test_cli.py>
- Small example: <https://raw.githubusercontent.com/manuelsampedro1/agent-diff-budget/main/examples/small.diff>
- Large example: <https://raw.githubusercontent.com/manuelsampedro1/agent-diff-budget/main/examples/large.diff>
- CI badge: <https://github.com/manuelsampedro1/agent-diff-budget/actions/workflows/ci.yml/badge.svg?branch=main>
- Recipe: [`../../recipes/agent-diff-budget.md`](../../recipes/agent-diff-budget.md)

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
- `make lint`: Python compile check passed.
- `make build`: compileall check passed.
- `make smoke`: small and large diff examples rendered successfully, with the large example exiting non-zero as expected.
- `repo-flightcheck --check-remote --strict --threshold 80`: `100/100`.
- Public repo, commit, README, CLI source, tests, small example, and large example raw URLs returned `200`.
- Public CI badge reports `CI - passing`.

## Takeaway

Review quality depends on diff size as well as correctness. `agent-diff-budget` gives coding-agent workflows an explicit size and risk budget before proof packets, merge readiness, or closeout claims make an oversized diff sound safer than it is.
