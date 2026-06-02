# Local-First Draft Round Trip

Use this when a browser-only product exports structured work that users may need to restore later without accounts, sync, or a backend.

## Goal

Turn a local export into a complete workflow: save the draft, restore the same draft, validate the payload, and keep the core format testable outside the browser.

## Source Event

This recipe came from `briefboard-local` commit `205a58723072`, which added JSON import support after the app already exported Markdown, text, and JSON artifacts.

Relevant files:

- `brief-format.js`
- `app.js`
- `index.html`
- `tests/brief-format.test.cjs`

## Workflow

1. Put the export and import format in a shared dependency-free module.
2. Include a stable `schema_version` in the exported JSON.
3. Normalize only known fields when exporting and importing.
4. Reject invalid JSON, unknown schema versions, and wrapper payloads without a draft object.
5. Let the UI import a local file without sending data to a server.
6. Show import success or error status in the page, not only in the console.
7. Re-render generated outputs immediately after restore so the imported state is visibly active.
8. Keep accepting raw draft objects only if that helps manual handoff files and the fields are still normalized.

## Checklist

- Can an exported JSON file be imported back into the same app?
- Does a bad file fail with a clear message instead of silently changing state?
- Are unknown fields ignored rather than persisted into output?
- Does the import path reuse the same normalization as render/export?
- Can the core parser be tested with `node --test`?

## Verification

For a static browser app, run:

```sh
node --test
node --check app.js
node --check brief-format.js
git diff --check
```

Then serve the app locally and check the main static assets:

```sh
python3 -m http.server 4173
curl -I http://localhost:4173/index.html
curl -I http://localhost:4173/app.js
curl -I http://localhost:4173/brief-format.js
```

## Failure Modes

- Exporting JSON with no matching import path.
- Parsing imported JSON directly in UI code instead of testing the parser in isolation.
- Accepting any schema and making old or unrelated files look valid.
- Importing unknown fields into generated prompts.
- Showing import failures only in `console.warn`, where users will miss them.

## Source Linkage

- Public repo: <https://github.com/manuelsampedro1/briefboard-local>
- Commit: <https://github.com/manuelsampedro1/briefboard-local/commit/205a587230721776100bc68d2a47eabc87c22499>
- Import parser: <https://raw.githubusercontent.com/manuelsampedro1/briefboard-local/205a587230721776100bc68d2a47eabc87c22499/brief-format.js>
