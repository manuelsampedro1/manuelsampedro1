#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import asdict, dataclass
from pathlib import Path


REQUIRED_README_SECTIONS = [
    "Current Focus",
    "Reviewer Path",
    "Selected Work",
    "Agent Safety Layer",
    "How I Work With Codex",
    "Public Workbench",
    "Verify This Repo",
    "Latest Proof",
    "Principles",
]

REVIEWER_PATH_TARGETS = [
    "https://github.com/manuelsampedro1/repo-flightcheck",
    "https://github.com/manuelsampedro1/codex-review-packet",
    "https://github.com/manuelsampedro1/verify-by-change",
    "https://github.com/manuelsampedro1/agent-run-ledger",
    "https://github.com/manuelsampedro1/agent-context-sentinel",
    "https://github.com/manuelsampedro1/agent-secret-sentinel",
    "https://github.com/manuelsampedro1/mcp-guard",
    "./examples/profile-evidence-map.md",
    "./examples/agent-release-readiness-chain.md",
    "./examples/agent-review-packet-to-ledger-chain.md",
]

REQUIRED_EXAMPLES = [
    "examples/profile-evidence-map.md",
    "examples/external-reviewer-navigation.md",
    "examples/agent-review-packet-to-ledger-chain.md",
    "examples/agent-release-readiness-chain.md",
    "examples/profile-curation-guard-proof-packet.md",
    "examples/profile-verification-proof-packet.md",
]

EVIDENCE_MAP_REPOS = [
    "repo-flightcheck",
    "codex-review-packet",
    "verify-by-change",
    "agent-run-ledger",
    "agent-context-sentinel",
    "agent-secret-sentinel",
    "mcp-guard",
    "agent-merge-readiness",
    "agent-proof-packet",
    "agent-release-note-check",
    "agent-ci-failure-packet",
    "agent-retry-guard",
    "agent-rollback-plan",
]

RISKY_README_PHRASES = [
    "guaranteed",
    "production-ready",
    "best in the world",
    "fully autonomous",
    "perfect",
    "award",
    "premio",
]

VERIFY_SECTION_REQUIRED_PHRASES = [
    "shell scripts",
    "python unit tests",
    "commit-script shell fixture",
    "profile quality audit",
]

MAX_SELECTED_WORK_ROWS = 50


@dataclass(frozen=True)
class AuditResult:
    schema_version: str
    score: int
    selected_work_rows: int
    issues: list[str]
    warnings: list[str]


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except FileNotFoundError:
        return ""


def section_order(markdown: str) -> dict[str, int]:
    order: dict[str, int] = {}
    for index, line in enumerate(markdown.splitlines()):
        match = re.match(r"^##\s+(.+?)\s*$", line)
        if match:
            order[match.group(1).strip()] = index
    return order


def section_body(markdown: str, section: str) -> str:
    pattern = re.compile(rf"^##\s+{re.escape(section)}\s*$", re.MULTILINE)
    match = pattern.search(markdown)
    if not match:
        return ""
    rest = markdown[match.end() :]
    next_match = re.search(r"^##\s+", rest, re.MULTILINE)
    if next_match:
        return rest[: next_match.start()]
    return rest


def count_selected_work_rows(markdown: str) -> int:
    body = section_body(markdown, "Selected Work")
    rows = 0
    for line in body.splitlines():
        stripped = line.strip()
        if not stripped.startswith("|"):
            continue
        if "---" in stripped or "Repo |" in stripped:
            continue
        if stripped.count("|") >= 3:
            rows += 1
    return rows


def audit(root: Path) -> AuditResult:
    readme = read_text(root / "README.md")
    decisions = read_text(root / "DECISIONS.md")
    todo = read_text(root / "TODO.md")
    evidence_map = read_text(root / "examples/profile-evidence-map.md")
    examples_index = read_text(root / "examples/README.md")
    issues: list[str] = []
    warnings: list[str] = []

    order = section_order(readme)
    for section in REQUIRED_README_SECTIONS:
        if section not in order:
            issues.append(f"README is missing required section: {section}.")

    if "Reviewer Path" in order and "Selected Work" in order and order["Reviewer Path"] > order["Selected Work"]:
        issues.append("README Reviewer Path must appear before Selected Work.")

    reviewer_path = section_body(readme, "Reviewer Path")
    for target in REVIEWER_PATH_TARGETS:
        if target not in reviewer_path:
            issues.append(f"Reviewer Path is missing target: {target}.")

    verify_section = section_body(readme, "Verify This Repo").lower()
    for phrase in VERIFY_SECTION_REQUIRED_PHRASES:
        if phrase not in verify_section:
            issues.append(f"Verify This Repo is missing verification detail: {phrase}.")

    selected_rows = count_selected_work_rows(readme)
    if selected_rows > MAX_SELECTED_WORK_ROWS:
        issues.append(
            f"Selected Work has {selected_rows} rows; curate before exceeding {MAX_SELECTED_WORK_ROWS} rows."
        )
    elif selected_rows >= 45:
        if "Pause Proof Repo Volume After Saturation" not in decisions:
            issues.append("Selected Work is saturated but DECISIONS.md lacks the curation decision.")
        if "Pause new proof-repo creation by default" not in todo:
            issues.append("Selected Work is saturated but TODO.md lacks the pause-new-repo rule.")

    lowered_readme = readme.lower()
    for phrase in RISKY_README_PHRASES:
        if phrase in lowered_readme:
            issues.append(f"README contains risky unsupported phrase: {phrase}.")

    for relative_path in REQUIRED_EXAMPLES:
        path = root / relative_path
        if not path.exists():
            issues.append(f"Missing required example: {relative_path}.")
        if f"./{Path(relative_path).name}" not in examples_index and Path(relative_path).name not in examples_index:
            issues.append(f"examples/README.md does not link {relative_path}.")

    if not evidence_map:
        issues.append("Missing profile evidence map.")
    else:
        for repo in EVIDENCE_MAP_REPOS:
            if repo not in evidence_map:
                issues.append(f"Profile evidence map is missing repo: {repo}.")
        for example in [
            "agent-release-readiness-chain.md",
            "agent-review-packet-to-ledger-chain.md",
            "external-reviewer-navigation.md",
            "profile-verification-proof-packet.md",
            "profile-curation-guard-proof-packet.md",
        ]:
            if example not in evidence_map:
                issues.append(f"Profile evidence map is missing example: {example}.")

    score = max(0, 100 - (len(issues) * 10) - (len(warnings) * 3))
    return AuditResult(
        schema_version="profile-quality-audit.v1",
        score=score,
        selected_work_rows=selected_rows,
        issues=issues,
        warnings=warnings,
    )


def render_markdown(result: AuditResult) -> str:
    lines = [
        "# Profile Quality Audit",
        "",
        f"Score: {result.score}/100",
        f"Selected Work rows: {result.selected_work_rows}",
        "",
        "## Issues",
        "",
    ]
    lines.extend(f"- {issue}" for issue in result.issues or ["none"])
    lines.extend(["", "## Warnings", ""])
    lines.extend(f"- {warning}" for warning in result.warnings or ["none"])
    return "\n".join(lines) + "\n"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Audit profile first-read quality and evidence mapping.")
    parser.add_argument("--root", default=".", help="Profile repository root.")
    parser.add_argument("--format", choices=["markdown", "json"], default="markdown")
    parser.add_argument("--min-score", type=int, default=100)
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    result = audit(Path(args.root))

    if args.format == "json":
        print(json.dumps(asdict(result), indent=2))
    else:
        print(render_markdown(result), end="")

    if result.issues or result.score < args.min_score:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
