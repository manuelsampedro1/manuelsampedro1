# Sensitive Review Packet to Ledger Evidence

Use this when a review packet flags secret material, authorization and approval paths, or deploy/release paths and the handoff needs an auditable closeout.

## Goal

Carry sensitive review requirements from `codex-review-packet` into `agent-run-ledger` so `doctor --strict` keeps the handoff open until those paths are explicitly reviewed.

## Source Event

This recipe came from adding `Sensitive Change Check` import support to `agent-run-ledger`.

The public change turns each sensitive review packet category into a blocked ledger event instead of leaving it as passive Markdown.

## Workflow

1. Generate a review packet with `codex-review-packet`.
2. Confirm the packet includes `## Sensitive Change Check` when sensitive paths changed.
3. Import the packet into a ledger with `agent-run-ledger import-review-packet`.
4. Run `agent-run-ledger doctor --strict`.
5. Treat `Sensitive change: ...` blocker events as required reviewer work before merge.
6. Record the follow-up review or resolution as ledger evidence.
7. Keep CI evidence attached, but do not use CI success as a substitute for sensitive-path review.

## Example

```sh
python3 /path/to/codex-review-packet/codex_review_packet.py \
  --repo /path/to/target-repo \
  --base origin/main \
  --output /tmp/review-packet.md

node /path/to/agent-run-ledger/bin/agent-run-ledger.js import-review-packet \
  --ledger .agent-run/ledger.jsonl \
  --packet /tmp/review-packet.md

node /path/to/agent-run-ledger/bin/agent-run-ledger.js doctor \
  --ledger .agent-run/ledger.jsonl \
  --strict
```

Expected ledger signal:

```text
Ledger OK: 4 events
Files: 3
Commands: 0
Open commands: 0
Attention: 2
```

## Checklist

- Does the packet contain `## Sensitive Change Check` for secret, auth, approval, deploy, or release paths?
- Did import create `Sensitive change: ...` blocker events?
- Does `doctor --strict` fail while those blockers are unresolved?
- Did the closeout record how each sensitive category was reviewed?
- Is CI evidence tied to the same commit SHA as the packet?

## Failure Modes

- Letting sensitive paths remain only in packet Markdown where the ledger report does not surface them.
- Treating a review lane as equivalent to an explicit sensitive-risk blocker.
- Closing strict doctor with planned verification still open.
- Claiming sensitive paths are safe because CI passed.
- Importing a packet generated for a different base commit than the reviewed change.

## Source Linkage

- Public repo: <https://github.com/manuelsampedro1/agent-run-ledger>
- Commit: <https://github.com/manuelsampedro1/agent-run-ledger/commit/dfee2519370f165f509297378a600bd1f88f422d>
- CI run: <https://github.com/manuelsampedro1/agent-run-ledger/actions/runs/26804279018>
- Lab note: <../labs/2026/2026-06-02-agent-run-ledger-sensitive-review-packets.md>
