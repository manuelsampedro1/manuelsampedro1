# Fail-Fast Git Identity for Agent Publish Flows

Use this when a Codex, Claude Code, or scheduled automation can create commits, but the machine may not have a valid Git author identity yet.

## Use When

- The workflow can regenerate indexes, READMEs, or public artifacts before `git commit`.
- The repo is used across fresh clones, CI-like environments, or multiple Macs.
- A missing or wrong `git config user.name` or `git config user.email` would leave noisy file churn behind.
- You want the publish script to stop before mutating tracked files.

## Goal

Fail on Git identity preflight before running any generator or staging step.

In this repo, that means [`../scripts/commit_daily_update.sh`](../scripts/commit_daily_update.sh) should reject the run before calling:

- [`../scripts/update_lab_index.sh`](../scripts/update_lab_index.sh)
- [`../scripts/update_recipe_index.sh`](../scripts/update_recipe_index.sh)
- [`../scripts/update_radar_index.sh`](../scripts/update_radar_index.sh)
- [`../scripts/update_root_readme_latest.sh`](../scripts/update_root_readme_latest.sh)

## Inputs

- The real publish entrypoint under `scripts/`.
- One temp clone or isolated config environment.
- One small real artifact to prove the success path, such as a new lab note or recipe.
- One missing-identity setup for the failure path.

## Workflow

1. Read the publish entrypoint and find the first command that mutates tracked files.
2. Move the Git identity check above every generator, index refresh, or staging command.
3. Treat these as blocking conditions:
   - empty `git config user.name`,
   - empty `git config user.email`,
   - placeholder local-only email such as `*.local`.
4. Print the exact recovery commands instead of a generic error.
5. Verify the negative path in an isolated environment where Git identity is neutralized.
6. Verify the positive path with a valid local identity and one substantive artifact.
7. Inspect `git status --short` after the negative-path run and the final commit contents after the positive-path run.

## Isolation Pattern

Use an empty config environment so the test does not inherit your normal Git identity:

```bash
tmp="$(mktemp -d)"
git clone . "$tmp/repo"
mkdir -p "$tmp/home" "$tmp/xdg"

cd "$tmp/repo"
printf '# 2099-01-01 - Identity Test\n' > labs/2099/2099-01-01-identity-test.md

HOME="$tmp/home" XDG_CONFIG_HOME="$tmp/xdg" GIT_CONFIG_NOSYSTEM=1 \
  scripts/commit_daily_update.sh "test: missing identity"
```

Success condition for this negative path:

- the script exits with the identity guidance,
- tracked files such as `README.md` and `labs/README.md` stay unchanged.

Then verify the success path:

```bash
git config user.name "Test User"
git config user.email "test@example.com"
scripts/commit_daily_update.sh "test: valid identity"
git show --stat --name-only --oneline HEAD
```

## Agent Prompt Pattern

```text
Harden this publish flow against missing Git identity.

Inputs:
- publish entrypoint: <script path>
- generated files it may touch: <paths>

Tasks:
1. Find whether the script mutates tracked files before checking Git identity.
2. If yes, move the identity preflight above every mutating step.
3. Reject empty name, empty email, or obviously local-only email placeholders.
4. Print the exact recovery commands.
5. Verify one missing-identity run in an isolated config environment.
6. Verify one success run with a valid local identity and one real artifact.
7. Report only:
   - what changed,
   - what the negative path proved,
   - what the success path proved,
   - any remaining identity blind spots.

Rules:
- Do not trust global Git config during verification.
- Do not claim safety from stdout alone; inspect changed files too.
- Do not add commit or push logic before the identity gate.
```

## Fast Checklist

- Does the identity check happen before any `update_*` script or staged write?
- Does the failure path leave `README.md` and index files clean?
- Does the script print exact remediation commands?
- Did you test with identity truly neutralized, not just assumed missing?
- Did the success path still produce the expected commit?

## Evaluation Pattern

Score each item `0` or `1`:

- Preflight runs before any mutating command.
- Missing identity path was executed in isolation.
- Negative path left tracked generated files unchanged.
- Positive path still committed the intended artifact.
- Output tells the operator exactly how to recover.

`5`: publish the recipe or keep the script change.
`4`: publish if the remaining gap is minor and explicit.
`0-3`: rerun the negative path before claiming the flow is hardened.

## Failure Modes

- Checking identity after regenerating indexes.
- Verifying only on a machine that already has global Git config.
- Treating any non-empty email as valid enough for GitHub publishing.
- Reporting a clean failure path without checking the working tree afterward.
- Fixing the guard but skipping the positive-path regression check.

## Source Linkage

- Repo / tool / workflow: this profile repo's daily publish automation.
- Supporting prompt, script, or note: [`../labs/2026/2026-05-29-fail-fast-git-identity-for-agent-publish-flows.md`](../labs/2026/2026-05-29-fail-fast-git-identity-for-agent-publish-flows.md), [`../scripts/commit_daily_update.sh`](../scripts/commit_daily_update.sh), and [`./executable-runbook-drift-check.md`](./executable-runbook-drift-check.md).
