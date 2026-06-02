# 2026-06-02 - Agent Review Map Public Launch

## Context

`agent-review-map` covers a handoff failure mode: a coding-agent diff can span auth, workflows, tests, docs, and app code while still arriving as one flat patch with one confident closeout.

Before public launch, the repo needed agent instructions, Make targets, `.env` hygiene, Python 3 README commands, CI/local command parity, and one more CLI output test. Local virtualenv and egg-info artifacts were present but ignored rather than versioned.

## Useful Artifact

`agent-review-map` is now public as a dependency-free Python CLI that reads a unified diff and reports:

- changed files,
- additions, deletions, and total changed lines,
- review lanes,
- suggested reviewer owner per lane,
- handoff order,
- lane-specific reviewer questions.

It gives reviewers a concrete routing artifact before proof packets, merge readiness checks, or final closeout claims compress several specialties into one generic review.

## Source Linkage

- Public repo: <https://github.com/manuelsampedro1/agent-review-map>
- Commit: <https://github.com/manuelsampedro1/agent-review-map/commit/9e392da69b5a96c80777ba6292c7bbd205e01ea5>
- README: <https://raw.githubusercontent.com/manuelsampedro1/agent-review-map/main/README.md>
- CLI: <https://raw.githubusercontent.com/manuelsampedro1/agent-review-map/main/src/agent_review_map/cli.py>
- Tests: <https://raw.githubusercontent.com/manuelsampedro1/agent-review-map/main/tests/test_cli.py>
- Mixed diff example: <https://raw.githubusercontent.com/manuelsampedro1/agent-review-map/main/examples/mixed.diff>
- CI badge: <https://github.com/manuelsampedro1/agent-review-map/actions/workflows/ci.yml/badge.svg?branch=main>
- Recipe: [`../../recipes/agent-review-map.md`](../../recipes/agent-review-map.md)

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
- `make smoke`: mixed diff example rendered successfully as JSON and Markdown.
- `repo-flightcheck --check-remote --strict --threshold 80`: `100/100`.
- Public repo, commit, README, CLI source, tests, and mixed diff raw URLs returned `200`.
- Public CI badge reports `CI - passing`.

## Takeaway

Review quality depends on ownership as well as test status. `agent-review-map` makes mixed agent diffs easier to route by naming the review lanes, owners, files, line counts, questions, and handoff order before the final proof artifact is accepted.
