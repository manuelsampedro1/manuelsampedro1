# Verified Command Receipts for Closeout Claims

Use this pattern when a coding-agent closeout claims a command passed and that
claim should be checked against evidence, not trust.

## Problem

Closeouts often include exact commands but weak proof:

- the final answer says `make test`,
- the reviewer cannot inspect the original output,
- a manually supplied `--ran-command` string can be copied incorrectly,
- stale evidence can survive after output files change.

## Pattern

Create a receipt for the command output:

```sh
python3 -m agent_command_receipt create \
  --command "PYTHONPATH=src python3 -m unittest discover -s tests" \
  --status pass \
  --exit-code 0 \
  --base-dir . \
  --evidence /tmp/test-output.log \
  --output /tmp/command-receipt.json
```

Check the closeout with the receipt:

```sh
PYTHONPATH=src python3 -m agent_claim_check closeout.md \
  --diff /tmp/agent-change.diff \
  --receipt /tmp/command-receipt.json \
  --receipt-base-dir .
```

Optionally preserve the same receipt in a run ledger:

```sh
node /path/to/agent-run-ledger/bin/agent-run-ledger.js import-receipt \
  --ledger /tmp/agent-run-ledger.jsonl \
  --receipt /tmp/command-receipt.json \
  --base-dir .
```

## Acceptance Criteria

- The closeout includes the exact command it is claiming.
- The receipt uses `agent-command-receipt.v1`.
- Receipt evidence files exist and match their recorded sizes and SHA-256
  hashes.
- Only pass receipts satisfy command evidence for the claim checker.
- Missing, drifted, empty, failed, skipped, or unknown receipts block the
  closeout instead of silently supporting it.

## Review Rule

For important verification claims, prefer a verified receipt over a manually
repeated command string. If the receipt does not verify, the closeout claim is
not supported.
