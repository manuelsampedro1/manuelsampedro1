# 2026-06-02 - Repo Flightcheck Tool Availability

## Context

Agent-ready repos often document a clean command contract: `npm test`, `npm run build`, `make test`, or `python -m unittest`. That is not enough when the local agent environment lacks the tool needed to run the command.

This came up while validating public proof repos from Codex desktop: Node was available through the app runtime, but `npm` was not present on `PATH`. A readiness scanner should surface that gap instead of letting an agent discover it at closeout time.

## Change

- Added a `Tool availability` check to `repo-flightcheck`.
- Derived required executables from detected verification, build, and lint commands.
- Checked the current `PATH` for those tools.
- Reported missing tools as warnings with exact command evidence.
- Kept the check injectable in tests so fixtures do not depend on the machine running the suite.
- Updated README coverage, sample output, and limits.

Public commit: `44f62751ae08 feat: flag missing local command tools`.

## Verification

Local checks:

```sh
node --test
node scripts/build.js
node scripts/lint.js
git diff --check
node bin/repo-flightcheck.js . --strict --threshold 80
```

Results:

- `node --test`: 21 tests passed.
- `node scripts/build.js`: passed for 6 JavaScript files.
- `node scripts/lint.js`: passed.
- `git diff --check`: passed.
- `repo-flightcheck --strict --threshold 80`: `98/100` after commit, with the intended local warning that `npm` is missing in this Codex desktop `PATH`.
- GitHub Actions run `26803070963` completed with conclusion `success`.

## Source Linkage

- Repo: <https://github.com/manuelsampedro1/repo-flightcheck>
- Commit: <https://github.com/manuelsampedro1/repo-flightcheck/commit/44f62751ae089cdbb07dbd69520c8bf4879fbbd6>
- CI run: <https://github.com/manuelsampedro1/repo-flightcheck/actions/runs/26803070963>
- Scanner: <https://raw.githubusercontent.com/manuelsampedro1/repo-flightcheck/main/src/scan.js>
- Tests: <https://raw.githubusercontent.com/manuelsampedro1/repo-flightcheck/main/test/scan.test.js>

## Takeaway

Repo readiness should verify both the command contract and the local toolchain needed to execute it. A missing `npm`, `make`, `python`, `cargo`, or `swift` is not a failed implementation, but it is critical context before handing the repo to an agent.
