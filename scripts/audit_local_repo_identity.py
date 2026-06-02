#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import subprocess
from dataclasses import asdict, dataclass
from pathlib import Path


EXPECTED_NAME = "Manuel Sampedro"
EXPECTED_EMAIL = "202281585+manuelsampedro1@users.noreply.github.com"


@dataclass(frozen=True)
class RepoIdentityResult:
    path: str
    name: str
    email: str
    issues: list[str]


@dataclass(frozen=True)
class RepoIdentityReport:
    schema_version: str
    root: str
    expected_name: str
    expected_email: str
    results: list[RepoIdentityResult]

    @property
    def issues(self) -> list[str]:
        all_issues: list[str] = []
        for result in self.results:
            all_issues.extend(f"{result.path}: {issue}" for issue in result.issues)
        return all_issues


def git_config(repo: Path, key: str) -> str:
    result = subprocess.run(
        ["git", "-C", str(repo), "config", "--get", key],
        check=False,
        capture_output=True,
        text=True,
    )
    return result.stdout.strip()


def discover_repos(root: Path) -> list[Path]:
    repos: list[Path] = []
    if (root / ".git").exists():
        repos.append(root)
    for child in sorted(root.iterdir() if root.exists() else []):
        if child.is_dir() and (child / ".git").exists():
            repos.append(child)
    return sorted(set(repos))


def audit_repo(repo: Path, expected_name: str, expected_email: str) -> RepoIdentityResult:
    name = git_config(repo, "user.name")
    email = git_config(repo, "user.email")
    issues: list[str] = []
    if name != expected_name:
        issues.append(f"user.name is {name!r}, expected {expected_name!r}")
    if email != expected_email:
        issues.append(f"user.email is {email!r}, expected {expected_email!r}")
    return RepoIdentityResult(str(repo), name, email, issues)


def audit_root(root: Path, expected_name: str = EXPECTED_NAME, expected_email: str = EXPECTED_EMAIL) -> RepoIdentityReport:
    repos = discover_repos(root)
    results = [audit_repo(repo, expected_name, expected_email) for repo in repos]
    return RepoIdentityReport(
        schema_version="local-repo-identity-audit.v1",
        root=str(root),
        expected_name=expected_name,
        expected_email=expected_email,
        results=results,
    )


def render_markdown(report: RepoIdentityReport) -> str:
    lines = [
        "# Local Repo Identity Audit",
        "",
        f"Root: `{report.root}`",
        f"Expected name: `{report.expected_name}`",
        f"Expected email: `{report.expected_email}`",
        "",
        "## Results",
        "",
    ]
    if not report.results:
        lines.append("- no git repositories found")
    for result in report.results:
        status = "pass" if not result.issues else "fail"
        lines.append(f"- `{result.path}`: {status}")
        for issue in result.issues:
            lines.append(f"  - {issue}")
    return "\n".join(lines) + "\n"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Audit repo-local Git author identity before public proof pushes.")
    parser.add_argument("--root", default=str(Path.cwd().parent), help="Parent folder or repo to audit.")
    parser.add_argument("--expected-name", default=EXPECTED_NAME)
    parser.add_argument("--expected-email", default=EXPECTED_EMAIL)
    parser.add_argument("--format", choices=["markdown", "json"], default="markdown")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    report = audit_root(Path(args.root), args.expected_name, args.expected_email)
    if args.format == "json":
        print(json.dumps(asdict(report), indent=2))
    else:
        print(render_markdown(report), end="")
    return 1 if report.issues else 0


if __name__ == "__main__":
    raise SystemExit(main())
