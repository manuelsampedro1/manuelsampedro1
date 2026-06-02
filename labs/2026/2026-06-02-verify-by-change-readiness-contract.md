# 2026-06-02 - Verify by Change Readiness Contract

## Context

`verify-by-change` is already one of the profile's selected proof repos because it maps changed files to honest verification commands. The weak signal was not the CLI behavior; it was repo readiness. A public tool meant for agent handoffs should be easy to clone, inspect, run, and audit without guessing the local contract.

Before this pass, `repo-flightcheck` scored the repo at `59/100` with missing license, missing `AGENTS.md`, no standard build or lint command, no examples, and no `.env` ignore rule.

## Change

- Added `AGENTS.md` with purpose, constraints, and verification commands.
- Added MIT license and `pyproject.toml` metadata with a console script entrypoint.
- Added `Makefile` targets for `make test`, `make build`, and `make lint`.
- Updated CI to run those same local targets.
- Added `examples/verification-envelope.json` as a stable automation handoff example.
- Updated README and `DECISIONS.md` with the repo readiness contract.
- Extended `.gitignore` for `.env`, build artifacts, and package metadata.

Public commit: `dd26fffd7fb3 chore: add repo readiness contract`.

## Verification

Local checks:

```sh
make test
make build
make lint
python3 verify_by_change.py verify_by_change.py README.md
python3 verify_by_change.py verify_by_change.py README.md --json-envelope
python3 verify_by_change.py --repo . --base HEAD --include-working-tree
node /Users/manuelsampedro/Documents/Codex/2026-05-21/repo-flightcheck/bin/repo-flightcheck.js . --strict --threshold 80
git diff --check
```

Results:

- `make test`: 15 tests passed.
- `make build`: passed.
- `make lint`: passed.
- `repo-flightcheck`: `100/100` after commit on a clean working tree.
- Public commit page returned `200`.
- Raw `AGENTS.md` returned `200`.
- GitHub Actions run `26796285609` completed with conclusion `success`.

## Source Linkage

- Repo: <https://github.com/manuelsampedro1/verify-by-change>
- Commit: <https://github.com/manuelsampedro1/verify-by-change/commit/dd26fffd7fb3c7b296aa8a620e954e0fc52a4e93>
- CI run: <https://github.com/manuelsampedro1/verify-by-change/actions/runs/26796285609>
- Agent contract: <https://raw.githubusercontent.com/manuelsampedro1/verify-by-change/main/AGENTS.md>
- Example envelope: <https://raw.githubusercontent.com/manuelsampedro1/verify-by-change/main/examples/verification-envelope.json>

## Takeaway

Small proof repos still need a clear operating contract. A single-file CLI looks more professional when reviewers can see the license, local commands, CI parity, package metadata, examples, and agent instructions without inferring intent.
