# 2026-06-02 - Repo Flightcheck Remote Failure Classification

## Context

While preparing `agent-task-contract` for publication, the repo reached `99/100` in `repo-flightcheck`, but the first push failed because `manuelsampedro1/agent-task-contract` does not exist yet on GitHub.

Before this change, `repo-flightcheck --check-remote` collapsed that failure into the generic message `Origin remote is configured but could not be reached.` That was technically true, but not sharp enough for a publish queue or profile-proof workflow.

## Change

- Classified `Repository not found` as `Origin remote repository was not found or is not accessible.`
- Classified common auth failures such as `Permission denied`, `authentication failed`, and `could not read Username`.
- Kept sanitized remote URL and Git stderr evidence in the report.
- Added tests for missing-repository and authentication failure classification.
- Updated README scope and limits to document missing-repository and permission checks.

Public commit: `2c0a42bdf016 feat: classify remote publish failures`.

## Verification

Local checks:

```sh
node --test
node scripts/lint.js
node scripts/build.js
git diff --check
node bin/repo-flightcheck.js . --check-remote --strict --threshold 80
node bin/repo-flightcheck.js /Users/manuelsampedro/Documents/Codex/2026-05-21/agent-task-contract --check-remote --strict --threshold 80
```

Results:

- `node --test`: 26 tests passed.
- `node scripts/lint.js`: passed.
- `node scripts/build.js`: passed.
- `git diff --check`: passed.
- Self-scan after push: `98/100`, with published `HEAD` passing on `origin/main`; only local warning was missing `npm` in this Codex environment.
- Real blocked repo scan: `agent-task-contract` scored `99/100` and now reports `Origin remote repository was not found or is not accessible.`
- Commit URL returned HTTP `200`.
- Raw `src/scan.js` URL returned HTTP `200`.
- GitHub Actions run `26806662928` completed with conclusion `success`.

## Source Linkage

- Repo: <https://github.com/manuelsampedro1/repo-flightcheck>
- Commit: <https://github.com/manuelsampedro1/repo-flightcheck/commit/2c0a42bdf016757235e349bc746860cdc6a30f3a>
- CI run: <https://github.com/manuelsampedro1/repo-flightcheck/actions/runs/26806662928>
- Scanner: <https://raw.githubusercontent.com/manuelsampedro1/repo-flightcheck/main/src/scan.js>
- Tests: <https://raw.githubusercontent.com/manuelsampedro1/repo-flightcheck/main/test/scan.test.js>
- README: <https://raw.githubusercontent.com/manuelsampedro1/repo-flightcheck/main/README.md>

## Takeaway

Public-proof tooling should distinguish "remote URL configured" from "remote repo exists and this identity can access it." The failure mode changes the next action: create the repo, fix permissions, or push the missing branch.
