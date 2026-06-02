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

## Artifact Linkage

Every new public note or recipe should declare what real work it came from.

Accepted anchors:

- a public repo URL,
- a concrete local script or tool path,
- a specific lab note or decision file,
- a real workflow prompt or verification command,
- a shipped case or working demo.

If a draft cannot point to one of those anchors, do not publish it yet.

## Promotion Eligibility

An artifact can be promoted to the root `README.md` or the `Selected Work` surface only if all of these are true:

- it links to owned proof such as a public repo, working tool, or verified case,
- it includes a real verification section,
- it would still be useful if separated from the profile repo,
- it supports the client-facing story more than a more concrete repo would.

## Quality Guard

- Monday 10:15 Madrid, `GitHub Profile Quality Audit`: review recent automated contributions and flag or fix drift toward generic filler.

The audit should also check:

- too much meta-content versus repo-backed proof,
- artifacts that do not link back to real work,
- weak README promotions,
- drift away from the client-facing narrative.
- first-read quality with `python3 scripts/profile_quality_audit.py --root . --min-score 100`.
- Canonical README section order so reviewer navigation, selected proof, and safety proof stay before the longer workflow archive.
- Indexed `Latest Proof` targets so root README highlights stay discoverable from the public lab, recipe, or radar indexes.
- Reviewer Path length staying at four bullets or fewer, with extra routes moved to examples instead of the first-read README section.
- Unique `Selected Work` repo targets so repeated links cannot inflate the proof surface.
- Owned `Selected Work` repo targets under `https://github.com/manuelsampedro1/`; external links belong in notes, recipes, or radar, not the primary proof table.
- Matching `Selected Work` labels and repo slugs so visible repo names cannot point to a different target.
- Owned, unique, and correctly labelled `Agent Safety Layer` repo targets so the permission and safety surface cannot drift into external references or inflated proof.

## Commit Rule

No empty commits. No timestamp-only changes. No filler.

The scripts should commit only when files changed and should push only when a remote is configured.

Current maintenance refreshes:

- `labs/README.md`
- `recipes/README.md`
- `radar/README.md`
- root `README.md` latest links when a newer public artifact exists
- `TODO.md` when a review checkpoint or next step genuinely changes
- `examples/` when a concrete proof packet or fixture helps verify public claims

The maintenance script should skip a run when the diff only touches those surface files.

Changes under `scripts/` are eligible for a maintenance commit when they improve artifact generation, publishing safety, or verification quality.

Changes under `tests/` are eligible when they prove a public verification gate catches both passing and failing profile states.

Before refreshing indexes or staging files, `scripts/commit_daily_update.sh` now checks managed public paths for pre-existing changes.

Pass the exact intended changed paths after the commit message so the run can distinguish the real artifact from unrelated draft work:

```sh
scripts/commit_daily_update.sh \
  "maintenance: tighten publish guard" \
  scripts/commit_daily_update.sh \
  docs/automation-runbook.md \
  DECISIONS.md \
  TODO.md
```

If the script reports unexpected public-path changes, narrow the run or move the unrelated draft work before retrying.

After a publish run, the script warns when uncommitted local changes remain so scratch files do not silently carry into the next automation run.

Audit the local GitHub automation prompts after changing them:

```sh
python3 scripts/audit_github_automation_prompts.py --format json
```

The audit expects the lab, recipe, maintenance, and quality-audit prompts to pass exact changed paths after the `scripts/commit_daily_update.sh` commit message.

Audit local proof-repo Git identity before first public pushes:

```sh
python3 scripts/audit_local_repo_identity.py --root .. --format json
```

The expected identity is `Manuel Sampedro` with `202281585+manuelsampedro1@users.noreply.github.com`.

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

If GitHub SSH authentication fails with `Permission denied (publickey)`, check whether the Codex GitHub key is loaded:

```sh
ssh-add -l
ssh-add ~/.ssh/id_ed25519_github_codex
ssh -T git@github.com
```

If GitHub browser authentication expires, sign in again in the browser or configure GitHub CLI. Do not put tokens in this repo.

## Automation Safety

Automations can prepare, commit, and push useful public artifacts. They should not:

- invent credentials,
- commit secrets,
- create fake contributions,
- publish private notes,
- claim tool results that were not verified.
