# Schema-Backed Tool Examples

Use this pattern before exposing a JSON tool catalog to a coding agent,
especially when a tool has nested inputs, enums, or high-cost actions.

## Problem

Tool schemas can be technically valid while their examples are absent or wrong:

- required fields are missing from the sample call;
- examples include fields the schema rejects;
- enum examples use values not accepted at runtime;
- parameter types drift from the schema;
- reviewers have no fast way to see how the model should call the tool.

## Pattern

Add realistic examples beside the schema:

```json
{
  "name": "create_patch_plan",
  "description": "Creates a non-executing patch plan for a proposed code change. Does not modify the repository.",
  "input_schema": {
    "type": "object",
    "additionalProperties": false,
    "required": ["objective", "risk_level"],
    "properties": {
      "objective": {
        "type": "string",
        "description": "Concrete change objective that the patch plan should address."
      },
      "risk_level": {
        "type": "string",
        "enum": ["low", "medium", "high"],
        "description": "Expected review risk for this planned change."
      }
    }
  },
  "input_examples": [
    {
      "objective": "Add regression coverage for enum validation.",
      "risk_level": "low"
    }
  ]
}
```

Lint the catalog:

```sh
PYTHONPATH=/path/to/agent-tool-schema-lint/src \
  python3 -m agent_tool_schema_lint tools.json \
  --fail-on medium \
  --min-score 85
```

## Acceptance Criteria

- Every important tool has at least one realistic input example.
- Each example is a JSON object.
- Required fields appear in the example.
- Closed schemas reject extra example properties.
- Simple JSON types match the parameter schema.
- Enum example values are in the declared enum list.
- The linter report shows `example_count` for reviewer scanability.

## Review Rule

Do not treat examples as documentation-only. If an example would fail the
schema, fix the example or the schema before giving the tool to an agent.
