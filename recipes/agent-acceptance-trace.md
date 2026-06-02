# Agent Acceptance Trace

Use this when a coding-agent task had explicit acceptance criteria and the
closeout needs a criterion-by-criterion evidence check.

## Source

- Public tool: https://github.com/manuelsampedro1/agent-acceptance-trace
- Launch note: [2026-06-02 - Agent Acceptance Trace Public Launch](../labs/2026/2026-06-02-agent-acceptance-trace-public-launch.md)

## Pattern

1. Save the task contract with an `Acceptance Criteria` section.
2. Save the implementation diff:

```sh
git diff origin/main -- . > /tmp/agent-change.diff
```

3. Save closeout, proof packet, command receipts, or CI notes as evidence files.
4. Generate the trace:

```sh
agent-acceptance-trace TASK_CONTRACT.md \
  --diff /tmp/agent-change.diff \
  --evidence closeout.md \
  --min-covered 80
```

5. Treat `partial` as unresolved unless a reviewer intentionally accepts the
remaining gap.
6. Use `--strict` when every criterion must have direct evidence before merge.

## What Good Looks Like

- Every acceptance criterion appears as its own row.
- Changed files are visible.
- Evidence snippets point to exact files and lines.
- Missing terms are visible instead of hidden behind a pass/fail summary.
- JSON output can be imported into proof packets, merge gates, or run ledgers.

## Prompt Pattern

```text
Trace this coding-agent run against its acceptance criteria.

Rules:
- Do not treat a confident closeout as evidence by itself.
- Use the task contract as the source of truth.
- For each criterion, cite changed files, commands, receipts, proof packet lines, or CI notes.
- Mark weak evidence as partial.
- Mark absent evidence as missing.

<task contract>
<diff>
<closeout or proof packet>
```

## Pair With

- `agent-task-contract` before the run,
- `agent-handoff-brief` before handing work to the agent,
- `agent-proof-packet` after the diff exists,
- `agent-claim-check` before publishing the final answer,
- `agent-run-ledger` when evidence needs to be preserved.

## Failure Mode

Do not lower the threshold to make a closeout look complete. If a criterion is
missing evidence, either gather stronger evidence, rerun verification, or keep
the task open.

