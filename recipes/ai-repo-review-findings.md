# AI Repo Review Findings

Use this recipe when Codex, Claude Code, or another repo-aware agent should review a diff and return only the issues that matter.

## When To Use It

- Pull request review.
- Pre-merge self-review after an AI edit.
- Daily automation that touches code and docs.
- Any repo where "LGTM" is less useful than one concrete bug report.

## Review Goal

Return the smallest set of findings that would change the merge decision.

A good review does not summarize the diff first. It finds:

- bugs,
- regressions,
- missing verification on risky changes,
- security or data-loss risks,
- scope drift that weakens the change.

## Input Packet

Give the agent:

- base branch or target branch,
- changed files,
- diff or commit range,
- relevant repo rules,
- test/build command if one exists.

Without that packet, most review output becomes generic.

## Agent Prompt Pattern

```text
Review this repo change like a strict senior engineer.

Focus on findings that would change whether the diff should merge.
Look for:
- correctness bugs,
- behavioral regressions,
- missing tests for risky logic,
- security or data handling mistakes,
- accidental scope expansion.

Rules:
- Findings first, ordered by severity.
- Use file paths and line references when possible.
- Do not pad with praise or a change summary before findings.
- If there are no meaningful findings, say that explicitly.
- Do not invent tests or runtime evidence.

For each finding, include:
1. What is wrong.
2. Why it matters in behavior, not style.
3. What condition triggers it.
4. The smallest credible fix.
```

## Severity Ladder

Use a tight ladder so the output stays decision-oriented:

- `P0`: data loss, security exposure, or broken release path.
- `P1`: user-visible bug or major logic error likely in normal use.
- `P2`: edge-case bug, regression risk, or missing guard on important code.
- `P3`: maintainability issue only if it is likely to cause a near-term bug.

If an item is only preference, omit it.

## Review Loop

1. Read the changed files and nearby code, not only the patch.
2. Ask what behavior changed for the user, caller, or automation.
3. Check invariants: auth, persistence, state transitions, empty states, error paths, cleanup.
4. Compare the claimed verification with the actual risk of the diff.
5. Write only findings that survive a "would I block merge on this?" test.

## Fast Checklist

Run this against each risky file:

- Can this branch now return the wrong value?
- Can this silently skip an error or cleanup step?
- Does the new path differ from existing local patterns?
- Was a public interface changed without updating all callers?
- Was a guard, fallback, or validation removed?
- Does the test coverage match the blast radius?
- Could the automation now publish or delete the wrong thing?

## Output Pattern

```text
P1 - Missing guard lets maintenance-only runs commit
File: scripts/commit_daily_update.sh

The script commits whenever any tracked file changes, so a regenerated index can satisfy the daily publish rule without a substantive artifact.
This matters because the repo policy says useful artifact first, maintenance second.
It triggers when an automation edits only README indexes or similar generated files.
Smallest fix: require at least one non-index artifact path before allowing commit.
```

## No-Findings Rule

If nothing is worth blocking or revising, say:

```text
No findings. I checked correctness, regression risk, and verification scope for the touched files. Residual risk: untested runtime paths if the build/tests were not run.
```

That is better than inventing low-signal comments.

## Failure Modes

- Reviewing the patch without reading adjacent code.
- Confusing style preferences with merge-blocking defects.
- Claiming a test gap on a trivial text-only change.
- Writing vague findings with no trigger condition.
- Hiding the only real issue below a long summary.
