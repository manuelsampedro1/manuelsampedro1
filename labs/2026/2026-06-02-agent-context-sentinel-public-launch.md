# 2026-06-02 - Agent Context Sentinel Public Launch

## Source

- Public repo: https://github.com/manuelsampedro1/agent-context-sentinel
- Published HEAD: `9c2324b10df731fcbbfc405caaedc85cddbdf2e4`
- CI run: https://github.com/manuelsampedro1/agent-context-sentinel/actions/runs/26834647206

## What Changed

Built and published `agent-context-sentinel`, a dependency-free Python CLI for
auditing context files before they are passed into a coding-agent handoff.

The tool reports:

- prompt-injection phrases that try to ignore, override, or bypass higher
  priority instructions,
- hidden, secret, system, developer, admin, or root authority claims,
- requests to dump, print, send, upload, or expose secrets, `.env`, SSH keys,
  tokens, credentials, or environment variables,
- dangerous shell and Git patterns such as `rm -rf`, `git reset --hard`, force
  pushes, skipped hooks, privileged commands, and `curl | bash`,
- public or sensitive actions such as publishing, sending, deploying, deleting,
  charging, refunding, committing, pushing, or releasing without human approval,
- secret-material markers with redacted evidence,
- absolute local paths and missing source metadata when source metadata is
  required.

## Why It Matters

Agent reliability is not only about the final diff. The input context can carry
instructions that should be quoted, summarized, or excluded instead of treated
as authority.

`agent-context-sentinel` adds a pre-handoff gate for untrusted context from
tickets, chats, docs, webpages, or previous run notes. It does not claim to
solve prompt injection completely. It makes risky context visible before the
next agent sees it as part of the task.

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
- GitHub Actions run `26834647206` completed with `success`.

## Takeaway

Treat retrieved or user-provided context as data until it is screened. If it
contains override language, hidden authority claims, secret exfiltration
requests, dangerous commands, or unattended action shortcuts, do not pass it to
the next agent as trusted instructions.
