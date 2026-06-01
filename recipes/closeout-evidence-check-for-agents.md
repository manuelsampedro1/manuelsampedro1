# Closeout Evidence Check for Agents

Use this before accepting a coding-agent final answer, PR comment, or run ledger entry.

## Use When

- The agent says the task is done.
- The closeout claims tests passed.
- The change touched more than one file.
- A human reviewer needs to decide whether to trust the handoff.

## Goal

Make the closeout reviewable, not just confident.

The final answer should include:

- what changed,
- which files or paths changed,
- exact verification commands or manual checks,
- risks, limitations, or unverified work,
- no vague confidence language without evidence.

## Workflow

1. Save the closeout:

```sh
pbpaste > /tmp/agent-closeout.md
```

2. Check for evidence:

```sh
agent-closeout-check /tmp/agent-closeout.md
```

3. If the helper is unavailable, use a manual gate:

```text
Does it name changed files?
Does it name exact commands or checks?
Does it say what was not verified?
Does it avoid phrases like "should work"?
```

4. Ask for a revised closeout when evidence is missing.

## Prompt Pattern

```text
Rewrite this coding-agent closeout so it is reviewable.

Rules:
- Include a short summary.
- Name changed files or paths.
- List exact verification commands and results.
- State any risks, limitations, or checks not run.
- Remove vague claims such as "should work" unless tied to evidence.

<paste closeout>
```

## Fast Checklist

- Is there a summary?
- Are changed files or paths named?
- Are verification commands exact?
- Are risks or limitations stated?
- Would a reviewer know what evidence supports the claim?

## Failure Modes

- "Done" with no file or command evidence.
- "Tests pass" without the command.
- "Should work" without verification.
- Hiding manual checks under generic wording.
- Omitting unverified areas because they sound negative.

## Source Linkage

- Repo / tool / workflow: local `agent-closeout-check` prototype and this profile repo's evidence-led closeout style.
- Supporting prompt, script, or note: [`./verification-by-change-type.md`](./verification-by-change-type.md), [`./ci-failure-packet-for-agent-reruns.md`](./ci-failure-packet-for-agent-reruns.md), and [`../docs/profile-strategy.md`](../docs/profile-strategy.md).

