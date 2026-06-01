# 2026-06-01 - Expected Paths Contract for Agent Publish Runs

## Context

I wanted to verify the exact contract introduced by this repo's publish guard after adding `expected_paths` support to [`scripts/commit_daily_update.sh`](../../scripts/commit_daily_update.sh).

The open question was practical, not conceptual: does the script now require every publish flow to pass the real artifact path up front, and if so, do generated surface files such as `README.md` and `labs/README.md` also need to be listed?

## Useful Artifact

The reusable rule is: pass only the pre-existing artifact paths you intentionally created before invoking the publish script.

In this repo, that means a lab-note flow should pass the concrete dated note file after the commit message, for example:

```sh
scripts/commit_daily_update.sh \
  "lab: expected paths contract" \
  labs/2026/2026-06-01-expected-paths-contract-for-agent-publish-runs.md
```

The generated surfaces do not belong in that list because the preflight runs before index refresh and README sync.

## Source Linkage

- Repo / tool / workflow: this profile repo's daily publish flow
- Supporting prompt, script, or file: [`scripts/commit_daily_update.sh`](../../scripts/commit_daily_update.sh), [`docs/automation-runbook.md`](../../docs/automation-runbook.md), and [`TODO.md`](../../TODO.md)

## Notes

- Observation: in a temp clone with `origin` removed and a throwaway local Git identity, running [`scripts/commit_daily_update.sh`](../../scripts/commit_daily_update.sh) after creating one new dated lab note but without passing `expected_paths` failed immediately with `Publish blocked: pre-existing changes found in staged public paths:` and listed the new note path.
- Observation: repeating the same run while passing the exact lab note path succeeded and produced a local commit containing only the new note plus the generated surface updates in `labs/README.md` and `README.md`.
- Tradeoff: this contract is stricter than the earlier whole-directory staging flow because every artifact-producing automation now has to know and pass its intended changed paths. The extra explicitness is worth it because it narrows what an agent-run publish is allowed to ship.
- Failure mode: if a lab or recipe automation is not updated to pass its exact artifact path, the publish step will fail even when the artifact itself is valid. That is a good failure, but it will look like a broken automation until every caller adopts the new contract.

## Verification

Local temp-clone verification completed for this note:

- cloned the repo into a temporary directory, removed `origin`, and configured a throwaway local Git identity,
- created `labs/2026/2026-06-01-expected-paths-contract-for-agent-publish-runs.md` with [`scripts/new_daily_lab_note.sh`](../../scripts/new_daily_lab_note.sh),
- case 1: ran [`scripts/commit_daily_update.sh`](../../scripts/commit_daily_update.sh) with only a commit message and confirmed that the script exited non-zero before mutating generated surfaces,
- case 2: reran the same setup while passing the exact note path and confirmed that the script committed the note together with `labs/README.md` and `README.md`,
- inspected `git show --stat HEAD` in the temp clone and confirmed the committed file set matched the intended contract.

## Next Step

Update any lab, recipe, or maintenance automation entrypoints so they always pass the exact artifact paths expected for that run.
