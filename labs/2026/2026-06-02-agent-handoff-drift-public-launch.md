# 2026-06-02 - Agent Handoff Drift Public Launch

## Source

- Public repo: https://github.com/manuelsampedro1/agent-handoff-drift
- Published HEAD: `24db9c4d52e113a608bca0a2a9a5d75f1d902286`
- CI run: https://github.com/manuelsampedro1/agent-handoff-drift/actions/runs/26840812678

## What Changed

Built and published `agent-handoff-drift`, a dependency-free Python CLI for
auditing coding-agent handoff or continuation notes against the live repository.

The tool checks for:

- referenced repo files that no longer exist,
- claimed `HEAD` or commit values that do not match the current repo,
- claimed branches that do not match the checked-out branch,
- clean-worktree claims when Git reports dirty paths,
- command-success claims without nearby evidence such as output, exit code,
  report, receipt, or CI run.

It emits Markdown for reviewers, JSON for automation, score gates via
`--min-score`, severity gates via `--fail-on`, and optional reports via
`--write-report`.

## Why It Matters

Context can be correctly scoped and still stale. A continuation note might point
to a deleted file, claim a different branch, say the tree is clean when it is
not, or tell the next agent that tests passed without keeping evidence.

`agent-handoff-drift` turns those contradictions into a small preflight gate.
It complements request briefs, handoff briefs, continuation notes, context
budgets, and context-injection checks by comparing the note to the repo state
that actually exists now.

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
- installed CLI smoke run against `examples/handoffs/good-handoff.md`,
- `agent-instruction-audit AGENTS.md --min-score 80` at `100/100`,
- `repo-flightcheck . --check-remote --strict --threshold 80` at `100/100`,
- public raw README/source/test/example URLs returned `200`,
- GitHub Actions run `26840812678` completed with `success`.

## Takeaway

Before another agent continues, check the handoff against the repo that exists
now. Stale state is a coordination bug, not just a documentation issue.
