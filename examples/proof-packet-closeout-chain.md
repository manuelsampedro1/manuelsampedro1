# Proof Packet Closeout Chain

Use this example when a reviewer wants a final answer checked against the proof
packet it cites.

## Scenario

A coding agent changed source and tests, generated command receipts, and wrote a
final closeout. Before that closeout is reused in a PR comment or run ledger,
the reviewer wants to confirm the proof packet is complete and covers the files
named by the final answer.

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
  --title "Receipt-backed closeout" \
  --receipt /tmp/run-evidence/command-receipt.json \
  --receipt-base-dir /tmp/run-evidence \
  --format json \
  > /tmp/proof-packet.json
```

Check the final answer:

```sh
PYTHONPATH=/path/to/agent-closeout-check/src \
  python3 -m agent_closeout_check /tmp/closeout.md \
  --proof-packet /tmp/proof-packet.json
```

Preserve the run:

```sh
node /path/to/agent-run-ledger/bin/agent-run-ledger.js import-receipt \
  --ledger /tmp/agent-run-ledger.jsonl \
  --receipt /tmp/run-evidence/command-receipt.json \
  --base-dir /tmp/run-evidence
```

## Expected Signals

- `agent-closeout-check` passes only if the closeout still includes exact
  verification evidence.
- The proof packet can supply changed-path evidence.
- The closeout fails if the proof packet is not `complete`.
- The closeout fails if cited files are not covered by the proof packet.
- The final output lists proof-packet status so reviewers can inspect the
  evidence chain.

## Reviewer Interpretation

This chain prevents a final answer from treating a proof packet as authority by
default. The closeout remains reviewable only when its own verification section
is concrete and the packet it cites is complete and aligned.
