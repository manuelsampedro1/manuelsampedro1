# 2026-06-02 - Agent Memory Audit Public Launch

## Source

- Public repo: https://github.com/manuelsampedro1/agent-memory-audit
- Published HEAD: `a9091b5f0337f59a594de39dd0bc7a70279f7b9c`
- CI run: https://github.com/manuelsampedro1/agent-memory-audit/actions/runs/26833979294

## What Changed

Built and published `agent-memory-audit`, a dependency-free Python CLI for
reviewing local agent memory files before the next run reuses them as context.

The tool reports:

- secret-material markers and unsafe credential-handling notes with redacted
  evidence,
- stale dated entries and higher-priority stale claims that still say
  "current", "authenticated", or "latest",
- current-state or external claims that lack nearby source evidence,
- public-action notes such as publishing, sending, deploying, deleting, or
  billing without explicit human approval language,
- absolute local paths that need review before public reuse,
- missing memory usage rules or weak memory hygiene policy.

## Why It Matters

Agent memory is useful only when it is treated as auxiliary context, not as a
source of truth. Old account-state notes, browser-auth claims, permission
shortcuts, or copied credential hints can silently steer a future run.

`agent-memory-audit` gives reviewers a deterministic local pass before memory
is imported into a handoff, run ledger, proof packet, or automation loop. It
does not claim to verify truth or replace a full secret scanner; it makes risky
memory reuse visible enough to stop and re-check.

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
- GitHub Actions run `26833979294` completed with `success`.

## Takeaway

Memory hygiene needs a gate before reuse. If a memory file contains stale
current-state claims, missing sources, unattended public-action shortcuts, or
credential markers, the next agent should not inherit that context as trusted
fact.
