# External Reviewer Navigation

Use this example when a public profile has enough proof that the main problem is
scan time, not missing work.

## Scenario

A reviewer opens the profile and needs to judge whether the work shows useful
agent-engineering taste. A long Selected Work table is useful for depth, but the
first read needs a shorter path through the strongest evidence.

## Five-Minute Path

Start with the core loop:

- `repo-flightcheck`: repo readiness before an agent starts.
- `codex-review-packet`: repo-aware review context before handoff.
- `verify-by-change`: change-aware verification instead of generic closeout.
- `agent-run-ledger`: durable run evidence after the work happens.

Then check safety judgment:

- `agent-context-sentinel`: untrusted context and prompt-injection preflight.
- `agent-secret-sentinel`: secret-like diff scanning before publication.
- `mcp-guard`: tool-call permission rules before dangerous actions execute.

Then inspect composition:

- `examples/agent-release-readiness-chain.md`
- `examples/agent-review-packet-to-ledger-chain.md`

## What This Proves

- The profile is not only a list of small CLIs; it has a coherent reliability
  loop.
- The safety layer is visible without forcing a reviewer to infer it from repo
  names.
- Cross-repo examples show sequencing judgment, including cases where a packet
  exists but merge readiness or strict doctor mode still keeps evidence open.

## Review Prompt

```text
Review this profile using the reviewer path first. Decide whether the core loop
shows readiness, review context, verification, and auditability. Then inspect
the safety layer and cross-repo examples. Only use the full Selected Work table
for depth after the main workflow is clear.
```
