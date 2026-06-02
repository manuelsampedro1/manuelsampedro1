# Runbook Drift Check

Use this when a repo has operational docs that tell agents or humans which commands, scripts, or files to trust.

## Use When

- A README or runbook includes shell commands.
- Automation docs mention local scripts.
- A profile or docs page links to local artifacts.
- A coding agent changed scripts, generated indexes, or operational paths.

## Goal

Keep operational Markdown executable enough to trust.

The check should catch:

- missing local Markdown links,
- backticked paths that no longer exist,
- shell code blocks that call missing scripts,
- referenced shell scripts that fail `bash -n`.

## Workflow

1. Identify the docs that act like runbooks:

```sh
README.md
docs/automation-runbook.md
AGENTS.md
```

2. Check referenced paths and commands:

```sh
runbook-drift-check README.md docs/automation-runbook.md --root . --bash-syntax
```

3. If the helper is unavailable, use a manual pass:

```sh
rg -n "scripts/|docs/|\\.md\\)|```sh|```bash" README.md docs
bash -n scripts/*.sh
```

4. Treat missing local paths as blockers when the docs are part of the agent workflow.

5. Update the docs or scripts in the same change when drift is caused by a refactor.

## Prompt Pattern

```text
Audit these operational docs for runbook drift.

Inputs:
- repo root: <path>
- docs to check: <paths>
- scripts expected to remain executable: <paths>

Tasks:
1. Extract local Markdown links and backticked local paths.
2. Verify those paths exist from the right base directory.
3. Extract shell code blocks and identify local script calls.
4. Run syntax checks on referenced shell scripts when safe.
5. Report exact file, line, issue, and smallest fix.
```

## Fast Checklist

- Do local links resolve?
- Do backticked paths exist?
- Do shell blocks reference existing scripts?
- Do referenced shell scripts pass syntax checks?
- Did README/latest links update after new artifacts?

## Failure Modes

- Trusting a README because it looks current.
- Checking only links and missing shell commands.
- Running arbitrary commands from docs instead of syntax-checking known scripts.
- Resolving all paths from repo root when Markdown links are document-relative.
- Leaving profile links pointing at artifacts that were renamed.

## Source Linkage

- Repo / tool / workflow: public [`runbook-drift-check`](https://github.com/manuelsampedro1/runbook-drift-check) repo and verified launch commit [`7c13df4`](https://github.com/manuelsampedro1/runbook-drift-check/commit/7c13df4464b0cea6bada5e7369b658bd562751f1).
- Supporting prompt, script, or note: [`./executable-runbook-drift-check.md`](./executable-runbook-drift-check.md), [`./public-surface-sync-for-agent-repos.md`](./public-surface-sync-for-agent-repos.md), [`../labs/2026/2026-06-02-runbook-drift-check-public-launch.md`](../labs/2026/2026-06-02-runbook-drift-check-public-launch.md), and [`../docs/automation-runbook.md`](../docs/automation-runbook.md).
