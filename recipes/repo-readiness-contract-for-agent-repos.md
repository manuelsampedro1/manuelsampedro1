# Repo Readiness Contract for Agent Repos

Use this when a small public repo has useful behavior but still feels incomplete to reviewers or coding agents.

## Goal

Make the repo easy to clone, inspect, run, and hand to an agent without adding fake complexity.

## Source Event

This recipe came from hardening `verify-by-change` after `repo-flightcheck` flagged missing repo-readiness signals.

The source repo moved from a weak readiness score to `100/100` by adding a small operating contract instead of changing the CLI's scope.

## Workflow

1. Run a readiness audit before editing so the work is anchored in actual gaps.
2. Add `AGENTS.md` with purpose, constraints, and exact verification commands.
3. Add a license if the repo is public and meant to be reused.
4. Add standard local targets such as `make test`, `make build`, and `make lint`.
5. Make CI run the same local targets, not a separate hidden command path.
6. Add package metadata only as far as it helps install or invoke the tool.
7. Add one stable example or fixture that shows the output shape.
8. Update README with install, usage, examples, and verification.
9. Re-run the readiness audit on a clean working tree after commit.

## Checklist

- Does the README explain install and usage without relying on tribal knowledge?
- Is there one obvious test command?
- Is there one obvious build or syntax command?
- Is there one obvious lint or preflight command?
- Does CI execute the same local commands?
- Does `AGENTS.md` tell a coding agent what not to change?
- Are `.env` files ignored?
- Is there at least one example or fixture that proves expected output?
- Is the working tree clean before claiming readiness?

## Verification

For a dependency-light Python CLI:

```sh
make test
make build
make lint
python3 verify_by_change.py verify_by_change.py README.md
node /path/to/repo-flightcheck/bin/repo-flightcheck.js . --strict --threshold 80
git diff --check
```

## Failure Modes

- Adding packaging before the tool has a real command surface.
- Treating CI existence as proof when CI does not run local verification.
- Writing a generic `AGENTS.md` that does not name scope, constraints, or checks.
- Adding examples that are not generated from or consistent with the real CLI.
- Claiming a clean readiness score while uncommitted local changes still exist.

## Source Linkage

- Public repo: <https://github.com/manuelsampedro1/verify-by-change>
- Commit: <https://github.com/manuelsampedro1/verify-by-change/commit/dd26fffd7fb3c7b296aa8a620e954e0fc52a4e93>
- CI run: <https://github.com/manuelsampedro1/verify-by-change/actions/runs/26796285609>
- Lab note: <../labs/2026/2026-06-02-verify-by-change-readiness-contract.md>
