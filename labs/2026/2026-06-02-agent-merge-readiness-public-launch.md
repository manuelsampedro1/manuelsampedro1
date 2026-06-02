# 2026-06-02 - Agent Merge Readiness Public Launch

## Context

`agent-merge-readiness` is the verdict layer for the agent workflow stack. A diff can have risk tags, passing checks, rollback notes, and a confident closeout, but reviewers still need one strict answer before merge: `ready`, `needs-review`, or `blocked`.

The local repo needed agent instructions, Make targets, explicit `.env` hygiene, README command alignment, CI/local command parity, and corrected gate semantics so non-ready verdicts exit non-zero.

## Useful Artifact

`agent-merge-readiness` is now public as a dependency-free Python CLI that reads a unified diff, explicit check results, and optional closeout Markdown, then returns:

- changed files,
- risk tags and score,
- passing checks,
- blocking findings,
- missing evidence,
- reviewer questions,
- final verdict.

It exits `0` only for `ready`. `needs-review` and `blocked` return `1`, so the tool can act as a real local or CI gate instead of a passive report.

## Source Linkage

- Public repo: <https://github.com/manuelsampedro1/agent-merge-readiness>
- Commit: <https://github.com/manuelsampedro1/agent-merge-readiness/commit/448478f95f3ff402588f07e43d824e0c940f746b>
- README: <https://raw.githubusercontent.com/manuelsampedro1/agent-merge-readiness/main/README.md>
- CLI: <https://raw.githubusercontent.com/manuelsampedro1/agent-merge-readiness/main/src/agent_merge_readiness/cli.py>
- Tests: <https://raw.githubusercontent.com/manuelsampedro1/agent-merge-readiness/main/tests/test_cli.py>
- Sample diff: <https://raw.githubusercontent.com/manuelsampedro1/agent-merge-readiness/main/examples/risky.diff>
- Closeout fixture: <https://raw.githubusercontent.com/manuelsampedro1/agent-merge-readiness/main/examples/closeout.md>
- CI badge: <https://github.com/manuelsampedro1/agent-merge-readiness/actions/workflows/ci.yml/badge.svg?branch=main>
- Recipe: [`../../recipes/merge-readiness-gate-for-agent-diffs.md`](../../recipes/merge-readiness-gate-for-agent-diffs.md)

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
- `make lint`: compile check passed.
- `make build`: compile check passed.
- `make smoke`: rendered ready Markdown and JSON readiness packets.
- `repo-flightcheck --check-remote --strict --threshold 80`: `100/100`.
- Public repo, commit, README, CLI source, tests, sample diff, and closeout fixture raw URLs returned `200`.
- Public CI badge reports `CI - passing`.

## Takeaway

Merge readiness should be a gate, not a vibe. `agent-merge-readiness` makes non-ready agent work fail automation until evidence catches up.
