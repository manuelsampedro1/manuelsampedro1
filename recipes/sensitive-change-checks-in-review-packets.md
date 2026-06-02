# Sensitive Change Checks in Review Packets

Use this when an agent handoff includes paths that could affect secrets, permissions, approvals, receipts, guards, deploys, releases, or CI workflows.

## Goal

Make sensitive changed paths visible in the review packet before the reviewer has to infer risk from the full diff.

## Source Event

This recipe came from adding `## Sensitive Change Check` to `codex-review-packet`.

The public change groups flagged paths into secret material, authorization and approval, and deploy or release categories while preserving the normal review lanes.

## Workflow

1. Generate the review packet from the target repo and base commit.
2. Check whether the packet contains `## Sensitive Change Check`.
3. If secret material is listed, inspect the diff for real credentials, tokens, webhook URLs, or production identifiers.
4. If authorization or approval code is listed, require denial, expiry, malformed-input, and missing-approval checks.
5. If deploy or release paths are listed, require rollback, environment, CI, and release-path review.
6. Keep CI evidence attached, but do not treat a green CI run as sufficient proof for sensitive behavior.
7. Summarize the sensitive-path review in the closeout before claiming the change is safe.

## Example

```sh
python3 /path/to/codex-review-packet/codex_review_packet.py \
  --repo /path/to/target-repo \
  --base origin/main \
  --output /tmp/review-packet.md

grep -q '## Sensitive Change Check' /tmp/review-packet.md
```

Expected packet signal:

```md
## Sensitive Change Check

These paths need explicit risk review before merge.

### Secret material

- `.env`

### Authorization and approval

- `permission_protocol/client.py`

### Deploy or release path

- `scripts/deploy.sh`
```

## Checklist

- Did the packet separate sensitive paths from ordinary implementation paths?
- Did the reviewer inspect secret-bearing paths for real credentials or production identifiers?
- Did authorization checks include at least one negative path?
- Did deploy or release checks include rollback and environment assumptions?
- Does CI evidence point to the same SHA as the reviewed packet?
- Did the closeout mention residual risk instead of saying only "tests passed"?

## Failure Modes

- Hiding `.env`, key, token, or credential paths inside a generic "changed files" list.
- Reviewing approval or permission logic only through the successful path.
- Treating deploy scripts as normal shell changes without environment and rollback review.
- Letting sensitive fixtures look realistic enough to be mistaken for production material.
- Claiming safety from CI status without tying the run to the exact commit SHA.

## Source Linkage

- Public repo: <https://github.com/manuelsampedro1/codex-review-packet>
- Commit: <https://github.com/manuelsampedro1/codex-review-packet/commit/8a71e89eafbeb23a065fa47adb29f130c28ab32b>
- CI run: <https://github.com/manuelsampedro1/codex-review-packet/actions/runs/26803873622>
- Lab note: <../labs/2026/2026-06-02-codex-review-packet-sensitive-change-check.md>
