#!/usr/bin/env bash
set -euo pipefail

readme="README.md"

if [ ! -f "$readme" ]; then
  echo "Missing $readme"
  exit 1
fi

lab_file="$(find labs -type f -name "*.md" ! -path "labs/README.md" | sort -r | head -n 1)"

if [ -z "$lab_file" ]; then
  echo "No lab notes found."
  exit 1
fi

latest_recipe_files="$(
  find recipes -type f -name "*.md" ! -path "recipes/README.md" | while read -r file; do
    added_at="$(git log --diff-filter=A --follow --format='%ct' -- "$file" | tail -n 1)"
    if [ -z "$added_at" ]; then
      added_at="$(stat -f '%m' "$file")"
    fi
    printf '%s\t%s\n' "$added_at" "$file"
  done | sort -r -n | head -n 3 | cut -f2-
)"

lab_title="$(grep -m 1 '^# ' "$lab_file" | sed 's/^# //')"

latest_section="$(mktemp)"

{
  echo "## Latest Proof"
  echo
  printf -- "- Latest lab note: [%s](./%s)\n" "$lab_title" "${lab_file#./}"
  echo "- Latest recipes:"
  while read -r recipe_file; do
    [ -z "$recipe_file" ] && continue
    recipe_title="$(grep -m 1 '^# ' "$recipe_file" | sed 's/^# //')"
    printf -- "  - [%s](./%s)\n" "$recipe_title" "${recipe_file#./}"
  done <<< "$latest_recipe_files"
  echo
} > "$latest_section"

tmp="$(mktemp)"
awk -v replacement="$latest_section" '
  BEGIN {
    while ((getline line < replacement) > 0) {
      block = block line "\n"
    }
    close(replacement)
  }
  /^## Latest Proof$/ {
    printf "%s", block
    skip = 1
    next
  }
  /^## Principles$/ {
    skip = 0
  }
  !skip {
    print
  }
' "$readme" > "$tmp"

mv "$tmp" "$readme"
rm -f "$latest_section"
