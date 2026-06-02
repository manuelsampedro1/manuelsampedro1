# Agent Command Receipt

Use this when a command result will be reused in a closeout, proof packet, ledger, or follow-up agent handoff.

## Use When

- A final answer says tests, lint, build, smoke, or CI passed.
- A proof packet needs evidence files, not just a sentence that verification happened.
- A later agent or reviewer should detect whether evidence files drifted after the command ran.
- A command result should be imported into a run ledger without losing status, exit code, or timestamp.

## Goal

Create a compact receipt that records:

- the exact command,
- `pass`, `fail`, `blocked`, or `skipped` status,
- exit code,
- creation time,
- evidence file paths and SHA-256 hashes.

Then verify the receipt before reusing it. Verification should fail if an evidence file is missing or its hash changed.

## Workflow

1. Run the verification command and keep any evidence files.

```sh
make test
```

2. Create a receipt from the command result.

```sh
PYTHONPATH=src python3 -m agent_command_receipt create \
  --command "make test" \
  --status pass \
  --exit-code 0 \
  --created-at 2026-06-02T00:00:00Z \
  --base-dir . \
  --evidence examples/test-output.log \
  --output /tmp/agent-command-receipt.json
```

3. Verify the receipt before attaching it to a closeout, proof packet, or ledger.

```sh
PYTHONPATH=src python3 -m agent_command_receipt verify /tmp/agent-command-receipt.json --base-dir .
```

4. If verification fails, do not reuse the claim. Rerun the command, regenerate the evidence, or mark the blocker explicitly.

## Prompt Pattern

```text
Before closing this agent run, create a command receipt for every verification claim.

Rules:
- Include exact command text, status, exit code, and timestamp.
- Attach evidence file hashes for logs, reports, or generated artifacts.
- Verify receipts after file changes and before final answer claims.
- If a receipt does not verify, report the drift instead of claiming the command still passed.
```

## Fast Checklist

- Is every strong verification claim backed by an exact command?
- Does each receipt include status and exit code?
- Are evidence files relative to the repo or declared base directory?
- Did receipt verification run after the last file change?
- Did any missing or drifted evidence downgrade the closeout claim?

## Failure Modes

- Treating copied terminal output as durable evidence without file hashes.
- Reusing an old receipt after README, examples, tests, or generated artifacts changed.
- Omitting `blocked` or `skipped` command outcomes and making the run look cleaner than it was.
- Letting proof packets or ledgers import command claims without checking evidence drift first.

## Source Linkage

- Public repo: <https://github.com/manuelsampedro1/agent-command-receipt>
- Current public HEAD: <https://github.com/manuelsampedro1/agent-command-receipt/commit/358ad912b161fa7d385551e10e44fc72aff2e16a>
- CI run: <https://github.com/manuelsampedro1/agent-command-receipt/actions/runs/26822164679>
- README: <https://raw.githubusercontent.com/manuelsampedro1/agent-command-receipt/main/README.md>
- CLI: <https://raw.githubusercontent.com/manuelsampedro1/agent-command-receipt/main/src/agent_command_receipt/cli.py>
- Tests: <https://raw.githubusercontent.com/manuelsampedro1/agent-command-receipt/main/tests/test_cli.py>
- Passing receipt: <https://raw.githubusercontent.com/manuelsampedro1/agent-command-receipt/main/examples/passing-receipt.json>
- Launch note: [`../labs/2026/2026-06-02-agent-command-receipt-public-launch.md`](../labs/2026/2026-06-02-agent-command-receipt-public-launch.md)
- Supporting recipes: [`./agent-claim-check.md`](./agent-claim-check.md), [`./agent-proof-packet-for-review.md`](./agent-proof-packet-for-review.md), and [`./verification-envelope-to-ledger-evidence.md`](./verification-envelope-to-ledger-evidence.md).
