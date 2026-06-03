# Proof Packet Backed Scope Guards

Use this pattern when a coding-agent diff needs an explicit path allowlist and
structured proof-packet evidence for the same changed paths.

## Problem

Scope gates get weaker when test evidence is treated as scope approval:

- a proof packet can describe a different diff;
- a packet can be incomplete while scope output looks reusable;
- passing checks can hide an unrelated file edit;
- reviewers need to separate evidence from authorization.

## Pattern

Declare scope before the agent starts:

```sh
cat > /tmp/agent-scope.txt <<'EOF'
src/billing/**
tests/billing/**
docs/billing-runbook.md
EOF
```

Generate a proof packet from the same diff:

```sh
PYTHONPATH=/path/to/agent-proof-packet/src \
  python3 -m agent_proof_packet /tmp/change.diff \
  --title "Scope evidence" \
  --receipt /tmp/run-evidence/command-receipt.json \
  --receipt-base-dir /tmp/run-evidence \
  --format json \
  > /tmp/proof-packet.json
```

Run the scope gate with packet evidence:

```sh
PYTHONPATH=/path/to/agent-scope-guard/src \
  python3 -m agent_scope_guard /tmp/change.diff \
  --allow-file /tmp/agent-scope.txt \
  --proof-packet /tmp/proof-packet.json \
  --format json
```

## Acceptance Criteria

- The proof packet uses `agent-proof-packet.v1`.
- The proof packet verdict is `complete`.
- The proof packet has at least one passing check.
- The proof packet has changed-file evidence and no missing evidence.
- The proof packet changed-file list matches the provided diff or path list.
- Passing checks appear in the scope report.
- Unexpected paths remain blockers even when the packet is valid.

## Review Rule

Use `--proof-packet` to show evidence for changed paths, not to widen scope. If
the packet is incomplete, invalid, missing evidence, failing, or mismatched with
the diff, treat the scope report as not ready for reuse.
