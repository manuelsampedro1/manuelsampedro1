# Agent Handoff Brief

Use this when a task is clear enough to start, but the next agent still needs a compact operating brief instead of scattered docs and assumptions.

## Source

- Public tool: https://github.com/manuelsampedro1/agent-handoff-brief
- Launch note: [2026-06-02 - Agent Handoff Brief Public Launch](../labs/2026/2026-06-02-agent-handoff-brief-public-launch.md)

## Pattern

1. Write or locate the task contract.
2. Start from a clean checkout.
3. Generate the handoff:

```sh
agent-handoff-brief . --task AGENT_TASK.md --min-score 80
```

4. Give the generated `Agent Prompt` section to the next agent.
5. If the brief reports gaps, fix the task or repo context before starting the run.

## What Good Looks Like

- Objective is specific.
- Acceptance criteria are testable.
- Constraints and out-of-scope boundaries are explicit.
- Required reading points to real repo docs.
- Verification commands are exact.
- Risk paths are visible before edits begin.
- Dirty Git state is either absent or intentionally documented.

## Good Follow-Up

Pair it with:

- `agent-task-contract` to validate task intent,
- `agent-repo-map` to inspect repo terrain,
- `repo-flightcheck` to verify readiness,
- `codex-review-packet` after the diff exists,
- `agent-run-ledger` to preserve the handoff and results.

## Failure Mode

Do not use a generated handoff to hide weak task definition. If the brief says `needs-context`, fix the task contract or repo setup before asking an agent to execute broad work.
