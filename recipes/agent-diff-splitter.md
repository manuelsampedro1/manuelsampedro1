# Agent Diff Splitter

Use this after a coding-agent diff exceeds the review budget and needs to become smaller, safer slices.

## Use When

- `agent-diff-budget` blocks a broad diff.
- A change mixes auth, migrations, release, automation, tests, app code, and docs.
- A reviewer asks for smaller PRs but the split plan is unclear.
- You want the next agent run to be scoped by concrete file groups.

## Goal

Turn a unified diff into a split plan:

- changed files,
- additions and deletions,
- review lanes,
- proposed split order,
- files per split,
- rationale for each split,
- reviewer question per split.

This makes "split the PR" actionable. The tool does not rewrite commits; it tells the human or agent how to cut the work.

## Workflow

1. Capture the diff:

```sh
git diff -- . > /tmp/agent-change.diff
```

2. Check whether it is too broad:

```sh
PYTHONPATH=src python3 -m agent_diff_budget /tmp/agent-change.diff --max-files 6 --max-total 350
```

3. If blocked, generate the split plan:

```sh
PYTHONPATH=src python3 -m agent_diff_splitter /tmp/agent-change.diff --max-files-per-split 3
```

4. Feed each split into the next agent run:

```text
Implement only split 1 from the split plan.
Allowed files:
<files from split 1>

Do not touch files from later splits.
```

5. Verify each split independently before merging the broader change.

## Prompt Pattern

```text
Split this oversized coding-agent diff into reviewable slices.

Rules:
- Security, data, release, and automation splits come before application code.
- Tests should validate the behavior from earlier splits, not hide risk.
- Product/docs claims should wait until implementation and verification evidence exists.
- Each split needs files, rationale, reviewer question, and suggested order.
- Do not rewrite the diff; produce a plan for smaller follow-up work.

<paste diff>
```

## Fast Checklist

- Are high-risk files isolated before low-risk implementation?
- Can each split be reviewed and verified independently?
- Does each follow-up agent run have expected paths from the split?
- Did docs/public claims move to the final split?
- Does the proof packet preserve the split rationale?

## Failure Modes

- Splitting only by file count and leaving auth plus deploy in the same slice.
- Moving tests before the behavior they are supposed to validate.
- Letting README claims ship before verification.
- Treating a split plan as a substitute for rollback or risk review.
- Asking the next agent to "continue" without giving exact split files.

## Source Linkage

- Public repo: <https://github.com/manuelsampedro1/agent-diff-splitter>
- Commit: <https://github.com/manuelsampedro1/agent-diff-splitter/commit/6554cc05857044bfb63b66a6d7e8719988c86b12>
- README: <https://raw.githubusercontent.com/manuelsampedro1/agent-diff-splitter/main/README.md>
- CLI: <https://raw.githubusercontent.com/manuelsampedro1/agent-diff-splitter/main/src/agent_diff_splitter/cli.py>
- Tests: <https://raw.githubusercontent.com/manuelsampedro1/agent-diff-splitter/main/tests/test_cli.py>
- Mixed diff example: <https://raw.githubusercontent.com/manuelsampedro1/agent-diff-splitter/main/examples/mixed.diff>
- Launch note: [`../labs/2026/2026-06-02-agent-diff-splitter-public-launch.md`](../labs/2026/2026-06-02-agent-diff-splitter-public-launch.md)
- Supporting recipes: [`./agent-diff-budget.md`](./agent-diff-budget.md), [`./agent-review-map.md`](./agent-review-map.md), and [`./agent-proof-packet-for-review.md`](./agent-proof-packet-for-review.md).
