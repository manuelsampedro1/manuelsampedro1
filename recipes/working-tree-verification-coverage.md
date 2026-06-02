# Working Tree Verification Coverage

Use this when a coding-agent closeout tool derives verification steps from changed files.

## Goal

Do not let the verification checklist miss files just because they are staged, unstaged, or newly created. The checklist should cover the review surface, not only `git diff`.

## Source Event

This recipe came from `verify-by-change` commit `638f452a64a5`, which changed `--repo .` detection from a narrow diff-only path to working-tree status coverage and added tests plus CI.

Relevant files:

- `verify_by_change.py`
- `tests/test_verify_by_change.py`
- `.github/workflows/ci.yml`

## Workflow

1. Decide what the operator means by "changed files".
2. For default working-tree mode, read `git status --porcelain --untracked-files=all`.
3. Parse status rows into paths, including rename targets after `old -> new`.
4. Keep an explicit staged-only mode for reviewers who want `git diff --cached --name-only`.
5. Classify config files such as `.yml`, `.yaml`, `.json`, and `.toml`; CI files are often part of the verification plan.
6. Add a CLI `--output` option when the checklist needs to become a handoff artifact.

## Checklist

- Does default mode include staged files?
- Does default mode include unstaged files?
- Does default mode include untracked files?
- Does staged-only mode stay narrower than default mode?
- Does the tool classify CI/config files instead of burying them as uncategorized?
- Does the README show both default and staged-only usage?

## Verification

Use temp Git repos in tests so the behavior is proven instead of inferred:

```sh
python3 -m unittest discover -s tests
python3 -m py_compile verify_by_change.py
python3 verify_by_change.py --repo . --json | python3 -m json.tool
```

The `verify-by-change` run that produced this recipe also confirmed public CI success for the new tests.

## Failure Modes

- Using `git diff --name-only` as the default and missing untracked files.
- Checking only explicit path arguments and never exercising Git working-tree state.
- Adding a CI workflow without a local test command that proves the same behavior.
- Treating YAML workflow changes as generic unknown files instead of config changes that affect verification.

## Source Linkage

- Public repo: <https://github.com/manuelsampedro1/verify-by-change>
- Commit: <https://github.com/manuelsampedro1/verify-by-change/commit/638f452a64a533e10e68c29d0a900832ec87d2ee>
- CI run: <https://github.com/manuelsampedro1/verify-by-change/actions/runs/26791647595>
