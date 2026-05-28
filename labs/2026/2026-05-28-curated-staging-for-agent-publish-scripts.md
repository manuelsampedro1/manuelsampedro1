# 2026-05-28 - Curated Staging for Agent Publish Scripts

## Context

I wanted to verify a practical safety property in this repo's publish flow: if a coding agent leaves scratch files or private working notes outside the public artifact paths, does the daily commit script accidentally publish them?

That matters for Codex or Claude Code workflows because agent runs often create temporary files, one-off notes, or local experiment output in the repo root while the useful artifact is being prepared elsewhere.

## Useful Artifact

This repo's publish flow uses a two-layer safety pattern that is worth copying into other agent repos:

- the preflight check looks at the whole working tree to decide whether the run is surface-only or potentially substantive,
- the staging step then adds only a curated allowlist of project paths such as `labs/`, `recipes/`, `radar/`, `docs/`, `scripts/`, and a few root files.

That separation means a stray file can exist in the repo without automatically landing in the commit. The run only produces history if a staged public artifact also changed.

## Source Linkage

- Repo / tool / workflow: this profile repo's daily publish flow
- Supporting prompt, script, or file: [`scripts/commit_daily_update.sh`](../../scripts/commit_daily_update.sh), [`docs/automation-runbook.md`](../../docs/automation-runbook.md), and [`labs/2026/2026-05-26-latest-proof-sync-after-publish-script-repair.md`](../../labs/2026/2026-05-26-latest-proof-sync-after-publish-script-repair.md)

## Notes

- Observation: in a temp clone with valid Git identity and no `origin`, a stray `scratch/private-scratch.txt` file by itself did not create a commit. The script finished with `No useful changes to commit.` and left the scratch file untracked.
- Observation: when I added a real dated lab note under `labs/2026/` plus the same stray scratch file, the resulting local commit changed only `README.md`, `labs/README.md`, and the new lab note. The scratch file stayed untracked after the run.
- Tradeoff: this is safer than `git add .`, but it is not the same as secret scanning. Anything accidentally written inside an allowed path such as `labs/` or `docs/` would still be eligible for commit.
- Failure mode: the preflight "surface-only" check and the final staged diff are not identical concepts. A file outside the allowlist can make the run look substantive at first, but the later curated staging can still reduce the result to "nothing to commit." That is correct behavior, but it can confuse debugging if an agent only reads the first gate.
- Practical note: a temp clone does not inherit repo-local Git identity, so reproducible publish-script tests need an explicit `git config user.name` and `git config user.email` inside the clone before measuring commit behavior.

## Verification

Local temp-clone verification completed for this note:

- case 1: added only `scratch/private-scratch.txt`, ran [`scripts/commit_daily_update.sh`](../../scripts/commit_daily_update.sh), observed no new commit and the scratch file remained untracked,
- case 2: added `labs/2026/2026-05-28-curated-staging-smoke.md` plus the same scratch file, ran the same script, observed a local commit with only `README.md`, `labs/README.md`, and the lab note staged,
- in both cases, `origin` was removed from the temp clone so the script stopped locally and could not push by accident.

## Next Step

Decide whether the publish script should emit a warning when unstaged files remain outside the allowlist after a successful run, so agent operators can notice leftover scratch state without weakening the current safety behavior.
