# 2026-06-02 - Agent Bug Repro Public Launch

## Source

- Public repo: https://github.com/manuelsampedro1/agent-bug-repro
- Published HEAD: `a85886d6b2693baecff4c205aea1af78ac863b02`
- CI run: https://github.com/manuelsampedro1/agent-bug-repro/actions/runs/26836493094

## What Changed

Built and published `agent-bug-repro`, a dependency-free Python CLI for auditing
bug reports before they become coding-agent debugging handoffs.

The tool checks:

- summary or title clarity,
- reproduction steps,
- expected behavior,
- actual behavior,
- environment or version context,
- evidence such as logs, traces, screenshots, or failing commands,
- regression, frequency, scope, or suspected area detail,
- vague language that weakens a handoff,
- error signals inside attached text evidence.

It emits Markdown for reviewers, JSON for automation, optional handoff packets
via `--write-packet`, score gates via `--min-score`, and status gates via
`--fail-on`.

## Why It Matters

Many debugging runs fail before code is touched because the bug report is too
thin. A coding agent can move quickly, but speed is harmful if the report does
not separate expected behavior, actual behavior, reproduction steps, and
evidence.

`agent-bug-repro` gives the workflow a pre-debugging stop condition. It does
not execute repro steps or claim root cause. It makes the bug report actionable
enough for a focused debugging run.

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
- installed CLI smoke run against `examples/complete-bug.md`,
- `agent-instruction-audit AGENTS.md --min-score 80` at `100/100`,
- `repo-flightcheck . --check-remote --strict --threshold 80` at `100/100`,
- public raw README/source/test/example URLs returned `200`,
- GitHub Actions run `26836493094` completed with `success`.

## Takeaway

Do not hand a vague bug report to another agent and hope it infers the missing
context. First require repro steps, expected and actual behavior, environment,
evidence, and regression context, then generate a focused next-agent prompt.
