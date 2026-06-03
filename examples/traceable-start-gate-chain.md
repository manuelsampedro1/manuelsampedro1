# Traceable Start Gate Chain

Use this chain when a start packet will be reused by another agent, imported
into a run ledger, or referenced in a review packet.

## Scenario

A start packet names objective, scope, worktree state, context, verification,
and stop conditions. The remaining question is whether its `pass` evidence can
be inspected later.

## Command Chain

Run the start gate with evidence pointers required:

```sh
agent-start-gate check AGENT_START.md \
  --require-evidence-pointers \
  --format json \
  > /tmp/start-gate.json
```

Inspect the pointer surface before handoff:

```sh
python3 - <<'PY'
import json
from pathlib import Path

report = json.loads(Path("/tmp/start-gate.json").read_text())
print(report["evidence_pointer_required"])
print(report["evidence_pointer_count"])
print([(item["name"], item["has_pointer"]) for item in report["evidence"]])
PY
```

Stop if the report includes `Ready evidence lacks a concrete pointer` or if
the pointer count does not cover the ready task, repo, and context evidence.

## Expected Signals

- The packet still passes the normal start gate.
- `evidence_pointer_required` is `true`.
- Ready task, repo, and context evidence each expose `has_pointer: true`.
- The text report shows an `Evidence pointers` count for quick scanning.

## Reviewer Interpretation

This chain proves the start packet can be inspected before the first edit. It
does not prove the referenced commands ran, the artifacts are complete, or the
later agent stayed inside scope. Use receipts, ledgers, proof packets, and
worktree guards for those claims.
