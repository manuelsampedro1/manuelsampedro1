# 2026-06-02 - Verify by Change Sensitive Paths

## Context

Generic file-extension verification is not enough for agent closeouts. A changed `.env`, private key fixture, approval handler, permission policy, receipt parser, guard, or deploy script needs different verification from an ordinary Python, shell, config, or docs edit.

`verify-by-change` already mapped changed paths to verification categories for docs, Python, Node CLI, Python CLI, GitHub Actions, GitHub workflows, review packets, and readiness context. The gap was path sensitivity: security and permission changes should ask for negative-path checks and leakage review before a confident closeout.

## Change

- Added `secret_material` classification for `.env` files, private key material, credential paths, token paths, and similar secret-bearing names.
- Added `security_sensitive` classification for authorization, approval, permission, receipt, guard, and deploy paths.
- Kept GitHub Action and workflow rules higher priority so workflow-specific guidance still wins for `.github/workflows/deploy.yml`.
- Added tests for secret paths, permission-sensitive paths, and rule precedence.
- Updated README examples and recorded the decision in `DECISIONS.md`.

Public commit: `9c26979b5331 feat: flag sensitive verification paths`.

## Verification

Local checks:

```sh
python3 -m unittest discover -s tests
make test
make build
make lint
python3 -m py_compile verify_by_change.py
git diff --check
python3 verify_by_change.py .env permission_protocol/client.py scripts/deploy.sh
node /Users/manuelsampedro/Documents/Codex/2026-05-21/repo-flightcheck/bin/repo-flightcheck.js . --strict --threshold 80
```

Results:

- `python3 -m unittest discover -s tests`: 37 tests passed.
- `make test`: 37 tests passed.
- `make build`: passed.
- `make lint`: passed.
- `python3 -m py_compile verify_by_change.py`: passed.
- `git diff --check`: passed.
- Sensitive-path smoke output produced `Secret Material` and `Security Sensitive` sections.
- `repo-flightcheck --strict --threshold 80`: `100/100` after commit.
- GitHub Actions run `26803556934` completed with conclusion `success`.

## Source Linkage

- Repo: <https://github.com/manuelsampedro1/verify-by-change>
- Commit: <https://github.com/manuelsampedro1/verify-by-change/commit/9c26979b5331a3a86b25fef1c5295ef07f3a9289>
- CI run: <https://github.com/manuelsampedro1/verify-by-change/actions/runs/26803556934>
- Scanner: <https://raw.githubusercontent.com/manuelsampedro1/verify-by-change/main/verify_by_change.py>
- Tests: <https://raw.githubusercontent.com/manuelsampedro1/verify-by-change/main/tests/test_verify_by_change.py>

## Takeaway

Agent verification should route by risk, not only by language. A deploy script, approval handler, or secret file should force negative-path and leakage checks even when the file extension looks routine.
