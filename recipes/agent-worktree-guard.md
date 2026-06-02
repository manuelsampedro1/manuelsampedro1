# Agent Worktree Guard

Use this when a coding agent must work in a repository that already has user edits.

## Pattern

1. Snapshot the dirty working tree before the agent starts.
2. Give the agent an explicit allowlist for task-owned paths.
3. Check the tree after the run.
4. Block if a protected dirty file disappeared, became clean, changed hash, or if a new dirty path appears outside the allowlist.

## Commands

```sh
agent-worktree-guard snapshot --output /tmp/pre-agent-snapshot.json
agent-worktree-guard check /tmp/pre-agent-snapshot.json --allow "src/**" --allow "tests/**"
```

Use JSON output when another gate needs to consume the verdict:

```sh
agent-worktree-guard check /tmp/pre-agent-snapshot.json --allow "src/**" --format json
```

## When It Fails

- Treat protected-file drift as a stop condition, not a warning.
- Ask whether the user wants the accidental edit preserved, reverted manually, or folded into scope.
- Pair this with `agent-scope-guard` when the diff also needs committed-path enforcement.

Proof repo: [agent-worktree-guard](https://github.com/manuelsampedro1/agent-worktree-guard).
