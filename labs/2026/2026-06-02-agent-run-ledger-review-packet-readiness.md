# 2026-06-02 - Agent Run Ledger Review Packet Readiness

## Context

`agent-run-ledger import-review-packet` could already record a review packet, changed files, review lanes, and embedded verification checks. But when the packet included `## Repo Readiness`, that readiness context was lost unless the user separately imported a readiness report or routed through a `verify-by-change` JSON envelope.

That made the direct review-packet path weaker than the envelope path.

## Change

- Added `parseReviewPacketReadiness` for the Markdown `## Repo Readiness` section emitted by `codex-review-packet`.
- Parsed contract metrics such as ready state, score, required blockers, recommendations, and critical failures.
- Parsed rendered readiness checks from `Required before agent`, `Recommended before agent`, and `Attention checks` blocks.
- Updated `parseReviewPacket` to attach a normalized readiness report.
- Updated `reviewPacketEvents` so readiness evidence is imported between review lanes and planned verification commands.
- Updated README behavior notes.
- Added parser, event, and CLI import tests.

Public commit: `2ac96029bbb5 feat: import review packet readiness`.

## Verification

Local checks:

```sh
node --test
node scripts/lint.js
node scripts/build.js
git diff --check
node /Users/manuelsampedro/Documents/Codex/2026-05-21/repo-flightcheck/bin/repo-flightcheck.js . --strict --threshold 80
```

Cross-tool smoke:

```sh
node /Users/manuelsampedro/Documents/Codex/2026-05-21/repo-flightcheck/bin/repo-flightcheck.js . --contract --threshold 80 > /tmp/readiness-contract.json
python3 /Users/manuelsampedro/Documents/Codex/2026-05-24/flagships/codex-review-packet/codex_review_packet.py --repo . --readiness-report /tmp/readiness-contract.json --output /tmp/review-packet.md
node bin/agent-run-ledger.js import-review-packet --ledger /tmp/ledger.jsonl --packet /tmp/review-packet.md
node bin/agent-run-ledger.js doctor --ledger /tmp/ledger.jsonl --json
```

Results:

- `node --test`: 32 tests passed.
- `node scripts/lint.js`: passed.
- `node scripts/build.js`: passed.
- `git diff --check`: passed.
- Dirty-tree smoke imported 6 events, including `Repo readiness: 96/100` as `blocked` and `Readiness warn: Working tree` as a blocker.
- Clean post-commit `repo-flightcheck`: `100/100`.
- GitHub Actions run `26800182143` completed with conclusion `success`.

The local shell had `node` but not `npm`, so local validation ran the package scripts directly. Public CI covered the repository workflow after push.

## Source Linkage

- Repo: <https://github.com/manuelsampedro1/agent-run-ledger>
- Commit: <https://github.com/manuelsampedro1/agent-run-ledger/commit/2ac96029bbb58dfd1db45dbde76c6332d0ee5c05>
- CI run: <https://github.com/manuelsampedro1/agent-run-ledger/actions/runs/26800182143>
- CLI: <https://raw.githubusercontent.com/manuelsampedro1/agent-run-ledger/main/src/cli.js>
- Tests: <https://raw.githubusercontent.com/manuelsampedro1/agent-run-ledger/main/test/ledger.test.js>
- Packet renderer: <https://github.com/manuelsampedro1/codex-review-packet>

## Takeaway

The direct review-packet path should be as evidence-preserving as the envelope path. If a packet already contains repo readiness, importing that packet into a ledger should keep blockers and scores visible without requiring a second import command.
