# 2026-06-02 - Briefboard JSON Restore Loop

## Context

`briefboard-local` had become a stronger product proof after adding Markdown, text, and JSON exports. The remaining workflow gap was obvious: a downloaded JSON draft could leave the browser, but the app could not restore it. That made the export useful as an artifact, but not yet as a working loop.

## Change

- Added a shared `parseJsonImport` formatter that validates `briefboard-local.v1` JSON exports.
- Added browser import controls for saved JSON drafts, including accessible status feedback for success and validation errors.
- Hardened draft restoration so corrupted `localStorage` data does not leak bad values into the form.
- Added Node tests for exported JSON import, raw draft-object import, and invalid JSON/schema rejection.
- Updated README verification steps and `DECISIONS.md` so the product rationale matches the new restore loop.

Public commit: `205a58723072 feat: restore exported brief drafts`.

## Verification

Local checks:

```sh
node --test
node --check app.js
node --check brief-format.js
git diff --check
```

Local static smoke check:

```sh
python3 -m http.server 4173
curl -I http://localhost:4173/index.html
curl -I http://localhost:4173/app.js
curl -I http://localhost:4173/brief-format.js
```

Results:

- `node --test`: 8 tests passed.
- JS syntax checks passed.
- `git diff --check` passed.
- Local static assets returned `200 OK`.
- Public commit page, raw `brief-format.js`, and raw `tests/brief-format.test.cjs` returned `200`.

## Source Linkage

- Repo: <https://github.com/manuelsampedro1/briefboard-local>
- Commit: <https://github.com/manuelsampedro1/briefboard-local/commit/205a587230721776100bc68d2a47eabc87c22499>
- Formatter and import contract: <https://raw.githubusercontent.com/manuelsampedro1/briefboard-local/205a587230721776100bc68d2a47eabc87c22499/brief-format.js>
- Tests: <https://raw.githubusercontent.com/manuelsampedro1/briefboard-local/205a587230721776100bc68d2a47eabc87c22499/tests/brief-format.test.cjs>

## Takeaway

For local-first tools, export is only half of portability. A serious workflow needs a round trip: save the structured artifact, restore it later, validate the format, and keep the whole loop testable without adding backend infrastructure.
