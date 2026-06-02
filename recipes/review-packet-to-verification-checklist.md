# Review Packet to Verification Checklist

Use this when a review packet already lists the changed files and the next agent or reviewer needs a focused verification plan.

## Goal

Turn packet scope into honest checks without reopening the original repo state or guessing from a generic test checklist.

## Source Event

This recipe came from adding `--review-packet` to `verify-by-change`.

The public change lets `verify-by-change` parse the `## Changed Files` section from `codex-review-packet` Markdown and classify those paths into a verification checklist.

## Workflow

1. Generate or receive a review packet that lists the intended changed files.
2. Run `verify-by-change --review-packet` against that packet.
3. Use `--json-envelope` when the output will be consumed by a ledger, gate, or another tool.
4. Treat the output as a plan, not as completed evidence.
5. Run the listed checks and record exact commands, results, and blockers in the final handoff.

## Example

```sh
python3 /path/to/codex-review-packet/codex_review_packet.py \
  --repo /path/to/repo \
  --output /tmp/review-packet.md

python3 /path/to/verify-by-change/verify_by_change.py \
  --review-packet /tmp/review-packet.md

python3 /path/to/verify-by-change/verify_by_change.py \
  --review-packet /tmp/review-packet.md \
  --json-envelope > /tmp/verification-plan.json
```

## Checklist

- Does the packet contain the changed files the reviewer is expected to inspect?
- Does the verification output cover the real change categories, not only the language runtime?
- Is the packet path source recorded when the plan is imported into another tool?
- Are missing or ambiguous packet inputs rejected before handoff?
- Are executed commands recorded separately from the generated checklist?

## Failure Modes

- Treating a packet-derived checklist as proof that verification ran.
- Mixing `--review-packet` with explicit paths and creating ambiguous scope.
- Using a stale packet after the diff changed.
- Publishing a packet that contains private local context or chat-only details.
- Losing the original command that generated the packet.

## Source Linkage

- Public repo: <https://github.com/manuelsampedro1/verify-by-change>
- Commit: <https://github.com/manuelsampedro1/verify-by-change/commit/9e8720e7150bf5faa6731e2a5a16027b90b93742>
- CI run: <https://github.com/manuelsampedro1/verify-by-change/actions/runs/26797987666>
- Lab note: <../labs/2026/2026-06-02-verify-by-change-review-packet-source.md>
