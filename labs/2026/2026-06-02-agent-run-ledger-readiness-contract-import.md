# 2026-06-02 - Agent Run Ledger Readiness Contract Import

## Context

`repo-flightcheck` now emits a compact `repo-flightcheck.agent-contract.v1` readiness contract. `agent-run-ledger` already imported full `repo-flightcheck --json` reports, but it rejected the compact contract because it expected `summary` and `checks`.

That left a useful cross-tool loop incomplete: a repo could generate a machine-readable agent-readiness contract, but the run ledger could not record that contract as evidence or turn required blockers into ledger blockers.

## Change

- Taught `import-readiness` to accept `repo-flightcheck.agent-contract.v1` artifacts.
- Normalized `requiredBeforeAgent` into blocker events.
- Normalized `recommendedBeforeAgent` into decision/attention events.
- Preserved the existing full-report import path.
- Added extraction for Git status evidence such as ` M README.md` so ledger events point at the actual file.
- Added parser, event conversion, and CLI import tests.
- Updated README examples to show both `--json` and `--contract` imports.

Public commit: `331b91fdd405 feat: import readiness contracts`.

## Verification

Local checks:

```sh
node --test
node scripts/lint.js
node scripts/build.js
git diff --check
node /Users/manuelsampedro/Documents/Codex/2026-05-21/repo-flightcheck/bin/repo-flightcheck.js . --strict --threshold 80
node /Users/manuelsampedro/Documents/Codex/2026-05-21/repo-flightcheck/bin/repo-flightcheck.js . --contract --threshold 80
node bin/agent-run-ledger.js import-readiness --ledger /tmp/ledger.jsonl --readiness-report /tmp/readiness-contract.json --command "node repo-flightcheck --contract --threshold 80"
node bin/agent-run-ledger.js doctor --ledger /tmp/ledger.jsonl --json
node bin/agent-run-ledger.js doctor --ledger /tmp/ledger.jsonl --strict
node bin/agent-run-ledger.js report --ledger /tmp/ledger.jsonl --out /tmp/report.html
```

Results:

- `node --test`: 28 tests passed.
- `node scripts/lint.js`: passed across 14 files.
- `node scripts/build.js`: generated demo ledger and report.
- Dirty-tree smoke: imported a contract with 1 required blocker, `doctor --strict` exited `1`, and an HTML report was generated.
- Clean-tree smoke after commit: contract `ready: true`, score `100`, 1 ledger event, 0 attention items, 0 open commands.
- `repo-flightcheck`: `100/100` after commit.
- GitHub Actions run `26799042402` completed with conclusion `success`.

## Source Linkage

- Repo: <https://github.com/manuelsampedro1/agent-run-ledger>
- Commit: <https://github.com/manuelsampedro1/agent-run-ledger/commit/331b91fdd4058f8086342250c9b165c8b8a6e00a>
- CI run: <https://github.com/manuelsampedro1/agent-run-ledger/actions/runs/26799042402>
- CLI: <https://raw.githubusercontent.com/manuelsampedro1/agent-run-ledger/main/src/cli.js>
- Tests: <https://raw.githubusercontent.com/manuelsampedro1/agent-run-ledger/main/test/ledger.test.js>
- Readiness contract producer: <https://github.com/manuelsampedro1/repo-flightcheck>

## Takeaway

Compact readiness contracts should not stop at generation. Importing them into the run ledger makes pre-agent blockers durable evidence, and strict doctor mode can keep the handoff open until those blockers are resolved.
