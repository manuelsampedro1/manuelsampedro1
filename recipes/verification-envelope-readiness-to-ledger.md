# Verification Envelope Readiness to Ledger Evidence

Use this when a `verify-by-change` JSON envelope includes `repo_readiness` and the agent run ledger should preserve that readiness state.

## Goal

Import both the verification commands and the embedded repo readiness summary into `agent-run-ledger`.

## Source Event

This recipe came from updating `agent-run-ledger import-checklist` to preserve `repo_readiness` from `verify-by-change --review-packet ... --json-envelope`.

The public change prevents downstream ledgers from losing readiness status, required blockers, and score after a review packet becomes a verification envelope.

## Workflow

1. Generate a repo readiness contract with `repo-flightcheck`.
2. Render a review packet with `codex-review-packet --readiness-report`.
3. Generate a JSON verification envelope from that review packet.
4. Import the envelope into `agent-run-ledger`.
5. Run `agent-run-ledger doctor --strict` so planned checks and blocked readiness stay visible.

## Example

```sh
node /path/to/repo-flightcheck/bin/repo-flightcheck.js \
  /path/to/target-repo \
  --contract \
  --threshold 80 \
  > /tmp/repo-readiness-contract.json

python3 /path/to/codex-review-packet/codex_review_packet.py \
  --repo /path/to/target-repo \
  --readiness-report /tmp/repo-readiness-contract.json \
  --output /tmp/review-packet.md

python3 /path/to/verify-by-change/verify_by_change.py \
  --review-packet /tmp/review-packet.md \
  --json-envelope \
  --output /tmp/verification-envelope.json

node /path/to/agent-run-ledger/bin/agent-run-ledger.js \
  import-checklist \
  --ledger /tmp/agent-run-ledger.jsonl \
  --checklist /tmp/verification-envelope.json
```

Expected ledger signal:

```json
{
  "type": "command",
  "title": "Repo readiness: 96/100",
  "status": "blocked",
  "summary": "Imported repo-flightcheck report from /tmp/verification-envelope.json. 0 passed, 0 warnings, 1 failed, 0 critical failures, 1 required blockers."
}
```

## Checklist

- Does the envelope include `repo_readiness`?
- Does the ledger include a `Repo readiness` event before the planned verification commands?
- Does a blocked readiness state remain visible in `doctor --json` or `doctor --strict`?
- Are planned verification commands still imported from the envelope categories?
- Did the review packet, envelope, and ledger come from the same repo state?

## Failure Modes

- Importing an older envelope after the working tree changed.
- Treating readiness as proof that behavior is correct instead of as repo-state context.
- Dropping `repo_readiness` when converting packets to verification guidance.
- Marking `null` readiness metrics as zero and accidentally turning blocked context into clean context.

## Source Linkage

- Public repo: <https://github.com/manuelsampedro1/agent-run-ledger>
- Commit: <https://github.com/manuelsampedro1/agent-run-ledger/commit/69921dbca0efddd377c467ca87040bddba8b9043>
- CI run: <https://github.com/manuelsampedro1/agent-run-ledger/actions/runs/26799928892>
- Related recipe: <./review-packet-readiness-to-verification-envelope.md>
