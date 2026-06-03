# Proof Packet Scope Guard Chain

Use this example when a reviewer wants both path-scope enforcement and
structured proof-packet evidence for the same coding-agent diff.

## Scenario

A coding agent is asked to edit `src/billing/**` and `tests/billing/**`, but
the diff also touches `docs/roadmap.md`. Tests may pass, but the extra path
still needs a deliberate scope decision.

## Command Chain

Create a command receipt:

```sh
PYTHONPATH=/path/to/agent-command-receipt/src \
  python3 -m agent_command_receipt record \
  --command "make test && make smoke" \
  --status pass \
  --evidence /tmp/run-evidence/scope-checks.log \
  --output /tmp/run-evidence/command-receipt.json
```

Package the proof:

```sh
PYTHONPATH=/path/to/agent-proof-packet/src \
  python3 -m agent_proof_packet /tmp/change.diff \
  --title "Scope evidence" \
  --receipt /tmp/run-evidence/command-receipt.json \
  --receipt-base-dir /tmp/run-evidence \
  --format json \
  > /tmp/proof-packet.json
```

Run the scope gate:

```sh
PYTHONPATH=/path/to/agent-scope-guard/src \
  python3 -m agent_scope_guard /tmp/change.diff \
  --allow "src/billing/**" \
  --allow "tests/billing/**" \
  --proof-packet /tmp/proof-packet.json \
  --format json
```

## Expected Signals

- The proof packet must be complete and match the diff.
- Passing packet checks appear in the scope report.
- Any path outside the allowlist remains in `unexpected_paths`.
- Invalid or diff-mismatched packets make the command fail.

## Reviewer Interpretation

This chain prevents passing checks from becoming silent scope expansion. The
packet shows what was checked; the allowlist decides whether the changed paths
belong to the task.
