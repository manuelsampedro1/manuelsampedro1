# 2026-06-02 - Repo Flightcheck CI Verification

## Context

`repo-flightcheck` already detected whether a repo had a local verification command and whether it had GitHub Actions workflows. That was not strict enough. A repo can have both and still fail the practical question: does CI actually run the same check contributors and agents are expected to run locally?

That gap matters for coding-agent readiness. If local and CI verification drift, an agent can close with a passing local command while the public automation does something weaker or unrelated.

## Change

- Added a `CI verification` check.
- Compared workflow files against the detected local verification command.
- Included the underlying `package.json` test script as a candidate, so `npm test` and `node --test` can both be recognized.
- Added evidence showing the workflow file and matched command when CI covers verification.
- Added test coverage for healthy CI verification and CI that only runs build.
- Updated README checks and fixture output.

Public commit: `a17a7149c56a feat: check ci verification coverage`.

## Verification

Local checks:

```sh
node --test
node scripts/lint.js
node scripts/build.js
node bin/repo-flightcheck.js . --json > /tmp/repo-flightcheck-report.json
node -e 'const fs=require("fs"); const r=JSON.parse(fs.readFileSync("/tmp/repo-flightcheck-report.json","utf8")); const check=r.checks.find(c=>c.id==="ci-verification"); if (!check || check.status !== "pass") process.exit(1);'
node bin/repo-flightcheck.js . --strict --threshold 80
git diff --check
```

Results:

- `node --test`: 7 tests passed.
- Lint and build preflight passed.
- JSON scan included `ci-verification` with `status: "pass"`.
- Strict self-scan after commit reported `Score: 100/100`.
- Public commit page and raw changed files returned `200`.
- GitHub Actions run `26793769368` completed with conclusion `success`.

## Source Linkage

- Repo: <https://github.com/manuelsampedro1/repo-flightcheck>
- Commit: <https://github.com/manuelsampedro1/repo-flightcheck/commit/a17a7149c56a1b1fbc0845bb9a6722b5fe4800eb>
- CI run: <https://github.com/manuelsampedro1/repo-flightcheck/actions/runs/26793769368>
- Scanner: <https://raw.githubusercontent.com/manuelsampedro1/repo-flightcheck/a17a7149c56a1b1fbc0845bb9a6722b5fe4800eb/src/scan.js>
- Tests: <https://raw.githubusercontent.com/manuelsampedro1/repo-flightcheck/a17a7149c56a1b1fbc0845bb9a6722b5fe4800eb/test/scan.test.js>

## Takeaway

Readiness checks should not stop at "CI exists." For agent work, the stronger signal is that CI runs the same verification contract that local contributors and agents are told to run.
