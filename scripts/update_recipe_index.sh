#!/usr/bin/env bash
set -euo pipefail

tmp="$(mktemp)"

{
  echo "# Recipes"
  echo
  echo "Reusable AI-building patterns live here. Keep each recipe short, practical, and testable."
  echo
  echo "## Suggested Types"
  echo
  echo "- Coding-agent repo loop."
  echo "- Prompt template with failure modes."
  echo "- Evaluation checklist."
  echo "- Automation runbook."
  echo "- Small implementation pattern."
  echo
  echo "## Entries"
  echo
  find recipes -type f -name "*.md" ! -path "recipes/README.md" | sort -r | while read -r file; do
    title="$(grep -m 1 '^# ' "$file" | sed 's/^# //')"
    rel="${file#recipes/}"
    echo "- [${title}](./${rel})"
  done
} > "$tmp"

mv "$tmp" recipes/README.md
