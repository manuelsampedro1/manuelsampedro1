# Automation Runbook

This repo is designed for daily useful GitHub contributions around AI tooling and coding-agent work.

## Daily Streams

- 09:05 Madrid, `GitHub AI Lab Note`: create or improve one technical note under `labs/`.
- 14:10 Madrid, `GitHub AI Recipe`: add one reusable workflow, prompt, checklist, or implementation pattern under `recipes/`.
- 20:20 Madrid, `GitHub Profile Maintenance`: refresh public indexes, update README links or TODO status when they materially change, and commit/push any useful changes.

## Intensity Target

Default target: produce two substantive public artifacts per day across the lab and recipe streams, then use maintenance to tighten discoverability or backlog only when something genuinely improved.

Prefer:

- one artifact from a real Codex workflow, bug, review, or repo automation run,
- one supporting artifact that turns that work into a reusable prompt, checklist, or pattern,
- small follow-up maintenance only after the artifact work is done.

Do not chase volume with generic notes. More intense means more concrete, more reusable, and closer to actual Codex work.

## Codex Focus

Bias daily output toward artifacts that help with work done inside Codex:

- repo review workflows and findings patterns,
- debugging loops and failure-mode notes,
- prompt patterns for scoped edits, planning, and verification,
- agent memory, automation, and runbook patterns,
- AGENTS.md structures, guardrails, and repo setup decisions,
- small scripts or templates that reduce friction in repeat tasks.

## Artifact Linkage

Every new public note or recipe should declare what real work it came from.

Accepted anchors:

- a public repo URL,
- a concrete local script or tool path,
- a specific lab note or decision file,
- a real workflow prompt or verification command,
- a shipped case or working demo.

If a draft cannot point to one of those anchors, do not publish it yet.

## Promotion Eligibility

An artifact can be promoted to the root `README.md` or the `Selected Work` surface only if all of these are true:

- it links to owned proof such as a public repo, working tool, or verified case,
- it includes a real verification section,
- it would still be useful if separated from the profile repo,
- it supports the client-facing story more than a more concrete repo would.

## Quality Guard

- Monday 10:15 Madrid, `GitHub Profile Quality Audit`: review recent automated contributions and flag or fix drift toward generic filler.

The audit should also check:

- too much meta-content versus repo-backed proof,
- artifacts that do not link back to real work,
- weak README promotions,
- drift away from the client-facing narrative.
- first-read quality with `python3 scripts/profile_quality_audit.py --root . --min-score 100`.
- strict profile proof gates with `profile-proof-audit --min-score 100 --fail-on-warnings` when profile or public-proof changes need a non-zero CI failure instead of an informational report.
- command-evidence integrity with `agent-command-receipt` plus `agent-run-ledger import-receipt` when a closeout relies on important local command output.
- command-receipt proof reuse with `agent-command-receipt verify --require-status pass --min-evidence 1` before a receipt supports a passing closeout, ledger entry, review packet, or claim-check result.
- proof-packet command evidence with `agent-proof-packet --receipt --receipt-base-dir` when a review packet should carry verified command output instead of a manual pass-check string.
- retry-loop receipt evidence with `agent-retry-guard --receipt` when repeated failed commands should be checked from failed, non-empty, hash-verified command receipts.
- CI-failure receipt evidence with `agent-ci-failure-packet --receipt` when retry context should be generated only from a failed, non-empty, hash-verified command receipt.
- acceptance-trace packet evidence with `agent-acceptance-trace --proof-packet` when acceptance criteria rely on structured proof packets and should fail on incomplete or diff-mismatched packets.
- test-impact packet evidence with `agent-test-impact --proof-packet` when broad test checks should appear as partial evidence and fail on incomplete or diff-mismatched packets.
- change-risk packet evidence with `agent-change-risk --proof-packet` when recommended gates should show packet-backed evidence without reducing the diff-derived risk level.
- dependency-review packet evidence with `agent-dependency-guard --proof-packet` when required dependency checks should show packet-backed evidence without reducing dependency findings.
- release-note proof-packet evidence with `agent-release-note-check --proof-packet` when release notes make verification claims from structured packet evidence without suppressing diff-derived release findings.
- review-map proof-packet evidence with `agent-review-map --proof-packet` when review lanes should show packet-backed checks without changing diff-derived owners, questions, or handoff order.
- plan-trace packet evidence with `agent-plan-trace --proof-packet` when completed plan items depend on structured proof packets and should fail on incomplete or diff-mismatched packets.
- PR-description packet evidence with `agent-pr-brief --proof-packet` when a PR body relies on structured proof packets and should fail on incomplete or diff-mismatched packets.
- merge-readiness packet evidence with `agent-merge-readiness --proof-packet` when a merge gate should import proof-packet checks only after verifying packet verdict and diff alignment.
- closeout proof-packet evidence with `agent-closeout-check --proof-packet` when a final answer cites packet evidence and should fail on incomplete, missing-evidence, or file-misaligned packets.
- closeout-claim integrity with `agent-claim-check --receipt` when exact command claims should be backed by hashed evidence files.
- The profile heading, opening agentic-engineering positioning, and `@manuelsampedrop` CTA staying intact.
- Current Focus retaining the profile's core narrative anchors: reliability, verification, auditability, safety, and product judgment.
- Current Focus staying shaped as exactly five bullets so the opening narrative does not turn into a generic interest list.
- Canonical README section order so reviewer navigation, selected proof, and safety proof stay before the longer workflow archive.
- Public Workbench linking to labs, recipes, examples, radar, the docs index, and the automation runbook so supporting evidence remains discoverable.
- How I Work With Codex staying at 18 bullets or fewer so the workflow archive does not become another unbounded index.
- Indexed `Latest Proof` targets so root README highlights stay discoverable from the public lab, recipe, or radar indexes.
- `Latest Proof` staying shaped as one lab note and three recipe links so the highlight remains concise instead of becoming another index.
- `Latest Proof` freshness matching the newest public lab note and three newest public recipes by Git add time, with filesystem modification time only for uncommitted files.
- Reviewer Path length staying at four bullets or fewer, with extra routes moved to examples instead of the first-read README section.
- Reviewer Path links staying on the approved first-read route instead of accumulating extra proof links.
- Selected Work row-count freeze at the current 50-row cap; future useful work should improve existing repos or add examples, recipes, labs, or curation instead of another root row.
- Unique `Selected Work` repo targets so repeated links cannot inflate the proof surface.
- Owned `Selected Work` repo targets under `https://github.com/manuelsampedro1/`; external links belong in notes, recipes, or radar, not the primary proof table.
- Matching `Selected Work` labels and repo slugs so visible repo names cannot point to a different target.
- Root-level `Selected Work` and `Agent Safety Layer` repo links so primary proof rows point to cloneable repo fronts, not issues, files, branches, or docs subpages.
- Owned, unique, and correctly labelled `Agent Safety Layer` repo targets so the permission and safety surface cannot drift into external references or inflated proof.
- Linked repo entries for every `Selected Work` and `Agent Safety Layer` table row so primary proof never becomes an unclickable claim.
- `Agent Safety Layer` row-count freeze at the saturated 6-row baseline unless an explicit post-saturation growth decision is recorded.
- `examples/external-reviewer-navigation.md` keeping a concrete five-minute review path through the core loop, safety layer, composition examples, and review prompt instead of drifting into generic profile copy.
- `examples/profile-evidence-map.md` keeping the primary claim repos, including `agent-start-gate`, `agent-output-contract`, `agent-evidence-chain`, and `agent-source-grounding`, linked to canonical owned GitHub repo roots so the profile can be reviewed by capability instead of repo count.
- Public folder indexes linking every Markdown file under `docs`, `examples`, `labs`, `radar`, and `recipes` so proof packets, notes, and operating docs do not become hidden artifacts.
- Public notes, recipes, docs, radar, and examples staying free of external-validation or approval-chasing language; the profile should show useful proof, not ask for outcomes it cannot verify.
- Relative links in public notes, recipes, docs, radar, and examples resolving inside this repo, with code examples ignored so upstream Markdown snippets do not create false positives.
- Public Markdown pages keeping exactly one real page H1, with fenced code examples ignored, so indexes and reviewer anchors stay stable.

## Commit Rule

No empty commits. No timestamp-only changes. No filler.

The scripts should commit only when files changed and should push only when a remote is configured.

Current maintenance refreshes:

- `labs/README.md`
- `docs/README.md`
- `recipes/README.md`
- `radar/README.md`
- root `README.md` latest links when a newer public artifact exists
- `TODO.md` when a review checkpoint or next step genuinely changes
- `examples/` when a concrete proof packet or fixture helps verify public claims

The maintenance script should skip a run when the diff only touches those surface files.

Changes under `scripts/` are eligible for a maintenance commit when they improve artifact generation, publishing safety, or verification quality.

Changes under `tests/` are eligible when they prove a public verification gate catches both passing and failing profile states.

Before refreshing indexes or staging files, `scripts/commit_daily_update.sh` now checks managed public paths for pre-existing changes.

Pass the exact intended changed paths after the commit message so the run can distinguish the real artifact from unrelated draft work:

```sh
scripts/commit_daily_update.sh \
  "maintenance: tighten publish guard" \
  scripts/commit_daily_update.sh \
  docs/automation-runbook.md \
  DECISIONS.md \
  TODO.md
```

If the script reports unexpected public-path changes, narrow the run or move the unrelated draft work before retrying.

After a publish run, the script warns when uncommitted local changes remain so scratch files do not silently carry into the next automation run.

Audit the local GitHub automation prompts after changing them:

```sh
python3 scripts/audit_github_automation_prompts.py --format json
```

The audit expects the lab, recipe, maintenance, and quality-audit prompts to pass exact changed paths after the `scripts/commit_daily_update.sh` commit message.

Audit local proof-repo Git identity before first public pushes:

```sh
python3 scripts/audit_local_repo_identity.py --root .. --format json
```

The expected identity is `Manuel Sampedro` with `202281585+manuelsampedro1@users.noreply.github.com`.

## GitHub Setup

Remote publishing is configured for `manuelsampedro1/manuelsampedro1`.

Current remote:

```sh
git remote -v
```

Current Git identity:

```sh
git config user.name
git config user.email
```

Expected values:

```sh
Manuel Sampedro
202281585+manuelsampedro1@users.noreply.github.com
```

Manual push if an automation leaves local commits behind:

```sh
git push
```

If GitHub SSH authentication fails with `Permission denied (publickey)`, check whether the Codex GitHub key is loaded:

```sh
ssh-add -l
ssh-add ~/.ssh/id_ed25519_github_codex
ssh -T git@github.com
```

If GitHub browser authentication expires, sign in again in the browser or configure GitHub CLI. Do not put tokens in this repo.

## Automation Safety

Automations can prepare, commit, and push useful public artifacts. They should not:

- invent credentials,
- commit secrets,
- create fake contributions,
- publish private notes,
- claim tool results that were not verified.
