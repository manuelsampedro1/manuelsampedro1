# 2026-06-02 - Codex Review Packet Published HEAD Proof

## Context

`repo-flightcheck` now detects whether local `HEAD` is actually published on the configured remote branch. That closes a profile-proof gap, but review handoffs still need to carry the evidence into the packet a reviewer or agent sees.

`codex-review-packet` already embeds repo readiness, verification checklists, generated verification envelopes, sensitive-change checks, review maps, and GitHub Actions CI evidence. The missing piece was public commit proof: whether the reviewed local commit is visible on the remote branch before links and CI evidence are trusted.

## Change

- Added `--published-head` to embed published-HEAD proof JSON in a review packet.
- Supports dedicated `published-head.v1` JSON and full `repo-flightcheck --check-remote --json` reports.
- Extracts the `git-remote` check from `repo-flightcheck` and renders it as `## Published HEAD`.
- Sanitizes HTTPS credential material from remote evidence before rendering.
- Added unit tests for dedicated proof JSON, repo-flightcheck report extraction, packet embedding, and CLI output.
- Updated README usage, example output, and verification commands.

Public commit: `3b7f9121f532 feat: include published head proof`.

## Verification

Local checks:

```sh
python3 -m unittest discover -s tests
python3 -m py_compile codex_review_packet.py
make test
make build
make lint
git diff --check
node /Users/manuelsampedro/Documents/Codex/2026-05-21/repo-flightcheck/bin/repo-flightcheck.js . --check-remote --strict --threshold 80
node /Users/manuelsampedro/Documents/Codex/2026-05-21/repo-flightcheck/bin/repo-flightcheck.js . --check-remote --json > /tmp/codex-review-packet-published-head.json
python3 codex_review_packet.py --repo . --published-head /tmp/codex-review-packet-published-head.json --output /tmp/review-packet-with-published-head.md
```

Results:

- `python3 -m unittest discover -s tests`: 39 tests passed.
- `python3 -m py_compile codex_review_packet.py`: passed.
- `make test`: 39 tests passed.
- `make build`: passed.
- `make lint`: passed.
- `git diff --check`: passed.
- Before push, `repo-flightcheck --check-remote` warned that local `HEAD` was not published on `origin/main`.
- After push, `repo-flightcheck --check-remote --strict --threshold 80`: `100/100`, including `PASS Git remote Origin remote is reachable and local HEAD is published on origin/main.`
- Published-head smoke packet rendered `## Published HEAD` with schema `repo-flightcheck`.
- Commit URL returned HTTP `200`.
- GitHub Actions run `26805711366` completed with conclusion `success`.

## Source Linkage

- Repo: <https://github.com/manuelsampedro1/codex-review-packet>
- Commit: <https://github.com/manuelsampedro1/codex-review-packet/commit/3b7f9121f5326cd5e02936c81b0e6905584d1c01>
- CI run: <https://github.com/manuelsampedro1/codex-review-packet/actions/runs/26805711366>
- CLI: <https://raw.githubusercontent.com/manuelsampedro1/codex-review-packet/main/codex_review_packet.py>
- Tests: <https://raw.githubusercontent.com/manuelsampedro1/codex-review-packet/main/tests/test_codex_review_packet.py>
- README: <https://raw.githubusercontent.com/manuelsampedro1/codex-review-packet/main/README.md>

## Takeaway

Review packets should carry public-proof status alongside CI status. A reviewer needs to know whether the diff, CI run, and public links all refer to the same pushed commit before trusting the handoff.
