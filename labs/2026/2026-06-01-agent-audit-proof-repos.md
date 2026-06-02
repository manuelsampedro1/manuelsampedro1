# 2026-06-01 - Agent Audit Proof Repos

## Context

The public profile needed stronger proof than recipes and lab notes alone. A GitHub account with real projects gives reviewers concrete artifacts to inspect, so the useful move was to ship small tools that an AI builder can inspect, run, and understand quickly.

## Useful Artifact

Two public repos now cover the before-and-after loop of agent work:

- [`repo-flightcheck`](https://github.com/manuelsampedro1/repo-flightcheck): checks whether a repo is ready for Codex, Claude Code, and human review before an agent starts.
- [`agent-run-ledger`](https://github.com/manuelsampedro1/agent-run-ledger): records agent run evidence as JSONL and renders a static HTML review report after the work is done.

Together they make a practical workflow:

1. Run `repo-flightcheck` before delegating work to an agent.
2. Start an `agent-run-ledger` file when the run has enough scope to need review.
3. Record decisions, changed files, commands, blockers, and the final review focus.
4. Attach or commit the generated HTML report when it helps a teammate review the run.

## Source Linkage

- Repo / tool / workflow: [`repo-flightcheck`](https://github.com/manuelsampedro1/repo-flightcheck) and [`agent-run-ledger`](https://github.com/manuelsampedro1/agent-run-ledger)
- Supporting prompt, script, or file: [`docs/profile-strategy.md`](../../docs/profile-strategy.md), [`DECISIONS.md`](../../DECISIONS.md), and [`TODO.md`](../../TODO.md)

## Notes

- Observation: `repo-flightcheck` is intentionally a no-dependency CLI because repo readiness checks should work in locked-down project folders.
- Observation: `agent-run-ledger` keeps the audit format as JSONL and generates static HTML so the handoff survives outside a chat transcript.
- Tradeoff: these projects are compact rather than broad. That is deliberate because the profile needs fast proof of judgment, not a large demo surface with weak maintenance.
- Failure mode: if the profile README highlights only notes and recipes, the strongest proof gets buried. The selected-work table now needs to show the shipped repos first.

## Verification

Local verification completed before publishing:

- `repo-flightcheck`: `node scripts/lint.js`, `node scripts/build.js`, `node --test`, and a strict self-audit run.
- `agent-run-ledger`: `node scripts/lint.js`, `node scripts/build.js`, `node --test`, and `node bin/agent-run-ledger.js demo --out .agent-run` followed by `doctor`.
- Both repos were pushed to GitHub over SSH and pinned on the public profile.

## Next Step

Check the first GitHub Actions runs after GitHub finishes scheduling CI, then use the two repos as the primary evidence in the application.
