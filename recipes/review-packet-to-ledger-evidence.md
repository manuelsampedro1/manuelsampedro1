# Review Packet to Ledger Evidence

Use this when a Codex or Claude Code handoff should be kept as durable audit evidence.

## Goal

Turn a generated review packet into ledger events that a reviewer can inspect later without reopening the original chat or rebuilding the packet.

## Source Event

This recipe came from adding `import-review-packet` to `agent-run-ledger`.

The public change lets the ledger parse `codex-review-packet` Markdown and record the packet summary, changed files, and review lanes.

## Workflow

1. Generate a review packet from the repo and scope that need review.
2. Include generated verification guidance when useful.
3. Import the packet into the run ledger.
4. Record the packet-generation command so the artifact is reproducible.
5. Run `doctor --json` to confirm the ledger has no open commands or attention items unless the run is intentionally incomplete.
6. Render the static report for the reviewer.

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

node /path/to/agent-run-ledger/bin/agent-run-ledger.js doctor --ledger /tmp/ledger.jsonl --json
node /path/to/agent-run-ledger/bin/agent-run-ledger.js report --ledger /tmp/ledger.jsonl --out /tmp/report.html
```

## Checklist

- Does the packet list the intended changed files?
- Are review lanes captured as ledger events?
- Is the packet file itself referenced in the ledger?
- Is the packet-generation command recorded?
- Does `doctor --json` show open commands or attention items that should block handoff?
- Is the rendered report non-empty and shareable without private chat context?

## Failure Modes

- Importing a packet generated from a different base or staged state.
- Recording the packet without the command that produced it.
- Treating review-lane events as proof that review happened.
- Committing private packet content when the ledger should stay local or attached only to a private handoff.

## Source Linkage

- Public repo: <https://github.com/manuelsampedro1/agent-run-ledger>
- Commit: <https://github.com/manuelsampedro1/agent-run-ledger/commit/4ac9bf1e65e043126280786b448275054d564dd8>
- CI run: <https://github.com/manuelsampedro1/agent-run-ledger/actions/runs/26797769875>
- Lab note: <../labs/2026/2026-06-02-agent-run-ledger-review-packet-import.md>
