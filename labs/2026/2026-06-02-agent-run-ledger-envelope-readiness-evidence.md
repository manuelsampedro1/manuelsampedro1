# 2026-06-02 - Agent Run Ledger Envelope Readiness Evidence

## Context

`verify-by-change --review-packet ... --json-envelope` can now carry `repo_readiness` from a `codex-review-packet` handoff. `agent-run-ledger import-checklist` already imported verification commands from JSON envelopes, but it ignored that readiness context.

That left a gap in the agent proof loop: a ledger could record what to verify, while losing whether the source packet said the repo was ready, blocked, or below threshold.

## Change

- Split JSON envelope parsing so `agent-run-ledger` can reuse the full payload, not only category commands.
- Added `parseVerificationEnvelopeReadiness` for embedded `repo_readiness`.
- Added `readinessEventsFromVerificationEnvelope` to turn that readiness summary into ledger evidence.
- Updated `import-checklist` so JSON envelopes import readiness evidence before planned verification commands.
- Treated `null` readiness metrics as missing values, not as zero.
- Added parser, event, and CLI import tests.
- Updated README behavior notes.

Public commit: `69921dbca0ef feat: import envelope readiness evidence`.

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
python3 /Users/manuelsampedro/Documents/Codex/2026-05-24/flagships/verify-by-change/verify_by_change.py --review-packet /tmp/review-packet.md --json-envelope --output /tmp/verification-envelope.json
node bin/agent-run-ledger.js import-checklist --ledger /tmp/ledger.jsonl --checklist /tmp/verification-envelope.json
node bin/agent-run-ledger.js doctor --ledger /tmp/ledger.jsonl --json
```

Results:

- `node --test`: 31 tests passed.
- `node scripts/lint.js`: passed.
- `node scripts/build.js`: passed.
- `git diff --check`: passed.
- Dirty-tree smoke imported 3 ledger events, including `Repo readiness: 96/100` as `blocked` with 1 required blocker.
- Clean post-commit `repo-flightcheck`: `100/100`.
- GitHub Actions run `26799928892` completed with conclusion `success`.

The local shell had `node` but not `npm`, so local validation ran the package scripts directly. Public CI covered the repository workflow after push.

## Source Linkage

- Repo: <https://github.com/manuelsampedro1/agent-run-ledger>
- Commit: <https://github.com/manuelsampedro1/agent-run-ledger/commit/69921dbca0efddd377c467ca87040bddba8b9043>
- CI run: <https://github.com/manuelsampedro1/agent-run-ledger/actions/runs/26799928892>
- CLI: <https://raw.githubusercontent.com/manuelsampedro1/agent-run-ledger/main/src/cli.js>
- Tests: <https://raw.githubusercontent.com/manuelsampedro1/agent-run-ledger/main/test/ledger.test.js>
- Upstream envelope source: <https://github.com/manuelsampedro1/verify-by-change>

## Takeaway

A ledger should not only store the generated verification commands. If the verification envelope came from a review packet, the ledger should preserve the readiness state that shaped that packet, including blocked states and required blockers.
