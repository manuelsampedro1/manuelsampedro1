# Agent Diff Budget

Use this before accepting a coding-agent diff that might be too broad for one review pass.

## Use When

- A coding agent touched multiple files or risk categories.
- A task started small but the diff grew during implementation.
- Reviewers need a hard stop before broad diffs become normal.
- You want review budgets that are explicit instead of vibes-based.

## Goal

Turn a unified diff into a budget packet:

- changed file count,
- additions, deletions, and total changed lines,
- high-risk file count,
- path-level risk tags,
- budget failures,
- reviewer questions.

This does not replace review. It forces oversized changes to be split, justified, or escalated before a handoff sounds cleaner than the diff really is.

## Workflow

1. Capture the current diff:

```sh
git diff -- . > /tmp/agent-change.diff
```

2. Run a strict budget for normal agent work:

```sh
PYTHONPATH=src python3 -m agent_diff_budget /tmp/agent-change.diff \
  --max-files 6 \
  --max-total 350 \
  --max-high-risk-files 2
```

3. For autonomous or risky tasks, tighten the budget:

```sh
PYTHONPATH=src python3 -m agent_diff_budget /tmp/agent-change.diff \
  --max-files 3 \
  --max-total 120 \
  --max-high-risk-files 1 \
  --format json
```

4. If blocked, choose one action:

- split the diff into smaller commits or PRs,
- rerun the agent with a narrower task contract,
- add explicit rationale for why this broad diff is still reviewable,
- escalate high-risk files into rollback, secret, and runbook gates.

5. Attach structured proof-packet evidence when checks exist for the same diff:

```sh
PYTHONPATH=src python3 -m agent_diff_budget /tmp/agent-change.diff \
  --max-files 6 \
  --max-total 350 \
  --max-high-risk-files 2 \
  --proof-packet /tmp/proof-packet.json \
  --format json
```

## Prompt Pattern

```text
Review this coding-agent diff against a strict change budget.

Rules:
- Count changed files, additions, deletions, total changed lines, and high-risk files.
- Treat CI, database, deploy, security, config, and AGENTS.md/runbook files as high risk.
- If the diff is over budget, ask how it can be split before reviewing details.
- Do not let passing tests justify an oversized diff.
- Return the exact budget failures and reviewer questions.

<paste diff>
```

## Fast Checklist

- Is the diff small enough for a human to inspect without skipping files?
- Did high-risk files stay under the explicit threshold?
- Are tests, rollback, and runbook checks proportional to the risk tags?
- Would splitting the diff improve review quality without losing context?
- Does the final proof packet mention budget failures or the reason the budget was relaxed?
- If a proof packet is attached, does it match the same diff without removing
  budget failures?

## Failure Modes

- Accepting a giant diff because the agent produced a polished closeout.
- Letting documentation, CI, config, and product changes ship in one mixed review.
- Relaxing budgets silently instead of recording why.
- Treating a passing proof packet as permission to exceed file, line, or
  high-risk limits.
- Counting only files and missing line volume.
- Counting only line volume and missing one high-risk file.

## Source Linkage

- Repo / tool / workflow: [`agent-diff-budget`](https://github.com/manuelsampedro1/agent-diff-budget), public commit [`c336a9b`](https://github.com/manuelsampedro1/agent-diff-budget/commit/c336a9b41858800002d4d47d34f99b75500faf73), [`README`](https://raw.githubusercontent.com/manuelsampedro1/agent-diff-budget/main/README.md), [`CLI`](https://raw.githubusercontent.com/manuelsampedro1/agent-diff-budget/main/src/agent_diff_budget/cli.py), [`tests`](https://raw.githubusercontent.com/manuelsampedro1/agent-diff-budget/main/tests/test_cli.py), [`proof packet`](https://raw.githubusercontent.com/manuelsampedro1/agent-diff-budget/main/examples/proof-packet.json), [`small example`](https://raw.githubusercontent.com/manuelsampedro1/agent-diff-budget/main/examples/small.diff), and [`large example`](https://raw.githubusercontent.com/manuelsampedro1/agent-diff-budget/main/examples/large.diff).
- Supporting prompt, script, or note: [`./proof-packet-backed-diff-budgets.md`](./proof-packet-backed-diff-budgets.md), [`./scope-guard-for-agent-diffs.md`](./scope-guard-for-agent-diffs.md), [`./change-risk-matrix-for-agent-diffs.md`](./change-risk-matrix-for-agent-diffs.md), [`./agent-proof-packet-for-review.md`](./agent-proof-packet-for-review.md), [`../labs/2026/2026-06-03-agent-diff-budget-proof-packets.md`](../labs/2026/2026-06-03-agent-diff-budget-proof-packets.md), and [`../labs/2026/2026-06-02-agent-diff-budget-public-launch.md`](../labs/2026/2026-06-02-agent-diff-budget-public-launch.md).
