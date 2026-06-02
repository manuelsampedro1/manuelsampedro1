# Readiness Contract to Ledger Evidence

Use this when a repo readiness contract needs to become auditable evidence in an agent run ledger.

## Goal

Record `repo-flightcheck --contract` output as ledger evidence so required readiness blockers stay visible before or after an agent run.

## Source Event

This recipe came from updating `agent-run-ledger import-readiness` to accept `repo-flightcheck.agent-contract.v1`.

The public change lets a compact readiness contract become command evidence, blocker events, and reviewer-visible file references.

## Workflow

1. Generate a contract from the target repo.
2. Import the contract into the run ledger.
3. Run `doctor --strict`.
4. Treat `requiredBeforeAgent` blockers as work that must be resolved or explicitly accepted.
5. Record follow-up command evidence after blockers are fixed, skipped, or accepted.
6. Re-run `repo-flightcheck --contract` on a clean tree before final handoff.

## Example

```sh
node /path/to/repo-flightcheck/bin/repo-flightcheck.js \
  /path/to/target-repo \
  --contract \
  --threshold 80 \
  > /tmp/repo-readiness-contract.json

node /path/to/agent-run-ledger/bin/agent-run-ledger.js import-readiness \
  --ledger /path/to/target-repo/.agent-run/ledger.jsonl \
  --readiness-report /tmp/repo-readiness-contract.json \
  --command "repo-flightcheck --contract --threshold 80"

node /path/to/agent-run-ledger/bin/agent-run-ledger.js doctor \
  --ledger /path/to/target-repo/.agent-run/ledger.jsonl \
  --strict
```

## Checklist

- Was the contract generated after the current diff or working tree state?
- Does `ready` match the threshold expected by the workflow?
- Did every `requiredBeforeAgent` entry become a blocker event?
- Did Git status evidence such as ` M README.md` resolve to the actual file?
- Does `doctor --strict` fail while blockers or open command evidence remain?
- Is a fresh clean-tree contract recorded before final closeout?

## Failure Modes

- Importing a stale contract generated before the agent changed files.
- Treating `recommendedBeforeAgent` as proof that no follow-up is needed.
- Recording the contract but never re-running it after blockers are fixed.
- Using a different threshold in the contract than in CI or review policy.
- Relying on the score alone while ignoring required blocker fields.

## Source Linkage

- Public repo: <https://github.com/manuelsampedro1/agent-run-ledger>
- Commit: <https://github.com/manuelsampedro1/agent-run-ledger/commit/331b91fdd4058f8086342250c9b165c8b8a6e00a>
- CI run: <https://github.com/manuelsampedro1/agent-run-ledger/actions/runs/26799042402>
- Lab note: <../labs/2026/2026-06-02-agent-run-ledger-readiness-contract-import.md>
