# 2026-06-02 - Agent Handoff Brief Public Launch

## Source

- Public repo: https://github.com/manuelsampedro1/agent-handoff-brief
- Published HEAD: `a8890ae79548d209e5d0ce5e5ed28be1bdc99df2`
- CI run: https://github.com/manuelsampedro1/agent-handoff-brief/actions/runs/26830032727

## What Changed

Built and published `agent-handoff-brief`, a dependency-free Python CLI that turns a task contract plus repository context into a compact pre-run handoff brief for a coding agent.

The tool reports:

- objective, acceptance criteria, constraints, expected changes, verification, risks, and out-of-scope task sections,
- README, agent instructions, docs, TODO, decisions, commands, tests, CI, entrypoints, and Git state,
- secret-looking, deploy, migration, auth, security, and workflow paths by path only,
- handoff gaps such as missing task criteria, missing repo commands, no verification signal, dirty Git state, or missing agent instructions,
- a ready-to-copy agent prompt for the next run.

## Why It Matters

The profile already has tools for task contracts, repo maps, readiness checks, review packets, verification, and ledgers. The missing pre-run link was the actual brief that gives the next agent enough intent and terrain to start without guessing.

`agent-handoff-brief` makes that handoff explicit.

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

- editable install in a temporary virtualenv,
- `agent-handoff-brief . --task examples/task-contract.md --min-score 80`,
- `agent-instruction-audit AGENTS.md --min-score 80`,
- `repo-flightcheck . --check-remote --strict --threshold 80` at `100/100`,
- public repo and raw README/source/test URLs returned `200`,
- GitHub Actions run `26830032727` completed with `success`.

## Takeaway

A strong pre-run agent handoff should combine task intent, repo terrain, risk paths, verification commands, and known gaps before the agent changes files.
