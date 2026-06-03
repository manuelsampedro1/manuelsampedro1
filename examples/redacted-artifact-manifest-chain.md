# Redacted Artifact Manifest Chain

Use this chain when a reviewer asks how a public proof packet was sanitized
without exposing the original source artifact.

## Scenario

A command log contains an authorization header, local workspace path, and
contact detail. The log is useful evidence for a run ledger, but the raw file
should not be attached to a public profile note.

## Command Chain

Create a redacted copy and manifest:

```sh
agent-artifact-redactor /tmp/agent-run-output.txt \
  --write-dir /tmp/public-agent-run \
  --manifest /tmp/public-agent-run/manifest.json \
  --min-score 0
```

Inspect the manifest:

```sh
python3 - <<'PY'
import json
from pathlib import Path

manifest = json.loads(Path("/tmp/public-agent-run/manifest.json").read_text())
print(manifest["schema_version"])
print(manifest["files"][0]["source_sha256"])
print(manifest["files"][0]["redacted_sha256"])
print(manifest["files"][0]["rules"])
PY
```

Attach only:

```text
/tmp/public-agent-run/agent-run-output.txt
/tmp/public-agent-run/manifest.json
```

## Expected Signals

- The redacted artifact replaces configured sensitive patterns with redaction
  markers.
- The manifest carries a source hash and redacted hash.
- The manifest lists the rules that fired without echoing the sensitive value.
- The public note can cite the redaction command and manifest instead of the
  original artifact.

## Reviewer Interpretation

The redacted copy is the shareable artifact. The manifest is the audit receipt
that ties it back to the local source hash and rule summary.
