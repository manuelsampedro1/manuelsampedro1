# 2026-06-02 - Codex Review Packet Sensitive Change Check

## Context

`codex-review-packet` already packaged diffs, repo rules, local context, review lanes, readiness reports, readiness contracts, generated verification, verification envelopes, and CI evidence.

The missing signal was a direct risk callout for paths that should not be reviewed like routine code. A packet that includes `.env`, approval logic, permission code, receipts, guards, deploy scripts, or release workflows should make those paths visible before the reviewer reads the full diff.

## Change

- Added a `## Sensitive Change Check` section to review packets when changed paths include secret material, authorization/approval behavior, or deploy/release paths.
- Grouped flagged paths under `Secret material`, `Authorization and approval`, and `Deploy or release path`.
- Routed secret and authorization paths into the security review lane without stealing workflow/deploy files from CI and release review.
- Added unit tests for sensitive path rendering, ordinary path omission, and working-tree packet output.
- Updated README examples and recorded the repo decision.

Public commit: `8a71e89eafbe feat: surface sensitive review paths`.

## Verification

Local checks:

```sh
python3 -m unittest discover -s tests
make test
make build
make lint
git diff --check
python3 codex_review_packet.py --repo /tmp/sensitive-review-packet-smoke --base HEAD~1 --output /tmp/sensitive-review-packet.md
grep -q '## Sensitive Change Check' /tmp/sensitive-review-packet.md
node /Users/manuelsampedro/Documents/Codex/2026-05-21/repo-flightcheck/bin/repo-flightcheck.js . --strict --threshold 80
```

Results:

- `python3 -m unittest discover -s tests`: 35 tests passed.
- `make test`: 35 tests passed.
- `make build`: passed.
- `make lint`: passed.
- `git diff --check`: passed.
- Smoke packet rendered `## Sensitive Change Check`, `### Secret material`, `### Authorization and approval`, and `### Deploy or release path`.
- `repo-flightcheck --strict --threshold 80`: `100/100` after commit.
- GitHub Actions run `26803873622` completed with conclusion `success`.

## Source Linkage

- Repo: <https://github.com/manuelsampedro1/codex-review-packet>
- Commit: <https://github.com/manuelsampedro1/codex-review-packet/commit/8a71e89eafbeb23a065fa47adb29f130c28ab32b>
- CI run: <https://github.com/manuelsampedro1/codex-review-packet/actions/runs/26803873622>
- Packet generator: <https://raw.githubusercontent.com/manuelsampedro1/codex-review-packet/main/codex_review_packet.py>
- Tests: <https://raw.githubusercontent.com/manuelsampedro1/codex-review-packet/main/tests/test_codex_review_packet.py>

## Takeaway

Review context should call out operational risk before it asks the reviewer to infer risk from filenames. Sensitive paths need explicit review routing because a green generic test run does not prove secrets, authorization, or deploy behavior is safe.
