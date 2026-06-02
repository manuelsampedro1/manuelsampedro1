# Agent Retry Guard

Use this before asking another coding agent to continue after repeated command
failures.

## Source

- Public tool: https://github.com/manuelsampedro1/agent-retry-guard
- Launch note: [2026-06-02 - Agent Retry Guard Public Launch](../labs/2026/2026-06-02-agent-retry-guard-public-launch.md)

## Pattern

1. Save the transcript or command log:

```sh
agent-retry-guard transcript.log --min-score 80
```

2. Fail on obvious blind retry loops:

```sh
agent-retry-guard transcript.log --fail-on high
```

3. Write a handoff report:

```sh
agent-retry-guard transcript.log --write-report /tmp/retry-guard.md
```

4. If the report is `blocked`, require investigation before the next agent run.

## What Good Looks Like

- Repeated failures have a different hypothesis or command path.
- The transcript shows source, docs, environment, or diff inspection between retries.
- Same-command retries are limited and intentional.
- The next agent gets a concrete reason for the new strategy.
- The closeout does not hide repeated failures behind a generic "tests failed" note.

## Prompt Pattern

```text
Review this failed agent run before continuing.

Rules:
- Detect whether the same command and same error repeated without investigation.
- If the run is blocked, do not propose another blind retry.
- Require the smallest concrete strategy shift: source inspection, docs lookup, environment check, changed hypothesis, or alternate verification command.
- Preserve the failed commands and line references in the next-agent handoff.

<agent-retry-guard output>
<transcript>
```

## Pair With

- `agent-bug-repro` when the failure started from a vague bug report,
- `agent-ci-failure-packet` when CI logs need focused retry context,
- `agent-tool-call-audit` when the repeated failures came from tool-call misuse,
- `agent-continuation-brief` before handing the run to another agent.

## Failure Mode

Do not block every repeated command. Some retries are valid after a real fix.
Block the pattern where the command, error signature, and strategy stay the
same.
