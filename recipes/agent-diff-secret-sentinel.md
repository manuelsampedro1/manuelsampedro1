# Agent Diff Secret Sentinel

Use this before committing, publishing, or sharing changes produced by a coding agent.

## Use When

- A Codex or Claude Code run touched config, auth, deployment, CI, docs, examples, or environment files.
- The agent copied values from logs, terminal output, dashboards, or local `.env` files.
- You are about to publish a repo, gist, README example, or support artifact.
- A run created sample credentials that should be obviously fake.

## Goal

Catch likely secrets in added diff lines before they become public history.

This is a preflight, not a full security audit. It should stop obvious leaks and force review of suspicious additions.

## Workflow

1. Scan staged changes:

```sh
git diff --cached -- . | agent-secret-sentinel -
```

2. If the repo has no scanner yet, use a plain-text review pass:

```sh
git diff --cached -- . | rg -n "api[_-]?key|secret|token|password|BEGIN .*PRIVATE KEY|AKIA|xox[baprs]-|sk-"
```

3. Treat findings as blockers until one of these is true:

- the value is removed,
- the value is replaced with a clearly fake example,
- the value is already public test data and marked as an example,
- the file is not going to be committed or published.

4. For documentation examples, require obvious fake values:

```text
OPENAI_API_KEY=sk-example-not-real
```

5. For allowed examples, make the allow intent visible in the diff:

```text
OPENAI_API_KEY=sk-example-not-real sentinel: allow-secret-example
```

## Prompt Pattern

```text
Review this agent-generated diff for possible secret exposure.

Inputs:
- diff: <paste or path>
- files intended for commit: <paths>
- public/private destination: <destination>

Tasks:
1. Inspect only added lines.
2. Flag likely private keys, provider tokens, webhook secrets, credentials, and high-entropy values.
3. Separate real blockers from clearly fake examples.
4. Recommend the smallest edit that removes or neutralizes each risk.
5. Do not print full secret-looking values back to the user.
```

## Fast Checklist

- Did the review inspect added lines, not only filenames?
- Did config, CI, deployment, auth, and docs examples get extra attention?
- Are examples obviously fake?
- Were suspicious values removed before commit?
- Did the final answer avoid repeating secret-looking strings?

## Failure Modes

- Assuming `.env.example` cannot leak real credentials.
- Letting an agent paste a token from terminal output into a README.
- Treating a secret scanner as proof that no secrets exist.
- Printing full suspicious values in review comments.
- Allowlisting vague examples that still look usable.

## Source Linkage

- Repo / tool / workflow: local `agent-secret-sentinel` prototype and this profile repo's agent workflow stack.
- Supporting prompt, script, or note: [`./verification-by-change-type.md`](./verification-by-change-type.md), [`./diff-to-eval-case.md`](./diff-to-eval-case.md), and [`../docs/profile-strategy.md`](../docs/profile-strategy.md).

