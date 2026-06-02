# 2026-06-02 - Verify by Change Python CLI Context

## Context

`repo-flightcheck` now detects Python CLI entrypoint readiness. `verify-by-change` still treated many Python entrypoint edits as generic Python or config changes, which meant the suggested verification could miss the installed console-script surface that users actually run.

## Change

- Added Python CLI repo context detection from `pyproject.toml` `[project.scripts]`.
- Added a `python_cli` verification category before generic Python or config classification.
- Classified `pyproject.toml`, `src/`, `bin/`, `cli/`, `cli.py`, and `__main__.py` changes as Python CLI work when the repo context supports it.
- Recommended editable install, console-script smoke checks, and targeted tests for Python CLI changes.
- Updated the README and unit tests so the behavior is visible and guarded.

## Verification

- `python3 -m unittest discover -s tests`: 34 tests passed.
- `python3 -m py_compile verify_by_change.py`: passed.
- `make test`: 34 tests passed.
- `make build && make lint && git diff --check`: passed.
- Temporary Python CLI repo smoke: changed `src/demo/cli.py` with `[project.scripts] demo = "demo.cli:main"` and confirmed JSON output contained `python_cli` plus editable install guidance.
- `repo-flightcheck` against the committed repo: 100/100.
- GitHub Actions run `26802075234`: success for commit `4da7c108e1005abd97855e24b203143c7ef8e7e0`.

## Source Linkage

- Repo: https://github.com/manuelsampedro1/verify-by-change
- Commit: https://github.com/manuelsampedro1/verify-by-change/commit/4da7c108e1005abd97855e24b203143c7ef8e7e0
- CI run: https://github.com/manuelsampedro1/verify-by-change/actions/runs/26802075234
- CLI source: https://raw.githubusercontent.com/manuelsampedro1/verify-by-change/main/verify_by_change.py
- Tests: https://raw.githubusercontent.com/manuelsampedro1/verify-by-change/main/tests/test_verify_by_change.py
- Readiness producer: https://github.com/manuelsampedro1/repo-flightcheck

## Takeaway

Verification advice should match the package surface, not only the file extension. For CLI packages, a passing import test is weaker than installing the package and smoking the command users will execute.
