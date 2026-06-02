# 2026-06-02 - Agent Acceptance Trace Public Launch

## Source

- Public repo: https://github.com/manuelsampedro1/agent-acceptance-trace
- Published HEAD: `26c4a566a493b25c138b34c2a16d224dc646ae54`
- CI run: https://github.com/manuelsampedro1/agent-acceptance-trace/actions/runs/26831051993

## What Changed

Built and published `agent-acceptance-trace`, a dependency-free Python CLI that
turns a Markdown task contract into a criterion-by-criterion trace matrix
against a unified diff and optional evidence files.

The tool reports:

- acceptance criteria parsed from task contracts,
- changed files from the diff,
- matched and missing terms per criterion,
- evidence snippets with source and line references,
- `covered`, `partial`, or `missing` status per criterion,
- Markdown or JSON output,
- non-zero exits with `--min-covered` or `--strict`.

## Why It Matters

The profile already has task contracts, handoff briefs, review packets,
verification plans, proof packets, claim checks, command receipts, and ledgers.
The gap was traceability between the original acceptance criteria and the final
evidence.

`agent-acceptance-trace` makes the closeout review more concrete: do not ask
"does the final answer sound good?" Ask "which acceptance criteria have evidence,
which are only partial, and which are missing?"

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
- public repo and raw README/source/test URLs returned `200`,
- GitHub Actions run `26831051993` completed with `success`.

## Takeaway

Acceptance criteria should survive the whole agent run. A strong closeout should
show traceable evidence per criterion, not only a confident summary and a list of
commands.

