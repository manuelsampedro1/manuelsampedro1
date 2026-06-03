# Stable Tool Call ID Chain

Use this chain when a saved tool-call transcript is about to support a review
packet, run ledger, regression case, or profile proof note.

## Scenario

An agent run contains captured tool calls. The calls still need schema replay,
but the replay report should also stay traceable to exact transcript entries.

## Command Chain

Run schema replay with stable call ids required:

```sh
agent-tool-call-replay tools.json tool-calls.jsonl \
  --require-call-ids \
  --format json \
  > /tmp/tool-call-replay.json
```

Check the id surface before importing the report:

```sh
python3 - <<'PY'
import json
from pathlib import Path

report = json.loads(Path("/tmp/tool-call-replay.json").read_text())
print(report["call_count"])
print(report["call_id_count"])
print([call["call_id"] for call in report["calls"]])
PY
```

Stop if `call_id_count` is lower than `call_count`, or if the findings include
`missing-call-id` or `duplicate-call-id`.

## Expected Signals

- The replay report still validates current schema compatibility.
- `call_id_count` shows how many calls are traceable.
- Each call summary exposes a stable id.
- Missing or duplicate ids block strict evidence reuse.

## Reviewer Interpretation

This chain proves the replay report can be mapped back to transcript entries.
It does not prove that the tool calls were authorized, executed, or safe. Use
tool-call audit, command receipts, runtime logs, or ledger events for those
claims.
