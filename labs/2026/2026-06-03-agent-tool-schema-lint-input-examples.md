# 2026-06-03 - Agent Tool Schema Lint Input Examples

## What Changed

Added input-example validation to
[`agent-tool-schema-lint`](https://github.com/manuelsampedro1/agent-tool-schema-lint).

The CLI now recognizes `input_examples`, `inputExamples`, or `examples` on a
tool definition or inside a function-style `function` object. It reports how
many examples each tool carries and checks that examples are realistic enough
to guide an agent instead of drifting away from the declared schema.

## Why It Matters

Good tool descriptions and schemas reduce guessing, but examples catch another
failure mode: arguments that look plausible to a model while violating the
actual interface.

This change checks for:

- missing input examples;
- non-object or empty example arrays;
- examples that omit required fields;
- examples that add fields blocked by `additionalProperties: false`;
- examples that use wrong primitive JSON types;
- examples that use values outside declared enums.

## Verification Evidence

- Added example extraction for MCP-like and function-style tool definitions.
- Added schema-aligned validation for required fields, closed-schema extras,
  simple JSON types, and enum values.
- Added `example_count` to JSON and Markdown summaries.
- Updated the good fixture with realistic examples for both supported shapes.
- Added regression tests for missing examples, missing required fields, extra
  properties, type mismatches, enum mismatches, JSON output, and Markdown
  summaries.
- Verified the public repo with tests, lint, build, smoke, whitespace checks,
  local Git identity audit, raw GitHub source URLs, `repo-flightcheck` at
  `100/100`, and GitHub Actions success for commit `bb2399b`.

## Reusable Lesson

Treat tool examples as part of the agent interface. They should compile
against the same schema reviewers expect the agent to call, otherwise examples
become another source of silent tool-use drift.
