# 2026-06-02 - Codex Review Packet CI Evidence

## Context

`codex-review-packet` could already package diffs, repo rules, local context, readiness reports, readiness contracts, and generated verification plans.

The remaining gap was public CI evidence. A review handoff can say "CI passed", but the packet is stronger when it carries the GitHub Actions run ID, conclusion, URL, and SHA that prove what actually passed.

## Change

- Added optional `--ci-run` input to `codex-review-packet`.
- Accepted both single GitHub Actions run JSON and `workflow_runs` list payloads.
- Rendered a dedicated `## CI Evidence` section with source path, run ID, workflow, status, conclusion, branch, SHA, event, and URL.
- Preserved existing readiness and verification packet behavior.
- Added parser, renderer, packet-builder, and CLI tests.
- Updated README examples and verification notes.

Public commit: `25b526a9aa7e feat: embed ci run evidence`.

## Verification

Local checks:

```sh
python3 -m py_compile codex_review_packet.py
python3 -m unittest discover -s tests
make test
make build
make lint
git diff --check
python3 codex_review_packet.py --repo . --ci-run /tmp/ci-run.json --output /tmp/review-packet.md
grep -q '## CI Evidence' /tmp/review-packet.md
```

Results:

- `python3 -m py_compile`: passed.
- `python3 -m unittest discover -s tests`: 30 tests passed.
- `make test`, `make build`, and `make lint`: passed.
- Temp CI JSON smoke rendered `## CI Evidence`, `Conclusion: success`, and the expected SHA.
- `repo-flightcheck`: `100/100` after commit.
- GitHub Actions run `26801172625` completed with conclusion `success`.
- Fetching the real run JSON from GitHub Actions and rebuilding a packet preserved run `26801172625`, conclusion `success`, and commit `25b526a9aa7e252d3da12fc26e10affb40bfc1cd`.

## Source Linkage

- Repo: <https://github.com/manuelsampedro1/codex-review-packet>
- Commit: <https://github.com/manuelsampedro1/codex-review-packet/commit/25b526a9aa7e252d3da12fc26e10affb40bfc1cd>
- CI run: <https://github.com/manuelsampedro1/codex-review-packet/actions/runs/26801172625>
- Packet generator: <https://raw.githubusercontent.com/manuelsampedro1/codex-review-packet/main/codex_review_packet.py>
- Tests: <https://raw.githubusercontent.com/manuelsampedro1/codex-review-packet/main/tests/test_codex_review_packet.py>

## Takeaway

Review packets should make external verification inspectable. If the handoff includes CI evidence with a run URL, conclusion, and SHA, a reviewer can challenge the claim without reconstructing the whole chat.
