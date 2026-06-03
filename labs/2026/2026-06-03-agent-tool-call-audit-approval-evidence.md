# 2026-06-03 - Agent Tool Call Audit Approval Evidence

## What Changed

Added approval-evidence gating to
[`agent-tool-call-audit`](https://github.com/manuelsampedro1/agent-tool-call-audit).

The CLI can now run in a stricter mode:

```sh
agent-tool-call-audit examples/tool-calls.jsonl --require-approval --fail-on high
```

When enabled, sensitive tool calls and external action commands such as
`git push`, package publishing, release creation, or deploy commands need
explicit approval or receipt evidence in the tool log.

## Why It Matters

Post-run audits should not only ask whether a command was dangerous. They
should also ask whether a sensitive external action had the right authority
evidence attached at the time it appeared in the run history.

This helps separate:

- ordinary local verification commands;
- sensitive tools that deserve reviewer attention;
- sensitive tools or external action commands that lack approval evidence;
- sensitive actions that still need review but carry a receipt or approval
  marker.

## Verification Evidence

- Added `--require-approval` as an opt-in CLI gate.
- Added approval-required and approval-evidence counters to Markdown and JSON.
- Added recognition for approval/permission/authorization receipt fields,
  `approved_by`, `authorized_by`, `human_approved: true`, and `approved: true`.
- Added external action command detection for `git push`, package publishing,
  release creation, and common deploy commands.
- Added regression tests for missing approval, accepted receipt evidence,
  external action commands, and JSON output.
- Verified the public repo with tests, lint, build, smoke, whitespace checks,
  local Git identity audit, raw GitHub source URLs, `repo-flightcheck` at
  `100/100`, and GitHub Actions success for commit
  `6f2d3fa808af36814fe556f70902c1ecc0c1ab37` in run `26869242363`.

## Reusable Lesson

Tool-call history is stronger when sensitive actions carry authority evidence.
A post-run audit should make missing approval explicit instead of relying on a
final answer to describe what happened.
