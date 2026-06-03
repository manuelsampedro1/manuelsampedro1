# Concrete Source Memory Audits

Use this pattern before reusing long-lived agent memory that contains current
state, account state, pricing, policy, tool availability, authentication, or
other external claims.

## Problem

Memory files can contain source-shaped text that is not usable evidence:
`Sources: manual note`, `verified earlier`, or `from chat`. That may be enough
for a human reminder, but it is weak input for a future agent that may treat
memory as context for action.

## Pattern

Run the memory audit and fail on medium findings when current-state claims
should be evidence-backed:

```sh
agent-memory-audit memory.md \
  --today 2026-06-03 \
  --fail-on medium \
  --format json \
  > /tmp/memory-audit.json
```

Treat `weak-source-evidence` as a request to attach a concrete pointer:

- a public or private URL;
- a repo-relative file path;
- a command output, log, transcript, receipt, or report path;
- a Git commit SHA;
- a CI run, job, artifact, issue, PR, or pull request ID.

## Acceptance Criteria

- Current-state claims have nearby source lines.
- Nearby source lines stay in the same paragraph or Markdown list item.
- Source evidence points at something inspectable, not only a vague human note.
- JSON output reports `concrete_source_mentions` for each audited file.
- `weak-source-evidence` and `unsourced-current-claim` are resolved before the
  memory is passed into a proof packet, run ledger, handoff, or next agent run.

## Review Rule

A concrete source is not a truth guarantee. It is a reusable pointer that lets
the next reviewer decide whether the memory claim is still valid.
