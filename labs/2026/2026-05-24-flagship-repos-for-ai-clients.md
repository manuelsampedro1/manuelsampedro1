# 2026-05-24 - Flagship Repos for AI Client Credibility

## Context

The profile README was already public, but it still looked too much like a workbench and not enough like proof. The main weakness was obvious: the surface had commentary and process, but not enough owned repos that a client could click and evaluate quickly.

## Useful Artifact

I published three small owned repos that map directly to the kind of work I actually do in Codex:

- [codex-review-packet](https://github.com/manuelsampedro1/codex-review-packet): a Python CLI that bundles diff + repo context into a sharper review packet.
- [verify-by-change](https://github.com/manuelsampedro1/verify-by-change): a Python CLI that suggests verification steps from changed files.
- [briefboard-local](https://github.com/manuelsampedro1/briefboard-local): a local-first browser app that turns kickoff notes into a build brief and Codex prompt.

That changes the profile from "mostly meta" to "here are three owned tools/products you can inspect right now".

## Source Linkage

- Repo / tool / workflow: [manuelsampedro1/codex-review-packet](https://github.com/manuelsampedro1/codex-review-packet), [manuelsampedro1/verify-by-change](https://github.com/manuelsampedro1/verify-by-change), [manuelsampedro1/briefboard-local](https://github.com/manuelsampedro1/briefboard-local)
- Supporting prompt, script, or file: [`README.md`](../../README.md), [`docs/profile-strategy.md`](../../docs/profile-strategy.md), and [`scripts/commit_daily_update.sh`](../../scripts/commit_daily_update.sh)

## Notes

- Observation: the fastest way to improve first impression was not another recipe. It was shipping owned repos with real code and honest README files.
- Tradeoff: these v1 repos are intentionally small. That is good for trust, but it means the next wave of artifacts should deepen them instead of creating five more surfaces.
- Failure mode: if future profile updates return to meta-content without repo-backed proof, the profile will drift back toward looking busy rather than useful.

## Verification

Checked locally before publish:

- `python3 -m py_compile` passed for both Python repos.
- `codex-review-packet` produced a non-empty Markdown packet.
- `verify-by-change` produced a non-empty checklist.
- `briefboard-local` served successfully over a local `python3 -m http.server`.

Checked publicly after publish:

- all three repos were created under `manuelsampedro1`,
- each repo pushed successfully to `main`,
- the repos are public and visible through the GitHub API.

## Next Step

Pin these repos on the public profile and make the next notes/recipes come from them, not from profile maintenance alone.
