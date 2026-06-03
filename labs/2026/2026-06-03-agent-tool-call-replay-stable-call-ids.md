# 2026-06-03 - Agent Tool Call Replay Stable Call IDs

## What Changed

Added stable-call-id gating to
[`agent-tool-call-replay`](https://github.com/manuelsampedro1/agent-tool-call-replay).

The CLI can now run with:

```sh
agent-tool-call-replay tools.json tool-calls.jsonl --require-call-ids
```

In that mode, each replayed call needs a stable id from `id`, `call_id`, or
`tool_call_id`. Duplicate ids block the report because per-call findings would
be ambiguous.

## Why It Matters

Tool-call replay already answers whether captured arguments still match the
current schema. Evidence reuse needs one more property: a reviewer should be
able to map every replay finding back to the exact transcript entry.

This change helps separate:

- schema-compatible calls;
- calls with stable transcript identity;
- ambiguous transcripts with missing or duplicate ids;
- replay evidence that still needs separate authorization or runtime proof.

## Verification Evidence

- Added opt-in `--require-call-ids`.
- Added `call_id_count` to Markdown and JSON reports.
- Added `call_id` to each per-call summary.
- Added validation for missing call ids and duplicate call ids.
- Updated smoke verification and the passing fixture to exercise stable ids.
- Added regression tests for accepted ids, missing ids, duplicate ids, and JSON
  output.
- Verified the public repo with tests, lint, build, smoke, whitespace checks,
  local Git identity audit, raw GitHub source URLs, `repo-flightcheck` at
  `100/100`, and GitHub Actions success for commits
  `b4c6d8f34b57f70f7a3e9701d04badbce80bfa77` and
  `a4f31946493428773b2b7d6d71be1abd35353474` in runs `26871783674` and
  `26871868652`.

## Reusable Lesson

Schema replay is stronger when every finding has a stable transcript identity.
Stable ids do not prove execution or authorization, but they make later review,
ledger import, and proof-packet composition less ambiguous.
