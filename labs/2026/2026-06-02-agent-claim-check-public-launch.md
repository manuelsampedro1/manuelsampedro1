# 2026-06-02 - Agent Claim Check Public Launch

## Context

`agent-claim-check` covers a final-answer failure mode: a coding-agent closeout can have the right sections and still overclaim changed files, verification commands, or residual risk.

Before public launch, the repo needed agent instructions, Make targets, `.env` hygiene, Python 3 README commands, CI/local command parity, and a CLI test proving weak Markdown closeouts return a blocked exit code.

## Useful Artifact

`agent-claim-check` is now public as a dependency-free Python CLI that reads a closeout, unified diff, and optional command evidence, then reports:

- changed files,
- files referenced by the closeout,
- exact commands claimed by the closeout,
- command evidence passed with `--ran-command`,
- unsupported strong verification claims,
- risky-path contradictions with "no risk" language.

It makes final-answer verification stricter than section shape: a closeout can sound good and still fail when claims do not match the diff or command ledger.

## Source Linkage

- Public repo: <https://github.com/manuelsampedro1/agent-claim-check>
- Commit: <https://github.com/manuelsampedro1/agent-claim-check/commit/c9d6cded23fe3a069e38f7dfd9c030ec9668032f>
- README: <https://raw.githubusercontent.com/manuelsampedro1/agent-claim-check/main/README.md>
- CLI: <https://raw.githubusercontent.com/manuelsampedro1/agent-claim-check/main/src/agent_claim_check/cli.py>
- Tests: <https://raw.githubusercontent.com/manuelsampedro1/agent-claim-check/main/tests/test_cli.py>
- Sample diff: <https://raw.githubusercontent.com/manuelsampedro1/agent-claim-check/main/examples/sample.diff>
- Good closeout: <https://raw.githubusercontent.com/manuelsampedro1/agent-claim-check/main/examples/good-closeout.md>
- Weak closeout: <https://raw.githubusercontent.com/manuelsampedro1/agent-claim-check/main/examples/weak-closeout.md>
- CI badge: <https://github.com/manuelsampedro1/agent-claim-check/actions/workflows/ci.yml/badge.svg?branch=main>
- Recipe: [`../../recipes/agent-claim-check.md`](../../recipes/agent-claim-check.md)

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

- `make test`: 6 tests passed.
- `make lint`: Python compile check passed.
- `make build`: compileall check passed.
- `make smoke`: good closeout rendered as JSON and weak closeout returned blocked as expected.
- `repo-flightcheck --check-remote --strict --threshold 80`: `100/100`.
- Public repo, commit, README, CLI source, tests, sample diff, good closeout, and weak closeout raw URLs returned `200`.
- Public CI badge reports `CI - passing`.

## Takeaway

Closeout quality is not only formatting. `agent-claim-check` makes claims auditable by comparing final-answer language to changed files and command evidence before proof packets, PR comments, or run ledgers treat the closeout as reliable.
