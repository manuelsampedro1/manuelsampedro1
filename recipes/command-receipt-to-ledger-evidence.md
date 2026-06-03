# Command Receipt to Ledger Evidence

Use this pattern when a coding-agent closeout needs durable command proof rather
than a sentence saying tests passed.

## Problem

Command evidence gets weaker as it moves through handoffs:

- terminal output disappears from chat context,
- closeouts compress results into prose,
- proof packets can reference files without checking whether they changed,
- ledgers can preserve a command but still lack evidence integrity.

## Pattern

Create a command receipt immediately after running a meaningful check:

```sh
python3 -m agent_command_receipt create \
  --command "npm test" \
  --status pass \
  --exit-code 0 \
  --base-dir . \
  --evidence /tmp/test-output.log \
  --output /tmp/command-receipt.json
```

Import the receipt into the run ledger:

```sh
node bin/agent-run-ledger.js import-receipt \
  --ledger .agent-run/ledger.jsonl \
  --receipt /tmp/command-receipt.json \
  --base-dir .
```

Then require strict ledger review before closeout:

```sh
node bin/agent-run-ledger.js doctor --ledger .agent-run/ledger.jsonl --strict
```

## Acceptance Criteria

- The receipt uses `agent-command-receipt.v1`.
- The receipt includes the exact command, outcome, exit code, and evidence file
  hashes.
- Ledger import verifies evidence sizes and SHA-256 hashes.
- Drifted, missing, or unknown receipt evidence becomes non-closed ledger
  attention.
- The final closeout references the ledger event, not only the original command
  sentence.

## Review Rule

For important checks, do not accept "tests passed" as durable evidence. Accept a
verified receipt imported into the ledger, or keep the command evidence open.
