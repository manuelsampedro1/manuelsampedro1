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
    "python audit tools",
    "python unit tests",
    "commit-script shell fixture",
    "profile quality audit",
]

MAX_SELECTED_WORK_ROWS = 50
SELECTED_WORK_SATURATION_BASELINE_ROWS = 46
SELECTED_WORK_GROWTH_DECISION_TITLE = "Allow Selected Work Growth After Saturation"
MAX_REVIEWER_PATH_BULLETS = 4
OWNED_GITHUB_REPO_PREFIX = "https://github.com/manuelsampedro1/"
LATEST_PROOF_INDEXES = {
    "./labs/": "labs/README.md",
    "./recipes/": "recipes/README.md",
    "./radar/": "radar/README.md",
}


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


def has_decision_title(markdown: str, title: str) -> bool:
    pattern = rf"^##\s+\d{{4}}-\d{{2}}-\d{{2}}\s+-\s+{re.escape(title)}\s*$"
    return re.search(pattern, markdown, re.MULTILINE) is not None


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


def repo_table_entries(markdown: str, section: str) -> list[tuple[str, str]]:
    body = section_body(markdown, section)
    entries: list[tuple[str, str]] = []
    for line in body.splitlines():
        stripped = line.strip()
        if not stripped.startswith("|"):
            continue
        if "---" in stripped or "Repo |" in stripped:
            continue
        match = re.search(r"\[([^\]]+)\]\(([^)]+)\)", stripped)
        if match:
            entries.append((match.group(1).strip(), match.group(2).rstrip("/")))
    return entries


def selected_work_repo_entries(markdown: str) -> list[tuple[str, str]]:
    return repo_table_entries(markdown, "Selected Work")


def selected_work_repo_targets(markdown: str) -> list[str]:
    return [target for _, target in selected_work_repo_entries(markdown)]


def github_repo_slug(target: str) -> str:
    if not target.startswith(OWNED_GITHUB_REPO_PREFIX):
        return ""
    return target.removeprefix(OWNED_GITHUB_REPO_PREFIX).split("/", 1)[0]


def duplicated_values(values: list[str]) -> list[str]:
    seen: set[str] = set()
    duplicates: list[str] = []
    for value in values:
        if value in seen and value not in duplicates:
            duplicates.append(value)
        seen.add(value)
    return duplicates


def count_markdown_bullets(markdown: str) -> int:
    return sum(1 for line in markdown.splitlines() if line.lstrip().startswith("- "))


def markdown_links(markdown: str) -> list[tuple[str, str]]:
    return [(match.group(1).strip(), match.group(2).strip()) for match in re.finditer(r"\[([^\]]+)\]\(([^)]+)\)", markdown)]


def audit_repo_table(section: str, entries: list[tuple[str, str]], issues: list[str]) -> None:
    targets = [target for _, target in entries]
    for target in duplicated_values(targets):
        issues.append(f"{section} contains duplicate repo target: {target}.")
    for label, target in entries:
        if not target.startswith(OWNED_GITHUB_REPO_PREFIX):
            issues.append(f"{section} target is not an owned GitHub repo: {target}.")
            continue
        slug = github_repo_slug(target)
        if label != slug:
            issues.append(f"{section} label `{label}` does not match repo target `{slug}`.")


def audit_latest_proof_indexes(root: Path, readme: str, issues: list[str]) -> None:
    latest_proof = section_body(readme, "Latest Proof")
    index_text = {
        prefix: read_text(root / index_path)
        for prefix, index_path in LATEST_PROOF_INDEXES.items()
    }
    for _, target in markdown_links(latest_proof):
        normalized_target = target.split("#", 1)[0].rstrip("/")
        for prefix, index_path in LATEST_PROOF_INDEXES.items():
            if not normalized_target.startswith(prefix):
                continue
            relative_path = normalized_target.removeprefix("./")
            if not (root / relative_path).exists():
                issues.append(f"Latest Proof target is missing: {target}.")
            if Path(relative_path).name not in index_text[prefix]:
                issues.append(f"Latest Proof target is not indexed in {index_path}: {target}.")
            break


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

    for first, second in zip(REQUIRED_README_SECTIONS, REQUIRED_README_SECTIONS[1:]):
        if first in order and second in order and order[first] > order[second]:
            issues.append(f"README section order is wrong: {first} must appear before {second}.")

    reviewer_path = section_body(readme, "Reviewer Path")
    for target in REVIEWER_PATH_TARGETS:
        if target not in reviewer_path:
            issues.append(f"Reviewer Path is missing target: {target}.")
    allowed_reviewer_targets = set(REVIEWER_PATH_TARGETS)
    for _, target in markdown_links(reviewer_path):
        normalized_target = target.rstrip("/")
        if normalized_target not in allowed_reviewer_targets:
            issues.append(f"Reviewer Path contains unapproved target: {target}.")
    reviewer_path_bullets = count_markdown_bullets(reviewer_path)
    if reviewer_path_bullets > MAX_REVIEWER_PATH_BULLETS:
        issues.append(
            "Reviewer Path has "
            f"{reviewer_path_bullets} bullets; keep it at {MAX_REVIEWER_PATH_BULLETS} or fewer for first-read clarity."
        )

    verify_section = section_body(readme, "Verify This Repo").lower()
    for phrase in VERIFY_SECTION_REQUIRED_PHRASES:
        if phrase not in verify_section:
            issues.append(f"Verify This Repo is missing verification detail: {phrase}.")
    audit_latest_proof_indexes(root, readme, issues)

    selected_rows = count_selected_work_rows(readme)
    selected_entries = selected_work_repo_entries(readme)
    safety_entries = repo_table_entries(readme, "Agent Safety Layer")
    audit_repo_table("Selected Work", selected_entries, issues)
    audit_repo_table("Agent Safety Layer", safety_entries, issues)
    if selected_rows > MAX_SELECTED_WORK_ROWS:
        issues.append(
            f"Selected Work has {selected_rows} rows; curate before exceeding {MAX_SELECTED_WORK_ROWS} rows."
        )
    elif selected_rows > SELECTED_WORK_SATURATION_BASELINE_ROWS:
        if not has_decision_title(decisions, SELECTED_WORK_GROWTH_DECISION_TITLE):
            issues.append(
                "Selected Work has grown to "
                f"{selected_rows} rows; document an explicit post-saturation growth decision "
                f"before adding rows above {SELECTED_WORK_SATURATION_BASELINE_ROWS}."
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
