# 2026-06-02 - Codex Review Packet Readiness Report

## Context

The profile proof stack now has separate tools for repo readiness, review packet generation, change-aware verification, and run ledgers. The next credibility gap was integration: a review packet could include a diff and verification checklist, but not the repo readiness state that should shape the review before the diff is inspected.

## Change

- Added `--readiness-report` to `codex-review-packet`.
- Rendered a `## Repo Readiness` section from `repo-flightcheck --json` output.
- Summarized score, stack, pass/warn/fail counts, critical failures, warning or failed checks, and next fixes.
- Kept the readiness report external so the Python CLI does not depend on Node or on `repo-flightcheck`.
- Added a `--readiness-checks` cap for long reports.
- Added tests for dirty readiness reports, clean readiness reports, packet rendering, and CLI output.
- Hardened `codex-review-packet` itself with `LICENSE`, `AGENTS.md`, `Makefile`, `pyproject.toml`, `.env` ignores, and a sample readiness report.
- Updated CI to run the same Makefile verification aliases documented locally.

Public commit: `1cb7a8276e6a feat: embed repo readiness reports`.

## Verification

Local checks:

```sh
python3 -m py_compile codex_review_packet.py
python3 -m unittest discover -s tests
make test
make build
make lint
python3 codex_review_packet.py --repo . >/tmp/review-packet.md
python3 codex_review_packet.py --repo . --diff-lines 80 >/tmp/review-packet-capped.md
python3 codex_review_packet.py --repo . --verification-checklist /tmp/verification-checklist.md >/tmp/review-packet-with-checklist.md
python3 codex_review_packet.py --repo . --readiness-report examples/readiness-report.json >/tmp/review-packet-with-readiness.md
node /Users/manuelsampedro/Documents/Codex/2026-05-21/repo-flightcheck/bin/repo-flightcheck.js . --strict --threshold 80
git diff --check
```

Results:

- Python compile passed.
- `python3 -m unittest discover -s tests`: 15 tests passed.
- `make test`, `make build`, and `make lint` passed.
- Smoke packets generated review map, verification checklist, and repo readiness sections.
- Post-commit `repo-flightcheck` self-audit scored `100/100` with `0` warnings and `0` failures.
- Public commit page and raw changed files returned `200`.
- GitHub Actions run `26795792272` completed with conclusion `success`.

## Source Linkage

- Repo: <https://github.com/manuelsampedro1/codex-review-packet>
- Commit: <https://github.com/manuelsampedro1/codex-review-packet/commit/1cb7a8276e6a87ec51fbae4c95feff5ee34c2426>
- CI run: <https://github.com/manuelsampedro1/codex-review-packet/actions/runs/26795792272>
- CLI: <https://raw.githubusercontent.com/manuelsampedro1/codex-review-packet/1cb7a8276e6a87ec51fbae4c95feff5ee34c2426/codex_review_packet.py>
- Tests: <https://raw.githubusercontent.com/manuelsampedro1/codex-review-packet/1cb7a8276e6a87ec51fbae4c95feff5ee34c2426/tests/test_codex_review_packet.py>
- Agent guide: <https://raw.githubusercontent.com/manuelsampedro1/codex-review-packet/1cb7a8276e6a87ec51fbae4c95feff5ee34c2426/AGENTS.md>

## Takeaway

Review packets should include setup risk, not only diff risk. If the repo is missing CI, agent instructions, clean working tree, or executable commands, the reviewer should know that before trusting the generated packet.
