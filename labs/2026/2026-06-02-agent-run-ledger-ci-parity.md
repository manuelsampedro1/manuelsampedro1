# 2026-06-02 - Agent Run Ledger CI Parity

## Context

`agent-run-ledger` is one of the profile's primary proof repos because it records agent runs, imports verification evidence, imports repo readiness reports, and renders static review reports. After the readiness import work, the repo was strong functionally but still had two readiness gaps: CI hid verification behind `npm run check`, and `.env` files were not explicitly ignored.

Before this pass, `repo-flightcheck` scored the repo at `91/100` with warnings for CI verification parity and secret hygiene.

## Change

- Updated GitHub Actions to run the same explicit local commands shown to contributors: `npm run lint`, `npm run build`, and `npm test`.
- Added `.env` and `.env.*` to `.gitignore`.

Public commit: `a6897e54c762 ci: run explicit verification commands`.

## Verification

Local checks:

```sh
node --test
node scripts/lint.js
node scripts/build.js
node /Users/manuelsampedro/Documents/Codex/2026-05-21/repo-flightcheck/bin/repo-flightcheck.js . --strict --threshold 80
git diff --check
```

Results:

- `node --test`: 21 tests passed.
- `node scripts/lint.js`: passed across 14 files.
- `node scripts/build.js`: generated a demo ledger and report successfully.
- `repo-flightcheck`: `100/100` after commit on a clean working tree.
- Public commit page returned `200`.
- Raw workflow file returned `200`.
- GitHub Actions run `26796641661` completed with conclusion `success`, covering the public `npm` script path.

Note: the local Codex desktop runtime exposes `node` but not `npm`, so local verification used direct Node equivalents while GitHub Actions verified the npm scripts.

## Source Linkage

- Repo: <https://github.com/manuelsampedro1/agent-run-ledger>
- Commit: <https://github.com/manuelsampedro1/agent-run-ledger/commit/a6897e54c7627bd2bc331bbf691850068d3680e9>
- CI run: <https://github.com/manuelsampedro1/agent-run-ledger/actions/runs/26796641661>
- Workflow: <https://raw.githubusercontent.com/manuelsampedro1/agent-run-ledger/main/.github/workflows/ci.yml>

## Takeaway

CI parity should be visible, not only implied by a wrapper script. For agent-facing repos, a reviewer should be able to see the exact lint, build, and test commands in both README guidance and GitHub Actions.
