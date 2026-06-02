# 2026-06-02 - Agent Decision Guard Public Launch

## Context

`agent-decision-guard` covers a gap in the agent reliability stack: a diff can pass tests and stay in scope while still changing CI, automation, configuration, product scope, security posture, or future agent behavior without a durable rationale.

Before public launch, the local repo also had a contract mismatch. The README said an explicit no-follow-up decision could replace a `TODO.md` entry, but the CLI did not recognize that waiver. The launch hardening fixed that behavior before promotion.

## Useful Artifact

`agent-decision-guard` is now public as a dependency-free Python CLI that reads a unified diff and reports:

- changed files,
- decision-worthy risk tags,
- whether `DECISIONS.md` changed,
- whether `TODO.md` changed,
- whether a `DECISIONS.md` no-follow-up waiver was added,
- missing documentation blockers,
- reviewer questions.

It returns a non-zero exit for blocked diffs, so it can run before commits, in CI, or as part of a proof-packet flow.

## Source Linkage

- Public repo: <https://github.com/manuelsampedro1/agent-decision-guard>
- Commit: <https://github.com/manuelsampedro1/agent-decision-guard/commit/c7ac1bf2b9bb297a3c53bd5a5ba93aacd11ab2d4>
- README: <https://raw.githubusercontent.com/manuelsampedro1/agent-decision-guard/main/README.md>
- CLI: <https://raw.githubusercontent.com/manuelsampedro1/agent-decision-guard/main/src/agent_decision_guard/cli.py>
- Tests: <https://raw.githubusercontent.com/manuelsampedro1/agent-decision-guard/main/tests/test_cli.py>
- Blocking example: <https://raw.githubusercontent.com/manuelsampedro1/agent-decision-guard/main/examples/risky.diff>
- Waiver example: <https://raw.githubusercontent.com/manuelsampedro1/agent-decision-guard/main/examples/risky-with-waiver.diff>
- CI badge: <https://github.com/manuelsampedro1/agent-decision-guard/actions/workflows/ci.yml/badge.svg?branch=main>
- Recipe: [`../../recipes/agent-decision-guard.md`](../../recipes/agent-decision-guard.md)

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
- `make smoke`: blocking, documented, and waiver examples rendered successfully.
- `repo-flightcheck --check-remote --strict --threshold 80`: `100/100`.
- Public repo, commit, README, CLI source, tests, blocking example, and waiver example raw URLs returned `200`.
- Public CI badge reports `CI - passing`.

## Takeaway

Agent systems need durable intent, not only passing tests. `agent-decision-guard` makes missing decision and follow-up documentation a concrete gate while still allowing explicit no-follow-up decisions when the rationale is written down.
