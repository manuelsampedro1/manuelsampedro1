# 2026-06-02 - Agent Run Ledger Task Contract Evidence

## Context

`codex-review-packet` now renders `## Task Contract` sections from `AGENT_TASK.md`, `TASK_CONTRACT.md`, or explicit `--task-contract` input. That makes the review handoff stronger, but the evidence still needed to survive after the packet is imported into a run ledger.

`agent-run-ledger` already imports review packet summaries, review lanes, sensitive-change blockers, repo readiness, CI evidence, published-HEAD proof, and verification checklists. The missing audit link was task-contract evidence: whether the original agent task had complete sections or still contained placeholders.

## Change

- Added `Task Contract` to the recognized review packet sections.
- Added parsing for task contract source, status, required-section count, missing sections, and placeholder markers.
- Imports passing task contracts as `done` decision events.
- Imports non-passing task contracts as `blocked` blocker events so `doctor --strict` keeps the handoff open.
- Records the review packet and task contract source path as ledger files.
- Added unit tests for parser behavior, pass/warn event conversion, and CLI `import-review-packet` import.
- Updated README examples and strict-doctor behavior notes.

Public commit: `9db00e994152 feat: import task contract evidence`.

## Verification

Local checks:

```sh
node --test
node scripts/lint.js
node scripts/build.js
git diff --check
python3 /Users/manuelsampedro/Documents/Codex/2026-05-24/flagships/codex-review-packet/codex_review_packet.py --repo . --task-contract /tmp/agent-run-ledger-task-contract.md --task-contract-lines 40 --output /tmp/agent-run-ledger-review-packet-task-contract.md
node bin/agent-run-ledger.js import-review-packet --ledger /tmp/agent-run-ledger-task-contract-ledger.jsonl --packet /tmp/agent-run-ledger-review-packet-task-contract.md
node bin/agent-run-ledger.js doctor --ledger /tmp/agent-run-ledger-task-contract-ledger.jsonl --strict
grep -q 'Task contract passed' /tmp/agent-run-ledger-task-contract-ledger.jsonl
node /Users/manuelsampedro/Documents/Codex/2026-05-21/repo-flightcheck/bin/repo-flightcheck.js . --check-remote --strict --threshold 80
```

Results:

- `node --test`: 51 tests passed.
- `node scripts/lint.js`: passed.
- `node scripts/build.js`: passed.
- `git diff --check`: passed.
- Cross-tool smoke imported a review packet with task contract as 5 ledger events.
- `doctor --strict` on the smoke ledger reported `Attention: 0`.
- `repo-flightcheck --check-remote --strict --threshold 80`: `98/100`; only warning was missing local `npm`, while direct `node` verification passed.
- `origin/main` points to `9db00e99415254a351d0aa66a29a30beeb6b11e2`.
- Commit URL returned HTTP `200`.
- Raw `src/cli.js` and `test/ledger.test.js` returned HTTP `200`.
- GitHub Actions run `26808167644` completed with conclusion `success`.

## Source Linkage

- Repo: <https://github.com/manuelsampedro1/agent-run-ledger>
- Commit: <https://github.com/manuelsampedro1/agent-run-ledger/commit/9db00e99415254a351d0aa66a29a30beeb6b11e2>
- CI run: <https://github.com/manuelsampedro1/agent-run-ledger/actions/runs/26808167644>
- CLI: <https://raw.githubusercontent.com/manuelsampedro1/agent-run-ledger/main/src/cli.js>
- Tests: <https://raw.githubusercontent.com/manuelsampedro1/agent-run-ledger/main/test/ledger.test.js>
- README: <https://raw.githubusercontent.com/manuelsampedro1/agent-run-ledger/main/README.md>

## Takeaway

Task contracts should not disappear after review packet import. If the task was incomplete, the ledger should keep that as a blocker; if it was complete, the ledger should preserve the contract source as part of the audit trail.
