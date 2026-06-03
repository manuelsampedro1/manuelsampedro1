# Stable Tool Call IDs

Use this pattern when a saved agent tool-call transcript will become review
evidence, regression input, run-ledger context, or proof-packet support.

## Problem

A replay can show that arguments still match the current schema, but reviewers
also need to know which captured call each finding belongs to. Missing ids make
later evidence joins fragile. Duplicate ids make per-call findings ambiguous.

## Pattern

Require stable ids before reusing the replay report:

```sh
agent-tool-call-replay tools.json tool-calls.jsonl \
  --require-call-ids \
  --format json \
  > /tmp/tool-call-replay.json
```

Accepted id fields are:

- `id`;
- `call_id`;
- `tool_call_id`.

Treat these as blockers:

- any replayed call with no stable id;
- any repeated id in the same transcript;
- any replay report where `call_id_count` is lower than `call_count`.

## Acceptance Criteria

- Tool arguments still validate against the current schema.
- `call_id_count` equals the number of replayed calls.
- Each per-call summary exposes the id a reviewer can trace back to the
  transcript.
- Missing or duplicate ids fail before the report feeds a ledger, regression
  fixture, or proof packet.

## Review Rule

Stable ids improve traceability. They do not prove that a tool call was
authorized, executed, or returned the claimed result. Pair replay evidence with
approval checks, command receipts, runtime logs, or ledger events when those
claims matter.
