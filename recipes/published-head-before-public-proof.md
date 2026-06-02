# Published HEAD Before Public Proof

Use this before adding a commit, CI run, raw source file, or repo change to a profile proof list.

## Goal

Prevent a public surface from claiming evidence for a local commit that has not been pushed yet.

## Source Event

This recipe came from extending `repo-flightcheck --check-remote` so it verifies that local `HEAD` matches the current branch on `origin`, not only that the remote exists.

## Workflow

1. Finish local validation: tests, build, lint, and working-tree cleanup.
2. Commit the change locally.
3. Run `repo-flightcheck --check-remote`.
4. If it warns that local `HEAD` is not published, push before updating the profile.
5. Confirm `git ls-remote origin refs/heads/main` returns the same SHA as `git rev-parse HEAD`.
6. Wait for CI on that SHA.
7. Only then add commit URLs, CI URLs, raw source links, lab notes, or recipes to the public profile.

## Expected Signals

Blocked:

```text
WARN  Git remote                   Origin remote is reachable, but local HEAD is not published on origin/main.
```

Proof-ready:

```text
PASS  Git remote                   Origin remote is reachable and local HEAD is published on origin/main.
```

## Checklist

- Does `git rev-parse HEAD` equal `git ls-remote origin refs/heads/<branch>`?
- Does `repo-flightcheck --check-remote` pass after the commit and push, not only before committing?
- Does the commit URL return HTTP `200`?
- Does the CI run for that exact SHA finish with `success`?
- Do raw source URLs point to `main` after the pushed commit is visible?
- Is the working tree clean before the proof is documented?

## Failure Modes

- Treating a reachable GitHub repo as proof that the latest local commit is public.
- Updating the profile after a local commit but before `git push`.
- Linking to CI from an older SHA that does not cover the current code.
- Using raw `main` source links before confirming `main` moved to the expected SHA.
- Forgetting that a clean working tree and a published `HEAD` are separate checks.

## Source Linkage

- Public repo: <https://github.com/manuelsampedro1/repo-flightcheck>
- Commit: <https://github.com/manuelsampedro1/repo-flightcheck/commit/6bf313ec67ce5a0fffd1658fcd182ab1e37d4fe7>
- CI run: <https://github.com/manuelsampedro1/repo-flightcheck/actions/runs/26805326508>
- Lab note: <../labs/2026/2026-06-02-repo-flightcheck-published-head.md>
