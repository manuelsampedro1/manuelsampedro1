# 2026-06-02 - Codex Review Packet Task Contract Envelope Summary

## Context

`verify-by-change` can preserve `task_contract` metadata in JSON envelopes, and `agent-run-ledger` can import that metadata into durable audit events.

Before this change, `codex-review-packet` rendered `verify-by-change.v1` envelopes as readable Markdown checklists, but it did not show the envelope's task-contract status in the packet unless the reviewer opened the raw JSON.

## Change

- Rendered compact task-contract status from `verify-by-change.v1` envelopes.
- Included task-contract source, missing sections, and placeholder markers when present.
- Kept the summary outside the fenced checklist body so downstream packet parsers do not mistake it for a top-level packet section.
- Updated README guidance and decision notes in the public repo.

Public commit: `4a4019d feat: render task contract envelope context`.

## Verification

Local checks:

```sh
python3 -m py_compile codex_review_packet.py
python3 -m unittest discover -s tests
make test
make build
make lint
git diff --check
```

Cross-tool smoke:

```sh
python3 codex_review_packet.py \
  --repo /Users/manuelsampedro/Documents/Codex/2026-05-24/flagships/codex-review-packet \
  --task-contract /tmp/AGENT_TASK.md \
  --verify-by-change /Users/manuelsampedro/Documents/Codex/2026-05-24/flagships/verify-by-change/verify_by_change.py \
  --output /tmp/review-packet.md

node /Users/manuelsampedro/Documents/Codex/2026-05-21/agent-run-ledger/bin/agent-run-ledger.js import-review-packet \
  --ledger /tmp/ledger.jsonl \
  --packet /tmp/review-packet.md
```

Results:

- `python3 -m unittest discover -s tests`: 45 tests passed.
- `make test`: passed.
- `make build`: passed.
- `make lint`: passed.
- `git diff --check`: passed.
- Cross-tool smoke rendered `Task contract: pass (8/8 required sections)`.
- Cross-tool smoke imported 7 ledger events with `Attention: 0`.
- `repo-flightcheck --check-remote --strict --threshold 80`: `100/100`.
- Public commit page returned `200`.
- Raw source and test URLs returned `200`.
- GitHub Actions run `26809468718` completed with conclusion `success`.

## Source Linkage

- Repo: <https://github.com/manuelsampedro1/codex-review-packet>
- Commit: <https://github.com/manuelsampedro1/codex-review-packet/commit/4a4019d4f9894e24ac068aecde189da24e6354a0>
- CI run: <https://github.com/manuelsampedro1/codex-review-packet/actions/runs/26809468718>
- Packet generator: <https://raw.githubusercontent.com/manuelsampedro1/codex-review-packet/4a4019d4f9894e24ac068aecde189da24e6354a0/codex_review_packet.py>
- Tests: <https://raw.githubusercontent.com/manuelsampedro1/codex-review-packet/4a4019d4f9894e24ac068aecde189da24e6354a0/tests/test_codex_review_packet.py>
- Verification envelope source: <https://github.com/manuelsampedro1/verify-by-change>
- Ledger importer: <https://github.com/manuelsampedro1/agent-run-ledger>

## Takeaway

Review packets should make automation metadata readable at the handoff point. A reviewer should not need to open raw JSON to see whether the generated verification plan came from a complete task contract.
