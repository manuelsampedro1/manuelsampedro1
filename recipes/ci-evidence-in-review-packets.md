# CI Evidence in Review Packets

Use this after pushing agent-assisted work when a review packet should prove which CI run verified the change.

## Goal

Attach GitHub Actions run evidence to the same packet that already carries the diff, repo context, readiness state, and verification plan.

## Source Event

This recipe came from adding `--ci-run` to `codex-review-packet`.

The public change lets a packet render GitHub Actions run JSON as a dedicated `## CI Evidence` section.

## Workflow

1. Push the repo change.
2. Wait for the relevant GitHub Actions run to complete.
3. Fetch the run JSON from the GitHub Actions API.
4. Build the review packet with `--ci-run`.
5. Confirm the packet contains `## CI Evidence`.
6. Check that the run URL, conclusion, and SHA match the commit being reviewed.
7. Attach the packet to the final handoff or import the same evidence into a ledger.

## Example

```sh
curl -fsS \
  https://api.github.com/repos/OWNER/REPO/actions/runs/RUN_ID \
  > /tmp/ci-run.json

python3 /path/to/codex-review-packet/codex_review_packet.py \
  --repo /path/to/target-repo \
  --ci-run /tmp/ci-run.json \
  --output /tmp/review-packet.md

grep -q '## CI Evidence' /tmp/review-packet.md
grep -q 'Conclusion: success' /tmp/review-packet.md
```

Expected packet signal:

```md
## CI Evidence

- Run: 26801172625
- Workflow: CI
- Status: completed
- Conclusion: success
- SHA: 25b526a9aa7e252d3da12fc26e10affb40bfc1cd
```

## Checklist

- Does the run JSON refer to the same commit SHA as the reviewed change?
- Is the run `completed` before claiming success?
- Is `conclusion` visible and not inferred from status alone?
- Does the packet preserve the run URL?
- If the API response is a `workflow_runs` list, did the packet select the intended run?
- If CI failed, does the packet show failure instead of hiding the run?

## Failure Modes

- Using the latest run from the wrong branch.
- Treating `completed` as `success` when conclusion is `failure` or `cancelled`.
- Dropping the SHA, which makes the evidence hard to tie to the commit.
- Keeping CI evidence only in chat, where a later reviewer cannot inspect it.
- Rebuilding the packet from stale CI JSON after a new commit lands.

## Source Linkage

- Public repo: <https://github.com/manuelsampedro1/codex-review-packet>
- Commit: <https://github.com/manuelsampedro1/codex-review-packet/commit/25b526a9aa7e252d3da12fc26e10affb40bfc1cd>
- CI run: <https://github.com/manuelsampedro1/codex-review-packet/actions/runs/26801172625>
- Lab note: <../labs/2026/2026-06-02-codex-review-packet-ci-evidence.md>
