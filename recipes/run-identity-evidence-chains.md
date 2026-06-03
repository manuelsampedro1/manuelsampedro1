# Run Identity Evidence Chains

Use this pattern when JSON artifacts from one coding-agent run will be combined
into a review packet, verification envelope, run ledger, closeout, or profile
proof note.

## Problem

The same task, repository, and commit can still represent separate reruns. If
artifacts from those reruns are mixed, the final proof chain can look coherent
while actually combining different agent executions.

## Pattern

Require a shared run identity before reusing the artifacts:

```sh
agent-evidence-chain check \
  review-packet.json \
  verification-envelope.json \
  ledger-summary.json \
  --require-task-id \
  --require-run-id \
  --format json \
  > /tmp/evidence-chain.json
```

Accepted run-id fields are:

- `run_id`;
- `runId`;
- `agent_run_id`;
- `execution_id`;
- `session_id`;
- `run`.

Treat these as blockers:

- any artifact missing run identity when `--require-run-id` is active;
- any mismatched run identity across the chain;
- nonpassing outcomes unless the reuse case intentionally allows nonpassing
  artifacts;
- populated blocker lists such as `blocking_findings`, `blockers`, or
  `missing_evidence`.

## Acceptance Criteria

- `shared_identity.run_id` is present in JSON output.
- Every artifact summary exposes the same run id.
- Task, repository, and commit identity still match.
- No issues remain before the chain feeds a ledger, closeout, or public proof
  note.

## Review Rule

Run identity proves the artifacts belong to the same agent run. It does not
prove the commands executed, the outputs were authorized, or the artifacts are
complete. Use command receipts, runtime logs, ledger events, and approval
audits for those claims.
