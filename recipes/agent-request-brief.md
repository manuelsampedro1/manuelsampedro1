# Agent Request Brief

Use this before a raw human request becomes a coding-agent task.

## Source

- Public tool: https://github.com/manuelsampedro1/agent-request-brief
- Launch note: [2026-06-02 - Agent Request Brief Public Launch](../labs/2026/2026-06-02-agent-request-brief-public-launch.md)

## Pattern

1. Save the raw request or transcript:

```sh
agent-request-brief /tmp/request.md --min-score 80
```

2. Block vague requests before broad edits:

```sh
agent-request-brief /tmp/request.md --fail-on needs-info
```

3. Write a next-agent brief:

```sh
agent-request-brief /tmp/request.md --write-brief /tmp/request-brief.md
```

4. If the status is `blocked` or `needs-info`, clarify the missing section before
asking an agent to edit the repo.

## What Good Looks Like

- The objective is concrete.
- Scope names the repo, files, paths, or artifact boundary.
- Acceptance criteria are observable.
- Constraints and non-goals are preserved.
- Current context and source evidence are included.
- Verification commands are explicit.
- External outcomes stay marked as uncertainty.
- Next actions are ordered enough for a new run to start safely.

## Prompt Pattern

```text
Prepare this raw request for a coding-agent run.

Rules:
- Do not start broad edits until objective, scope, acceptance criteria, constraints, context, verification, risks, and next actions are clear.
- Separate agent-verifiable work from external outcomes such as hiring, prizes, approvals, or public perception.
- Ask the smallest concrete question if a required signal is missing.
- Preserve residual uncertainty in the handoff and final closeout.

<agent-request-brief output>
<raw request>
```

## Pair With

- `agent-task-contract` after the raw request has enough structure,
- `agent-handoff-brief` before the first editing run,
- `agent-continuation-brief` when the work spans runs,
- `agent-acceptance-trace` after the diff exists,
- `agent-claim-check` before reusing the final answer publicly.

## Failure Mode

Do not translate enthusiasm into requirements. "Make it more pro" is direction,
not an acceptance criterion. The agent needs inspectable scope and verification.
