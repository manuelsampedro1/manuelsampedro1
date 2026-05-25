# Executable Runbook Drift Check

Use this when a repo has both agent-facing docs and shell automation, and you need to know whether the written runbook still matches what the scripts actually do.

## Use When

- A repo has `README.md`, runbooks, or `AGENTS.md` that describe publish behavior.
- Codex or Claude Code is expected to follow those docs without human correction.
- You suspect the scripts and the docs may have drifted.
- You need one reusable note or fix instead of another vague "automation cleanup".

## Goal

Turn documentation claims into executable checks, then decide whether to patch the script, narrow the docs, or publish the drift as a lab note.

## Inputs

- One or two markdown files that describe the workflow.
- The real script entrypoint, usually under `scripts/`.
- One safe temp clone so you can test without touching the working copy.
- Three to five observable claims, such as:
  - which files should update,
  - what should block the run,
  - what should be committed,
  - what should happen when `origin` is missing.

## Workflow

1. Pull exact claims out of the docs. Rewrite each one as `condition -> observable result`.
2. Pick the smallest command that exercises the real workflow. Avoid fake stubs if the actual script is safe to run in a temp clone.
3. Clone the repo into a temp directory and remove `origin` before the first run.
4. Run one negative-path check first: missing Git identity, missing remote, or surface-only diff.
5. Run one positive-path check with a minimal substantive artifact such as a new recipe or lab note.
6. Inspect both stdout and the resulting changed files or commit contents.
7. Mark each claim as `matched`, `drifted`, or `blocked by setup`.
8. Fix the smaller side of the contract:
   - patch the script if the docs are right and behavior is wrong,
   - patch the docs if the script is the intended behavior.

## Temp Clone Pattern

```bash
tmp="$(mktemp -d)"
git clone . "$tmp/repo"
git -C "$tmp/repo" remote remove origin || true

# Optional positive-path identity for local-only verification
git -C "$tmp/repo" config user.name "Test User"
git -C "$tmp/repo" config user.email "test@example.com"
```

If the workflow includes a required failure mode, unset one prerequisite on purpose before the first run.

## Agent Prompt Pattern

```text
Audit this repo for runbook drift.

Inputs:
- docs that describe the workflow: <paths>
- executable entrypoint: <script path>
- claims to verify:
  1. <condition -> expected result>
  2. <condition -> expected result>
  3. <condition -> expected result>

Tasks:
1. Convert each claim into a concrete local check.
2. Use a temp clone when the script could commit or push.
3. Run one negative-path scenario and one positive-path scenario.
4. Compare the documented behavior against stdout, changed files, and commit contents.
5. Return only:
   - matched claims,
   - drifted claims,
   - the smallest credible fix,
   - verification actually run.

Rules:
- Do not trust the prose over the script.
- Do not claim a path was verified if it was not executed.
- If setup blocks a scenario, report the exact blocker instead of inferring the outcome.
```

## Fast Checklist

- Did you test the actual entrypoint instead of rephrasing the docs?
- Did you isolate the run in a temp clone before any commit-capable command?
- Did you verify both a rejection path and a success path?
- Did you compare the final changed files, not only the terminal output?
- Can you name the smallest diff that would remove the drift?

## Evaluation Pattern

Score each item `0` or `1`:

- Claims are written as observable behaviors.
- Negative path was executed.
- Positive path was executed.
- Result is backed by changed files, commit contents, or exact stdout.
- Fix recommendation patches one side of the contract only once.

`5`: publish the note or patch.
`4`: publish if the drift is already clearly reproducible.
`0-3`: gather one more real run before publishing.

## Output Pattern

```text
Claim checked: "A new artifact refreshes the root latest links"
Result: drifted
Evidence: the run updated labs/README.md but left README.md unchanged
Smallest fix: teach scripts/commit_daily_update.sh to refresh root latest links, or narrow the runbook claim
Verification: temp clone run with local identity and origin removed
```

## Failure Modes

- Trusting the runbook and never executing the script.
- Testing only the happy path.
- Looking only at stdout and missing the wrong files in the commit.
- Patching both docs and scripts at once so the real source of drift stays unclear.
- Using the working repo instead of a disposable clone for commit-capable automation.

## Source Linkage

- Repo / tool / workflow: this profile repo's publish automation.
- Supporting prompt, script, or note: [`../labs/2026/2026-05-25-runbook-drift-in-agent-repo-automation.md`](../labs/2026/2026-05-25-runbook-drift-in-agent-repo-automation.md), [`../labs/2026/2026-05-24-publish-gate-matrix-for-ai-repo-automation.md`](../labs/2026/2026-05-24-publish-gate-matrix-for-ai-repo-automation.md), and [`../scripts/commit_daily_update.sh`](../scripts/commit_daily_update.sh).
