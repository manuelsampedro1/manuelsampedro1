# 2026-06-03 - Residual Scratch Warnings After Agent Publish

## Context

I wanted to verify the cleanup behavior of this repo's publish helper after the
expected-path guard was already satisfied.

The open question was operational: if a lab-note automation publishes a valid
artifact but leaves unrelated local scratch outside the managed public paths,
does the run fail, silently ignore the residue, or surface a warning that the
next automation can act on?

## Useful Artifact

The reusable rule is: treat a successful publish plus a residual-change warning
as "artifact shipped, workspace still dirty," not as a clean success.

In this repo, [`scripts/commit_daily_update.sh`](../../scripts/commit_daily_update.sh)
commits the intended public artifact first, then runs a whole-worktree warning
check:

```sh
remaining_changes="$(git status --porcelain -- .)"
```

That means scratch outside the managed public paths does not block the current
artifact, but it is still called out before the next automation run can inherit
it by accident.

## Source Linkage

- Repo / tool / workflow: this profile repo's daily publish flow
- Supporting prompt, script, or file: [`scripts/commit_daily_update.sh`](../../scripts/commit_daily_update.sh),
  [`tests/test_commit_daily_update.sh`](../../tests/test_commit_daily_update.sh),
  and [`TODO.md`](../../TODO.md)

## Notes

- Observation: in a temp repo that copied this publish script, a valid lab-note
  publish with the exact expected note path succeeded even when an unrelated
  untracked `scratch.log` file was present.
- Observation: after the local commit, the script printed `Warning: working tree
  still has uncommitted changes after this publish run:` followed by the
  scratch path and `Review or move scratch files before the next automation
  run.`
- Tradeoff: warning instead of blocking keeps publish momentum for the intended
  public artifact while still making leftover local state explicit.
- Failure mode: if an automation or operator treats a green publish as a fully
  clean workspace, the next run can start from a misleading baseline and mix old
  scratch into future work.
- Implementation detail: this behavior is already encoded as a shell fixture in
  [`tests/test_commit_daily_update.sh`](../../tests/test_commit_daily_update.sh),
  so the warning contract is part of the repo's verification surface, not only
  a manual expectation.

## Verification

Local verification completed for this note:

- ran the repo fixture [`tests/test_commit_daily_update.sh`](../../tests/test_commit_daily_update.sh)
  to confirm the no-op path still warns when `scratch.log` remains after the run,
- created a temp Git repo with a tracked `labs/2026/` path, copied
  [`scripts/commit_daily_update.sh`](../../scripts/commit_daily_update.sh) plus
  stub index scripts, committed an initial state, then added a new dated lab
  note and an unrelated untracked `scratch.log`,
- ran `scripts/commit_daily_update.sh "lab: scratch warning test" labs/2026/2026-06-03-residual-scratch-warnings-after-agent-publish.md`
  in that temp repo and confirmed it exited `0`, created a local commit for the
  note, and still warned about `scratch.log`,
- inspected `git show --stat HEAD` in the temp repo and confirmed the commit
  only contained the intended lab note while `git status --short` still showed
  `?? scratch.log`.

## Next Step

During future GitHub automation runs, treat the residual-change warning as a
required cleanup checkpoint and clear or relocate scratch before the next
publish step.
