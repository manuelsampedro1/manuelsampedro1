# Agent Artifact Gate

Use this recipe before letting Codex, Claude Code, or another automation publish to a repo. The goal is simple: commit only when the run produced one reusable artifact, not just file churn.

## When To Use It

- Daily repo automations.
- Profile or portfolio repos.
- Agent loops that regenerate indexes, docs, or notes.
- Any workflow where "activity" can be faked by maintenance diffs.

## Publish Rule

Publish only if the run leaves at least one artifact another builder could reuse within five minutes.

Acceptable artifacts:

- A recipe with a concrete workflow, checklist, or prompt.
- A lab note with a tested observation, failure mode, or decision.
- A radar note with source-backed research and a usable takeaway.
- A small implementation change with verification.

Reject these on their own:

- Index-only diffs.
- Timestamp churn.
- Reworded filler without a new pattern or result.
- Generic summaries that could fit any repo.

## Agent Prompt Pattern

```text
You are maintaining a public AI-builder repo.

Your job is to either:
1. create exactly one reusable artifact, then update any affected indexes, or
2. stop without committing.

A valid artifact must include at least one of:
- a concrete workflow,
- a prompt pattern with failure modes,
- a tested checklist,
- a source-backed decision,
- a verified implementation note.

Before committing, answer:
- What is the artifact?
- Who can reuse it?
- What evidence makes it specific to this repo?
- What verification was run?

If the only diffs are maintenance or wording polish, exit without committing.
```

## Five-Minute Gate

Ask these in order:

1. Is there one named artifact in the diff?
2. Would a builder learn a workflow, decision, or fix from it?
3. Does it contain repo-specific evidence instead of generic AI advice?
4. Was at least one relevant check run?
5. If I remove the new artifact, do the remaining diffs still deserve a commit?

If any answer is "no", skip the commit.

## Fast Evaluation Pattern

Score each item `0` or `1`:

- Artifact exists and is easy to point to.
- Specificity: references actual files, tools, prompts, or checks.
- Reusability: another builder could copy the pattern.
- Verification: includes a check, test, source, or observed result.
- Honesty: clearly states limits or open questions.

`4-5`: publish.
`3`: revise once, then decide again.
`0-2`: skip.

## Example Reviewer Output

```text
Artifact: recipes/agent-artifact-gate.md
Reusable for: public AI-builder repos with daily automations
Repo-specific evidence: matches current scripts that refresh indexes and skip empty commits
Verification: bash -n on commit/update scripts
Decision: publish
```

## Failure Modes

- Treating "a changed file" as equal to "a useful artifact".
- Hiding weak content behind regenerated indexes.
- Claiming verification that was not run.
- Publishing broad best practices with no repo anchor.

## Implementation Hint

Keep the quality gate in two layers:

- Prompt layer: define what counts as an artifact.
- Repo layer: make the commit script refuse empty or misconfigured runs.

That split matters because shell checks can confirm a diff exists, but only the artifact gate can decide whether the diff is worth publishing.
