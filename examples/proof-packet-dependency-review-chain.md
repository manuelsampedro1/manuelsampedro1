# Proof Packet Dependency Review Chain

Use this example when a reviewer wants dependency findings and structured proof
evidence in the same report.

## Scenario

A coding agent changes `package.json` and `requirements.txt`. The diff adds a
floating Node dependency, a direct Python URL, and a lifecycle script. A proof
packet may show checks were run, but the dependency findings should remain
visible and severe.

## Command Chain

Create a command receipt:

```sh
PYTHONPATH=/path/to/agent-command-receipt/src \
  python3 -m agent_command_receipt record \
  --command "npm ci && npm audit && pip check" \
  --status pass \
  --evidence /tmp/run-evidence/dependency-checks.log \
  --output /tmp/run-evidence/command-receipt.json
```

Package the proof:

```sh
PYTHONPATH=/path/to/agent-proof-packet/src \
  python3 -m agent_proof_packet /tmp/dependency-change.diff \
  --title "Dependency review evidence" \
  --receipt /tmp/run-evidence/command-receipt.json \
  --receipt-base-dir /tmp/run-evidence \
  --format json \
  > /tmp/proof-packet.json
```

Inspect dependency risk:

```sh
PYTHONPATH=/path/to/agent-dependency-guard/src \
  python3 -m agent_dependency_guard /tmp/dependency-change.diff \
  --proof-packet /tmp/proof-packet.json \
  --fail-on high
```

## Expected Signals

- Dependency findings, score, and severity still come from the diff.
- The proof packet must be complete and match the diff.
- Passing packet checks can mark matching required checks as `evidence-found`.
- Missing dependency checks remain `evidence-missing`.
- Packet evidence does not lower dependency risk or remove findings.

## Reviewer Interpretation

This chain prevents a proof packet from becoming a supply-chain pass stamp. The
report keeps risky dependency changes visible and uses packet evidence only to
show what review checks already happened.
