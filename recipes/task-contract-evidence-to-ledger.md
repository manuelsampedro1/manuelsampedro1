# Task Contract Evidence to Ledger

Use this when a review packet includes a task contract and the agent run needs a durable audit trail.

## Goal

Preserve task-contract status after importing a review packet into `agent-run-ledger`, so reviewers can see whether the original agent task was complete or still blocked by missing sections.

## Source Event

This recipe came from adding `## Task Contract` import support to `agent-run-ledger`.

The public change parses task contract source, status, required-section count, missing sections, and placeholder markers from `codex-review-packet` output.

## Workflow

1. Write or select the task contract before generating the review packet.
2. Generate the packet with `codex-review-packet`, letting it auto-detect `AGENT_TASK.md` or passing `--task-contract`.
3. Import the packet into `agent-run-ledger`.
4. Run `doctor --strict` on the ledger.
5. If the task contract status is not `pass`, treat the ledger blocker as unresolved scope evidence.
6. If the task contract passes, keep the event as durable proof of the run boundary.

## Example

```sh
python3 /path/to/codex-review-packet/codex_review_packet.py \
  --repo /path/to/repo \
  --task-contract /path/to/AGENT_TASK.md \
  --output /tmp/review-packet.md

node /path/to/agent-run-ledger/bin/agent-run-ledger.js import-review-packet \
  --ledger /path/to/repo/.agent-run/ledger.jsonl \
  --packet /tmp/review-packet.md

node /path/to/agent-run-ledger/bin/agent-run-ledger.js doctor \
  --ledger /path/to/repo/.agent-run/ledger.jsonl \
  --strict
```

Expected passing ledger event:

```json
{
  "type": "decision",
  "title": "Task contract passed",
  "status": "done"
}
```

Expected incomplete contract behavior:

```json
{
  "type": "blocker",
  "title": "Task contract needs attention",
  "status": "blocked"
}
```

## Checklist

- Does the review packet include `## Task Contract`?
- Does the ledger import include the review packet file and task contract source file?
- Does `Status: pass` become a `done` decision event?
- Does any non-pass status become a `blocked` blocker event?
- Does `doctor --strict` fail while task-contract blockers remain?
- Are missing sections and placeholder markers visible in the event summary?

## Failure Modes

- Importing the packet but dropping the original task boundary.
- Treating a warning task contract as a routine decision.
- Letting placeholders pass because the ledger only records changed files.
- Keeping task constraints only in chat instead of durable JSONL evidence.
- Running strict doctor on commands while ignoring scope blockers.

## Source Linkage

- Public repo: <https://github.com/manuelsampedro1/agent-run-ledger>
- Commit: <https://github.com/manuelsampedro1/agent-run-ledger/commit/9db00e99415254a351d0aa66a29a30beeb6b11e2>
- CI run: <https://github.com/manuelsampedro1/agent-run-ledger/actions/runs/26808167644>
- Lab note: <../labs/2026/2026-06-02-agent-run-ledger-task-contract-evidence.md>
