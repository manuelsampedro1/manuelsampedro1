# Proof Packet Backed Merge Readiness

Use this pattern when a merge gate should consume a review packet, but only if
that packet still matches the current diff.

## Problem

Review packets make evidence easier to inspect, but they can drift:

- the packet can be `blocked` or `needs-review`;
- the packet can describe a previous diff;
- checks can be copied into merge readiness without proving their source;
- reviewers need the merge gate to fail closed when packet evidence is stale.

## Pattern

Generate a proof packet:

```sh
PYTHONPATH=/path/to/agent-proof-packet/src \
  python3 -m agent_proof_packet /tmp/change.diff \
  --title "Receipt-backed agent change" \
  --receipt /tmp/run-evidence/command-receipt.json \
  --receipt-base-dir /tmp/run-evidence \
  --format json \
  > /tmp/proof-packet.json
```

Gate merge readiness against the same diff:

```sh
PYTHONPATH=/path/to/agent-merge-readiness/src \
  python3 -m agent_merge_readiness /tmp/change.diff \
  --title "Receipt-backed agent change" \
  --proof-packet /tmp/proof-packet.json \
  --closeout /tmp/closeout.md
```

## Acceptance Criteria

- The proof packet uses `agent-proof-packet.v1`.
- The proof packet verdict is `complete`.
- The proof packet changed-file list matches the current diff.
- Imported proof-packet checks satisfy the required merge-readiness gates.
- Blocked, needs-review, invalid, or diff-mismatched proof packets block the
  merge verdict.

## Review Rule

Use proof packets as merge evidence only when the merge gate validates both
packet verdict and diff alignment. If either fails, treat the merge as blocked.
