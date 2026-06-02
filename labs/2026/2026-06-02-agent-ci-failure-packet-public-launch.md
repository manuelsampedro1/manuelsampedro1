# 2026-06-02 - Agent CI Failure Packet Public Launch

## Context

`agent-ci-failure-packet` is the retry-context piece of the agent workflow stack: when CI fails after an agent change, the next run should receive a compact packet with the failing command, actionable error lines, referenced files, and suggested checks instead of a raw log dump.

The local repo needed agent instructions, Make targets, explicit `.env` hygiene, aligned README commands, CI/local command parity, and a sample log that points to `make test`.

## Useful Artifact

`agent-ci-failure-packet` is now public as a dependency-free Python CLI that turns CI logs into Markdown or JSON packets with:

- failing commands,
- error signals,
- referenced files,
- test summaries,
- suggested checks,
- a scoped prompt for the next agent run.

## Source Linkage

- Public repo: <https://github.com/manuelsampedro1/agent-ci-failure-packet>
- Commit: <https://github.com/manuelsampedro1/agent-ci-failure-packet/commit/fc21a18f088e34734239ba69b47789d5bdb5d1da>
- README: <https://raw.githubusercontent.com/manuelsampedro1/agent-ci-failure-packet/main/README.md>
- CLI: <https://raw.githubusercontent.com/manuelsampedro1/agent-ci-failure-packet/main/src/agent_ci_failure_packet/cli.py>
- Tests: <https://raw.githubusercontent.com/manuelsampedro1/agent-ci-failure-packet/main/tests/test_cli.py>
- Example log: <https://raw.githubusercontent.com/manuelsampedro1/agent-ci-failure-packet/main/examples/ci-failure.log>
- CI badge: <https://github.com/manuelsampedro1/agent-ci-failure-packet/actions/workflows/ci.yml/badge.svg?branch=main>

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

- `make test`: 3 tests passed.
- `make lint`: compile check passed.
- `make build`: compile check passed.
- `make smoke`: rendered the sample CI log as JSON.
- `repo-flightcheck --check-remote --strict --threshold 80`: `100/100`.
- Public repo, commit, README, CLI source, tests, and example raw URLs returned `200`.
- Public CI badge reports `CI - passing`.

## Takeaway

The next agent run should not start from a noisy CI archive. A focused failure packet keeps the retry scoped to the actual failing command and evidence.
