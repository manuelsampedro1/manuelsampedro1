# Agent Dependency Guard

Use this when a coding-agent diff touches dependency manifests, lockfiles, or
install scripts.

## Source

- Public tool: https://github.com/manuelsampedro1/agent-dependency-guard
- Launch note: [2026-06-02 - Agent Dependency Guard Public Launch](../labs/2026/2026-06-02-agent-dependency-guard-public-launch.md)

## Pattern

1. Save the diff:

```sh
git diff origin/main -- . > /tmp/agent-change.diff
```

2. Run the dependency guard:

```sh
agent-dependency-guard /tmp/agent-change.diff --fail-on high
```

3. If the guard blocks, do not ask for a broader "looks fine" review. Ask for
the exact dependency evidence that is missing.

4. Record the output in the review packet, proof packet, or run ledger.

## What Good Looks Like

- Manifest and lockfile changes are visible.
- Runtime additions are separated from dev dependency changes.
- Floating specs and direct URLs are called out explicitly.
- Install lifecycle scripts are treated as high-signal review items.
- Missing lockfile updates are not hidden by a green test run.
- Required follow-up checks are listed before closeout.

## Prompt Pattern

```text
Review this coding-agent dependency change.

Rules:
- Do not claim a dependency is safe without external evidence.
- Classify only what is visible in the diff.
- Call out new runtime dependencies, floating specs, direct URL/path specs, install scripts, and missing lockfile changes.
- Require exact follow-up checks before merge.

<dependency guard output>
<diff>
<closeout>
```

## Pair With

- `agent-change-risk` to route the diff to the right gate,
- `agent-secret-sentinel` before publication,
- `agent-proof-packet` to preserve dependency evidence,
- `agent-merge-readiness` before merge,
- `agent-run-ledger` when the dependency decision needs an audit trail.

## Failure Mode

Do not treat `make test` as enough evidence for dependency changes. Tests can be
green while the diff adds a broad version range, external source, lifecycle
script, or stale lockfile.

