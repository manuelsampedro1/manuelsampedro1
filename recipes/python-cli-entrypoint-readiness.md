# Python CLI Entrypoint Readiness

Use this before handing a Python CLI repo to an agent or publishing it as proof work.

## Goal

Make sure `pyproject.toml` console scripts point to modules and functions that exist, especially in `src/` layout repos.

## Source Event

This recipe came from adding Python CLI entrypoint validation to `repo-flightcheck`.

The public change checks `[project.scripts]` entries shaped as `module:function` and reports missing modules, missing functions, or malformed targets.

## Workflow

1. Inspect `pyproject.toml` for `[project.scripts]`.
2. Confirm each script target uses `module:function`.
3. Check that the module exists as either `package/module.py`, `package/module/__init__.py`, `src/package/module.py`, or `src/package/module/__init__.py`.
4. Check that the referenced function is defined in that module.
5. Run `repo-flightcheck` and treat Python CLI entrypoint warnings as publish blockers for CLI repos.
6. Run the local test command after fixing entrypoint issues.

## Example

```toml
[project.scripts]
agent-task-contract = "agent_task_contract.cli:main"
```

Expected source path:

```text
src/agent_task_contract/cli.py
```

Expected Python function:

```python
def main():
    ...
```

Run the readiness check:

```sh
node /path/to/repo-flightcheck/bin/repo-flightcheck.js /path/to/python-cli --json
```

Expected signal:

```text
PASS  Python CLI entrypoint        Validated 1 Python CLI entrypoint.
```

## Checklist

- Does `pyproject.toml` declare the intended script under `[project.scripts]`?
- Does the target use `module:function` rather than a free-form command?
- Is the module path valid for the repo layout?
- Is the referenced function defined?
- Does CI run the same test command expected locally?
- Does README show the command a reviewer can actually run?

## Failure Modes

- Moving code into `src/` without updating the package path.
- Renaming `main()` or `cli()` while leaving the script target stale.
- Declaring a console script before the module exists.
- Treating `python -m unittest` passing as proof that the installed CLI command works.
- Documenting a CLI command that cannot be imported after package install.

## Source Linkage

- Public repo: <https://github.com/manuelsampedro1/repo-flightcheck>
- Commit: <https://github.com/manuelsampedro1/repo-flightcheck/commit/b678a19bbf5aaf671a6c8bcd69e61c4e9781fe9c>
- CI run: <https://github.com/manuelsampedro1/repo-flightcheck/actions/runs/26801847938>
- Lab note: <../labs/2026/2026-06-02-repo-flightcheck-python-cli-entrypoints.md>
