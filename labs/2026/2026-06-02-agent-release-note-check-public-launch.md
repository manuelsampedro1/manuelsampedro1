# 2026-06-02 - Agent Release Note Check Public Launch

## Source

- Repo: https://github.com/manuelsampedro1/agent-release-note-check
- Commit: `2cb4056c2480aeb1d79bd4bad3b37e798d8f19f8`
- CI: https://github.com/manuelsampedro1/agent-release-note-check/actions/runs/26844750386

## What Shipped

`agent-release-note-check` is a dependency-free Python 3.9+ CLI that compares a
release note or changelog draft against a unified diff. It outputs Markdown or
JSON and supports score/severity gates for CI or proof-packet use.

The tool flags:

- empty or thin release notes,
- missing version/date-like release headings,
- changed files not covered directly or by useful category language,
- breaking-change signals without migration or compatibility notes,
- security-sensitive paths without security/auth/permission wording,
- dependency manifest or lockfile changes without dependency notes,
- CI, workflow, script, or automation changes without operational notes,
- test changes without verification or test wording,
- code changes described as docs-only,
- unsupported claims such as "fully tested", "no breaking changes", or "no
  security impact" when the diff contradicts them or the note lacks evidence.

## Why It Matters

Maintainers publish releases, not just pull requests. A generated changelog can
sound professional while omitting exactly the information users need before
upgrading. This project makes that failure mode executable and reviewable.

It complements:

- `agent-ci-failure-packet` for failed workflow triage,
- `agent-rollback-plan` for operational reversibility,
- `agent-proof-packet` for release evidence,
- `agent-run-ledger` for durable run records.

## Verification

- `make test` passed with 10 tests.
- `make lint` passed.
- `make build` passed.
- `make smoke` passed with `100/100`.
- JSON smoke returned `pass 100 4`.
- Weak release-note smoke failed as expected on high-severity findings.
- `git diff --check` passed after Git initialization.
- Editable install succeeded after upgrading `pip`, `setuptools`, and `wheel`.
- Installed CLI JSON smoke returned `pass 100 4`.
- `agent-instruction-audit AGENTS.md --min-score 80` returned `100/100`.
- Raw GitHub URLs for README, CLI, tests, and examples returned `200`.
- GitHub Actions run `26844750386` completed with `success`.
- `repo-flightcheck --check-remote --strict --threshold 80` returned `100/100`.

## Next Use

Use this before publishing generated release notes, turning a PR summary into a
changelog entry, or importing release evidence into a proof packet.

