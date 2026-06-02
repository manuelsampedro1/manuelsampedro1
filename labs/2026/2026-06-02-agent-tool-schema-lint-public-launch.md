# 2026-06-02 - Agent Tool Schema Lint Public Launch

## Source

- Public repo: https://github.com/manuelsampedro1/agent-tool-schema-lint
- Published HEAD: `086fd3987934ecbce080a0f62971ba8ff91684a2`
- CI run: https://github.com/manuelsampedro1/agent-tool-schema-lint/actions/runs/26838599853

## What Changed

Built and published `agent-tool-schema-lint`, a dependency-free Python CLI for
auditing JSON tool definitions before they are exposed to coding agents.

The tool checks whether each tool definition has:

- specific tool descriptions,
- object-shaped input schemas,
- declared properties and required fields,
- `additionalProperties: false` when closed input is expected,
- useful parameter descriptions,
- enum value guidance,
- safety language for sensitive or destructive tools.

It accepts OpenAI-style function tools, MCP-like `inputSchema` shapes, raw
`parameters`, arrays of tools, or objects with a top-level `tools` list. It emits
Markdown for review, JSON for automation, score gates via `--min-score`, and
severity gates via `--fail-on`.

## Why It Matters

Tool-call safety is not only a runtime authorization problem. If the schema is
vague, the agent has to infer when to call the tool, what each field means, and
whether extra arguments are acceptable.

`agent-tool-schema-lint` moves part of that review earlier. It gives tool authors
a small preflight before MCP tools, function tools, or local automation hooks are
added to an agent run.

## Verification

Ran locally:

```sh
make test
make lint
make build
make smoke
git diff --check
```

Additional checks:

- editable install in a temporary virtualenv after upgrading `pip`, `setuptools`, and `wheel`,
- installed CLI smoke run against `examples/good-tools.json`,
- `agent-instruction-audit AGENTS.md --min-score 80` at `100/100`,
- `repo-flightcheck . --check-remote --strict --threshold 80` at `100/100`,
- public raw README/source/test/example URLs returned `200`,
- GitHub Actions run `26838599853` completed with `success`.

## Takeaway

Lint tool schemas before handing them to an agent. Strong runtime permissions
matter, but schema clarity is the first line of defense against ambiguous or
over-broad tool calls.
