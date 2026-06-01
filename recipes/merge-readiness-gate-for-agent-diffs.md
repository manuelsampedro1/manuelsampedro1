# Merge Readiness Gate for Agent Diffs

Use this after a coding-agent change has been implemented but before accepting the handoff or merging.

## Use When

- The agent says the task is done.
- The diff touches CI, deploy, database, auth, config, scripts, or runbooks.
- Some checks passed, but reviewer confidence still depends on missing context.
- You need a repeatable `ready`, `needs-review`, or `blocked` decision.

## Goal

Separate merge readiness from agent confidence.

The gate should produce:

- changed files,
- risk level,
- passing checks,
- blocking findings,
- missing evidence,
- reviewer questions,
- final verdict.

## Workflow

1. Capture the diff:

```sh
git diff -- . > /tmp/agent-change.diff
```

2. Save the agent closeout if one exists:

```sh
pbpaste > /tmp/agent-closeout.md
```

3. Run readiness with explicit evidence:

```sh
agent-merge-readiness /tmp/agent-change.diff \
  --title "Deploy workflow migration" \
  --check "scope guard:pass" \
  --check "unit tests:pass" \
  --check "secret scan:pass" \
  --check "runbook drift:pass" \
  --check "rollback plan:pass" \
  --closeout /tmp/agent-closeout.md
```

4. Treat the verdict strictly:

| Verdict | Action |
| --- | --- |
| `ready` | Reviewer can proceed to normal code review and merge policy. |
| `needs-review` | Produce the missing evidence before merge. |
| `blocked` | Fix the failed check or rerun the agent with failure context. |

## Evidence Rules

- Any failed check blocks the merge.
- Every agent diff needs scope evidence.
- Code changes need a passing test or CI check.
- Security or config changes need secret-scan evidence.
- CI or docs changes need runbook/workflow evidence.
- Database, release, or high-risk changes need rollback evidence.
- Medium and high-risk changes need a closeout with files, verification, and risks.

## Prompt Pattern

```text
Evaluate this coding-agent change for merge readiness.

Rules:
- Work from the diff, explicit check results, and closeout evidence only.
- Return one verdict: ready, needs-review, or blocked.
- Treat failed checks as blockers.
- Treat missing scope, test, secret, runbook, rollback, or closeout evidence as not ready.
- Do not accept confident language as evidence.

<paste diff, checks, and closeout>
```

## Fast Checklist

- Are all check results explicit, not implied?
- Does the closeout name changed files?
- Does it include exact verification commands or checks?
- Does it state risks, limitations, or checks not run?
- Is rollback evidence present for high-risk changes?
- Would a reviewer know why the verdict was chosen?

## Failure Modes

- Calling a change ready because the agent's final answer sounded confident.
- Accepting "tests pass" without the exact command or CI link.
- Ignoring failed checks because the diff looks small.
- Treating rollback text as optional for database, release, or high-risk changes.
- Merging before missing evidence is resolved.

## Source Linkage

- Repo / tool / workflow: local `agent-merge-readiness` prototype at `/Users/manuelsampedro/Documents/Codex/2026-05-21/agent-merge-readiness`.
- Supporting prompt, script, or note: [`./change-risk-matrix-for-agent-diffs.md`](./change-risk-matrix-for-agent-diffs.md), [`./closeout-evidence-check-for-agents.md`](./closeout-evidence-check-for-agents.md), and [`./scope-guard-for-agent-diffs.md`](./scope-guard-for-agent-diffs.md).
