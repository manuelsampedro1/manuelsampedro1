# Profile Curation Guard Proof Packet

Use this example when a profile is already strong enough that adding another
small proof repo may reduce clarity instead of improving the first read.

## Scenario

The profile has a broad public proof stack, current verification passes, and the
next maintenance question is whether to keep adding projects or pause for
curation.

## Evidence Commands

```sh
PYTHONPATH=/path/to/profile-proof-audit/src \
  python3 -m profile_proof_audit README.md --check-http --format json

node /path/to/repo-flightcheck/bin/repo-flightcheck.js \
  . --check-remote --strict --threshold 80

make test
make lint
make build
git status --short --branch
```

## Curation Signals

- `profile-proof-audit` returns `100/100` with no issues or warnings.
- `repo-flightcheck` returns `100/100` with a clean tree and published HEAD.
- Selected Work already has enough rows that another adjacent tool would make
  the profile harder to scan.
- The proposed next repo does not cover a materially new workflow gap.
- The stronger next action is hardening, combining, demonstrating, or curating
  the existing proof stack.

## Decision Rule

Do not publish another proof repo by default when all curation signals are true.

Accept a new repo only if it provides one of these:

- a new workflow category not already represented,
- a real cross-repo demonstration,
- a deeper implementation of an existing flagship repo,
- evidence from a real external user or review workflow.

## Review Prompt

```text
Review this profile update for saturation risk. If the profile already has
passing proof audits and a dense Selected Work table, prefer curation or
cross-repo demonstrations over another adjacent proof repo. Flag any proposed
addition that improves activity count more than first-read clarity.
```
