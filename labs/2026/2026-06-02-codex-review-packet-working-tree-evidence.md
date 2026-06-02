# 2026-06-02 - Codex Review Packet Working Tree Evidence

## Context

`codex-review-packet` is in the profile's selected work because it packages repo context and diffs for stricter AI review. The first public version listed staged, unstaged, and untracked files in working-tree mode, but the diff body only used `git diff`, so staged and untracked evidence could be missing from the packet.

## Change

- Working-tree packets now include staged diff, unstaged diff, and text previews for untracked files.
- Staged-only mode remains index-only.
- Added `--untracked-lines` to keep new-file previews bounded.
- Added tests for rename parsing, working-tree packets, staged-only packets, untracked preview limits, and CLI output.
- Added GitHub Actions CI for tests and Python compilation.

Public commit: `775fa9afab7e feat: include full working tree evidence`.

## Verification

Local checks:

```sh
python3 -m py_compile codex_review_packet.py
python3 -m unittest discover -s tests
python3 codex_review_packet.py --repo . --output /tmp/codex-review-packet.md
test -s /tmp/codex-review-packet.md
python3 codex_review_packet.py --repo . --staged >/tmp/codex-review-packet-staged.md
test -s /tmp/codex-review-packet-staged.md
git diff --check
```

Generated packet smoke check:

```sh
grep -n "tests/test_codex_review_packet.py\|.github/workflows/ci.yml\|new file mode" /tmp/codex-review-packet.md
```

Public checks:

- Raw tests returned `200`.
- Raw CI workflow returned `200`.
- GitHub Actions run `26791855282` for commit `775fa9afab7ef9ed335a4db1a8b31af863e570be` completed with conclusion `success`.

## Source Linkage

- Repo: <https://github.com/manuelsampedro1/codex-review-packet>
- Commit: <https://github.com/manuelsampedro1/codex-review-packet/commit/775fa9afab7ef9ed335a4db1a8b31af863e570be>
- CI run: <https://github.com/manuelsampedro1/codex-review-packet/actions/runs/26791855282>
- Tests: <https://raw.githubusercontent.com/manuelsampedro1/codex-review-packet/775fa9a/tests/test_codex_review_packet.py>

## Takeaway

A review packet should not only name changed files; it should include enough evidence for the reviewer to inspect the same surface. If a tool lists untracked files but shows no content, the packet can still produce generic review output.
