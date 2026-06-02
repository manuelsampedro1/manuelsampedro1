# 2026-06-02 - Agent Request Brief Public Launch

## Source

- Public repo: https://github.com/manuelsampedro1/agent-request-brief
- Published HEAD: `f595f8c41eaf0592038e139051174dec62105ffd`
- CI run: https://github.com/manuelsampedro1/agent-request-brief/actions/runs/26837867257

## What Changed

Built and published `agent-request-brief`, a dependency-free Python CLI for
auditing raw coding-agent requests before they become broad edits.

The tool checks whether the request includes:

- objective,
- scope,
- acceptance criteria,
- constraints,
- current context,
- verification commands or checks,
- risks and external outcomes,
- concrete next actions.

It emits Markdown for reviewers, JSON for automation, optional next-agent briefs
via `--write-brief`, score gates via `--min-score`, and status gates via
`--fail-on`.

## Why It Matters

Coding-agent quality often depends on the first sentence a human writes. A raw
request can be emotionally clear but operationally weak: "make it more pro",
"fix it", "finish this", or "they need to give me the prize" does not define
scope, acceptance criteria, verification, or external uncertainty.

`agent-request-brief` gives the workflow a pre-contract gate. It does not
pretend to know hidden intent. It makes missing state visible, asks the smallest
clarifying questions, and keeps external outcomes out of completion claims.

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
- installed CLI smoke run against `examples/complete-request.md`,
- `agent-instruction-audit AGENTS.md --min-score 80` at `100/100`,
- `repo-flightcheck . --check-remote --strict --threshold 80` at `100/100`,
- public raw README/source/test/example URLs returned `200`,
- GitHub Actions run `26837867257` completed with `success`.

## Takeaway

Do not hand vague intent directly to a coding agent. First separate what the
agent can verify from what remains external, then preserve objective, scope,
acceptance criteria, constraints, context, checks, risks, and next actions.
