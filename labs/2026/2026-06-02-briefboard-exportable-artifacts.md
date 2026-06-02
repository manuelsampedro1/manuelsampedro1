# 2026-06-02 - Briefboard Exportable Artifacts

## Context

`briefboard-local` already had a public preview, but the product was still mostly a copy-to-clipboard tool. For a stronger product proof, the output needed to become portable: a client brief should leave the browser as files a reviewer or agent can keep.

## Change

- Added `brief-format.js` as a dependency-free formatter shared by the browser app and Node tests.
- Added downloads for the Markdown brief, text Codex prompt, and JSON draft.
- Added `node --test` coverage for field normalization, Markdown rendering, prompt rendering, JSON export, and safe file names.
- Updated README, `DECISIONS.md`, and the SVG preview to match the new export flow.
- Configured the repo-local Git author identity with the documented no-reply GitHub address before committing.

Public commit: `aef19c449924 feat: add exportable brief artifacts`.

## Verification

Local checks:

```sh
node --test
node --check brief-format.js
node --check app.js
node --check tests/brief-format.test.cjs
python3 - <<'PY'
from xml.etree import ElementTree as ET
ET.parse('docs/preview.svg')
print('svg xml ok')
PY
git diff --check
```

Local HTTP smoke check:

```sh
python3 -m http.server 4173 --bind 127.0.0.1
curl -L -s -o /dev/null -w "%{http_code}\n" http://127.0.0.1:4173/
curl -L -s -o /dev/null -w "%{http_code}\n" http://127.0.0.1:4173/brief-format.js
curl -L -s -o /dev/null -w "%{http_code}\n" http://127.0.0.1:4173/app.js
curl -L -s -o /dev/null -w "%{http_code}\n" http://127.0.0.1:4173/docs/preview.svg
```

Results:

- `node --test`: 5 tests passed.
- SVG XML parse passed.
- Local HTTP assets returned `200`.
- Public raw `brief-format.js` and `tests/brief-format.test.cjs` returned `200`.

`npm` is not installed in the local environment, so verification used `node --test` directly.

## Source Linkage

- Repo: <https://github.com/manuelsampedro1/briefboard-local>
- Commit: <https://github.com/manuelsampedro1/briefboard-local/commit/aef19c449924fa167df909fc3bc03b70a721c612>
- Formatter: <https://raw.githubusercontent.com/manuelsampedro1/briefboard-local/aef19c4/brief-format.js>
- Tests: <https://raw.githubusercontent.com/manuelsampedro1/briefboard-local/aef19c4/tests/brief-format.test.cjs>

## Takeaway

Small product repos should prove more than taste: they should show a useful workflow, exportable output, and tests around the core transformation. This moves `briefboard-local` closer to a real agent-work kickoff tool without adding backend weight.
