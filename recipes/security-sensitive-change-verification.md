# Security-Sensitive Change Verification

Use this when a Codex run changes secrets, credentials, authorization logic, approval flows, receipts, policies, guards, or deploy paths.

## Goal

Route security-sensitive changes to negative-path and leakage checks instead of treating them like generic Python, shell, config, or docs edits.

## Source Event

This recipe came from adding `secret_material` and `security_sensitive` categories to `verify-by-change`.

The public change makes the CLI classify `.env`, private-key, credential, token, approval, permission, receipt, guard, and deploy paths before generic extension rules, while keeping GitHub Action and workflow guidance higher priority.

## Workflow

1. Identify whether any changed path contains secret material or permission-sensitive behavior.
2. If secret material changed, inspect the diff for real credentials, tokens, webhook URLs, or production identifiers.
3. If a real secret was committed, rotate it before treating the run as safe.
4. For authorization or approval changes, run tests for allow, deny, expired, missing, malformed, and failure paths.
5. Exercise at least one negative path manually or through a targeted test.
6. Review logs, errors, receipts, and artifacts for accidental secret or approval-payload leakage.
7. Keep CI workflow checks separate; a green YAML check does not prove permission behavior is safe.

## Checklist

- Did any changed path include `.env`, key material, credentials, tokens, approvals, permissions, receipts, guards, or deploy code?
- Did the closeout mention negative-path verification, not only happy-path execution?
- Were denial, expiry, malformed input, and missing-approval cases covered where relevant?
- Were logs and generated artifacts checked for sensitive payload leakage?
- If secret material appeared, was rotation/removal handled before publication?

## Verification

```sh
python3 verify_by_change.py .env permission_protocol/client.py scripts/deploy.sh
python3 -m unittest discover -s tests
git diff --check
```

## Failure Modes

- Treating `scripts/deploy.sh` as ordinary shell syntax only.
- Treating `permission_protocol/client.py` as ordinary Python without denial or timeout tests.
- Publishing a fixture private key without checking whether it is clearly fake and scoped to tests.
- Letting CI pass while generated receipts or logs expose approval payloads.
- Saying "tests passed" when only the successful authorization path was exercised.

## Source Linkage

- Public repo: <https://github.com/manuelsampedro1/verify-by-change>
- Commit: <https://github.com/manuelsampedro1/verify-by-change/commit/9c26979b5331a3a86b25fef1c5295ef07f3a9289>
- CI run: <https://github.com/manuelsampedro1/verify-by-change/actions/runs/26803556934>
- Lab note: <../labs/2026/2026-06-02-verify-by-change-sensitive-paths.md>
