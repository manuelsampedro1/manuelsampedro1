# Manuel Sampedro

I build agentic engineering tools: repo readiness checks, review handoffs, verification gates, run ledgers, and local-first product prototypes.

My focus is the practical layer around coding agents: the prompts, scripts, workflows, and small products that make AI-generated work scoped, inspectable, and easier to trust.

If you are building with Codex or evaluating how AI changes software work, find me on [X @manuelsampedrop](https://x.com/manuelsampedrop).

## Current Focus

- Agent reliability: repo setup checks, context contracts, review packets, and repeatable handoffs.
- Verification discipline: change-aware test plans, honest closeout notes, and evidence before claims.
- Agent auditability: run ledgers, decisions, file changes, command history, and blockers a reviewer can inspect.
- Agent safety: permission gates, MCP tool controls, and receipt-based authorization for sensitive actions.
- Product judgment: small local-first prototypes that test the workflow before adding backend weight.

## Selected Work

| Repo | What it proves | Why it matters |
| --- | --- | --- |
| [agent-run-ledger](https://github.com/manuelsampedro1/agent-run-ledger) | Agent audit trails | Records AI agent runs as JSONL and renders static review reports with decisions, files, commands, and blockers. |
| [repo-flightcheck](https://github.com/manuelsampedro1/repo-flightcheck) | Pre-agent readiness | Audits whether a repository is ready for Codex, Claude Code, and human reviewers before asking an agent to work in it. |
| [codex-review-packet](https://github.com/manuelsampedro1/codex-review-packet) | Review context quality | Packages diffs, repo rules, and local context into a sharper handoff for Codex or Claude Code. |
| [verify-by-change](https://github.com/manuelsampedro1/verify-by-change) | Evidence-based closeout | Suggests honest checks from changed files so AI-generated work closes with evidence instead of boilerplate. |
| [briefboard-local](https://github.com/manuelsampedro1/briefboard-local) | Product scoping taste | Turns messy kickoff notes into a structured build brief and a Codex-ready prompt with no backend. |

These are small on purpose. I prefer tools a reviewer can clone, inspect, run, and challenge over larger demos with less operational signal.

## Agent Safety Layer

| Repo | What it proves | Why it matters |
| --- | --- | --- |
| [deploy-gate](https://github.com/manuelsampedro1/deploy-gate) | Human authorization for AI-driven deploys | Blocks sensitive PRs until a named human approves the exact action with a signed receipt. |
| [mcp-guard](https://github.com/manuelsampedro1/mcp-guard) | Tool-call control for MCP agents | Enforces allow, block, or approval rules before dangerous MCP tool calls execute. |
| [pp-cli](https://github.com/manuelsampedro1/pp-cli) | Local receipt verification | Verifies Permission Protocol receipts with local Ed25519 signature checks. |
| [python-sdk](https://github.com/manuelsampedro1/python-sdk) | Approval workflow integration | Lets Python workflows request and verify authority receipts around sensitive actions. |

## How I Work With Codex

- Start with a real brief, explicit acceptance criteria, and the smallest useful scope. See [briefboard-local](https://github.com/manuelsampedro1/briefboard-local).
- Check repo readiness before handing work to an agent. See [repo-flightcheck](https://github.com/manuelsampedro1/repo-flightcheck).
- Package repo-aware context so reviews can be stricter and more useful. See [codex-review-packet](https://github.com/manuelsampedro1/codex-review-packet) and [AI Repo Review Findings](./recipes/ai-repo-review-findings.md).
- Match verification to the actual change type instead of pasting the same test advice everywhere. See [verify-by-change](https://github.com/manuelsampedro1/verify-by-change) and [Verification by Change Type](./recipes/verification-by-change-type.md).
- Leave an audit trail for non-trivial agent runs. See [agent-run-ledger](https://github.com/manuelsampedro1/agent-run-ledger).
- Gate sensitive agent actions with explicit human authorization where execution risk is higher than review risk. See [deploy-gate](https://github.com/manuelsampedro1/deploy-gate) and [mcp-guard](https://github.com/manuelsampedro1/mcp-guard).

## Public Workbench

- [AI lab notes](./labs/README.md): build notes, decisions, and launch logs tied to real repos or workflows.
- [Recipes](./recipes/README.md): reusable prompts, checklists, and implementation patterns that came from actual work.
- [Tooling radar](./radar/README.md): short research only when it changes a build or tooling decision.
- [Automation runbook](./docs/automation-runbook.md): how the profile publishing loop works and what it refuses to publish.

## Latest Proof

- Latest lab note: [2026-06-01 - Expected Paths Contract for Agent Publish Runs](./labs/2026/2026-06-01-expected-paths-contract-for-agent-publish-runs.md)
- Latest recipes:
  - [Agent Diff Budget](./recipes/agent-diff-budget.md)
  - [Agent Decision Guard](./recipes/agent-decision-guard.md)
  - [Agent Eval Runner](./recipes/agent-eval-runner.md)

## Principles

- Ship useful proof, not activity theater.
- Optimize for reviewability: strong AI workflows should leave evidence.
- Prefer own repos and working artifacts over meta commentary.
- Keep claims honest: what exists, what was tested, and what is still limited.
- Use the workbench as supporting evidence, not as a substitute for real projects.
