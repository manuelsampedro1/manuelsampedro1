# 2026-06-02 - Agent Run Ledger Packet Verification Import

## Context

`codex-review-packet` can embed a `verify-by-change` checklist in the handoff artifact. `agent-run-ledger` could already import review packets and import checklists separately, but importing the packet did not turn the embedded checklist into planned command evidence.

That left a small workflow gap: the packet said what should be verified, but `doctor --strict` did not know those checks were still open.

## Change

- Parsed the `## Verification Checklist` section from imported review packets.
- Ignored packet-like headings that appear inside repo context or diff blocks.
- Converted embedded checklist sections into `planned` command events.
- Kept review packet summary and review lane events intact.
- Added parser, event-builder, CLI import, and strict-doctor tests.
- Updated README behavior notes.

Public commit: `c0ad4a62d1 feat: import packet verification checks`.

## Verification

Local checks:

```sh
node --test
node scripts/build.js
node scripts/lint.js
git diff --check
python3 /Users/manuelsampedro/Documents/Codex/2026-05-24/flagships/codex-review-packet/codex_review_packet.py --repo /Users/manuelsampedro/Documents/Codex/2026-05-21/agent-run-ledger --verify-by-change /Users/manuelsampedro/Documents/Codex/2026-05-24/flagships/verify-by-change/verify_by_change.py --output /tmp/agent-run-ledger-review-packet-verification-smoke/review-packet.md
node bin/agent-run-ledger.js import-review-packet --ledger /tmp/agent-run-ledger-review-packet-verification-smoke/ledger.jsonl --packet /tmp/agent-run-ledger-review-packet-verification-smoke/review-packet.md --command "python3 codex_review_packet.py --repo agent-run-ledger --verify-by-change verify_by_change.py"
node bin/agent-run-ledger.js doctor --ledger /tmp/agent-run-ledger-review-packet-verification-smoke/ledger.jsonl --json
node bin/agent-run-ledger.js doctor --ledger /tmp/agent-run-ledger-review-packet-verification-smoke/ledger.jsonl --strict
node bin/agent-run-ledger.js report --ledger /tmp/agent-run-ledger-review-packet-verification-smoke/ledger.jsonl --out /tmp/agent-run-ledger-review-packet-verification-smoke/report.html
node /Users/manuelsampedro/Documents/Codex/2026-05-21/repo-flightcheck/bin/repo-flightcheck.js . --strict --threshold 80
```

Results:

- `node --test`: 25 tests passed.
- `node scripts/build.js`: passed.
- `node scripts/lint.js`: passed.
- `git diff --check`: passed.
- Cross-tool smoke imported 6 ledger events from a generated review packet.
- Doctor JSON reported 4 commands and 3 open planned commands.
- Strict doctor exited non-zero while planned checks remained open.
- Static HTML report was generated and non-empty.
- `repo-flightcheck`: `100/100` after commit.
- Public commit page returned `200`.
- Raw `src/cli.js` and tests returned `200`.
- GitHub Actions run `26798504388` completed with conclusion `success`.

Note: `npm` was not available in the local shell, so the local checks ran the direct Node commands behind the package scripts. GitHub Actions ran the `npm` workflow successfully.

## Source Linkage

- Repo: <https://github.com/manuelsampedro1/agent-run-ledger>
- Commit: <https://github.com/manuelsampedro1/agent-run-ledger/commit/c0ad4a62d1e3b820778dd31755b67deb03099508>
- CI run: <https://github.com/manuelsampedro1/agent-run-ledger/actions/runs/26798504388>
- CLI: <https://raw.githubusercontent.com/manuelsampedro1/agent-run-ledger/main/src/cli.js>
- Tests: <https://raw.githubusercontent.com/manuelsampedro1/agent-run-ledger/main/test/ledger.test.js>
- Packet generator: <https://github.com/manuelsampedro1/codex-review-packet>
- Checklist generator: <https://github.com/manuelsampedro1/verify-by-change>

## Takeaway

Review packets should not only preserve context; they should preserve pending verification obligations. Importing embedded checks as planned command events makes strict handoffs fail open until the reviewer records actual evidence.
