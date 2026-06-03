# Proof Packet Backed Release Notes

Use this pattern when release notes make verification claims and the supporting
checks already exist in a structured proof packet.

## Problem

Release notes get weaker when verification evidence sits outside the note:

- a proof packet can describe a different diff;
- a packet can be incomplete while release notes still say `fully tested`;
- broad green checks can be mistaken for release safety;
- reviewers need to distinguish verification evidence from release-risk
  coverage.

## Pattern

Generate a proof packet from the same release diff:

```sh
PYTHONPATH=/path/to/agent-proof-packet/src \
  python3 -m agent_proof_packet /tmp/release.diff \
  --title "Release note verification evidence" \
  --receipt /tmp/run-evidence/command-receipt.json \
  --receipt-base-dir /tmp/run-evidence \
  --format json \
  > /tmp/proof-packet.json
```

Audit the release notes with the packet:

```sh
PYTHONPATH=/path/to/agent-release-note-check/src \
  python3 -m agent_release_note_check /tmp/release-notes.md \
  --diff /tmp/release.diff \
  --proof-packet /tmp/proof-packet.json \
  --fail-on high
```

## Acceptance Criteria

- The proof packet uses `agent-proof-packet.v1`.
- The proof packet verdict is `complete`.
- The proof packet has at least one passing check.
- The proof packet has changed-file evidence and no missing evidence.
- The proof packet changed-file list matches the provided diff.
- Strong verification claims are supported by passing packet checks or named
  checks in the note.
- Breaking, security, dependency, CI, docs-only, and contradiction findings
  still come from the diff and note.

## Review Rule

Use `--proof-packet` to audit release-note verification evidence next to
release-note coverage findings. If the packet is incomplete, invalid, missing
evidence, failing, or mismatched with the diff, treat the release notes as not
ready for reuse.
