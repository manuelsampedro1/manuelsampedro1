# 2026-06-02 - Agent Run Ledger Readiness Import

## Context

`repo-flightcheck` can say whether a repo is ready before agent work starts. `codex-review-packet` can now embed that readiness report in review context. The remaining audit gap was after the run: the readiness artifact was still not part of the structured agent ledger.

For a serious agent workflow, pre-run repo readiness should be auditable beside decisions, changes, verification commands, blockers, and final results.

## Change

- Added `import-readiness` to `agent-run-ledger`.
- Parsed `repo-flightcheck --json` reports into normalized readiness summaries.
- Recorded a summary command event with score, pass/warn/fail counts, critical failures, source report, optional command evidence, and honest status.
- Mapped failed or critical readiness checks into `blocker` events.
- Mapped warning checks into non-blocking decision events.
- Preserved evidence file references from readiness checks when they look like repo paths.
- Added tests for clean reports, failed reports, blocker mapping, and CLI import.
- Updated README examples with the readiness import workflow.

Public commit: `d1710f505311 feat: import repo readiness reports`.

## Verification

Local checks:

```sh
node --test
node scripts/lint.js
node scripts/build.js
node /Users/manuelsampedro/Documents/Codex/2026-05-21/repo-flightcheck/bin/repo-flightcheck.js /Users/manuelsampedro/Documents/Codex/2026-05-21/repo-flightcheck --json > /tmp/readiness.json
node bin/agent-run-ledger.js import-readiness --ledger /tmp/ledger.jsonl --readiness-report /tmp/readiness.json --command "node /Users/manuelsampedro/Documents/Codex/2026-05-21/repo-flightcheck/bin/repo-flightcheck.js /Users/manuelsampedro/Documents/Codex/2026-05-21/repo-flightcheck --json"
node bin/agent-run-ledger.js doctor --ledger /tmp/ledger.jsonl --strict
git diff --check
```

Results:

- `node --test`: 21 tests passed.
- `node scripts/lint.js`: passed.
- `node scripts/build.js`: passed.
- Clean readiness smoke imported one passed event, with `0` open commands and `0` attention items under strict doctor.
- `git diff --check` passed before commit.
- Public commit page and raw changed files returned `200`.
- GitHub Actions run `26796019884` completed with conclusion `success`.

## Source Linkage

- Repo: <https://github.com/manuelsampedro1/agent-run-ledger>
- Commit: <https://github.com/manuelsampedro1/agent-run-ledger/commit/d1710f50531171a9e8e6edce95d416531711f882>
- CI run: <https://github.com/manuelsampedro1/agent-run-ledger/actions/runs/26796019884>
- CLI: <https://raw.githubusercontent.com/manuelsampedro1/agent-run-ledger/d1710f50531171a9e8e6edce95d416531711f882/src/cli.js>
- Tests: <https://raw.githubusercontent.com/manuelsampedro1/agent-run-ledger/d1710f50531171a9e8e6edce95d416531711f882/test/ledger.test.js>

## Takeaway

Readiness is evidence, not pre-chat trivia. Once a repo readiness report exists, it should travel into the ledger so later reviewers can see whether the run started from a trustworthy workspace or from known blockers.
