# 2026-06-02 - Agent Tool Call Replay Public Launch

## Source

- Repo: https://github.com/manuelsampedro1/agent-tool-call-replay
- Commit: `8cb35cdd4e1e8952060aac2ca38ed9149e9c3ccf`
- CI: https://github.com/manuelsampedro1/agent-tool-call-replay/actions/runs/26844074841

## What Shipped

`agent-tool-call-replay` is a dependency-free Python CLI that replays captured
agent tool calls against a current tool catalog. It supports OpenAI-style
function tools, MCP-like `inputSchema` tools, local JSON tool definitions,
JSONL logs, JSON arrays, and wrapper objects with `calls`, `tool_calls`, or
`events`.

The tool flags:

- unknown tool names,
- invalid JSON argument strings,
- non-object argument payloads,
- missing required fields,
- extra arguments when `additionalProperties` is false,
- type mismatches,
- enum and const drift,
- array item mismatches,
- unsupported schema combinators that need manual review.

## Why It Matters

Tool schemas are not static. A transcript can look useful while its arguments no
longer match the current interface. That makes proof packets, reruns, eval cases,
and ledger imports weaker than they look.

This project fills the gap between:

- `agent-tool-schema-lint`, which checks whether tool definitions are clear and
  constrained, and
- `agent-tool-call-audit`, which checks whether a run included risky tool-call
  behavior.

Replay checks whether the captured calls still fit the schema that will be used
now.

## Verification

- `make test` passed with 9 tests.
- `make lint` passed.
- `make build` passed.
- `make smoke` passed with `100/100`.
- JSON smoke returned `pass 100 2`.
- Bad-call smoke failed as expected on high-severity findings.
- Editable install succeeded after upgrading `pip`, `setuptools`, and `wheel`.
- Installed CLI JSON smoke returned `pass 100 2`.
- `agent-instruction-audit AGENTS.md --min-score 80` returned `100/100`.
- Raw GitHub URLs for README, CLI, tests, and examples returned `200`.
- GitHub Actions run `26844074841` completed with `success`.
- `repo-flightcheck --check-remote --strict --threshold 80` returned `100/100`.

## Next Use

Use this before publishing tool-call examples, importing transcripts into
`agent-run-ledger`, or using captured calls as proof in a review packet.

