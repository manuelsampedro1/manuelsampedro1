# Python Unittest Readiness Check

Use this when a Python repo intentionally uses only the standard library but still needs an executable verification contract for Codex, Claude Code, or human review.

## Goal

Make a dependency-free Python repo look ready because it is ready: tests are discoverable, documented commands are executable, and CI runs the same command.

## Source Event

This recipe came from `repo-flightcheck` commit `a024b678cd70`, which added Python `unittest` detection for standard-library repos.

Relevant files:

- `src/scan.js`
- `test/scan.test.js`
- `README.md`

## Workflow

1. Put unit tests under `tests/`.
2. Name test files with the default unittest discovery pattern, such as `test_cli.py`.
3. Document the exact command in `README.md` and `AGENTS.md`.
4. Run the same command in CI.
5. Scan the repo with `repo-flightcheck`.
6. Treat any documented-command warning as a docs or script drift bug.

## Recommended Command

```sh
python3 -m unittest discover -s tests
```

For local docs that prefer `python` instead of `python3`, keep CI explicit:

```yaml
- run: python3 -m unittest discover -s tests
```

## Checklist

- Does `tests/` exist?
- Does it contain files matching `test*.py`?
- Does README or `AGENTS.md` document the same command contributors should run?
- Does GitHub Actions run the same command?
- Does the repo avoid claiming a third-party test runner if it does not use one?

## Verification

For a repo scanned by `repo-flightcheck`:

```sh
node /path/to/repo-flightcheck/bin/repo-flightcheck.js /path/to/python-repo --json > /tmp/readiness.json
node -e 'const fs=require("fs"); const r=JSON.parse(fs.readFileSync("/tmp/readiness.json","utf8")); for (const id of ["verification-command","ci-verification","documented-commands"]) { const c=r.checks.find(x=>x.id===id); if (!c || c.status !== "pass") { console.error(id, c && c.message); process.exit(1); }}'
```

## Failure Modes

- Tests live under `tests/` but files are named outside the default discovery pattern.
- README says `python3 -m unittest discover -s missing`, but that directory does not exist.
- CI runs only import or compile checks while README tells agents to run unit tests.
- A repo adds a third-party runner later but leaves old unittest commands in docs.

## Source Linkage

- Public repo: <https://github.com/manuelsampedro1/repo-flightcheck>
- Commit: <https://github.com/manuelsampedro1/repo-flightcheck/commit/a024b678cd700de084555d754920e8b82b8025df>
- CI run: <https://github.com/manuelsampedro1/repo-flightcheck/actions/runs/26795493554>
