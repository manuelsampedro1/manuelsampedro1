# Task Contracts in Review Packets

Use this when an agent-generated diff should be reviewed against the original task, not only against repo context and tests.

## Goal

Make the review packet carry the objective, acceptance criteria, constraints, expected changes, verification, risks, and out-of-scope boundaries before the diff.

## Source Event

This recipe came from adding task-contract rendering to `codex-review-packet`.

The public change auto-detects `AGENT_TASK.md` or `TASK_CONTRACT.md`, accepts explicit external contracts with `--task-contract`, and renders a bounded `## Task Contract` section with lightweight completeness warnings.

## Workflow

1. Write the task contract before the agent starts, or keep a repo-level `AGENT_TASK.md` for the current run.
2. Include the required sections: Objective, Acceptance Criteria, Context, Constraints, Expected Changes, Verification, Risks, and Out of Scope.
3. Generate the review packet after the diff is ready.
4. Let `codex-review-packet` auto-detect the repo contract, or pass an external file with `--task-contract`.
5. Check the packet's `## Task Contract` status before reviewing the diff.
6. Treat missing sections or placeholder markers as review blockers unless the task is intentionally exploratory.

## Example

```sh
python3 /path/to/codex-review-packet/codex_review_packet.py \
  --repo /path/to/repo \
  --task-contract /path/to/AGENT_TASK.md \
  --task-contract-lines 80 \
  --output /tmp/review-packet.md
```

Expected packet signal:

```md
## Task Contract

- Status: `pass`
- Required sections: `8/8`
- Missing sections: none
- Placeholder markers: none
```

## Checklist

- Does the packet include `## Task Contract` before the diff?
- Does the contract come from the same run being reviewed?
- Are all eight required sections present?
- Are placeholder markers absent?
- Do expected changes match the actual changed files?
- Do acceptance criteria map to the verification commands?
- Does out-of-scope work explain what the agent should not touch?

## Failure Modes

- Reviewing a clean diff without knowing the original acceptance criteria.
- Reusing a stale task contract after scope changed.
- Treating `pass` as proof of correctness instead of proof that the task context is complete.
- Letting the contract exceed the model context without a visible omission marker.
- Hiding constraints in chat instead of placing them in the review artifact.

## Source Linkage

- Public repo: <https://github.com/manuelsampedro1/codex-review-packet>
- Commit: <https://github.com/manuelsampedro1/codex-review-packet/commit/0df7499f1e2b47b679072e52c4060198a1559e60>
- CI run: <https://github.com/manuelsampedro1/codex-review-packet/actions/runs/26807708146>
- Lab note: <../labs/2026/2026-06-02-codex-review-packet-task-contracts.md>
