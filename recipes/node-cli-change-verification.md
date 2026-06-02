# Node CLI Change Verification

Use this when a Codex change touches JavaScript or TypeScript in a Node CLI or small Node runtime package.

## Goal

Avoid treating every `.js` or `.ts` diff as a web/UI change. A CLI package needs runtime checks, command-path coverage, and safe input smokes.

## Source Event

This recipe came from adding Node CLI context detection to `verify-by-change`.

The public change makes `verify-by-change` inspect `package.json` for `bin` plus test/build/lint/check scripts, then emit `node_cli` guidance instead of generic web guidance.

## Workflow

1. Confirm whether the repo has a CLI entrypoint, usually `package.json` `bin`.
2. Check whether local scripts exist for `test`, `build`, `lint`, or `check`.
3. Classify changed JS/TS files in that repo as Node runtime or CLI surface, not browser UI by default.
4. Run the closest test/build/lint command that exercises the changed code path.
5. Run one safe CLI smoke with minimal input, help output, a fixture file, or a no-op mode.
6. If a review packet is the source, preserve the packet's repo path so context-sensitive verification still works.
7. Report any live integrations, credentials, or destructive commands that were intentionally not exercised.

## Checklist

- Does `package.json` expose a `bin` entrypoint?
- Did the changed file affect CLI argument parsing, exit codes, stdout/stderr, file writes, or JSON output shape?
- Did tests cover both success and failure paths?
- Did the smoke command avoid network calls, production data, deploys, and credentials?
- Did generated review or verification artifacts keep the repo context intact?

## Verification

```sh
python3 -m unittest discover -s tests
python3 verify_by_change.py --repo /path/to/node-cli --json
node bin/your-cli.js --help
git diff --check
```

## Failure Modes

- Reporting "UI not checked" for a backend or CLI-only Node change.
- Running only syntax checks when argument parsing or output contracts changed.
- Exercising a destructive CLI command instead of a safe help, dry-run, or fixture path.
- Dropping repo metadata when a review packet is converted into a verification envelope.

## Source Linkage

- Public repo: <https://github.com/manuelsampedro1/verify-by-change>
- Commit: <https://github.com/manuelsampedro1/verify-by-change/commit/bb4cf7a85ba16eccbb7604e5c2df3b9dd2bae5d5>
- CI run: <https://github.com/manuelsampedro1/verify-by-change/actions/runs/26800472479>
- Lab note: <../labs/2026/2026-06-02-verify-by-change-node-cli-context.md>
