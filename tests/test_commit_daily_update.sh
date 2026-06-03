#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
tmp="$(mktemp -d)"

cleanup() {
  rm -rf "$tmp"
}
trap cleanup EXIT

cd "$tmp"
git init -q
git config user.name "Test User"
git config user.email "test@example.com"

mkdir -p scripts
cp "$repo_root/scripts/commit_daily_update.sh" scripts/commit_daily_update.sh
chmod +x scripts/commit_daily_update.sh

for script in update_lab_index.sh update_docs_index.sh update_recipe_index.sh update_radar_index.sh update_root_readme_latest.sh; do
  {
    echo '#!/usr/bin/env bash'
    echo 'set -euo pipefail'
  } > "scripts/$script"
  chmod +x "scripts/$script"
done

echo "# Test Profile" > README.md
git add README.md scripts
git commit -q -m "initial"

echo "local scratch" > scratch.log
output="$(scripts/commit_daily_update.sh "test: no useful change" 2>&1)"

echo "$output" | grep -q "No useful changes to commit."
echo "$output" | grep -q "Warning: working tree still has uncommitted changes after this publish run:"
echo "$output" | grep -q "scratch.log"
