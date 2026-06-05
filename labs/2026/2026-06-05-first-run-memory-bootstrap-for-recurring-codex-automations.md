# 2026-06-05 - First-Run Memory Bootstrap for Recurring Codex Automations

## Context

This recurring GitHub lab-note run now expects automation memory before it
chooses a new artifact, but the actual memory file for this automation did not
exist at the start of the run.

That made the workflow concrete instead of theoretical: the repo already had a
public recipe for recurring automation memory, but the live automation still
started from zero state and could have repeated yesterday's theme.

## Useful Artifact

Treat a missing automation memory file as a first-run bootstrap event, not as a
normal steady-state run.

For a recurring Codex automation, the minimum bootstrap contract is:

- read the memory path first,
- if it is missing, record that as an operational gap,
- choose an artifact that does not repeat the newest public theme,
- write back the artifact path, verification, and next gap before closeout.

That keeps the first run honest and makes the second run cheaper.

## Source Linkage

- Repo / tool / workflow: this profile repo's recurring GitHub artifact flow
- Supporting prompt, script, or file:
  [`../../recipes/automation-memory-for-recurring-codex-runs.md`](../../recipes/automation-memory-for-recurring-codex-runs.md),
  [`../../docs/automation-runbook.md`](../../docs/automation-runbook.md),
  and [`../../TODO.md`](../../TODO.md)

## Notes

- Observation: reading `$CODEX_HOME/automations/github-ai-lab-note/memory.md`
  returned `__MISSING__` at the start of this run, so there was no persisted
  artifact summary, changed-path list, or next-step guidance.
- Observation: the repo's newest recipe was already
  [`Automation Memory for Recurring Codex Runs`](../../recipes/automation-memory-for-recurring-codex-runs.md),
  which means the workflow guidance existed before the automation state did.
- Tradeoff: bootstrapping memory adds one more write step at the end of the
  run, but it removes redundant rediscovery on every later run.
- Failure mode: if a recurring automation treats missing memory as harmless, it
  can keep publishing adjacent notes from fresh context each day without
  carrying forward what was already verified or what gap still matters.

## Verification

Checked locally for this run:

- read the expected memory path before topic selection and confirmed it was
  absent,
- reviewed the repo guidance and current public indexes before choosing the
  note,
- inspected recent commits and confirmed the latest public artifact was the
  recipe
  [`Automation Memory for Recurring Codex Runs`](../../recipes/automation-memory-for-recurring-codex-runs.md),
  which made a repeated memory-themed recipe a bad follow-up,
- refreshed [`../../labs/README.md`](../../labs/README.md) after adding this
  note so the archive index reflected the new dated entry.

## Next Step

Backfill or bootstrap memory files for the other recurring GitHub automations
so the memory pattern is enforced by practice, not only documented in public
recipes.
