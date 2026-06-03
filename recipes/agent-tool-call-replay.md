# Agent Tool Call Replay

## Use When

You have captured agent tool calls and need to know whether those calls still
match the current tool catalog before rerunning them or reusing them as evidence.

## Inputs

- Tool catalog JSON from OpenAI-style functions, MCP-like tools, or local tool
  definitions.
- Tool-call log as JSONL, JSON array, or object with `calls`, `tool_calls`, or
  `events`.
- Optional score or severity threshold for CI gating.

## Command

```sh
agent-tool-call-replay tools.json tool-calls.jsonl --min-score 80
```

When the transcript will be reused as evidence:

```sh
agent-tool-call-replay tools.json tool-calls.jsonl --require-call-ids
```

For automation:

```sh
agent-tool-call-replay tools.json tool-calls.jsonl --format json --fail-on medium
```

## Review Checklist

- Unknown tools are stale names, wrapper names, or missing catalog entries.
- Invalid JSON argument strings are fixed before rerun.
- Missing required fields are treated as blocked calls, not cosmetic warnings.
- Enum or const failures are checked for schema drift versus bad agent behavior.
- Extra arguments are reviewed against `additionalProperties`.
- Unsupported schema combinators get manual review before publishing proof.
- Evidence transcripts include stable call ids when another system will reuse
  the replay output.
- Duplicate call ids block strict evidence reuse because per-call findings
  become ambiguous.
- A schema-valid call is still separately checked for authorization and runtime
  safety.

## Output Contract

- `status`: `pass`, `pass-with-notes`, `review`, or `blocked`.
- `score`: deterministic score out of 100.
- `call_id_count`: number of calls with stable ids.
- `findings`: severity, rule, call index, tool, path, message, and redacted
  evidence.
- `calls`: per-call id, status, argument keys, and finding count.
- `follow_up_checks`: reviewer actions that should happen outside schema replay.

## Source

- Public repo: https://github.com/manuelsampedro1/agent-tool-call-replay
- Launch note: [2026-06-02 - Agent Tool Call Replay Public Launch](../labs/2026/2026-06-02-agent-tool-call-replay-public-launch.md)
