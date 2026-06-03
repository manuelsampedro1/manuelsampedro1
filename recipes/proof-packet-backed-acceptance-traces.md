# Proof Packet Backed Acceptance Traces

Use this pattern when acceptance criteria should be checked against structured
proof-packet evidence before a final answer is accepted.

## Problem

Acceptance traces become weak when proof artifacts are adjacent but unchecked:

- a criterion can look covered while the proof packet is incomplete;
- a packet can describe a different diff;
- verification checks can live outside the trace report;
- reviewers need acceptance status and packet status in one output.

## Pattern

Generate a proof packet from the same diff:

```sh
PYTHONPATH=/path/to/agent-proof-packet/src \
  python3 -m agent_proof_packet /tmp/change.diff \
  --title "Acceptance evidence" \
  --receipt /tmp/run-evidence/command-receipt.json \
  --receipt-base-dir /tmp/run-evidence \
  --format json \
  > /tmp/proof-packet.json
```

Trace acceptance criteria against the diff, closeout, and packet:

```sh
PYTHONPATH=/path/to/agent-acceptance-trace/src \
  python3 -m agent_acceptance_trace /tmp/task-contract.md \
  --diff /tmp/change.diff \
  --evidence /tmp/closeout.md \
  --proof-packet /tmp/proof-packet.json \
  --min-covered 90 \
  --strict
```

## Acceptance Criteria

- The task file has an explicit acceptance criteria section.
- The proof packet uses `agent-proof-packet.v1`.
- The proof packet verdict is `complete`.
- The proof packet has at least one passing check.
- The proof packet has changed-file evidence and no missing evidence.
- The proof packet changed-file list matches the provided diff.
- Each criterion has concrete evidence from the diff, closeout, or verified
  proof-packet checks.

## Review Rule

Use `--proof-packet` when accepting a final answer depends on structured packet
evidence. If the packet is incomplete, invalid, missing evidence, failing, or
mismatched with the diff, treat the acceptance trace as not ready.
