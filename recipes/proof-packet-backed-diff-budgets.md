# Proof Packet Backed Diff Budgets

Use this pattern when a coding-agent diff needs both a strict size/risk budget
and structured proof-packet evidence in the same report.

## Problem

Diff budgets get weaker when evidence is treated as a waiver:

- a proof packet can describe a different diff;
- a packet can be incomplete while the budget report looks reusable;
- passing tests can be mistaken for permission to review too much at once;
- reviewers need to distinguish checks already run from whether the diff should
  be split.

## Pattern

Generate a proof packet from the same diff:

```sh
PYTHONPATH=/path/to/agent-proof-packet/src \
  python3 -m agent_proof_packet /tmp/change.diff \
  --title "Diff-budget evidence" \
  --receipt /tmp/run-evidence/command-receipt.json \
  --receipt-base-dir /tmp/run-evidence \
  --format json \
  > /tmp/proof-packet.json
```

Run the budget gate with packet evidence:

```sh
PYTHONPATH=/path/to/agent-diff-budget/src \
  python3 -m agent_diff_budget /tmp/change.diff \
  --max-files 6 \
  --max-total 350 \
  --max-high-risk-files 2 \
  --proof-packet /tmp/proof-packet.json \
  --format json
```

## Acceptance Criteria

- The proof packet uses `agent-proof-packet.v1`.
- The proof packet verdict is `complete`.
- The proof packet has at least one passing check.
- The proof packet has changed-file evidence and no missing evidence.
- The proof packet changed-file list matches the provided diff.
- Passing checks are shown beside matching changed files.
- Budget failures remain visible and still produce a non-zero exit.

## Review Rule

Use `--proof-packet` to attach evidence to changed files, not to waive the
budget. If the packet is incomplete, invalid, missing evidence, failing, or
mismatched with the diff, treat the budget report as not ready for reuse.
