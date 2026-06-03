# Concrete Source Memory Audit Chain

Use this chain when an agent memory file contains current-state claims that may
influence a new run.

## Scenario

A memory file says a browser session is currently authenticated. It also says
`Sources: manual note.` The next agent needs to know whether that claim has a
reusable evidence pointer before trusting it.

## Command Chain

Run the audit with a medium gate:

```sh
agent-memory-audit memory.md \
  --today 2026-06-03 \
  --fail-on medium \
  --format json \
  > /tmp/memory-audit.json
```

Inspect source findings and concrete source counts:

```sh
python3 - <<'PY'
import json
from pathlib import Path

report = json.loads(Path("/tmp/memory-audit.json").read_text())
print(report["files"][0]["concrete_source_mentions"])
print([finding["rule"] for finding in report["findings"]])
PY
```

If the report includes `weak-source-evidence`, replace the vague source text
with an inspectable pointer such as a log path, command receipt, CI run, report,
URL, or commit.

## Expected Signals

- `unsourced-current-claim` means no source marker is close enough.
- `weak-source-evidence` means source language exists but lacks concrete
  evidence.
- `concrete_source_mentions` shows how many source lines point at inspectable
  artifacts.
- Source evidence stays bound to the same Markdown paragraph or list item.

## Reviewer Interpretation

This chain proves the memory was checked for reusable source pointers. It does
not prove the memory claim is still true; it tells reviewers what to open before
the claim influences another run.
