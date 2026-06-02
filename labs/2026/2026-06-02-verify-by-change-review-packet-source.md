# 2026-06-02 - Verify by Change Review Packet Source

## Context

`codex-review-packet` can generate a compact Markdown handoff with changed files, repo context, review lanes, and verification guidance.

That packet is often what a reviewer or follow-up agent has in hand. Before this change, `verify-by-change` could inspect repo diffs and working-tree state, but it could not reuse a packet as the source of changed files.

## Change

- Added `--review-packet` to `verify-by-change`.
- Parsed the `## Changed Files` section from `codex-review-packet` Markdown.
- De-duped inline-code file bullets before classification.
- Added a `review_packet` JSON envelope source type.
- Rejected ambiguous inputs that combine `--review-packet` with explicit paths or `--repo`.
- Reported missing packet files without a traceback.
- Updated README and decision notes in the public repo.

Public commit: `9e8720e715 feat: read review packet changes`.

## Verification

Local checks:

```sh
make test
make build
make lint
git diff --check
python3 /Users/manuelsampedro/Documents/Codex/2026-05-24/flagships/codex-review-packet/codex_review_packet.py --repo . --output /tmp/verify-review-packet.md
python3 verify_by_change.py --review-packet /tmp/verify-review-packet.md
python3 verify_by_change.py --review-packet /tmp/verify-review-packet.md --json-envelope
python3 verify_by_change.py --review-packet /tmp/verify-review-packet.md README.md
node /Users/manuelsampedro/Documents/Codex/2026-05-21/repo-flightcheck/bin/repo-flightcheck.js . --strict --threshold 80
```

Results:

- `make test`: 23 tests passed.
- `make build`: passed.
- `make lint`: passed.
- `git diff --check`: passed.
- Cross-tool smoke generated a review packet, then produced verification guidance from that packet.
- JSON envelope reported `source.type` as `review_packet`.
- Conflict smoke rejected mixed packet and explicit-path inputs.
- `repo-flightcheck`: `100/100` after commit.
- Public commit page returned `200`.
- Raw `verify_by_change.py` returned `200`.
- GitHub Actions run `26797987666` completed with conclusion `success`.

## Source Linkage

- Repo: <https://github.com/manuelsampedro1/verify-by-change>
- Commit: <https://github.com/manuelsampedro1/verify-by-change/commit/9e8720e7150bf5faa6731e2a5a16027b90b93742>
- CI run: <https://github.com/manuelsampedro1/verify-by-change/actions/runs/26797987666>
- CLI: <https://raw.githubusercontent.com/manuelsampedro1/verify-by-change/main/verify_by_change.py>
- Tests: <https://raw.githubusercontent.com/manuelsampedro1/verify-by-change/main/tests/test_verify_by_change.py>
- Packet generator: <https://github.com/manuelsampedro1/codex-review-packet>

## Takeaway

A review packet can be a verification planning input, but not proof that checks ran. This keeps the agent workflow honest: packet for scope, checklist for expected checks, command output for evidence.
