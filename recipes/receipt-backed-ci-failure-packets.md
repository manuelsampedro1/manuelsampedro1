# Receipt-Backed CI Failure Packets

Use this pattern when a retry handoff should prove that the CI failure log came
from a specific failed command and has not drifted.

## Problem

CI retry context gets weaker when logs are copied as plain text:

- the pasted log can belong to a different command;
- a passing command can be treated as a failure source;
- evidence files can change after the retry packet is written;
- the next agent may debug from a stale error signature.

## Pattern

Record the failed command with hashed evidence:

```sh
PYTHONPATH=/path/to/agent-command-receipt/src \
  python3 -m agent_command_receipt create \
  --command "make test" \
  --status fail \
  --exit-code 1 \
  --evidence /tmp/ci-failure.log \
  --output /tmp/failed-command-receipt.json
```

Build the CI failure packet from the receipt:

```sh
PYTHONPATH=/path/to/agent-ci-failure-packet/src \
  python3 -m agent_ci_failure_packet \
  --receipt /tmp/failed-command-receipt.json \
  --receipt-base-dir /tmp \
  --title "CI failure after agent change"
```

## Acceptance Criteria

- The receipt uses `agent-command-receipt.v1`.
- The receipt status is `fail`.
- At least one receipt evidence file exists and is non-empty.
- Each evidence file size matches the receipt.
- Each evidence file SHA-256 hash matches the receipt.
- The packet includes the failing command, error signals, referenced files,
  summaries, suggested checks, and a scoped next-agent prompt.
- If receipt evidence drifts, the packet command fails before producing retry
  context.

## Review Rule

Use `--receipt` for CI retry packets when the failure evidence is important
enough to preserve. If the receipt is missing, passing, empty, or drifted, do
not ask another agent to debug from it until the failed command is captured
again.
