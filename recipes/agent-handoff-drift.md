# Agent Handoff Drift

Use this before another coding agent continues from a handoff or continuation
note.

## Source

- Public tool: https://github.com/manuelsampedro1/agent-handoff-drift
- Launch note: [2026-06-02 - Agent Handoff Drift Public Launch](../labs/2026/2026-06-02-agent-handoff-drift-public-launch.md)

## Pattern

1. Audit the note against the repo the next agent will inherit:

```sh
agent-handoff-drift handoff.md --repo . --min-score 80
```

2. Fail on concrete contradictions:

```sh
agent-handoff-drift handoff.md --repo . --fail-on medium
```

3. Write the report into the next-agent packet:

```sh
agent-handoff-drift handoff.md --repo . --write-report /tmp/handoff-drift.md
```

4. Refresh the note before continuing if the report is `blocked`.

## What Good Looks Like

- Referenced files exist in the current repo.
- Branch and HEAD claims match the checked-out state.
- Dirty worktree state is either absent or explicitly documented.
- Command success includes minimal evidence: exit code, output, report path,
  receipt, or CI run.
- The next agent gets a current note instead of stale state from a prior run.

## Prompt Pattern

```text
Review this continuation handoff before another coding agent continues.

Rules:
- Compare the handoff claims to the current repo state.
- If files, branch, HEAD, worktree state, or command evidence drifted, refresh the note first.
- Do not ask the next agent to infer whether stale claims are still true.
- Include the drift report in the handoff packet.

<agent-handoff-drift output>
<handoff note>
```

## Pair With

- `agent-handoff-brief` when preparing a fresh pre-run packet,
- `agent-continuation-brief` when resuming long-running work,
- `agent-context-budget` when the handoff bundle is too large,
- `agent-context-sentinel` when copied context may contain hostile instructions.

## Failure Mode

Do not treat this as a full truth engine. It catches concrete drift signals
against Git and repo files; subjective project status still needs human or
agent review.
