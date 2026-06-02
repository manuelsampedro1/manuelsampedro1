# 2026-06-02 - Verify by Change Empty Diff Guard

## Context

`verify-by-change` already detected staged, unstaged, and untracked files and mapped changed paths to verification checks. The weak case was an empty change set. A blank checklist can look like a rendering issue, a bad base ref, or a skipped scan, especially in CI.

## Change

- Added an explicit Markdown message when no changed files are detected.
- Added `--fail-on-empty` so automation can exit with code `2` when it expected files.
- Kept the default non-failing for local use.
- Kept JSON output stable: an empty change set emits `{}`.
- Added tests for empty Markdown output, empty JSON output, and `--fail-on-empty` against a clean Git repo.
- Updated README verification and `DECISIONS.md`.

Public commit: `8fbb14ef523e feat: flag empty verification inputs`.

## Verification

Local checks:

```sh
python3 -m py_compile verify_by_change.py
python3 -m unittest discover -s tests
python3 verify_by_change.py verify_by_change.py README.md >/tmp/verify-output.txt
python3 verify_by_change.py --repo . --staged --json --output /tmp/verify-staged.json
test -s /tmp/verify-output.txt
test -s /tmp/verify-staged.json
git diff --check
```

Clean-repo empty check:

```sh
tmp=$(mktemp -d)
git -C "$tmp" init -q
git -C "$tmp" config user.name 'Test User'
git -C "$tmp" config user.email test@example.com
printf 'initial\n' > "$tmp/README.md"
git -C "$tmp" add README.md
git -C "$tmp" commit -q -m initial
python3 verify_by_change.py --repo "$tmp" --fail-on-empty >/tmp/verify-empty-check.txt
```

Results:

- Python compile passed.
- `python3 -m unittest discover -s tests`: 9 tests passed.
- Explicit-path and staged JSON checklists were generated and non-empty.
- `--fail-on-empty` returned exit code `2` for a clean repo and wrote the empty-change message.
- Public commit page and raw changed files returned `200`.
- GitHub Actions run `26793152799` completed with conclusion `success`.

## Source Linkage

- Repo: <https://github.com/manuelsampedro1/verify-by-change>
- Commit: <https://github.com/manuelsampedro1/verify-by-change/commit/8fbb14ef523e7973dc9ca96d8876fe6e0c2dbe2c>
- CI run: <https://github.com/manuelsampedro1/verify-by-change/actions/runs/26793152799>
- CLI: <https://raw.githubusercontent.com/manuelsampedro1/verify-by-change/8fbb14e/verify_by_change.py>
- Tests: <https://raw.githubusercontent.com/manuelsampedro1/verify-by-change/8fbb14e/tests/test_verify_by_change.py>

## Takeaway

Verification tooling should make empty evidence explicit. A clean “no changed files detected” result is fine for local inspection, but CI should be able to fail when a diff was expected and no verification target exists.
