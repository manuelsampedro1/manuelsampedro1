# Proof Packet Backed Review Findings

Use this pattern when review findings should carry structured proof-packet
evidence without weakening the finding-quality gate.

## Problem

Review findings get weaker when proof evidence is treated as a blanket pass:

- a packet can describe a different diff;
- a packet can be incomplete while findings look ready;
- broad green checks can hide missing file lines, impact, or fix paths;
- reviewers need to separate evidence that checks ran from the quality of each
  comment.

## Pattern

Generate a proof packet from the same diff:

```sh
PYTHONPATH=/path/to/agent-proof-packet/src \
  python3 -m agent_proof_packet /tmp/change.diff \
  --title "Review-finding evidence" \
  --receipt /tmp/run-evidence/command-receipt.json \
  --receipt-base-dir /tmp/run-evidence \
  --format json \
  > /tmp/proof-packet.json
```

Audit review findings with packet evidence:

```sh
PYTHONPATH=/path/to/agent-review-finding-check/src \
  python3 -m agent_review_finding_check /tmp/review-findings.md \
  --diff /tmp/change.diff \
  --proof-packet /tmp/proof-packet.json \
  --min-score 90 \
  --fail-on medium
```

## Acceptance Criteria

- The proof packet uses `agent-proof-packet.v1`.
- The proof packet verdict is `complete`.
- The proof packet has at least one passing check.
- The proof packet has changed-file evidence and no missing evidence.
- The proof packet changed-file list matches the provided diff.
- Passing checks are shown beside findings that reference matching files.
- The finding audit still flags missing severity, missing location, missing
  impact, missing action, vague language, and outside-diff references.

## Review Rule

Use `--proof-packet` to attach evidence to review findings, not to approve weak
comments. If the packet is incomplete, invalid, missing evidence, failing, or
mismatched with the diff, treat the finding report as not ready for reuse.
