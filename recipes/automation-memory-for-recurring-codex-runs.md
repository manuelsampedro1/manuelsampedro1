# Automation Memory for Recurring Codex Runs

Use this when a recurring Codex or GitHub automation revisits the same repo and should build on prior work instead of rediscovering the same context every run.

## Goal

Keep each run grounded in the last real outcome:

- what was already changed,
- what was verified,
- what theme was already covered,
- what blocker or next step still matters.

The memory should make the next run sharper, not more confident.

## Workflow

1. Read the automation memory before choosing the artifact:

```sh
test -f "$CODEX_HOME/automations/<automation-id>/memory.md" \
  && sed -n '1,160p' "$CODEX_HOME/automations/<automation-id>/memory.md"
```

2. Read the repo guidance and the current public surfaces that define quality:

```sh
sed -n '1,220p' README.md
sed -n '1,220p' docs/profile-strategy.md
sed -n '1,220p' docs/automation-runbook.md
sed -n '1,220p' recipes/README.md
```

3. Inspect the newest labs or recipes so the run does not publish the same lesson twice:

```sh
ls -1t labs/2026/*.md | head -n 5
ls -1t recipes/*.md | head -n 10
```

4. Pick one concrete gap that is both:

- consistent with the repo strategy,
- different from the last run summary in memory.

5. Create exactly one reusable artifact, then run the smallest verification that matches the diff.

6. Update the memory at the end with:

- artifact created,
- exact changed paths,
- verification run,
- remaining blocker or next useful follow-up.

## Prompt Pattern

```text
You are continuing a recurring Codex automation in the same repo.

Rules:
- Read the automation memory first.
- Do not repeat the last run's artifact unless you are materially improving it.
- Re-read the repo README, strategy docs, and the relevant public index before deciding what to publish.
- Prefer one concrete artifact over broad cleanup.
- Record exact changed paths, verification, and the next unresolved gap back into memory before closing.

Output:
- one artifact another builder can reuse,
- honest verification notes,
- an updated memory entry for the next run.
```

## Fast Checklist

- Did the run read the memory before choosing the topic?
- Did the new artifact avoid the last run's theme or clearly deepen it?
- Did the artifact link back to a real repo file, script, lab, decision, or workflow?
- Did the verification fit the changed file types instead of using a generic test claim?
- Did the memory capture exact paths and the next unresolved step?

## Failure Modes

- Treating memory as source of truth instead of as a pointer to fresh repo context.
- Repeating yesterday's artifact because the memory was skipped.
- Writing vague memory such as `updated recipe` instead of naming the file and check run.
- Copying stale blockers into the next run after the repo already changed.
- Closing the run without writing back what changed, which forces the next automation to rediscover the same context.

## Source Linkage

- Repo / tool / workflow: this profile repo's recurring GitHub automation flow.
- Supporting prompt, script, or note: [`../docs/codex-priority-topics.md`](../docs/codex-priority-topics.md), [`../docs/automation-runbook.md`](../docs/automation-runbook.md), [`../scripts/commit_daily_update.sh`](../scripts/commit_daily_update.sh), and [`../TODO.md`](../TODO.md).
