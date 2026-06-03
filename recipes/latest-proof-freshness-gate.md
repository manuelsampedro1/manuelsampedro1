# Latest Proof Freshness Gate

Use this pattern when a public README has a small highlight section backed by
generated indexes.

## Problem

A highlight can be valid but stale:

- every link resolves,
- every link appears in the matching index,
- the section has the intended number of links,
- newer public evidence exists but is not shown.

## Gate

Compare highlight links against the same ranking rule used by the refresh
script. In this repo, that means:

- one newest lab note,
- three newest recipes,
- Git add time for tracked files,
- filesystem modification time for uncommitted files.

## Command

```sh
python3 scripts/profile_quality_audit.py --root . --format json --min-score 100
```

## Review Rule

Treat stale highlights as maintenance drift. Either refresh the generated
section or record a deliberate curation decision before overriding the freshness
rule.
