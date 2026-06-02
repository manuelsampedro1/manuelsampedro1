# 2026-06-02 - Agent Test Impact Public Launch

## Source

- Public repo: https://github.com/manuelsampedro1/agent-test-impact
- Published HEAD: `fe7e9039cc86da178e78f61b98d68a4074bcdcc9`
- CI run: https://github.com/manuelsampedro1/agent-test-impact/actions/runs/26832654835

## What Changed

Built and published `agent-test-impact`, a dependency-free Python CLI that maps
coding-agent diffs to likely test coverage gaps.

The tool reports:

- changed source files across common Python, JavaScript, TypeScript, Go, Rust,
  Ruby, Java, Kotlin, Swift, and C# conventions,
- changed test files using common `tests/`, `__tests__/`, `test_*`, `*_test`,
  `*.test.*`, `*.spec.*`, and `*Tests` patterns,
- direct, partial, or missing test evidence for each changed source file,
- likely test paths when related tests did not change,
- suggested targeted checks by ecosystem,
- Markdown or JSON output for CI gates, proof packets, or run ledgers.

## Why It Matters

A green test command is not the same as test evidence for the behavior that
changed. Coding agents can run broad checks, then close confidently while the
diff changed source files without any nearby test signal.

`agent-test-impact` makes that gap visible. It does not claim runtime coverage or
assertion quality. It gives reviewers a deterministic pre-closeout question:
which source files changed, and did the diff include a related test change?

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
- `agent-instruction-audit AGENTS.md --min-score 80` at `100/100`,
- `repo-flightcheck . --check-remote --strict --threshold 80` at `100/100`,
- public repo and raw README/source/test/example URLs returned `200`,
- GitHub Actions run `26832654835` completed with `success`.

## Takeaway

Verification needs a path-level test-impact check. A reviewer should not have to
infer from a generic closeout whether a source change has direct, partial, or
missing test evidence.
