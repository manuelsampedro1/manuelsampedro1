# Local Tool Availability Preflight

Use this before giving a repo to Codex, Claude Code, or a reviewer when the expected verification commands are known.

## Goal

Catch the gap between documented commands and the local tools actually available in the agent environment.

## Source Event

This recipe came from adding `Tool availability` to `repo-flightcheck`.

The public change makes `repo-flightcheck` derive executables from detected verification, build, and lint commands, then warn when tools such as `npm`, `make`, `python`, `cargo`, or `swift` are missing from the current `PATH`.

## Workflow

1. Detect the repo's expected commands from package scripts, Makefile targets, stack config, or agent instructions.
2. Extract the executable for each command, such as `npm` from `npm test`.
3. Check whether that executable is available in the current `PATH`.
4. Report missing tools as warnings, not silent closeout surprises.
5. Include the exact commands that require each missing tool.
6. Keep CI verification separate, because CI may have a different toolchain than the local agent shell.
7. Document an equivalent local command only when it has actually been run.

## Checklist

- Can the current shell run the tool required by the test command?
- Can it run the tools required by build and lint commands?
- Does the warning include the missing tool and the command that needs it?
- Is CI still running the intended verification command?
- Does the closeout distinguish "not installed locally" from "verification failed"?

## Verification

```sh
node --test
node scripts/build.js
node scripts/lint.js
node /path/to/repo-flightcheck/bin/repo-flightcheck.js . --strict --threshold 80
git diff --check
```

## Failure Modes

- README says `npm test`, but the Codex desktop environment has Node without `npm`.
- A repo has Makefile verification, but `make` is missing in a container.
- Python tests are documented, but only `python3` is available while the command says `python`.
- CI passes, but the local handoff still cannot reproduce the command.
- The closeout claims verification succeeded when only an alternative command was run.

## Source Linkage

- Public repo: <https://github.com/manuelsampedro1/repo-flightcheck>
- Commit: <https://github.com/manuelsampedro1/repo-flightcheck/commit/44f62751ae089cdbb07dbd69520c8bf4879fbbd6>
- CI run: <https://github.com/manuelsampedro1/repo-flightcheck/actions/runs/26803070963>
- Lab note: <../labs/2026/2026-06-02-repo-flightcheck-tool-availability.md>
