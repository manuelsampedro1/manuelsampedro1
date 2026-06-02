# Agent Readiness Contract Output

Use this when a readiness scan needs to become an input to another agent workflow.

## Goal

Turn repo readiness checks into compact JSON that a review packet, run ledger, or CI gate can consume without parsing a full human report.

## Source Event

This recipe came from adding `--contract` to `repo-flightcheck`.

The public change made the scanner emit `repo-flightcheck.agent-contract.v1` with readiness, detected commands, required blockers, recommendations, and next fixes.

## Workflow

1. Run `repo-flightcheck` on a clean working tree.
2. Choose the readiness threshold expected by the workflow.
3. Generate a compact contract with `--contract`.
4. Treat `requiredBeforeAgent` as blockers before handing the repo to an agent.
5. Treat `recommendedBeforeAgent` as review notes unless the project policy makes them mandatory.
6. Store or import the contract with the review packet, run ledger, or CI evidence.
7. Re-run after fixing blockers and require `ready: true` before claiming readiness.

## Example

```sh
node /path/to/repo-flightcheck/bin/repo-flightcheck.js \
  /path/to/target-repo \
  --contract \
  --threshold 80
```

Expected ready shape:

```json
{
  "schemaVersion": "repo-flightcheck.agent-contract.v1",
  "ready": true,
  "score": 100,
  "commands": {
    "test": "npm test",
    "build": "npm run build",
    "lint": "npm run lint"
  },
  "requiredBeforeAgent": [],
  "recommendedBeforeAgent": []
}
```

## Checklist

- Is the working tree clean before generating the contract?
- Does `ready` use the same threshold as the receiving workflow?
- Are high and critical unresolved checks treated as blockers?
- Are command fields copied into the next verification plan?
- Is the contract regenerated after README, AGENTS.md, CI, or script changes?

## Failure Modes

- Importing a contract generated before the latest diff.
- Treating recommendations as irrelevant when the receiving workflow has stricter policy.
- Ignoring a dirty-tree blocker because local changes are "just documentation."
- Using the score alone and missing unresolved high-severity checks.
- Claiming readiness from a local contract without checking CI when CI is part of the repo's quality bar.

## Source Linkage

- Public repo: <https://github.com/manuelsampedro1/repo-flightcheck>
- Commit: <https://github.com/manuelsampedro1/repo-flightcheck/commit/8b1253b593c66b44b775512a237756ca04b79697>
- CI run: <https://github.com/manuelsampedro1/repo-flightcheck/actions/runs/26798783115>
- Lab note: <../labs/2026/2026-06-02-repo-flightcheck-agent-readiness-contract.md>
