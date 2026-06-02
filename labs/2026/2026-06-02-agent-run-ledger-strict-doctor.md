# 2026-06-02 - Agent Run Ledger Strict Doctor

## Context

`agent-run-ledger` could import verification checklists as planned command evidence and expose doctor output in text or JSON. The weak point was closeout enforcement: a ledger could still contain planned or running commands, but a normal doctor run would only print counts.

For agent handoffs, that distinction matters. A planned verification command is useful as a plan, but it is not evidence that verification happened.

## Change

- Added `doctor --strict`.
- Added `summary.openCommands` for command evidence still marked `planned` or `running`.
- Kept text and JSON doctor output backward-compatible, with additive summary data.
- Made strict mode set exit code `1` when open commands or attention items remain.
- Added tests for strict doctor behavior and `openCommands` JSON output.
- Updated README examples and handoff guidance.

Public commit: `cc7ac08f0def feat: add strict doctor gate`.

## Verification

Local checks:

```sh
node --test
node scripts/lint.js
node scripts/build.js
git diff --check
```

Strict-mode smoke:

```sh
tmpdir=$(mktemp -d)
node bin/agent-run-ledger.js demo --out "$tmpdir" >/tmp/ledger-demo-output.txt
node bin/agent-run-ledger.js doctor --ledger "$tmpdir/ledger.jsonl" --strict >/tmp/ledger-strict-pass.txt
printf '## Python\n\n- `app.py`\n\n- Run tests.\n' > "$tmpdir/checklist.md"
node bin/agent-run-ledger.js import-checklist --ledger "$tmpdir/planned.jsonl" --checklist "$tmpdir/checklist.md" >/tmp/ledger-import-output.txt
node bin/agent-run-ledger.js doctor --ledger "$tmpdir/planned.jsonl" --strict >/tmp/ledger-strict-fail.txt
```

Results:

- `node --test`: 14 tests passed.
- Lint and build preflight passed.
- Strict doctor passed for the demo ledger.
- Strict doctor returned non-zero for a ledger with planned imported checks.
- Strict JSON output included one `openCommands` entry for the planned command.
- Public commit page and raw changed files returned `200`.
- GitHub Actions run `26794153252` completed with conclusion `success`.

## Source Linkage

- Repo: <https://github.com/manuelsampedro1/agent-run-ledger>
- Commit: <https://github.com/manuelsampedro1/agent-run-ledger/commit/cc7ac08f0deffedc8f4568a15bac8a6858c8a743>
- CI run: <https://github.com/manuelsampedro1/agent-run-ledger/actions/runs/26794153252>
- CLI: <https://raw.githubusercontent.com/manuelsampedro1/agent-run-ledger/cc7ac08f0deffedc8f4568a15bac8a6858c8a743/src/cli.js>
- Tests: <https://raw.githubusercontent.com/manuelsampedro1/agent-run-ledger/cc7ac08f0deffedc8f4568a15bac8a6858c8a743/test/ledger.test.js>

## Takeaway

An audit trail should distinguish planned checks from executed evidence. Strict doctor mode turns that distinction into a gate that automation can enforce before closeout.
