# Published HEAD Proof in Review Packets

Use this when a review packet includes public links, CI evidence, or profile-ready proof.

## Goal

Make the packet show whether the reviewed local commit is actually published on the remote branch.

## Source Event

This recipe came from adding `--published-head` to `codex-review-packet`. The flag accepts either a dedicated proof JSON file or a full `repo-flightcheck --check-remote --json` report and renders the result as `## Published HEAD`.

## Workflow

1. Finish the local change and commit it.
2. Run `repo-flightcheck --check-remote --json` against the repo.
3. If the `git-remote` check warns, push the commit or fix the remote before claiming public proof.
4. Generate the review packet with `--published-head`.
5. Include CI evidence only after the CI run belongs to the same published SHA.
6. Use the packet for final review, profile notes, or run-ledger import only after the public proof section passes.

## Example

```sh
node /path/to/repo-flightcheck/bin/repo-flightcheck.js \
  /path/to/repo \
  --check-remote \
  --json \
  > /tmp/published-head.json

python3 /path/to/codex-review-packet/codex_review_packet.py \
  --repo /path/to/repo \
  --published-head /tmp/published-head.json \
  --output /tmp/review-packet.md
```

Expected packet section:

```md
## Published HEAD

- Status: `pass`
- Message: Origin remote is reachable and local HEAD is published on origin/main.
- Schema: `repo-flightcheck`
```

## Checklist

- Does the packet include `## Published HEAD`?
- Does the published-head source come from the same repo being reviewed?
- Does the section show `pass`, not only a reachable remote?
- Does CI evidence use the same SHA as the published branch?
- Are remote URLs sanitized before they enter the packet?
- Is the packet regenerated after the final push?

## Failure Modes

- Embedding CI evidence but omitting whether the local commit is public.
- Reusing an old `repo-flightcheck` JSON file after another commit.
- Passing a generic readiness report that was generated without `--check-remote`.
- Treating `origin` reachability as equivalent to published `HEAD`.
- Copying HTTPS remote URLs with credentials into review artifacts.

## Source Linkage

- Public repo: <https://github.com/manuelsampedro1/codex-review-packet>
- Commit: <https://github.com/manuelsampedro1/codex-review-packet/commit/3b7f9121f5326cd5e02936c81b0e6905584d1c01>
- CI run: <https://github.com/manuelsampedro1/codex-review-packet/actions/runs/26805711366>
- Lab note: <../labs/2026/2026-06-02-codex-review-packet-published-head.md>
