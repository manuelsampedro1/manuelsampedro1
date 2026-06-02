# 2026-06-02 - Agent Plan Trace Public Launch

## Source

- Public repo: https://github.com/manuelsampedro1/agent-plan-trace
- Published HEAD: `2dfb21a4bd9291070ae6787a7245a43802b30f78`
- CI run: https://github.com/manuelsampedro1/agent-plan-trace/actions/runs/26842429111

## What Changed

Built and published `agent-plan-trace`, a dependency-free Python CLI for
auditing coding-agent plans against the evidence produced during execution.

The tool checks for:

- completed plan items without matching evidence in diffs, commands, or
  closeout notes,
- pending, in-progress, or blocked plan items when the closeout sounds fully
  complete,
- verification-shaped steps without command evidence,
- changed files that are never mentioned by the plan or closeout,
- closeout claims such as "tests passed" without matching successful command
  output,
- empty or weak plans that cannot support a reviewer-facing completion claim.

It supports Markdown task lists and JSON plans, emits Markdown or JSON, writes
optional reports, and gates runs with `--min-score` and `--fail-on`.

## Why It Matters

Plans are useful only if they stay attached to execution. Without a trace, an
agent can mark steps complete, skip pending work, and still produce a confident
final answer that looks clean to a reviewer.

`agent-plan-trace` adds a narrow gate between the live plan and the final
handoff. It complements closeout checks, claim checks, command receipts, and run
ledgers by asking one concrete question: did the completed plan actually leave
evidence?

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
- installed CLI smoke run against `examples/agent-plan.md`, `examples/sample.diff`, `examples/commands.txt`, and `examples/closeout.md`,
- `agent-instruction-audit AGENTS.md --min-score 80` at `100/100`,
- `repo-flightcheck . --check-remote --strict --threshold 80` at `100/100`,
- public raw README/source/test/example URLs returned `200`,
- GitHub Actions run `26842429111` completed with `success`.

## Takeaway

Treat an agent plan as a traceable artifact, not a progress decoration. If a
step is marked complete, it should have evidence; if work is still pending, the
closeout should say so.
