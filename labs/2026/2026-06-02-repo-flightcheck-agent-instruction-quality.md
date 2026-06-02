# 2026-06-02 - Repo Flightcheck Agent Instruction Quality

## Context

`repo-flightcheck` is one of the profile's primary proof repos because it audits whether a repo is ready before handing work to Codex, Claude Code, or a human reviewer. Its first public rule for agent instructions accepted any `AGENTS.md`, even a thin placeholder like `# Rules`, which could overstate readiness.

## Change

- Added an `AGENTS.md` quality heuristic for goal or product scope, constraints or repo rules, and verification or quality guidance.
- Changed the `agent-instructions` check to warn when the file exists but lacks those signals.
- Added a regression test for thin agent instructions.
- Updated the repo's own `AGENTS.md` with exact verification commands.
- Updated README limits to disclose that the heuristic is keyword-based.

Public commit: `63ffbf68245d feat: check agent instruction quality`.

## Verification

Local checks:

```sh
node --test
node scripts/lint.js
node scripts/build.js
node bin/repo-flightcheck.js . --strict --threshold 80
git diff --check
```

Public checks:

- Raw `src/scan.js` returned `200`.
- Raw `test/scan.test.js` returned `200`.
- GitHub Actions run `26792017274` for commit `63ffbf68245d2017046afcd56648e90cc0e24ab5` completed with conclusion `success`.

## Source Linkage

- Repo: <https://github.com/manuelsampedro1/repo-flightcheck>
- Commit: <https://github.com/manuelsampedro1/repo-flightcheck/commit/63ffbf68245d2017046afcd56648e90cc0e24ab5>
- CI run: <https://github.com/manuelsampedro1/repo-flightcheck/actions/runs/26792017274>
- Tests: <https://raw.githubusercontent.com/manuelsampedro1/repo-flightcheck/63ffbf6/test/scan.test.js>

## Takeaway

Agent-readiness checks should not reward placeholder instruction files. A repo is more ready when the agent file names the goal, constraints, and verification path a contributor can actually run.
