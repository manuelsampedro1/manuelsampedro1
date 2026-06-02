# Node CLI Entrypoint Readiness

Use this before publishing or handing off a Node CLI repo to an agent, reviewer, or user.

## Goal

Make sure the command advertised by `package.json` can actually launch locally.

## Source Event

This recipe came from adding Node CLI entrypoint validation to `repo-flightcheck`.

The public change makes `repo-flightcheck` inspect `package.json` `bin` targets and warn when a CLI file is missing, lacks a Node shebang, or is not executable.

## Workflow

1. Open `package.json` and find the `bin` field.
2. Resolve every declared bin target relative to the repo root.
3. Confirm each target file exists.
4. Confirm the first line uses a Node shebang such as `#!/usr/bin/env node`.
5. Confirm the file is executable on POSIX systems.
6. Run the CLI through a safe path such as `--help`, `--version`, or a fixture input.
7. Keep the check in CI or a repo-readiness gate so the command cannot silently drift.

## Checklist

- Does every `bin` entry point to a real file?
- Does the target file have a Node shebang?
- Is the target executable in git, not only on the current machine?
- Does the README show an invocation that matches the actual command?
- Does CI run the same readiness or smoke check?

## Verification

```sh
node bin/your-cli.js --help
node --test
node /path/to/repo-flightcheck/bin/repo-flightcheck.js . --strict --threshold 80
git diff --check
```

## Failure Modes

- `package.json` advertises a CLI path that was renamed or deleted.
- The CLI works with `node bin/tool.js` but fails when invoked through the package bin because the shebang is missing.
- The script has a shebang but is not executable after clone.
- README examples drift from the actual `bin` command.
- Agent handoff says the repo is ready because tests pass, while the primary CLI cannot launch.

## Source Linkage

- Public repo: <https://github.com/manuelsampedro1/repo-flightcheck>
- Commit: <https://github.com/manuelsampedro1/repo-flightcheck/commit/cb13c46c058e63c6345e0417acba1b2fa1d7bb86>
- CI run: <https://github.com/manuelsampedro1/repo-flightcheck/actions/runs/26800753403>
- Lab note: <../labs/2026/2026-06-02-repo-flightcheck-node-cli-entrypoints.md>
