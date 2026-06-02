# 2026-06-02 - Repo Flightcheck Node CLI Entrypoints

## Context

Several agent reliability tools in this profile are small Node CLIs. A repo can look ready because it has `package.json`, tests, CI, and docs, while its declared `bin` entrypoint still fails at the first real invocation.

`repo-flightcheck` already checked metadata, scripts, CI parity, documented commands, working tree cleanliness, and agent instructions. It did not verify that a `package.json` `bin` target actually pointed to an executable Node script.

## Change

- Added a `Node CLI entrypoint` check.
- Parsed string and object forms of `package.json` `bin`.
- Warned when a declared CLI target is missing, lacks a Node shebang, or is not executable on POSIX systems.
- Kept non-CLI packages passing with an explicit "no bin entrypoints declared" message.
- Made `bin/repo-flightcheck.js` executable so the repo satisfies its own check.
- Added passing and warning tests for CLI entrypoints.
- Updated the README checks list, sample output, and limits.

Public commit: `cb13c46c058e feat: validate node cli entrypoints`.

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

- `node --test`: 17 tests passed.
- `node scripts/lint.js`: passed.
- `node scripts/build.js`: passed.
- `repo-flightcheck --strict --threshold 80`: `100/100` after commit.
- GitHub Actions run `26800753403` completed with conclusion `success`.

## Source Linkage

- Repo: <https://github.com/manuelsampedro1/repo-flightcheck>
- Commit: <https://github.com/manuelsampedro1/repo-flightcheck/commit/cb13c46c058e63c6345e0417acba1b2fa1d7bb86>
- CI run: <https://github.com/manuelsampedro1/repo-flightcheck/actions/runs/26800753403>
- Scanner: <https://raw.githubusercontent.com/manuelsampedro1/repo-flightcheck/main/src/scan.js>
- Tests: <https://raw.githubusercontent.com/manuelsampedro1/repo-flightcheck/main/test/scan.test.js>

## Takeaway

Repo readiness for CLI tools should include whether the declared command can actually launch. For agent-facing utilities, a broken `bin` target is not a packaging detail; it is an onboarding failure.
