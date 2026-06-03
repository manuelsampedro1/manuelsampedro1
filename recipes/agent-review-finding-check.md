# Agent Review Finding Check

Use this before sending agent-generated review findings to a PR, proof packet,
or human reviewer.

## Source

- Public tool: https://github.com/manuelsampedro1/agent-review-finding-check
- Launch note: [2026-06-02 - Agent Review Finding Check Public Launch](../labs/2026/2026-06-02-agent-review-finding-check-public-launch.md)
- Proof-packet follow-up: [2026-06-03 - Agent Review Finding Check Proof Packets](../labs/2026/2026-06-03-agent-review-finding-check-proof-packets.md)

## Pattern

1. Save the review findings:

```sh
cp /path/to/review-findings.md /tmp/review-findings.md
```

2. Capture the reviewed diff:

```sh
git diff main...HEAD > /tmp/review.diff
```

3. Audit finding quality:

```sh
agent-review-finding-check /tmp/review-findings.md \
  --diff /tmp/review.diff \
  --min-score 80 \
  --fail-on high
```

4. Tighten before posting to a PR:

```sh
agent-review-finding-check /tmp/review-findings.md \
  --diff /tmp/review.diff \
  --min-score 90 \
  --fail-on medium
```

5. Preserve the report in review evidence:

```sh
agent-review-finding-check /tmp/review-findings.md \
  --diff /tmp/review.diff \
  --write-report /tmp/review-finding-check.md
```

6. Attach structured proof-packet evidence when available:

```sh
agent-review-finding-check /tmp/review-findings.md \
  --diff /tmp/review.diff \
  --proof-packet /tmp/proof-packet.json \
  --min-score 90 \
  --fail-on medium
```

## What Good Looks Like

- Each finding has severity and a concrete `file:line`.
- Referenced files appear in the reviewed diff unless the reviewer explicitly
  allowed outside-diff context.
- The finding explains impact or risk.
- The finding gives a fix path or next action.
- High-priority findings include evidence language, not just assertion.
- Empty reviews still mention residual risks or testing gaps.
- Proof-packet checks can support matching file references, but they do not hide
  missing severity, missing location, missing impact, missing action, vague
  language, or outside-diff issues.

## Prompt Pattern

```text
Rewrite these review findings so they are actionable.

Rules:
- Include severity for each finding.
- Include exact file:line references.
- Explain impact or risk in one sentence.
- Include a concrete fix or next action.
- Remove vague language such as "maybe", "probably", or "I think".
- Preserve no-findings reviews only when residual risks or test gaps are stated.

<agent-review-finding-check output>
<current findings>
<diff summary>
```

## Pair With

- `codex-review-packet` for repo-aware review context,
- `agent-review-map` for lane routing,
- `agent-proof-packet` for structured command and file evidence,
- `agent-pr-brief` before posting the PR description.

## Failure Mode

Do not force every valid concern into the changed diff. If a finding relies on
outside context, allow it explicitly and explain why that context is relevant.
