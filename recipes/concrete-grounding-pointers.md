# Concrete Grounding Pointers

Use this pattern when agent-written Markdown or JSON will become a public note,
decision, review packet, closeout, profile claim, or proof artifact.

## Problem

Phrases like `Source: manual review`, `Evidence: checked earlier`, or
`References: internal note` can make a claim look grounded while giving the next
reviewer nothing inspectable.

## Pattern

Run source grounding with both gates enabled:

```sh
agent-source-grounding check artifact.md \
  --require-sources \
  --require-concrete \
  --format json \
  > /tmp/source-grounding.json
```

Treat zero `concrete_source_count` or any `no concrete source or evidence`
issue as a blocker before the artifact becomes durable proof.

Concrete pointers can be:

- URLs;
- repo-relative file paths;
- command outputs or log paths;
- run, job, or artifact IDs;
- issue, PR, or pull request references;
- receipts, reports, transcripts, or commits.

## Acceptance Criteria

- Markdown artifacts have source/evidence sections or links.
- Claim rows have non-empty grounding.
- JSON claims include sources, evidence, references, links, or URLs.
- Placeholder citation language is removed.
- Each important claim has at least one concrete pointer.
- `concrete_source_count` is visible in text or JSON output.

## Review Rule

A concrete pointer is not a fact-check. It proves the claim has something a
reviewer can inspect before deciding whether the claim is true enough to reuse.
