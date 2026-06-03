# 2026-06-03 - Agent Artifact Redactor Manifests

## What Changed

Added hash-backed redaction manifests to
[`agent-artifact-redactor`](https://github.com/manuelsampedro1/agent-artifact-redactor).

The CLI can now write redacted artifact copies and a manifest in one run:

```sh
agent-artifact-redactor examples/raw-artifact.txt \
  --write-dir /tmp/redacted \
  --manifest /tmp/redacted/manifest.json
```

The manifest records the schema version, tool version, source SHA-256,
redacted SHA-256, redacted output path, finding counts, replacement counts,
rule names, and severity counts.

## Why It Matters

Public agent proof needs two properties that can conflict:

- reviewers need enough evidence to trust that a risky artifact was processed;
- public notes should not expose the original transcript, log, packet, token,
  local path, or contact detail.

The manifest bridges that gap. It lets a reviewer connect a redacted copy to a
specific local source hash without publishing the source artifact itself.

## Verification Evidence

- Added `--manifest` and required it to be paired with `--write-dir`.
- Added source and redacted SHA-256 values to file summaries.
- Added a stable `agent-artifact-redactor.manifest.v1` JSON shape.
- Added tests for JSON hash output, manifest writing, sensitive-value omission,
  and the `--manifest`/`--write-dir` contract.
- Updated the smoke test to prove redacted copy and manifest creation.
- Verified the public repo with tests, lint, build, smoke, whitespace checks,
  local Git identity audit, raw GitHub source URLs, `repo-flightcheck` at
  `100/100`, and GitHub Actions success for commit
  `3b3b70d01e98787f38e536dc3a7e5e07f86dd1c2` in run `26868672750`.

## Reusable Lesson

Redaction is stronger when it leaves a receipt. If an artifact is too sensitive
to publish raw, publish the redacted copy plus a manifest that makes the
processing step reviewable.
