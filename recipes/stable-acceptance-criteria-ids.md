# Stable Acceptance Criteria IDs

Use this pattern when a task contract will feed acceptance traces, proof
packets, PR briefs, closeouts, run ledgers, or profile proof.

## Problem

Anonymous acceptance bullets are easy to write but hard to audit later. Once
criteria move through review packets, verification envelopes, ledgers, and
final answers, references such as "the second bullet" become brittle.

## Pattern

Require stable IDs before reusing the task contract:

```sh
agent-task-contract check AGENT_TASK.md \
  --require-acceptance-ids \
  --format json \
  > /tmp/task-contract.json
```

Write criteria like:

```md
## Acceptance Criteria
- AC-1: The CLI exits zero for a complete contract.
- AC-2: Missing verification details produce a non-zero exit.
- AC-3: JSON output exposes status, score, issues, and acceptance IDs.
```

Treat these as blockers:

- any acceptance bullet without an `AC-N` id;
- duplicate acceptance IDs;
- fewer than two concrete acceptance bullets;
- placeholder acceptance language.

## Acceptance Criteria

- AC-1: `acceptance_ids_required` is `true` in JSON output.
- AC-2: `acceptance_id_count` equals `acceptance_criteria_count`.
- AC-3: Each criterion can be referenced by ID in traces, proof packets,
  ledgers, and closeouts.

## Review Rule

Stable IDs prove criteria are referenceable. They do not prove the criteria
were satisfied. Pair them with acceptance traces, command receipts, CI runs, or
proof packets when checking completion.
