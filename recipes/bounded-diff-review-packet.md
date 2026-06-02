# Bounded Diff Review Packet

Use this when a review packet includes raw diffs that can exceed the useful context budget for Codex, Claude Code, or another reviewer.

## Goal

Keep review packets compact without hiding the fact that content was omitted.

## Source Event

This recipe came from `codex-review-packet` commit `710a2b2bbc60`, which added `--diff-lines` for capped Markdown review packets.

Relevant files:

- `codex_review_packet.py`
- `tests/test_codex_review_packet.py`
- `README.md`
- `DECISIONS.md`

## Workflow

1. Keep the default full diff for local reviewers who want complete context.
2. Add an explicit `--diff-lines` option for context-constrained reviews.
3. Validate the limit as a positive integer.
4. Truncate only after collecting the combined diff so staged, unstaged, and untracked evidence share one budget.
5. Append an omission marker that states how many diff lines were dropped.
6. Test the helper and a full packet so the marker appears in real output.
7. Document that capped packets are a review tradeoff, not complete evidence.

## Checklist

- Does the packet say when diff content was omitted?
- Is the default still uncapped?
- Does the limit apply to the combined diff block, not only one source of changes?
- Is the cap configurable at CLI time?
- Do tests prove omitted lines do not appear in the packet?

## Verification

For a standard-library Python CLI, run:

```sh
python3 -m py_compile codex_review_packet.py
python3 -m unittest discover -s tests
python3 codex_review_packet.py --repo . --diff-lines 80 >/tmp/review-packet-capped.md
test -s /tmp/review-packet-capped.md
```

## Failure Modes

- Silently truncating the diff with no omission marker.
- Applying the cap before combining staged, unstaged, and untracked evidence.
- Making capped output the default and surprising local reviewers.
- Using word or byte limits that split lines in ways reviewers cannot inspect.
- Treating a capped packet as complete evidence for high-risk changes.

## Source Linkage

- Public repo: <https://github.com/manuelsampedro1/codex-review-packet>
- Commit: <https://github.com/manuelsampedro1/codex-review-packet/commit/710a2b2bbc60bde50f6d6372464069dc3280caf5>
- CI run: <https://github.com/manuelsampedro1/codex-review-packet/actions/runs/26792956323>
