# Proof Packet Backed Test Impact

Use this pattern when a broad proof-packet test pass should be visible in a
test-impact report without pretending it is direct source-level test coverage.

## Problem

Test-impact review becomes weak when broad verification claims sit outside the
diff report:

- a source file can lack nearby changed tests while a proof packet claims tests
  passed;
- a proof packet can describe a different diff;
- a broad `make test` pass can be mistaken for direct test evidence;
- reviewers need test-impact status and packet status in one report.

## Pattern

Generate a proof packet from the same diff:

```sh
PYTHONPATH=/path/to/agent-proof-packet/src \
  python3 -m agent_proof_packet /tmp/change.diff \
  --title "Test impact evidence" \
  --receipt /tmp/run-evidence/command-receipt.json \
  --receipt-base-dir /tmp/run-evidence \
  --format json \
  > /tmp/proof-packet.json
```

Run test-impact review with the packet:

```sh
PYTHONPATH=/path/to/agent-test-impact/src \
  python3 -m agent_test_impact /tmp/change.diff \
  --proof-packet /tmp/proof-packet.json \
  --fail-on-missing \
  --min-score 80
```

## Acceptance Criteria

- The proof packet uses `agent-proof-packet.v1`.
- The proof packet verdict is `complete`.
- The proof packet has at least one passing test-like check.
- The proof packet has changed-file evidence and no missing evidence.
- The proof packet changed-file list matches the provided diff.
- Related changed tests remain the only direct `covered` signal.
- Packet-backed checks can only produce `partial` evidence for changed source
  files.

## Review Rule

Use `--proof-packet` when a test-impact report should account for structured
verification evidence. If the packet is incomplete, invalid, missing evidence,
failing, or mismatched with the diff, treat the test-impact report as not ready.
