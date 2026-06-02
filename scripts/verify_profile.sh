#!/usr/bin/env bash
set -euo pipefail

bash -n \
  scripts/new_daily_lab_note.sh \
  scripts/update_lab_index.sh \
  scripts/update_recipe_index.sh \
  scripts/update_radar_index.sh \
  scripts/update_root_readme_latest.sh \
  scripts/commit_daily_update.sh \
  scripts/verify_profile.sh \
  tests/test_commit_daily_update.sh

python3 -m py_compile scripts/profile_quality_audit.py
python3 -m unittest discover -s tests
bash tests/test_commit_daily_update.sh
python3 scripts/profile_quality_audit.py --root . --min-score 100 >/dev/null

tmp="$(mktemp -d)"
cleanup() {
  rm -rf "$tmp"
}
trap cleanup EXIT

mkdir -p "$tmp/labs" "$tmp/recipes" "$tmp/radar"
cp README.md "$tmp/README.md"
cp labs/README.md "$tmp/labs/README.md"
cp recipes/README.md "$tmp/recipes/README.md"
cp radar/README.md "$tmp/radar/README.md"

scripts/update_lab_index.sh
scripts/update_recipe_index.sh
scripts/update_radar_index.sh
scripts/update_root_readme_latest.sh

for file in README.md labs/README.md recipes/README.md radar/README.md; do
  if ! cmp -s "$file" "$tmp/$file"; then
    echo "$file changed after regeneration. Re-run the update scripts and review the diff."
    exit 1
  fi
done
