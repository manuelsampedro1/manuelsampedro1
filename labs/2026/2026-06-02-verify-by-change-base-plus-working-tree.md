# 2026-06-02 - Verify by Change Base Plus Working Tree

## Context

`verify-by-change` could scan explicit paths, staged changes, full working-tree changes, or a committed diff against a base ref. The remaining gap was mixed agent work: a Codex session can have a committed change against `origin/main` plus local staged, unstaged, or untracked follow-ups that still need verification.

If the checklist only uses `--base`, the uncommitted follow-ups can be invisible. If it only uses the working tree, the committed PR diff can be invisible. The tool needed an explicit merged mode.

## Change

- Added `--include-working-tree`.
- Kept `--base` unchanged by default for CI and PR-diff users.
- When `--base` and `--include-working-tree` are both set, merged committed diff paths with staged, unstaged, and untracked paths.
- Added ordered de-duplication so a file changed in both places appears once.
- Added function and CLI tests for base-ref plus working-tree detection.
- Updated README and `DECISIONS.md`.

Public commit: `1d38d6264dd1 feat: combine base diff with working tree`.

## Verification

Local checks:

```sh
python3 -m py_compile verify_by_change.py
python3 -m unittest discover -s tests
python3 verify_by_change.py --repo . --base HEAD --include-working-tree >/tmp/verify-base-plus-working-tree.txt
test -s /tmp/verify-base-plus-working-tree.txt
grep -q 'verify_by_change.py' /tmp/verify-base-plus-working-tree.txt
python3 verify_by_change.py --repo . --staged --json --output /tmp/verify-staged.json
test -s /tmp/verify-staged.json
git diff --check
```

Results:

- Python compile passed.
- `python3 -m unittest discover -s tests`: 12 tests passed.
- The new CLI mode generated a non-empty checklist from the current working tree while using `--base HEAD`.
- Staged JSON output still worked.
- `git diff --check` passed.
- Public commit page and raw changed files returned `200`.
- GitHub Actions run `26793937990` completed with conclusion `success`.

## Source Linkage

- Repo: <https://github.com/manuelsampedro1/verify-by-change>
- Commit: <https://github.com/manuelsampedro1/verify-by-change/commit/1d38d6264dd11c7e3b0e0f2bab2dbc015a19886c>
- CI run: <https://github.com/manuelsampedro1/verify-by-change/actions/runs/26793937990>
- CLI: <https://raw.githubusercontent.com/manuelsampedro1/verify-by-change/1d38d6264dd11c7e3b0e0f2bab2dbc015a19886c/verify_by_change.py>
- Tests: <https://raw.githubusercontent.com/manuelsampedro1/verify-by-change/1d38d6264dd11c7e3b0e0f2bab2dbc015a19886c/tests/test_verify_by_change.py>

## Takeaway

Agent verification should match the real session shape. A base-ref diff is useful for PR review, but local follow-ups still need to be visible before the agent closes with confidence.
