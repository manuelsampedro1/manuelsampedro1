# Proof Packet Backed Diff Splits

Use this pattern when an oversized coding-agent diff needs both a reviewable
split plan and structured proof-packet evidence for the same changed files.

## Problem

Split plans get weaker when proof is treated as permission to keep reviewing a
broad diff:

- a proof packet can describe a different diff;
- a packet can be incomplete while the split plan looks reusable;
- passing checks can be mistaken for permission to review risky lanes together;
- reviewers need to distinguish checks already run from the order in which
  slices should be reviewed.

## Pattern

Generate a proof packet from the same diff:

```sh
PYTHONPATH=/path/to/agent-proof-packet/src \
  python3 -m agent_proof_packet /tmp/change.diff \
  --title "Diff-split evidence" \
  --receipt /tmp/run-evidence/command-receipt.json \
  --receipt-base-dir /tmp/run-evidence \
  --format json \
  > /tmp/proof-packet.json
```

Generate the split plan with packet evidence:

```sh
PYTHONPATH=/path/to/agent-diff-splitter/src \
  python3 -m agent_diff_splitter /tmp/change.diff \
  --max-files-per-split 3 \
  --proof-packet /tmp/proof-packet.json \
  --format json
```

## Acceptance Criteria

- The proof packet uses `agent-proof-packet.v1`.
- The proof packet verdict is `complete`.
- The proof packet has at least one passing check.
- The proof packet has changed-file evidence and no missing evidence.
- The proof packet changed-file list matches the provided diff.
- Passing checks are shown beside matching split files.
- Security, data, release, and automation lanes remain ahead of lower-risk
  application or product-docs splits.
- Invalid or diff-mismatched packets return a non-zero exit.

## Review Rule

Use `--proof-packet` to attach evidence to split files, not to change the split
strategy. If the packet is incomplete, invalid, missing evidence, failing, or
mismatched with the diff, treat the split plan as not ready for reuse.
