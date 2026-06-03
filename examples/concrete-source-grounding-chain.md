# Concrete Source Grounding Chain

Use this chain when a generated note or JSON claim file will be reused as proof
in a review packet, profile README, lab note, or decision record.

## Scenario

An agent writes a release note that says the change is safe. The artifact also
says `Source: manual review`, but it does not link to a diff, command output,
CI run, report, receipt, or commit.

## Command Chain

Run the grounding check in strict pointer mode:

```sh
agent-source-grounding check release-note.md \
  --require-sources \
  --require-concrete \
  --format json \
  > /tmp/source-grounding.json
```

Inspect pointer counts and issues:

```sh
python3 - <<'PY'
import json
from pathlib import Path

report = json.loads(Path("/tmp/source-grounding.json").read_text())
print(report["artifacts"][0]["concrete_source_count"])
print(report["issues"])
PY
```

If the report says a claim has no concrete source or evidence, add an
inspectable pointer such as a repo path, command log, CI run, review packet,
receipt, report, URL, or commit.

## Expected Signals

- `missing source/evidence section or links` means the artifact is not grounded.
- `no concrete source or evidence` means source-shaped prose exists but is too
  weak for reuse.
- `concrete_source_count` shows how many inspectable pointers were found.
- Placeholder citations remain blocking issues.

## Reviewer Interpretation

This chain proves an artifact was checked for inspectable pointers. It does not
prove the pointed-at evidence supports every claim; that remains the reviewer
step.
