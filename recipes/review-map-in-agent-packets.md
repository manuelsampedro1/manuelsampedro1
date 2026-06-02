# Review Map in Agent Packets

Use this when a review packet includes a mixed diff and the reviewer needs more than one flat changed-file list.

## Goal

Route changed files into review lanes before showing the full diff, so CI, security, data, tests, docs, agent instructions, and application code get the right scrutiny.

## Source Event

This recipe came from `codex-review-packet` commit `2d76953f5bcb`, which added a deterministic `Review Map` section to generated packets.

Relevant files:

- `codex_review_packet.py`
- `tests/test_codex_review_packet.py`
- `README.md`
- `DECISIONS.md`

## Workflow

1. Collect changed files from the same state used for the review diff.
2. Classify each path with deterministic rules.
3. Keep high-risk lanes visible before repo context and diff details.
4. Add a short focus prompt per lane.
5. Include an `Unmapped` lane so unknown files are not silently ignored.
6. Avoid confidence scores unless there is a real evidence model behind them.
7. Test classification rules directly and through packet rendering.

## Checklist

- Does the packet show review lanes before the diff?
- Are CI/release, security, data, tests, docs, agent instructions, and application code distinct?
- Does every changed file appear in exactly one lane or an explicit `Unmapped` lane?
- Are lane prompts specific enough to change reviewer behavior?
- Can a reviewer challenge the path rules from the code?

## Verification

For a standard-library packet generator:

```sh
python3 -m py_compile codex_review_packet.py
python3 -m unittest discover -s tests
python3 codex_review_packet.py --repo . >/tmp/review-packet.md
grep -q '## Review Map' /tmp/review-packet.md
```

## Failure Modes

- Treating the review map as a risk score.
- Sending every file through application-code review.
- Hiding docs and README claims below implementation details.
- Forgetting agent-instruction files such as `AGENTS.md`.
- Leaving unknown file types out of the handoff instead of marking them unmapped.

## Source Linkage

- Public repo: <https://github.com/manuelsampedro1/codex-review-packet>
- Commit: <https://github.com/manuelsampedro1/codex-review-packet/commit/2d76953f5bcb1994647b8f6bb2f13dea7fe28d17>
- CI run: <https://github.com/manuelsampedro1/codex-review-packet/actions/runs/26794611781>
