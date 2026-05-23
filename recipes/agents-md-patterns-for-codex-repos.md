# AGENTS.md Patterns for Codex Repos

## Use When

Use this when a repo needs clearer instructions for Codex without collapsing into a giant process manual.

## Source Linkage

- Repo / tool / workflow: this profile repo and the way its `AGENTS.md` pushes toward proof, verification, and no-filler output.
- Supporting prompt, script, or note: [`docs/automation-runbook.md`](../docs/automation-runbook.md), [`docs/profile-strategy.md`](../docs/profile-strategy.md), and [`TODO.md`](../TODO.md).

## Steps

1. Start with the repo's actual constraints: platform, product style, build bar, auth limits, and closure rules.
2. Add only the instructions that materially change behavior in that repo.
3. Separate permanent rules from temporary project backlog.
4. Prefer operational rules such as "read the repo first" or "report failed verification" over style fluff.
5. Add one closure rule so the agent has to leave the repo more understandable than it found it.

## Checks

- Would these instructions change the next real Codex run?
- Are the rules short enough to stay maintained?
- Do they reduce avoidable mistakes rather than describe ideals?
- Is anything here really TODO/backlog material instead of a stable repo rule?

## Example

A good `AGENTS.md` pattern is:

1. repo contract,
2. role and principles,
3. product/platform rules,
4. workflow and verification bar,
5. closeout expectations.

That structure is strong enough to change behavior without turning the file into internal lore.
