# 2026-06-02 - Repo Flightcheck Python Unittest Detection

## Context

Many small agent reliability tools in this workbench are dependency-free Python CLIs. They use `unittest` because that keeps the repos easy to clone, inspect, and run in locked-down environments.

`repo-flightcheck` already detected Python projects and documented command drift, but it was still biased toward package metadata and third-party runners. A standard-library Python repo with `tests/test_*.py` could look less ready than it really was.

## Change

- Detected Python `tests/test*.py` suites as `python -m unittest discover -s tests` when no third-party runner is configured.
- Added documented-command parsing for `python -m unittest` and `python3 -m unittest` discovery commands.
- Matched `python` and `python3` variants when comparing local verification commands with GitHub Actions workflows.
- Avoided treating trailing sentence punctuation as part of the unittest start directory.
- Added tests for successful unittest detection and missing documented start directories.
- Updated the repo README to document the new Python standard-library coverage.

Public commit: `a024b678cd70 feat: detect python unittest checks`.

## Verification

Local checks:

```sh
node --test
node scripts/lint.js
node scripts/build.js
node bin/repo-flightcheck.js . --strict --threshold 80
node bin/repo-flightcheck.js . --json > /tmp/repo-flightcheck-unittest-report.json
git diff --check
```

Results:

- `node --test`: 11 tests passed.
- `node scripts/lint.js`: passed.
- `node scripts/build.js`: passed.
- Post-commit strict self-audit scored `100/100`.
- JSON self-audit showed `warnings: 0`, `failed: 0`, documented commands `pass`, and working tree `pass`.
- `git diff --check` passed before commit.
- Public commit page and raw changed files returned `200`.
- GitHub Actions run `26795493554` completed with conclusion `success`.

## Source Linkage

- Repo: <https://github.com/manuelsampedro1/repo-flightcheck>
- Commit: <https://github.com/manuelsampedro1/repo-flightcheck/commit/a024b678cd700de084555d754920e8b82b8025df>
- CI run: <https://github.com/manuelsampedro1/repo-flightcheck/actions/runs/26795493554>
- Scanner: <https://raw.githubusercontent.com/manuelsampedro1/repo-flightcheck/a024b678cd700de084555d754920e8b82b8025df/src/scan.js>
- Tests: <https://raw.githubusercontent.com/manuelsampedro1/repo-flightcheck/a024b678cd700de084555d754920e8b82b8025df/test/scan.test.js>

## Takeaway

Agent readiness checks should reward simple, standard-library verification when it is real. A dependency-free Python repo with a discoverable unittest suite is often more agent-ready than a larger repo with unclear commands.
