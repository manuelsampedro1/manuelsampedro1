# Verification Envelope in Review Packets

Use this when a generated review packet should carry automation-friendly verification metadata without forcing reviewers to read raw JSON.

## Goal

Preserve `verify-by-change` source metadata and categories while keeping the final Codex or Claude Code packet readable.

## Source Event

This recipe came from adding `verify-by-change.v1` envelope rendering to `codex-review-packet`.

The public change lets `codex-review-packet --verification-checklist` accept a JSON envelope and render it as Markdown inside the packet.

## Workflow

1. Generate the verification plan as a JSON envelope.
2. Pass the envelope file into `codex-review-packet --verification-checklist`.
3. Inspect the packet's `## Verification Checklist` section before handoff.
4. Confirm the section names the envelope schema and source.
5. Run the planned checks separately and record exact command results elsewhere, such as a final closeout or ledger.

## Example

```sh
python3 /path/to/verify-by-change/verify_by_change.py \
  --repo /path/to/repo \
  --json-envelope \
  --output /tmp/verification-envelope.json

python3 /path/to/codex-review-packet/codex_review_packet.py \
  --repo /path/to/repo \
  --verification-checklist /tmp/verification-envelope.json \
  --output /tmp/review-packet.md
```

## Checklist

- Does the packet show `Envelope: verify-by-change.v1`?
- Does the verification source match the repo, base, staged state, or review packet being handed off?
- Are changed files listed before category-specific commands?
- Is raw JSON absent from the verification section?
- Are planned checks clearly separated from checks that were actually executed?

## Failure Modes

- Treating the envelope as proof that verification commands passed.
- Passing an envelope generated from a stale diff or different base ref.
- Losing source metadata by converting JSON to plain text too early.
- Embedding raw JSON that a human reviewer will skip.
- Publishing a packet with private local paths when the handoff should be public.

## Source Linkage

- Public repo: <https://github.com/manuelsampedro1/codex-review-packet>
- Commit: <https://github.com/manuelsampedro1/codex-review-packet/commit/669346be5b7260a3511aab68e136050b7e128bd3>
- CI run: <https://github.com/manuelsampedro1/codex-review-packet/actions/runs/26798250260>
- Lab note: <../labs/2026/2026-06-02-codex-review-packet-verification-envelope.md>
