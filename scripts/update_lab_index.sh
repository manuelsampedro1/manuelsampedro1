#!/usr/bin/env bash
set -euo pipefail

tmp="$(mktemp)"

{
  echo "# AI Lab Notes"
  echo
  echo "Daily notes should capture something concrete: an experiment, a workflow, a bug pattern, a reusable prompt, a tool comparison, or a decision that would help another builder."
  echo
  echo "## Entries"
  echo
  find labs -type f -name "*.md" ! -path "labs/README.md" | sort -r | while read -r file; do
    title="$(grep -m 1 '^# ' "$file" | sed 's/^# //')"
    rel="${file#labs/}"
    echo "- [${title}](./${rel})"
  done
} > "$tmp"

mv "$tmp" labs/README.md

