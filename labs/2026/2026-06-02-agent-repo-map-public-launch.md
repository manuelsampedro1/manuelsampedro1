# 2026-06-02 - Agent Repo Map Public Launch

## Source

- Public repo: https://github.com/manuelsampedro1/agent-repo-map
- Published HEAD: `31de03df409e0e5a4335bb32a8d4a4ff66e3c282`
- CI run: https://github.com/manuelsampedro1/agent-repo-map/actions/runs/26829067968

## What Changed

Built and published `agent-repo-map`, a dependency-free Python CLI that generates compact repository context maps before a coding agent starts work.

The tool reports:

- docs and agent-instruction files,
- languages and top-level directories,
- CLI entrypoints and workflow files,
- local commands and verification signals,
- Git branch, HEAD, remote, and clean/dirty state,
- secret-looking paths, deploy or infra paths, and auth/security paths,
- readiness gaps such as missing README, tests, CI, commands, or entrypoints.

## Why It Matters

Task contracts say what the user wants, and repo readiness checks say whether a checkout is safe to use. The missing pre-run artifact is a compact map of what the agent should not miss inside the repo.

This gives a reviewer or next agent a fast handoff artifact before any diff exists.

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
- `agent-repo-map . --min-score 80`,
- `agent-instruction-audit AGENTS.md --min-score 80`,
- `repo-flightcheck . --check-remote --strict --threshold 80` at `100/100`,
- public repo and raw README/source/test URLs returned `200`,
- GitHub Actions run `26829067968` completed with `success`.

## Takeaway

A repo handoff should include both intent and terrain: task contract plus repository context map before execution, then proof packet after execution.
