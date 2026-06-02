# Command Evidence Status Contract

Use this when an agent audit log, run ledger, or proof packet records shell commands as review evidence.

## Goal

Every recorded command should carry an outcome status. A reviewer should never have to infer whether a verification command passed, failed, blocked the run, or was skipped.

## Source Event

This recipe came from `agent-run-ledger` commit `0ca833a526df`, which changed validation so command events and events with `commands` require `status`.

Relevant files:

- `src/ledger.js`
- `test/ledger.test.js`
- `README.md`

## Workflow

1. Define allowed statuses before accepting ledger events.
2. Treat `type: "command"` as command evidence.
3. Treat any event with a non-empty `commands` array as command evidence, even if its type is `decision` or `change`.
4. Reject command evidence without `status`.
5. Keep status validation separate from event-type validation so unsupported statuses still produce a clear error.
6. Add a CLI regression test that tries to record `--type command --command "..."` without `--status`.
7. Update README/schema text so examples and runtime behavior match.

## Checklist

- Does every command event include `status`?
- Do decision/change events with command evidence also require `status`?
- Does the CLI fail before appending invalid JSONL?
- Does the sample ledger still validate?
- Does the report show command statuses without inventing a default?

## Verification

For a zero-dependency Node CLI, run:

```sh
node --test
node scripts/lint.js
node scripts/build.js
node bin/agent-run-ledger.js doctor --ledger examples/sample-ledger.jsonl
```

The source change also has public CI success.

## Failure Modes

- Defaulting missing command status to `done` and hiding uncertainty.
- Only checking `type: "command"` while allowing other event types to carry status-free commands.
- Updating docs without adding a validator regression test.
- Letting the CLI append invalid ledger lines before validation fails.

## Source Linkage

- Public repo: <https://github.com/manuelsampedro1/agent-run-ledger>
- Commit: <https://github.com/manuelsampedro1/agent-run-ledger/commit/0ca833a526df52d1d641864670694dba663c3c6a>
- CI run: <https://github.com/manuelsampedro1/agent-run-ledger/actions/runs/26792162435>
