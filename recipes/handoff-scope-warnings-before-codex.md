# Handoff Scope Warnings Before Codex

Use this before handing a product or repo task to Codex when the required brief fields are present but scope risk may still be hidden.

## Goal

Separate hard missing fields from non-blocking scope warnings so a Codex prompt is both executable and honest about uncertainty.

## Source Event

This recipe came from adding non-blocking handoff warnings to `briefboard-local`.

The public change warns when constraints, preferred stack, or rollout/risk notes are empty without changing the `briefboard-local.v1` JSON schema.

## Workflow

1. Capture the required brief fields: project name, audience, problem, deliverable, and acceptance criteria.
2. Treat missing required fields as blockers before generating a handoff.
3. Check the optional scope fields: constraints, stack, and rollout/risk notes.
4. If any optional scope field is empty, add a warning rather than pretending the brief is fully scoped.
5. Let the user write `none` when the absence is intentional.
6. Include the warnings in both the human brief and Codex prompt.
7. Verify that complete briefs do not render warning noise.

## Example

```js
const { evaluateReadiness } = require("./brief-format.js");

const readiness = evaluateReadiness({
  projectName: "Runbook checker",
  audience: "solo builders",
  problem: "Docs drift from scripts.",
  deliverable: "Local checker.",
  acceptance: "Flags broken command references.",
});

console.log(readiness.ready);
console.log(readiness.warnings);
```

Expected signal:

```text
true
[
  'Constraints: empty; say "none" if this is intentional.',
  'Preferred stack: empty; say "none" if this is intentional.',
  'Rollout / risk notes: empty; say "none" if this is intentional.'
]
```

## Checklist

- Are all hard blockers explicit before the handoff?
- Are constraints empty because there are none, or because nobody decided them?
- Is stack preference empty because any stack is acceptable, or because the build context is missing?
- Are rollout and risk notes empty despite deploy, migration, privacy, auth, billing, or public-facing risk?
- Does the generated Codex prompt carry the warnings forward?
- Does a fully scoped brief stay clean and avoid warning fatigue?

## Failure Modes

- Marking a brief "ready" when acceptance criteria exist but constraints are unstated.
- Adding too many required fields and making the tool heavy.
- Hiding optional risk notes outside the prompt, where Codex cannot use them.
- Treating `none` as missing when the user intentionally declared no constraint.
- Letting warnings become fake quality scores.

## Source Linkage

- Public repo: <https://github.com/manuelsampedro1/briefboard-local>
- Commit: <https://github.com/manuelsampedro1/briefboard-local/commit/4dac6252c3b3825c6adae6845fd36a429fbaa18f>
- CI run: <https://github.com/manuelsampedro1/briefboard-local/actions/runs/26804568702>
- Lab note: <../labs/2026/2026-06-02-briefboard-handoff-scope-warnings.md>
