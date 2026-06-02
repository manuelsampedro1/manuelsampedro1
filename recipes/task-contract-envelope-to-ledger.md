# Task Contract Envelope to Ledger Evidence

Use this when a `verify-by-change.v1` JSON envelope includes `task_contract` metadata and the run ledger should preserve that scope signal.

## Goal

Turn task-contract completeness from a verification envelope into durable ledger evidence before planned commands are recorded.

## Source Event

This recipe came from updating `agent-run-ledger import-checklist` to import `task_contract` from `verify-by-change --json-envelope`.

The public change connects three tools: `codex-review-packet` carries the task contract, `verify-by-change` preserves it in the envelope, and `agent-run-ledger` records it as review evidence.

## Workflow

1. Create the task contract before the agent run.
2. Generate a review packet with `codex-review-packet --task-contract`.
3. Generate a JSON envelope with `verify-by-change --review-packet ... --json-envelope`.
4. Import the envelope with `agent-run-ledger import-checklist`.
5. Run `agent-run-ledger doctor --strict` before accepting the handoff.
6. Record actual command outcomes separately after checks run.

## Example

```sh
python3 /path/to/codex-review-packet/codex_review_packet.py \
  --repo /path/to/repo \
  --task-contract /path/to/AGENT_TASK.md \
  --output /tmp/review-packet.md

python3 /path/to/verify-by-change/verify_by_change.py \
  --review-packet /tmp/review-packet.md \
  --json-envelope \
  --output /tmp/verification-envelope.json

node /path/to/agent-run-ledger/bin/agent-run-ledger.js import-checklist \
  --ledger .agent-run/ledger.jsonl \
  --checklist /tmp/verification-envelope.json
```

Expected ledger signal:

```text
Task contract passed
Verify docs
Verify node
```

If the envelope says the task contract is incomplete, the first event becomes `Task contract needs attention` with `blocked` status.

## Checklist

- Does the envelope include `schema_version: verify-by-change.v1`?
- Does the envelope include `task_contract`?
- Is `task_contract.status` `pass` before treating the verification plan as fully scoped?
- Are missing sections or placeholders recorded as blockers?
- Are planned verification commands still imported separately?
- Are actual command results recorded after execution rather than inferred from the envelope?

## Failure Modes

- Treating task-contract completeness as test success.
- Importing only planned commands and losing the task boundary.
- Letting `doctor --strict` pass while a contract has missing sections.
- Mixing a task contract from one review packet with verification evidence from another run.
- Recording `passed` commands before the commands actually ran.

## Source Linkage

- Public repo: <https://github.com/manuelsampedro1/agent-run-ledger>
- Commit: <https://github.com/manuelsampedro1/agent-run-ledger/commit/123639a2a6816b003f945608301f30253640d7ee>
- CI run: <https://github.com/manuelsampedro1/agent-run-ledger/actions/runs/26809075266>
- Lab note: <../labs/2026/2026-06-02-agent-run-ledger-task-contract-envelope-import.md>
