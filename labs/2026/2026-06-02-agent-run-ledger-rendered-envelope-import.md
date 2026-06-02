# 2026-06-02 - Agent Run Ledger Rendered Envelope Import

## Context

`codex-review-packet` now renders generated `verify-by-change.v1` envelopes into Markdown review packets. `agent-run-ledger` could already import raw JSON envelopes, but a rendered envelope inside a review packet was treated like anonymous Markdown.

## Change

- Added rendered `verify-by-change.v1` envelope detection in `agent-run-ledger`.
- Preserved envelope schema, source, and verification source metadata when importing review packets.
- Kept checklist commands as planned ledger command events.
- Included envelope source files when the source points to a real artifact.
- Added tests for rendered envelope parsing and review-packet event import.
- Updated the repo README to describe the packet-to-ledger metadata path.

## Verification

- `node --test`: 40 tests passed.
- `node scripts/build.js`: passed.
- `node scripts/lint.js`: passed.
- `git diff --check`: passed.
- Integrated smoke: generated a review packet with real `codex-review-packet` and `verify-by-change`, imported it into a ledger, and confirmed ledger JSONL contained `verify-by-change.v1 verification envelope` plus `Verification source`.
- `repo-flightcheck --strict --threshold 80`: 100/100 after commit.
- GitHub Actions run `26802727474`: success for commit `815d2ce85071117f056e30726e461e38d9a3ea71`.

Note: local `npm` was not available in this Codex session PATH, so local verification used direct Node equivalents. The public GitHub Actions run completed successfully on the pushed commit.

## Source Linkage

- Repo: https://github.com/manuelsampedro1/agent-run-ledger
- Commit: https://github.com/manuelsampedro1/agent-run-ledger/commit/815d2ce85071117f056e30726e461e38d9a3ea71
- CI run: https://github.com/manuelsampedro1/agent-run-ledger/actions/runs/26802727474
- Source: https://raw.githubusercontent.com/manuelsampedro1/agent-run-ledger/main/src/cli.js
- Tests: https://raw.githubusercontent.com/manuelsampedro1/agent-run-ledger/main/test/ledger.test.js
- Packet producer: https://github.com/manuelsampedro1/codex-review-packet
- Verification generator: https://github.com/manuelsampedro1/verify-by-change

## Takeaway

Agent audit trails should not discard metadata that was preserved upstream. If a review packet carries structured verification source data, the ledger should keep that provenance visible when it turns the packet into planned command evidence.
