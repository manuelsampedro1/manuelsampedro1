# Proof Packet Backed Plan Traces

Use this pattern when a completed coding-agent plan should be checked against a
structured proof packet before the closeout is accepted.

## Problem

Plan traces can become weak when proof artifacts are outside the trace:

- a plan item can be marked complete while the proof packet is incomplete;
- a proof packet can describe a different diff;
- verification-shaped plan items can rely on unstated command evidence;
- reviewers need the plan report to show packet status instead of trusting a
  link or filename.

## Pattern

Generate a proof packet:

```sh
PYTHONPATH=/path/to/agent-proof-packet/src \
  python3 -m agent_proof_packet /tmp/change.diff \
  --title "Receipt-backed plan evidence" \
  --receipt /tmp/run-evidence/command-receipt.json \
  --receipt-base-dir /tmp/run-evidence \
  --format json \
  > /tmp/proof-packet.json
```

Trace the plan against the same diff and packet:

```sh
PYTHONPATH=/path/to/agent-plan-trace/src \
  python3 -m agent_plan_trace /tmp/plan.md \
  --diff /tmp/change.diff \
  --closeout /tmp/closeout.md \
  --proof-packet /tmp/proof-packet.json \
  --min-score 90 \
  --fail-on high
```

## Acceptance Criteria

- The plan uses explicit completed, pending, in-progress, or blocked statuses.
- The proof packet uses `agent-proof-packet.v1`.
- The proof packet verdict is `complete`.
- The proof packet has at least one passing check.
- The proof packet has changed-file evidence and no missing evidence.
- If a diff is provided, the proof packet changed-file list matches the diff.
- Verification-shaped completed plan items have command evidence or passing
  proof-packet checks.

## Review Rule

Use `--proof-packet` when a completed plan item depends on structured packet
evidence. If the packet is incomplete, invalid, missing evidence, or mismatched
with the diff, treat the plan trace as not ready.
