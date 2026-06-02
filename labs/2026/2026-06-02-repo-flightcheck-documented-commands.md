# 2026-06-02 - Repo Flightcheck Documented Commands

## Context

`repo-flightcheck` already checked whether a repo had local verification commands and whether CI ran the same command. The next drift point was in the docs themselves: README or `AGENTS.md` can tell an agent to run a command that does not exist anymore.

That matters because coding agents often follow the written runbook literally. A stale `npm run e2e`, missing Make target, or outdated stack command can waste the first run and weaken the closeout evidence.

## Change

- Added a `Documented commands` check.
- Extracted common documented commands from README and agent instruction files.
- Validated `npm test`, `npm run <script>`, built-in npm setup commands, `make <target>`, Python test commands, Rust commands, and Swift commands against repo metadata.
- Deduplicated README casing on case-insensitive filesystems.
- Reported unresolved commands with file-level evidence.
- Added tests for broken documented commands and matching package scripts / Make targets.
- Updated README checks, example output, and limits.

Public commit: `767ccb2320a2 feat: validate documented commands`.

## Verification

Local checks:

```sh
node --test
node scripts/lint.js
node scripts/build.js
node bin/repo-flightcheck.js . --strict --threshold 80
git diff --check
```

Results:

- `node --test`: 9 tests passed.
- Lint and build preflight passed.
- Strict self-scan passed with `Score: 96/100`; the only warning was the expected dirty working tree from the in-progress feature.
- Public commit page and raw changed files returned `200`.
- GitHub Actions run `26794828840` completed with conclusion `success`.

## Source Linkage

- Repo: <https://github.com/manuelsampedro1/repo-flightcheck>
- Commit: <https://github.com/manuelsampedro1/repo-flightcheck/commit/767ccb2320a21935d87fbc9bce9b4dc956d01aac>
- CI run: <https://github.com/manuelsampedro1/repo-flightcheck/actions/runs/26794828840>
- Scanner: <https://raw.githubusercontent.com/manuelsampedro1/repo-flightcheck/767ccb2320a21935d87fbc9bce9b4dc956d01aac/src/scan.js>
- Tests: <https://raw.githubusercontent.com/manuelsampedro1/repo-flightcheck/767ccb2320a21935d87fbc9bce9b4dc956d01aac/test/scan.test.js>

## Takeaway

Agent readiness should check not only whether commands exist, but whether the commands written for the agent still map to executable repo reality.
