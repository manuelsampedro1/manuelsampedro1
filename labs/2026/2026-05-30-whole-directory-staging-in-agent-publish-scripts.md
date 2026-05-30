# 2026-05-30 - Whole-Directory Staging in Agent Publish Scripts

## Context

I wanted to verify one messy but realistic agent-automation case in this repo: what happens when the daily publish script is run after a coding agent already left tracked edits inside one of the repo's allowed public paths?

That matters because Codex or Claude Code sessions often resume from an already-dirty worktree. A publish helper that stages broad directories can silently merge old draft work into today's otherwise valid lab-note commit.

## Useful Artifact

The reusable pattern is not just "use an allowlist instead of `git add .`." It is also: understand whether your allowlist stages exact files or whole directories.

In this repo, [`scripts/commit_daily_update.sh`](../../scripts/commit_daily_update.sh) stages public paths with:

- `git add README.md DECISIONS.md TODO.md docs labs recipes radar templates scripts`

That is safer than staging the whole repo, but it still sweeps every tracked or untracked change inside those directories into the same commit. Builders copying this pattern should decide explicitly whether that bundling behavior is acceptable for their agent workflow.

## Source Linkage

- Repo / tool / workflow: this profile repo's daily publish flow
- Supporting prompt, script, or file: [`scripts/commit_daily_update.sh`](../../scripts/commit_daily_update.sh), [`docs/automation-runbook.md`](../../docs/automation-runbook.md), and [`labs/2026/2026-05-28-curated-staging-for-agent-publish-scripts.md`](../../labs/2026/2026-05-28-curated-staging-for-agent-publish-scripts.md)

## Notes

- Observation: in a temp clone with valid Git identity and `origin` removed, I created one new dated lab note and also modified the already tracked file [`recipes/ai-repo-review-findings.md`](../../recipes/ai-repo-review-findings.md). Running [`scripts/commit_daily_update.sh`](../../scripts/commit_daily_update.sh) produced a local commit that included both the intended lab note and the pre-existing recipe edit.
- Observation: the resulting commit touched `README.md`, `labs/README.md`, the new lab note, and the recipe file. Nothing in the script limited the commit to files changed by the current note workflow.
- Tradeoff: whole-directory staging is convenient for multi-file artifact updates because generated indexes and supporting docs land automatically. It also reduces the chance that a legitimate public artifact is left partially unstaged.
- Failure mode: if an agent has half-written tracked changes in `labs/`, `recipes/`, `docs/`, or another staged public path, a later "publish today's note" run can accidentally ship that unrelated work as collateral.
- Practical mitigation: either run the publish step from a clean worktree, keep drafts outside the staged public paths until ready, or add a preflight that refuses pre-existing tracked changes outside an expected file set.

## Verification

Local temp-clone verification completed for this note:

- cloned the repo into a temporary directory, removed `origin`, and configured a throwaway local Git identity,
- added a new note under `labs/2026/` and separately appended one draft line to [`recipes/ai-repo-review-findings.md`](../../recipes/ai-repo-review-findings.md),
- ran [`scripts/commit_daily_update.sh`](../../scripts/commit_daily_update.sh) with message `lab: temp publish scope smoke`,
- inspected `git show --stat HEAD` and confirmed that the commit included both the lab-note files and the unrelated tracked recipe change,
- confirmed the run stayed local because `origin` was absent.

## Next Step

Decide whether the publish script should warn on or block pre-existing tracked changes inside staged public paths before creating a new public artifact commit.
