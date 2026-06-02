# Empty Diff Verification Guard

Use this when a verification helper derives checks from changed files.

## Goal

Avoid silent no-op verification. If there are no changed files, the tool should say so explicitly, and automation should be able to fail when a diff was expected.

## Source Event

This recipe came from `verify-by-change` commit `8fbb14ef523e`, which added explicit empty-change output and `--fail-on-empty`.

Relevant files:

- `verify_by_change.py`
- `tests/test_verify_by_change.py`
- `README.md`
- `DECISIONS.md`

## Workflow

1. Detect changed files normally.
2. Render a clear empty state when the classified change set is empty.
3. Keep the local default non-failing so users can inspect clean repos without noise.
4. Add a `--fail-on-empty` option for CI and scripted handoffs.
5. Use a distinct exit code, such as `2`, so callers can distinguish “no files” from validation or runtime failure.
6. Keep JSON output stable; an empty change set can be `{}`.
7. Test the renderer, JSON artifact, and CLI exit code against a clean Git fixture.

## Checklist

- Does the Markdown output say no changed files were detected?
- Does JSON output remain parseable for empty input?
- Does CI have an opt-in way to fail on empty?
- Is the empty exit code documented?
- Do tests use a real clean Git repo, not only mocked paths?

## Verification

For a standard-library Python CLI, run:

```sh
python3 -m py_compile verify_by_change.py
python3 -m unittest discover -s tests
python3 verify_by_change.py --repo <clean-repo> --fail-on-empty
```

Expect exit code `2` for the last command when the repo has no changed files.

## Failure Modes

- Printing only a title with no sections and making users infer emptiness.
- Returning success in CI when the workflow expected a changed file list.
- Treating empty diffs as a generic crash.
- Emitting malformed JSON for empty classifications.
- Failing by default for local users who only wanted to inspect the current repo.

## Source Linkage

- Public repo: <https://github.com/manuelsampedro1/verify-by-change>
- Commit: <https://github.com/manuelsampedro1/verify-by-change/commit/8fbb14ef523e7973dc9ca96d8876fe6e0c2dbe2c>
- CI run: <https://github.com/manuelsampedro1/verify-by-change/actions/runs/26793152799>
