# 2026-06-02 - Codex Review Packet Generated Verification

## Context

`codex-review-packet` could already embed a Markdown verification checklist, but the caller had to generate that checklist in a separate step. That kept the tool flexible, but made the strongest handoff flow more manual than necessary: diff, repo context, readiness report, and verification plan should be easy to put in one packet.

The public reliability stack now has enough sibling tools for a tighter integration: `codex-review-packet` can ask `verify-by-change` for the checklist directly while keeping the dependency optional.

## Change

- Added `--verify-by-change` to invoke a local executable or `.py` script and embed its Markdown checklist.
- Kept `--verification-checklist` for pre-generated files and rejected using both sources at once.
- Ran the generator with `subprocess.run` argument lists, not a shell.
- Forwarded staged/base mode so the generated checklist matches the packet scope.
- Added unit and CLI tests with a fake generator, plus docs and a decision note.

Public commit: `60296f3ddc feat: generate verification checklist`.

## Verification

Local checks:

```sh
python3 -m py_compile codex_review_packet.py
python3 -m unittest discover -s tests
make test
make build
make lint
python3 codex_review_packet.py --repo . --verify-by-change /Users/manuelsampedro/Documents/Codex/2026-05-24/flagships/verify-by-change/verify_by_change.py --output /tmp/review-packet-generated-checklist.md
python3 codex_review_packet.py --repo . --verification-checklist /tmp/review-packet-generated-checklist.md --verify-by-change /Users/manuelsampedro/Documents/Codex/2026-05-24/flagships/verify-by-change/verify_by_change.py >/tmp/review-packet-conflict.txt 2>&1 || test $? -eq 1
git diff --check
node /Users/manuelsampedro/Documents/Codex/2026-05-21/repo-flightcheck/bin/repo-flightcheck.js . --strict --threshold 80
```

Results:

- `python3 -m unittest discover -s tests`: 19 tests passed.
- `make test`, `make build`, and `make lint`: passed.
- Generated-packet smoke included `Source: verify-by-change:` and `## Verification Checklist`.
- Conflict smoke rejected two checklist sources with the expected error.
- README smoke commands with a fake generator passed.
- `repo-flightcheck`: `100/100` after commit.
- Public commit page returned `200`.
- Raw `codex_review_packet.py` returned `200`.
- GitHub Actions run `26797488725` completed with conclusion `success`.

## Source Linkage

- Repo: <https://github.com/manuelsampedro1/codex-review-packet>
- Commit: <https://github.com/manuelsampedro1/codex-review-packet/commit/60296f3ddc4b3dbc179bcbfd61cec8dd247c4aeb>
- CI run: <https://github.com/manuelsampedro1/codex-review-packet/actions/runs/26797488725>
- Tool: <https://raw.githubusercontent.com/manuelsampedro1/codex-review-packet/main/codex_review_packet.py>
- Tests: <https://raw.githubusercontent.com/manuelsampedro1/codex-review-packet/main/tests/test_codex_review_packet.py>

## Takeaway

A useful agent review handoff should not make the reviewer assemble evidence by hand. Keeping generator tools optional but directly invokable lets a packet carry repo context, readiness, diff evidence, and verification guidance without adding a hosted service or hidden dependency.
