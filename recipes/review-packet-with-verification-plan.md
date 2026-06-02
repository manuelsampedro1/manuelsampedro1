# Review Packet with Verification Plan

Use this when preparing a code review packet for an AI agent or strict human reviewer.

## Goal

Put the diff, repo rules, and proposed verification plan in the same packet. This makes the review less generic and gives the reviewer a concrete basis for asking whether the right checks were run.

## Source Event

This recipe came from `codex-review-packet` commit `7ccc8ff6093b`, which added optional checklist embedding with `--verification-checklist`.

Relevant files:

- `codex_review_packet.py`
- `tests/test_codex_review_packet.py`
- `README.md`
- `DECISIONS.md`

## Workflow

1. Generate a change-aware checklist from the current diff.
2. Generate the review packet from the same repo state.
3. Embed the checklist as a separate fenced Markdown section.
4. Preserve the checklist source path so reviewers know where it came from.
5. Cap checklist lines with an explicit omission marker when context size matters.
6. Ask the reviewer to assess correctness, scope, and whether the verification plan is sufficient.
7. After the checks run, compare final closeout claims against the packet and command evidence.

## Checklist

- Does the packet list changed files?
- Does it include repo rules or top-level context?
- Does it show the actual diff or an honest capped diff marker?
- Does it include a verification checklist generated from the same repo state?
- Is the checklist clearly separate from the review prompt?
- Does the CLI test prove checklist inclusion through the real command path?

## Verification

For a standard-library Python CLI:

```sh
python3 -m py_compile codex_review_packet.py
python3 -m unittest discover -s tests
python3 /path/to/verify-by-change/verify_by_change.py --repo . --output /tmp/verification-checklist.md
python3 codex_review_packet.py --repo . --verification-checklist /tmp/verification-checklist.md --output /tmp/review-packet.md
grep -q '## Verification Checklist' /tmp/review-packet.md
```

## Failure Modes

- Embedding checklist text without saying where it came from.
- Letting a stale checklist drift from the actual diff.
- Dropping the diff to make room for checklist text.
- Marking omitted checklist lines without saying they were omitted.
- Treating the plan as proof that checks already ran.

## Source Linkage

- Public repo: <https://github.com/manuelsampedro1/codex-review-packet>
- Commit: <https://github.com/manuelsampedro1/codex-review-packet/commit/7ccc8ff6093b9ab680e4e29da4a1d8ce39b50a9f>
- CI run: <https://github.com/manuelsampedro1/codex-review-packet/actions/runs/26793567192>
