# Proof Packet Review Finding Chain

Use this example when a reviewer wants actionable review findings and
structured proof-packet evidence in the same report.

## Scenario

A coding agent changes an auth file and a report builder. Review findings should
name exact lines, explain impact, and include a fix path. A proof packet can
show that checks ran for the same files, but it should not hide weak finding
text.

## Command Chain

Create a command receipt:

```sh
PYTHONPATH=/path/to/agent-command-receipt/src \
  python3 -m agent_command_receipt record \
  --command "make test && make smoke" \
  --status pass \
  --evidence /tmp/run-evidence/review-finding-checks.log \
  --output /tmp/run-evidence/command-receipt.json
```

Package the proof:

```sh
PYTHONPATH=/path/to/agent-proof-packet/src \
  python3 -m agent_proof_packet /tmp/change.diff \
  --title "Review-finding evidence" \
  --receipt /tmp/run-evidence/command-receipt.json \
  --receipt-base-dir /tmp/run-evidence \
  --format json \
  > /tmp/proof-packet.json
```

Audit the findings with evidence:

```sh
PYTHONPATH=/path/to/agent-review-finding-check/src \
  python3 -m agent_review_finding_check /tmp/review-findings.md \
  --diff /tmp/change.diff \
  --proof-packet /tmp/proof-packet.json \
  --min-score 90 \
  --fail-on medium \
  --format json
```

## Expected Signals

- The proof packet must be complete and match the diff.
- Passing packet checks appear beside findings that reference matching files.
- Missing severity, missing file lines, missing impact, missing action, vague
  language, and outside-diff references remain visible as issues.
- Invalid or diff-mismatched packets make the command fail.

## Reviewer Interpretation

This chain prevents proof packets from becoming generic review approval. The
report can show which checks were performed while still requiring each finding
to be concrete, actionable, and tied to the reviewed diff.
