# 2026-06-02 - Agent Scope Guard Public Launch

## Context

`agent-scope-guard` is the boundary-control piece of the agent workflow stack: tests can pass while an agent edits files outside the requested task scope.

The local repo needed agent instructions, Make targets, explicit `.env` hygiene, aligned README commands, CI/local command parity, and generated metadata kept out of version control before public launch.

## Useful Artifact

`agent-scope-guard` is now public as a dependency-free Python CLI that checks changed paths from a unified diff, stdin, or newline-delimited path list against explicit exact-path and glob allowlists.

It emits text or JSON and exits non-zero when unexpected paths appear, making scope drift usable as a CI or publish gate.

## Source Linkage

- Public repo: <https://github.com/manuelsampedro1/agent-scope-guard>
- Commit: <https://github.com/manuelsampedro1/agent-scope-guard/commit/c472eedeeafd1d4baf0128fdbcd54bc123891436>
- README: <https://raw.githubusercontent.com/manuelsampedro1/agent-scope-guard/main/README.md>
- CLI: <https://raw.githubusercontent.com/manuelsampedro1/agent-scope-guard/main/src/agent_scope_guard/cli.py>
- Tests: <https://raw.githubusercontent.com/manuelsampedro1/agent-scope-guard/main/tests/test_cli.py>
- Example diff: <https://raw.githubusercontent.com/manuelsampedro1/agent-scope-guard/main/examples/sample.diff>
- CI badge: <https://github.com/manuelsampedro1/agent-scope-guard/actions/workflows/ci.yml/badge.svg?branch=main>

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
- `make smoke`: rendered both failing and passing scope checks.
- `repo-flightcheck --check-remote --strict --threshold 80`: `100/100`.
- Public repo, commit, README, CLI source, tests, and example raw URLs returned `200`.
- Public CI badge reports `CI - passing`.

## Takeaway

Task contracts are stronger when the allowed changed paths are executable. `agent-scope-guard` makes scope drift visible before a broad agent diff becomes a review burden.
