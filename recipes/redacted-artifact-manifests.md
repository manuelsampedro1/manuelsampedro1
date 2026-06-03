# Redacted Artifact Manifests

Use this pattern when an agent proof packet, transcript, command log, or
handoff artifact needs to be shared publicly after redaction.

## Problem

Plain redaction leaves weak evidence:

- reviewers can see the sanitized file, but not what exact local artifact it
  came from;
- maintainers may accidentally publish the original instead of the redacted
  copy;
- follow-up audits have no stable hash to compare against;
- sensitive findings can be handled in prose instead of a machine-readable
  record.

## Pattern

Write the redacted copy and manifest together:

```sh
agent-artifact-redactor /tmp/proof-packet.md \
  --write-dir /tmp/redacted-proof \
  --manifest /tmp/redacted-proof/manifest.json \
  --fail-on high
```

If the command exits non-zero because high or critical findings exist, stop the
public handoff. Review the findings, rotate any real credential, and only
continue after deciding that the redacted copy is appropriate to share.

If the artifact is acceptable after review, publish or attach:

- the redacted artifact;
- the manifest;
- the exact command used to generate them.

Keep the raw source artifact local unless a reviewer explicitly needs it.

## Acceptance Criteria

- `--manifest` is used only with `--write-dir`.
- The manifest includes `agent-artifact-redactor.manifest.v1`.
- The manifest includes both source and redacted SHA-256 values.
- The published artifact path points to the redacted copy, not the source.
- The manifest does not include the raw secret-looking value that triggered
  the finding.
- High or critical findings trigger explicit review before publication.

## Review Rule

Treat the manifest as a receipt for the redaction step, not as proof that the
artifact is safe for every audience. It proves which configured redaction rules
ran and what redacted output was produced.
