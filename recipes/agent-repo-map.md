# Agent Repo Map

Use this before giving a repo to a coding agent, especially when the checkout is unfamiliar or has multiple tools, docs, workflows, or risk surfaces.

## Source

- Public tool: https://github.com/manuelsampedro1/agent-repo-map
- Launch note: [2026-06-02 - Agent Repo Map Public Launch](../labs/2026/2026-06-02-agent-repo-map-public-launch.md)

## Pattern

1. Start from a clean checkout.
2. Generate a context map:

```sh
agent-repo-map . --min-score 80
```

3. Read the map before planning agent work.
4. Copy the relevant docs, commands, verification signals, entrypoints, and risk paths into the task handoff.
5. If the map reports gaps, fix the repo context before asking the agent to make a broad change.

## What To Look For

- Missing `README.md` or agent instructions.
- No obvious local test, lint, build, or smoke command.
- Entry points that do not match the requested work.
- CI, deploy, migration, auth, or secret-looking paths that require tighter review.
- Dirty Git state before the task starts.

## Good Follow-Up

Pair it with:

- `agent-task-contract` for the task intent,
- `repo-flightcheck` for readiness,
- `agent-instruction-audit` for instruction quality,
- `codex-review-packet` after the diff exists.

## Failure Mode

Do not treat the map as a security audit or architecture review. It is a fast context preflight that tells the agent and reviewer where to look first.
