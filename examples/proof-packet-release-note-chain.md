# Proof Packet Release Note Chain

Use this example when a reviewer wants release-note coverage and structured
verification evidence in the same report.

## Scenario

A coding agent updates auth code, dependency pins, CI workflow steps, and tests.
The draft release notes say the change is fully tested. A proof packet may
support that verification claim, but it should not hide missing security,
dependency, CI, or breaking-change coverage.

## Command Chain

Create a command receipt:

```sh
PYTHONPATH=/path/to/agent-command-receipt/src \
  python3 -m agent_command_receipt record \
  --command "make test && make smoke" \
  --status pass \
  --evidence /tmp/run-evidence/release-checks.log \
  --output /tmp/run-evidence/command-receipt.json
```

Package the proof:

```sh
PYTHONPATH=/path/to/agent-proof-packet/src \
  python3 -m agent_proof_packet /tmp/release.diff \
  --title "Release note verification evidence" \
  --receipt /tmp/run-evidence/command-receipt.json \
  --receipt-base-dir /tmp/run-evidence \
  --format json \
  > /tmp/proof-packet.json
```

Inspect the release notes:

```sh
PYTHONPATH=/path/to/agent-release-note-check/src \
  python3 -m agent_release_note_check /tmp/release-notes.md \
  --diff /tmp/release.diff \
  --proof-packet /tmp/proof-packet.json \
  --fail-on high
```

## Expected Signals

- The proof packet must be complete and match the diff.
- Passing packet checks can support strong verification language.
- Missing release-note coverage still appears as findings.
- Contradictions such as `docs only`, `no breaking changes`, or `no security
  impact` still fail when the diff disagrees.
- Packet evidence does not lower release risk or remove diff-derived findings.

## Reviewer Interpretation

This chain prevents a proof packet from becoming a release stamp. The report
keeps release-note gaps visible and uses packet evidence only to show which
verification checks are actually backed by structured proof.
