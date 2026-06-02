# Rendered Verification Envelope to Ledger Evidence

Use this when a review packet contains a rendered `verify-by-change.v1` envelope and the handoff needs to become auditable ledger evidence.

## Workflow

1. Generate a review packet with `codex-review-packet --verify-by-change /path/to/verify_by_change.py`.
2. Confirm the packet's `Verification Checklist` section includes `Envelope: verify-by-change.v1`.
3. Import the packet with `agent-run-ledger import-review-packet --ledger .agent-run/ledger.jsonl --packet /tmp/review-packet.md`.
4. Check the resulting ledger for planned `Verify ...` command events.
5. Confirm those command summaries include the envelope schema and verification source.
6. Run `agent-run-ledger doctor --ledger .agent-run/ledger.jsonl --strict` so planned checks keep the handoff open until resolved.

## Checklist

- The review packet includes changed files and review lanes.
- The verification checklist was generated from repo-aware `verify-by-change`.
- The ledger records the packet source and changed files.
- The ledger command summaries preserve `verify-by-change.v1` provenance.
- Planned verification commands are later updated to `passed`, `skipped`, `failed`, or `blocked`.

## Failure Modes

- Importing a rendered envelope as anonymous Markdown and losing source metadata.
- Recording planned commands but not running strict doctor afterward.
- Treating the packet import itself as proof that verification passed.
- Dropping the packet path from ledger files, making the evidence hard to trace.
- Using a generated checklist without repo context, which can miss CLI or package-specific checks.

## Source

- Lab note: <../labs/2026/2026-06-02-agent-run-ledger-rendered-envelope-import.md>
- Repo: https://github.com/manuelsampedro1/agent-run-ledger
- Commit: https://github.com/manuelsampedro1/agent-run-ledger/commit/815d2ce85071117f056e30726e461e38d9a3ea71
- CI run: https://github.com/manuelsampedro1/agent-run-ledger/actions/runs/26802727474
