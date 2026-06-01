# CI Failure Packet for Agent Reruns

Use this when a coding-agent change fails CI and the next agent run needs focused evidence instead of a raw log dump.

## Use When

- CI failed after a Codex or Claude Code edit.
- The log is long enough that pasting all of it would dilute the signal.
- The next run should fix the failure, not re-open the whole task.
- You need a PR comment or prompt that a human can review quickly.

## Goal

Turn noisy CI output into a compact packet with:

- failing command,
- error signals,
- referenced files and line numbers,
- test summary,
- suggested checks,
- a scoped next-agent prompt.

## Workflow

1. Save the CI log:

```sh
pbpaste > /tmp/ci-failure.log
```

2. Extract the useful failure packet:

```sh
agent-ci-failure-packet /tmp/ci-failure.log --title "Publish guard CI failure"
```

3. If the helper is unavailable, build the packet manually:

```md
# CI Failure Packet: <title>

## Failing Commands
- `<command>`

## Error Signals
- `<first real error>`
- `<assertion or traceback>`

## Referenced Files
- `<path>:<line>`

## Suggested Checks
- `<smallest command that reproduces or verifies the fix>`

## Next Agent Prompt
Fix this CI failure using only the evidence above. Keep the patch scoped, rerun the failing command, and report the exact verification result.
```

4. Give the next agent the packet plus the current diff, not the entire CI archive.

## Prompt Pattern

```text
Fix this CI failure from the packet below.

Rules:
- Treat the packet as evidence, not as the whole repo context.
- Start with the referenced files and failing command.
- Keep the patch scoped to the failure.
- Rerun the failing command before closing.
- If the packet is insufficient, say exactly what log or file is missing.

<paste packet>
```

## Fast Checklist

- Does the packet name the failing command?
- Does it include the first actionable error, not only the final exit code?
- Does it include file references when available?
- Is the suggested check runnable?
- Does the next prompt prevent broad refactors?

## Failure Modes

- Pasting the entire CI log and asking the agent to "fix it."
- Omitting the command that failed.
- Keeping only the final `exit code 1` line.
- Sending stale logs after the branch has changed.
- Letting the retry agent expand scope beyond the failure.

## Source Linkage

- Repo / tool / workflow: local `agent-ci-failure-packet` prototype and this profile repo's agent workflow stack.
- Supporting prompt, script, or note: [`./codex-debugging-checklist.md`](./codex-debugging-checklist.md), [`./diff-to-eval-case.md`](./diff-to-eval-case.md), and [`../docs/profile-strategy.md`](../docs/profile-strategy.md).

