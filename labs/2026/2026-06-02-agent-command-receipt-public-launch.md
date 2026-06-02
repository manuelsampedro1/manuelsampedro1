# 2026-06-02 - Agent Command Receipt Public Launch

## Context

`agent-command-receipt` covers the gap between "I ran this command" and reusable evidence. Closeout checks and claim checks can flag vague verification language, but command evidence still needs a compact artifact that records status, exit code, timestamp, and evidence file hashes.

Terminal GitHub write auth is still unavailable, so the public repo was populated through browser-authenticated GitHub commits and then checked by raw-file hashes, a fresh public clone, local commands, and GitHub Actions.

## Useful Artifact

`agent-command-receipt` is now public as a dependency-free Python CLI that can:

- create JSON command receipts,
- render Markdown receipt summaries,
- hash evidence files with SHA-256,
- verify receipts after file changes,
- fail when evidence files are missing or drifted,
- preserve `pass`, `fail`, `blocked`, and `skipped` command outcomes.

This gives proof packets, closeout checks, claim checks, and run ledgers a stricter source of command evidence than copied terminal text.

## Source Linkage

- Public repo: <https://github.com/manuelsampedro1/agent-command-receipt>
- Current public HEAD: <https://github.com/manuelsampedro1/agent-command-receipt/commit/358ad912b161fa7d385551e10e44fc72aff2e16a>
- README: <https://raw.githubusercontent.com/manuelsampedro1/agent-command-receipt/main/README.md>
- CLI: <https://raw.githubusercontent.com/manuelsampedro1/agent-command-receipt/main/src/agent_command_receipt/cli.py>
- Tests: <https://raw.githubusercontent.com/manuelsampedro1/agent-command-receipt/main/tests/test_cli.py>
- Passing receipt: <https://raw.githubusercontent.com/manuelsampedro1/agent-command-receipt/main/examples/passing-receipt.json>
- CI run: <https://github.com/manuelsampedro1/agent-command-receipt/actions/runs/26822164679>
- Recipe: [`../../recipes/agent-command-receipt.md`](../../recipes/agent-command-receipt.md)

## Verification

Fresh public clone checks:

```sh
make test
make lint
make build
make smoke
python3 -m venv .venv
.venv/bin/python -m pip install --upgrade pip
.venv/bin/python -m pip install -e .
.venv/bin/agent-command-receipt verify examples/passing-receipt.json
```

Results:

- `make test`: 5 tests passed.
- `make lint`: Python compile check passed.
- `make build`: compileall check passed.
- `make smoke`: receipt create, verify, example verify, and Markdown output checks passed.
- Editable install from the fresh public clone succeeded.
- `agent-command-receipt verify examples/passing-receipt.json`: `Verdict: passed`.
- Raw workflow SHA-256 matched the local `.github/workflows/ci.yml`.
- GitHub Actions run `26822164679`: completed with `success`.

## Takeaway

Agent verification should not stop at a confident sentence. A command receipt lets later tools ask a sharper question: does the evidence attached to this command still exist, and does it still hash to what the agent claimed?
