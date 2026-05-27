# Public Surface Sync for Agent Repos

Use this when an automation publishes artifacts into repo folders such as `labs/`, `recipes/`, or `radar/`, but readers discover the work first through a root `README.md` or another public surface.

## Use When

- A repo has both artifact indexes and a top-level proof surface.
- Codex, Claude Code, or another agent is expected to publish notes or recipes through scripts.
- The docs imply that a new artifact becomes visible from the repo root.
- You want to verify the full publish path, not only individual generator scripts.

## Goal

Keep the public discovery surfaces in sync so one real artifact updates every promised entrypoint in the same publish run.

In this repo, that means a new lab note should update:

- `labs/README.md`
- the root `README.md` "Latest Proof" section

## Inputs

- The public surface file, usually `README.md`.
- The artifact index generators under `scripts/`.
- The commit-capable publish entrypoint, such as `scripts/commit_daily_update.sh`.
- One disposable local clone for end-to-end verification.
- One small real artifact to publish, such as a dated lab note or a new recipe.

## Workflow

1. List the surfaces that the repo promises to keep current. Write them as exact file paths.
2. Find the real publish entrypoint. Do not test helper scripts in isolation first.
3. Create a disposable clone and remove `origin` so a successful run cannot push.
4. Configure a valid local Git identity inside the clone.
5. Add one new artifact under the real publish path, such as `labs/YYYY/...` or `recipes/...`.
6. Run the publish script with a short message.
7. Inspect the resulting commit, not only stdout.
8. Compare the touched files against the promised surfaces:
   - if all expected surfaces changed, the sync contract holds,
   - if only some changed, patch the missing updater path and rerun the full publish script.
9. Keep the updater narrow. Prefer a dedicated sync script such as `scripts/update_root_readme_latest.sh` over adding more logic directly into the commit script.

## Temp Clone Pattern

```bash
tmp="$(mktemp -d)"
git clone . "$tmp/repo"
git -C "$tmp/repo" remote remove origin || true
git -C "$tmp/repo" config user.name "Test User"
git -C "$tmp/repo" config user.email "test@example.com"
```

Then add one artifact and run the real entrypoint:

```bash
cd "$tmp/repo"
printf '# 2099-01-01 - Test Note\n' > labs/2099/2099-01-01-test-note.md
scripts/commit_daily_update.sh "test: verify public surface sync"
git show --stat --name-only --oneline HEAD
```

## Agent Prompt Pattern

```text
Verify and repair public surface sync for this agent repo.

Inputs:
- public surfaces: <paths>
- publish entrypoint: <script path>
- artifact path to add: <path>

Tasks:
1. Run the real publish flow in a disposable clone with origin removed.
2. Add one small artifact through the expected path.
3. Inspect the resulting commit and list which promised surfaces changed.
4. If a surface stayed stale, patch the narrowest updater path.
5. Rerun the full publish flow and confirm the repaired commit touches the artifact and every promised surface.

Rules:
- Do not trust helper scripts without running the publish entrypoint.
- Do not claim success from stdout alone.
- Prefer one focused updater script over expanding the commit script into a second indexer.
- Report the exact files that changed in the final verified run.
```

## Fast Checklist

- Did you test the commit-capable publish script instead of only the index scripts?
- Did you remove `origin` before the verification run?
- Did the final commit touch the new artifact and every promised public surface?
- Did you keep the fix in one narrow updater path?
- Can another builder repeat the check with one artifact and one temp clone?

## Evaluation Pattern

Score each item `0` or `1`:

- Promised surfaces are named explicitly.
- Verification used the real publish entrypoint.
- Result is backed by final commit contents.
- Fix is isolated to the missing sync path.
- Re-run proved the surfaces now update together.

`5`: publish the recipe or patch.
`4`: publish if the missing surface and fix are already explicit.
`0-3`: rerun the full path before making claims.

## Failure Modes

- Testing `update_*` scripts one by one and assuming the publish flow is covered.
- Checking regenerated files in the working tree but not the actual commit contents.
- Mixing sync logic into the commit script until it becomes hard to reason about.
- Calling a run successful when the root `README.md` is still stale.
- Publishing a repair note without proving the second run touched the expected files.

## Source Linkage

- Repo / tool / workflow: this profile repo's artifact publishing flow.
- Supporting prompt, script, or note: [`../labs/2026/2026-05-25-runbook-drift-in-agent-repo-automation.md`](../labs/2026/2026-05-25-runbook-drift-in-agent-repo-automation.md), [`../labs/2026/2026-05-26-latest-proof-sync-after-publish-script-repair.md`](../labs/2026/2026-05-26-latest-proof-sync-after-publish-script-repair.md), [`../scripts/commit_daily_update.sh`](../scripts/commit_daily_update.sh), and [`../scripts/update_root_readme_latest.sh`](../scripts/update_root_readme_latest.sh).
