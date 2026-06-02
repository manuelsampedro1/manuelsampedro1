# 2026-06-02 - Agent Run Ledger Review Packet CI Evidence

## Context

`codex-review-packet` can now render a `## CI Evidence` section from GitHub Actions run JSON.

The next auditability gap was in `agent-run-ledger`: importing a review packet captured changed files, review lanes, readiness, and verification checks, but it did not turn embedded CI evidence into a ledger command event.

## Change

- Added `CI Evidence` to the recognized review packet sections.
- Parsed embedded run ID, workflow, status, conclusion, branch, SHA, event, URL, and source path.
- Reused the existing CI status mapping so embedded evidence becomes `passed`, `failed`, `running`, `planned`, `skipped`, or `done` command evidence.
- Preserved both the review packet path and the original CI JSON source path as referenced files.
- Fixed `ciRunEvent` option normalization so a single link string is not expanded character-by-character.
- Updated README language and added parser, event, and CLI import tests.

Public commit: `79ccca7eff5b feat: import review packet ci evidence`.

## Verification

Local checks:

```sh
node --test
node scripts/lint.js
node scripts/build.js
git diff --check
node /Users/manuelsampedro/Documents/Codex/2026-05-21/repo-flightcheck/bin/repo-flightcheck.js . --strict --threshold 80
```

Results:

- `node --test`: 39 tests passed.
- `node scripts/lint.js`: passed.
- `node scripts/build.js`: passed.
- `git diff --check`: passed.
- End-to-end smoke built a `codex-review-packet` packet with real CI run `26801172625`, imported it with `agent-run-ledger import-review-packet`, and `doctor --json` reported 2 events, 1 command, 0 open commands, and 0 attention items.
- `repo-flightcheck`: `100/100` after commit.
- GitHub Actions run `26801558072` completed with conclusion `success` for commit `79ccca7eff5b3b961293652a4f5d5841f01df20a`.

## Source Linkage

- Repo: <https://github.com/manuelsampedro1/agent-run-ledger>
- Commit: <https://github.com/manuelsampedro1/agent-run-ledger/commit/79ccca7eff5b3b961293652a4f5d5841f01df20a>
- CI run: <https://github.com/manuelsampedro1/agent-run-ledger/actions/runs/26801558072>
- CLI: <https://raw.githubusercontent.com/manuelsampedro1/agent-run-ledger/main/src/cli.js>
- Tests: <https://raw.githubusercontent.com/manuelsampedro1/agent-run-ledger/main/test/ledger.test.js>
- Review packet producer: <https://github.com/manuelsampedro1/codex-review-packet>

## Takeaway

Audit trails should not lose evidence when artifacts move between tools. A review packet can now carry CI proof, and the ledger can import that proof as durable command evidence tied to a run URL and commit SHA.
