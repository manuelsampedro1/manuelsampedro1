# Copy-Paste Start Packet for Codex

Use this when Codex, Claude Code, or another coding agent is about to make a
real repo change and the request is still spread across chat, docs, and local
assumptions.

## Goal

Give the agent one Markdown packet that is narrow enough to execute and strong
enough to review later.

This pattern combines four things that usually drift apart:

- explicit acceptance criteria with stable IDs;
- allowed scope and stop conditions;
- inspectable evidence pointers for task, repo, and context readiness;
- exact verification commands.

## Copy-Paste Packet

```md
# Agent Start Packet

## Objective
Ship one narrow outcome:
<one sentence with the user-visible result>

## Acceptance Criteria
- AC-1: <observable behavior or output>
- AC-2: <observable behavior or output>
- AC-3: <verification or safety condition>

## Allowed Scope
- Edit only: <exact paths or globs>
- Read as needed: <exact paths or globs>
- Do not change: <exact paths, systems, or product areas>

## Inputs
- Task contract: `docs/tasks/<task>.md`
- Repo map: `reports/repo-map.md`
- Repo readiness: `repo-flightcheck --strict --threshold 80`
- Context scan: `reports/context-audit.md`

## Evidence Pointers
- Task evidence: `docs/tasks/<task>.md`
- Repo evidence: `reports/repo-flightcheck.json`
- Context evidence: `reports/context-audit.md`
- Dirty-tree baseline: `reports/worktree-snapshot.json`

## Worktree
- Branch: `<branch-name>`
- Base commit: `<sha>`
- Pre-existing changes: `git status --short`

## Verification
- `make test`
- `make lint`
- `git diff --check`

## Stop Conditions
- Stop if the fix needs credentials, deploy access, or production data.
- Stop if the required change expands beyond `Allowed Scope`.
- Stop if the same error appears twice without a new hypothesis.
- Stop if verification fails and the failure is not explained by the task.
```

## Workflow

1. Write the objective as one outcome, not a task list.
2. Turn acceptance bullets into stable IDs such as `AC-1`, `AC-2`, and `AC-3`.
3. List exact allowed paths before the agent reads the whole repo.
4. Add one inspectable pointer each for task evidence, repo evidence, and
   context evidence.
5. Record the current branch, base commit, and dirty-tree state before edits.
6. Replace placeholder verification with the exact commands the repo actually
   uses.
7. Add stop conditions that force escalation on scope growth, repeated failure,
   secrets, or unclear verification.
8. Give the packet to the agent as the top-level instruction, not as an
   appendix after a long chat transcript.

## Evaluation Pattern

Score each item `0` or `1`:

- Single objective: one outcome, not multiple unrelated asks.
- Acceptance IDs: every criterion has a stable `AC-N` label.
- Scope boundary: allowed and forbidden paths are explicit.
- Evidence pointers: task, repo, and context each point somewhere inspectable.
- Worktree state: branch, base commit, and pre-existing changes are visible.
- Verification: commands are exact and runnable in this repo.
- Stop conditions: at least one rule covers scope drift or sensitive access.

`7`: ready to hand off.
`5-6`: tighten the weak sections before the run.
`0-4`: do not start the agent yet.

## Optional Tool Check

If you use the related tools, validate the packet before handoff:

```sh
agent-task-contract check AGENT_TASK.md --require-acceptance-ids
agent-start-gate check AGENT_START.md --require-evidence-pointers
```

If the repo starts dirty, preserve a reusable baseline first:

```sh
agent-worktree-guard snapshot --output /tmp/worktree-snapshot.json
```

## Failure Modes

- Treating a long prompt as proof that scope is clear.
- Using anonymous acceptance bullets that later traces cannot reference.
- Writing `pass` or `verified` with no file, command, report, or commit behind
  it.
- Hiding pre-existing dirty files until the agent appears to have changed them.
- Letting the agent invent verification because the packet only says
  `run tests if needed`.

## Source Linkage

- Supporting recipes: [`./stable-acceptance-criteria-ids.md`](./stable-acceptance-criteria-ids.md),
  [`./traceable-start-packets.md`](./traceable-start-packets.md),
  [`./hash-backed-worktree-snapshots.md`](./hash-backed-worktree-snapshots.md),
  and [`./concrete-grounding-pointers.md`](./concrete-grounding-pointers.md).
- Supporting notes: [`../labs/2026/2026-06-03-agent-task-contract-acceptance-ids.md`](../labs/2026/2026-06-03-agent-task-contract-acceptance-ids.md),
  [`../labs/2026/2026-06-03-agent-start-gate-evidence-pointers.md`](../labs/2026/2026-06-03-agent-start-gate-evidence-pointers.md),
  [`../labs/2026/2026-06-03-agent-worktree-guard-snapshot-hashes.md`](../labs/2026/2026-06-03-agent-worktree-guard-snapshot-hashes.md),
  and [`../labs/2026/2026-06-03-agent-source-grounding-concrete-pointers.md`](../labs/2026/2026-06-03-agent-source-grounding-concrete-pointers.md).
