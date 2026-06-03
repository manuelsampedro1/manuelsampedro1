# Hash-Backed Worktree Snapshots

Use this pattern when a coding agent starts from a dirty repository and the
pre-agent worktree snapshot will later be reused as evidence.

## Problem

Worktree snapshots are easy to trust too much:

- a snapshot file can be edited after capture;
- a removed dirty-path entry can hide protected user work;
- a later closeout may cite the guard without proving which baseline it used;
- reviewers need a compact way to connect pre-run and post-run evidence.

## Pattern

Capture the dirty tree before the agent starts:

```sh
PYTHONPATH=/path/to/agent-worktree-guard/src \
  python3 -m agent_worktree_guard snapshot \
  --output /tmp/pre-agent-snapshot.json \
  > /tmp/pre-agent-snapshot.receipt.txt
```

Store the printed `Snapshot SHA-256` in the task brief, handoff, or run ledger.

After the agent run, require that exact digest:

```sh
PYTHONPATH=/path/to/agent-worktree-guard/src \
  python3 -m agent_worktree_guard check /tmp/pre-agent-snapshot.json \
  --expect-snapshot-sha256 "<snapshot-sha256>" \
  --allow "src/**" \
  --allow "tests/**" \
  --format json
```

## Acceptance Criteria

- The snapshot digest is captured before the agent edits files.
- The post-run check includes `--expect-snapshot-sha256`.
- A mismatched or invalid digest exits non-zero before the snapshot is trusted.
- The guard still blocks protected-file drift and unexpected dirty paths.
- The JSON or Markdown report includes `snapshot_sha256` so downstream artifacts
  can cite the exact baseline.

## Review Rule

Treat an unhashed snapshot as a weaker baseline. For important dirty-worktree
runs, require the snapshot hash before accepting a worktree guard report as
closeout, ledger, or review-packet evidence.
