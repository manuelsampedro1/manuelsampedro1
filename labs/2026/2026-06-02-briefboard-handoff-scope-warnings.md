# 2026-06-02 - Briefboard Handoff Scope Warnings

## Context

`briefboard-local` already flagged missing essential fields before generating a Codex handoff: project name, audience, problem, deliverable, and acceptance criteria.

The remaining product gap was a brief that technically passes the required-field check but still hides execution risk. Empty constraints, preferred stack, or rollout/risk notes often lead to oversized implementations, vague assumptions, or weak closeouts.

## Change

- Added non-blocking handoff warnings for empty constraints, preferred stack, and rollout/risk notes.
- Kept `briefboard-local.v1` JSON export/import compatibility; no fields were added.
- Rendered warnings inside both generated brief and Codex prompt.
- Exported the recommended-field list for tests and future UI use.
- Updated README manual checks and recorded the decision.

Public commit: `4dac6252c3b3 feat: warn on weak handoff scope`.

## Verification

Local checks:

```sh
node --test
node scripts/build.js
node scripts/lint.js
git diff --check
node - <<'NODE'
const { renderBrief, renderPrompt, evaluateReadiness } = require('./brief-format.js');
const incomplete = { projectName: 'Agent Scope Tool', audience: 'AI builders', problem: 'Briefs miss risks.', deliverable: 'Local helper.', acceptance: 'Shows warnings.' };
const complete = { ...incomplete, constraints: 'No backend.', stack: 'Vanilla JS.', rollout: 'Use on one kickoff first.' };
console.log(renderBrief(incomplete).includes('Warnings before handoff'));
console.log(evaluateReadiness(complete).warnings.length);
console.log(renderPrompt(complete).includes('Warnings before handoff'));
NODE
node /Users/manuelsampedro/Documents/Codex/2026-05-21/repo-flightcheck/bin/repo-flightcheck.js . --strict --threshold 80
```

Results:

- `node --test`: 10 tests passed.
- `node scripts/build.js`: passed.
- `node scripts/lint.js`: passed.
- `git diff --check`: passed.
- Smoke output confirmed incomplete briefs show warnings, complete briefs have `0` warnings, and complete prompts do not render warning text.
- `repo-flightcheck --strict --threshold 80`: `98/100` after commit; only warning was missing local `npm` in this Codex environment.
- GitHub Actions run `26804568702` completed with conclusion `success`.

`npm test`, `npm run build`, and `npm run lint` were not runnable locally because `npm` is not installed in this Codex PATH. The equivalent Node entrypoints above and GitHub Actions CI covered the same scripts.

## Source Linkage

- Repo: <https://github.com/manuelsampedro1/briefboard-local>
- Commit: <https://github.com/manuelsampedro1/briefboard-local/commit/4dac6252c3b3825c6adae6845fd36a429fbaa18f>
- CI run: <https://github.com/manuelsampedro1/briefboard-local/actions/runs/26804568702>
- Formatter: <https://raw.githubusercontent.com/manuelsampedro1/briefboard-local/main/brief-format.js>
- Tests: <https://raw.githubusercontent.com/manuelsampedro1/briefboard-local/main/tests/brief-format.test.cjs>

## Takeaway

A brief should distinguish blockers from quality warnings. Missing acceptance criteria should stop the handoff; missing constraints or rollout notes should not block everything, but they should be visible before Codex turns ambiguity into code.
