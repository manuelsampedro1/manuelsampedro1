# Proof Packet Review Map Chain

Use this example when a reviewer wants lane routing and structured proof-packet
evidence in the same report.

## Scenario

A coding agent changes an auth file, a workflow, tests, and public
documentation. The review map should still route the diff through security,
release, automation, tests, application, and product/docs lanes, even if a proof
packet shows checks were run.

## Command Chain

Create a command receipt:

```sh
PYTHONPATH=/path/to/agent-command-receipt/src \
  python3 -m agent_command_receipt record \
  --command "make test && make smoke" \
  --status pass \
  --evidence /tmp/run-evidence/review-map-checks.log \
  --output /tmp/run-evidence/command-receipt.json
```

Package the proof:

```sh
PYTHONPATH=/path/to/agent-proof-packet/src \
  python3 -m agent_proof_packet /tmp/change.diff \
  --title "Review-map evidence" \
  --receipt /tmp/run-evidence/command-receipt.json \
  --receipt-base-dir /tmp/run-evidence \
  --format json \
  > /tmp/proof-packet.json
```

Map review lanes with evidence:

```sh
PYTHONPATH=/path/to/agent-review-map/src \
  python3 -m agent_review_map /tmp/change.diff \
  --proof-packet /tmp/proof-packet.json \
  --format json
```

## Expected Signals

- Review lanes and handoff order still come from the diff.
- The proof packet must be complete and match the diff.
- Passing packet checks appear beside matching lane files.
- Security, release, automation, test, application, and docs lanes remain
  visible when their files are touched.
- Packet evidence does not change owners or remove reviewer questions.

## Reviewer Interpretation

This chain prevents proof packets from becoming generic review approval. The
report keeps lane ownership visible and uses packet evidence only to show which
checks can already be inspected.
