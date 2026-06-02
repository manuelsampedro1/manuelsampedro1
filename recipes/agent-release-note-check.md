# Agent Release Note Check

## Use When

You have generated or edited release notes and need to verify that they match the
actual diff before publishing a GitHub release, changelog entry, proof packet, or
maintainer handoff.

## Inputs

- Markdown release note or changelog draft.
- Unified diff for the release scope.
- Optional score or severity threshold for automation.

## Command

```sh
agent-release-note-check release-notes.md --diff release.diff --min-score 80
```

For JSON automation:

```sh
agent-release-note-check release-notes.md --diff release.diff --format json --fail-on medium
```

## Review Checklist

- Breaking-change signals are covered with migration, compatibility, removed, or
  deprecation language.
- Security-sensitive path changes are covered with security, auth, permission,
  token, secret, or credential language.
- Dependency manifest and lockfile changes are called out explicitly.
- CI, workflow, script, Docker, or automation changes are not hidden behind a
  generic feature note.
- Test changes are paired with verification wording or named checks.
- Release notes do not claim docs-only scope when code files changed.
- Release notes do not claim "fully tested", "no breaking changes", or "no
  security impact" unless the note names evidence and the diff supports it.

## Output Contract

- `status`: `pass`, `pass-with-notes`, `review`, or `blocked`.
- `score`: deterministic score out of 100.
- `changed_files`: path, added lines, removed lines, and tags.
- `findings`: severity, rule, path, message, and redacted evidence.
- `coverage_terms`: release-note categories detected from the note.
- `follow_up_checks`: reviewer actions before publication.

## Source

- Public repo: https://github.com/manuelsampedro1/agent-release-note-check
- Launch note: [2026-06-02 - Agent Release Note Check Public Launch](../labs/2026/2026-06-02-agent-release-note-check-public-launch.md)

