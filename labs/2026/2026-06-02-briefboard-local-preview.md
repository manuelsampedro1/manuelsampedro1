# 2026-06-02 - Briefboard Local Preview

## Context

`briefboard-local` was already a public local-first product example, but its README asked readers to infer the workflow from text only. The open profile TODO was to add a lightweight real screenshot or SVG preview if it improved the repo without adding noise.

## Change

- Added a static SVG preview at `docs/preview.svg`.
- Linked the preview near the top of the README.
- Pushed the public commit `b42607b02f44 docs: add briefboard preview`.

## Verification

Local checks before push:

```sh
python3 - <<'PY'
from xml.etree import ElementTree as ET
ET.parse('docs/preview.svg')
print('svg xml ok')
PY
git diff --check
git diff --cached --check
```

Public checks after push:

```sh
curl -L -s -o /dev/null -w "%{http_code}\n" https://raw.githubusercontent.com/manuelsampedro1/briefboard-local/b42607b/docs/preview.svg
curl -L -s https://raw.githubusercontent.com/manuelsampedro1/briefboard-local/b42607b/README.md | grep -n "Briefboard Local preview"
```

Results:

- Raw SVG returned `200`.
- Raw README includes `![Briefboard Local preview](docs/preview.svg)`.

## Source Linkage

- Repo: <https://github.com/manuelsampedro1/briefboard-local>
- Commit: <https://github.com/manuelsampedro1/briefboard-local/commit/b42607b02f44>
- Raw SVG: <https://raw.githubusercontent.com/manuelsampedro1/briefboard-local/b42607b/docs/preview.svg>

## Takeaway

Profile proof repos should reduce first-read friction with visible evidence when it is cheap and honest. A small SVG preview is enough here: it shows the product shape without adding screenshot maintenance, external assets, or fake activity.
