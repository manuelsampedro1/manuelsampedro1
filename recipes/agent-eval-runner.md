# Agent Eval Runner

Use this after saving `diff-to-eval` cases and before trusting a new proof packet, closeout, or review note.

## Use When

- A useful agent failure mode has been converted into JSON eval cases.
- A new agent run claims it handled the same class of work.
- You need a lightweight regression suite without calling a model.
- You want to check whether the proof artifact names files, checks, risks, and expected outcomes.

## Goal

Score a candidate artifact against saved cases:

- changed files mentioned,
- suggested checks covered,
- risk tags represented,
- expected outcome covered,
- pass/fail using a threshold.

## Workflow

1. Create or collect cases:

```sh
diff-to-eval /tmp/agent-change.diff \
  --title "Publish guard" \
  --expect "Unexpected public-path changes fail before generated indexes are refreshed." \
  --output cases/publish-guard.json
```

2. Save the candidate proof artifact:

```sh
pbpaste > /tmp/agent-proof.md
```

3. Run the eval suite:

```sh
agent-eval-runner cases/*.json /tmp/agent-proof.md --threshold 75
```

4. Treat failures as regression context, not as a vague quality complaint:

- missing changed files means the handoff is not inspectable enough,
- missing check terms means verification is not specific enough,
- missing risk tags means the reviewer may miss operational context,
- missing expected outcome means the proof does not show the original behavior.

## Prompt Pattern

```text
Run this proof artifact against saved coding-agent eval cases.

Inputs:
- Eval cases: <paths or JSON>
- Candidate artifact: <proof packet, closeout, or review note>
- Threshold: <0-100>

Rules:
- Score only observable text coverage.
- Do not use model judgment to fill missing evidence.
- Report missing files, check terms, risk tags, and expected outcome terms.
- Convert failures into concrete repair instructions for the next closeout.
```

## Fast Checklist

- Do the cases come from real diffs?
- Does the candidate mention every important changed file?
- Does it include exact checks or command names?
- Does it carry risk language forward?
- Does it prove the expected outcome from the saved case?

## Failure Modes

- Treating eval cases as generic prompts instead of regression fixtures.
- Scoring broad writing quality instead of evidence coverage.
- Letting a passing score hide missing security or rollback evidence.
- Creating cases that have no observable expected outcome.
- Forgetting to preserve eval results in the run ledger.

## Source Linkage

- Repo / tool / workflow: [`agent-eval-runner`](https://github.com/manuelsampedro1/agent-eval-runner), public commit [`8c7960e`](https://github.com/manuelsampedro1/agent-eval-runner/commit/8c7960e28d8e964db05d16e249369af7d507dc52), [`README`](https://raw.githubusercontent.com/manuelsampedro1/agent-eval-runner/main/README.md), [`CLI`](https://raw.githubusercontent.com/manuelsampedro1/agent-eval-runner/main/src/agent_eval_runner/cli.py), [`tests`](https://raw.githubusercontent.com/manuelsampedro1/agent-eval-runner/main/tests/test_cli.py), [`example case`](https://raw.githubusercontent.com/manuelsampedro1/agent-eval-runner/main/examples/cases/publish-guard.json), and [`example candidate`](https://raw.githubusercontent.com/manuelsampedro1/agent-eval-runner/main/examples/candidate.md).
- Supporting prompt, script, or note: [`./diff-to-eval-case.md`](./diff-to-eval-case.md), [`./agent-proof-packet-for-review.md`](./agent-proof-packet-for-review.md), [`./change-risk-matrix-for-agent-diffs.md`](./change-risk-matrix-for-agent-diffs.md), and [`../labs/2026/2026-06-02-agent-eval-runner-public-launch.md`](../labs/2026/2026-06-02-agent-eval-runner-public-launch.md).
