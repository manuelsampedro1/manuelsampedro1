# 2026-06-02 - Agent PR Brief Public Launch

## Source

- Public repo: https://github.com/manuelsampedro1/agent-pr-brief
- Published HEAD: `12a2a150cfbef415d874b24709469a9616b9ec26`
- CI run: https://github.com/manuelsampedro1/agent-pr-brief/actions/runs/26841522014

## What Changed

Built and published `agent-pr-brief`, a dependency-free Python CLI for auditing
pull-request descriptions against the unified diff they are supposed to explain.

The tool checks for:

- required sections for summary, changes, verification, risks, and follow-up,
- changed files that are not mentioned or summarized,
- risky paths such as CI, scripts, deploy, auth, security, billing, dependency,
  or config changes without reviewer callouts,
- verification claims without nearby command, output, CI, report, or receipt
  evidence,
- vague language such as "misc", "various", "should work", or "probably",
- oversized diffs without a scope or review-slice note.

It emits Markdown for reviewers, JSON for automation, score gates via
`--min-score`, severity gates via `--fail-on`, and optional reports via
`--write-report`.

## Why It Matters

The PR description is often the first review artifact a human sees. If an agent
posts a polished but incomplete description, the reviewer starts from the wrong
frame: risky paths can be hidden, verification can be implied, and broad diffs
can look smaller than they are.

`agent-pr-brief` turns the PR description into a checkable review contract. It
complements review packets, change-risk gates, proof packets, and closeout
claim checks by focusing on the public PR surface.

## Verification

Ran locally:

```sh
make test
make lint
make build
make smoke
git diff --check
```

Additional checks:

- editable install in a temporary virtualenv after upgrading `pip`, `setuptools`, and `wheel`,
- installed CLI smoke run against `examples/pr-description.md` and `examples/sample.diff`,
- `agent-instruction-audit AGENTS.md --min-score 80` at `100/100`,
- `repo-flightcheck . --check-remote --strict --threshold 80` at `100/100`,
- public raw README/source/test/example URLs returned `200`,
- GitHub Actions run `26841522014` completed with `success`.

## Takeaway

Do not let the PR description become a softer version of the diff. If a reviewer
will see it first, it needs the same evidence discipline as the closeout.
