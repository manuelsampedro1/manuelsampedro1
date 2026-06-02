# Task Contract Readiness Before Agent Work

Use this when a coding-agent run needs a concrete brief before any file edits start.

## Goal

Make the task itself reviewable before the agent starts. A ready repo still produces weak work if the requested task is vague, missing acceptance criteria, or silent about constraints.

## Required Contract

Create `AGENT_TASK.md` or `TASK_CONTRACT.md` with these sections:

- `Objective`
- `Acceptance Criteria`
- `Context`
- `Constraints`
- `Expected Changes`
- `Verification`
- `Risks`
- `Out of Scope`

## Workflow

1. Write the task contract before starting the agent run.
2. Include at least two concrete acceptance criteria.
3. Add explicit constraints and expected change areas.
4. Add verification commands or concrete manual checks.
5. List risks and tempting out-of-scope work.
6. Run `repo-flightcheck --strict --threshold 80`.
7. If `Task contract` warns, fix the brief before asking an agent to edit files.

## Expected Signals

- No task contract: pass for general repo readiness, because the file is optional.
- Complete task contract: `AGENT_TASK.md includes objective, acceptance criteria, constraints, verification, risks, and out-of-scope boundaries.`
- Incomplete task contract: warning with concrete evidence such as missing sections, placeholder text, or too few acceptance bullets.

## Checklist

- Does the objective name one outcome?
- Do acceptance criteria prove completion without reading the agent's intent?
- Do constraints prevent broad opportunistic edits?
- Does verification include commands or concrete review gates?
- Are risks and out-of-scope work explicit enough for a reviewer to challenge the run?

## Failure Modes

- Starting from a task that says "improve this" without observable acceptance criteria.
- Keeping template language such as `TBD`, `todo`, or `state the outcome`.
- Listing verification as "looks good" instead of commands or manual checks.
- Letting a task contract become stale after the implementation changes.

## Source Linkage

- Public repo: <https://github.com/manuelsampedro1/repo-flightcheck>
- Commit: <https://github.com/manuelsampedro1/repo-flightcheck/commit/48c22da1aa9d65477ac345729c0f28beece7e3a1>
- CI run: <https://github.com/manuelsampedro1/repo-flightcheck/actions/runs/26807151587>
- Lab note: <../labs/2026/2026-06-02-repo-flightcheck-agent-task-contracts.md>
