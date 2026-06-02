#!/usr/bin/env python3
from __future__ import annotations

import argparse
import ast
import json
import os
import re
from dataclasses import asdict, dataclass
from pathlib import Path


EXPECTED_AUTOMATIONS = [
    "github-ai-lab-note",
    "github-ai-recipe",
    "github-profile-maintenance",
    "github-profile-quality-audit",
]

REQUIRED_FRAGMENTS = [
    "scripts/commit_daily_update.sh",
    "exact",
    "path",
    "after the commit message",
]


@dataclass(frozen=True)
class AutomationPromptResult:
    automation_id: str
    path: str
    issues: list[str]


@dataclass(frozen=True)
class AutomationPromptReport:
    schema_version: str
    automation_root: str
    results: list[AutomationPromptResult]

    @property
    def issues(self) -> list[str]:
        all_issues: list[str] = []
        for result in self.results:
            all_issues.extend(f"{result.automation_id}: {issue}" for issue in result.issues)
        return all_issues


def default_automation_root() -> Path:
    codex_home = os.environ.get("CODEX_HOME")
    if codex_home:
        return Path(codex_home) / "automations"
    return Path.home() / ".codex" / "automations"


def parse_toml_field(text: str, field: str) -> str:
    match = re.search(rf'^{re.escape(field)}\s*=\s*(".*")\s*$', text, re.MULTILINE)
    if not match:
        return ""
    try:
        return ast.literal_eval(match.group(1))
    except (SyntaxError, ValueError):
        return ""


def audit_automation_file(path: Path, expected_id: str) -> AutomationPromptResult:
    issues: list[str] = []
    if not path.exists():
        return AutomationPromptResult(expected_id, str(path), [f"missing {path}"])

    text = path.read_text(encoding="utf-8")
    automation_id = parse_toml_field(text, "id") or expected_id
    prompt = parse_toml_field(text, "prompt")

    if automation_id != expected_id:
        issues.append(f"expected id {expected_id!r}, found {automation_id!r}")
    if not prompt:
        issues.append("missing prompt")
    else:
        prompt_lower = prompt.lower()
        for fragment in REQUIRED_FRAGMENTS:
            if fragment not in prompt_lower:
                issues.append(f"prompt missing required fragment: {fragment}")

    return AutomationPromptResult(expected_id, str(path), issues)


def audit_root(root: Path) -> AutomationPromptReport:
    results = [
        audit_automation_file(root / automation_id / "automation.toml", automation_id)
        for automation_id in EXPECTED_AUTOMATIONS
    ]
    return AutomationPromptReport(
        schema_version="github-automation-prompt-audit.v1",
        automation_root=str(root),
        results=results,
    )


def render_markdown(report: AutomationPromptReport) -> str:
    lines = [
        "# GitHub Automation Prompt Audit",
        "",
        f"Automation root: `{report.automation_root}`",
        "",
        "## Results",
        "",
    ]
    for result in report.results:
        status = "pass" if not result.issues else "fail"
        lines.append(f"- `{result.automation_id}`: {status}")
        for issue in result.issues:
            lines.append(f"  - {issue}")
    return "\n".join(lines) + "\n"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Audit GitHub automation prompts for exact publish path contracts.")
    parser.add_argument("--automation-root", default=str(default_automation_root()))
    parser.add_argument("--format", choices=["markdown", "json"], default="markdown")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    report = audit_root(Path(args.automation_root))
    if args.format == "json":
        print(json.dumps(asdict(report), indent=2))
    else:
        print(render_markdown(report), end="")
    return 1 if report.issues else 0


if __name__ == "__main__":
    raise SystemExit(main())
