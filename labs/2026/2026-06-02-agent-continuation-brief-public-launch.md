# 2026-06-02 - Agent Continuation Brief Public Launch

## Source

- Public repo: https://github.com/manuelsampedro1/agent-continuation-brief
- Published HEAD: `6de26ebf667c537ba76f8adfe293ae3c46f4f19f`
- CI run: https://github.com/manuelsampedro1/agent-continuation-brief/actions/runs/26837214756

## What Changed

Built and published `agent-continuation-brief`, a dependency-free Python CLI for
auditing continuation notes before a long-running coding-agent task is resumed by
another run.

The tool checks whether a continuation note preserves:

- the original objective,
- current state,
- completed work,
- in-progress work,
- blockers,
- changed files,
- commands already run,
- concrete next actions,
- residual risks,
- next-agent handoff instructions.

It emits Markdown for reviewers, JSON for automation, optional next-agent briefs
via `--write-brief`, score gates via `--min-score`, and status gates via
`--fail-on`.

## Why It Matters

Long-running agent work often fails at the continuation boundary. The next run
inherits a partial summary, guesses which checks already passed, narrows the
objective, or marks an external outcome as complete because the previous state
was vague.

`agent-continuation-brief` gives the workflow a stop condition before resuming.
It does not claim the task is done. It verifies that the next agent receives
enough state to continue without inventing context.

## Verification

Ran locally:

```sh
make test
make lint
make build
make smoke
git diff --check
```

Additional checks:

- editable install in a temporary virtualenv after upgrading `pip`, `setuptools`, and `wheel`,
- installed CLI smoke run against `examples/complete-continuation.md`,
- `agent-instruction-audit AGENTS.md --min-score 80` at `100/100`,
- `repo-flightcheck . --check-remote --strict --threshold 80` at `100/100`,
- public raw README/source/test/example URLs returned `200`,
- GitHub Actions run `26837214756` completed with `success`.

## Takeaway

Do not let a continuation note shrink the task to what is convenient to finish.
Require original objective, current state, completed work, blockers, commands,
risks, changed files, and next actions before another agent resumes.
