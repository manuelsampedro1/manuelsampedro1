# Approval-Backed Tool Call Audits

Use this pattern when a coding-agent run includes tool calls that can send,
delete, deploy, publish, install, charge, modify credentials, or push public
state.

## Problem

A transcript can contain a sensitive action and still end with a confident
closeout. Without an approval gate, the reviewer has to infer whether that
action had human authorization, a permission receipt, or some other explicit
authority marker.

## Pattern

Audit the tool-call log in approval-required mode:

```sh
agent-tool-call-audit /tmp/tool-calls.jsonl \
  --require-approval \
  --fail-on high \
  --format json \
  > /tmp/tool-call-audit.json
```

Treat `missing-approval-evidence` as a blocker. Add or attach the approval
evidence before accepting the run history as clean enough for a proof packet,
run ledger, or closeout.

Recognized evidence can be explicit fields or text such as:

- `approval_receipt`;
- `permission_receipt`;
- `authorization_receipt`;
- `approved_by`;
- `authorized_by`;
- `human_approved: true`;
- `approved: true`.

## Acceptance Criteria

- The audit is run with `--require-approval`.
- Sensitive tool names remain visible as findings.
- External action commands such as `git push`, package publishing, release
  creation, or deploy commands require approval evidence.
- JSON output shows `approval_required_calls` and `approval_evidence_calls`.
- Runs with missing approval evidence fail when `--fail-on high` is used.
- A receipt-backed sensitive action can proceed to normal review instead of
  being treated as unauthorized.

## Review Rule

Approval evidence does not make an action safe by itself. It proves the action
had an authority marker in the run history; reviewers still inspect the action,
scope, command, and output.
