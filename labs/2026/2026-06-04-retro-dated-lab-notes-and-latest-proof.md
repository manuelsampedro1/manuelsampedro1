# 2026-06-04 - Retro-Dated Lab Notes and Latest Proof

## Context

I wanted to verify a subtle publish behavior in this profile repo before
assuming the lab index and the root README highlight always point at the same
"newest" note.

The practical question was: what happens when I publish a lab note today but
give it an older date in the filename because it documents an earlier
experiment or backfilled repo work?

## Useful Artifact

Treat the two surfaces as different views with different ordering rules:

- [`labs/README.md`](../../labs/README.md) is an archive index ordered by
  filename, so backfilled notes stay in chronological filename position.
- Root [`README.md`](../../README.md) `Latest Proof` is ordered by publication
  freshness using Git add time, so a newly added backfilled note can still
  become the highlighted latest lab proof.

That means a retro-dated note is safe when you want the archive to preserve its
historical date while still letting the profile highlight the most recently
published proof.

## Source Linkage

- Repo / tool / workflow: this profile repo's lab-note publish flow
- Supporting prompt, script, or file:
  [`scripts/update_lab_index.sh`](../../scripts/update_lab_index.sh),
  [`scripts/update_root_readme_latest.sh`](../../scripts/update_root_readme_latest.sh),
  and [`DECISIONS.md`](../../DECISIONS.md)

## Notes

- Observation: in a temp clone, adding
  `labs/2026/2026-05-15-retro-added-note-ordering-check.md` left the top of
  [`labs/README.md`](../../labs/README.md) unchanged because the index sorts by
  reverse filename order.
- Observation: the same temp-clone run changed root
  [`README.md`](../../README.md) `Latest Proof` to the retro-dated note because
  [`scripts/update_root_readme_latest.sh`](../../scripts/update_root_readme_latest.sh)
  selects the newest lab by Git add time.
- Tradeoff: the two surfaces can disagree briefly by design. The index answers
  "where does this note belong in the archive?" while `Latest Proof` answers
  "what was published most recently?"
- Failure mode: if a reviewer expects the first entry in
  [`labs/README.md`](../../labs/README.md) to match the root highlight, a
  backfilled note can look like drift even when both generators are behaving
  correctly.

## Verification

Local temp-clone verification completed for this note:

- cloned this repo into a temporary directory, removed `origin`, and set a
  throwaway local Git identity,
- added `labs/2026/2026-05-15-retro-added-note-ordering-check.md` by hand,
- ran [`scripts/update_lab_index.sh`](../../scripts/update_lab_index.sh) and
  confirmed the top of [`labs/README.md`](../../labs/README.md) still started
  with `2026-06-03` entries,
- ran
  [`scripts/update_root_readme_latest.sh`](../../scripts/update_root_readme_latest.sh)
  and confirmed root [`README.md`](../../README.md) `Latest Proof` switched to
  the retro-dated note,
- inspected `git status --short` in the temp clone and confirmed only the retro
  note, [`labs/README.md`](../../labs/README.md), and root
  [`README.md`](../../README.md) changed.

## Next Step

Document this distinction whenever a workflow intentionally backfills dated lab
notes, so reviewers do not mistake the archive order for a broken freshness
rule.
