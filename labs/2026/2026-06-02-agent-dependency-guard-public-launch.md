# 2026-06-02 - Agent Dependency Guard Public Launch

## Source

- Public repo: https://github.com/manuelsampedro1/agent-dependency-guard
- Published HEAD: `230220b4387130934605451f1776722f2c4685c6`
- CI run: https://github.com/manuelsampedro1/agent-dependency-guard/actions/runs/26831896104

## What Changed

Built and published `agent-dependency-guard`, a dependency-free Python CLI that
classifies dependency-surface changes in coding-agent diffs.

The tool reports:

- changed dependency manifests and lockfiles,
- added, removed, and changed direct dependencies,
- runtime versus development dependency groups when visible,
- floating specs such as `latest`, `*`, `^`, `~`, and range operators,
- direct external sources such as `https`, `git+`, `github:`, and `file:`,
- Node install lifecycle scripts such as `postinstall` and `prepare`,
- manifest changes without a matching lockfile change,
- Markdown or JSON output for CI gates and proof packets.

## Why It Matters

Tests can pass while a dependency change silently increases supply-chain risk.
This is especially easy in agent-generated diffs because the agent may add a
library to solve a narrow problem without explaining lockfile, install-script,
or source-spec implications.

`agent-dependency-guard` does not claim vulnerability intelligence. It provides
a deterministic pre-review gate: if the dependency surface changed, reviewers
see the exact files, specs, scripts, severity, and follow-up checks.

## Verification

Ran locally:

```sh
make test
make lint
make build
make smoke
git diff --check
```

Additional checks:

- editable install in a temporary virtualenv after upgrading `pip`, `setuptools`, and `wheel`,
- `agent-instruction-audit AGENTS.md --min-score 80` at `100/100`,
- `repo-flightcheck . --check-remote --strict --threshold 80` at `100/100`,
- public repo and raw README/source/test/example URLs returned `200`,
- GitHub Actions run `26831896104` completed with `success`.

## Takeaway

Dependency changes deserve a separate gate. A reviewer should not have to infer
from a generic diff summary whether a new runtime package, direct URL, install
script, or missing lockfile changed the trust boundary.

