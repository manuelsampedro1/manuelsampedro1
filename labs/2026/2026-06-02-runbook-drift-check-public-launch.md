# 2026-06-02 - Runbook Drift Check Public Launch

## Context

`runbook-drift-check` is the operational-docs piece of the agent workflow stack: README files, AGENTS.md, and runbooks can look current while pointing to renamed files, deleted scripts, or stale commands.

The local repo needed agent instructions, Make targets, explicit `.env` hygiene, aligned README commands, and CI/local command parity before public launch.

## Useful Artifact

`runbook-drift-check` is now public as a dependency-free Python CLI that checks operational Markdown for:

- missing local Markdown links,
- backticked local paths that no longer exist,
- shell code blocks that call missing local scripts,
- optional `bash -n` syntax checks for referenced shell scripts.

It does not execute arbitrary runbook commands. It checks paths and script syntax so reviewers can fix drift before agents trust stale instructions.

## Source Linkage

- Public repo: <https://github.com/manuelsampedro1/runbook-drift-check>
- Commit: <https://github.com/manuelsampedro1/runbook-drift-check/commit/7c13df4464b0cea6bada5e7369b658bd562751f1>
- README: <https://raw.githubusercontent.com/manuelsampedro1/runbook-drift-check/main/README.md>
- CLI: <https://raw.githubusercontent.com/manuelsampedro1/runbook-drift-check/main/src/runbook_drift_check/cli.py>
- Tests: <https://raw.githubusercontent.com/manuelsampedro1/runbook-drift-check/main/tests/test_cli.py>
- Example runbook: <https://raw.githubusercontent.com/manuelsampedro1/runbook-drift-check/main/examples/RUNBOOK.md>
- CI badge: <https://github.com/manuelsampedro1/runbook-drift-check/actions/workflows/ci.yml/badge.svg?branch=main>

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
- `make smoke`: checked the example runbook and rendered JSON output.
- `repo-flightcheck --check-remote --strict --threshold 80`: `100/100`.
- Public repo, commit, README, CLI source, tests, and example raw URLs returned `200`.
- Public CI badge reports `CI - passing`.

## Takeaway

Agent instructions are only useful if their operational docs still point at real files and scripts. `runbook-drift-check` makes stale runbook references visible before they become bad agent context.
