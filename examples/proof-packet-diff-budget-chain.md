# Proof Packet Diff Budget Chain

Use this example when a reviewer wants a strict diff budget and structured
proof-packet evidence in the same report.

## Scenario

A coding agent changes application code, CI, database migrations, and runbook
docs. Checks may have passed, but the diff can still be too broad or too risky
for one review pass.

## Command Chain

Create a command receipt:

```sh
PYTHONPATH=/path/to/agent-command-receipt/src \
  python3 -m agent_command_receipt record \
  --command "make test && make smoke" \
  --status pass \
  --evidence /tmp/run-evidence/diff-budget-checks.log \
  --output /tmp/run-evidence/command-receipt.json
```

Package the proof:

```sh
PYTHONPATH=/path/to/agent-proof-packet/src \
  python3 -m agent_proof_packet /tmp/change.diff \
  --title "Diff-budget evidence" \
  --receipt /tmp/run-evidence/command-receipt.json \
  --receipt-base-dir /tmp/run-evidence \
  --format json \
  > /tmp/proof-packet.json
```

Run the budget gate with evidence:

```sh
PYTHONPATH=/path/to/agent-diff-budget/src \
  python3 -m agent_diff_budget /tmp/change.diff \
  --max-files 6 \
  --max-total 350 \
  --max-high-risk-files 2 \
  --proof-packet /tmp/proof-packet.json \
  --format json
```

## Expected Signals

- The proof packet must be complete and match the diff.
- Passing packet checks appear beside matching changed files.
- Budget failures remain visible when file count, line volume, or high-risk file
  count exceed the configured limits.
- Invalid or diff-mismatched packets make the command fail.

## Reviewer Interpretation

This chain prevents test evidence from becoming a review-budget waiver. The
report can show which checks were performed while still forcing broad diffs to
be split, justified, or escalated before review.
