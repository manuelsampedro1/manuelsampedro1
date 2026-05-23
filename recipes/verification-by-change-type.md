# Verification by Change Type

## Use When

Use this after a Codex edit when the next step is unclear and generic "run tests" advice would be too weak.

## Source Linkage

- Repo / tool / workflow: [verify-by-change](https://github.com/manuelsampedro1/verify-by-change).
- Supporting prompt, script, or note: [`scripts/commit_daily_update.sh`](../scripts/commit_daily_update.sh) and [`recipes/ai-repo-review-findings.md`](./ai-repo-review-findings.md).

## Steps

1. List the files that actually changed.
2. Bucket them by behavior: docs, shell, Python, web, Swift, or uncategorized.
3. Run the smallest verification that would catch the likely failure mode for that bucket.
4. If the change spans multiple buckets, verify the highest-risk bucket first.
5. Report the checks you ran and the remaining blind spots explicitly.

## Checks

- Docs-only: rendered content and public links still make sense.
- Shell: `bash -n` and one safe execution path.
- Python: `py_compile` plus the closest script/test run.
- Web: the nearest build/test command plus a real UI pass on the changed surface.
- Swift: target build plus the most direct simulator or test coverage you can run.

## Example

If the diff touches `README.md` and `scripts/deploy.sh`, do not treat that as a single "docs" change. Split it:

1. render or reread the README section,
2. run `bash -n scripts/deploy.sh`,
3. only then report whether the change is safe to ship.
