# 2026-05-25 - Runbook Drift in Agent Repo Automation

## Context

This repo documents a clear maintenance promise in [`docs/automation-runbook.md`](../../docs/automation-runbook.md): when a newer public artifact exists, maintenance should refresh the root [`README.md`](../../README.md) latest links.

I wanted to verify the executable behavior instead of trusting the prose, because coding-agent repos often drift when the runbook and the shell scripts stop matching.

## Experiment Setup

I used a temporary local clone of this repo so the test would not affect the working copy:

- removed `origin` to avoid any accidental push,
- configured a valid local Git identity,
- added one new dated lab file under `labs/2026/`,
- ran [`scripts/commit_daily_update.sh`](../../scripts/commit_daily_update.sh) with a short test message.

The key question was whether the commit flow would update both discovery surfaces:

- [`labs/README.md`](../../labs/README.md)
- the root [`README.md`](../../README.md) "Latest Proof" section

## Findings

- The commit script does refresh [`labs/README.md`](../../labs/README.md) automatically.
- The same run does not refresh the root [`README.md`](../../README.md) latest lab note link.
- The resulting temp-clone commit contained only the new lab file and `labs/README.md`.
- A separate temp-clone pass without Git identity stopped before commit, which confirms the identity guard is real and still works.

This means the runbook currently describes a stronger maintenance behavior than the script actually enforces.

## Why It Matters for Coding Agents

This is a practical failure mode for Codex or Claude Code workflows: an agent that reads the runbook can reasonably infer that "publish the new lab note" also updates the profile surface. Today that inference would be false.

The broader pattern is useful: for agent repos, treat shell scripts as the operational contract and markdown runbooks as intent until both are verified together.

## Source Linkage

- Repo / tool / workflow: this profile repo's daily publish flow
- Supporting prompt, script, or file: [`scripts/commit_daily_update.sh`](../../scripts/commit_daily_update.sh), [`docs/automation-runbook.md`](../../docs/automation-runbook.md), and [`README.md`](../../README.md)

## Verification

Local verification completed for this note:

- temp clone run 1: missing Git identity blocked commit with the expected instructions,
- temp clone run 2: a new lab artifact produced a local commit,
- that commit changed only the new lab note and `labs/README.md`,
- after the successful run, the root `README.md` still pointed to `2026-05-24` as the latest lab note.

## Next Step

Either teach [`scripts/commit_daily_update.sh`](../../scripts/commit_daily_update.sh) to refresh the root latest links, or narrow the claim in [`docs/automation-runbook.md`](../../docs/automation-runbook.md) so the written policy matches the executable one.
