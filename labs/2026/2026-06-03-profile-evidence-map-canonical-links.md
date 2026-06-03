# 2026-06-03 - Profile Evidence Map Canonical Links

## What Changed

Tightened `scripts/profile_quality_audit.py` so
`examples/profile-evidence-map.md` must link every primary claim repo to its
canonical owned GitHub repo root.

Previously, the audit only required repo names to appear somewhere in the
evidence map. That allowed a plain-text mention to pass even though a reviewer
would still need to search manually.

## Why It Matters

The profile is now saturated at 50 `Selected Work` rows. The useful next move is
not more rows; it is making the existing evidence easier to inspect.

Canonical links turn the evidence map into a review route rather than a prose
summary. A reviewer can move from claim to repo without relying on table volume
or naming confidence.

## Verification Evidence

- Added canonical owned repo-root checks for every repo in
  `EVIDENCE_MAP_REPOS`.
- Added a regression test where plain-text repo names no longer satisfy the
  evidence-map gate.
- Confirmed the current profile still passes `profile-quality-audit.v1` at
  `100/100` with 50 `Selected Work` rows.

## Reusable Lesson

When a page exists to prove claims, require direct proof links. Text mentions
are not enough for an evidence map.
