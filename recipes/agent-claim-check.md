# Agent Claim Check

Use this when a coding-agent closeout sounds confident and needs to be checked against actual evidence.

## Use When

- A final answer claims tests passed, risk is gone, or files changed cleanly.
- A PR comment should not rely on chat confidence alone.
- A proof packet needs to distinguish evidence from unsupported assertions.
- You have a diff and a command ledger, but the closeout may not match them.

## Goal

Compare a closeout against evidence:

- changed files from a unified diff,
- files referenced in the closeout,
- exact commands claimed in the closeout,
- commands that were actually run,
- risky paths that contradict "no risk" claims,
- strong verification claims without command evidence.

This is stricter than a closeout shape check. A closeout can have nice sections and still overclaim what was verified.

## Workflow

1. Save the diff:

```sh
git diff -- . > /tmp/agent-change.diff
```

2. Save or pipe the closeout:

```sh
PYTHONPATH=src python3 -m agent_claim_check closeout.md --diff /tmp/agent-change.diff
```

3. Pass command evidence from the run ledger or terminal transcript:

```sh
PYTHONPATH=src python3 -m agent_claim_check closeout.md \
  --diff /tmp/agent-change.diff \
  --ran-command "PYTHONPATH=src python3 -m unittest discover -s tests"
```

4. If blocked, fix the closeout or rerun verification. Do not soften the tool just to keep a confident final answer.

## Prompt Pattern

```text
Check this coding-agent closeout against the evidence.

Rules:
- Every changed file in the diff must be mentioned or intentionally excluded.
- Every verification claim needs an exact command.
- If command evidence is provided, claimed commands must match it.
- If risky paths changed, reject "no risks" unless the closeout explains the actual risk.
- Report unsupported claims before judging the work as ready.

<paste diff>
<paste closeout>
<paste command evidence>
```

## Fast Checklist

- Did the closeout mention every changed file?
- Did claimed commands match the command ledger exactly?
- Did strong claims like "all tests pass" include evidence?
- Did risky paths make "no risk" language invalid?
- Did the proof packet include claim-check output before merge readiness?

## Decision Pattern

Use the findings to decide the next move instead of treating claim check as a vague warning:

- `ready`: every changed file is covered, each verification claim has an exact command, and risky paths are either absent or explicitly discussed.
- `revise closeout`: the code change may be fine, but the final answer skipped a changed file, used fuzzy verification wording, or claimed a command that does not match the ledger.
- `rerun verification`: the closeout claims tests, lint, or deploy checks passed but no command evidence exists yet.
- `escalate review`: risky paths changed and the closeout still says `no risk`, or command evidence conflicts with the claimed result.

Minimal reviewer note:

```text
Claim check verdict: revise closeout
- Missing changed file: scripts/release.sh
- Unsupported claim: "all tests passed"
- Needed next step: rerun the exact test command or remove the claim
```

## Failure Modes

- Accepting a polished closeout that skips a changed file.
- Treating inline commands as proof they actually ran.
- Claiming "no risks" after auth, deploy, workflow, token, or migration changes.
- Letting "all tests pass" replace an exact command and result.
- Checking section shape but not checking claims against evidence.

## Source Linkage

- Public repo: <https://github.com/manuelsampedro1/agent-claim-check>
- Commit: <https://github.com/manuelsampedro1/agent-claim-check/commit/c9d6cded23fe3a069e38f7dfd9c030ec9668032f>
- README: <https://raw.githubusercontent.com/manuelsampedro1/agent-claim-check/main/README.md>
- CLI: <https://raw.githubusercontent.com/manuelsampedro1/agent-claim-check/main/src/agent_claim_check/cli.py>
- Tests: <https://raw.githubusercontent.com/manuelsampedro1/agent-claim-check/main/tests/test_cli.py>
- Sample diff: <https://raw.githubusercontent.com/manuelsampedro1/agent-claim-check/main/examples/sample.diff>
- Good closeout: <https://raw.githubusercontent.com/manuelsampedro1/agent-claim-check/main/examples/good-closeout.md>
- Weak closeout: <https://raw.githubusercontent.com/manuelsampedro1/agent-claim-check/main/examples/weak-closeout.md>
- Launch note: [`../labs/2026/2026-06-02-agent-claim-check-public-launch.md`](../labs/2026/2026-06-02-agent-claim-check-public-launch.md)
- Supporting recipes: [`./closeout-evidence-check-for-agents.md`](./closeout-evidence-check-for-agents.md), [`./agent-proof-packet-for-review.md`](./agent-proof-packet-for-review.md), and [`./agent-review-map.md`](./agent-review-map.md).
