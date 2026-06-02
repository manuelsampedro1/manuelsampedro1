# Agent Review Map

Use this when a coding-agent diff needs to be routed to the right review lanes instead of handed over as one flat patch.

## Use When

- A diff crosses product, code, tests, automation, release, data, or security boundaries.
- A reviewer needs to know who should inspect which part first.
- A polished closeout hides the fact that several specialties are involved.
- You need concrete reviewer questions before building a proof packet.

## Goal

Turn a unified diff into a review handoff map:

- changed files,
- additions and deletions,
- review lanes,
- suggested reviewer owner per lane,
- high-risk handoff order,
- lane-specific reviewer questions.

This keeps reviews from becoming generic. Security, data, release, and automation questions should happen before broad application-code review when those lanes are touched.

## Workflow

1. Capture the current diff:

```sh
git diff -- . > /tmp/agent-change.diff
```

2. Generate a Markdown handoff:

```sh
PYTHONPATH=src python3 -m agent_review_map /tmp/agent-change.diff
```

3. Generate JSON for a proof packet or CI artifact:

```sh
PYTHONPATH=src python3 -m agent_review_map /tmp/agent-change.diff --format json > /tmp/review-map.json
```

4. Use the handoff order to route review:

- security before application review,
- data before release,
- automation before runbook closeout,
- product/docs before public claims are accepted,
- tests before merge readiness.

## Prompt Pattern

```text
Create a review map for this coding-agent diff.

Rules:
- Group files by review lane: security, data, release, automation, agent instructions, product/docs, tests, and application code.
- Put high-risk lanes first.
- Name the suggested reviewer owner for each lane.
- Ask specific questions each reviewer must answer.
- Do not treat one green test command as enough if the diff crosses multiple lanes.

<paste diff>
```

## Fast Checklist

- Does every risky file have a review lane?
- Is the handoff order stricter than the final answer's narrative?
- Are docs/public claims reviewed separately from implementation?
- Are test changes reviewed for coverage quality, not just presence?
- Did the proof packet include the review map or its conclusions?

## Failure Modes

- Reviewing a mixed diff as if it belongs to one owner.
- Sending CI, auth, release, and README changes through normal app-code review only.
- Letting docs claims bypass implementation verification.
- Asking generic reviewer questions that could apply to any PR.
- Skipping ownership because the project is small.

## Source Linkage

- Public repo: <https://github.com/manuelsampedro1/agent-review-map>
- Commit: <https://github.com/manuelsampedro1/agent-review-map/commit/9e392da69b5a96c80777ba6292c7bbd205e01ea5>
- README: <https://raw.githubusercontent.com/manuelsampedro1/agent-review-map/main/README.md>
- CLI: <https://raw.githubusercontent.com/manuelsampedro1/agent-review-map/main/src/agent_review_map/cli.py>
- Tests: <https://raw.githubusercontent.com/manuelsampedro1/agent-review-map/main/tests/test_cli.py>
- Mixed diff example: <https://raw.githubusercontent.com/manuelsampedro1/agent-review-map/main/examples/mixed.diff>
- Launch note: [`../labs/2026/2026-06-02-agent-review-map-public-launch.md`](../labs/2026/2026-06-02-agent-review-map-public-launch.md)
- Supporting recipes: [`./agent-diff-budget.md`](./agent-diff-budget.md), [`./change-risk-matrix-for-agent-diffs.md`](./change-risk-matrix-for-agent-diffs.md), and [`./agent-proof-packet-for-review.md`](./agent-proof-packet-for-review.md).
