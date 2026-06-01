# Scope Guard for Agent Diffs

Use this when a coding-agent task has an explicit file or module boundary.

## Use When

- The task should only touch a narrow set of files.
- The agent may be tempted to update docs, config, tests, or unrelated helpers.
- A publish script stages broad directories.
- You need CI to fail if the diff exceeds the task contract.

## Goal

Fail fast when changed paths fall outside the declared scope.

The scope should be explicit enough to review:

- exact files,
- directory globs,
- generated files that are allowed,
- known exclusions.

## Workflow

1. Declare allowed paths before the agent starts:

```text
src/billing/**
tests/billing/**
docs/billing-runbook.md
```

2. Save them in a scope file:

```sh
cat > /tmp/agent-scope.txt <<'EOF'
src/billing/**
tests/billing/**
docs/billing-runbook.md
EOF
```

3. Check the diff:

```sh
git diff -- . | agent-scope-guard - --allow-file /tmp/agent-scope.txt
```

4. For staged changes:

```sh
git diff --cached --name-only | agent-scope-guard - --paths-only --allow-file /tmp/agent-scope.txt
```

5. Treat unexpected paths as blockers unless the task contract is updated deliberately.

## Prompt Pattern

```text
Enforce this coding-agent task scope.

Allowed paths:
- <path or glob>

Tasks:
1. Inspect the current diff path list.
2. Separate allowed paths from unexpected paths.
3. Block the run if unexpected paths exist.
4. Do not silently widen scope; explain why each new path is necessary.
```

## Fast Checklist

- Was the allowed path list declared before implementation?
- Are generated files included explicitly?
- Does the guard inspect paths from the actual diff?
- Did unexpected files block the run?
- Was any scope expansion reviewed as a product or engineering decision?

## Failure Modes

- Allowing an entire repo because exact scope is inconvenient.
- Adding README or docs changes after the fact without scope review.
- Checking only staged paths when the worktree has other dirty files.
- Treating tests as automatically allowed for every task.
- Letting the commit script stage whole directories without a preflight.

## Source Linkage

- Repo / tool / workflow: local `agent-scope-guard` prototype and this profile repo's expected-path publish guard.
- Supporting prompt, script, or note: [`./dirty-public-path-preflight.md`](./dirty-public-path-preflight.md), [`./expected-paths-contract-for-agent-publish-flows.md`](./expected-paths-contract-for-agent-publish-flows.md), and [`../scripts/commit_daily_update.sh`](../scripts/commit_daily_update.sh).

