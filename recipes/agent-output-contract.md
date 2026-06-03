# Agent Output Contract

Use this pattern when agent workflow tools emit JSON that another system will consume: CI summaries, review packets, ledgers, merge gates, profile proof, or regression cases.

## Contract Shape

Require each output to include:

- `schema_version`: a non-placeholder version string.
- exactly one outcome field: `status`, `verdict`, or `result`.
- a recognized outcome, such as `pass`, `fail`, `ready`, `needs-review`, or `blocked`.
- `score` only when it is an integer from `0` to `100`.
- issue-like fields as arrays, not strings.
- actionable evidence when the outcome is failing or blocked.
- no blocking findings when the outcome is passing.

## CLI Pattern

```sh
agent-output-contract check output.json
agent-output-contract check reports/*.json
agent-output-contract check output.json --format json
```

The important distinction: a tool output with `status: fail` can still pass the output contract when it includes clear issues. The contract should fail when the JSON is invalid, ambiguous, contradictory, or unsafe to reuse.

## Review Rule

Do not let downstream automation infer meaning from arbitrary JSON. Before a ledger, proof packet, or CI summary consumes an output, check:

- Can the consumer identify the schema?
- Can it find one outcome without guessing?
- Are blockers represented as structured lists?
- Does a passing outcome avoid hidden blockers?
- Does a failing outcome provide actionable evidence?
- Is the output free of obvious secrets and local absolute paths?

## Public Example

The implementation lives in [`agent-output-contract`](https://github.com/manuelsampedro1/agent-output-contract), with valid and invalid examples under `examples/`.
