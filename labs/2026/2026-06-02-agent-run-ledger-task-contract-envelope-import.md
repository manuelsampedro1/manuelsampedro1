# 2026-06-02 - Agent Run Ledger Task Contract Envelope Import

## Context

`verify-by-change` can now preserve `task_contract` metadata in a `verify-by-change.v1` JSON envelope when the verification plan comes from a `codex-review-packet` handoff.

Before this change, `agent-run-ledger import-checklist` could import verification commands and embedded repo readiness from that envelope, but it dropped whether the verification plan was scoped by a complete task contract.

## Change

- Parsed `task_contract` from `verify-by-change.v1` JSON envelopes.
- Imported passing task contracts as `done` decision events.
- Imported incomplete task contracts as `blocked` blocker events.
- Kept task-contract evidence before readiness and planned verification commands in the ledger.
- Updated README guidance for envelope imports.

Public commit: `123639a feat: import task contract envelopes`.

## Verification

Local checks:

```sh
node --test
node scripts/lint.js
node scripts/build.js
git diff --check
```

Cross-tool smoke:

```sh
python3 /Users/manuelsampedro/Documents/Codex/2026-05-24/flagships/codex-review-packet/codex_review_packet.py \
  --repo /Users/manuelsampedro/Documents/Codex/2026-05-21/agent-run-ledger \
  --task-contract /tmp/AGENT_TASK.md \
  --output /tmp/review-packet.md

python3 /Users/manuelsampedro/Documents/Codex/2026-05-24/flagships/verify-by-change/verify_by_change.py \
  --review-packet /tmp/review-packet.md \
  --json-envelope \
  --output /tmp/verification-envelope.json

node bin/agent-run-ledger.js import-checklist \
  --ledger /tmp/ledger.jsonl \
  --checklist /tmp/verification-envelope.json
```

Results:

- `node --test`: 54 tests passed.
- `node scripts/lint.js`: passed.
- `node scripts/build.js`: passed.
- `git diff --check`: passed.
- Cross-tool smoke produced `task_contract.status` as `pass`.
- Cross-tool smoke produced `task_contract.required_sections` as `8/8`.
- Cross-tool smoke imported 3 ledger events with `Attention: 0`.
- `repo-flightcheck --check-remote --strict --threshold 80`: `95/100`; warnings were the intentional dirty working tree before commit and missing local `npm`, while direct `node` checks passed.
- Public commit page returned `200`.
- Raw source and test URLs returned `200`.
- GitHub Actions run `26809075266` completed with conclusion `success`.

## Source Linkage

- Repo: <https://github.com/manuelsampedro1/agent-run-ledger>
- Commit: <https://github.com/manuelsampedro1/agent-run-ledger/commit/123639a2a6816b003f945608301f30253640d7ee>
- CI run: <https://github.com/manuelsampedro1/agent-run-ledger/actions/runs/26809075266>
- CLI: <https://raw.githubusercontent.com/manuelsampedro1/agent-run-ledger/123639a2a6816b003f945608301f30253640d7ee/src/cli.js>
- Tests: <https://raw.githubusercontent.com/manuelsampedro1/agent-run-ledger/123639a2a6816b003f945608301f30253640d7ee/test/ledger.test.js>
- Verification envelope source: <https://github.com/manuelsampedro1/verify-by-change>
- Packet generator: <https://github.com/manuelsampedro1/codex-review-packet>

## Takeaway

A verification envelope should not lose the task boundary that produced it. Importing `task_contract` into the ledger lets reviewers distinguish between "we have a verification plan" and "that plan was derived from a complete scoped task."
