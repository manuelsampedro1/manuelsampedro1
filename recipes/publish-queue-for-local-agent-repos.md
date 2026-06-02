# Publish Queue for Local Agent Repos

Use this when several local agent tools are ready, but the public GitHub state has not caught up.

## Use When

- You have multiple local proof repos.
- Some remotes point to GitHub repos that do not exist yet.
- The profile TODO list and public README need to stay honest.
- You need a publication order before promoting anything as public proof.

## Goal

Produce a queue that separates ready local work from publication blockers:

- repo name,
- local path,
- branch and HEAD,
- dirty worktree state,
- origin remote,
- public GitHub URL,
- public HTTP status,
- blockers,
- next action.

## Workflow

1. Scan the local workspace:

```sh
agent-publish-queue /Users/me/Code --max-depth 2
```

2. Check public GitHub status when you need to update profile TODOs:

```sh
agent-publish-queue /Users/me/Code --max-depth 2 --check-remote
```

3. Treat `public repo not found` as a setup blocker, not a code failure.

4. Create empty GitHub repos manually or with authenticated tooling, then push the matching local repos.

5. Promote a repo to the profile only after:

- local tests pass,
- push succeeds,
- CI passes or its initial failure is understood,
- README is strong enough to stand alone.

## Prompt Pattern

```text
Audit this local agent repo workspace for publication readiness.

Inputs:
- Workspace root: <path>
- Max depth: <n>
- Expected GitHub owner: <owner>

Tasks:
1. List every local Git repo.
2. Report branch, HEAD, dirty state, origin remote, public URL, and public HTTP status.
3. Separate code blockers from GitHub setup blockers.
4. Do not claim a repo is public when GitHub returns 404.
5. Produce the exact next action for each blocked repo.
```

## Fast Checklist

- Is every local proof repo committed?
- Does every repo have an `origin` remote?
- Does the public GitHub URL return `200` before profile promotion?
- Are dirty worktrees fixed before publication?
- Does TODO name the exact missing GitHub repo instead of vague "publish later" wording?

## Failure Modes

- Adding local-only repos to the profile as if they are public.
- Treating `git push` failure as a code failure when the GitHub repo simply does not exist.
- Losing track of which local repos are already committed.
- Creating profile churn without moving a repo closer to publication.
- Forgetting to rerun the queue after creating remotes.

## Source Linkage

- Repo / tool / workflow: [`agent-publish-queue`](https://github.com/manuelsampedro1/agent-publish-queue), public commit [`6a221f7`](https://github.com/manuelsampedro1/agent-publish-queue/commit/6a221f7d6f9cef88f8bfce1261a1b591392d41a6), [`README`](https://raw.githubusercontent.com/manuelsampedro1/agent-publish-queue/main/README.md), [`CLI`](https://raw.githubusercontent.com/manuelsampedro1/agent-publish-queue/main/src/agent_publish_queue/cli.py), [`tests`](https://raw.githubusercontent.com/manuelsampedro1/agent-publish-queue/main/tests/test_cli.py), and [`sample report`](https://raw.githubusercontent.com/manuelsampedro1/agent-publish-queue/main/examples/sample-report.md).
- Supporting prompt, script, or note: [`./public-surface-sync-for-agent-repos.md`](./public-surface-sync-for-agent-repos.md), [`./flagship-repo-proof-packet.md`](./flagship-repo-proof-packet.md), [`../labs/2026/2026-06-02-agent-publish-queue-public-launch.md`](../labs/2026/2026-06-02-agent-publish-queue-public-launch.md), and [`../TODO.md`](../TODO.md).
