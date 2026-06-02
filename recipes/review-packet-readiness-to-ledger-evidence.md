# Review Packet Readiness to Ledger Evidence

Use this when a `codex-review-packet` handoff includes `## Repo Readiness` and the run ledger should preserve that readiness state directly.

## Goal

Import review packet context, review lanes, repo readiness, and planned verification checks into `agent-run-ledger` with one command.

## Source Event

This recipe came from updating `agent-run-ledger import-review-packet` to parse the `## Repo Readiness` Markdown emitted by `codex-review-packet`.

The public change makes direct packet import preserve readiness evidence without requiring a separate `import-readiness` run or an intermediate JSON envelope.

## Workflow

1. Generate a readiness report or agent contract with `repo-flightcheck`.
2. Render a review packet with `codex-review-packet --readiness-report`.
3. Import the review packet into `agent-run-ledger`.
4. Run `doctor --json` or `doctor --strict` to verify readiness blockers and planned checks are visible.
5. Record follow-up verification events as checks pass, fail, or get skipped with reason.

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
  --verify-by-change /path/to/verify-by-change/verify_by_change.py \
  --output /tmp/review-packet.md

node /path/to/agent-run-ledger/bin/agent-run-ledger.js \
  import-review-packet \
  --ledger /tmp/agent-run-ledger.jsonl \
  --packet /tmp/review-packet.md

node /path/to/agent-run-ledger/bin/agent-run-ledger.js \
  doctor \
  --ledger /tmp/agent-run-ledger.jsonl \
  --json
```

Expected ledger signals:

```json
[
  {
    "type": "decision",
    "title": "Review packet: 3 changed files"
  },
  {
    "type": "command",
    "title": "Repo readiness: 96/100",
    "status": "blocked"
  },
  {
    "type": "blocker",
    "title": "Readiness warn: Working tree",
    "status": "blocked"
  }
]
```

## Checklist

- Does the packet include `## Repo Readiness`?
- Does ledger import include a `Repo readiness` event?
- Are required readiness checks represented as blockers?
- Are review lanes still present as decision events?
- Are embedded verification checklist sections still imported as planned command events?

## Failure Modes

- Importing a packet generated before the latest working tree state.
- Running `import-review-packet` and assuming planned checks have passed.
- Dropping readiness because the packet was generated without `--readiness-report`.
- Treating readiness score as behavior correctness instead of repo-state context.

## Source Linkage

- Public repo: <https://github.com/manuelsampedro1/agent-run-ledger>
- Commit: <https://github.com/manuelsampedro1/agent-run-ledger/commit/2ac96029bbb58dfd1db45dbde76c6332d0ee5c05>
- CI run: <https://github.com/manuelsampedro1/agent-run-ledger/actions/runs/26800182143>
- Related recipe: <./verification-envelope-readiness-to-ledger.md>
