# 2026-06-02 - Repo Flightcheck Structured Task Contract

## Context

`repo-flightcheck` already validated optional `AGENT_TASK.md` or `TASK_CONTRACT.md` files and surfaced issues as a normal readiness check.

Before this change, downstream tools that consumed `repo-flightcheck --json` or `repo-flightcheck --contract` had to parse check prose to know whether a task contract existed, where it came from, and which sections were missing.

## Change

- Added structured `taskContract` metadata to JSON reports.
- Added the same `taskContract` metadata to compact agent-readiness contracts.
- Exposed `present`, `source`, `status`, `requiredSections`, `missingSections`, `placeholderMarkers`, and `issues`.
- Kept the existing readiness check and score behavior unchanged.
- Updated README guidance in the public repo.

Public commit: `9a7f8d7 feat: expose task contract metadata`.

## Verification

Local checks:

```sh
node --test
node scripts/lint.js
node scripts/build.js
git diff --check
```

CLI smoke:

```sh
node bin/repo-flightcheck.js /tmp/repo-with-agent-task --json > /tmp/report.json
node bin/repo-flightcheck.js /tmp/repo-with-agent-task --contract --threshold 80 > /tmp/contract.json
```

Results:

- `node --test`: 28 tests passed.
- `node scripts/lint.js`: passed.
- `node scripts/build.js`: passed.
- `git diff --check`: passed.
- CLI smoke showed `taskContract.status` as `pass`.
- CLI smoke showed `taskContract.requiredSections` as `8/8`.
- CLI smoke confirmed `--contract` preserves the same `taskContract` object as `--json`.
- `repo-flightcheck --check-remote --strict --threshold 80`: `98/100`; only warning was local `npm` unavailable while direct `node` checks passed.
- Public commit page returned `200`.
- Raw source and test URLs returned `200`.
- GitHub Actions run `26809946918` completed with conclusion `success`.

## Source Linkage

- Repo: <https://github.com/manuelsampedro1/repo-flightcheck>
- Commit: <https://github.com/manuelsampedro1/repo-flightcheck/commit/9a7f8d792073dcb3740f47c64b16d5e4d7cb5acc>
- CI run: <https://github.com/manuelsampedro1/repo-flightcheck/actions/runs/26809946918>
- Scanner: <https://raw.githubusercontent.com/manuelsampedro1/repo-flightcheck/9a7f8d792073dcb3740f47c64b16d5e4d7cb5acc/src/scan.js>
- Tests: <https://raw.githubusercontent.com/manuelsampedro1/repo-flightcheck/9a7f8d792073dcb3740f47c64b16d5e4d7cb5acc/test/scan.test.js>

## Takeaway

Readiness contracts should carry structured task-contract state, not only prose. That lets review packets, ledgers, or future gates check whether the agent task was scoped without scraping human-readable messages.
