# Proof Packet Backed Change Risk

Use this pattern when a change-risk report should show which recommended review
gates already have structured proof-packet evidence.

## Problem

Risk routing gets weaker when gate evidence lives in a separate artifact:

- a proof packet can describe a different diff;
- a packet can be incomplete while the risk report still looks confident;
- broad passing checks can be mistaken for lower risk;
- reviewers need to distinguish gates with evidence from gates still pending.

## Pattern

Generate a proof packet from the same diff:

```sh
PYTHONPATH=/path/to/agent-proof-packet/src \
  python3 -m agent_proof_packet /tmp/change.diff \
  --title "Gate evidence" \
  --receipt /tmp/run-evidence/command-receipt.json \
  --receipt-base-dir /tmp/run-evidence \
  --format json \
  > /tmp/proof-packet.json
```

Run change-risk classification with the packet:

```sh
PYTHONPATH=/path/to/agent-change-risk/src \
  python3 -m agent_change_risk /tmp/change.diff \
  --title "Risk gate routing" \
  --proof-packet /tmp/proof-packet.json
```

## Acceptance Criteria

- The proof packet uses `agent-proof-packet.v1`.
- The proof packet verdict is `complete`.
- The proof packet has at least one passing check.
- The proof packet has changed-file evidence and no missing evidence.
- The proof packet changed-file list matches the provided diff.
- Gate evidence is mapped by passing check names, not by free-form claims.
- The risk level and required gates still come from the diff.

## Review Rule

Use `--proof-packet` to audit gate evidence next to risk classification. If the
packet is incomplete, invalid, missing evidence, failing, or mismatched with the
diff, treat the risk report as not ready for reuse.
