# Repo Readiness to Ledger Evidence

Use this when a repo readiness scan should become part of an auditable agent run.

## Goal

Record `repo-flightcheck --json` output in `agent-run-ledger` before or after agent work, so setup risks become durable evidence rather than a separate JSON file that reviewers might miss.

## Source Event

This recipe came from `agent-run-ledger` commit `d1710f505311`, which added `import-readiness` for `repo-flightcheck --json` reports.

Relevant files:

- `src/cli.js`
- `test/ledger.test.js`
- `README.md`

## Workflow

1. Run `repo-flightcheck` against the target repo.
2. Save the JSON readiness report.
3. Import the report into the run ledger.
4. Let clean reports become passed command evidence.
5. Let critical or failed checks become blocker events.
6. Run strict doctor mode before closing the handoff.

## Commands

```sh
node /path/to/repo-flightcheck/bin/repo-flightcheck.js /path/to/repo --json > /tmp/repo-readiness.json
node /path/to/agent-run-ledger/bin/agent-run-ledger.js import-readiness \
  --ledger /path/to/repo/.agent-run/ledger.jsonl \
  --readiness-report /tmp/repo-readiness.json \
  --command "node /path/to/repo-flightcheck/bin/repo-flightcheck.js /path/to/repo --json"
node /path/to/agent-run-ledger/bin/agent-run-ledger.js doctor \
  --ledger /path/to/repo/.agent-run/ledger.jsonl \
  --strict
```

## Checklist

- Does the readiness report come from the same repo path the agent will edit?
- Does the ledger include the report path as evidence?
- Do failed or critical readiness checks become blocker events?
- Does strict doctor fail when readiness blockers are unresolved?
- If the report is clean, does the ledger record one passed readiness event?

## Verification

For `agent-run-ledger`:

```sh
node --test
node bin/agent-run-ledger.js import-readiness --ledger /tmp/ledger.jsonl --readiness-report /tmp/repo-readiness.json
node bin/agent-run-ledger.js doctor --ledger /tmp/ledger.jsonl --strict
```

## Failure Modes

- Importing a stale readiness report from a different repo path.
- Treating failed readiness checks as informational notes instead of blockers.
- Leaving the readiness JSON outside the ledger and then losing the setup context during review.
- Recording the readiness command without preserving the report path.

## Source Linkage

- Public repo: <https://github.com/manuelsampedro1/agent-run-ledger>
- Commit: <https://github.com/manuelsampedro1/agent-run-ledger/commit/d1710f50531171a9e8e6edce95d416531711f882>
- CI run: <https://github.com/manuelsampedro1/agent-run-ledger/actions/runs/26796019884>
