# JSON Envelope for Verification Gates

Use this when a verification checklist needs to feed another tool, gate, proof packet, or CI artifact.

## Goal

Wrap machine-readable verification categories with enough metadata that downstream automation can tell what was scanned and whether an empty result is intentional.

## Source Event

This recipe came from `verify-by-change` commit `9baf7b4a34c5`, which added `--json-envelope`.

Relevant files:

- `verify_by_change.py`
- `tests/test_verify_by_change.py`
- `README.md`
- `DECISIONS.md`

## Workflow

1. Keep the human-first Markdown output as the default.
2. Keep any legacy JSON shape stable for existing callers.
3. Add an opt-in envelope for automation.
4. Include a schema version.
5. Include source metadata such as explicit paths versus Git scan, repo path, base ref, staged mode, and working-tree inclusion.
6. Include the exact changed file list.
7. Include an explicit `empty` boolean.
8. Put the existing category map under a named `categories` key.

## Checklist

- Can automation distinguish an empty scan from a rendering failure?
- Does the envelope preserve the legacy JSON categories without changing their shape?
- Does the source metadata explain how the file list was collected?
- Is the schema version stable and visible?
- Do tests cover explicit paths, output files, and clean repo scans?

## Verification

For `verify-by-change`:

```sh
python3 -m py_compile verify_by_change.py
python3 -m unittest discover -s tests
python3 verify_by_change.py README.md app.js --json-envelope > /tmp/verification-envelope.json
python3 -m json.tool /tmp/verification-envelope.json >/dev/null
```

## Failure Modes

- Breaking existing `--json` callers while adding metadata.
- Returning `{}` for empty scans with no way to tell whether the scan actually ran.
- Omitting changed files and forcing downstream tools to reconstruct them.
- Hiding whether the scan came from staged changes, a base ref, or the working tree.
- Adding a schema version only in docs instead of the output payload.

## Source Linkage

- Public repo: <https://github.com/manuelsampedro1/verify-by-change>
- Commit: <https://github.com/manuelsampedro1/verify-by-change/commit/9baf7b4a34c51b5e5a52a98d0b04d51622c601a1>
- CI run: <https://github.com/manuelsampedro1/verify-by-change/actions/runs/26794983429>
