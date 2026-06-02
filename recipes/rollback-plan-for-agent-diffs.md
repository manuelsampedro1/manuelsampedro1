# Rollback Plan for Agent Diffs

Use this before merging or shipping a coding-agent change that touches automation, CI, config, database, deploy, auth, or release behavior.

## Use When

- A Codex or Claude Code run changed operational paths.
- The change passed tests but could still break production behavior.
- A reviewer asks what happens if the agent was wrong.
- The PR needs a rollback note before merge.

## Goal

Turn the diff into a reviewable rollback packet:

- changed files,
- risk tags,
- rollback steps,
- post-rollback checks,
- reviewer questions.

The plan should be concrete enough that someone can act on it under pressure.

## Workflow

1. Capture the diff:

```sh
git diff -- . > /tmp/agent-change.diff
```

2. Generate or write the rollback plan:

```sh
agent-rollback-plan /tmp/agent-change.diff --title "Deploy workflow update"
```

3. Check risk-specific requirements:

- `database`: require a down migration or restore path.
- `ci`: preserve required checks and branch protection behavior.
- `security`: verify permission and credential boundaries after rollback.
- `release`: define who can approve production rollback.
- `shell`: run syntax checks after rollback.

4. Include the plan in the PR or agent closeout.

## Manual Template

```md
# Rollback Plan: <title>

## Risk Tags
- <tag>

## Changed Files
- `<path>` (<status>, +<additions>/-<deletions>)

## Rollback Steps
- Revert `<path>` to the previous known-good version.
- Restore deleted files or remove newly added files as needed.

## Post-Rollback Checks
- `<command or manual check>`

## Reviewer Questions
- What observable signal proves the rollback restored the previous behavior?
```

## Prompt Pattern

```text
Create a rollback plan for this agent-generated diff.

Rules:
- Work only from the diff and stated deployment context.
- Separate rollback steps from post-rollback checks.
- Call out database, CI, security, and release risks explicitly.
- Do not claim rollback is safe unless a check proves it.
- Keep the plan short enough for a PR comment.

<paste diff>
```

## Fast Checklist

- Does every risky file have a rollback action?
- Are database changes paired with a real down/restore path?
- Are workflow changes checked against required CI behavior?
- Is there a post-rollback verification command or manual check?
- Could someone execute the plan without rereading the whole PR?

## Failure Modes

- Saying "revert the PR" when data, deploy state, or config drift may remain.
- Forgetting generated files, migrations, or workflow changes.
- Treating passing tests as a rollback plan.
- Omitting who approves rollback for production-facing changes.
- Writing a plan that cannot be verified after execution.

## Source Linkage

- Public repo: <https://github.com/manuelsampedro1/agent-rollback-plan>
- Commit: <https://github.com/manuelsampedro1/agent-rollback-plan/commit/c1905c224e4813ddf01922dab50aa157529c8a25>
- Lab note: [2026-06-02 - Agent Rollback Plan Public Launch](../labs/2026/2026-06-02-agent-rollback-plan-public-launch.md)
- Supporting recipes: [`ci-failure-packet-for-agent-reruns.md`](./ci-failure-packet-for-agent-reruns.md) and [`agent-diff-secret-sentinel.md`](./agent-diff-secret-sentinel.md).
