# CI Runs Local Verification

Use this when auditing whether a repo is ready for coding agents or external contributors.

## Goal

Make sure CI executes the same verification command that the repo advertises locally. A repo with tests and a workflow can still be weak if the workflow only builds, lints, or runs unrelated commands.

## Source Event

This recipe came from `repo-flightcheck` commit `a17a7149c56a`, which added the `CI verification` check.

Relevant files:

- `src/scan.js`
- `test/scan.test.js`
- `README.md`

## Workflow

1. Detect the local verification command from package scripts, Make targets, or stack conventions.
2. Detect workflow files under `.github/workflows`.
3. Build a small candidate set for equivalent commands.
4. For Node repos, include both the package-manager command and the underlying `package.json` test script.
5. Search workflow content for one of those candidates.
6. Report a pass with the matched workflow and command.
7. Warn when CI exists but does not appear to run verification.

## Checklist

- Does the repo expose one obvious local test or check command?
- Does CI exist?
- Does CI run that command or the underlying script it maps to?
- Does the report include file-level evidence for the match?
- Is a build-only workflow treated as insufficient verification?
- Does the rule stay heuristic and avoid pretending to parse every CI platform semantically?

## Verification

For a dependency-light Node CLI:

```sh
node --test
node scripts/lint.js
node scripts/build.js
node bin/repo-flightcheck.js . --json > /tmp/repo-flightcheck-report.json
node -e 'const fs=require("fs"); const r=JSON.parse(fs.readFileSync("/tmp/repo-flightcheck-report.json","utf8")); const check=r.checks.find(c=>c.id==="ci-verification"); if (!check || check.status !== "pass") process.exit(1);'
```

## Failure Modes

- Treating any workflow as proof that tests run.
- Matching only `npm test` and missing `node --test` from the actual script.
- Requiring exact YAML structure instead of a conservative text check.
- Giving a pass when CI only runs build or lint.
- Overclaiming: this proves command presence in workflow text, not that branch protection requires it.

## Source Linkage

- Public repo: <https://github.com/manuelsampedro1/repo-flightcheck>
- Commit: <https://github.com/manuelsampedro1/repo-flightcheck/commit/a17a7149c56a1b1fbc0845bb9a6722b5fe4800eb>
- CI run: <https://github.com/manuelsampedro1/repo-flightcheck/actions/runs/26793769368>
