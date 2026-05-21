#!/usr/bin/env bash
set -euo pipefail

title="${1:-daily-ai-agent-note}"
today="${TODAY:-$(date +%F)}"
year="$(date -j -f "%Y-%m-%d" "$today" +%Y 2>/dev/null || date +%Y)"
slug="$(printf '%s' "$title" | tr '[:upper:]' '[:lower:]' | tr -cs 'a-z0-9' '-' | sed 's/^-//;s/-$//')"
dir="labs/${year}"
file="${dir}/${today}-${slug}.md"

mkdir -p "$dir"

if [ -f "$file" ]; then
  echo "$file"
  exit 0
fi

cp templates/daily-lab-note.md "$file"
sed -i '' "s/YYYY-MM-DD/${today}/" "$file"
sed -i '' "s/Title/${title}/" "$file"
echo "$file"

