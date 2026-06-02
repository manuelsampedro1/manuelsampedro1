# Machine-Readable Doctor Output

Use this when a CLI has a `doctor`, `check`, or `validate` command that currently prints only human text.

## Goal

Make validation output useful for both humans and automation. A reviewer can read text output, while CI or another local tool can parse a stable JSON contract.

## Source Event

This recipe came from `agent-run-ledger` commit `996a824ba7a1`, which added `doctor --json` to the ledger validator.

Relevant files:

- `src/cli.js`
- `test/ledger.test.js`
- `README.md`

## Workflow

1. Keep the existing text output unchanged for normal local use.
2. Add a boolean `--json` flag to the validator command.
3. Start the JSON payload with a stable `schema_version`.
4. Include the input path that was validated.
5. Reuse the same internal summary object that text output already trusts.
6. Add a CLI test that parses stdout as JSON and asserts meaningful fields.
7. Document both text and JSON examples in the README.

## Checklist

- Does text output remain backward-compatible?
- Does JSON output include `schema_version`?
- Does the payload include enough data for CI to make a decision without parsing prose?
- Does a test parse the emitted JSON instead of only matching a substring?
- Is the schema narrow and honest rather than a fake score?

## Verification

For a zero-dependency Node CLI, run:

```sh
node --test
node scripts/lint.js
node scripts/build.js
node bin/agent-run-ledger.js doctor --ledger examples/sample-ledger.jsonl --json
```

Then parse the JSON in a separate command so malformed output fails fast:

```sh
node bin/agent-run-ledger.js doctor --ledger examples/sample-ledger.jsonl --json > /tmp/doctor.json
node -e 'JSON.parse(require("fs").readFileSync("/tmp/doctor.json", "utf8"))'
```

## Failure Modes

- Making JSON output a lightly formatted version of human text.
- Omitting `schema_version`, which makes future changes ambiguous.
- Testing only the parser and not the actual CLI stdout.
- Changing text output while adding JSON and breaking existing usage.
- Adding a confidence score that the validator does not actually prove.

## Source Linkage

- Public repo: <https://github.com/manuelsampedro1/agent-run-ledger>
- Commit: <https://github.com/manuelsampedro1/agent-run-ledger/commit/996a824ba7a14df4da77f3d227ee3e5f48298bb3>
- CI run: <https://github.com/manuelsampedro1/agent-run-ledger/actions/runs/26792794350>
