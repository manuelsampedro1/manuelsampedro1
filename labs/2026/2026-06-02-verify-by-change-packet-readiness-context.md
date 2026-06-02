# 2026-06-02 - Verify by Change Packet Readiness Context

## Context

`codex-review-packet` can render a `repo-flightcheck.agent-contract.v1` readiness contract, and `agent-run-ledger` can import that contract as evidence. `verify-by-change` could read changed files from a review packet, but its JSON envelope dropped the packet's `## Repo Readiness` summary.

That meant the verification envelope knew what files changed, but not whether the packet had already identified repo-readiness blockers.

## Change

- Parsed the `## Repo Readiness` section from `codex-review-packet` Markdown.
- Extracted contract metadata such as ready state, score, threshold, stack, required blockers, recommendations, and critical failures.
- Also parsed the older full `repo-flightcheck --json` report summary format rendered by review packets.
- Added `repo_readiness` to `verify-by-change --json-envelope` when the source is `--review-packet`.
- Kept legacy `--json` output unchanged.
- Added parser and CLI envelope tests.
- Updated README examples to show `--review-packet ... --json-envelope`.

Public commit: `b310c861b6f2 feat: carry packet readiness context`.

## Verification

Local checks:

```sh
python3 -m py_compile verify_by_change.py
python3 -m unittest discover -s tests
make test
make build
make lint
git diff --check
node /Users/manuelsampedro/Documents/Codex/2026-05-21/repo-flightcheck/bin/repo-flightcheck.js . --strict --threshold 80
node /Users/manuelsampedro/Documents/Codex/2026-05-21/repo-flightcheck/bin/repo-flightcheck.js . --contract --threshold 80
python3 /Users/manuelsampedro/Documents/Codex/2026-05-24/flagships/codex-review-packet/codex_review_packet.py --repo . --readiness-report /tmp/readiness-contract.json --output /tmp/review-packet.md
python3 verify_by_change.py --review-packet /tmp/review-packet.md --json-envelope --output /tmp/verification-envelope.json
```

Results:

- `python3 -m py_compile`: passed.
- `python3 -m unittest discover -s tests`: 26 tests passed.
- `make test`, `make build`, and `make lint`: passed.
- Dirty-tree smoke before commit preserved `repo_readiness.ready: false`, score `96`, and 1 required blocker.
- Clean-tree smoke after commit preserved `repo_readiness.ready: true`, score `100`, and 0 required blockers.
- `repo-flightcheck`: `100/100` after commit.
- GitHub Actions run `26799554734` completed with conclusion `success`.

## Source Linkage

- Repo: <https://github.com/manuelsampedro1/verify-by-change>
- Commit: <https://github.com/manuelsampedro1/verify-by-change/commit/b310c861b6f22d1fd15174071a5ca26e9f722fd1>
- CI run: <https://github.com/manuelsampedro1/verify-by-change/actions/runs/26799554734>
- CLI: <https://raw.githubusercontent.com/manuelsampedro1/verify-by-change/main/verify_by_change.py>
- Tests: <https://raw.githubusercontent.com/manuelsampedro1/verify-by-change/main/tests/test_verify_by_change.py>
- Packet renderer: <https://github.com/manuelsampedro1/codex-review-packet>
- Ledger importer: <https://github.com/manuelsampedro1/agent-run-ledger>

## Takeaway

Verification plans should preserve readiness context when they come from a review packet. The envelope can now tell downstream tools both what should be tested and whether the repo was ready for agent work at packet time.
