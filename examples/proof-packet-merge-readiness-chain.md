# Proof Packet Merge Readiness Chain

Use this example when a reviewer wants to move from a review packet to a merge
gate without trusting stale packet evidence.

## Scenario

A coding agent produced a proof packet for a release-sensitive diff. Before
merge, the reviewer wants to confirm that the packet is complete and still
matches the exact diff being merged.

## Command Chain

Create the proof packet:

```sh
PYTHONPATH=/path/to/agent-proof-packet/src \
  python3 -m agent_proof_packet /tmp/change.diff \
  --title "Receipt-backed release change" \
  --receipt /tmp/run-evidence/command-receipt.json \
  --receipt-base-dir /tmp/run-evidence \
  --format json \
  > /tmp/proof-packet.json
```

Gate merge readiness:

```sh
PYTHONPATH=/path/to/agent-merge-readiness/src \
  python3 -m agent_merge_readiness /tmp/change.diff \
  --title "Receipt-backed release change" \
  --proof-packet /tmp/proof-packet.json \
  --closeout /tmp/closeout.md
```

Preserve the run:

```sh
node /path/to/agent-run-ledger/bin/agent-run-ledger.js import-receipt \
  --ledger /tmp/agent-run-ledger.jsonl \
  --receipt /tmp/run-evidence/command-receipt.json \
  --base-dir /tmp/run-evidence
```

## Expected Signals

- `agent-merge-readiness` imports checks from a complete proof packet.
- The merge gate blocks if the proof packet is not `complete`.
- The merge gate blocks if proof-packet changed files differ from the current
  diff.
- The final readiness packet shows proof-packet findings for reviewers.

## Reviewer Interpretation

This chain keeps a review packet from becoming stale approval-by-artifact. The
same diff must pass receipt-backed proof packaging and merge-readiness checks
before the change is ready.
