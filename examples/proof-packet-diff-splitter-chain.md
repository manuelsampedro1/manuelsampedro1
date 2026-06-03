# Proof Packet Diff Splitter Chain

Use this example when a reviewer wants an oversized diff split into risk-first
lanes while still seeing structured proof-packet checks for the same files.

## Scenario

A coding agent changes auth code, migrations, release workflow, tests,
application code, and README claims. Checks may have passed, but the mixed
surface still needs review slices instead of one flat pass.

## Command Chain

Create a command receipt:

```sh
PYTHONPATH=/path/to/agent-command-receipt/src \
  python3 -m agent_command_receipt record \
  --command "make test && make smoke" \
  --status pass \
  --evidence /tmp/run-evidence/diff-splitter-checks.log \
  --output /tmp/run-evidence/command-receipt.json
```

Package the proof:

```sh
PYTHONPATH=/path/to/agent-proof-packet/src \
  python3 -m agent_proof_packet /tmp/change.diff \
  --title "Diff-split evidence" \
  --receipt /tmp/run-evidence/command-receipt.json \
  --receipt-base-dir /tmp/run-evidence \
  --format json \
  > /tmp/proof-packet.json
```

Generate the split plan with evidence:

```sh
PYTHONPATH=/path/to/agent-diff-splitter/src \
  python3 -m agent_diff_splitter /tmp/change.diff \
  --max-files-per-split 3 \
  --proof-packet /tmp/proof-packet.json \
  --format json
```

## Expected Signals

- The proof packet must be complete and match the diff.
- Passing packet checks appear beside matching split files.
- Security, data, release, and automation splits stay ahead of application,
  tests, or product-docs review.
- Invalid or diff-mismatched packets make the command fail.

## Reviewer Interpretation

This chain prevents test evidence from flattening review order. The report can
show which checks were performed while still forcing risky lanes to remain
isolated and reviewed in sequence.
