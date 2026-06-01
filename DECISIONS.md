# Decisions

## 2026-05-21 - Profile Repo as AI Builder Workbench

Use the GitHub profile repository as the professional front door and daily AI workbench.

Rationale:

- The profile README stays readable.
- Daily work remains visible in structured folders.
- Contributions can be useful without creating empty commits.
- The system works locally first and can push once GitHub authentication is configured.

## 2026-05-21 - No Fake Activity

Automations must skip commits when they cannot produce useful content.

Rationale:

- Empty contribution farming weakens the profile.
- Useful artifacts compound into a credible public body of work.
- This keeps the account aligned with platform trust and professional reputation.

## 2026-05-21 - Live GitHub Account

Use `manuelsampedro1/manuelsampedro1` as the live GitHub profile repository.

Rationale:

- The browser-authenticated GitHub account is `manuelsampedro1`.
- GitHub publicly recognizes `manuelsampedro1/manuelsampedro1` as the special profile README repository.
- Commits are authored with the account's no-reply address: `202281585+manuelsampedro1@users.noreply.github.com`.

## 2026-05-21 - Weekly Quality Guard

Add a weekly quality audit automation in addition to the daily contribution automations.

Rationale:

- Daily publishing needs a guard against generic filler.
- The audit checks recent artifacts against the profile's topic and usefulness bar.
- Corrective actions go into `TODO.md` instead of silently letting automation drift.

## 2026-05-21 - Refresh All Public Indexes During Maintenance

The maintenance commit should refresh the folder indexes for `labs/`, `recipes/`, and `radar/`.

Rationale:

- The profile README should point to current public artifacts, not stale folders.
- Daily recipe and radar additions need the same discoverability as lab notes.
- Index refresh belongs in maintenance because it is lightweight and deterministic.

## 2026-05-24 - Optimize the Profile for AI Client Credibility

The profile should act first as proof of execution for AI clients, and second as an internal workbench archive.

Rationale:

- Clients need to understand the offer and see proof quickly.
- The README should sell clarity, taste, and execution, not only activity.
- Meta-workflows are useful only when they support visible shipped work.

## 2026-05-24 - Flagship Repos Are the Primary Proof Layer

Public proof should be anchored in 2-3 owned repos before secondary notes, recipes, or radar updates.

Rationale:

- Owned repos are stronger than forks or commentary for first impressions.
- They give pinned repositories a clear job.
- Labs and recipes become more credible when they point back to working repos.

## 2026-05-24 - Use X as the Public CTA

Use `@manuelsampedrop` as the primary public CTA from the profile surface.

Rationale:

- The profile needs a direct next step.
- X is the lowest-friction place to continue a conversation publicly.
- It keeps the CTA aligned with builder-facing distribution.

## 2026-05-24 - Maintenance Automation Must Reject Surface-Only Diffs

The maintenance commit flow should not publish changes when the diff only touches profile surface files or indexes.

Rationale:

- README churn alone is not strong public proof.
- The maintenance job should follow substantive work, not simulate it.
- This forces the public surface to be tightened only after something real improved.

## 2026-05-24 - Repo Automation Script Fixes Count as Substantive Work

Changes under `scripts/` can be published by maintenance when they improve artifact generation, publishing safety, or verification quality.

Rationale:

- The public workbench includes the automation logic that produces and guards its artifacts.
- Hardening publish scripts is operational proof, not surface churn.
- This keeps maintenance strict about README-only edits without blocking real tooling improvements.

## 2026-05-31 - Block Unexpected Public-Path Changes Before Publish

`scripts/commit_daily_update.sh` should block when staged public paths already contain changes outside the explicit file set intended for the current publish run.

Rationale:

- Whole-directory staging is convenient but can silently bundle unrelated draft work.
- Scheduled or agent-driven publish flows need an explicit contract for what this run is allowed to ship.
- Blocking before index refresh and `git add` is safer than relying on commit-message discipline or manual review after staging.

## 2026-06-01 - Add Agent Audit Repos as Primary Proof

Use `repo-flightcheck` and `agent-run-ledger` as first-class proof repos on the profile.

Rationale:

- The strongest application signal is working public code, not profile copy alone.
- Both repos address real AI builder friction: repo readiness before agent work and auditability after agent work.
- They are small enough to inspect quickly but complete enough to show README quality, tests, CI, and local-first implementation judgment.

## 2026-06-02 - Lead With Agent Reliability Proof

Frame the profile around coding-agent reliability, reviewability, verification, and auditability before broader "AI builder" language.

Rationale:

- Serious AI teams need evidence that agent workflows can be trusted in real repos.
- The strongest current proof repos already cluster around readiness, review context, verification, and audit trails.
- Subtle proof reads better than direct job-pitch language for a high-caliber technical audience.

## 2026-06-02 - Build Task Contracts as Next Agent Reliability Proof

Use `agent-task-contract` as the next public proof project once a GitHub remote can be created.

Rationale:

- The current proof stack covers repo readiness, review handoffs, verification, and run auditability.
- A task-contract checker covers the missing pre-run question: is the requested task specific enough for an agent to execute safely?
- The project is dependency-free, local-first, testable, and aligned with the profile's reliability narrative.

## 2026-06-02 - Surface Agent Safety and Permission Work

Expose `deploy-gate`, `mcp-guard`, `pp-cli`, and `python-sdk` as a distinct agent safety layer on the profile.

Rationale:

- The profile should show not only agent productivity, but also judgment around tool permissions, deploy risk, and audit receipts.
- These repos strengthen the OpenAI-relevant narrative because serious agent systems need controls before actions execute.
- Keeping them in a separate section avoids diluting the primary selected-work table while still making the safety work visible.

## 2026-06-02 - Build Diff-to-Eval as Agent Learning Loop Proof

Use `diff-to-eval` as another next public proof project once a GitHub remote can be created.

Rationale:

- The profile should show a full improvement loop: task contract, repo readiness, execution, verification, audit, and reusable eval cases.
- Real diffs are stronger eval seeds than generic benchmark prompts.
- A dependency-free CLI that turns diffs into JSON eval cases is small, reviewable, and directly useful for agent teams.

## 2026-06-02 - Build Secret Sentinel as Agent Diff Safety Proof

Use `agent-secret-sentinel` as another next public proof project once a GitHub remote can be created.

Rationale:

- Agent-generated diffs can accidentally include copied tokens, webhook secrets, private keys, or realistic sample credentials.
- A local diff scanner fits the profile's safety narrative because it blocks obvious leaks before commit or publication.
- The project is intentionally narrow: dependency-free, diff-only, and explicit that it is a preflight rather than a full security audit.

## 2026-06-02 - Build CI Failure Packets for Agent Reruns

Use `agent-ci-failure-packet` as another next public proof project once a GitHub remote can be created.

Rationale:

- CI failure logs are often too noisy for a high-quality agent retry.
- A compact packet with failing commands, error signals, file references, and suggested checks improves the next run's context quality.
- This completes another part of the agent workflow loop: failure triage after verification fails.

## 2026-06-02 - Build Rollback Plans for Agent Diffs

Use `agent-rollback-plan` as another next public proof project once a GitHub remote can be created.

Rationale:

- Serious agent workflows need a rollback answer, especially for CI, deploy, database, config, and security changes.
- A diff-derived rollback packet makes operational risk reviewable before merge.
- The project extends the reliability stack from "did it pass?" to "can we undo it safely?"

## 2026-06-02 - Build Runbook Drift Checks for Agent Repos

Use `runbook-drift-check` as another next public proof project once a GitHub remote can be created.

Rationale:

- Agent-ready repos rely on README, AGENTS.md, and runbook instructions staying true to executable reality.
- Local links, path references, and script commands often drift after automation changes.
- A dependency-free checker that flags missing paths and broken script references reinforces the profile's evidence-led reliability story.
