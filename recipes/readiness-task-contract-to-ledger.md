# Readiness Task Contract to Ledger Evidence

Use this when `repo-flightcheck` emits structured `taskContract` metadata and the run ledger should preserve that scope signal alongside readiness evidence.

## Goal

Record task-contract completeness from a readiness report before importing repo readiness checks into the agent run ledger.

## Source Event

This recipe came from updating `agent-run-ledger import-readiness` to import `taskContract` from `repo-flightcheck --json` and `repo-flightcheck --contract` output.

The public change connects the pre-run repo readiness check with post-run auditability: `repo-flightcheck` declares whether the task contract is complete, and `agent-run-ledger` keeps that as durable evidence.

## Workflow

1. Write `AGENT_TASK.md` or `TASK_CONTRACT.md` before agent work starts.
2. Run `repo-flightcheck --json` or `repo-flightcheck --contract` after the current diff is in place.
3. Import the readiness artifact with `agent-run-ledger import-readiness`.
4. Run `agent-run-ledger doctor --strict`.
5. Treat `Task contract needs attention` as a blocker, not a warning to ignore.
6. Record actual verification command outcomes separately after commands run.

## Example

```sh
node /path/to/repo-flightcheck/bin/repo-flightcheck.js \
  /path/to/repo \
  --json \
  > /tmp/repo-readiness.json

node /path/to/agent-run-ledger/bin/agent-run-ledger.js import-readiness \
  --ledger /path/to/repo/.agent-run/ledger.jsonl \
  --readiness-report /tmp/repo-readiness.json \
  --command "repo-flightcheck --json"

node /path/to/agent-run-ledger/bin/agent-run-ledger.js doctor \
  --ledger /path/to/repo/.agent-run/ledger.jsonl \
  --strict
```

Expected ledger signal when the contract passes:

```text
Task contract passed
Repo readiness: 98/100
```

Expected ledger signal when the contract has gaps:

```text
Task contract needs attention
Repo readiness: 95/100
```

## Checklist

- Was the readiness report generated after the current diff or task context?
- Does `taskContract.present` reflect a real `AGENT_TASK.md` or `TASK_CONTRACT.md`?
- Does `taskContract.status` equal `pass` before treating the scope as complete?
- Are `missingSections` and `placeholderMarkers` visible in the ledger blocker?
- Does readiness evidence stay separate from actual command results?
- Does `doctor --strict` fail while the task contract is incomplete?

## Failure Modes

- Treating task-contract completeness as proof that tests passed.
- Importing a stale readiness report from before the task contract changed.
- Allowing a readiness score to hide missing task sections.
- Recording actual command results from a planned readiness import.
- Mixing a task contract from one repo with readiness evidence from another.

## Source Linkage

- Public repo: <https://github.com/manuelsampedro1/agent-run-ledger>
- Commit: <https://github.com/manuelsampedro1/agent-run-ledger/commit/2ac604b2fc0068d2f68cbed23b20cec33fa012d4>
- CI run: <https://github.com/manuelsampedro1/agent-run-ledger/actions/runs/26810454727>
- Lab note: <../labs/2026/2026-06-02-agent-run-ledger-readiness-task-contract.md>
- Readiness source: <https://github.com/manuelsampedro1/repo-flightcheck>
