# Agent Tool Call Audit

Use this after a coding-agent run when the transcript or JSONL tool history
needs review before the closeout is trusted.

## Source

- Public tool: https://github.com/manuelsampedro1/agent-tool-call-audit
- Launch note: [2026-06-02 - Agent Tool Call Audit Public Launch](../labs/2026/2026-06-02-agent-tool-call-audit-public-launch.md)

## Pattern

1. Save the tool-call log as JSONL or plain text:

```sh
agent-tool-call-audit /tmp/tool-calls.jsonl --fail-on high
```

2. For automation, emit JSON:

```sh
agent-tool-call-audit /tmp/tool-calls.jsonl --format json --min-score 80
```

3. When sensitive external actions must carry authority evidence, require
approval markers:

```sh
agent-tool-call-audit /tmp/tool-calls.jsonl --require-approval --fail-on high
```

4. If the audit blocks, do not accept the final answer as proof. Review the
specific call, command, severity, repeated failure, or redacted evidence.

5. Preserve the audit output in the proof packet, merge-readiness verdict, or
run ledger.

## What Good Looks Like

- Destructive shell commands are visible and explained.
- Sensitive external actions are separated from ordinary local checks.
- Sensitive external actions can require approval or receipt evidence.
- Repeated failed attempts are not hidden by a later success.
- Secret-material markers are redacted in rendered evidence.
- Missing working directories are caught in structured shell logs.
- Findings are attached to exact call indexes or aggregate repeated-failure
  counts.

## Prompt Pattern

```text
Review this coding-agent run for tool-call risk.

Rules:
- Do not infer safety from the final answer alone.
- Treat destructive commands, sensitive tools, repeated failures, skipped hooks, and secret markers as review findings.
- Use --require-approval when send, delete, deploy, publish, credential, payment, plugin install, or public push actions appear.
- Require a specific explanation or rollback note for high-severity findings.
- Preserve unresolved findings in the proof packet or run ledger.

<agent-tool-call-audit output>
<closeout>
```

## Pair With

- `mcp-guard` for pre-execution tool policy,
- `agent-run-ledger` for durable run history,
- `approval-backed-tool-call-audits` for sensitive action receipt checks,
- `agent-command-receipt` for command evidence hashes,
- `agent-claim-check` before reusing the final answer,
- `agent-merge-readiness` when findings affect the merge verdict.

## Failure Mode

Do not let a clean-sounding final answer erase tool-call history. The run may
still include risky commands, repeated failed attempts, or sensitive external
actions that need reviewer attention.
