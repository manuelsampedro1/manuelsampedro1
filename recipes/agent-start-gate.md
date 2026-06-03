# Agent Start Gate

Use this pattern when a coding-agent run has enough moving parts that starting immediately would be risky: unclear scope, untrusted context, dirty worktree, missing verification, or vague stop conditions.

## Gate Shape

Create a Markdown start packet with these sections:

- `Objective`: the single outcome for this run.
- `Scope`: allowed files, folders, commands, or product areas plus explicit out-of-scope work.
- `Inputs`: task contract, request brief, repo readiness, or other source evidence.
- `Worktree`: clean state or documented pre-existing user changes.
- `Context`: trusted sources and untrusted context screening.
- `Verification`: exact commands or manual checks.
- `Stop Conditions`: when the agent must stop, ask, or block instead of guessing.

## CLI Pattern

```sh
agent-start-gate init AGENT_START.md
agent-start-gate check AGENT_START.md
agent-start-gate check AGENT_START.md --format json
```

The gate should return `0` only when the packet is ready. Missing sections, failed evidence, absent commands, or weak stop conditions should return non-zero with actionable issues.

## Review Rule

Do not treat a long prompt as equivalent to start readiness. A reviewer should be able to inspect one packet and see:

- What the agent may change.
- What it must not change.
- Which evidence says the repo and task are ready.
- What context is trusted or untrusted.
- How completion will be checked.
- When the agent should stop before causing drift.

## Public Example

The implementation lives in [`agent-start-gate`](https://github.com/manuelsampedro1/agent-start-gate), with an example packet at `examples/agent-start-packet.md`.
