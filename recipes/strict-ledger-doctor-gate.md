# Strict Ledger Doctor Gate

Use this when an agent run ledger should block closeout until verification evidence is resolved.

## Goal

Make planned or running command evidence visible as an incomplete handoff state. A checklist imported into a ledger is useful, but it should not count as executed verification until command evidence is marked passed, done, blocked, failed, or otherwise resolved.

## Source Event

This recipe came from `agent-run-ledger` commit `cc7ac08f0def`, which added `doctor --strict`.

Relevant files:

- `src/cli.js`
- `src/ledger.js`
- `test/ledger.test.js`
- `README.md`

## Workflow

1. Start a ledger before a non-trivial agent run.
2. Import or record planned verification commands.
3. Run the actual checks.
4. Record command evidence with concrete status.
5. Run `agent-run-ledger doctor --ledger <path> --strict`.
6. Fail closeout when open commands or attention items remain.
7. Use `doctor --json --strict` when another tool needs structured failure data.

## Checklist

- Are planned and running command entries counted separately?
- Does strict mode fail when open command evidence remains?
- Does strict mode also fail when blockers, failed checks, or skipped checks need attention?
- Does text output remain readable for humans?
- Does JSON output expose the same summary data?
- Is the exit code tested through the CLI path?

## Verification

For a zero-dependency Node CLI:

```sh
node --test
node scripts/lint.js
node scripts/build.js
node bin/agent-run-ledger.js doctor --ledger .agent-run/ledger.jsonl --strict
```

For automation:

```sh
node bin/agent-run-ledger.js doctor --ledger .agent-run/ledger.jsonl --json --strict > /tmp/ledger-doctor.json
```

Expect exit code `1` when the ledger still has planned or running commands.

## Failure Modes

- Treating imported checklist items as executed evidence.
- Printing counts but never returning a failing exit code.
- Failing on planned commands but ignoring blockers.
- Hiding the reason for strict failure from JSON output.
- Using a fake readiness score instead of explicit evidence state.

## Source Linkage

- Public repo: <https://github.com/manuelsampedro1/agent-run-ledger>
- Commit: <https://github.com/manuelsampedro1/agent-run-ledger/commit/cc7ac08f0deffedc8f4568a15bac8a6858c8a743>
- CI run: <https://github.com/manuelsampedro1/agent-run-ledger/actions/runs/26794153252>
