# Receipt-Backed CI Failure Chain

Use this example when a reviewer wants a failed CI retry packet tied to hashed
command evidence instead of a loose pasted log.

## Scenario

A coding agent pushes a small CLI change. CI fails on `make test`, and the next
agent needs enough context to fix the failure without guessing from a noisy job
page.

## Command Chain

Save the failed CI output:

```sh
gh run view --log-failed > /tmp/ci-failure.log
```

Create a failed command receipt:

```sh
PYTHONPATH=/path/to/agent-command-receipt/src \
  python3 -m agent_command_receipt create \
  --command "make test" \
  --status fail \
  --exit-code 1 \
  --evidence /tmp/ci-failure.log \
  --output /tmp/failed-command-receipt.json
```

Build the retry packet from the verified receipt:

```sh
PYTHONPATH=/path/to/agent-ci-failure-packet/src \
  python3 -m agent_ci_failure_packet \
  --receipt /tmp/failed-command-receipt.json \
  --receipt-base-dir /tmp \
  --title "CI failure after agent change" \
  --format json \
  > /tmp/ci-failure-packet.json
```

## Expected Signals

- The receipt status must be `fail`.
- The evidence file must exist, be non-empty, and match the stored size and
  SHA-256 hash.
- The packet includes the receipt path, receipt status, exit code, and verified
  evidence files.
- The packet still extracts failing commands, error signals, referenced files,
  test summaries, and suggested checks.
- Missing, passing, empty, or drifted receipt evidence blocks packet generation.

## Reviewer Interpretation

This chain makes CI retry context auditable. The next agent gets a focused
packet, and the reviewer can see that the log behind it still matches the
failed command receipt.
