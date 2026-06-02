# Agent Instruction Audit

Use this before treating a repo as ready for Codex, Claude Code, Gemini, Cursor, or another coding agent.

## Pattern

1. Audit `AGENTS.md`, `CLAUDE.md`, `GEMINI.md`, `CURSOR.md`, or `.cursorrules`.
2. Require the file to explain repo goal or scope, constraints, verification commands, safety guidance, and closeout expectations.
3. Block risky guidance such as unguarded destructive commands, stored tokens, disabled tests, or instructions to ask for passwords.
4. Re-run the audit after changing agent instructions, not only before the first handoff.

## Commands

```sh
agent-instruction-audit AGENTS.md --min-score 80
agent-instruction-audit AGENTS.md --format json
```

Strict mode turns warnings into blockers:

```sh
agent-instruction-audit AGENTS.md --strict
```

## When It Fails

- Add concrete repo scope instead of generic "be helpful" rules.
- Name exact verification commands.
- Add explicit secret, credential, destructive-command, and approval guidance.
- Remove instructions that weaken tests or authorize broad cleanup.

Proof repo: [agent-instruction-audit](https://github.com/manuelsampedro1/agent-instruction-audit).
