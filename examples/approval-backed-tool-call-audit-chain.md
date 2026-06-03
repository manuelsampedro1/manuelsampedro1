# Approval-Backed Tool Call Audit Chain

Use this chain when a reviewer needs to check whether a sensitive tool action
inside an agent run carried explicit approval evidence.

## Scenario

A tool-call log includes a public push and an email send. The final answer says
the work is complete, but the run history must show whether those actions had
approval evidence before the closeout is trusted.

## Command Chain

Run the audit in approval-required mode:

```sh
agent-tool-call-audit /tmp/tool-calls.jsonl \
  --require-approval \
  --fail-on high \
  --format json \
  > /tmp/tool-call-audit.json
```

Inspect the approval counters:

```sh
python3 - <<'PY'
import json
from pathlib import Path

report = json.loads(Path("/tmp/tool-call-audit.json").read_text())
print(report["approval_required_calls"])
print(report["approval_evidence_calls"])
print([finding["rule"] for finding in report["findings"]])
PY
```

If the report includes `missing-approval-evidence`, stop the closeout and add
the matching approval receipt or reviewer note to the run evidence.

## Expected Signals

- Sensitive tool names remain visible even when approval evidence exists.
- Missing approval evidence appears as a high-severity finding.
- `approval_required_calls` counts sensitive external actions.
- `approval_evidence_calls` counts sensitive actions with recognized authority
  evidence.
- The audit output can be attached to a proof packet or run ledger.

## Reviewer Interpretation

This chain proves that the run history was checked for authority evidence. It
does not prove that every sensitive action was correct; it tells reviewers
where to inspect next.
