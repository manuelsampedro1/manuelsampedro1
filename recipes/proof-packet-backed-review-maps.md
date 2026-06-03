# Proof Packet Backed Review Maps

Use this pattern when a mixed coding-agent diff needs both review-lane routing
and structured proof-packet evidence in the same report.

## Problem

Review routing gets weaker when proof evidence sits outside the map:

- a proof packet can describe a different diff;
- a packet can be incomplete while the review map looks reusable;
- broad green checks can be mistaken for complete review coverage;
- reviewers need to distinguish lane ownership from checks already run.

## Pattern

Generate a proof packet from the same diff:

```sh
PYTHONPATH=/path/to/agent-proof-packet/src \
  python3 -m agent_proof_packet /tmp/change.diff \
  --title "Review-map evidence" \
  --receipt /tmp/run-evidence/command-receipt.json \
  --receipt-base-dir /tmp/run-evidence \
  --format json \
  > /tmp/proof-packet.json
```

Build the review map with packet evidence:

```sh
PYTHONPATH=/path/to/agent-review-map/src \
  python3 -m agent_review_map /tmp/change.diff \
  --proof-packet /tmp/proof-packet.json \
  --format json
```

## Acceptance Criteria

- The proof packet uses `agent-proof-packet.v1`.
- The proof packet verdict is `complete`.
- The proof packet has at least one passing check.
- The proof packet has changed-file evidence and no missing evidence.
- The proof packet changed-file list matches the provided diff.
- Passing checks are shown beside matching lane files.
- Lanes, owners, reviewer questions, and handoff order still come from the diff.

## Review Rule

Use `--proof-packet` to attach evidence to review lanes, not to replace review
routing. If the packet is incomplete, invalid, missing evidence, failing, or
mismatched with the diff, treat the review map as not ready for reuse.
