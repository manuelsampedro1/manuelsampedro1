# Command Receipt Proof Packet Chain

Use this example when a reviewer needs one review packet that includes both the
diff and verified command evidence.

## Scenario

A coding agent changed release-sensitive files and produced command output in a
temporary evidence directory. The reviewer wants a packet that blocks if the
command receipt is failed, skipped, missing, or drifted.

## Command Chain

Create the receipt from the command output:

```sh
PYTHONPATH=/path/to/agent-command-receipt/src \
  python3 -m agent_command_receipt create \
  --command "make test" \
  --status pass \
  --exit-code 0 \
  --base-dir /tmp/run-evidence \
  --evidence test-output.log \
  --output /tmp/run-evidence/command-receipt.json
```

Generate the review packet:

```sh
PYTHONPATH=/path/to/agent-proof-packet/src \
  python3 -m agent_proof_packet /tmp/change.diff \
  --title "Receipt-backed agent change" \
  --receipt /tmp/run-evidence/command-receipt.json \
  --receipt-base-dir /tmp/run-evidence
```

Preserve the same receipt in the run ledger:

```sh
node /path/to/agent-run-ledger/bin/agent-run-ledger.js import-receipt \
  --ledger /tmp/agent-run-ledger.jsonl \
  --receipt /tmp/run-evidence/command-receipt.json \
  --base-dir /tmp/run-evidence
```

## Expected Signals

- `agent-proof-packet` renders a `Command Receipts` section.
- A verified pass receipt becomes a passing check in the packet.
- A failed, skipped, missing, empty, or drifted receipt blocks the packet.
- `agent-run-ledger` stores the same receipt for later review.

## Reviewer Interpretation

This chain keeps the review packet from becoming a prose-only summary. The
packet can still be read quickly, but command evidence remains tied to hashed
output that downstream tools can verify again.
