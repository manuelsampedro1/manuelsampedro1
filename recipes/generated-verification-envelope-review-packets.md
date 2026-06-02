# Generated Verification Envelopes in Review Packets

Use this when a review packet should generate its own verification plan from `verify-by-change`.

## Workflow

1. Generate the packet with `--verify-by-change /path/to/verify_by_change.py` instead of preparing a separate checklist.
2. Prefer current `verify-by-change` versions that support `--json-envelope`.
3. Render the envelope inside the packet so reviewers see changed files, categories, commands, and source metadata.
4. Keep a fallback to plain Markdown for older local scripts, but treat the fallback as weaker automation evidence.
5. In the closeout, cite the packet output and the commands that proved the envelope rendered correctly.

## Checklist

- The packet includes `Envelope: verify-by-change.v1`.
- The verification source points to the repo or packet being reviewed.
- Changed files are listed before category commands.
- The rendered commands match the changed surface, not only generic language.
- Older generators fail gracefully instead of breaking the packet path.

## Failure Modes

- Embedding raw JSON in Markdown and making the reviewer parse it manually.
- Losing source metadata when a generated checklist is rendered.
- Treating a generated plain Markdown fallback as equivalent to an envelope.
- Calling `verify-by-change` without repo context and missing CLI/package-specific guidance.
- Updating the packet tool but not adding a smoke check with a real generator.

## Source

- Lab note: <../labs/2026/2026-06-02-codex-review-packet-generated-verification-envelope.md>
- Repo: https://github.com/manuelsampedro1/codex-review-packet
- Commit: https://github.com/manuelsampedro1/codex-review-packet/commit/6feb7b3c84f28a3f54b621949feb441314130475
- CI run: https://github.com/manuelsampedro1/codex-review-packet/actions/runs/26802456278
