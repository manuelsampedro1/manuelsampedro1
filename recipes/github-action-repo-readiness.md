# GitHub Action Repo Readiness

Use this when a GitHub Action repo needs to be handed to Codex, reviewed by another engineer, or promoted as public proof.

## Goal

Make an action repo inspectable without requiring a hosted service, live token, or production workflow run.

## Source Event

This recipe came from adding GitHub Action stack detection to `repo-flightcheck` after auditing a local clone of `deploy-gate`.

The public change taught `repo-flightcheck` to classify dependency-light action repos with `action.yml` or `action.yaml` as `github-action` when no language-specific stack is present.

## Workflow

1. Keep `action.yml` or `action.yaml` as the public contract.
2. Add `AGENTS.md` with purpose, constraints, and exact verification commands.
3. Add `Makefile` targets for `make test`, `make build`, and `make lint`.
4. Make `make test` validate action inputs, outputs, runtime, and safety-critical defaults.
5. Make `make build` validate docs, install examples, required assets, and example workflows.
6. Make `make lint` syntax-check local verifier scripts.
7. Add CI that runs the same Make targets.
8. Add an `examples/` workflow that users can adapt without copying from prose.
9. Run `repo-flightcheck` and require a clean working tree before claiming readiness.

## Checklist

- Does `action.yml` expose the expected inputs and outputs?
- Does the action fail closed where safety requires it?
- Are install docs and example workflows consistent?
- Does CI run the same verification commands documented locally?
- Are `.env` files ignored?
- Is there an agent contract warning against secrets, live tokens, and silent action-contract changes?
- Is any live API behavior clearly separated from offline repo checks?

## Verification

For a dependency-light composite action:

```sh
make test
make build
make lint
node /path/to/repo-flightcheck/bin/repo-flightcheck.js . --strict --threshold 80
git diff --check
```

## Failure Modes

- Using a production workflow as the only test.
- Adding fake tests that only check file existence and miss action inputs or safety defaults.
- Documenting `make` commands without Make targets.
- Letting CI call a wrapper while README tells reviewers to run different commands.
- Committing sample API keys, tenant IDs, or approval tokens.

## Source Linkage

- Public repo: <https://github.com/manuelsampedro1/repo-flightcheck>
- Commit: <https://github.com/manuelsampedro1/repo-flightcheck/commit/c697fa3e8c87ca9322f8e3b1040795f3bd81c777>
- CI run: <https://github.com/manuelsampedro1/repo-flightcheck/actions/runs/26796926606>
- Lab note: <../labs/2026/2026-06-02-repo-flightcheck-github-action-detection.md>
