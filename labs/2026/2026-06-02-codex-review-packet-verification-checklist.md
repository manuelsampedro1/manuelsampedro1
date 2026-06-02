# 2026-06-02 - Codex Review Packet Verification Checklist

## Context

`codex-review-packet` already bundled changed files, repo context, diffs, and a suggested review prompt. `verify-by-change` already generated a checklist from the actual changed files. The missing piece was putting the proposed verification plan next to the diff before asking an agent or reviewer to judge the change.

This matters because review context without verification context can still produce generic advice. A stricter packet should show both "what changed" and "how this should be checked."

## Change

- Added `--verification-checklist <path>`.
- Added `--verification-lines` to cap the embedded checklist and keep packets model-context friendly.
- Added a `Verification Checklist` packet section with the source path and fenced Markdown.
- Added tests for checklist section rendering, line omission, packet inclusion, and CLI output.
- Updated README examples with a `verify-by-change` to `codex-review-packet` flow.
- Recorded the design decision in `DECISIONS.md`.

Public commit: `7ccc8ff6093b feat: include verification checklists in packets`.

## Verification

Local checks:

```sh
python3 -m py_compile codex_review_packet.py
python3 -m unittest discover -s tests
printf '## Python\n\n- Run unit tests.\n' >/tmp/verification-checklist.md
python3 codex_review_packet.py --repo . --verification-checklist /tmp/verification-checklist.md >/tmp/review-packet-with-checklist.md
test -s /tmp/review-packet-with-checklist.md
grep -q '## Verification Checklist' /tmp/review-packet-with-checklist.md
git diff --check
```

End-to-end smoke with the real checklist generator:

```sh
python3 /Users/manuelsampedro/Documents/Codex/2026-05-24/flagships/verify-by-change/verify_by_change.py --repo . --output "$tmpdir/verification-checklist.md"
python3 codex_review_packet.py --repo . --verification-checklist "$tmpdir/verification-checklist.md" --output "$tmpdir/review-packet.md"
test -s "$tmpdir/review-packet.md"
grep -q '## Verification Checklist' "$tmpdir/review-packet.md"
```

Results:

- Python compile passed.
- `python3 -m unittest discover -s tests`: 9 tests passed.
- CLI output with a checklist was generated and non-empty.
- The real `verify-by-change` to `codex-review-packet` smoke passed.
- `git diff --check` passed.
- Public commit page and raw changed files returned `200`.
- GitHub Actions run `26793567192` completed with conclusion `success`.

## Source Linkage

- Repo: <https://github.com/manuelsampedro1/codex-review-packet>
- Commit: <https://github.com/manuelsampedro1/codex-review-packet/commit/7ccc8ff6093b9ab680e4e29da4a1d8ce39b50a9f>
- CI run: <https://github.com/manuelsampedro1/codex-review-packet/actions/runs/26793567192>
- CLI: <https://raw.githubusercontent.com/manuelsampedro1/codex-review-packet/7ccc8ff6093b9ab680e4e29da4a1d8ce39b50a9f/codex_review_packet.py>
- Tests: <https://raw.githubusercontent.com/manuelsampedro1/codex-review-packet/7ccc8ff6093b9ab680e4e29da4a1d8ce39b50a9f/tests/test_codex_review_packet.py>

## Takeaway

A review packet should not only summarize the diff. It should carry the expected verification plan so the reviewer can compare findings, tests, and final claims against the same evidence contract.
