#!/usr/bin/env bash
set -euo pipefail

tmp="$(mktemp)"

{
  echo "# Docs"
  echo
  echo "Public operating docs for the profile workbench. Keep these tied to real scripts, decisions, and publishing rules."
  echo
  echo "## Entries"
  echo
  find docs -type f -name "*.md" ! -path "docs/README.md" | sort | while read -r file; do
    title="$(grep -m 1 '^# ' "$file" | sed 's/^# //')"
    rel="${file#docs/}"
    echo "- [${title}](./${rel})"
  done
} > "$tmp"

mv "$tmp" docs/README.md
