# 2026-06-02 - Agent Run Ledger Command Status

## Context

`agent-run-ledger` is a primary proof repo because it makes AI-agent work auditable through JSONL events and static reports. The README said command-like evidence needed a status, but the validator accepted command events without `passed`, `failed`, `blocked`, or another outcome marker.

## Change

- Added validation that requires `status` for events with `type: "command"` or any `commands` entries.
- Added a unit test for command events without status.
- Added a CLI regression test proving `note --type command --command ...` is rejected without `--status`.
- Updated README wording so the schema contract matches runtime behavior.

Public commit: `0ca833a526df feat: require status for command evidence`.

## Verification

Local checks:

```sh
node --test
node scripts/lint.js
node scripts/build.js
node bin/agent-run-ledger.js doctor --ledger examples/sample-ledger.jsonl
node bin/agent-run-ledger.js report --ledger examples/sample-ledger.jsonl --out /tmp/agent-run-ledger-report.html
test -s /tmp/agent-run-ledger-report.html
git diff --check
```

Public checks:

- Raw `src/ledger.js` returned `200`.
- Raw `test/ledger.test.js` returned `200`.
- GitHub Actions run `26792162435` for commit `0ca833a526df52d1d641864670694dba663c3c6a` completed with conclusion `success`.

`npm` is not installed in this local environment, so verification used the direct commands behind the package scripts.

## Source Linkage

- Repo: <https://github.com/manuelsampedro1/agent-run-ledger>
- Commit: <https://github.com/manuelsampedro1/agent-run-ledger/commit/0ca833a526df52d1d641864670694dba663c3c6a>
- CI run: <https://github.com/manuelsampedro1/agent-run-ledger/actions/runs/26792162435>
- Tests: <https://raw.githubusercontent.com/manuelsampedro1/agent-run-ledger/0ca833a/test/ledger.test.js>

## Takeaway

Audit ledgers should not record command evidence without an outcome. A command with no status forces reviewers to guess whether it passed, failed, was skipped, or blocked the run.
