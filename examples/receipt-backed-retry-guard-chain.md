# Receipt-Backed Retry Guard Chain

Use this example when a reviewer wants to decide whether another agent should
continue after repeated failed commands.

## Scenario

A coding agent runs `make test`, gets the same import error twice, and has not
shown a meaningful investigation step between attempts. The reviewer wants a
machine-checkable stop signal before another retry.

## Command Chain

Create the first failed command receipt:

```sh
PYTHONPATH=/path/to/agent-command-receipt/src \
  python3 -m agent_command_receipt create \
  --command "make test" \
  --status fail \
  --exit-code 2 \
  --evidence /tmp/run-1/test-output.log \
  --output /tmp/run-1/failed-command-receipt.json
```

Create the second failed command receipt:

```sh
PYTHONPATH=/path/to/agent-command-receipt/src \
  python3 -m agent_command_receipt create \
  --command "make test" \
  --status fail \
  --exit-code 2 \
  --evidence /tmp/run-2/test-output.log \
  --output /tmp/run-2/failed-command-receipt.json
```

Run the retry guard:

```sh
PYTHONPATH=/path/to/agent-retry-guard/src \
  python3 -m agent_retry_guard \
  --receipt /tmp/run-1/failed-command-receipt.json \
  --receipt /tmp/run-2/failed-command-receipt.json \
  --receipt-base-dir /tmp \
  --fail-on high
```

## Expected Signals

- Each receipt must have status `fail`.
- Each evidence file must exist, be non-empty, and match the stored size and
  SHA-256 hash.
- The retry guard reports the receipt path for each failed event.
- The same failed command and error signature produce retry-loop findings.
- Missing strategy-shift evidence produces a blocking finding.
- Passing, missing, empty, or drifted receipts fail before retry-loop scoring.

## Reviewer Interpretation

This chain gives the reviewer a concrete stop condition. The next agent should
inspect context or change strategy before running the same command again.
