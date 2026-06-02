# Agent Plan Trace

Use this before accepting a coding-agent closeout when the run had a plan.

## Source

- Public tool: https://github.com/manuelsampedro1/agent-plan-trace
- Launch note: [2026-06-02 - Agent Plan Trace Public Launch](../labs/2026/2026-06-02-agent-plan-trace-public-launch.md)

## Pattern

1. Save the plan as Markdown or JSON:

```sh
cp /path/to/agent-plan.md /tmp/plan.md
```

2. Capture the diff:

```sh
git diff --stat
git diff > /tmp/agent.diff
```

3. Save command evidence and the final closeout:

```sh
cp /path/to/commands.txt /tmp/commands.txt
cp /path/to/closeout.md /tmp/closeout.md
```

4. Audit plan traceability:

```sh
agent-plan-trace /tmp/plan.md \
  --diff /tmp/agent.diff \
  --commands /tmp/commands.txt \
  --closeout /tmp/closeout.md \
  --min-score 80 \
  --fail-on high
```

5. Persist the report when the result feeds review:

```sh
agent-plan-trace /tmp/plan.md \
  --diff /tmp/agent.diff \
  --commands /tmp/commands.txt \
  --closeout /tmp/closeout.md \
  --write-report /tmp/plan-trace.md
```

## What Good Looks Like

- Completed plan items are mentioned by diff paths, command evidence, or
  closeout text.
- Verification-shaped completed items have test, lint, build, smoke, or CI
  command evidence.
- Pending, in-progress, or blocked items stay visible in the closeout.
- Changed files are not hidden from both plan and final answer.
- Test-pass claims include successful command output or CI evidence.

## Prompt Pattern

```text
Rewrite this closeout so it matches the plan trace.

Rules:
- Keep completed items tied to evidence.
- Preserve pending, in-progress, or blocked work.
- Mention changed files that the plan missed.
- Replace broad completion claims with exact command or CI evidence.
- Do not claim tests passed without a successful command receipt.

<agent-plan-trace output>
<current closeout>
<plan>
```

## Pair With

- `agent-closeout-check` before final answer quality review,
- `agent-claim-check` before reusing closeout claims in PRs or proof packets,
- `agent-command-receipt` when command outcomes need tamper-evident hashes,
- `agent-run-ledger` when the plan trace should become durable run evidence.

## Failure Mode

Do not force every plan item to map to one file. Some planning work is
environmental or review-oriented. In that case, make the command log or closeout
carry the evidence explicitly.
