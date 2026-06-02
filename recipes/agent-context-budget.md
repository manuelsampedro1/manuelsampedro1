# Agent Context Budget

Use this before handing a large context bundle to another coding agent.

## Source

- Public tool: https://github.com/manuelsampedro1/agent-context-budget
- Launch note: [2026-06-02 - Agent Context Budget Public Launch](../labs/2026/2026-06-02-agent-context-budget-public-launch.md)

## Pattern

1. Check a bundle against a realistic context budget:

```sh
agent-context-budget README.md AGENTS.md TODO.md docs/ --budget 12000 --min-score 80
```

2. Fail when oversized or duplicate context would waste the next run:

```sh
agent-context-budget handoff/ --fail-on medium
```

3. Write the plan into the next-agent packet:

```sh
agent-context-budget handoff/ --write-report /tmp/context-budget.md
```

4. Keep only the `keep` files verbatim, summarize the `summarize` files, and
   drop the `drop` files before starting the next agent.

## What Good Looks Like

- The next agent receives the current task brief, repo instructions, README,
  decision context, and concrete verification commands.
- Large logs, generated files, build outputs, and repeated copies are excluded
  or summarized.
- The handoff explains why each high-volume file is needed.
- Context budget failure blocks the run before the model has to infer what to
  ignore.

## Prompt Pattern

```text
Prepare this context for the next coding-agent run.

Rules:
- Keep task state, repo rules, acceptance criteria, decisions, and verification commands.
- Summarize large logs or repeated context instead of pasting them verbatim.
- Drop generated files and duplicate bundles unless they contain unique failure evidence.
- Include the context-budget findings and the final keep/summarize/drop plan.

<agent-context-budget output>
<candidate context files>
```

## Pair With

- `agent-repo-map` to discover the candidate repo context,
- `agent-handoff-brief` to turn the final context into a scoped prompt,
- `agent-continuation-brief` when a long-running task spans multiple runs,
- `agent-context-sentinel` when copied or retrieved context is untrusted.

## Failure Mode

Do not optimize only for a smaller token count. The goal is to preserve the
minimum evidence needed for a correct next action while removing context that
would distract, duplicate, or override the task.
