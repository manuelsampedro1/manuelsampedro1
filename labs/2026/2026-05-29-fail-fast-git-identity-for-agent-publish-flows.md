# 2026-05-29 - Fail-Fast Git Identity for Agent Publish Flows

## Context

I wanted one more temp-clone check around this repo's daily publish script after yesterday's staging-safety note: what happens when a coding agent creates a real lab artifact but the machine running the publish flow does not have a usable Git identity?

That matters because agent automations often run in fresh environments, throwaway clones, or machines where GitHub auth exists in the browser but `git config user.name` and `git config user.email` are still missing or wrong.

## Useful Artifact

The reusable pattern is simple: fail the publish script on identity preflight before regenerating indexes or mutating public surface files.

In this repo, that means checking Git identity immediately after confirming the working tree is a Git repo, and only then running:

- [`scripts/update_lab_index.sh`](../../scripts/update_lab_index.sh)
- [`scripts/update_recipe_index.sh`](../../scripts/update_recipe_index.sh)
- [`scripts/update_radar_index.sh`](../../scripts/update_radar_index.sh)
- [`scripts/update_root_readme_latest.sh`](../../scripts/update_root_readme_latest.sh)

This keeps an invalid publish environment from leaving extra README churn behind for the next agent run.

## Source Linkage

- Repo / tool / workflow: this profile repo's daily publish flow
- Supporting prompt, script, or file: [`scripts/commit_daily_update.sh`](../../scripts/commit_daily_update.sh), [`docs/automation-runbook.md`](../../docs/automation-runbook.md), and [`labs/2026/2026-05-28-curated-staging-for-agent-publish-scripts.md`](../../labs/2026/2026-05-28-curated-staging-for-agent-publish-scripts.md)

## Notes

- Observation: in a temp clone with `HOME` and `XDG_CONFIG_HOME` pointed at empty directories and `GIT_CONFIG_NOSYSTEM=1`, running the old publish flow after adding a real dated note failed on missing identity but still modified `README.md` and `labs/README.md` before exiting.
- Observation: after moving the identity check to the top of [`scripts/commit_daily_update.sh`](../../scripts/commit_daily_update.sh), the same missing-identity scenario failed with the same configuration message and did not modify generated surface files such as `README.md` or `labs/README.md`.
- Tradeoff: this fix does not validate whether the configured email is actually connected to the intended GitHub account. It only guarantees the script will not mutate generated surfaces before the obvious identity gate passes.
- Failure mode: if an agent writes sensitive scratch content directly inside allowed paths such as `labs/` or `docs/`, the fail-fast identity check does not help. Curated staging still needs disciplined artifact paths and human review.

## Verification

Local temp-clone verification completed for this note:

- case 1, before the script fix: added one dated note, ran [`scripts/commit_daily_update.sh`](../../scripts/commit_daily_update.sh) with Git identity neutralized, observed the expected identity error plus dirty `README.md` and `labs/README.md`,
- case 2, after the script fix: repeated the same setup, observed the same identity error and confirmed that `README.md` and `labs/README.md` stayed clean in `git status --short`,
- syntax checks passed for [`scripts/new_daily_lab_note.sh`](../../scripts/new_daily_lab_note.sh), [`scripts/update_lab_index.sh`](../../scripts/update_lab_index.sh), and [`scripts/commit_daily_update.sh`](../../scripts/commit_daily_update.sh).

## Next Step

Add one small executable smoke test for the publish script's missing-identity path so future automation changes cannot reintroduce preflight mutations silently.
