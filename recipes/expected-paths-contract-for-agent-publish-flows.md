# Expected Paths Contract for Agent Publish Flows

Use this when a Codex, Claude Code, or scheduled repo automation calls a publish script that blocks unless the run declares the exact artifact paths it is allowed to ship.

## Use When

- The publish entrypoint accepts artifact paths after the commit message.
- A preflight checks dirty public paths before staging broad directories such as `labs/`, `recipes/`, or `docs/`.
- The run should publish one concrete artifact plus generated surfaces, not "whatever changed in public folders."
- You need the caller contract, not only the guard inside the publish script.

## Goal

Make every artifact-producing automation pass the exact pre-existing file paths created for that run, and nothing broader.

In this repo, [`../scripts/commit_daily_update.sh`](../scripts/commit_daily_update.sh) now treats paths after the commit message as `expected_paths`. If a new recipe file already exists in `recipes/` before the script starts, the caller must pass that exact file path or the run is blocked.

Generated files such as `README.md`, `recipes/README.md`, or `labs/README.md` do not belong in that argument list when the publish script regenerates them later in the run.

## Decision Rule

Pass only files that already exist as intentional artifacts before the publish entrypoint begins.

Good examples:

- `recipes/expected-paths-contract-for-agent-publish-flows.md`
- `labs/2026/2026-06-01-expected-paths-contract-for-agent-publish-runs.md`
- `docs/automation-runbook.md` when that file is the substantive artifact you edited before publish

Bad examples:

- `recipes`
- `labs`
- `README.md`
- `recipes/README.md`

If you need to allow a directory, the publish contract is too loose for an agent-run flow.

## Workflow

1. Read the real publish entrypoint and confirm when its dirty-path preflight runs.
2. Identify the one substantive artifact this run creates or edits before publish.
3. Capture that artifact path explicitly in the caller:
   - from a note-generator script output,
   - from a fixed recipe path,
   - or from a deterministic artifact naming rule.
4. Call the publish script with:
   - a concise commit message,
   - the exact artifact path or paths after the message.
5. Do not pass generated indexes or root surface files if the publish script creates them after preflight.
6. Verify the failure path:
   - omit the artifact path once,
   - confirm the script blocks and prints the unexpected path.
7. Verify the success path:
   - rerun with the exact artifact path,
   - inspect the final commit to confirm the artifact and generated surfaces were included.

## Caller Pattern

If a helper script creates the artifact, make it return or print the real path and forward it into publish:

```bash
note_path="$(scripts/new_daily_lab_note.sh "Expected paths contract for agent publish runs" | tail -n 1)"

scripts/commit_daily_update.sh \
  "recipe: add expected paths contract" \
  "$note_path"
```

If the artifact path is fixed, pass it directly:

```bash
scripts/commit_daily_update.sh \
  "recipe: add expected paths contract" \
  recipes/expected-paths-contract-for-agent-publish-flows.md
```

The important contract is not how the path is discovered. It is that the caller names the exact artifact file before broad staging begins.

## Agent Prompt Pattern

```text
Wire this automation to a publish flow that requires exact expected paths.

Inputs:
- publish entrypoint: <script path>
- artifact created by this run: <exact path or deterministic rule>
- generated surfaces updated later: <paths>

Tasks:
1. Read the publish entrypoint and find when it checks dirty public paths.
2. Make the caller pass only the exact artifact file paths that already exist before publish.
3. Do not pass generated indexes or root README files unless the preflight expects them to pre-exist.
4. Verify one failure run without the artifact path.
5. Verify one success run with the exact artifact path.
6. Report:
   - the artifact path contract,
   - the exact invocation,
   - what generated files are intentionally excluded from the argument list,
   - what final files landed in the successful commit.

Rules:
- Do not pass whole directories as expected paths.
- Do not weaken the publish guard to avoid updating callers.
- Do not claim the contract works without checking the final commit contents.
```

## Fast Checklist

- Does the caller pass exact file paths instead of directories?
- Are those paths real artifacts that already exist before publish starts?
- Are generated files intentionally excluded because they appear only after preflight?
- Did the missing-path run fail with the artifact path named in the error?
- Did the success run commit the artifact plus generated surfaces only?

## Evaluation Pattern

Score each item `0` or `1`:

- The caller names exact artifact files, not directories.
- Generated surfaces are excluded from `expected_paths` for the right reason.
- Missing-path verification failed before staging.
- Success-path verification produced the intended commit.
- The contract is documented where another builder can copy it.

`5`: ship the caller update or recipe.
`4`: ship if the remaining gap is only missing documentation.
`0-3`: do not trust the publish flow yet.

## Failure Modes

- Passing `recipes/` or `labs/` because it feels more convenient.
- Adding `README.md` or `recipes/README.md` to `expected_paths` even though the script generates them later.
- Hardcoding the wrong dated artifact path in an automation wrapper.
- Testing only the success path and never proving the guard still blocks missing paths.
- Relaxing the preflight because one caller was not updated after the contract changed.

## Source Linkage

- Repo / tool / workflow: this profile repo's daily publish automation.
- Supporting prompt, script, or note: [`../labs/2026/2026-06-01-expected-paths-contract-for-agent-publish-runs.md`](../labs/2026/2026-06-01-expected-paths-contract-for-agent-publish-runs.md), [`../scripts/commit_daily_update.sh`](../scripts/commit_daily_update.sh), and [`./dirty-public-path-preflight.md`](./dirty-public-path-preflight.md).
