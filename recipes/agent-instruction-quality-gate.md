# Agent Instruction Quality Gate

Use this when a repo-readiness audit checks for `AGENTS.md`, `CLAUDE.md`, or another coding-agent instruction file.

## Goal

Avoid treating placeholder agent instructions as real readiness. A repo should pass the gate only when the instruction file gives an agent enough context to stay scoped and verify its work.

## Source Event

This recipe came from `repo-flightcheck` commit `63ffbf68245d`, which changed the agent-instructions check from "file exists" to "file includes goal, constraints, and verification guidance."

Relevant files:

- `src/scan.js`
- `test/scan.test.js`
- `AGENTS.md`
- `README.md`

## Workflow

1. Detect the candidate agent files, such as `AGENTS.md`, `CLAUDE.md`, `GEMINI.md`, or `CURSOR.md`.
2. If no file exists, warn that agent guidance is missing.
3. If a file exists, inspect its text instead of passing immediately.
4. Look for three signals:
   - Goal or product scope.
   - Constraints, principles, or repo rules.
   - Verification, test, build, lint, CI, or quality guidance.
5. Pass only when all three signals are present.
6. Warn, not fail, when the file is present but too thin; keyword heuristics can false-positive or miss unusual phrasing.
7. Add a regression test with a placeholder file such as `# Rules`.

## Checklist

- Does the file explain what the repo is trying to do?
- Does it tell the agent what not to do or what to prefer?
- Does it name a verification path?
- Does the repo's own agent file satisfy the same rule?
- Does the README disclose heuristic limits?

## Verification

For a Node standard-library audit tool, run:

```sh
node --test
node scripts/lint.js
node scripts/build.js
node bin/repo-flightcheck.js . --strict --threshold 80
```

The source change also has public CI success.

## Failure Modes

- Passing `# Rules` or another placeholder because the file exists.
- Requiring exact headings and failing useful but differently structured guidance.
- Making the check a hard failure even when a human reviewer could still interpret the repo.
- Forgetting to update the audited repo's own `AGENTS.md`, causing dogfood drift.

## Source Linkage

- Public repo: <https://github.com/manuelsampedro1/repo-flightcheck>
- Commit: <https://github.com/manuelsampedro1/repo-flightcheck/commit/63ffbf68245d2017046afcd56648e90cc0e24ab5>
- CI run: <https://github.com/manuelsampedro1/repo-flightcheck/actions/runs/26792017274>
