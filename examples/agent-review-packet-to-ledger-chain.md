# Agent Review Packet to Ledger Chain

Use this example when a coding-agent change needs to survive beyond the chat:
the reviewer should be able to inspect the repo context, changed files,
verification plan, and open evidence in one durable ledger.

## Scenario

A non-trivial agent run has a local diff and the maintainer wants a reviewable
handoff before closeout. The flow should:

- package the diff and repo context,
- derive change-aware verification from that packet,
- import the packet into a run ledger,
- keep planned checks open until real command evidence is recorded,
- render a static report that can be reviewed later.

## Command Chain

```sh
python3 /path/to/codex-review-packet/codex_review_packet.py \
  --repo /path/to/repo \
  --verify-by-change /path/to/verify-by-change/verify_by_change.py \
  --output /tmp/review-packet.md

python3 /path/to/verify-by-change/verify_by_change.py \
  --review-packet /tmp/review-packet.md \
  --json-envelope \
  --output /tmp/verification-envelope.json

node /path/to/agent-run-ledger/bin/agent-run-ledger.js start \
  --ledger /tmp/agent-run-ledger.jsonl \
  --goal "Review and verify the current agent diff"

node /path/to/agent-run-ledger/bin/agent-run-ledger.js import-review-packet \
  --ledger /tmp/agent-run-ledger.jsonl \
  --packet /tmp/review-packet.md \
  --command "codex-review-packet with verify-by-change"

node /path/to/agent-run-ledger/bin/agent-run-ledger.js import-checklist \
  --ledger /tmp/agent-run-ledger.jsonl \
  --checklist /tmp/verification-envelope.json

node /path/to/agent-run-ledger/bin/agent-run-ledger.js doctor \
  --ledger /tmp/agent-run-ledger.jsonl \
  --strict

node /path/to/agent-run-ledger/bin/agent-run-ledger.js report \
  --ledger /tmp/agent-run-ledger.jsonl \
  --out /tmp/agent-run-report.html
```

## Expected Signals

- The review packet should name the changed files and include a suggested review
  prompt.
- The verification envelope should preserve source metadata from the review
  packet instead of becoming anonymous checklist prose.
- Ledger import should add packet context, changed-file evidence, and planned
  verification commands.
- `doctor --strict` may intentionally return non-zero while planned checks are
  still open. That is useful: it prevents a handoff from looking complete before
  tests, lint, build, CI, or reviewer checks actually run.
- The HTML report should render the current state even when strict doctor mode
  says more evidence is required.

## Observed Signals From This Profile Fixture

This chain was tested against the profile repo while this example file was still
an untracked working-tree change.

- `codex-review-packet` wrote a packet with `## Review Map`.
- The packet included `examples/agent-review-packet-to-ledger-chain.md`.
- `verify-by-change --review-packet ... --json-envelope` emitted
  `verify-by-change.v1`.
- The envelope listed 2 changed files from the packet.
- `agent-run-ledger import-review-packet` and `import-checklist` produced a
  5-event ledger.
- `agent-run-ledger doctor --strict` exited `1` with `Open commands: 2` and
  `Attention: 0`.
- `agent-run-ledger report` rendered an HTML report.

## Reviewer Interpretation

This chain separates three jobs that are often blurred in a final answer:

- `codex-review-packet` packages context for review.
- `verify-by-change` proposes the checks that match the changed files.
- `agent-run-ledger` preserves the packet and keeps unfinished evidence visible.

Do not close the run just because a packet exists. Close it only when the ledger
contains executed command outcomes or explicit skipped/blocked decisions for
every planned check that matters.

## Review Prompt

```text
Review this handoff as durable run evidence. Confirm the review packet contains
the relevant repo context and diff, the verification envelope matches the
changed files, and the run ledger keeps planned checks open until real evidence
is recorded. Flag any closeout that treats planned verification as executed
verification.
```
