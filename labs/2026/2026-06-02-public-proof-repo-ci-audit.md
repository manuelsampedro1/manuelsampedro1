# 2026-06-02 - Public Proof Repo CI Audit

## Context

`repo-flightcheck` and `agent-run-ledger` are promoted in the profile as primary proof repos. After adding README CLI-output snippets, they needed a public-view audit and first GitHub Actions check so the profile claim stays backed by public evidence.

## Public Evidence

- `repo-flightcheck` is public at <https://github.com/manuelsampedro1/repo-flightcheck>.
- `agent-run-ledger` is public at <https://github.com/manuelsampedro1/agent-run-ledger>.
- `repo-flightcheck` GitHub Actions shows workflow run `26790637962` for commit `4005ba0` with status `completed` and conclusion `success`: <https://github.com/manuelsampedro1/repo-flightcheck/actions/runs/26790637962>.
- `agent-run-ledger` GitHub Actions shows workflow run `26790637961` for commit `c55ac7f` with status `completed` and conclusion `success`: <https://github.com/manuelsampedro1/agent-run-ledger/actions/runs/26790637961>.

## Local Verification Before Push

For `repo-flightcheck`:

```sh
node --test
node scripts/lint.js
node scripts/build.js
node bin/repo-flightcheck.js fixtures/sample-repo
```

For `agent-run-ledger`:

```sh
node --test
node scripts/lint.js
node scripts/build.js
node bin/agent-run-ledger.js doctor --ledger examples/sample-ledger.jsonl
node bin/agent-run-ledger.js report --ledger examples/sample-ledger.jsonl --out /tmp/agent-run-ledger-report.html
```

## Takeaway

The profile can keep these repos in `Selected Work`: both public proof repos now show runnable CLI output in their READMEs and have successful public CI on the latest documentation commits.
