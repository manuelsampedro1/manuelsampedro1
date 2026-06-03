# Proof Packet Backed PR Briefs

Use this pattern when a pull-request description cites structured proof-packet
evidence and should be checked before posting or review.

## Problem

PR descriptions become weak when proof artifacts are trusted by filename:

- a packet can be incomplete while the PR says verification passed;
- a packet can describe a different diff;
- a successful command claim can lack concrete evidence near the verification
  section;
- reviewers need the PR audit report to show packet status directly.

## Pattern

Generate a proof packet from the same diff:

```sh
PYTHONPATH=/path/to/agent-proof-packet/src \
  python3 -m agent_proof_packet /tmp/change.diff \
  --title "PR verification evidence" \
  --receipt /tmp/run-evidence/command-receipt.json \
  --receipt-base-dir /tmp/run-evidence \
  --format json \
  > /tmp/proof-packet.json
```

Audit the PR description against that diff and packet:

```sh
PYTHONPATH=/path/to/agent-pr-brief/src \
  python3 -m agent_pr_brief /tmp/pr-description.md \
  --diff /tmp/change.diff \
  --proof-packet /tmp/proof-packet.json \
  --min-score 90
```

## Acceptance Criteria

- The PR description includes summary, changes, verification, risks, and
  follow-up sections.
- The proof packet uses `agent-proof-packet.v1`.
- The proof packet verdict is `complete`.
- The proof packet has at least one passing check.
- The proof packet has changed-file evidence and no missing evidence.
- The proof packet changed-file list matches the provided diff.
- Verification-shaped PR claims are backed by nearby evidence or passing
  proof-packet checks.

## Review Rule

Use `--proof-packet` when a PR description relies on structured packet evidence.
If the packet is incomplete, invalid, missing evidence, failing, or mismatched
with the diff, treat the PR description as not ready to post.
