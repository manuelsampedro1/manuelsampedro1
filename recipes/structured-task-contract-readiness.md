# Structured Task Contract Readiness

Use this when a downstream tool needs to inspect agent task scope from `repo-flightcheck` output without parsing check messages.

## Goal

Expose task-contract source and completeness as structured JSON in both full readiness reports and compact agent contracts.

## Source Event

This recipe came from updating `repo-flightcheck` so `--json` and `--contract` include the same `taskContract` object.

The public change makes task-contract readiness easier to pass into review packets, ledgers, or merge gates.

## Workflow

1. Add `AGENT_TASK.md` or `TASK_CONTRACT.md` before the agent run.
2. Run `repo-flightcheck --json` for a full readiness report.
3. Run `repo-flightcheck --contract --threshold 80` for compact agent handoff.
4. Check `taskContract.status` before treating the task as fully scoped.
5. Use `missingSections`, `placeholderMarkers`, and `issues` for review blockers or TODOs.

## Example

```sh
node /path/to/repo-flightcheck/bin/repo-flightcheck.js \
  /path/to/repo \
  --contract \
  --threshold 80 \
  > /tmp/repo-readiness-contract.json
```

Expected contract signal:

```json
{
  "schemaVersion": "repo-flightcheck.agent-contract.v1",
  "taskContract": {
    "present": true,
    "source": "AGENT_TASK.md",
    "status": "pass",
    "requiredSections": "8/8",
    "missingSections": [],
    "placeholderMarkers": [],
    "issues": []
  }
}
```

## Checklist

- Does `taskContract.present` match whether the repo has an agent task file?
- Is `taskContract.status` `pass` before starting scoped agent work?
- Are `missingSections` empty?
- Are `placeholderMarkers` empty?
- Are `issues` shown to the next reviewer when the contract is incomplete?
- Is the structured object used instead of scraping the task-contract check message?

## Failure Modes

- Treating `status: pass` as proof that implementation is correct.
- Ignoring `taskContract` because the overall readiness score passes.
- Scraping check prose even though structured fields exist.
- Letting a missing contract silently pass when the run requires a specific scoped task.

## Source Linkage

- Public repo: <https://github.com/manuelsampedro1/repo-flightcheck>
- Commit: <https://github.com/manuelsampedro1/repo-flightcheck/commit/9a7f8d792073dcb3740f47c64b16d5e4d7cb5acc>
- CI run: <https://github.com/manuelsampedro1/repo-flightcheck/actions/runs/26809946918>
- Lab note: <../labs/2026/2026-06-02-repo-flightcheck-structured-task-contract.md>
