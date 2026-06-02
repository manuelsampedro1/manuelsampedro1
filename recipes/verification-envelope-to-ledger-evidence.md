# Verification Envelope to Ledger Evidence

Use this when a verification tool emits structured JSON and an agent run ledger needs planned command evidence.

## Goal

Import a machine-readable verification envelope directly into the audit ledger, preserving files and commands while keeping their status honest as `planned` until execution happens.

## Source Event

This recipe came from `agent-run-ledger` commit `33813aa34802`, which added support for importing `verify-by-change --json-envelope` artifacts.

Relevant files:

- `src/cli.js`
- `test/ledger.test.js`
- `README.md`

## Workflow

1. Generate a verification envelope from the actual changed files.
2. Detect the envelope by schema version.
3. Read category names as ledger event titles.
4. Copy category files into structured `files`.
5. Copy category commands into structured `commands`.
6. Append one planned command event per category.
7. Run the checks and add passed, failed, blocked, skipped, or done command evidence later.
8. Run strict doctor mode to catch imported checks that were never resolved.

## Checklist

- Does the importer preserve file references separately from commands?
- Does it default imported checks to `planned`?
- Does Markdown checklist import still work?
- Does doctor JSON show open commands after import?
- Does strict doctor fail until planned commands are resolved?

## Verification

For `agent-run-ledger`:

```sh
python3 /path/to/verify-by-change/verify_by_change.py --repo . --json-envelope --output /tmp/verification-envelope.json
node bin/agent-run-ledger.js import-checklist --ledger .agent-run/ledger.jsonl --checklist /tmp/verification-envelope.json
node bin/agent-run-ledger.js doctor --ledger .agent-run/ledger.jsonl --json
node bin/agent-run-ledger.js doctor --ledger .agent-run/ledger.jsonl --strict
```

Expect strict doctor to fail while imported commands are still `planned`.

## Failure Modes

- Treating imported verification plans as already executed.
- Dropping envelope files and keeping only command text.
- Requiring a Markdown conversion step after a tool already emitted structured JSON.
- Breaking existing Markdown checklist imports.
- Letting planned checks disappear from doctor output.

## Source Linkage

- Public repo: <https://github.com/manuelsampedro1/agent-run-ledger>
- Commit: <https://github.com/manuelsampedro1/agent-run-ledger/commit/33813aa348027098e9c52eb0a253a427074954a5>
- CI run: <https://github.com/manuelsampedro1/agent-run-ledger/actions/runs/26795131861>
