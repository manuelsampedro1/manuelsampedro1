# Receipt-Backed Retry Guard

Use this pattern when repeated command failures should be checked from verified
receipts instead of copied transcript text.

## Problem

Retry-loop review is weak when failure evidence is loose:

- the same error can be pasted from an older run;
- a passing command can be treated as a failed retry;
- evidence files can change after the retry report is generated;
- the next agent can continue a blind loop without proving what actually
  failed.

## Pattern

Record each failed command with hashed evidence:

```sh
PYTHONPATH=/path/to/agent-command-receipt/src \
  python3 -m agent_command_receipt create \
  --command "make test" \
  --status fail \
  --exit-code 2 \
  --evidence /tmp/run-1/test-output.log \
  --output /tmp/run-1/failed-command-receipt.json
```

Run the retry guard across the failed receipts:

```sh
PYTHONPATH=/path/to/agent-retry-guard/src \
  python3 -m agent_retry_guard \
  --receipt /tmp/run-1/failed-command-receipt.json \
  --receipt /tmp/run-2/failed-command-receipt.json \
  --receipt-base-dir /tmp \
  --fail-on high
```

## Acceptance Criteria

- Each receipt uses `agent-command-receipt.v1`.
- Each receipt status is `fail`.
- Each receipt has at least one non-empty evidence file.
- Each evidence file size matches the receipt.
- Each evidence file SHA-256 hash matches the receipt.
- The retry report includes receipt paths next to failed events.
- Repeated failed commands with the same error signature are blocked unless
  there is a clear strategy-shift signal.

## Review Rule

Use `--receipt` when retry-loop evidence spans multiple command runs or agent
turns. If any receipt is missing, passing, empty, or drifted, regenerate the
command evidence before asking another agent to continue.
