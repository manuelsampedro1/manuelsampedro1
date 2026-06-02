# Agent Decision Guard

Use this when a coding-agent diff changes behavior that future maintainers need to understand.

## Use When

- The diff touches CI, automation scripts, deploy, release, config, auth, security, migrations, AGENTS.md, runbooks, prompts, templates, or product scope.
- The repo expects decisions to be recorded in `DECISIONS.md`.
- The repo expects concrete follow-ups to be recorded in `TODO.md`.
- A reviewer needs to know whether the agent updated documentation of intent, not only implementation.

## Goal

Fail fast when decision-worthy changes lack decision or follow-up documentation.

The guard should report:

- changed files,
- risk tags,
- whether `DECISIONS.md` changed,
- whether `TODO.md` changed,
- missing documentation,
- reviewer questions.

## Workflow

1. Capture the diff:

```sh
git diff -- . > /tmp/agent-change.diff
```

2. Run the guard:

```sh
PYTHONPATH=src python3 -m agent_decision_guard /tmp/agent-change.diff
```

3. If blocked, either:

- add the missing `DECISIONS.md` entry,
- add the missing `TODO.md` follow-up,
- or explicitly document why no persistent decision/follow-up is needed.

4. Re-run before commit.

## Prompt Pattern

```text
Check this coding-agent diff for decision documentation.

Rules:
- If the diff touches CI, scripts, deploy, config, security, database, product scope, AGENTS.md, runbooks, prompts, or templates, require a decision note.
- If the diff creates operational risk or future follow-up, require TODO coverage.
- Do not invent a decision. Ask for the actual rationale or block the merge.
- Report exact missing docs and reviewer questions.

<paste diff>
```

## Fast Checklist

- Did the diff change future agent behavior?
- Did it change CI, deploy, auth, data, or config behavior?
- Did `DECISIONS.md` capture the rationale?
- Did `TODO.md` capture concrete follow-up?
- Did the closeout mention why persistent docs changed or did not change?

## Failure Modes

- Making a real architecture decision only in chat.
- Updating CI or deploy behavior without a future-readable rationale.
- Adding a TODO without explaining the decision that created it.
- Treating docs updates as optional because tests pass.
- Letting agents repeatedly rediscover the same undocumented tradeoff.

## Source Linkage

- Repo / tool / workflow: [`agent-decision-guard`](https://github.com/manuelsampedro1/agent-decision-guard), public commit [`c7ac1bf`](https://github.com/manuelsampedro1/agent-decision-guard/commit/c7ac1bf2b9bb297a3c53bd5a5ba93aacd11ab2d4), [`README`](https://raw.githubusercontent.com/manuelsampedro1/agent-decision-guard/main/README.md), [`CLI`](https://raw.githubusercontent.com/manuelsampedro1/agent-decision-guard/main/src/agent_decision_guard/cli.py), [`tests`](https://raw.githubusercontent.com/manuelsampedro1/agent-decision-guard/main/tests/test_cli.py), [`blocking example`](https://raw.githubusercontent.com/manuelsampedro1/agent-decision-guard/main/examples/risky.diff), and [`waiver example`](https://raw.githubusercontent.com/manuelsampedro1/agent-decision-guard/main/examples/risky-with-waiver.diff).
- Supporting prompt, script, or note: [`./agents-md-patterns-for-codex-repos.md`](./agents-md-patterns-for-codex-repos.md), [`./runbook-drift-check.md`](./runbook-drift-check.md), [`./closeout-evidence-check-for-agents.md`](./closeout-evidence-check-for-agents.md), and [`../labs/2026/2026-06-02-agent-decision-guard-public-launch.md`](../labs/2026/2026-06-02-agent-decision-guard-public-launch.md).
