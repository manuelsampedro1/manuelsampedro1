# Run Identity Evidence Chain

Use this chain when a review packet, verification envelope, and ledger summary
share task, repository, and commit identity but may have been produced by
separate reruns.

## Scenario

A coding-agent workflow emits several JSON artifacts. They all point to the
same task and commit, but the reviewer needs to know they came from the same
agent execution before treating them as one proof chain.

## Command Chain

Run the chain check with task and run identity required:

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

Check the shared run before importing the report:

```sh
python3 - <<'PY'
import json
from pathlib import Path

report = json.loads(Path("/tmp/evidence-chain.json").read_text())
print(report["shared_identity"]["run_id"])
print([artifact["run_id"] for artifact in report["artifacts"]])
PY
```

Stop if any artifact is missing `run_id`, if the run ids differ, or if the
report includes `missing-run-id` or `mismatched-run-id`.

## Expected Signals

- The chain still validates shared task, repository, and commit identity.
- `shared_identity.run_id` exposes the run reviewers should compare.
- Each artifact summary exposes the same run id.
- Missing or mismatched run ids block strict evidence reuse.

## Reviewer Interpretation

This chain proves the JSON artifacts belong to the same run identity. It does
not prove command execution, authorization, or completeness. Use command
receipts, tool-call audits, runtime logs, or ledger events for those claims.
