# Task Contract Envelope Summary in Review Packets

Use this when a review packet embeds a `verify-by-change.v1` envelope and the reviewer needs to see the task-contract scope signal without opening raw JSON.

## Goal

Render task-contract metadata from a verification envelope as compact review context before the checklist body.

## Source Event

This recipe came from updating `codex-review-packet` to summarize `task_contract` from generated or supplied `verify-by-change.v1` envelopes.

The public change keeps the agent reliability chain readable: task contract in the packet, task-contract metadata in the verification envelope, and task-contract evidence in the ledger.

## Workflow

1. Write a complete `AGENT_TASK.md` or `TASK_CONTRACT.md`.
2. Generate a review packet with `codex-review-packet --task-contract --verify-by-change`.
3. Confirm the packet's verification section shows `Task contract: pass`.
4. Keep missing task sections and placeholders visible as review context.
5. Import the packet into `agent-run-ledger` when the handoff needs durable audit evidence.

## Example

```sh
python3 /path/to/codex-review-packet/codex_review_packet.py \
  --repo /path/to/repo \
  --task-contract /path/to/AGENT_TASK.md \
  --verify-by-change /path/to/verify-by-change/verify_by_change.py \
  --output /tmp/review-packet.md
```

Expected packet signal:

```md
## Verification Checklist

Envelope: `verify-by-change.v1`
Task contract: `pass` (8/8 required sections)
Task contract source: `/path/to/AGENT_TASK.md`
```

## Checklist

- Does the packet include `Envelope: verify-by-change.v1`?
- Does the verification section show task-contract status before the fenced checklist body?
- Are missing sections and placeholders visible when the contract is incomplete?
- Does the summary avoid top-level `## Task Contract` headings inside the checklist body?
- Can `agent-run-ledger import-review-packet` still parse the packet?

## Failure Modes

- Hiding task-contract status in raw JSON where reviewers will miss it.
- Rendering task-contract metadata as a fenced `## Task Contract` heading that breaks packet parsers.
- Treating `Task contract: pass` as proof that verification commands passed.
- Dropping missing sections or placeholders when the contract is incomplete.

## Source Linkage

- Public repo: <https://github.com/manuelsampedro1/codex-review-packet>
- Commit: <https://github.com/manuelsampedro1/codex-review-packet/commit/4a4019d4f9894e24ac068aecde189da24e6354a0>
- CI run: <https://github.com/manuelsampedro1/codex-review-packet/actions/runs/26809468718>
- Lab note: <../labs/2026/2026-06-02-codex-review-packet-task-contract-envelope-summary.md>
