# GitHub Actions Run Evidence to Ledger

Use this after pushing agent-assisted work when the final handoff needs CI evidence that a reviewer can inspect.

## Goal

Turn "CI passed" into a ledger event with a specific run ID, URL, status, conclusion, branch, and SHA.

## Source Event

This recipe came from adding `import-ci` to `agent-run-ledger`.

The public change lets a ledger import GitHub Actions run JSON and store it as command evidence.

## Workflow

1. Push the repo change.
2. Wait for the relevant GitHub Actions run to complete.
3. Fetch the run JSON from the GitHub Actions API.
4. Import the JSON into the run ledger with `agent-run-ledger import-ci`.
5. Run `agent-run-ledger doctor --json` to confirm the CI evidence is not open or attention-worthy.
6. Link the run URL in the final handoff or generated report.

## Example

```sh
curl -fsS \
  https://api.github.com/repos/OWNER/REPO/actions/runs/RUN_ID \
  > /tmp/ci-run.json

node /path/to/agent-run-ledger/bin/agent-run-ledger.js import-ci \
  --ledger .agent-run/ledger.jsonl \
  --ci-run /tmp/ci-run.json \
  --command "GitHub Actions CI"

node /path/to/agent-run-ledger/bin/agent-run-ledger.js doctor \
  --ledger .agent-run/ledger.jsonl \
  --json
```

## Checklist

- Does the imported JSON refer to the same commit SHA that was pushed?
- Is the run `completed` with conclusion `success` before claiming it passed?
- Did the ledger event preserve the run URL?
- Does `doctor --strict` have no open command evidence or blockers?
- If CI failed, does the ledger record `failed` instead of hiding the run?

## Failure Modes

- Claiming CI passed from memory instead of a run URL.
- Importing the latest run from the wrong branch or older commit.
- Treating `in_progress` as passed.
- Dropping the SHA, making the evidence hard to connect to the commit.
- Keeping CI evidence outside the ledger, so the generated report misses the strongest verification signal.

## Source Linkage

- Public repo: <https://github.com/manuelsampedro1/agent-run-ledger>
- Commit: <https://github.com/manuelsampedro1/agent-run-ledger/commit/072dcdca2feeaac7d29125b356d3e28c016c636e>
- CI run: <https://github.com/manuelsampedro1/agent-run-ledger/actions/runs/26800961149>
- Lab note: <../labs/2026/2026-06-02-agent-run-ledger-ci-evidence-import.md>
