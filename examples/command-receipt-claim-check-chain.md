# Command Receipt Claim Check Chain

Use this example when a reviewer needs to verify that a closeout command claim
is backed by durable evidence.

## Scenario

A coding agent changed auth-related files and wrote a closeout that claims a
test command passed. The reviewer wants to avoid accepting a command string as
proof unless the referenced output still matches the recorded receipt.

## Command Chain

Create a receipt from the real command output:

```sh
python3 -m agent_command_receipt create \
  --command "PYTHONPATH=src python3 -m unittest discover -s tests" \
  --status pass \
  --exit-code 0 \
  --base-dir . \
  --evidence /tmp/test-output.log \
  --output /tmp/command-receipt.json
```

Check the closeout against the diff and receipt:

```sh
PYTHONPATH=/path/to/agent-claim-check/src \
  python3 -m agent_claim_check /tmp/closeout.md \
  --diff /tmp/agent-change.diff \
  --receipt /tmp/command-receipt.json \
  --receipt-base-dir .
```

Preserve the same receipt in the run ledger:

```sh
node /path/to/agent-run-ledger/bin/agent-run-ledger.js import-receipt \
  --ledger /tmp/agent-run-ledger.jsonl \
  --receipt /tmp/command-receipt.json \
  --base-dir .
```

## Expected Signals

- `agent-claim-check` accepts the claimed command only if the receipt verifies.
- Drifted or missing receipt evidence becomes a blocking claim-check finding.
- Non-pass receipts do not support a passing closeout claim.
- `agent-run-ledger` preserves the same receipt as command evidence for later
  review.

## Reviewer Interpretation

This chain separates command phrasing from command evidence. A closeout can
state the exact command, but the receipt decides whether the evidence behind
that command is still intact.

## Review Prompt

```text
Review this closeout as receipt-backed command evidence. Confirm the closeout
names the exact command, agent-claim-check verified a pass receipt with matching
evidence hashes, and the same receipt was preserved in the run ledger. Flag any
closeout that relies on a command string without verified receipt evidence.
```
