# 2026-06-02 - Codex Review Packet Review Map

## Context

`codex-review-packet` already bundled repo context, changed files, diffs, and optional verification checklists. That made review packets sharper, but mixed diffs still had a routing problem: a reviewer saw one flat file list even when the change crossed CI, security, docs, tests, agent instructions, and application code.

For agent-generated work, flat review is weak. The reviewer needs to know which parts deserve specialized attention before reading the full diff.

## Change

- Added a deterministic `Review Map` section to generated packets.
- Routed changed files into path-derived lanes: agent instructions, CI/release, security/permissions, data/persistence, tests/verification, product/docs, application code, and unmapped.
- Added lane-specific focus prompts so reviewers get concrete questions before the diff.
- Kept the map simple and challengeable rather than adding a hidden score.
- Added tests for path classification, review map rendering, and packet inclusion.
- Updated README examples, verification steps, and `DECISIONS.md`.

Public commit: `2d76953f5bcb feat: add review lane map`.

## Verification

Local checks:

```sh
python3 -m py_compile codex_review_packet.py
python3 -m unittest discover -s tests
python3 codex_review_packet.py --repo . >/tmp/review-packet.md
python3 codex_review_packet.py --repo . --diff-lines 80 >/tmp/review-packet-capped.md
printf '## Python\n\n- Run unit tests.\n' >/tmp/verification-checklist.md
python3 codex_review_packet.py --repo . --verification-checklist /tmp/verification-checklist.md >/tmp/review-packet-with-checklist.md
grep -q '## Review Map' /tmp/review-packet.md
test -s /tmp/review-packet.md
git diff --check
```

Results:

- Python compile passed.
- `python3 -m unittest discover -s tests`: 11 tests passed.
- CLI smoke packets were generated and non-empty.
- The generated packet included `## Review Map`.
- `git diff --check` passed.
- Public commit page and raw changed files returned `200`.
- GitHub Actions run `26794611781` completed with conclusion `success`.

## Source Linkage

- Repo: <https://github.com/manuelsampedro1/codex-review-packet>
- Commit: <https://github.com/manuelsampedro1/codex-review-packet/commit/2d76953f5bcb1994647b8f6bb2f13dea7fe28d17>
- CI run: <https://github.com/manuelsampedro1/codex-review-packet/actions/runs/26794611781>
- CLI: <https://raw.githubusercontent.com/manuelsampedro1/codex-review-packet/2d76953f5bcb1994647b8f6bb2f13dea7fe28d17/codex_review_packet.py>
- Tests: <https://raw.githubusercontent.com/manuelsampedro1/codex-review-packet/2d76953f5bcb1994647b8f6bb2f13dea7fe28d17/tests/test_codex_review_packet.py>

## Takeaway

Review packets should route attention before asking for judgment. A deterministic path-derived review map gives the reviewer a stricter first pass without pretending to replace human review.
