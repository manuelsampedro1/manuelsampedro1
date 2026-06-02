# Profile Verification Proof Packet

Use this example as the expected shape for a profile maintenance proof packet.

## Scenario

The profile repository changed after a real public tool improvement, and the maintainer needs to prove the profile surface, indexes, automation scripts, remote state, and CI signal are still coherent.

## Evidence Commands

```sh
bash -n scripts/new_daily_lab_note.sh scripts/update_lab_index.sh scripts/commit_daily_update.sh
make test
make lint
make build
git diff --check
node /path/to/repo-flightcheck/bin/repo-flightcheck.js . --check-remote --strict --threshold 80
```

## Expected Signals

- `make test`, `make lint`, and `make build` all run `scripts/verify_profile.sh`.
- `scripts/verify_profile.sh` validates shell syntax, regenerates public indexes, refreshes latest-proof links, and fails if generated files drift.
- `repo-flightcheck --check-remote --strict --threshold 80` passes with a clean working tree and published `origin/main`.
- The GitHub Actions workflow badge for `.github/workflows/ci.yml` reports `CI - passing`.
- Raw GitHub URLs for newly published lab notes, recipes, examples, or scripts return `200`.

## Failure Modes This Catches

- A profile README link points to a missing recipe, lab note, or generated index entry.
- A maintenance script works on macOS but fails in GitHub Actions.
- A generated index was edited manually and drifts from the scripts.
- The root README claims a latest proof artifact that is not the latest committed artifact.
- A public proof claim exists before the backing commit, CI run, or raw file is reachable.

## Review Prompt

```text
Review this profile maintenance change as a proof packet, not as copywriting.
Check whether every public claim has a backing repo, commit, command, CI signal,
or raw artifact URL. Flag any surface-only wording that is not supported by
the changed files or verification output.
```
