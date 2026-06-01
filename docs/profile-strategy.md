# Profile Strategy

## Positioning

Public identity: AI builder for teams that need coding-agent workflows, small tools, automation systems, and local-first product prototypes that can actually ship.

Lead with agent reliability: readiness checks, context packaging, verification gates, audit trails, and reviewable outputs. This is the strongest signal for serious AI teams because it shows judgment around the hard parts of using coding agents in real repos.

## Visual Direction

- Tone: clear, technical, direct, and evidence-led.
- Palette if custom assets are added later: neutral base, electric blue accent, restrained green success state.
- Typography: GitHub markdown first; avoid image-heavy gimmicks unless there is a real project screenshot.
- Iconography: GitHub-native badges only when they add signal.

## Contribution Mix

- 40% flagship repos and owned product/tool proof.
- 30% lab notes from actual Codex-assisted builds, reviews, and debugging.
- 20% reusable recipes and workflows that can be copied into Codex sessions.
- 10% tool radar and maintenance combined, only when they sharpen the client-facing story.

## Quality Bar

A daily artifact is worth publishing when it has at least one of these:

- a concrete code or workflow example,
- a decision with reusable reasoning,
- a tested checklist,
- source-backed research,
- a clear failure mode and fix.

## Current Bias

When in doubt, prefer content that helps future Codex sessions move faster:

- sharper prompts,
- better review output,
- less repeated debugging,
- clearer repo instructions,
- stronger verification discipline.

## Proof Hierarchy

Rank public proof in this order:

1. Owned repos with working code.
2. Labs and recipes linked to those repos.
3. README framing and selected-work curation.
4. Radar or ecosystem notes.

If a lower layer starts overshadowing a higher one, rebalance the profile.

Next flagship gaps:

- Task contracts before an agent starts. The local `agent-task-contract` project fills this by checking objective, acceptance criteria, constraints, verification, risks, and out-of-scope items before a coding-agent run begins.
- Scope guards while an agent edits. The local `agent-scope-guard` project fills this by failing diffs that touch files outside declared paths or globs.
- Secret scanning before an agent diff is committed or published. The local `agent-secret-sentinel` project fills this by scanning added diff lines for likely tokens, keys, and unsafe examples.
- CI failure packets after verification fails. The local `agent-ci-failure-packet` project fills this by turning noisy logs into compact retry context for the next agent run.
- Rollback planning before risky agent diffs ship. The local `agent-rollback-plan` project fills this by turning changed files and risk tags into rollback steps and post-rollback checks.
- Runbook drift checks while agent repos evolve. The local `runbook-drift-check` project fills this by checking operational Markdown against real files, links, and scripts.
- Reusable eval cases after an agent finishes. The local `diff-to-eval` project fills this by turning real diffs into JSON cases with changed files, risk tags, suggested checks, and expected outcomes.

## CTA

Primary public CTA: `@manuelsampedrop`.

Avoid direct job-pitch language on the profile surface. For high-caliber AI readers, the better signal is public proof that the work is scoped, runnable, verifiable, and reviewable.
