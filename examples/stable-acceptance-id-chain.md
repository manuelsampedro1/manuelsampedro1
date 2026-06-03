# Stable Acceptance ID Chain

Use this chain when an `AGENT_TASK.md` will be reused by acceptance traces,
review packets, PR briefs, or closeouts.

## Scenario

A task contract has concrete acceptance criteria. Before another artifact
references them, each criterion needs a stable ID that survives reordering and
copying.

## Command Chain

Run the task-contract gate with acceptance IDs required:

```sh
agent-task-contract check AGENT_TASK.md \
  --require-acceptance-ids \
  --format json \
  > /tmp/task-contract.json
```

Inspect the ID surface:

```sh
python3 - <<'PY'
import json
from pathlib import Path

report = json.loads(Path("/tmp/task-contract.json").read_text())
print(report["acceptance_ids_required"])
print(report["acceptance_id_count"], report["acceptance_criteria_count"])
print(report["acceptance_ids"])
PY
```

Stop if any criterion lacks an ID, if IDs are duplicated, or if
`acceptance_id_count` is lower than `acceptance_criteria_count`.

## Expected Signals

- The contract still passes the normal completeness gate.
- `acceptance_ids_required` is `true`.
- Every acceptance criterion has an `AC-N` ID.
- The text report shows `Acceptance ids` for quick scanning.

## Reviewer Interpretation

This chain proves the task contract has a stable criterion surface. It does not
prove implementation or verification. Use acceptance traces, command receipts,
CI evidence, and proof packets for completion claims.
