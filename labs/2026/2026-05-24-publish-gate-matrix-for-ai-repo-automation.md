# 2026-05-24 - Publish Gate Matrix for AI Repo Automation

## Context

This repo already had an artifact gate in `scripts/commit_daily_update.sh`, but I wanted to verify the real behavior instead of repeating the intended policy from the docs.

The question was simple: what does the daily publish flow actually do when the diff is surface-only, when there is a real lab artifact, and when repo setup is incomplete?

## Experiment Setup

I copied the daily publish scripts into a temporary git repo, seeded minimal `README.md`, `DECISIONS.md`, `TODO.md`, `labs/`, `recipes/`, and `radar/` files, and then ran `scripts/commit_daily_update.sh` under four conditions.

The temporary repo used the same local scripts:

- [`scripts/commit_daily_update.sh`](../../scripts/commit_daily_update.sh)
- [`scripts/update_lab_index.sh`](../../scripts/update_lab_index.sh)
- [`scripts/update_recipe_index.sh`](../../scripts/update_recipe_index.sh)
- [`scripts/update_radar_index.sh`](../../scripts/update_radar_index.sh)

## Findings

- Surface-only diffs are rejected correctly. Changing only `README.md` produced: `Maintenance-only surface diff detected. Skipping commit until a substantive artifact changes.`
- A real lab note is enough to open the gate. Adding one new file under `labs/2026/` created a local commit and then stopped cleanly because the temporary repo had no `origin` remote.
- Missing git identity is blocked before commit. After unsetting `user.email`, the script stopped with the expected `git config user.name` and `git config user.email` instructions.
- The script is not fully portable yet. In the first temp-repo pass, the run failed because `git add README.md DECISIONS.md TODO.md docs labs recipes radar templates scripts .gitignore` assumes `.gitignore` exists.
- Repo-infra changes count as substantive changes. Editing `scripts/commit_daily_update.sh` alone was enough to pass the surface-only guard because `scripts/*` is outside the surface-file allowlist.

## Why It Matters for Coding Agents

This is the useful pattern: treat `git diff` as the outer gate, then add a narrower path-based guard so an agent cannot satisfy the run with index churn alone.

The limit is also clear from the experiment: path rules are still weaker than artifact semantics. A script-only change may be valid engineering work, but it is not automatically the same thing as a public lab artifact another builder can reuse immediately.

## Source Linkage

- Repo / tool / workflow: this profile repo's daily publish flow
- Supporting prompt, script, or file: [`docs/automation-runbook.md`](../../docs/automation-runbook.md), [`recipes/agent-artifact-gate.md`](../../recipes/agent-artifact-gate.md), and [`TODO.md`](../../TODO.md)

## Verification

Local checks run during this note:

- current repo git identity is configured as `Manuel Sampedro` with the GitHub no-reply email,
- current repo has an `origin` remote configured for `manuelsampedro1/manuelsampedro1`,
- temp repo run 1: surface-only diff skipped,
- temp repo run 2: new lab file committed locally,
- temp repo run 3: missing `user.email` blocked commit,
- temp repo run 4: repo without `.gitignore` failed on the hard-coded `git add` path list.

## Next Step

Harden `scripts/commit_daily_update.sh` so optional paths such as `.gitignore` do not abort a valid run, then decide whether `scripts/*` changes alone should count as publishable daily proof or require a paired public artifact.
