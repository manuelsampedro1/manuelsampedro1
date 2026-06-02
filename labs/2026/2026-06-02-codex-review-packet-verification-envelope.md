# 2026-06-02 - Codex Review Packet Verification Envelope

## Context

`verify-by-change` can emit a `verify-by-change.v1` JSON envelope with changed files, source metadata, empty-state information, and verification categories.

`codex-review-packet` could already embed Markdown checklists and generated verification text, but a machine-readable envelope would have been pasted as raw JSON. That is useful for automation, but weak for a human review packet.

## Change

- Detected `verify-by-change.v1` files passed through `--verification-checklist`.
- Rendered envelope source metadata, changed files, categories, and commands as Markdown.
- Preserved the existing Markdown checklist behavior for non-envelope files.
- Added empty-envelope handling so no-change packets stay explicit.
- Added unit and CLI tests for envelope parsing and packet rendering.
- Updated README verification commands and `DECISIONS.md`.

Public commit: `669346be5b feat: render verification envelopes`.

## Verification

Local checks:

```sh
make test
make build
make lint
git diff --check
python3 /Users/manuelsampedro/Documents/Codex/2026-05-24/flagships/verify-by-change/verify_by_change.py README.md codex_review_packet.py --json-envelope --output /tmp/codex-review-packet-envelope.json
python3 codex_review_packet.py --repo . --verification-checklist /tmp/codex-review-packet-envelope.json --output /tmp/codex-review-packet-with-envelope.md
awk '/^## Verification Checklist$/{flag=1} /^## Suggested Review Prompt$/{flag=0} flag' /tmp/codex-review-packet-with-envelope.md > /tmp/codex-review-packet-verification-section.md
grep -q 'Envelope: `verify-by-change.v1`' /tmp/codex-review-packet-verification-section.md
grep -q 'Changed files:' /tmp/codex-review-packet-verification-section.md
! grep -q '"schema_version"' /tmp/codex-review-packet-verification-section.md
node /Users/manuelsampedro/Documents/Codex/2026-05-21/repo-flightcheck/bin/repo-flightcheck.js . --strict --threshold 80
```

Results:

- `make test`: 24 tests passed.
- `make build`: passed.
- `make lint`: passed.
- `git diff --check`: passed.
- Cross-tool smoke rendered the JSON envelope into Markdown.
- Verification section includes `Envelope: verify-by-change.v1` and changed files without raw JSON.
- `repo-flightcheck`: `100/100` after commit.
- Public commit page returned `200`.
- Raw `codex_review_packet.py` and tests returned `200`.
- GitHub Actions run `26798250260` completed with conclusion `success`.

## Source Linkage

- Repo: <https://github.com/manuelsampedro1/codex-review-packet>
- Commit: <https://github.com/manuelsampedro1/codex-review-packet/commit/669346be5b7260a3511aab68e136050b7e128bd3>
- CI run: <https://github.com/manuelsampedro1/codex-review-packet/actions/runs/26798250260>
- CLI: <https://raw.githubusercontent.com/manuelsampedro1/codex-review-packet/main/codex_review_packet.py>
- Tests: <https://raw.githubusercontent.com/manuelsampedro1/codex-review-packet/main/tests/test_codex_review_packet.py>
- Envelope producer: <https://github.com/manuelsampedro1/verify-by-change>

## Takeaway

Machine-readable evidence should not make human review worse. The useful pattern is to preserve structured source metadata while rendering the checklist in a form a reviewer can scan quickly.
