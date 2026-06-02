# 2026-06-02 - Agent Worktree Guard Public Launch

Published [agent-worktree-guard](https://github.com/manuelsampedro1/agent-worktree-guard), a dependency-free Python CLI for protecting pre-existing dirty working-tree changes around coding-agent runs.

## What Changed

- Added `snapshot` to record dirty paths, file hashes, git branch, and HEAD before an agent starts.
- Added `check` to block protected-file drift and unexpected dirty paths outside an explicit allowlist.
- Added Markdown and JSON output so humans and automation can consume the same verdict.
- Added unit tests, smoke checks, editable package install support, and GitHub Actions CI.

## Verification

- Public clone from GitHub passed `make test`, `make lint`, `make build`, and `make smoke`.
- Editable install from the public clone succeeded, and `agent-worktree-guard --help` rendered.
- Remote `cli.py`, `tests/test_cli.py`, and `.github/workflows/ci.yml` matched local SHA-256 hashes after browser-authenticated publication.
- GitHub Actions run `26825761406` completed with `success`.

## Lesson

Scope gates catch where the final diff should land. Worktree guards catch whether the agent damaged user changes that were already present before the run. Both checks belong in the same reliability stack.
