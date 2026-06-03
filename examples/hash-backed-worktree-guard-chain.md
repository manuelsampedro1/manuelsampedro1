# Hash-Backed Worktree Guard Chain

Use this example when a reviewer needs to prove that a post-agent worktree
guard checked the same dirty-tree snapshot captured before the agent run.

## Scenario

A repository already has `notes/user-draft.md` modified by the user. The agent
is allowed to touch only `src/**` and `tests/**`. The pre-run snapshot must not
be silently edited before the final worktree check.

## Command Chain

Capture the pre-agent snapshot and its digest:

```sh
PYTHONPATH=/path/to/agent-worktree-guard/src \
  python3 -m agent_worktree_guard snapshot \
  --output /tmp/pre-agent-snapshot.json \
  > /tmp/pre-agent-snapshot.receipt.txt
```

Record the printed `Snapshot SHA-256` in the handoff or ledger.

Run the post-agent guard with that digest:

```sh
PYTHONPATH=/path/to/agent-worktree-guard/src \
  python3 -m agent_worktree_guard check /tmp/pre-agent-snapshot.json \
  --expect-snapshot-sha256 "<snapshot-sha256>" \
  --allow "src/**" \
  --allow "tests/**" \
  --format json
```

## Expected Signals

- If the snapshot file changed, the command exits before comparing paths.
- If `notes/user-draft.md` drifted, the verdict is blocked.
- If a new dirty path appears outside `src/**` or `tests/**`, the verdict is
  blocked.
- If only allowed paths changed and the snapshot hash matches, the verdict can
  pass.
- The report includes `snapshot_sha256` for downstream evidence.

## Reviewer Interpretation

The snapshot hash connects the pre-run dirty-tree baseline to the post-run
guard result. It does not authorize extra paths; it only proves the guard used
the expected baseline artifact before applying the allowlist.
