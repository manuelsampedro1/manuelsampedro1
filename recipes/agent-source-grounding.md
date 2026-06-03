# Agent Source Grounding

Use this pattern when an agent produces Markdown or JSON that will become a public note, decision, review packet, closeout, profile claim, or reusable proof artifact.

## Grounding Contract

Require each artifact to expose:

- source or evidence sections for Markdown notes,
- claim rows with non-empty evidence or sources,
- JSON `claims` entries with `sources`, `evidence`, `references`, `links`, or `urls`,
- no placeholder citation language such as `TBD` or `citation needed`,
- concrete pointers when claims will become durable public proof,
- optional HTTP checks when external links are part of the evidence.

## CLI Pattern

```sh
agent-source-grounding check note.md --require-sources
agent-source-grounding check claims.json --format json
agent-source-grounding check proof.md --require-sources --require-concrete
agent-source-grounding check docs/*.md --require-sources --check-http
```

## Review Rule

Do not reuse an agent-written claim as evidence until a reviewer can inspect the source.

Check:

- Does the artifact have a source or evidence section?
- Does each claim row point to a file, command, link, or explicit evidence item?
- Does important evidence use `--require-concrete` so vague source-shaped prose
  cannot pass as proof?
- Are any sources still placeholders?
- Do research-style phrases have nearby grounding?
- Do important external links resolve when HTTP checking is enabled?

## Public Example

The implementation lives in [`agent-source-grounding`](https://github.com/manuelsampedro1/agent-source-grounding), with grounded and ungrounded Markdown/JSON fixtures under `examples/`.
