# Proof Packet Plan Trace Chain

Use this example when a reviewer wants to confirm that completed plan items are
backed by the same proof packet as the final closeout.

## Scenario

A coding agent marks all plan items complete, produces a proof packet, and writes
a final closeout. Before accepting the handoff, the reviewer wants to verify that
the plan, diff, and packet describe the same work.

## Command Chain

Create a command receipt:

```sh
PYTHONPATH=/path/to/agent-command-receipt/src \
  python3 -m agent_command_receipt record \
  --command "make test" \
  --status pass \
  --evidence /tmp/run-evidence/test-output.log \
  --output /tmp/run-evidence/command-receipt.json
```

Package the proof:

```sh
PYTHONPATH=/path/to/agent-proof-packet/src \
  python3 -m agent_proof_packet /tmp/change.diff \
  --title "Receipt-backed plan evidence" \
  --receipt /tmp/run-evidence/command-receipt.json \
  --receipt-base-dir /tmp/run-evidence \
  --format json \
  > /tmp/proof-packet.json
```

Trace the plan:

```sh
PYTHONPATH=/path/to/agent-plan-trace/src \
  python3 -m agent_plan_trace /tmp/plan.md \
  --diff /tmp/change.diff \
  --closeout /tmp/closeout.md \
  --proof-packet /tmp/proof-packet.json \
  --min-score 90 \
  --fail-on high
```

Preserve the run:

```sh
node /path/to/agent-run-ledger/bin/agent-run-ledger.js import-receipt \
  --ledger /tmp/agent-run-ledger.jsonl \
  --receipt /tmp/run-evidence/command-receipt.json \
  --base-dir /tmp/run-evidence
```

## Expected Signals

- `agent-plan-trace` reports the proof packet count and packet status.
- Completed verification items can be backed by passing proof-packet checks.
- The trace fails if the proof packet is not `complete`.
- The trace fails if proof-packet changed files differ from the provided diff.
- The closeout still remains inspectable as separate final-answer evidence.

## Reviewer Interpretation

This chain prevents completed plan items from becoming unchecked checkboxes. The
same diff must be represented in the proof packet before the plan trace accepts
packet evidence.
