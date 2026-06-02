# Repo Readiness in Review Packets

Use this when a review packet should carry both the diff context and the repository's readiness state.

## Goal

Put repo setup risk in front of the reviewer before the diff. A review packet is stronger when it says whether the repo has agent instructions, executable verification, CI parity, secret hygiene, and a clean working tree.

## Source Event

This recipe came from `codex-review-packet` commit `1cb7a8276e6a`, which added `--readiness-report` support for `repo-flightcheck --json` output.

Relevant files:

- `codex_review_packet.py`
- `tests/test_codex_review_packet.py`
- `README.md`
- `AGENTS.md`

## Workflow

1. Run `repo-flightcheck` against the repo under review.
2. Save the JSON report.
3. Generate the review packet with the readiness report attached.
4. Read the `## Repo Readiness` section before reviewing the diff.
5. Treat critical readiness failures as review context, not as cosmetic warnings.
6. Pair this with a verification checklist when the diff also needs command-level checks.

## Commands

```sh
node /path/to/repo-flightcheck/bin/repo-flightcheck.js /path/to/repo --json > /tmp/repo-readiness.json
python3 /path/to/codex-review-packet/codex_review_packet.py \
  --repo /path/to/repo \
  --readiness-report /tmp/repo-readiness.json \
  --output /tmp/review-packet.md
```

With a change-aware verification checklist:

```sh
python3 /path/to/verify-by-change/verify_by_change.py --repo /path/to/repo --output /tmp/verification-checklist.md
python3 /path/to/codex-review-packet/codex_review_packet.py \
  --repo /path/to/repo \
  --readiness-report /tmp/repo-readiness.json \
  --verification-checklist /tmp/verification-checklist.md \
  --output /tmp/review-packet.md
```

## Checklist

- Does the packet include `## Repo Readiness` before the diff?
- Are warning or failed readiness checks visible without opening another artifact?
- Does the readiness report remain external so the packet generator stays dependency-light?
- Does the review prompt still focus on merge-relevant findings rather than generic commentary?
- If readiness score is weak, should the reviewer request repo setup fixes before reviewing code behavior?

## Verification

For `codex-review-packet`:

```sh
python3 -m unittest discover -s tests
python3 codex_review_packet.py --repo . --readiness-report examples/readiness-report.json >/tmp/review-packet-with-readiness.md
grep -q '## Repo Readiness' /tmp/review-packet-with-readiness.md
node /path/to/repo-flightcheck/bin/repo-flightcheck.js . --strict --threshold 80
```

## Failure Modes

- Running a review packet on a repo that has no executable verification command.
- Hiding readiness warnings in a separate JSON artifact the reviewer never opens.
- Coupling the packet generator to a specific scanner runtime instead of accepting a report file.
- Treating a high readiness score as a substitute for reviewing the actual diff.

## Source Linkage

- Public repo: <https://github.com/manuelsampedro1/codex-review-packet>
- Commit: <https://github.com/manuelsampedro1/codex-review-packet/commit/1cb7a8276e6a87ec51fbae4c95feff5ee34c2426>
- CI run: <https://github.com/manuelsampedro1/codex-review-packet/actions/runs/26795792272>
