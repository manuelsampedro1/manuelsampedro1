# Proof Packet Test Impact Chain

Use this example when a reviewer wants broad test evidence from a proof packet
visible inside the same report that maps source changes to test impact.

## Scenario

A coding agent changes one source file with a nearby test and another source
file without a directly changed test. A proof packet shows that broad tests
passed. The reviewer wants the report to keep nearby test coverage separate from
packet-backed broad checks.

## Command Chain

Create a command receipt:

```sh
PYTHONPATH=/path/to/agent-command-receipt/src \
  python3 -m agent_command_receipt record \
  --command "make test" \
  --status pass \
  --evidence /tmp/run-evidence/test-output.log \
  --output /tmp/run-evidence/command-receipt.json
```

Package the proof:

```sh
PYTHONPATH=/path/to/agent-proof-packet/src \
  python3 -m agent_proof_packet /tmp/change.diff \
  --title "Test impact evidence" \
  --receipt /tmp/run-evidence/command-receipt.json \
  --receipt-base-dir /tmp/run-evidence \
  --format json \
  > /tmp/proof-packet.json
```

Inspect test impact:

```sh
PYTHONPATH=/path/to/agent-test-impact/src \
  python3 -m agent_test_impact /tmp/change.diff \
  --proof-packet /tmp/proof-packet.json \
  --fail-on-missing \
  --min-score 80
```

## Expected Signals

- Sources with related changed tests remain `covered`.
- Sources without related changed tests can become packet-backed `partial`.
- Proof packets with incomplete verdicts fail the CLI.
- Proof packets with changed files that differ from the diff fail the CLI.
- The report still shows suggested targeted checks for source files.

## Reviewer Interpretation

This chain prevents broad proof-packet checks from being treated as direct test
coverage. The packet must match the diff, and its checks only provide partial
test-impact evidence unless related tests changed in the same diff.
