# 2026-06-02 - Repo Flightcheck Remote Readiness

## Context

Several local proof repos had `origin` remotes configured for GitHub names that do not exist yet. That creates a bad profile failure mode: a project can look publish-ready locally while `git ls-remote` still returns `Repository not found`.

`repo-flightcheck` already checked local readiness: README, AGENTS.md, commands, CI, tool availability, working tree, CLI entrypoints, and secret hygiene. The missing check was publish readiness.

## Change

- Added a `Git remote` check to report whether `origin` is configured.
- Added `--check-remote` to validate that `origin` is reachable before claiming public proof.
- Kept remote reachability opt-in because it can need network access or GitHub authentication.
- Sanitized HTTPS credentials from remote evidence and remote-check errors.
- Added tests for configured origins, missing origins, reachable remotes, and unreachable remotes.
- Updated README usage, example output, and limitations.

Public commit: `af87c6cd1952 feat: check publish remote readiness`.

## Verification

Local checks:

```sh
node --test
node scripts/build.js
node scripts/lint.js
git diff --check
node bin/repo-flightcheck.js /Users/manuelsampedro/Documents/Codex/2026-05-21/agent-task-contract --check-remote
node bin/repo-flightcheck.js . --check-remote --strict --threshold 80
```

Results:

- `node --test`: 24 tests passed.
- `node scripts/build.js`: passed.
- `node scripts/lint.js`: passed.
- `git diff --check`: passed.
- Pending local repo smoke flagged `Git remote` with `Origin remote is configured but could not be reached.`
- Self-scan with `--check-remote --strict --threshold 80`: `98/100`, origin remote reachable; only warning was missing local `npm` in this Codex environment.
- GitHub Actions run `26804858130` completed with conclusion `success`.

## Source Linkage

- Repo: <https://github.com/manuelsampedro1/repo-flightcheck>
- Commit: <https://github.com/manuelsampedro1/repo-flightcheck/commit/af87c6cd1952ebab1c4617656417cd343e5f450e>
- CI run: <https://github.com/manuelsampedro1/repo-flightcheck/actions/runs/26804858130>
- Scanner: <https://raw.githubusercontent.com/manuelsampedro1/repo-flightcheck/main/src/scan.js>
- Tests: <https://raw.githubusercontent.com/manuelsampedro1/repo-flightcheck/main/test/scan.test.js>

## Takeaway

Public-proof tooling should separate local readiness from publish readiness. A repo can pass tests, build, lint, and CI locally, but it should not be promoted to a profile until the configured remote actually exists and is reachable.
