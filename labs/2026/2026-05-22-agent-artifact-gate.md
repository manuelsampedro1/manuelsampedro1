# 2026-05-22 - Agent Artifact Gate for Daily Repo Automation

## Context

This profile repo is set up to publish one useful AI-builder artifact per day. The risk in that setup is obvious: once the schedule exists, an agent can start farming activity with index churn, timestamps, or generic notes instead of shipping something another builder could reuse.

## Useful Artifact

This repo already has a simple but strong guardrail pattern for coding-agent automation:

- `scripts/new_daily_lab_note.sh` creates a dated note path once and exits early if the file already exists.
- `scripts/commit_daily_update.sh` refreshes public indexes before commit so discoverability stays in sync with the artifact.
- The same commit script exits without committing when `git status --porcelain -- .` shows no real changes.
- The commit step also blocks on missing Git identity or a placeholder local email before creating history.

That combination is more useful than a scheduler-only loop because it makes the artifact, the index, and the commit policy agree on one rule: no useful change, no commit.

## Notes

- Observation: the automation enforces quality mostly through repository mechanics, not prompt wording. The shell scripts are doing the hard gatekeeping.
- Tradeoff: index regeneration means a valid lab note often changes `labs/README.md` too, which is good for visibility but can make small content changes look broader than they are.
- Failure mode: if the agent writes a vague note, the guardrail still allows the commit because the repo sees a file diff. The remaining quality bar has to live in note content and review discipline, not only in bash checks.
- Practical pattern: for public coding-agent repos, treat `git diff` as necessary but not sufficient. Pair it with a narrow artifact definition such as "one tested note, recipe, or source-backed radar entry."

## Verification

Checked locally in the current repo:

- `scripts/new_daily_lab_note.sh` is idempotent for an existing dated file path.
- `scripts/commit_daily_update.sh` refreshes `labs/`, `recipes/`, and `radar/` indexes before deciding whether there is anything useful to commit.
- The commit script verifies `user.name`, `user.email`, and the presence of `origin` before attempting the full publish flow.

## Next Step

Improve the guardrail from "changed files exist" to "changed files include one substantive artifact" so maintenance-only diffs cannot satisfy a daily publish on their own.
