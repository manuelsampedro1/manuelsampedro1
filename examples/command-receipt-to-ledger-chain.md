# Command Receipt to Ledger Chain

Use this example when a reviewer needs to know whether command evidence survived
handoff with integrity.

## Scenario

A coding agent ran tests and produced a closeout. The reviewer does not want to
trust a prose claim such as "tests passed"; they want a durable record that ties
the command to evidence files and keeps drift visible.

## Command Chain

Create a receipt for the executed command:

```sh
python3 -m agent_command_receipt create \
  --command "npm test" \
  --status pass \
  --exit-code 0 \
  --base-dir . \
  --evidence /tmp/test-output.log \
  --output /tmp/command-receipt.json
```

Import the receipt into the ledger:

```sh
node /path/to/agent-run-ledger/bin/agent-run-ledger.js import-receipt \
  --ledger /tmp/agent-run-ledger.jsonl \
  --receipt /tmp/command-receipt.json \
  --base-dir .
```

Check strict ledger status:

```sh
node /path/to/agent-run-ledger/bin/agent-run-ledger.js doctor \
  --ledger /tmp/agent-run-ledger.jsonl \
  --strict
```

## Expected Signals

- The ledger records one command event with the exact command from the receipt.
- The event references both the receipt JSON and the evidence files.
- Passing receipts with unchanged evidence become `passed` command events.
- Missing, changed, or unknown receipt evidence becomes `blocked`, so strict
  doctor mode cannot close the run silently.

## Reviewer Interpretation

This chain separates three claims:

- the command was reported,
- the evidence files existed with specific hashes,
- the current ledger can still verify those files.

If any part breaks, the handoff is not ready to treat that command as durable
proof.

## Review Prompt

```text
Review this handoff as command-evidence integrity. Confirm the receipt records
the exact command and evidence hashes, then confirm the ledger import checked
those files and strict doctor mode has no open or blocked command evidence.
Do not accept a closeout sentence as equivalent to a verified receipt event.
```
