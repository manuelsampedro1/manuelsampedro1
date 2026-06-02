# Review Packet Readiness to Verification Envelope

Use this when a review packet already contains repo readiness context and the verification envelope needs to preserve it.

## Goal

Carry the `## Repo Readiness` section from a `codex-review-packet` handoff into `verify-by-change --json-envelope` output.

## Source Event

This recipe came from updating `verify-by-change --review-packet ... --json-envelope` to include `repo_readiness`.

The public change lets one review packet feed downstream verification gates without losing readiness status, threshold, blockers, or score.

## Workflow

1. Generate a readiness contract from the target repo.
2. Generate a review packet with that contract passed through `--readiness-report`.
3. Generate a verification envelope from the review packet.
4. Check `repo_readiness.ready` and `repo_readiness.required_blockers` before treating the verification plan as complete.
5. Import the same packet or contract into a ledger if the run needs durable evidence.

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
```

Expected envelope signal:

```json
{
  "schema_version": "verify-by-change.v1",
  "source": { "type": "review_packet" },
  "repo_readiness": {
    "contract": "repo-flightcheck.agent-contract.v1",
    "ready": true,
    "score": 100,
    "threshold": 80,
    "required_blockers": 0
  }
}
```

## Checklist

- Was the review packet generated after the current diff or working tree state?
- Does the packet include `## Repo Readiness`?
- Does the envelope include `repo_readiness`?
- Are readiness blockers checked before accepting generated verification guidance?
- Are changed files and readiness context coming from the same packet?

## Failure Modes

- Creating a verification envelope from a packet generated before the latest code change.
- Treating `repo_readiness.ready` as proof that the changed behavior is correct.
- Losing readiness context by using explicit file paths instead of `--review-packet`.
- Letting packet readiness and ledger readiness come from different artifacts.

## Source Linkage

- Public repo: <https://github.com/manuelsampedro1/verify-by-change>
- Commit: <https://github.com/manuelsampedro1/verify-by-change/commit/b310c861b6f22d1fd15174071a5ca26e9f722fd1>
- CI run: <https://github.com/manuelsampedro1/verify-by-change/actions/runs/26799554734>
- Lab note: <../labs/2026/2026-06-02-verify-by-change-packet-readiness-context.md>
