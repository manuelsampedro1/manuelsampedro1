# Schema-Backed Tool Example Chain

Use this example when a reviewer wants to verify that tool examples match the
same schema a coding agent will call.

## Scenario

A tool catalog includes a `create_patch_plan` tool with a required `risk_level`
enum. The schema looks reasonable, but an example uses `urgent`, which the tool
will reject at runtime.

## Command Chain

Lint the catalog before exposing it:

```sh
PYTHONPATH=/path/to/agent-tool-schema-lint/src \
  python3 -m agent_tool_schema_lint tools.json \
  --fail-on medium \
  --format json \
  > /tmp/tool-schema-report.json
```

If the example drifts from the schema, the report should include:

```json
{
  "code": "input-example-enum-mismatch",
  "path": "input_examples[0].risk_level"
}
```

Fix the example:

```json
{
  "objective": "Add a regression test for enum validation.",
  "risk_level": "low"
}
```

Run the gate again:

```sh
PYTHONPATH=/path/to/agent-tool-schema-lint/src \
  python3 -m agent_tool_schema_lint tools.json \
  --min-score 100 \
  --format json
```

## Expected Signals

- Missing examples are visible as low findings.
- Invalid or schema-drifting examples are medium findings.
- JSON and Markdown output show `example_count`.
- A clean catalog can reach `ready` and `100/100`.

## Reviewer Interpretation

The schema decides what the tool can accept. Examples should teach the model
how to call that exact interface, not introduce a second, unofficial interface.
