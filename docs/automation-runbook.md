# Automation Runbook

This repo is designed for daily useful GitHub contributions around AI tooling and coding-agent work.

## Daily Streams

- 09:05 Madrid, `GitHub AI Lab Note`: create or improve one technical note under `labs/`.
- 14:10 Madrid, `GitHub AI Recipe`: add one reusable workflow, prompt, checklist, or implementation pattern under `recipes/`.
- 20:20 Madrid, `GitHub Profile Maintenance`: refresh public indexes, update README links or TODO status when they materially change, and commit/push any useful changes.

## Intensity Target

Default target: produce two substantive public artifacts per day across the lab and recipe streams, then use maintenance to tighten discoverability or backlog only when something genuinely improved.

Prefer:

- one artifact from a real Codex workflow, bug, review, or repo automation run,
- one supporting artifact that turns that work into a reusable prompt, checklist, or pattern,
- small follow-up maintenance only after the artifact work is done.

Do not chase volume with generic notes. More intense means more concrete, more reusable, and closer to actual Codex work.

## Codex Focus

Bias daily output toward artifacts that help with work done inside Codex:

- repo review workflows and findings patterns,
- debugging loops and failure-mode notes,
- prompt patterns for scoped edits, planning, and verification,
- agent memory, automation, and runbook patterns,
- AGENTS.md structures, guardrails, and repo setup decisions,
- small scripts or templates that reduce friction in repeat tasks.

## Quality Guard

- Monday 10:15 Madrid, `GitHub Profile Quality Audit`: review recent automated contributions and flag or fix drift toward generic filler.

## Commit Rule

No empty commits. No timestamp-only changes. No filler.

The scripts should commit only when files changed and should push only when a remote is configured.

Current maintenance refreshes:

- `labs/README.md`
- `recipes/README.md`
- `radar/README.md`
- root `README.md` latest links when a newer public artifact exists
- `TODO.md` when a review checkpoint or next step genuinely changes

## GitHub Setup

Remote publishing is configured for `manuelsampedro1/manuelsampedro1`.

Current remote:

```sh
git remote -v
```

Current Git identity:

```sh
git config user.name
git config user.email
```

Expected values:

```sh
Manuel Sampedro
202281585+manuelsampedro1@users.noreply.github.com
```

Manual push if an automation leaves local commits behind:

```sh
git push
```

If GitHub authentication expires, sign in again in the browser or configure GitHub CLI. Do not put tokens in this repo.

## Automation Safety

Automations can prepare, commit, and push useful public artifacts. They should not:

- invent credentials,
- commit secrets,
- create fake contributions,
- publish private notes,
- claim tool results that were not verified.
