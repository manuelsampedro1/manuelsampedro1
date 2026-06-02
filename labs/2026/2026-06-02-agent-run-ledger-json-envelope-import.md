# 2026-06-02 - Agent Run Ledger JSON Envelope Import

## Context

`agent-run-ledger` could import Markdown verification checklists as planned command evidence. `verify-by-change` then gained `--json-envelope`, which carries schema, source metadata, changed files, empty state, and categories.

The audit loop was close but not complete: a structured verification artifact still had to be converted back to Markdown before it could become ledger evidence.

## Change

- Added JSON envelope detection inside `import-checklist`.
- Parsed `verify-by-change.v1` envelopes into planned command events.
- Preserved category titles, files, and commands from the envelope.
- Kept Markdown checklist import behavior as the fallback path.
- Added parser tests for JSON envelopes and Markdown fallback.
- Added CLI coverage for importing a JSON envelope into a ledger.
- Updated README examples to show both Markdown and JSON envelope import.

Public commit: `33813aa34802 feat: import verification json envelopes`.

## Verification

Local checks:

```sh
node --test
node scripts/lint.js
node scripts/build.js
git diff --check
```

JSON envelope smoke:

```sh
tmpdir=$(mktemp -d)
printf '{"schema_version":"verify-by-change.v1","source":{"type":"explicit_paths"},"changed_files":["README.md"],"empty":false,"categories":{"docs":{"files":["README.md"],"commands":["Review rendered Markdown and verify links if public-facing."]}}}\n' > "$tmpdir/checklist.json"
node bin/agent-run-ledger.js import-checklist --ledger "$tmpdir/ledger.jsonl" --checklist "$tmpdir/checklist.json"
node bin/agent-run-ledger.js doctor --ledger "$tmpdir/ledger.jsonl" --json > "$tmpdir/doctor.json"
```

Results:

- `node --test`: 17 tests passed.
- Lint and build preflight passed through `node scripts/lint.js` and `node scripts/build.js`.
- Local `npm` was not available in the Codex shell, so `npm test` / `npm run check` could not be run locally.
- The JSON envelope smoke imported one planned verification event and doctor JSON showed one open command.
- `git diff --check` passed.
- Public commit page and raw changed files returned `200`.
- GitHub Actions run `26795131861` completed with conclusion `success`.

## Source Linkage

- Repo: <https://github.com/manuelsampedro1/agent-run-ledger>
- Commit: <https://github.com/manuelsampedro1/agent-run-ledger/commit/33813aa348027098e9c52eb0a253a427074954a5>
- CI run: <https://github.com/manuelsampedro1/agent-run-ledger/actions/runs/26795131861>
- CLI: <https://raw.githubusercontent.com/manuelsampedro1/agent-run-ledger/33813aa348027098e9c52eb0a253a427074954a5/src/cli.js>
- Tests: <https://raw.githubusercontent.com/manuelsampedro1/agent-run-ledger/33813aa348027098e9c52eb0a253a427074954a5/test/ledger.test.js>

## Takeaway

Structured verification artifacts should flow directly into the audit ledger. That keeps planned checks, source metadata, and later execution evidence connected instead of scattered across Markdown, JSON, and final-answer prose.
