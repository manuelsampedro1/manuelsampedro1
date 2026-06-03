# Agent Evidence Chain

Use this pattern when a coding-agent workflow combines several JSON evidence artifacts into one review packet, ledger entry, closeout, or proof bundle.

## Chain Contract

Require each artifact to include:

- `schema_version` so the consumer knows what produced it.
- shared repository identity, such as `repo`, `repository`, or `repository_url`.
- shared commit identity, such as `head_sha`, `commit`, or `source_commit`.
- shared `task_id` when the workflow has one.
- a non-blocking outcome when the artifact is being reused as ready evidence.
- empty blocker-like lists such as `blocking_findings`, `blockers`, and `missing_evidence`.

## CLI Pattern

```sh
agent-evidence-chain check \
  review-packet.json \
  verification-envelope.json \
  ledger-summary.json \
  --require-task-id
```

For automation:

```sh
agent-evidence-chain check artifacts/*.json --require-task-id --format json
```

## Review Rule

Do not treat several artifacts as one proof chain until the shared identity is explicit.

Check:

- Do all artifacts point at the same task?
- Do all artifacts point at the same repository?
- Do all artifacts point at the same commit?
- Is every artifact versioned?
- Are any outcomes still `blocked`, `needs-review`, `failed`, or `invalid`?
- Are any blocker or missing-evidence lists still populated?

## Public Example

The implementation lives in [`agent-evidence-chain`](https://github.com/manuelsampedro1/agent-evidence-chain), with matching and mismatched JSON examples under `examples/`.
