# Profile Proof Audit

Use this before treating a GitHub profile README as ready for serious external review.

## Use When

- The profile links to multiple repos, recipes, and lab notes.
- You added new public proof and need to verify the surface stayed coherent.
- You want to catch broken relative links before pushing.
- You need an HTTP pass over promoted repo links without adding credentials.

## Goal

Turn profile quality into a repeatable audit:

- required sections,
- Selected Work table shape,
- Latest Proof entries,
- relative link existence,
- optional external HTTP status,
- risky unsupported phrasing,
- score, issues, and warnings.

## Workflow

1. Audit local structure:

```sh
profile-proof-audit README.md
```

2. Audit public links when profile links changed:

```sh
profile-proof-audit README.md --check-http
```

3. Treat these as blockers:

- missing required sections,
- broken relative links,
- promoted GitHub repos returning `404`,
- unsupported guarantee language,
- Selected Work with too few proof rows.

4. Only promote a local repo after the public URL returns `200` and the repo page can stand alone.

## Prompt Pattern

```text
Audit this GitHub profile README for proof quality.

Rules:
- Check required sections: Current Focus, Selected Work, How I Work With Codex, Public Workbench, Latest Proof, Principles.
- Check every relative Markdown link against the repo.
- Check promoted external links when HTTP access is available.
- Flag unsupported guarantee language.
- Do not fix the profile by hiding broken proof; either repair the proof or move it back to TODO.

Output:
- score,
- issues,
- warnings,
- exact links or sections to fix.
```

## Fast Checklist

- Does every promoted repo URL return `200`?
- Do all relative links resolve locally?
- Does Selected Work contain at least three strong proof rows?
- Does Latest Proof show recent real artifacts?
- Are local-only repos kept in TODO instead of public claims?

## Failure Modes

- Promoting a local repo before the GitHub URL exists.
- Trusting README appearance without checking links.
- Treating a cached raw README as proof of current `main`.
- Using confidence words such as "perfect" or "production-ready" without evidence.
- Letting recipes accumulate without a clear path back to working repos.

## Source Linkage

- Repo / tool / workflow: local `profile-proof-audit` prototype at `/Users/manuelsampedro/Documents/Codex/2026-05-21/profile-proof-audit`.
- Supporting prompt, script, or note: [`./publish-queue-for-local-agent-repos.md`](./publish-queue-for-local-agent-repos.md), [`./public-surface-sync-for-agent-repos.md`](./public-surface-sync-for-agent-repos.md), and [`../docs/profile-strategy.md`](../docs/profile-strategy.md).
