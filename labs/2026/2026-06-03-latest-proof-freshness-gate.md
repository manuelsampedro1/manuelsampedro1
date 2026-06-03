# 2026-06-03 - Latest Proof Freshness Gate

## What Changed

Added a freshness check to `scripts/profile_quality_audit.py` so the root README
`Latest Proof` section must point to the newest public lab note and the three
newest public recipes.

The check uses Git add time when the artifact is already tracked, matching
`scripts/update_root_readme_latest.sh`. For uncommitted files, it falls back to
filesystem modification time so local maintenance can still catch drift before a
commit exists.

## Why It Matters

The previous guard proved that `Latest Proof` links were present, indexed, and
kept to one lab plus three recipes. That was necessary but not sufficient: a
stale highlight could still pass if it linked older, valid artifacts.

Freshness is a different review property. The first-read surface should show the
newest proof work unless there is a deliberate curation reason to do otherwise.

## Verification Evidence

- Added `latest_public_artifacts` and target comparison logic in
  `scripts/profile_quality_audit.py`.
- Added a regression test where stale but indexed `Latest Proof` links fail.
- Confirmed the current profile still passes `profile-quality-audit.v1` at
  `100/100` with 50 `Selected Work` rows.

## Reusable Lesson

Do not only validate that highlights are well-formed. For profile maintenance,
validate that generated highlights are fresh enough to match the intended
selection rule.
