# Proof Packet Backed Dependency Review

Use this pattern when dependency-risk output should show which required checks
already have structured proof-packet evidence.

## Problem

Dependency review gets weaker when proof evidence sits outside the report:

- a proof packet can describe a different diff;
- a packet can be incomplete while the dependency report looks reusable;
- broad green tests can be mistaken for dependency safety;
- reviewers need to distinguish dependency findings from checks already run.

## Pattern

Generate a proof packet from the same dependency diff:

```sh
PYTHONPATH=/path/to/agent-proof-packet/src \
  python3 -m agent_proof_packet /tmp/dependency-change.diff \
  --title "Dependency review evidence" \
  --receipt /tmp/run-evidence/command-receipt.json \
  --receipt-base-dir /tmp/run-evidence \
  --format json \
  > /tmp/proof-packet.json
```

Run dependency review with the packet:

```sh
PYTHONPATH=/path/to/agent-dependency-guard/src \
  python3 -m agent_dependency_guard /tmp/dependency-change.diff \
  --proof-packet /tmp/proof-packet.json \
  --fail-on high
```

## Acceptance Criteria

- The proof packet uses `agent-proof-packet.v1`.
- The proof packet verdict is `complete`.
- The proof packet has at least one passing check.
- The proof packet has changed-file evidence and no missing evidence.
- The proof packet changed-file list matches the provided diff.
- Check evidence is mapped by passing check names, not by vague prose.
- Dependency findings, score, and severity still come from the diff.

## Review Rule

Use `--proof-packet` to audit dependency-review evidence next to dependency
findings. If the packet is incomplete, invalid, missing evidence, failing, or
mismatched with the diff, treat the dependency report as not ready for reuse.
