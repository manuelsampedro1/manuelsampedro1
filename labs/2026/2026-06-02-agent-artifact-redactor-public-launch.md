# 2026-06-02 - Agent Artifact Redactor Public Launch

## Source

- Public repo: https://github.com/manuelsampedro1/agent-artifact-redactor
- Published HEAD: `53412e48e97e1a6301abaee5907832cc547eef0e`
- CI run: https://github.com/manuelsampedro1/agent-artifact-redactor/actions/runs/26835477835

## What Changed

Built and published `agent-artifact-redactor`, a dependency-free Python CLI for
redacting local text artifacts before they are committed, shared, or copied into
an agent handoff.

The tool reports and can replace:

- authorization bearer headers,
- secret-looking assignments such as `API_KEY=...` or `token=...`,
- JWT-like tokens,
- email addresses,
- phone-like values,
- absolute local paths,
- SSH key path references,
- private-key block markers.

It emits Markdown for human review, JSON for automation, optional redacted
copies via `--write-dir`, score gates via `--min-score`, and severity gates via
`--fail-on`.

## Why It Matters

Public proof is only credible if it is safe to publish. Agent workflows produce
useful artifacts, but logs, transcripts, proof packets, run ledgers, and CI
failure notes can accidentally carry sensitive content.

`agent-artifact-redactor` fills the gap between secret scanning diffs and
publishing human-readable evidence. It does not upload artifact content, call a
model, or claim to be full DLP. It makes common publication risks visible before
evidence becomes public.

## Verification

Ran locally:

```sh
make test
make lint
make build
make smoke
git diff --check
```

Additional checks:

- editable install in a temporary virtualenv after upgrading `pip`, `setuptools`, and `wheel`,
- installed CLI smoke run against `examples/raw-artifact.txt`,
- `agent-instruction-audit AGENTS.md --min-score 80` at `100/100`,
- `repo-flightcheck . --check-remote --strict --threshold 80` at `100/100`,
- public raw README/source/test/example URLs returned `200`,
- GitHub Actions run `26835477835` completed with `success`.

## Takeaway

Treat public evidence as a separate surface from the code diff. Before a proof
packet, transcript, command log, or lab note is published, redact it locally and
review the sanitized copy instead of assuming the source artifact is safe.
