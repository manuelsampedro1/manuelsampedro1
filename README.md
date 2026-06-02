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
| [agent-run-ledger](https://github.com/manuelsampedro1/agent-run-ledger) | Agent audit trails | Records AI agent runs as JSONL, imports review packets with embedded verification checks, repo readiness reports and contracts, plus Markdown or JSON-envelope verification plans with readiness evidence, gates unresolved evidence with strict doctor mode, and renders static review reports. |
| [repo-flightcheck](https://github.com/manuelsampedro1/repo-flightcheck) | Pre-agent readiness | Audits whether a repository is ready for Codex, Claude Code, and human reviewers, including agent-readiness contract output, CI/local verification coverage, Python unittest detection, GitHub Action repos, and stale documented commands. |
| [codex-review-packet](https://github.com/manuelsampedro1/codex-review-packet) | Review context quality | Packages diffs, repo rules, local context, review lanes, repo readiness reports or contracts, and Markdown or JSON-envelope verification plans into a sharper handoff for Codex or Claude Code. |
| [verify-by-change](https://github.com/manuelsampedro1/verify-by-change) | Evidence-based closeout | Suggests honest checks from committed diffs, working-tree changes, and generated review packets, with JSON envelope metadata, packet readiness context, CI-local command parity, GitHub Action/workflow guidance, and a repo readiness contract. |
| [briefboard-local](https://github.com/manuelsampedro1/briefboard-local) | Product scoping taste | Turns messy kickoff notes into a structured build brief, flags missing essentials, and generates a Codex-ready prompt with no backend, importable examples, and CI-local checks. |

These are small on purpose. I prefer tools a reviewer can clone, inspect, run, and challenge over larger demos with less operational signal.

## Agent Safety Layer

| Repo | What it proves | Why it matters |
| --- | --- | --- |
| [deploy-gate](https://github.com/manuelsampedro1/deploy-gate) | Human authorization for AI-driven deploys | Blocks sensitive PRs until a named human approves the exact action with a signed receipt. |
| [mcp-guard](https://github.com/manuelsampedro1/mcp-guard) | Tool-call control for MCP agents | Enforces allow, block, or approval rules before dangerous MCP tool calls execute. |
| [pp-cli](https://github.com/manuelsampedro1/pp-cli) | Local receipt verification | Verifies Permission Protocol receipts with local Ed25519 signature checks. |
| [python-sdk](https://github.com/manuelsampedro1/python-sdk) | Approval workflow integration | Lets Python workflows request and verify authority receipts around sensitive actions. |

## How I Work With Codex

- Start with a real brief, explicit acceptance criteria, and the smallest useful scope. See [briefboard-local](https://github.com/manuelsampedro1/briefboard-local) and [Brief Readiness Before Codex](./recipes/brief-readiness-before-codex.md).
- Check repo readiness before handing work to an agent. See [repo-flightcheck](https://github.com/manuelsampedro1/repo-flightcheck), [Agent Readiness Contract Output](./recipes/agent-readiness-contract-output.md), [Python Unittest Readiness Check](./recipes/python-unittest-readiness-check.md), [GitHub Action Repo Readiness](./recipes/github-action-repo-readiness.md), and [Documented Command Drift Check](./recipes/documented-command-drift-check.md).
- Package repo-aware context so reviews can be stricter and more useful. See [codex-review-packet](https://github.com/manuelsampedro1/codex-review-packet), [Readiness Contract in Review Packets](./recipes/readiness-contract-in-review-packets.md), [Repo Readiness in Review Packets](./recipes/repo-readiness-in-review-packets.md), [Review Packet With Generated Verification](./recipes/review-packet-with-generated-verification.md), [Verification Envelope in Review Packets](./recipes/verification-envelope-in-review-packets.md), [Review Map in Agent Packets](./recipes/review-map-in-agent-packets.md), and [AI Repo Review Findings](./recipes/ai-repo-review-findings.md).
- Match verification to the actual change type instead of pasting the same test advice everywhere. See [verify-by-change](https://github.com/manuelsampedro1/verify-by-change), [Review Packet Readiness to Verification Envelope](./recipes/review-packet-readiness-to-verification-envelope.md), [Verification by Change Type](./recipes/verification-by-change-type.md), [GitHub Action Change Verification](./recipes/github-action-change-verification.md), [JSON Envelope for Verification Gates](./recipes/json-envelope-for-verification-gates.md), [Review Packet to Verification Checklist](./recipes/review-packet-to-verification-checklist.md), and [Repo Readiness Contract for Agent Repos](./recipes/repo-readiness-contract-for-agent-repos.md).
- Leave an audit trail for non-trivial agent runs. See [agent-run-ledger](https://github.com/manuelsampedro1/agent-run-ledger), [Verification Envelope Readiness to Ledger Evidence](./recipes/verification-envelope-readiness-to-ledger.md), [Readiness Contract to Ledger Evidence](./recipes/readiness-contract-to-ledger-evidence.md), [Review Packet Verification to Ledger](./recipes/review-packet-verification-to-ledger.md), [Review Packet to Ledger Evidence](./recipes/review-packet-to-ledger-evidence.md), [Repo Readiness to Ledger Evidence](./recipes/repo-readiness-to-ledger-evidence.md), and [Verification Envelope to Ledger Evidence](./recipes/verification-envelope-to-ledger-evidence.md).
- Gate sensitive agent actions with explicit human authorization where execution risk is higher than review risk. See [deploy-gate](https://github.com/manuelsampedro1/deploy-gate) and [mcp-guard](https://github.com/manuelsampedro1/mcp-guard).

## Public Workbench

- [AI lab notes](./labs/README.md): build notes, decisions, and launch logs tied to real repos or workflows.
- [Recipes](./recipes/README.md): reusable prompts, checklists, and implementation patterns that came from actual work.
- [Tooling radar](./radar/README.md): short research only when it changes a build or tooling decision.
- [Automation runbook](./docs/automation-runbook.md): how the profile publishing loop works and what it refuses to publish.

## Latest Proof

- Latest lab note: [2026-06-02 - Agent Run Ledger Envelope Readiness Evidence](./labs/2026/2026-06-02-agent-run-ledger-envelope-readiness-evidence.md)
- Latest recipes:
  - [Verification Envelope Readiness to Ledger Evidence](./recipes/verification-envelope-readiness-to-ledger.md)
  - [Review Packet Readiness to Verification Envelope](./recipes/review-packet-readiness-to-verification-envelope.md)
  - [Readiness Contract in Review Packets](./recipes/readiness-contract-in-review-packets.md)

## Principles

- Ship useful proof, not activity theater.
- Optimize for reviewability: strong AI workflows should leave evidence.
- Prefer own repos and working artifacts over meta commentary.
- Keep claims honest: what exists, what was tested, and what is still limited.
- Use the workbench as supporting evidence, not as a substitute for real projects.
