# 2026-06-02 - Repo Flightcheck GitHub Action Detection

## Context

The profile's Agent Safety Layer includes `deploy-gate`, a composite GitHub Action for human authorization around sensitive agent-driven deploys. Auditing a local clone of that repo exposed a gap in `repo-flightcheck`: dependency-light action repos without `package.json`, Python metadata, Rust, or Swift config were reported as `generic`.

That made the readiness report less precise for exactly the kind of repo serious agent systems need: GitHub Actions that enforce safety gates.

## Change

- Added stack detection for dependency-light GitHub Action repos that expose `action.yml` or `action.yaml`.
- Kept language-specific detection first, so JavaScript actions with `package.json` still report as Node.
- Added a regression test with `action.yml`, `Makefile` verification targets, CI commands, examples, and agent guidance.
- Updated README checks and limits to describe GitHub Action repo detection.

Public commit: `c697fa3e8c87 feat: detect github action repos`.

## Verification

Local checks:

```sh
node --test
node scripts/lint.js
node scripts/build.js
node bin/repo-flightcheck.js . --strict --threshold 80
node bin/repo-flightcheck.js /Users/manuelsampedro/Documents/Codex/2026-05-24/flagships/deploy-gate --strict --threshold 80
git diff --check
```

Results:

- `node --test`: 12 tests passed.
- `node scripts/lint.js`: passed.
- `node scripts/build.js`: passed across 6 JavaScript files.
- Self-audit: `repo-flightcheck` stayed at `100/100` after commit.
- Local `deploy-gate` smoke: `Stack: github-action`, score `100/100`.
- Public commit page returned `200`.
- Raw `src/scan.js` returned `200`.
- GitHub Actions run `26796926606` completed with conclusion `success`.

## Source Linkage

- Repo: <https://github.com/manuelsampedro1/repo-flightcheck>
- Commit: <https://github.com/manuelsampedro1/repo-flightcheck/commit/c697fa3e8c87ca9322f8e3b1040795f3bd81c777>
- CI run: <https://github.com/manuelsampedro1/repo-flightcheck/actions/runs/26796926606>
- Scanner: <https://raw.githubusercontent.com/manuelsampedro1/repo-flightcheck/main/src/scan.js>
- Tests: <https://raw.githubusercontent.com/manuelsampedro1/repo-flightcheck/main/test/scan.test.js>

## Takeaway

Agent-safety repositories are often GitHub Actions, not app repos. A readiness tool should identify action metadata directly so reviewers can see when a safety gate repo has explicit local checks, CI parity, examples, and agent instructions.
