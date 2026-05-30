# Dirty Public Path Preflight for Agent Publish Flows

Use this when a Codex, Claude Code, or scheduled publish script stages whole public directories such as `labs/`, `recipes/`, or `docs/`.

## Use When

- The publish entrypoint uses broad staging such as `git add labs recipes docs`.
- Agents often resume from a dirty worktree instead of a fresh clone.
- One run is supposed to publish one narrow artifact, not sweep unrelated draft edits along with it.
- You need a guard before `git add` or `git commit`, not just a prettier commit message.

## Goal

Detect pre-existing edits that already exist inside staged public paths before the publish run bundles them into today's commit.

In this repo, the risk comes from [`../scripts/commit_daily_update.sh`](../scripts/commit_daily_update.sh), which stages:

- `README.md`
- `DECISIONS.md`
- `TODO.md`
- `docs`
- `labs`
- `recipes`
- `radar`
- `templates`
- `scripts`
- `.gitignore`

That allowlist is safer than `git add .`, but it still stages every change already sitting in those paths.

## Decision Rule

Prefer `block` by default.

Use `warn` only if the workflow intentionally bundles multiple public artifacts in one publish run and the operator can still inspect the path list before commit.

Good default:

- block on pre-existing edits inside staged public paths,
- allow untracked scratch files outside those paths,
- print the exact conflicting paths and stop before staging.

## Workflow

1. Read the real publish entrypoint, not only helper scripts.
2. List the paths the script stages broadly.
3. Define the small expected file set for this run:
   - the new artifact path,
   - generated index files,
   - any root surface file the run intentionally refreshes.
4. Before `git add`, collect pre-existing changes inside the staged public paths.
5. Remove the expected file set from that list.
6. If anything remains, block or warn with exact paths.
7. Verify the clean path:
   - one real artifact,
   - expected generated files only,
   - successful commit.
8. Verify the dirty path:
   - add one unrelated tracked edit inside a staged public directory,
   - rerun the publish script,
   - confirm the guard stops before commit.

## Bash Pattern

Add a preflight like this before the broad `git add` step:

```bash
public_paths=(README.md DECISIONS.md TODO.md docs labs recipes radar templates scripts .gitignore)
expected_paths=("$artifact_path" README.md recipes/README.md)

mapfile -t dirty_public_paths < <(
  git status --porcelain -- "${public_paths[@]}" |
    awk '{print substr($0,4)}'
)

unexpected_paths=()
for path in "${dirty_public_paths[@]}"; do
  skip=false
  for expected in "${expected_paths[@]}"; do
    if [ "$path" = "$expected" ]; then
      skip=true
      break
    fi
  done
  if [ "$skip" = false ]; then
    unexpected_paths+=("$path")
  fi
done

if [ "${#unexpected_paths[@]}" -gt 0 ]; then
  echo "Publish blocked: pre-existing tracked changes found in staged public paths:"
  printf '  %s\n' "${unexpected_paths[@]}"
  echo "Commit or move those edits before running the publish flow."
  exit 1
fi
```

Adjust `expected_paths` to the real artifact and generator outputs for your repo. If the publish flow can update `labs/README.md` or `radar/README.md`, name them explicitly instead of allowing their whole directories.

## Agent Prompt Pattern

```text
Add a dirty-public-path preflight to this publish flow.

Inputs:
- publish entrypoint: <script path>
- broad staged paths: <paths>
- expected artifact for this run: <path>
- expected generated files: <paths>

Tasks:
1. Find whether the publish script stages whole public directories.
2. Before staging, detect tracked edits already present inside those staged paths.
3. Ignore only the exact file set expected for this run.
4. Block by default and print the unexpected paths.
5. Verify:
   - a clean run with one real artifact succeeds,
   - a dirty run with one unrelated tracked edit stops before commit.
6. Report:
   - the preflight logic,
   - the exact verification commands,
   - what still remains intentionally unguarded.

Rules:
- Do not replace the allowlist with `git add .`.
- Do not rely on commit-message discipline as the guard.
- Do not claim success from stdout alone; inspect `git show --stat` or `git status --short`.
```

## Fast Checklist

- Does the guard run before `git add`?
- Does it look only inside the staged public paths?
- Are expected generated files named exactly, not by directory wildcard?
- Did you test one unrelated tracked edit inside `recipes/` or `labs/`?
- Did the clean path still publish the intended artifact?

## Evaluation Pattern

Score each item `0` or `1`:

- Broad staging risk was confirmed in the real entrypoint.
- Preflight filters against an explicit expected file set.
- Dirty pre-existing edits block or warn before staging.
- Clean publish path still succeeds.
- Verification checked final Git state, not just shell output.

`5`: publish the recipe or ship the guard.
`4`: publish if the remaining gap is documented and minor.
`0-3`: do not call the publish flow safe yet.

## Failure Modes

- Checking only untracked scratch files and missing tracked draft edits.
- Allowing an entire directory such as `recipes/` as "expected."
- Running the guard after generated files are already staged.
- Testing only on a clean worktree and assuming the dirty case is covered.
- Using `warn` in a fully automated scheduled publish flow with no human review step.

## Source Linkage

- Repo / tool / workflow: this profile repo's daily publish automation.
- Supporting prompt, script, or note: [`../labs/2026/2026-05-30-whole-directory-staging-in-agent-publish-scripts.md`](../labs/2026/2026-05-30-whole-directory-staging-in-agent-publish-scripts.md), [`../scripts/commit_daily_update.sh`](../scripts/commit_daily_update.sh), and [`./fail-fast-git-identity-for-agent-publish-flows.md`](./fail-fast-git-identity-for-agent-publish-flows.md).
