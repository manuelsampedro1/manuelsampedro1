# Clean Working Tree Agent Preflight

Use this before handing a repository to Codex, Claude Code, or another coding agent.

## Goal

Separate the current task from pre-existing local work. A reviewer should be able to tell which changes came from the agent run and which changes were already present.

## Source Event

This recipe came from `repo-flightcheck` commit `5c76aecde3f9`, which added a `working-tree` readiness check for clean, dirty, and non-Git target directories.

Relevant files:

- `src/scan.js`
- `test/scan.test.js`
- `README.md`

## Workflow

1. Run a local Git status check before starting agent work.
2. Use porcelain output so staged, unstaged, and untracked paths are machine-readable.
3. Treat a clean Git working tree as ready.
4. Treat a dirty working tree as a warning unless the workflow explicitly allows carrying existing changes.
5. Include bounded evidence, such as the first few status lines, so the reviewer can see what is already present.
6. Warn when the target is not a Git repo instead of pretending cleanliness is known.
7. After committing the agent change, rerun the same check and expect it to pass.

## Checklist

- Did `git status --porcelain --untracked-files=all` run against the same repo the agent will edit?
- Are existing staged, unstaged, and untracked files documented before work starts?
- Does the final closeout distinguish pre-existing changes from agent-created changes?
- Did the post-commit scan return a clean working tree?
- Is the check represented in tests, not only in README prose?

## Verification

For a Node CLI, cover the rule with three fixtures:

```sh
node --test
node scripts/lint.js
node scripts/build.js
node bin/repo-flightcheck.js . --strict --threshold 80
```

The `repo-flightcheck` source change also has public CI success for the commit that introduced the rule.

## Failure Modes

- Running tests while ignoring unrelated dirty files already present in the repo.
- Letting untracked files silently enter a review packet or final summary.
- Treating non-Git directories as clean instead of unknown.
- Failing the whole scan when Git status is unavailable; a warning is usually more useful.
- Checking only unstaged changes and missing staged or untracked files.

## Source Linkage

- Public repo: <https://github.com/manuelsampedro1/repo-flightcheck>
- Commit: <https://github.com/manuelsampedro1/repo-flightcheck/commit/5c76aecde3f937c0ad12308dbaa74e83a2e9acea>
- CI run: <https://github.com/manuelsampedro1/repo-flightcheck/actions/runs/26792633038>
