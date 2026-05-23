# Codex Debugging Checklist

## Use When

Use this after a Codex edit when a bug persists, a check failed twice, or the repo context is still too fuzzy for another blind patch.

## Source Linkage

- Repo / tool / workflow: [codex-review-packet](https://github.com/manuelsampedro1/codex-review-packet) and this profile repo's maintenance/debugging loop.
- Supporting prompt, script, or note: [`labs/2026/2026-05-22-agent-artifact-gate.md`](../labs/2026/2026-05-22-agent-artifact-gate.md) and [`scripts/commit_daily_update.sh`](../scripts/commit_daily_update.sh).

## Steps

1. Restate the failure in one sentence with the exact command, file, or user path that broke.
2. Read the closest local rules before changing code again: `AGENTS.md`, `README.md`, `DECISIONS.md`, `TODO.md`, or adjacent code.
3. Reproduce with the smallest safe command you can run locally.
4. Check whether the problem is logic, repo context, environment, or wrong verification.
5. Compare two or three plausible fixes before editing again.
6. Apply the smallest fix that changes the failing condition directly.
7. Re-run only the checks that prove the bug moved.

## Checks

- Can you name the exact trigger, not just the symptom?
- Did you inspect local repo rules before another patch?
- Did the rerun prove the changed behavior, not just produce a cleaner diff?
- If the same error appeared twice, did you stop and investigate instead of patching faster?

## Example

When `codex-review-packet` failed in a fresh repo with no commits, the right move was not "retry with another base ref". The useful loop was:

1. reproduce the failure,
2. identify that `HEAD` did not exist yet,
3. decide whether the tool should support that state,
4. patch the script to fall back to untracked-file handling,
5. rerun the local verification.
