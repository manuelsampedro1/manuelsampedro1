# 2026-06-02 - Repo Flightcheck Agent Task Contracts

## Context

`agent-task-contract` is ready locally, but the public repo cannot be pushed until `manuelsampedro1/agent-task-contract` exists on GitHub. To make the same idea visible in public proof now, I added optional task-contract validation to `repo-flightcheck`.

The goal is not to force every repo to carry a task file. The useful behavior is narrower: if a repo declares `AGENT_TASK.md` or `TASK_CONTRACT.md`, `repo-flightcheck` should check whether the file is concrete enough before an agent run starts.

## Change

- Added a `Task contract` check to `repo-flightcheck`.
- Detects `AGENT_TASK.md` and `TASK_CONTRACT.md`.
- Validates required sections: objective, acceptance criteria, context, constraints, expected changes, verification, risks, and out-of-scope boundaries.
- Flags placeholder language such as `TBD`, `todo`, `placeholder`, and template instructions.
- Requires concrete bullets for acceptance criteria, constraints, expected changes, risks, and out-of-scope work.
- Keeps missing task contracts as a pass, because task-specific contracts are optional for general repo readiness.
- Added tests for complete and incomplete task contracts.

Public commit: `48c22da1aa9d feat: validate agent task contracts`.

## Verification

Local checks:

```sh
node --test
node scripts/lint.js
node scripts/build.js
git diff --check
node bin/repo-flightcheck.js . --check-remote --strict --threshold 80
node bin/repo-flightcheck.js /Users/manuelsampedro/Documents/Codex/2026-05-21/agent-task-contract --check-remote --strict --threshold 80
```

Results:

- `node --test`: 28 tests passed.
- `node scripts/lint.js`: passed.
- `node scripts/build.js`: passed.
- `git diff --check`: passed.
- Self-scan after push: `98/100`, with `Task contract` pass, clean working tree, and local `HEAD` published on `origin/main`; only local warning was missing `npm` in this Codex environment.
- `agent-task-contract` scan: `99/100`, with its remote still correctly flagged as not found or inaccessible.
- Commit URL returned HTTP `200`.
- Raw `src/scan.js` and `test/scan.test.js` URLs returned HTTP `200`.
- GitHub Actions run `26807151587` completed with conclusion `success`.

## Source Linkage

- Repo: <https://github.com/manuelsampedro1/repo-flightcheck>
- Commit: <https://github.com/manuelsampedro1/repo-flightcheck/commit/48c22da1aa9d65477ac345729c0f28beece7e3a1>
- CI run: <https://github.com/manuelsampedro1/repo-flightcheck/actions/runs/26807151587>
- Scanner: <https://raw.githubusercontent.com/manuelsampedro1/repo-flightcheck/main/src/scan.js>
- Tests: <https://raw.githubusercontent.com/manuelsampedro1/repo-flightcheck/main/test/scan.test.js>
- README: <https://raw.githubusercontent.com/manuelsampedro1/repo-flightcheck/main/README.md>

## Takeaway

Agent reliability starts before the agent edits code. A repo can now expose not only its setup and verification readiness, but also whether a declared task contract is concrete enough to run.
