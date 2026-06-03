# 2026-06-03 - Profile Proof Audit CI Thresholds

## What Changed

Added strict gate options to
[`profile-proof-audit`](https://github.com/manuelsampedro1/profile-proof-audit):

- `--min-score` exits non-zero when the profile proof score is too low.
- `--fail-on-warnings` exits non-zero when the audit still has warnings.

The default CLI remains informational and exits `0` after rendering a report.
That keeps local review friendly while allowing CI to opt into a hard gate.

## Why It Matters

A profile audit has two different jobs:

- explain proof quality to a human reviewer,
- fail automation when public profile proof falls below an agreed bar.

Mixing those modes makes the tool less useful. Default failure on every issue
can be noisy during drafting, while report-only behavior is too weak for CI.
Explicit thresholds make the contract visible at the call site.

## Verification Evidence

- Added CLI tests proving default informational exit, low-score failure, and
  warning failure.
- Updated the smoke target to exercise the strict path with `--min-score 100`
  and `--fail-on-warnings`.
- Verified the public repo with tests, lint, build, smoke, whitespace checks,
  `repo-flightcheck` at `100/100`, raw GitHub source URLs, and GitHub Actions
  success for commit `85970be`.

## Reusable Lesson

Keep audit tools readable by default, then make CI strict through explicit flags.
The reviewer should see the report; automation should decide whether the report
is acceptable.
