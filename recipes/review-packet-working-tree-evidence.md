# Review Packet Working Tree Evidence

Use this when a coding-agent review packet is generated from a dirty working tree.

## Goal

Make the packet match the real review surface: staged changes, unstaged changes, and newly created files. A reviewer should not have to discover missing evidence after the packet is generated.

## Source Event

This recipe came from `codex-review-packet` commit `775fa9afab7e`, which changed working-tree packet generation from a narrow `git diff` body to staged diff plus unstaged diff plus bounded untracked file previews.

Relevant files:

- `codex_review_packet.py`
- `tests/test_codex_review_packet.py`
- `.github/workflows/ci.yml`

## Workflow

1. Use `git status --porcelain --untracked-files=all` to define the changed-file surface.
2. Include `git diff --cached` for staged content.
3. Include `git diff` for unstaged tracked-file content.
4. Add bounded previews for untracked text files.
5. Keep a staged-only mode for reviewers who intentionally want the index.
6. Add tests with a temp Git repo that has one staged file, one unstaged edit, and one untracked file.
7. Check the generated packet for `new file mode` entries so untracked files are not only listed.

## Checklist

- Does the packet list staged files and include their diff?
- Does it list unstaged files and include their diff?
- Does it list untracked files and include bounded content?
- Does staged-only mode exclude unstaged and untracked content?
- Is there a line limit for untracked previews?
- Does CI run the same tests locally documented in README?

## Verification

Use these checks for a standard-library Python implementation:

```sh
python3 -m py_compile codex_review_packet.py
python3 -m unittest discover -s tests
python3 codex_review_packet.py --repo . --output /tmp/codex-review-packet.md
test -s /tmp/codex-review-packet.md
grep -n "new file mode" /tmp/codex-review-packet.md
```

The source change also has a public successful CI run.

## Failure Modes

- Listing untracked files under "Changed Files" but omitting their content from the diff.
- Using only `git diff` and missing staged changes.
- Letting untracked previews dump large files without a line limit.
- Treating staged-only mode and working-tree mode as the same review target.

## Source Linkage

- Public repo: <https://github.com/manuelsampedro1/codex-review-packet>
- Commit: <https://github.com/manuelsampedro1/codex-review-packet/commit/775fa9afab7ef9ed335a4db1a8b31af863e570be>
- CI run: <https://github.com/manuelsampedro1/codex-review-packet/actions/runs/26791855282>
