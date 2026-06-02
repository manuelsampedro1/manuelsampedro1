# 2026-06-02 - Agent Diff Splitter Public Launch

## Context

`agent-diff-splitter` covers the next step after a diff-budget blocker: telling a human or follow-up agent exactly how to cut a broad patch into reviewable slices.

Before public launch, the repo needed agent instructions, Make targets, `.env` hygiene, Python 3 README commands, CI/local command parity, removal of a command-drift false positive in README wording, and a Markdown CLI output test.

## Useful Artifact

`agent-diff-splitter` is now public as a dependency-free Python CLI that reads a unified diff and reports:

- changed files,
- additions, deletions, and total changed lines,
- review lanes,
- proposed split order,
- files per split,
- changed-line totals per split,
- rationale and reviewer question per split.

It makes "split the PR" actionable after `agent-diff-budget` blocks a broad agent diff.

## Source Linkage

- Public repo: <https://github.com/manuelsampedro1/agent-diff-splitter>
- Commit: <https://github.com/manuelsampedro1/agent-diff-splitter/commit/6554cc05857044bfb63b66a6d7e8719988c86b12>
- README: <https://raw.githubusercontent.com/manuelsampedro1/agent-diff-splitter/main/README.md>
- CLI: <https://raw.githubusercontent.com/manuelsampedro1/agent-diff-splitter/main/src/agent_diff_splitter/cli.py>
- Tests: <https://raw.githubusercontent.com/manuelsampedro1/agent-diff-splitter/main/tests/test_cli.py>
- Mixed diff example: <https://raw.githubusercontent.com/manuelsampedro1/agent-diff-splitter/main/examples/mixed.diff>
- CI badge: <https://github.com/manuelsampedro1/agent-diff-splitter/actions/workflows/ci.yml/badge.svg?branch=main>
- Recipe: [`../../recipes/agent-diff-splitter.md`](../../recipes/agent-diff-splitter.md)

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

Blocking broad diffs is only half the workflow. `agent-diff-splitter` turns the blocker into ordered slices so the next agent run can use concrete allowed files instead of a vague request to make the work smaller.
