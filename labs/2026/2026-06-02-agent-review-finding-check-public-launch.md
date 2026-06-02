# 2026-06-02 - Agent Review Finding Check Public Launch

## Source

- Public repo: https://github.com/manuelsampedro1/agent-review-finding-check
- Published HEAD: `fa204e7f38271827fe6df18f2c5999e1e812eb47`
- CI run: https://github.com/manuelsampedro1/agent-review-finding-check/actions/runs/26843166501

## What Changed

Built and published `agent-review-finding-check`, a dependency-free Python CLI
for auditing coding-agent review findings before they are sent to a human
reviewer, PR thread, or proof packet.

The tool checks for:

- severity labels such as `P0`, `P1`, `P2`, `P3`, `high`, `medium`, or `low`,
- concrete `file:line` references,
- whether referenced files exist in the supplied diff,
- impact or risk explanation,
- actionable fix language,
- evidence language on high-priority findings,
- vague or hedged wording,
- empty reviews that omit residual risks or testing gaps.

It accepts Markdown or JSON findings, emits Markdown or JSON reports, writes
optional report files, and gates runs with `--min-score` and `--fail-on`.

## Why It Matters

Review quality is not only about having a diff packet. The final findings must
be specific enough that a reviewer can evaluate severity, reproduce the concern,
and act on the fix without reverse-engineering the agent's intent.

`agent-review-finding-check` fills that gap between review context and PR
surface. It makes review comments more inspectable before they become public
feedback.

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
- installed CLI JSON smoke run against `examples/review-findings.md` and `examples/sample.diff`,
- `agent-instruction-audit AGENTS.md --min-score 80` at `100/100`,
- `repo-flightcheck . --check-remote --strict --threshold 80` at `100/100`,
- public raw README/source/test/example URLs returned `200`,
- GitHub Actions run `26843166501` completed with `success`.

## Takeaway

Do not accept a review finding just because it sounds serious. It needs a
severity, a location, impact, evidence, and a concrete fix path.
