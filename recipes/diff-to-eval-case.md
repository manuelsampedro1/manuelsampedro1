# Diff to Eval Case

Use this when a coding-agent run produces a useful diff that should become a future regression case instead of disappearing into chat history.

## Use When

- A Codex or Claude Code run exposed a repeatable failure mode.
- A review found missing verification, unsafe scope, or weak assumptions.
- A fix touched files whose risk can be described from the diff.
- You want future agents to be tested against real examples from your own repos.

## Goal

Convert a real diff into a small JSON evaluation case with enough structure to rerun, review, or score later.

The case should preserve:

- the task title,
- the agent objective,
- changed files,
- risk tags,
- expected outcome,
- suggested verification checks,
- notes about what made the run valuable.

## Workflow

1. Capture the diff before it is lost:

```sh
git diff -- . > /tmp/current-run.diff
```

2. Name the behavior the next agent should prove:

```text
The agent should block unrelated public-path changes before publishing.
```

3. Classify the changed files:

```text
scripts/commit_daily_update.sh -> shell, automation
docs/automation-runbook.md -> documentation
```

4. Add the smallest checks that would catch a bad repeat:

```sh
bash -n scripts/commit_daily_update.sh
scripts/commit_daily_update.sh "test: expected path guard" <expected-path>
```

5. Save the case as JSON:

```json
{
  "schema_version": "diff-to-eval.v1",
  "title": "Expected path publish guard",
  "objective": "Block unrelated public-path changes before publishing.",
  "changed_files": [
    {
      "path": "scripts/commit_daily_update.sh",
      "status": "modified",
      "additions": 12,
      "deletions": 4
    }
  ],
  "risk_tags": ["shell", "automation"],
  "suggested_checks": ["bash -n scripts/commit_daily_update.sh"],
  "expected_outcome": "Unexpected public-path changes fail before generated indexes are refreshed."
}
```

## Prompt Pattern

```text
Turn this agent-run diff into a reusable eval case.

Inputs:
- task title: <title>
- original objective: <objective>
- diff: <paste or path>
- important failure mode: <what should future agents catch?>

Tasks:
1. Extract changed files with additions/deletions when possible.
2. Infer lightweight risk tags from paths and file types.
3. Propose the smallest verification commands or manual checks.
4. Write one JSON eval case.
5. Do not claim the eval covers behavior that the diff does not expose.
```

## Fast Checklist

- Does the case point to a real diff?
- Is the expected outcome observable?
- Are suggested checks specific enough to run?
- Are risk tags boring and reviewable rather than overfit?
- Could this case catch a future weak agent run?

## Failure Modes

- Turning every diff into an eval, including uninteresting formatting churn.
- Writing broad expected outcomes that no command could prove.
- Storing private repo context or secrets in the case.
- Treating inferred risk tags as security analysis.
- Forgetting to connect the case back to the original task objective.

## Source Linkage

- Public repo: <https://github.com/manuelsampedro1/diff-to-eval>
- Commit: <https://github.com/manuelsampedro1/diff-to-eval/commit/bd196719a29db55f99aec3640d20f12916d2801a>
- Lab note: [2026-06-02 - Diff to Eval Public Launch](../labs/2026/2026-06-02-diff-to-eval-public-launch.md)
- Supporting recipes: [`verification-by-change-type.md`](./verification-by-change-type.md) and [`real-diff-to-recipe.md`](./real-diff-to-recipe.md).
