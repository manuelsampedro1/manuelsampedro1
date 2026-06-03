# Structured Output Check Chain

Use this chain when a JSON result from an agent workflow will be reused by
another system.

## Scenario

An agent emits `status: pass` and `score: 100`, then a ledger or proof packet
plans to trust that output. Before reuse, the output should expose which checks
passed and whether any check contradicts the overall outcome.

## Command Chain

Run the output contract with structured checks required:

```sh
agent-output-contract check output.json \
  --require-checks \
  --format json \
  > /tmp/output-contract.json
```

Inspect the check count and issues:

```sh
python3 - <<'PY'
import json
from pathlib import Path

report = json.loads(Path("/tmp/output-contract.json").read_text())
print(report["files"][0]["check_count"])
print(report["issues"])
PY
```

If `check_count` is zero or the report says a passing output includes a
non-passing check, stop before importing the output into a ledger, review
packet, or profile proof artifact.

## Expected Signals

- `check_count` shows how many structured checks were present.
- Missing or empty checks fail when `--require-checks` is used.
- Non-object check entries fail the strict gate.
- Passing outputs cannot carry failed, blocked, partial, or needs-review checks.

## Reviewer Interpretation

This chain proves the JSON output has an inspectable check surface. It does not
prove the underlying commands actually ran; pair it with receipts, CI URLs, or
proof packets when the output makes concrete verification claims.
