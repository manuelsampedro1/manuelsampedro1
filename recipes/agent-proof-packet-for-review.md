# Agent Proof Packet for Review

Use this when a coding-agent change has multiple evidence fragments and a reviewer needs one compact handoff.

## Use When

- The final answer, diff, checks, rollback notes, and risk notes are scattered.
- A PR needs a clear evidence section.
- A run ledger needs a durable summary of what was actually verified.
- You want to distinguish "agent says done" from "reviewer has proof".

## Goal

Create one review packet with:

- changed files,
- check results,
- evidence links,
- risks,
- decisions,
- open questions,
- missing evidence,
- final verdict.

## Workflow

1. Capture the diff:

```sh
git diff -- . > /tmp/agent-change.diff
```

2. Save the closeout or readiness output:

```sh
pbpaste > /tmp/agent-closeout.md
```

3. Build the proof packet:

```sh
agent-proof-packet /tmp/agent-change.diff \
  --title "Deploy workflow migration" \
  --check "scope guard:pass" \
  --check "unit tests:pass" \
  --check "secret scan:pass" \
  --risk "Deploy workflow permissions changed; rollback plan required." \
  --decision "Kept the migration narrow and documented rollback." \
  --evidence "closeout:/tmp/agent-closeout.md"
```

4. Paste the Markdown output into the PR or attach the JSON output to a run ledger.

## Verdict Rules

| Verdict | Meaning |
| --- | --- |
| `complete` | At least one passing check exists, evidence is attached, no blockers remain. |
| `needs-review` | Evidence is missing or reviewer questions are still open. |
| `blocked` | At least one check failed. |

## Prompt Pattern

```text
Create a review proof packet for this coding-agent change.

Inputs:
- Diff: <paste or path>
- Checks: <name:status>
- Evidence files: <label:path>
- Risks: <risk notes>
- Decisions: <decision notes>
- Open questions: <questions>

Rules:
- Do not claim checks passed unless they are explicitly listed.
- Treat failed checks as blockers.
- Treat missing evidence files as not ready.
- Keep the packet short enough for a PR comment.
- Include changed files and missing evidence.
```

## Fast Checklist

- Does the packet name changed files?
- Are checks explicit and statused?
- Are evidence files attached and readable?
- Are risks and decisions separated?
- Are open questions visible instead of buried?
- Does the verdict follow the evidence?

## Failure Modes

- Rewriting a confident final answer instead of collecting proof.
- Collapsing risks and decisions into one vague summary.
- Omitting failed or skipped checks.
- Linking evidence files that do not exist.
- Calling the packet complete while reviewer questions remain open.

## Source Linkage

- Repo / tool / workflow: local `agent-proof-packet` prototype at `/Users/manuelsampedro/Documents/Codex/2026-05-21/agent-proof-packet`.
- Supporting prompt, script, or note: [`./merge-readiness-gate-for-agent-diffs.md`](./merge-readiness-gate-for-agent-diffs.md), [`./closeout-evidence-check-for-agents.md`](./closeout-evidence-check-for-agents.md), and [`./flagship-repo-proof-packet.md`](./flagship-repo-proof-packet.md).
