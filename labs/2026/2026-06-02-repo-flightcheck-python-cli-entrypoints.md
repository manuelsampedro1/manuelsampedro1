# 2026-06-02 - Repo Flightcheck Python CLI Entrypoints

## Context

`repo-flightcheck` already checked Node CLI `package.json` `bin` entrypoints, but many local agent tools in this workbench are Python CLIs with `pyproject.toml` `[project.scripts]`.

That left an avoidable packaging gap: a repo could look ready while its public command pointed to a missing module or an undefined function.

## Change

- Added a `Python CLI entrypoint` check to `repo-flightcheck`.
- Parsed simple `pyproject.toml` `[project.scripts]` entries shaped as `module:function`.
- Validated both root package layout and `src/` package layout.
- Checked that the module file exists and that the referenced function is defined.
- Added tests for valid Python CLIs, missing modules, missing functions, invalid entrypoint shape, and `src/` layout.
- Updated README checks, example output, and limits.

Public commit: `b678a19bbf5a feat: validate python cli entrypoints`.

## Verification

Local checks:

```sh
node --test
node scripts/lint.js
node scripts/build.js
git diff --check
node bin/repo-flightcheck.js . --strict --threshold 80
```

Results:

- `node --test`: 19 tests passed.
- `node scripts/lint.js`: passed.
- `node scripts/build.js`: passed.
- `git diff --check`: passed.
- Smoke scans against local Python CLI repos `agent-task-contract`, `diff-to-eval`, and `profile-proof-audit` validated one Python CLI entrypoint each.
- `repo-flightcheck`: `100/100` after commit.
- GitHub Actions run `26801847938` completed with conclusion `success` for commit `b678a19bbf5aaf671a6c8bcd69e61c4e9781fe9c`.

## Source Linkage

- Repo: <https://github.com/manuelsampedro1/repo-flightcheck>
- Commit: <https://github.com/manuelsampedro1/repo-flightcheck/commit/b678a19bbf5aaf671a6c8bcd69e61c4e9781fe9c>
- CI run: <https://github.com/manuelsampedro1/repo-flightcheck/actions/runs/26801847938>
- Scanner: <https://raw.githubusercontent.com/manuelsampedro1/repo-flightcheck/main/src/scan.js>
- Tests: <https://raw.githubusercontent.com/manuelsampedro1/repo-flightcheck/main/test/scan.test.js>

## Takeaway

Agent-ready Python repos need their CLI surface checked, not just their tests. A broken console script is an onboarding failure because the command a reviewer expects to run may not import at all.
