# 2026-06-02 - Agent Run Ledger Readiness Task Contract Import

## Context

`repo-flightcheck` now emits structured `taskContract` metadata in both full readiness JSON and agent contract output.

Before this change, `agent-run-ledger import-readiness` could record the readiness summary and failed checks, but it ignored whether the readiness report was tied to a complete task contract.

## Change

- Normalized `taskContract` from `repo-flightcheck --json` reports.
- Normalized `taskContract` from `repo-flightcheck --contract` artifacts.
- Imported passing readiness task contracts as `done` decision events.
- Imported incomplete readiness task contracts as `blocked` blocker events.
- Kept task-contract evidence before the repo readiness summary in the ledger.
- Updated README guidance for readiness imports.

Public commit: `2ac604b feat: import readiness task contracts`.

## Verification

Local checks:

```sh
node --test
node scripts/lint.js
node scripts/build.js
git diff --check
```

Cross-tool smoke:

```sh
node /path/to/repo-flightcheck/bin/repo-flightcheck.js /tmp/task-contract-smoke-repo --json > /tmp/readiness.json

node /path/to/agent-run-ledger/bin/agent-run-ledger.js import-readiness \
  --ledger /tmp/task-contract-smoke-repo/ledger.jsonl \
  --readiness-report /tmp/readiness.json
```

Results:

- `node --test`: 56 tests passed.
- `node scripts/lint.js`: passed.
- `node scripts/build.js`: passed.
- `git diff --check`: passed.
- Cross-tool smoke produced `taskContract.status` as `pass`.
- Cross-tool smoke imported `Task contract passed` before the repo readiness event.
- GitHub Actions run `26810454727` completed with conclusion `success`.
- `repo-flightcheck --check-remote --strict --threshold 80`: `98/100`; the only warning was missing local `npm`, while direct `node` checks passed.

## Source Linkage

- Repo: <https://github.com/manuelsampedro1/agent-run-ledger>
- Commit: <https://github.com/manuelsampedro1/agent-run-ledger/commit/2ac604b2fc0068d2f68cbed23b20cec33fa012d4>
- CI run: <https://github.com/manuelsampedro1/agent-run-ledger/actions/runs/26810454727>
- CLI: <https://raw.githubusercontent.com/manuelsampedro1/agent-run-ledger/2ac604b2fc0068d2f68cbed23b20cec33fa012d4/src/cli.js>
- Tests: <https://raw.githubusercontent.com/manuelsampedro1/agent-run-ledger/2ac604b2fc0068d2f68cbed23b20cec33fa012d4/test/ledger.test.js>
- Readiness source: <https://github.com/manuelsampedro1/repo-flightcheck>

## Takeaway

Readiness evidence is stronger when it carries the task boundary that produced it. A clean readiness score and a complete task contract should be recorded as separate evidence so reviewers can see both repository health and task scope.
