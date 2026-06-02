# Remote Readiness Before Public Proof

Use this before adding a local project to a GitHub profile, workbench README, or public proof list.

## Goal

Detect the gap between "this repo is locally ready" and "this repo is actually published and reachable."

## Source Event

This recipe came from adding the `Git remote` check and `--check-remote` flag to `repo-flightcheck`.

The public change keeps remote reachability opt-in, because checking GitHub remotes can require network access or authentication.

## Workflow

1. Finish local repo validation first: tests, build, lint, working tree, README, and agent instructions.
2. Confirm an `origin` remote exists.
3. Run `repo-flightcheck --check-remote` before claiming the repo is public.
4. If the remote is unreachable, do not add the repo to the profile yet.
5. Create the missing GitHub repo or fix authentication outside the repo.
6. Push again and wait for CI.
7. Only update the profile after the commit URL and CI URL are reachable.

## Example

```sh
node /path/to/repo-flightcheck/bin/repo-flightcheck.js \
  /path/to/local-project \
  --check-remote
```

Expected blocker signal:

```text
WARN  Git remote                   Origin remote is configured but could not be reached.
```

Expected proof-ready signal:

```text
PASS  Git remote                   Origin remote is reachable.
```

## Checklist

- Does `git remote get-url origin` point at the intended GitHub owner and repo?
- Does `repo-flightcheck --check-remote` pass before the repo is promoted?
- Does `git ls-remote origin refs/heads/main` return the expected SHA?
- Does the pushed commit URL return HTTP `200`?
- Does the GitHub Actions run for that SHA finish with `success` before the profile claims CI evidence?
- Are credentials absent from README, logs, and profile artifacts?

## Failure Modes

- Setting `origin` to a future repo name and treating that as publication.
- Adding a project to the profile before the empty GitHub repo exists.
- Letting SSH auth work for existing repos but assuming it can create new repos.
- Publishing a profile link before CI has run for the pushed SHA.
- Exposing HTTPS credentials in remote URLs or copied command output.

## Source Linkage

- Public repo: <https://github.com/manuelsampedro1/repo-flightcheck>
- Commit: <https://github.com/manuelsampedro1/repo-flightcheck/commit/af87c6cd1952ebab1c4617656417cd343e5f450e>
- CI run: <https://github.com/manuelsampedro1/repo-flightcheck/actions/runs/26804858130>
- Lab note: <../labs/2026/2026-06-02-repo-flightcheck-remote-readiness.md>
