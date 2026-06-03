# Traceable Start Packets

Use this pattern when a coding-agent start packet will feed another agent, run
ledger, review packet, closeout, or public proof note.

## Problem

A start packet can say `pass` for task, repo, and context readiness while
leaving no inspectable trail. That creates a weak pre-run gate: the next agent
sees confidence, but the reviewer cannot inspect the evidence behind it.

## Pattern

Require evidence pointers before allowing the run to start:

```sh
agent-start-gate check AGENT_START.md \
  --require-evidence-pointers \
  --format json \
  > /tmp/start-gate.json
```

Accepted pointer shapes include:

- paths such as `AGENT_TASK.md`, `docs/task.md`, or `reports/context.json`;
- URLs to tickets, reports, runs, or source artifacts;
- commands such as `repo-flightcheck --strict --threshold 80`;
- run ids, commits, receipts, reports, jobs, issues, PRs, or artifact ids.

Treat these as blockers:

- task-contract or request-brief evidence that only says `pass`;
- repo-readiness evidence that only says `pass`;
- context-scan evidence that only says `pass`;
- missing objective, scope, worktree, verification, or stop-condition sections.

## Acceptance Criteria

- The start gate exits `0`.
- `evidence_pointer_required` is `true` in JSON output.
- `evidence_pointer_count` covers the ready task, repo, and context evidence.
- The packet still names allowed scope, out-of-scope work, verification
  commands, and stop conditions.

## Review Rule

Evidence pointers prove the pre-run packet is inspectable. They do not prove
the linked commands actually ran or the referenced artifacts are complete. Use
command receipts, CI runs, run ledgers, or proof packets for those claims.
