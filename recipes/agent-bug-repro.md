# Agent Bug Repro

Use this before a vague bug report becomes a coding-agent debugging task.

## Source

- Public tool: https://github.com/manuelsampedro1/agent-bug-repro
- Launch note: [2026-06-02 - Agent Bug Repro Public Launch](../labs/2026/2026-06-02-agent-bug-repro-public-launch.md)

## Pattern

1. Save the bug report as Markdown:

```sh
agent-bug-repro /tmp/bug-report.md --fail-on blocked
```

2. Attach available text evidence:

```sh
agent-bug-repro /tmp/bug-report.md --evidence /tmp/error-log.txt --min-score 80
```

3. Write a next-agent packet:

```sh
agent-bug-repro /tmp/bug-report.md --evidence /tmp/error-log.txt --write-packet /tmp/repro-packet.md
```

4. If the status is `blocked` or `needs-info`, fix the report before assigning
the debugging run.

## What Good Looks Like

- Repro steps are explicit and ordered.
- Expected behavior and actual behavior are separate.
- Environment, version, branch, browser, device, or command context is present.
- Evidence includes a failing command, log signal, screenshot reference, trace,
  or minimal fixture.
- Regression or frequency context narrows where the next agent should inspect.
- The next-agent prompt says what is known and what must not be guessed.

## Prompt Pattern

```text
Prepare this bug for a coding-agent debugging run.

Rules:
- Do not start broad code edits until repro steps, expected behavior, actual behavior, environment, and evidence are present.
- If evidence is thin, ask for the missing artifact or build the smallest local reproduction.
- Prefer a failing test before product-code changes when feasible.
- Preserve exact commands and residual uncertainty in the closeout.

<agent-bug-repro output>
<candidate bug report>
```

## Pair With

- `agent-ci-failure-packet` when the bug starts from a CI log,
- `agent-test-impact` when choosing verification scope,
- `agent-rollback-plan` if the fix touches risky release paths,
- `agent-proof-packet` for the final debugging handoff,
- `agent-claim-check` before reusing the closeout publicly.

## Failure Mode

Do not confuse a plausible bug summary with a reproducible case. A debugging
agent needs enough concrete evidence to reproduce or falsify the report.
