# 2026-06-02 - Agent Publish Queue Public Launch

## Context

`agent-publish-queue` is the public-surface sync layer for the agent workflow stack. A profile can look polished while local proof repos, GitHub remotes, TODO blockers, and README claims drift apart; the queue makes that state inspectable before promotion.

The local repo needed agent instructions, Make targets, explicit `.env` hygiene, README command alignment, CI/local command parity, and an empty public GitHub repo before it could be pushed as real proof.

## Useful Artifact

`agent-publish-queue` is now public as a dependency-free Python CLI that audits local proof repos and reports:

- local path,
- branch,
- HEAD,
- dirty worktree state,
- origin remote,
- public GitHub URL,
- optional public HTTP status,
- blockers,
- next action.

It does not create repositories, push code, store credentials, or pretend that a `404` is public proof. That constraint keeps profile promotion honest.

## Source Linkage

- Public repo: <https://github.com/manuelsampedro1/agent-publish-queue>
- Commit: <https://github.com/manuelsampedro1/agent-publish-queue/commit/6a221f7d6f9cef88f8bfce1261a1b591392d41a6>
- README: <https://raw.githubusercontent.com/manuelsampedro1/agent-publish-queue/main/README.md>
- CLI: <https://raw.githubusercontent.com/manuelsampedro1/agent-publish-queue/main/src/agent_publish_queue/cli.py>
- Tests: <https://raw.githubusercontent.com/manuelsampedro1/agent-publish-queue/main/tests/test_cli.py>
- Sample report: <https://raw.githubusercontent.com/manuelsampedro1/agent-publish-queue/main/examples/sample-report.md>
- CI badge: <https://github.com/manuelsampedro1/agent-publish-queue/actions/workflows/ci.yml/badge.svg?branch=main>
- Recipe: [`../../recipes/publish-queue-for-local-agent-repos.md`](../../recipes/publish-queue-for-local-agent-repos.md)

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
- `make smoke`: rendered Markdown and JSON queue outputs.
- `repo-flightcheck --check-remote --strict --threshold 80`: `100/100`.
- Public repo, commit, README, CLI source, tests, and sample report raw URLs returned `200`.
- Public CI badge reports `CI - passing`.

## Takeaway

Profile promotion should be a queue with blockers, not a memory exercise. `agent-publish-queue` makes the remaining local-to-public backlog visible before README claims change.
