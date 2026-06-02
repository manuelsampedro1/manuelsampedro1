# Remote Failure Classification Before Public Proof

Use this when a local repo has an `origin` URL but cannot be used as public proof yet.

## Goal

Separate three different remote states before claiming a project is published:

- `origin` is only configured locally.
- the remote repository exists and is reachable.
- local `HEAD` is actually published on the remote branch.

## Workflow

1. Run the local verification suite first.
2. Run `repo-flightcheck --check-remote --strict --threshold 80`.
3. Read the `Git remote` row before sharing any GitHub links.
4. If the message says the repository was not found or is not accessible, create the missing GitHub repo or fix ownership/access first.
5. If the message says authentication is missing, fix Git identity, SSH keys, or HTTPS credentials before retrying.
6. If the message says local `HEAD` is not published, push the current branch and rerun the check.
7. Only promote the repo to a profile README after the public commit, raw file URLs, and CI run are visible.

## Expected Signals

- Ready: `Origin remote is reachable and local HEAD is published on origin/main.`
- Missing repo or no access: `Origin remote repository was not found or is not accessible.`
- Auth problem: `Origin remote requires authentication or the current Git identity does not have access.`
- Local-only work: `Origin remote is reachable, but local HEAD is not published on origin/main.`

## Checklist

- Does `git remote get-url origin` point at the intended owner/repo?
- Does `git ls-remote origin refs/heads/main` return the expected SHA?
- Does the profile or proof packet link to a commit URL that returns HTTP `200`?
- Does the repo CI run correspond to the same SHA?
- Does `repo-flightcheck --check-remote` pass after the push?

## Failure Modes

- Treating a configured local remote as proof that the GitHub repo exists.
- Publishing profile links before the first branch has been pushed.
- Confusing a missing repository with a stale local branch.
- Hiding an auth failure behind a generic network error.
- Claiming public proof from CI on one SHA while local `HEAD` points at another.

## Source Linkage

- Public repo: <https://github.com/manuelsampedro1/repo-flightcheck>
- Commit: <https://github.com/manuelsampedro1/repo-flightcheck/commit/2c0a42bdf016757235e349bc746860cdc6a30f3a>
- CI run: <https://github.com/manuelsampedro1/repo-flightcheck/actions/runs/26806662928>
- Lab note: <../labs/2026/2026-06-02-repo-flightcheck-remote-failure-classification.md>
