# Backfilled Lab Note Latest Proof Check

Use this when you want to publish a lab note today with an older date in the filename because it documents earlier work, and you need to verify that your public archive and your profile highlight will behave intentionally instead of looking broken.

## Goal

Preserve both truths at once:

- the lab archive should keep the note in chronological filename order,
- the root `README.md` "Latest Proof" section should highlight the most recently published proof.

## Workflow

1. Add or draft the backfilled note with the date that matches the work, not the publish day.

```sh
cp templates/daily-lab-note.md labs/2026/2026-05-15-example-backfill.md
```

2. Regenerate the lab index and confirm the note lands where its filename says it belongs.

```sh
scripts/update_lab_index.sh
sed -n '1,20p' labs/README.md
```

3. Regenerate the root highlight and confirm it follows publish freshness instead of filename order.

```sh
scripts/update_root_readme_latest.sh
rg -n "Latest Proof|2026-05-15-example-backfill" README.md
```

4. If you are unsure about side effects, run the check in a temp clone instead of experimenting in the live repo.

```sh
tmp="$(mktemp -d)"
git clone . "$tmp/repo" >/dev/null
cd "$tmp/repo"
git remote remove origin || true
git config user.name "Local Check"
git config user.email "local-check@example.com"
```

5. Treat archive order and highlight order as separate outputs with separate invariants:

- `labs/README.md` answers "where does this note belong in the archive?"
- root `README.md` `Latest Proof` answers "what proof was published most recently?"

6. Publish only if both surfaces match that split on purpose. If they differ unexpectedly, inspect the generator scripts before editing the indexes by hand.

## Prompt Pattern

```text
I am adding a retro-dated lab note to a public AI builder repo.

Check two surfaces separately:
- the folder index should keep chronological filename order,
- the root "Latest Proof" section should reflect publication freshness.

Tasks:
1. Add or inspect the dated note.
2. Run the index generator and the root latest-proof generator.
3. Explain whether differing outputs are expected or a bug.
4. Report the exact changed paths.

Rules:
- Do not hand-edit generated indexes before checking the scripts.
- If the behavior is ambiguous, reproduce it in a temp clone first.
- Treat archive order and publish freshness as different concerns.
```

## Fast Checklist

- Does the backfilled note filename reflect the work date, not the publish date?
- Did `labs/README.md` place it by reverse filename order?
- Did root `README.md` `Latest Proof` treat it as newly published proof?
- Did you verify the behavior with scripts instead of manual README edits?
- Did you report the exact paths that changed?

## Failure Modes

- Assuming the first entry in `labs/README.md` must always match root `README.md`.
- Hand-editing generated indexes and hiding the actual script behavior.
- Using the live repo to test uncertain publish behavior instead of a temp clone.
- Treating a backfilled note as broken because the archive and highlight disagree by design.

## Verification

Run the smallest pair of checks that exercises both views:

```sh
scripts/update_lab_index.sh
scripts/update_root_readme_latest.sh
```

If the behavior is surprising, repeat the same steps in a temp clone and inspect `git status --short` there before touching the real repo.

## Source Linkage

- Repo / tool / workflow: this profile repo's lab-note publish flow.
- Supporting prompt, script, or note: [`../labs/2026/2026-06-04-retro-dated-lab-notes-and-latest-proof.md`](../labs/2026/2026-06-04-retro-dated-lab-notes-and-latest-proof.md), [`../recipes/latest-proof-freshness-gate.md`](./latest-proof-freshness-gate.md), [`../scripts/update_lab_index.sh`](../scripts/update_lab_index.sh), and [`../scripts/update_root_readme_latest.sh`](../scripts/update_root_readme_latest.sh).
