# Real Diff to Recipe

Use this when Codex, Claude Code, or another coding agent produced a real repo change and you want to turn that work into one reusable recipe instead of a vague retrospective.

## Use When

- You have a finished diff, commit, or lab note with one concrete lesson.
- The repo changed in a way another builder could copy.
- You want a recipe grounded in evidence, not in generic AI advice.
- The automation should publish one practical artifact under `recipes/`.

## Goal

Extract one narrow reusable pattern from a real change and package it so another builder can apply it in under ten minutes.

Good recipe seeds:

- a verification loop that caught a real failure,
- a prompt pattern that improved repo output,
- a review checklist anchored in actual changed files,
- a small implementation approach that removed repeated friction,
- a failure mode with a clear guardrail.

Reject these as seeds:

- "the repo was improved",
- commit summaries with no reusable method,
- broad AI best practices with no repo evidence,
- notes that only restate what the scripts already say.

## Inputs

- The real changed files or commit range.
- One nearby lab note, issue, or verification log if it explains why the change mattered.
- The actual commands or checks that were run.
- One sentence on who should reuse the pattern.

## Workflow

1. Read the diff before writing prose. Name the smallest behavior that changed.
2. Ask what another builder could copy from that change tomorrow.
3. Reduce the lesson to one pattern only. If the change teaches two ideas, publish one and drop the other.
4. Pull concrete evidence into the recipe: file paths, commands, failure modes, or observed outputs.
5. Write the recipe in four reusable parts:
   - when to use it,
   - the workflow or prompt,
   - the checks,
   - the failure modes.
6. Remove any sentence that would still make sense in an unrelated repo.
7. Verify the supporting command, script, or path still exists before publishing.

## Extraction Questions

Answer these before drafting:

1. What exact repo event created the lesson?
2. Which part is reusable across repos?
3. What evidence makes the pattern believable here?
4. What would a weaker generic version of this recipe say?
5. Which sentence proves this recipe came from work, not from brainstorming?

If you cannot answer `3` or `5`, do not publish the recipe yet.

## Agent Prompt Pattern

```text
Create one reusable recipe from this real repo change.

Inputs:
- changed files or commit: <paths or range>
- supporting note or verification: <paths>
- user for the recipe: <builder type>

Tasks:
1. Find the single most reusable pattern in the change.
2. Ignore generic commentary and avoid summarizing the whole diff.
3. Write a recipe with:
   - Use When
   - Goal
   - Workflow
   - Prompt Pattern or Checklist
   - Failure Modes
   - Verification
4. Anchor every section in repo evidence such as files, commands, or observed behavior.
5. If the change does not support a practical recipe, say so and stop.

Rules:
- No fake benchmarks.
- No "best practices" section unless the diff proves it.
- No timestamp-only or index-only recipes.
- Prefer one narrow lesson over a complete postmortem.
```

## Fast Checklist

- Can you point to the exact diff or file that taught the lesson?
- Would another builder know when to apply this pattern?
- Does the recipe include at least one real command, file, or failure mode?
- Did you remove repo-generic filler?
- Would the recipe still be useful if the reader never saw the original diff?

## Evaluation Pattern

Score each item `0` or `1`:

- Real source: tied to a concrete diff, commit, or note.
- Narrow scope: teaches one pattern, not the whole project.
- Repo evidence: cites files, commands, or observed behavior.
- Reusability: another builder can run the workflow quickly.
- Honesty: includes at least one limit or failure mode.

`5`: publish.
`4`: publish if the pattern fills a clear gap in the repo.
`3`: tighten the scope and cut filler once.
`0-2`: skip and return to the source change.

## Verification

Before publishing, run the smallest check that proves the recipe still points to something real.

Examples:

- docs/recipe only: reread links and referenced file paths,
- shell-backed workflow: `bash -n` plus one safe execution path,
- repo review pattern: confirm the referenced files still exist and match the claimed behavior.

Report the exact check you ran, not a generic "validated locally".

## Failure Modes

- Writing a recipe from memory instead of from the diff.
- Explaining the whole project instead of one reusable move.
- Copying the lab note title and calling that a recipe.
- Publishing a pattern with no file, command, or trigger condition.
- Hiding a thin artifact behind regenerated indexes or README churn.

## Source Linkage

- Repo / tool / workflow: this profile repo's recipe and lab automation loop.
- Supporting prompt, script, or note: [`../labs/2026/2026-05-26-latest-proof-sync-after-publish-script-repair.md`](../labs/2026/2026-05-26-latest-proof-sync-after-publish-script-repair.md), [`../recipes/executable-runbook-drift-check.md`](./executable-runbook-drift-check.md), and [`../scripts/commit_daily_update.sh`](../scripts/commit_daily_update.sh).
