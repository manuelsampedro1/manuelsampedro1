# Agent Tool Schema Lint

Use this before exposing JSON tool definitions to a coding agent.

## Source

- Public tool: https://github.com/manuelsampedro1/agent-tool-schema-lint
- Launch note: [2026-06-02 - Agent Tool Schema Lint Public Launch](../labs/2026/2026-06-02-agent-tool-schema-lint-public-launch.md)

## Pattern

1. Save the tool definitions:

```sh
agent-tool-schema-lint tools.json --min-score 80
```

2. Fail CI on unclear or unsafe schemas:

```sh
agent-tool-schema-lint tools.json --fail-on medium --min-score 85
```

3. Write a review report:

```sh
agent-tool-schema-lint tools.json --write-report /tmp/tool-schema-report.md
```

4. Fix vague descriptions, missing `required` fields, open extra properties, and
missing safety language before the tools are made callable.

## What Good Looks Like

- Each tool description says when to use the tool and what it does not do.
- Input schemas are object-shaped and declare expected properties.
- Required fields are explicit.
- Extra properties are rejected unless open input is intentional.
- Parameter descriptions include format, constraints, or examples.
- Enums explain how values should be selected.
- Input examples are present for important tools and match required fields,
  closed-schema properties, simple JSON types, and enum values.
- Sensitive tools mention approval, dry-run, validation, or authorization.

## Prompt Pattern

```text
Review these tool schemas before I expose them to a coding agent.

Rules:
- Do not judge runtime implementation yet; judge whether the schema is safe and clear enough to call.
- Flag vague tool descriptions, missing object schemas, absent required fields, open extra properties, weak parameter descriptions, unclear enums, schema-drifting input examples, and sensitive tools without safety language.
- Return the smallest concrete schema changes needed before the tools become callable.

<agent-tool-schema-lint output>
<tool definitions>
```

## Pair With

- `agent-context-sentinel` before untrusted tool context reaches the agent,
- `mcp-guard` when runtime calls need allow, block, or approval rules,
- `agent-tool-call-audit` after a run to review what the agent actually called,
- `agent-command-receipt` when command outcomes need reusable evidence.

Follow-up: [Schema-Backed Tool Examples](./schema-backed-tool-examples.md).

## Failure Mode

Do not treat a passing schema lint as proof that the implementation is safe. It
only means the agent-facing interface is specific enough to review before runtime
authorization and behavior testing.
