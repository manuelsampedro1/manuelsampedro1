# Agent PR Brief

Use this before posting or relying on an agent-generated pull-request
description.

## Source

- Public tool: https://github.com/manuelsampedro1/agent-pr-brief
- Launch note: [2026-06-02 - Agent PR Brief Public Launch](../labs/2026/2026-06-02-agent-pr-brief-public-launch.md)

## Pattern

1. Generate a unified diff:

```sh
git diff main...HEAD > /tmp/pr.diff
```

2. Audit the PR description:

```sh
agent-pr-brief pr-description.md --diff /tmp/pr.diff --min-score 80
```

3. Fail on review-surface blockers:

```sh
agent-pr-brief pr-description.md --diff /tmp/pr.diff --fail-on medium
```

4. Attach the report to a proof packet or ledger:

```sh
agent-pr-brief pr-description.md --diff /tmp/pr.diff --write-report /tmp/pr-brief-audit.md
```

## What Good Looks Like

- Summary, changes, verification, risks, and follow-up are explicit.
- Main changed files or directories are mentioned.
- CI, script, deploy, auth, security, billing, dependency, and config changes
  are called out as reviewer notes.
- Verification includes command or CI evidence, not just "tests passed".
- Broad diffs include scope, review order, or split rationale.
- Vague words are replaced with concrete behavior, files, and evidence.

## Prompt Pattern

```text
Rewrite this PR description so it matches the actual diff.

Rules:
- Mention the main changed files or directories.
- Call out risky paths and reviewer focus areas.
- Include exact verification commands, outputs, reports, or CI runs.
- Avoid vague language such as "misc", "various", "probably", or "should work".
- Preserve residual risks and follow-up explicitly.

<agent-pr-brief output>
<current PR description>
<diff summary>
```

## Pair With

- `codex-review-packet` when packaging review context,
- `agent-change-risk` when deciding required gates,
- `agent-proof-packet` when preserving evidence,
- `agent-closeout-check` and `agent-claim-check` before final handoff claims.

## Failure Mode

Do not overfit the PR description to mention every file in a large diff. Group
files by directory, risk, or review lane when that is clearer for the reviewer.
