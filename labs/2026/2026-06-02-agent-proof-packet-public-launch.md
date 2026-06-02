# 2026-06-02 - Agent Proof Packet Public Launch

## Context

`agent-proof-packet` is the review artifact layer for the agent workflow stack. Diffs, check results, closeout notes, risks, decisions, and open questions often sit in separate places; reviewers need one compact packet that shows what was actually proved.

The local repo needed agent instructions, Make targets, explicit `.env` hygiene, README command alignment, CI/local command parity, non-complete exit-code semantics, and safer evidence-path rendering before public launch.

## Useful Artifact

`agent-proof-packet` is now public as a dependency-free Python CLI that generates Markdown or JSON packets with:

- changed files,
- explicit check results,
- evidence files and headings,
- risks,
- decisions,
- open questions,
- missing evidence,
- final verdict.

It exits `0` only for `complete`. `needs-review` and `blocked` return `1`, and evidence output preserves the declared relative path instead of leaking local absolute paths into PR-ready packets.

## Source Linkage

- Public repo: <https://github.com/manuelsampedro1/agent-proof-packet>
- Commit: <https://github.com/manuelsampedro1/agent-proof-packet/commit/d8ea5ca5a7bbc9ae892399e53cb1a844f7a1ae05>
- README: <https://raw.githubusercontent.com/manuelsampedro1/agent-proof-packet/main/README.md>
- CLI: <https://raw.githubusercontent.com/manuelsampedro1/agent-proof-packet/main/src/agent_proof_packet/cli.py>
- Tests: <https://raw.githubusercontent.com/manuelsampedro1/agent-proof-packet/main/tests/test_cli.py>
- Sample diff: <https://raw.githubusercontent.com/manuelsampedro1/agent-proof-packet/main/examples/sample.diff>
- Closeout fixture: <https://raw.githubusercontent.com/manuelsampedro1/agent-proof-packet/main/examples/closeout.md>
- CI badge: <https://github.com/manuelsampedro1/agent-proof-packet/actions/workflows/ci.yml/badge.svg?branch=main>
- Recipe: [`../../recipes/agent-proof-packet-for-review.md`](../../recipes/agent-proof-packet-for-review.md)

## Verification

Local checks:

```sh
make test
make lint
make build
make smoke
git diff --check
node /path/to/repo-flightcheck/bin/repo-flightcheck.js . --check-remote --strict --threshold 80
```

Results:

- `make test`: 6 tests passed.
- `make lint`: compile check passed.
- `make build`: compile check passed.
- `make smoke`: rendered complete Markdown and JSON proof packets.
- `repo-flightcheck --check-remote --strict --threshold 80`: `100/100`.
- Public repo, commit, README, CLI source, tests, sample diff, and closeout fixture raw URLs returned `200`.
- Public CI badge reports `CI - passing`.

## Takeaway

Review evidence should be one inspectable artifact. `agent-proof-packet` makes agent handoffs easier to challenge, archive, and attach to PRs or ledgers.
