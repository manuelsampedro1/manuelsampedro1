#!/usr/bin/env bash
set -euo pipefail

message="${1:-daily: update ai builder workbench}"

if ! git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  echo "Not inside a git repository."
  exit 1
fi

scripts/update_lab_index.sh

if [ -z "$(git status --porcelain -- .)" ]; then
  echo "No useful changes to commit."
  exit 0
fi

git_name="$(git config --get user.name || true)"
git_email="$(git config --get user.email || true)"

if [ -z "$git_name" ] || [ -z "$git_email" ] || [[ "$git_email" == *.local ]]; then
  echo "Configure a Git identity with a verified GitHub email before committing:"
  echo "  git config user.name \"Manuel Sampedro\""
  echo "  git config user.email \"YOUR_VERIFIED_GITHUB_EMAIL\""
  echo "Then amend the existing commit if needed:"
  echo "  git commit --amend --reset-author"
  exit 1
fi

git add README.md DECISIONS.md TODO.md docs labs recipes radar templates scripts .gitignore

if git diff --cached --quiet -- .; then
  echo "No useful changes to commit."
  exit 0
fi

git commit -m "$message"

if git remote get-url origin >/dev/null 2>&1; then
  git push
else
  echo "Committed locally. Add a remote named origin to push to GitHub."
fi
