# 2026-06-02 - Verify by Change JSON Envelope

## Context

`verify-by-change` already supported Markdown checklists and compact JSON category output. That was useful for humans and simple scripts, but downstream gates still had to infer key metadata: which source mode produced the checklist, which files were scanned, and whether the result was intentionally empty.

For agent workflows, that metadata matters. A proof packet or merge gate should be able to distinguish "no changed files were detected" from "the category map happened to be empty."

## Change

- Added `--json-envelope`.
- Kept legacy `--json` unchanged as the compact category map.
- Added `schema_version`, `source`, `changed_files`, `empty`, and `categories` to the envelope.
- Recorded whether input came from explicit paths or Git scanning.
- Preserved repo, base ref, staged mode, and include-working-tree metadata for Git scans.
- Added tests for the helper, output-file CLI path, and empty repo scans.
- Updated README verification steps and `DECISIONS.md`.

Public commit: `9baf7b4a34c5 feat: add json envelope output`.

## Verification

Local checks:

```sh
python3 -m py_compile verify_by_change.py
python3 -m unittest discover -s tests
python3 verify_by_change.py verify_by_change.py README.md >/tmp/verify-output.txt
python3 verify_by_change.py --repo . --staged --json --output /tmp/verify-staged.json
python3 verify_by_change.py verify_by_change.py README.md --json-envelope >/tmp/verify-envelope.json
python3 verify_by_change.py --repo . --base HEAD --include-working-tree >/tmp/verify-base-plus-working-tree.txt
python3 verify_by_change.py --repo . --fail-on-empty >/tmp/verify-empty-check.txt || test $? -eq 2
test -s /tmp/verify-output.txt
git diff --check
```

Results:

- Python compile passed.
- `python3 -m unittest discover -s tests`: 15 tests passed.
- Legacy JSON output still parsed as the existing category map.
- JSON envelope output included schema, source metadata, changed files, empty state, and categories.
- `git diff --check` passed.
- Public commit page and raw changed files returned `200`.
- GitHub Actions run `26794983429` completed with conclusion `success`.

## Source Linkage

- Repo: <https://github.com/manuelsampedro1/verify-by-change>
- Commit: <https://github.com/manuelsampedro1/verify-by-change/commit/9baf7b4a34c51b5e5a52a98d0b04d51622c601a1>
- CI run: <https://github.com/manuelsampedro1/verify-by-change/actions/runs/26794983429>
- CLI: <https://raw.githubusercontent.com/manuelsampedro1/verify-by-change/9baf7b4a34c51b5e5a52a98d0b04d51622c601a1/verify_by_change.py>
- Tests: <https://raw.githubusercontent.com/manuelsampedro1/verify-by-change/9baf7b4a34c51b5e5a52a98d0b04d51622c601a1/tests/test_verify_by_change.py>

## Takeaway

Machine-readable verification artifacts need metadata, not only buckets. A schema and explicit empty state make downstream agent gates stricter without breaking the human-first checklist flow.
