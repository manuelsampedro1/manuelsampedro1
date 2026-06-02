# 2026-06-02 - Repo Flightcheck Agent Readiness Contract

## Context

`repo-flightcheck` already produced a full readiness report, but downstream tools had to parse every check to answer a simpler handoff question: can an agent start, or are there blockers to fix first?

That matters for the rest of the public stack. Review packets, ledgers, and verification gates need a compact contract with commands, blockers, and recommendations, not only a human-readable audit.

## Change

- Added `buildAgentContract(report, threshold)` to turn a full scan into a compact readiness contract.
- Added `agentContract` to the full JSON report for importers that already consume `scanRepo()`.
- Added `--contract` to the CLI for contract-only JSON output.
- Split unresolved checks into `requiredBeforeAgent` for critical/high issues and `recommendedBeforeAgent` for lower-severity gaps.
- Made contract readiness depend on score threshold, critical failures, and unresolved required checks.
- Added tests for ready repos, blocker separation, and CLI contract output.
- Updated README usage, practical use cases, and limits.

Public commit: `8b1253b593c6 feat: emit agent readiness contracts`.

## Verification

Local checks:

```sh
node --test
node scripts/lint.js
node scripts/build.js
node bin/repo-flightcheck.js . --strict --threshold 80
node bin/repo-flightcheck.js . --contract --threshold 80
git diff --check
```

Results:

- `node --test`: 15 tests passed.
- `node scripts/lint.js`: passed.
- `node scripts/build.js`: passed across 6 JavaScript files.
- Self-audit after commit: `repo-flightcheck` scored `100/100`.
- Contract smoke after commit: `ready: true`, `score: 100`, no required or recommended unresolved checks.
- `git diff --check`: passed.
- GitHub Actions run `26798783115` completed with conclusion `success`.

## Source Linkage

- Repo: <https://github.com/manuelsampedro1/repo-flightcheck>
- Commit: <https://github.com/manuelsampedro1/repo-flightcheck/commit/8b1253b593c66b44b775512a237756ca04b79697>
- CI run: <https://github.com/manuelsampedro1/repo-flightcheck/actions/runs/26798783115>
- CLI: <https://raw.githubusercontent.com/manuelsampedro1/repo-flightcheck/main/src/cli.js>
- Scanner: <https://raw.githubusercontent.com/manuelsampedro1/repo-flightcheck/main/src/scan.js>
- Tests: <https://raw.githubusercontent.com/manuelsampedro1/repo-flightcheck/main/test/scan.test.js>

## Takeaway

Agent readiness should be machine-readable. A compact contract lets the next tool fail fast on unresolved repo blockers instead of trusting prose or forcing every integration to re-interpret the full scan.
