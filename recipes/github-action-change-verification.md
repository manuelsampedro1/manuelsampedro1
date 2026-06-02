# GitHub Action Change Verification

Use this when a Codex change touches `action.yml`, `action.yaml`, or files under `.github/workflows/`.

## Goal

Treat action metadata and workflow YAML as execution surfaces, not generic configuration.

## Source Event

This recipe came from adding GitHub Action and GitHub workflow categories to `verify-by-change` after hardening `deploy-gate`.

The public change makes `verify-by-change` emit `github_action` and `github_workflow` guidance before extension-based YAML checks.

## Workflow

1. Classify `action.yml` and `action.yaml` as the action contract.
2. Classify `.github/workflows/*.yml` and `.github/workflows/*.yaml` as workflow execution plans.
3. Review action inputs, outputs, defaults, shell steps, and failure behavior.
4. Review workflow triggers, permissions, secrets usage, matrix coverage, and invoked local commands.
5. Run local tests or validators that inspect the action/workflow files directly.
6. Run the same commands the workflow invokes when they are safe offline.
7. Keep live deploys, production credentials, and token-dependent checks out of the smoke path.
8. Report what was verified, what was only syntax-checked, and what still requires a live environment.

## Checklist

- Does the action fail closed for safety-critical decisions?
- Did any input, output, or default change in a way callers must know about?
- Are workflow permissions minimal for the job?
- Are secrets referenced by name only, with no sample token values committed?
- Do workflow commands match local `make test`, `make build`, or `make lint` targets?
- Is the changed workflow triggered only on the intended events?
- Does the verification cover both the action contract and the workflow that calls it?

## Verification

```sh
make test
make build
make lint
python3 verify_by_change.py action.yml .github/workflows/example.yml
python3 verify_by_change.py --json --envelope action.yml .github/workflows/example.yml
git diff --check
```

## Failure Modes

- Treating workflow YAML as docs because it is not application code.
- Syntax-checking the file but ignoring permissions, triggers, and secrets.
- Changing `action.yml` inputs without updating examples or tests.
- Claiming deployment behavior was verified when only offline validation ran.
- Letting a safety gate fail open when an approval or receipt is missing.

## Source Linkage

- Public repo: <https://github.com/manuelsampedro1/verify-by-change>
- Commit: <https://github.com/manuelsampedro1/verify-by-change/commit/95a009ba903c4a96ad660d3070444711d252d8d6>
- CI run: <https://github.com/manuelsampedro1/verify-by-change/actions/runs/26797127705>
- Lab note: <../labs/2026/2026-06-02-verify-by-change-action-safety.md>
