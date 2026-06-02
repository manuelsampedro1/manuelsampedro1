# 2026-06-02 - Agent Closeout Check Public Launch

## Context

`agent-closeout-check` is the final-answer evidence piece of the agent workflow stack: an agent can produce a confident closeout while omitting changed files, exact verification, residual risks, or unverified work.

The local repo needed agent instructions, Make targets, explicit `.env` hygiene, README command alignment, CI/local command parity, and support for `make test` as a verification command before public launch.

## Useful Artifact

`agent-closeout-check` is now public as a dependency-free Python CLI that lints coding-agent closeout Markdown for:

- a clear summary or changes section,
- file references or changed-path evidence,
- exact verification commands or checks,
- risks, limitations, or residual notes,
- vague confidence phrases such as "should work."

It does not judge code quality. It checks whether the final answer gives a reviewer enough evidence to trust or challenge the handoff.

## Source Linkage

- Public repo: <https://github.com/manuelsampedro1/agent-closeout-check>
- Commit: <https://github.com/manuelsampedro1/agent-closeout-check/commit/cb23294cb4ec1f4dac8644d0130faab213bc27cd>
- README: <https://raw.githubusercontent.com/manuelsampedro1/agent-closeout-check/main/README.md>
- CLI: <https://raw.githubusercontent.com/manuelsampedro1/agent-closeout-check/main/src/agent_closeout_check/cli.py>
- Tests: <https://raw.githubusercontent.com/manuelsampedro1/agent-closeout-check/main/tests/test_cli.py>
- Good fixture: <https://raw.githubusercontent.com/manuelsampedro1/agent-closeout-check/main/examples/good-closeout.md>
- CI badge: <https://github.com/manuelsampedro1/agent-closeout-check/actions/workflows/ci.yml/badge.svg?branch=main>

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
- `make smoke`: rendered passing, failing, and JSON closeout checks.
- `repo-flightcheck --check-remote --strict --threshold 80`: `100/100`.
- Public repo, commit, README, CLI source, tests, and fixture raw URLs returned `200`.
- Public CI badge reports `CI - passing`.

## Takeaway

The closeout is part of the artifact, not just a message. `agent-closeout-check` makes evidence quality reviewable before the next human or agent trusts the work.
