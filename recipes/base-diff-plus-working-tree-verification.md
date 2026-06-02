# Base Diff Plus Working Tree Verification

Use this when a repo has committed changes against a base ref and current local edits in the same agent session.

## Goal

Generate one verification checklist that covers both the committed diff and any staged, unstaged, or untracked follow-up work. This avoids closing an agent run with checks that only cover half of the actual change set.

## Source Event

This recipe came from `verify-by-change` commit `1d38d6264dd1`, which added `--include-working-tree` for base-ref scans.

Relevant files:

- `verify_by_change.py`
- `tests/test_verify_by_change.py`
- `README.md`
- `DECISIONS.md`

## Workflow

1. Decide whether the review target is a base ref, the working tree, or both.
2. Use the plain base-ref mode when CI or PR tooling should only inspect committed changes.
3. Use the merged mode when an agent session includes committed work and local follow-ups.
4. Collect paths from `git diff --name-only <base>...HEAD`.
5. Collect paths from `git status --porcelain --untracked-files=all`.
6. De-duplicate paths while preserving first occurrence.
7. Classify the merged path list into verification categories.

## Checklist

- Are committed and uncommitted changes both part of the handoff?
- Is the merged mode explicit rather than changing base-ref behavior silently?
- Are untracked files included?
- Are duplicate paths shown once?
- Does CLI coverage prove the flag works through the user-facing command?
- Does the final checklist still render in the same format downstream tools expect?

## Verification

For `verify-by-change`:

```sh
python3 -m py_compile verify_by_change.py
python3 -m unittest discover -s tests
python3 verify_by_change.py --repo . --base origin/main --include-working-tree --output /tmp/verification-checklist.md
test -s /tmp/verification-checklist.md
```

If the repo does not have `origin/main`, use a local tag, branch, or `HEAD` for a smoke check:

```sh
python3 verify_by_change.py --repo . --base HEAD --include-working-tree
```

## Failure Modes

- Treating `--base` as if it automatically sees local uncommitted edits.
- Scanning only the working tree and missing committed PR changes.
- Emitting duplicate checklist entries for files changed in both places.
- Making merged mode implicit and surprising CI users.
- Forgetting untracked files, which are common in Codex sessions.

## Source Linkage

- Public repo: <https://github.com/manuelsampedro1/verify-by-change>
- Commit: <https://github.com/manuelsampedro1/verify-by-change/commit/1d38d6264dd11c7e3b0e0f2bab2dbc015a19886c>
- CI run: <https://github.com/manuelsampedro1/verify-by-change/actions/runs/26793937990>
