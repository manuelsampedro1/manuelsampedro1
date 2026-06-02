# 2026-06-02 - Agent Tool Call Audit Public Launch

## Source

- Public repo: https://github.com/manuelsampedro1/agent-tool-call-audit
- Published HEAD: `274aba5b606ebecd1e742c01b7aa3fa645c2c17c`
- CI run: https://github.com/manuelsampedro1/agent-tool-call-audit/actions/runs/26833266596

## What Changed

Built and published `agent-tool-call-audit`, a dependency-free Python CLI that
audits coding-agent tool-call logs for risky actions and repeated failures.

The tool reports:

- destructive shell commands such as hard resets, force pushes, broad deletes,
  unsafe install pipes, privileged commands, and skipped hooks,
- sensitive tool names such as send, delete, deploy, publish, payment, secret,
  credential, token, and key actions,
- repeated failed commands or tool calls,
- secret-material markers in tool input or output with rendered evidence
  redacted,
- shell commands missing a structured working directory in JSONL logs,
- Markdown or JSON output for proof packets, CI gates, and run ledgers.

## Why It Matters

Preflight guards are not enough. A coding-agent run can contain risky tool calls
or repeated failed attempts while the final answer still sounds disciplined.

`agent-tool-call-audit` gives reviewers a deterministic post-run pass over the
actual tool history. It does not claim to be a sandbox or full security audit.
It highlights the exact tool call, rule, severity, redacted evidence, and
follow-up checks before a run is accepted.

## Verification

Ran locally:

```sh
make test
make lint
make build
make smoke
git diff --check
```

Additional checks:

- editable install in a temporary virtualenv after upgrading `pip`, `setuptools`, and `wheel`,
- `agent-instruction-audit AGENTS.md --min-score 80` at `100/100`,
- `repo-flightcheck . --check-remote --strict --threshold 80` at `100/100`,
- public repo and raw README/source/test/example URLs returned `200`,
- GitHub Actions run `26833266596` completed with `success`.

## Takeaway

Tool-call history deserves its own review gate. If an agent used risky tools,
retried the same failing action, skipped hooks, or exposed secret markers, that
evidence should be visible before the closeout becomes trusted proof.
