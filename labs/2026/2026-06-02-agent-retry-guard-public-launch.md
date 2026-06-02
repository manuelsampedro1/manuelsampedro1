# 2026-06-02 - Agent Retry Guard Public Launch

## Source

- Public repo: https://github.com/manuelsampedro1/agent-retry-guard
- Published HEAD: `740c8924aa1ef92d5cd28abc3d0ec435743e8892`
- CI run: https://github.com/manuelsampedro1/agent-retry-guard/actions/runs/26839336924

## What Changed

Built and published `agent-retry-guard`, a dependency-free Python CLI for
detecting repeated failure loops in coding-agent transcripts.

The tool reads plain text transcripts or JSONL command events and checks for:

- the same failed command repeated beyond a configured retry threshold,
- repeated command plus error-signature pairs,
- adjacent blind retries with no investigation signal in between,
- failure-heavy transcripts with no strategy-shift marker.

It emits Markdown for reviewers, JSON for automation, score gates via
`--min-score`, severity gates via `--fail-on`, and optional reports via
`--write-report`.

## Why It Matters

One of the most expensive agent failure modes is not a bad first attempt. It is
the fifth attempt that repeats the same command, sees the same error, and still
does not change hypothesis.

`agent-retry-guard` turns that pattern into a reviewable gate. It helps a human
or automation stop a run and require source inspection, docs, environment
checks, or a new plan before more context is spent.

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
- installed CLI smoke run against `examples/healthy-transcript.txt`,
- `agent-instruction-audit AGENTS.md --min-score 80` at `100/100`,
- `repo-flightcheck . --check-remote --strict --threshold 80` at `100/100`,
- public raw README/source/test/example URLs returned `200`,
- GitHub Actions run `26839336924` completed with `success`.

## Takeaway

After the same failure repeats, require investigation before another retry.
Agent speed is useful only when the loop changes with new evidence.
