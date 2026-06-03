# Structured Output Checks

Use this pattern when a JSON output from an agent workflow will be consumed by
CI, a run ledger, a review packet, a merge gate, a profile proof note, or a
regression fixture.

## Problem

A JSON output can be syntactically valid and still be weak evidence. A bare
`status: pass` does not show which checks ran, and a passing output that embeds
a failed check is contradictory.

## Pattern

Run the output contract with structured checks required:

```sh
agent-output-contract check output.json \
  --require-checks \
  --format json \
  > /tmp/output-contract.json
```

Treat these as blockers:

- missing `checks`;
- empty `checks`;
- check entries that are not objects;
- check entries without a non-empty `name`, `check`, `command`, or `id`;
- check entries without exactly one outcome field;
- a passing output that contains a failed, blocked, partial, or needs-review
  check.

## Acceptance Criteria

- The output has `schema_version`.
- Exactly one top-level outcome field is present.
- `score`, when present, is an integer from `0` to `100`.
- Issue-like fields are arrays.
- Failing outputs include actionable evidence.
- Passing outputs have non-empty structured checks when `--require-checks` is
  used.
- JSON or text output exposes `check_count`.

## Review Rule

Structured checks prove only that the output made its internal evidence
inspectable. They do not prove the underlying command, CI run, or reviewer claim
is true; that remains the next evidence check.
