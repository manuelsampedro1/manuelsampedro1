# Flagship Repo Proof Packet

Use this when you already have a small working repo and want to turn it into credible public proof for a GitHub profile, client intro, or Codex portfolio.

## Use When

- You shipped a small tool, CLI, workflow helper, or local-first prototype.
- The repo works, but the public story is still weak or too meta.
- You need one owned repo to carry more proof than three extra notes.

## Goal

Make one repo answer five client questions fast:

1. What problem does it solve?
2. Is it real or just positioning?
3. Can I inspect the implementation quickly?
4. Was it verified honestly?
5. What are the current limits?

## Proof Packet

Before updating the repo or profile, collect these exact inputs:

- Repo link and one-line description.
- The primary artifact: command, screen, output, or workflow the repo actually produces.
- One reason the implementation is inspectable: small codebase, local-first setup, simple CLI, clear script entrypoint, or bounded stack.
- Verification you actually ran.
- One limit you are willing to say publicly.

If any item is missing, fix the repo first instead of polishing the profile.

## Workflow

1. Pick one owned repo with a working artifact, not a half-started idea.
2. Write a blunt one-sentence value statement: user, problem, output.
3. Add a short "how it works" section anchored in the real entrypoint or workflow.
4. Add a "why it matters" section that explains the workflow friction removed.
5. Add a "verification" section with only checks you ran.
6. Add a "limits" section so the proof reads honest instead of salesy.
7. Link one supporting lab note or recipe only if it deepens the repo, not if it distracts from it.
8. Surface that repo in the profile README, pinned repos, or outreach CTA only after the repo page can stand on its own.

## Codex Or Claude Prompt Pattern

```text
Turn this repo into stronger public proof for an AI builder profile.

Inputs:
- Repo purpose: <one sentence>
- Primary artifact: <command, screen, or output>
- Entrypoint files: <paths>
- Verification actually run: <commands/results>
- Current limits: <honest constraints>

Tasks:
1. Rewrite or tighten the README so a client can understand the repo in under 60 seconds.
2. Keep the repo small and inspectable; do not add fake roadmap, fake benchmarks, or generic AI claims.
3. Add only sections supported by the repo today.
4. Surface the exact verification and one clear limit.
5. Suggest one supporting recipe or lab note only if it points back to the repo.

Output:
- proposed README structure,
- 3 strongest proof bullets,
- missing evidence that should block publishing.
```

## Fast Checklist

- Can a stranger identify the artifact in under one minute?
- Does the README show a real output, flow, or entrypoint?
- Is the verification specific enough to trust the claim?
- Is there at least one explicit limit or non-goal?
- Would this repo still look useful if you removed profile-level framing around it?

## Evaluation Pattern

Score each item `0` or `1`:

- Owned proof: the repo contains original work, not commentary only.
- Fast clarity: the README explains user, problem, and output quickly.
- Inspectability: a builder can find the core implementation path fast.
- Honest verification: checks are concrete and believable.
- Honest limits: the repo does not pretend to be broader than it is.

`5`: publish and feature it.
`4`: publish if the repo fills an important proof gap.
`3`: improve the repo page before surfacing it.
`0-2`: do not use it as flagship proof yet.

## Failure Modes

- Using profile copy to compensate for a weak repo page.
- Listing features without showing the artifact they produce.
- Hiding missing verification behind broad language like "production-ready".
- Linking too many notes and making the repo feel secondary.
- Treating size as weakness instead of using small scope as proof of clarity.

## Source Linkage

- Repo / tool / workflow: this profile repo's builder-facing proof system.
- Supporting prompt, script, or note: [`docs/profile-strategy.md`](../docs/profile-strategy.md), [`README.md`](../README.md), and [`labs/2026/2026-05-24-flagship-repos-for-ai-clients.md`](../labs/2026/2026-05-24-flagship-repos-for-ai-clients.md).
