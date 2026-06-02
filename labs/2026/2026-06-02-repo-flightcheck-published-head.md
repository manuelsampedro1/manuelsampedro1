# 2026-06-02 - Repo Flightcheck Published HEAD Readiness

## Context

`repo-flightcheck` already checks whether an `origin` remote exists and, with `--check-remote`, whether Git can reach it. That caught local repos whose GitHub remotes were configured but missing.

The next profile failure mode is subtler: after a local commit, `origin` can be reachable while the new `HEAD` is not pushed yet. A profile can then claim a public commit, CI run, or raw source link before the exact code is available on GitHub.

## Change

- Extended `--check-remote` so it compares local `HEAD` with the current branch on `origin`.
- Warns when `origin/<branch>` cannot be read, local `HEAD` is detached, or the local SHA does not match the remote branch SHA.
- Keeps the deeper check opt-in because it can require network access or GitHub authentication.
- Sanitizes remote evidence before printing it.
- Added a local bare-remote test that proves the stale-HEAD warning after a commit that has not been pushed.
- Updated CLI help and README language so public proof means both reachable remote and published commit.

Public commit: `6bf313ec67ce feat: check published head readiness`.

## Verification

Local checks:

```sh
node --test
node scripts/build.js
node scripts/lint.js
git diff --check
node bin/repo-flightcheck.js . --check-remote --strict --threshold 80
```

Results:

- `node --test`: 25 tests passed.
- `node scripts/build.js`: passed.
- `node scripts/lint.js`: passed.
- `git diff --check`: passed.
- Before push, self-scan warned: `Origin remote is reachable, but local HEAD is not published on origin/main.`
- After push, self-scan returned `98/100` and `PASS Git remote Origin remote is reachable and local HEAD is published on origin/main.`
- Commit URL returned HTTP `200`.
- GitHub Actions run `26805326508` completed with conclusion `success`.

## Source Linkage

- Repo: <https://github.com/manuelsampedro1/repo-flightcheck>
- Commit: <https://github.com/manuelsampedro1/repo-flightcheck/commit/6bf313ec67ce5a0fffd1658fcd182ab1e37d4fe7>
- CI run: <https://github.com/manuelsampedro1/repo-flightcheck/actions/runs/26805326508>
- Scanner: <https://raw.githubusercontent.com/manuelsampedro1/repo-flightcheck/main/src/scan.js>
- Tests: <https://raw.githubusercontent.com/manuelsampedro1/repo-flightcheck/main/test/scan.test.js>
- README: <https://raw.githubusercontent.com/manuelsampedro1/repo-flightcheck/main/README.md>

## Takeaway

Public proof should be tied to the exact commit, not only to a repo name. A reachable remote proves the repository exists; a matching remote branch proves the local change is actually published.
