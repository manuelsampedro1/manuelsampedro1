# 2026-06-02 - Diff to Eval Public Launch

## Context

`diff-to-eval` is the learning-loop piece of the agent reliability stack: after a useful or risky agent run, the real diff should become a reusable evaluation case instead of disappearing into chat history.

The local repo needed agent instructions, Make targets, secret hygiene, and local command alignment before public launch.

## Useful Artifact

`diff-to-eval` is now public as a dependency-free Python CLI that turns unified diffs into `diff-to-eval.v1` JSON cases with:

- changed files,
- additions and deletions,
- lightweight risk tags,
- suggested verification checks,
- expected outcomes,
- notes for future evaluators.

## Source Linkage

- Public repo: <https://github.com/manuelsampedro1/diff-to-eval>
- Commit: <https://github.com/manuelsampedro1/diff-to-eval/commit/bd196719a29db55f99aec3640d20f12916d2801a>
- README: <https://raw.githubusercontent.com/manuelsampedro1/diff-to-eval/main/README.md>
- CLI: <https://raw.githubusercontent.com/manuelsampedro1/diff-to-eval/main/src/diff_to_eval/cli.py>
- Tests: <https://raw.githubusercontent.com/manuelsampedro1/diff-to-eval/main/tests/test_cli.py>
- Example diff: <https://raw.githubusercontent.com/manuelsampedro1/diff-to-eval/main/examples/sample.diff>
- CI badge: <https://github.com/manuelsampedro1/diff-to-eval/actions/workflows/ci.yml/badge.svg?branch=main>

## Verification

Local checks:

```sh
make test
make lint
make build
git diff --check
PYTHONPATH=src python3 -m diff_to_eval examples/sample.diff --title "Sample" --output /tmp/diff-to-eval-case.json
node /path/to/repo-flightcheck/bin/repo-flightcheck.js . --check-remote --strict --threshold 80
```

Results:

- `make test`: 4 tests passed.
- `make lint`: compile check passed.
- `make build`: compile check passed.
- CLI smoke wrote a JSON case with schema `diff-to-eval.v1`.
- The sample case inferred `automation`, `documentation`, and `shell` risk tags.
- `repo-flightcheck --check-remote --strict --threshold 80`: `100/100`.
- Public repo, commit, README, CLI source, tests, and example raw URLs returned `200`.
- Public CI badge reports `CI - passing`.

## Takeaway

Real diffs are better eval seeds than generic prompts. `diff-to-eval` gives the profile a concrete way to turn shipped agent work into future regression cases.
