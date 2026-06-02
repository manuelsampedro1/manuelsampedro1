# Documented Command Drift Check

Use this when README, runbook, or `AGENTS.md` instructions tell an agent which commands to run.

## Goal

Catch stale documented commands before a coding agent or reviewer follows them. The repo should not advertise `npm run e2e`, `make test`, or a stack test command unless that command maps to an actual script, target, or project type.

## Source Event

This recipe came from `repo-flightcheck` commit `767ccb2320a2`, which added the `Documented commands` check.

Relevant files:

- `src/scan.js`
- `test/scan.test.js`
- `README.md`

## Workflow

1. Scan README and agent instruction files for common runnable commands.
2. Deduplicate equivalent README filenames on case-insensitive filesystems.
3. Compare `npm test` and `npm run <script>` against `package.json`.
4. Compare `make <target>` against Makefile targets.
5. Treat stack commands as valid only when the matching project marker exists.
6. Report unresolved commands with the source file and exact command.
7. Keep the rule heuristic and explicit; do not pretend to parse every shell command.

## Checklist

- Does every command in README or `AGENTS.md` map to a script, Make target, or stack marker?
- Are built-in setup commands such as npm install handled without requiring a package script?
- Does the warning name the source file and exact command?
- Are command examples in prose written so they do not look like required repo commands?
- Does CI run the same scanner after the rule changes?

## Verification

For a Node repo-readiness scanner:

```sh
node --test
node scripts/lint.js
node scripts/build.js
node bin/repo-flightcheck.js . --strict --threshold 80
```

## Failure Modes

- Letting README verification instructions drift from package scripts.
- Treating all CI presence as enough while local docs point to a different command.
- Flagging explanatory prose as if it were a required command.
- Ignoring case-insensitive README duplicates on macOS.
- Hiding unresolved commands without file-level evidence.

## Source Linkage

- Public repo: <https://github.com/manuelsampedro1/repo-flightcheck>
- Commit: <https://github.com/manuelsampedro1/repo-flightcheck/commit/767ccb2320a21935d87fbc9bce9b4dc956d01aac>
- CI run: <https://github.com/manuelsampedro1/repo-flightcheck/actions/runs/26794828840>
