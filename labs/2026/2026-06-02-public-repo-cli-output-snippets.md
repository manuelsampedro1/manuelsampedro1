# 2026-06-02 - Public Repo CLI Output Snippets

## Context

The profile already promotes `repo-flightcheck` and `agent-run-ledger` as primary proof repos. Both were public, tested, and pushed, but their first-read README experience could show more executable proof before readers inspect implementation details.

## Change

- `repo-flightcheck` now includes fixture-backed CLI output from `node bin/repo-flightcheck.js fixtures/sample-repo`.
- `agent-run-ledger` now includes sample `doctor` and `report` commands plus their expected CLI output.
- Both changes were pushed to their public GitHub remotes.

## Verification

For `repo-flightcheck`:

```sh
node --test
node scripts/lint.js
node scripts/build.js
node bin/repo-flightcheck.js fixtures/sample-repo
git push
```

For `agent-run-ledger`:

```sh
node --test
node scripts/lint.js
node scripts/build.js
node bin/agent-run-ledger.js doctor --ledger examples/sample-ledger.jsonl
node bin/agent-run-ledger.js report --ledger examples/sample-ledger.jsonl --out /tmp/agent-run-ledger-report.html
git push
```

`npm test` was not used because `npm` is not installed in this local environment; the equivalent available test command was `node --test`.

## Takeaway

Public proof repos should show a runnable output sample near the top of the README. It reduces trust friction: a reviewer sees the tool's shape, output vocabulary, and failure mode before reading code.

## Source Linkage

- `repo-flightcheck` commit: `4005ba0 docs: show fixture audit output`
- `agent-run-ledger` commit: `c55ac7f docs: show sample ledger output`
