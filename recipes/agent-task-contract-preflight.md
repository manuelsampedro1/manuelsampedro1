# Agent Task Contract Preflight

Use this before handing a non-trivial task to Codex, Claude Code, or another coding agent.

## Goal

Reject vague agent tasks before the first edit by requiring a complete Markdown task contract.

## Source Event

This recipe came from publishing `agent-task-contract`, a dependency-free Python CLI that validates task briefs before coding-agent work starts.

## Workflow

1. Create `AGENT_TASK.md` in the target repo or handoff folder.
2. Fill in objective, acceptance criteria, context, constraints, expected changes, verification, risks, and out-of-scope boundaries.
3. Run `agent-task-contract check AGENT_TASK.md`.
4. Fix missing sections, placeholders, weak acceptance criteria, or missing verification.
5. Use `--require-acceptance-ids` when criteria will be reused by traces, packets, ledgers, or closeouts.
6. Only then run repo readiness, review packet generation, or the agent itself.
7. Keep the task contract attached to review packets, verification envelopes, and run ledgers when possible.

## Example

```sh
agent-task-contract init AGENT_TASK.md
agent-task-contract check AGENT_TASK.md
agent-task-contract check AGENT_TASK.md --require-acceptance-ids
agent-task-contract check AGENT_TASK.md --format json
```

Expected pass signal:

```text
Agent Task Contract: AGENT_TASK.md
Status: pass
Score: 100/100
Acceptance ids: 2/2

No blocking issues found.
```

## Checklist

- Does the objective name one concrete outcome?
- Are there at least two observable acceptance criteria?
- Does each reusable criterion have a stable ID such as `AC-1`?
- Does the context explain why the task matters?
- Do constraints identify files, APIs, product boundaries, or behaviors that must not change?
- Do expected changes name likely files, modules, commands, or artifacts?
- Does verification include a command or concrete manual review gate?
- Are risks and out-of-scope items explicit enough to prevent agent overreach?

## Failure Modes

- Starting from a polished prompt that still lacks acceptance criteria.
- Treating repo readiness as a substitute for task readiness.
- Allowing placeholder text like `TBD` or `state the objective`.
- Asking an agent to infer non-goals from context.
- Recording downstream verification without preserving the task boundary that created it.
- Referring to "the second acceptance criterion" after the criteria have been reordered.

## Source Linkage

- Public repo: <https://github.com/manuelsampedro1/agent-task-contract>
- Commit: <https://github.com/manuelsampedro1/agent-task-contract/commit/3b78889e1b25de9b2450187f1b8ffadd737bf2fb>
- Lab note: <../labs/2026/2026-06-02-agent-task-contract-public-launch.md>
