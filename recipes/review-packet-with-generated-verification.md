# Review Packet With Generated Verification

Use this when a Codex review handoff needs repo context, changed files, readiness risks, and a verification plan in one Markdown artifact.

## Goal

Avoid sending a reviewer a diff plus vague "run tests" advice. Generate a packet that includes the repo map and the change-aware checks a human should expect.

## Source Event

This recipe came from adding `--verify-by-change` to `codex-review-packet`.

The public change lets `codex-review-packet` invoke a local `verify-by-change` executable or `.py` script and embed the generated checklist without adding a runtime dependency.

## Workflow

1. Start from the repo that needs review and make sure the intended diff is present.
2. Generate a repo readiness report if setup quality is relevant.
3. Generate the packet with `--verify-by-change` so the checklist matches the same repo scope.
4. Use `--staged` when the review should only cover the index.
5. Use `--base origin/main` when the review should cover committed branch work.
6. Add `--diff-lines` if the diff is too large for the model context, and keep the omission marker.
7. Reject packets that mix `--verification-checklist` and `--verify-by-change`; one verification source is clearer.

## Example

```sh
node /path/to/repo-flightcheck/bin/repo-flightcheck.js /path/to/repo --json > /tmp/repo-readiness.json
python3 /path/to/codex-review-packet/codex_review_packet.py \
  --repo /path/to/repo \
  --readiness-report /tmp/repo-readiness.json \
  --verify-by-change /path/to/verify-by-change/verify_by_change.py \
  --output /tmp/review-packet.md
```

## Checklist

- Does the packet list the same changed files the reviewer is expected to inspect?
- Does the review map route files into CI, security, docs, tests, application, or agent-instruction lanes?
- Does the readiness report show repo setup risks before the diff?
- Does the verification section come from the same repo/base/staged scope as the packet?
- Does the final handoff report any capped diff lines or omitted checklist lines?

## Failure Modes

- Generating a verification checklist for the working tree while the packet reviews staged changes.
- Pasting a stale checklist generated before the diff changed.
- Adding a shell-based generator command that makes quoting or injection behavior unclear.
- Treating a generated checklist as proof that checks were run.

## Source Linkage

- Public repo: <https://github.com/manuelsampedro1/codex-review-packet>
- Commit: <https://github.com/manuelsampedro1/codex-review-packet/commit/60296f3ddc4b3dbc179bcbfd61cec8dd247c4aeb>
- CI run: <https://github.com/manuelsampedro1/codex-review-packet/actions/runs/26797488725>
- Lab note: <../labs/2026/2026-06-02-codex-review-packet-generated-verification.md>
