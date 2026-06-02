# Brief Readiness Before Codex

Use this when a product or automation turns messy kickoff notes into a prompt for a coding agent.

## Goal

Make missing essentials visible before the prompt is copied into Codex, without pretending a simple form can score overall project quality.

## Source Event

This recipe came from `briefboard-local` commit `3346373fdfd0`, which added missing-field readiness checks to the shared formatter and generated Codex prompt.

Relevant files:

- `brief-format.js`
- `tests/brief-format.test.cjs`
- `README.md`
- `DECISIONS.md`

## Workflow

1. Define the smallest set of essential fields for the handoff.
2. Normalize draft input before checking readiness.
3. Return a boolean readiness value and the exact missing field labels.
4. Render missing fields inside the human brief.
5. Include the same missing-field context in the Codex prompt.
6. Avoid numeric scores unless they are backed by a real rubric.
7. Test both complete and incomplete drafts through the shared formatter.
8. Add CI for the formatter tests once the behavior affects public handoffs.

## Checklist

- Can the prompt show what is missing before asking Codex to implement?
- Are missing fields named in product language, not internal key names?
- Does the check live in a shared module instead of only browser UI code?
- Can a complete draft and an incomplete draft both be tested with `node --test`?
- Is the readiness signal descriptive rather than a fake confidence score?

## Verification

For a browser-only handoff tool:

```sh
node --test
git diff --check
```

Then verify public evidence if the change is promoted:

```sh
curl -L --max-time 15 -s -o /dev/null -w '%{http_code}' https://github.com/<owner>/<repo>/commit/<sha>
curl -L --max-time 15 -s -o /dev/null -w '%{http_code}' https://raw.githubusercontent.com/<owner>/<repo>/<sha>/<changed-file>
```

## Failure Modes

- Making a formatted prompt look ready while core problem details are still blank.
- Hiding readiness only in UI state that exported prompts do not include.
- Using a score that cannot explain what the user should fix next.
- Letting browser-only code define behavior that tests cannot cover.
- Promoting the change without CI or a reproducible local test command.

## Source Linkage

- Public repo: <https://github.com/manuelsampedro1/briefboard-local>
- Behavior commit: <https://github.com/manuelsampedro1/briefboard-local/commit/3346373fdfd0a2e104f564fd870567edd353105e>
- CI run: <https://github.com/manuelsampedro1/briefboard-local/actions/runs/26794326305>
