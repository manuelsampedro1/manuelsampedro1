# 2026-06-02 - Briefboard Readiness Contract

## Context

`briefboard-local` is the profile's local-first product proof: a static app that turns messy kickoff notes into a structured brief and Codex-ready prompt. The app behavior was useful, but the repo itself still looked less ready than the agent tooling repos.

Before this pass, `repo-flightcheck` scored the repo at `69/100` with missing license, missing `.gitignore`, missing `AGENTS.md`, no build or lint command, no examples folder, and incomplete package metadata.

## Change

- Added `AGENTS.md` with product purpose, local-first constraints, and verification commands.
- Added MIT license, `.gitignore`, `Makefile`, and package metadata.
- Added `npm run build` and `npm run lint` scripts backed by dependency-free Node preflights.
- Updated CI to run `npm test`, `npm run build`, and `npm run lint`.
- Added `examples/briefboard-draft.json` as an importable ready-for-handoff draft.
- Updated README and `DECISIONS.md` with setup, examples, automated checks, and the repo readiness contract.

Public commit: `5ad93eb23b0e chore: add repo readiness contract`.

## Verification

Local checks:

```sh
node --test
node scripts/build.js
node scripts/lint.js
node /Users/manuelsampedro/Documents/Codex/2026-05-21/repo-flightcheck/bin/repo-flightcheck.js . --strict --threshold 80
git diff --check
```

Results:

- `node --test`: 9 tests passed.
- `node scripts/build.js`: passed.
- `node scripts/lint.js`: passed.
- `repo-flightcheck`: `100/100` after commit on a clean working tree.
- Public commit page returned `200`.
- Raw `AGENTS.md` returned `200`.
- Raw example JSON returned `200`.
- GitHub Actions run `26796527483` completed with conclusion `success`, covering the public `npm` script path.

Note: the local Codex desktop runtime exposes `node` but not `npm`, so local verification used the direct Node equivalents while GitHub Actions verified the npm scripts.

## Source Linkage

- Repo: <https://github.com/manuelsampedro1/briefboard-local>
- Commit: <https://github.com/manuelsampedro1/briefboard-local/commit/5ad93eb23b0e5c4b707655f79347b3be16519219>
- CI run: <https://github.com/manuelsampedro1/briefboard-local/actions/runs/26796527483>
- Agent contract: <https://raw.githubusercontent.com/manuelsampedro1/briefboard-local/main/AGENTS.md>
- Example draft: <https://raw.githubusercontent.com/manuelsampedro1/briefboard-local/main/examples/briefboard-draft.json>

## Takeaway

Product taste is stronger when the repo around the product is also ready for review. A static local-first app can stay dependency-free while still exposing license, examples, CI parity, agent instructions, and exact verification commands.
