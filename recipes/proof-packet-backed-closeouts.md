# Proof Packet Backed Closeouts

Use this pattern when a final answer cites a proof packet and the reviewer needs
to know that packet is valid for the closeout.

## Problem

Closeouts can overstate evidence when they point to proof artifacts without
checking them:

- the proof packet can be `blocked` or `needs-review`;
- the packet can have missing evidence or open questions;
- the final answer can cite files not covered by the packet;
- the closeout can avoid exact verification commands by hiding behind a packet.

## Pattern

Generate the proof packet:

```sh
PYTHONPATH=/path/to/agent-proof-packet/src \
  python3 -m agent_proof_packet /tmp/change.diff \
  --title "Receipt-backed final answer" \
  --receipt /tmp/run-evidence/command-receipt.json \
  --receipt-base-dir /tmp/run-evidence \
  --format json \
  > /tmp/proof-packet.json
```

Check the final answer against the packet:

```sh
PYTHONPATH=/path/to/agent-closeout-check/src \
  python3 -m agent_closeout_check /tmp/closeout.md \
  --proof-packet /tmp/proof-packet.json
```

## Acceptance Criteria

- The closeout still has a summary, verification section, exact command, and
  residual-risk note.
- The proof packet uses `agent-proof-packet.v1`.
- The proof packet verdict is `complete`.
- The proof packet has at least one passing check.
- The proof packet has changed-file evidence and no missing evidence.
- Files cited by the closeout are covered by the proof packet or are the proof
  packet file itself.

## Review Rule

Use `--proof-packet` when a closeout depends on a packet for changed-path
evidence. If the packet is incomplete, invalid, or misaligned with the files
cited in the closeout, treat the closeout as not ready.
