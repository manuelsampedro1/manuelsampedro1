# Agent Artifact Redactor

Use this before logs, transcripts, proof packets, or command artifacts are
published or copied into a public handoff.

## Source

- Public tool: https://github.com/manuelsampedro1/agent-artifact-redactor
- Launch note: [2026-06-02 - Agent Artifact Redactor Public Launch](../labs/2026/2026-06-02-agent-artifact-redactor-public-launch.md)

## Pattern

1. Save the artifact to a local text file:

```sh
agent-artifact-redactor /tmp/proof-packet.md --fail-on high
```

2. Write a sanitized copy for publication:

```sh
agent-artifact-redactor /tmp/proof-packet.md --write-dir /tmp/redacted --min-score 80
```

3. When the redacted artifact will be referenced later, write a hash manifest:

```sh
agent-artifact-redactor /tmp/proof-packet.md \
  --write-dir /tmp/redacted \
  --manifest /tmp/redacted/manifest.json \
  --min-score 80
```

4. For automation, emit JSON and fail on high-severity findings:

```sh
agent-artifact-redactor /tmp/proof-packet.md --format json --fail-on high
```

5. Publish or attach only the redacted copy and manifest, then preserve the
original locally if a reviewer needs deeper evidence.

## What Good Looks Like

- Public proof packets do not include bearer headers, secret assignments,
  JWT-like strings, emails, phone-like values, local paths, or SSH key paths.
- Findings include line numbers and redacted evidence, not raw sensitive values.
- Manifests include source and redacted SHA-256 values so the redaction step is
  reviewable without publishing the source artifact.
- Automation fails before risky artifacts are committed or copied into profile
  notes.
- The original artifact stays local unless a reviewer explicitly needs it.

## Prompt Pattern

```text
Prepare this agent artifact for public sharing.

Rules:
- Run agent-artifact-redactor before publishing.
- Use the redacted copy, not the original artifact.
- Generate a manifest when the redacted artifact will be cited as evidence.
- Do not claim the artifact is fully safe; say which configured risks were checked.
- If high or critical findings appear, stop publication and rotate any real secret.

<agent-artifact-redactor output>
<candidate artifact summary>
```

## Pair With

- `agent-secret-sentinel` before committing agent-generated diffs,
- `agent-proof-packet` when building review evidence,
- `agent-run-ledger` when storing durable run history,
- `agent-claim-check` before reusing closeout claims publicly,
- `redacted-artifact-manifests` when attaching public proof,
- `profile-proof-audit` before treating profile claims as ready.

## Failure Mode

Do not treat diff secret scanning as proof that copied logs or proof packets are
safe. Artifacts can leak sensitive content outside the changed files.
