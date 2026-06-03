# Profile Evidence Map Link Gate

Use this pattern when a public profile includes a claim-to-evidence map.

## Problem

A claim map can drift into a list of repo names:

- repo names are present,
- claims look mapped,
- reviewers still need to search manually,
- links can point to non-canonical locations.

## Gate

Require every primary claim repo to appear as a canonical repo-root link:

```text
https://github.com/<owner>/<repo>
```

For this profile, the audit checks each repo in `EVIDENCE_MAP_REPOS` against
`https://github.com/manuelsampedro1/<repo>`.

## Command

```sh
python3 scripts/profile_quality_audit.py --root . --format json --min-score 100
```

## Review Rule

If a claim needs a repo as evidence, link the repo root directly. Use examples
or recipes for secondary narratives instead of relying on unlinked names.
