# 2026-06-02 - Briefboard Readiness Before Handoff

## Context

`briefboard-local` already turned kickoff notes into a structured brief, prompt, and exportable local artifacts. The remaining product risk was more subtle: a generated Codex prompt could look polished while still missing essentials such as audience, problem, deliverable, or acceptance criteria.

For agent work, that is a real failure mode. A vague brief does not become safer because it is formatted well.

## Change

- Added a shared readiness check for essential brief fields.
- Rendered missing essentials inside the generated project brief.
- Added the same readiness context to the Codex-ready prompt before the implementation request.
- Kept the check descriptive instead of inventing a fake quality score.
- Added Node formatter tests for ready and incomplete drafts.
- Added a GitHub Actions workflow that runs the formatter test suite on push and pull request.

Public behavior commit: `3346373fdfd0 feat: flag incomplete Codex briefs`.

Public CI commit: `796e482fe64e ci: add formatter test workflow`.

## Verification

Local checks:

```sh
node --test
git diff --check
```

Results:

- `node --test`: 9 tests passed.
- `git diff --check` passed.
- Public commit pages returned `200`.
- Raw `brief-format.js`, `tests/brief-format.test.cjs`, and `.github/workflows/ci.yml` returned `200`.
- GitHub Actions run `26794326305` completed with conclusion `success`.

## Source Linkage

- Repo: <https://github.com/manuelsampedro1/briefboard-local>
- Behavior commit: <https://github.com/manuelsampedro1/briefboard-local/commit/3346373fdfd0a2e104f564fd870567edd353105e>
- CI commit: <https://github.com/manuelsampedro1/briefboard-local/commit/796e482fe64edc76c508ba2a49f31a07a9c98563>
- CI run: <https://github.com/manuelsampedro1/briefboard-local/actions/runs/26794326305>
- Formatter: <https://raw.githubusercontent.com/manuelsampedro1/briefboard-local/3346373fdfd0a2e104f564fd870567edd353105e/brief-format.js>
- Tests: <https://raw.githubusercontent.com/manuelsampedro1/briefboard-local/3346373fdfd0a2e104f564fd870567edd353105e/tests/brief-format.test.cjs>

## Takeaway

A handoff tool should not only format the user's request. It should expose missing inputs before the agent receives the prompt, while keeping the rule simple enough to test and challenge.
