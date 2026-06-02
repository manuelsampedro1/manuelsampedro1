# 2026-06-02 - Codex Review Packet Bounded Diff

## Context

`codex-review-packet` already bundled repo context, changed files, staged diffs, unstaged diffs, and bounded untracked previews. The next review-quality gap was large combined diffs: a packet can become too big for a useful model review even when every included piece is technically relevant.

## Change

- Added `--diff-lines` to cap the combined diff block.
- Added `limit_lines` with an explicit omission marker instead of silently dropping content.
- Kept the default uncapped so local reviewers choose the tradeoff.
- Added tests for line limiting and packet-level diff omission.
- Updated README verification and `DECISIONS.md`.

Public commit: `710a2b2bbc60 feat: cap review packet diff size`.

## Verification

Local checks:

```sh
python3 -m py_compile codex_review_packet.py
python3 -m unittest discover -s tests
python3 codex_review_packet.py --repo . >/tmp/review-packet.md
python3 codex_review_packet.py --repo . --diff-lines 80 >/tmp/review-packet-capped.md
test -s /tmp/review-packet.md
test -s /tmp/review-packet-capped.md
git diff --check
```

Results:

- Python compile passed.
- `python3 -m unittest discover -s tests`: 7 tests passed.
- Normal and capped review packets were generated and non-empty.
- Public commit page and raw changed files returned `200`.
- GitHub Actions run `26792956323` completed with conclusion `success`.

## Source Linkage

- Repo: <https://github.com/manuelsampedro1/codex-review-packet>
- Commit: <https://github.com/manuelsampedro1/codex-review-packet/commit/710a2b2bbc60bde50f6d6372464069dc3280caf5>
- CI run: <https://github.com/manuelsampedro1/codex-review-packet/actions/runs/26792956323>
- CLI: <https://raw.githubusercontent.com/manuelsampedro1/codex-review-packet/710a2b2/codex_review_packet.py>
- Tests: <https://raw.githubusercontent.com/manuelsampedro1/codex-review-packet/710a2b2/tests/test_codex_review_packet.py>

## Takeaway

AI review packets need context budgets, not just more context. A bounded diff with an explicit omission marker is better than either overwhelming the model or quietly hiding part of the change.
