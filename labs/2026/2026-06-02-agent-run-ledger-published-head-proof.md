# 2026-06-02 - Agent Run Ledger Published HEAD Proof

## Context

`repo-flightcheck` can now prove whether local `HEAD` is published on `origin/main`, and `codex-review-packet` can render that proof inside a review packet. The remaining gap was the audit trail: once a packet is imported into `agent-run-ledger`, the public proof should not disappear.

Without that import, a run ledger could preserve changed files, review lanes, CI, readiness, verification, and sensitive-change blockers while losing the question that matters for public proof: is the reviewed commit actually visible on the remote branch?

## Change

- Added `Published HEAD` to the review-packet section parser.
- Added `parseReviewPacketPublishedHead` for rendered packet sections.
- Imports passing published-HEAD proof as command evidence with status `passed`.
- Imports non-passing published-HEAD proof as a `blocked` blocker event, so `doctor --strict` keeps the run open.
- Added tests for parser extraction, passing proof import, blocked proof import, and CLI review-packet import.
- Updated README workflow docs to show the `repo-flightcheck` to `codex-review-packet` to `agent-run-ledger` loop.

Public commit: `2b1f594ebaf1 feat: import published head proof`.

## Verification

Local checks:

```sh
node --test
node scripts/build.js
node scripts/lint.js
git diff --check
node /Users/manuelsampedro/Documents/Codex/2026-05-21/repo-flightcheck/bin/repo-flightcheck.js . --check-remote --strict --threshold 80
node /Users/manuelsampedro/Documents/Codex/2026-05-21/repo-flightcheck/bin/repo-flightcheck.js . --check-remote --json > /tmp/published-head.json
python3 /Users/manuelsampedro/Documents/Codex/2026-05-24/flagships/codex-review-packet/codex_review_packet.py --repo . --published-head /tmp/published-head.json --output /tmp/review-packet.md
node bin/agent-run-ledger.js import-review-packet --ledger /tmp/ledger.jsonl --packet /tmp/review-packet.md
```

Results:

- `node --test`: 47 tests passed.
- `node scripts/build.js`: passed.
- `node scripts/lint.js`: passed.
- `git diff --check`: passed.
- Before push, `repo-flightcheck --check-remote` warned that local `HEAD` was not published on `origin/main`.
- After push, `repo-flightcheck --check-remote --strict --threshold 80`: `98/100`, including `PASS Git remote Origin remote is reachable and local HEAD is published on origin/main.`
- Cross-tool smoke imported a review packet with `Published HEAD proof` into a temporary ledger and doctor JSON showed passed command evidence.
- Commit URL returned HTTP `200`.
- GitHub Actions run `26806046627` completed with conclusion `success`.

## Source Linkage

- Repo: <https://github.com/manuelsampedro1/agent-run-ledger>
- Commit: <https://github.com/manuelsampedro1/agent-run-ledger/commit/2b1f594ebaf15d506044053624de6255de0307bc>
- CI run: <https://github.com/manuelsampedro1/agent-run-ledger/actions/runs/26806046627>
- CLI: <https://raw.githubusercontent.com/manuelsampedro1/agent-run-ledger/main/src/cli.js>
- Tests: <https://raw.githubusercontent.com/manuelsampedro1/agent-run-ledger/main/test/ledger.test.js>
- README: <https://raw.githubusercontent.com/manuelsampedro1/agent-run-ledger/main/README.md>

## Takeaway

Public-proof status should travel through the full handoff chain. It is not enough to check the remote once; the review packet and run ledger should both preserve whether the exact reviewed commit is published.
