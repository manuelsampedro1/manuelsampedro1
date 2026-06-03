# Proof Packet Change Risk Chain

Use this example when a reviewer wants risk routing and structured proof-packet
gate evidence in the same report.

## Scenario

A coding agent changes a deploy workflow, a migration, and an auth file. The
risk report should still classify the diff as high risk, but it should also show
which recommended gates already have packet-backed checks.

## Command Chain

Create a command receipt:

```sh
PYTHONPATH=/path/to/agent-command-receipt/src \
  python3 -m agent_command_receipt record \
  --command "make test && make smoke" \
  --status pass \
  --evidence /tmp/run-evidence/check-output.log \
  --output /tmp/run-evidence/command-receipt.json
```

Package the proof:

```sh
PYTHONPATH=/path/to/agent-proof-packet/src \
  python3 -m agent_proof_packet /tmp/change.diff \
  --title "Risk gate evidence" \
  --receipt /tmp/run-evidence/command-receipt.json \
  --receipt-base-dir /tmp/run-evidence \
  --format json \
  > /tmp/proof-packet.json
```

Classify risk and map gate evidence:

```sh
PYTHONPATH=/path/to/agent-change-risk/src \
  python3 -m agent_change_risk /tmp/change.diff \
  --title "Deploy auth migration" \
  --proof-packet /tmp/proof-packet.json
```

## Expected Signals

- Risk tags and required gates still come from the diff.
- The proof packet must be complete and match the diff.
- Passing packet checks can mark matching gates as `evidence-found`.
- Missing gate checks remain `evidence-missing`.
- Packet evidence does not lower risk level or remove reviewer questions.

## Reviewer Interpretation

This chain prevents proof packets from becoming a vague pass stamp. The report
keeps the risk classification intact and uses the packet only to make gate
evidence easier to inspect.
