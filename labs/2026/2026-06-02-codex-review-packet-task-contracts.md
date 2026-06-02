# 2026-06-02 - Codex Review Packet Task Contracts

## Context

`repo-flightcheck` can now validate repo-level task contracts, but a reviewer still needs to see the task itself before reading a generated diff. Without that context, review packets can prove readiness and CI while still missing the most important question: what was the agent asked to do?

`codex-review-packet` already carries repo rules, review lanes, sensitive-change checks, readiness reports, verification plans, CI evidence, and published-HEAD proof. The next useful step was to embed the task contract that defines objective, constraints, acceptance criteria, expected changes, verification, risks, and out-of-scope work.

## Change

- Added automatic detection for repo-level `AGENT_TASK.md` and `TASK_CONTRACT.md`.
- Added `--task-contract` for explicit external task contracts.
- Added `--task-contract-lines` so contract context stays bounded.
- Renders a dedicated `## Task Contract` section before readiness, CI, and diff evidence.
- Reports `pass` or `warn` based on required sections and obvious placeholder lines.
- Added unit and CLI coverage for section rendering, missing sections, placeholders, auto-detection, and explicit contracts.
- Updated README usage, example output, verification commands, and repo decisions.

Public commit: `0df7499f1e2 feat: include agent task contracts`.

## Verification

Local checks:

```sh
python3 -m py_compile codex_review_packet.py
python3 -m unittest discover -s tests
make test
make build
make lint
git diff --check
python3 codex_review_packet.py --repo . --task-contract /tmp/codex-review-packet-agent-task.md --task-contract-lines 20 --output /tmp/review-packet-with-task-contract.md
grep -q '## Task Contract' /tmp/review-packet-with-task-contract.md
grep -q 'Required sections: `8/8`' /tmp/review-packet-with-task-contract.md
node /Users/manuelsampedro/Documents/Codex/2026-05-21/repo-flightcheck/bin/repo-flightcheck.js . --check-remote --strict --threshold 80
```

Results:

- `python3 -m unittest discover -s tests`: 44 tests passed.
- `python3 -m py_compile codex_review_packet.py`: passed.
- `make test`: 44 tests passed.
- `make build`: passed.
- `make lint`: passed.
- `git diff --check`: passed.
- Task-contract smoke packet rendered `## Task Contract` and `Required sections: 8/8`.
- `repo-flightcheck --check-remote --strict --threshold 80`: `100/100`.
- `origin/main` points to `0df7499f1e2b47b679072e52c4060198a1559e60`.
- Commit URL returned HTTP `200`.
- Raw README returned HTTP `200`.
- GitHub Actions run `26807708146` completed with conclusion `success`.

## Source Linkage

- Repo: <https://github.com/manuelsampedro1/codex-review-packet>
- Commit: <https://github.com/manuelsampedro1/codex-review-packet/commit/0df7499f1e2b47b679072e52c4060198a1559e60>
- CI run: <https://github.com/manuelsampedro1/codex-review-packet/actions/runs/26807708146>
- CLI: <https://raw.githubusercontent.com/manuelsampedro1/codex-review-packet/main/codex_review_packet.py>
- Tests: <https://raw.githubusercontent.com/manuelsampedro1/codex-review-packet/main/tests/test_codex_review_packet.py>
- README: <https://raw.githubusercontent.com/manuelsampedro1/codex-review-packet/main/README.md>

## Takeaway

Review packets should show the task contract before they show the diff. CI, readiness, and published-HEAD proof are stronger when the reviewer can compare them against the exact intended outcome and constraints.
