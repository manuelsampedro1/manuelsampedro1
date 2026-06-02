# 2026-06-02 - Verify by Change Node CLI Context

## Context

`verify-by-change` previously treated `.js` and `.ts` files as web changes unless a more specific path rule matched first.

That was wrong for small Node CLI repos such as `agent-run-ledger`: a changed `src/cli.js` should suggest runtime, test, build, and safe CLI smoke checks, not browser/UI review.

## Change

- Added Node CLI repo context detection from `package.json`.
- Treated packages with `bin` plus test/build/lint/check scripts as CLI/runtime repos.
- Used review packet `Repo: ...` metadata to recover package context when generating a verification envelope from `--review-packet`.
- Preserved web classification for plain explicit paths such as `app.js` when no CLI context exists.
- Added unit and CLI tests for direct classification, repo scans, and review-packet envelopes.
- Updated the public README to describe Node CLI guidance separately from web JS/TS guidance.

Public commit: `bb4cf7a85ba1 feat: detect node cli verification context`.

## Verification

Local checks:

```sh
python3 -m py_compile verify_by_change.py
python3 -m unittest discover -s tests
make test
make build
make lint
git diff --check
node /Users/manuelsampedro/Documents/Codex/2026-05-21/repo-flightcheck/bin/repo-flightcheck.js /Users/manuelsampedro/Documents/Codex/2026-05-24/flagships/verify-by-change --strict --threshold 80
```

Results:

- `python3 -m unittest discover -s tests`: 31 tests passed.
- `make test`, `make build`, and `make lint`: passed.
- Manual temporary Node CLI smoke returned the `node_cli` category for `src/cli.js`.
- `repo-flightcheck`: `100/100`.
- GitHub Actions run `26800472479` completed with conclusion `success`.

## Source Linkage

- Repo: <https://github.com/manuelsampedro1/verify-by-change>
- Commit: <https://github.com/manuelsampedro1/verify-by-change/commit/bb4cf7a85ba16eccbb7604e5c2df3b9dd2bae5d5>
- CI run: <https://github.com/manuelsampedro1/verify-by-change/actions/runs/26800472479>
- CLI: <https://raw.githubusercontent.com/manuelsampedro1/verify-by-change/main/verify_by_change.py>
- Tests: <https://raw.githubusercontent.com/manuelsampedro1/verify-by-change/main/tests/test_verify_by_change.py>

## Takeaway

Verification categories should use repository context when extension-only rules are too broad. JavaScript can mean browser UI, Node scripts, or a CLI entrypoint; the closeout checklist should not guess from the suffix alone.
