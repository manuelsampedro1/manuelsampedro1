# 2026-06-02 - Profile Proof Audit Public Launch

## Context

`profile-proof-audit` is the profile-quality gate for the agent workflow stack. A strong README can still overclaim, link to missing files, promote local-only repos, or bury stale latest-proof sections; the audit makes those failures repeatable instead of subjective.

The local repo needed agent instructions, Make targets, explicit `.env` hygiene, README command alignment, CI/local command parity, and removal of generated package metadata before it could stand as public proof.

## Useful Artifact

`profile-proof-audit` is now public as a dependency-free Python CLI that audits a GitHub profile README for:

- required sections,
- Selected Work table shape,
- Latest Proof entries,
- relative Markdown links,
- optional public HTTP status,
- risky unsupported phrasing,
- score, issues, and warnings.

It does not edit the profile, hide broken proof, create GitHub repos, or store credentials. The output is meant to make claim quality reviewable.

## Source Linkage

- Public repo: <https://github.com/manuelsampedro1/profile-proof-audit>
- Commit: <https://github.com/manuelsampedro1/profile-proof-audit/commit/ab7c8ae741a755c06e92f8f39145784c4627232a>
- README: <https://raw.githubusercontent.com/manuelsampedro1/profile-proof-audit/main/README.md>
- CLI: <https://raw.githubusercontent.com/manuelsampedro1/profile-proof-audit/main/src/profile_proof_audit/cli.py>
- Tests: <https://raw.githubusercontent.com/manuelsampedro1/profile-proof-audit/main/tests/test_cli.py>
- Example profile: <https://raw.githubusercontent.com/manuelsampedro1/profile-proof-audit/main/examples/profile.md>
- CI badge: <https://github.com/manuelsampedro1/profile-proof-audit/actions/workflows/ci.yml/badge.svg?branch=main>
- Recipe: [`../../recipes/profile-proof-audit.md`](../../recipes/profile-proof-audit.md)

## Verification

Local checks:

```sh
make test
make lint
make build
make smoke
git diff --check
node /path/to/repo-flightcheck/bin/repo-flightcheck.js . --check-remote --strict --threshold 80
```

Results:

- `make test`: 5 tests passed.
- `make lint`: compile check passed.
- `make build`: compile check passed.
- `make smoke`: rendered Markdown and JSON profile audit outputs; the example profile scored `100/100`.
- `repo-flightcheck --check-remote --strict --threshold 80`: `100/100`.
- Public repo, commit, README, CLI source, tests, and example profile raw URLs returned `200`.
- Public CI badge reports `CI - passing`.

## Takeaway

Profile quality should be auditable. `profile-proof-audit` gives the public surface the same evidence discipline as the tools it promotes.
