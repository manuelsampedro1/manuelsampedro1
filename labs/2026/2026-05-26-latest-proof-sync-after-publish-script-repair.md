# 2026-05-26 - Latest Proof Sync After Publish Script Repair

## Context

Yesterday's lab note documented a real drift: the daily publish flow refreshed [`labs/README.md`](../../labs/README.md) but left the root [`README.md`](../../README.md) "Latest Proof" section stale.

This repo now includes [`scripts/update_root_readme_latest.sh`](../../scripts/update_root_readme_latest.sh) and calls it from [`scripts/commit_daily_update.sh`](../../scripts/commit_daily_update.sh), so I wanted to verify the repair with the same style of temp-clone test instead of trusting the new script on sight.

## Useful Artifact

For coding-agent repos, the reusable pattern is simple: when a note or recipe is meant to drive a public profile surface, test the full publish script in a throwaway clone and inspect the resulting commit contents instead of checking file generation in isolation.

In this repo, the expected success condition is now explicit:

- a new lab artifact lands under `labs/YYYY/`,
- [`labs/README.md`](../../labs/README.md) refreshes automatically,
- the root [`README.md`](../../README.md) updates its latest lab note link in the same commit.

## Source Linkage

- Repo / tool / workflow: this profile repo's daily publish flow
- Supporting prompt, script, or file: [`scripts/commit_daily_update.sh`](../../scripts/commit_daily_update.sh), [`scripts/update_root_readme_latest.sh`](../../scripts/update_root_readme_latest.sh), and [`labs/2026/2026-05-25-runbook-drift-in-agent-repo-automation.md`](../../labs/2026/2026-05-25-runbook-drift-in-agent-repo-automation.md)

## Notes

- Observation: in a temp clone with `origin` removed and valid Git identity configured, adding one dated lab note and running the commit script produced a commit that changed exactly `README.md`, `labs/README.md`, and the new lab note file.
- Tradeoff: the root README updater derives the latest lab note from reverse-sorted dated filenames and the latest recipes from Git add-times, which is pragmatic here but still couples correctness to filename discipline and Git history.
- Failure mode: if someone bypasses the dated filename convention or edits `README.md` manually without rerunning the script, the public surface can drift again even though the automation path is now repaired.

## Verification

Local temp-clone verification completed for this note:

- before the test commit, the root README latest lab link pointed to `2026-05-25 - Runbook Drift in Agent Repo Automation`,
- after adding a new dated lab note and running [`scripts/commit_daily_update.sh`](../../scripts/commit_daily_update.sh), the root README latest lab link pointed to the new `2026-05-26` note,
- the temp-clone commit touched only `README.md`, `labs/README.md`, and the new lab file,
- because the temp clone had no `origin` remote, the script stopped after the local commit with `Committed locally. Add a remote named origin to push to GitHub.`

## Next Step

Add one targeted smoke test around [`scripts/update_root_readme_latest.sh`](../../scripts/update_root_readme_latest.sh) so future publish-script edits do not silently reintroduce root README drift.
