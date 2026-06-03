# Proof Packet Acceptance Trace Chain

Use this example when a reviewer wants to confirm that task criteria, diff,
closeout, and proof packet describe the same work.

## Scenario

A coding agent finishes a task, writes a closeout, and generates a proof packet.
Before accepting the final answer, the reviewer wants a criterion-by-criterion
trace that also validates the packet.

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
  --title "Acceptance evidence" \
  --receipt /tmp/run-evidence/command-receipt.json \
  --receipt-base-dir /tmp/run-evidence \
  --format json \
  > /tmp/proof-packet.json
```

Trace acceptance:

```sh
PYTHONPATH=/path/to/agent-acceptance-trace/src \
  python3 -m agent_acceptance_trace /tmp/task-contract.md \
  --diff /tmp/change.diff \
  --evidence /tmp/closeout.md \
  --proof-packet /tmp/proof-packet.json \
  --min-covered 90 \
  --strict
```

## Expected Signals

- `agent-acceptance-trace` reports proof-packet status in Markdown and JSON.
- Passing proof-packet checks can contribute criterion evidence.
- The CLI fails if the proof packet is not `complete`.
- The CLI fails if proof-packet changed files differ from the provided diff.
- Criteria remain visible as covered, partial, or missing; the packet does not
  replace criterion-level review.

## Reviewer Interpretation

This chain prevents acceptance criteria from being approved by stale proof. The
same diff must be represented in the proof packet before the acceptance trace
uses packet checks as evidence.
