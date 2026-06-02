# Agent Test Impact

Use this when a coding-agent diff changes source files and the closeout needs
evidence that tests changed near the behavior.

## Source

- Public tool: https://github.com/manuelsampedro1/agent-test-impact
- Launch note: [2026-06-02 - Agent Test Impact Public Launch](../labs/2026/2026-06-02-agent-test-impact-public-launch.md)

## Pattern

1. Save the diff:

```sh
git diff origin/main -- . > /tmp/agent-change.diff
```

2. Run the impact check:

```sh
agent-test-impact /tmp/agent-change.diff --min-score 80 --fail-on-missing
```

3. If the check reports missing evidence, do not accept a generic "tests pass"
closeout. Ask for the related test, a precise reason no test is needed, or a
review packet that preserves the gap.

4. Record the output in the proof packet, merge-readiness verdict, or run
ledger.

## What Good Looks Like

- Source files changed by the diff are visible.
- Related test files changed when behavior changed.
- Partial evidence is treated as a prompt for reviewer attention, not as proof.
- Missing evidence blocks confident closeout unless explicitly waived.
- Suggested commands are targeted to the changed language or test convention.

## Prompt Pattern

```text
Review this coding-agent diff for test impact.

Rules:
- Do not treat broad test success as proof that the changed behavior has coverage.
- Classify source changes as direct, partial, or missing test evidence.
- Ask for exact test evidence or an explicit waiver when evidence is missing.
- Keep the final verdict separate from runtime coverage claims.

<agent-test-impact output>
<diff>
<closeout>
```

## Pair With

- `verify-by-change` for broader change-aware verification,
- `agent-acceptance-trace` to connect tests back to acceptance criteria,
- `agent-claim-check` before reusing a final answer as proof,
- `agent-proof-packet` to preserve missing or partial evidence,
- `agent-merge-readiness` before merge.

## Failure Mode

Do not accept "I ran make test" as sufficient when source changed and no related
test evidence appears in the diff. That can be true, useful, and still not
enough for a confident agent closeout.
