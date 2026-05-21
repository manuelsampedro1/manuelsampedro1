#!/usr/bin/env bash
set -euo pipefail

tmp="$(mktemp)"

{
  echo "# Tooling Radar"
  echo
  echo "Short notes on AI coding tools, agent infrastructure, evals, and product workflows."
  echo
  echo "Each radar entry should include:"
  echo
  echo "- What changed or what was tested."
  echo "- Why it matters for builders."
  echo "- One practical takeaway."
  echo "- Sources when the note depends on current external facts."
  echo
  echo "## Entries"
  echo
  find radar -type f -name "*.md" ! -path "radar/README.md" | sort -r | while read -r file; do
    title="$(grep -m 1 '^# ' "$file" | sed 's/^# //')"
    rel="${file#radar/}"
    echo "- [${title}](./${rel})"
  done
} > "$tmp"

mv "$tmp" radar/README.md
