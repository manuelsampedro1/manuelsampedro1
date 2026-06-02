# 2026-06-02 - Verify by Change Working Tree CI

## Context

`verify-by-change` is part of the profile's selected work because it turns changed files into honest verification steps. Its first public version worked for explicit paths and base refs, but `--repo .` without `--base` only used `git diff --name-only`, which can miss staged or untracked files in a real Codex closeout.

## Change

- `--repo` without `--base` now reads `git status --porcelain --untracked-files=all`.
- Added `--staged` for index-only verification.
- Added `--output` so Markdown or JSON checklists can be saved as handoff artifacts.
- Added a `config` bucket for JSON, TOML, YAML, and GitHub Actions files.
- Added `tests/test_verify_by_change.py` with working-tree, staged-only, renderer, and CLI coverage.
- Added GitHub Actions CI for tests and Python compilation.

Public commit: `638f452a64a5 feat: detect full working tree changes`.

## Verification

Local checks:

```sh
python3 -m py_compile verify_by_change.py
python3 -m unittest discover -s tests
python3 verify_by_change.py verify_by_change.py README.md --json --output /tmp/verify-by-change-checks.json
test -s /tmp/verify-by-change-checks.json
python3 verify_by_change.py --repo . --json | python3 -m json.tool
git diff --check
```

Public checks:

- Raw tests returned `200`.
- Raw CI workflow returned `200`.
- GitHub Actions run `26791647595` for commit `638f452a64a533e10e68c29d0a900832ec87d2ee` completed with conclusion `success`.

## Source Linkage

- Repo: <https://github.com/manuelsampedro1/verify-by-change>
- Commit: <https://github.com/manuelsampedro1/verify-by-change/commit/638f452a64a533e10e68c29d0a900832ec87d2ee>
- CI run: <https://github.com/manuelsampedro1/verify-by-change/actions/runs/26791647595>
- Tests: <https://raw.githubusercontent.com/manuelsampedro1/verify-by-change/638f452/tests/test_verify_by_change.py>

## Takeaway

Verification helpers need to inspect the same file set a reviewer will see. For Codex closeouts, that means staged, unstaged, and untracked files unless the operator explicitly asks for a narrower staged-only view.
