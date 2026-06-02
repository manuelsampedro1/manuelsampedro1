# AGENTS.md

## Purpose

Maintain this GitHub profile repository as a public AI builder workbench backed by real repos, lab notes, recipes, and automation evidence.

## Constraints

- Do not create empty commits, timestamp-only churn, fake contributions, secrets, or unsupported claims.
- Do not publish radar claims about current tools or ecosystem changes without verifying facts and citing sources.
- Prefer repo-backed proof over profile-copy changes.
- Keep public indexes current only when useful artifacts changed.

## Verification

Run these checks before publishing profile maintenance changes:

```sh
make test
make lint
make build
```

## Commit Expectations

- Commit only substantive artifacts or tooling/docs changes that improve the public workbench.
- Use `scripts/commit_daily_update.sh` with the exact intended changed paths for maintenance commits.
- If Git identity or `origin` is missing, report the setup blocker instead of inventing credentials.
