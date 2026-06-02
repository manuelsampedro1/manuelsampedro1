# 2026-06-02 - Verify by Change Task Contract Metadata

## Context

`codex-review-packet` can now carry a bounded `## Task Contract` section that says whether the original agent task had objective, acceptance criteria, context, constraints, expected changes, verification, risks, and out-of-scope boundaries.

Before this change, `verify-by-change --review-packet ... --json-envelope` preserved changed files and other packet context, but downstream tools could not see whether the verification plan came from a packet with complete task context.

## Change

- Parsed `## Task Contract` from generated review packets.
- Added optional `task_contract` metadata to `verify-by-change.v1` JSON envelopes.
- Preserved `source`, `status`, `required_sections`, `missing_sections`, and `placeholder_markers`.
- Kept plain Markdown verification output unchanged.
- Updated README and decision notes in the public repo.

Public commit: `4e8380d feat: include task contract metadata`.

## Verification

Local checks:

```sh
python3 -m py_compile verify_by_change.py
python3 -m unittest discover -s tests
make test
make build
make lint
git diff --check
```

Cross-tool smoke:

```sh
python3 /Users/manuelsampedro/Documents/Codex/2026-05-24/flagships/codex-review-packet/codex_review_packet.py \
  --repo . \
  --task-contract /tmp/verify-task-contract.md \
  --output /tmp/verify-review-packet-task-contract.md

python3 verify_by_change.py \
  --review-packet /tmp/verify-review-packet-task-contract.md \
  --json-envelope \
  > /tmp/verify-from-task-contract-packet.json
```

Results:

- `python3 -m unittest discover -s tests`: 41 tests passed.
- `make test`: passed.
- `make build`: passed.
- `make lint`: passed.
- `git diff --check`: passed.
- Cross-tool smoke produced `task_contract.status` as `pass`.
- Cross-tool smoke produced `task_contract.required_sections` as `8/8`.
- Cross-tool smoke produced no missing sections.
- `repo-flightcheck --check-remote --strict --threshold 80`: `100/100`.
- Public commit page returned `200`.
- Raw source and test URLs returned `200`.
- GitHub Actions run `26808615897` completed with conclusion `success`.

## Source Linkage

- Repo: <https://github.com/manuelsampedro1/verify-by-change>
- Commit: <https://github.com/manuelsampedro1/verify-by-change/commit/4e8380d6bed3e36be1715f4849d8b9357f802277>
- CI run: <https://github.com/manuelsampedro1/verify-by-change/actions/runs/26808615897>
- CLI: <https://raw.githubusercontent.com/manuelsampedro1/verify-by-change/4e8380d6bed3e36be1715f4849d8b9357f802277/verify_by_change.py>
- Tests: <https://raw.githubusercontent.com/manuelsampedro1/verify-by-change/4e8380d6bed3e36be1715f4849d8b9357f802277/tests/test_verify_by_change.py>
- Packet generator: <https://github.com/manuelsampedro1/codex-review-packet>

## Takeaway

Verification envelopes should preserve task-contract context from review packets. That does not prove the change is correct, but it tells downstream tools and reviewers whether the verification plan was derived from a complete, scoped agent task.
