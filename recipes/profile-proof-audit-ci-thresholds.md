# Profile Proof Audit CI Thresholds

Use this pattern when a profile or proof README needs both a human-readable
audit report and a hard automation gate.

## Problem

Report-only audits are useful during review but weak in CI:

- a low score can still return success,
- warnings can accumulate without breaking a release,
- maintainers need to remember the quality bar outside the command.

Fail-fast audits have the opposite problem during drafting:

- every incomplete section can interrupt exploration,
- local review becomes less convenient,
- the command hides the difference between "show me the report" and "gate this
  release."

## Pattern

Keep the default command informational:

```sh
PYTHONPATH=src python3 -m profile_proof_audit README.md --check-http
```

Use explicit flags when CI or release work should fail below the public bar:

```sh
PYTHONPATH=src python3 -m profile_proof_audit README.md \
  --check-http \
  --min-score 100 \
  --fail-on-warnings
```

## Acceptance Criteria

- The default command exits `0` after rendering the report.
- `--min-score N` exits non-zero when the score is below `N`.
- `--fail-on-warnings` exits non-zero when warnings are present.
- Smoke tests exercise the strict path, not only the report path.
- README usage explains the difference between informational and gate modes.

## Review Rule

If the command is used to protect a public profile surface, make the threshold
visible in the CI command. Do not rely on maintainers remembering the score that
counts as acceptable.
