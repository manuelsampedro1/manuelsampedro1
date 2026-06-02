# 2026-06-02 - Verify by Change Action Safety

## Context

Hardening `deploy-gate` made a weakness in `verify-by-change` visible: `action.yml` and `.github/workflows/*.yml` are not ordinary config when they define an agent safety gate. They change how code is invoked, what permissions run, and whether a workflow can fail open.

Generic YAML guidance was too soft for that risk. The verification planner now gives GitHub Action and GitHub workflow files their own buckets before falling back to extension-based checks.

## Change

- Added path-specific classification for `action.yml`, `action.yaml`, and `.github/workflows/*.yml` or `.yaml`.
- Kept path rules ahead of extension rules so action metadata is not collapsed into generic YAML.
- Added tests for precedence, Windows-style paths, case normalization, and readable section headings.
- Updated README examples and decisions so action/workflow verification is part of the public contract.

Public commit: `95a009ba903 feat: add github action verification guidance`.

## Verification

Local checks:

```sh
make test
make build
make lint
python3 verify_by_change.py action.yml .github/workflows/deploy-gate.yml
python3 verify_by_change.py --json --envelope action.yml .github/workflows/deploy-gate.yml
python3 verify_by_change.py --repo . --fail-on-empty
repo-flightcheck --strict --threshold 80
git diff --check
```

Results:

- `make test`: 18 tests passed.
- `make build`: passed.
- `make lint`: passed.
- CLI smoke output included `Github Action` and `Github Workflow` sections.
- JSON envelope smoke returned `github_action` and `github_workflow` categories.
- Empty-diff guard returned the expected non-zero empty state after commit.
- `repo-flightcheck`: `100/100` after commit.
- Public commit page returned `200`.
- Raw `verify_by_change.py` returned `200`.
- GitHub Actions run `26797127705` completed with conclusion `success`.

## Source Linkage

- Repo: <https://github.com/manuelsampedro1/verify-by-change>
- Commit: <https://github.com/manuelsampedro1/verify-by-change/commit/95a009ba903c4a96ad660d3070444711d252d8d6>
- CI run: <https://github.com/manuelsampedro1/verify-by-change/actions/runs/26797127705>
- Tool: <https://raw.githubusercontent.com/manuelsampedro1/verify-by-change/main/verify_by_change.py>
- Tests: <https://raw.githubusercontent.com/manuelsampedro1/verify-by-change/main/tests/test_verify_by_change.py>

## Takeaway

Agent-facing verification should respect execution surfaces, not only file extensions. A workflow YAML file can change permissions, deploy behavior, or safety checks; a closeout tool should make that review lane visible before a human accepts the work.
