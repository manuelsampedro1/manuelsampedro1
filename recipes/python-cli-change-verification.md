# Python CLI Change Verification

Use this when a coding agent changes a Python package that exposes console scripts.

## Workflow

1. Confirm the repo has `pyproject.toml` with `[project.scripts]`.
2. Run `verify-by-change --repo PATH --json` so the tool can inspect repo context, not only changed paths.
3. If the output includes `python_cli`, install the package in editable mode with `python3 -m pip install -e .`.
4. Smoke each changed console command with `--help`, `--version`, or the safest deterministic input available.
5. Run the targeted unit tests around the command parser, entrypoint module, and any changed implementation paths.
6. Close out with the exact install, smoke, and test commands rather than a generic "tests passed" note.

## Checklist

- The console script target still imports.
- The installed command resolves to the changed code.
- `pyproject.toml` script names match the intended public command names.
- The command fails clearly on invalid input.
- The README or usage docs still match the command surface if they mention it.

## Failure Modes

- Running only `python3 -m unittest` while the console script target is broken.
- Testing `python path/to/cli.py` even though users run an installed command.
- Forgetting editable install after changing script metadata.
- Treating `pyproject.toml` changes as generic config instead of command-surface changes.
- Closing the agent run without naming the smoke command that proved the entrypoint works.

## Source

- Lab note: <../labs/2026/2026-06-02-verify-by-change-python-cli-context.md>
- Repo: https://github.com/manuelsampedro1/verify-by-change
- Commit: https://github.com/manuelsampedro1/verify-by-change/commit/4da7c108e1005abd97855e24b203143c7ef8e7e0
- CI run: https://github.com/manuelsampedro1/verify-by-change/actions/runs/26802075234
