# Decisions

## 2026-06-03 - Require Concrete Pointers in Source Grounding

Use `agent-source-grounding check --require-sources --require-concrete` when
agent-written Markdown or JSON will become public proof, decisions, review
packets, closeouts, or profile claims.

Rationale:

- Source-shaped prose can make claims look grounded while leaving reviewers
  nothing to inspect.
- Concrete pointers should include URLs, file paths, command/log evidence, run
  IDs, job/artifact IDs, issue/PR references, receipts, reports, transcripts,
  or commits.
- JSON and text output should expose `concrete_source_count` so reviewers can
  scan grounding strength quickly.
- Placeholder citations and missing evidence remain separate blockers.
- This hardens an existing selected repo without increasing the root proof
  table.

## 2026-06-03 - Require Concrete Sources in Memory Audits

Use `agent-memory-audit --fail-on medium` when reused memory contains
current-state or external claims that should be backed by inspectable evidence.

Rationale:

- Source-shaped prose such as `Sources: manual note` can make stale memory look
  safer than it is.
- Current-state claims should point at reusable evidence such as URLs, files,
  command/log outputs, run IDs, issues/PRs, receipts, reports, or commits.
- Source lookup should stay bound to the same Markdown paragraph or list item
  so evidence from one memory entry cannot cover the next.
- JSON and Markdown summaries should expose concrete source counts for quick
  review.
- This hardens an existing selected repo without increasing the root proof
  table.

## 2026-06-03 - Require Approval Evidence in Tool-Call Audits

Use `agent-tool-call-audit --require-approval` when a saved tool-call history
contains sensitive tools or external action commands.

Rationale:

- Post-run review should distinguish local verification from actions that send,
  delete, deploy, publish, push, charge, or touch credentials.
- Sensitive actions should carry explicit approval, permission, authorization,
  or receipt evidence in the run history before the closeout is trusted.
- The audit should count approval-required calls and calls with approval
  evidence so reviewers can see the authority surface quickly.
- Approval evidence should not suppress normal sensitive-tool review; it only
  proves that an authority marker was present.
- This hardens an existing selected repo without increasing the root proof
  table.

## 2026-06-03 - Hash Redacted Artifacts Before Public Proof

Use `agent-artifact-redactor --manifest` when a redacted proof artifact should
be attached to a public note, recipe, run ledger, or review packet.

Rationale:

- Redaction should leave a reviewable receipt, not only a transformed file.
- Source and redacted SHA-256 values let reviewers connect the sanitized copy
  to the local source without publishing the source artifact.
- Requiring `--write-dir` with `--manifest` avoids manifests that point at
  redacted artifacts that were never written.
- The manifest should summarize rules and severity counts without echoing the
  sensitive value that triggered a finding.
- This hardens an existing safety repo without increasing the root proof table.

## 2026-06-03 - Validate Tool Input Examples

Use `agent-tool-schema-lint` to check `input_examples`, `inputExamples`, or
`examples` before a JSON tool catalog becomes callable by a coding agent.

Rationale:

- Tool examples are part of the agent-facing interface, not only
  documentation.
- Examples should include required fields, avoid closed-schema extras, respect
  simple JSON types, and use declared enum values.
- Missing examples should stay visible as weak guidance, while schema-drifting
  examples should block medium-strict gates.
- The report should expose example counts so reviewers can scan interface
  quality quickly.
- This hardens an existing selected repo without increasing the root proof
  table.

## 2026-06-03 - Hash Worktree Snapshots Before Agent Runs

Use `agent-worktree-guard --expect-snapshot-sha256` when a dirty-worktree
baseline is reused after a coding-agent run.

Rationale:

- Worktree guards depend on the pre-agent snapshot being the same artifact
  captured before edits begin.
- A changed snapshot can hide protected user edits and make a later guard
  report look safer than it is.
- Printing and requiring a snapshot SHA-256 connects the pre-run handoff to the
  post-run guard result.
- Snapshot hashes should prove baseline integrity, not authorize unexpected
  dirty paths or protected-file drift.
- This hardens an existing selected repo without increasing the root proof
  table.

## 2026-06-03 - Verify Proof Packets in Scope Guards

Use `agent-scope-guard --proof-packet` when scope reports should show
structured packet evidence for the same changed paths.

Rationale:

- Scope verdicts should stay derived from explicit path and glob allowlists.
- Proof packets can show which checks already exist for changed paths, but only
  after schema, verdict, missing-evidence, passing-check, and diff-alignment
  checks pass.
- Invalid, incomplete, missing-evidence, failing-check, or diff-mismatched
  packets should fail before their checks are reused in scope reports.
- Packet checks should never authorize unexpected paths or widen task scope.
- This hardens an existing selected repo without increasing the root proof
  table.

## 2026-06-03 - Verify Proof Packets in Diff Splits

Use `agent-diff-splitter --proof-packet` when split plans should show
structured packet evidence beside matching split files.

Rationale:

- Split order should stay derived from risk-first lanes, not from broad proof
  claims.
- Proof packets can show which checks already exist for files in each split,
  but only after schema, verdict, missing-evidence, passing-check, and
  diff-alignment checks pass.
- Invalid, incomplete, missing-evidence, failing-check, or diff-mismatched
  packets should fail before their checks are reused in split plans.
- Packet checks should never reorder lanes, merge splits, or mark risky splits
  as safe.
- This hardens an existing selected repo without increasing the root proof
  table.

## 2026-06-03 - Verify Proof Packets in Diff Budgets

Use `agent-diff-budget --proof-packet` when budget reports should show
structured packet evidence beside matching changed files.

Rationale:

- Diff-budget verdicts should stay derived from file count, line volume, and
  high-risk file count.
- Proof packets can show which checks already exist for changed files, but only
  after schema, verdict, missing-evidence, passing-check, and diff-alignment
  checks pass.
- Invalid, incomplete, missing-evidence, failing-check, or diff-mismatched
  packets should fail before their checks are reused in budget reports.
- Packet checks should never raise limits or remove budget failures.
- This hardens an existing selected repo without increasing the root proof
  table.

## 2026-06-03 - Verify Proof Packets in Review Findings

Use `agent-review-finding-check --proof-packet` when review findings should
show structured packet evidence beside matching file references.

Rationale:

- Review-finding quality should stay derived from the comments themselves:
  severity, file lines, impact, actionability, vague language, and diff
  membership.
- Proof packets can show which checks already exist for files mentioned by a
  finding, but only after schema, verdict, missing-evidence, passing-check, and
  diff-alignment checks pass.
- Invalid, incomplete, missing-evidence, failing-check, or diff-mismatched
  packets should fail before their checks are reused in finding reports.
- This hardens an existing selected repo without increasing the root proof
  table.

## 2026-06-03 - Verify Proof Packets in Review Maps

Use `agent-review-map --proof-packet` when review-lane routing should show
structured packet evidence beside matching lane files.

Rationale:

- Review lanes, owners, questions, and handoff order should stay derived from
  the diff.
- Proof packets can show which checks already exist for lane files, but only
  after schema, verdict, missing-evidence, passing-check, and diff-alignment
  checks pass.
- Invalid, incomplete, missing-evidence, failing-check, or diff-mismatched
  packets should fail before their checks are reused in review routing.
- This hardens an existing selected repo without increasing the root proof
  table.

## 2026-06-03 - Verify Proof Packets in Release Notes

Use `agent-release-note-check --proof-packet` when release notes make
verification claims from structured proof evidence.

Rationale:

- Release-note coverage findings should stay derived from the diff and note,
  especially for breaking, security, dependency, CI, test, and docs-only risks.
- Proof packets can support verification claims such as `fully tested`, but
  only after schema, verdict, missing-evidence, passing-check, and diff-alignment
  checks pass.
- Invalid, incomplete, missing-evidence, failing-check, or diff-mismatched
  packets should fail before their checks are reused in release notes.
- This hardens an existing selected repo without increasing the root proof
  table.

## 2026-06-03 - Verify Failed Command Receipts in Retry Guards

Use `agent-retry-guard --receipt` when retry-loop evidence spans failed command
receipts instead of one plain transcript.

Rationale:

- Repeated failure detection should not trust copied logs when hashed command
  receipts are available.
- Receipt status must be `fail`; passing, missing, empty, or drifted evidence
  should fail before retry-loop scoring.
- Receipt paths in the report make repeated failures easier to audit across
  separate agent turns.
- This hardens an existing selected repo without increasing the root proof
  table.

## 2026-06-03 - Verify Failed Command Receipts in CI Failure Packets

Use `agent-ci-failure-packet --receipt` when retry context should be generated
from a failed command receipt instead of loose copied CI logs.

Rationale:

- CI retry packets should prove which command failed before another agent uses
  the log as debugging context.
- Receipt status must be `fail`; passing, missing, empty, or drifted evidence
  should not produce retry packets.
- Size and SHA-256 checks keep copied CI logs from becoming stale hidden state.
- This hardens an existing selected repo without increasing the root proof
  table.

## 2026-06-03 - Audit Proof Packets in Dependency Review

Use `agent-dependency-guard --proof-packet` to show which required dependency
checks already have structured packet evidence.

Rationale:

- Dependency findings should stay derived from the diff, especially for
  floating versions, direct URLs, install scripts, and missing lockfiles.
- Reviewers still need to see which dependency checks have evidence attached.
- Invalid, incomplete, missing-evidence, or diff-mismatched packets should fail
  before their checks are reused in dependency review.

## 2026-06-03 - Audit Proof Packets in Change Risk

Use `agent-change-risk --proof-packet` to show which diff-derived review gates
already have structured packet evidence.

Rationale:

- Risk level and required gates should remain derived from the diff, not from a
  broad proof packet.
- Reviewers still need to see which recommended gates have evidence attached.
- Invalid, incomplete, missing-evidence, or diff-mismatched packets should fail
  before their checks are reused in risk routing.

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

## 2026-06-02 - Build Acceptance Trace as Closeout Proof

Use `agent-acceptance-trace` as another public proof project for criterion-level
closeout review.

Rationale:

- Task contracts and handoff briefs improve pre-run clarity, but reviewers still
  need to check whether each acceptance criterion received evidence after the
  diff exists.
- A trace matrix is more useful than a confident final answer because it exposes
  `covered`, `partial`, and `missing` criteria.
- The project stays dependency-free, local-first, testable, and reusable across
  proof packets, claim checks, merge readiness, and run ledgers.

## 2026-06-02 - Promote Agent Task Contract as Primary Proof

Add `agent-task-contract` to the profile's selected work once the public repository is created, pushed, verified, and reachable.

Rationale:

- It closes the pre-run gap in the agent reliability stack: task clarity before repo readiness, review packets, verification, and ledgers.
- The repo is small, dependency-free, testable, and has a clear user-facing CLI with JSON automation output.
- Public proof is now stronger than a TODO entry because the repo, commit, CI badge, raw source, tests, and self-scan are reachable.

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

## 2026-06-02 - Promote Diff to Eval as Learning Loop Proof

Add `diff-to-eval` to selected work once the public repo is created, hardened, pushed, and verified.

Rationale:

- It extends the profile from one-off verification toward reusable agent evaluation cases.
- It is backed by a dependency-free CLI, tests, sample diff, CI, and `repo-flightcheck` at `100/100`.
- It makes the agent workflow story more complete: task, repo, review, verification, eval, and ledger.

## 2026-06-02 - Build Secret Sentinel as Agent Diff Safety Proof

Use `agent-secret-sentinel` as another next public proof project once a GitHub remote can be created.

Rationale:

- Agent-generated diffs can accidentally include copied tokens, webhook secrets, private keys, or realistic sample credentials.
- A local diff scanner fits the profile's safety narrative because it blocks obvious leaks before commit or publication.
- The project is intentionally narrow: dependency-free, diff-only, and explicit that it is a preflight rather than a full security audit.

## 2026-06-02 - Build Dependency Guard as Supply-Chain Review Proof

Use `agent-dependency-guard` as another public proof project for dependency
surface changes in coding-agent diffs.

Rationale:

- Dependency changes alter trust boundaries even when tests pass.
- Coding agents often add libraries, broad version ranges, direct URLs, or
  install scripts to solve narrow tasks without preserving review context.
- A dependency-specific diff gate strengthens the profile's safety narrative
  without claiming vulnerability intelligence or relying on external feeds.

## 2026-06-03 - Make Profile Proof Audit Strict by Explicit Opt-In

Keep `profile-proof-audit` informational by default, but add explicit CI gate
flags for score thresholds and warnings.

Rationale:

- Reviewers need a readable profile proof report while drafting or inspecting
  changes.
- CI needs a non-zero exit path when the public profile falls below a stated
  proof bar.
- Putting the threshold in the command is clearer than burying the policy in
  prose or relying on maintainers to interpret a report manually.

## 2026-06-03 - Preserve Command Receipts in Run Ledgers

Teach `agent-run-ledger` to import and verify `agent-command-receipt.v1`
artifacts as command evidence.

Rationale:

- Command claims are weak when they exist only as closeout prose.
- Receipt files carry evidence hashes, but they are easier to review when they
  become part of the same durable run ledger as decisions, blockers, CI, and
  review-packet imports.
- Drifted or missing evidence should keep strict ledger review open instead of
  letting a stale command claim look closed.

## 2026-06-03 - Verify Proof Packets in PR Briefs

Teach `agent-pr-brief` to accept `agent-proof-packet.v1` JSON only after
checking packet completeness, passing checks, missing evidence, and diff
alignment.

Rationale:

- PR descriptions are reviewer-facing, so stale proof packets can make a weak
  handoff look verified.
- The PR brief checker already compares description text with the diff; packet
  evidence should obey the same current-diff contract.
- Exposing packet status in Markdown and JSON reports keeps the proof visible
  instead of hidden behind a filename.

## 2026-06-03 - Verify Proof Packets in Acceptance Traces

Teach `agent-acceptance-trace` to accept `agent-proof-packet.v1` JSON only after
checking packet completeness, passing checks, missing evidence, and diff
alignment.

Rationale:

- Acceptance criteria are the task contract, so stale packet evidence can make
  a criterion look covered when the current diff does not support it.
- The trace already joins task criteria, diff evidence, and closeout text;
  structured proof packets should enter that matrix only after validation.
- Exposing packet status beside criterion status keeps acceptance review
  inspectable instead of relying on a separate artifact name.

## 2026-06-03 - Verify Proof Packets in Test Impact

Teach `agent-test-impact` to accept `agent-proof-packet.v1` JSON only after
checking packet completeness, passing checks, missing evidence, and diff
alignment.

Rationale:

- Broad test passes are useful, but they should not be mistaken for direct
  source-level test evidence.
- Test-impact review already separates direct, partial, and missing evidence;
  packet-backed checks belong in `partial` unless a related changed test exists.
- Exposing packet status in Markdown and JSON keeps broad verification evidence
  inspectable inside the same report.

## 2026-06-03 - Verify Closeout Commands With Receipts

Teach `agent-claim-check` to accept verified `agent-command-receipt.v1`
artifacts as command evidence for closeout claims.

Rationale:

- `--ran-command` is compatible and lightweight, but it is still a manually
  supplied string.
- Receipt-backed command evidence lets the claim checker reject stale, missing,
  empty, non-pass, or drifted command output.
- The same receipt can then be preserved by `agent-run-ledger`, keeping closeout
  verification and durable run evidence aligned.

## 2026-06-02 - Audit Agent Safety Layer Repo Targets

Apply the same owned, unique, and label-matching repo-target checks to the
`Agent Safety Layer` table that already protect `Selected Work`.

Rationale:

- The safety section is now a first-read proof surface, not just supporting context.
- External links or duplicated repo targets would inflate or blur the agent-safety claim.
- Label-to-slug matching keeps visible repo names honest when reviewers skim the profile.

## 2026-06-03 - Require Linked Repo Rows on Proof Tables

Require every root README row in `Selected Work` and `Agent Safety Layer` to
contain a linked repository entry.

Rationale:

- A table row without a repo link looks like proof but gives reviewers no
  inspectable artifact.
- The profile is strongest when every primary proof row points to owned,
  cloneable, and already-audited work.
- Counting visible table rows against linked entries prevents accidental
  placeholder rows or copy-only claims from reaching the public surface.

## 2026-06-03 - Freeze Agent Safety Layer Growth

Keep the root README `Agent Safety Layer` at the saturated 6-row baseline unless
a future change records an explicit post-saturation growth decision.

Rationale:

- The section should prove safety judgment, not become a second Selected Work
  table.
- The current six repos already cover secrets, artifact redaction, deploy
  authorization, MCP tool control, receipt verification, and Python workflow
  integration.
- Requiring a decision before growth keeps future safety promotion deliberate
  and reviewable.

## 2026-06-03 - Fix Current Focus Shape

Keep the root README `Current Focus` section to exactly five bullets: agent
reliability, verification discipline, agent auditability, agent safety, and
product judgment.

Rationale:

- The opening profile story should be a sharp first-read summary, not a growing
  list of adjacent interests.
- Each bullet maps to a claim that the rest of the profile can prove with repos,
  examples, recipes, and verification gates.
- New focus areas should replace an existing focus deliberately or move into
  recipes, examples, or lab notes until they have stronger evidence.

## 2026-06-03 - Audit Profile Intro and CTA

Keep the root README heading, opening positioning, and public CTA fixed unless
the profile strategy is deliberately changed.

Rationale:

- The first three paragraphs decide whether a reviewer understands the profile
  before scanning the repo table.
- The opening should stay anchored on agentic engineering tools, coding-agent
  trust, and inspectable work rather than drifting into generic AI-builder copy.
- The `@manuelsampedrop` CTA is the documented public next step, so removing or
  changing it should fail the profile quality gate.

## 2026-06-02 - Audit README Section Order

Treat the root README section order as part of the executable profile quality
contract.

Rationale:

- The first read should move from focus to reviewer path, selected proof, and safety proof before the longer workflow archive.
- A future edit that buries safety or verification below supporting material would weaken the profile without breaking links.
- Enforcing canonical order keeps README navigation intentional as the public workbench grows.

## 2026-06-03 - Audit Latest Proof Index Coverage

Require every root README `Latest Proof` link under `labs/`, `recipes/`, or
`radar/` to also appear in its public folder index.

Rationale:

- A direct proof link can work while the broader public workbench becomes harder to browse.
- Latest proof should be both highlighted on the profile and discoverable from the relevant index.
- This catches index-refresh drift without adding more proof-repo volume or README churn.

## 2026-06-03 - Audit Latest Proof Shape

Keep the root README `Latest Proof` section to one lab note and three recipe
links.

Rationale:

- The profile is already saturated with repo-backed proof, so the latest-proof
  surface should stay a concise highlight, not another index.
- One lab note plus three recipes balances recent execution evidence with
  reusable workflow patterns.
- Encoding the shape in `scripts/profile_quality_audit.py` catches empty,
  recipe-only, or overgrown latest-proof edits before they reach the profile.

## 2026-06-03 - Allowlist Reviewer Path Targets

Treat the root README `Reviewer Path` links as a focused first-read allowlist,
not just a minimum set of required links.

Rationale:

- The five-minute reviewer route should stay intentional as the repo list grows.
- Extra links in the first-read path dilute the strongest reliability and safety story.
- New proof routes should move into examples or the evidence map unless the approved path is deliberately changed.

## 2026-06-02 - Build Tool Schema Lint as Agent Interface Proof

Use `agent-tool-schema-lint` as public proof for reviewing tool schemas before
they are exposed to coding agents.

Rationale:

- Tool-call risk starts before runtime authorization when names, descriptions,
  parameters, enums, and object schemas are vague.
- A dependency-free CLI gives reviewers a concrete preflight for OpenAI-style
  function tools, MCP-like `inputSchema` definitions, and local automation hooks.
- This complements `agent-context-sentinel`, `agent-tool-call-audit`, and
  `mcp-guard` by checking the agent-facing interface before a tool becomes
  callable.

## 2026-06-02 - Build Retry Guard as Failure-Loop Proof

Use `agent-retry-guard` as public proof for detecting repeated command failures
before another coding-agent run continues.

Rationale:

- Repeating the same failed command with the same error and no investigation is
  a common token-wasting failure mode in agent workflows.
- A small transcript gate makes the stop-and-investigate rule executable instead
  of relying on a human to remember it during a long run.
- This complements `agent-bug-repro`, `agent-ci-failure-packet`, and
  `agent-continuation-brief` by deciding whether a failed run is ready for
  continuation or needs a strategy shift first.

## 2026-06-02 - Promote Secret Sentinel as Safety Proof

Add `agent-secret-sentinel` to the profile's agent safety layer once the public repo is created, sanitized, pushed, and verified.

Rationale:

- It gives the profile a concrete pre-publication secret hygiene gate for agent-generated diffs.
- The publish attempt itself proved the risk: GitHub Push Protection blocked a token-shaped fixture, which was fixed rather than bypassed.
- It is backed by a dependency-free CLI, tests, examples, CI, and `repo-flightcheck` at `100/100`.

## 2026-06-02 - Build Tool Call Replay as Schema Drift Proof

Use `agent-tool-call-replay` as public proof for validating captured tool calls
against current tool schemas before reruns, proof packets, evals, or run ledgers
reuse them.

Rationale:

- Tool-call failures often come from drift between the schema an agent saw and
  the schema a reviewer is about to trust.
- `agent-tool-schema-lint` checks interface quality and `agent-tool-call-audit`
  checks risky run behavior, but neither replays recorded arguments against the
  current schema.
- A dependency-free replay validator strengthens the OpenAI-relevant agent-tool
  narrative without executing tools or claiming full JSON Schema compliance.

## 2026-06-02 - Build Release Note Check as Maintainer Workflow Proof

Use `agent-release-note-check` as public proof for auditing generated release
notes against real diffs before maintainer-facing publication.

Rationale:

- Open-source maintenance includes releases and changelogs, not only PR review
  and CI triage.
- Agent-generated release notes can omit breaking, security, dependency, CI, or
  test changes while sounding polished.
- A dependency-free diff-to-release-note checker strengthens the profile's
  maintainer workflow narrative without claiming vulnerability intelligence or
  replacing human release review.

## 2026-06-02 - Build CI Failure Packets for Agent Reruns

Use `agent-ci-failure-packet` as another next public proof project once a GitHub remote can be created.

Rationale:

- CI failure logs are often too noisy for a high-quality agent retry.
- A compact packet with failing commands, error signals, file references, and suggested checks improves the next run's context quality.
- This completes another part of the agent workflow loop: failure triage after verification fails.

## 2026-06-02 - Build Test Impact as Verification Evidence Proof

Use `agent-test-impact` as a public proof project for path-level test evidence
in coding-agent diffs.

Rationale:

- Broad test commands can pass while changed source files lack nearby test
  evidence.
- Reviewers need a deterministic way to separate direct, partial, and missing
  test evidence before accepting a closeout.
- The project stays dependency-free, local-first, testable, and aligned with
  the profile's verification discipline narrative.

## 2026-06-02 - Build Tool Call Audit as Post-Run Safety Proof

Use `agent-tool-call-audit` as a public proof project for post-run review of
coding-agent tool-call history.

Rationale:

- Pre-execution guards do not prove the actual run stayed clean.
- Reviewers need to see destructive commands, sensitive tools, repeated
  failures, skipped hooks, and secret markers before trusting a closeout.
- The project complements `mcp-guard`, `agent-run-ledger`, and
  `agent-command-receipt` without becoming a sandbox or external service.

## 2026-06-02 - Promote CI Failure Packets as Retry Proof

Add `agent-ci-failure-packet` to selected work once the public repo is created, hardened, pushed, and verified.

Rationale:

- It gives the profile a concrete answer for agent retry loops after CI failures.
- It is backed by a dependency-free CLI, sample log, tests, CI, and `repo-flightcheck` at `100/100`.
- It keeps failed verification actionable without asking the next agent to parse an entire noisy CI archive.

## 2026-06-02 - Build Rollback Plans for Agent Diffs

Use `agent-rollback-plan` as another next public proof project once a GitHub remote can be created.

Rationale:

- Serious agent workflows need a rollback answer, especially for CI, deploy, database, config, and security changes.
- A diff-derived rollback packet makes operational risk reviewable before merge.
- The project extends the reliability stack from "did it pass?" to "can we undo it safely?"

## 2026-06-02 - Promote Rollback Plans as Operational Proof

Add `agent-rollback-plan` to selected work once the public repo is created, hardened, pushed, and verified.

Rationale:

- It makes rollback review a first-class part of agent-generated changes instead of an afterthought.
- It is backed by a dependency-free CLI, realistic sample diff, tests, CI, and `repo-flightcheck` at `100/100`.
- It broadens the profile from verification to operational safety: how to undo risky diffs if the agent was wrong.

## 2026-06-02 - Build Runbook Drift Checks for Agent Repos

Use `runbook-drift-check` as another next public proof project once a GitHub remote can be created.

Rationale:

- Agent-ready repos rely on README, AGENTS.md, and runbook instructions staying true to executable reality.
- Local links, path references, and script commands often drift after automation changes.
- A dependency-free checker that flags missing paths and broken script references reinforces the profile's evidence-led reliability story.

## 2026-06-02 - Promote Runbook Drift Check as Docs Reliability Proof

Add `runbook-drift-check` to selected work once the public repo is created, hardened, pushed, and verified.

Rationale:

- It covers the operational-docs layer that agents rely on before scripts, CI, or review packets are trustworthy.
- It is backed by a dependency-free CLI, example runbook, tests, CI, and `repo-flightcheck` at `100/100`.
- It turns README, AGENTS.md, and runbook drift into a concrete blocker instead of a stale-docs surprise.

## 2026-06-02 - Build Scope Guards for Agent Diffs

Use `agent-scope-guard` as another next public proof project once a GitHub remote can be created.

Rationale:

- Agent runs should be constrained by explicit expected paths, not only by tests.
- Scope drift is a common failure mode when agents opportunistically edit docs, config, or helper files.
- A small diff-path guard makes task contracts enforceable in CI and publish scripts.

## 2026-06-02 - Promote Scope Guard as Boundary Proof

Add `agent-scope-guard` to selected work once the public repo is created, hardened, pushed, and verified.

Rationale:

- It turns task scope from a prompt instruction into an enforceable diff-path gate.
- It is backed by a dependency-free CLI, fake sample diff, tests, CI, and `repo-flightcheck` at `100/100`.
- It fills the gap between task-contract clarity and review evidence: the agent must stay inside the expected file boundary.

## 2026-06-02 - Build Closeout Evidence Checks for Agents

Use `agent-closeout-check` as another next public proof project once a GitHub remote can be created.

Rationale:

- Agent closeouts often sound confident without enough review evidence.
- A small linter can enforce summary, changed files, exact verification, and risk notes before a handoff is accepted.
- This strengthens the profile's message that AI work should close with evidence, not vibes.

## 2026-06-02 - Promote Closeout Check as Evidence Proof

Add `agent-closeout-check` to selected work once the public repo is created, hardened, pushed, and verified.

Rationale:

- It catches overconfident agent final answers before they become PR comments, handoffs, or ledger entries.
- It is backed by a dependency-free CLI, good and bad closeout fixtures, tests, CI, and `repo-flightcheck` at `100/100`.
- It closes the workflow loop: task scope, changed-path boundaries, verification, rollback risk, and final evidence.

## 2026-06-02 - Build Change Risk Matrix for Agent Diffs

Use `agent-change-risk` as another next public proof project once a GitHub remote can be created.

Rationale:

- The reliability stack needs a routing layer that decides which gates apply before a reviewer runs everything by default.
- Changed paths are enough to identify many high-value risk categories: CI, database, release, security, configuration, documentation, and tests.
- A dependency-free CLI that produces a risk packet connects the existing local tools into a coherent pre-merge workflow.

## 2026-06-02 - Promote Change Risk Matrix as Gate Routing Proof

Add `agent-change-risk` to selected work once the public repo is created, hardened, pushed, and verified.

Rationale:

- It decides which proof gates should run from changed paths before a reviewer treats a diff as safe.
- It is backed by a dependency-free CLI, realistic sample diff, tests, CI, and `repo-flightcheck` at `100/100`.
- It connects existing tools into a coherent pre-merge routing layer.

## 2026-06-02 - Build Merge Readiness Gate for Agent Diffs

Use `agent-merge-readiness` as another next public proof project once a GitHub remote can be created.

Rationale:

- A reviewer needs a merge decision, not only a list of suggested gates.
- Agent closeouts should be checked against explicit evidence: passing checks, changed files, rollback coverage, risks, and blockers.
- A dependency-free CLI that returns `ready`, `needs-review`, or `blocked` makes agent handoffs stricter without requiring a hosted service.

## 2026-06-02 - Promote Merge Readiness as Verdict Proof

Add `agent-merge-readiness` to selected work once the public repo is created, hardened, pushed, and verified.

Rationale:

- It turns the output of risk routing, checks, and closeout evidence into a strict merge verdict.
- It is backed by a dependency-free CLI, non-ready exit-code semantics, tests, CI, examples, and `repo-flightcheck` at `100/100`.
- It completes the handoff loop between "which gates apply?" and "is this safe enough to proceed?"

## 2026-06-02 - Build Proof Packets for Agent Review

Use `agent-proof-packet` as another next public proof project once a GitHub remote can be created.

Rationale:

- Useful agent work should leave a compact review artifact, not scattered claims across chat, logs, and CI.
- A proof packet connects changed files, checks, evidence files, risks, decisions, open questions, and a verdict.
- Keeping it dependency-free makes it easy to run locally, in CI, or before appending to an agent run ledger.

## 2026-06-02 - Promote Proof Packets as Review Evidence

Add `agent-proof-packet` to selected work once the public repo is created, hardened, pushed, and verified.

Rationale:

- It consolidates scattered agent evidence into one Markdown or JSON artifact a reviewer can inspect.
- It is backed by a dependency-free CLI, non-complete exit-code semantics, relative evidence paths, tests, CI, examples, and `repo-flightcheck` at `100/100`.
- It connects merge readiness, closeout evidence, risks, decisions, and ledger import into one handoff artifact.

## 2026-06-02 - Build Publish Queues for Local Agent Repos

Use `agent-publish-queue` as another next public proof project once a GitHub remote can be created.

Rationale:

- A strong profile can still drift if local proof repos, remotes, TODOs, and public README claims are not kept in sync.
- The current blocker is GitHub repo creation for many committed local tools, so a queue makes that blocker explicit and auditable.
- A dependency-free CLI can scan local Git state and optional public HTTP status without storing credentials or inventing access.

## 2026-06-02 - Promote Publish Queue as Public Surface Sync Proof

Add `agent-publish-queue` to selected work once the public repo is created, hardened, pushed, and verified.

Rationale:

- It makes the remaining local-to-public publication backlog auditable instead of relying on memory or manual TODO scanning.
- It is backed by a dependency-free CLI, tests, sample report, CI, and `repo-flightcheck` at `100/100`.
- It keeps README claims, TODO blockers, GitHub remotes, and public proof status aligned before profile promotion.

## 2026-06-02 - Build Profile Proof Audits

Use `profile-proof-audit` as another next public proof project once a GitHub remote can be created.

Rationale:

- A polished AI-builder profile needs a repeatable proof check, not only manual taste edits.
- The audit verifies required sections, selected-work shape, latest proof, relative links, optional HTTP status, and unsupported claim language.
- This keeps the profile honest while new local projects wait for GitHub repo creation.

## 2026-06-02 - Promote Profile Proof Audit as Profile Quality Gate

Add `profile-proof-audit` to selected work once the public repo is created, hardened, pushed, and verified.

Rationale:

- It turns profile polish into a repeatable audit instead of a subjective README pass.
- It is backed by a dependency-free CLI, tests, CI, example profile, and `repo-flightcheck` at `100/100`.
- It reinforces the profile's credibility by checking required sections, links, latest proof, table shape, and unsupported claim language.

## 2026-06-02 - Build Eval Runners for Agent Proof Artifacts

Use `agent-eval-runner` as another next public proof project once a GitHub remote can be created.

Rationale:

- `diff-to-eval` creates cases from real diffs, but the workflow needs a runner that checks later proof artifacts against those cases.
- A transparent local scorer is better than model-only judgment for regression coverage of files, checks, risks, and expected outcomes.
- This completes the profile's eval-loop story: real diff, saved case, scored artifact, and auditable result.

## 2026-06-02 - Promote Agent Eval Runner as Regression Proof

Add `agent-eval-runner` to selected work once the public repo is created, hardened, pushed, and verified.

Rationale:

- It closes the eval loop by checking whether later proof artifacts still cover saved `diff-to-eval` cases.
- It is backed by a dependency-free CLI, tests, example case and candidate, CI, and `repo-flightcheck` at `100/100`.
- It keeps the profile's agent-quality story concrete: real diff, saved case, scored proof artifact, and auditable pass/fail.

## 2026-06-02 - Build Decision Guards for Agent Diffs

Use `agent-decision-guard` as another next public proof project once a GitHub remote can be created.

Rationale:

- Agent-generated changes can alter CI, automation, config, security, product scope, or future agent behavior without leaving a durable rationale.
- A small diff guard can enforce `DECISIONS.md` and `TODO.md` updates before reviewers accept decision-worthy changes.
- This strengthens the profile's reliability story by covering intent preservation, not only tests and closeout evidence.

## 2026-06-02 - Promote Decision Guard as Intent Preservation Proof

Add `agent-decision-guard` to selected work once the public repo is created, hardened, pushed, and verified.

Rationale:

- It blocks decision-worthy agent diffs when durable rationale or follow-up tracking is missing.
- It is backed by a dependency-free CLI, tests, examples including explicit no-follow-up waiver handling, CI, and `repo-flightcheck` at `100/100`.
- It fills the gap between scope control and audit trails: future maintainers can see why CI, automation, config, product, or agent-instruction behavior changed.

## 2026-06-02 - Build Diff Budgets for Agent Reviews

Use `agent-diff-budget` as another next public proof project once a GitHub remote can be created.

Rationale:

- Agent diffs can be technically correct but too broad for one honest review pass.
- A budget gate covers size and complexity, which scope guards and risk classifiers do not enforce by themselves.
- Keeping the tool dependency-free and diff-only makes it easy to run before proof packets, merge readiness, or CI promotion.

## 2026-06-02 - Promote Diff Budget as Reviewability Proof

Add `agent-diff-budget` to selected work once the public repo is created, hardened, pushed, and verified.

Rationale:

- It turns oversized agent diffs into a concrete blocker before reviewers skip files or accept a polished closeout.
- It is backed by a dependency-free CLI, small and large diff examples, tests, CI, and `repo-flightcheck` at `100/100`.
- It complements scope and risk tools by measuring changed-file count, line volume, high-risk file count, and review questions.

## 2026-06-02 - Build Review Maps for Agent Handoffs

Use `agent-review-map` as another next public proof project once a GitHub remote can be created.

Rationale:

- Agent proof packets still need routing: a mixed diff should not be reviewed as one flat unit.
- Mapping files into security, data, release, automation, agent-instruction, product/docs, tests, and application lanes makes review ownership explicit.
- A dependency-free diff mapper fits the profile's reliability story by turning agent handoffs into concrete reviewer questions instead of generic confidence.

## 2026-06-02 - Promote Review Map as Handoff Routing Proof

Add `agent-review-map` to selected work once the public repo is created, hardened, pushed, and verified.

Rationale:

- It turns a flat mixed diff into concrete review lanes, owners, questions, and handoff order.
- It is backed by a dependency-free CLI, mixed diff example, tests, CI, and `repo-flightcheck` at `100/100`.
- It complements scope, budget, decision, and risk tools by making review ownership explicit before proof packets or merge readiness.

## 2026-06-02 - Build Claim Checks for Agent Closeouts

Use `agent-claim-check` as another next public proof project once a GitHub remote can be created.

Rationale:

- Agent final answers can have the right sections and still overclaim tests, files, or risk posture.
- Comparing closeout text against the diff and command evidence adds a stricter evidence layer than structure-only closeout linting.
- A dependency-free local checker supports the profile's core message: AI work should be trusted only when claims are tied to inspectable proof.

## 2026-06-02 - Promote Claim Check as Closeout Evidence Proof

Add `agent-claim-check` to selected work once the public repo is created, hardened, pushed, and verified.

Rationale:

- It checks final-answer claims against changed files, exact commands, explicit command evidence, and risky-path/no-risk contradictions.
- It is backed by a dependency-free CLI, good and weak closeout examples, tests, CI, and `repo-flightcheck` at `100/100`.
- It complements closeout shape checks by validating whether the final answer's claims match inspectable evidence before proof packets or PR comments reuse them.

## 2026-06-02 - Build Diff Split Plans for Oversized Agent Changes

Use `agent-diff-splitter` as another next public proof project once a GitHub remote can be created.

Rationale:

- Blocking oversized diffs is useful only if the next action is concrete.
- A split planner turns broad agent diffs into ordered review slices by security, data, release, automation, tests, application, and docs.
- Keeping it diff-only and dependency-free makes it easy to pair with budget checks, scope guards, review maps, and proof packets.

## 2026-06-02 - Promote Diff Splitter as Oversized Diff Recovery Proof

Add `agent-diff-splitter` to selected work once the public repo is created, hardened, pushed, and verified.

Rationale:

- It turns an oversized diff blocker into concrete next slices with order, files, line counts, rationale, and reviewer questions.
- It is backed by a dependency-free CLI, mixed diff example, tests, CI, and `repo-flightcheck` at `100/100`.
- It complements diff budgets by giving reviewers and the next agent run an actionable split plan instead of a vague "make it smaller" instruction.

## 2026-06-02 - Select Latest Lab Proof by Git Addition Time

Use git addition time, not filename order, when selecting the root README's latest lab note.

Rationale:

- Multiple lab notes can share the same date prefix.
- Filename order can keep an older same-day note on the profile after a newer note is published.
- Matching the recipe selection logic makes `Latest Proof` reflect the most recently added public artifact.

## 2026-06-02 - Promote Cross-Tool Agent Loops With Public Evidence

When a flagship repo change connects two or more public agent tools, document the loop as a lab note or recipe only after the commit, CI run, local checks, and raw public files are verified.

Rationale:

- Cross-tool workflows are stronger profile proof than isolated README improvements.
- The profile should show how repo readiness, review packets, verification plans, and ledgers compose into a reliable agent workflow.
- Requiring public links and verification keeps the workbench from drifting into speculative architecture notes.

## 2026-06-02 - Build Command Receipts for Agent Evidence

Use `agent-command-receipt` as another public proof project for command evidence before closeout claims are reused.

Rationale:

- Agent final answers and proof packets need more than copied terminal text when a command result becomes review evidence.
- A small receipt with command status, exit code, timestamp, and evidence file hashes makes drift visible before the receipt is reused.
- Keeping it dependency-free makes it suitable for local handoffs, CI artifacts, proof packets, and ledger import without requiring hosted infrastructure.

## 2026-06-02 - Promote Command Receipt as Evidence Hash Proof

Add `agent-command-receipt` to selected work once the public repo is created, browser-published, cloned, locally verified, and its GitHub Actions run succeeds.

Rationale:

- It strengthens the profile's closeout-evidence story by tying command claims to hashed files rather than trust in wording.
- It is backed by a dependency-free CLI, example receipt, tests, local smoke checks, fresh public clone verification, and GitHub Actions success.
- It complements `agent-claim-check`, `agent-proof-packet`, and `agent-run-ledger` by making command evidence reusable without hiding file drift.

## 2026-06-02 - Build Worktree Guard for User Change Protection

Use `agent-worktree-guard` as another public proof project for protecting pre-existing user edits during coding-agent runs.

Rationale:

- Coding agents often work in dirty repositories where user drafts, notes, or partial edits must not be touched.
- Scope guards catch final changed paths, but they do not prove that pre-existing dirty files stayed intact.
- A dependency-free snapshot/check CLI gives the workflow a concrete stop condition before accidental user-change loss becomes a cleanup problem.

## 2026-06-02 - Promote Worktree Guard as Dirty-State Proof

Add `agent-worktree-guard` to selected work once the public repo is created, browser-published, cloned, locally verified, and its GitHub Actions run succeeds.

Rationale:

- It fills a real reliability gap: protecting user-owned dirty state before and after an agent run.
- It is backed by a dependency-free CLI, example snapshot, tests, local smoke checks, fresh public clone verification, and GitHub Actions success.
- It complements `agent-scope-guard` by checking protected dirty files and unexpected dirty paths before review packets or closeout claims are trusted.

## 2026-06-02 - Restore Terminal GitHub SSH Publishing

Load `~/.ssh/id_ed25519_github_codex` into `ssh-agent` when terminal GitHub pushes fail with `Permission denied (publickey)`.

Rationale:

- The SSH key already existed and was associated with the no-reply GitHub identity, but `ssh-agent` had no identities loaded.
- Loading the key restored `git@github.com` authentication as `manuelsampedro1`.
- Terminal pushes are materially safer and faster than browser-authenticated file-by-file publication for future proof repos.

## 2026-06-02 - Build Agent Instruction Audit for Repo Readiness

Use `agent-instruction-audit` as another public proof project for checking the quality of coding-agent instruction files.

Rationale:

- Repo readiness is weak if it only checks whether `AGENTS.md` exists.
- Bad instruction files can authorize broad cleanup, secrets mishandling, skipped tests, or vague "be helpful" behavior before any agent sees the task.
- A dependency-free audit CLI makes instruction quality inspectable before repo-flightcheck, review packets, or handoffs rely on it.

## 2026-06-02 - Promote Agent Instruction Audit as Readiness Proof

Add `agent-instruction-audit` to selected work once the public repo is created, pushed by terminal SSH, cloned, locally verified, and its GitHub Actions run succeeds.

Rationale:

- It gives the profile a concrete quality gate for the instruction layer behind Codex-style repo work.
- It is backed by a dependency-free CLI, examples, tests, smoke checks, editable install, public clone verification, `repo-flightcheck` at `100/100`, and GitHub Actions success.
- It complements `repo-flightcheck` by making the agent-instructions rule deeper than file existence.

## 2026-06-02 - Build Agent Repo Map as Context Proof

Use `agent-repo-map` as another public proof repo for pre-run coding-agent handoffs.

Rationale:

- Task contracts cover intent, but agents also need a compact map of repo terrain before changing files.
- The tool fills a practical gap between task definition, repo readiness, instruction audit, and review packets.
- It is dependency-free, bounded, testable, CI-backed, and verified with `repo-flightcheck` at `100/100`.

## 2026-06-02 - Build Agent Handoff Brief as Pre-Run Prompt Proof

Use `agent-handoff-brief` as another public proof repo for converting task contracts and repo context into a concrete coding-agent prompt.

Rationale:

- A task contract and a repo map are stronger when the next agent receives them as one actionable handoff.
- The tool reduces guessing before execution by surfacing required reading, commands, verification, risk paths, gaps, and closeout expectations.
- It is dependency-free, testable, CI-backed, published by terminal SSH, and verified with `repo-flightcheck` at `100/100`.

## 2026-06-02 - Build Memory Audit as Agent Context Hygiene Proof

Use `agent-memory-audit` as another public proof repo for checking long-lived
agent memory before it is reused as context.

Rationale:

- Agent memory can preserve useful decisions, but it can also preserve stale
  auth claims, outdated "current" facts, public-action shortcuts, local paths,
  or credential-handling mistakes.
- A local audit gate is stronger than trusting a future agent to notice stale
  context inside a long memory file.
- The project is dependency-free, testable, CI-backed, published by terminal
  SSH, and verified with `repo-flightcheck` at `100/100`.

## 2026-06-02 - Build Context Sentinel as Prompt-Injection Preflight Proof

Use `agent-context-sentinel` as another public proof repo for screening
untrusted context before it is passed to a coding-agent handoff.

Rationale:

- Repo maps and handoff briefs help agents work faster, but retrieved or copied
  context can still contain override instructions, hidden authority claims,
  secret exfiltration requests, dangerous commands, or unattended action
  shortcuts.
- A local context gate makes that risk visible before the next agent sees the
  text as task authority.
- The project is dependency-free, testable, CI-backed, published by terminal
  SSH, and verified with `repo-flightcheck` at `100/100`.

## 2026-06-02 - Build Artifact Redactor as Public-Proof Hygiene

Use `agent-artifact-redactor` as another public proof repo for cleaning logs,
transcripts, proof packets, and command artifacts before they are published.

Rationale:

- Agent proof workflows need evidence, but copied evidence can include auth
  headers, secret-looking assignments, contact details, local paths, SSH paths,
  or JWT-like values.
- Diff secret scanning is not enough because lab notes, review packets,
  transcripts, and run ledgers can leak sensitive content outside a Git diff.
- A dependency-free local redactor keeps the publication loop safer without
  uploading artifact content or pretending to be a full DLP system.

## 2026-06-02 - Build Bug Repro as Debugging Handoff Proof

Use `agent-bug-repro` as another public proof repo for converting vague bug
reports into reproducible debugging handoffs before another agent starts work.

Rationale:

- The profile already covers CI failures, rollback risk, proof packets, and
  closeout checks, but a lot of debugging waste starts earlier with a weak bug
  report.
- A dependency-free bug-report audit makes missing repro steps, expected versus
  actual behavior, environment, evidence, regression context, and vague wording
  visible before the next agent guesses at root cause.
- The tool complements CI failure packets by handling human bug reports and
  local evidence, not only post-CI logs.

## 2026-06-02 - Build Continuation Brief as Long-Run Handoff Proof

Use `agent-continuation-brief` as another public proof repo for preserving
task state when long-running coding-agent work spans multiple runs.

Rationale:

- Pre-run handoff briefs are not enough when the next agent inherits partial
  work, previous commands, changed files, blockers, and residual uncertainty.
- Continuation notes should preserve the original objective instead of
  redefining the task around whatever is easiest to finish.
- The tool is dependency-free, testable, CI-backed, published by terminal SSH,
  and verified with `repo-flightcheck` at `100/100`.

## 2026-06-02 - Build Request Brief as Raw-Ask Clarification Proof

Use `agent-request-brief` as another public proof repo for converting raw,
messy human requests into scoped coding-agent briefs before execution starts.

Rationale:

- Task contracts are stronger when the raw user ask has already been audited
  for objective, scope, acceptance criteria, constraints, context, verification,
  risks, and next actions.
- Some requests include external outcomes such as hiring, prizes, approvals, or
  public perception; these must stay residual uncertainty instead of being
  treated as agent-verifiable completion.
- The tool is dependency-free, testable, CI-backed, published by terminal SSH,
  and verified with `repo-flightcheck` at `100/100`.

## 2026-06-02 - Build Context Budget as Handoff Quality Proof

Use `agent-context-budget` as another public proof repo for keeping coding-agent
handoffs within an explicit context budget before another run starts.

Rationale:

- Repo maps, handoff briefs, continuation notes, and context-injection checks
  cover what context means, but not whether the bundle is too large,
  duplicative, or low-signal for the next agent.
- A local budget gate makes context pressure visible as a keep, summarize, or
  drop plan instead of hoping the next model spends attention on the right
  files.
- The tool is dependency-free, testable, CI-backed, published by terminal SSH,
  and verified with `repo-flightcheck` at `100/100`.

## 2026-06-02 - Build Handoff Drift as Live-State Proof

Use `agent-handoff-drift` as another public proof repo for checking handoff and
continuation notes against the repository state the next agent will actually
inherit.

Rationale:

- A handoff can be well scoped and still stale: files can be deleted, the branch
  or HEAD can change, the worktree can become dirty, or command-success claims
  can lose their evidence.
- The next agent should not have to infer whether a note still matches the repo.
  A local drift gate catches concrete contradictions before more context is
  spent on a false state.
- The tool is dependency-free, testable, CI-backed, published by terminal SSH,
  and verified with `repo-flightcheck` at `100/100`.

## 2026-06-02 - Build PR Brief as Review Surface Proof

Use `agent-pr-brief` as another public proof repo for checking PR descriptions
against the real diffs they summarize.

Rationale:

- Reviewers usually read the PR description before the code. A vague or
  incomplete description can hide risky files, weak verification, or oversized
  changes behind a confident summary.
- A local PR-description gate keeps the public review surface tied to changed
  files, risk paths, explicit verification, and concrete language.
- The tool is dependency-free, testable, CI-backed, published by terminal SSH,
  and verified with `repo-flightcheck` at `100/100`.

## 2026-06-02 - Build Plan Trace as Execution Evidence Proof

Use `agent-plan-trace` as another public proof repo for tracing completed agent
plan items against diffs, command logs, and closeout evidence.

Rationale:

- Plans help coordinate multi-step agent work, but they can become theater if
  completed items are not checked against real execution evidence.
- Pending or in-progress plan items should not disappear behind a confident
  final answer.
- The tool is dependency-free, testable, CI-backed, published by terminal SSH,
  and verified with `repo-flightcheck` at `100/100`.

## 2026-06-02 - Build Review Finding Check as Review Quality Proof

Use `agent-review-finding-check` as another public proof repo for auditing the
quality of coding-agent review findings before they are sent to humans.

Rationale:

- Review packets and review maps improve context, but the actual findings still
  need concrete severity, file lines, impact, evidence, and actionability.
- Vague review comments waste reviewer attention and make agent review quality
  harder to trust.
- The tool is dependency-free, testable, CI-backed, published by terminal SSH,
  and verified with `repo-flightcheck` at `100/100`.

## 2026-06-02 - Pause Proof Repo Volume After Saturation

Treat new proof-repo creation as exceptional until the profile needs a
materially new workflow gap rather than another adjacent agent-quality tool.

Rationale:

- The public profile already has 46 Selected Work rows and profile proof audit
  holds at `100/100` with no issues or warnings.
- More rows can weaken first-read clarity even when each repo is individually
  useful.
- The next strongest signal is curation, cross-repo demonstrations, hardening,
  and real workflow evidence, not volume for its own sake.

## 2026-06-03 - Freeze Selected Work Row Count After Saturation

Keep the root README `Selected Work` table at the saturated 46-row baseline
unless a future change records an explicit `Allow Selected Work Growth After
Saturation` decision.

Rationale:

- The profile is already dense enough that adding rows can reduce reviewer
  clarity even when the new repo is useful.
- A hard gate makes the pause rule executable instead of relying on future
  maintenance judgment under pressure.
- New signal should come from curation, examples, verification, and materially
  new workflow gaps before increasing the primary proof table.

## 2026-06-03 - Audit Profile Narrative Anchors

Require the root README `Current Focus` and `Public Workbench` sections to keep
their core narrative and discoverability anchors.

Rationale:

- A profile can keep all required sections while quietly losing the first-read
  story that makes the proof stack coherent.
- The current strongest narrative is reliability, verification, auditability,
  safety, and product judgment, backed by labs, recipes, examples, radar, and
  the automation runbook.
- Encoding those anchors in `scripts/profile_quality_audit.py` prevents future
  maintenance from preserving the shell of the README while weakening its
  reviewer path.

## 2026-06-03 - Cap Workflow Archive Growth

Keep the root README `How I Work With Codex` section at 18 bullets or fewer.

Rationale:

- The section already links the full workflow stack and has enough depth for a
  reviewer who wants more than the five-minute route.
- Adding more bullets would make the README behave like another index and
  weaken the profile's curation discipline.
- New workflow routes should move into recipes, examples, or the evidence map
  instead of expanding the root first-read surface.

## 2026-06-02 - Prefer Cross-Repo Workflow Demos After Saturation

Use examples that chain existing proof repos together when the profile needs
more signal but not more project volume.

Rationale:

- Mature agent workflows depend on sequencing: risk routing, release-note
  coverage, merge readiness, proof packets, and ledgers have different jobs.
- A cross-repo demo shows judgment about how the tools work together instead of
  only listing tool names.
- The first useful demo is release readiness because it exposes a concrete
  reviewer trap: a complete proof packet can coexist with a `needs-review`
  merge-readiness verdict when scope or residual-risk evidence is missing.

## 2026-06-02 - Add Durable Run Evidence Chain

Document a cross-repo handoff chain from review packet to verification envelope
to run ledger.

Rationale:

- A serious agent workflow needs more than a final answer; it needs durable
  evidence that survives outside the chat transcript.
- `codex-review-packet`, `verify-by-change`, and `agent-run-ledger` already
  support this sequence, and the profile should show how they compose.
- The demo intentionally preserves a strict-doctor non-ready state when planned
  checks remain open, which is stronger than pretending every generated packet
  means the run is complete.

## 2026-06-02 - Add Reviewer Path Before Selected Work

Add a short reviewer path near the top of the README so evaluators can inspect
the strongest workflow evidence before scanning the full Selected Work table.

Rationale:

- The profile now has enough public proof that discoverability is the main
  first-read risk.
- A five-minute path through readiness, review context, verification, ledger,
  and safety repos is clearer than asking a reviewer to infer the narrative
  from 46 rows.
- The path links to cross-repo examples so the claim is backed by composition,
  not only repo names.

## 2026-06-02 - Add Profile Evidence Map

Add a claim-to-evidence map so external reviewers can audit the profile by
assertion rather than by repo count.

Rationale:

- The profile now needs traceability between public claims and inspectable
  artifacts.
- A claim map makes it easier to challenge or verify readiness, review context,
  verification, ledger, safety, merge-readiness, release, CI, and rollback
  claims.
- This reinforces the "evidence before claims" principle without adding another
  proof repo.

## 2026-06-02 - Make Profile Quality Audit Executable

Add `scripts/profile_quality_audit.py` and run it from profile verification.

Rationale:

- First-read quality is now part of the profile's correctness, not just a taste
  preference.
- The audit checks reviewer-path placement, evidence-map coverage, required
  examples, saturation control, and risky unsupported README language.
- Integrating it into `make test`, `make lint`, and `make build` turns the
  weekly quality guard into an executable gate instead of a manual reminder.

## 2026-06-02 - Test Profile Quality Audit Failure Modes

Add unit coverage for the executable profile quality gate.

Rationale:

- A quality gate without negative tests can quietly become decorative.
- The tests prove the current profile passes and that missing reviewer-path or
  saturation-curation evidence fails.
- This keeps first-read quality and curation discipline enforceable in CI.

## 2026-06-02 - Warn on Residual Local Changes After Publish

Keep the maintenance publish flow from silently leaving scratch files behind.

Rationale:

- Whole-directory staging intentionally ignores unmanaged scratch paths outside
  public profile surfaces.
- A successful commit can still leave local files that confuse the next
  automation run or reviewer.
- A non-failing warning preserves publish momentum while making residual local
  state visible.

## 2026-06-02 - Audit the README Verification Contract

Keep the public verification section tied to the gates that actually run.

Rationale:

- The README is part of the profile proof surface; stale verification copy
  weakens trust even when the checks themselves pass.
- The profile now runs shell syntax checks, Python unit tests, a commit-script
  shell fixture, index drift checks, latest-proof sync, and the profile quality
  audit.
- Encoding those expectations in `scripts/profile_quality_audit.py` makes future
  verification changes visible instead of relying on manual copy review.

## 2026-06-02 - Audit External GitHub Automation Prompts

Keep scheduled GitHub profile automations aligned with the exact-path publish
contract.

Rationale:

- The repo publish script now blocks unexpected public-path changes, but the
  active lab, recipe, maintenance, and quality-audit automation prompts also
  need to tell future runs to pass exact changed paths.
- A small local prompt audit catches stale automation wording without requiring
  the public CI environment to have access to the user's Codex automation
  folder.
- This closes a real automation drift risk without adding another proof repo or
  changing the public Selected Work surface.

## 2026-06-02 - Audit Local Proof Repo Git Identity

Make Git author identity checks repeatable before local proof repos are pushed
or promoted.

Rationale:

- Public proof repos should be authored with the documented GitHub no-reply
  identity, not an accidental local or placeholder email.
- The current sibling proof repos already use the expected identity, but that
  check was previously ad hoc.
- A versioned local audit script keeps the check reusable without storing
  credentials or requiring a new public proof repo.

## 2026-06-02 - Cap Reviewer Path Length

Keep the root README Reviewer Path short enough to work as a first-read route,
not as another index.

Rationale:

- The profile already has a dense Selected Work table, examples, labs, and
  recipes; the top-level reviewer path should reduce scan cost.
- A short route through core reliability, safety, and composition evidence is
  stronger than adding every new proof repo to the opening section.
- Encoding the cap in `scripts/profile_quality_audit.py` keeps future profile
  maintenance from quietly trading clarity for volume.

## 2026-06-02 - Reject Duplicate Selected Work Rows

Keep each root README Selected Work repo target unique.

Rationale:

- With 46 rows, an accidental duplicate would look like padding even if every
  individual repo remains useful.
- The profile is stronger when each row buys a distinct proof surface rather
  than repeating a link under slightly different wording.
- Encoding duplicate detection in `scripts/profile_quality_audit.py` protects
  curation discipline during future profile maintenance.

## 2026-06-02 - Keep Selected Work Owned

Limit the root README Selected Work table to owned `manuelsampedro1` GitHub
repositories.

Rationale:

- The primary proof table should show shipped work that a reviewer can attribute
  directly to this account.
- External tools, references, or ecosystem notes are still useful, but they
  belong in recipes, lab notes, or radar instead of the main proof surface.
- Encoding the ownership rule in `scripts/profile_quality_audit.py` prevents a
  future maintenance pass from diluting the profile with borrowed credibility.

## 2026-06-02 - Match Selected Work Labels to Repo Slugs

Require each visible root README Selected Work repo label to match the GitHub
repo slug it links to.

Rationale:

- A mismatched label can make the profile look sloppy or misleading even when
  the link is reachable and owned.
- Reviewers should not need to hover links to know which repository a row
  represents.
- Encoding this in `scripts/profile_quality_audit.py` keeps the primary proof
  table inspectable as it changes over time.

## 2026-06-03 - Keep Primary Proof Links at Repo Roots

Require each root README `Selected Work` and `Agent Safety Layer` repo link to
point at the canonical owned repository root.

Rationale:

- Primary proof rows should send reviewers to cloneable repo fronts, not a
  branch, issue list, file, or docs subpage.
- Subpage links can still be useful inside examples, recipes, and lab notes,
  but they make the primary proof table less stable and harder to skim.
- Encoding repo-root enforcement in `scripts/profile_quality_audit.py` keeps the
  profile's highest-signal links direct and inspectable.

## 2026-06-03 - Audit External Reviewer Navigation

Keep the external reviewer navigation example concrete as the profile proof
surface grows.

Rationale:

- The profile now has enough proof that scan cost is a real review risk.
- The reviewer example should preserve a five-minute route through the core
  reliability loop, safety layer, composition examples, and review prompt.
- Encoding the route in `scripts/profile_quality_audit.py` prevents future
  maintenance from turning the example into generic profile copy or another
  unbounded index.

## 2026-06-03 - Audit Public Surface Tone

Keep public profile-workbench artifacts focused on inspectable proof instead of
external validation or approval-chasing requests.

Rationale:

- The strongest profile signal is shipped, verifiable work; public notes should
  not preserve casual outcome-chasing language after the lesson is captured.
- The root README already rejects unsupported hype, but lab notes and recipes
  also shape reviewer trust.
- A narrow public-surface tone audit catches these phrases without blocking
  legitimate technical references to agent tooling or provider-style schemas.
- Approval should be earned by evidence and reviewer navigation, not requested
  inside public artifacts.

## 2026-06-03 - Audit Public Relative Links

Keep public profile-workbench Markdown links resolvable inside this repo unless
they intentionally point to external URLs.

Rationale:

- Labs, recipes, docs, examples, and radar pages are reviewer-facing proof, so
  broken local links create avoidable trust friction.
- A broad public-surface link audit catches drift outside the root README and
  `Latest Proof` highlight.
- Code examples are ignored so snippets that show upstream README Markdown do
  not become false positives.

## 2026-06-03 - Audit Examples Index Coverage

Require every public example Markdown file to be linked from
`examples/README.md`.

Rationale:

- Examples are the profile's compact proof-packet layer; hidden examples reduce
  reviewer navigation quality even when the files exist.
- Labs, recipes, and radar already have generated indexes, but examples are
  curated manually and need an executable coverage check.
- Encoding index coverage in `scripts/profile_quality_audit.py` keeps future
  examples discoverable without expanding the root README.

## 2026-06-03 - Audit Public Markdown H1 Structure

Require each public Markdown page in the profile workbench to have exactly one
real page H1, while ignoring fenced code examples.

Rationale:

- The public workbench uses generated indexes that derive titles from page H1s;
  missing or repeated H1s make navigation and anchors less reliable.
- Recipe templates sometimes need to show Markdown snippets with their own H1s,
  so the audit must ignore fenced code instead of flattening useful examples.
- Encoding the rule in `scripts/profile_quality_audit.py` keeps public notes,
  recipes, docs, examples, and radar pages structurally consistent.

## 2026-06-03 - Generate Public Docs Index

Add a generated `docs/README.md` index and expose it from the root
`Public Workbench` section.

Rationale:

- The repo already generated indexes for labs, recipes, and radar, but public
  docs still relied on scattered direct references.
- Profile strategy and priority-topic docs are useful reviewer context when
  discoverable, but they should not expand the root README.
- Generating and verifying the docs index keeps operating docs visible while
  preserving the curated first-read profile surface.

## 2026-06-03 - Audit Public Folder Index Coverage

Require every public Markdown file under `docs`, `examples`, `labs`, `radar`,
and `recipes` to be linked from its folder index.

Rationale:

- The public workbench is only useful if reviewers can navigate it from stable
  indexes instead of discovering files by repository search.
- Generated indexes already prevent drift during local verification, but the
  profile quality audit should catch hidden public artifacts directly.
- Applying one rule across all public folders keeps labs, recipes, radar,
  examples, and operating docs equally discoverable.

## 2026-06-03 - Allow Selected Work Growth After Saturation

Add `agent-start-gate` as a single post-saturation `Selected Work` exception.

Rationale:

- It covers a real workflow gap before the first edit: deciding whether a
  coding-agent run should start based on objective, scope, inputs, worktree,
  context, verification, and stop conditions.
- The repo is public, dependency-free, tested, has CI, and passed
  `repo-flightcheck --check-remote` at `100/100` before profile promotion.
- Growth remains constrained; this decision documents this specific addition
  rather than reopening the profile to unbounded repo volume.

## 2026-06-03 - Promote Agent Output Contract as Structured Evidence Proof

Add `agent-output-contract` as a second post-saturation `Selected Work`
exception.

Rationale:

- It covers a distinct automation boundary: checking JSON outputs before CI,
  ledgers, review packets, or profile proof reuse them as evidence.
- The repo is public, dependency-free, tested, has CI, and passed
  `repo-flightcheck --check-remote` at `100/100` before profile promotion.
- It strengthens the agent-tooling story without duplicating pre-run, scope,
  review, or closeout gates already present in the profile.

## 2026-06-03 - Promote Agent Evidence Chain as Cross-Artifact Proof

Add `agent-evidence-chain` as a third post-saturation `Selected Work`
exception.

Rationale:

- It covers a different failure mode from individual output validation: multiple
  valid artifacts can still disagree about task, repository, or commit.
- The repo is public, dependency-free, tested, has CI, and passed
  `repo-flightcheck --check-remote` at `100/100` before profile promotion.
- It keeps the profile focused on inspectable agent reliability by validating a
  proof chain before review packets, ledgers, or closeouts reuse it.

## 2026-06-03 - Promote Agent Source Grounding as Claim Evidence Proof

Add `agent-source-grounding` as the final 50-row `Selected Work` exception.

Rationale:

- It covers a distinct review failure mode: agent-written Markdown or JSON can
  sound useful while its claims lack sources, evidence, or inspectable links.
- The repo is public, dependency-free, tested, has CI, and passed
  `repo-flightcheck --check-remote` at `100/100` before profile promotion.
- Reaching the 50-row cap should stop root proof-table growth; future work
  should harden, combine, or curate the existing public stack.

## 2026-06-03 - Audit Latest Proof Freshness

Require the root README `Latest Proof` links to match the newest public lab note
and the three newest public recipes.

Rationale:

- A highlight can be valid, indexed, and correctly shaped while still pointing
  at older proof after a newer lab note or recipe ships.
- Matching the same Git-add-time ordering used by the refresh script keeps the
  first-read profile surface tied to the newest public evidence.
- This improves profile maintenance without adding another root proof row.

## 2026-06-03 - Audit Evidence Map Canonical Links

Require `examples/profile-evidence-map.md` to link each primary claim repo to
its canonical owned GitHub repo root.

Rationale:

- A claim map can look complete if it mentions repo names, while still leaving a
  reviewer without direct proof links.
- Canonical repo-root links make the capability map inspectable and avoid
  drifting into branch, file, issue, or plain-text references.
- This strengthens the profile's review path without growing the root proof
  table.

## 2026-06-03 - Require Strict Command Receipt Verification for Proof Reuse

Prefer strict `agent-command-receipt verify` gates before a receipt is reused as
passing proof.

Rationale:

- Hash integrity and pass readiness are different claims; a failed receipt can
  be historically valid while still unsuitable for a passing closeout.
- `--require-status pass` makes the required command outcome explicit.
- `--min-evidence 1` prevents empty receipts from satisfying proof workflows.
- This hardens an existing visible repo without adding another root proof row.

## 2026-06-03 - Verify Command Receipts in Proof Packets

Teach `agent-proof-packet` to verify `agent-command-receipt.v1` artifacts before
using them as passing review evidence.

Rationale:

- A proof packet should not turn a command claim into a review artifact without
  checking the receipt behind it.
- Receipt-backed packets keep command status, evidence hashes, and drift
  findings visible in the review packet.
- Failed, skipped, missing, empty, or drifted receipts now block the packet
  instead of letting a weak pass-check string carry the review.
- This strengthens an existing selected repo without growing the root proof
  table.

## 2026-06-03 - Verify Proof Packets Before Merge Readiness

Teach `agent-merge-readiness` to verify `agent-proof-packet.v1` artifacts before
using packet checks as merge evidence.

Rationale:

- A proof packet can be stale, blocked, or generated for a different diff.
- Merge readiness should import packet checks only after the packet verdict is
  `complete` and its changed files match the current diff.
- Mismatched or incomplete proof packets now block the merge gate instead of
  quietly supplying checks.
- This hardens an existing selected repo without increasing the root proof
  table.

## 2026-06-03 - Verify Proof Packets in Closeout Checks

Teach `agent-closeout-check` to verify `agent-proof-packet.v1` artifacts before
using packet evidence to support a final answer.

Rationale:

- A closeout can cite a proof packet that is incomplete, stale, or missing
  evidence.
- Final-answer review should still require an exact verification section while
  allowing a complete packet to supply changed-path evidence.
- Closeout checks should fail when cited files are not covered by the packet.
- This hardens an existing selected repo without increasing the root proof
  table.

## 2026-06-03 - Trace Proof Packets in Agent Plans

Teach `agent-plan-trace` to verify `agent-proof-packet.v1` artifacts before
using packet evidence to support completed plan items.

Rationale:

- A completed plan item can be backed by a stale or incomplete proof packet.
- Plan tracing should accept structured packet evidence only when the packet is
  `complete`, has passing checks, carries changed-file evidence, and has no
  missing evidence.
- When a diff is provided, packet changed files should match the diff before
  supporting the trace.
- This hardens an existing selected repo without increasing the root proof
  table.
