# Agent Release Readiness Chain

Use this example when a coding agent prepares release notes, CI changes, auth
changes, dependency updates, or tests and the reviewer needs a stricter answer
than "the release note looks good."

## Scenario

A release diff touches:

- auth/session code,
- `requirements.txt`,
- a GitHub Actions workflow,
- tests for the changed auth behavior.

The release note may be accurate, but the change still needs risk routing,
scope evidence, release-note coverage, merge readiness, and one reviewable proof
packet.

## Command Chain

```sh
PYTHONPATH=/path/to/agent-change-risk/src \
  python3 -m agent_change_risk /path/to/sample.diff \
  --title "Session release readiness" \
  --format json

PYTHONPATH=/path/to/agent-release-note-check/src \
  python3 -m agent_release_note_check /path/to/release-notes.md \
  --diff /path/to/sample.diff \
  --format json \
  --min-score 80

PYTHONPATH=/path/to/agent-merge-readiness/src \
  python3 -m agent_merge_readiness /path/to/sample.diff \
  --title "Session release readiness" \
  --check "change risk:pass" \
  --check "release note check:pass" \
  --check "unit tests:pass" \
  --check "secret scan:pass" \
  --check "runbook drift:pass" \
  --check "rollback plan:pass" \
  --closeout /path/to/closeout.md \
  --format json

PYTHONPATH=/path/to/agent-proof-packet/src \
  python3 -m agent_proof_packet /path/to/sample.diff \
  --title "Session release readiness" \
  --check "change risk:pass" \
  --check "release note check:pass" \
  --check "unit tests:pass" \
  --risk "Auth, dependency, CI, and test changes require release-note and rollback review." \
  --decision "Package release readiness evidence before publishing." \
  --evidence "release notes:/path/to/release-notes.md" \
  --format json
```

## Observed Signals From The Fixture

- `agent-change-risk` classified the diff as `high` risk with `ci`, `python`,
  `security`, and `tests` tags.
- `agent-release-note-check` returned `pass` at `100/100` with no findings.
- `agent-merge-readiness` still returned `needs-review` because scope evidence
  was missing and the closeout did not state residual risks.
- `agent-proof-packet` returned `complete` once release-note evidence was
  attached.

## Reviewer Interpretation

Do not treat a complete proof packet as the same thing as merge readiness.

The proof packet packages what exists. The merge-readiness gate decides whether
the evidence is sufficient. In this fixture, release-note coverage is good, but
the reviewer should still ask for:

- declared scope evidence,
- explicit risk or limitation language in the closeout,
- rollback evidence if the release can affect auth, CI, or dependencies.

## Review Prompt

```text
Review this release handoff as an evidence chain. Confirm the release note
covers the diff, then check whether merge readiness still requires scope,
rollback, secret-scan, or residual-risk evidence. Do not accept a complete proof
packet as a merge-ready verdict unless the merge-readiness gate is also ready.
```
