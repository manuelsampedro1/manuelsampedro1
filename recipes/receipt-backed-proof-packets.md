# Receipt-Backed Proof Packets

Use this pattern when a coding-agent review packet needs to include command
evidence that was verified rather than copied from a final answer.

## Problem

Review packets can still become weak if they package unchecked command claims:

- a command line can be copied correctly while the output changed;
- a receipt can exist but record a failed or skipped command;
- evidence files can be missing after a cleanup step;
- reviewers need one artifact that shows both the diff and command evidence.

## Pattern

Create a command receipt:

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

Generate a proof packet with the verified receipt:

```sh
PYTHONPATH=/path/to/agent-proof-packet/src \
  python3 -m agent_proof_packet /tmp/change.diff \
  --title "Receipt-backed agent change" \
  --receipt /tmp/run-evidence/command-receipt.json \
  --receipt-base-dir /tmp/run-evidence
```

Optionally keep the same receipt in the run ledger:

```sh
node /path/to/agent-run-ledger/bin/agent-run-ledger.js import-receipt \
  --ledger /tmp/agent-run-ledger.jsonl \
  --receipt /tmp/run-evidence/command-receipt.json \
  --base-dir /tmp/run-evidence
```

## Acceptance Criteria

- The proof packet includes the changed files from the diff.
- The receipt uses `agent-command-receipt.v1`.
- The receipt status is `pass`.
- At least one receipt evidence file verifies by size and SHA-256 hash.
- Failed, skipped, missing, empty, or drifted receipts make the packet
  `blocked` instead of `complete`.

## Review Rule

If a proof packet claims a command passed, prefer `--receipt` over a manual
`--check` string. The packet should verify the receipt before presenting the
command as passing evidence.
