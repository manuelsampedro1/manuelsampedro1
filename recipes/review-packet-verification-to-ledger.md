# Review Packet Verification to Ledger

Use this when a review packet already contains generated verification guidance and the handoff needs to stay open until those checks are handled.

## Goal

Convert embedded packet verification into ledger command events so `doctor --strict` can detect unexecuted checks.

## Source Event

This recipe came from updating `agent-run-ledger import-review-packet` to parse embedded `## Verification Checklist` sections.

The public change imports packet summary, review lanes, and planned verification commands in one step.

## Workflow

1. Generate a review packet with `codex-review-packet`.
2. Include verification guidance with `--verify-by-change` or `--verification-checklist`.
3. Import the review packet into the ledger.
4. Run `doctor --strict` and expect it to fail while planned checks are open.
5. Record executed commands as `passed`, `failed`, `skipped`, or `blocked`.
6. Re-run `doctor --strict` before final handoff.

## Example

```sh
python3 /path/to/codex-review-packet/codex_review_packet.py \
  --repo /path/to/repo \
  --verify-by-change /path/to/verify-by-change/verify_by_change.py \
  --output /tmp/review-packet.md

node /path/to/agent-run-ledger/bin/agent-run-ledger.js import-review-packet \
  --ledger /tmp/ledger.jsonl \
  --packet /tmp/review-packet.md \
  --command "python3 codex_review_packet.py --repo /path/to/repo --verify-by-change verify_by_change.py"

node /path/to/agent-run-ledger/bin/agent-run-ledger.js doctor \
  --ledger /tmp/ledger.jsonl \
  --strict
```

## Checklist

- Does the packet include the intended changed files?
- Does the packet include a `## Verification Checklist` section?
- Does ledger import create review lane events and planned command events?
- Does `doctor --strict` fail while planned checks remain open?
- Are actual command results recorded separately from generated guidance?

## Failure Modes

- Treating imported planned commands as proof that checks already passed.
- Importing a stale packet generated before the diff changed.
- Letting headings inside repo context or diff blocks confuse packet parsing.
- Closing the ledger without recording skipped or blocked checks explicitly.

## Source Linkage

- Public repo: <https://github.com/manuelsampedro1/agent-run-ledger>
- Commit: <https://github.com/manuelsampedro1/agent-run-ledger/commit/c0ad4a62d1e3b820778dd31755b67deb03099508>
- CI run: <https://github.com/manuelsampedro1/agent-run-ledger/actions/runs/26798504388>
- Lab note: <../labs/2026/2026-06-02-agent-run-ledger-packet-verification-import.md>
