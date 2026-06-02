# 2026-06-02 - Repo Flightcheck Dirty Tree Preflight

## Context

`repo-flightcheck` already checked README quality, verification commands, CI, agent instructions, package metadata, examples, and secret hygiene. One important pre-agent condition was still missing: whether the target repository already had staged, unstaged, or untracked changes before asking an agent to work.

That matters because pre-existing local changes make it harder to tell which edits belong to the current task. They also increase the chance that a closing summary, review packet, or verification checklist mixes user work with agent work.

## Change

- Added a `working-tree` check backed by `git status --porcelain --untracked-files=all`.
- The check passes for clean Git working trees.
- It warns when the target is not a Git working tree.
- It warns when pre-existing changed paths are present and includes bounded status evidence.
- It degrades to a warning if Git status cannot be read instead of crashing the whole scan.
- Added `node:test` coverage for clean Git repos, dirty Git repos, and non-Git directories.
- Updated README check list, sample output, and limits.

Public commit: `5c76aecde3f9 feat: flag dirty working trees`.

## Verification

Local checks:

```sh
node --test
node scripts/lint.js
node scripts/build.js
node bin/repo-flightcheck.js . --strict --threshold 80
node bin/repo-flightcheck.js . --json > /tmp/repo-flightcheck-report.json
test -s /tmp/repo-flightcheck-report.json
git diff --check
```

Post-commit checks:

```sh
node bin/repo-flightcheck.js . --strict --threshold 80
node bin/repo-flightcheck.js fixtures/sample-repo
```

Results:

- `node --test`: 6 tests passed.
- Lint and build preflight passed.
- Pre-commit self-scan passed strict mode and correctly warned about the current dirty working tree.
- Post-commit self-scan returned `100/100` with `PASS Working tree`.
- Fixture scan returned the README-documented `49/100` example with `PASS Working tree`.
- Public commit page and raw changed files returned `200`.
- GitHub Actions run `26792633038` completed with conclusion `success`.

## Source Linkage

- Repo: <https://github.com/manuelsampedro1/repo-flightcheck>
- Commit: <https://github.com/manuelsampedro1/repo-flightcheck/commit/5c76aecde3f937c0ad12308dbaa74e83a2e9acea>
- CI run: <https://github.com/manuelsampedro1/repo-flightcheck/actions/runs/26792633038>
- Scanner: <https://raw.githubusercontent.com/manuelsampedro1/repo-flightcheck/5c76aec/src/scan.js>
- Tests: <https://raw.githubusercontent.com/manuelsampedro1/repo-flightcheck/5c76aec/test/scan.test.js>

## Takeaway

Agent readiness is not only about whether a repo has tests. A clean Git state is part of the handoff contract: it makes scope, ownership, verification, and closeout evidence easier to trust.
