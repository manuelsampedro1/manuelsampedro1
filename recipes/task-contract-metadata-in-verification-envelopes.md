# Task Contract Metadata in Verification Envelopes

Use this when a verification plan is generated from a review packet and downstream tools need to know whether the original task was complete enough to verify.

## Goal

Carry `## Task Contract` status from `codex-review-packet` into `verify-by-change --json-envelope` output.

## Source Event

This recipe came from updating `verify-by-change` to parse task-contract metadata from review packets.

The public change lets a single review packet feed verification gates or ledgers without losing whether the task contract passed, which required sections were present, and whether placeholder markers remain.

## Workflow

1. Write or generate a task contract before the agent run.
2. Generate a review packet with `codex-review-packet --task-contract`.
3. Generate a verification envelope with `verify-by-change --review-packet ... --json-envelope`.
4. Check `task_contract.status` before accepting the envelope as planned against a complete task.
5. Treat missing sections or placeholder markers as a scope blocker, not as a test failure.
6. Keep command evidence separate from task-contract completeness.

## Example

```sh
python3 /path/to/codex-review-packet/codex_review_packet.py \
  --repo /path/to/target-repo \
  --task-contract /path/to/AGENT_TASK.md \
  --output /tmp/review-packet.md

python3 /path/to/verify-by-change/verify_by_change.py \
  --review-packet /tmp/review-packet.md \
  --json-envelope \
  --output /tmp/verification-envelope.json
```

Expected envelope signal:

```json
{
  "schema_version": "verify-by-change.v1",
  "source": { "type": "review_packet" },
  "task_contract": {
    "source": "AGENT_TASK.md",
    "status": "pass",
    "required_sections": "8/8",
    "missing_sections": [],
    "placeholder_markers": []
  }
}
```

## Checklist

- Does the review packet include `## Task Contract`?
- Was the task contract generated for the same run and diff?
- Does `task_contract.status` equal `pass`?
- Are `missing_sections` and `placeholder_markers` empty?
- Do acceptance criteria map to the suggested verification commands?
- Does the envelope still include separate command evidence when checks actually run?

## Failure Modes

- Treating a complete task contract as proof that implementation is correct.
- Accepting a verification envelope from a packet whose task contract has placeholders.
- Mixing a review packet from one run with command evidence from another.
- Hiding acceptance criteria in chat instead of preserving them in the packet.
- Dropping task-contract metadata before importing the run into a ledger.

## Source Linkage

- Public repo: <https://github.com/manuelsampedro1/verify-by-change>
- Commit: <https://github.com/manuelsampedro1/verify-by-change/commit/4e8380d6bed3e36be1715f4849d8b9357f802277>
- CI run: <https://github.com/manuelsampedro1/verify-by-change/actions/runs/26808615897>
- Lab note: <../labs/2026/2026-06-02-verify-by-change-task-contract-metadata.md>
