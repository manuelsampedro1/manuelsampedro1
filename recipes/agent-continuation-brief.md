# Agent Continuation Brief

Use this before a long-running coding-agent task is resumed by another run.

## Source

- Public tool: https://github.com/manuelsampedro1/agent-continuation-brief
- Launch note: [2026-06-02 - Agent Continuation Brief Public Launch](../labs/2026/2026-06-02-agent-continuation-brief-public-launch.md)

## Pattern

1. Save the continuation note as Markdown:

```sh
agent-continuation-brief /tmp/continuation.md --min-score 80
```

2. Block weak handoffs before the next run starts:

```sh
agent-continuation-brief /tmp/continuation.md --fail-on needs-info
```

3. Write a compact next-agent brief:

```sh
agent-continuation-brief /tmp/continuation.md --write-brief /tmp/next-agent-brief.md
```

4. If the status is `blocked` or `needs-info`, reconstruct the missing state or
ask for the smallest concrete clarification before resuming.

## What Good Looks Like

- The original objective is preserved, not rewritten around completed work.
- Current state separates what exists now from what still needs action.
- Completed and in-progress work are explicit.
- Blockers, risks, and external outcomes are not hidden.
- Changed files and commands already run can be verified.
- Next actions are ordered and concrete.
- The next-agent instructions say what must not be guessed.

## Prompt Pattern

```text
Prepare this continuation note for a coding-agent resume.

Rules:
- Preserve the original objective exactly; do not shrink it to the current subtask.
- Require current state, completed work, in-progress work, blockers, changed files, commands, next actions, risks, and handoff instructions.
- Treat missing verification or external outcomes as residual uncertainty, not completion.
- Return the smallest next-agent brief that can be executed without guessing.

<agent-continuation-brief output>
<candidate continuation note>
```

## Pair With

- `agent-handoff-brief` when starting the first run,
- `agent-run-ledger` when preserving command and evidence history,
- `agent-tool-call-audit` when the previous run used sensitive tools,
- `agent-proof-packet` when resuming near review or merge,
- `agent-claim-check` before reusing a continuation closeout publicly.

## Failure Mode

Do not treat "almost done" as continuation state. A continuation handoff should
make the next agent faster by removing ambiguity, not by hiding unfinished work.
