# Change Risk Matrix for Agent Diffs

Use this before choosing which gates a coding-agent diff must pass.

## Use When

- A task changed more than one kind of file.
- The diff touches CI, deploy, database, auth, config, scripts, or runbooks.
- A reviewer needs to decide whether normal tests are enough.
- You want consistent pre-merge gates instead of ad hoc review instincts.

## Goal

Turn a diff into a short risk packet:

- changed files,
- risk tags,
- risk level,
- required gates,
- reviewer questions.

This keeps low-risk changes lightweight and makes high-risk changes prove scope, safety, rollback, and closeout evidence.

## Workflow

1. Capture the current diff:

```sh
git diff -- . > /tmp/agent-change.diff
```

2. Classify the change:

```sh
agent-change-risk /tmp/agent-change.diff --title "Deploy workflow update"
```

3. Run the gates suggested by the packet:

```sh
agent-scope-guard - --allow-file /tmp/expected-paths.txt < /tmp/agent-change.diff
agent-secret-sentinel /tmp/agent-change.diff
agent-rollback-plan /tmp/agent-change.diff --title "Deploy workflow update"
agent-closeout-check /tmp/agent-closeout.md
```

4. If CI fails, package the retry context:

```sh
agent-ci-failure-packet /tmp/ci.log --title "Deploy workflow update"
```

5. If the failure mode should become reusable, save an eval case:

```sh
diff-to-eval /tmp/agent-change.diff --title "Deploy workflow update" --format json
```

## Risk Tags

- `security`: auth, permissions, tokens, secrets, or access behavior.
- `database`: migrations, schema, SQL, data movement, or persistence.
- `release`: deploy, production, rollout, or packaging paths.
- `ci`: GitHub Actions, workflow config, checks, or automation scripts.
- `configuration`: TOML, JSON, YAML, env, config, or policy files.
- `documentation`: README, runbooks, AGENTS.md, or operational docs.
- `tests`: tests changed, added, or removed.

## Gate Matrix

| Risk | Required gate |
| --- | --- |
| Any non-trivial diff | `agent-scope-guard` |
| Security or config | `agent-secret-sentinel` |
| CI or operational docs | `runbook-drift-check` |
| CI failure | `agent-ci-failure-packet` |
| Database, release, or high risk | `agent-rollback-plan` |
| Medium or high risk | `diff-to-eval` |
| Final handoff | `agent-closeout-check` |

## Prompt Pattern

```text
Classify this coding-agent diff before merge.

Rules:
- Identify changed files and risk tags.
- Choose a risk level: low, medium, or high.
- Recommend only gates that match the actual risk.
- Include reviewer questions for scope, secrets, rollback, CI, and closeout evidence.
- Do not treat passing tests as enough for operational, security, or release changes.

<paste diff>
```

## Fast Checklist

- Does the risk packet explain why each gate is required?
- Are scope and secret checks run before commit or publication?
- Does high-risk work include rollback and post-rollback checks?
- Does CI failure context become a compact retry packet?
- Does the final answer pass an evidence check?

## Failure Modes

- Running every gate on every change until the process becomes noise.
- Running only tests on changes that alter deploy, permissions, config, or data.
- Generating rollback text after merge instead of before review.
- Saving eval cases only from artificial examples instead of real diffs.
- Accepting a confident closeout without exact files and verification commands.

## Source Linkage

- Repo / tool / workflow: [`agent-change-risk`](https://github.com/manuelsampedro1/agent-change-risk), public commit [`49dc92d`](https://github.com/manuelsampedro1/agent-change-risk/commit/49dc92d624906a9523af60188b3a30936a79037e), [`README`](https://raw.githubusercontent.com/manuelsampedro1/agent-change-risk/main/README.md), [`CLI`](https://raw.githubusercontent.com/manuelsampedro1/agent-change-risk/main/src/agent_change_risk/cli.py), [`tests`](https://raw.githubusercontent.com/manuelsampedro1/agent-change-risk/main/tests/test_cli.py), and [`sample diff`](https://raw.githubusercontent.com/manuelsampedro1/agent-change-risk/main/examples/sample.diff).
- Supporting prompt, script, or note: [`./scope-guard-for-agent-diffs.md`](./scope-guard-for-agent-diffs.md), [`./agent-diff-secret-sentinel.md`](./agent-diff-secret-sentinel.md), [`./rollback-plan-for-agent-diffs.md`](./rollback-plan-for-agent-diffs.md), [`./closeout-evidence-check-for-agents.md`](./closeout-evidence-check-for-agents.md), and [`../labs/2026/2026-06-02-agent-change-risk-public-launch.md`](../labs/2026/2026-06-02-agent-change-risk-public-launch.md).
