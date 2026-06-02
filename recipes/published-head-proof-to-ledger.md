# Published HEAD Proof to Ledger

Use this when a run ledger imports a review packet that includes public-proof evidence.

## Goal

Keep published-HEAD proof visible after review packet import, so a ledger can show whether the exact reviewed commit was public.

## Source Event

This recipe came from adding `Published HEAD` import support to `agent-run-ledger`. The import now treats passing proof as command evidence and non-passing proof as a blocker.

## Workflow

1. Generate published-head evidence with `repo-flightcheck --check-remote --json`.
2. Generate a review packet with `codex-review-packet --published-head`.
3. Import that packet with `agent-run-ledger import-review-packet`.
4. Run `agent-run-ledger doctor --strict`.
5. If the published-head status is not `pass`, leave the run open until the commit is pushed or the remote issue is fixed.
6. Only use the ledger as public proof after published HEAD, CI, and verification evidence all align.

## Example

```sh
node /path/to/repo-flightcheck/bin/repo-flightcheck.js \
  /path/to/repo \
  --check-remote \
  --json \
  > /tmp/published-head.json

python3 /path/to/codex-review-packet/codex_review_packet.py \
  --repo /path/to/repo \
  --published-head /tmp/published-head.json \
  --output /tmp/review-packet.md

node /path/to/agent-run-ledger/bin/agent-run-ledger.js \
  import-review-packet \
  --ledger /tmp/ledger.jsonl \
  --packet /tmp/review-packet.md
```

Expected ledger behavior:

- `Status: pass` becomes command evidence named `Published HEAD proof`.
- Any non-pass status becomes a `Published HEAD blocked` blocker.
- `doctor --strict` fails while the blocker remains.

## Checklist

- Does the review packet include `## Published HEAD`?
- Does the ledger include `Published HEAD proof` after import?
- Does non-pass proof create a blocker, not a soft note?
- Does the ledger also include CI evidence for the same SHA?
- Does the final closeout avoid public links until `doctor --strict` is clean?

## Failure Modes

- Losing public-proof status when a review packet becomes a ledger.
- Treating a warning from `repo-flightcheck` as an informational note instead of a blocker.
- Recording CI success without confirming the reviewed commit is on the remote branch.
- Reusing a stale review packet after another local commit.

## Source Linkage

- Public repo: <https://github.com/manuelsampedro1/agent-run-ledger>
- Commit: <https://github.com/manuelsampedro1/agent-run-ledger/commit/2b1f594ebaf15d506044053624de6255de0307bc>
- CI run: <https://github.com/manuelsampedro1/agent-run-ledger/actions/runs/26806046627>
- Lab note: <../labs/2026/2026-06-02-agent-run-ledger-published-head-proof.md>
