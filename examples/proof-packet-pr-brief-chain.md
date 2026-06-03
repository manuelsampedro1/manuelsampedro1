# Proof Packet PR Brief Chain

Use this example when a reviewer wants to confirm that a PR description, diff,
and proof packet all describe the same work.

## Scenario

A coding agent prepares a PR description after running local verification and
generating a proof packet. Before posting the description, the reviewer wants to
avoid stale packet evidence and weak verification claims.

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
  --title "PR verification evidence" \
  --receipt /tmp/run-evidence/command-receipt.json \
  --receipt-base-dir /tmp/run-evidence \
  --format json \
  > /tmp/proof-packet.json
```

Audit the PR description:

```sh
PYTHONPATH=/path/to/agent-pr-brief/src \
  python3 -m agent_pr_brief /tmp/pr-description.md \
  --diff /tmp/change.diff \
  --proof-packet /tmp/proof-packet.json \
  --min-score 90
```

## Expected Signals

- `agent-pr-brief` reports the proof packet count and packet status.
- Passing proof-packet checks can support verification-shaped PR claims.
- The audit blocks if the proof packet is not `complete`.
- The audit blocks if proof-packet changed files differ from the provided diff.
- The PR description still needs risks and follow-up notes; the packet does not
  replace reviewer context.

## Reviewer Interpretation

This chain prevents a PR body from borrowing stale proof. The same diff must be
represented in the proof packet before the PR-description audit accepts packet
evidence.
