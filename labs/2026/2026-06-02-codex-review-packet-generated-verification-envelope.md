# 2026-06-02 - Codex Review Packet Generated Verification Envelope

## Context

`codex-review-packet` could already embed an external `verify-by-change --json-envelope` artifact, but the direct `--verify-by-change` path rendered generated output as a plain Markdown block. That made generated packets less structured than externally prepared envelope packets.

## Change

- `--verify-by-change` now asks the generator for `--json-envelope` first.
- Valid `verify-by-change.v1` envelopes are rendered into Markdown with source metadata, changed files, categories, and commands.
- Older compatible generators that do not support `--json-envelope` fall back to plain Markdown output.
- Added tests for envelope rendering, staged-mode forwarding, and fallback behavior.
- Updated README verification commands and repo decisions to document the generated-envelope path.

## Verification

- `python3 -m unittest discover -s tests`: 32 tests passed.
- `python3 -m py_compile codex_review_packet.py`: passed.
- `make test`: 32 tests passed.
- `make build`: passed.
- `make lint`: passed.
- `git diff --check`: passed.
- Smoke generated a packet with real `verify-by-change` and confirmed `Envelope: verify-by-change.v1` plus `Verification source: git`.
- `repo-flightcheck --strict --threshold 80`: 100/100 after commit.
- GitHub Actions run `26802456278`: success for commit `6feb7b3c84f28a3f54b621949feb441314130475`.

## Source Linkage

- Repo: https://github.com/manuelsampedro1/codex-review-packet
- Commit: https://github.com/manuelsampedro1/codex-review-packet/commit/6feb7b3c84f28a3f54b621949feb441314130475
- CI run: https://github.com/manuelsampedro1/codex-review-packet/actions/runs/26802456278
- Source: https://raw.githubusercontent.com/manuelsampedro1/codex-review-packet/main/codex_review_packet.py
- Tests: https://raw.githubusercontent.com/manuelsampedro1/codex-review-packet/main/tests/test_codex_review_packet.py
- Generator: https://github.com/manuelsampedro1/verify-by-change

## Takeaway

Generated review packets should preserve structured verification metadata whenever possible. Markdown stays useful for humans, but source, changed files, categories, and commands are stronger when they survive as an envelope before being rendered.
