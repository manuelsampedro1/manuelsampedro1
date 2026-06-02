# 2026-06-02 - Agent Run Ledger JSON Doctor

## Context

`agent-run-ledger doctor` already validated JSONL ledgers and printed a compact human summary. That was useful for local review, but weak for CI and automation because another tool would have to parse human text to learn event counts, command evidence, attention items, and referenced files.

## Change

- Added `doctor --json`.
- The JSON payload starts with `schema_version: "agent-run-ledger.doctor.v1"`.
- The payload includes the ledger path and the existing structured summary from `summarize`.
- Added boolean flag parsing for `--json`.
- Added `node:test` coverage that writes a demo ledger, runs `doctor --json`, parses stdout, and checks event, command, and attention counts.
- Updated README examples so text and machine-readable doctor output are both visible.

Public commit: `996a824ba7a1 feat: add json doctor output`.

## Verification

Local checks:

```sh
node --test
node scripts/lint.js
node scripts/build.js
node bin/agent-run-ledger.js doctor --ledger examples/sample-ledger.jsonl
node bin/agent-run-ledger.js doctor --ledger examples/sample-ledger.jsonl --json > /tmp/agent-run-ledger-doctor.json
node -e 'const fs=require("fs"); const payload=JSON.parse(fs.readFileSync("/tmp/agent-run-ledger-doctor.json", "utf8")); if (payload.schema_version !== "agent-run-ledger.doctor.v1" || payload.summary.eventCount !== 4) process.exit(1);'
git diff --check
```

Results:

- `node --test`: 11 tests passed.
- Lint and build preflight passed.
- Text doctor output still returned `Ledger OK: 4 events`.
- JSON doctor output parsed successfully and reported the expected schema and sample event count.
- Public commit page and raw changed files returned `200`.
- GitHub Actions run `26792794350` completed with conclusion `success`.

## Source Linkage

- Repo: <https://github.com/manuelsampedro1/agent-run-ledger>
- Commit: <https://github.com/manuelsampedro1/agent-run-ledger/commit/996a824ba7a14df4da77f3d227ee3e5f48298bb3>
- CI run: <https://github.com/manuelsampedro1/agent-run-ledger/actions/runs/26792794350>
- CLI: <https://raw.githubusercontent.com/manuelsampedro1/agent-run-ledger/996a824/src/cli.js>
- Tests: <https://raw.githubusercontent.com/manuelsampedro1/agent-run-ledger/996a824/test/ledger.test.js>

## Takeaway

Audit tools should expose the same truth in two forms: readable text for humans and stable JSON for automation. Once a doctor command can emit JSON, CI jobs and proof-packet generators can consume ledger status without brittle text parsing.
