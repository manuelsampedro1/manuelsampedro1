# Strict Command Receipt Verification

Use this pattern when a command receipt is going to support a closeout, ledger
entry, review packet, or claim-check result.

## Problem

A receipt can be structurally valid while still being too weak for a passing
claim:

- its evidence hashes match, but the receipt status is `fail`;
- its status is `skipped` or `unknown`;
- it records zero evidence files;
- it verifies integrity but does not meet the proof threshold for reuse.

## Pattern

Create the receipt from command output:

```sh
PYTHONPATH=src python3 -m agent_command_receipt create \
  --command "make test" \
  --status pass \
  --exit-code 0 \
  --base-dir . \
  --evidence /tmp/test-output.log \
  --output /tmp/command-receipt.json
```

Verify both integrity and claim strength:

```sh
PYTHONPATH=src python3 -m agent_command_receipt verify \
  /tmp/command-receipt.json \
  --base-dir . \
  --require-status pass \
  --min-evidence 1 \
  --format json
```

Then pass the same receipt to downstream tools:

```sh
PYTHONPATH=/path/to/agent-claim-check/src \
  python3 -m agent_claim_check closeout.md \
  --diff /tmp/agent-change.diff \
  --receipt /tmp/command-receipt.json \
  --receipt-base-dir .
```

## Acceptance Criteria

- The receipt uses `agent-command-receipt.v1`.
- `verify` exits `0` with `--require-status pass`.
- `verify` exits `0` with `--min-evidence 1` or a stricter project-specific
  threshold.
- The verification report records `receipt_status` and the applied
  `requirements`.
- Failed, skipped, unknown, empty, missing, or drifted receipts do not support a
  passing closeout claim.

## Review Rule

For important command evidence, do not stop at hash integrity. Require the
receipt status and minimum evidence count that match the claim being reused.
