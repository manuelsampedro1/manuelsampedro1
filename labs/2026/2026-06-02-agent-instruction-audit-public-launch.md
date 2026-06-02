# 2026-06-02 - Agent Instruction Audit Public Launch

Published [agent-instruction-audit](https://github.com/manuelsampedro1/agent-instruction-audit), a dependency-free Python CLI that audits coding-agent instruction files for actionable scope, constraints, verification, safety, closeout guidance, and risky command patterns.

## What Changed

- Added default detection for `AGENTS.md`, `CLAUDE.md`, `GEMINI.md`, `CURSOR.md`, and `.cursorrules`.
- Added scoring and Markdown/JSON verdicts for instruction quality.
- Added blockers for thin instruction files, unguarded destructive commands, unsafe credential guidance, and disabled-test language.
- Added examples, tests, smoke checks, package metadata, and GitHub Actions CI.

## Verification

- Public clone from GitHub passed `make test`, `make lint`, `make build`, and `make smoke`.
- Editable install from the public clone succeeded, and `agent-instruction-audit AGENTS.md --min-score 80` returned `passed` at `100/100`.
- `repo-flightcheck` on the public clone returned `100/100`.
- GitHub Actions run `26827382470` completed with `success`.

## Lesson

Repo readiness cannot stop at "an agent file exists." The instruction file itself needs a quality bar, because weak or risky defaults become invisible once they are stored in the repo.
