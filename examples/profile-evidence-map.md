# Profile Evidence Map

Use this map to review the profile by claim instead of by repo count.

## Core Claims

| Claim | Primary evidence | What to inspect |
| --- | --- | --- |
| I gate agent starts before the first edit. | [`agent-start-gate`](https://github.com/manuelsampedro1/agent-start-gate), [`agent-task-contract`](https://github.com/manuelsampedro1/agent-task-contract), [`repo-flightcheck`](https://github.com/manuelsampedro1/repo-flightcheck) | Start-packet checks, task-contract checks, repo readiness output, non-zero failures, tests, and CI. |
| I build repo-readiness gates for coding agents. | [`repo-flightcheck`](https://github.com/manuelsampedro1/repo-flightcheck) | README usage, `bin/repo-flightcheck.js`, tests, CI, and `--check-remote --strict` output. |
| I package better review context for agents and humans. | [`codex-review-packet`](https://github.com/manuelsampedro1/codex-review-packet) | Review-map output, task-contract support, verification envelope rendering, CI/published-HEAD sections. |
| I tie verification to actual changed files. | [`verify-by-change`](https://github.com/manuelsampedro1/verify-by-change) | Path-category rules, JSON envelope output, review-packet input, empty-diff behavior. |
| I keep agent runs auditable after the chat ends. | [`agent-run-ledger`](https://github.com/manuelsampedro1/agent-run-ledger) | JSONL ledger format, strict doctor mode, report rendering, review-packet and CI imports. |
| I treat safety as part of the workflow, not as a footer. | [`agent-context-sentinel`](https://github.com/manuelsampedro1/agent-context-sentinel), [`agent-secret-sentinel`](https://github.com/manuelsampedro1/agent-secret-sentinel), [`mcp-guard`](https://github.com/manuelsampedro1/mcp-guard) | Untrusted-context checks, secret-like diff scanning, and MCP tool-call policy rules. |
| I distinguish packaged evidence from merge readiness. | [`agent-merge-readiness`](https://github.com/manuelsampedro1/agent-merge-readiness), [`agent-proof-packet`](https://github.com/manuelsampedro1/agent-proof-packet) | Non-ready exit codes, required checks by risk, proof-packet verdict rules. |
| I handle release, CI, retry, and rollback handoffs explicitly. | [`agent-release-note-check`](https://github.com/manuelsampedro1/agent-release-note-check), [`agent-ci-failure-packet`](https://github.com/manuelsampedro1/agent-ci-failure-packet), [`agent-retry-guard`](https://github.com/manuelsampedro1/agent-retry-guard), [`agent-rollback-plan`](https://github.com/manuelsampedro1/agent-rollback-plan) | Release-note coverage, CI log packet extraction, retry-loop findings, rollback steps and checks. |

## Composition Proof

| Workflow | Evidence artifact | Signal |
| --- | --- | --- |
| Release readiness | [Agent Release Readiness Chain](./agent-release-readiness-chain.md) | Shows risk routing, release-note coverage, proof packet packaging, and a `needs-review` merge verdict when scope/risk evidence is incomplete. |
| Durable run review | [Agent Review Packet to Ledger Chain](./agent-review-packet-to-ledger-chain.md) | Shows review packet generation, `verify-by-change.v1` envelope output, ledger import, strict doctor mode, and report rendering. |
| External scan path | [External Reviewer Navigation](./external-reviewer-navigation.md) | Gives a five-minute path through the strongest repos before reading the full Selected Work table. |
| Profile claim audit | [Profile Verification Proof Packet](./profile-verification-proof-packet.md) | Defines local commands, remote readiness checks, raw URL checks, and CI signals for profile maintenance. |
| Saturation control | [Profile Curation Guard Proof Packet](./profile-curation-guard-proof-packet.md) | Explains when not to add another repo because curation is stronger than volume. |

## Review Prompt

```text
Review this profile by claim. For each claim, inspect the linked repo or example
and decide whether the artifact proves the claim through code, tests, CI, CLI
output, or a reusable workflow. Flag claims that rely only on phrasing, repo
count, or confidence instead of inspectable evidence.
```
